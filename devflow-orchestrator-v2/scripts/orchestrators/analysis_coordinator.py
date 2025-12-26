#!/usr/bin/env python3
"""Analysis Coordinator - Multi-perspective analysis orchestration."""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

DEVFLOW_DIR = ".devflow"

class AnalysisCoordinator:
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

    def generate_analysis_agents(self) -> Dict:
        """Generate prompts for multi-perspective analysis agents."""
        domain = self.project.get("domain", "general")
        idea = self.project.get("idea", "")

        # Load research synthesis if available
        research_context = self._load_research_context()

        agents = {
            "user_perspective": {
                "coordinator": "Analysis Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "description": "User perspective analysis",
                "prompt": f"""As the User Perspective Analyst, evaluate from user viewpoint.

## Context
Project: {idea[:300]}
Domain: {domain}

{research_context}

## Analysis Framework

### User Needs Analysis
| Need | Priority | Current Solution | Pain Points |
|------|----------|------------------|-------------|

### UX Considerations
- Accessibility requirements
- Learning curve
- User journey friction points

### User Personas
| Persona | Goals | Frustrations | Features Needed |
|---------|-------|--------------|-----------------|

### Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|

### Feasibility Score
Rate 1-10 with justification for:
- User adoption likelihood
- Learning curve acceptability
- Value proposition clarity
"""
            },
            "technical_perspective": {
                "coordinator": "Analysis Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "description": "Technical perspective analysis",
                "prompt": f"""As the Technical Perspective Analyst, evaluate technical feasibility.

## Context
Project: {idea[:300]}
Domain: {domain}

{research_context}

## Analysis Framework

### Architecture Assessment
- Scalability requirements
- Performance constraints
- Integration complexity

### Technical Debt Risk
| Area | Risk Level | Mitigation |
|------|------------|------------|

### Technology Fit
| Component | Maturity | Team Expertise | Risk |
|-----------|----------|----------------|------|

### Maintenance Considerations
- Long-term supportability
- Upgrade paths
- Documentation needs

### Feasibility Score
Rate 1-10 with justification for:
- Implementation complexity
- Scalability potential
- Maintainability
"""
            },
            "business_perspective": {
                "coordinator": "Analysis Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "description": "Business perspective analysis",
                "prompt": f"""As the Business Perspective Analyst, evaluate market viability.

## Context
Project: {idea[:300]}
Domain: {domain}

{research_context}

## Analysis Framework

### Market Fit Assessment
- Problem-solution fit
- Market timing
- Competitive positioning

### Revenue Model Analysis
| Model | Viability | Pros | Cons |
|-------|-----------|------|------|

### Growth Potential
- TAM/SAM/SOM analysis
- Growth vectors
- Expansion opportunities

### Resource Requirements
| Resource | Quantity | Cost | Priority |
|----------|----------|------|----------|

### Feasibility Score
Rate 1-10 with justification for:
- Market opportunity
- ROI potential
- Resource efficiency
"""
            },
            "risk_perspective": {
                "coordinator": "Analysis Coordinator",
                "agent_type": "general-purpose",
                "model": "sonnet",
                "run_in_background": True,
                "description": "Risk perspective analysis",
                "prompt": f"""As the Risk Perspective Analyst, identify and assess risks.

## Context
Project: {idea[:300]}
Domain: {domain}

{research_context}

## Risk Framework

### Risk Matrix
| Risk | Category | Likelihood (1-5) | Impact (1-5) | Score | Mitigation |
|------|----------|------------------|--------------|-------|------------|

### Risk Categories
1. Technical Risks
2. Market Risks
3. Security Risks
4. Compliance Risks
5. Operational Risks

### Top 5 Critical Risks
1. [Risk]: [Impact]: [Mitigation]

### Risk Mitigation Plan
| Risk | Strategy | Owner | Timeline |
|------|----------|-------|----------|

### Overall Risk Score
Calculate weighted average: (Likelihood × Impact) / 25 × 100

### Go/No-Go Recommendation
Based on risk analysis, recommend:
- GO: Proceed with mitigations
- CAUTION: Address critical risks first
- NO-GO: Fundamental issues to resolve
"""
            }
        }

        return agents

    def _load_research_context(self) -> str:
        """Load research findings for analysis context."""
        domain = self.project.get("domain", "general")
        research_dir = self.devflow / "research" / domain

        context_parts = []
        files = ["tech_stack.md", "market_trends.md", "competitors.md"]

        for f in files:
            filepath = research_dir / f
            if filepath.exists():
                with open(filepath) as file:
                    content = file.read()
                    # Truncate to avoid context overflow
                    context_parts.append(f"## {f.replace('.md', '').replace('_', ' ').title()}\n{content[:500]}...")

        if context_parts:
            return "## Research Context (Summary)\n" + "\n\n".join(context_parts)
        return ""

    def generate_risk_matrix(self, risks: List[Dict]) -> Dict:
        """Generate risk matrix data structure."""
        matrix = {
            "high_high": [],  # High likelihood, high impact
            "high_low": [],
            "low_high": [],
            "low_low": []
        }

        for risk in risks:
            likelihood = risk.get("likelihood", 3)
            impact = risk.get("impact", 3)

            if likelihood > 3 and impact > 3:
                matrix["high_high"].append(risk)
            elif likelihood > 3:
                matrix["high_low"].append(risk)
            elif impact > 3:
                matrix["low_high"].append(risk)
            else:
                matrix["low_low"].append(risk)

        return matrix

    def calculate_feasibility_score(self, perspectives: Dict) -> Dict:
        """Calculate overall feasibility score from perspectives."""
        weights = {
            "user": 0.25,
            "technical": 0.30,
            "business": 0.25,
            "risk": 0.20
        }

        total_score = 0
        for perspective, weight in weights.items():
            score = perspectives.get(perspective, {}).get("score", 5)
            total_score += score * weight

        return {
            "overall_score": round(total_score, 2),
            "max_score": 10,
            "percentage": round(total_score * 10, 1),
            "recommendation": self._get_recommendation(total_score)
        }

    def _get_recommendation(self, score: float) -> str:
        if score >= 8:
            return "Strong GO - Excellent feasibility"
        elif score >= 6:
            return "GO - Good feasibility with minor concerns"
        elif score >= 4:
            return "CAUTION - Moderate feasibility, address concerns"
        else:
            return "REVIEW - Significant concerns, reconsider approach"

    def save_analysis(self, content: str, perspectives: Dict = None):
        """Save analysis results."""
        with open(self.devflow / "analysis" / "perspectives.md", "w") as f:
            f.write(f"""# Multi-Perspective Analysis

## Generated
{datetime.now().isoformat()}

{content}
""")

        if perspectives:
            feasibility = self.calculate_feasibility_score(perspectives)
            with open(self.devflow / "analysis" / "feasibility.json", "w") as f:
                json.dump({
                    "perspectives": perspectives,
                    "feasibility": feasibility,
                    "generated_at": datetime.now().isoformat()
                }, f, indent=2)

        print("Analysis saved")

def main():
    if len(sys.argv) < 2:
        print("Usage: analysis_coordinator.py <command>")
        print("Commands: generate, save, feasibility")
        sys.exit(1)

    coordinator = AnalysisCoordinator()
    cmd = sys.argv[1]

    if cmd == "generate":
        agents = coordinator.generate_analysis_agents()
        print(json.dumps(agents, indent=2))
    elif cmd == "save":
        if len(sys.argv) < 3:
            print("Usage: analysis_coordinator.py save '<content>'")
            sys.exit(1)
        coordinator.save_analysis(sys.argv[2])
    elif cmd == "feasibility":
        # Example calculation
        perspectives = {
            "user": {"score": 7},
            "technical": {"score": 6},
            "business": {"score": 8},
            "risk": {"score": 5}
        }
        result = coordinator.calculate_feasibility_score(perspectives)
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
