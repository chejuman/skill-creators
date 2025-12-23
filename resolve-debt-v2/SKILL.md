---
name: resolve-debt-v2
description: Multi-agent technical debt resolution system with parallel workers for code smells, dependencies, architecture violations, and test coverage gaps. Use when analyzing technical debt, planning refactoring, auditing code quality, or when user mentions "tech debt", "resolve debt", "code quality audit", depth levels (1-5), or refactoring analysis.
---

# Resolve Debt v2 - Multi-Agent Technical Debt Resolution

Hierarchical multi-agent system for comprehensive technical debt analysis with parallel worker execution.

## Architecture

```
Orchestrator
    |
    +---> Planning Agent ---> Scope decomposition & context gathering
    |
    +---> Worker Agents (PARALLEL)
    |         |-- Code Smell Agent: complexity, duplication, long methods
    |         |-- Dependency Agent: vulnerabilities, outdated packages
    |         |-- Architecture Agent: coupling, pattern violations
    |         +-- Test Coverage Agent: untested paths, coverage gaps
    |
    +---> Analysis Agent ---> Prioritization matrix synthesis
    |
    +---> Synthesis Agent ---> Report generation
```

## Execution Workflow

### Step 1: Parse Arguments & Set Depth

**Arguments format:** `[target] [--level N]`
- `target`: Directory, file pattern, or module name (default: entire codebase)
- `--level N`: Analysis depth 1-5 (default: 3)

**Depth levels:**
| Level | Workers | Description |
|-------|---------|-------------|
| 1 | 1-2 | Quick scan, critical issues only |
| 2 | 2 | Standard scan with prioritization |
| 3 | 3-4 | Detailed analysis with all workers (default) |
| 4 | 4 | Deep audit with cross-references |
| 5 | 4+ | Comprehensive with historical analysis |

### Step 2: Launch Planning Agent

```
Task(
  subagent_type='Explore',
  model='haiku',
  prompt='Analyze project structure for tech debt assessment:
    1. Identify main source directories and file patterns
    2. Find package.json/requirements.txt for dependency info
    3. Locate test directories and coverage config
    4. Check for linting config (.eslintrc, .prettierrc)
    5. Analyze git history for high-churn files (last 3 months)
    Return: file_patterns, dep_file, test_patterns, lint_config, churn_files',
  description='Plan debt analysis scope'
)
```

### Step 3: Launch Parallel Worker Agents

Execute all 4 workers in parallel using single Task block:

```
# Code Smell Agent
Task(
  subagent_type='Explore',
  model='haiku',
  prompt=CODE_SMELL_PROMPT,  # See references/agent_prompts.md
  description='Analyze code smells',
  run_in_background=true
)

# Dependency Agent
Task(
  subagent_type='Explore',
  model='haiku',
  prompt=DEPENDENCY_PROMPT,
  description='Analyze dependencies',
  run_in_background=true
)

# Architecture Agent
Task(
  subagent_type='Explore',
  model='haiku',
  prompt=ARCHITECTURE_PROMPT,
  description='Analyze architecture',
  run_in_background=true
)

# Test Coverage Agent
Task(
  subagent_type='Explore',
  model='haiku',
  prompt=TEST_COVERAGE_PROMPT,
  description='Analyze test coverage',
  run_in_background=true
)
```

Wait for all workers: `TaskOutput(task_id=..., block=true)`

### Step 4: Launch Analysis Agent

```
Task(
  subagent_type='general-purpose',
  model='sonnet',
  prompt='Given worker results, create prioritization matrix:

    Worker Results:
    - Code Smells: {code_smell_results}
    - Dependencies: {dependency_results}
    - Architecture: {architecture_results}
    - Test Coverage: {test_coverage_results}

    Score each item (1-5):
    | Item | Severity | Change Freq | Fix Effort | Priority |
    Priority = (Severity x Change Freq) / Fix Effort

    Categorize:
    - Critical (Priority >= 4): Address this sprint
    - High (Priority 2-4): Address this quarter
    - Medium (Priority < 2): Backlog

    Return: prioritized_items, quick_wins, metrics',
  description='Prioritize debt items'
)
```

### Step 5: Launch Synthesis Agent

```
Task(
  subagent_type='general-purpose',
  model='sonnet',
  prompt='Generate technical debt report using template.

    Input:
    - Project: {target}
    - Analysis Level: {level}
    - Prioritized Items: {prioritized_items}
    - Quick Wins: {quick_wins}
    - Metrics: {metrics}

    Use template from assets/report_template.md
    Follow output format exactly.',
  description='Generate debt report'
)
```

## Agent Prompts Reference

Detailed agent prompts: [references/agent_prompts.md](references/agent_prompts.md)

## Report Template

Output template: [assets/report_template.md](assets/report_template.md)

## Usage Examples

**Basic usage (level 3):**
```
/resolve-debt-v2 src/
```

**Quick scan (level 1):**
```
/resolve-debt-v2 --level 1
```

**Deep audit (level 5):**
```
/resolve-debt-v2 src/api --level 5
```

**Full codebase:**
```
/resolve-debt-v2
```

## Principles

1. **Parallel Execution**: Workers run concurrently for speed
2. **Impact-First**: Prioritize by business impact x change frequency / effort
3. **Incremental Resolution**: Atomic, reviewable changes
4. **Preserve Behavior**: No changes without test coverage
5. **Root Cause Focus**: Address patterns, not symptoms
6. **Measurable Outcomes**: Concrete metrics for improvement

## Output

Report includes:
- Executive summary with total items and effort estimate
- Debt inventory table with type, location, severity
- Prioritized resolution plan (Critical/High/Medium)
- Quick wins list (< 30 min each)
- Implementation order with dependencies
- Metrics to track (before/target/measurement)
