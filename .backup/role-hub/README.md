# Role-Hub - AI智能团队角色切换系统

> 让AI扮演不同角色,实现优雅的团队协作

## ✨ 特性

- 🎭 **多角色切换**: 支持PM、UI、架构师、开发、QA五大角色
- 📋 **文档交接**: 标准化文档模板确保角色间顺畅对接
- ✅ **任务清单**: 开发角色自动管理任务清单,实时跟踪进度
- 🔍 **前置检查**: 自动检查角色执行的前置条件,避免返工
- 💾 **断点续做**: 任务上下文持久化,防止任务中断
- 📁 **简化目录**: 所有文档直接保存在 `.role-hub/` 目录下

## 🚀 快速开始

### 基本使用

在对话中使用 `@角色代号` 激活对应角色:

```
@PM 我们想做一个用户积分系统
→ 激活产品经理,梳理需求并产出PRD
→ 保存到: .role-hub/pm-20231217-143025.md

@ARCH 基于上面的PRD设计技术方案
→ 激活架构师,设计系统架构
→ 保存到: .role-hub/arch-20231217-143530.md

@DEV 实现用户积分系统
→ 激活开发工程师,编写代码并管理任务清单
→ 保存到: .role-hub/dev-20231217-144020.md

@QA 测试用户积分系统
→ 激活QA工程师,执行测试并产出报告
→ 保存到: .role-hub/qa-20231217-150015.md
```

### 角色列表

| 角色代号 | 角色名称 | 核心职责 | 文件名格式 |
|---------|---------|---------|-----------|
| @PM | 产品经理 | 需求分析,产出PRD | `pm-*.md` |
| @UI | UI设计师 | 界面设计,产出设计稿 | `ui-*.md` |
| @ARCH | 架构师 | 技术方案,产出设计文档 | `arch-*.md` |
| @DEV | 开发工程师 | 代码实现,管理任务清单 | `dev-*.md` |
| @QA | 质量工程师 | 质量测试,产出测试报告 | `qa-*.md` |

## 📖 文档

- [使用指南](./USAGE_GUIDE.md) - 详细的使用说明和最佳实践
- [技能说明](./SKILL.md) - 技能配置和执行方式

## 🎯 核心功能

### 1. 标准化文档交接

每个角色完成任务后,会产出标准化的交接文档:

```
PM  → pm-YYYYMMDD-HHMMSS.md (PRD文档)
UI  → ui-YYYYMMDD-HHMMSS.md (UI设计文档)
ARCH → arch-YYYYMMDD-HHMMSS.md (技术设计文档)
DEV → dev-YYYYMMDD-HHMMSS.md (开发清单)
QA  → qa-YYYYMMDD-HHMMSS.md (测试报告)
```

所有文档直接保存在项目的 `.role-hub/` 目录,文件名包含时间戳,易于追踪。

### 2. 前置条件自动检查

切换角色时自动检查前置条件:

```
@UI 设计界面
↓ 检查: 是否有PM文档? ✅

@DEV 开始开发
↓ 检查: 是否有ARCH文档? ✅
↓ 提示: 建议等待UI设计完成 ⚠️

@QA 开始测试
↓ 检查: 是否有DEV文档? ✅
```

### 3. 任务上下文持久化

支持保存和恢复任务状态:

```bash
# 保存当前任务状态
python3 ~/.claude/skills/role-hub/context_manager.py save DEV '{"progress": "50%"}'

# 恢复任务
python3 ~/.claude/skills/role-hub/context_manager.py load
```

## 🔧 工具命令

### 文档生成

```bash
# 生成文档模板
python3 ~/.claude/skills/role-hub/doc_generator.py generate PM
python3 ~/.claude/skills/role-hub/doc_generator.py generate DEV

# 带任务名称(可选)
python3 ~/.claude/skills/role-hub/doc_generator.py generate PM "用户积分系统"
```

### 上下文管理

```bash
# 列出所有产出物
python3 ~/.claude/skills/role-hub/context_manager.py list

# 检查前置条件
python3 ~/.claude/skills/role-hub/context_manager.py check DEV

# 保存/加载上下文
python3 ~/.claude/skills/role-hub/context_manager.py save DEV '{"progress": "50%"}'
python3 ~/.claude/skills/role-hub/context_manager.py load
```

## 📂 项目结构

```
~/.claude/skills/role-hub/   # 全局技能目录
├── SKILL.md
├── README.md
├── USAGE_GUIDE.md
├── role_switcher.py
├── doc_generator.py
├── context_manager.py
├── roles/                # 角色定义
└── templates/            # 文档模板

<项目目录>/.role-hub/        # 项目级产出物
├── pm-20231217-143025.md
├── arch-20231217-143530.md
├── ui-20231217-144000.md
├── dev-20231217-144020.md
├── qa-20231217-150015.md
├── context.json
└── templates/            # 自定义模板(可选)
```

## 🌟 协作流程示例

```
1. @PM 梳理需求
   ↓ 产出: .role-hub/pm-*.md

2. @UI 设计界面 (基于PRD)
   ↓ 产出: .role-hub/ui-*.md

3. @ARCH 设计架构 (基于PRD)
   ↓ 产出: .role-hub/arch-*.md

4. @DEV 实现功能 (基于ARCH+UI)
   ↓ 产出: .role-hub/dev-*.md

5. @QA 测试验收 (基于DEV)
   ↓ 产出: .role-hub/qa-*.md

6. 上线发布
```

## 💡 最佳实践

1. **始终从PM开始** - 确保需求清晰
2. **使用标准模板** - 确保交接信息完整
3. **实时更新进度** - 开发阶段及时更新清单
4. **检查前置条件** - 避免因缺失文档而返工
5. **文档按时间追踪** - 文件名包含时间戳,易于查找最新版本

## 🤝 为什么选择 Role-Hub?

### 传统协作的痛点

- ❌ 角色职责不清晰
- ❌ 文档格式不统一
- ❌ 任务交接不顺畅
- ❌ 进度不透明
- ❌ 文档目录复杂难找

### Role-Hub 的解决方案

- ✅ 角色职责明确,专业分工
- ✅ 标准化文档模板
- ✅ 清晰的交接清单
- ✅ 简化的目录结构 (所有文档直接在 `.role-hub/`)
- ✅ 时间戳命名,易于追踪

---

**Happy Coding with Role-Hub!** 🎉
