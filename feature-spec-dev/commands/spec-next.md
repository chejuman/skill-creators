# /spec-next Command

Get next implementation task with pre-verification.

## Usage

```bash
/spec-next
/spec-next --skip-verify
```

## Arguments

| Argument        | Description                     |
| --------------- | ------------------------------- |
| `--skip-verify` | Skip previous task verification |
| `--force`       | Force next task even if blocked |

## Workflow

### Step 1: Verify Previous Task

```bash
python3 scripts/verify_task.py --task {previous_task_id} --path .
```

Check if previous task is complete:

- Target files exist
- Tests written
- Acceptance criteria met

### Step 2: Handle Verification Failure

If verification fails, output warning:

```markdown
## Pre-Verification: TASK-003 ❌ FAILED

### Gaps Found

- [ ] Missing: src/services/auth_service.py
- [ ] Missing: tests/test_auth_service.py

**Action Required:** Complete TASK-003 before proceeding.
Use `/spec-next --skip-verify` to force next task.
```

### Step 3: Get Next Task

```bash
python3 scripts/update_status.py --next --path .
```

Load and display the next pending task from `.spec-docs/tasks/`.

### Step 4: Update Status

```bash
python3 scripts/update_status.py --task {next_task_id} --status in_progress --path .
```

## Output Format

```markdown
## Pre-Verification: {previous_task} ✅ PASSED

All checks passed for previous task.

---

## Current Task: TASK-004

[Full task content from TASK-004.md]

---

After implementation:

1. Run tests: `pytest tests/`
2. Verify: `/spec-check --task TASK-004`
3. Next task: `/spec-next`
```

## Error Handling

| Situation             | Action                          |
| --------------------- | ------------------------------- |
| No .spec-docs found   | Prompt to run `/spec-dev` first |
| No pending tasks      | Show completion message         |
| Blocked by dependency | Show blocking task info         |
| Verification failed   | Add task back to pending        |
