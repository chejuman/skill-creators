#!/usr/bin/env python3
"""Feature scoring engine - RICE and MoSCoW prioritization."""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

DEVFLOW_DIR = ".devflow"

class Feature:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.reach = 0
        self.impact = 1.0
        self.confidence = 50
        self.effort = 1
        self.moscow = "could"
        self.rice_score = 0

    def calculate_rice(self):
        """Calculate RICE score."""
        self.rice_score = (self.reach * self.impact * (self.confidence / 100)) / self.effort
        return self.rice_score

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "reach": self.reach,
            "impact": self.impact,
            "confidence": self.confidence,
            "effort": self.effort,
            "moscow": self.moscow,
            "rice_score": self.rice_score
        }

def load_backlog() -> List[Dict]:
    """Load feature backlog."""
    devflow = Path.cwd() / DEVFLOW_DIR
    backlog_file = devflow / "features" / "backlog.json"

    if not backlog_file.exists():
        return []

    with open(backlog_file) as f:
        data = json.load(f)
    return data.get("features", [])

def save_backlog(features: List[Dict]):
    """Save feature backlog."""
    devflow = Path.cwd() / DEVFLOW_DIR
    backlog_file = devflow / "features" / "backlog.json"

    data = {
        "features": features,
        "last_updated": datetime.now().isoformat()
    }

    with open(backlog_file, "w") as f:
        json.dump(data, f, indent=2)

def add_feature(name: str, description: str, reach: int = 100,
                impact: float = 1.0, confidence: int = 50,
                effort: int = 1, moscow: str = "could"):
    """Add a feature to the backlog with scoring."""
    features = load_backlog()

    feature = {
        "name": name,
        "description": description,
        "reach": reach,
        "impact": impact,
        "confidence": confidence,
        "effort": effort,
        "moscow": moscow,
        "rice_score": (reach * impact * (confidence / 100)) / effort,
        "added_at": datetime.now().isoformat(),
        "status": "proposed"
    }

    features.append(feature)
    save_backlog(features)
    print(f"Added feature: {name} (RICE: {feature['rice_score']:.1f})")

def prioritize_features(target_version: str = None):
    """Prioritize features for a version using RICE + MoSCoW."""
    features = load_backlog()

    if not features:
        print("No features in backlog.")
        return []

    # Sort by MoSCoW priority first, then RICE score
    moscow_order = {"must": 0, "should": 1, "could": 2, "wont": 3}

    sorted_features = sorted(
        features,
        key=lambda f: (moscow_order.get(f.get("moscow", "could"), 2), -f.get("rice_score", 0))
    )

    print(f"# Prioritized Features")
    print()

    for i, f in enumerate(sorted_features[:10], 1):
        moscow = f.get("moscow", "could").upper()
        rice = f.get("rice_score", 0)
        print(f"{i}. [{moscow}] **{f['name']}** (RICE: {rice:.1f})")
        print(f"   {f['description'][:80]}...")
        print()

    return sorted_features

def generate_version_features(version: str, count: int = 5):
    """Generate feature suggestions for a version."""
    features = load_backlog()
    prioritized = prioritize_features()

    must_haves = [f for f in prioritized if f.get("moscow") == "must"]
    should_haves = [f for f in prioritized if f.get("moscow") == "should"]
    could_haves = [f for f in prioritized if f.get("moscow") == "could"]

    selected = []
    selected.extend(must_haves[:2])
    selected.extend(should_haves[:2])
    selected.extend(could_haves[:1])

    devflow = Path.cwd() / DEVFLOW_DIR
    roadmap_file = devflow / "features" / "roadmap.md"

    with open(roadmap_file, "a") as f:
        f.write(f"""
## v{version} Features

| Feature | Priority | RICE | Status |
|---------|----------|------|--------|
""")
        for feat in selected[:count]:
            f.write(f"| {feat['name']} | {feat.get('moscow', 'could').upper()} | {feat.get('rice_score', 0):.1f} | Planned |\n")
        f.write("\n")

    print(f"Generated {len(selected[:count])} features for v{version}")
    return selected[:count]

def show_scoring_guide():
    """Show RICE and MoSCoW scoring guide."""
    print("""
# Feature Scoring Guide

## RICE Score Formula
Score = (Reach × Impact × Confidence) / Effort

### Reach (1-1000)
How many users will this affect per quarter?
- 1-10: Internal/admin feature
- 10-100: Power users
- 100-500: Active users
- 500-1000: All users

### Impact (0.25, 0.5, 1, 2, 3)
What's the effect on each user?
- 0.25: Minimal improvement
- 0.5: Low impact
- 1: Medium impact
- 2: High impact
- 3: Massive impact

### Confidence (0-100%)
How sure are we about estimates?
- 100%: High confidence (data-backed)
- 80%: Medium confidence (some data)
- 50%: Low confidence (gut feeling)

### Effort (1-12)
Person-months required
- 1: Few days
- 2-3: 1-3 weeks
- 4-6: 1-2 months
- 7-12: Quarter+

## MoSCoW Prioritization

- **Must have**: Critical for this version, breaks core functionality if missing
- **Should have**: Important but not vital, can work around
- **Could have**: Nice to have, improves experience
- **Won't have**: Out of scope for this version, consider later

## Combined Scoring

1. First sort by MoSCoW (Must > Should > Could > Won't)
2. Within each category, sort by RICE score
3. Select top features fitting effort budget
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: feature_scorer.py <command> [args]")
        print("Commands: add, list, prioritize, generate, guide")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "add":
        if len(sys.argv) < 4:
            print("Usage: feature_scorer.py add '<name>' '<description>' [reach] [impact] [confidence] [effort] [moscow]")
            sys.exit(1)
        name = sys.argv[2]
        desc = sys.argv[3]
        reach = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        impact = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
        conf = int(sys.argv[6]) if len(sys.argv) > 6 else 50
        effort = int(sys.argv[7]) if len(sys.argv) > 7 else 1
        moscow = sys.argv[8] if len(sys.argv) > 8 else "could"
        add_feature(name, desc, reach, impact, conf, effort, moscow)
    elif cmd == "list":
        features = load_backlog()
        for f in features:
            print(f"- {f['name']}: RICE {f.get('rice_score', 0):.1f}")
    elif cmd == "prioritize":
        prioritize_features()
    elif cmd == "generate":
        version = sys.argv[2] if len(sys.argv) > 2 else "1.0"
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        generate_version_features(version, count)
    elif cmd == "guide":
        show_scoring_guide()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
