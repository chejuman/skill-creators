# /spec-start

Start a new feature specification with the full 5-phase workflow.

## Usage

```
/spec-start {feature_description}
```

## Examples

```
/spec-start "사용자 인증 시스템"
/spec-start "payment integration"
/spec-start "실시간 알림 기능"
```

## Workflow

1. **Initialize Project**

   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/spec_manager.py init --feature "{feature}"
   ```

2. **Phase 1: DISCOVER**
   - Deep intent analysis via AskUserQuestion
   - Launch parallel research agents:
     - Tech trends 2025
     - Similar implementations
     - API/library research
   - Save to `.spec-docs/discovery/`

3. **Phase 2: ANALYZE**
   - Generate requirements in EARS format
   - Research relevant APIs
   - Save to `.spec-docs/requirements/`

4. **Phase 3: DESIGN**
   - Architecture design with Mermaid diagrams
   - Component specifications
   - Data models and interfaces
   - Save to `.spec-docs/design/`

5. **Phase 4: PLAN**
   - Generate atomic task files (TASK-XXX.md)
   - Build dependency graph
   - Save to `.spec-docs/tasks/`

6. **Phase 5: VERIFY**
   - Pre-task verification on each `/spec-next`
   - Gap detection and re-queuing

## Output

All artifacts saved to `.spec-docs/`:

- `discovery/` - Intent analysis, research findings
- `requirements/` - EARS format requirements
- `design/` - Architecture, components
- `tasks/` - Individual task files
- `tracking/` - Status and verification logs

## Related Commands

- `/spec-next` - Get next task with verification
- `/spec-status` - Show overall progress
- `/spec-check` - Verify specific task
