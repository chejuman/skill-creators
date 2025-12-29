# /wire-list

List all registered wireframes in the project.

## Usage

```
/wire-list
/wire-list --format json
```

## Workflow

1. **Get Wireframe Registry**
   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/wireframe_manager.py list
   ```

## Output

```markdown
# Wireframe Registry

| ID     | Screen    | Type      | Status | Created    |
| ------ | --------- | --------- | ------ | ---------- |
| WF-001 | dashboard | dashboard | draft  | 2024-12-29 |
| WF-002 | settings  | form      | draft  | 2024-12-29 |
| WF-003 | users     | list      | draft  | 2024-12-29 |
```

## Options

| Option        | Description          |
| ------------- | -------------------- |
| --format json | Output as JSON array |

## Related Commands

- `/wire-view {screen}` - View specific wireframe
- `/wire-start {screen}` - Create new wireframe
