# 更新日志

## v2.0 - 2023-12-17

### 🎯 简化目录结构

**变更前**:
```
.role-hub/
├── artifacts/
│   └── <任务名>/
│       ├── index.json
│       ├── pm-prd-任务名-YYYYMMDD.md
│       ├── arch-design-任务名-YYYYMMDD.md
│       └── ...
├── context/
│   └── <任务名>.json
└── templates/
```

**变更后**:
```
.role-hub/
├── pm-YYYYMMDD-HHMMSS.md
├── arch-YYYYMMDD-HHMMSS.md
├── ui-YYYYMMDD-HHMMSS.md
├── dev-YYYYMMDD-HHMMSS.md
├── qa-YYYYMMDD-HHMMSS.md
├── context.json
└── templates/
```

### ✨ 主要改进

1. **去掉任务名子目录** - 所有文档直接保存在 `.role-hub/` 下
2. **简化文件命名** - `<角色>-<时间戳>.md`,去掉任务名
3. **统一上下文管理** - 使用单一的 `context.json` 文件
4. **简化命令参数** - 移除大部分命令的任务名参数

### 📝 命令变更

#### doc_generator.py

**之前**:
```bash
python3 doc_generator.py generate PM 用户积分系统
```

**现在**:
```bash
python3 doc_generator.py generate PM
# 或带任务名(可选,用于填充模板变量)
python3 doc_generator.py generate PM "用户积分系统"
```

#### context_manager.py

**之前**:
```bash
# 保存
python3 context_manager.py save 任务名 DEV '{"data": "..."}'
# 加载
python3 context_manager.py load 任务名
# 检查
python3 context_manager.py check DEV 任务名
# 查看产出物
python3 context_manager.py artifacts 任务名 DEV
```

**现在**:
```bash
# 保存
python3 context_manager.py save DEV '{"data": "..."}'
# 加载
python3 context_manager.py load
# 清除
python3 context_manager.py clear
# 检查
python3 context_manager.py check DEV
# 列出产出物
python3 context_manager.py list
python3 context_manager.py list PM
```

### 🎨 文件命名规则

- **时间戳格式**: `YYYYMMDD-HHMMSS` (精确到秒)
- **文件名格式**: `<角色小写>-<时间戳>.md`
- **示例**:
  - `pm-20231217-143025.md`
  - `arch-20231217-143530.md`
  - `dev-20231217-144020.md`

### 💡 为什么简化?

在实际项目中使用时,发现:
1. **任务名子目录冗余** - 项目本身就是一个具体任务
2. **文件名过长** - 包含任务名导致文件名很长
3. **命令复杂** - 每次都要输入任务名
4. **目录层级深** - artifacts/任务名/ 两层目录不必要

简化后:
- ✅ 目录结构扁平,一目了然
- ✅ 文件名简洁,易于管理
- ✅ 命令简单,提高效率
- ✅ 时间戳命名,自然排序

### 📚 更新的文档

- `README.md` - 完全重写,反映新结构
- `USAGE_GUIDE.md` - 完全重写,简化示例
- `doc_generator.py` - 简化输出路径和参数
- `context_manager.py` - 简化目录结构和命令

### ⚠️ 注意事项

- 文件名包含时间戳,按修改时间自然排序
- 使用 `context_manager.py list` 可查看所有产出物
- 旧版本的数据不兼容,需要手动迁移

---

## v1.0 - 2023-12-10 (初始版本)

- ✅ 创建角色切换系统
- ✅ 建立文档模板
- ✅ 实现上下文管理
- ✅ 添加前置条件检查
