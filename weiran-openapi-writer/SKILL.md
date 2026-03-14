---
name: weiran-openapi-writer
description: 为 Weiran Framework 中的 Laravel 控制器自动生成 OpenAPI（Swagger）文档。处理 Request/Response 类与 PHP Attributes。
---

# Weiran OpenAPI 文档编写器

## 角色
你是一名专注于 Weiran Framework 的 Laravel 专家开发者。你的任务是使用 PHP Attributes 为控制器方法生成完整的 OpenAPI（Swagger）文档。

## 目标
1. 分析目标控制器方法，理解其输入参数、参数来源与返回结构。
2. 优先复用项目中已有的 `Request` / `ResponseBody` / OpenAPI Schema 类，而不是机械按命名猜测。
3. 为控制器方法生成符合当前项目规范的 `#[OA\...]` Attributes。
4. 严格遵守 Weiran 当前仓库的命名、目录结构与 OpenAPI 风格约定。

## 工作流说明

你必须严格按照以下阶段顺序执行。

### 阶段 1：分析与上下文收集
1.  **通过 Route 确认目标**：
    -   你 MUST 从定位与用户意图匹配的 route 定义开始。
    -   使用 `Grep` 或 `SearchCodebase` 查找路由文件。匹配模式：`[modules|weiran]/**/src/Http/Routes/api*.php`。
    -   路由文件中定义的 Controller 与 Method 是 **Source of Truth**。
2.  **确定 Prefix 与 Path**：
    -   读取对应模块中的 `src/Http/RouteServiceProvider.php`，找到 `mapApiRoutes` 方法并提取 route `prefix`。
    -   将模块 prefix 与 route path 组合成完整的 API Path。
3.  **Namespace 与路径推导**：
    -   读取 Controller 文件，提取其 `namespace`。
    -   **约束**：Controller 的 namespace 中 MUST 包含子串 `Api`。如果不包含，立即 STOP，并告知用户当前仅支持 API 控制器。
    -   *推导* 可能的 Request 与 Response 目录，但这只是初始线索，不是唯一来源。
4.  **识别 HTTP 语义**：
    -   优先读取 route 的 HTTP method。
    -   如果 route 使用 `Route::any` / `$route->any(...)`，不要直接照搬为通用方法；必须结合方法语义判断：
        -   纯读取、纯查询参数、列表/详情/校验类接口，优先使用 `OA\Get`。
        -   登录、提交、修改、上传、需要 `requestBody` 的接口，优先使用 `OA\Post`。
        -   如果仍无法可靠判断，STOP 并告知用户该接口需要人工确认 HTTP 语义。
5.  **识别参数来源与返回风格**：
    -   检查方法参数、`input()` / `$request->input()` / `Request::file()` 等调用，判断该接口是：
        -   query parameters 接口
        -   JSON requestBody 接口
        -   `multipart/form-data` 上传接口
        -   内联响应 schema 接口

### 阶段 2：规划与存在性检查（Mental Sandbox）
在生成代码前，你必须基于 **文件是否存在** 制定计划：
1.  **定义目标类名**：
    -   格式：`{ControllerNameWithoutSuffix}{MethodName}{Suffix}`
    -   示例：`UserController::login` -> Request：`UserLoginRequest`，Response：`UserLoginResponseBody`。
2.  **检查 Request 类是否存在**：
    -   优先检查以下来源，而不是只检查推导目录：
        -   Controller 方法签名中的具体 Request 类型
        -   Controller 顶部现有 `use` 语句中已引入的 Request 类
        -   Controller 方法体中通过 `app(FooRequest::class, [...])`、`resolve(FooRequest::class)`、容器别名等方式解析出的 Request 类
        -   与当前模块相关的 `src/Http/**` 目录中的 `*Request.php`
        -   再使用 `{Controller}{Method}Request` 作为兜底命名线索
    -   **决策**：
        -   如果 **Exists** 且接口是 JSON body：在 `requestBody` -> `content` -> `ref` 中使用它。
        -   如果 **Exists** 且接口是上传接口：使用 `OA\MediaType(mediaType: 'multipart/form-data', schema: new OA\Schema(ref: RequestClass::class))`。
        -   如果 **Not Exists** 且接口是 query parameters：不要创建 Request 类，改为使用 `parameters`。
        -   如果 **Not Exists**，但接口是 `POST` / `PUT` / `PATCH` 且方法体明确读取少量标量 body 字段（如 `input('device_id')`、`input('device_type')`），允许生成内联 `OA\RequestBody`，不要错误降级为 query `parameters`。
        -   如果 **Not Exists** 且接口没有明显 body：Do NOT create。将 `requestBody` 设为 `null`（或完全省略）。
3.  **检查 Response 类是否存在**：
    -   优先检查以下来源，而不是只检查推导目录：
        -   Controller 顶部现有 `use` 语句中已引入的 `*ResponseBody` 类
        -   当前模块中的 `src/Http/**/OpenApi/**` 目录
        -   当前模块中的 `src/Http/**/ApiV1/**` 目录
        -   再使用 `{Controller}{Method}ResponseBody` 作为兜底命名线索
    -   **决策**：
        -   如果 **Exists**：在 `responses` -> `content` -> `ref` 中使用它。
        -   如果 **Not Exists**，但该接口返回结构简单且项目中已有内联 schema 风格（例如固定字段对象响应），可以使用 `OA\JsonContent(properties: [...])` 内联定义响应结构。
        -   如果 **Not Exists** 且无法可靠提炼结构：Do NOT create。使用 `ref: \Weiran\System\Http\OpenApi\BaseResponseBody::class`。
4.  **检查参数表达方式**：
    -   如果接口主要通过 `input()`、query string 或简单标量参数读取输入，优先使用 `parameters`。
    -   但如果 route 语义明显是写操作（尤其 `POST` / `PUT` / `PATCH`），且这些标量来自 body 而不是 query string，应优先生成 `requestBody`，必要时使用内联 `OA\JsonContent(properties: [...])`。
    -   所有 `parameters` 都应尽量补全 `name`、`description`、`in`、`required`、`schema`。
    -   不要因为没有 Request 类就机械省略 body；要根据真实输入来源判断是 `parameters` 还是内联 `requestBody`。

### 阶段 3：执行
1.  **更新 Controller（分两步）**：
    -   **Step 3.1**：添加 Imports。
        -   读取文件。
        -   添加 `use OpenApi\Attributes as OA;`。
        -   仅当 Phase 2 中确认找到 Request / Response 类时，才添加对应的 `use` 语句。
        -   如果使用了 fallback，则添加 `use Weiran\System\Http\OpenApi\BaseResponseBody;`。
    -   **Step 3.2**：添加 Attribute。
        -   使用 `SearchReplace`，将 `#[OA\...]` Attribute 插入到目标方法定义的*正前方*。
        -   确保 `path` 与阶段 1 得到的完整 API Path 完全一致。
        -   确保已设置 `tags`（通常为模块名）。
        -   根据接口类型选择正确结构：
            -   query parameters 接口：优先使用 `parameters`
            -   JSON body 接口：使用 `requestBody` + `OA\JsonContent(ref: RequestClass::class)`
            -   无专用 Request 类但存在少量标量 body 字段的写接口：允许使用 `requestBody` + 内联 `OA\JsonContent(properties: [...])`
            -   上传接口：使用 `requestBody` + `OA\MediaType(mediaType: 'multipart/form-data', ...)`
            -   简单固定响应：允许 `OA\JsonContent(properties: [...])` 内联响应结构

### 阶段 4：验证
1.  **检查一致性**：确保 Attribute 中的 `path` 与路由文件完全一致。
2.  **检查语法**：确保没有引入语法错误。
3.  **检查风格**：确保使用的是 `OpenApi\Attributes as OA`，而不是 `Annotations` 或注释式 Swagger。
4.  **检查完整性**：
    -   `parameters` 尽量包含 `schema`
    -   `requestBody` 与接口真实输入方式一致
    -   能复用已有 `ResponseBody` 时，不要错误回退到 `BaseResponseBody`

## 规则与命名约定

| 实体 | 约定 | 示例 |
| :--- | :--- | :--- |
| **Request Class** | `{Controller}{Method}Request` | `UserLoginRequest` |
| **ResponseBody** | `{Controller}{Method}ResponseBody` | `UserLoginResponseBody` |
| **Controller** | `{Module}Controller` | `AuthController` |
| **API Path** | 小写、snake_case | `/api/web/system/v1/auth/login` |
| **Tags** | 模块名（PascalCase） | `System` |

## 项目适配规则

1. **OpenAPI 风格**
   - 当前项目使用的是 PHP 8 Attributes 风格。
   - 必须使用 `use OpenApi\Attributes as OA;`。
   - 不要使用 `OpenApi\Annotations as OA;`。

2. **Request / Response 发现策略**
   - 不要只依赖 `{Controller}{Method}*` 命名规则。
   - 优先相信：方法签名、现有 `use` 语句、方法体中的容器解析（如 `app(FooRequest::class, [...])` / `resolve(FooRequest::class)`）、模块内 `Http` 目录真实文件结构。
   - 当前项目中，ResponseBody 可能位于 `OpenApi` 子目录，请主动搜索。

3. **query parameters 接口**
   - 对于列表、详情、验证、纯查询类接口，通常应使用 `OA\Parameter`。
   - 即使 route 是 `any`，也不要默认生成 `requestBody`。

4. **标量 body 写接口**
   - 对于 `POST` / `PUT` / `PATCH` 写接口，即使没有独立 Request 类，只要方法体明确从 body 读取少量固定字段，也可以生成内联 `OA\RequestBody`。
   - 这类字段通常应放在 `OA\JsonContent(properties: [...])` 中，而不是错误标为 query `parameters`。

5. **上传接口**
   - 对于文件/图片上传接口，优先生成 `multipart/form-data` 结构。
   - 典型写法是 `OA\RequestBody` + `OA\MediaType(mediaType: 'multipart/form-data', schema: ...)`。

6. **响应结构**
   - 优先使用已有 `*ResponseBody` 类。
   - 如果项目中没有现成 ResponseBody，但返回字段非常固定且清晰，可使用内联 `OA\JsonContent(properties: [...])`。
   - 只有在无法可靠提炼结构时，才回退到 `BaseResponseBody`。

## 上下文与规范

### 1. Controller Attributes 结构（POST 示例）
```php
#[OA\Post(
    path: '/api/web/system/v1/auth/login',
    summary: 'Login',
    tags: ['System'],
    requestBody: new OA\RequestBody(
        required: true,
        content: new OA\JsonContent(ref: UserLoginRequest::class)
    ),
    responses: [
        new OA\Response(
            response: 200,
            description: 'Success',
            content: new OA\JsonContent(ref: UserLoginResponseBody::class)
        )
    ]
)]
public function login(...)
```

### 2. Controller Attributes 结构（Fallback 示例）
当没有独立 Request 类，且接口也不存在明确 body 输入时：
```php
#[OA\Post(
    path: '/api/web/system/v1/auth/logout',
    summary: 'Logout',
    tags: ['System'],
    // No requestBody because this endpoint has no clear body payload
    responses: [
        new OA\Response(
            response: 200,
            description: 'Success',
            content: new OA\JsonContent(ref: BaseResponseBody::class)
        )
    ]
)]
public function logout(...)
```

### 3. Query Parameters 结构示例
```php
#[OA\Get(
    path: '/api/web/content/v1/content/detail',
    summary: '内容详细',
    tags: ['Content'],
    parameters: [
        new OA\Parameter(
            name: 'id',
            description: '内容 ID',
            in: 'query',
            required: true,
            schema: new OA\Schema(type: 'integer')
        ),
    ],
    responses: [
        new OA\Response(
            response: 200,
            description: 'success',
            content: new OA\JsonContent(ref: ContentContentDetailResponseBody::class)
        )
    ]
)]
public function detail(...)
```

### 4. Multipart 上传结构示例
```php
#[OA\Post(
    path: '/api/web/system/v1/upload/image',
    summary: '图片上传',
    requestBody: new OA\RequestBody(
        required: true,
        content: new OA\MediaType(
            mediaType: 'multipart/form-data',
            schema: new OA\Schema(ref: UploadImageRequest::class)
        )
    ),
    tags: ['System'],
    responses: [
        new OA\Response(
            response: 200,
            description: '图片上传',
            content: new OA\JsonContent(ref: BaseResponseBody::class)
        )
    ]
)]
public function image(...)
```

### 5. 内联响应结构示例
```php
#[OA\Get(
    path: '/api/web/version/v1/version/latest',
    summary: '版本检测',
    tags: ['Version'],
    parameters: [
        new OA\Parameter(
            name: 'version',
            description: '版本号',
            in: 'query',
            required: true,
            schema: new OA\Schema(type: 'string')
        ),
    ],
    responses: [
        new OA\Response(
            response: 200,
            description: '获取版本成功',
            content: new OA\JsonContent(
                properties: [
                    new OA\Property(property: 'download_url', description: '下载地址', type: 'string'),
                    new OA\Property(property: 'description', description: '描述', type: 'string'),
                    new OA\Property(property: 'version', description: '版本', type: 'string'),
                    new OA\Property(property: 'is_upgrade', description: '是否需要强制更新', type: 'string'),
                ]
            )
        )
    ]
)]
public function latest(...)
```

### 6. 标量 body 写接口示例
当方法没有专用 Request 类，但明确从 body 中读取固定字段时：
```php
#[OA\Post(
    path: '/api/web/system/v1/auth/renew',
    summary: '续期',
    requestBody: new OA\RequestBody(
        required: true,
        content: new OA\JsonContent(properties: [
            new OA\Property(property: 'device_id', description: '设备 ID, 参考 header x-id', type: 'string'),
            new OA\Property(property: 'device_type', description: '设备类型, 参考 header x-os', type: 'string'),
        ])
    ),
    tags: ['System'],
    responses: [
        new OA\Response(
            response: 200,
            description: '操作成功',
            content: new OA\JsonContent(ref: BaseResponseBody::class)
        )
    ]
)]
public function renew(...)
```

### 7. 方法体解析 Request 示例
当方法签名不是具体 Request，但方法体中解析了 Request 对象时，应视为已存在 Request 线索：
```php
public function login(Request $req): JsonResponse
{
    /** @var AuthLoginRequest $request */
    $request = app(AuthLoginRequest::class, [$req]);
    $reqPassport = $request->scene('passport')->validated();
    ...
}
```

此时应优先使用 `AuthLoginRequest::class` 作为 `requestBody` 的 schema 引用，而不是因为方法签名是 `Request` 就省略或降级。
