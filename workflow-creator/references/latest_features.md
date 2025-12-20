# Claude Code Latest Features Reference

Last updated: 2025-12-20

## Extension Mechanisms Overview

| Mechanism | Purpose | Invocation | Location |
|-----------|---------|------------|----------|
| Skill | Complex workflows | Auto (model) | `~/.claude/skills/` |
| Slash Command | Quick prompts | Manual (`/`) | `~/.claude/commands/` |
| Subagent | Specialized AI | Auto/Explicit | `~/.claude/agents/` |
| Hook | Event reactions | Automatic | `settings.json` |
| MCP | External tools | Via tools | `.mcp.json` |

## Skills (SKILL.md)

### Frontmatter Fields
```yaml
---
name: skill-name          # Required, hyphen-case, max 64 chars
description: ...          # Required, max 1024 chars, include WHAT + WHEN
allowed-tools: Read, Grep # Optional, restrict available tools
---
```

### Directory Structure
```
skill-name/
├── SKILL.md         # Required
├── scripts/         # Executable code
├── references/      # Documentation
└── assets/          # Output templates
```

### Progressive Disclosure
1. **Metadata** (~100 words) - Always in context
2. **SKILL.md body** (~5k words) - When triggered
3. **Resources** - Loaded as needed

## Slash Commands

### Frontmatter Fields
```yaml
---
allowed-tools: Bash(git:*)     # Tool restrictions
argument-hint: [message]        # Usage hint
description: Brief description  # Command description
model: claude-3-5-haiku-20241022  # Model override
disable-model-invocation: false # Prevent auto-invoke
---
```

### Argument Access
- `$ARGUMENTS` - All arguments as string
- `$1`, `$2`, `$3` - Individual arguments
- `!`backticks`` - Execute bash inline

## Subagents

### Frontmatter Fields
```yaml
---
name: agent-name           # Required, hyphen-case
description: When to use   # Required
tools: Read, Grep, Bash    # Optional, comma-separated
model: inherit             # sonnet/opus/haiku/inherit
permissionMode: default    # Permission handling
skills: skill1, skill2     # Auto-load skills
---
```

### Built-in Agents
- **Explore** - Fast, read-only codebase exploration (Haiku)
- **Plan** - Research-only planning (Sonnet)
- **general-purpose** - Full capabilities (Sonnet)

## Hooks

### Event Types
| Event | When | Use Case |
|-------|------|----------|
| PreToolUse | Before tool | Block/modify |
| PostToolUse | After tool | Format/validate |
| UserPromptSubmit | Before processing | Add context |
| SessionStart | Session begins | Setup env |
| Stop | Claude stops | Prevent stopping |
| SubagentStop | Subagent done | Evaluate completion |
| PreCompact | Before compaction | Cleanup |

### Configuration
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash|Write",
      "hooks": [{
        "type": "command",
        "command": "/path/to/script.sh"
      }]
    }]
  }
}
```

### Hook I/O
- **Input**: JSON via stdin (session_id, tool_name, tool_input, etc.)
- **Output**: Exit code 0=success, 2=block; JSON for decisions

## MCP Integration

### Configuration Locations
1. `~/.claude.json` - Personal, per-project (default)
2. `.mcp.json` - Shared via git
3. `~/.claude.json` (global) - All projects

### Server Types
```json
{
  "mcpServers": {
    "http-server": {
      "type": "http",
      "url": "https://mcp.example.com"
    },
    "stdio-server": {
      "type": "stdio",
      "command": "/path/to/server",
      "args": ["--config", "config.json"],
      "env": {"API_KEY": "${API_KEY}"}
    }
  }
}
```

## CLAUDE.md Memory

### Hierarchy (Priority)
1. Enterprise policy
2. Project `./CLAUDE.md`
3. Project rules `.claude/rules/*.md`
4. User `~/.claude/CLAUDE.md`
5. Local `./CLAUDE.local.md`

### Features
- File imports: `@path/to/file`
- Recursive discovery up directory tree
- Path-specific rules with `paths:` frontmatter

## Settings (settings.json)

### Locations
- `~/.claude/settings.json` - User
- `.claude/settings.json` - Project (shared)
- `.claude/settings.local.json` - Local (not committed)

### Key Fields
```json
{
  "permissions": {
    "allow": ["Bash(npm run:*)"],
    "deny": ["Read(.env)"],
    "defaultMode": "acceptEdits"
  },
  "hooks": {},
  "model": "claude-opus-4-5-20251101"
}
```
