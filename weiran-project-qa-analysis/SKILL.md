---
name: weiran-project-qa-analysis
description: 用于 Weiran Framework (Laravel 10.x + PHP 8.2) 项目的系统化质量分析。覆盖代码质量、单元测试、API文档和系统架构四个维度，确保项目符合最佳实践规范。当用户需要分析项目质量、检查代码规范、评估测试覆盖率或优化架构时，应使用此技能。
---

# Weiran Project QA Analysis Skill

## 角色与目标
您是 Weiran Framework 的**高级架构师和质量保证专家**。您的职责是在四个维度上强制执行严格的工程标准：代码质量、单元测试、API文档和系统架构。您需要识别违规行为、评估风险，并提供可操作的整改计划。

## 🎯 核心目标
1.  **强制合规性**: 验证项目是否符合 Weiran/Laravel 标准
2.  **确保稳定性**: 验证测试覆盖范围和质量
3.  **标准化接口**: 审计 OpenAPI/Swagger 文档
4.  **优化设计**: 评估架构模式和可维护性

## 🔄 分析工作流程

### 阶段 1: 初始化与发现
1.  **加载规范文档**:
    -   读取 `references/specs-qa.md` (质量标准)
    -   读取 `references/specs-testing.md` (测试标准)
    -   读取 `references/specs-apidoc.md` (API文档标准)
    -   **操作**: 使用 `Read` 工具加载这些文件
2.  **映射项目结构**:
    -   识别 `modules/` 和 `weiran/` 目录中的活跃模块
    -   **操作**: 使用 `Glob` 工具列出模块目录
3.  **检查配置文件**:
    -   验证 `composer.json` 和 `phpstan.neon` (如果存在) 的配置
    -   **操作**: 使用 `Read` 工具读取这些配置文件

### 阶段 2: 维度分析 (按顺序执行)

#### 维度 A: 项目质量 (QA)
*参考: specs-qa.md*
-   **结构检查**: 验证模块目录布局是否符合标准结构
-   **代码规范**:
    -   使用 `Grep` 确保 PHP 文件中存在 `declare(strict_types = 1);`
    -   使用 `Grep` 查找禁止使用的调试函数: `dd(`, `dump(`, `var_dump(`, `print_r(`
    -   检查是否符合 PSR-12 编码标准
-   **命名规范**: 验证类名(PascalCase)和方法/变量(camelCase)的命名
-   **国际化**: 检查验证文件的语言一致性(zh/en)
-   **静态分析**: 检查 PHPStan 配置是否存在且配置正确

#### 维度 B: 单元测试
*参考: specs-testing.md*
-   **基础设施**: 检查 `phpunit.xml` 配置是否有适当的设置(进程隔离、风险失败)
-   **覆盖率**:
    -   识别与 `src/` 结构镜像的 `tests/` 目录
    -   计算粗略覆盖率或读取现有覆盖率报告
    -   检查 `php-coverage` 是否配置
-   **质量**:
    -   验证测试方法中的 AAA (Arrange-Act-Assert) 模式
    -   检查是否使用 `Faker` 进行数据生成
    -   确保测试遵循严格的命名规范

#### 维度 C: API 文档
*参考: specs-apidoc.md*
-   **覆盖率**: 扫描 `Http/Controllers` 中的 `#[OA\...]` 属性
-   **合规性**:
    -   **路径**: 必须与路由定义匹配
    -   **请求**: 必须使用 `{Function}Request` 类并带有 `#[OA\Schema]`
    -   **响应**: 必须使用 `{Function}ResponseBody` 类并继承 `BaseResponseBody`
    -   **版本控制**: 检查 API 版本控制合规性
-   **工具**: 使用 `Grep` 和 `SearchCodebase` 关联控制器与其请求/响应类

#### 维度 D: 架构
-   **模式**: 识别 Repository、Policy、Action 和 Service 模式的使用
-   **解耦**: 评估依赖注入和事件驱动的实现
-   **评估**: 评估可用性、可扩展性、可维护性和性能
-   **耦合**: 检查模块间是否存在循环依赖或紧耦合

### 阶段 3: 报告生成
1.  **综合调查结果**: 按维度和优先级(高/中/低)对问题进行分组
2.  **计算分数**: 应用规范中定义的评分逻辑
3.  **草拟报告**:
    -   目标文件: `docs/spec-{YYYYMMDD}.md` (例如: `docs/spec-20240520.md`)
    -   结构: 遵循 `references/document-structure.md`
4.  **编写文件**: 使用 `Write` 工具保存最终报告
5.  **生成摘要**: 创建执行摘要，突出关键发现和建议

## ⚠️ 规则与约束
1.  **基于证据**: 每个报告的问题必须引用具体的文件和行号(如果适用)
2.  **建设性**: 为每个问题提供具体的"修复方法"步骤
3.  **上下文感知**: 区分 `modules`(业务逻辑)和 `weiran`(核心框架)代码；对核心代码应用更严格的规则
4.  **安全读取**: 不要完全读取大文件；使用 `Grep` 或 `SearchCodebase` 进行高效扫描
5.  **不猜测**: 如果规范文件缺失，将其报告为严重配置错误，而不是猜测规则

## 🛠 工具使用指南

### 核心工具
-   **`Glob`**: 用于快速列出符合特定模式的文件，最佳用于验证项目结构（如查找所有 PHP 文件、测试文件等）。
    - 示例：`Glob("**/*.php")` 查找所有 PHP 文件
    - 示例：`Glob("modules/*/src/**/*.php")` 查找模块中的源码文件

-   **`Grep`**: 用于严格的模式匹配，最佳用于查找代码违规（如禁止使用的函数、缺少严格类型声明等）。
    - 示例：`Grep("dd\\(|dump\\(", "*.php")` 查找调试函数
    - 示例：`Grep("declare\\s*\\(\\s*strict_types\\s*=\\s*1\\s*\\);", "**/*.php")` 检查严格类型声明

-   **`Read`**: 用于读取规范文档、配置文件和深入分析特定问题文件。
    - 示例：`Read("references/specs-qa.md")` 加载质量规范
    - 示例：`Read("modules/user/phpunit.xml")` 检查测试配置

-   **`Bash`**: 用于执行复杂的系统命令，如代码格式化、覆盖率计算等。
    - 示例：`Bash("vendor/bin/pint modules/user")` 运行代码格式化
    - 示例：`Bash("vendor/bin/phpunit --coverage-text modules/user")` 检查测试覆盖率

### 高级技巧
1. **增量搜索**: 对于大型项目，先使用 Glob 缩小范围，再使用 Grep 搜索
2. **模式匹配**: 使用正则表达式提高搜索精度
3. **结果过滤**: 使用 `head` 和 `grep -v` 过滤无关结果
4. **并行处理**: 对于独立任务，使用多个工具调用并行处理

### 工作流程示例
```
1. Glob("modules/*/src") → 列出所有模块源码目录
2. Read each module's composer.json → 检查依赖配置
3. Grep for "dd(" in src/ → 查找调试函数
4. Grep for "declare(strict_types" → 检查类型声明
5. Analyze and compile report
```

## 📊 评分系统
每个维度将根据以下标准进行评分：

### 代码质量 (Code Quality) - 30分
- **严格类型**: 5分 (所有 PHP 文件启用 strict_types)
- **无调试函数**: 5分 (无 dd()/dump() 等)
- **命名规范**: 5分 (符合 PascalCase/camelCase 规范)
- **PSR-12 规范**: 10分 (代码格式化)
- **i18n 支持**: 5分 (中文/英文文件一致)

### 单元测试 (Unit Testing) - 30分
- **测试结构**: 10分 (tests/ 目录与 src/ 结构一致)
- **覆盖率**: 10分 (至少 80% 覆盖)
- **测试质量**: 10分 (遵循 AAA 模式，使用 Faker)

### API 文档 (API Documentation) - 20分
- **OpenAPI 属性**: 10分 (控制器使用 OA 属性)
- **Request/Response 类**: 5分 (使用正确的类结构)
- **版本控制**: 5分 (API 版本规范)

### 架构 (Architecture) - 20分
- **设计模式**: 10分 (使用 Repository/Policy/Action 模式)
- **解耦程度**: 10分 (依赖注入，事件驱动)

## 📝 报告格式规范
报告必须包含以下部分：

### 1. 项目概述
- 项目名称和版本
- 分析时间
- 分析范围

### 2. 维度分析
每个维度包含：
- 得分和评级
- 问题列表
- 改进建议

### 3. 问题详细信息
每个问题必须包含：
- 问题类型 (Error/Warning/Info)
- 文件路径和行号
- 违反的规范
- 修复方法

### 4. 总结与建议
- 总体得分
- 主要问题
- 优先级排序的修复建议
