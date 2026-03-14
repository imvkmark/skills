#!/usr/bin/env python3
"""
任务上下文管理器
用于保存、恢复和管理团队协作的任务上下文,防止任务中断
"""

import json
from pathlib import Path
from datetime import datetime


class ContextManager:
    """任务上下文管理器"""

    def __init__(self, project_root=None):
        """初始化上下文管理器

        Args:
            project_root: 项目根目录,如果不指定则使用当前目录
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.role_hub_dir = self.project_root / '.role-hub'
        self.context_file = self.role_hub_dir / 'context.json'

        # 确保目录存在
        self.role_hub_dir.mkdir(parents=True, exist_ok=True)

    def save_context(self, role, data):
        """保存任务上下文

        Args:
            role: 当前角色 (PM/UI/ARCH/DEV/QA)
            data: 上下文数据 (字典格式)
        """
        # 加载现有上下文
        all_context = self._load_all_context()

        # 更新上下文
        all_context['current_role'] = role
        all_context['last_update'] = datetime.now().isoformat()
        all_context['data'] = data

        # 保存到文件
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(all_context, f, ensure_ascii=False, indent=2)

        return str(self.context_file)

    def load_context(self):
        """加载当前任务上下文

        Returns:
            上下文数据字典,如果不存在则返回空字典
        """
        return self._load_all_context()

    def _load_all_context(self):
        """加载完整上下文"""
        if not self.context_file.exists():
            return {
                'current_role': None,
                'last_update': None,
                'data': {}
            }

        with open(self.context_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def clear_context(self):
        """清除上下文"""
        if self.context_file.exists():
            self.context_file.unlink()
        return True

    def list_artifacts(self, role=None):
        """列出所有产出物

        Args:
            role: 角色过滤 (可选)

        Returns:
            产出物文件列表
        """
        artifacts = []

        # 扫描 .role-hub/ 目录下的所有 markdown 文件
        for md_file in self.role_hub_dir.glob('*.md'):
            file_info = {
                'file': md_file.name,
                'path': str(md_file),
                'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
            }

            # 从文件名推断角色
            filename_lower = md_file.name.lower()
            if filename_lower.startswith('pm-'):
                file_info['role'] = 'PM'
            elif filename_lower.startswith('ui-'):
                file_info['role'] = 'UI'
            elif filename_lower.startswith('arch-'):
                file_info['role'] = 'ARCH'
            elif filename_lower.startswith('dev-'):
                file_info['role'] = 'DEV'
            elif filename_lower.startswith('qa-'):
                file_info['role'] = 'QA'
            else:
                file_info['role'] = 'UNKNOWN'

            artifacts.append(file_info)

        # 按修改时间倒序排列
        artifacts.sort(key=lambda x: x['modified'], reverse=True)

        # 角色过滤
        if role:
            artifacts = [a for a in artifacts if a['role'] == role]

        return artifacts

    def check_prerequisites(self, role):
        """检查角色执行的前置条件

        Args:
            role: 当前角色

        Returns:
            检查结果 {'passed': bool, 'missing': [], 'warnings': []}
        """
        result = {
            'passed': True,
            'missing': [],
            'warnings': []
        }

        # 定义角色依赖关系
        prerequisites = {
            'UI': ['PM'],  # UI设计需要先有PRD
            'ARCH': ['PM'],  # 架构设计需要先有PRD
            'DEV': ['ARCH'],  # 开发需要先有技术设计,最好也有UI设计
            'QA': ['DEV']  # 测试需要先有开发完成
        }

        # 检查前置角色的产出物
        required_roles = prerequisites.get(role, [])
        artifacts = self.list_artifacts()

        completed_roles = set(a['role'] for a in artifacts)

        for required_role in required_roles:
            if required_role not in completed_roles:
                result['passed'] = False
                result['missing'].append(required_role)

        # 特殊检查:开发阶段建议有UI设计
        if role == 'DEV' and 'UI' not in completed_roles:
            result['warnings'].append('建议等待UI设计完成后再开始开发')

        return result


def main():
    """命令行接口"""
    import sys

    if len(sys.argv) < 2:
        print(json.dumps({
            'error': '缺少命令参数',
            'usage': 'python context_manager.py <command> [args...]'
        }, ensure_ascii=False))
        return

    command = sys.argv[1]
    manager = ContextManager()

    if command == 'save':
        # 保存上下文: save <role> <json_data>
        if len(sys.argv) < 4:
            print(json.dumps({'error': '参数不足'}, ensure_ascii=False))
            return

        role = sys.argv[2]
        data = json.loads(sys.argv[3])

        file_path = manager.save_context(role, data)
        print(json.dumps({
            'success': True,
            'message': '上下文已保存',
            'file': file_path
        }, ensure_ascii=False))

    elif command == 'load':
        # 加载上下文: load
        context = manager.load_context()
        print(json.dumps({
            'success': True,
            'context': context
        }, ensure_ascii=False, indent=2))

    elif command == 'clear':
        # 清除上下文: clear
        manager.clear_context()
        print(json.dumps({
            'success': True,
            'message': '上下文已清除'
        }, ensure_ascii=False))

    elif command == 'check':
        # 检查前置条件: check <role>
        if len(sys.argv) < 3:
            print(json.dumps({'error': '缺少角色参数'}, ensure_ascii=False))
            return

        role = sys.argv[2]
        result = manager.check_prerequisites(role)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == 'list':
        # 列出产出物: list [role]
        role = sys.argv[2] if len(sys.argv) > 2 else None
        artifacts = manager.list_artifacts(role)
        print(json.dumps({
            'success': True,
            'artifacts': artifacts,
            'count': len(artifacts)
        }, ensure_ascii=False, indent=2))

    else:
        print(json.dumps({
            'error': f'未知命令: {command}',
            'available_commands': ['save', 'load', 'clear', 'check', 'list']
        }, ensure_ascii=False))


if __name__ == '__main__':
    main()
