# /reimpl-next

Get the next task with pre-verification of previous task.

## Usage

```
/reimpl-next [--skip-verify]
```

## Options

- `--skip-verify`: Skip verification of current task (use with caution)

## What This Does

### Step 1: Pre-Verification

Before providing the next task, verifies the current in-progress task:

```bash
python3 ~/.claude/skills/legacy-code-reimplementor-v2/scripts/verify_task.py --next
```

Verification checks:

- Target files exist in Repo B
- Functions/classes are implemented (not just stubs)
- Test files exist

### Step 2: Handle Verification Result

**If Verification PASSES:**

- Mark current task as completed
- Find next pending task with satisfied dependencies
- Output the next task details

**If Verification FAILS:**

- Mark current task as still pending
- Add gaps to `tracking/gaps_report.md`
- Log in `tracking/verification_log.md`
- Prompt to fix before continuing

### Step 3: Output Next Task

Displays full task details including:

- Task ID, name, description
- Source files to reference
- Target files to create
- Acceptance criteria
- Dependencies status

## Output Format

### When Verification Passes

```markdown
## Pre-Verification: TASK-003 ✅ PASSED

All checks passed.

---

## Next Task: TASK-004

# TASK-004: User Repository

| Field      | Value  |
| ---------- | ------ |
| Priority   | 2      |
| Complexity | Medium |

## Source Reference

- legacy/dao/UserDAO.java

## Target Files

- src/repositories/user_repository.py

## Acceptance Criteria

- [ ] CRUD operations
- [ ] Query methods
- [ ] Unit tests

---

After implementation: `/reimpl-check --task TASK-004`
```

### When Verification Fails

```markdown
## Pre-Verification: TASK-003 ❌ FAILED

### Gaps Found

- Missing: src/models/user.py
- Missing: tests/test_user_model.py

This task has been added back to pending.

### Action Required

Complete TASK-003 before proceeding.

Use `/reimpl-next --skip-verify` to force next task (not recommended).
```

### When All Tasks Complete

```markdown
## All Tasks Completed! 🎉

All {N} tasks have been verified as complete.

### Next Steps

1. Run final validation suite
2. Review `.reimpl-docs/tracking/gaps_report.md`
3. Generate final migration report
```

## Example

```
User: /reimpl-next
```
