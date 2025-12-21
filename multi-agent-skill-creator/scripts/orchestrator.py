#!/usr/bin/env python3
"""
Multi-Agent Skill Creator Orchestrator

Self-upgradable skill generator with 4-phase workflow:
1. Self-Upgrade: Learn latest Claude Code features
2. Research: Web search for domain best practices
3. Requirements: AskUserQuestion for user refinement
4. Generate: Create complete multi-agent skill

Usage:
    python orchestrator.py generate --domain "code review" --name "code-reviewer-v2"
    python orchestrator.py workflow --domain "security audit"
    python orchestrator.py questions --domain "research"
"""

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class AgentConfig:
    """Configuration for a single agent."""
    name: str
    role: str
    focus: str
    subagent_type: str = "general-purpose"
    model: str = "haiku"
    tools: List[str] = field(default_factory=lambda: ["Read", "Grep", "Glob"])


@dataclass
class SkillConfig:
    """Configuration for generated skill."""
    name: str
    domain: str
    description: str = ""
    level: int = 3
    workers: List[AgentConfig] = field(default_factory=list)
    output_formats: List[str] = field(default_factory=lambda: ["markdown", "html"])

    @property
    def worker_count(self) -> int:
        return max(1, min(self.level, 5))


def generate_workflow_instructions(domain: str) -> str:
    """Generate 4-phase workflow instructions for Claude."""
    return f'''
## Multi-Agent Skill Creator: 4-Phase Workflow

**Domain:** {domain}

### Phase 1: Self-Upgrade

Upgrade knowledge on latest Claude Code features:

```
Task(
  subagent_type='claude-code-guide',
  prompt='Get latest info on: Agent Skills SKILL.md format, Task tool parameters (subagent_type, model, run_in_background), built-in agents (Plan, Explore, general-purpose), parallel execution patterns for multi-agent systems',
  description='Upgrade Claude Code knowledge'
)
```

### Phase 2: Domain Research

Perform real-time web search for domain best practices:

```
WebSearch(query='{domain} best practices 2025')
WebSearch(query='{domain} multi-agent automation patterns')
WebSearch(query='{domain} workflow tools APIs')
```

Then spawn research agents in PARALLEL:
```
Task(subagent_type='Explore', prompt='Research {domain} industry patterns...', model='haiku')
Task(subagent_type='Explore', prompt='Research {domain} tool integrations...', model='haiku')
Task(subagent_type='Explore', prompt='Research {domain} quality metrics...', model='haiku')
```

### Phase 3: Requirements Gathering

Use AskUserQuestion to refine requirements:

```python
AskUserQuestion(questions=[
  {{
    "question": "What is the primary purpose of this {domain} skill?",
    "header": "Purpose",
    "options": [
      {{"label": "Research/Analysis", "description": "Gather and analyze information"}},
      {{"label": "Code/Development", "description": "Code review, testing, generation"}},
      {{"label": "Security/Audit", "description": "Scanning, compliance, threats"}},
      {{"label": "Content/Docs", "description": "Documentation, content generation"}}
    ],
    "multiSelect": False
  }},
  {{
    "question": "Which worker agents should be included?",
    "header": "Workers",
    "options": [
      {{"label": "Researcher", "description": "Web search, data gathering"}},
      {{"label": "Analyzer", "description": "Data analysis, insights"}},
      {{"label": "Validator", "description": "Fact-checking, verification"}},
      {{"label": "Reporter", "description": "Report generation"}}
    ],
    "multiSelect": True
  }}
])

AskUserQuestion(questions=[
  {{
    "question": "Default depth level?",
    "header": "Depth",
    "options": [
      {{"label": "Level 3 (Recommended)", "description": "3 workers, detailed"}},
      {{"label": "Level 1-2", "description": "Quick, 1-2 workers"}},
      {{"label": "Level 4-5", "description": "Deep, 4-5+ workers"}}
    ],
    "multiSelect": False
  }},
  {{
    "question": "Output formats?",
    "header": "Output",
    "options": [
      {{"label": "Markdown + HTML (Recommended)", "description": "Rich reports"}},
      {{"label": "JSON only", "description": "Structured data"}},
      {{"label": "All formats", "description": "MD, HTML, JSON"}}
    ],
    "multiSelect": False
  }}
])
```

### Phase 4: Skill Generation

Based on gathered requirements, generate the skill:

1. Create skill structure using orchestrator.py
2. Generate agent prompts using agent_generator.py
3. Validate with quick_validate.py
4. Package with package_skill.py
5. Install to ~/.claude/skills/

```bash
python3 scripts/orchestrator.py generate \\
  --domain "{domain}" \\
  --name "<skill-name>" \\
  --workers "<selected-workers>" \\
  --level <selected-level> \\
  --output ./
```
'''


def generate_questions_json(domain: str) -> dict:
    """Generate AskUserQuestion JSON for a domain."""
    return {
        "domain": domain,
        "question_batches": [
            {
                "batch": 1,
                "questions": [
                    {
                        "question": f"What is the primary purpose of this {domain} skill?",
                        "header": "Purpose",
                        "options": [
                            {"label": "Research/Analysis", "description": "Gather and analyze information"},
                            {"label": "Code/Development", "description": "Code review, testing, generation"},
                            {"label": "Security/Audit", "description": "Scanning, compliance, threats"},
                            {"label": "Content/Docs", "description": "Documentation, content generation"}
                        ],
                        "multiSelect": False
                    },
                    {
                        "question": "Which worker agents should be included?",
                        "header": "Workers",
                        "options": [
                            {"label": "Researcher", "description": "Web search, data gathering"},
                            {"label": "Analyzer", "description": "Data analysis, insights"},
                            {"label": "Validator", "description": "Fact-checking, verification"},
                            {"label": "Reporter", "description": "Report generation"}
                        ],
                        "multiSelect": True
                    }
                ]
            },
            {
                "batch": 2,
                "questions": [
                    {
                        "question": "Default depth level?",
                        "header": "Depth",
                        "options": [
                            {"label": "Level 3 (Recommended)", "description": "3 workers, detailed"},
                            {"label": "Level 1-2", "description": "Quick, 1-2 workers"},
                            {"label": "Level 4-5", "description": "Deep, 4-5+ workers"}
                        ],
                        "multiSelect": False
                    },
                    {
                        "question": "Output formats?",
                        "header": "Output",
                        "options": [
                            {"label": "Markdown + HTML (Recommended)", "description": "Rich reports"},
                            {"label": "JSON only", "description": "Structured data"},
                            {"label": "All formats", "description": "MD, HTML, JSON"}
                        ],
                        "multiSelect": False
                    }
                ]
            }
        ]
    }


def generate_skill_md(config: SkillConfig) -> str:
    """Generate SKILL.md content."""
    workers_arch = "\n".join(
        [f"    │       ├── Worker #{i+1}: {w.focus}" for i, w in enumerate(config.workers)]
    )
    worker_tasks = "\n".join(
        [f"Task(subagent_type='general-purpose', prompt='{w.name}: {w.focus}...', model='haiku')"
         for w in config.workers]
    )

    return f'''---
name: {config.name}
description: {config.description or f"Multi-agent {config.domain} system with parallel execution and depth levels 1-5. Use for {config.domain} tasks."}
---

# {config.name.replace("-", " ").title()}

Hierarchical multi-agent {config.domain} system.

## Architecture

```
Orchestrator
    ├─► Planning Agent ──► Scope decomposition
    ├─► Worker Agents (PARALLEL)
{workers_arch}
    ├─► Analysis Agent ──► Result synthesis
    ├─► Synthesis Agent ──► Report generation
    └─► Visualization Agent ──► HTML output
```

## Depth Levels

| Level | Workers | Analysis | Report |
|-------|---------|----------|--------|
| 1 | 1 | Inline | Basic |
| 2 | 2 | 1 agent | Standard |
| 3 | 3 | 1 agent | Detailed |
| 4 | 4 | 1 agent | Expert |
| 5 | 5+ | 1 agent | Full |

## Execution

### Phase 1: Planning
```
Task(subagent_type='Plan', prompt='Analyze {config.domain} scope...', description='Plan')
```

### Phase 2: Workers (PARALLEL)
```
{worker_tasks}
```

### Phase 3-5: Analysis → Synthesis → Visualization
Sequential after workers complete.

## Resources
- [Agent Prompts](references/agent_prompts.md)
'''


def generate_agent_prompts(config: SkillConfig) -> str:
    """Generate agent_prompts.md reference."""
    worker_prompts = "\n\n".join([f'''## {w.name.title()} Agent

```
You are a {w.name} agent for {config.domain}.

FOCUS: {w.focus}

Instructions:
1. Analyze assigned subtask
2. Execute domain operations
3. Return JSON findings

Output:
{{"agent": "{w.name}", "findings": [...], "summary": "...", "gaps": [...]}}
```''' for w in config.workers])

    return f'''# Agent Prompts for {config.name}

## Planning Agent
```
Analyze {config.domain} scope. Decompose into {len(config.workers)} subtasks.
Output: {{"subtasks": [...], "worker_count": {len(config.workers)}}}
```

{worker_prompts}

## Analysis Agent
```
Synthesize all findings. Score by priority.
Output: {{"total": 0, "high_priority": [...], "insights": [...], "quality": 0.85}}
```
'''


def create_skill_structure(config: SkillConfig, output_path: str) -> Path:
    """Create complete skill directory structure."""
    base = Path(output_path) / config.name
    (base / "scripts").mkdir(parents=True, exist_ok=True)
    (base / "references").mkdir(exist_ok=True)
    (base / "assets").mkdir(exist_ok=True)

    (base / "SKILL.md").write_text(generate_skill_md(config))
    (base / "references" / "agent_prompts.md").write_text(generate_agent_prompts(config))

    print(f"Created skill: {base}")
    return base


def parse_workers(workers_str: str, domain: str) -> List[AgentConfig]:
    """Parse worker specification string."""
    if not workers_str:
        return [AgentConfig(name=f"worker-{i+1}", role="worker", focus=f"Subtask {i+1}")
                for i in range(3)]
    return [AgentConfig(name=w.strip(), role="worker", focus=f"{w.strip()} for {domain}")
            for w in workers_str.split(",")]


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Skill Creator (4-Phase)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate command
    gen = subparsers.add_parser("generate", help="Generate a new skill")
    gen.add_argument("--domain", "-d", required=True, help="Domain")
    gen.add_argument("--name", "-n", required=True, help="Skill name")
    gen.add_argument("--workers", "-w", default="", help="Workers (comma-separated)")
    gen.add_argument("--level", "-l", type=int, default=3, help="Depth level")
    gen.add_argument("--output", "-o", default=".", help="Output dir")

    # Workflow command
    wf = subparsers.add_parser("workflow", help="Show 4-phase workflow")
    wf.add_argument("--domain", "-d", required=True, help="Domain")

    # Questions command
    qs = subparsers.add_parser("questions", help="Generate AskUserQuestion JSON")
    qs.add_argument("--domain", "-d", required=True, help="Domain")
    qs.add_argument("--output", "-o", help="Output file")

    args = parser.parse_args()

    if args.command == "generate":
        workers = parse_workers(args.workers, args.domain)
        config = SkillConfig(name=args.name, domain=args.domain, level=args.level, workers=workers)
        create_skill_structure(config, args.output)

    elif args.command == "workflow":
        print(generate_workflow_instructions(args.domain))

    elif args.command == "questions":
        questions = generate_questions_json(args.domain)
        if args.output:
            Path(args.output).write_text(json.dumps(questions, indent=2))
            print(f"Saved: {args.output}")
        else:
            print(json.dumps(questions, indent=2))


if __name__ == "__main__":
    main()
