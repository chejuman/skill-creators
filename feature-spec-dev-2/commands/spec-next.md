# /spec-next

Get the next pending task with pre-verification of the previous task.

## Usage

```
/spec-next
/spec-next --skip-verify
```

## Workflow

1. **Check Current Task**

   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/task_tracker.py current
   ```

2. **Verify Previous Task** (unless --skip-verify)

   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/verify_task.py --task TASK-XXX --update-status
   ```

   - Check files exist
   - Check acceptance criteria
   - If failed: re-add to pending queue

3. **Get Next Task**

   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/task_tracker.py next
   ```

4. **Display Task Details**
   - Read TASK-XXX.md from `.spec-docs/tasks/`
   - Show metadata, steps, acceptance criteria

5. **Update Status**
   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/task_tracker.py update --task TASK-XXX --status in_progress
   ```

## Output

```markdown
## Pre-Verification: TASK-002 ✅ PASSED

All checks passed for previous task.

---

## Next Task: TASK-003

# TASK-003: Implement User Service

| Field        | Value              |
| ------------ | ------------------ |
| Priority     | 2 (Core)           |
| Complexity   | Medium             |
| Dependencies | TASK-001, TASK-002 |

### Description

Create the user service with authentication logic...

### Acceptance Criteria

- [ ] User registration with validation
- [ ] Password hashing with bcrypt
- [ ] Tests with 80%+ coverage

---

After implementation, run `/spec-check --task TASK-003` to verify.
```

## Options

| Option        | Description                     |
| ------------- | ------------------------------- |
| --skip-verify | Skip previous task verification |

## Related Commands

- `/spec-check --task TASK-XXX` - Verify task completion
- `/spec-status` - Show overall progress
