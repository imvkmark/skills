---
name: prd-generator-doc
description: Generate structured product requirement documents (PRD) and functional specifications from code, ideas, or descriptions. Use when: (1) User wants to document product features or requirements, (2) User provides code and needs functional documentation, (3) User requests PRD, BRD, functional spec, or requirements document, (4) User asks to document features, products, or systems,  Triggers include "generat prd X"
---

# Product Requirement Doc Generator

## Overview

This skill helps generate comprehensive, structured product requirement documents from various inputs (code, descriptions, existing documents). It follows a systematic workflow to gather context, analyze requirements, and produce professional documentation.

## Prerequisites

Requires an existing analysis plan with:
- `prd-analysis-plan.md` - Document specifications
- `progress-tracking.md` - Progress tracking table

## Workflow

1. **Load** - Read analysis plan and current progress
2. **Analyze** - Generate specified document(s)
3. **Update** - Update progress tracking

## Step 1: Load Context

Identify:
- Which phase is in progress
- Which document to generate next
- Document requirements from the plan

## Step 2: Generate Analysis Document

For each document, follow this process:

### 2.1 Locate Relevant Code

```bash
# Explore specific directories
ls -la path/to/module/src/
```

### 2.2 Analyze Systematically

Follow the requirements in the analysis plan. For each document:

1. **Understand purpose** - What does this code do?
2. **Map structure** - How is it organized?
3. **Trace flows** - How does data/control flow?
4. **Note insights** - What non-obvious decisions were made?
5. **Core Functionality**: What does the system/feature do?
6. **User Flows**: How do users interact with it?
7. **Data Models**: What data is involved?
8. **Business Logic**: What rules govern behavior?
9. **Dependencies**: What does it rely on?
10. **Edge Cases**: What special scenarios exist?

If analyzing code, examine:
- Function/class names
- Comments and docstrings

### 2.3 Write the Document

Use the standard document structure. See `references/templates.md` for templates.

**Essential elements:**
- Clear section headers
- Mermaid diagrams for complex flows


## Step 3: Update Progress

After completing each document:

### Update progress-tracking.md Progress Table

```markdown
| 阶段 | 状态 | 完成度 | 备注 |
|------|------|--------|------|
| 01-商品管理核心功能 | 已完成 | 100% | ✓ |
| 02-商品共享与回收 | 进行中 | 40% | 已完成 04, 05 |
```

### Update Document Checklist

```markdown
- [x] 01-商品管理核心功能.md
- [x] 02-商品共享与回收.md
- [ ] 03-....md  ← Next
```

### Status Values

- `待开始` - Not started (0%)
- `进行中` - In progress (1-99%)
- `已完成` - Completed (100%)

## Execution Modes

**Single document**: "Generate prd 05"
→ Generate only the specified document

**Phase execution**: "Execute prd feature 2"
→ Generate all documents in the feature sequentially

**Continue**: "Continue prd analysis"
→ Pick up from the next incomplete document

**Full execution**: "Execute entire prd plan"
→ Generate all remaining documents

## Quality Checklist

Before completing a document, verify:

- [ ] All requirements from prd-analysis-plan.md are addressed
- [ ] Complex flows have diagrams
- [ ] Document follows standard structure
