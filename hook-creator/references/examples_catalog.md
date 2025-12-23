# Hook Examples Catalog

## 1. Auto-Formatter (PostToolUse)

Format code after file changes:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/format.py",
        "timeout": 30
      }]
    }]
  }
}
```

**format.py:**
```python
#!/usr/bin/env python3
import json, sys, subprocess
data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")
if path.endswith((".ts", ".tsx", ".js", ".jsx")):
    subprocess.run(["npx", "prettier", "--write", path])
```

## 2. Secret Detector (UserPromptSubmit)

Block prompts with secrets:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/detect-secrets.py"
      }]
    }]
  }
}
```

**detect-secrets.py:**
```python
#!/usr/bin/env python3
import json, sys, re
data = json.load(sys.stdin)
prompt = data.get("prompt", "")
if re.search(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]", prompt):
    print(json.dumps({"decision": "block", "reason": "Secrets detected"}))
sys.exit(0)
```

## 3. File Protection (PreToolUse)

Protect sensitive files:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/protect.py"
      }]
    }]
  }
}
```

**protect.py:**
```python
#!/usr/bin/env python3
import json, sys
data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")
protected = [".env", "package-lock.json", ".git/"]
for p in protected:
    if p in path:
        print(f"Protected: {path}", file=sys.stderr)
        sys.exit(2)
```

## 4. Context Injector (SessionStart)

Load context at session start:

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "git status && git log -1 --oneline"
      }]
    }]
  }
}
```

## 5. Auto-Approve Docs (PreToolUse)

Auto-approve reading documentation:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Read",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/auto-approve.py"
      }]
    }]
  }
}
```

**auto-approve.py:**
```python
#!/usr/bin/env python3
import json, sys
data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")
if path.endswith((".md", ".txt", ".json", ".yml")):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Documentation file"
        }
    }))
```

## 6. Command Validator (PreToolUse)

Validate bash commands:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/validate-cmd.py"
      }]
    }]
  }
}
```

## 7. Intelligent Stop (Prompt-Based)

LLM-based stop decision:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Check if all tasks complete. Respond: {\"decision\": \"approve\"|\"block\", \"reason\": \"...\"}",
        "timeout": 30
      }]
    }]
  }
}
```

## 8. MCP Tool Logger

Log MCP tool usage:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "mcp__.*",
      "hooks": [{
        "type": "command",
        "command": "echo \"$(date): MCP tool used\" >> ~/mcp.log"
      }]
    }]
  }
}
```
