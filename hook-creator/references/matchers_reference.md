# Matcher Patterns Reference

## Matcher Syntax

Matchers are **case-sensitive** regex patterns that filter which tools trigger hooks.

### Basic Patterns

| Pattern | Matches | Example |
|---------|---------|---------|
| `Write` | Exact tool name | Only Write tool |
| `Write\|Edit` | Multiple tools | Write OR Edit |
| `Write.*` | Regex wildcard | Write, WriteFile, etc. |
| `*` | All tools | Everything |
| `""` (empty) | All tools | Everything |

### MCP Tool Patterns

```
mcp__<server>__<tool>
```

| Pattern | Matches |
|---------|---------|
| `mcp__memory__.*` | All memory server tools |
| `mcp__.*__write.*` | All write operations |
| `mcp__github__search.*` | GitHub search tools |

## Common Tool Names

### File Operations

| Tool | Description |
|------|-------------|
| `Read` | Read file contents |
| `Write` | Create/overwrite file |
| `Edit` | Modify existing file |
| `Glob` | File pattern matching |
| `Grep` | Content search |

### System Operations

| Tool | Description |
|------|-------------|
| `Bash` | Shell command execution |
| `Task` | Subagent task |
| `WebFetch` | Fetch web content |
| `WebSearch` | Web search |

### Notebook Operations

| Tool | Description |
|------|-------------|
| `NotebookEdit` | Edit Jupyter notebook |
| `NotebookRead` | Read notebook |

## Matcher by Event

| Event | Matcher Support | Examples |
|-------|-----------------|----------|
| PreToolUse | Yes | `Bash`, `Write\|Edit` |
| PostToolUse | Yes | `Write\|Edit` |
| PermissionRequest | Yes | `Bash`, `Read` |
| UserPromptSubmit | No | N/A |
| Stop | No | N/A |
| SubagentStop | No | N/A |
| SessionStart | Yes | `startup`, `resume` |
| PreCompact | Yes | `manual`, `auto` |
| Notification | Yes | `permission_prompt` |

## SessionStart Matchers

| Matcher | Trigger |
|---------|---------|
| `startup` | New session start |
| `resume` | Session resume |
| `clear` | After /clear command |
| `compact` | After context compact |

## PreCompact Matchers

| Matcher | Trigger |
|---------|---------|
| `manual` | /compact command |
| `auto` | Automatic compaction |

## Notification Matchers

| Matcher | Trigger |
|---------|---------|
| `permission_prompt` | Permission dialog |
| `idle_prompt` | Waiting for input |
| `auth_success` | Auth completed |
| `elicitation_dialog` | MCP elicitation |

## Pattern Examples

### Format TypeScript files

```json
{"matcher": "Write|Edit"}
```

### Block dangerous commands

```json
{"matcher": "Bash"}
```

### Auto-approve documentation reads

```json
{"matcher": "Read"}
```

### Log all MCP operations

```json
{"matcher": "mcp__.*"}
```

### Protect specific files

```json
{"matcher": "Write|Edit"}
```
Filter in script: check `file_path` for `.env`, `.git/`

## Regex Tips

- Case-sensitive: `Write` ≠ `write`
- Use `|` for OR: `Write|Edit`
- Use `.*` for wildcards: `mcp__.*`
- Escape special chars: `\\.env`
- No anchors needed: patterns match anywhere
