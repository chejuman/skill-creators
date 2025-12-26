# /reimpl-search

Search through all documentation in .reimpl-docs/.

## Usage

```
/reimpl-search <query> [options]
```

## Arguments

- `query` (required): Search term or phrase

## Options

- `--tasks` or `-t`: Search only in task files
- `--features` or `-f`: Search only in feature catalog
- `--category <cat>`: Search specific category (analysis, plans, tasks, tracking)
- `--verbose` or `-v`: Show context around matches

## What This Does

Full-text search across all documentation:

```bash
python3 ~/.claude/skills/legacy-code-reimplementor-v2/scripts/search_docs.py "{query}"
```

Searches in:

- `analysis/` - Structure, features, issues
- `plans/` - Implementation plan, task breakdown
- `tasks/` - Individual task files
- `tracking/` - Status, logs, gaps

## Output Format

### General Search

```markdown
# Search Results for "authentication"

**Matches:** 15 in 6 files

## analysis/feature_extraction.md (3 matches)

- **Line 45:** FEAT-007: User **Authentication**
- **Line 89:** JWT **authentication** middleware
- **Line 123:** OAuth **authentication** provider

## tasks/TASK-015.md (5 matches)

- **Line 1:** # TASK-015: **Authentication** Endpoints
- **Line 25:** Implement **authentication** flow
  ...

## plans/implementation_plan.md (2 matches)

- **Line 78:** Phase 3 includes **authentication** tasks
```

### Task Search

```markdown
# Tasks matching "user"

- **TASK-002**: User Model Implementation (3 matches)
- **TASK-004**: User Repository (5 matches)
- **TASK-008**: User Service (4 matches)
- **TASK-015**: User Authentication (2 matches)
```

### Feature Search

```markdown
# Features matching "api"

- **FEAT-010**: User API (api)
- **FEAT-011**: Product API (api)
- **FEAT-012**: Order API (api)
```

## Use Cases

### Find related tasks

```
/reimpl-search "database"
```

### Find all authentication-related work

```
/reimpl-search "auth" --tasks
```

### Search in analysis only

```
/reimpl-search "deprecated" --category analysis
```

### Verbose output with context

```
/reimpl-search "migration" --verbose
```

## Example

```
User: /reimpl-search authentication

User: /reimpl-search "user model" --tasks

User: /reimpl-search config --features
```
