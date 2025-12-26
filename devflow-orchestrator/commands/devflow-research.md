# /devflow-research

Run multi-agent research phase for current project.

## Usage

```
/devflow-research [--focus <area>]
```

## Options

- `--focus <area>`: Focus on specific area (tech, market, security, competitors, opensource)

## What This Does

### Step 1: Load Project Context

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py status
```

### Step 2: Generate Research Prompts

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/research_orchestrator.py generate
```

### Step 3: Launch 5 Parallel Research Agents

```
# Agent 1: Tech Stack
Task(
  subagent_type='Explore',
  model='haiku',
  run_in_background=true,
  description='Tech stack research',
  prompt='Research latest {domain} tech stack 2025...'
)

# Agent 2: Market Trends
Task(
  subagent_type='general-purpose',
  model='haiku',
  run_in_background=true,
  description='Market trends research',
  prompt='WebSearch for {domain} market trends 2025...'
)

# Agent 3: Open Source
Task(
  subagent_type='general-purpose',
  model='haiku',
  run_in_background=true,
  description='Open source research',
  prompt='Use GitMVP to find relevant repositories...'
)

# Agent 4: Security
Task(
  subagent_type='general-purpose',
  model='haiku',
  run_in_background=true,
  description='Security research',
  prompt='WebSearch for {domain} security best practices...'
)

# Agent 5: Competitors
Task(
  subagent_type='general-purpose',
  model='haiku',
  run_in_background=true,
  description='Competitor analysis',
  prompt='WebSearch for {domain} competitors products...'
)
```

### Step 4: Collect Results

Use TaskOutput to collect all agent results.

### Step 5: Synthesize Findings

Save each research result:

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py save_research "tech_stack" "<content>"
```

### Step 6: Output Research Summary

```markdown
## Research Complete

### Tech Stack

- [Key findings]

### Market Trends

- [Key findings]

### Open Source

- [Top repositories]

### Security

- [Key considerations]

### Competitors

- [Key players]

### Next Steps

1. `/devflow-suggest` - Get feature suggestions based on research
2. `/devflow-plan` - Generate development plan
```

## Example

```
User: /devflow-research

User: /devflow-research --focus security
```
