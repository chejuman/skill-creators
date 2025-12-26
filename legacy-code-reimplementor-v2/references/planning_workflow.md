# Planning-Only Workflow Reference

This skill focuses ONLY on analysis and planning - NO implementation.

## Core Principle

> "Plan twice, implement once."

This workflow generates comprehensive documentation and task breakdowns that can be:

- Executed manually by developers
- Fed to implementation agents
- Reviewed before any code is written

## Workflow Phases

### Phase 1: Analysis

```
┌─────────────────────────────────────────────────────┐
│ INPUT: Repository path                              │
├─────────────────────────────────────────────────────┤
│ 3 Parallel Agents:                                  │
│   ├── Structure Analysis                           │
│   ├── Feature Extraction                           │
│   └── Issue Detection                              │
├─────────────────────────────────────────────────────┤
│ OUTPUT: .reimpl-docs/analysis/                      │
│   ├── structure_analysis.md                        │
│   ├── feature_extraction.md                        │
│   ├── feature_catalog.json                         │
│   ├── dependency_graph.md                          │
│   └── issue_detection.md                           │
└─────────────────────────────────────────────────────┘
```

### Phase 2: Technology Selection

```
┌─────────────────────────────────────────────────────┐
│ INPUT: Analysis results                             │
├─────────────────────────────────────────────────────┤
│ AskUserQuestion:                                    │
│   ├── Target language (with recommendations)       │
│   ├── Target framework                             │
│   └── Architecture pattern                         │
├─────────────────────────────────────────────────────┤
│ OUTPUT: .reimpl-docs/config.json                    │
│   tech_stack: { lang, framework, architecture }    │
└─────────────────────────────────────────────────────┘
```

### Phase 3: Task Generation

```
┌─────────────────────────────────────────────────────┐
│ INPUT: Feature catalog + Tech stack                │
├─────────────────────────────────────────────────────┤
│ Generate:                                           │
│   ├── Implementation plan (phases)                 │
│   ├── Task breakdown (all tasks)                   │
│   └── Individual task files (TASK-XXX.md)          │
├─────────────────────────────────────────────────────┤
│ OUTPUT: .reimpl-docs/                              │
│   ├── plans/implementation_plan.md                 │
│   ├── plans/task_breakdown.md                      │
│   └── tasks/TASK-001.md ... TASK-XXX.md           │
└─────────────────────────────────────────────────────┘
```

## Pre-Task Verification

Before outputting any task, the system verifies:

```
┌─────────────────────────────────────────────────────┐
│ CHECK: Is previous task complete?                   │
├─────────────────────────────────────────────────────┤
│ Verify in Repo B:                                   │
│   ├── Target files exist?                          │
│   ├── Functions implemented?                       │
│   └── Tests written?                               │
├─────────────────────────────────────────────────────┤
│ IF NOT COMPLETE:                                    │
│   ├── Mark task as pending                         │
│   ├── Log gaps in verification_log.md             │
│   ├── Add to gaps_report.md                       │
│   └── Prompt to complete before continuing        │
└─────────────────────────────────────────────────────┘
```

## Document Persistence

All outputs are saved in `.reimpl-docs/`:

```
.reimpl-docs/
├── index.md                  # Quick links to all docs
├── config.json               # Project configuration
│
├── analysis/                 # Phase 1 outputs
│   ├── structure_analysis.md
│   ├── feature_extraction.md
│   ├── feature_catalog.json
│   ├── dependency_graph.md
│   └── issue_detection.md
│
├── plans/                    # Phase 3 outputs
│   ├── implementation_plan.md
│   ├── task_breakdown.md
│   └── architecture_design.md
│
├── tasks/                    # Individual tasks
│   ├── TASK-001.md
│   ├── TASK-002.md
│   └── ...
│
└── tracking/                 # Progress tracking
    ├── completion_status.json
    ├── verification_log.md
    └── gaps_report.md
```

## Task File Format

Each task file contains:

```markdown
# TASK-XXX: Name

## Metadata

| Field        | Value              |
| ------------ | ------------------ |
| ID           | TASK-XXX           |
| Feature      | FEAT-YYY           |
| Priority     | N                  |
| Complexity   | Low/Medium/High    |
| Dependencies | TASK-aaa, TASK-bbb |

## Description

What needs to be implemented.

## Source Reference (Repo A)

Files to analyze in original codebase.

## Target Files (Repo B)

Files to create in new codebase.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Tests Required

- [ ] Test 1
- [ ] Test 2
```

## Slash Commands Summary

| Command          | Purpose                           |
| ---------------- | --------------------------------- |
| `/reimpl-plan`   | Full analysis + plan generation   |
| `/reimpl-next`   | Get next task (with verification) |
| `/reimpl-check`  | Verify task implementation        |
| `/reimpl-search` | Search documentation              |

## Best Practices

1. **Always verify before proceeding** - Don't skip verification
2. **Check gaps regularly** - Review `tracking/gaps_report.md`
3. **Use search** - Find related tasks with `/reimpl-search`
4. **Follow dependencies** - Implement in order
5. **Update status** - Mark tasks complete after verification
