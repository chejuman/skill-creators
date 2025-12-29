# /wire-next

Get the next pending implementation task with verification of previous task.

## Usage

```
/wire-next
```

## Workflow

1. **Check Current Task**

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/task_tracker.py current
   ```

2. **Verify Previous Task** (if in_progress exists)

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/task_tracker.py verify --task TASK-XXX
   ```

   - Checks acceptance criteria completion
   - Reports criteria met vs total

3. **Get Next Task**

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/task_tracker.py next
   ```

4. **Display Task Details**
   - Task ID, screen, priority
   - Description and shadcn/ui components
   - Files to create
   - Acceptance criteria

5. **Update Status**
   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/task_tracker.py update --task TASK-XXX --status in_progress
   ```

## Output

```markdown
## Current Task: TASK-003

| Field        | Value              |
| ------------ | ------------------ |
| Screen       | dashboard-main     |
| Priority     | 2                  |
| Status       | in_progress        |
| Dependencies | TASK-001, TASK-002 |

### Description

Create the StatCard grid component...

### Acceptance Criteria

- [ ] 4-column grid on desktop
- [ ] Responsive layout
- [ ] Icon support
- [ ] Trend indicators
```

## Related Commands

- `/wire-status` - Full progress report
- `/wire-start` - Start new wireframe project
