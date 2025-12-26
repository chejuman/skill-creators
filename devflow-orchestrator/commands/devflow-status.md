# /devflow-status

Show current project state and progress.

## Usage

```
/devflow-status [--verbose]
```

## Options

- `--verbose` or `-v`: Show detailed metrics and history

## What This Does

### Step 1: Load Project State

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py status
```

### Step 2: Load Metrics

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/self_upgrade.py analyze
```

### Step 3: Calculate Progress

- Current version vs target (v10.0)
- Features completed vs planned
- Research coverage

### Output

```markdown
# DevFlow Status

## Project

- **Idea**: {idea}
- **Domain**: {domain}
- **Current Version**: v{X}.0
- **Target**: v10.0

## Progress

[========>----------] 30% toward v10.0

## Current Version: v{X}.0

### Features

| Feature   | Priority | Status      |
| --------- | -------- | ----------- |
| Feature A | Must     | In Progress |
| Feature B | Should   | Planned     |

### Tasks

- Total: N
- Completed: M
- In Progress: K
- Pending: L

## Metrics

| Metric              | Value |
| ------------------- | ----- |
| Cycles Completed    | X     |
| Features Planned    | Y     |
| Research Sessions   | Z     |
| Effectiveness Score | W/100 |

## Version History

| Version | Status   | Features         |
| ------- | -------- | ---------------- |
| v0.0    | Complete | Idea             |
| v1.0    | Complete | MVP (3 features) |
| v2.0    | Current  | 2 features       |

## Research Coverage

- [x] Tech Stack
- [x] Market Trends
- [ ] Open Source
- [x] Security
- [ ] Competitors

## Actions Available

| Command             | Purpose                   |
| ------------------- | ------------------------- |
| `/devflow-research` | Fill research gaps        |
| `/devflow-suggest`  | Get feature suggestions   |
| `/devflow-plan`     | Generate development plan |
| `/devflow-next`     | Advance to next version   |
```

## Example

```
User: /devflow-status

User: /devflow-status --verbose
```
