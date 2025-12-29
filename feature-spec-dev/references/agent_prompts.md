# Agent Prompts Reference

Specialized agent prompts for each phase.

## Phase 1: DISCOVER

### Intent Analyzer Agent

```
Analyze user intent beyond written expression:

User Request: "{request}"
User Decisions: {askuser_responses}

Identify:
1. Primary intent (what they truly want)
2. Implicit requirements (unstated needs)
3. Hidden constraints (assumed limitations)
4. Success criteria (how they'll judge success)

Return JSON format:
{
  "primary_intent": "...",
  "implicit_requirements": [...],
  "hidden_constraints": [...],
  "success_criteria": [...],
  "recommended_clarifications": [...]
}
```

### Domain Researcher Agent

```
Research best practices for: {domain}

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
```

### Tech Context Analyzer Agent

```
Analyze codebase for implementation context:

Focus on:
- Existing architecture patterns
- Current tech stack and versions
- Related existing features
- Code conventions and standards
- Test patterns used

Return structured context report.
```

## Phase 2: SPEC

### Requirements Writer Agent

```
Create requirements using EARS format:

Intent Analysis: {intent_analysis}
Research Findings: {research_findings}

Structure:
1. Introduction with feature summary
2. Functional requirements (REQ-F-XXX)
3. Non-functional requirements (REQ-NF-XXX)
4. Constraints (CONST-XXX)
5. Out of scope items

Use patterns:
- WHEN [event] THEN system SHALL [response]
- IF [condition] THEN system SHALL [behavior]
- WHILE [state] system SHALL [action]

Return markdown document.
```

### Design Architect Agent

```
Create design document:

Requirements: {requirements_doc}
Best Practices: {best_practices}
Tech Context: {tech_context}

Include:
- Architecture overview
- Component diagram (Mermaid)
- Data models with schemas
- API contracts (if applicable)
- Integration points
- Error handling strategy
- Security considerations
- Testing strategy

Return markdown document.
```

## Phase 3: PLAN

### Task Generator Agent

```
Generate implementation tasks:

Requirements: {requirements}
Design: {design}

For each task create:
- Metadata (ID, priority, complexity, dependencies)
- Clear objective (one concern per task)
- Target files to create/modify
- Acceptance criteria (checkboxes)
- Implementation notes
- Test requirements

Rules:
- Maximum 2 hierarchy levels
- Each task = 1-2 hours of work
- ONE concern per task
- Code-only tasks (no deployment, docs)

Return JSON array of tasks.
```

### Dependency Mapper Agent

```
Create dependency graph:

Tasks: {task_list}

Determine:
- Which tasks block others
- Parallel execution opportunities
- Critical path

Return:
1. Dependency graph (Mermaid)
2. Execution phases
3. Recommended order
```

## Phase 4: IMPLEMENT

### Pre-Verifier Agent

```
Verify task completion:

Task: {task_id}
Target Files: {target_files}
Acceptance Criteria: {criteria}

Check:
- Target files exist
- Required functions implemented
- Tests written and passing

Return JSON format:
{
  "passed": true/false,
  "checks": {...},
  "gaps": [...],
  "message": "..."
}
```

## Synthesis Agent

```
Synthesize phase outputs into deliverable:

DISCOVER: {discovery_output}
SPEC: {spec_output}
PLAN: {plan_output}

Create comprehensive summary with:
1. Feature overview
2. Key decisions made
3. Implementation roadmap
4. Risk assessment
5. Next steps

Return markdown document.
```
