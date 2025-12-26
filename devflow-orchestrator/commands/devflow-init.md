# /devflow-init

Initialize a new DevFlow project from an idea.

## Usage

```
/devflow-init <idea> [domain]
```

## Arguments

- `idea` (required): The project idea or concept
- `domain` (optional): Domain category (default: "general")

## What This Does

### Step 1: Initialize Project Structure

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py init "<idea>" "<domain>"
```

Creates `.devflow/` structure:

```
.devflow/
├── project.json           # Project metadata
├── versions/
│   └── v0.0-idea.md      # Initial idea capture
├── research/              # Research findings
├── features/
│   ├── backlog.json      # Feature backlog
│   └── decisions.md      # Decision log
├── plans/                 # Current plans
└── meta/
    ├── self_upgrade_log.md
    └── workflow_metrics.json
```

### Step 2: Self-Upgrade Check

```
Task(
  subagent_type='claude-code-guide',
  prompt='Get latest Claude Code features: Skills, Subagents, MCP tools',
  description='Upgrade knowledge'
)
```

### Step 3: Domain Detection

Analyze idea to detect domain and recommend initial research focus:

- DevOps, Security, WebDev, DataOps, Documentation, Testing, General

### Step 4: Output Confirmation

```markdown
## DevFlow Project Initialized

**Idea**: {idea}
**Domain**: {domain}
**Version**: v0.0 (Idea Stage)
**Target**: v10.0+

### Next Steps

1. `/devflow-research` - Run multi-agent research
2. `/devflow-suggest` - Get feature suggestions
3. `/devflow-status` - View current state
```

## Example

```
User: /devflow-init "AI-powered code review tool" devops

User: /devflow-init "Real-time collaboration platform"
```
