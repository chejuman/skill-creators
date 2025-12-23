---
name: hook-creator
description: Self-upgrading Claude Code hook creator. Generates hooks.json configurations with latest schema by fetching current documentation via claude-code-guide. Use when creating hooks for PreToolUse, PostToolUse, SessionStart, UserPromptSubmit, Stop events. Triggers on "create hook", "add hook", "hook for formatting", "auto-approve permission", "session context".
---

# Hook Creator

Self-upgradable skill for creating Claude Code hooks with the latest schema.

## Phase 1: Self-Upgrade (Before Every Hook Creation)

Before creating hooks, always fetch latest documentation:

```
Task(subagent_type='claude-code-guide', prompt='Get latest Claude Code hooks: events, JSON schema, matchers, input/output formats, examples')
```

## Phase 2: Hook Creation Workflow

### Step 1: Identify Hook Type

| Event | Trigger | Matcher | Use Case |
|-------|---------|---------|----------|
| PreToolUse | Before tool runs | Yes | Validate/block/modify tool calls |
| PostToolUse | After tool completes | Yes | Format code, validate results |
| PermissionRequest | Permission dialog | Yes | Auto-approve/deny permissions |
| UserPromptSubmit | User submits prompt | No | Add context, block secrets |
| Stop | Agent finishes | No | Force continuation |
| SessionStart | Session begins | Yes | Load environment, inject context |

### Step 2: Generate Hook

Use the generator script:

```bash
python3 scripts/generate_hook.py \
  --event PostToolUse \
  --matcher "Write|Edit" \
  --command "npx prettier --write" \
  --description "Auto-format on save"
```

Interactive mode:

```bash
python3 scripts/generate_hook.py --interactive
```

### Step 3: Validate

```bash
python3 scripts/validate_hook.py hooks.json
```

### Step 4: Merge into Settings

```bash
python3 scripts/merge_hooks.py hooks.json ~/.claude/settings.json
```

## Quick Examples

### Auto-Formatter

```json
{"hooks":{"PostToolUse":[{"matcher":"Write|Edit","hooks":[{"type":"command","command":"npx prettier --write \"$(jq -r '.tool_input.file_path')\""}]}]}}
```

### Secret Detector

```json
{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"python3 ~/.claude/hooks/detect-secrets.py"}]}]}}
```

### Context Injector

```json
{"hooks":{"SessionStart":[{"matcher":"startup","hooks":[{"type":"command","command":"git status && git log -1 --oneline"}]}]}}
```

## Hook JSON Schema

```json
{
  "hooks": {
    "EventName": [{
      "matcher": "Pattern",
      "hooks": [{"type": "command", "command": "cmd", "timeout": 60}]
    }]
  }
}
```

## Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `Write` | Exact tool |
| `Write\|Edit` | Multiple tools |
| `mcp__*` | All MCP tools |
| `*` | All tools |

## Exit Codes

| Code | Behavior |
|------|----------|
| 0 | Success, continue |
| 2 | Block action |
| Other | Warning only |

## References

- [Events Reference](references/events_reference.md) - All 10 events with schemas
- [Examples Catalog](references/examples_catalog.md) - Ready-to-use examples
