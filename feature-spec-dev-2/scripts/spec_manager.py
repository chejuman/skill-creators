#!/usr/bin/env python3
"""
Spec Manager for Feature Spec Dev 2
Manages persistent documentation in .spec-docs/ directory.

Usage:
    python3 spec_manager.py init --feature user-auth
    python3 spec_manager.py save --phase discovery --file intent_analysis.md
    python3 spec_manager.py list
    python3 spec_manager.py view --feature user-auth
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"


def get_docs_path(base_path: str = ".") -> Path:
    return Path(base_path) / SPEC_DOCS_DIR


def init_structure(feature_name: str, base_path: str = ".") -> dict:
    """Initialize .spec-docs directory structure."""
    docs = get_docs_path(base_path)

    directories = [
        docs,
        docs / "discovery",
        docs / "requirements",
        docs / "design",
        docs / "tasks",
        docs / "tracking"
    ]

    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)

    config = {
        "feature": feature_name,
        "created_at": datetime.now().isoformat(),
        "phases": {
            "discover": "pending",
            "analyze": "pending",
            "design": "pending",
            "plan": "pending",
            "verify": "pending"
        },
        "current_phase": "discover"
    }

    config_path = docs / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    status = {
        "feature": feature_name,
        "last_updated": datetime.now().isoformat(),
        "summary": {"total_tasks": 0, "completed": 0, "in_progress": 0, "pending": 0},
        "tasks": {}
    }

    status_path = docs / "tracking" / "completion_status.json"
    with open(status_path, "w") as f:
        json.dump(status, f, indent=2)

    index_content = f"""# Feature Spec Documentation Index

**Feature:** {feature_name}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Phases

- [ ] DISCOVER - Intent analysis + research
- [ ] ANALYZE - Requirements in EARS format
- [ ] DESIGN - Architecture + components
- [ ] PLAN - Task breakdown
- [ ] VERIFY - Implementation verification

## Documents

### Discovery
- [Intent Analysis](discovery/intent_analysis.md)
- [Tech Trends](discovery/tech_trends.md)
- [Case Studies](discovery/case_studies.md)

### Requirements
- [Requirements](requirements/requirements.md)
- [API Research](requirements/api_research.md)

### Design
- [Architecture](design/architecture.md)
- [Components](design/components.md)

### Tasks
- [Task Breakdown](tasks/task_breakdown.md)

### Tracking
- [Completion Status](tracking/completion_status.json)
- [Verification Log](tracking/verification_log.md)
"""

    index_path = docs / "index.md"
    with open(index_path, "w") as f:
        f.write(index_content)

    return {"status": "initialized", "path": str(docs), "feature": feature_name}


def update_phase(phase: str, status: str, base_path: str = ".") -> dict:
    """Update phase status."""
    config_path = get_docs_path(base_path) / "config.json"

    if not config_path.exists():
        return {"error": "Project not initialized"}

    with open(config_path) as f:
        config = json.load(f)

    config["phases"][phase] = status
    if status == "in_progress":
        config["current_phase"] = phase

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    return {"phase": phase, "status": status}


def save_document(phase: str, filename: str, content: str, base_path: str = ".") -> dict:
    """Save a document to the appropriate directory."""
    docs = get_docs_path(base_path)

    phase_dirs = {
        "discovery": docs / "discovery",
        "requirements": docs / "requirements",
        "design": docs / "design",
        "tasks": docs / "tasks",
        "tracking": docs / "tracking"
    }

    if phase not in phase_dirs:
        raise ValueError(f"Unknown phase: {phase}")

    target = phase_dirs[phase] / filename
    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "w") as f:
        f.write(content)

    return {"status": "saved", "path": str(target), "size": len(content)}


def get_config(base_path: str = ".") -> Optional[dict]:
    """Get project configuration."""
    config_path = get_docs_path(base_path) / "config.json"

    if not config_path.exists():
        return None

    with open(config_path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Manage spec documentation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize spec docs")
    init_parser.add_argument("--feature", required=True, help="Feature name")
    init_parser.add_argument("--path", default=".", help="Base path")

    phase_parser = subparsers.add_parser("phase", help="Update phase status")
    phase_parser.add_argument("--name", required=True, help="Phase name")
    phase_parser.add_argument("--status", required=True, help="Status")
    phase_parser.add_argument("--path", default=".", help="Base path")

    save_parser = subparsers.add_parser("save", help="Save document")
    save_parser.add_argument("--phase", required=True, help="Phase")
    save_parser.add_argument("--file", required=True, help="Filename")
    save_parser.add_argument("--content", required=True, help="Content")
    save_parser.add_argument("--path", default=".", help="Base path")

    config_parser = subparsers.add_parser("config", help="Get configuration")
    config_parser.add_argument("--path", default=".", help="Base path")

    args = parser.parse_args()

    if args.command == "init":
        result = init_structure(args.feature, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "phase":
        result = update_phase(args.name, args.status, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "save":
        result = save_document(args.phase, args.file, args.content, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "config":
        config = get_config(args.path)
        if config:
            print(json.dumps(config, indent=2))
        else:
            print("Not initialized")


if __name__ == "__main__":
    main()
