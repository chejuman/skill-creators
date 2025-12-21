---
name: {{SKILL_NAME}}
description: {{DESCRIPTION}}
---

# {{SKILL_TITLE}}

{{DOMAIN}} system with parallel agent execution.

## Architecture

```
Orchestrator
    ├─► Planning Agent ──► Scope analysis
    ├─► Worker Agents (PARALLEL)
{{WORKER_ARCHITECTURE}}
    ├─► Analysis Agent ──► Result synthesis
    ├─► Synthesis Agent ──► Report generation
    └─► Visualization Agent ──► HTML output
```

## Depth Levels

| Level | Workers | Analysis | Report | Use Case |
|-------|---------|----------|--------|----------|
| 1 | 1 | Inline | Basic | Quick check |
| 2 | 2 | 1 agent | Standard | General |
| 3 | 3 | 1 agent | Detailed | Production |
| 4 | 4 | 1 agent | Expert | Deep |
| 5 | 5+ | 1 agent | Full | Audit |

## Execution Workflow

### Phase 1: Planning

```
Task(
  subagent_type='Plan',
  prompt='Analyze {{DOMAIN}} scope and decompose into parallel tasks...',
  description='Plan {{DOMAIN}}'
)
```

### Phase 2: Worker Execution (PARALLEL)

Spawn ALL workers in ONE message:

```python
{{WORKER_TASKS}}
```

### Phase 3: Analysis

```
Task(
  subagent_type='general-purpose',
  prompt='Analyze all worker findings, score by priority...',
  description='Analyze findings'
)
```

### Phase 4: Synthesis

```
Task(
  subagent_type='general-purpose',
  prompt='Generate Level {{LEVEL}} report with executive summary...',
  description='Generate report'
)
```

### Phase 5: Visualization (Optional)

```
Task(
  subagent_type='general-purpose',
  prompt='Convert markdown to HTML using scripts/md_to_html.py...',
  description='Generate HTML',
  model='haiku'
)
```

## Orchestration Rules

1. Planning Agent runs FIRST
2. Worker Agents run in PARALLEL
3. Analysis Agent waits for ALL workers
4. Synthesis Agent runs after analysis
5. Visualization Agent runs LAST

## Resources

- [Agent Prompts](references/agent_prompts.md)
- [Report Template](assets/report_template.md)

## Trigger Phrases

- "{{TRIGGER_1}}"
- "{{TRIGGER_2}}"
- "level X {{DOMAIN}}"
