#!/usr/bin/env python3
"""
Agent Prompt Generator

Generates agent prompt templates for any domain.

Usage:
    python agent_generator.py --domain "security audit" --output ./prompts/
    python agent_generator.py --domain "code review" --agents "security,perf,style"
"""

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class AgentPrompt:
    """Agent prompt configuration."""
    name: str
    role: str
    focus: str
    tools: List[str]
    model: str
    output_schema: dict


AGENT_TEMPLATES = {
    "planning": {
        "role": "Planning Agent",
        "tools": ["Glob", "Grep", "Read"],
        "model": "sonnet",
        "prompt": '''You are a Planning Agent for {domain}.

TASK: {task}

Instructions:
1. Analyze the scope and requirements
2. Decompose into {worker_count} parallel, non-overlapping subtasks
3. Define expected outputs for each subtask

Output JSON:
{{
  "domain": "{domain}",
  "subtasks": [
    {{"id": 1, "focus": "...", "query": "...", "expected_output": "..."}}
  ],
  "worker_count": {worker_count},
  "quality_criteria": "..."
}}'''
    },
    "worker": {
        "role": "Worker Agent",
        "tools": ["Read", "Grep", "Glob", "WebSearch"],
        "model": "haiku",
        "prompt": '''You are a {name} Worker Agent for {domain}.

SUBTASK ID: {subtask_id}
FOCUS: {focus}

Instructions:
1. Execute the assigned subtask
2. Collect findings with severity/priority
3. Return structured results

Output JSON:
{{
  "subtask_id": {subtask_id},
  "agent": "{name}",
  "findings": [
    {{"id": "...", "severity": "high|medium|low", "score": 0.85, "details": "..."}}
  ],
  "summary": "...",
  "gaps": ["..."]
}}'''
    },
    "analysis": {
        "role": "Analysis Agent",
        "tools": ["Read", "Grep"],
        "model": "sonnet",
        "prompt": '''You are an Analysis Agent for {domain}.

WORKER RESULTS:
{results}

Instructions:
1. Consolidate findings from all workers
2. Score and prioritize by importance
3. Identify contradictions and gaps
4. Extract key insights

Output JSON:
{{
  "total_findings": 0,
  "high_priority": [...],
  "medium_priority": [...],
  "low_priority": [...],
  "contradictions": [...],
  "gaps": [...],
  "key_insights": [...],
  "quality_score": 0.85
}}'''
    },
    "synthesis": {
        "role": "Synthesis Agent",
        "tools": ["Read", "Write"],
        "model": "sonnet",
        "prompt": '''You are a Synthesis Agent for {domain}.

ANALYSIS RESULTS:
{analysis}

REPORT LEVEL: {level}

Generate a Markdown report with:
1. Executive Summary
2. Key Findings (high priority)
3. Supporting Information
4. Gaps and Limitations
5. Recommendations
6. Methodology
7. Sources'''
    },
    "visualization": {
        "role": "Visualization Agent",
        "tools": ["Bash", "Read", "Write"],
        "model": "haiku",
        "prompt": '''You are a Visualization Agent.

INPUT: {markdown_path}
OUTPUT: {html_path}

Convert the markdown report to styled HTML:
1. Read the markdown file
2. Convert using md_to_html.py or inline conversion
3. Include responsive sidebar, styled tables, syntax highlighting
4. Return the output file path'''
    }
}


def generate_domain_prompts(domain: str, agents: List[str], worker_count: int = 3) -> dict:
    """Generate all prompts for a domain."""
    prompts = {
        "domain": domain,
        "agents": {}
    }

    # Planning agent
    prompts["agents"]["planning"] = AGENT_TEMPLATES["planning"]["prompt"].format(
        domain=domain,
        task="{task}",
        worker_count=worker_count
    )

    # Worker agents
    for i, agent_name in enumerate(agents):
        prompts["agents"][f"worker_{agent_name}"] = AGENT_TEMPLATES["worker"]["prompt"].format(
            domain=domain,
            name=agent_name,
            subtask_id="{subtask_id}",
            focus=f"{agent_name} analysis"
        )

    # Analysis agent
    prompts["agents"]["analysis"] = AGENT_TEMPLATES["analysis"]["prompt"].format(
        domain=domain,
        results="{results}"
    )

    # Synthesis agent
    prompts["agents"]["synthesis"] = AGENT_TEMPLATES["synthesis"]["prompt"].format(
        domain=domain,
        analysis="{analysis}",
        level="{level}"
    )

    # Visualization agent
    prompts["agents"]["visualization"] = AGENT_TEMPLATES["visualization"]["prompt"].format(
        markdown_path="{markdown_path}",
        html_path="{html_path}"
    )

    return prompts


def generate_markdown_reference(prompts: dict) -> str:
    """Generate markdown reference file."""
    lines = [f"# Agent Prompts for {prompts['domain']}\n"]

    for agent_name, prompt in prompts["agents"].items():
        lines.append(f"\n## {agent_name.replace('_', ' ').title()}\n")
        lines.append(f"```\n{prompt}\n```\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Agent Prompt Generator")
    parser.add_argument("--domain", "-d", required=True, help="Domain name")
    parser.add_argument("--agents", "-a", default="worker-1,worker-2,worker-3",
                        help="Comma-separated worker agent names")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--format", "-f", choices=["json", "md", "both"], default="both")

    args = parser.parse_args()

    agents = [a.strip() for a in args.agents.split(",")]
    prompts = generate_domain_prompts(args.domain, agents, len(agents))

    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    if args.format in ["json", "both"]:
        json_file = output_path / f"{args.domain.replace(' ', '_')}_prompts.json"
        json_file.write_text(json.dumps(prompts, indent=2))
        print(f"Created: {json_file}")

    if args.format in ["md", "both"]:
        md_file = output_path / f"{args.domain.replace(' ', '_')}_prompts.md"
        md_file.write_text(generate_markdown_reference(prompts))
        print(f"Created: {md_file}")


if __name__ == "__main__":
    main()
