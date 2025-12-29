# /spec-status

Show current feature specification implementation progress.

## Usage

```
/spec-status
/spec-status --format json
```

## Workflow

1. **Generate Status Report**

   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/task_tracker.py status
   ```

2. **Display Progress**

## Output

```markdown
# Feature Spec Implementation Status

**Generated:** 2025-12-29 14:30
**Feature:** user-authentication

## Phase Progress

| Phase    | Status         |
| -------- | -------------- |
| DISCOVER | ✅ completed   |
| ANALYZE  | ✅ completed   |
| DESIGN   | ✅ completed   |
| PLAN     | ✅ completed   |
| VERIFY   | 🔄 in_progress |

## Task Progress

| Metric      | Count |
| ----------- | ----- |
| Total Tasks | 8     |
| Completed   | 4     |
| In Progress | 1     |
| Pending     | 3     |

**Progress:** 50.0%
```

[==========..........] 50.0%

```

## Task Details

- [x] **TASK-001**: completed
- [x] **TASK-002**: completed
- [x] **TASK-003**: completed
- [x] **TASK-004**: completed
- [-] **TASK-005**: in_progress
- [ ] **TASK-006**: pending
- [ ] **TASK-007**: pending
- [ ] **TASK-008**: pending

## Current Task

**TASK-005** (in progress)

## Next Task

**TASK-006** is ready to start.
```

## Options

| Option        | Description    |
| ------------- | -------------- |
| --format json | Output as JSON |

## Related Commands

- `/spec-next` - Get next task
- `/spec-check` - Verify task
