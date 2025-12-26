#!/usr/bin/env python3
"""Research orchestrator - generates prompts for parallel research agents."""

import json
import sys
from pathlib import Path
from datetime import datetime

DEVFLOW_DIR = ".devflow"

def get_project():
    """Load project configuration."""
    devflow = Path.cwd() / DEVFLOW_DIR
    if not devflow.exists():
        print("No DevFlow project found.")
        sys.exit(1)

    with open(devflow / "project.json") as f:
        return json.load(f)

def generate_research_prompts(domain: str = None):
    """Generate prompts for 5 parallel research agents."""
    project = get_project()
    domain = domain or project.get("domain", "software")
    idea = project.get("idea", "")

    prompts = {
        "tech_stack": {
            "agent_type": "Explore",
            "model": "haiku",
            "description": "Tech stack research",
            "prompt": f"""Research latest technology stack for {domain} development in 2025.

Context: {idea[:200]}

Find and summarize:
1. Recommended programming languages
2. Popular frameworks and libraries
3. Database technologies
4. Infrastructure/cloud options
5. DevOps tools

Output format:
## Tech Stack Recommendations

### Languages
- [Language]: [Why suitable]

### Frameworks
- [Framework]: [Use case]

### Databases
- [Database]: [When to use]

### Infrastructure
- [Service]: [Benefits]
"""
        },
        "market_trends": {
            "agent_type": "general-purpose",
            "model": "haiku",
            "description": "Market trends research",
            "prompt": f"""Research current market trends for {domain} in 2025.

Context: {idea[:200]}

WebSearch for:
- "{domain} market trends 2025"
- "{domain} industry growth forecast"
- "{domain} user expectations 2025"

Summarize:
1. Market size and growth
2. User behavior trends
3. Emerging patterns
4. Opportunities and challenges
"""
        },
        "open_source": {
            "agent_type": "general-purpose",
            "model": "haiku",
            "description": "Open source research",
            "prompt": f"""Find best open source repositories for {domain}.

Use GitMVP MCP tools:
- mcp-cli call gitmvp/search_repositories with relevant query

Look for:
1. Popular starter templates
2. Well-maintained libraries
3. Reference implementations
4. Testing frameworks

Summarize top 5-10 repositories with:
- Name and URL
- Stars/activity level
- Key features
- How it helps the project
"""
        },
        "security": {
            "agent_type": "general-purpose",
            "model": "haiku",
            "description": "Security research",
            "prompt": f"""Research security best practices for {domain} in 2025.

WebSearch for:
- "{domain} security best practices 2025"
- "OWASP {domain} security"
- "{domain} compliance requirements"

Document:
1. Common vulnerabilities
2. Security frameworks
3. Authentication patterns
4. Data protection requirements
5. Compliance considerations
"""
        },
        "competitors": {
            "agent_type": "general-purpose",
            "model": "haiku",
            "description": "Competitor analysis",
            "prompt": f"""Analyze competitors and similar products in {domain}.

Context: {idea[:200]}

WebSearch for:
- "{domain} top products 2025"
- "{domain} alternatives comparison"

For each competitor, identify:
1. Key features
2. Pricing model
3. Target audience
4. Strengths/weaknesses
5. Differentiation opportunities
"""
        }
    }

    return prompts

def generate_agent_calls(domain: str = None):
    """Generate Task tool calls for parallel execution."""
    prompts = generate_research_prompts(domain)

    print("# Multi-Agent Research Tasks")
    print()
    print("Launch these 5 agents in parallel using Task tool:")
    print()

    for name, config in prompts.items():
        print(f"""## {name.replace('_', ' ').title()} Agent

```
Task(
  subagent_type='{config['agent_type']}',
  model='{config['model']}',
  run_in_background=true,
  description='{config['description']}',
  prompt='''{config['prompt']}'''
)
```
""")

def save_research_template():
    """Save research synthesis template."""
    devflow = Path.cwd() / DEVFLOW_DIR
    template = """# Research Synthesis

## Tech Stack Findings
(Insert tech_stack agent results)

## Market Trends
(Insert market_trends agent results)

## Open Source Options
(Insert open_source agent results)

## Security Considerations
(Insert security agent results)

## Competitive Landscape
(Insert competitors agent results)

## Key Insights

### Recommended Approach
1.

### Critical Decisions Needed
1.

### Risks Identified
1.

---
Generated: {timestamp}
"""
    with open(devflow / "research" / "synthesis_template.md", "w") as f:
        f.write(template.format(timestamp=datetime.now().isoformat()))

    print("Saved research synthesis template")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: research_orchestrator.py <command> [domain]")
        print("Commands: generate, template")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "generate":
        domain = sys.argv[2] if len(sys.argv) > 2 else None
        generate_agent_calls(domain)
    elif cmd == "template":
        save_research_template()
    elif cmd == "prompts":
        domain = sys.argv[2] if len(sys.argv) > 2 else None
        prompts = generate_research_prompts(domain)
        print(json.dumps(prompts, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
