# /wire-start

Start a new wireframe design project with full 4-phase workflow.

## Usage

```
/wire-start {screen_name_or_description}
```

## Examples

```
/wire-start "사용자 대시보드"
/wire-start dashboard
/wire-start "설정 페이지"
```

## Workflow

1. **Initialize Project**

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/wireframe_manager.py init --project "{screen}"
   ```

2. **Requirements Gathering** (AskUserQuestion)
   - Screen purpose (data view, input, navigation, interaction)
   - Core components (navigation, tables, forms, cards)
   - Interaction complexity (simple, moderate, complex, advanced)

3. **Domain Research** (Parallel Agents)
   - UI/UX trends 2025 WebSearch
   - shadcn/ui component matching
   - Best practices research

4. **Design Phase**
   - Layout architecture (grid, sections)
   - ASCII wireframe generation
   - Component hierarchy (Mermaid)

5. **Spec Phase**
   - Component specs (props, state, events)
   - A11y checklist (WCAG 2.1 AA)
   - Responsive breakpoints

6. **Build Phase**
   - Task generation (atomic tasks)
   - Interaction flows (state diagrams)

## Output

All artifacts saved to `.wireframe-docs/`:

- `discovery/` - Requirements, research
- `designs/{screen}/` - Layout, wireframe, components
- `specs/{screen}/` - Component specs, a11y, responsive
- `tasks/` - Implementation tasks (TASK-001.md, etc.)

## Arguments

| Argument    | Description                             |
| ----------- | --------------------------------------- |
| screen_name | Name or description of screen to design |

## Related Commands

- `/wire-next` - Get next implementation task
- `/wire-status` - Check current progress
- `/wire-view {screen}` - View wireframe details
