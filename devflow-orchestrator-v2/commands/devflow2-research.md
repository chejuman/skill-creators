# /devflow2-research

Run hierarchical multi-agent research with source credibility scoring.

## Usage

```
/devflow2-research [--depth <level>] [--focus <area>]
```

## Options

- `--depth`: Research depth (1=quick, 2=standard, 3=comprehensive)
- `--focus`: Focus area (tech, market, security, competitors, opensource)

## What This Does

### Step 1: Generate Research Agents

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/research_coordinator.py generate
```

### Step 2: Launch Research Coordinator

The Research Coordinator spawns 5 specialized sub-agents in parallel:

```
# Launch all 5 agents simultaneously
Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Tech stack research',
     prompt='...')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Market trends research',
     prompt='...')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Open source research',
     prompt='Use GitMVP MCP tools to find repositories...')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Security research',
     prompt='...')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Competitor analysis',
     prompt='...')
```

### Step 3: Collect Results

```
TaskOutput(task_id='tech_agent_id', block=true)
TaskOutput(task_id='market_agent_id', block=true)
...
```

### Step 4: Synthesize with Credibility Scoring

Research Coordinator synthesizes all findings:

- Tier 1 sources (official docs): 100% weight
- Tier 2 sources (tech publications): 80% weight
- Tier 3 sources (community): 60% weight

### Step 5: Save Research

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/research_coordinator.py save "tech_stack" "<content>"
```

### Step 6: Quality Gate Check

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/quality_gate.py run research_complete
```

### Output

```markdown
## Research Complete

### Summary

- Tech Stack: {summary}
- Market Trends: {summary}
- Open Source: {top_repos}
- Security: {key_concerns}
- Competitors: {landscape}

### Source Credibility

| Category | Tier 1 | Tier 2 | Tier 3 | Confidence |
| -------- | ------ | ------ | ------ | ---------- |
| Tech     | 3      | 5      | 2      | 85%        |
| Market   | 2      | 4      | 3      | 72%        |

### Quality Gate: research_complete

Status: ✅ PASSED (100%)

### Next Steps

1. `/devflow2-analyze` - Multi-perspective analysis
2. `/devflow2-gate research_complete` - Verify gate
```

## Example

```
/devflow2-research

/devflow2-research --depth 3 --focus security
```
