#!/usr/bin/env python3
"""Self-upgrade system - workflow effectiveness analysis and improvement."""

import json
import sys
from pathlib import Path
from datetime import datetime

DEVFLOW_DIR = ".devflow"

def get_devflow_path():
    return Path.cwd() / DEVFLOW_DIR

def load_metrics():
    """Load workflow metrics."""
    devflow = get_devflow_path()
    metrics_file = devflow / "meta" / "workflow_metrics.json"

    if not metrics_file.exists():
        return {
            "cycles_completed": 0,
            "features_planned": 0,
            "research_sessions": 0,
            "last_upgrade": None,
            "effectiveness_scores": [],
            "improvement_history": []
        }

    with open(metrics_file) as f:
        return json.load(f)

def save_metrics(metrics: dict):
    """Save workflow metrics."""
    devflow = get_devflow_path()
    with open(devflow / "meta" / "workflow_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

def analyze_effectiveness():
    """Analyze workflow effectiveness and identify gaps."""
    devflow = get_devflow_path()
    metrics = load_metrics()

    analysis = {
        "timestamp": datetime.now().isoformat(),
        "findings": [],
        "gaps": [],
        "suggestions": []
    }

    # Check research coverage
    research_dir = devflow / "research"
    if research_dir.exists():
        research_files = list(research_dir.glob("*.md"))
        expected = ["tech_stack.md", "market_trends.md", "open_source.md",
                   "security.md", "competitors.md"]
        missing = [f for f in expected if not (research_dir / f).exists()]

        if missing:
            analysis["gaps"].append({
                "area": "research",
                "missing": missing,
                "suggestion": f"Run research for: {', '.join(missing)}"
            })

    # Check feature backlog health
    backlog_file = devflow / "features" / "backlog.json"
    if backlog_file.exists():
        with open(backlog_file) as f:
            backlog = json.load(f)

        features = backlog.get("features", [])

        # Check for unscored features
        unscored = [f for f in features if f.get("rice_score", 0) == 0]
        if unscored:
            analysis["gaps"].append({
                "area": "scoring",
                "count": len(unscored),
                "suggestion": "Score pending features with RICE methodology"
            })

        # Check MoSCoW distribution
        moscow_dist = {}
        for f in features:
            m = f.get("moscow", "unset")
            moscow_dist[m] = moscow_dist.get(m, 0) + 1

        if not moscow_dist.get("must"):
            analysis["suggestions"].append("Define Must-have features for next version")

    # Check version progress
    project_file = devflow / "project.json"
    if project_file.exists():
        with open(project_file) as f:
            project = json.load(f)

        current = float(project.get("current_version", "0.0"))
        target = float(project.get("target_version", "10.0"))

        if current < target:
            progress = (current / target) * 100
            analysis["findings"].append(f"Progress: {progress:.1f}% toward v{target}")

            if progress < 10:
                analysis["suggestions"].append("Focus on MVP (v1.0) - define core features only")
            elif progress < 50:
                analysis["suggestions"].append("Build momentum - complete 1-2 versions quickly")

    # Calculate effectiveness score
    score = 100
    score -= len(analysis["gaps"]) * 15
    score -= len([s for s in analysis["suggestions"] if "must" in s.lower()]) * 10
    score = max(0, score)
    analysis["effectiveness_score"] = score

    return analysis

def log_upgrade(improvement: str, details: str):
    """Log a workflow improvement."""
    devflow = get_devflow_path()
    log_file = devflow / "meta" / "self_upgrade_log.md"

    with open(log_file, "a") as f:
        f.write(f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')}

### Improvement
{improvement}

### Details
{details}

---
""")

    metrics = load_metrics()
    metrics["last_upgrade"] = datetime.now().isoformat()
    metrics["improvement_history"] = metrics.get("improvement_history", [])
    metrics["improvement_history"].append({
        "date": datetime.now().isoformat(),
        "improvement": improvement
    })
    save_metrics(metrics)

    print(f"Logged improvement: {improvement}")

def generate_upgrade_prompts():
    """Generate prompts for workflow improvement research."""
    analysis = analyze_effectiveness()

    prompts = []

    if analysis["gaps"]:
        for gap in analysis["gaps"]:
            prompts.append({
                "type": "WebSearch",
                "query": f"best practices {gap['area']} software development workflow 2025"
            })

    if analysis["effectiveness_score"] < 70:
        prompts.append({
            "type": "WebSearch",
            "query": "agile product development workflow improvements 2025"
        })

    prompts.append({
        "type": "WebSearch",
        "query": "iterative product development MVP to enterprise best practices"
    })

    return {
        "analysis": analysis,
        "research_prompts": prompts
    }

def show_report():
    """Show self-upgrade analysis report."""
    analysis = analyze_effectiveness()

    print(f"""
# Self-Upgrade Analysis Report

## Effectiveness Score: {analysis['effectiveness_score']}/100

## Findings
""")
    for f in analysis["findings"]:
        print(f"- {f}")

    print("\n## Gaps Identified")
    for g in analysis["gaps"]:
        print(f"- **{g['area']}**: {g.get('suggestion', g)}")

    print("\n## Suggestions")
    for s in analysis["suggestions"]:
        print(f"- {s}")

    print(f"""
## Recommended Actions

1. Address gaps before next version cycle
2. Run WebSearch for improvement research
3. Update workflow based on findings
4. Log improvements to track evolution

---
Generated: {analysis['timestamp']}
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: self_upgrade.py <command> [args]")
        print("Commands: analyze, report, log, prompts")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "analyze":
        analysis = analyze_effectiveness()
        print(json.dumps(analysis, indent=2))
    elif cmd == "report":
        show_report()
    elif cmd == "log":
        if len(sys.argv) < 4:
            print("Usage: self_upgrade.py log '<improvement>' '<details>'")
            sys.exit(1)
        log_upgrade(sys.argv[2], sys.argv[3])
    elif cmd == "prompts":
        result = generate_upgrade_prompts()
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
