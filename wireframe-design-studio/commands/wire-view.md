# /wire-view

View details of a specific wireframe including layout, components, and specs.

## Usage

```
/wire-view {screen_name}
```

## Examples

```
/wire-view dashboard
/wire-view settings
/wire-view user-profile
```

## Workflow

1. **Get Wireframe Registry**

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/wireframe_manager.py view --screen {screen}
   ```

2. **Load Wireframe Files**
   - Layout: `.wireframe-docs/designs/{screen}/layout.md`
   - Wireframe: `.wireframe-docs/designs/{screen}/wireframe.md`
   - Components: `.wireframe-docs/designs/{screen}/components.md`
   - Specs: `.wireframe-docs/specs/{screen}/component_specs.md`

3. **Display Summary**

## Output

```markdown
## Wireframe: dashboard

| Property | Value      |
| -------- | ---------- |
| ID       | WF-001     |
| Type     | dashboard  |
| Status   | draft      |
| Created  | 2024-12-29 |

### Files

| File                               | Purpose         |
| ---------------------------------- | --------------- |
| designs/dashboard/layout.md        | Grid structure  |
| designs/dashboard/wireframe.md     | ASCII wireframe |
| specs/dashboard/component_specs.md | Component specs |
| specs/dashboard/a11y_checklist.md  | Accessibility   |
| specs/dashboard/responsive.md      | Breakpoints     |

### Quick Preview

┌─────────────────────────────────────┐
│ Header │
├─────────┬───────────────────────────┤
│ Sidebar │ Main Content │
└─────────┴───────────────────────────┘
```

## Arguments

| Argument    | Description            |
| ----------- | ---------------------- |
| screen_name | Name of screen to view |

## Related Commands

- `/wire-list` - List all wireframes
- `/wire-search {query}` - Search wireframe docs
