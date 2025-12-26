#!/usr/bin/env python3
"""Master Orchestrator - Premium DevFlow v2 central coordinator."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DEVFLOW_DIR = ".devflow"

# Domain detection keywords
DOMAIN_KEYWORDS = {
    "devops": ["deploy", "ci/cd", "kubernetes", "docker", "terraform", "aws", "gcp", "azure"],
    "security": ["auth", "security", "encryption", "compliance", "audit", "pentest"],
    "webdev": ["frontend", "react", "vue", "api", "rest", "graphql", "component"],
    "dataops": ["data", "etl", "pipeline", "analytics", "database", "ml", "ai"],
    "mobile": ["ios", "android", "react native", "flutter", "mobile"],
    "enterprise": ["enterprise", "b2b", "saas", "multi-tenant", "sso"]
}

# Complexity indicators
COMPLEXITY_INDICATORS = {
    1: ["simple", "basic", "minimal", "prototype"],
    2: ["standard", "typical", "common"],
    3: ["moderate", "medium", "integrated"],
    4: ["complex", "advanced", "enterprise"],
    5: ["highly complex", "mission-critical", "large-scale"]
}

class MasterOrchestrator:
    def __init__(self):
        self.devflow = Path.cwd() / DEVFLOW_DIR
        self.project = None
        self.load_state()

    def load_state(self):
        """Load project state if exists."""
        if (self.devflow / "project.json").exists():
            with open(self.devflow / "project.json") as f:
                self.project = json.load(f)

    def save_state(self):
        """Save project state."""
        with open(self.devflow / "project.json", "w") as f:
            json.dump(self.project, f, indent=2)

    def detect_domain(self, idea: str) -> str:
        """Detect project domain from idea."""
        idea_lower = idea.lower()
        scores = {}

        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in idea_lower)
            if score > 0:
                scores[domain] = score

        if scores:
            return max(scores, key=scores.get)
        return "general"

    def detect_complexity(self, idea: str) -> int:
        """Detect project complexity level (1-5)."""
        idea_lower = idea.lower()

        for level in [5, 4, 3, 2, 1]:
            for indicator in COMPLEXITY_INDICATORS[level]:
                if indicator in idea_lower:
                    return level

        # Default based on idea length
        if len(idea) > 500:
            return 4
        elif len(idea) > 200:
            return 3
        return 2

    def init_project(self, idea: str, domain: str = None, complexity: int = None):
        """Initialize premium DevFlow project."""
        if self.devflow.exists():
            print(f"Error: {DEVFLOW_DIR}/ already exists.")
            sys.exit(1)

        # Auto-detect if not specified
        domain = domain or self.detect_domain(idea)
        complexity = complexity or self.detect_complexity(idea)

        # Create directory structure
        dirs = [
            "versions",
            "research",
            f"research/{domain}",
            "analysis",
            "features",
            "plans/current",
            "plans/archive",
            "analytics",
            "knowledge",
            "knowledge/retrospectives",
            "meta"
        ]
        for d in dirs:
            (self.devflow / d).mkdir(parents=True, exist_ok=True)

        # Create master project state
        self.project = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "idea": idea,
            "domain": domain,
            "complexity": complexity,
            "current_version": "0.0",
            "target_version": "10.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version_history": ["0.0"],
            "workflow_phase": "initialized",
            "quality_gates_passed": [],
            "agent_count": self._calculate_agent_count(complexity)
        }
        self.save_state()

        # Initialize analytics
        self._init_analytics()

        # Initialize knowledge base
        self._init_knowledge_base()

        # Initialize quality gates
        self._init_quality_gates()

        # Create initial version file
        self._create_version_file("0.0", "Idea Stage")

        print(f"""
# DevFlow V2 Project Initialized

## Project Details
| Field | Value |
|-------|-------|
| Idea | {idea[:60]}... |
| Domain | {domain} (auto-detected) |
| Complexity | Level {complexity}/5 |
| Agent Count | {self.project['agent_count']} |
| Version | v0.0 (Idea Stage) |
| Target | v10.0+ |

## Next Steps
1. `/devflow2-research` - Run hierarchical research
2. `/devflow2-status` - View dashboard
""")

    def _calculate_agent_count(self, complexity: int) -> int:
        """Calculate optimal agent count based on complexity."""
        return min(5 + complexity, 10)

    def _init_analytics(self):
        """Initialize analytics tracking."""
        analytics = {
            "velocity": {"history": [], "current": 0},
            "predictions": {"next_version_days": None, "confidence": 0},
            "burndown": {"total_features": 0, "completed": 0, "history": []},
            "created_at": datetime.now().isoformat()
        }
        with open(self.devflow / "analytics" / "velocity.json", "w") as f:
            json.dump(analytics, f, indent=2)

    def _init_knowledge_base(self):
        """Initialize knowledge accumulation."""
        knowledge = {
            "patterns": [],
            "anti_patterns": [],
            "domain_insights": {},
            "source_credibility": {},
            "created_at": datetime.now().isoformat()
        }
        with open(self.devflow / "knowledge" / "patterns.json", "w") as f:
            json.dump(knowledge, f, indent=2)

        with open(self.devflow / "knowledge" / "insights.md", "w") as f:
            f.write("# Accumulated Insights\n\nKnowledge extracted from research and analysis.\n\n")

    def _init_quality_gates(self):
        """Initialize quality gate tracking."""
        gates = {
            "gates": {
                "research_complete": {"passed": False, "timestamp": None},
                "analysis_complete": {"passed": False, "timestamp": None},
                "plan_validated": {"passed": False, "timestamp": None},
                "version_ready": {"passed": False, "timestamp": None}
            },
            "history": []
        }
        with open(self.devflow / "meta" / "quality_gates.json", "w") as f:
            json.dump(gates, f, indent=2)

    def _create_version_file(self, version: str, stage: str):
        """Create version documentation file."""
        filename = f"v{version}-{stage.lower().replace(' ', '-')}.md"
        content = f"""# v{version} - {stage}

## Created
{datetime.now().isoformat()}

## Stage
{stage}

## Features
(To be defined)

## Quality Gates
- [ ] Research complete
- [ ] Analysis complete
- [ ] Plan validated
- [ ] Version ready
"""
        with open(self.devflow / "versions" / filename, "w") as f:
            f.write(content)

    def get_status(self) -> Dict:
        """Get comprehensive project status."""
        if not self.project:
            return {"error": "No project found"}

        # Load analytics
        analytics = {}
        if (self.devflow / "analytics" / "velocity.json").exists():
            with open(self.devflow / "analytics" / "velocity.json") as f:
                analytics = json.load(f)

        # Load quality gates
        gates = {}
        if (self.devflow / "meta" / "quality_gates.json").exists():
            with open(self.devflow / "meta" / "quality_gates.json") as f:
                gates = json.load(f)

        # Calculate progress
        current = float(self.project.get("current_version", "0.0"))
        target = float(self.project.get("target_version", "10.0"))
        progress = min(100, (current / target) * 100)

        return {
            "project": self.project,
            "analytics": analytics,
            "quality_gates": gates.get("gates", {}),
            "progress": progress
        }

    def update_phase(self, phase: str):
        """Update workflow phase."""
        if self.project:
            self.project["workflow_phase"] = phase
            self.project["updated_at"] = datetime.now().isoformat()
            self.save_state()

def main():
    if len(sys.argv) < 2:
        print("Usage: master.py <command> [args]")
        print("Commands: init, status, phase, detect")
        sys.exit(1)

    orchestrator = MasterOrchestrator()
    cmd = sys.argv[1]

    if cmd == "init":
        if len(sys.argv) < 3:
            print("Usage: master.py init '<idea>' [domain] [complexity]")
            sys.exit(1)
        idea = sys.argv[2]
        domain = sys.argv[3] if len(sys.argv) > 3 else None
        complexity = int(sys.argv[4]) if len(sys.argv) > 4 else None
        orchestrator.init_project(idea, domain, complexity)
    elif cmd == "status":
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))
    elif cmd == "phase":
        if len(sys.argv) < 3:
            print("Usage: master.py phase <phase_name>")
            sys.exit(1)
        orchestrator.update_phase(sys.argv[2])
        print(f"Phase updated to: {sys.argv[2]}")
    elif cmd == "detect":
        if len(sys.argv) < 3:
            print("Usage: master.py detect '<idea>'")
            sys.exit(1)
        idea = sys.argv[2]
        domain = orchestrator.detect_domain(idea)
        complexity = orchestrator.detect_complexity(idea)
        print(f"Domain: {domain}")
        print(f"Complexity: {complexity}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
