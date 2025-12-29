# /wire-search

Search wireframe documentation for specific terms.

## Usage

```
/wire-search {query}
/wire-search {query} --type specs
```

## Examples

```
/wire-search "sidebar"
/wire-search "Card" --type specs
/wire-search "responsive" --type designs
```

## Workflow

1. **Execute Search**

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/search_docs.py --query "{query}"
   ```

2. **Filter by Type** (optional)
   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/search_docs.py --query "{query}" --type specs
   ```

## Output

```markdown
# Search Results for "sidebar"

**Files Searched:** 15
**Files with Matches:** 3
**Total Matches:** 7

---

## designs/dashboard/layout.md (3 matches)

**Line 24:**
```

│ SIDEBAR │ Main Content

```

**Line 45:**
```

Sidebar width: w-64 (desktop)

```

---

## specs/dashboard/responsive.md (2 matches)

**Line 12:**
```

Sidebar: Hidden on mobile, Sheet drawer

```

```

## Options

| Option    | Description                                                    |
| --------- | -------------------------------------------------------------- |
| --type    | Filter by doc type: discovery, designs, specs, tasks, tracking |
| --context | Context lines (default: 2)                                     |
| --limit   | Max results (default: 50)                                      |
| --format  | Output format: markdown, json                                  |

## Arguments

| Argument | Description           |
| -------- | --------------------- |
| query    | Search term or phrase |

## Related Commands

- `/wire-view {screen}` - View specific wireframe
- `/wire-spec {component}` - View component spec
