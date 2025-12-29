# /spec-search

Search through all feature specification documentation.

## Usage

```
/spec-search {query}
/spec-search {query} --phase requirements
```

## Examples

```
/spec-search "authentication"
/spec-search "API" --phase design
/spec-search "password" --phase requirements
```

## Workflow

1. **Execute Search**

   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/search_docs.py --query "{query}"
   ```

2. **Filter by Phase** (optional)
   ```bash
   python3 ~/.claude/skills/feature-spec-dev-2/scripts/search_docs.py --query "{query}" --phase design
   ```

## Output

```markdown
# Search Results for "authentication"

**Files Searched:** 12
**Files with Matches:** 4
**Total Matches:** 8

---

## requirements/requirements.md (3 matches)

**Line 15:**
```

WHEN a user submits login THEN the system SHALL authenticate credentials

```

**Line 28:**
```

IF authentication fails THEN display error message

```

---

## design/architecture.md (2 matches)

**Line 45:**
```

AuthService: Handles authentication and session management

```

---

## tasks/TASK-003.md (3 matches)

**Line 8:**
```

Implement authentication middleware

```

```

## Options

| Option    | Description                                              |
| --------- | -------------------------------------------------------- |
| --phase   | Filter: discovery, requirements, design, tasks, tracking |
| --context | Context lines around match (default: 2)                  |
| --limit   | Max results (default: 50)                                |
| --format  | Output: markdown, json                                   |

## Related Commands

- `/spec-status` - Overall progress
- `/spec-check` - Verify task
