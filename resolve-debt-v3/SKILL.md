---
name: resolve-debt-v3
description: Premium multi-agent technical debt resolution with 8 parallel analysis workers covering code quality, dependencies, architecture, tests, performance, security, documentation, and type safety. Features RICE-based prioritization, self-critique validation, and multi-format reporting (MD/HTML/JSON). Use for comprehensive debt audits, refactoring planning, or when mentions "tech debt", "resolve debt", "code audit", depth levels (1-5).
---

# Resolve Debt v3 - Premium Multi-Agent Technical Debt Resolution

Hierarchical multi-agent system with 8 specialized workers, self-critique validation, and multi-format output.

## Architecture

```
Orchestrator
    │
    ├──▶ Phase 1: Planning Agent
    │         └── Scope decomposition, context gathering
    │
    ├──▶ Phase 2: Analysis Workers (8 PARALLEL)
    │         ├── Code Quality Agent    [complexity, smells, duplication]
    │         ├── Dependency Agent      [CVE, outdated, licenses]
    │         ├── Architecture Agent    [coupling, patterns, SOLID]
    │         ├── Test Coverage Agent   [gaps, quality, flaky tests]
    │         ├── Performance Agent     [N+1, memory, async issues]
    │         ├── Security Agent        [injection, auth, secrets]
    │         ├── Documentation Agent   [JSDoc, README, changelog]
    │         └── Type Safety Agent     [any usage, inference gaps]
    │
    ├──▶ Phase 3: Correlation Agent
    │         └── Cross-reference issues, identify root causes
    │
    ├──▶ Phase 4: Impact Analysis Agent
    │         └── RICE scoring, business impact assessment
    │
    ├──▶ Phase 5: Self-Critique Agent
    │         └── Validate findings, filter false positives
    │
    └──▶ Phase 6: Synthesis Agent
              └── Multi-format report generation
```

## Execution Workflow

### Arguments

```
/resolve-debt-v3 [target] [--level N] [--format FORMAT] [--focus AREAS]
```

| Argument    | Description                           | Default         |
| ----------- | ------------------------------------- | --------------- |
| `target`    | Directory, file pattern, or module    | entire codebase |
| `--level N` | Analysis depth 1-5                    | 3               |
| `--format`  | Output: `md`, `html`, `json`, `all`   | md              |
| `--focus`   | Comma-separated: `perf,sec,arch,test` | all areas       |

**Depth Levels:**
| Level | Workers | Model | Description |
|:-----:|:-------:|:-----:|-------------|
| 1 | 2-3 | haiku | Quick scan, critical issues only |
| 2 | 4 | haiku | Standard scan with prioritization |
| 3 | 6 | sonnet | Detailed analysis (default) |
| 4 | 8 | sonnet | Deep audit with all workers |
| 5 | 8+ | opus | Comprehensive with self-critique |

### Phase 1: Planning Agent

Launch planning agent to gather project context:

```
Task(
  subagent_type='Explore', model='sonnet',
  prompt='Analyze project for comprehensive debt assessment:
    1. Identify source directories, file patterns, languages
    2. Find package manifests (package.json, requirements.txt, go.mod)
    3. Locate test directories, coverage config, CI pipelines
    4. Check linting/formatting configs (.eslintrc, tsconfig.json)
    5. Analyze git history: high-churn files, recent hotfixes
    6. Identify critical business modules (auth, payments, core)
    7. Map module dependencies and boundaries
    Return: JSON with file_patterns, deps, tests, lint, churn, critical_modules',
  description='Plan v3 debt analysis'
)
```

### Phase 2: Parallel Worker Agents

Launch all 8 workers simultaneously using a single Task block with `run_in_background=true`.

**Worker agent prompts:** See [references/agent_prompts.md](references/agent_prompts.md)

```
# Launch all workers in parallel
Task(subagent_type='Explore', prompt=CODE_QUALITY_PROMPT, run_in_background=true)
Task(subagent_type='Explore', prompt=DEPENDENCY_PROMPT, run_in_background=true)
Task(subagent_type='Explore', prompt=ARCHITECTURE_PROMPT, run_in_background=true)
Task(subagent_type='Explore', prompt=TEST_COVERAGE_PROMPT, run_in_background=true)
Task(subagent_type='Explore', prompt=PERFORMANCE_PROMPT, run_in_background=true)
Task(subagent_type='Explore', prompt=SECURITY_PROMPT, run_in_background=true)
Task(subagent_type='Explore', prompt=DOCUMENTATION_PROMPT, run_in_background=true)
Task(subagent_type='Explore', prompt=TYPE_SAFETY_PROMPT, run_in_background=true)
```

Wait for completion: `TaskOutput(task_id=..., block=true)` for each worker.

### Phase 3: Correlation Agent

Cross-reference findings to identify root causes:

```
Task(
  subagent_type='general-purpose', model='sonnet',
  prompt='Correlate findings across all workers:

    Worker Results: {all_worker_results}

    1. Identify ROOT CAUSES:
       - Single issues causing multiple symptoms
       - Architectural decisions creating debt clusters

    2. Map DEPENDENCIES between issues:
       - Which fixes enable other fixes
       - Which issues block each other

    3. Find PATTERNS:
       - Repeated mistakes across codebase
       - Team knowledge gaps indicated by issue types

    Return: {root_causes[], dependencies{}, patterns[], clusters[]}'
)
```

### Phase 4: Impact Analysis Agent

Apply RICE scoring for prioritization:

```
Task(
  subagent_type='general-purpose', model='sonnet',
  prompt='Apply RICE scoring to prioritize debt items:

    Items: {all_items}
    Correlations: {correlations}
    Critical Modules: {critical_modules}

    For each item calculate:
    - Reach: How much of codebase affected (1-10)
    - Impact: Severity if not fixed (1-10)
    - Confidence: How certain is the assessment (0.5-1.0)
    - Effort: Person-hours to fix

    RICE Score = (Reach × Impact × Confidence) / Effort

    Categorize:
    - Critical (RICE >= 50): This sprint
    - High (RICE 20-50): This quarter
    - Medium (RICE < 20): Backlog

    Identify Quick Wins: High impact, low effort (<30 min)

    Return: {prioritized_items[], quick_wins[], metrics{}}'
)
```

### Phase 5: Self-Critique Agent

Validate and filter findings (Level 5 only, or --validate flag):

```
Task(
  subagent_type='general-purpose', model='opus',
  prompt='Critically evaluate the analysis findings:

    Findings: {prioritized_items}

    For each finding:
    1. Is this a real issue or false positive?
    2. Is severity assessment accurate?
    3. Is the suggested fix appropriate?
    4. Are there edge cases not considered?

    Filter criteria:
    - Remove duplicates and overlaps
    - Merge related issues into single actionable items
    - Adjust severity based on actual codebase context
    - Flag uncertain items for human review

    Return: {validated_items[], removed_items[], adjusted_items[], review_needed[]}'
)
```

### Phase 6: Synthesis Agent

Generate final report in requested format(s):

```
Task(
  subagent_type='general-purpose', model='sonnet',
  prompt='Generate technical debt report.

    Input:
    - Target: {target}, Level: {level}
    - Validated Items: {validated_items}
    - Quick Wins: {quick_wins}
    - Correlations: {correlations}
    - Metrics: {metrics}
    - Format: {format}

    Use templates from assets/report_template_{format}.md

    Include:
    - Executive summary with RICE-based priorities
    - Issue breakdown by category (8 types)
    - Dependency-aware implementation roadmap
    - Before/after metrics projections'
)
```

## New Analysis Dimensions (v3)

### Performance Agent

- N+1 query patterns in DB access
- Memory leaks and inefficient allocations
- Blocking I/O in async contexts
- Missing caching opportunities
- Bundle size issues (JS/TS)
- Lazy loading opportunities

### Security Agent

- SQL/NoSQL injection risks
- XSS and CSRF vulnerabilities
- Hardcoded secrets and credentials
- Missing input validation
- Authentication/authorization gaps
- Dependency CVEs (cross-referenced with Dependency Agent)

### Documentation Agent

- Missing JSDoc/docstrings on public APIs
- Outdated README content
- Missing CHANGELOG entries
- Undocumented environment variables
- Missing API documentation
- Stale inline comments

### Type Safety Agent (TS/Python)

- Explicit `any` usage
- Missing return type annotations
- Implicit `any` from inference failures
- Type assertion overuse (`as`)
- Missing generic constraints
- Inconsistent null handling

## Output Formats

| Format | Use Case                                   |
| ------ | ------------------------------------------ |
| `md`   | Standard markdown report (default)         |
| `html` | Interactive HTML with collapsible sections |
| `json` | Machine-readable for integration           |
| `all`  | Generate all formats                       |

## Usage Examples

**Standard analysis:**

```
/resolve-debt-v3 src/
```

**Quick security-focused scan:**

```
/resolve-debt-v3 --level 2 --focus sec,dep
```

**Comprehensive audit with HTML report:**

```
/resolve-debt-v3 --level 5 --format html
```

**Performance and architecture focus:**

```
/resolve-debt-v3 src/api --focus perf,arch --level 4
```

## Principles

1. **Parallel Execution**: 8 workers run concurrently for speed
2. **Root Cause Focus**: Address causes, not symptoms
3. **RICE Prioritization**: Data-driven priority scoring
4. **Self-Critique**: Validate findings, reduce noise
5. **Multi-Dimensional**: 8 analysis perspectives
6. **Actionable Output**: Dependency-aware roadmaps
7. **Format Flexibility**: MD/HTML/JSON output options
