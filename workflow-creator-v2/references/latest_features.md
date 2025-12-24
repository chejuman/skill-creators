# Claude Code Latest Features

Last updated: 2025-12-24

## Extension Mechanisms

| Mechanism     | Purpose           | Invocation    | Location              |
| ------------- | ----------------- | ------------- | --------------------- |
| Skill         | Complex workflows | Auto (model)  | `~/.claude/skills/`   |
| Slash Command | Quick prompts     | Manual (`/`)  | `~/.claude/commands/` |
| Subagent      | Specialized AI    | Auto/Explicit | `~/.claude/agents/`   |
| Hook          | Event reactions   | Automatic     | `settings.json`       |
| MCP           | External tools    | Via tools     | `.mcp.json`           |

## Skills (SKILL.md)

### Frontmatter

```yaml
---
name: skill-name # Required, hyphen-case, max 64 chars
description: ... # Required, max 1024 chars, include WHAT + WHEN
allowed-tools: Read, Grep # Optional, restrict available tools
---
```

### Structure

```
skill-name/
├── SKILL.md         # Required, <200 lines
├── scripts/         # Executable code
├── references/      # Documentation
└── assets/          # Output templates
```

## Slash Commands

### Frontmatter

```yaml
---
allowed-tools: Bash(git:*)     # Tool restrictions
argument-hint: [arg1] [arg2]   # Usage hint
description: Brief description  # Command description
---
```

### Argument Access

- `$ARGUMENTS` - All arguments as string
- `$1`, `$2`, `$3` - Individual arguments
- `!`command`` - Execute bash inline
- `@file` - Include file contents

## Subagents

### Frontmatter

```yaml
---
name: agent-name # Required, hyphen-case
description: When to use # Required
tools: Read, Grep, Bash # Optional
model: sonnet # sonnet/opus/haiku/inherit
---
```

### Built-in Agents

| Agent           | Model  | Tools     | Purpose       |
| --------------- | ------ | --------- | ------------- |
| Explore         | Haiku  | Read-only | Fast search   |
| Plan            | Sonnet | Read-only | Research      |
| general-purpose | Sonnet | All       | Complex tasks |

### Task Tool Parameters

```python
Task(
  subagent_type='agent-name',
  prompt='Task description',
  description='Short summary',
  model='haiku',
  run_in_background=True  # Parallel execution
)
```

## Hooks

### Event Types

| Event            | Triggers       | Control           |
| ---------------- | -------------- | ----------------- |
| PreToolUse       | Before tool    | Allow/deny/modify |
| PostToolUse      | After tool     | Block/allow       |
| UserPromptSubmit | User submits   | Block/add context |
| SessionStart     | Session begins | Setup env         |
| Stop             | Agent stops    | Block/allow       |

### Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh"
          }
        ]
      }
    ]
  }
}
```

### Exit Codes

- **0**: Success (allow)
- **2**: Block (deny)
- Other: Non-blocking error

## MCP Integration

### Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": { "API_KEY": "${API_KEY}" }
    }
  }
}
```

## Multi-Agent Patterns

### Parallel Execution

```python
# Launch multiple agents in parallel
for domain in domains:
    Task(
        subagent_type='Explore',
        prompt=f'Research {domain}',
        model='haiku',
        run_in_background=True
    )
```

### Supervisor-Worker Pattern

```
Orchestrator
├── Research Agents (parallel, haiku)
├── Analysis Agent (sequential, sonnet)
└── Report Agent (final, sonnet)
```

## Composite Workflows

Combine multiple mechanisms:

1. **Skill**: Main orchestration
2. **Command**: Quick entry point
3. **Hook**: Automatic reactions
4. **Subagent**: Specialized tasks

### Example Structure

```
workflow/
├── skills/workflow/SKILL.md
├── commands/quick.md
├── agents/expert.md
└── hooks/hooks.json
```

## Best Practices

1. **Narrow Focus**: Specialized agents > generalized
2. **Context Efficiency**: Share only needed data
3. **Error Handling**: Graceful degradation
4. **Validation**: Test before installation
5. **Documentation**: Clear trigger phrases
