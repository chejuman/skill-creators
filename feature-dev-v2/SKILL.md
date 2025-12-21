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

## Resources

- [Agent Prompts](references/agent_prompts.md) - Complete agent templates
- [Task Template](assets/task_template.md) - Task tracking format

## Trigger Phrases

- "implement feature" / "기능 구현"
- "feature development" / "피처 개발"
- "level X development" / "X 레벨 개발"
- "build feature" / "기능 만들기"
- "add functionality" / "기능 추가"
