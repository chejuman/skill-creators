---
name: codex-v2
description: Delegate coding tasks to OpenAI Codex CLI with async execution, retry logic, and batch processing. Use when needing algorithm implementation, debugging, code review, or multi-turn coding sessions via SESSION_ID.
---

## Quick Start

```bash
# Single task
python3 scripts/codex_bridge.py --cd "/project" --prompt "Analyze auth flow"

# Health check
python3 scripts/codex_bridge.py --health-check

# Batch processing
python3 scripts/codex_bridge.py --cd "/project" --batch prompts.json
```

## Parameters

### Required
| Parameter | Description |
|-----------|-------------|
| `--prompt` | Task instruction for Codex |
| `--cd` | Workspace root directory |

### Optional - Execution
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--session-id` | None | Resume previous session |
| `--sandbox` | `read-only` | `read-only` \| `workspace-write` \| `full-access` |
| `--timeout` | 300 | Max execution time in seconds |
| `--retries` | 3 | Retry attempts on failure |

### Optional - Features
| Parameter | Description |
|-----------|-------------|
| `--health-check` | Verify Codex CLI availability |
| `--batch FILE` | Process multiple prompts from JSON file |
| `--config FILE` | Load settings from config file |
| `--verbose` | Enable debug logging |
| `--all-messages` | Include full reasoning trace |

### Optional - Advanced
| Parameter | Description |
|-----------|-------------|
| `--image PATH` | Attach image files (comma-separated) |
| `--model NAME` | Specify model (use only when requested) |
| `--yolo` | Bypass approvals (use with caution) |

## Multi-turn Sessions

Capture `SESSION_ID` from first response for follow-ups:

```bash
# Initial task - returns SESSION_ID in response
python3 scripts/codex_bridge.py --cd "/project" --prompt "Review login.py"

# Continue session
python3 scripts/codex_bridge.py --cd "/project" --session-id "uuid" --prompt "Write tests"
```

## Batch Processing

Create `prompts.json`:
```json
[
  {"prompt": "Analyze security in auth.py", "cd": "/project"},
  {"prompt": "Review error handling", "cd": "/project"}
]
```

Run batch:
```bash
python3 scripts/codex_bridge.py --batch prompts.json
```

## Configuration File

Create `.codex-bridge.json` in project root or `~/.config/codex-bridge.json`:

```json
{
  "sandbox": "read-only",
  "timeout": 300,
  "retries": 3,
  "verbose": false
}
```

## Output Schema

### Success Response
```json
{
  "success": true,
  "session_id": "uuid-string",
  "response": "Codex response text",
  "duration_ms": 1234
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "type": "timeout|execution|network|validation",
    "message": "Error description",
    "retries_attempted": 2
  }
}
```

### Batch Response
```json
{
  "success": true,
  "results": [...],
  "summary": {"total": 3, "succeeded": 2, "failed": 1}
}
```

## Error Handling

| Error Type | Cause | Resolution |
|------------|-------|------------|
| `validation` | Invalid parameters | Check required params |
| `network` | Connection issues | Auto-retry with backoff |
| `timeout` | Exceeded time limit | Increase --timeout |
| `execution` | Codex CLI error | Check --verbose output |

## Troubleshooting

**Codex not found:**
```bash
python3 scripts/codex_bridge.py --health-check
# Ensure: npm i -g @openai/codex
```

**Session expired:**
- Sessions may expire after inactivity
- Start new session without --session-id

**Timeout issues:**
```bash
python3 scripts/codex_bridge.py --timeout 600 --prompt "Complex task"
```
