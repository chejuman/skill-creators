# /spec-status Command

Show overall specification and implementation progress.

## Usage

```bash
/spec-status
/spec-status --detailed
/spec-status --phase
```

## Arguments

| Argument     | Description              |
| ------------ | ------------------------ |
| `--detailed` | Show all task details    |
| `--phase`    | Show phase-level summary |
| `--json`     | Output as JSON           |

## Workflow

### Generate Report

```bash
python3 scripts/update_status.py --report --path .
```

### Load Config

Read `.spec-docs/config.json` for phase status.

### Load Completion

Read `.spec-docs/tracking/completion_status.json` for task status.

## Output Format

```markdown
# Feature Spec Status: user-authentication

**Generated:** 2025-12-28 15:30

## Phase Progress

| Phase     | Status      | Progress |
| --------- | ----------- | -------- |
| DISCOVER  | ✅ Complete | 100%     |
| SPEC      | ✅ Complete | 100%     |
| PLAN      | ✅ Complete | 100%     |
| IMPLEMENT | 🔄 Active   | 42%      |

## Implementation Progress
```

[========..............] 42%

```

| Metric      | Count |
| ----------- | ----- |
| Total Tasks | 12    |
| Completed   | 5     |
| In Progress | 1     |
| Pending     | 6     |

## Current Task

**TASK-006:** Implement password hashing

## Recently Completed

- ✅ TASK-005: Create user model (2h ago)
- ✅ TASK-004: Setup database schema (4h ago)

## Blocked Tasks

- ⏸️ TASK-010: Blocked by TASK-008

## Next Steps

1. Complete TASK-006
2. Run `/spec-check --task TASK-006`
3. Continue with `/spec-next`

---

Documentation: `.spec-docs/`
```

## Related Commands

| Command        | Purpose       |
| -------------- | ------------- |
| `/spec-next`   | Get next task |
| `/spec-check`  | Verify task   |
| `/spec-search` | Search docs   |
