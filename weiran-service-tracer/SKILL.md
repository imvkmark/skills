---
name: weiran-service-tracer
description: 为 Weiran 框架追踪并分析指定控制器 (Controller) 或服务/动作 (Service/Action) 方法的完整执行链路。当用户希望了解一个接口从路由到数据库的底层逻辑，或者想单独分析某个 Service/Action 类的内部工作流时使用。触发词包括“分析 [方法名] 控制器链路”、“追踪 [X] 服务类的 [Y] 方法实现”、“梳理从路由到数据库的链路”。
---

# Weiran 控制器与服务链路追踪助手

为 Weiran 框架 (Laravel 10.x + PHP 8.2) 代码库深入追踪并梳理单一“控制器方法 (Controller)”或“服务动作 (Action/Service)”的完整上下文链路。

## 目标识别与模式判定

根据用户提供的信息，判断分析目标是 **URL 路径**、**控制器 (Controller)** 还是 **服务/动作 (Service/Action)**。

- **URL 路径模式**：当用户给出诸如 `/api/v1/user/profile` 的路由地址时。
  - **前置步骤**：使用 `Grep` 在 `modules/*/src/Http/Routes/*.php` 中搜索该 URL（注意处理路由定义中的变量槽，如 `{id}`）。
  - **目标转换**：从路由定义（通过看使用到的控制器和方法名）准确定位到对应的 Controller，然后无缝切换到 **Controller 模式** 进行后续追踪。
- **Controller 模式**：分析重点是 `路由入口 -> 表单验证/中间件 -> Controller 逻辑调配 -> 关联 Action 分发 -> 视图/JSON 响应`。
- **Service/Action 模式**：分析重点是 `Action 前置状态装载 (Fluent Setters) -> 核心业务处理 -> 模型调取 (Model/DB) -> 第三方 API 请求 -> 事件分发 (Event/Job) -> 状态获取 (Getters/Errors)`。

无论是由于用户起手指定的哪种模式，你在追踪时如果发现了另一半，**必须将完整的链路补全**（即分析控制器时要深挖里面的 Action，分析 Action 时需指出哪些控制器调用了它）。

## 工具使用规范 (CRITICAL)

- **内容/方法检索**：必须使用专有 `Grep` 工具。例如搜索 `index` 方法时使用正则表达式 `function\s+index` 并配合 `type: "php"`。
- **文件定位**：必须使用专有 `Glob` 工具定位控制器或 Action 文件。例如：`pattern: "**/DeviceController.php"`。
- **文件读取**：必须使用专有 `Read` 工具。
- **请发扬极度的探索与追踪精神**：不要仅仅停留在表面文件，只要遇到依赖的自定义 Request 类、Action 类、基类继承，必须继续使用工具深挖下去！

## 步骤 1：梳理调用入口与参数 (入参解析)

### 如果目标是 Controller：
1. **路由探测**：使用 `Grep` 在 `modules/*/src/Http/Routes/*.php` 中寻找指向该控制器的路由定义。提取：路由 URL、HTTP 动词（GET/POST）、应用的中间件。
2. **请求验证**：进入控制器方法内部。Weiran 通常使用表单请求类进行验证（如 `$request->scene('...')->validated()`）。追踪并读取该 Request 类，提取出参数的验证规则。
3. **参数提取**：记录控制器从 Request 中获取了哪些参数，准备传递给下层代码。

### 如果目标是 Action / Service：
Weiran 的 Action 类（如 `ActDevice`）通常采用 **Fluent 接口模式 (状态构造器)**。它们不直接将参数传入执行方法。
1. **追踪 Setters**：识别为了执行目标方法，调用方需要提前调用哪些 setter 方法（例如 `$action->setDeviceId($id)->setOnline($online)`）。
2. **寻找调用方**：使用 `Grep` 搜索整个代码库，找出是哪些 Controller 或是 Job 在调用这个 Action 方法，并梳理它们是如何传参的。

## 步骤 2：业务逻辑深潜 (核心处理)

进入核心的业务执行区域（通常是在 Action 提供的方法内部，它一般不需要传参且返回 `bool` 类型）。

1. **依赖分析**：检查该方法内部注入或实例化了哪些其他的服务类、Repository 或第三方 HTTP 客户端。
2. **数据库与模型 (Model/DB)**：梳理所有的 Eloquent 查询。重点记录：是否使用了事务(`DB::transaction`)？执行的是查询(Select)还是写入(Create/Update/Delete)？涉及了哪张表？
3. **外部系统交互**：是否通过 Guzzle、Http facade 或特定的 SDK 请求了外部系统的 API（例如微信支付、第三方短信接口）。
4. **异步与解耦 (Weiran 特定机制)**：
   - 是否通过 `Event::dispatch()` 抛出了事件？如果是，需简单指出该事件可能关联的 listeners。
   - 是否通过 `dispatch()` 分发了异步队列任务 (Job)？

## 步骤 3：状态返回与响应层 (出参解析)

1. **Action 的状态维护**：
   - 错误处理：检查 `$this->setError('...')` 是在哪些条件下被触发的。
   - 成功状态：检查成功时是如何保存数据的，以及相关的 Getter 方法（如 `$action->getDetail()`）。
2. **Controller 的格式化包装**：
   - 查看 Controller 是如何承接 Action 的 `bool` 返回值，并如何调用 `Resp::success()` / `Resp::error()` 格式化最终的 API JSON 响应的。

## 步骤 4：生成分析报告

依据上述追踪的成果，将其保存为一份规范的 Markdown 链路追踪分析报告文件。
文件必须创建在 `@docs/` 目录下，并按照以下格式命名：`@docs/[类名的小写烤肉串格式]-[方法名小写]-[当前日期].md`。
（例如，如果要分析 `MerchantController` 的 `register` 方法，并且今天是 2026年3月7日，那么文件路径应当为：`docs/merchant-controller-register-2026-03-07.md`）

### 报告模板结构

```markdown
# [类名] :: [方法名] 链路追踪分析

## 1. 链路概览 (Mermaid 流程图)
使用 `flowchart TD` 或 `sequenceDiagram` 绘制从请求发起到数据库操作的完整链路。
> ⚠️ **重要提示：避免 Mermaid 语法错误**：所有包含如冒号 `:`、斜杠 `/`、大括号 `{}` 或 `<br>` 等特殊字符的节点，**必须使用双引号将节点文本包裹起来**。例如：`A["路由: POST /api/v1/user"]`。

## 2. 入口与参数验证 (Controller 层)
- **路由定义**: [方法 / URL / 中间件]
- **参数校验**: [列出核心必填参数与验证规则，引用的 FormRequest/scene]

## 3. 业务逻辑与状态转移 (Action 层)
- **状态装配 (Setters)**: [列出执行该操作所需的前置状态和设置方法]
- **核心逻辑流程**: [分步说明该方法内部的 `if/else` 核心业务逻辑]
- **数据库交互**: [明确指出影响了哪些 Model，是读操作还是写操作，有无事务保护]
- **事件/任务触发 (可选)**: [触发的 Event 或分发的 Job]

## 4. 返回值与异常处理
- **成功场景**: [返回的成功结构及包含的业务数据]
- **失败场景 (Errors)**: [列举出会触发 `$this->setError()` 的业务条件]

## 5. 潜在风险与优化建议
（作为分析师提出技术洞察，可选填）
- 例如：这里存在 N+1 查询问题。
- 例如：这里外部 API 调用没有设置超时保护。
```
