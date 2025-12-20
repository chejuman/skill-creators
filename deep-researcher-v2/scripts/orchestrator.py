#!/usr/bin/env python3
"""
Deep Researcher v2.0 Orchestrator

Programmatic interface for the multi-agent research system.
Can be used standalone or as a reference for Claude Code skill execution.

Usage:
    python orchestrator.py "research query" --level 3 --output report.md
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ResearchConfig:
    """Configuration for research execution."""
    level: int = 3
    max_sources_per_agent: int = 5
    parallel_agents: int = 3
    output_format: str = "markdown"
    save_raw_outputs: bool = False

    @property
    def subtask_count(self) -> int:
        """Number of parallel research subtasks based on level."""
        return max(1, min(self.level, 5))

    @property
    def min_sources(self) -> int:
        """Minimum sources required for the level."""
        return {1: 3, 2: 5, 3: 10, 4: 15, 5: 25}.get(self.level, 10)

    @property
    def min_high_relevance(self) -> int:
        """Minimum high-relevance findings required."""
        return {1: 1, 2: 2, 3: 3, 4: 5, 5: 8}.get(self.level, 3)


@dataclass
class Subtask:
    """Research subtask definition."""
    id: int
    focus: str
    search_query: str
    source_types: list = field(default_factory=lambda: ["news", "official"])
    expected_findings: str = ""


@dataclass
class Source:
    """Research source with findings."""
    url: str
    title: str
    key_findings: list
    relevance_score: float
    source_type: str = "unknown"
    date: Optional[str] = None
    credibility: str = "medium"


@dataclass
class ResearchResult:
    """Result from a Research Agent."""
    subtask_id: int
    focus: str
    sources: list
    summary: str
    gaps: list = field(default_factory=list)


@dataclass
class AnalysisResult:
    """Result from the Analysis Agent."""
    high_relevance: list
    medium_relevance: list
    low_relevance: list
    contradictions: list
    gaps: list
    key_insights: list
    data_quality_score: float
    coverage_score: float


def generate_planning_prompt(query: str, config: ResearchConfig) -> str:
    """Generate prompt for Planning Agent."""
    return f"""You are a Research Planning Agent. Decompose this query into parallel subtasks.

RESEARCH QUERY: {query}
RESEARCH LEVEL: {config.level}
SUBTASK COUNT: {config.subtask_count}

Decompose into {config.subtask_count} independent, parallelizable subtasks.
Each subtask should cover a distinct aspect of the research.

Output JSON format:
{{
  "original_query": "{query}",
  "level": {config.level},
  "subtasks": [
    {{
      "id": 1,
      "focus": "Specific aspect",
      "search_query": "Optimized query with 2025 context",
      "source_types": ["news", "official", "academic"],
      "expected_findings": "What to discover"
    }}
  ],
  "search_strategy": "Overall approach",
  "quality_criteria": "What makes good findings"
}}"""


def generate_research_prompt(subtask: Subtask) -> str:
    """Generate prompt for Research Agent."""
    return f"""You are a Research Agent. Execute focused web research.

SUBTASK ID: {subtask.id}
FOCUS: {subtask.focus}
SEARCH QUERY: {subtask.search_query}

Instructions:
1. Use WebSearch with the query
2. Select top 3-5 relevant sources
3. Use WebFetch to extract key information
4. Score each source's relevance (0.0-1.0)

Output JSON:
{{
  "subtask_id": {subtask.id},
  "focus": "{subtask.focus}",
  "sources": [
    {{
      "url": "...",
      "title": "...",
      "key_findings": ["..."],
      "relevance_score": 0.85
    }}
  ],
  "summary": "One paragraph summary",
  "gaps": ["What couldn't be found"]
}}"""


def generate_analysis_prompt(results: list) -> str:
    """Generate prompt for Analysis Agent."""
    results_json = json.dumps([r.__dict__ for r in results], indent=2, default=str)
    return f"""You are an Analysis Agent. Synthesize research findings.

RESEARCH FINDINGS:
{results_json}

Tasks:
1. Consolidate findings from all agents
2. Score relevance with cross-reference validation
3. Identify contradictions
4. Detect information gaps
5. Extract key insights

Output JSON with:
- high_relevance_findings (score >= 0.8)
- medium_relevance_findings (0.5 <= score < 0.8)
- contradictions
- gaps
- key_insights
- data_quality_score
- coverage_score"""


def generate_synthesis_prompt(analysis: AnalysisResult, query: str, config: ResearchConfig) -> str:
    """Generate prompt for Synthesis Agent."""
    return f"""You are a Synthesis Agent. Generate a comprehensive report.

QUERY: {query}
LEVEL: {config.level}
ANALYSIS: {json.dumps(analysis.__dict__, indent=2, default=str)}

Generate a Markdown report with:
- Executive Summary
- Key Findings (high relevance)
- Supporting Information (medium relevance)
- Contradictions & Conflicts
- Research Gaps
- Recommendations
- Methodology
- Full Source List"""


def generate_claude_code_instructions(query: str, config: ResearchConfig) -> str:
    """
    Generate Claude Code instructions for multi-agent execution.

    This is the key output - instructions for Claude Code to execute
    the multi-agent research using Task tool.
    """
    instructions = f"""
## Deep Research Execution Instructions

**Query:** {query}
**Level:** {config.level}
**Subtasks:** {config.subtask_count}
**Min Sources:** {config.min_sources}

### Step 1: Planning (Sequential)

```
Task(
  subagent_type='Plan',
  prompt='''Decompose this research query into {config.subtask_count} parallel subtasks:

Query: "{query}"
Level: {config.level}

Output JSON with subtasks array, each with: id, focus, search_query, source_types.
''',
  description='Plan research strategy'
)
```

### Step 2: Research (PARALLEL - Single Message)

After receiving planning output, spawn ALL research agents in ONE message:

```python
# Include ALL these Task calls in a SINGLE response message
{"Task calls": [
  """

    for i in range(1, config.subtask_count + 1):
        instructions += f"""  Task(subagent_type='Explore', prompt='Research subtask {i}: {{subtask_{i}_focus}}. Use WebSearch and WebFetch.', description='Research subtask {i}'),
"""

    instructions += f"""]}
```

### Step 3: Analysis (Sequential)

After ALL research agents complete:

```
Task(
  subagent_type='general-purpose',
  prompt='Analyze all research findings. Score relevance, find contradictions, identify gaps.',
  description='Analyze findings'
)
```

### Step 4: Synthesis (Sequential)

```
Task(
  subagent_type='general-purpose',
  prompt='Generate Level {config.level} research report with all sections.',
  description='Generate report'
)
```

### Key Rules

1. **Parallel Research**: ALL research Task calls MUST be in ONE message
2. **Wait for completion**: Analysis runs AFTER all research completes
3. **Use returned data**: Pass research outputs to analysis, analysis to synthesis
4. **Quality check**: Verify minimum sources ({config.min_sources}) and high-relevance findings ({config.min_high_relevance})
"""
    return instructions


def main():
    parser = argparse.ArgumentParser(
        description="Deep Researcher v2.0 - Multi-Agent Research System"
    )
    parser.add_argument("query", help="Research query")
    parser.add_argument(
        "--level", "-l", type=int, default=3, choices=[1, 2, 3, 4, 5],
        help="Research depth level (1=quick, 5=exhaustive)"
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output file path for the report"
    )
    parser.add_argument(
        "--instructions", "-i", action="store_true",
        help="Generate Claude Code execution instructions"
    )

    args = parser.parse_args()
    config = ResearchConfig(level=args.level)

    print(f"Deep Researcher v2.0")
    print(f"=" * 50)
    print(f"Query: {args.query}")
    print(f"Level: {config.level}")
    print(f"Parallel Agents: {config.subtask_count}")
    print(f"Min Sources: {config.min_sources}")
    print(f"=" * 50)

    if args.instructions:
        instructions = generate_claude_code_instructions(args.query, config)
        print(instructions)

        if args.output:
            with open(args.output, "w") as f:
                f.write(instructions)
            print(f"\nInstructions saved to: {args.output}")
    else:
        # Generate prompt templates for manual execution
        print("\n## Planning Agent Prompt:\n")
        print(generate_planning_prompt(args.query, config))

        print("\n## Research Agent Prompt Template:\n")
        sample_subtask = Subtask(
            id=1,
            focus="Sample focus area",
            search_query=f"{args.query} 2025"
        )
        print(generate_research_prompt(sample_subtask))


if __name__ == "__main__":
    main()
