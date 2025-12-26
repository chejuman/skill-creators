---
name: legacy-code-reimplementor-v2
description: Planning-only codebase reimplementation workflow. Analyzes legacy code, generates detailed implementation plans and tasks WITHOUT executing implementation. Persists all documentation in .reimpl-docs/ for searchability. Verifies previous task completion before providing next task, auto-adding incomplete tasks back to plan. Use for migration planning, architecture design, or when you want plans before implementation. Triggers on "reimpl plan", "migration plan", "implementation plan", "마이그레이션 계획", "구현 계획".
---

# Legacy Code Reimplementor v2 (Planning Only)

Analysis and planning workflow that generates detailed implementation plans without executing them.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    PLANNING-ONLY REIMPLEMENTOR                            │
├──────────────────────────────────────────────────────────────────────────┤
│ /reimpl-plan ──► Full Analysis + Plan Generation                         │
│     Phase 1: Deep codebase analysis (3 parallel agents)                  │
│     Phase 2: Technology selection (AskUserQuestion)                      │
│     Phase 3: Feature extraction & dependency mapping                     │
│     Phase 4: Implementation Plan & Task breakdown                        │
│     └──► All docs saved to .reimpl-docs/                                │
├──────────────────────────────────────────────────────────────────────────┤
│ /reimpl-next ──► Get Next Task (with pre-verification)                   │
│     Step 1: Verify previous task implementation                          │
│     Step 2: If incomplete → add back to plan + log gap                  │
│     Step 3: Output next ready task                                       │
├──────────────────────────────────────────────────────────────────────────┤
│ /reimpl-check ──► Verify all implementation status                       │
│ /reimpl-search ──► Search documentation                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

## Document Persistence Structure

All outputs are saved to `.reimpl-docs/` directory:

```
.reimpl-docs/
├── index.md                      # Searchable index of all documents
├── config.json                   # Project configuration
│
├── analysis/                     # Phase 1 outputs
│   ├── structure_analysis.md     # Codebase structure, modules, deps
│   ├── feature_extraction.md     # Extracted features with details
│   ├── issue_detection.md        # Security, deprecated, tech debt
│   └── dependency_graph.md       # Module dependency visualization
│
├── plans/                        # Phase 4 outputs
│   ├── implementation_plan.md    # Master implementation plan
│   ├── task_breakdown.md         # Detailed task list
│   ├── architecture_design.md    # Target architecture
│   └── migration_strategy.md     # Migration approach
│
├── tasks/                        # Individual task files
│   ├── TASK-001.md              # Task details
│   ├── TASK-002.md
│   └── ...
│
└── tracking/                     # Progress tracking
    ├── completion_status.json    # Task completion status
    ├── verification_log.md       # Verification history
    └── gaps_report.md            # Incomplete task log
```

## Slash Commands

### /reimpl-plan

Start full analysis and generate implementation plan:

```
/reimpl-plan <repo-a-path> [repo-b-path]
```

Executes all 4 phases and saves documentation.

### /reimpl-next

Get next task with pre-verification:

```
/reimpl-next [--skip-verify]
```

Verifies previous task before outputting next.

### /reimpl-check

Check implementation status of all tasks:

```
/reimpl-check [--task TASK-ID] [--all]
```

### /reimpl-search

Search through all documentation:

```
/reimpl-search <query>
```

## Phase 1: Deep Codebase Analysis

Launch 3 parallel analysis agents:

```
# Agent 1: Structure Analysis
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Analyze codebase structure comprehensively:
          - All modules, packages, directories
          - Entry points and main flows
          - External dependencies with versions
          - Internal module dependencies
          - Configuration files and patterns
          Output detailed structure report.',
  description='Deep structure analysis')

# Agent 2: Feature Extraction
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Extract all features as atomic units:
          - API endpoints with contracts
          - Services and business logic
          - Data models and schemas
          - Utility functions
          - Each feature: name, description, files, complexity
          Output feature catalog.',
  description='Feature extraction')

# Agent 3: Issue Detection
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Identify all issues and risks:
          - Security vulnerabilities (OWASP)
          - Deprecated dependencies
          - Technical debt patterns
          - Code smells and anti-patterns
          - Performance bottlenecks
          Output prioritized issue report.',
  description='Issue detection')
```

Save outputs to `.reimpl-docs/analysis/`.

## Phase 2: Technology Selection

Use AskUserQuestion with analysis-based recommendations:

```
AskUserQuestion(questions=[
  {
    "question": "Based on analysis, which target language?",
    "header": "Language",
    "options": [
      {"label": "{recommended} (Recommended)", "description": "{analysis_reason}"},
      {"label": "{alt1}", "description": "{reason}"},
      {"label": "{alt2}", "description": "{reason}"}
    ],
    "multiSelect": false
  },
  {
    "question": "Which framework for the new implementation?",
    "header": "Framework",
    "options": [...],
    "multiSelect": false
  },
  {
    "question": "What architecture pattern?",
    "header": "Architecture",
    "options": [
      {"label": "Clean Architecture (Recommended)", "description": "Layered, testable"},
      {"label": "Hexagonal", "description": "Domain-centric"},
      {"label": "Microservices", "description": "Distributed"},
      {"label": "Modular Monolith", "description": "Organized monolith"}
    ],
    "multiSelect": false
  }
])
```

Save selection to `.reimpl-docs/config.json`.

## Phase 3: Feature Extraction & Dependency Mapping

Build detailed feature catalog with dependencies:

```python
# Use scripts/build_feature_catalog.py
features = [
  {
    "id": "FEAT-001",
    "name": "Configuration Management",
    "category": "foundation",
    "description": "Application configuration and environment handling",
    "source_files": ["config.py", "settings.py"],
    "dependencies": [],
    "dependents": ["FEAT-002", "FEAT-003"],
    "complexity": "low",
    "estimated_tasks": 2
  },
  ...
]
```

Generate dependency graph:

```
FEAT-001 (Config)
    └──► FEAT-002 (Database)
         └──► FEAT-005 (User Service)
              └──► FEAT-008 (Auth API)
    └──► FEAT-003 (Logging)
```

Save to `.reimpl-docs/analysis/dependency_graph.md`.

## Phase 4: Implementation Plan & Task Generation

### Generate Master Plan

Create `.reimpl-docs/plans/implementation_plan.md`:

```markdown
# Implementation Plan

## Overview

- Source: {repo_a} ({source_lang})
- Target: {repo_b} ({target_lang} + {framework})
- Total Features: {count}
- Total Tasks: {count}
- Estimated Phases: {count}

## Implementation Order

Based on dependency analysis:

### Phase 1: Foundation (Tasks 1-5)

- TASK-001: Configuration setup
- TASK-002: Logging infrastructure
- ...

### Phase 2: Data Layer (Tasks 6-12)

...
```

### Generate Individual Task Files

For each task, create `.reimpl-docs/tasks/TASK-XXX.md`:

```markdown
# TASK-001: Configuration Management Setup

## Metadata

| Field        | Value              |
| ------------ | ------------------ |
| ID           | TASK-001           |
| Feature      | FEAT-001           |
| Priority     | 1 (Foundation)     |
| Complexity   | Low                |
| Status       | pending            |
| Dependencies | None               |
| Blocked By   | -                  |
| Blocks       | TASK-002, TASK-003 |

## Description

Implement configuration management for the new {target_lang} application.

## Source Reference (Repo A)

| File                 | Purpose              |
| -------------------- | -------------------- |
| `config/settings.py` | Main settings        |
| `config/env.py`      | Environment handling |

## Target Files (Repo B)

| File                   | Purpose              |
| ---------------------- | -------------------- |
| `src/core/config.py`   | Configuration loader |
| `src/core/settings.py` | Settings schema      |
| `.env.example`         | Environment template |

## Acceptance Criteria

- [ ] Configuration loads from environment variables
- [ ] Supports multiple environments (dev, staging, prod)
- [ ] Validation of required settings on startup
- [ ] Type-safe settings access

## Implementation Notes

- Use Pydantic Settings for {target_lang}
- Follow 12-factor app principles
- Reference original for all config keys

## Tests Required

- [ ] Unit tests for config loading
- [ ] Test missing required vars raises error
- [ ] Test environment-specific overrides
```

## Pre-Task Verification

Before outputting next task, verify previous task:

```python
# scripts/verify_task.py
def verify_task(task_id: str, repo_b: str) -> VerificationResult:
    task = load_task(task_id)

    checks = {
        'files_exist': check_target_files_exist(repo_b, task['target_files']),
        'functions_implemented': check_functions(repo_b, task['expected_functions']),
        'tests_written': check_tests_exist(repo_b, task['test_files']),
        'acceptance_criteria': check_criteria(repo_b, task['acceptance_criteria'])
    }

    return VerificationResult(
        task_id=task_id,
        passed=all(checks.values()),
        checks=checks,
        gaps=identify_gaps(checks)
    )
```

### If Verification Fails

1. Mark task as `pending` again in `completion_status.json`
2. Add gap entry to `verification_log.md`
3. Include in next task output as blocker

```markdown
## Verification Warning

TASK-003 (User Repository) is NOT complete:

- [ ] Missing: src/repositories/user_repo.py
- [ ] Missing: tests/test_user_repo.py

This task has been added back to the pending queue.

## Current Task (with unmet dependency)

You should first complete TASK-003 before proceeding.
Or use `/reimpl-next --skip-verify` to force next task.
```

## Completion Status Tracking

`.reimpl-docs/tracking/completion_status.json`:

```json
{
  "project_id": "uuid",
  "last_updated": "2025-01-15T14:30:00Z",
  "summary": {
    "total_tasks": 25,
    "completed": 8,
    "in_progress": 1,
    "pending": 14,
    "blocked": 2
  },
  "tasks": {
    "TASK-001": {
      "status": "completed",
      "verified_at": "2025-01-15T10:00:00Z",
      "verification": { "files": true, "functions": true, "tests": true }
    },
    "TASK-002": {
      "status": "pending",
      "blocked_by": [],
      "last_verification": {
        "checked_at": "2025-01-15T14:00:00Z",
        "passed": false,
        "gaps": ["Missing UserModel class", "No unit tests"]
      }
    }
  }
}
```

## Document Search

Use `scripts/search_docs.py` for full-text search:

```bash
python3 scripts/search_docs.py --query "authentication" --docs-path .reimpl-docs/
```

Returns:

```markdown
## Search Results for "authentication"

### analysis/feature_extraction.md (3 matches)

- Line 45: "FEAT-007: User Authentication..."
- Line 89: "authentication middleware..."
- Line 123: "JWT token authentication..."

### tasks/TASK-015.md (5 matches)

- Full task: "Implement authentication endpoints"

### plans/implementation_plan.md (2 matches)

- Phase 3 includes authentication tasks
```

## Scripts Reference

| Script                             | Purpose                           |
| ---------------------------------- | --------------------------------- |
| `scripts/doc_manager.py`           | Document persistence and indexing |
| `scripts/build_feature_catalog.py` | Feature extraction and cataloging |
| `scripts/generate_tasks.py`        | Task file generation              |
| `scripts/verify_task.py`           | Pre-task verification             |
| `scripts/search_docs.py`           | Full-text document search         |
| `scripts/update_status.py`         | Status tracking updates           |

## Output Example

When running `/reimpl-next`:

```markdown
## Pre-Verification: TASK-003 ✅ PASSED

All checks passed for previous task.

---

## Next Task: TASK-004

# TASK-004: User Repository Implementation

| Field        | Value                                      |
| ------------ | ------------------------------------------ |
| Priority     | 2                                          |
| Complexity   | Medium                                     |
| Dependencies | TASK-002 (completed), TASK-003 (completed) |

## What to Implement

Create the User repository with CRUD operations.

### Source Reference

- `legacy/dao/UserDAO.java` (lines 1-150)
- `legacy/repository/UserRepository.java`

### Target Structure
```

src/infrastructure/repositories/
└── user_repository.py
tests/infrastructure/repositories/
└── test_user_repository.py

```

### Acceptance Criteria
- [ ] CRUD operations for User entity
- [ ] Query by email, username
- [ ] Proper error handling
- [ ] Unit tests with 80%+ coverage

---

After implementation, run `/reimpl-check --task TASK-004` to verify.
Then run `/reimpl-next` to get the next task.

Documentation: .reimpl-docs/tasks/TASK-004.md
```

## Trigger Phrases

- "reimpl plan", "implementation plan", "migration plan"
- "generate tasks", "create plan", "plan migration"
- "마이그레이션 계획", "구현 계획", "작업 계획"
- `/reimpl-plan`, `/reimpl-next`, `/reimpl-check`, `/reimpl-search`
