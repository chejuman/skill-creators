# Hook Events Reference

## All Events

| Event | Matcher | Trigger |
|-------|---------|---------|
| PreToolUse | Yes | Before tool execution |
| PostToolUse | Yes | After tool completes |
| PermissionRequest | Yes | Permission dialog shown |
| UserPromptSubmit | No | User submits prompt |
| Stop | No | Agent finishes |
| SubagentStop | No | Subagent completes |
| SessionStart | Yes | Session begins |
| SessionEnd | No | Session ends |
| PreCompact | Yes | Before context compact |
| Notification | Yes | Notification sent |

## Input Schema (All Events)

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "EventName"
}
```

## PreToolUse

**Input:**
```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {"file_path": "/path", "content": "..."},
  "tool_use_id": "toolu_01ABC..."
}
```

**Output (JSON):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "reason",
    "updatedInput": {"field": "new_value"}
  }
}
```

## PostToolUse

**Input:**
```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {"file_path": "/path"},
  "tool_response": {"success": true},
  "tool_use_id": "toolu_01ABC..."
}
```

**Output:**
```json
{
  "decision": "block",
  "reason": "explanation",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "info for Claude"
  }
}
```

## UserPromptSubmit

**Input:**
```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "user's prompt text"
}
```

**Output:**
```json
{
  "decision": "block",
  "reason": "shown to user only",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "injected context"
  }
}
```

## Stop / SubagentStop

**Input:**
```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

**Output:**
```json
{
  "decision": "block",
  "reason": "must continue because..."
}
```

## SessionStart

**Matchers:** `startup`, `resume`, `clear`, `compact`

**Input:**
```json
{
  "hook_event_name": "SessionStart",
  "source": "startup|resume|clear|compact"
}
```

**Output:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "loaded context"
  }
}
```

**Environment Variable:** Use `$CLAUDE_ENV_FILE` to persist env vars.

## PreCompact

**Matchers:** `manual`, `auto`

**Input:**
```json
{
  "hook_event_name": "PreCompact",
  "trigger": "manual|auto",
  "custom_instructions": ""
}
```

## Notification

**Matchers:** `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`

**Input:**
```json
{
  "hook_event_name": "Notification",
  "message": "notification message",
  "notification_type": "permission_prompt"
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success, continue execution |
| 2 | Block action, stderr as error |
| Other | Non-blocking warning |

## Environment Variables

- `CLAUDE_PROJECT_DIR` - Project root path
- `CLAUDE_ENV_FILE` - Env file path (SessionStart only)
- `CLAUDE_CODE_REMOTE` - "true" if web environment
