# Phase Output Templates

## Phase 0: Initialization Output

```markdown
# DevFlow Project Initialized

## Project Details

| Field   | Value             |
| ------- | ----------------- |
| Idea    | {idea}            |
| Domain  | {domain}          |
| Version | v0.0 (Idea Stage) |
| Target  | v10.0+            |
| Created | {timestamp}       |

## Structure Created

.devflow/
├── project.json
├── versions/v0.0-idea.md
├── research/
├── features/backlog.json
├── plans/
└── meta/

## Next Steps

1. `/devflow-research` - Run multi-agent research
2. `/devflow-suggest` - Get feature suggestions
```

## Phase 2: Research Output

```markdown
# Research Synthesis: {domain}

## Tech Stack Recommendations

### Languages

| Language | Use Case | Maturity |
| -------- | -------- | -------- |
| {lang}   | {use}    | {level}  |

### Frameworks

- **{framework}**: {description}

## Market Trends

### Key Trends

1. {trend1}
2. {trend2}

### Growth Forecast

{forecast}

## Open Source Landscape

| Repository | Stars   | Key Features |
| ---------- | ------- | ------------ |
| {repo}     | {stars} | {features}   |

## Security Considerations

### OWASP Top 10 Relevance

- {vulnerability}: {mitigation}

### Compliance

- {framework}: {requirement}

## Competitive Analysis

| Competitor | Strengths | Weaknesses | Gap   |
| ---------- | --------- | ---------- | ----- |
| {name}     | {str}     | {weak}     | {gap} |

## Recommendations

1. **Architecture**: {recommendation}
2. **Technology**: {recommendation}
3. **Differentiation**: {recommendation}
```

## Phase 4: Feature Suggestions

```markdown
# Feature Suggestions for v{X}.0

## Recommended Features

### 1. {Feature Name} (Recommended)

| Metric     | Value           |
| ---------- | --------------- |
| RICE Score | {score}         |
| Reach      | {reach}         |
| Impact     | {impact}        |
| Confidence | {confidence}%   |
| Effort     | {effort} months |
| Priority   | {moscow}        |

**Description**: {description}

**User Value**: {value}

**Technical Approach**: {approach}

---

(Repeat for 3-5 features)

## Selection Summary

| Feature | RICE    | Priority | Selected |
| ------- | ------- | -------- | -------- |
| {name}  | {score} | {moscow} | {yes/no} |
```

## Phase 5: Development Plan

```markdown
# Development Plan: v{X}.0

## Overview

| Metric           | Value         |
| ---------------- | ------------- |
| Features         | {count}       |
| Total Tasks      | {count}       |
| Estimated Effort | {days} days   |
| Target Duration  | {weeks} weeks |

## Features

### Feature 1: {Name}

**Architecture**:
{architecture diagram or description}

**Tasks**:

| ID       | Task   | Effort  | Dependencies |
| -------- | ------ | ------- | ------------ |
| TASK-001 | {task} | {days}d | -            |
| TASK-002 | {task} | {days}d | TASK-001     |

**Risks**:

- {risk}: {mitigation}

---

## Dependency Graph

TASK-001 ──► TASK-002 ──► TASK-003
│
└──► TASK-004

## Critical Path

1. TASK-001 → TASK-002 → TASK-005 → TASK-008

## Risk Register

| Risk   | Probability | Impact   | Mitigation |
| ------ | ----------- | -------- | ---------- |
| {risk} | {prob}      | {impact} | {action}   |
```

## Phase 7: Version Advancement

```markdown
# Version Transition: v{X-1}.0 → v{X}.0

## Completed: v{X-1}.0

### Features Delivered

| Feature | Status   | Notes   |
| ------- | -------- | ------- |
| {name}  | Complete | {notes} |

### Metrics

- Features: {count}
- Tasks: {count}
- Duration: {weeks} weeks

## Starting: v{X}.0

### Status

- Version: v{X}.0
- Phase: Research

### Focus Areas

1. {area1}
2. {area2}

## Progress to v10.0

[████████████░░░░░░░░] {percent}%

Current: v{X}.0 | Target: v10.0

## Self-Upgrade Insights

### Effectiveness Score: {score}/100

### Improvements Applied

- {improvement1}
- {improvement2}

### Gaps Identified

- {gap1}: {action}
```
