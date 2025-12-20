# Hooks Integration Guide

Reference for integrating hooks with skills. Update via `upgrade_knowledge.py`.

## Hook Events

| Event | Triggered | Use Case |
|-------|-----------|----------|
| PreToolUse | Before tool execution | Block/approve, modify input |
| PostToolUse | After tool completes | Format, validate, cleanup |
| PermissionRequest | Permission dialog shown | Auto-approve/deny |
| UserPromptSubmit | User submits prompt | Validate, add context |
| Notification | Claude sends notification | Custom alerts |
| Stop | Claude finishes responding | Evaluate completion |
| SubagentStop | Subagent finishes | Evaluate subagent |
| PreCompact | Before context compaction | Handle compaction |
| SessionStart | Session begins | Load context, setup |
| SessionEnd | Session ends | Cleanup, logging |

## Configuration

Location: `~/.claude/settings.json` or `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "validation-script.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

## Hook Input (stdin)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": { "file_path": "...", "content": "..." }
}
```

## Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | Continue, stdout in verbose mode |
| 2 | Block | Block tool call, stderr as error |
| Other | Non-blocking error | Continue, stderr in verbose mode |

## Decision Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": { "modified": "input" }
  },
  "continue": true,
  "systemMessage": "Optional message"
}
```

### Decision Options

| Event | Decisions |
|-------|-----------|
| PreToolUse | `allow`, `deny`, `ask` |
| PermissionRequest | `allow`, `deny` |
| PostToolUse | `block` |
| Stop/SubagentStop | `block` |

## Skill Integration Patterns

### Auto-format on Write

```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "command": "npx prettier --write \"$(jq -r '.tool_input.file_path')\""
    }]
  }]
}
```

### Protect Files

```bash
#!/bin/bash
path=$(jq -r '.tool_input.file_path')
if [[ "$path" == *".env"* ]]; then
  exit 2
fi
exit 0
```

### Validate Before Commit

```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "command": "echo \"$1\" | grep -q 'git commit' && npm test"
    }]
  }]
}
```

## Security Best Practices

1. **Validate inputs** - Sanitize all JSON data
2. **Quote variables** - Use `"$VAR"` not `$VAR`
3. **Check paths** - Block path traversal (`..`)
4. **Skip sensitive files** - `.env`, credentials, keys
5. **Use absolute paths** - Avoid relative path confusion
6. **Set timeouts** - Default 60s, max 600s

## Version

Last updated: 2025-01

To refresh: Run `python3 scripts/upgrade_knowledge.py`
