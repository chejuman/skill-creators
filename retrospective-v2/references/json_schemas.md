# JSON Schemas for Agent Communication

Structured data formats for inter-agent communication in retrospective-v2.

## Base Message Schema

All agents use this base structure:

```json
{
  "phase": "COLLECT|ANALYZE|SYNTHESIZE|DELIVER",
  "agent_id": "unique-agent-identifier",
  "timestamp": "ISO-8601 timestamp",
  "status": "pending|running|complete|error",
  "data": { },
  "insights": ["array of string insights"],
  "confidence": 0.0-1.0,
  "errors": []
}
```

## Phase 1: COLLECT Schemas

### Git Analyzer Output

```json
{
  "phase": "COLLECT",
  "agent_id": "git-analyzer",
  "timestamp": "2025-12-27T10:30:00Z",
  "status": "complete",
  "data": {
    "commit_count": 42,
    "date_range": {
      "start": "2025-12-01",
      "end": "2025-12-27"
    },
    "hotspots": [
      {
        "file": "src/services/auth.ts",
        "changes": 15,
        "authors": ["dev1", "dev2"]
      }
    ],
    "commit_patterns": {
      "by_day": {
        "Monday": 12,
        "Tuesday": 8,
        "Wednesday": 10,
        "Thursday": 7,
        "Friday": 5
      },
      "by_hour": {
        "09": 5,
        "10": 8,
        "14": 12,
        "15": 10
      }
    },
    "author_stats": [
      {
        "name": "Developer 1",
        "commits": 20,
        "additions": 1500,
        "deletions": 300
      }
    ],
    "merge_count": 8,
    "revert_count": 1
  },
  "insights": [
    "High activity on auth.ts suggests ongoing feature development",
    "Friday commits lower - potential end-of-week fatigue"
  ],
  "confidence": 0.92
}
```

### Code Analyzer Output

```json
{
  "phase": "COLLECT",
  "agent_id": "code-analyzer",
  "timestamp": "2025-12-27T10:31:00Z",
  "status": "complete",
  "data": {
    "files_changed": 35,
    "file_types": {
      ".ts": 20,
      ".tsx": 10,
      ".test.ts": 5
    },
    "test_ratio": 0.25,
    "doc_files": 3,
    "new_dependencies": ["zod@3.22.0", "react-query@5.0.0"],
    "complexity_indicators": [
      {
        "file": "src/utils/parser.ts",
        "indicator": "high_cyclomatic",
        "value": 25
      }
    ]
  },
  "insights": [
    "Test ratio below recommended 0.5 threshold",
    "New validation library (zod) introduced"
  ],
  "confidence": 0.88
}
```

### Metrics Collector Output

```json
{
  "phase": "COLLECT",
  "agent_id": "metrics-collector",
  "timestamp": "2025-12-27T10:32:00Z",
  "status": "complete",
  "data": {
    "loc_estimate": 45000,
    "test_files": 120,
    "source_files": 450,
    "config_files": [
      "tsconfig.json",
      "jest.config.js",
      ".eslintrc",
      "docker-compose.yml"
    ],
    "dependencies": 85,
    "has_ci": true,
    "has_tests": true,
    "build_time_seconds": 45
  },
  "insights": [
    "Mature project with CI/CD infrastructure",
    "Dependency count moderate"
  ],
  "confidence": 0.95
}
```

### Pattern Detector Output (Level >= 3)

```json
{
  "phase": "COLLECT",
  "agent_id": "pattern-detector",
  "timestamp": "2025-12-27T10:33:00Z",
  "status": "complete",
  "data": {
    "patterns_found": [
      {
        "name": "Repository Pattern",
        "files": ["src/repositories/*.ts"],
        "quality": "good"
      },
      {
        "name": "Service Layer",
        "files": ["src/services/*.ts"],
        "quality": "inconsistent"
      }
    ],
    "anti_patterns": [
      {
        "name": "God Object",
        "file": "src/utils/helpers.ts",
        "severity": "medium"
      }
    ],
    "duplication_indicators": [
      {
        "files": ["src/api/users.ts", "src/api/products.ts"],
        "similarity": 0.75
      }
    ],
    "naming_consistency": 0.82,
    "error_handling_score": 0.68
  },
  "insights": [
    "Service layer pattern inconsistently applied",
    "Error handling needs standardization"
  ],
  "confidence": 0.78
}
```

## Phase 2: ANALYZE Schemas

### Framework Applicator Output

```json
{
  "phase": "ANALYZE",
  "agent_id": "framework-applicator",
  "framework": "Start-Stop-Continue",
  "timestamp": "2025-12-27T10:35:00Z",
  "status": "complete",
  "data": {
    "start": [
      {
        "item": "Implement pre-commit hooks",
        "evidence": "15% of PRs had linting issues",
        "impact": "high"
      }
    ],
    "stop": [
      {
        "item": "Manual deployments to staging",
        "evidence": "2 failed deploys due to human error",
        "impact": "medium"
      }
    ],
    "continue": [
      {
        "item": "Code review within 4 hours",
        "evidence": "95% of PRs reviewed same day",
        "impact": "high"
      }
    ]
  },
  "summary": "Team shows strong code review culture but deployment process needs automation",
  "confidence": 0.85
}
```

### Gap Analyzer Output

```json
{
  "phase": "ANALYZE",
  "agent_id": "gap-analyzer",
  "timestamp": "2025-12-27T10:36:00Z",
  "status": "complete",
  "data": {
    "test_gaps": [
      {
        "area": "API integration tests",
        "severity": "high",
        "suggestion": "Add test suite for /api/v2/* endpoints"
      }
    ],
    "doc_gaps": [
      {
        "area": "API documentation",
        "severity": "medium",
        "suggestion": "Generate OpenAPI spec from types"
      }
    ],
    "process_gaps": [
      {
        "area": "Deployment automation",
        "severity": "high",
        "suggestion": "Implement CI/CD for staging"
      }
    ],
    "tech_debt": [
      {
        "area": "Legacy auth module",
        "severity": "high",
        "suggestion": "Migrate to new auth library"
      }
    ],
    "skill_gaps": [
      {
        "area": "Performance optimization",
        "severity": "low",
        "suggestion": "Training on profiling tools"
      }
    ]
  },
  "priority_order": [
    "test_gaps",
    "process_gaps",
    "tech_debt",
    "doc_gaps",
    "skill_gaps"
  ],
  "confidence": 0.82
}
```

### Root Cause Analyzer Output (Level >= 4)

```json
{
  "phase": "ANALYZE",
  "agent_id": "root-cause-analyzer",
  "timestamp": "2025-12-27T10:37:00Z",
  "status": "complete",
  "data": {
    "issues": [
      {
        "issue": "Frequent production hotfixes",
        "why_chain": [
          "Bugs not caught before deployment",
          "Integration tests incomplete",
          "Test coverage prioritized over depth",
          "Sprint velocity pressure",
          "Unrealistic sprint commitments"
        ],
        "root_cause": "Sprint planning doesn't account for quality time",
        "preventive_action": "Reserve 20% of sprint capacity for testing"
      }
    ]
  },
  "systemic_patterns": [
    "Velocity over quality trade-off",
    "Technical debt accumulation cycle"
  ],
  "confidence": 0.75
}
```

## Phase 3: SYNTHESIZE Schemas

### Insight Synthesizer Output

```json
{
  "phase": "SYNTHESIZE",
  "agent_id": "insight-synthesizer",
  "timestamp": "2025-12-27T10:40:00Z",
  "status": "complete",
  "data": {
    "key_takeaways": [
      "Deployment automation is the highest-impact improvement",
      "Test coverage improving but integration tests needed",
      "Team collaboration strong, maintain code review culture"
    ],
    "patterns_summary": "Repository pattern well-established; service layer needs standardization",
    "team_insights": "Strong collaboration, potential for knowledge silos in auth module",
    "process_insights": "Manual deployment is primary bottleneck",
    "technical_health": {
      "score": 72,
      "summary": "Good foundation with specific areas needing attention"
    }
  },
  "executive_summary": "The team delivered well but deployment automation and test coverage are priority improvements for next sprint.",
  "confidence": 0.88
}
```

### Action Generator Output

```json
{
  "phase": "SYNTHESIZE",
  "agent_id": "action-generator",
  "timestamp": "2025-12-27T10:41:00Z",
  "status": "complete",
  "data": {
    "immediate": [
      {
        "action": "Set up CI/CD pipeline for staging",
        "owner": "DevOps Lead",
        "effort": "M",
        "impact": "High",
        "category": "process"
      }
    ],
    "short_term": [
      {
        "action": "Add integration tests for payment API",
        "owner": "Backend Team",
        "effort": "L",
        "impact": "High",
        "category": "technical"
      },
      {
        "action": "Document error handling patterns",
        "owner": "Tech Lead",
        "effort": "S",
        "impact": "Medium",
        "category": "technical"
      }
    ],
    "backlog": [
      {
        "action": "Refactor helpers.ts into focused modules",
        "owner": "Any Developer",
        "effort": "M",
        "impact": "Low",
        "category": "technical"
      }
    ]
  },
  "total_actions": 4,
  "confidence": 0.9
}
```

### Priority Scorer Output (Level >= 4)

```json
{
  "phase": "SYNTHESIZE",
  "agent_id": "priority-scorer",
  "timestamp": "2025-12-27T10:42:00Z",
  "status": "complete",
  "data": {
    "scored_actions": [
      {
        "action": "Set up CI/CD pipeline for staging",
        "impact": 9,
        "confidence": 8,
        "ease": 6,
        "ice_score": 7.67
      },
      {
        "action": "Add integration tests for payment API",
        "impact": 8,
        "confidence": 9,
        "ease": 5,
        "ice_score": 7.33
      }
    ],
    "top_3_recommendations": [
      "Set up CI/CD pipeline for staging",
      "Add integration tests for payment API",
      "Document error handling patterns"
    ],
    "quick_wins": ["Document error handling patterns"]
  },
  "confidence": 0.85
}
```

## Aggregated Phase Output

Each phase produces an aggregated output:

```json
{
  "phase": "COLLECT",
  "timestamp": "2025-12-27T10:35:00Z",
  "agents_completed": 4,
  "agents_failed": 0,
  "aggregated_data": {
    "git": {},
    "code": {},
    "metrics": {},
    "patterns": {}
  },
  "combined_insights": [],
  "overall_confidence": 0.88
}
```

## Error Schema

When agents fail:

```json
{
  "phase": "COLLECT",
  "agent_id": "git-analyzer",
  "timestamp": "2025-12-27T10:30:00Z",
  "status": "error",
  "data": null,
  "errors": [
    {
      "code": "GIT_NOT_FOUND",
      "message": "Not a git repository",
      "recoverable": false
    }
  ],
  "confidence": 0.0
}
```
