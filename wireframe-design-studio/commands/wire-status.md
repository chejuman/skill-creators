# /wire-status

Show current wireframe implementation progress and status report.

## Usage

```
/wire-status
/wire-status --format json
```

## Workflow

1. **Generate Status Report**

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/task_tracker.py status
   ```

2. **Display Progress**

## Output

```markdown
# Wireframe Implementation Status

**Generated:** 2024-12-29 10:30

## Progress

| Metric      | Count |
| ----------- | ----- |
| Total Tasks | 12    |
| Completed   | 5     |
| In Progress | 1     |
| Pending     | 6     |

**Progress:** 41.7%
```

[========............] 41.7%

```

## Task Details

- [x] **TASK-001**: completed
- [x] **TASK-002**: completed
- [-] **TASK-003**: in_progress
- [ ] **TASK-004**: pending

## Current Task

**TASK-003** (in progress)

## Next Task

**TASK-004** is ready to start.
```

## Options

| Option        | Description                        |
| ------------- | ---------------------------------- |
| --format json | Output as JSON instead of markdown |

## Related Commands

- `/wire-next` - Get next task
- `/wire-list` - List all wireframes
