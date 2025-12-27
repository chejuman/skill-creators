---
name: resolve-debt-v4
description: Enterprise-grade multi-agent technical debt resolution with 10 parallel workers, business cost quantification ($), AI-generated code analysis, knowledge silo detection, auto-fix generation, and DevEx impact metrics. Features TDR calculation, CodeHealth scoring, trend tracking, and executive dashboard. Use for comprehensive audits, refactoring planning, or when mentions "tech debt", "resolve debt", "code audit", depth levels (1-5), "--cost", "--autofix".
---

# Resolve Debt v4 - Enterprise Technical Debt Resolution

Multi-agent orchestrated system following workflow-creator-v2 patterns.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ORCHESTRATOR                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Phase 1: Initialization ──► Parse args, create TodoWrite plan               │
│ Phase 2: Context Gathering ──► 2 parallel agents (Planning + Git History)   │
│ Phase 3: Parallel Analysis ──► 10 background workers                        │
│ Phase 4: Synthesis ──► Correlation + Business Impact agents                 │
│ Phase 5: Validation ──► Self-Critique agent (Opus)                          │
│ Phase 6: Remediation ──► Auto-Fix + PR Generator (optional)                 │
│ Phase 7: Output ──► Report generation + Installation                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Arguments

```
/resolve-debt-v4 [target] [options]
```

| Option            | Description                         | Default  |
| ----------------- | ----------------------------------- | -------- |
| `target`          | Directory, file pattern, or module  | codebase |
| `--level N`       | Analysis depth 1-5                  | 3        |
| `--format`        | `md`, `html`, `json`, `exec`, `all` | md       |
| `--focus`         | Areas: `perf,sec,arch,ai,silo`      | all      |
| `--cost`          | Enable business cost quantification | off      |
| `--autofix`       | Generate fix patches                | off      |
| `--compare FILE`  | Compare with previous report        | -        |
| `--hourly-rate N` | Developer hourly rate for $ calc    | 75       |

## Phase 1: Initialization

Parse arguments and create execution plan with TodoWrite:

```python
# Step 1.1: Parse Arguments
args = parse_arguments(user_input)
target = args.get('target', '.')
level = args.get('level', 3)
format = args.get('format', 'md')
cost_enabled = args.get('cost', False)
autofix_enabled = args.get('autofix', False)

# Step 1.2: Determine Worker Count
worker_config = {
    1: {'workers': 4, 'model': 'haiku'},
    2: {'workers': 6, 'model': 'haiku'},
    3: {'workers': 8, 'model': 'sonnet'},
    4: {'workers': 10, 'model': 'sonnet'},
    5: {'workers': 10, 'model': 'opus'}
}
config = worker_config[level]
```

```
# Step 1.3: Create TodoWrite Plan
TodoWrite(todos=[
    {content: "Phase 1: Initialize and parse arguments", status: "completed"},
    {content: "Phase 2: Gather context (Planning + Git History)", status: "in_progress"},
    {content: "Phase 3: Run parallel analysis workers", status: "pending"},
    {content: "Phase 4: Synthesize findings", status: "pending"},
    {content: "Phase 5: Validate with self-critique", status: "pending"},
    {content: "Phase 6: Generate remediation patches", status: "pending"},
    {content: "Phase 7: Generate reports and install", status: "pending"}
])
```

## Phase 2: Context Gathering

Launch 2 parallel context agents:

```
# Launch both agents in parallel (single message, multiple Task calls)
Task(
    subagent_type='Explore',
    model='sonnet',
    prompt=PLANNING_AGENT_PROMPT,  # See references/orchestrator_prompts.md
    description='Plan debt analysis scope',
    run_in_background=true
)

Task(
    subagent_type='Explore',
    model='sonnet',
    prompt=GIT_HISTORY_AGENT_PROMPT,
    description='Analyze git history',
    run_in_background=true
)
```

Wait for completion:

```
planning_result = TaskOutput(task_id=planning_task_id, block=true)
git_result = TaskOutput(task_id=git_task_id, block=true)
```

Update TodoWrite:

```
TodoWrite(todos=[
    {content: "Phase 2: Gather context", status: "completed"},
    {content: "Phase 3: Run parallel analysis workers", status: "in_progress"},
    ...
])
```

## Phase 3: Parallel Analysis Workers

Launch all workers in a single message with `run_in_background=true`:

```
# Worker 1-8: Core Analysis (from v3)
Task(subagent_type='Explore', model=config.model, prompt=CODE_QUALITY_PROMPT,
     description='Analyze code quality', run_in_background=true)
Task(subagent_type='Explore', model=config.model, prompt=DEPENDENCY_PROMPT,
     description='Analyze dependencies', run_in_background=true)
Task(subagent_type='Explore', model=config.model, prompt=ARCHITECTURE_PROMPT,
     description='Analyze architecture', run_in_background=true)
Task(subagent_type='Explore', model=config.model, prompt=TEST_COVERAGE_PROMPT,
     description='Analyze test coverage', run_in_background=true)
Task(subagent_type='Explore', model=config.model, prompt=PERFORMANCE_PROMPT,
     description='Analyze performance', run_in_background=true)
Task(subagent_type='Explore', model=config.model, prompt=SECURITY_PROMPT,
     description='Analyze security', run_in_background=true)
Task(subagent_type='Explore', model=config.model, prompt=DOCUMENTATION_PROMPT,
     description='Analyze documentation', run_in_background=true)
Task(subagent_type='Explore', model=config.model, prompt=TYPE_SAFETY_PROMPT,
     description='Analyze type safety', run_in_background=true)

# Worker 9-10: New v4 Analysis (level >= 4)
if level >= 4:
    Task(subagent_type='Explore', model=config.model, prompt=AI_CODE_PROMPT,
         description='Analyze AI-generated code', run_in_background=true)
    Task(subagent_type='Explore', model=config.model, prompt=KNOWLEDGE_SILO_PROMPT,
         description='Analyze knowledge silos', run_in_background=true)
```

Collect all results:

```
results = {}
for task_id, name in worker_tasks:
    results[name] = TaskOutput(task_id=task_id, block=true)
```

## Phase 4: Synthesis

Launch synthesis agents sequentially (dependent data):

```
# Step 4.1: Correlation Agent
Task(
    subagent_type='general-purpose',
    model='sonnet',
    prompt=f'''Correlate findings across all workers.

    Worker Results: {json.dumps(results)}

    Identify:
    1. Root causes (single issues causing multiple symptoms)
    2. Dependencies between issues (which fixes unblock others)
    3. Patterns (repeated mistakes, team knowledge gaps)
    4. Clusters (related issues for batch fixing)

    Return JSON: {{root_causes, dependencies, patterns, clusters}}''',
    description='Correlate findings'
)
correlation_result = TaskOutput(task_id=correlation_id, block=true)
```

```
# Step 4.2: Business Impact Agent (if --cost enabled)
if cost_enabled:
    Task(
        subagent_type='general-purpose',
        model='sonnet',
        prompt=f'''Calculate business impact of technical debt.

        Issues: {json.dumps(all_issues)}
        Hourly Rate: ${hourly_rate}
        Correlations: {correlation_result}

        Calculate:
        1. Per-issue cost (remediation + annual interest)
        2. TDR (Technical Debt Ratio)
        3. DevEx impact (hours lost weekly)
        4. ROI ranking for prioritization

        Return JSON: {{total_cost, tdr, devex, roi_ranking}}''',
        description='Calculate business impact'
    )
    business_result = TaskOutput(task_id=business_id, block=true)
```

## Phase 5: Validation

Self-critique with Opus (level 5 or --validate):

```
if level >= 5:
    Task(
        subagent_type='general-purpose',
        model='opus',
        prompt=f'''Critically validate analysis findings.

        Findings: {json.dumps(prioritized_items)}
        Codebase Context: {context_summary}

        For each finding:
        1. Is this a real issue or false positive?
        2. Is severity accurate?
        3. Is suggested fix appropriate?
        4. Should confidence be adjusted?

        Filter: Remove duplicates, merge related, flag uncertain.

        Return JSON: {{
            validated_items,
            removed_items,
            adjusted_items,
            review_needed
        }}''',
        description='Self-critique validation'
    )
    validated_result = TaskOutput(task_id=critique_id, block=true)
```

## Phase 6: Remediation

Auto-fix generation (if --autofix):

```
if autofix_enabled:
    # Step 6.1: Generate Patches
    Task(
        subagent_type='general-purpose',
        model='opus',
        prompt=f'''Generate fix patches for quick wins.

        Quick Wins: {json.dumps(quick_wins)}

        For each (confidence >= 0.8, effort <= 2h):
        1. Read current file
        2. Generate minimal, safe fix
        3. Output unified diff
        4. Include verification steps

        Return JSON: {{patches: [...], skipped: [...], stats: {{...}}}}''',
        description='Generate auto-fix patches'
    )
    patches_result = TaskOutput(task_id=patches_id, block=true)

    # Step 6.2: Generate PR Descriptions (optional)
    if len(patches_result.patches) > 0:
        Task(
            subagent_type='general-purpose',
            model='sonnet',
            prompt=f'''Generate PR descriptions for patches.

            Patches: {json.dumps(patches_result.patches)}

            Group by type/module, generate:
            - Title: "[type] Brief description"
            - Body: Summary, changes, impact, testing
            - Labels: tech-debt, auto-generated, etc.

            Return JSON: {{prs: [...]}}''',
            description='Generate PR descriptions'
        )
```

## Phase 7: Output Generation

Generate reports and install:

```
# Step 7.1: Generate Report
Task(
    subagent_type='general-purpose',
    model='sonnet',
    prompt=f'''Generate technical debt report.

    Data:
    - Target: {target}
    - Level: {level}
    - Issues: {validated_items or prioritized_items}
    - Correlations: {correlation_result}
    - Business Impact: {business_result if cost_enabled else None}
    - Patches: {patches_result if autofix_enabled else None}
    - Format: {format}

    Use templates from assets/report_template_{format}.md

    Generate complete report following template structure.''',
    description='Generate debt report'
)
```

```
# Step 7.2: Save Report
report_path = f'./debt-report-{timestamp}.{format}'
Write(file_path=report_path, content=report)
```

```
# Step 7.3: Update TodoWrite - Complete
TodoWrite(todos=[
    {content: "Phase 1-6", status: "completed"},
    {content: "Phase 7: Generate reports", status: "completed"}
])
```

## Worker Selection by Level

| Level | Workers Enabled          | Features      |
| :---: | :----------------------- | :------------ |
|   1   | CQ, DEP, SEC, TEST       | Quick scan    |
|   2   | + ARCH, PERF             | Standard      |
|   3   | + DOC, TYPE              | Detailed      |
|   4   | + AI, SILO, Cost         | Full analysis |
|   5   | All + Critique + AutoFix | Premium       |

## Agent Prompts

All prompts in [references/orchestrator_prompts.md](references/orchestrator_prompts.md):

- Phase 2: Planning Agent, Git History Agent
- Phase 3: 10 Analysis Worker Prompts
- Phase 4: Correlation Agent, Business Impact Agent
- Phase 5: Self-Critique Agent
- Phase 6: Auto-Fix Agent, PR Generator Agent
- Phase 7: Synthesis Agent

## Report Templates

- [assets/report_template_md.md](assets/report_template_md.md)
- [assets/report_template_exec.md](assets/report_template_exec.md)
- [assets/report_template_html.html](assets/report_template_html.html)

## Usage Examples

```bash
# Standard analysis (level 3)
/resolve-debt-v4 src/

# Quick scan
/resolve-debt-v4 --level 1

# Full enterprise audit with cost analysis
/resolve-debt-v4 --level 5 --cost --hourly-rate 100

# Security focus with auto-fix
/resolve-debt-v4 --focus sec --autofix

# Executive summary
/resolve-debt-v4 --format exec --cost

# Trend comparison
/resolve-debt-v4 --compare ./reports/previous.json
```

## Composite Workflow Structure

```
resolve-debt-v4/
├── SKILL.md                    # Main orchestrator
├── references/
│   └── orchestrator_prompts.md # All agent prompts
├── assets/
│   ├── report_template_md.md   # Markdown template
│   ├── report_template_exec.md # Executive template
│   └── report_template_html.html
├── scripts/
│   ├── parse_args.py           # Argument parser
│   ├── collect_results.py      # Result aggregator
│   └── validate_report.py      # Report validator
└── commands/
    └── quick-debt.md           # Quick trigger command
```

## Principles

1. **Phase-Based Orchestration**: Clear 7-phase execution
2. **Parallel Execution**: Workers run concurrently via background tasks
3. **Progressive Loading**: Workers enabled by level
4. **TodoWrite Integration**: Real-time progress tracking
5. **Structured Output**: JSON-based inter-agent communication
6. **Self-Critique**: Opus validation at level 5
7. **Composite Ready**: Skill + Command + Hook compatible
