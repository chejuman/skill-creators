---
name: multi-agent-skill-creator
description: Self-upgradable multi-agent skill generator. Creates production-ready skills through 4 phases - self-upgrade (learn latest Claude Code features), research (real-time web search for domain knowledge), requirements gathering (AskUserQuestion for user refinement), and generation (produce complete multi-agent skill). Use when building any agent-based skill. Triggers on "create multi-agent skill", "build agent skill", "generate parallel workflow", or domain requests like "make a research agent".
---

# Multi-Agent Skill Creator

Self-upgradable skill generator that produces multi-agent skills through intelligent workflow.

## Core Workflow (4 Phases)

```
Phase 1: Self-Upgrade ──► Learn latest Claude Code features
    │
Phase 2: Research ──► WebSearch for domain best practices
    │
Phase 3: Requirements ──► AskUserQuestion to refine specs
    │
Phase 4: Generate ──► Create complete multi-agent skill
```

## Phase 1: Self-Upgrade

Before creating any skill, upgrade knowledge on latest Claude Code features:

```
Task(
  subagent_type='claude-code-guide',
  prompt='Get latest info on: Agent Skills format, Task tool parameters,
         subagent types, parallel execution patterns, model options',
  description='Upgrade Claude Code knowledge'
)
```

**Topics to refresh:**
- SKILL.md format and frontmatter
- Task tool: subagent_type, model, run_in_background
- Built-in agents: Plan, Explore, general-purpose
- Parallel execution rules

## Phase 2: Domain Research

Perform real-time web search to gather domain-specific knowledge:

```
WebSearch(query='{domain} best practices 2025')
WebSearch(query='{domain} multi-agent architecture patterns')
WebSearch(query='{domain} automation workflow examples')
```

**Research goals:**
- Industry best practices for the domain
- Common agent patterns used in similar systems
- Tool/API integrations relevant to domain
- Quality metrics and success criteria

**Research Agent (parallel):**
```
Task(subagent_type='Explore', prompt='Research {domain} patterns...', model='haiku')
Task(subagent_type='Explore', prompt='Research {domain} tools...', model='haiku')
Task(subagent_type='Explore', prompt='Research {domain} metrics...', model='haiku')
```

## Phase 3: Requirements Gathering

Use AskUserQuestion to refine and validate requirements:

### Question 1: Skill Purpose
```
AskUserQuestion(questions=[{
  "question": "What is the primary purpose of this multi-agent skill?",
  "header": "Purpose",
  "options": [
    {"label": "Research/Analysis", "description": "Gather and analyze information"},
    {"label": "Code/Development", "description": "Code review, testing, generation"},
    {"label": "Security/Audit", "description": "Security scanning, compliance"},
    {"label": "Content/Docs", "description": "Documentation, content generation"}
  ],
  "multiSelect": False
}])
```

### Question 2: Worker Agents
```
AskUserQuestion(questions=[{
  "question": "Which worker agents should be included?",
  "header": "Workers",
  "options": [
    {"label": "Researcher", "description": "Web search and data gathering"},
    {"label": "Analyzer", "description": "Data analysis and insights"},
    {"label": "Validator", "description": "Fact-checking and verification"},
    {"label": "Reporter", "description": "Report and summary generation"}
  ],
  "multiSelect": True
}])
```

### Question 3: Depth Level
```
AskUserQuestion(questions=[{
  "question": "What default depth level for the skill?",
  "header": "Depth",
  "options": [
    {"label": "Level 3 (Recommended)", "description": "3 workers, detailed analysis"},
    {"label": "Level 1-2", "description": "Quick checks, 1-2 workers"},
    {"label": "Level 4-5", "description": "Deep audit, 4-5+ workers"}
  ],
  "multiSelect": False
}])
```

### Question 4: Output Format
```
AskUserQuestion(questions=[{
  "question": "What output formats should be supported?",
  "header": "Output",
  "options": [
    {"label": "Markdown + HTML", "description": "Reports with visual styling"},
    {"label": "JSON", "description": "Structured data output"},
    {"label": "Both", "description": "All formats supported"}
  ],
  "multiSelect": False
}])
```

## Phase 4: Skill Generation

Generate the complete multi-agent skill based on gathered requirements:

### 4.1 Create Skill Structure
```
skill-name/
├── SKILL.md              # Main documentation
├── scripts/
│   ├── orchestrator.py   # Execution engine
│   └── md_to_html.py     # Report converter
├── references/
│   └── agent_prompts.md  # Agent templates
└── assets/
    └── report_template.md
```

### 4.2 Generate SKILL.md

Use template from [assets/skill_template.md](assets/skill_template.md) with:
- Domain-specific description
- Configured worker agents
- Appropriate depth levels
- Output format support

### 4.3 Generate Agent Prompts

For each worker identified in Phase 3:
```python
python3 scripts/agent_generator.py \
  --domain "{domain}" \
  --agents "{selected_workers}" \
  --output ./references/
```

### 4.4 Validate & Install

```bash
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py ./skill-name
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./skill-name .
unzip -o skill-name.zip -d ~/.claude/skills/
```

## Generated Skill Architecture

Output skills follow this pattern:

```
Orchestrator
    ├─► Planning Agent ──► Scope decomposition
    ├─► Worker Agents (PARALLEL)
    │       ├── Worker #1: {focus_1}
    │       ├── Worker #2: {focus_2}
    │       └── Worker #3: {focus_3}
    ├─► Analysis Agent ──► Result synthesis
    ├─► Synthesis Agent ──► Report generation
    └─► Visualization Agent ──► HTML output
```

## Complete Workflow Example

**User:** "멀티 에이전트 기반 코드 리뷰 스킬을 만들어줘"

**Phase 1 - Self-Upgrade:**
```
Task(subagent_type='claude-code-guide', prompt='Latest skill format...', description='Upgrade')
```

**Phase 2 - Research:**
```
WebSearch(query='code review multi-agent automation 2025')
WebSearch(query='static analysis best practices')
```

**Phase 3 - Requirements:**
```
AskUserQuestion(questions=[
  {"question": "Which review aspects to cover?", "header": "Focus", ...},
  {"question": "Include auto-fix capability?", "header": "Auto-fix", ...}
])
```

**Phase 4 - Generate:**
- Create `code-reviewer-v2/SKILL.md`
- Generate worker prompts for security, performance, style, logic
- Install to `~/.claude/skills/`

## Resources

- [Agent Patterns](references/agent_patterns.md) - Multi-agent patterns
- [Parallel Execution](references/parallel_execution.md) - Execution rules
- [Requirements Questions](references/requirements_questions.md) - Question templates
- [Skill Template](assets/skill_template.md) - SKILL.md template

## Trigger Phrases

- "create multi-agent skill" / "멀티 에이전트 스킬 생성"
- "build agent-based skill" / "에이전트 기반 스킬 만들어줘"
- "generate parallel workflow" / "병렬 워크플로우 생성"
- "{domain} agent skill" / "{도메인} 에이전트 스킬"
