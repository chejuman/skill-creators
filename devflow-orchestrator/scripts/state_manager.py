#!/usr/bin/env python3
"""DevFlow state management - persistent project state across versions."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

DEVFLOW_DIR = ".devflow"

def get_devflow_path():
    """Get the .devflow directory path."""
    return Path.cwd() / DEVFLOW_DIR

def init_project(idea: str, domain: str = "general"):
    """Initialize a new DevFlow project."""
    devflow = get_devflow_path()

    if devflow.exists():
        print(f"Error: {DEVFLOW_DIR}/ already exists. Use 'status' to view.")
        sys.exit(1)

    # Create directory structure
    dirs = ["versions", "research", "features", "plans", "meta"]
    for d in dirs:
        (devflow / d).mkdir(parents=True, exist_ok=True)

    # Create project.json
    project = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "idea": idea,
        "domain": domain,
        "current_version": "0.0",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version_history": ["0.0"],
        "target_version": "10.0"
    }

    with open(devflow / "project.json", "w") as f:
        json.dump(project, f, indent=2)

    # Create initial version file
    version_content = f"""# v0.0 - Idea Stage

## Initial Idea
{idea}

## Domain
{domain}

## Created
{datetime.now().isoformat()}

## Status
- [ ] Research phase
- [ ] Feature definition
- [ ] MVP planning
"""
    with open(devflow / "versions" / "v0.0-idea.md", "w") as f:
        f.write(version_content)

    # Initialize feature backlog
    backlog = {"features": [], "last_updated": datetime.now().isoformat()}
    with open(devflow / "features" / "backlog.json", "w") as f:
        json.dump(backlog, f, indent=2)

    # Initialize decisions log
    with open(devflow / "features" / "decisions.md", "w") as f:
        f.write("# Decision Log\n\nAll user decisions recorded here.\n\n")

    # Initialize self-upgrade log
    with open(devflow / "meta" / "self_upgrade_log.md", "w") as f:
        f.write("# Self-Upgrade Log\n\nWorkflow improvements tracked here.\n\n")

    # Initialize metrics
    metrics = {
        "cycles_completed": 0,
        "features_planned": 0,
        "research_sessions": 0,
        "last_upgrade": None
    }
    with open(devflow / "meta" / "workflow_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Initialized DevFlow project: {idea[:50]}...")
    print(f"Domain: {domain}")
    print(f"Version: v0.0 (Idea Stage)")
    print(f"Target: v10.0+")

def get_status():
    """Get current project status."""
    devflow = get_devflow_path()

    if not devflow.exists():
        print("No DevFlow project found. Run 'init' first.")
        sys.exit(1)

    with open(devflow / "project.json") as f:
        project = json.load(f)

    with open(devflow / "features" / "backlog.json") as f:
        backlog = json.load(f)

    with open(devflow / "meta" / "workflow_metrics.json") as f:
        metrics = json.load(f)

    current = float(project["current_version"])
    target = float(project["target_version"])
    progress = min(100, (current / target) * 100)

    print(f"""
# DevFlow Status

## Project
- **Idea**: {project['idea'][:60]}...
- **Domain**: {project['domain']}
- **Current Version**: v{project['current_version']}
- **Target**: v{project['target_version']}
- **Progress**: {progress:.1f}%

## Metrics
- Cycles Completed: {metrics['cycles_completed']}
- Features Planned: {metrics['features_planned']}
- Research Sessions: {metrics['research_sessions']}

## Features in Backlog
- Total: {len(backlog['features'])}

## Version History
{', '.join(['v' + v for v in project['version_history'][-5:]])}
""")
    return project

def advance_version():
    """Advance to next version."""
    devflow = get_devflow_path()

    if not devflow.exists():
        print("No DevFlow project found.")
        sys.exit(1)

    with open(devflow / "project.json") as f:
        project = json.load(f)

    current = project["current_version"]
    parts = current.split(".")

    if parts[0] == "0":
        new_version = "1.0"  # MVP
    else:
        new_version = f"{int(parts[0]) + 1}.0"

    project["current_version"] = new_version
    project["version_history"].append(new_version)
    project["updated_at"] = datetime.now().isoformat()

    with open(devflow / "project.json", "w") as f:
        json.dump(project, f, indent=2)

    # Create version file
    version_file = devflow / "versions" / f"v{new_version}.md"
    with open(version_file, "w") as f:
        f.write(f"""# v{new_version}

## Created
{datetime.now().isoformat()}

## Features Planned
(To be filled by planning phase)

## Status
- [ ] Research complete
- [ ] Features selected
- [ ] Tasks generated
""")

    print(f"Advanced to v{new_version}")
    return new_version

def save_research(research_type: str, content: str):
    """Save research findings."""
    devflow = get_devflow_path()

    if not devflow.exists():
        print("No DevFlow project found.")
        sys.exit(1)

    filename = f"{research_type}.md"
    filepath = devflow / "research" / filename

    with open(filepath, "w") as f:
        f.write(f"""# {research_type.replace('_', ' ').title()} Research

## Generated
{datetime.now().isoformat()}

{content}
""")

    # Update metrics
    with open(devflow / "meta" / "workflow_metrics.json") as f:
        metrics = json.load(f)
    metrics["research_sessions"] += 1
    with open(devflow / "meta" / "workflow_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Saved research: {filename}")

def log_decision(decision: str, rationale: str):
    """Log a user decision."""
    devflow = get_devflow_path()

    with open(devflow / "features" / "decisions.md", "a") as f:
        f.write(f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Decision**: {decision}

**Rationale**: {rationale}

---
""")
    print(f"Decision logged: {decision[:50]}...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: state_manager.py <command> [args]")
        print("Commands: init, status, advance, save_research, log_decision")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        if len(sys.argv) < 3:
            print("Usage: state_manager.py init '<idea>' [domain]")
            sys.exit(1)
        idea = sys.argv[2]
        domain = sys.argv[3] if len(sys.argv) > 3 else "general"
        init_project(idea, domain)
    elif cmd == "status":
        get_status()
    elif cmd == "advance":
        advance_version()
    elif cmd == "save_research":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py save_research <type> '<content>'")
            sys.exit(1)
        save_research(sys.argv[2], sys.argv[3])
    elif cmd == "log_decision":
        if len(sys.argv) < 4:
            print("Usage: state_manager.py log_decision '<decision>' '<rationale>'")
            sys.exit(1)
        log_decision(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
