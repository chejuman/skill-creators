# /devflow2-next

Advance to next version with retrospective and knowledge accumulation.

## Usage

```
/devflow2-next [--skip-retro] [--skip-gate]
```

## Options

- `--skip-retro`: Skip retrospective (not recommended)
- `--skip-gate`: Skip version_ready gate (not recommended)

## What This Does

### Step 1: Run Version Ready Gate

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/quality_gate.py run version_ready
```

### Step 2: Interactive Retrospective

```
AskUserQuestion(questions=[
  {
    "question": "What worked well this version?",
    "header": "Success",
    "options": [
      {"label": "Research quality", "description": "Comprehensive research helped"},
      {"label": "Planning accuracy", "description": "Estimates were accurate"},
      {"label": "Feature selection", "description": "Right features chosen"},
      {"label": "Team velocity", "description": "Good progress rate"}
    ],
    "multiSelect": true
  },
  {
    "question": "What could improve?",
    "header": "Improve",
    "options": [
      {"label": "Research depth", "description": "Needed more research"},
      {"label": "Scope creep", "description": "Features grew unexpectedly"},
      {"label": "Risk management", "description": "Risks not anticipated"},
      {"label": "Time estimates", "description": "Took longer than expected"}
    ],
    "multiSelect": true
  }
])
```

### Step 3: Create Retrospective

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/knowledge_base.py retro ...
```

Automatically extracts:

- Patterns from successes
- Anti-patterns from failures

### Step 4: Update Velocity

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/predictive_analytics.py velocity <features> <days>
```

### Step 5: Self-Upgrade Analysis

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/knowledge_base.py suggest
```

### Step 6: Advance Version

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/master.py advance
```

### Step 7: Archive Current Plan

Move current plan to archive, reset for new version.

### Output

```markdown
## Version Advancement: v{X-1}.0 → v{X}.0

### Completed: v{X-1}.0

| Metric             | Value             |
| ------------------ | ----------------- |
| Features Delivered | 3                 |
| Tasks Completed    | 18                |
| Duration           | 21 days           |
| Velocity           | 1.1 features/week |

### Retrospective Summary

**What Worked:**

- Research quality
- Feature selection

**What Didn't:**

- Scope creep
- Time estimates

### Knowledge Captured

- Patterns Added: 2
- Anti-patterns Added: 1
- Insights Updated: 3

### Self-Upgrade Suggestions

1. **Research**: Increase competitor analysis depth
2. **Planning**: Add buffer for scope changes

### Now: v{X}.0

| Field    | Value         |
| -------- | ------------- |
| Version  | v{X}.0        |
| Status   | Planning      |
| Features | To be defined |

### Progress to v10.0

[█████████████░░░░░░░] 50%

Previous: v{X-1}.0 → Current: v{X}.0 → Target: v10.0

### Velocity Trend

| Version  | Velocity | Trend |
| -------- | -------- | ----- |
| v{X-3}.0 | 0.8/week | -     |
| v{X-2}.0 | 1.0/week | ↗️    |
| v{X-1}.0 | 1.1/week | ↗️    |

### Next Steps

1. `/devflow2-research` - Research for new version
2. `/devflow2-suggest` - Get feature suggestions
3. `/devflow2-status` - View updated dashboard
```

## Milestones

| Version | Milestone  | Status |
| ------- | ---------- | ------ |
| v1.0    | MVP        | ✅     |
| v2.0    | Stability  | ✅     |
| v3.0    | Growth     | 🔄     |
| v5.0    | Maturity   | ⏳     |
| v7.0    | Enterprise | ⏳     |
| v10.0   | Excellence | ⏳     |

## Example

```
/devflow2-next

/devflow2-next --skip-retro
```
