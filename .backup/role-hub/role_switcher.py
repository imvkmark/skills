#!/usr/bin/env python3
"""
AI智能团队角色切换器
自动识别用户输入中的角色标识符,加载对应的角色定义
"""

import json
import os
import sys
import re
from pathlib import Path


def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_role_file(role_code, config):
    """查找角色定义文件,优先查找项目级,再查找全局"""
    role_info = config['roles'].get(role_code)
    if not role_info:
        return None

    role_filename = role_info['file']

    # 按优先级查找角色文件
    for path_pattern in config['rolePaths']:
        # 扩展 ~ 为用户目录
        path = Path(path_pattern.replace('~', str(Path.home())))
        role_file = path / role_filename

        if role_file.exists():
            return role_file

    return None


def find_workflow_file(workflow_name, config):
    """查找流程定义文件"""
    workflow_filename = config['workflows'].get(workflow_name)
    if not workflow_filename:
        return None

    # 按优先级查找流程文件
    for path_pattern in config['workflowPaths']:
        path = Path(path_pattern.replace('~', str(Path.home())))
        workflow_file = path / workflow_filename

        if workflow_file.exists():
            return workflow_file

    return None


def detect_role(user_input):
    """检测用户输入中的角色标识符"""
    # 匹配 @角色代号 模式
    pattern = r'@(PM|UI|ARCH|DEV|QA)\b'
    match = re.search(pattern, user_input, re.IGNORECASE)

    if match:
        return match.group(1).upper()

    return None


def detect_workflow(user_input):
    """检测用户输入中的流程关键词"""
    workflows = {
        '需求评审': ['需求评审', '评审需求', 'requirement review'],
        '技术设计': ['技术设计', '设计技术方案', 'technical design'],
        '发布流程': ['发布流程', '版本发布', 'release process']
    }

    user_input_lower = user_input.lower()
    for workflow_name, keywords in workflows.items():
        if any(keyword in user_input_lower for keyword in keywords):
            return workflow_name

    return None


def load_file_content(file_path):
    """读取文件内容"""
    if not file_path or not file_path.exists():
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "缺少用户输入参数"
        }, ensure_ascii=False))
        return

    user_input = sys.argv[1]
    config = load_config()

    result = {
        "success": False,
        "role": None,
        "workflow": None,
        "content": None
    }

    # 优先检测角色
    role_code = detect_role(user_input)
    if role_code:
        role_file = find_role_file(role_code, config)
        if role_file:
            content = load_file_content(role_file)
            if content:
                result["success"] = True
                result["role"] = {
                    "code": role_code,
                    "name": config['roles'][role_code]['name'],
                    "file": str(role_file)
                }
                result["content"] = content
                result["message"] = f"已激活 {config['roles'][role_code]['name']} 角色"

    # 检测流程
    workflow_name = detect_workflow(user_input)
    if workflow_name:
        workflow_file = find_workflow_file(workflow_name, config)
        if workflow_file:
            content = load_file_content(workflow_file)
            if content:
                result["success"] = True
                result["workflow"] = {
                    "name": workflow_name,
                    "file": str(workflow_file)
                }
                # 如果同时有角色和流程,追加流程内容
                if result["content"]:
                    result["content"] += f"\n\n---\n\n# 协作流程: {workflow_name}\n\n{content}"
                else:
                    result["content"] = content
                result["message"] = f"已加载 {workflow_name} 流程"

    # 如果没有检测到任何内容
    if not result["success"]:
        result["error"] = "未检测到有效的角色标识符或流程关键词"
        result["hint"] = "请使用 @PM、@UI、@ARCH、@DEV、@QA 调用角色,或提及'需求评审'、'技术设计'、'发布流程'等关键词"

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
