# Latest Claude Code Features (2025)

Reference for current Claude Code capabilities. Update via `upgrade_knowledge.py`.

## Agent Skills

### SKILL.md Format

```yaml
---
name: skill-name
description: What it does + when to use it (WHAT + WHEN)
allowed-tools: Read, Grep, Bash  # Optional: restrict tools
---
```

**Requirements:**
- `name`: Hyphen-case, max 64 chars
- `description`: Max 1024 chars, include trigger scenarios
- SKILL.md: Under 200 lines total

### Bundled Resources

| Directory | Purpose | Loaded |
|-----------|---------|--------|
| `scripts/` | Executable code | On execution |
| `references/` | Documentation | On demand |
| `assets/` | Output files | Never (used in output) |

### Progressive Disclosure

1. Metadata (name+description) - Always in context
2. SKILL.md body - When skill triggers
3. Bundled resources - As needed

## Slash Commands

### Locations

- **Project**: `.claude/commands/` (team-wide)
- **Personal**: `~/.claude/commands/` (user-only)

### Frontmatter

```yaml
---
allowed-tools: Read, Grep, Bash(git status:*)
argument-hint: [priority] [assignee]
description: Brief description
model: claude-3-5-haiku-20241022
---
```

### Argument Syntax

- `$ARGUMENTS` - All arguments
- `$1`, `$2`, `$3` - Positional arguments
- `!`command`` - Execute bash inline
- `@file.txt` - Reference file

## Agents/Subagents

### Configuration

Location: `.claude/agents/` or `~/.claude/agents/`

```yaml
---
name: agent-name
description: When to use this agent
tools: Read, Edit, Bash
model: sonnet
permissionMode: default
skills: skill1, skill2
---

System prompt here...
```

### Built-in Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| Explore | Haiku | Fast codebase exploration |
| Plan | Sonnet | Research in plan mode |
| General | Sonnet | Complex multi-step tasks |

### Permission Modes

- `default` - Standard permissions
- `acceptEdits` - Auto-accept edits
- `bypassPermissions` - Skip permission prompts
- `plan` - Read-only mode

## MCP Integration

### Installation

```bash
# HTTP transport
claude mcp add --transport http server https://api.example.com/mcp

# Stdio transport
claude mcp add --transport stdio local-server -- npx my-mcp-server

# With env vars
claude mcp add --transport stdio db --env DB_KEY=xxx -- npx db-mcp
```

### Scopes

| Scope | Location | Access |
|-------|----------|--------|
| Local | `~/.claude.json` | Current project |
| Project | `.mcp.json` | Team-wide |
| User | `~/.claude.json` | All projects |

### Tool Access in Skills

MCP tools follow pattern: `mcp__<server>__<tool>`

```bash
# In hooks
"matcher": "mcp__github__.*"
```

## Version

Last updated: 2025-01 (Knowledge cutoff reference)

To refresh: Run `python3 scripts/upgrade_knowledge.py`
