# Workflow Format Examples

Complete examples for each output format.

## Skill Example

**File:** `~/.claude/skills/code-formatter/SKILL.md`

```yaml
---
name: code-formatter
description: Format code files using project-specific formatters. Use when user asks to format code, clean up files, or apply code style. Supports Prettier, ESLint, Black, and rustfmt.
---

# Code Formatter

Format code files using detected project formatters.

## Workflow

1. Detect project type and available formatters
2. Identify files to format (from user request or git status)
3. Run appropriate formatter
4. Report results

## Formatter Detection

Check for configuration files:
- `package.json` with prettier/eslint → npm run format
- `pyproject.toml` with black → black .
- `Cargo.toml` → cargo fmt
- `.prettierrc` → npx prettier --write

## Usage

Trigger phrases:
- "format this file"
- "clean up the code"
- "apply code style"
```

## Slash Command Example

**File:** `~/.claude/commands/pr-review.md`

```yaml
---
allowed-tools: Bash(gh:*), Read, Grep, Glob
argument-hint: [PR number]
description: Review a GitHub pull request
---

Review PR #$1 thoroughly.

## Context
- PR details: !`gh pr view $1 --json title,body,files`
- Changed files: !`gh pr diff $1 --name-only`

## Review Steps

1. Understand the PR purpose from title and description
2. Review each changed file for:
   - Code quality and readability
   - Potential bugs or edge cases
   - Security concerns
   - Test coverage
3. Provide constructive feedback
4. Suggest improvements if needed

## Output Format

Provide review as:
- Summary (1-2 sentences)
- File-by-file comments
- Overall recommendation (approve/request changes)
```

## Subagent Example

**File:** `~/.claude/agents/debugger.md`

```yaml
---
name: debugger
description: Expert debugger for investigating errors and issues. Use when encountering bugs, errors, or unexpected behavior. Methodically traces execution paths and identifies root causes.
tools: Read, Grep, Glob, Bash, LSP
model: sonnet
---

You are an expert debugger with deep experience in systematic problem-solving.

## Approach

When investigating issues:

1. **Reproduce**: Understand how to trigger the issue
2. **Isolate**: Narrow down the problem scope
3. **Trace**: Follow execution path to find the source
4. **Verify**: Confirm the root cause
5. **Fix**: Propose minimal, targeted fix

## Techniques

- Read error messages and stack traces carefully
- Use Grep to find related code patterns
- Check recent git changes that might have introduced the issue
- Add strategic logging if needed
- Test hypotheses systematically

## Communication

- Explain findings clearly
- Show evidence for conclusions
- Propose fixes with rationale
```

## Hook Example

**File:** `.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$FILE_PATH\"",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/validate_command.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/add_context.sh"
          }
        ]
      }
    ]
  }
}
```

**Hook Script Example:** `~/.claude/hooks/validate_command.py`

```python
#!/usr/bin/env python3
import json
import sys

# Read hook input from stdin
data = json.load(sys.stdin)
command = data.get('tool_input', {}).get('command', '')

# Block dangerous commands
dangerous = ['rm -rf /', 'sudo rm', ':(){:|:&};:']
for pattern in dangerous:
    if pattern in command:
        print(f"Blocked dangerous command: {pattern}", file=sys.stderr)
        sys.exit(2)  # Exit 2 = block

sys.exit(0)  # Exit 0 = allow
```

## Combination Example

A complex workflow might use multiple formats:

1. **Skill** (`deploy-assistant`) - Main workflow orchestration
2. **Slash Command** (`/deploy`) - Quick trigger for common deploy
3. **Hook** (PostToolUse on Bash) - Auto-log deployment commands
4. **Subagent** (`deploy-reviewer`) - Review deployment plans

This creates a cohesive deployment system with multiple entry points.
