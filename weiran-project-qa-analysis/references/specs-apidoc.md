# Weiran API 接口文档规范

本文档旨在提供统一的接口文档规范，方便对项目接口文档进行验证

## 目录

1. [接口定义规范](#接口定义规范)
2. [请求体规范](#请求体规范)
3. [响应体规范](#响应体规范)
4. [参数规范](#参数规范)
5. [API 版本控制](#api版本控制)
6. [🚫 Anti-Patterns (反模式)](#🚫-anti-patterns-反模式)

---

### 接口定义规范

#### 基础结构

接口定义使用 OpenAPI (Swagger) PHP Attributes 注解：

```php
#[OA\{METHOD}(
    path: '/api/web/system/v1/xxx',
    summary: '接口名称',
    description: '接口详细描述(可选)',
    tags: ['标签名'],
    // parameters 或 requestBody
    // responses
)]
```

METHOD : GET | POST | PUT | DELETE | OPTIONS

#### 规范要求

1. **path**: 完整的 API 路径, 示例 : `/api/web/system/v1/auth/login`
2. **summary**: 简洁的中文接口名称，不超过 20 字
3. **description**: [可选], 提供更详细的说明
4. **tags**: 接口分组标签
5. **请求参数**: GET 使用 `parameters`，POST/PUT 使用 `requestBody`
6. **响应定义**: `responses` 数组必须包含至少一个 200 响应
7. **Request 类名**: `{功能}Request`
8. **ResponseBody 类名**: `{功能}ResponseBody`
9. **Controller 类名**: `{模块}Controller`

### 请求体规范

#### 使用独立的 Request 类

推荐为每个接口创建独立的 Request 类，使用 `#[OA\Schema]` 注解：

```php
#[OA\Schema(
    required: ['passport'],
    properties: [
        new OA\Property(
            property: 'passport',
            description: '通行证',
            type: 'string',
        ),
    ]
)]
class AuthLoginRequest extends Request
{
    // ...
}
```

#### 在接口中引用

```php
#[OA\Post(
    // ...
    requestBody: new OA\RequestBody(
        required: true,
        content: new OA\JsonContent(ref: AuthLoginRequest::class)
    ),
)]
```

---

### 响应体规范

#### 使用独立的 Response 类

推荐为每个响应创建独立的 ResponseBody 类，继承自 `BaseResponseBody`：

```php
#[OA\Schema(description: '登录成功')]
class AuthLoginResponseBody extends BaseResponseBody
{
    #[OA\Property(
        description: '登录成功返回的token信息',
        properties: [
            new OA\Property(property: 'token', description: 'Token', type: 'string'),
        ],
        type: 'object'
    )]
    public object $data;
}
```

#### BaseResponseBody 结构

基础响应体包含 `code`, `message`, `data` 字段。

---

### 参数规范

#### Query/Path Parameters (GET/Path)

```php
parameters: [
    new OA\Parameter(
        name: 'token',
        description: 'Token',
        in: 'query',      // 'query' | 'path' | 'header'
        required: true,
        schema: new OA\Schema(type: 'string')
    ),
]
```

### 🚫 Anti-Patterns (反模式)

以下是在文档编写中常见的错误模式，AI 必须能够识别并报告：

#### 1. 内联定义复杂 Schema
❌ **错误**:
```php
#[OA\Post(
    requestBody: new OA\RequestBody(
        content: new OA\JsonContent(
            properties: [
                new OA\Property(property: 'username', type: 'string') // 禁止内联定义，必须使用 Ref
            ]
        )
    )
)]
```
✅ **正确**: 使用 `ref: LoginRequest::class`

#### 2. 错误的 Path 定义
❌ **错误**: `path: 'auth/login'` (缺少前缀)
✅ **正确**: `path: '/api/web/system/v1/auth/login'` (完整路径)

#### 3. 缺失 BaseResponseBody 继承
❌ **错误**: `class LoginResponse { ... }`
✅ **正确**: `class LoginResponseBody extends BaseResponseBody { ... }`

#### 4. 混合使用 Parameters 和 RequestBody
❌ **错误**: 在 `POST` 请求中使用 `parameters` 传递表单数据。
✅ **正确**: `POST/PUT` 使用 `requestBody`, `GET/DELETE` 使用 `parameters`。

---

## 验证清单

在验证其他项目时，应检查以下内容：

- [ ] **Method Coverage**: 所有控制器方法都有对应的 `#[OA\Get|Post|...]` 注解
- [ ] **Path Match**: `path` 与路由文件定义一致
- [ ] **Ref Usage**: POST/PUT 必须使用 Request/Response 类引用 (Ref)，禁止内联
- [ ] **Inheritance**: ResponseBody 必须继承自 `BaseResponseBody`
- [ ] **Naming**: Request/Response 类名必须符合 `{Function}Request/ResponseBody` 格式
