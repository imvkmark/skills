---
name: weiran-project-analyst
description: 为 Weiran 框架 (Laravel 10.x + PHP 8.2) 项目创建、更新和执行结构化的代码分析计划。当用户希望系统性地分析代码库、规划代码走查、生成文档计划或逐步执行现有的分析计划时请使用此技能。典型的触发词包括“创建 weiran 项目分析计划”、“更新分析计划”以及“执行 weiran 项目代码分析”。
---

# Weiran 项目代码分析助手

为 Weiran 框架 (Laravel 10.x + PHP 8.2) 代码库创建全面的、分阶段的分析计划，并系统性地执行这些计划。

根据用户的请求以及是否存在已有的计划，此技能在两种主要模式下运行：**规划模式** 和 **执行模式**。

## 配置选项
- `output-dir: @docs/` - 用于存储分析计划和输出文档的默认目录

## 模式 1：规划（新建或更新计划时）

如果用户要求创建计划、更新计划，或者要求执行分析但 `@docs/` 目录下尚未存在计划文件时，请遵循以下步骤：

### 步骤 1.1：探索代码库

理解项目结构和技术栈。

#### Weiran 项目通常具有以下结构
```
├── config/                      # 配置文件夹
├── modules/                     # 所有模块存放的文件夹
│   └── [module name]/           # 模块文件夹
│       ├── configurations/      # 配置文件夹
│       │   ├── permissions.yaml # 权限定义
│       │   ├── menus.yaml       # 菜单定义
│       │   ├── services.yaml    # 服务定义文件
│       │   ├── hooks.yaml       # 服务钩子定义文件
│       ├── resources/           # 资源文件夹
│       │   ├── lang/            # 多语言支持包文件夹
│       │   ├── migrations/      # 数据库设计文件夹
│       │   └── views/           # 视图文件夹
│       │       ├── backend/     # 视图 - 后台
│       │       ├── develop/     # 视图 - 开发者平台
│       │       └── tpl/         # 视图 - 核心模板
│       ├── src
│       │   ├── ServiceProvider  # 服务提供者文件, 用来注册命令, 路由, 事件监听
│       │   ├── Action/          # 服务层文件夹
│       │   ├── Classes/         # 服务层所需的基础类文件夹
│       │   │   ├── {Model}Def.php      # 模块定义文件
│       │   │   └── Traits/      # traits
│       │   ├── Commands/        # 命令文件夹
│       │   ├── Events/          # 事件文件夹, 事件使用 Event 后缀
│       │   ├── Listeners/       # 事件监听器文件夹
│       │   ├── Jobs/            # 队列文件夹
│       │   ├── Http/            # 路由和中间件/控制器
│       │   │   ├── [Web|..]/    # 控制器 / Validation / Swagger 文件定义
│       │   │   ├── Middlewares/ # 中间件
│       │   │   └── Routes/      # 路由
│       │   └── Models/          # 模型文件夹
│       │       ├── Policies/    # 模型 - 策略
│       │       └── Resources/   # 模型 - 资源
│       └── tests                # 单元测试
├── public              # 公共资源目录
│   └── index.php       # 入口文件
├── resources           # 资源文件
├── storage             # 调试/日志/缓存存储目录
└── vendor              # 第三方文档(只是预览, 不做详细说明)
```

#### 快速定位关键文件 (重要提示：必须使用专用内置工具)
请使用合适的 Claude 工具替代 bash 命令来探索代码：

```yaml
# 使用 Glob 工具搜索文件
pattern: "**/*Controller.php"
pattern: "*/modules/*/src/Models/*.php"
pattern: "*/modules/*/src/Action/*.php"

# 使用 Read 工具读取文件 (示例)
file_path: "routes/web.php"
file_path: "config/app.php"
```

识别 Weiran 框架的特定特征：
- **技术栈**: Weiran 框架 (Laravel 10.x + PHP 8.2)
- **架构模式**: 带有 Weiran 组件的模块化单体架构
- **核心组件**: Controllers (控制器), Models (模型), Services (服务), Middleware (中间件), Jobs (任务), Events (事件)
- **基础设施**: MySQL/Redis, Laravel Queue, 任务调度
- **Weiran 特性**: 事件系统, 任务调度, 模块化系统

### 步骤 1.2：设计/更新分阶段计划

**如果是创建新计划：**
创建包含文档规范的分阶段分析计划。将分析任务组织成逻辑阶段。请参考 `references/phase-templates.md` 中的常见模式。
- 将相关的组件分组。
- 按依赖关系对阶段进行排序（优先分析被依赖的底层模块）。

**如果是更新已有计划（处理调整请求）：**
1. 读取当前的 `plan-analysis.md` 以及由用户或早期阶段提供的调整请求详情。
2. 将请求的更改/新增内容更新到计划中。
3. 在 Metadata (元数据) 中递增计划版本号。
4. 将 `plan-progress.md` 文件中的状态 (Status) 更新为 `计划已调整`。

### 步骤 1.3：生成输出文件

在分析输出目录（默认为 `@docs/`）中创建两个文件：
- 分析计划主体: 参考 `references/plan-analysis.md` 进行编写。保存为 `@docs/plan-analysis.md`。
- 分析计划进度追踪: 参考 `references/plan-progress.md` 进行编写。保存为 `@docs/plan-progress.md`。

确保 `plan-progress.md` 文件中包含以下格式的 Metadata 部分：
```markdown
## Metadata
- Plan ID: [唯一生成的ID]
- Last updated: [时间戳]
- Status: 待执行
- Current phase/document: [正在执行的文档名，如 initial]
- Last completed step: [None]
- Auto-execution: disabled (在自动开始执行代码分析前，必须事先询问用户的意见)
- Adjustment requests: []
```

**关键要求**：完成规划后，必须先向用户总结计划并请求确认，绝对禁止自动跳转执行。

## 模式 2：执行（生成分析文档时）

此模式要求 `@docs/` 目录下必须存在已建好的分析计划文件：
- `@docs/plan-analysis.md` - 文档规范主体
- `@docs/plan-progress.md` - 进度追踪表格

如果这些文件缺失，请立即自动切换回 **模式 1：规划**，先完成计划文件的生成。

### 步骤 2.1：加载上下文

使用 `Read` 工具读取分析计划和当前的进度：
- 读取 `docs/plan-analysis.md`
- 读取 `docs/plan-progress.md`

通过文件内容识别出：
- 当前正在进行哪个阶段。
- 接下来需要生成哪个文档。
- 计划对该文档提出的具体分析要求。
- 从 Metadata 取出恢复点信息（如果有中断的话）。

### 步骤 2.2：生成分析文档

生成指定的文档。对于每一份文档，请遵循以下流程：

#### 2.2.1 定位相关代码
参阅本技能底部的 **工具使用指南**。绝对禁止使用 bash 下的 `grep` 或 `find` 命令。

#### 2.2.2 系统性分析
遵循分析计划 (`plan-analysis.md`) 中提出的要求。对于每份文档请分析：
1. **理解用途** - 这些代码是做什么用的？
2. **绘制结构** - 它是如何被组织起来的？
3. **追踪流程** - 数据/控制流是如何运转的？
4. **识别模式** - 用到了哪些设计模式？
5. **记录洞察** - 记录那些非显而易见的设计决策。

#### 2.2.3 编写文档
使用标准的文档结构规范。模板请参考 `references/document-structure.md`。
**文档必须包含的基本元素：**
- 清晰的章节标题
- 附带解释说明的代码片段（必须包含具体的文件路径）
- 针对复杂流程的 Mermaid 图表（⚠️注意：在 Mermaid 图表的节点文本中，如果包含特殊字符如 `:`、`/` 或 `<br>`，必须使用双引号将文本包裹起来，例如 `node["节点文本<br>包含特殊字符"]`，以避免渲染或语法错误）
- 对性能和架构设计的考量

### 步骤 2.3：执行验证与计划动态调整

在生成文档的过程中：
1. 验证当前计划中针对该文档的细节指导是否充足。
2. 如果计划被发现存在缺陷或需要调整（例如：在分析时发现了原计划未曾注意到的关键架构组件）：
   - 记录下需要调整的详细细节。
   - 将 `plan-progress.md` 文件中的状态 (Status) 更改为 `计划待调整`。
   - 在 Metadata 部分的 `Adjustment requests` 中追加这次调整请求。
   - 自动切换到 **模式 1：规划**，使用这些调整意见对原计划进行更新。在此更新完成后，等待用户批准新的计划，然后再恢复执行流程。

### 步骤 2.4：更新执行进度

每完成一份文档后，请立即更新 `@docs/plan-progress.md` 文件：

更新进度表格 (Progress Table)：
```markdown
| 阶段 | 状态 | 完成度 | 备注 |
|------|------|--------|------|
| 第1阶段：基础架构 | 已完成 | 100% | ✓ |
| 第2阶段：核心服务 | 进行中 | 40% | 已完成 04, 05 |
```

更新元数据部分 (Metadata)：
```markdown
## Metadata
- Plan ID: [匹配由规划器生成的 ID]
- Last updated: [时间戳]
- Status: [待执行/执行中/已完成/计划待调整]
- Current phase/document: [目前正在被生成的文档名]
- Last completed step: [最后一步完成的步骤编号]
- Auto-execution: disabled
- Adjustment requests: [如果存在需要更新规划的要求，填写在此处]
```

## 质量检查清单 (Quality Checklists)

在宣布一份文档完成之前，必须确认：
- [ ] analysis-plan.md 中的所有针对性要求都已被解答
- [ ] 代码引用示例中都包含了对应的文件路径
- [ ] 复杂的逻辑链路都配有对应的图表
- [ ] 解释了非显而易见的设计决策
- [ ] 指出了影响性能的隐患
- [ ] 输出文档的排版遵循了标准的结构模板

### 针对 Weiran 项目的专项检查点
- **架构**: 控制器是否严格遵循单一职责；服务层是否正确封装；模型关联是否合理；路由命名是否规范。
- **代码质量**: 是否使用了类型声明；是否存在冗余重复代码；是否遗留了硬编码常量。
- **安全**: 输入验证；SQL 注入防护；XSS 防护；权限控制。
- **性能**: 识别潜在的 N+1 查询问题；缓存利用率；数据库查询调优；关联数据的懒加载问题。

## 工具使用指南 (CRITICAL: 必须严格遵守)

在探索代码库或搜索特定的代码实现时，你必须遵守以下工具使用原则：
- **文件搜索 (File Search)**：永远使用内置的专有 `Glob` 工具，严禁使用 bash `find` 或 `ls`。（示例：`pattern: "**/*Controller.php"`）
- **内容检索 (Content Search)**：永远使用内置的专有 `Grep` 工具，严禁使用 bash `grep` 或 `rg`。请严格使用类型参数来缩小范围。（示例：`type: "php"`）
- **文件阅读 (File Reading)**：永远使用内置的 `Read` 工具去检视代码逻辑，严禁使用 `cat`, `head`, 或是 `tail`。
- **并发调用 (Parallelism)**：当需要调查多个文件或组件时，请在同一次回复中**并发（Parallel）**触发多个 `Glob`, `Grep`, 或 `Read` 工具以此达到最高的性能表现。