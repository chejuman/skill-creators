---
name: feature-spec-dev
description: Premium hierarchical multi-agent feature specification and development skill. Combines real-time research, deep intent analysis via AskUserQuestion, spec-driven development with EARS format, and task-based implementation with verification. Features 4-phase architecture (DISCOVER → SPEC → PLAN → IMPLEMENT), persistent tracking in .spec-docs/, and pre-task verification. Triggers on "기능 스펙", "feature spec", "spec 작성", "implementation plan", "기능 개발", "feature development".
---

# Feature Spec Dev

Premium feature specification and development skill with hierarchical multi-agent architecture.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FEATURE SPEC DEV ORCHESTRATOR                        │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 1: DISCOVER ──► Deep intent analysis + real-time research         │
│   └── IntentAnalyzer Agent (AskUserQuestion flow)                       │
│   └── DomainResearcher Agent (WebSearch, background)                    │
│   └── TechStackAnalyzer Agent (codebase analysis, background)           │
│ Phase 2: SPEC ──► Requirements + Design with research                   │
│   └── RequirementsWriter Agent (EARS format)                            │
│   └── DesignArchitect Agent (with latest patterns)                      │
│   └── Save to .spec-docs/specs/                                         │
│ Phase 3: PLAN ──► Task breakdown with dependencies                      │
│   └── TaskGenerator Agent (atomic tasks)                                │
│   └── DependencyMapper Agent (execution order)                          │
│   └── Save to .spec-docs/tasks/                                         │
│ Phase 4: IMPLEMENT ──► Verified task execution                          │
│   └── PreVerifier Agent (check previous task)                           │
│   └── TaskExecutor (one task at a time)                                 │
│   └── Update .spec-docs/tracking/                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Start new feature specification
/spec-dev "사용자 인증 기능"

# Get next implementation task
/spec-next

# Check implementation status
/spec-check

# Search documentation
/spec-search "authentication"
```

## Document Persistence Structure

All outputs saved to `.spec-docs/` directory:

```
.spec-docs/
├── index.md                      # Searchable index
├── config.json                   # Project configuration
│
├── discovery/                    # Phase 1 outputs
│   ├── intent_analysis.md        # Deep intent understanding
│   ├── domain_research.md        # Real-time research findings
│   ├── tech_context.md           # Codebase analysis
│   └── user_decisions.md         # AskUserQuestion responses
│
├── specs/                        # Phase 2 outputs
│   ├── {feature}/
│   │   ├── requirements.md       # EARS format requirements
│   │   ├── design.md             # Architecture & design
│   │   └── diagrams/             # Mermaid diagrams
│
├── plans/                        # Phase 3 outputs
│   ├── implementation_plan.md    # Master plan
│   └── task_breakdown.md         # Task dependencies
│
├── tasks/                        # Individual task files
│   ├── TASK-001.md
│   ├── TASK-002.md
│   └── ...
│
└── tracking/                     # Progress tracking
    ├── completion_status.json    # Task status
    ├── verification_log.md       # Verification history
    └── gaps_report.md            # Incomplete task log
```

## Phase 1: DISCOVER

### Step 1.1: Deep Intent Analysis

Use AskUserQuestion to understand user's true intent beyond their expression:

```
AskUserQuestion(questions=[
  {
    "question": "이 기능의 핵심 목적은 무엇인가요?",
    "header": "Core Purpose",
    "options": [
      {"label": "새로운 비즈니스 기능", "description": "매출/사용자 가치 창출"},
      {"label": "기존 기능 개선", "description": "성능/UX 향상"},
      {"label": "기술 부채 해결", "description": "리팩토링/마이그레이션"},
      {"label": "보안/규정 준수", "description": "필수 요구사항"}
    ],
    "multiSelect": false
  },
  {
    "question": "주요 사용자는 누구인가요?",
    "header": "Target Users",
    "options": [
      {"label": "최종 사용자 (End Users)", "description": "고객, 일반 사용자"},
      {"label": "내부 사용자 (Internal)", "description": "직원, 관리자"},
      {"label": "개발자 (Developers)", "description": "API 소비자, 통합"},
      {"label": "시스템 (System)", "description": "자동화, 백그라운드"}
    ],
    "multiSelect": true
  },
  {
    "question": "성공 기준은 무엇인가요?",
    "header": "Success Criteria",
    "options": [
      {"label": "기능 완성도", "description": "모든 요구사항 충족"},
      {"label": "성능 목표", "description": "응답시간, 처리량"},
      {"label": "사용자 만족도", "description": "UX 품질"},
      {"label": "코드 품질", "description": "테스트 커버리지, 유지보수성"}
    ],
    "multiSelect": true
  },
  {
    "question": "예상되는 주요 제약사항은?",
    "header": "Constraints",
    "options": [
      {"label": "기존 시스템 호환성", "description": "레거시 통합 필요"},
      {"label": "기술 스택 제한", "description": "특정 기술 사용 필수"},
      {"label": "시간/리소스 제한", "description": "일정 압박"},
      {"label": "특별한 제약 없음", "description": "자유로운 구현"}
    ],
    "multiSelect": true
  }
])
```

Save responses to `.spec-docs/discovery/user_decisions.md`.

### Step 1.2: Real-Time Domain Research

Launch parallel research agents before spec generation:

```
# Agent 1: Domain Best Practices
Task(
  subagent_type='general-purpose',
  description='Research domain best practices',
  prompt='''Research best practices for: {feature_description}

  Use WebSearch to find:
  - "{domain} best practices 2025"
  - "{feature_type} implementation patterns"
  - "{tech_stack} {feature_type} examples"

  Return JSON format:
  {
    "best_practices": [...],
    "common_patterns": [...],
    "anti_patterns": [...],
    "recommended_libraries": [...],
    "security_considerations": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)

# Agent 2: Technology Context
Task(
  subagent_type='Explore',
  description='Analyze codebase context',
  prompt='''Analyze the current codebase for context:
  - Existing architecture patterns
  - Current tech stack and versions
  - Related existing features
  - Code conventions and standards
  - Test patterns used

  Output detailed context report.
  ''',
  model='haiku',
  run_in_background=true
)

# Agent 3: Similar Implementations
Task(
  subagent_type='general-purpose',
  description='Research similar implementations',
  prompt='''Use WebSearch to find similar implementations:
  - Open source examples
  - Industry case studies
  - Common pitfalls to avoid

  Return structured findings.
  ''',
  model='haiku',
  run_in_background=true
)
```

Synchronize and save to `.spec-docs/discovery/`.

### Step 1.3: Intent Synthesis

Combine user decisions with research findings:

```
Task(
  subagent_type='general-purpose',
  description='Synthesize intent',
  prompt='''Synthesize deep understanding of user intent:

  User Input: {original_request}
  User Decisions: {askuser_responses}
  Domain Research: {research_findings}
  Codebase Context: {tech_context}

  Generate:
  1. True intent beyond written expression
  2. Implicit requirements user didn't state
  3. Potential risks they may not have considered
  4. Recommended scope adjustments

  Return JSON format.
  ''',
  model='sonnet'
)
```

Save to `.spec-docs/discovery/intent_analysis.md`.

## Phase 2: SPEC

### Step 2.1: Requirements Document (EARS Format)

Generate requirements with research-informed content:

```
Task(
  subagent_type='general-purpose',
  description='Write requirements',
  prompt='''Create comprehensive requirements document:

  Intent Analysis: {intent_analysis}
  Research Findings: {research_findings}

  Use EARS format:
  1. WHEN [event] THEN [system] SHALL [response]
  2. IF [precondition] THEN [system] SHALL [response]
  3. WHILE [state] THEN [system] SHALL [behavior]

  Include:
  - Introduction with feature summary
  - Numbered hierarchical requirements
  - User stories: "As a [role], I want [feature], so that [benefit]"
  - Acceptance criteria (research-informed)
  - Non-functional requirements
  - Out of scope items

  Output as markdown.
  ''',
  model='sonnet'
)
```

Save to `.spec-docs/specs/{feature}/requirements.md`.

### Step 2.2: User Review Cycle

```
AskUserQuestion(questions=[
  {
    "question": "요구사항이 정확하게 작성되었나요?",
    "header": "Requirements",
    "options": [
      {"label": "승인 - 다음 단계로", "description": "요구사항 확정"},
      {"label": "수정 필요", "description": "피드백 제공하겠음"},
      {"label": "범위 재조정", "description": "일부 제외/추가 필요"}
    ],
    "multiSelect": false
  }
])
```

Continue revision cycle until explicit approval.

### Step 2.3: Design Document

Generate design with latest patterns from research:

```
Task(
  subagent_type='general-purpose',
  description='Create design document',
  prompt='''Create design document:

  Requirements: {requirements_doc}
  Research Best Practices: {best_practices}
  Codebase Context: {tech_context}

  Include:
  - Architecture Overview
  - Component Diagram (Mermaid)
  - Data Models with schemas
  - API Contracts (if applicable)
  - Integration Points
  - Error Handling Strategy
  - Security Considerations (from research)
  - Testing Strategy

  Apply patterns from research findings.
  ''',
  model='sonnet'
)
```

Save to `.spec-docs/specs/{feature}/design.md`.

## Phase 3: PLAN

### Step 3.1: Task Generation

Generate atomic implementation tasks:

```
Task(
  subagent_type='general-purpose',
  description='Generate tasks',
  prompt='''Generate implementation task list:

  Requirements: {requirements_doc}
  Design: {design_doc}

  For each task create TASK-XXX.md with:
  - Metadata (ID, priority, complexity, dependencies)
  - Clear objective
  - Source files to reference
  - Target files to create/modify
  - Acceptance criteria (checkboxes)
  - Implementation notes
  - Test requirements

  Rules:
  - Maximum 2 hierarchy levels
  - Each task = 1-2 hours of work
  - ONE concern per task
  - Code-only tasks (no deployment, docs)

  Output as JSON array.
  ''',
  model='sonnet'
)
```

### Step 3.2: Dependency Mapping

```
Task(
  subagent_type='general-purpose',
  description='Map dependencies',
  prompt='''Create dependency graph:

  Tasks: {task_list}

  Determine:
  - Which tasks block others
  - Parallel execution opportunities
  - Critical path

  Output:
  1. Dependency graph (Mermaid)
  2. Execution phases
  3. Recommended order
  ''',
  model='sonnet'
)
```

Save to `.spec-docs/plans/implementation_plan.md`.

### Step 3.3: Create Individual Task Files

For each task, create `.spec-docs/tasks/TASK-XXX.md`:

```markdown
# TASK-001: {Task Title}

## Metadata

| Field        | Value              |
| ------------ | ------------------ |
| ID           | TASK-001           |
| Feature      | {feature_name}     |
| Priority     | 1                  |
| Complexity   | Low/Medium/High    |
| Status       | pending            |
| Dependencies | -                  |
| Blocks       | TASK-002, TASK-003 |

## Description

{Clear task description}

## Files to Create/Modify

| File | Action        | Purpose |
| ---- | ------------- | ------- |
| ...  | Create/Modify | ...     |

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Implementation Notes

{Research-informed implementation guidance}

## Tests Required

- [ ] {Test requirement 1}
- [ ] {Test requirement 2}

## Reference

- Requirements: {requirement_refs}
- Design: {design_section}
```

## Phase 4: IMPLEMENT

### Step 4.1: Pre-Task Verification

Before providing next task, verify previous completion:

```python
# scripts/verify_task.py
def verify_task(task_id: str) -> VerificationResult:
    task = load_task(task_id)

    checks = {
        'files_exist': check_files_exist(task['target_files']),
        'tests_exist': check_tests_exist(task['test_files']),
        'criteria_met': check_acceptance_criteria(task['criteria'])
    }

    return VerificationResult(
        passed=all(checks.values()),
        gaps=identify_gaps(checks)
    )
```

### Step 4.2: If Verification Fails

1. Mark task as `pending` in `completion_status.json`
2. Log gap to `verification_log.md`
3. Show warning with specific gaps

```markdown
## Verification Warning

TASK-003 is NOT complete:

- [ ] Missing: src/services/auth_service.py
- [ ] Missing: tests/test_auth_service.py

This task has been added back to pending.

Complete TASK-003 first or use `/spec-next --skip-verify`.
```

### Step 4.3: Execute Single Task

Only ONE task at a time:

```markdown
## Current Task: TASK-004

[Full task content from TASK-004.md]

---

After implementation:

1. Run tests: `pytest tests/`
2. Verify: `/spec-check --task TASK-004`
3. Next task: `/spec-next`
```

## Completion Tracking

`.spec-docs/tracking/completion_status.json`:

```json
{
  "feature": "user-authentication",
  "last_updated": "2025-12-28T10:00:00Z",
  "summary": {
    "total_tasks": 12,
    "completed": 4,
    "in_progress": 1,
    "pending": 7
  },
  "tasks": {
    "TASK-001": {
      "status": "completed",
      "verified_at": "2025-12-28T09:00:00Z"
    },
    "TASK-002": {
      "status": "in_progress",
      "started_at": "2025-12-28T10:00:00Z"
    }
  }
}
```

## Slash Commands

| Command                | Purpose                         |
| ---------------------- | ------------------------------- |
| `/spec-dev {idea}`     | Start new feature specification |
| `/spec-next`           | Get next task with verification |
| `/spec-check`          | Check implementation status     |
| `/spec-search {query}` | Search documentation            |
| `/spec-status`         | Show overall progress           |

## Scripts

| Script              | Purpose               |
| ------------------- | --------------------- |
| `doc_manager.py`    | Document persistence  |
| `verify_task.py`    | Pre-task verification |
| `search_docs.py`    | Full-text search      |
| `update_status.py`  | Status tracking       |
| `generate_tasks.py` | Task file generation  |

## Trigger Phrases

- "기능 스펙" / "feature spec"
- "스펙 작성" / "write spec"
- "구현 계획" / "implementation plan"
- "기능 개발" / "feature development"
- "다음 작업" / "next task"
- `/spec-dev`, `/spec-next`, `/spec-check`
