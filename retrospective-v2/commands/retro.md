---
allowed-tools:
  [Read, Bash(git:*), Grep, Glob, Task, TaskOutput, TodoWrite, AskUserQuestion]
description: Multi-agent retrospective with phase isolation, parallel workers, and JSON communication. Supports 5 frameworks and progressive depth levels (1-5).
---

## Context

- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
- Changed files: !`git diff --name-only HEAD~10 2>/dev/null | head -20`
- Commit frequency: !`git log --since="2 weeks ago" --format="%ad" --date=short | sort | uniq -c | tail -7`

## Arguments

Parse from $ARGUMENTS:

- `--depth N` or `--level N`: Set depth level 1-5 (default: 3)
- `--quick`: Shortcut for --depth 1
- `--deep`: Shortcut for --depth 5
- `--framework NAME`: Pre-select framework (ssc, 4ls, daki, 5whys, quality)
- `SCOPE`: Git scope (branch name, commit range, or "HEAD~N")

## Execution Protocol

### Step 1: Parse Arguments and Initialize

```python
# Default values
depth = 3
framework = None
scope = "HEAD~10"

# Parse arguments
if "--quick" in args: depth = 1
if "--deep" in args: depth = 5
if "--depth" in args: depth = parse_depth(args)
if "--framework" in args: framework = parse_framework(args)
scope = parse_scope(args) or scope
```

### Step 2: PHASE 1 - COLLECT (Parallel Background Workers)

Launch all collectors with `run_in_background=true`:

```
# Worker 1: Git Analysis
git_agent = Task(
  subagent_type='Explore',
  description='Analyze git history',
  prompt='Analyze git history for scope "{scope}". Return JSON with commit stats, hotspots, author distribution. Use git log, git shortlog, git diff commands.',
  model='haiku',
  run_in_background=true
)

# Worker 2: Code Analysis
code_agent = Task(
  subagent_type='Explore',
  description='Analyze code changes',
  prompt='Analyze changed files in "{scope}". Return JSON with file types, test ratio, complexity indicators.',
  model='haiku',
  run_in_background=true
)

# Worker 3: Metrics Collection
metrics_agent = Task(
  subagent_type='Explore',
  description='Collect project metrics',
  prompt='Collect project metrics. Return JSON with LOC, dependencies, CI status, test file count.',
  model='haiku',
  run_in_background=true
)

# Worker 4: Pattern Detection (depth >= 3)
if depth >= 3:
  pattern_agent = Task(
    subagent_type='Explore',
    description='Detect patterns',
    prompt='Detect design patterns and anti-patterns in changed files. Return JSON with patterns found.',
    model='haiku',
    run_in_background=true
  )
```

### Step 3: Synchronize Phase 1

```
# Wait for all workers
git_result = TaskOutput(task_id=git_agent.id, block=true)
code_result = TaskOutput(task_id=code_agent.id, block=true)
metrics_result = TaskOutput(task_id=metrics_agent.id, block=true)
pattern_result = TaskOutput(task_id=pattern_agent.id, block=true) if depth >= 3

# Aggregate
phase1_output = merge_results([git_result, code_result, metrics_result, pattern_result])
```

### Step 4: Ask Framework Preference (if not specified)

```
if not framework:
  AskUserQuestion(questions=[{
    "question": "Which retrospective framework?",
    "header": "Framework",
    "options": [
      {"label": "Start-Stop-Continue (Recommended)", "description": "Quick, action-oriented"},
      {"label": "4 Ls", "description": "Liked-Learned-Lacked-Longed"},
      {"label": "DAKI", "description": "Drop-Add-Keep-Improve"},
      {"label": "5 Whys", "description": "Root cause analysis"},
      {"label": "Code Quality", "description": "Technical focus"}
    ],
    "multiSelect": false
  }])
```

### Step 5: PHASE 2 - ANALYZE (Parallel Background Workers)

```
# Worker 1: Apply Framework
framework_agent = Task(
  subagent_type='general-purpose',
  description='Apply {framework} framework',
  prompt='Apply {framework} to: {phase1_output}. Return structured JSON.',
  model='sonnet',
  run_in_background=true
)

# Worker 2: Gap Analysis
gap_agent = Task(
  subagent_type='general-purpose',
  description='Analyze gaps',
  prompt='Identify gaps from: {phase1_output}. Return JSON with test/doc/process/tech gaps.',
  model='sonnet',
  run_in_background=true
)

# Worker 3: Root Cause (depth >= 4)
if depth >= 4:
  rca_agent = Task(
    subagent_type='general-purpose',
    description='Root cause analysis',
    prompt='Perform 5 Whys on top issues. Return JSON with why chains.',
    model='sonnet',
    run_in_background=true
  )
```

### Step 6: Synchronize Phase 2

```
framework_result = TaskOutput(task_id=framework_agent.id, block=true)
gap_result = TaskOutput(task_id=gap_agent.id, block=true)
rca_result = TaskOutput(task_id=rca_agent.id, block=true) if depth >= 4

phase2_output = merge_results([framework_result, gap_result, rca_result])
```

### Step 7: PHASE 3 - SYNTHESIZE (Parallel Background Workers)

```
# Worker 1: Synthesize Insights
insight_agent = Task(
  subagent_type='general-purpose',
  description='Synthesize insights',
  prompt='Synthesize key insights from phases 1-2. Return JSON with takeaways.',
  model='sonnet',
  run_in_background=true
)

# Worker 2: Generate Actions
action_agent = Task(
  subagent_type='general-purpose',
  description='Generate actions',
  prompt='Generate prioritized action items. Return JSON with immediate/short-term/backlog.',
  model='sonnet',
  run_in_background=true
)

# Worker 3: Priority Scoring (depth >= 4)
if depth >= 4:
  priority_agent = Task(
    subagent_type='general-purpose',
    description='Score priorities',
    prompt='Score actions using ICE framework. Return JSON with scores.',
    model='sonnet',
    run_in_background=true
  )
```

### Step 8: Synchronize Phase 3

```
insight_result = TaskOutput(task_id=insight_agent.id, block=true)
action_result = TaskOutput(task_id=action_agent.id, block=true)
priority_result = TaskOutput(task_id=priority_agent.id, block=true) if depth >= 4

phase3_output = merge_results([insight_result, action_result, priority_result])
```

### Step 9: PHASE 4 - DELIVER

Generate final report using template:

```markdown
# Retrospective: [Scope]

**Date:** [Today] | **Framework:** [Selected] | **Level:** [Depth] | **Scope:** [Scope]

## Executive Summary

[2-3 sentences from insight_agent]

## Metrics Dashboard

| Metric        | Value | Trend | Insight   |
| ------------- | ----- | ----- | --------- |
| Commits       | N     | ↑/↓/→ | [insight] |
| Files Changed | N     | ↑/↓/→ | [insight] |
| Test Ratio    | N%    | ↑/↓/→ | [insight] |
| Authors       | N     | -     | [insight] |
| Hotspots      | N     | -     | [insight] |

## [Framework Sections]

[Output from framework_agent based on selected framework]

## Action Items

### Immediate (This Week)

- [ ] [Action] | Owner: [Role] | Effort: S | Impact: High

### Short-term (This Sprint)

- [ ] [Action] | Owner: [Role] | Effort: M | Impact: Medium

### Backlog

- [ ] [Action] | Category: [Type]

## Lessons Learned

1. [Key lesson]
2. [Key lesson]
3. [Key lesson]

## Notes for Next Retro

- [Context to track]
- [Metrics to watch]

---

_Generated by retrospective-v2 | Level {depth} | {timestamp}_
```

## Depth Level Reference

| Level | Workers | Phases            | Time Est. |
| ----- | ------- | ----------------- | --------- |
| 1     | 4       | COLLECT → DELIVER | ~2 min    |
| 2     | 5       | + Basic ANALYZE   | ~3 min    |
| 3     | 7       | + Full ANALYZE    | ~5 min    |
| 4     | 9       | + SYNTHESIZE      | ~7 min    |
| 5     | 10+     | + Iteration       | ~10 min   |

## Examples

```bash
# Quick retrospective
/retro --quick

# Standard retrospective on current branch
/retro

# Deep analysis of specific branch
/retro --deep feature/auth

# Use specific framework
/retro --framework ssc

# Analyze last 20 commits
/retro HEAD~20

# Full post-mortem
/retro --depth 5 --framework 5whys
```
