---
name: feature-dev-v2
description: Multi-agent feature development system with parallel execution. Spawns Exploration Agents for codebase analysis, Architecture Agents for design alternatives, Implementation Agents for coding, and Review Agents for quality assurance. Use when implementing features, building new functionality, or when user mentions "feature development", "implement feature", development levels (1-5), or needs systematic multi-agent development workflow.
---

# Feature Development v2.0

Hierarchical multi-agent feature development system with parallel execution and comprehensive review.

## Architecture

```
Orchestrator (this skill)
    │
    ├─► Discovery Agent ──► Requirements clarification
    │
    ├─► Exploration Agents (PARALLEL) ──► Codebase analysis
    │       ├── Explorer #1: Similar features
    │       ├── Explorer #2: Architecture patterns
    │       └── Explorer #3: Integration points
    │
    ├─► Clarification ──► AskUserQuestion for ambiguities
    │
    ├─► Architecture Agents (PARALLEL) ──► Design alternatives
    │       ├── Architect #1: Minimal approach
    │       ├── Architect #2: Clean architecture
    │       └── Architect #3: Pragmatic balance
    │
    ├─► Implementation Agent ──► Code generation
    │
    ├─► Review Agents (PARALLEL) ──► Quality assurance
    │       ├── Reviewer #1: Code quality/DRY
    │       ├── Reviewer #2: Bugs/correctness
    │       └── Reviewer #3: Conventions/patterns
    │
    └─► Summary Agent ──► Documentation
```

## Development Levels

| Level | Explorers | Architects | Reviewers | Use Case |
|-------|-----------|------------|-----------|----------|
| 1 | 1 | Skip | 1 | Quick fix, small change |
| 2 | 2 | 1 | 2 | Simple feature |
| 3 | 3 | 2 | 3 | Standard feature |
| 4 | 3 | 3 | 3 | Complex feature |
| 5 | 3+ | 3 | 3+ | Major feature, refactor |

## Execution Workflow

### Phase 1: Discovery

Parse user request and clarify requirements:

```
Task(
  subagent_type='Plan',
  prompt='Analyze feature request and identify: 1) Core requirements 2) Ambiguous aspects 3) Potential scope boundaries 4) Technical constraints...',
  description='Analyze feature request'
)
```

**Output Format:**
```json
{
  "feature": "...",
  "requirements": ["..."],
  "ambiguities": ["..."],
  "scope": {"in": [...], "out": [...]},
  "constraints": ["..."]
}
```

### Phase 2: Parallel Codebase Exploration

Spawn Exploration Agents simultaneously in ONE message:

```
# CRITICAL: All Task calls in ONE message for true parallelism
Task(
  subagent_type='Explore',
  prompt='Find similar features and trace implementation patterns...',
  description='Explore similar features',
  model='haiku'
)
Task(
  subagent_type='Explore',
  prompt='Map architecture layers and abstractions relevant to feature...',
  description='Explore architecture',
  model='haiku'
)
Task(
  subagent_type='Explore',
  prompt='Identify integration points, dependencies, and extension patterns...',
  description='Explore integrations',
  model='haiku'
)
```

**Explorer Agent Prompt Template:**
```
You are a Code Exploration Agent. Analyze codebase for feature implementation context.

FOCUS: {{focus_area}}
FEATURE: {{feature_description}}

Instructions:
1. Use Glob to find relevant files by patterns
2. Use Grep to search for related code
3. Use Read to understand implementations
4. Trace execution flows comprehensively

Output EXACTLY this JSON:
{
  "focus": "{{focus_area}}",
  "key_files": ["path1", "path2", ...],
  "patterns_found": [
    {"pattern": "...", "location": "file:line", "relevance": "..."}
  ],
  "abstractions": ["..."],
  "recommendations": ["..."],
  "files_to_read": ["top 5-10 files for deep understanding"]
}
```

### Phase 3: Clarifying Questions

After exploration, present questions to user:

```
AskUserQuestion(questions=[
  {
    "question": "Which implementation approach do you prefer?",
    "header": "Approach",
    "options": [
      {"label": "Minimal (Recommended)", "description": "Smallest change, maximum reuse"},
      {"label": "Clean", "description": "Maintainability, elegant abstractions"},
      {"label": "Pragmatic", "description": "Balance of speed and quality"}
    ],
    "multiSelect": False
  },
  {
    "question": "Any specific edge cases to handle?",
    "header": "Edge Cases",
    "options": [
      {"label": "Standard handling", "description": "Common error scenarios"},
      {"label": "Comprehensive", "description": "All possible edge cases"},
      {"label": "User specified", "description": "Let me specify..."}
    ],
    "multiSelect": False
  }
])
```

**CRITICAL:** Wait for user answers before Phase 4.

### Phase 4: Parallel Architecture Design

Spawn Architecture Agents in ONE message:

```
Task(
  subagent_type='Plan',
  prompt='Design MINIMAL approach: smallest change, maximum code reuse...',
  description='Design minimal approach'
)
Task(
  subagent_type='Plan',
  prompt='Design CLEAN ARCHITECTURE: maintainability, elegant abstractions...',
  description='Design clean architecture'
)
Task(
  subagent_type='Plan',
  prompt='Design PRAGMATIC approach: balance speed and quality...',
  description='Design pragmatic approach'
)
```

**Architect Agent Prompt Template:**
```
You are a Code Architecture Agent. Design implementation approach.

FEATURE: {{feature}}
APPROACH: {{approach_type}}
CODEBASE CONTEXT: {{exploration_summary}}
USER PREFERENCES: {{user_answers}}

Design an implementation with:
1. High-level architecture diagram
2. Specific files to create/modify
3. Key abstractions and patterns
4. Data flow description
5. Trade-offs analysis

Output EXACTLY this JSON:
{
  "approach": "{{approach_type}}",
  "architecture": {
    "components": [...],
    "data_flow": "...",
    "patterns": [...]
  },
  "file_changes": [
    {"path": "...", "action": "CREATE|MODIFY", "description": "..."}
  ],
  "trade_offs": {
    "pros": [...],
    "cons": [...]
  },
  "implementation_steps": [...],
  "estimated_complexity": "LOW|MEDIUM|HIGH"
}
```

**Present Options to User:**
```markdown
## Architecture Options

### Option 1: Minimal Approach
- **Changes:** X files
- **Pros:** Fast, low risk
- **Cons:** May accumulate tech debt
- **Recommendation:** Best for urgent fixes

### Option 2: Clean Architecture
...

**My Recommendation:** [approach] because [reasoning]

Which approach would you like to proceed with?
```

### Phase 5: Implementation

**WAIT FOR USER APPROVAL BEFORE PROCEEDING**

```
Task(
  subagent_type='general-purpose',
  prompt='Implement feature following approved architecture. Read all relevant files first, then implement step by step...',
  description='Implement feature'
)
```

**Implementation Agent Instructions:**
1. Read all files identified in exploration phase
2. Follow chosen architecture exactly
3. Maintain codebase conventions
4. Write clean, documented code
5. Update TodoWrite progress throughout

### Phase 6: Parallel Code Review

Spawn Review Agents in ONE message:

```
Task(
  subagent_type='general-purpose',
  prompt='Review for code quality: DRY, readability, simplicity, elegance...',
  description='Review code quality',
  model='haiku'
)
Task(
  subagent_type='general-purpose',
  prompt='Review for bugs: logic errors, edge cases, correctness, security...',
  description='Review bugs/correctness',
  model='haiku'
)
Task(
  subagent_type='general-purpose',
  prompt='Review for conventions: project patterns, abstractions, consistency...',
  description='Review conventions',
  model='haiku'
)
```

**Reviewer Agent Prompt Template:**
```
You are a Code Review Agent. Review implemented code for {{focus}}.

FOCUS: {{review_focus}}
FILES CHANGED: {{file_list}}
CONFIDENCE_THRESHOLD: 0.8

Instructions:
1. Read all changed files
2. Identify issues in your focus area
3. Score each issue by confidence (0.0-1.0)
4. Only report issues with confidence >= 0.8

Output EXACTLY this JSON:
{
  "focus": "{{review_focus}}",
  "files_reviewed": [...],
  "issues": [
    {
      "file": "path",
      "line": 123,
      "severity": "HIGH|MEDIUM|LOW",
      "confidence": 0.92,
      "description": "...",
      "suggestion": "..."
    }
  ],
  "summary": "...",
  "approval": "APPROVED|NEEDS_CHANGES"
}
```

**Present Review Findings:**
```markdown
## Code Review Results

### High Severity Issues
- [Issue 1]: file:line - description

### Recommendations
- [Suggestion 1]

**Overall Status:** APPROVED / NEEDS_CHANGES

What would you like to do?
- Fix all issues now
- Fix high severity only
- Proceed as-is
```

### Phase 7: Summary

Generate completion summary:

```
Task(
  subagent_type='general-purpose',
  prompt='Generate feature implementation summary with deliverables, decisions made, and suggested next steps...',
  description='Generate summary',
  model='haiku'
)
```

**Summary Format:**
```markdown
# Feature Implementation Complete

**Feature:** {{feature_name}}
**Level:** {{level}}
**Agents Used:** {{agent_count}}

## What Was Built
- [Deliverable 1]
- [Deliverable 2]

## Key Decisions
- [Decision 1]: [Rationale]

## Files Modified
| File | Action | Description |
|------|--------|-------------|
| path | CREATED | ... |

## Suggested Next Steps
- [Step 1]
- [Step 2]
```

## Orchestration Rules

### Parallel Execution Pattern

To run agents in TRUE parallel, include ALL Task calls in ONE response:

```python
# CORRECT - True parallel execution
message_with_multiple_tools:
  - Task(explorer1)
  - Task(explorer2)
  - Task(explorer3)

# INCORRECT - Sequential execution
message1: Task(explorer1)
message2: Task(explorer2)  # Waits for message1
```

### Agent Coordination

1. **Discovery Agent** runs FIRST (sequential)
2. **Exploration Agents** run in PARALLEL
3. **User clarification** after exploration
4. **Architecture Agents** run in PARALLEL
5. **User approval** before implementation
6. **Implementation Agent** runs (sequential)
7. **Review Agents** run in PARALLEL
8. **Summary Agent** runs LAST

### Model Selection

| Agent Type | Model | Reason |
|------------|-------|--------|
| Discovery | sonnet | Complex reasoning |
| Exploration | haiku | Fast search |
| Architecture | sonnet | Design quality |
| Implementation | sonnet | Code quality |
| Review | haiku | Fast checks |
| Summary | haiku | Quick output |

## Quality Metrics

**Minimum Requirements by Level:**

| Level | Explorers | Files Analyzed | Review Issues |
|-------|-----------|----------------|---------------|
| 1 | 1 | 5 | 0 high severity |
| 2 | 2 | 10 | 0 high severity |
| 3 | 3 | 15 | 0 high, ≤2 medium |
| 4 | 3 | 20 | 0 high, ≤1 medium |
| 5 | 3+ | 25+ | 0 high/medium |

## Error Recovery

### Agent Failure Handling

When a parallel agent fails or returns malformed output:

```
1. DETECT: Check if agent returned valid JSON
2. REPORT: Log which agent failed and error message
3. DECIDE: Ask user how to proceed
   - Retry failed agent only
   - Continue with remaining agent outputs
   - Abort and restart phase
4. RECOVER: Execute chosen recovery action
```

**Recovery Options by Phase:**

| Phase | Failure | Recovery |
|-------|---------|----------|
| Exploration | 1 of 3 fails | Continue with 2 explorers' output |
| Exploration | 2+ fail | Retry phase or ask user for manual context |
| Architecture | 1 of 3 fails | Present 2 options to user |
| Architecture | All fail | Escalate - user provides architecture |
| Review | 1 of 3 fails | Proceed with 2 reviewers' output |
| Review | 2+ fail | Retry or skip review with warning |

**Malformed Output Recovery:**
```
If agent output is not valid JSON:
1. Extract any readable findings from text
2. Mark agent as "partial success"
3. Continue workflow with available data
4. Note gap in final summary
```

## Context Budget Management

### File Limits by Codebase Size

To prevent context explosion, limit files based on repository size:

| Codebase Size | Files | Limit per Explorer | Total Context |
|---------------|-------|-------------------|---------------|
| Small (< 100 files) | < 100 | 10 files | ~30 files |
| Medium (100-1000) | 100-1000 | 5-7 files | ~21 files |
| Large (1000+) | 1000+ | 3-5 files | ~15 files |

**Context Estimation:**
```
Codebase size check:
  find . -type f -name "*.{js,ts,py,go,java}" | wc -l

If > 1000 files:
  Instruct explorers: "Limit files_to_read to 3-5 most critical files"
If 100-1000 files:
  Instruct explorers: "Limit files_to_read to 5-7 files"
If < 100 files:
  Default: "Return top 10 files for deep understanding"
```

**Priority for File Selection:**
1. Entry points (main, index, app)
2. Files with highest relevance to feature
3. Shared utilities and abstractions
4. Test files (if testing focus)

## Inter-Agent Data Format

### Exploration Summary Schema

All exploration agents output JSON that combines into `{{exploration_summary}}`:

```json
{
  "exploration_summary": {
    "similar_features": {
      "agent": "Explorer #1",
      "features": [...],
      "patterns": [...],
      "reusable_components": [...]
    },
    "architecture": {
      "agent": "Explorer #2",
      "layers": [...],
      "data_flow": {...},
      "abstractions": [...]
    },
    "integrations": {
      "agent": "Explorer #3",
      "external_apis": [...],
      "internal_deps": [...],
      "extension_points": [...]
    },
    "combined_key_files": ["path1", "path2", ...],
    "combined_recommendations": [...]
  }
}
```

**Merging Algorithm:**
```python
def merge_exploration_outputs(explorer_outputs):
    summary = {"exploration_summary": {}}
    key_files = set()
    recommendations = []

    for output in explorer_outputs:
        # Add agent-specific findings
        summary["exploration_summary"][output["focus"]] = output
        # Merge key files (deduplicate)
        key_files.update(output.get("key_files", []))
        # Collect recommendations
        recommendations.extend(output.get("recommendations", []))

    summary["exploration_summary"]["combined_key_files"] = list(key_files)
    summary["exploration_summary"]["combined_recommendations"] = recommendations
    return summary
```

### Architecture Design Schema

All architect agents use this unified schema:

```json
{
  "approach": "MINIMAL|CLEAN|PRAGMATIC",
  "philosophy": "...",
  "architecture": {
    "components": [{"name": "...", "type": "...", "responsibility": "..."}],
    "patterns": ["..."],
    "data_flow": "..."
  },
  "file_changes": [
    {"path": "...", "action": "CREATE|MODIFY", "lines_est": 50, "description": "..."}
  ],
  "trade_offs": {
    "pros": ["..."],
    "cons": ["..."]
  },
  "implementation_steps": ["Step 1", "Step 2", ...],
  "estimated_complexity": "LOW|MEDIUM|HIGH",
  "estimated_files": 5,
  "estimated_time": "2-4 hours"
}
```

## Review Consolidation

### Merging Three Reviewer Outputs

After parallel review agents complete, consolidate their findings:

```python
def consolidate_reviews(reviewer_outputs):
    consolidated = {
        "all_issues": [],
        "by_severity": {"HIGH": [], "MEDIUM": [], "LOW": []},
        "by_reviewer": {},
        "overall_status": "APPROVED",
        "summary": ""
    }

    for output in reviewer_outputs:
        reviewer_name = output["focus"]
        consolidated["by_reviewer"][reviewer_name] = output

        for issue in output.get("issues", []):
            issue["reviewer"] = reviewer_name
            consolidated["all_issues"].append(issue)
            consolidated["by_severity"][issue["severity"]].append(issue)

        # If ANY reviewer says NEEDS_CHANGES, overall is NEEDS_CHANGES
        if output.get("approval") == "NEEDS_CHANGES":
            consolidated["overall_status"] = "NEEDS_CHANGES"

    # Sort all issues by severity then confidence
    consolidated["all_issues"].sort(
        key=lambda x: (
            {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x["severity"]],
            -x["confidence"]
        )
    )

    return consolidated
```

### Approval Decision Matrix

| High Issues | Medium Issues | Decision |
|-------------|---------------|----------|
| 0 | 0 | APPROVED |
| 0 | 1-2 (Level 3) | APPROVED with notes |
| 0 | 3+ | NEEDS_CHANGES |
| 1+ | Any | NEEDS_CHANGES |

### Conflict Resolution

When reviewers disagree on the same code:

**Priority Order:**
1. **Security issues** (Correctness Reviewer) - Always highest priority
2. **Convention violations** (Conventions Reviewer) - Project consistency
3. **Quality suggestions** (Quality Reviewer) - Style preferences

**If conflicting suggestions:**
```markdown
## Reviewer Conflict Detected

**File:** src/api/auth.ts:45

**Quality Reviewer:** "Extract to helper function for clarity"
**Conventions Reviewer:** "Keep inline per project pattern"

**Resolution:** Follow Conventions Reviewer (project patterns take precedence)
```

## Phase 6b: Fix Iteration Cycle

When review status is NEEDS_CHANGES, enter fix iteration:

```
Phase 6b: Fix Iteration
    │
    ├─► Fix Agent ──► Address identified issues
    │
    ├─► Lite Review ──► Re-check ONLY changed lines
    │
    └─► Decision ──► APPROVED? → Phase 7 : → Repeat 6b
```

**Fix Agent Task:**
```
Task(
  subagent_type='general-purpose',
  prompt='Fix the following review issues:
    {{high_severity_issues}}
    {{medium_severity_issues_if_selected}}

    For each issue:
    1. Read the file
    2. Apply the suggested fix
    3. Verify fix doesn't break other code

    Return list of fixes applied.',
  description='Fix review issues'
)
```

**Lite Review (focused re-check):**
```
Task(
  subagent_type='general-purpose',
  prompt='Re-review ONLY the following fixed files:
    {{fixed_files}}

    Check that:
    1. Original issues are resolved
    2. No new issues introduced
    3. Changes are minimal and focused

    Return: APPROVED or remaining issues.',
  description='Lite review of fixes',
  model='haiku'
)
```

**Iteration Limits:**
- Maximum 3 fix iterations
- After 3 iterations, escalate to user for manual review
- Track iteration count in task template

## Resources

- [Agent Prompts](references/agent_prompts.md) - Complete agent templates
- [Task Template](assets/task_template.md) - Task tracking format

## Trigger Phrases

- "implement feature" / "기능 구현"
- "feature development" / "피처 개발"
- "level X development" / "X 레벨 개발"
- "build feature" / "기능 만들기"
- "add functionality" / "기능 추가"
