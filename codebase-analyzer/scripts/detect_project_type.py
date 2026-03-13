#!/usr/bin/env python3
"""
项目类型检测脚本
根据特征文件自动识别项目类型和架构模式
"""

import os
import json
from pathlib import Path
from typing import Dict, Tuple, Optional

class ProjectTypeDetector:
    """项目类型检测器"""

    # 项目类型特征文件映射
    PROJECT_TYPE_MARKERS = {
        'Java': ['pom.xml', 'build.gradle', 'settings.gradle'],
        'Python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
        'Go': ['go.mod', 'go.sum'],
        'Node.js': ['package.json', 'package-lock.json', 'yarn.lock'],
        'PHP': ['composer.json', 'composer.lock'],
        'Rust': ['Cargo.toml', 'Cargo.lock'],
        '.NET': ['*.csproj', '*.sln'],
    }

    # 框架特征
    FRAMEWORK_MARKERS = {
        'Java': {
            'Spring Boot': ['spring-boot', 'org.springframework.boot'],
            'Spring Cloud': ['spring-cloud'],
            'Quarkus': ['quarkus'],
        },
        'Python': {
            'Django': ['django'],
            'Flask': ['flask'],
            'FastAPI': ['fastapi'],
            'Celery': ['celery'],
        },
        'Go': {
            'Gin': ['github.com/gin-gonic/gin'],
            'Echo': ['github.com/labstack/echo'],
            'gRPC': ['google.golang.org/grpc'],
        },
        'Node.js': {
            'Express': ['express'],
            'NestJS': ['@nestjs/core'],
            'Fastify': ['fastify'],
        },
    }

    def __init__(self, project_root: str = '.'):
        self.project_root = Path(project_root)

    def detect_project_type(self) -> Optional[str]:
        """检测项目类型"""
        for project_type, markers in self.PROJECT_TYPE_MARKERS.items():
            for marker in markers:
                if self._file_exists(marker):
                    return project_type
        return None

    def detect_architecture(self) -> str:
        """检测架构模式"""
        # 检查是否为微服务架构
        if self._is_microservices():
            return 'microservices'

        # 检查是否为 Monorepo
        if self._is_monorepo():
            return 'monorepo'

        # 检查是否为 SDK/库
        if self._is_sdk():
            return 'sdk'

        # 默认为单体架构
        return 'monolith'

    def detect_frameworks(self) -> list:
        """检测使用的框架"""
        project_type = self.detect_project_type()
        if not project_type:
            return []

        frameworks = []
        framework_markers = self.FRAMEWORK_MARKERS.get(project_type, {})

        for framework, markers in framework_markers.items():
            if self._check_dependencies(markers):
                frameworks.append(framework)

        return frameworks

    def _file_exists(self, pattern: str) -> bool:
        """检查文件是否存在"""
        if '*' in pattern:
            # 处理通配符
            import glob
            matches = glob.glob(str(self.project_root / pattern))
            return len(matches) > 0
        return (self.project_root / pattern).exists()

    def _check_dependencies(self, markers: list) -> bool:
        """检查依赖是否存在"""
        project_type = self.detect_project_type()

        if project_type == 'Java':
            return self._check_java_dependencies(markers)
        elif project_type == 'Python':
            return self._check_python_dependencies(markers)
        elif project_type == 'Go':
            return self._check_go_dependencies(markers)
        elif project_type == 'Node.js':
            return self._check_nodejs_dependencies(markers)

        return False

    def _check_java_dependencies(self, markers: list) -> bool:
        """检查 Java 依赖"""
        pom_file = self.project_root / 'pom.xml'
        if pom_file.exists():
            content = pom_file.read_text()
            return any(marker in content for marker in markers)
        return False

    def _check_python_dependencies(self, markers: list) -> bool:
        """检查 Python 依赖"""
        req_file = self.project_root / 'requirements.txt'
        if req_file.exists():
            content = req_file.read_text()
            return any(marker in content for marker in markers)
        return False

    def _check_go_dependencies(self, markers: list) -> bool:
        """检查 Go 依赖"""
        go_mod = self.project_root / 'go.mod'
        if go_mod.exists():
            content = go_mod.read_text()
            return any(marker in content for marker in markers)
        return False

    def _check_nodejs_dependencies(self, markers: list) -> bool:
        """检查 Node.js 依赖"""
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any(marker in deps for marker in markers)
            except:
                return False
        return False

    def _is_microservices(self) -> bool:
        """检查是否为微服务架构"""
        # 检查是否有多个服务目录
        service_dirs = ['services', 'microservices', 'apps']
        for service_dir in service_dirs:
            path = self.project_root / service_dir
            if path.exists() and path.is_dir():
                # 检查是否有多个子目录，每个都有依赖文件
                subdirs = [d for d in path.iterdir() if d.is_dir()]
                if len(subdirs) > 1:
                    count = 0
                    for subdir in subdirs:
                        if self._has_dependency_file(subdir):
                            count += 1
                    if count > 1:
                        return True
        return False

    def _is_monorepo(self) -> bool:
        """检查是否为 Monorepo"""
        monorepo_markers = ['packages', 'apps', 'projects']
        for marker in monorepo_markers:
            path = self.project_root / marker
            if path.exists() and path.is_dir():
                subdirs = [d for d in path.iterdir() if d.is_dir()]
                if len(subdirs) > 1:
                    return True
        return False

    def _is_sdk(self) -> bool:
        """检查是否为 SDK/库"""
        # SDK 通常没有 main 入口，但有 src 或 lib 目录
        has_src = (self.project_root / 'src').exists()
        has_lib = (self.project_root / 'lib').exists()

        # 检查是否有 main 入口
        has_main = False
        for main_file in ['main.py', 'main.go', 'index.js', 'Main.java']:
            if (self.project_root / main_file).exists():
                has_main = True
                break

        return (has_src or has_lib) and not has_main

    def _has_dependency_file(self, directory: Path) -> bool:
        """检查目录是否有依赖文件"""
        dependency_files = [
            'pom.xml', 'build.gradle',
            'requirements.txt', 'setup.py', 'pyproject.toml',
            'go.mod',
            'package.json',
            'composer.json',
            'Cargo.toml'
        ]
        return any((directory / f).exists() for f in dependency_files)

    def get_analysis_template(self) -> str:
        """获取推荐的分析模板"""
        architecture = self.detect_architecture()

        templates = {
            'monolith': 'references/phase-templates.md#单体架构支持',
            'microservices': 'references/phase-templates.md#微服务架构支持',
            'sdk': 'references/phase-templates.md#sdk--库支持',
            'monorepo': 'references/phase-templates.md#monorepo-支持',
        }

        return templates.get(architecture, 'references/phase-templates.md')

    def get_language_guide(self) -> Optional[str]:
        """获取语言特定的分析指南"""
        project_type = self.detect_project_type()

        guides = {
            'Java': 'references/project-types/java.md',
            'Python': 'references/project-types/python.md',
            'Go': 'references/project-types/go.md',
            'Node.js': 'references/project-types/nodejs.md',
            'PHP': 'references/project-types/php.md',
            'Rust': 'references/project-types/rust.md',
        }

        return guides.get(project_type)

    def generate_report(self) -> Dict:
        """生成检测报告"""
        return {
            'project_type': self.detect_project_type(),
            'architecture': self.detect_architecture(),
            'frameworks': self.detect_frameworks(),
            'analysis_template': self.get_analysis_template(),
            'language_guide': self.get_language_guide(),
        }


if __name__ == '__main__':
    import sys

    project_root = sys.argv[1] if len(sys.argv) > 1 else '.'
    detector = ProjectTypeDetector(project_root)
    report = detector.generate_report()

    print(json.dumps(report, indent=2, ensure_ascii=False))
