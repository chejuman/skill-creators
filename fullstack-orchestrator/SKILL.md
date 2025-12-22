---
name: fullstack-orchestrator
description: Multi-agent fullstack development orchestrator with configurable depth levels (1-5). Covers complete SDLC from requirements to deployment using 15+ specialized agents including Exploration, Architecture Alternatives, Implementation, Review with Fix Iteration, and DevOps. Features error recovery, context budget management, and inter-agent data schemas. Triggers on "fullstack development", "build application", "create app from spec", "spec-driven development", "level X development", or comprehensive development requests.
---

# Fullstack Orchestrator v2.0

Multi-agent spec-driven fullstack development with configurable depth and comprehensive quality assurance.

## Architecture Overview

```
                           ┌─────────────────────┐
                           │   User Request      │
                           └─────────┬───────────┘
                                     ▼
                    ┌────────────────────────────────┐
                    │    ORCHESTRATOR AGENT          │
                    │  (Coordination & Integration)  │
                    └────────────────┬───────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
┌───────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ PHASE 1       │          │ PHASE 1.5       │          │ PHASE 2         │
│ Requirements  │    ──►   │ Exploration     │    ──►   │ Architecture    │
└───────┬───────┘          └────────┬────────┘          └────────┬────────┘
        │                           │                            │
   ┌────┴────┐                ┌─────┴─────┐             ┌────────┼────────┐
   ▼         ▼                ▼     ▼     ▼             ▼        ▼        ▼
┌─────┐  ┌──────┐        ┌────┐ ┌────┐ ┌────┐     ┌────────┐┌────────┐┌────────┐
│Spec │  │Env   │        │Sim │ │Arch│ │Intg│     │Minimal ││Clean   ││Pragmat │
│Agent│  │Setup │        │Exp │ │Exp │ │Exp │     │Arch    ││Arch    ││Arch    │
└─────┘  └──────┘        └────┘ └────┘ └────┘     └────────┘└────────┘└────────┘

        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
┌───────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ PHASE 3       │          │ PHASE 4         │          │ PHASE 4b        │
│ Implementation│    ──►   │ Quality         │    ──►   │ Fix Iteration   │
└───────┬───────┘          └────────┬────────┘          └────────┬────────┘
        │                           │                            │
   ┌────┼────┐                ┌─────┼─────┐                      │
   ▼    ▼    ▼                ▼     ▼     ▼                      ▼
┌────┐┌────┐┌────┐       ┌────┐ ┌────┐ ┌────┐              ┌──────────┐
│Back││Fron││DB  │       │Test│ │Sec │ │Perf│              │Fix+Lite  │
│end ││tend││    │       │Eng │ │Aud │ │Opt │              │Review    │
└────┘└────┘└────┘       └────┘ └────┘ └────┘              └──────────┘

        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
┌───────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ PHASE 5       │          │ PHASE 6         │          │ COMPLETE        │
│ Documentation │    ──►   │ Deployment      │    ──►   │ Summary         │
└───────────────┘          └─────────────────┘          └─────────────────┘
```

## Development Levels

| Level | Explorers | Architects | Reviewers | Use Case |
|-------|-----------|------------|-----------|----------|
| 1 | 1 | Skip | 1 | Quick prototype, MVP |
| 2 | 2 | 1 | 2 | Simple application |
| 3 | 3 | 2 | 3 | Standard fullstack app (default) |
| 4 | 3 | 3 | 3 | Complex enterprise app |
| 5 | 3+ | 3 | 3+ | Large-scale system |

**Quality Metrics by Level:**

| Level | Min Files Analyzed | Review Threshold | Max Fix Iterations |
|-------|-------------------|------------------|-------------------|
| 1 | 5 | 0 high severity | 1 |
| 2 | 10 | 0 high severity | 2 |
| 3 | 15 | 0 high, ≤2 medium | 3 |
| 4 | 20 | 0 high, ≤1 medium | 3 |
| 5 | 25+ | 0 high/medium | 5 |

## Quick Start

### 1. Start New Project
```
"Create a task management app (level 3)"
"풀스택 e-commerce 플랫폼 만들어줘 (레벨 4)"
```

### 2. From Existing Spec
```
"Build from spec.md using level 2"
"spec 기반으로 레벨 3 개발 시작"
```

---

## Workflow Phases

### Phase 1: Requirements Analysis

**Trigger**: User provides feature description or requirements

```
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Requirements Analyst Agent]
Analyze user requirements and create formal specification:

1. Extract functional requirements (FR-XXX)
2. Identify non-functional requirements (NFR-XXX)
3. Define acceptance criteria
4. Create user stories
5. Output: spec.md following template

Reference: [Spec Template](assets/spec_template.md)
''', description='Analyze requirements')
```

**Environment Setup (AskUserQuestion):**

```
AskUserQuestion(questions=[
  {
    "question": "어떤 데이터베이스를 사용할까요?",
    "header": "Database",
    "options": [
      {"label": "PostgreSQL (Recommended)", "description": "Production-ready, full SQL"},
      {"label": "SQLite", "description": "Development/prototype"},
      {"label": "MySQL", "description": "Widely used"}
    ],
    "multiSelect": false
  },
  {
    "question": "인증 방식을 선택해주세요",
    "header": "Auth",
    "options": [
      {"label": "JWT + OAuth2", "description": "Stateless, API-friendly"},
      {"label": "Session-based", "description": "Traditional, server-side"},
      {"label": "Third-party (Auth0/Clerk)", "description": "Managed service"}
    ],
    "multiSelect": false
  }
])
```

**Output Schema:**
```json
{
  "spec": {
    "project_name": "...",
    "requirements": {"functional": [], "non_functional": []},
    "user_stories": [],
    "constraints": [],
    "out_of_scope": []
  },
  "environment": {
    "database": "PostgreSQL|SQLite|MySQL",
    "auth": "JWT|Session|Third-party"
  },
  "suggested_level": 3
}
```

---

### Phase 1.5: Codebase Exploration (NEW)

**For existing codebases** - Skip for greenfield projects

Spawn Exploration Agents in **ONE message** for parallel execution:

```
# CRITICAL: All Task calls in ONE message for true parallelism
Task(
  subagent_type='Explore',
  prompt='Find similar features and existing patterns in codebase...',
  description='Explore similar features',
  model='haiku'
)
Task(
  subagent_type='Explore',
  prompt='Map architecture layers, abstractions, and data flow...',
  description='Explore architecture',
  model='haiku'
)
Task(
  subagent_type='Explore',
  prompt='Identify integration points, APIs, and dependencies...',
  description='Explore integrations',
  model='haiku'
)
```

**Explorer Output Schema:**
```json
{
  "focus": "Similar Features|Architecture|Integration",
  "key_files": ["path1", "path2"],
  "patterns_found": [
    {"pattern": "...", "location": "file:line", "relevance": "..."}
  ],
  "recommendations": ["..."],
  "files_to_read": ["top 5-10 files"]
}
```

**Context Budget by Codebase Size:**

| Codebase Size | Files | Limit per Explorer |
|---------------|-------|-------------------|
| Small (< 100) | < 100 | 10 files |
| Medium | 100-1000 | 5-7 files |
| Large (1000+) | 1000+ | 3-5 files |

---

### Phase 2: Architecture Design

Spawn Architecture Agents in **ONE message** for parallel alternatives:

```
Task(
  subagent_type='Plan',
  prompt='Design MINIMAL approach: smallest change, maximum reuse...',
  description='Design minimal architecture'
)
Task(
  subagent_type='Plan',
  prompt='Design CLEAN ARCHITECTURE: maintainability, abstractions...',
  description='Design clean architecture'
)
Task(
  subagent_type='Plan',
  prompt='Design PRAGMATIC approach: balance speed and quality...',
  description='Design pragmatic architecture'
)
```

**Architecture Output Schema:**
```json
{
  "approach": "MINIMAL|CLEAN|PRAGMATIC",
  "philosophy": "...",
  "architecture": {
    "components": [{"name": "...", "type": "...", "responsibility": "..."}],
    "patterns": ["Repository", "Factory", "..."],
    "data_flow": "..."
  },
  "file_changes": [
    {"path": "...", "action": "CREATE|MODIFY", "lines_est": 50}
  ],
  "trade_offs": {"pros": ["..."], "cons": ["..."]},
  "estimated_complexity": "LOW|MEDIUM|HIGH"
}
```

**Present Options to User:**
```markdown
## Architecture Options

### Option 1: Minimal Approach
- **Changes:** X files | **Complexity:** LOW
- **Pros:** Fast, low risk
- **Cons:** May accumulate tech debt

### Option 2: Clean Architecture
- **Changes:** Y files | **Complexity:** MEDIUM
- **Pros:** Maintainable, testable
- **Cons:** More initial work

### Option 3: Pragmatic Balance
- **Changes:** Z files | **Complexity:** MEDIUM
- **Pros:** Good balance
- **Cons:** Some compromises

**Recommendation:** [approach] because [reasoning]
```

**WAIT FOR USER APPROVAL BEFORE PHASE 3**

---

### Phase 3: Implementation

**Sequential with dependencies:**

```
# 1. Database & Models first
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Database Agent] Implement models and migrations:
- SQLAlchemy models from schema
- Alembic migrations
- Seed data scripts
Reference: [Backend Patterns](references/backend_patterns.md)
''', description='Implement database layer')

# 2. Backend API (depends on DB)
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Backend Developer Agent] Implement FastAPI backend:
- CRUD endpoints
- Business logic services
- Authentication middleware
- Error handling
Reference: [Backend Patterns](references/backend_patterns.md)
''', description='Implement backend API')

# 3. Frontend (can start after API design)
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Frontend Developer Agent] Implement React frontend:
- Component architecture
- State management (Zustand/TanStack Query)
- API integration
- Responsive UI with shadcn/ui
Reference: [Frontend Patterns](references/frontend_patterns.md)
''', description='Implement frontend')
```

---

### Phase 4: Quality Assurance

**Parallel quality checks** in ONE message:

```
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Test Engineer Agent] Create test suite:
- Unit tests (pytest/vitest)
- Integration tests
- E2E tests (Playwright)
- Coverage report (target: 80%+)
''', description='Create test suite')

Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Security Auditor Agent] Security assessment:
- OWASP Top 10 check
- Dependency vulnerabilities
- Auth security review
CONFIDENCE_THRESHOLD: 0.8
Reference: [Security Checklist](references/security_checklist.md)
''', description='Security audit')

Task(subagent_type='general-purpose', model='haiku', prompt='''
[Performance Optimizer Agent] Performance analysis:
- Database query optimization
- Bundle size analysis
- Lighthouse metrics
''', description='Performance optimization')

Task(subagent_type='general-purpose', model='haiku', prompt='''
[Code Quality Reviewer] Review for quality:
- DRY violations
- Readability and naming
- Complexity metrics
CONFIDENCE_THRESHOLD: 0.8
''', description='Code quality review')

Task(subagent_type='general-purpose', model='haiku', prompt='''
[Conventions Reviewer] Review for conventions:
- Project patterns adherence
- Consistency with existing code
- Abstraction usage
CONFIDENCE_THRESHOLD: 0.8
''', description='Conventions review')
```

**Review Consolidation:**
```python
def consolidate_reviews(reviewer_outputs):
    consolidated = {
        "all_issues": [],
        "by_severity": {"HIGH": [], "MEDIUM": [], "LOW": []},
        "overall_status": "APPROVED"
    }

    for output in reviewer_outputs:
        for issue in output.get("issues", []):
            if issue["confidence"] >= 0.8:
                consolidated["all_issues"].append(issue)
                consolidated["by_severity"][issue["severity"]].append(issue)

        if output.get("approval") == "NEEDS_CHANGES":
            consolidated["overall_status"] = "NEEDS_CHANGES"

    return consolidated
```

**Approval Decision Matrix:**

| High Issues | Medium Issues | Decision |
|-------------|---------------|----------|
| 0 | 0 | APPROVED |
| 0 | 1-2 (Level 3) | APPROVED with notes |
| 0 | 3+ | NEEDS_CHANGES |
| 1+ | Any | NEEDS_CHANGES |

---

### Phase 4b: Fix Iteration Cycle (NEW)

When review status is **NEEDS_CHANGES**:

```
Phase 4b: Fix Iteration (max 3 iterations)
    │
    ├─► Fix Agent ──► Address identified issues
    │
    ├─► Lite Review ──► Re-check ONLY changed files
    │
    └─► Decision ──► APPROVED? → Phase 5 : → Repeat 4b
```

**Fix Agent:**
```
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Fix Agent] Address review issues:
{{high_severity_issues}}
{{medium_severity_issues}}

For each issue:
1. Read the file
2. Apply the fix
3. Verify fix doesn't break other code

Return list of fixes applied.
''', description='Fix review issues')
```

**Lite Review:**
```
Task(subagent_type='general-purpose', model='haiku', prompt='''
[Lite Review Agent] Re-review ONLY fixed files:
{{fixed_files}}

Check:
1. Original issues resolved
2. No new issues introduced
3. Changes are minimal

Return: APPROVED or remaining issues.
''', description='Lite review of fixes')
```

**Iteration Limits:**
- Maximum iterations based on level (see Quality Metrics)
- After max iterations, escalate to user

---

### Phase 5: Documentation

```
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[Documentation Generator Agent] Generate documentation:
- README.md with setup instructions
- API documentation (OpenAPI)
- Component documentation
- Architecture decision records (ADR)
- Deployment guide
''', description='Generate documentation')
```

---

### Phase 6: Deployment

```
Task(subagent_type='general-purpose', model='sonnet', prompt='''
[DevOps Engineer Agent] Setup deployment:
- Dockerfile & docker-compose
- CI/CD pipeline (GitHub Actions)
- Environment configuration
Reference: [DevOps Patterns](references/devops_patterns.md)
''', description='Setup deployment')

Task(subagent_type='general-purpose', model='haiku', prompt='''
[Deployment Agent] Execute deployment:
- Build artifacts
- Run migrations
- Health checks
''', description='Execute deployment')
```

---

## Error Recovery System

### Agent Failure Handling

| Phase | Failure | Recovery |
|-------|---------|----------|
| Exploration | 1 of 3 fails | Continue with 2 explorers |
| Exploration | 2+ fail | Ask user for manual context |
| Architecture | 1 of 3 fails | Present 2 options |
| Architecture | All fail | User provides architecture |
| Implementation | Agent fails | Retry once, then escalate |
| Review | 1 of 3+ fails | Proceed with available output |
| Review | 2+ fail | Retry or skip with warning |

**Recovery Flow:**
```
1. DETECT: Check if agent returned valid output
2. REPORT: Log which agent failed
3. DECIDE: Ask user how to proceed
   - Retry failed agent
   - Continue with partial results
   - Abort and restart phase
4. RECOVER: Execute chosen action
```

---

## Inter-Agent Data Format

### Exploration Summary Schema
```json
{
  "exploration_summary": {
    "similar_features": {...},
    "architecture": {...},
    "integrations": {...},
    "combined_key_files": ["path1", "path2"],
    "combined_recommendations": [...]
  }
}
```

### Implementation Handoff Schema
```json
{
  "implementation_context": {
    "chosen_architecture": "MINIMAL|CLEAN|PRAGMATIC",
    "file_changes": [...],
    "implementation_steps": [...],
    "tech_stack": {...}
  }
}
```

### Review Results Schema
```json
{
  "review_results": {
    "overall_status": "APPROVED|NEEDS_CHANGES",
    "issues": [{
      "file": "path",
      "line": 123,
      "severity": "HIGH|MEDIUM|LOW",
      "confidence": 0.92,
      "description": "...",
      "suggestion": "..."
    }],
    "iteration_count": 1
  }
}
```

---

## Tech Stack (Default)

| Layer | Technology |
|-------|------------|
| Backend | FastAPI + SQLAlchemy + Pydantic |
| Frontend | React + TypeScript + shadcn/ui + Tailwind |
| Database | PostgreSQL (prod) / SQLite (dev) |
| Auth | JWT + OAuth2 |
| Testing | pytest + vitest + Playwright |
| DevOps | Docker + GitHub Actions |

---

## Agent Reference

| Agent | Model | Phase | Responsibility |
|-------|-------|-------|----------------|
| Orchestrator | opus | All | Overall coordination |
| Requirements Analyst | sonnet | 1 | Spec creation |
| Explorer (x3) | haiku | 1.5 | Codebase analysis |
| Architect (x3) | sonnet | 2 | Design alternatives |
| Database Agent | sonnet | 3 | Schema & models |
| Backend Developer | sonnet | 3 | FastAPI implementation |
| Frontend Developer | sonnet | 3 | React implementation |
| Test Engineer | sonnet | 4 | Test suite creation |
| Security Auditor | sonnet | 4 | Security assessment |
| Performance Optimizer | haiku | 4 | Performance tuning |
| Code Quality Reviewer | haiku | 4 | DRY, readability |
| Conventions Reviewer | haiku | 4 | Pattern adherence |
| Fix Agent | sonnet | 4b | Issue resolution |
| Lite Reviewer | haiku | 4b | Focused re-check |
| Documentation Generator | sonnet | 5 | Docs & README |
| DevOps Engineer | sonnet | 6 | CI/CD & Docker |

---

## Resources

- [Agent Prompts](references/agent_prompts.md) - Detailed agent instructions
- [Backend Patterns](references/backend_patterns.md) - FastAPI patterns
- [Frontend Patterns](references/frontend_patterns.md) - React patterns
- [Security Checklist](references/security_checklist.md) - Security guidelines
- [DevOps Patterns](references/devops_patterns.md) - Deployment patterns
- [Spec Template](assets/spec_template.md) - Specification template
- [Task Template](assets/task_template.md) - Execution tracking

---

## Trigger Phrases

- "fullstack development" / "풀스택 개발"
- "build application from spec" / "스펙 기반 앱 개발"
- "create new app" / "새 앱 만들어줘"
- "level X development" / "레벨 X 개발"
- "spec-driven development" / "스펙 드리븐 개발"
