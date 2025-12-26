# /reimpl-status

Show current reimplementation progress and status.

## Usage

```
/reimpl-status [context-path]
```

## Arguments

- `context-path` (optional): Path to context file
  - Default: `.reimpl-context.json` in current directory

## Workflow

### 1. Load and Display Status

```bash
python3 ~/.claude/skills/legacy-code-reimplementor/scripts/context_manager.py status --context {context-path}
```

### 2. Generate Visual Progress

Display comprehensive status including:

- Session information
- Repository paths
- Technology stack
- Feature progress (completed/in-progress/pending)
- Current work details
- Next steps

## Output Format

```
# Reimplementation Status

**Session:** abc12345...
**Phase:** implementation
**Last Updated:** 2025-01-15 14:30:00

## Repositories

| Repo | Path |
|------|------|
| Original (A) | /path/to/legacy-app |
| New (B) | /path/to/new-app |

## Technology Stack

| Aspect | Value |
|--------|-------|
| Source | Java (Spring Boot) |
| Target | Python (FastAPI) |
| Architecture | Clean Architecture |

## Progress Overview

```

[████████████░░░░░░░░] 60% Complete

```

| Status | Count |
|--------|-------|
| Completed | 9/15 |
| In Progress | 1 |
| Pending | 5 |

## Feature Status

| # | Feature | Status | Units |
|---|---------|--------|-------|
| 1 | Configuration | ✅ Done | 2/2 |
| 2 | Database Models | ✅ Done | 3/3 |
| 3 | User Service | ✅ Done | 4/4 |
| 4 | Auth Module | 🔄 Working | 2/3 |
| 5 | Product API | ⏳ Pending | 0/4 |
| ... | ... | ... | ... |

## Current Work

**Feature 4:** Auth Module
**Unit 2 of 3:** JWT Token Handler
**Files:**
- auth/token_handler.py
- auth/middleware.py

## Next Step

Continue with Unit 3 (Permission checks) by running:

/reimpl-continue
```

## Additional Options

### JSON Output

For programmatic access:

```bash
python3 ~/.claude/skills/legacy-code-reimplementor/scripts/context_manager.py progress --context {context-path}
```

Returns:

```json
{
  "total_features": 15,
  "completed_features": 9,
  "in_progress_features": 1,
  "pending_features": 5,
  "completion_pct": 60.0,
  "current_feature": {...},
  "current_unit": 2,
  "phase": "implementation"
}
```

## Example

```
User: /reimpl-status
```
