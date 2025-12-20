---
name: workflow-creator
description: Universal workflow creator that builds any type of Claude Code workflow (skills, slash commands, subagents, hooks). Use when user asks to create a workflow, automate a task, make a new skill, add a command, or build automation. Learns latest features, gathers requirements through questions, researches real-time trends and best practices, selects optimal output format, generates code, and installs.
---

# Workflow Creator

Create any Claude Code workflow through interactive requirement gathering and intelligent format selection.

## Workflow Overview

```
1. Self-Upgrade → 2. Gather Requirements → 3. Research & Trends → 4. Select Format → 5. Generate → 6. Install
```

## Phase 1: Self-Upgrade (Always First)

Before creating any workflow, upgrade knowledge using claude-code-guide agent:

```
Use Task tool with subagent_type='claude-code-guide' to learn:
- Latest skill/command/agent specifications
- Current hook events and configuration
- MCP integration patterns
- Best practices updates
```

Update `references/latest_features.md` with new information.

## Phase 2: Gather Requirements

Use AskUserQuestion tool to collect information:

### Essential Questions

1. **Purpose**: "What should this workflow do? Describe the main functionality."
2. **Trigger**: "When should this activate? (explicit command, automatic detection, specific event)"
3. **Steps**: "What are the main steps or actions?"
4. **Input/Output**: "What input does it need? What output should it produce?"

### Clarifying Questions (as needed)

- "Should this be shared with your team or personal only?"
- "Does this need external tools (MCP servers, APIs)?"
- "Any specific tools/permissions required or restricted?"

## Phase 3: Research & Trends (MANDATORY)

After gathering requirements, **always** research real-time information to enhance the workflow.

### Research Strategy

Use WebSearch tool to find:

1. **Latest Best Practices**
   - Search: `"<domain> best practices 2025"`
   - Search: `"<technology> workflow patterns"`

2. **Existing Solutions & Libraries**
   - Search: `"<task> automation tool"`
   - Search: `"<language> <task> library npm/pip"`

3. **Similar Implementations**
   - Search: `"Claude Code skill <similar-task>"`
   - Search: `"<task> CLI automation example"`

4. **Potential Issues & Solutions**
   - Search: `"<task> common problems solutions"`
   - Search: `"<technology> pitfalls avoid"`

### Research Queries by Domain

| Domain | Example Searches |
|--------|------------------|
| Development | "code review automation 2025", "git workflow best practices" |
| Documentation | "markdown generation tools", "API documentation patterns" |
| Data Processing | "data pipeline automation", "ETL best practices 2025" |
| DevOps | "CI/CD automation patterns", "deployment workflow tools" |
| Testing | "test automation framework comparison", "E2E testing best practices" |

### Using WebFetch for Documentation

For specific documentation or examples:
```
WebFetch: https://docs.example.com/api
Prompt: "Extract key API patterns and usage examples relevant to <task>"
```

### Synthesize Findings

After research, summarize:
1. **Recommended approach** based on current trends
2. **Libraries/tools** to integrate or reference
3. **Patterns to follow** from successful implementations
4. **Pitfalls to avoid** from common issues found

Store valuable findings in `references/` for the generated workflow.

## Phase 4: Select Output Format

Based on gathered requirements, select the optimal format:

| Requirement | Best Format |
|------------|-------------|
| User explicitly calls with `/` | **Slash Command** |
| Auto-detect from context | **Skill** |
| Specialized AI behavior | **Subagent** |
| React to tool usage/events | **Hook** |
| Multiple formats needed | **Combination** |

### Format Decision Tree

```
Is it triggered by specific command?
  YES → Slash Command (.claude/commands/)
  NO ↓
Should it auto-activate based on context?
  YES → Skill (.claude/skills/ or ~/.claude/skills/)
  NO ↓
Does it need specialized AI persona?
  YES → Subagent (.claude/agents/)
  NO ↓
Should it react to tool/event?
  YES → Hook (settings.json)
  NO → Skill (default)
```

## Phase 5: Generate Workflow

### For Skills (SKILL.md)

```bash
# Initialize structure
mkdir -p <skill-name>/{scripts,references,assets}
```

Create files in order:
1. `scripts/` - Executable code for repeated operations
2. `references/` - Documentation for context
3. `assets/` - Templates for output
4. `SKILL.md` - Main instructions with frontmatter

**SKILL.md Template:**
```yaml
---
name: <skill-name>
description: <what-it-does>. Use when <trigger-scenarios>.
---

# <Skill Name>

## Overview
<Brief description>

## Workflow
<Step-by-step instructions>

## Resources
- [script.py](scripts/script.py) - <purpose>
- [reference.md](references/reference.md) - <purpose>
```

### For Slash Commands

Location: `.claude/commands/<command-name>.md` or `~/.claude/commands/<command-name>.md`

**Template:**
```yaml
---
allowed-tools: <tool-list>
argument-hint: [<arg-hint>]
description: <brief-description>
---

<Command instructions>

Arguments: $ARGUMENTS or $1, $2, $3...
```

### For Subagents

Location: `.claude/agents/<agent-name>.md` or `~/.claude/agents/<agent-name>.md`

**Template:**
```yaml
---
name: <agent-name>
description: <when-to-use>
tools: <tool-list>
model: inherit
---

<Agent persona and instructions>
```

### For Hooks

Location: `.claude/settings.json` or `~/.claude/settings.json`

**Template:**
```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<tool-pattern>",
        "hooks": [
          {
            "type": "command",
            "command": "<script-path>"
          }
        ]
      }
    ]
  }
}
```

Hook events: PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, Stop, etc.

## Phase 6: Validate & Install

### Validation Checklist

- [ ] YAML frontmatter is valid
- [ ] Name uses hyphen-case
- [ ] Description includes WHAT + WHEN
- [ ] Files under 200 lines each
- [ ] No unused template files
- [ ] Scripts are executable

### Installation

**For Skills:**
```bash
# Package if in development workspace
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./<skill> .

# Install
unzip -o <skill>.zip -d ~/.claude/skills/
chmod +x ~/.claude/skills/<skill>/scripts/*.py 2>/dev/null || true
```

**For Slash Commands:**
```bash
# Personal
cp <command>.md ~/.claude/commands/

# Project
cp <command>.md .claude/commands/
```

**For Subagents:**
```bash
# Personal
cp <agent>.md ~/.claude/agents/

# Project
cp <agent>.md .claude/agents/
```

**For Hooks:**
```bash
# Merge into existing settings.json
# Use jq or manual merge
```

## Quick Reference

### Trigger Keywords (activate this skill)

- "워크플로우 만들어줘" / "create a workflow"
- "새 스킬 만들어" / "make a new skill"
- "자동화하고 싶어" / "automate this"
- "명령어 추가해줘" / "add a command"
- "에이전트 만들어" / "create an agent"

### Output Locations Summary

| Type | Personal | Project |
|------|----------|---------|
| Skill | `~/.claude/skills/` | `.claude/skills/` |
| Command | `~/.claude/commands/` | `.claude/commands/` |
| Agent | `~/.claude/agents/` | `.claude/agents/` |
| Hook | `~/.claude/settings.json` | `.claude/settings.json` |

### Resources

- [Latest Features](references/latest_features.md) - Current Claude Code capabilities
- [Format Examples](references/format_examples.md) - Template examples for each format
