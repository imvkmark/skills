# Role-Hub 使用指南 (简化版)

## 📖 概述

Role-Hub 是一个AI智能团队角色切换系统,支持团队协作、文档交接和任务状态管理。

## 🎯 核心功能

### 1️⃣ 角色切换
- `@PM` - 产品经理
- `@UI` - UI设计师
- `@ARCH` - 架构师
- `@DEV` - 开发工程师
- `@QA` - 质量工程师

### 2️⃣ 文档交接
每个角色完成后自动产出标准化文档,保存在项目的 `.role-hub/` 目录。

### 3️⃣ 前置条件检查
角色切换时自动检查前置条件,确保协作顺畅。

---

## 🚀 快速开始

### 完整流程示例

```
用户: @PM 我们想做一个用户积分系统
→ PM生成PRD文档,保存到 .role-hub/pm-20231217-143025.md

用户: @ARCH 基于PRD设计技术方案
→ 自动检查PRD是否存在
→ ARCH生成技术设计文档,保存到 .role-hub/arch-20231217-143530.md

用户: @DEV 实现功能
→ 自动检查技术设计文档是否存在
→ DEV生成开发清单,保存到 .role-hub/dev-20231217-144020.md

用户: @QA 测试功能
→ 自动检查开发交付文档是否存在
→ QA生成测试报告,保存到 .role-hub/qa-20231217-150015.md
```

---

## 📂 项目目录结构

```
<项目根目录>/
└── .role-hub/
    ├── pm-20231217-143025.md       # PRD文档
    ├── arch-20231217-143530.md     # 技术设计文档
    ├── ui-20231217-144000.md       # UI设计文档
    ├── dev-20231217-144020.md      # 开发清单
    ├── qa-20231217-150015.md       # 测试报告
    ├── context.json                # 任务上下文
    └── templates/                  # 自定义模板(可选)
```

---

## 🛠️ 工具命令

### 文档生成器

```bash
# 生成文档模板
python3 ~/.claude/skills/role-hub/doc_generator.py generate <角色>

# 示例
python3 ~/.claude/skills/role-hub/doc_generator.py generate PM
python3 ~/.claude/skills/role-hub/doc_generator.py generate DEV

# 带任务名称(可选,用于填充模板变量)
python3 ~/.claude/skills/role-hub/doc_generator.py generate PM "用户积分系统"

# 列出所有模板
python3 ~/.claude/skills/role-hub/doc_generator.py list

# 复制模板到项目供自定义
python3 ~/.claude/skills/role-hub/doc_generator.py copy DEV .
```

### 上下文管理器

```bash
# 保存上下文
python3 ~/.claude/skills/role-hub/context_manager.py save DEV '{"progress": "50%"}'

# 加载上下文
python3 ~/.claude/skills/role-hub/context_manager.py load

# 清除上下文
python3 ~/.claude/skills/role-hub/context_manager.py clear

# 检查前置条件
python3 ~/.claude/skills/role-hub/context_manager.py check DEV

# 列出所有产出物
python3 ~/.claude/skills/role-hub/context_manager.py list

# 列出特定角色的产出物
python3 ~/.claude/skills/role-hub/context_manager.py list PM
```

---

## 🔄 协作流程

```
PM (需求分析)
  ↓ 输出: .role-hub/pm-*.md
  ├─→ UI (界面设计)
  │     ↓ 输出: .role-hub/ui-*.md
  │
  └─→ ARCH (架构设计)
        ↓ 输出: .role-hub/arch-*.md
        ↓
      DEV (代码实现)
        ↓ 输出: .role-hub/dev-*.md
        ↓
       QA (质量测试)
        ↓ 输出: .role-hub/qa-*.md
```

### 前置条件依赖

| 角色 | 必须有 | 建议有 |
|------|-------|--------|
| PM | - | - |
| UI | PM文档 | - |
| ARCH | PM文档 | - |
| DEV | ARCH文档 | UI文档 |
| QA | DEV文档 | PM/ARCH/UI文档 |

---

## 📋 各角色产出物

| 角色 | 文件名格式 | 内容 |
|------|-----------|------|
| PM | `pm-YYYYMMDD-HHMMSS.md` | PRD文档 |
| UI | `ui-YYYYMMDD-HHMMSS.md` | UI设计文档 |
| ARCH | `arch-YYYYMMDD-HHMMSS.md` | 技术设计文档 |
| DEV | `dev-YYYYMMDD-HHMMSS.md` | 开发清单 |
| QA | `qa-YYYYMMDD-HHMMSS.md` | 测试报告 |

---

## 💡 最佳实践

1. **始终从PM开始** - 确保需求清晰
2. **使用标准模板** - 确保交接信息完整
3. **实时更新进度** - 开发阶段及时更新清单
4. **检查前置条件** - 避免因缺失文档而返工
5. **明确交接清单** - 每个文档都列出后续角色需确认的事项

---

## ❓ 常见问题

### Q: 如何查看所有产出物?
```bash
python3 ~/.claude/skills/role-hub/context_manager.py list
```

### Q: 如何恢复中断的任务?
```bash
python3 ~/.claude/skills/role-hub/context_manager.py load
```

### Q: 如何检查是否满足前置条件?
```bash
python3 ~/.claude/skills/role-hub/context_manager.py check DEV
```

### Q: 产出的文档在哪里?
所有产出物默认保存在项目根目录的 `.role-hub/` 目录下。

### Q: 文件名很长,如何找到最新的?
文件名包含时间戳,按修改时间排序即可。或使用 `context_manager.py list` 命令查看。

### Q: 可以自定义模板吗?
可以,使用 `doc_generator.py copy` 命令复制模板到项目目录自定义。

---

## 🎉 总结

Role-Hub 通过以下机制确保团队优雅协作:

1. ✅ **简化目录** - 所有文档直接保存在 `.role-hub/` 下
2. ✅ **时间戳命名** - 文件名包含时间戳,易于追踪
3. ✅ **前置检查** - 自动检查依赖关系
4. ✅ **标准模板** - 确保交接完整
5. ✅ **上下文持久化** - 防止任务中断
