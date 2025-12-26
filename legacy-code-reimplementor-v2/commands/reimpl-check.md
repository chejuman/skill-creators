# /reimpl-check

Verify implementation status of tasks.

## Usage

```
/reimpl-check [options]
```

## Options

- `--task TASK-ID` or `-t TASK-ID`: Verify specific task
- `--all` or `-a`: Verify all tasks
- `--summary` or `-s`: Show summary only

## What This Does

Runs verification checks against Repo B:

```bash
python3 ~/.claude/skills/legacy-code-reimplementor-v2/scripts/verify_task.py --task {TASK-ID}
```

### Verification Checks

1. **Files Exist**: Target files are present in Repo B
2. **Implementation**: Files contain actual code (not stubs)
3. **Tests**: Test files exist for the implementation

### Status Updates

Based on verification:

- Updates `tracking/completion_status.json`
- Logs result in `tracking/verification_log.md`
- Adds gaps to `tracking/gaps_report.md` if failed

## Output Format

### Single Task

```markdown
# Verification Report: TASK-004

**Status:** ✅ PASSED
**Verified:** 2025-01-15T14:30:00

## Check Results

| Check          | Status | Details      |
| -------------- | ------ | ------------ |
| Files Exist    | ✅     | 3/3 files    |
| Implementation | ✅     | 8 functions  |
| Tests          | ✅     | 2 test files |

**Result:** Task verified. Ready for next task.
```

### All Tasks Summary

```markdown
# Full Verification Report

| Task     | Status     |
| -------- | ---------- |
| TASK-001 | ✅ Passed  |
| TASK-002 | ✅ Passed  |
| TASK-003 | ❌ Failed  |
| TASK-004 | ⏳ Pending |

## Summary

| Status    | Count |
| --------- | ----- |
| Completed | 2     |
| Failed    | 1     |
| Pending   | 5     |
| Blocked   | 1     |

**Progress:** 25% complete
```

### When Verification Fails

```markdown
# Verification Report: TASK-003

**Status:** ❌ FAILED

## Check Results

| Check          | Status | Details      |
| -------------- | ------ | ------------ |
| Files Exist    | ❌     | 1/3 files    |
| Implementation | ⚠️     | 0 functions  |
| Tests          | ❌     | 0 test files |

### Missing Files

- `src/models/user.py`
- `src/models/product.py`

### Gaps

- No implementation found in target files
- Missing test coverage

**Action:** Complete implementation before running `/reimpl-next`
```

## Example

```
User: /reimpl-check --task TASK-004

User: /reimpl-check --all

User: /reimpl-check --summary
```
