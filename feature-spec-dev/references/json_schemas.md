# JSON Schemas Reference

Data exchange formats for inter-agent communication.

## Phase 1: Discovery Output

```json
{
  "phase": "DISCOVER",
  "timestamp": "2025-12-28T10:00:00Z",
  "intent_analysis": {
    "primary_intent": "string",
    "core_purpose": "new_feature|enhancement|tech_debt|compliance",
    "target_users": ["end_users", "internal", "developers", "system"],
    "success_criteria": ["functionality", "performance", "ux", "code_quality"],
    "constraints": ["legacy_compat", "tech_stack", "timeline", "none"],
    "implicit_requirements": ["string"],
    "potential_risks": ["string"]
  },
  "domain_research": {
    "best_practices": [{ "practice": "string", "source": "string" }],
    "common_patterns": ["string"],
    "anti_patterns": ["string"],
    "recommended_libraries": [{ "name": "string", "purpose": "string" }],
    "security_considerations": ["string"]
  },
  "tech_context": {
    "architecture_pattern": "string",
    "tech_stack": { "language": "string", "framework": "string" },
    "existing_features": ["string"],
    "code_conventions": ["string"],
    "test_patterns": ["string"]
  }
}
```

## Phase 2: Spec Output

```json
{
  "phase": "SPEC",
  "timestamp": "2025-12-28T11:00:00Z",
  "requirements": {
    "functional": [
      {
        "id": "REQ-F-001",
        "type": "event|state|unwanted|ubiquitous",
        "statement": "WHEN ... THEN system SHALL ...",
        "priority": "must|should|may",
        "acceptance_criteria": ["string"]
      }
    ],
    "non_functional": [
      {
        "id": "REQ-NF-001",
        "category": "performance|security|usability|reliability",
        "statement": "string",
        "metric": "string"
      }
    ],
    "constraints": ["string"],
    "out_of_scope": ["string"]
  },
  "design": {
    "architecture_overview": "string",
    "components": [{ "name": "string", "responsibility": "string" }],
    "data_models": [{ "name": "string", "fields": [] }],
    "api_contracts": [{ "endpoint": "string", "method": "string" }],
    "integration_points": ["string"],
    "error_handling": "string",
    "security_measures": ["string"],
    "test_strategy": "string"
  }
}
```

## Phase 3: Plan Output

```json
{
  "phase": "PLAN",
  "timestamp": "2025-12-28T12:00:00Z",
  "tasks": [
    {
      "id": "TASK-001",
      "title": "string",
      "feature": "string",
      "priority": 1,
      "complexity": "Low|Medium|High",
      "dependencies": ["TASK-XXX"],
      "blocks": ["TASK-XXX"],
      "description": "string",
      "files": [
        { "path": "string", "action": "Create|Modify", "purpose": "string" }
      ],
      "acceptance_criteria": ["string"],
      "implementation_notes": "string",
      "tests": ["string"],
      "requirement_refs": "REQ-F-001",
      "design_refs": "Component X"
    }
  ],
  "execution_phases": [
    { "phase": 1, "name": "Foundation", "tasks": ["TASK-001", "TASK-002"] }
  ],
  "critical_path": ["TASK-001", "TASK-003", "TASK-007"],
  "parallel_opportunities": [["TASK-002", "TASK-003"]]
}
```

## Verification Result

```json
{
  "task_id": "TASK-001",
  "passed": true,
  "checked_at": "2025-12-28T14:00:00Z",
  "checks": {
    "files_exist": true,
    "tests_written": true,
    "criteria_met": true
  },
  "gaps": [],
  "message": "All checks passed"
}
```

## Completion Status

```json
{
  "feature": "feature-name",
  "last_updated": "2025-12-28T15:00:00Z",
  "summary": {
    "total_tasks": 12,
    "completed": 4,
    "in_progress": 1,
    "pending": 7
  },
  "tasks": {
    "TASK-001": {
      "status": "completed",
      "verified_at": "2025-12-28T10:00:00Z"
    },
    "TASK-002": {
      "status": "in_progress",
      "started_at": "2025-12-28T14:00:00Z"
    },
    "TASK-003": {
      "status": "pending",
      "blocked_by": ["TASK-002"]
    }
  }
}
```

## Config

```json
{
  "feature": "feature-name",
  "created_at": "2025-12-28T09:00:00Z",
  "phases": {
    "discovery": "completed",
    "spec": "completed",
    "plan": "in_progress",
    "implement": "pending"
  },
  "current_phase": "plan"
}
```
