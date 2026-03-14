---
name: prd-planner
description: Generate structured product requirement documents (PRD) and functional specifications from code. Use when (1) User wants to document product features or requirements, (2) User requests PRD, BRD, functional spec, or requirements document, (3) User asks to document features, products, or systems. Triggers include "create prd analysis plan"
---

# Product Requirement Doc Planner

## Overview

This skill helps plan comprehensive, structured product requirement documents from various inputs codebase. It follows a systematic workflow to gather context, analyze requirements, and produce professional documentation.

## Workflow

1. **Explore** - Understand project structure / entry point
2. **Design** - Create phased prd analysis plan with document specifications
3. **Output** - Generate `prd-analysis-plan.md` and progress-tracking `progress-tracking.md`

## Step 1: Explore the Codebase

- **Position** : All modular under `modules` folder
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
