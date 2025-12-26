# /devflow2-status

Show premium analytics dashboard with predictions.

## Usage

```
/devflow2-status [--analytics] [--gates]
```

## Options

- `--analytics`: Show detailed analytics
- `--gates`: Show quality gate status

## What This Does

### Step 1: Load Project State

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/master.py status
```

### Step 2: Load Analytics Dashboard

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/predictive_analytics.py dashboard
```

### Step 3: Load Quality Gates

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/quality_gate.py status
```

### Step 4: Load Knowledge Summary

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/knowledge_base.py recommend
```

### Output

```markdown
# DevFlow V2 Dashboard

## Project Overview

| Field           | Value       |
| --------------- | ----------- |
| Idea            | {idea}      |
| Domain          | {domain}    |
| Complexity      | Level {X}/5 |
| Current Version | v{X}.0      |
| Target          | v10.0       |

## Progress to v10.0

[████████████░░░░░░░░] 40%

Current: v4.0 | Target: v10.0

## Velocity & Predictions

| Metric           | Value             | Trend          |
| ---------------- | ----------------- | -------------- |
| Current Velocity | 1.2 features/week | ↗️             |
| Next Version     | {date}            | 75% confidence |
| Target v10.0     | {date}            | 60% confidence |

## Quality Gates

| Gate              | Status | Pass Rate |
| ----------------- | ------ | --------- |
| research_complete | ✅     | 100%      |
| analysis_complete | ✅     | 100%      |
| plan_validated    | ⏳     | -         |
| version_ready     | ⏳     | -         |

## Feature Burndown

| Category      | Count |
| ------------- | ----- |
| Total Planned | 15    |
| Completed     | 6     |
| In Progress   | 2     |
| Remaining     | 7     |

Progress: [████████░░░░░░░░] 40%

## Current Version: v{X}.0

### Features

| Feature   | Priority | Status         |
| --------- | -------- | -------------- |
| Feature A | Must     | ✅ Complete    |
| Feature B | Should   | 🔄 In Progress |
| Feature C | Could    | ⏳ Pending     |

### Workflow Phase

Current: {phase}

## Knowledge Summary

- Patterns Collected: {X}
- Domain Insights: {Y}
- Retrospectives: {Z}

## Risks

| Risk    | Severity |
| ------- | -------- |
| {risk1} | High     |
| {risk2} | Medium   |

## Actions

| Command              | Purpose            |
| -------------------- | ------------------ |
| `/devflow2-research` | Fill research gaps |
| `/devflow2-analyze`  | Run analysis       |
| `/devflow2-suggest`  | Get features       |
| `/devflow2-plan`     | Generate plan      |
| `/devflow2-gate`     | Run quality check  |
| `/devflow2-next`     | Advance version    |
```

## Example

```
/devflow2-status

/devflow2-status --analytics

/devflow2-status --gates
```
