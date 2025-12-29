# /spec-search Command

Search all spec documentation.

## Usage

```bash
/spec-search "authentication"
/spec-search "TASK-" --type tasks
/spec-search "API" --context 5
```

## Arguments

| Argument       | Description                                        |
| -------------- | -------------------------------------------------- |
| `<query>`      | Search term or pattern                             |
| `--type TYPE`  | Limit to: discovery, specs, plans, tasks, tracking |
| `--context N`  | Lines of context (default: 2)                      |
| `--limit N`    | Maximum results (default: 50)                      |
| `--format FMT` | Output: markdown or json                           |

## Workflow

### Execute Search

```bash
python3 scripts/search_docs.py --query "authentication" --path . --format markdown
```

### Filter by Type

```bash
python3 scripts/search_docs.py --query "TASK-" --type tasks --path .
```

## Output Format

```markdown
# Search Results for "authentication"

**Files Searched:** 15
**Files with Matches:** 4
**Total Matches:** 12

---

## specs/user-auth/requirements.md (3 matches)

**Line 45:**
```

REQ-F-001: WHEN user submits credentials THEN system SHALL authenticate...

```

**Line 89:**
```

Authentication service must validate tokens within 100ms.

```

---

## tasks/TASK-003.md (5 matches)

**Line 12:**
```

Implement JWT authentication middleware.

```

*...and 3 more matches*

---
```

## Search Tips

| Pattern       | Use Case                      |
| ------------- | ----------------------------- |
| `REQ-F-`      | Find functional requirements  |
| `REQ-NF-`     | Find non-functional reqs      |
| `TASK-`       | Find all task references      |
| `WHEN.*SHALL` | Find EARS-format requirements |
| `acceptance`  | Find acceptance criteria      |

## Error Handling

| Situation           | Action                          |
| ------------------- | ------------------------------- |
| No .spec-docs found | Prompt to run `/spec-dev` first |
| No results          | Suggest broader search terms    |
| Too many results    | Suggest --type filter           |
