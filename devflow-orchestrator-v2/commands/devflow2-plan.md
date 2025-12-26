# /devflow2-plan

Generate detailed development plan with predictive analytics.

## Usage

```
/devflow2-plan [--version X.0] [--detailed]
```

## Options

- `--version X.0`: Target version (default: next version)
- `--detailed`: Include detailed task breakdowns

## What This Does

### Step 1: Load Selected Features

Load features from backlog with "selected" status.

### Step 2: Planning Coordinator

Planning Coordinator generates comprehensive plan:

```
Task(subagent_type='Plan',
     description='Generate development plan',
     prompt='Create detailed plan for selected features with:
             - Architecture design
             - Task decomposition (5-10 per feature)
             - Dependency mapping
             - Critical path analysis
             - Risk mitigation strategies')
```

### Step 3: Task Decomposition

For each feature, generate 5-10 subtasks:

```markdown
## Feature: User Authentication

### Tasks

| ID    | Task            | Effort | Dependencies | Risk   |
| ----- | --------------- | ------ | ------------ | ------ |
| T-001 | Database schema | 0.5d   | -            | Low    |
| T-002 | API endpoints   | 1d     | T-001        | Medium |
| T-003 | Frontend forms  | 1d     | T-002        | Low    |
| T-004 | Session mgmt    | 0.5d   | T-002        | Medium |
| T-005 | Unit tests      | 1d     | T-002,T-003  | Low    |
```

### Step 4: Dependency Graph

Generate dependency visualization:

```
T-001 ──► T-002 ──┬──► T-003
                  │
                  └──► T-004

         T-002 + T-003 ──► T-005
```

### Step 5: Predictive Analytics

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/predictive_analytics.py predict
```

Calculate:

- Estimated completion date
- Confidence interval
- Velocity projection
- Risk factors

### Step 6: Save Plan

Save to `.devflow/plans/current/v{X}.0_plan.md`

### Step 7: Quality Gate Check

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/quality_gate.py run plan_validated
```

### Output

```markdown
## Development Plan: v{X}.0

### Overview

| Metric      | Value   | Confidence |
| ----------- | ------- | ---------- |
| Features    | 3       | -          |
| Total Tasks | 18      | -          |
| Effort      | 15 days | ±3 days    |
| Duration    | 3 weeks | 75%        |

### Features

1. **Feature A** (Must)
   - Tasks: 6
   - Effort: 5 days
   - Risk: Low

2. **Feature B** (Should)
   - Tasks: 7
   - Effort: 6 days
   - Risk: Medium

### Critical Path

T-001 → T-002 → T-005 → T-008 → T-012

**Critical Path Duration**: 12 days

### Predictions

| Metric        | Prediction        | Confidence |
| ------------- | ----------------- | ---------- |
| Completion    | {date}            | 75%        |
| Velocity      | 1.2 features/week | 80%        |
| Risk of Delay | 25%               | -          |

### Risk Mitigation

| Risk            | Strategy        | Owner |
| --------------- | --------------- | ----- |
| Tech complexity | Spike first     | Dev   |
| Dependencies    | Parallel tracks | Lead  |

### Quality Gate: plan_validated

Status: ✅ PASSED (100%)

### Next Steps

1. Begin implementation (external)
2. `/devflow2-status` - Track progress
3. `/devflow2-next` - Advance when complete
```

## Example

```
/devflow2-plan

/devflow2-plan --version 2.0 --detailed
```
