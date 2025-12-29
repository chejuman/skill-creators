# /spec-check Command

Verify task completion status.

## Usage

```bash
/spec-check
/spec-check --task TASK-001
/spec-check --all
```

## Arguments

| Argument    | Description               |
| ----------- | ------------------------- |
| `--task ID` | Check specific task       |
| `--all`     | Check all tasks           |
| `--update`  | Update status after check |

## Workflow

### Single Task Verification

```bash
python3 scripts/verify_task.py --task TASK-001 --path . --update-status
```

Checks:

- Target files exist in codebase
- Tests written for the task
- Acceptance criteria met

### All Tasks Verification

```bash
for task in .spec-docs/tasks/TASK-*.md; do
  python3 scripts/verify_task.py --task $(basename $task .md) --path .
done
```

## Output Format

### Single Task

```markdown
## Verification: TASK-001 ✅ PASSED

### Checks

- ✅ files_exist: All target files created
- ✅ tests_written: Test files present
- ✅ criteria_met: Acceptance criteria satisfied

### Files Verified

| File                 | Status |
| -------------------- | ------ |
| src/services/auth.py | ✅     |
| tests/test_auth.py   | ✅     |
```

### All Tasks

```markdown
## Verification Report

| Task     | Status     | Files | Tests | Criteria |
| -------- | ---------- | ----- | ----- | -------- |
| TASK-001 | ✅ Passed  | ✅    | ✅    | ✅       |
| TASK-002 | ✅ Passed  | ✅    | ✅    | ✅       |
| TASK-003 | ❌ Failed  | ✅    | ❌    | ❌       |
| TASK-004 | ⏳ Pending | -     | -     | -        |

### Summary

- Completed: 2/4
- Failed: 1
- Pending: 1
```

## Logging

Verification results logged to:

- `.spec-docs/tracking/verification_log.md`
- `.spec-docs/tracking/gaps_report.md` (if gaps found)

## Error Handling

| Situation          | Action                          |
| ------------------ | ------------------------------- |
| Task not found     | Show available task IDs         |
| No .spec-docs      | Prompt to run `/spec-dev` first |
| Verification fails | Log gaps and suggest fixes      |
