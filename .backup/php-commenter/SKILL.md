---
name: php-commenter
description: Generate php swagger schema. Triggers include "create php comment"
---

# Php Commenter

## Overview

This skill helps user write swagger comment, Used to generate request schema, response schema, api schema.

## Workflow

1. **Explore** - Find file to used generate.
2. **Design** - Write Request schema, response schema, api schema.
3. **Output** - Use `php82 artisan core:doc api` to generate swagger doc.

## Step 1: Explore the Codebase

- **Entry** : All files use `Controller` suffix.
  - **Method** : Find public method to write url schema.
- **Source File** : All source file at `modules/[module]/src` Directory
- **Entry** : Entry File At `modules/[module]/src/Http` Directory, 
  - **Controller** : All need parsed controller file at `modules/[module]/src/Http/Request/Web` and `modules/[module]/src/Http/Request/Api` Directory
  - **Route** : All route file at `modules/[module]/src/Http/Routes` Directory
- **Features** : File At `modules/[module]/src/Action` Directory
- **User Story** : Method At `modules/[module]/src/Action` file, and each method should have a comment above it, describe the method and its parameters
- **顺序** : 依次分析每个模块, 先分析入口文件, 路由文件, 控制器文件, 最后分析功能文件和依赖

## Step 2: Design Phased Plan

Organize analysis into logical phases. See `references/templates.md` for common patterns.

**Phase design principles:**
- Start Modular, then go deep (features / user story)
- Group related features or user stories together
- Order phases by dependency (analyze dependencies before dependents)
- Each document should be completable in one session

## Step 3: Generate Output Files

Create two files in the analysis output directory:

### analysis-plan.md

Structure:
```markdown
# [Project Name] 代码分析计划

## 项目概述
[Brief description of project, tech stack, architecture type]

## 模块：[module-name] (N个文档)

### 01-[document-name].md
**目标**: [What this document aims to understand]
**要求**:
- [Specific feature 1]
   - [Brife user story 1 under feature 1]
   - [Brife user story 2 under feature 1]
- [Specific feature 2]

### 02-[document-name].md
...


### progress-tracking.md (Progress Tracking)

Structure:
```markdown
# [Project Name] 代码分析

## 进度总览

### 模块1 [module-name] 进度
| 阶段 | 状态 | 完成度 | 备注 |
|------|------|--------|------|
| Feature 1: [Name] | 待开始 | 0% | |
| Feature 2: [Name] | 待开始 | 0% | |
...

### 模块2 [module-name] 进度
| 阶段 | 状态 | 完成度 | 备注 |
|------|------|--------|------|
| Feature 1: [Name] | 待开始 | 0% | |
| Feature 2: [Name] | 待开始 | 0% | |
...

## 文档清单

- [ ] 01-[name].md
- [ ] 02-[name].md
...
