#!/usr/bin/env python3
"""Research Coordinator - Hierarchical multi-agent research orchestration."""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

DEVFLOW_DIR = ".devflow"

# Source credibility tiers
SOURCE_TIERS = {
    "tier1": {
        "name": "Official Documentation",
        "score": 1.0,
        "domains": ["docs.", "official.", ".io/docs", "developer."]
    },
    "tier2": {
        "name": "Established Tech Publications",
        "score": 0.8,
        "domains": ["techcrunch", "medium.com", "dev.to", "hackernoon"]
    },
    "tier3": {
        "name": "Community Sources",
        "score": 0.6,
        "domains": ["reddit.com", "stackoverflow", "github.com"]
    },
    "tier4": {
        "name": "General Sources",
        "score": 0.4,
        "domains": []
    }
}

class ResearchCoordinator:
    def __init__(self):
        self.devflow = Path.cwd() / DEVFLOW_DIR
        self.project = self._load_project()

    def _load_project(self) -> Dict:
        """Load project configuration."""
        if not self.devflow.exists():
            print("No DevFlow project found.")
            sys.exit(1)

        with open(self.devflow / "project.json") as f:
            return json.load(f)

    def generate_research_agents(self) -> Dict:
        """Generate prompts for hierarchical research agents."""
        domain = self.project.get("domain", "general")
        idea = self.project.get("idea", "")
        complexity = self.project.get("complexity", 3)

        # Adjust research depth based on complexity
        depth = "comprehensive" if complexity >= 4 else "focused"
        sources = "10-15" if complexity >= 4 else "5-10"

        agents = {
            "tech_stack": {
                "coordinator": "Research Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "priority": 1,
                "description": f"Tech stack research for {domain}",
                "prompt": f"""As the Tech Stack Research Agent, conduct {depth} research.

## Context
Project Idea: {idea[:300]}
Domain: {domain}

## Research Tasks
1. WebSearch "{domain} technology stack 2025 best practices"
2. WebSearch "{domain} programming languages comparison 2025"
3. WebSearch "{domain} frameworks benchmarks 2025"

## Deliverables
Find {sources} sources and synthesize:

### Languages
| Language | Use Case | Maturity | Community | Recommendation |
|----------|----------|----------|-----------|----------------|

### Frameworks
| Framework | Strengths | Weaknesses | When to Use |
|-----------|-----------|------------|-------------|

### Databases
| Database | Type | Best For | Scalability |
|----------|------|----------|-------------|

### Infrastructure
| Service | Provider | Cost Tier | Features |
|---------|----------|-----------|----------|

## Source Credibility
Rate each source: Tier 1 (official) / Tier 2 (tech pub) / Tier 3 (community)
"""
            },
            "market_trends": {
                "coordinator": "Research Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "priority": 2,
                "description": f"Market trends research for {domain}",
                "prompt": f"""As the Market Trends Research Agent, analyze current market.

## Context
Project Idea: {idea[:300]}
Domain: {domain}

## Research Tasks
1. WebSearch "{domain} market size growth 2025"
2. WebSearch "{domain} user behavior trends 2025"
3. WebSearch "{domain} industry forecast analysis"

## Deliverables

### Market Overview
- Market size and growth rate
- Key drivers and inhibitors
- Regional variations

### User Trends
| Trend | Impact | Opportunity |
|-------|--------|-------------|

### Growth Forecast
| Metric | 2025 | 2026 | 2027 |
|--------|------|------|------|

### Opportunities
1. [Opportunity with reasoning]
"""
            },
            "open_source": {
                "coordinator": "Research Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "priority": 3,
                "description": f"Open source research for {domain}",
                "prompt": f"""As the Open Source Research Agent, find relevant repositories.

## Context
Project Idea: {idea[:300]}
Domain: {domain}

## Research Tasks
Use GitMVP MCP tools:
1. mcp-cli call gitmvp/search_repositories with query "{domain} starter template"
2. mcp-cli call gitmvp/search_repositories with query "{domain} boilerplate"
3. WebSearch "awesome {domain} github repository list"

## Deliverables

### Top Repositories
| Repository | Stars | Last Update | Key Features | License |
|------------|-------|-------------|--------------|---------|

### Starter Templates
| Template | Framework | Features | Complexity |
|----------|-----------|----------|------------|

### Reusable Libraries
| Library | Purpose | Maturity | Documentation |
|---------|---------|----------|---------------|

### Recommendations
Prioritize repositories with:
- Active maintenance (commits < 3 months)
- Good documentation
- Permissive license
"""
            },
            "security": {
                "coordinator": "Research Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "priority": 4,
                "description": f"Security research for {domain}",
                "prompt": f"""As the Security Research Agent, identify security requirements.

## Context
Project Idea: {idea[:300]}
Domain: {domain}

## Research Tasks
1. WebSearch "OWASP {domain} security 2025"
2. WebSearch "{domain} compliance requirements"
3. WebSearch "{domain} security best practices checklist"

## Deliverables

### OWASP Top 10 Relevance
| Vulnerability | Relevance | Mitigation |
|---------------|-----------|------------|

### Compliance Requirements
| Framework | Requirement | Priority |
|-----------|-------------|----------|

### Security Checklist
- [ ] Authentication & Authorization
- [ ] Data encryption
- [ ] Input validation
- [ ] API security
- [ ] Logging & monitoring

### Risk Assessment
| Risk | Likelihood | Impact | Priority |
|------|------------|--------|----------|
"""
            },
            "competitors": {
                "coordinator": "Research Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "priority": 5,
                "description": f"Competitor analysis for {domain}",
                "prompt": f"""As the Competitor Analysis Agent, map the competitive landscape.

## Context
Project Idea: {idea[:300]}
Domain: {domain}

## Research Tasks
1. WebSearch "{domain} top products 2025 comparison"
2. WebSearch "{domain} alternatives review"
3. WebSearch "{domain} market leaders analysis"

## Deliverables

### Competitor Matrix
| Competitor | Strengths | Weaknesses | Pricing | Market Share |
|------------|-----------|------------|---------|--------------|

### Feature Comparison
| Feature | Comp 1 | Comp 2 | Comp 3 | Gap |
|---------|--------|--------|--------|-----|

### Differentiation Opportunities
1. [Opportunity]: [Why it matters]

### Positioning Recommendations
- Target segment:
- Key differentiator:
- Value proposition:
"""
            }
        }

        return agents

    def generate_synthesis_prompt(self) -> str:
        """Generate prompt for synthesizing all research."""
        return """## Research Synthesis Task

Synthesize all research findings into a coherent analysis:

### Executive Summary
(3-5 key insights)

### Technology Recommendations
| Component | Recommendation | Confidence | Rationale |
|-----------|----------------|------------|-----------|

### Market Positioning
- Target market:
- Key opportunity:
- Timing:

### Risk Summary
| Risk | Severity | Mitigation |
|------|----------|------------|

### Source Credibility Summary
- Tier 1 sources used: X
- Tier 2 sources used: Y
- Tier 3 sources used: Z
- Overall confidence: X%

### Next Steps
1.
2.
3.
"""

    def save_research(self, research_type: str, content: str, sources: List[Dict] = None):
        """Save research with source credibility tracking."""
        domain = self.project.get("domain", "general")
        research_dir = self.devflow / "research" / domain

        # Save content
        filename = f"{research_type}.md"
        with open(research_dir / filename, "w") as f:
            f.write(f"""# {research_type.replace('_', ' ').title()} Research

## Generated
{datetime.now().isoformat()}

{content}
""")

        # Track sources if provided
        if sources:
            sources_file = self.devflow / "research" / "sources.json"
            existing = {}
            if sources_file.exists():
                with open(sources_file) as f:
                    existing = json.load(f)

            existing[research_type] = {
                "sources": sources,
                "timestamp": datetime.now().isoformat()
            }

            with open(sources_file, "w") as f:
                json.dump(existing, f, indent=2)

        print(f"Saved research: {research_type}")

    def check_completeness(self) -> Dict:
        """Check research completeness for quality gate."""
        domain = self.project.get("domain", "general")
        research_dir = self.devflow / "research" / domain

        required = ["tech_stack.md", "market_trends.md", "open_source.md",
                   "security.md", "competitors.md"]

        status = {}
        for req in required:
            status[req.replace(".md", "")] = (research_dir / req).exists()

        complete = all(status.values())
        return {
            "complete": complete,
            "status": status,
            "completion_rate": sum(status.values()) / len(status) * 100
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: research_coordinator.py <command>")
        print("Commands: generate, save, check, synthesis")
        sys.exit(1)

    coordinator = ResearchCoordinator()
    cmd = sys.argv[1]

    if cmd == "generate":
        agents = coordinator.generate_research_agents()
        print(json.dumps(agents, indent=2))
    elif cmd == "save":
        if len(sys.argv) < 4:
            print("Usage: research_coordinator.py save <type> '<content>'")
            sys.exit(1)
        coordinator.save_research(sys.argv[2], sys.argv[3])
    elif cmd == "check":
        result = coordinator.check_completeness()
        print(json.dumps(result, indent=2))
    elif cmd == "synthesis":
        prompt = coordinator.generate_synthesis_prompt()
        print(prompt)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
