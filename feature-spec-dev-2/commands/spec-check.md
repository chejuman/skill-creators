# /spec-check

Verify task completion status and update tracking.

## Usage

```
/spec-check
/spec-check --task TASK-001
/spec-check --all
```

## Workflow

1. **Load Task Details**
   - Read TASK-XXX.md from `.spec-docs/tasks/`
   - Parse acceptance criteria and files

2. **Run Verification**

   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/verify_task.py --task TASK-XXX --update-status
   ```

3. **Check Results**
   - Files created: Check if specified files exist
   - Acceptance criteria: Check checkbox status
   - Tests exist: Verify test files created

4. **Update Status**
   - PASSED: Mark task as `completed`
   - FAILED: Mark task as `pending` (re-queue)
   - Log to `verification_log.md`

## Output

### Passed Example

```markdown
## Verification: TASK-003 ✅ PASSED

| Check               | Status              |
| ------------------- | ------------------- |
| Files Created       | ✅ All files exist  |
| Acceptance Criteria | ✅ All criteria met |
| Tests Exist         | ✅ Test files found |

Task marked as **completed**.
```

### Failed Example

```markdown
## Verification: TASK-003 ❌ FAILED

| Check               | Status                           |
| ------------------- | -------------------------------- |
| Files Created       | ❌ Missing: src/services/user.ts |
| Acceptance Criteria | ⚠️ 2/4 criteria met              |
| Tests Exist         | ❌ No test files                 |

### Gaps Identified

- [ ] Missing file: src/services/user.ts
- [ ] Unmet: "Password hashing with bcrypt"
- [ ] Missing test file

Task has been **re-queued** as pending.
```

## Options

| Option         | Description                     |
| -------------- | ------------------------------- |
| --task ID      | Verify specific task            |
| --all          | Verify all tasks                |
| --project-path | Path to project for file checks |

## Related Commands

- `/spec-next` - Get next task
- `/spec-status` - Overall progress
