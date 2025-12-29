#!/usr/bin/env python3
"""
Document Manager for Feature Spec Dev
Manages persistent documentation in .spec-docs/ directory.

Usage:
    python3 doc_manager.py init --feature user-auth
    python3 doc_manager.py save --phase discovery --file intent_analysis.md --content "..."
    python3 doc_manager.py index --rebuild
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"

DIRECTORY_STRUCTURE = {
    "discovery": ["intent_analysis.md", "domain_research.md", "tech_context.md", "user_decisions.md"],
    "specs": [],  # Dynamic per feature
    "plans": ["implementation_plan.md", "task_breakdown.md"],
    "tasks": [],  # Dynamic TASK-XXX.md files
    "tracking": ["completion_status.json", "verification_log.md", "gaps_report.md"]
}


def get_spec_docs_path(base_path: str = ".") -> Path:
    """Get the .spec-docs directory path."""
    return Path(base_path) / SPEC_DOCS_DIR


def init_structure(feature_name: str, base_path: str = ".") -> dict:
    """Initialize .spec-docs directory structure for a new feature."""
    spec_docs = get_spec_docs_path(base_path)

    # Create main directories
    directories = [
        spec_docs,
        spec_docs / "discovery",
        spec_docs / "specs" / feature_name,
        spec_docs / "specs" / feature_name / "diagrams",
        spec_docs / "plans",
        spec_docs / "tasks",
        spec_docs / "tracking"
    ]

    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create initial config
    config = {
        "feature": feature_name,
        "created_at": datetime.now().isoformat(),
        "phases": {
            "discovery": "pending",
            "spec": "pending",
            "plan": "pending",
            "implement": "pending"
        },
        "current_phase": "discovery"
    }

    config_path = spec_docs / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # Create initial completion status
    status = {
        "feature": feature_name,
        "last_updated": datetime.now().isoformat(),
        "summary": {
            "total_tasks": 0,
            "completed": 0,
            "in_progress": 0,
            "pending": 0
        },
        "tasks": {}
    }

    status_path = spec_docs / "tracking" / "completion_status.json"
    with open(status_path, "w") as f:
        json.dump(status, f, indent=2)

    # Create index
    index_content = f"""# Feature Spec Documentation Index

**Feature:** {feature_name}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Documents

### Discovery Phase
- [Intent Analysis](discovery/intent_analysis.md)
- [Domain Research](discovery/domain_research.md)
- [Tech Context](discovery/tech_context.md)
- [User Decisions](discovery/user_decisions.md)

### Specification Phase
- [Requirements](specs/{feature_name}/requirements.md)
- [Design](specs/{feature_name}/design.md)

### Planning Phase
- [Implementation Plan](plans/implementation_plan.md)
- [Task Breakdown](plans/task_breakdown.md)

### Tasks
See `tasks/` directory for individual task files.

### Tracking
- [Completion Status](tracking/completion_status.json)
- [Verification Log](tracking/verification_log.md)
"""

    index_path = spec_docs / "index.md"
    with open(index_path, "w") as f:
        f.write(index_content)

    return {
        "status": "initialized",
        "path": str(spec_docs),
        "feature": feature_name
    }


def save_document(phase: str, filename: str, content: str, base_path: str = ".") -> dict:
    """Save a document to the appropriate phase directory."""
    spec_docs = get_spec_docs_path(base_path)

    # Determine target path
    if phase == "discovery":
        target = spec_docs / "discovery" / filename
    elif phase == "specs":
        # Get feature name from config
        config = load_config(base_path)
        feature = config.get("feature", "unknown")
        target = spec_docs / "specs" / feature / filename
    elif phase == "plans":
        target = spec_docs / "plans" / filename
    elif phase == "tasks":
        target = spec_docs / "tasks" / filename
    elif phase == "tracking":
        target = spec_docs / "tracking" / filename
    else:
        raise ValueError(f"Unknown phase: {phase}")

    # Ensure parent directory exists
    target.parent.mkdir(parents=True, exist_ok=True)

    # Save content
    with open(target, "w") as f:
        f.write(content)

    # Update config phase status
    update_phase_status(phase, "in_progress", base_path)

    return {
        "status": "saved",
        "path": str(target),
        "size": len(content)
    }


def load_config(base_path: str = ".") -> dict:
    """Load the config.json file."""
    config_path = get_spec_docs_path(base_path) / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def update_phase_status(phase: str, status: str, base_path: str = "."):
    """Update the status of a phase in config."""
    config = load_config(base_path)
    if "phases" not in config:
        config["phases"] = {}
    config["phases"][phase] = status
    config["current_phase"] = phase

    config_path = get_spec_docs_path(base_path) / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def rebuild_index(base_path: str = ".") -> dict:
    """Rebuild the index.md file based on existing documents."""
    spec_docs = get_spec_docs_path(base_path)
    config = load_config(base_path)
    feature = config.get("feature", "unknown")

    # Collect all documents
    docs = []

    for phase_dir in ["discovery", "plans", "tracking"]:
        phase_path = spec_docs / phase_dir
        if phase_path.exists():
            for file in phase_path.glob("*.md"):
                docs.append({
                    "phase": phase_dir,
                    "name": file.stem,
                    "path": str(file.relative_to(spec_docs))
                })

    # Specs
    specs_path = spec_docs / "specs" / feature
    if specs_path.exists():
        for file in specs_path.glob("*.md"):
            docs.append({
                "phase": "specs",
                "name": file.stem,
                "path": str(file.relative_to(spec_docs))
            })

    # Tasks
    tasks_path = spec_docs / "tasks"
    if tasks_path.exists():
        for file in sorted(tasks_path.glob("TASK-*.md")):
            docs.append({
                "phase": "tasks",
                "name": file.stem,
                "path": str(file.relative_to(spec_docs))
            })

    # Generate index content
    index_content = f"""# Feature Spec Documentation Index

**Feature:** {feature}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Total Documents:** {len(docs)}

## Documents by Phase

"""

    for phase in ["discovery", "specs", "plans", "tasks", "tracking"]:
        phase_docs = [d for d in docs if d["phase"] == phase]
        if phase_docs:
            index_content += f"### {phase.title()}\n\n"
            for doc in phase_docs:
                index_content += f"- [{doc['name']}]({doc['path']})\n"
            index_content += "\n"

    index_path = spec_docs / "index.md"
    with open(index_path, "w") as f:
        f.write(index_content)

    return {
        "status": "rebuilt",
        "documents": len(docs)
    }


def main():
    parser = argparse.ArgumentParser(description="Manage spec documentation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize spec docs structure")
    init_parser.add_argument("--feature", required=True, help="Feature name")
    init_parser.add_argument("--path", default=".", help="Base path")

    # Save command
    save_parser = subparsers.add_parser("save", help="Save a document")
    save_parser.add_argument("--phase", required=True, help="Phase (discovery, specs, plans, tasks, tracking)")
    save_parser.add_argument("--file", required=True, help="Filename")
    save_parser.add_argument("--content", required=True, help="Content to save")
    save_parser.add_argument("--path", default=".", help="Base path")

    # Index command
    index_parser = subparsers.add_parser("index", help="Rebuild index")
    index_parser.add_argument("--rebuild", action="store_true", help="Rebuild index")
    index_parser.add_argument("--path", default=".", help="Base path")

    args = parser.parse_args()

    if args.command == "init":
        result = init_structure(args.feature, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "save":
        result = save_document(args.phase, args.file, args.content, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "index":
        if args.rebuild:
            result = rebuild_index(args.path)
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
