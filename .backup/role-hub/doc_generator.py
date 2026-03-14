#!/usr/bin/env python3
"""
文档生成器
根据角色和模板生成标准化交付文档
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import shutil


class DocGenerator:
    """文档生成器"""

    def __init__(self):
        """初始化文档生成器"""
        self.skill_dir = Path(__file__).parent
        self.templates_dir = self.skill_dir / 'templates'

        # 角色到模板的映射
        self.role_templates = {
            'PM': 'pm-prd.md',
            'UI': 'ui-design-spec.md',
            'ARCH': 'arch-design.md',
            'DEV': 'dev-checklist.md',
            'QA': 'qa-test-report.md'
        }

    def generate(self, role, task_name=None, output_dir=None):
        """生成文档

        Args:
            role: 角色代号 (PM/UI/ARCH/DEV/QA)
            task_name: 任务名称 (可选,用于填充模板变量)
            output_dir: 输出目录 (可选,默认为当前目录的.role-hub/)

        Returns:
            生成的文档路径
        """
        # 获取模板
        template_name = self.role_templates.get(role)
        if not template_name:
            raise ValueError(f'未知角色: {role}')

        template_file = self.templates_dir / template_name
        if not template_file.exists():
            raise FileNotFoundError(f'模板文件不存在: {template_file}')

        # 读取模板内容
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换模板变量
        if task_name:
            content = self._fill_template(content, task_name)

        # 确定输出路径 - 简化为直接保存在 .role-hub/ 下
        if output_dir is None:
            output_dir = Path.cwd() / '.role-hub'
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名 - 简化为 角色-时间戳.md
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_file = output_dir / f'{role.lower()}-{timestamp}.md'

        # 保存文档
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_file)

    def _fill_template(self, content, task_name):
        """填充模板变量

        Args:
            content: 模板内容
            task_name: 任务名称

        Returns:
            填充后的内容
        """
        today = datetime.now().strftime('%Y-%m-%d')

        # 替换常见占位符
        replacements = {
            '[功能名称]': task_name,
            '[产品/功能名称]': task_name,
            '[YYYY-MM-DD]': today,
        }

        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        return content

    def list_templates(self):
        """列出所有可用模板

        Returns:
            模板列表
        """
        templates = []
        for role, template_name in self.role_templates.items():
            template_file = self.templates_dir / template_name
            templates.append({
                'role': role,
                'template': template_name,
                'exists': template_file.exists(),
                'path': str(template_file)
            })

        return templates

    def copy_template_to_project(self, role, project_dir):
        """复制模板到项目目录供用户自定义

        Args:
            role: 角色代号
            project_dir: 项目目录

        Returns:
            复制后的模板路径
        """
        template_name = self.role_templates.get(role)
        if not template_name:
            raise ValueError(f'未知角色: {role}')

        source = self.templates_dir / template_name
        dest_dir = Path(project_dir) / '.role-hub' / 'templates'
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest = dest_dir / template_name
        shutil.copy2(source, dest)

        return str(dest)


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': '缺少命令参数',
            'usage': 'python doc_generator.py <command> [args...]'
        }, ensure_ascii=False))
        return

    command = sys.argv[1]
    generator = DocGenerator()

    if command == 'generate':
        # 生成文档: generate <role> [task_name] [output_dir]
        if len(sys.argv) < 3:
            print(json.dumps({'error': '缺少角色参数'}, ensure_ascii=False))
            return

        role = sys.argv[2].upper()
        task_name = sys.argv[3] if len(sys.argv) > 3 else None
        output_dir = sys.argv[4] if len(sys.argv) > 4 else None

        try:
            output_file = generator.generate(role, task_name, output_dir)
            print(json.dumps({
                'success': True,
                'message': '文档已生成',
                'file': output_file,
                'role': role
            }, ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False))

    elif command == 'list':
        # 列出模板: list
        templates = generator.list_templates()
        print(json.dumps({
            'success': True,
            'templates': templates
        }, ensure_ascii=False, indent=2))

    elif command == 'copy':
        # 复制模板到项目: copy <role> [project_dir]
        if len(sys.argv) < 3:
            print(json.dumps({'error': '缺少角色参数'}, ensure_ascii=False))
            return

        role = sys.argv[2].upper()
        project_dir = sys.argv[3] if len(sys.argv) > 3 else '.'

        try:
            dest_file = generator.copy_template_to_project(role, project_dir)
            print(json.dumps({
                'success': True,
                'message': '模板已复制到项目目录',
                'file': dest_file
            }, ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False))

    else:
        print(json.dumps({
            'error': f'未知命令: {command}',
            'available_commands': ['generate', 'list', 'copy']
        }, ensure_ascii=False))


if __name__ == '__main__':
    main()
