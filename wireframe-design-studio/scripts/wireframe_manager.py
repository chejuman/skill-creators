#!/usr/bin/env python3
"""
Wireframe Manager for Wireframe Design Studio
Manages persistent documentation in .wireframe-docs/ directory.

Usage:
    python3 wireframe_manager.py init --project dashboard
    python3 wireframe_manager.py save --phase design --screen main --file layout.md
    python3 wireframe_manager.py list
    python3 wireframe_manager.py view --screen main
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


WIREFRAME_DOCS_DIR = ".wireframe-docs"


def get_docs_path(base_path: str = ".") -> Path:
    """Get the .wireframe-docs directory path."""
    return Path(base_path) / WIREFRAME_DOCS_DIR


def init_structure(project_name: str, base_path: str = ".") -> dict:
    """Initialize .wireframe-docs directory structure."""
    docs = get_docs_path(base_path)

    directories = [
        docs,
        docs / "discovery",
        docs / "designs",
        docs / "specs",
        docs / "tasks",
        docs / "tracking"
    ]

    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)

    config = {
        "project": project_name,
        "created_at": datetime.now().isoformat(),
        "phases": {
            "discover": "pending",
            "design": "pending",
            "spec": "pending",
            "build": "pending"
        },
        "current_phase": "discover",
        "screens": []
    }

    config_path = docs / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    registry = {
        "project": project_name,
        "wireframes": [],
        "last_updated": datetime.now().isoformat()
    }

    registry_path = docs / "tracking" / "wireframe_registry.json"
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    status = {
        "project": project_name,
        "last_updated": datetime.now().isoformat(),
        "summary": {"total_tasks": 0, "completed": 0, "in_progress": 0, "pending": 0},
        "tasks": {}
    }

    status_path = docs / "tracking" / "completion_status.json"
    with open(status_path, "w") as f:
        json.dump(status, f, indent=2)

    index_content = f"""# Wireframe Documentation Index

**Project:** {project_name}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Phases

- [ ] DISCOVER - Requirements & Research
- [ ] DESIGN - Layout & Wireframes
- [ ] SPEC - Component Specifications
- [ ] BUILD - Implementation Tasks

## Screens

(No screens yet)

## Quick Links

- [Config](config.json)
- [Task Status](tracking/completion_status.json)
- [Wireframe Registry](tracking/wireframe_registry.json)
"""

    index_path = docs / "index.md"
    with open(index_path, "w") as f:
        f.write(index_content)

    return {"status": "initialized", "path": str(docs), "project": project_name}


def register_wireframe(screen_name: str, wireframe_type: str, base_path: str = ".") -> dict:
    """Register a new wireframe in the registry."""
    registry_path = get_docs_path(base_path) / "tracking" / "wireframe_registry.json"

    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = {"wireframes": []}

    wireframe = {
        "id": f"WF-{len(registry['wireframes']) + 1:03d}",
        "screen": screen_name,
        "type": wireframe_type,
        "created_at": datetime.now().isoformat(),
        "status": "draft",
        "files": {
            "layout": f"designs/{screen_name}/layout.md",
            "wireframe": f"designs/{screen_name}/wireframe.md",
            "components": f"designs/{screen_name}/components.md",
            "specs": f"specs/{screen_name}/component_specs.md",
            "a11y": f"specs/{screen_name}/a11y_checklist.md",
            "responsive": f"specs/{screen_name}/responsive.md"
        }
    }

    registry["wireframes"].append(wireframe)
    registry["last_updated"] = datetime.now().isoformat()

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    # Create screen directories
    docs = get_docs_path(base_path)
    (docs / "designs" / screen_name).mkdir(parents=True, exist_ok=True)
    (docs / "specs" / screen_name).mkdir(parents=True, exist_ok=True)

    return wireframe


def list_wireframes(base_path: str = ".") -> list:
    """List all registered wireframes."""
    registry_path = get_docs_path(base_path) / "tracking" / "wireframe_registry.json"

    if not registry_path.exists():
        return []

    with open(registry_path) as f:
        registry = json.load(f)

    return registry.get("wireframes", [])


def get_wireframe(screen_name: str, base_path: str = ".") -> Optional[dict]:
    """Get wireframe by screen name."""
    wireframes = list_wireframes(base_path)

    for wf in wireframes:
        if wf["screen"] == screen_name:
            return wf

    return None


def save_document(phase: str, screen: str, filename: str, content: str, base_path: str = ".") -> dict:
    """Save a document to the appropriate directory."""
    docs = get_docs_path(base_path)

    if phase == "discovery":
        target = docs / "discovery" / filename
    elif phase == "design":
        target = docs / "designs" / screen / filename
    elif phase == "spec":
        target = docs / "specs" / screen / filename
    elif phase == "task":
        target = docs / "tasks" / filename
    else:
        raise ValueError(f"Unknown phase: {phase}")

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "w") as f:
        f.write(content)

    return {"status": "saved", "path": str(target), "size": len(content)}


def format_wireframes_list(wireframes: list) -> str:
    """Format wireframes list as markdown."""
    if not wireframes:
        return "No wireframes found."

    output = "# Wireframe Registry\n\n"
    output += "| ID | Screen | Type | Status | Created |\n"
    output += "|----|--------|------|--------|--------|\n"

    for wf in wireframes:
        created = wf["created_at"][:10]
        output += f"| {wf['id']} | {wf['screen']} | {wf['type']} | {wf['status']} | {created} |\n"

    return output


def main():
    parser = argparse.ArgumentParser(description="Manage wireframe documentation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize wireframe docs")
    init_parser.add_argument("--project", required=True, help="Project name")
    init_parser.add_argument("--path", default=".", help="Base path")

    register_parser = subparsers.add_parser("register", help="Register new wireframe")
    register_parser.add_argument("--screen", required=True, help="Screen name")
    register_parser.add_argument("--type", default="dashboard", help="Wireframe type")
    register_parser.add_argument("--path", default=".", help="Base path")

    list_parser = subparsers.add_parser("list", help="List all wireframes")
    list_parser.add_argument("--path", default=".", help="Base path")
    list_parser.add_argument("--format", choices=["json", "markdown"], default="markdown")

    view_parser = subparsers.add_parser("view", help="View wireframe")
    view_parser.add_argument("--screen", required=True, help="Screen name")
    view_parser.add_argument("--path", default=".", help="Base path")

    save_parser = subparsers.add_parser("save", help="Save document")
    save_parser.add_argument("--phase", required=True, help="Phase")
    save_parser.add_argument("--screen", default="", help="Screen name")
    save_parser.add_argument("--file", required=True, help="Filename")
    save_parser.add_argument("--content", required=True, help="Content")
    save_parser.add_argument("--path", default=".", help="Base path")

    args = parser.parse_args()

    if args.command == "init":
        result = init_structure(args.project, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "register":
        result = register_wireframe(args.screen, args.type, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "list":
        wireframes = list_wireframes(args.path)
        if args.format == "json":
            print(json.dumps(wireframes, indent=2))
        else:
            print(format_wireframes_list(wireframes))
    elif args.command == "view":
        wireframe = get_wireframe(args.screen, args.path)
        if wireframe:
            print(json.dumps(wireframe, indent=2))
        else:
            print(f"Wireframe not found: {args.screen}")
    elif args.command == "save":
        result = save_document(args.phase, args.screen, args.file, args.content, args.path)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
