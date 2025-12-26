# /devflow-plan

Generate development plan with task decomposition.

## Usage

```
/devflow-plan [--version X.0]
```

## Options

- `--version X.0`: Target version (default: next version)

## What This Does

### Step 1: Load Selected Features

Load features from backlog with status "selected" for target version.

### Step 2: Architecture Design

For each feature, generate:

- High-level architecture
- Component breakdown
- Integration points
- Technical decisions

### Step 3: Task Decomposition

Break each feature into 5-10 subtasks:

```markdown
## Feature: User Authentication

### Tasks

1. **TASK-001**: Database schema design
   - Effort: 0.5 days
   - Dependencies: None

2. **TASK-002**: API endpoint implementation
   - Effort: 1 day
   - Dependencies: TASK-001

3. **TASK-003**: Frontend login component
   - Effort: 1 day
   - Dependencies: TASK-002

4. **TASK-004**: Session management
   - Effort: 0.5 days
   - Dependencies: TASK-002

5. **TASK-005**: Unit tests
   - Effort: 1 day
   - Dependencies: TASK-002, TASK-003
```

### Step 4: Dependency Mapping

Generate dependency graph:

```
TASK-001 ─┬─► TASK-002 ─┬─► TASK-003
          │             │
          │             └─► TASK-004
          │
          └─────────────────► TASK-005
```

### Step 5: Risk Assessment

Identify risks for each feature:

- Technical complexity
- External dependencies
- Knowledge gaps
- Time constraints

### Step 6: Save Plan

Save to `.devflow/plans/`:

- `v{X}.0_plan.md` - Full development plan
- `v{X}.0_tasks.json` - Machine-readable tasks

### Output

```markdown
## Development Plan: v{X}.0

### Features Included

1. Feature A (Must)
2. Feature B (Should)

### Task Summary

| Task     | Feature | Effort | Dependencies |
| -------- | ------- | ------ | ------------ |
| TASK-001 | A       | 0.5d   | -            |
| TASK-002 | A       | 1d     | TASK-001     |

...

### Timeline

- Total Effort: X person-days
- Recommended Duration: Y weeks

### Risks

1. [Risk description] - Mitigation: [strategy]

### Next Steps

1. Begin implementation (external to DevFlow)
2. `/devflow-status` - Track progress
3. `/devflow-next` - Advance to next version when complete
```

## Example

```
User: /devflow-plan

User: /devflow-plan --version 2.0
```
