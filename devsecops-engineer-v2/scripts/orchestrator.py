#!/usr/bin/env python3
"""
DevSecOps Engineer v2.0 Orchestrator

Multi-agent security assessment system with parallel execution.
Can be used standalone or as a reference for Claude Code skill execution.

Usage:
    python orchestrator.py --target local --level 3 --output report.md
    python orchestrator.py --target ssh --host server.example.com --level 4
    python orchestrator.py --instructions --level 3
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class SecurityConfig:
    """Configuration for security assessment."""
    level: int = 3
    target_type: str = "local"  # local, ssh, container
    hostname: Optional[str] = None
    output_format: str = "markdown"
    include_html: bool = True
    interactive_patch: bool = True

    @property
    def intel_agent_count(self) -> int:
        """Number of parallel intel agents based on level."""
        return {1: 1, 2: 2, 3: 3, 4: 3, 5: 3}.get(self.level, 3)

    @property
    def scan_categories(self) -> List[str]:
        """Scan categories based on level."""
        all_cats = ["vulnerability", "secrets", "config", "deps", "container"]
        return {
            1: all_cats[:2],
            2: all_cats[:3],
            3: all_cats,
            4: all_cats,
            5: all_cats,
        }.get(self.level, all_cats)

    @property
    def min_findings(self) -> int:
        """Minimum findings for the level."""
        return {1: 5, 2: 10, 3: 15, 4: 20, 5: 25}.get(self.level, 15)

    @property
    def requires_html(self) -> bool:
        """Whether HTML report is required."""
        return self.level >= 3


@dataclass
class IntelQuery:
    """Intelligence query definition."""
    type: str  # cve, tech, compliance
    focus: str
    technologies: List[str] = field(default_factory=list)


@dataclass
class ScanTask:
    """Security scan task definition."""
    category: str
    target: str
    tools: List[str] = field(default_factory=list)


@dataclass
class Finding:
    """Security finding."""
    id: str
    severity: str
    cvss_score: float
    title: str
    description: str
    location: str
    remediation: str
    category: str


@dataclass
class AnalysisResult:
    """Result from Analysis Agent."""
    risk_score: int
    risk_level: str
    critical_findings: List[Finding]
    high_findings: List[Finding]
    medium_findings: List[Finding]
    low_findings: List[Finding]
    compliance_gaps: dict
    remediation_priority: list


def generate_planning_prompt(config: SecurityConfig) -> str:
    """Generate prompt for Planning Agent."""
    return f"""You are a Security Planning Agent. Analyze the assessment scope.

TARGET TYPE: {config.target_type}
{"HOSTNAME: " + config.hostname if config.hostname else ""}
LEVEL: {config.level}

Instructions:
1. Identify technologies and frameworks in the target
2. Determine which scan categories apply
3. Generate intel queries for relevant technologies
4. Estimate expected findings based on target complexity

Output JSON:
{{
  "target": "{config.target_type}",
  "technologies": ["detected", "tech", "list"],
  "scan_categories": {json.dumps(config.scan_categories)},
  "intel_queries": [
    {{"type": "cve", "focus": "Latest CVEs for detected tech"}},
    {{"type": "tech", "focus": "Attack patterns for detected tech"}},
    {{"type": "compliance", "focus": "Compliance requirements"}}
  ],
  "expected_findings": {config.min_findings},
  "priority_technologies": ["most", "critical"]
}}"""


def generate_intel_prompt(query: IntelQuery) -> str:
    """Generate prompt for Intel Agent."""
    return f"""You are an Intel Agent gathering threat intelligence.

INTEL TYPE: {query.type}
FOCUS: {query.focus}
TECHNOLOGIES: {json.dumps(query.technologies)}

Instructions:
1. Use WebSearch for latest security advisories (last 30 days)
2. Focus on CVEs with CVSS >= 7.0
3. Check for active exploitation (CISA KEV)
4. Include patch availability status

Output JSON:
{{
  "intel_type": "{query.type}",
  "findings": [
    {{
      "cve_id": "CVE-XXXX-XXXXX",
      "severity": "critical|high",
      "cvss_score": 9.8,
      "affected_packages": ["package@version"],
      "description": "...",
      "exploited_in_wild": true|false,
      "patch_available": true|false,
      "source_url": "..."
    }}
  ],
  "zero_days": [...],
  "attack_patterns": [...],
  "summary": {{
    "total_cves": 0,
    "critical": 0,
    "high": 0
  }}
}}"""


def generate_scan_prompt(task: ScanTask) -> str:
    """Generate prompt for Scan Agent."""
    tools_map = {
        "vulnerability": ["trivy", "npm audit", "pip-audit"],
        "secrets": ["trufflehog", "detect-secrets"],
        "config": ["lynis", "cis-cat"],
        "deps": ["dependency-check", "npm outdated"],
        "container": ["trivy image", "hadolint"],
    }
    tools = tools_map.get(task.category, [])

    return f"""You are a Security Scan Agent for {task.category} scanning.

SCAN CATEGORY: {task.category}
TARGET: {task.target}
TOOLS: {json.dumps(tools)}

Instructions:
1. Run appropriate scanning tools
2. Collect all findings with severity
3. Calculate CVSS scores where applicable
4. Include remediation steps

Output JSON:
{{
  "scan_type": "{task.category}",
  "target": "{task.target}",
  "findings": [
    {{
      "id": "...",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0-10.0,
      "title": "...",
      "description": "...",
      "location": "file:line",
      "remediation": "..."
    }}
  ],
  "summary": {{"critical": 0, "high": 0, "medium": 0, "low": 0}}
}}"""


def generate_analysis_prompt(intel_results: str, scan_results: str) -> str:
    """Generate prompt for Analysis Agent."""
    return f"""You are a Security Analysis Agent. Process all findings.

INTEL RESULTS:
{intel_results}

SCAN RESULTS:
{scan_results}

Tasks:
1. Calculate composite risk score (CVSS-weighted)
2. Cross-reference findings with threat intelligence
3. Identify false positives based on context
4. Prioritize by exploitability and impact
5. Map findings to compliance frameworks (OWASP 2025, CIS, NIST CSF)

Risk Score Formula:
raw = sum(critical×10 + high×7 + medium×4 + low×1)
Apply modifiers: exploited_in_wild (+20%), patch_available (-10%)

Output JSON:
{{
  "risk_score": 0-100,
  "risk_level": "critical|high|medium|low",
  "critical_findings": [...with intel context...],
  "high_findings": [...],
  "medium_findings": [...],
  "low_findings": [...],
  "compliance_gaps": {{
    "owasp_2025": {{"score": 80, "gaps": [...]}},
    "cis": {{"score": 75, "gaps": [...]}},
    "nist_csf": {{"score": 85, "gaps": [...]}}
  }},
  "remediation_priority": [
    {{"rank": 1, "finding_id": "...", "action": "...", "sla": "24h"}}
  ]
}}"""


def generate_synthesis_prompt(analysis: str, config: SecurityConfig) -> str:
    """Generate prompt for Synthesis Agent."""
    length = {1: "2-3 pages", 2: "3-5 pages", 3: "5-7 pages", 4: "7-10 pages", 5: "10+ pages"}
    return f"""You are a Security Report Synthesis Agent.

ANALYSIS RESULTS:
{analysis}

LEVEL: {config.level}
TARGET: {config.target_type}
REPORT LENGTH: {length.get(config.level, "5-7 pages")}

Generate a Markdown report with:
1. Executive Summary (for leadership)
2. Critical Findings (CVSS >= 9.0) with detailed remediation
3. High Priority Findings (CVSS 7.0-8.9)
4. Compliance Status (OWASP 2025, CIS, NIST CSF)
5. Remediation Timeline with SLAs
6. Threat Intelligence Context
7. Full source list"""


def generate_claude_code_instructions(config: SecurityConfig) -> str:
    """Generate Claude Code instructions for multi-agent execution."""
    instructions = f"""
## DevSecOps v2.0 Execution Instructions

**Target:** {config.target_type}
**Level:** {config.level}
**Intel Agents:** {config.intel_agent_count}
**Scan Categories:** {len(config.scan_categories)}
**Min Findings:** {config.min_findings}

### Phase 1: Planning (Sequential)

```
Task(
  subagent_type='Plan',
  prompt='Analyze security assessment scope for {config.target_type} target at level {config.level}...',
  description='Plan security assessment'
)
```

### Phase 2: Intelligence Gathering (PARALLEL - Single Message)

After planning, spawn ALL intel agents in ONE message:

```python
# Include ALL these Task calls in a SINGLE response
[
  Task(subagent_type='Explore', prompt='Search latest CVE advisories...', description='Intel: CVE monitoring', model='haiku'),
  Task(subagent_type='Explore', prompt='Search technology-specific threats...', description='Intel: Tech threats', model='haiku'),
  Task(subagent_type='Explore', prompt='Search compliance updates...', description='Intel: Compliance', model='haiku'),
]
```

### Phase 3: Security Scanning (PARALLEL - Single Message)

Spawn ALL scan agents in ONE message:

```python
# Include ALL these Task calls in a SINGLE response
[
"""

    for cat in config.scan_categories:
        instructions += f"""  Task(subagent_type='general-purpose', prompt='Run {cat} scan...', description='Scan: {cat.title()}', model='haiku'),
"""

    instructions += f"""]
```

### Phase 4: Analysis (Sequential)

After ALL scans complete:

```
Task(
  subagent_type='general-purpose',
  prompt='Analyze all security findings. Calculate CVSS risk score, map compliance, prioritize remediation.',
  description='Analyze security findings'
)
```

### Phase 5: Interactive Remediation (Sequential)

```bash
python3 scripts/auto_patch.py --scan-report ./security-reports/analysis.json
```

### Phase 6: Synthesis (Sequential)

```
Task(
  subagent_type='general-purpose',
  prompt='Generate Level {config.level} security report with executive summary, findings, compliance, remediation timeline.',
  description='Generate security report'
)
```

### Phase 7: Visualization (Sequential)

{"Required for Level " + str(config.level) if config.requires_html else "Optional"}

```
Task(
  subagent_type='general-purpose',
  prompt='Convert markdown to HTML using scripts/md_to_html.py',
  description='Generate HTML report',
  model='haiku'
)
```

### Phase 8: Self-Upgrade (Sequential)

```bash
python3 scripts/self_upgrade.py --findings ./security-reports
```

### Key Rules

1. **Parallel Intel**: ALL intel Task calls MUST be in ONE message
2. **Parallel Scans**: ALL scan Task calls MUST be in ONE message
3. **Wait for completion**: Analysis runs AFTER all intel and scans complete
4. **Interactive patching**: User confirms each patch before applying
5. **Quality check**: Verify minimum findings ({config.min_findings})
"""
    return instructions


def main():
    parser = argparse.ArgumentParser(
        description="DevSecOps Engineer v2.0 - Multi-Agent Security Assessment"
    )
    parser.add_argument(
        "--target", "-t", type=str, default="local",
        choices=["local", "ssh", "container"],
        help="Target type for assessment"
    )
    parser.add_argument(
        "--host", type=str, default=None,
        help="Hostname for SSH target"
    )
    parser.add_argument(
        "--level", "-l", type=int, default=3, choices=[1, 2, 3, 4, 5],
        help="Security assessment level (1=quick, 5=exhaustive)"
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output file path"
    )
    parser.add_argument(
        "--instructions", "-i", action="store_true",
        help="Generate Claude Code execution instructions"
    )

    args = parser.parse_args()
    config = SecurityConfig(
        level=args.level,
        target_type=args.target,
        hostname=args.host
    )

    print("DevSecOps Engineer v2.0")
    print("=" * 50)
    print(f"Target: {config.target_type}")
    if config.hostname:
        print(f"Host: {config.hostname}")
    print(f"Level: {config.level}")
    print(f"Intel Agents: {config.intel_agent_count}")
    print(f"Scan Categories: {', '.join(config.scan_categories)}")
    print(f"Min Findings: {config.min_findings}")
    print(f"HTML Report: {'Required' if config.requires_html else 'Optional'}")
    print("=" * 50)

    if args.instructions:
        instructions = generate_claude_code_instructions(config)
        print(instructions)

        if args.output:
            with open(args.output, "w") as f:
                f.write(instructions)
            print(f"\nInstructions saved to: {args.output}")
    else:
        print("\n## Planning Agent Prompt:\n")
        print(generate_planning_prompt(config))

        print("\n## Intel Agent Prompt (CVE):\n")
        sample_intel = IntelQuery(type="cve", focus="CVE monitoring", technologies=["nodejs", "python"])
        print(generate_intel_prompt(sample_intel))

        print("\n## Scan Agent Prompt (Vulnerability):\n")
        sample_scan = ScanTask(category="vulnerability", target="./")
        print(generate_scan_prompt(sample_scan))


if __name__ == "__main__":
    main()
