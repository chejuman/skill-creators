---
name: legacy-code-reimplementor
description: Feature-based iterative codebase reimplementation with session continuity. Analyzes original source, extracts atomic features, and implements one feature at a time with verification. Uses slash commands (/reimpl-start, /reimpl-continue, /reimpl-status, /reimpl-verify) for seamless multi-session workflow. Triggers on "reimplement", "migrate codebase", "legacy renewal", "code migration", "레거시 마이그레이션", "코드 재구현".
---

# Legacy Code Reimplementor v2

Feature-based iterative reimplementation with slash command continuation for multi-session workflows.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FEATURE-BASED REIMPLEMENTOR                           │
├─────────────────────────────────────────────────────────────────────────┤
│ /reimpl-start ──► Phase 0-2: Setup + Analysis + Tech Selection          │
│                   └──► Outputs: /reimpl-continue <context>              │
├─────────────────────────────────────────────────────────────────────────┤
│ /reimpl-continue ──► Phase 3-N: Feature Implementation (one at a time)  │
│                      └──► Each feature: Implement → Test → Verify       │
│                      └──► Outputs: /reimpl-continue <next-context>      │
├─────────────────────────────────────────────────────────────────────────┤
│ /reimpl-status ──► Show current progress and pending features           │
│ /reimpl-verify ──► Verify current feature against Repo A                │
├─────────────────────────────────────────────────────────────────────────┤
│ Final ──► All features complete → Validation + Report                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Context Persistence Structure

Session state is persisted in `.reimpl-context.json`:

```json
{
  "session_id": "uuid-v4",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T14:20:00Z",
  "repo_a": "/path/to/original",
  "repo_b": "/path/to/new",
  "tech_stack": {
    "source_lang": "Java",
    "target_lang": "Python",
    "framework": "FastAPI",
    "architecture": "Clean Architecture"
  },
  "features": [
    {
      "id": 1,
      "name": "User authentication",
      "status": "completed",
      "tests_passed": true,
      "units": 3,
      "completed_units": 3
    },
    {
      "id": 2,
      "name": "Product catalog API",
      "status": "in_progress",
      "current_unit": 2,
      "units": 4,
      "completed_units": 1
    },
    { "id": 3, "name": "Shopping cart", "status": "pending", "units": 2 }
  ],
  "current_feature_id": 2,
  "current_phase": "implementation",
  "next_prompt": "Continue implementing Feature 2 (Product catalog API), Unit 2: ProductRepository..."
}
```

## Slash Commands

### /reimpl-start

Start a new reimplementation project:

```
/reimpl-start <repo-a-path> [repo-b-path]
```

Executes:

1. Phase 0: Self-upgrade via WebSearch
2. Phase 1: Analysis + Feature extraction
3. Phase 2: Technology selection (AskUserQuestion)
4. Outputs continuation command

### /reimpl-continue

Continue from saved context:

```
/reimpl-continue [context-file-path]
```

Default: `./.reimpl-context.json`

Resumes from last state, implements next feature/unit.

### /reimpl-status

Show current progress:

```
/reimpl-status [context-file-path]
```

Displays feature completion status, current work, next steps.

### /reimpl-verify

Verify current feature implementation:

```
/reimpl-verify [context-file-path]
```

Runs comparison against Repo A for current feature.

## Phase 0: Self-Upgrade (Always First)

```
WebSearch(query='code migration best practices 2025 {source_lang} to {target_lang}')
WebSearch(query='{target_lang} modern frameworks security performance 2025')
WebSearch(query='feature-based migration iterative development patterns 2025')
```

## Phase 1: Analysis + Feature Extraction

### Step 1.1: Codebase Analysis

Launch parallel agents:

```
# Agent 1: Structure Analysis
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Analyze: modules, packages, entry points, dependencies.
          Create module dependency graph.',
  description='Analyze structure')

# Agent 2: Feature Extraction
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Extract atomic features: each feature = smallest independently
          testable functionality. Break down by: API endpoints, services,
          data models, utilities. List with dependencies.',
  description='Extract features')

# Agent 3: Issue Detection
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Identify: security issues, deprecated packages, technical debt.',
  description='Detect issues')
```

### Step 1.2: Feature Planning

Use `scripts/extract_features.py` to generate feature list:

```python
features = [
  {
    "id": 1,
    "name": "Configuration management",
    "description": "App config, env vars, settings",
    "units": [
      {"id": 1, "name": "Config loader", "files": ["config.py"]},
      {"id": 2, "name": "Environment handling", "files": ["env.py"]}
    ],
    "dependencies": [],
    "priority": 1  # No dependencies, implement first
  },
  {
    "id": 2,
    "name": "Database models",
    "description": "ORM models and schemas",
    "units": [
      {"id": 1, "name": "User model", "files": ["models/user.py"]},
      {"id": 2, "name": "Product model", "files": ["models/product.py"]}
    ],
    "dependencies": [1],  # Depends on config
    "priority": 2
  }
  // ... more features ordered by dependency
]
```

Features are ordered by:

1. Dependency graph (implement dependencies first)
2. Complexity (simpler first within same dependency level)
3. Risk (higher risk later to gain experience)

## Phase 2: Technology Selection

Use AskUserQuestion with analysis-based recommendations:

```
AskUserQuestion(questions=[
  {
    "question": "Target language for reimplementation?",
    "header": "Language",
    "options": [
      {"label": "{recommended} (Recommended)", "description": "{analysis_reason}"},
      {"label": "{alt1}", "description": "{alt1_reason}"},
      {"label": "{alt2}", "description": "{alt2_reason}"}
    ],
    "multiSelect": false
  },
  // ... framework, architecture questions
])
```

After confirmation, save context and output:

```
## Next Step

To continue implementation, run:

/reimpl-continue .reimpl-context.json

Or copy this command for later:
/reimpl-continue eyJzZXNzaW9uX2lkIjoi...base64...
```

## Phase 3-N: Feature Implementation Cycles

### For Each Feature

```
┌─────────────────────────────────────────────────┐
│ Feature N: {feature_name}                       │
├─────────────────────────────────────────────────┤
│ Unit 1 ──► Implement ──► Test ──► Verify ──► ✓ │
│ Unit 2 ──► Implement ──► Test ──► Verify ──► ✓ │
│ Unit M ──► Implement ──► Test ──► Verify ──► ✓ │
├─────────────────────────────────────────────────┤
│ Feature Complete ──► Update Context             │
│                  ──► Output /reimpl-continue    │
└─────────────────────────────────────────────────┘
```

### Unit Implementation Pattern

For each unit within a feature:

```
TodoWrite(todos=[
  {"content": "F{N}.U{M}: Implement {unit_name}", "status": "in_progress", "activeForm": "Implementing {unit_name}"},
  {"content": "F{N}.U{M}: Write tests", "status": "pending", "activeForm": "Writing tests"},
  {"content": "F{N}.U{M}: Verify against Repo A", "status": "pending", "activeForm": "Verifying implementation"}
])
```

1. **Implement:**

```
Task(subagent_type='general-purpose', model='sonnet',
  prompt='Implement Feature {N}, Unit {M}: {unit_name}
          Source reference: {repo_a_files}
          Target: {repo_b_path}
          Stack: {tech_stack}
          Previous units completed: {completed_units}',
  description='Implement F{N}.U{M}')
```

2. **Test:**

```
Task(subagent_type='general-purpose', model='sonnet',
  prompt='Create tests for Feature {N}, Unit {M}: {unit_name}
          Test types: unit tests, edge cases from original
          Ensure: all paths covered, error handling tested',
  description='Test F{N}.U{M}')
```

3. **Verify:**

```bash
python3 scripts/verify_feature.py --feature {N} --unit {M} \
  --repo-a {path_a} --repo-b {path_b} --context .reimpl-context.json
```

### After Each Unit/Feature Completion

Update context and output continuation command:

```
## Progress Update

Feature 2 (Product catalog API): Unit 2 of 4 completed
Overall: 5/15 features complete (33%)

### Next Step

To continue with Unit 3, run:

/reimpl-continue

Current context saved to: .reimpl-context.json
```

## Final Phase: Validation

When all features complete:

```
# Parallel validation
Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
  prompt='Full test suite validation. Verify 100% feature coverage.',
  description='Test validation')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
  prompt='Security audit: OWASP Top 10, dependencies, secrets.',
  description='Security audit')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
  prompt='Performance benchmark against Repo A.',
  description='Performance benchmark')
```

Generate final report:

```bash
python3 scripts/generate_final_report.py \
  --repo-a {path_a} --repo-b {path_b} \
  --context .reimpl-context.json \
  --output migration_report.md
```

## Scripts Reference

| Script                                | Purpose                                        |
| ------------------------------------- | ---------------------------------------------- |
| `scripts/context_manager.py`          | Manage session context (save/load/update)      |
| `scripts/extract_features.py`         | Extract atomic features from codebase          |
| `scripts/verify_feature.py`           | Verify feature implementation against original |
| `scripts/generate_analysis_report.py` | Initial codebase analysis                      |
| `scripts/generate_final_report.py`    | Final migration report                         |

## Example Session Flow

```
Session 1:
User: /reimpl-start ./legacy-java-app ./new-python-app
→ Analysis complete, 15 features extracted
→ Tech selection: Python + FastAPI + Clean Architecture
→ Output: /reimpl-continue .reimpl-context.json

Session 2:
User: /reimpl-continue
→ Feature 1: Configuration (2 units) ✓ Complete
→ Feature 2: Database Models, Unit 1 ✓ Complete
→ Output: /reimpl-continue (for Unit 2)

Session 3:
User: /reimpl-continue
→ Feature 2: Unit 2 ✓, Unit 3 ✓ Complete
→ Feature 3: User Service, Unit 1 in progress...
→ Output: /reimpl-continue (for remaining)

... (continue until all features done)

Final Session:
User: /reimpl-continue
→ All 15 features complete
→ Running validation...
→ Migration Report generated
```

## Trigger Phrases

- "reimplement", "migrate codebase", "legacy renewal"
- "code migration", "레거시 마이그레이션", "코드 재구현"
- `/reimpl-start`, `/reimpl-continue`, `/reimpl-status`, `/reimpl-verify`
