---
name: devflow-orchestrator-v2
description: Premium AI-powered iterative development orchestrator from MVP to v10.0+ maturity. Features hierarchical multi-agent architecture with coordinator-subagent pattern, predictive analytics, quality gates, knowledge accumulation, and adaptive workflows. Triggers on "devflow", "project planning", "MVP roadmap", "feature prioritization", "development orchestration", "premium planning".
---

# DevFlow Orchestrator V2 - Premium Edition

Enterprise-grade iterative development planning with hierarchical multi-agent orchestration.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MASTER ORCHESTRATOR                              │
│            (Coordinates all phases, maintains global context)            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │   RESEARCH      │  │   ANALYSIS      │  │   PLANNING      │          │
│  │   COORDINATOR   │  │   COORDINATOR   │  │   COORDINATOR   │          │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤          │
│  │ ┌───┐ ┌───┐     │  │ ┌───┐ ┌───┐     │  │ ┌───┐ ┌───┐     │          │
│  │ │T1 │ │T2 │     │  │ │U1 │ │T1 │     │  │ │F1 │ │T1 │     │          │
│  │ └───┘ └───┘     │  │ └───┘ └───┘     │  │ └───┘ └───┘     │          │
│  │ ┌───┐ ┌───┐     │  │ ┌───┐ ┌───┐     │  │ ┌───┐ ┌───┐     │          │
│  │ │M1 │ │S1 │     │  │ │B1 │ │R1 │     │  │ │D1 │ │R1 │     │          │
│  │ └───┘ └───┘     │  │ └───┘ └───┘     │  │ └───┘ └───┘     │          │
│  │      ┌───┐      │  │                 │  │                 │          │
│  │      │C1 │      │  │                 │  │                 │          │
│  │      └───┘      │  │                 │  │                 │          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘          │
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │   QUALITY       │  │   KNOWLEDGE     │  │   SELF-UPGRADE  │          │
│  │   GATE          │  │   ACCUMULATOR   │  │   ENGINE        │          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘

Legend: T=Tech, M=Market, S=Security, C=Competitor, O=OpenSource
        U=User, B=Business, R=Risk, F=Feature, D=Dependency
```

## Premium Features

| Feature                | Description                               |
| ---------------------- | ----------------------------------------- |
| Hierarchical Agents    | Coordinators spawn specialized sub-agents |
| Quality Gates          | Automated validation at each phase        |
| Predictive Analytics   | Risk scoring, velocity tracking, burndown |
| Knowledge Base         | Accumulates insights across projects      |
| Adaptive Workflow      | Adjusts based on domain and complexity    |
| Source Credibility     | Tiered research source ranking            |
| Interactive Refinement | Multi-turn user guidance                  |

## State Persistence

```
.devflow/
├── project.json              # Master state
├── versions/                 # Version history
├── research/
│   ├── synthesis.md         # AI-synthesized insights
│   ├── sources.json         # Source credibility scores
│   └── {domain}/            # Domain-specific research
├── analysis/
│   ├── perspectives.md      # Multi-perspective analysis
│   ├── risk_matrix.json     # Risk heatmap data
│   └── feasibility.json     # Feasibility scores
├── features/
│   ├── backlog.json         # RICE++ scored features
│   ├── roadmap.md           # Visual roadmap
│   └── decisions.md         # Decision audit trail
├── plans/
│   ├── current/             # Active version plans
│   └── archive/             # Historical plans
├── analytics/
│   ├── velocity.json        # Velocity tracking
│   ├── predictions.json     # AI predictions
│   └── burndown.json        # Burndown data
├── knowledge/
│   ├── patterns.json        # Learned patterns
│   ├── insights.md          # Accumulated insights
│   └── retrospectives/      # Past learnings
└── meta/
    ├── quality_gates.json   # Gate results
    ├── workflow_metrics.json
    └── upgrade_log.md
```

## Commands

| Command              | Purpose                                 |
| -------------------- | --------------------------------------- |
| `/devflow2-init`     | Initialize with domain detection        |
| `/devflow2-research` | Hierarchical multi-agent research       |
| `/devflow2-analyze`  | Multi-perspective analysis              |
| `/devflow2-suggest`  | AI-powered feature suggestions          |
| `/devflow2-plan`     | Generate detailed plan with predictions |
| `/devflow2-gate`     | Run quality gate validation             |
| `/devflow2-next`     | Advance version with retrospective      |
| `/devflow2-status`   | Dashboard with analytics                |
| `/devflow2-roadmap`  | Visual roadmap to v10.0                 |
| `/devflow2-insights` | Query knowledge base                    |

## Workflow Phases

### Phase 1: Initialization & Domain Detection

Analyze idea, detect domain, set complexity level, initialize state.

### Phase 2: Hierarchical Research

Research Coordinator spawns 5 specialized agents:

- Tech Agent → WebSearch tech stack 2025
- Market Agent → WebSearch trends, growth
- OpenSource Agent → GitMVP repository analysis
- Security Agent → WebSearch compliance, OWASP
- Competitor Agent → WebSearch market leaders

AI synthesizes findings with source credibility scoring.

### Phase 3: Multi-Perspective Analysis

Analysis Coordinator evaluates from 4 perspectives:

- User Perspective: UX, accessibility, needs
- Technical Perspective: Scalability, maintainability
- Business Perspective: Market fit, ROI, growth
- Risk Perspective: Security, compliance, debt

Generates risk matrix and feasibility scores.

### Phase 4: Quality Gate #1

Validates research and analysis completeness before planning.

### Phase 5: Feature Suggestion with RICE++

Enhanced scoring with confidence intervals:

```
RICE++ = (Reach × Impact × Confidence × Urgency) / (Effort × Risk)
```

Interactive refinement with user preferences.

### Phase 6: Development Planning

Planning Coordinator generates:

- Task decomposition (5-10 per feature)
- Dependency graph with critical path
- Risk mitigation strategies
- Effort predictions with confidence intervals

### Phase 7: Quality Gate #2

Validates plan completeness and feasibility.

### Phase 8: Self-Upgrade & Knowledge Accumulation

- Analyze workflow effectiveness
- Extract reusable patterns
- Update knowledge base
- Generate improvement suggestions

### Phase 9: Version Advancement

- Retrospective analysis
- Velocity update
- Burndown projection
- Progress to v10.0

## Resources

- `scripts/orchestrators/master.py` - Master orchestrator
- `scripts/orchestrators/research_coordinator.py` - Research coordination
- `scripts/orchestrators/analysis_coordinator.py` - Analysis coordination
- `scripts/analyzers/quality_gate.py` - Quality validation
- `scripts/analyzers/predictive_analytics.py` - Predictions
- `scripts/generators/knowledge_base.py` - Knowledge accumulation
- `references/premium_scoring.md` - RICE++ methodology
- `references/quality_gates.md` - Gate criteria
