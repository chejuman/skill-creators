# /devflow-next

Advance project to next version after completing current version.

## Usage

```
/devflow-next [--skip-check]
```

## Options

- `--skip-check`: Skip completion verification (not recommended)

## What This Does

### Step 1: Verify Current Version Completion

Check that current version features are complete:

- All selected features implemented
- No blocking issues in backlog
- User confirmation if incomplete

### Step 2: Self-Upgrade Analysis

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/self_upgrade.py report
```

Review workflow effectiveness before advancing:

- Research coverage gaps
- Scoring completeness
- Process improvements

### Step 3: Log Version Completion

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py log_decision "Version X.0 complete" "<summary>"
```

### Step 4: Advance Version

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py advance
```

Increments version:

- v0.0 → v1.0 (MVP)
- v1.0 → v2.0
- v2.0 → v3.0
- ...

### Step 5: Create New Version File

Creates `.devflow/versions/v{X}.0.md` with:

- Version number
- Creation timestamp
- Feature placeholders
- Status checklist

### Step 6: Output Transition Summary

```markdown
## Version Advancement

### Completed: v{X-1}.0

- Features delivered: N
- Tasks completed: M
- Duration: Y weeks

### Now: v{X}.0

- Status: Planning
- Features: To be defined

### Self-Upgrade Insights

- Effectiveness Score: Z/100
- Improvements Applied: [list]

### Next Steps

1. `/devflow-research` - Research for new version
2. `/devflow-suggest` - Get feature suggestions
3. `/devflow-status` - View updated state

### Progress to v10.0

[=========>---------] 40% (v4.0)
```

## Milestones

| Version | Milestone                       |
| ------- | ------------------------------- |
| v1.0    | MVP - Core functionality        |
| v2.0    | Stability - Bug fixes, polish   |
| v3.0    | Growth - Key integrations       |
| v5.0    | Maturity - Full feature set     |
| v7.0    | Scale - Performance, enterprise |
| v10.0   | Excellence - Industry leader    |

## Example

```
User: /devflow-next

User: /devflow-next --skip-check
```
