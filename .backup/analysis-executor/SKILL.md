---
name: analysis-executor
description: Execute analysis plans step by step, generating analysis documents and tracking progress. Use when users have an analysis-plan.md and want to execute it, when they say "execute analysis", "analyze phase X", "generate document N", "continue analysis", or when working through a structured code analysis workflow.
---

# Analysis Executor

Execute analysis plans systematically, generating documents and tracking progress.

## Prerequisites

Requires an existing analysis plan with:
- `analysis-plan.md` - Document specifications
- `README.md` - Progress tracking table

## Workflow

1. **Load** - Read analysis plan and current progress
2. **Analyze** - Generate specified document(s)
3. **Update** - Update progress tracking

## Step 1: Load Context

```bash
# Read the analysis plan
cat analysis-plan.md

# Check current progress
cat README.md
```

Identify:
- Which phase is in progress
- Which document to generate next
- Document requirements from the plan

## Step 2: Generate Analysis Document

For each document, follow this process:

### 2.1 Locate Relevant Code

```bash
# Find related files
find . -type f -name "*.go" | xargs grep -l "keyword"

# Explore specific directories
ls -la path/to/module/

# Read key files
cat path/to/file.go
```

### 2.2 Analyze Systematically

Follow the requirements in the analysis plan. For each document:

1. **Understand purpose** - What does this code do?
2. **Map structure** - How is it organized?
3. **Trace flows** - How does data/control flow?
4. **Identify patterns** - What design patterns are used?
5. **Note insights** - What non-obvious decisions were made?

### 2.3 Write the Document

Use the standard document structure. See `references/document-structure.md` for templates.

**Essential elements:**
- Clear section headers
- Code examples with explanations
- Mermaid diagrams for complex flows
- File paths for code references
- Performance and design considerations

## Step 3: Update Progress

After completing each document:

### Update README.md Progress Table

```markdown
| 阶段 | 状态 | 完成度 | 备注 |
|------|------|--------|------|
| 第1阶段：基础架构 | 已完成 | 100% | ✓ |
| 第2阶段：核心服务 | 进行中 | 40% | 已完成 04, 05 |
```

### Update Document Checklist

```markdown
- [x] 01-architecture-overview.md
- [x] 02-infrastructure.md
- [ ] 03-authentication.md  ← Next
```

### Status Values

- `待开始` - Not started (0%)
- `进行中` - In progress (1-99%)
- `已完成` - Completed (100%)

## Execution Modes

**Single document**: "Generate document 05"
→ Generate only the specified document

**Phase execution**: "Execute phase 2"
→ Generate all documents in the phase sequentially

**Continue**: "Continue analysis"
→ Pick up from the next incomplete document

**Full execution**: "Execute entire plan"
→ Generate all remaining documents

## Quality Checklist

Before completing a document, verify:

- [ ] All requirements from analysis-plan.md are addressed
- [ ] Code examples include file paths
- [ ] Complex flows have diagrams
- [ ] Non-obvious design decisions are explained
- [ ] Performance implications are noted
- [ ] Document follows standard structure

## Commands Reference

```bash
# Search for patterns
grep -r "pattern" --include="*.go" ./path

# Find function definitions
grep -rn "func.*FunctionName" --include="*.go"

# Count occurrences
grep -c "pattern" file.go

# View file structure
tree -L 2 ./path

# Find interfaces
grep -rn "type.*interface" --include="*.go"
```
