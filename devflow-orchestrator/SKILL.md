---
name: devflow-orchestrator
description: AI-powered iterative development planning workflow from MVP to v10.0+ maturity. Focuses on research, analysis, planning, and task decomposition (NO implementation). Uses multi-agent orchestration for parallel research, self-upgrade mechanisms, RICE/MoSCoW scoring, and persistent version state. Triggers on "devflow", "project planning", "MVP roadmap", "feature prioritization", "development planning".
---

# DevFlow Orchestrator

Iterative development planning system that evolves projects from idea to v10.0+ maturity through continuous research and refinement.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEVFLOW ORCHESTRATOR                              │
├─────────────────────────────────────────────────────────────────────┤
│ RESEARCH LAYER (5 Parallel Agents)                                  │
│   ├── Tech Stack Agent → Latest technologies for domain            │
│   ├── Market Trends Agent → Industry trends & patterns             │
│   ├── Open Source Agent → Best repos via GitMVP                    │
│   ├── Security Agent → Security best practices                     │
│   └── Competitor Agent → Similar products analysis                  │
├─────────────────────────────────────────────────────────────────────┤
│ ANALYSIS LAYER                                                      │
│   ├── Multi-Perspective Review (User/Tech/Business/Risk)           │
│   ├── Feasibility Scoring                                           │
│   └── Gap Analysis                                                  │
├─────────────────────────────────────────────────────────────────────┤
│ PLANNING LAYER                                                      │
│   ├── Feature Prioritization (RICE + MoSCoW)                       │
│   ├── Task Decomposition (5-10 subtasks per feature)               │
│   ├── Dependency Mapper                                             │
│   └── Roadmap Generator                                             │
├─────────────────────────────────────────────────────────────────────┤
│ SELF-UPGRADE LAYER                                                  │
│   ├── Workflow Effectiveness Analysis                               │
│   ├── Research Gap Detection                                        │
│   └── Process Improvement Engine                                    │
└─────────────────────────────────────────────────────────────────────┘
```

## State Persistence

All state persisted in `.devflow/`:

```
.devflow/
├── project.json           # Metadata, current version
├── versions/              # Version evolution history
├── research/              # Research findings
├── features/              # Feature backlog & roadmap
├── plans/                 # Current plans & tasks
└── meta/                  # Self-upgrade logs
```

## Commands

| Command                | Purpose                   |
| ---------------------- | ------------------------- |
| `/devflow-init <idea>` | Initialize new project    |
| `/devflow-research`    | Run research phase        |
| `/devflow-suggest`     | Get feature suggestions   |
| `/devflow-plan`        | Generate development plan |
| `/devflow-next`        | Advance to next version   |
| `/devflow-status`      | Show current state        |
| `/devflow-roadmap`     | Show roadmap to v10.0     |

## Workflow Phases

### Phase 0: Initialization

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py init "<idea>"
```

### Phase 1: State Review

Load and display current version, features, decisions, progress toward v10.0.

### Phase 2: Multi-Agent Research

Launch 5 parallel research agents via Task tool:

- Tech Stack: `WebSearch "{domain} tech stack 2025"`
- Market Trends: `WebSearch "{domain} trends 2025"`
- Open Source: `mcp-cli call gitmvp/search_repositories`
- Security: `WebSearch "{domain} security best practices"`
- Competitors: `WebSearch "{domain} competitors products"`

### Phase 3: Multi-Perspective Analysis

Analyze from 4 perspectives:

- **User**: UX, accessibility, user needs
- **Technical**: Scalability, maintainability
- **Business**: Market fit, growth potential
- **Risk**: Security, compliance, tech debt

### Phase 4: Feature Suggestion

Use AskUserQuestion to present 3-5 prioritized features with RICE scores.

### Phase 5: Development Planning

For selected features:

- Architecture design
- Task decomposition (5-10 subtasks)
- Dependency mapping
- Risk identification

### Phase 6: Self-Upgrade

- Evaluate workflow effectiveness
- Identify research gaps
- WebSearch for improvements
- Update self_upgrade_log.md

### Phase 7: Version Advancement

Increment version, save state, loop to Phase 1.

## Scoring Systems

### RICE Score

```
Score = (Reach × Impact × Confidence) / Effort

Reach: Users affected (1-1000)
Impact: Effect per user (0.25, 0.5, 1, 2, 3)
Confidence: Certainty (0-100%)
Effort: Person-months (1-12)
```

### MoSCoW

- **Must**: Critical for version
- **Should**: Important but not vital
- **Could**: Nice to have
- **Won't**: Out of scope

## Resources

- `scripts/state_manager.py` - State persistence
- `scripts/research_orchestrator.py` - Multi-agent research
- `scripts/feature_scorer.py` - RICE/MoSCoW scoring
- `scripts/self_upgrade.py` - Workflow improvement
- `references/scoring_guide.md` - Scoring methodology
- `references/phase_templates.md` - Output templates
