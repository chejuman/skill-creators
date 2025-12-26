#!/usr/bin/env python3
"""Knowledge Accumulation System - Learn from projects and improve."""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DEVFLOW_DIR = ".devflow"

class KnowledgeBase:
    def __init__(self):
        self.devflow = Path.cwd() / DEVFLOW_DIR
        self.project = self._load_project()
        self.knowledge = self._load_knowledge()

    def _load_project(self) -> Dict:
        if not self.devflow.exists():
            print("No DevFlow project found.")
            sys.exit(1)
        with open(self.devflow / "project.json") as f:
            return json.load(f)

    def _load_knowledge(self) -> Dict:
        knowledge_file = self.devflow / "knowledge" / "patterns.json"
        if knowledge_file.exists():
            with open(knowledge_file) as f:
                return json.load(f)
        return {"patterns": [], "anti_patterns": [], "domain_insights": {}, "source_credibility": {}}

    def _save_knowledge(self):
        with open(self.devflow / "knowledge" / "patterns.json", "w") as f:
            json.dump(self.knowledge, f, indent=2)

    def add_pattern(self, name: str, description: str, context: str,
                   category: str = "general", confidence: float = 0.8):
        """Add a reusable pattern."""
        pattern = {
            "id": f"PAT-{len(self.knowledge['patterns']) + 1:03d}",
            "name": name,
            "description": description,
            "context": context,
            "category": category,
            "confidence": confidence,
            "usage_count": 1,
            "created_at": datetime.now().isoformat(),
            "domain": self.project.get("domain", "general")
        }
        self.knowledge["patterns"].append(pattern)
        self._save_knowledge()
        self._update_insights(f"New pattern added: {name}")
        print(f"Added pattern: {pattern['id']} - {name}")
        return pattern

    def add_anti_pattern(self, name: str, description: str, consequence: str,
                        alternative: str, category: str = "general"):
        """Add an anti-pattern to avoid."""
        anti_pattern = {
            "id": f"ANTI-{len(self.knowledge['anti_patterns']) + 1:03d}",
            "name": name,
            "description": description,
            "consequence": consequence,
            "alternative": alternative,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "domain": self.project.get("domain", "general")
        }
        self.knowledge["anti_patterns"].append(anti_pattern)
        self._save_knowledge()
        self._update_insights(f"Anti-pattern identified: {name}")
        print(f"Added anti-pattern: {anti_pattern['id']} - {name}")
        return anti_pattern

    def add_domain_insight(self, insight: str, source: str, confidence: float = 0.7):
        """Add domain-specific insight."""
        domain = self.project.get("domain", "general")

        if domain not in self.knowledge["domain_insights"]:
            self.knowledge["domain_insights"][domain] = []

        self.knowledge["domain_insights"][domain].append({
            "insight": insight,
            "source": source,
            "confidence": confidence,
            "created_at": datetime.now().isoformat()
        })
        self._save_knowledge()
        self._update_insights(f"Domain insight ({domain}): {insight[:50]}...")
        print(f"Added insight for domain: {domain}")

    def update_source_credibility(self, source: str, rating: float, notes: str = ""):
        """Update source credibility rating."""
        self.knowledge["source_credibility"][source] = {
            "rating": rating,
            "notes": notes,
            "last_updated": datetime.now().isoformat()
        }
        self._save_knowledge()
        print(f"Updated credibility for {source}: {rating}")

    def _update_insights(self, entry: str):
        """Append to insights markdown."""
        insights_file = self.devflow / "knowledge" / "insights.md"
        with open(insights_file, "a") as f:
            f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{entry}\n")

    def create_retrospective(self, version: str, what_worked: List[str],
                            what_didnt: List[str], improvements: List[str]):
        """Create version retrospective."""
        retro = {
            "version": version,
            "created_at": datetime.now().isoformat(),
            "what_worked": what_worked,
            "what_didnt": what_didnt,
            "improvements": improvements,
            "domain": self.project.get("domain", "general")
        }

        retro_file = self.devflow / "knowledge" / "retrospectives" / f"v{version}_retro.json"
        with open(retro_file, "w") as f:
            json.dump(retro, f, indent=2)

        # Extract patterns from what worked
        for item in what_worked:
            self.add_pattern(
                name=f"Success from v{version}",
                description=item,
                context=f"Learned from version {version}",
                category="retrospective",
                confidence=0.9
            )

        # Extract anti-patterns from what didn't work
        for item in what_didnt:
            if improvements:
                self.add_anti_pattern(
                    name=f"Issue from v{version}",
                    description=item,
                    consequence="Caused delays or issues",
                    alternative=improvements[0] if improvements else "TBD",
                    category="retrospective"
                )

        print(f"Created retrospective for v{version}")
        return retro

    def query(self, query: str, category: str = None) -> Dict:
        """Query knowledge base."""
        results = {
            "patterns": [],
            "anti_patterns": [],
            "insights": []
        }

        query_lower = query.lower()

        # Search patterns
        for pattern in self.knowledge["patterns"]:
            if query_lower in pattern["name"].lower() or \
               query_lower in pattern["description"].lower():
                if category is None or pattern["category"] == category:
                    results["patterns"].append(pattern)

        # Search anti-patterns
        for anti in self.knowledge["anti_patterns"]:
            if query_lower in anti["name"].lower() or \
               query_lower in anti["description"].lower():
                if category is None or anti["category"] == category:
                    results["anti_patterns"].append(anti)

        # Search domain insights
        domain = self.project.get("domain", "general")
        if domain in self.knowledge["domain_insights"]:
            for insight in self.knowledge["domain_insights"][domain]:
                if query_lower in insight["insight"].lower():
                    results["insights"].append(insight)

        return results

    def get_recommendations(self) -> Dict:
        """Get recommendations based on accumulated knowledge."""
        domain = self.project.get("domain", "general")

        recommendations = {
            "patterns_to_apply": [],
            "anti_patterns_to_avoid": [],
            "domain_insights": []
        }

        # Get top patterns by confidence and usage
        patterns = sorted(
            self.knowledge["patterns"],
            key=lambda p: p["confidence"] * p.get("usage_count", 1),
            reverse=True
        )[:5]
        recommendations["patterns_to_apply"] = patterns

        # Get relevant anti-patterns
        recommendations["anti_patterns_to_avoid"] = self.knowledge["anti_patterns"][:5]

        # Get domain insights
        if domain in self.knowledge["domain_insights"]:
            recommendations["domain_insights"] = self.knowledge["domain_insights"][domain][:5]

        return recommendations

    def generate_self_upgrade_suggestions(self) -> List[Dict]:
        """Analyze workflow and suggest improvements."""
        suggestions = []

        # Analyze pattern usage
        patterns = self.knowledge["patterns"]
        if len(patterns) < 5:
            suggestions.append({
                "area": "Knowledge Collection",
                "suggestion": "Extract more patterns from research and analysis",
                "priority": "high"
            })

        # Check source credibility tracking
        if len(self.knowledge["source_credibility"]) < 10:
            suggestions.append({
                "area": "Source Quality",
                "suggestion": "Rate more sources for better research quality",
                "priority": "medium"
            })

        # Check retrospectives
        retro_dir = self.devflow / "knowledge" / "retrospectives"
        if retro_dir.exists():
            retros = list(retro_dir.glob("*.json"))
            if len(retros) == 0:
                suggestions.append({
                    "area": "Learning",
                    "suggestion": "Create retrospectives to capture learnings",
                    "priority": "high"
                })

        return suggestions

def main():
    if len(sys.argv) < 2:
        print("Usage: knowledge_base.py <command> [args]")
        print("Commands: pattern, anti-pattern, insight, retro, query, recommend, suggest")
        sys.exit(1)

    kb = KnowledgeBase()
    cmd = sys.argv[1]

    if cmd == "pattern":
        if len(sys.argv) < 5:
            print("Usage: knowledge_base.py pattern '<name>' '<description>' '<context>'")
            sys.exit(1)
        kb.add_pattern(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "anti-pattern":
        if len(sys.argv) < 6:
            print("Usage: knowledge_base.py anti-pattern '<name>' '<desc>' '<consequence>' '<alternative>'")
            sys.exit(1)
        kb.add_anti_pattern(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "insight":
        if len(sys.argv) < 4:
            print("Usage: knowledge_base.py insight '<insight>' '<source>'")
            sys.exit(1)
        kb.add_domain_insight(sys.argv[2], sys.argv[3])
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("Usage: knowledge_base.py query '<search_term>'")
            sys.exit(1)
        results = kb.query(sys.argv[2])
        print(json.dumps(results, indent=2))
    elif cmd == "recommend":
        recommendations = kb.get_recommendations()
        print(json.dumps(recommendations, indent=2))
    elif cmd == "suggest":
        suggestions = kb.generate_self_upgrade_suggestions()
        print(json.dumps(suggestions, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
