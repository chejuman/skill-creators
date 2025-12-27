---
name: retrospective-v2
description: Hierarchical multi-agent retrospective system with phase-isolated architecture. Spawns 4-10 parallel workers by depth level, uses JSON-based inter-agent communication, and generates actionable retrospective reports. Use when conducting sprint retrospectives, post-mortems, lessons learned sessions, or project reviews. Triggers on "retrospective", "retro", "lessons learned", "post-mortem", "sprint review", "what went well".
---

# Retrospective V2

Phase-isolated multi-agent retrospective system with progressive disclosure.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RETROSPECTIVE ORCHESTRATOR                        │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 1: COLLECT ──► Gather data from multiple sources              │
│   └── GitAnalyzer Agent (background)                                │
│   └── CodeAnalyzer Agent (background)                               │
│   └── MetricsCollector Agent (background)                           │
│   └── PatternDetector Agent (background) [level >= 3]               │
│ Phase 2: ANALYZE ──► Apply retrospective framework                  │
│   └── FrameworkApplicator Agent (background)                        │
│   └── GapAnalyzer Agent (background)                                │
│   └── RootCauseAnalyzer Agent (background) [level >= 4]             │
│ Phase 3: SYNTHESIZE ──► Generate insights and actions               │
│   └── InsightSynthesizer Agent (background)                         │
│   └── ActionGenerator Agent (background)                            │
│   └── PriorityScorer Agent (background) [level >= 4]                │
│ Phase 4: DELIVER ──► Format and present results                     │
│   └── ReportGenerator Agent                                         │
│   └── MetricsDashboard Agent [level >= 3]                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Default retrospective (level 3)
/retro

# Quick retrospective (level 1-2)
/retro --quick

# Deep analysis (level 4-5)
/retro --depth 5

# Specific framework
/retro --framework "Start-Stop-Continue"

# Analyze specific branch/commits
/retro feature/auth-system
```

## Depth Levels (Progressive Disclosure)

| Level | Workers | Phases                  | Use Case               |
| ----- | ------- | ----------------------- | ---------------------- |
| 1     | 4       | COLLECT-DELIVER         | Quick reflection       |
| 2     | 5       | COLLECT-ANALYZE-DELIVER | Basic analysis         |
| 3     | 7       | All phases              | Standard retrospective |
| 4     | 9       | All + deep              | Comprehensive review   |
| 5     | 10+     | All + iter              | Full post-mortem       |

## Retrospective Frameworks

| Framework                          | ID        | Best For             | Focus           |
| ---------------------------------- | --------- | -------------------- | --------------- |
| Start-Stop-Continue                | `ssc`     | Quick sprints        | Action-oriented |
| 4 Ls (Liked-Learned-Lacked-Longed) | `4ls`     | Learning focus       | Capability gaps |
| DAKI (Drop-Add-Keep-Improve)       | `daki`    | Process optimization | Workflow        |
| 5 Whys (Root Cause)                | `5whys`   | Incident post-mortem | Deep analysis   |
| Code Quality Focus                 | `quality` | Technical debt       | Architecture    |

## Phase 1: COLLECT (Data Gathering)

### Background Workers (Parallel)

Launch workers with `run_in_background=true`:

```
# Worker 1: Git History Analysis
Task(
  subagent_type='Explore',
  description='Analyze git history',
  prompt='''Analyze git repository for retrospective data:

  Branch/Scope: "{scope}"

  Collect:
  1. Commit frequency and patterns (by day/author)
  2. File hotspots (most frequently changed)
  3. Commit message quality and patterns
  4. Merge/revert frequency
  5. Author contribution distribution

  Return JSON format:
  {
    "phase": "COLLECT",
    "agent_id": "git-analyzer",
    "data": {
      "commit_count": N,
      "date_range": {"start": "...", "end": "..."},
      "hotspots": [{"file": "...", "changes": N, "authors": [...]}],
      "commit_patterns": {"by_day": {...}, "by_hour": {...}},
      "author_stats": [{"name": "...", "commits": N, "additions": N, "deletions": N}],
      "merge_count": N,
      "revert_count": N
    },
    "insights": ["..."],
    "confidence": 0.0-1.0
  }

  IMPORTANT: Return ONLY valid JSON, no markdown.
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 2: Code Analysis
Task(
  subagent_type='Explore',
  description='Analyze code changes',
  prompt='''Analyze code changes for retrospective:

  Changed files: {changed_files}

  Analyze:
  1. File types and distribution
  2. Code complexity indicators
  3. Test coverage ratio (test files vs source files)
  4. Documentation coverage
  5. Dependency changes

  Return JSON format:
  {
    "phase": "COLLECT",
    "agent_id": "code-analyzer",
    "data": {
      "files_changed": N,
      "file_types": {"ts": N, "tsx": N, ...},
      "test_ratio": 0.0-1.0,
      "doc_files": N,
      "new_dependencies": [...],
      "complexity_indicators": [...]
    },
    "insights": ["..."],
    "confidence": 0.0-1.0
  }
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 3: Metrics Collection
Task(
  subagent_type='Explore',
  description='Collect project metrics',
  prompt='''Collect project metrics for retrospective:

  Project path: "{project_path}"

  Collect:
  1. Total lines of code (approximate)
  2. Test file count vs source count
  3. Config file presence (CI, linting, etc.)
  4. Package dependencies count
  5. Build/deploy indicators

  Return JSON format:
  {
    "phase": "COLLECT",
    "agent_id": "metrics-collector",
    "data": {
      "loc_estimate": N,
      "test_files": N,
      "source_files": N,
      "config_files": [...],
      "dependencies": N,
      "has_ci": true/false,
      "has_tests": true/false
    },
    "insights": ["..."],
    "confidence": 0.0-1.0
  }
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 4: Pattern Detection (level >= 3)
Task(
  subagent_type='Explore',
  description='Detect development patterns',
  prompt='''Detect development patterns and anti-patterns:

  Code samples: {code_samples}

  Detect:
  1. Design patterns used (singleton, factory, etc.)
  2. Anti-patterns present
  3. Code duplication indicators
  4. Naming conventions
  5. Error handling patterns

  Return JSON format:
  {
    "phase": "COLLECT",
    "agent_id": "pattern-detector",
    "data": {
      "patterns_found": [...],
      "anti_patterns": [...],
      "duplication_indicators": [...],
      "naming_consistency": 0.0-1.0,
      "error_handling_score": 0.0-1.0
    },
    "insights": ["..."],
    "confidence": 0.0-1.0
  }
  ''',
  model='haiku',
  run_in_background=true
)
```

### Synchronization Point

```
# Collect all Phase 1 results
git_result = TaskOutput(task_id=git_agent_id, block=true)
code_result = TaskOutput(task_id=code_agent_id, block=true)
metrics_result = TaskOutput(task_id=metrics_agent_id, block=true)
pattern_result = TaskOutput(task_id=pattern_agent_id, block=true) if level >= 3

# Merge into phase output
phase1_output = {
  "phase": "COLLECT",
  "timestamp": now(),
  "agents_completed": 3 or 4,
  "git_data": git_result.data,
  "code_data": code_result.data,
  "metrics_data": metrics_result.data,
  "pattern_data": pattern_result.data if level >= 3 else null
}
```

## Phase 2: ANALYZE (Framework Application)

### Ask Framework Preference

```
AskUserQuestion(questions=[{
  "question": "Which retrospective framework should we use?",
  "header": "Framework",
  "options": [
    {"label": "Start-Stop-Continue (Recommended)", "description": "Quick, action-oriented analysis"},
    {"label": "4 Ls", "description": "Liked-Learned-Lacked-Longed for learning focus"},
    {"label": "DAKI", "description": "Drop-Add-Keep-Improve for process optimization"},
    {"label": "5 Whys", "description": "Root cause analysis for incidents"},
    {"label": "Code Quality", "description": "Technical debt and architecture focus"}
  ],
  "multiSelect": false
}])
```

### Background Workers (Parallel)

```
# Worker 1: Framework Application
Task(
  subagent_type='general-purpose',
  description='Apply retrospective framework',
  prompt='''Apply {framework} framework to collected data:

  Collected Data: {phase1_output}
  Framework: {selected_framework}

  For Start-Stop-Continue:
  - START: New practices to adopt (from patterns/metrics)
  - STOP: Practices causing issues (from anti-patterns)
  - CONTINUE: Working practices (from positive patterns)

  For 4 Ls:
  - LIKED: Positive aspects with evidence
  - LEARNED: New insights gained
  - LACKED: Missing elements
  - LONGED: Desired improvements

  Return JSON format:
  {
    "phase": "ANALYZE",
    "agent_id": "framework-applicator",
    "framework": "{framework}",
    "data": {
      "category_1": [{"item": "...", "evidence": "...", "impact": "high/medium/low"}],
      "category_2": [...],
      "category_3": [...],
      "category_4": [...] // if applicable
    },
    "summary": "...",
    "confidence": 0.0-1.0
  }
  ''',
  model='sonnet',
  run_in_background=true
)

# Worker 2: Gap Analysis
Task(
  subagent_type='general-purpose',
  description='Analyze gaps and improvements',
  prompt='''Identify gaps and improvement opportunities:

  Collected Data: {phase1_output}

  Analyze:
  1. Test coverage gaps
  2. Documentation gaps
  3. Process inefficiencies
  4. Technical debt indicators
  5. Skill/knowledge gaps

  Return JSON format:
  {
    "phase": "ANALYZE",
    "agent_id": "gap-analyzer",
    "data": {
      "test_gaps": [{"area": "...", "severity": "...", "suggestion": "..."}],
      "doc_gaps": [...],
      "process_gaps": [...],
      "tech_debt": [...],
      "skill_gaps": [...]
    },
    "priority_order": [...],
    "confidence": 0.0-1.0
  }
  ''',
  model='sonnet',
  run_in_background=true
)

# Worker 3: Root Cause Analysis (level >= 4)
Task(
  subagent_type='general-purpose',
  description='Root cause analysis',
  prompt='''Perform root cause analysis (5 Whys):

  Issues identified: {issues_from_phase1}

  For each major issue:
  1. Why did this happen? (Level 1)
  2. Why? (Level 2)
  3. Why? (Level 3)
  4. Why? (Level 4)
  5. Why? (Root cause)

  Return JSON format:
  {
    "phase": "ANALYZE",
    "agent_id": "root-cause-analyzer",
    "data": {
      "issues": [
        {
          "issue": "...",
          "why_chain": ["...", "...", "...", "...", "..."],
          "root_cause": "...",
          "preventive_action": "..."
        }
      ]
    },
    "systemic_patterns": [...],
    "confidence": 0.0-1.0
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Phase 3: SYNTHESIZE (Insight Generation)

### Background Workers (Parallel)

```
# Worker 1: Insight Synthesis
Task(
  subagent_type='general-purpose',
  description='Synthesize insights',
  prompt='''Synthesize insights from analysis:

  Phase 1 (COLLECT): {phase1_output}
  Phase 2 (ANALYZE): {phase2_output}

  Generate:
  1. Key takeaways (3-5 bullets)
  2. Patterns and anti-patterns summary
  3. Team performance insights
  4. Process efficiency insights
  5. Technical health summary

  Return JSON format:
  {
    "phase": "SYNTHESIZE",
    "agent_id": "insight-synthesizer",
    "data": {
      "key_takeaways": ["..."],
      "patterns_summary": "...",
      "team_insights": "...",
      "process_insights": "...",
      "technical_health": {"score": 0-100, "summary": "..."}
    },
    "executive_summary": "...",
    "confidence": 0.0-1.0
  }
  ''',
  model='sonnet',
  run_in_background=true
)

# Worker 2: Action Generation
Task(
  subagent_type='general-purpose',
  description='Generate action items',
  prompt='''Generate prioritized action items:

  Analysis: {phase2_output}
  Framework: {selected_framework}

  Generate actions for:
  1. Immediate (this week) - Critical issues
  2. Short-term (this sprint) - Important improvements
  3. Backlog - Nice-to-have enhancements

  Each action must have:
  - Clear description
  - Owner suggestion (role, not person)
  - Effort estimate (S/M/L)
  - Expected impact (High/Medium/Low)
  - Category (Process/Technical/Team)

  Return JSON format:
  {
    "phase": "SYNTHESIZE",
    "agent_id": "action-generator",
    "data": {
      "immediate": [{"action": "...", "owner": "...", "effort": "...", "impact": "...", "category": "..."}],
      "short_term": [...],
      "backlog": [...]
    },
    "total_actions": N,
    "confidence": 0.0-1.0
  }
  ''',
  model='sonnet',
  run_in_background=true
)

# Worker 3: Priority Scoring (level >= 4)
Task(
  subagent_type='general-purpose',
  description='Score and prioritize actions',
  prompt='''Score and prioritize all actions using ICE framework:

  Actions: {actions_from_synthesis}

  For each action calculate:
  - Impact (1-10): How much will this improve things?
  - Confidence (1-10): How sure are we this will work?
  - Ease (1-10): How easy is this to implement?
  - ICE Score = (Impact + Confidence + Ease) / 3

  Return JSON format:
  {
    "phase": "SYNTHESIZE",
    "agent_id": "priority-scorer",
    "data": {
      "scored_actions": [
        {"action": "...", "impact": N, "confidence": N, "ease": N, "ice_score": N}
      ],
      "top_3_recommendations": [...],
      "quick_wins": [...] // High ease, reasonable impact
    },
    "confidence": 0.0-1.0
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Phase 4: DELIVER (Report Generation)

### Report Generator

```
Task(
  subagent_type='general-purpose',
  description='Generate final report',
  prompt='''Generate comprehensive retrospective report:

  COLLECT: {phase1_output}
  ANALYZE: {phase2_output}
  SYNTHESIZE: {phase3_output}
  Framework: {selected_framework}

  Generate markdown report with:
  1. Executive summary (2-3 sentences)
  2. Framework-specific sections
  3. Metrics dashboard (table)
  4. Action items (prioritized checklist)
  5. Lessons learned
  6. Next retro notes

  Follow the output template exactly.
  ''',
  model='sonnet'
)
```

### Output Template

```markdown
# Retrospective: [Scope/Feature Name]

**Date:** [YYYY-MM-DD] | **Framework:** [Selected] | **Level:** [1-5] | **Scope:** [Branch/Commits]

## Executive Summary

[2-3 sentence summary of key findings and recommendations]

## Metrics Dashboard

| Metric        | Value   | Trend | Insight           |
| ------------- | ------- | ----- | ----------------- |
| Commits       | N       | ↑/↓/→ | [Brief insight]   |
| Files Changed | N       | ↑/↓/→ | [Hotspots]        |
| Test Ratio    | N%      | ↑/↓/→ | [Coverage status] |
| Authors       | N       | -     | [Collaboration]   |
| Hotspots      | N files | -     | [Focus areas]     |

## [Framework Sections]

### (Start-Stop-Continue)

#### START (New practices to adopt)

- [Practice]: [Evidence] → [Expected benefit]

#### STOP (Practices to eliminate)

- [Practice]: [Evidence of harm] → [Alternative]

#### CONTINUE (Effective practices)

- [Practice]: [Evidence of success] → [Reinforce how]

### (Or 4 Ls / DAKI / 5 Whys / Code Quality sections)

## Action Items

### Immediate (This Week)

- [ ] [Action] | Owner: [Role] | Effort: S | Impact: High

### Short-term (This Sprint)

- [ ] [Action] | Owner: [Role] | Effort: M | Impact: Medium

### Backlog

- [ ] [Action] | Category: [Process/Technical/Team]

## Lessons Learned

1. [Key lesson with context]
2. [Key lesson with context]
3. [Key lesson with context]

## Notes for Next Retrospective

- [Context to remember]
- [Metrics to track]
- [Follow-up items]

---

_Generated by retrospective-v2 | [Timestamp]_
```

## Workflow Execution

### Complete Orchestration

```python
# 1. Parse arguments
scope = args.scope or "HEAD~10"
level = args.level or 3
framework = args.framework or None

# 2. PHASE 1: COLLECT (parallel)
git_agent = Task(subagent='Explore', prompt=GIT_PROMPT, run_in_background=true)
code_agent = Task(subagent='Explore', prompt=CODE_PROMPT, run_in_background=true)
metrics_agent = Task(subagent='Explore', prompt=METRICS_PROMPT, run_in_background=true)
if level >= 3:
    pattern_agent = Task(subagent='Explore', prompt=PATTERN_PROMPT, run_in_background=true)

# Sync point
phase1 = collect_results([git_agent, code_agent, metrics_agent, pattern_agent])

# 3. Ask framework preference (if not specified)
if not framework:
    framework = AskUserQuestion(FRAMEWORK_QUESTION)

# 4. PHASE 2: ANALYZE (parallel)
framework_agent = Task(subagent='general-purpose', prompt=FRAMEWORK_PROMPT, run_in_background=true)
gap_agent = Task(subagent='general-purpose', prompt=GAP_PROMPT, run_in_background=true)
if level >= 4:
    rca_agent = Task(subagent='general-purpose', prompt=RCA_PROMPT, run_in_background=true)

# Sync point
phase2 = collect_results([framework_agent, gap_agent, rca_agent])

# 5. PHASE 3: SYNTHESIZE (parallel)
insight_agent = Task(subagent='general-purpose', prompt=INSIGHT_PROMPT, run_in_background=true)
action_agent = Task(subagent='general-purpose', prompt=ACTION_PROMPT, run_in_background=true)
if level >= 4:
    priority_agent = Task(subagent='general-purpose', prompt=PRIORITY_PROMPT, run_in_background=true)

# Sync point
phase3 = collect_results([insight_agent, action_agent, priority_agent])

# 6. PHASE 4: DELIVER
report = Task(subagent='general-purpose', prompt=REPORT_PROMPT)

# 7. Output
print(report)
```

## Scripts

### metrics_collector.py

Collects git and code metrics from repository.
Usage: `python3 scripts/metrics_collector.py [--scope HEAD~10] [--format json]`

### report_generator.py

Generates formatted retrospective report.
Usage: `python3 scripts/report_generator.py input.json [--template markdown]`

### action_tracker.py

Tracks and manages action items from retrospectives.
Usage: `python3 scripts/action_tracker.py [--add|--list|--complete]`

## Resources

- [Frameworks Reference](references/frameworks.md) - Detailed framework guides
- [JSON Schemas](references/json_schemas.md) - Agent communication formats
- [Output Templates](assets/templates/) - Report templates
- [Action Tracker](scripts/action_tracker.py) - Action item management

## Trigger Phrases

Auto-activates on:

- "retrospective", "retro", "회고"
- "lessons learned", "교훈"
- "post-mortem", "포스트모템"
- "sprint review", "스프린트 리뷰"
- "what went well", "what went wrong"
- "reflect on", "분석해줘"
