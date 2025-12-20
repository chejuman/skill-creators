---
name: self-upgradable-skill-creator
description: Self-upgrading skill creator that learns latest Claude Code features (skills, hooks, agents, MCP, slash commands) before creating skills. Use when creating new skills, upgrading existing skills, or when user asks for skill development. Automatically fetches and applies latest documentation to ensure skills follow current best practices.
---

# Self-Upgradable Skill Creator

A skill creator that upgrades its own knowledge before creating skills for users.

## Core Workflow

### Phase 1: Self-Upgrade (Before Every Skill Creation)

Before creating any skill, always upgrade knowledge by:

1. **Fetch Latest Documentation** - Use claude-code-guide agent or WebSearch to get current info on:
   - Agent Skills (SKILL.md format, bundled resources, progressive disclosure)
   - Slash Commands (syntax, frontmatter, arguments)
   - Agents/Subagents (configuration, built-in agents, custom agents)
   - Hooks (events, configuration, security)
   - MCP Integration (servers, tools, resources)

2. **Update Knowledge Base** - Store learned info in `references/` for reuse

3. **Apply to Skill Creation** - Use upgraded knowledge to create skills

### Phase 2: Skill Creation

After self-upgrade, follow the skill creation workflow:

#### Step 1: Understand Requirements
Gather concrete examples of how the skill will be used. Key questions:
- "What functionality should the skill support?"
- "What triggers this skill?"
- "What would a user say that should activate this skill?"

#### Step 2: Plan Reusable Contents
For each example, identify:
- Scripts needed (`scripts/`) - Executable code for repeated operations
- References needed (`references/`) - Documentation for context
- Assets needed (`assets/`) - Templates, images for output

#### Step 3: Initialize Skill
```bash
python3 scripts/init_skill.py <skill-name> --path <output-dir>
```

#### Step 4: Edit Skill Contents
1. Create bundled resources first (scripts, references, assets)
2. Delete unused example files
3. Update SKILL.md with:
   - Clear description (WHAT + WHEN)
   - Imperative/infinitive writing style
   - References to all bundled resources

#### Step 5: Validate & Package
```bash
python3 scripts/quick_validate.py <skill-path>
python3 scripts/package_skill.py <skill-path> <output-dir>
```

#### Step 6: Install
```bash
unzip -o <skill-name>.zip -d ~/.claude/skills/
chmod +x ~/.claude/skills/<skill-name>/scripts/*.py
```

## Advanced Features

### Skill Analysis & Improvement
To analyze an existing skill for improvements:
```bash
python3 scripts/analyze_skill.py <skill-path>
```

### Upgrade Knowledge Cache
To refresh the knowledge base with latest Claude Code features:
```bash
python3 scripts/upgrade_knowledge.py
```

## Skill Structure Patterns

Choose based on skill purpose:

| Pattern | Best For | Structure |
|---------|----------|-----------|
| Workflow-Based | Sequential processes | Overview → Decision Tree → Steps |
| Task-Based | Tool collections | Overview → Quick Start → Tasks |
| Reference/Guidelines | Standards/specs | Overview → Guidelines → Specs |
| Capabilities-Based | Integrated systems | Overview → Capabilities list |

## Critical Requirements

- **SKILL.md**: Under 200 lines, valid YAML frontmatter
- **Naming**: Hyphen-case only (e.g., `my-skill`)
- **Description**: Include WHAT + WHEN (no angle brackets)
- **Scripts**: Under 200 lines each, include requirements.txt
- **Writing Style**: Imperative form ("To X, do Y" not "You should X")

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `init_skill.py` | Initialize new skill from template |
| `package_skill.py` | Validate and package into .zip |
| `quick_validate.py` | Quick validation check |
| `analyze_skill.py` | Analyze skill for improvements |
| `upgrade_knowledge.py` | Fetch latest Claude Code docs |

## Related Documentation

- [Latest Features](references/latest_features.md) - Current Claude Code capabilities
- [Skill Patterns](references/skill_patterns.md) - Detailed structure patterns
- [Hook Integration](references/hooks_integration.md) - Using hooks in skills
