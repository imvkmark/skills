#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多语言学习计划生成模板工具
用于生成标准化的 plan-learning.md 和 plan-progress.md 文件
"""

import os
import uuid
from datetime import datetime
import yaml


# 加载语言配置
def load_language_config(language):
    """加载指定语言的配置"""
    config_path = os.path.join(os.path.dirname(__file__), "../language-config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for lang_config in config["supported_languages"]:
        if lang_config["id"] == language:
            return lang_config
    raise ValueError(f"Unsupported language: {language}")


def generate_plan_id(language="general"):
    """生成唯一的计划ID"""
    return f"{language}-plan-{uuid.uuid4().hex[:8]}"


def generate_learning_plan(language, domain, level, total_phases=3):
    """
    生成学习计划主体内容
    :param language: 目标编程语言（java/python/go/php等）
    :param domain: 学习领域（基础/集合/多线程/Web开发等）
    :param level: 学习者水平（入门/中级/高级）
    :param total_phases: 总阶段数
    """
    lang_config = load_language_config(language)
    lang_name = lang_config["name"]
    lang_version = lang_config["version"]

    plan_id = generate_plan_id(language)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 学习计划头部
    content = f"""# {lang_name} {domain} 学习计划
> Plan ID: {plan_id}
> 生成时间: {current_time}
> 目标语言: {lang_name} {lang_version}
> 学习者水平: {level}
> 预计总学习时间: {total_phases * 4} 小时

## 计划概述
本计划针对 {level} 水平的学习者，系统覆盖 {lang_name} {domain} 领域的核心知识点，通过分阶段学习和配套练习，帮助学习者全面掌握相关技能。

## 学习目标
1. 理解 {lang_name} {domain} 的核心概念和原理
2. 掌握常见使用场景和最佳实践
3. 能够编写高质量的相关代码
4. 应对相关面试题和实际开发问题

"""
    # 读取对应语言的阶段模板
    phase_templates_path = os.path.join(
        os.path.dirname(__file__),
        f"../language-plugins/{language}/references/phase-templates.md",
    )
    if os.path.exists(phase_templates_path):
        with open(phase_templates_path, "r", encoding="utf-8") as f:
            phase_templates = f.read()
        content += "## 参考知识体系\n"
        content += "详细的知识点划分请参考对应语言的阶段模板\n\n"

    # 文档规范部分
    content += f"""## 文档编写规范
所有知识点文档必须遵循以下要求：
1. 结构符合 language-plugins/{language}/references/document-structure.md 中的规范
2. 包含概念讲解、代码示例、最佳实践、常见坑点
3. 代码示例可直接运行，注释清晰
4. 配套 {lang_config["test_framework"]} 单元测试，覆盖核心场景

## 输出要求
- 文档保存到 docs/ 目录，文件名：[知识点名称].md
- 代码示例保存到 {lang_config["directory_structure"]["sources"]} 目录
- 测试用例保存到 {lang_config["directory_structure"]["tests"]} 目录
- 所有文件命名遵循 {lang_config["style_guide"]} 规范
"""
    return content, plan_id


def generate_progress_plan(plan_id, language, total_phases=3):
    """生成进度追踪文件内容"""
    lang_config = load_language_config(language)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# 学习进度追踪
> Plan ID: {plan_id}
> 目标语言: {lang_config["name"]}
> 最后更新: {current_time}

## Metadata
- Plan ID: {plan_id}
- Target Language: {language}
- Last updated: {current_time}
- Status: 待确认
- Current phase: 1
- Last completed task: None
- Auto-execution: disabled
- Parallel agents: 3
- Adjustment requests: []

## 进度总览
| 总阶段 | 已完成 | 完成度 | 预计剩余时间 |
|--------|--------|--------|--------------|
| {total_phases} | 0 | 0% | {total_phases * 2} 小时 |

## 详细进度表
| 阶段 | 模块 | 章节 | 知识点 | 子知识点 | 状态 | 完成度 | 负责人 | 开始时间 | 完成时间 | 备注 |
|------|------|------|--------|----------|------|--------|--------|----------|----------|------|
| 第1阶段 | 待分配 | 待分配 | 待分配 | - | 待执行 | 0% | - | - | - | |
| 第1阶段 | 待分配 | 待分配 | 待分配 | - | 待执行 | 0% | - | - | - | |
| 第1阶段 | 待分配 | 待分配 | 待分配 | - | 待执行 | 0% | - | - | - | |

## 阶段状态说明
- 待确认：计划已生成，等待用户确认
- 待执行：尚未开始
- 进行中：正在生成内容
- 待审核：内容生成完成，等待质量检查
- 已完成：审核通过，内容可用
- 已失败：生成失败，需要重试
"""
    return content


def create_plan_files(output_dir, language, domain, level):
    """创建计划文件"""
    # 确保目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 生成学习计划
    learning_content, plan_id = generate_learning_plan(language, domain, level)
    learning_file = os.path.join(output_dir, "plan-learning.md")
    with open(learning_file, "w", encoding="utf-8") as f:
        f.write(learning_content)

    # 生成进度计划
    progress_content = generate_progress_plan(plan_id, language)
    progress_file = os.path.join(output_dir, "plan-progress.md")
    with open(progress_file, "w", encoding="utf-8") as f:
        f.write(progress_content)

    print(f"学习计划已生成：")
    print(f"- 目标语言: {language}")
    print(f"- 计划文件：{learning_file}")
    print(f"- 进度文件：{progress_file}")
    print(f"- Plan ID：{plan_id}")

    return plan_id


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="生成多语言学习计划")
    parser.add_argument(
        "--language", required=True, help="目标编程语言：java/python/go/php"
    )
    parser.add_argument(
        "--domain", required=True, help="学习领域：基础/集合/多线程/Web开发等"
    )
    parser.add_argument(
        "--level", default="中级", choices=["入门", "中级", "高级"], help="学习者水平"
    )
    parser.add_argument("--output-dir", default="./learning", help="输出目录")

    args = parser.parse_args()
    create_plan_files(args.output_dir, args.language, args.domain, args.level)
