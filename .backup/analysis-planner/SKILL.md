---
name: analysis-planner
description: Create structured analysis plans for codebases. Use when users want to analyze a codebase systematically, create analysis roadmaps, plan code reviews, or generate documentation plans. Triggers include "create analysis plan", "plan code analysis", "analyze this codebase", "create documentation roadmap", or when users provide a codebase and want a structured approach to understanding it.
---

# Code Analysis Planner

Create comprehensive, phased analysis plans for any codebase.

## Workflow

1. **Explore** - Understand project structure and tech stack
2. **Design** - Create phased analysis plan with document specifications
3. **Output** - Generate analysis-plan.md and progress-tracking README

## Step 1: Explore the Codebase

Run initial exploration:

```bash
# Project structure
tree -L 3 -d

# Identify languages
find . -type f \( -name "*.go" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" \) | head -20

# Find entry points
find . -name "main.*" -o -name "index.*" -o -name "app.*" | head -10

# Check for config files
ls -la | grep -E "(config|docker|k8s|yaml|yml|json)"
```

Identify:
- **Tech stack**: Languages, frameworks, dependencies
- **Architecture**: Monolith, microservices, modular
- **Key components**: Services, modules, packages
- **Infrastructure**: Databases, message queues, caches

## Step 2: Design Phased Plan

Organize analysis into logical phases. See `references/phase-templates.md` for common patterns.

**Phase design principles:**
- Start broad (architecture), then go deep (implementation)
- Group related components together
- Order phases by dependency (analyze dependencies before dependents)
- Each document should be completable in one session

**Document sizing:**
- Small doc: 1 component, focused scope
- Medium doc: 2-3 related components or one complex component
- Large doc: Cross-cutting concern or summary

## Step 3: Generate Output Files

Create two files in the analysis output directory:

### analysis-plan.md

Structure:
```markdown
# [Project Name] 代码分析计划

## 项目概述
[Brief description of project, tech stack, architecture type]

## 第一阶段：[Phase Name] (N个文档)

### 01-[document-name].md
**目标**: [What this document aims to understand]
**要求**:
- [Specific requirement 1]
- [Specific requirement 2]
- [Code/diagrams to include]

### 02-[document-name].md
...

## 第N阶段：...

## 文档质量标准
[Standards all documents should meet]

## 分析方法
[Recommended approaches for this codebase]
```

### README.md (Progress Tracking)

Structure:
```markdown
# [Project Name] 代码分析

## 进度总览

| 阶段 | 状态 | 完成度 | 备注 |
|------|------|--------|------|
| 第1阶段：[Name] | 待开始 | 0% | |
| 第2阶段：[Name] | 待开始 | 0% | |
...

## 文档清单

- [ ] 01-[name].md
- [ ] 02-[name].md
...

## 快速开始
[Instructions for using the analysis-executor skill]
```

## Common Phase Patterns

For detailed phase templates by project type, see `references/phase-templates.md`.

**Typical phase sequence:**
1. Infrastructure/Foundation
2. Core Services/Modules
3. Data Flow/Processing
4. External Interfaces (APIs, Webhooks)
5. Storage/Persistence
6. Performance/Reliability
7. Deployment/Operations
8. Summary/Best Practices
