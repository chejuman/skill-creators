---
name: workflow-creator-v2
description: Multi-agent universal workflow creator with domain-specific expert agents. Creates skills, commands, subagents, hooks, and composite workflows. Use when user asks to create workflow, automate task, make skill, add command, or build automation. Supports DevOps, Security, WebDev, DataOps, Documentation, Testing domains with parallel research and intelligent scaffolding.
---

# Workflow Creator V2

Multi-agent architecture for creating any Claude Code workflow with domain expertise.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                               │
├─────────────────────────────────────────────────────────────────┤
│ Phase 1: Self-Upgrade ──► claude-code-guide (latest features)  │
│ Phase 2: Domain Detection ──► Analyze request & detect domain   │
│ Phase 3: Requirements ──► AskUserQuestion (domain-aware)        │
│ Phase 4: Parallel Research ──► 3-5 Explore agents              │
│ Phase 5: Format Selection ──► Intelligent format decision       │
│ Phase 6: Generation ──► Domain expert agent                     │
│ Phase 7: Validation ──► Auto-test & install                    │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 1: Self-Upgrade

Always start by updating knowledge:

```
Task(
  subagent_type='claude-code-guide',
  prompt='Get latest on: Skills format, Slash Commands, Subagents, Hooks, MCP integration, composite workflows',
  description='Upgrade Claude Code knowledge',
  model='sonnet'
)
```

Update `references/latest_features.md` with new information.

## Phase 2: Domain Detection

Analyze user request to detect domain and complexity:

### Domain Classification

| Domain            | Trigger Keywords                              | Expert Focus                          |
| ----------------- | --------------------------------------------- | ------------------------------------- |
| **DevOps**        | deploy, CI/CD, kubernetes, docker, terraform  | Infrastructure, pipelines, containers |
| **Security**      | scan, audit, vulnerability, compliance, OWASP | Security testing, policy enforcement  |
| **WebDev**        | frontend, react, api, component, styling      | Web frameworks, UI/UX patterns        |
| **DataOps**       | data, ETL, pipeline, analytics, database      | Data processing, transformation       |
| **Documentation** | docs, readme, api-docs, changelog             | Technical writing, generation         |
| **Testing**       | test, e2e, unit, integration, coverage        | Test automation, quality              |
| **General**       | (default)                                     | Universal patterns                    |

### Complexity Levels

| Level | Indicators                  | Agent Count |
| ----- | --------------------------- | ----------- |
| 1-2   | Simple task, single format  | 1-2 agents  |
| 3     | Standard workflow           | 3 agents    |
| 4-5   | Complex, composite workflow | 4-5 agents  |

## Phase 3: Requirements Gathering

Use AskUserQuestion with domain-aware questions:

```
AskUserQuestion(questions=[
  {
    "question": "What domain does this workflow belong to?",
    "header": "Domain",
    "options": [
      {"label": "DevOps", "description": "CI/CD, deployment, infrastructure"},
      {"label": "Security", "description": "Scanning, auditing, compliance"},
      {"label": "WebDev", "description": "Frontend, API, components"},
      {"label": "DataOps", "description": "ETL, analytics, databases"},
      {"label": "Documentation", "description": "Docs generation, changelogs"},
      {"label": "Testing", "description": "Test automation, coverage"}
    ],
    "multiSelect": false
  },
  {
    "question": "What output format(s) do you need?",
    "header": "Format",
    "options": [
      {"label": "Skill only (Recommended)", "description": "Auto-triggered by context"},
      {"label": "Command only", "description": "Explicit /command invocation"},
      {"label": "Composite (skill+command+hook)", "description": "Full automation stack"}
    ],
    "multiSelect": false
  },
  {
    "question": "What complexity level?",
    "header": "Depth",
    "options": [
      {"label": "Level 3 (Recommended)", "description": "Standard workflow, 3 agents"},
      {"label": "Level 1-2", "description": "Simple task, 1-2 agents"},
      {"label": "Level 4-5", "description": "Complex composite, 4-5 agents"}
    ],
    "multiSelect": false
  }
])
```

### Domain-Specific Questions

After domain selection, ask domain-specific questions:

**DevOps:**

- Target platforms (AWS, GCP, Azure, K8s)?
- CI/CD tool preference (GitHub Actions, GitLab CI)?

**Security:**

- Scan types (SAST, DAST, SCA, container)?
- Compliance frameworks (OWASP, SOC2, PCI)?

**WebDev:**

- Framework (React, Vue, Next.js, Svelte)?
- Styling (Tailwind, CSS Modules, styled-components)?

**Testing:**

- Test types (unit, integration, e2e)?
- Framework preference (Jest, Vitest, Playwright)?

## Phase 4: Parallel Research

Launch domain-specific research agents:

```
# Research Agent 1: Best Practices
Task(
  subagent_type='Explore',
  prompt='Research {domain} best practices 2025. Find: patterns, anti-patterns, industry standards.',
  description='Research best practices',
  model='haiku',
  run_in_background=true
)

# Research Agent 2: Tools & Libraries
Task(
  subagent_type='Explore',
  prompt='Research {domain} automation tools and libraries. Find: CLI tools, npm/pip packages, MCP servers.',
  description='Research tools',
  model='haiku',
  run_in_background=true
)

# Research Agent 3: Existing Solutions
Task(
  subagent_type='Explore',
  prompt='Research existing Claude Code skills for {domain}. Find: similar implementations, reusable patterns.',
  description='Research existing solutions',
  model='haiku',
  run_in_background=true
)
```

### WebSearch for Domain Expertise

```
WebSearch(query='{domain} workflow automation 2025 best practices')
WebSearch(query='{domain} Claude Code skill example')
WebSearch(query='{task} CLI tools npm pip packages')
```

Synthesize findings into actionable recommendations.

## Phase 5: Format Selection

Intelligent format decision based on requirements:

### Decision Matrix

```
┌─────────────────────────────────────────────────────────┐
│ Is it triggered by explicit /command?                   │
│   YES → Slash Command                                   │
│   NO ↓                                                  │
├─────────────────────────────────────────────────────────┤
│ Should it auto-activate based on context?               │
│   YES → Skill                                           │
│   NO ↓                                                  │
├─────────────────────────────────────────────────────────┤
│ Does it need specialized AI persona?                    │
│   YES → Subagent                                        │
│   NO ↓                                                  │
├─────────────────────────────────────────────────────────┤
│ Should it react to tool/event?                          │
│   YES → Hook                                            │
│   NO → Skill (default)                                  │
├─────────────────────────────────────────────────────────┤
│ Complex automation with multiple entry points?          │
│   YES → Composite (skill + command + hook)              │
└─────────────────────────────────────────────────────────┘
```

### Composite Workflow Pattern

For complex automation, generate multiple formats:

```
workflow-name/
├── skills/
│   └── workflow-name/
│       ├── SKILL.md           # Main orchestration
│       ├── scripts/           # Automation scripts
│       └── references/        # Documentation
├── commands/
│   └── quick-run.md           # Quick trigger command
└── hooks/
    └── hooks.json             # Event reactions
```

## Phase 6: Generation

### Domain Expert Agents

Launch domain-specific generation agent:

```
Task(
  subagent_type='general-purpose',
  prompt='''Generate {domain} workflow with:
    - Requirements: {gathered_requirements}
    - Research findings: {research_results}
    - Format: {selected_format}
    - Best practices: {domain_best_practices}

    Create complete files following templates in references/domain_templates.md
  ''',
  description='Generate {domain} workflow',
  model='sonnet'
)
```

### File Generation Order

1. **scripts/** - Executable automation code
2. **references/** - Documentation and context
3. **assets/** - Templates and output formats
4. **SKILL.md** - Main instructions with frontmatter
5. **commands/** - Slash commands (if composite)
6. **hooks.json** - Hook configuration (if composite)

### Domain-Specific Templates

Use templates from `references/domain_templates.md`:

- DevOps: CI/CD pipelines, deployment scripts
- Security: Scan configurations, policy definitions
- WebDev: Component generators, API scaffolding
- DataOps: ETL scripts, data validators
- Documentation: Doc generators, changelog builders
- Testing: Test runners, coverage reporters

## Phase 7: Validation & Installation

### Automated Validation

```bash
# Validate skill structure
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py ./workflow-name

# Test scripts (if any)
python3 -m pytest ./workflow-name/scripts/ 2>/dev/null || true

# Validate hook syntax (if composite)
python3 -c "import json; json.load(open('./workflow-name/hooks/hooks.json'))" 2>/dev/null || true
```

### Installation

```bash
# Package skill
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./workflow-name .

# Install skill
unzip -o workflow-name.zip -d ~/.claude/skills/
chmod +x ~/.claude/skills/workflow-name/scripts/*.py 2>/dev/null || true

# Install command (if composite)
cp ./workflow-name/commands/*.md ~/.claude/commands/ 2>/dev/null || true

# Merge hooks (if composite)
# Manual merge into ~/.claude/settings.json
```

### Post-Installation Report

```markdown
## ✅ Workflow Created Successfully

### Generated Files

| File             | Type    | Purpose       |
| ---------------- | ------- | ------------- |
| `SKILL.md`       | Skill   | Main workflow |
| `scripts/run.py` | Script  | Automation    |
| `/quick-run.md`  | Command | Quick trigger |

### Installation Status

- [x] Skill installed to ~/.claude/skills/
- [x] Command installed to ~/.claude/commands/
- [ ] Hooks require manual merge

### Usage

- Auto-trigger: {trigger_phrases}
- Command: `/quick-run [args]`
```

## Domain Templates

See `references/domain_templates.md` for complete templates:

- [DevOps Templates](references/domain_templates.md#devops)
- [Security Templates](references/domain_templates.md#security)
- [WebDev Templates](references/domain_templates.md#webdev)
- [DataOps Templates](references/domain_templates.md#dataops)
- [Documentation Templates](references/domain_templates.md#documentation)
- [Testing Templates](references/domain_templates.md#testing)

## Trigger Phrases

- "워크플로우 만들어줘" / "create a workflow"
- "새 스킬 만들어" / "make a new skill"
- "자동화하고 싶어" / "automate this"
- "명령어 추가해줘" / "add a command"
- "{domain} workflow" / "{도메인} 워크플로우"
- "composite workflow" / "복합 워크플로우"

## Resources

- [Domain Templates](references/domain_templates.md) - Domain-specific templates
- [Format Examples](references/format_examples.md) - Output format examples
- [Latest Features](references/latest_features.md) - Claude Code capabilities
- [Agent Prompts](references/agent_prompts.md) - Expert agent prompts
