#!/usr/bin/env python3
"""
Action Tracker for Retrospective V2
Tracks and manages action items from retrospectives.

Usage:
    python3 action_tracker.py --add "Action description" --priority high --owner "Team Lead"
    python3 action_tracker.py --list [--status pending|completed|all]
    python3 action_tracker.py --complete ACTION_ID
    python3 action_tracker.py --export [--format json|markdown]
"""

import json
import argparse
import os
from datetime import datetime
from pathlib import Path

# Default storage location
ACTIONS_FILE = Path.home() / ".claude" / "retrospective-actions.json"


def load_actions() -> dict:
    """Load actions from storage."""
    if ACTIONS_FILE.exists():
        with open(ACTIONS_FILE, "r") as f:
            return json.load(f)
    return {"actions": [], "last_updated": None}


def save_actions(data: dict):
    """Save actions to storage."""
    ACTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    with open(ACTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_id(actions: list) -> str:
    """Generate unique action ID."""
    existing_ids = {a["id"] for a in actions}
    counter = 1
    while f"ACT-{counter:03d}" in existing_ids:
        counter += 1
    return f"ACT-{counter:03d}"


def add_action(description: str, priority: str, owner: str, category: str, retro_date: str = None):
    """Add a new action item."""
    data = load_actions()
    action = {
        "id": generate_id(data["actions"]),
        "description": description,
        "priority": priority,
        "owner": owner,
        "category": category,
        "status": "pending",
        "created": datetime.now().isoformat(),
        "retro_date": retro_date or datetime.now().strftime("%Y-%m-%d"),
        "completed_at": None
    }
    data["actions"].append(action)
    save_actions(data)
    print(f"Added: {action['id']} - {description}")
    return action


def list_actions(status: str = "all"):
    """List action items."""
    data = load_actions()
    actions = data["actions"]

    if status != "all":
        actions = [a for a in actions if a["status"] == status]

    if not actions:
        print("No actions found.")
        return

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    actions.sort(key=lambda x: priority_order.get(x["priority"], 99))

    print("\n# Action Items\n")
    print("| ID | Description | Priority | Owner | Status | Created |")
    print("|-----|-------------|----------|-------|--------|---------|")

    for a in actions:
        status_icon = "[ ]" if a["status"] == "pending" else "[x]"
        print(f"| {a['id']} | {a['description'][:40]} | {a['priority']} | {a['owner']} | {status_icon} | {a['created'][:10]} |")


def complete_action(action_id: str):
    """Mark an action as completed."""
    data = load_actions()
    for action in data["actions"]:
        if action["id"] == action_id:
            action["status"] = "completed"
            action["completed_at"] = datetime.now().isoformat()
            save_actions(data)
            print(f"Completed: {action_id}")
            return
    print(f"Action not found: {action_id}")


def export_actions(fmt: str = "markdown"):
    """Export actions to file."""
    data = load_actions()

    if fmt == "json":
        output = json.dumps(data, indent=2, ensure_ascii=False)
        filename = "retrospective-actions.json"
    else:
        lines = [
            "# Retrospective Action Items",
            f"*Last updated: {data.get('last_updated', 'N/A')[:10]}*",
            "",
            "## Pending",
            ""
        ]
        pending = [a for a in data["actions"] if a["status"] == "pending"]
        for a in pending:
            lines.append(f"- [ ] **{a['id']}** ({a['priority']}): {a['description']} - @{a['owner']}")

        lines.extend(["", "## Completed", ""])
        completed = [a for a in data["actions"] if a["status"] == "completed"]
        for a in completed:
            lines.append(f"- [x] **{a['id']}**: {a['description']} (completed {a['completed_at'][:10]})")

        output = "\n".join(lines)
        filename = "retrospective-actions.md"

    with open(filename, "w") as f:
        f.write(output)
    print(f"Exported to {filename}")


def get_stats():
    """Show action statistics."""
    data = load_actions()
    actions = data["actions"]

    pending = len([a for a in actions if a["status"] == "pending"])
    completed = len([a for a in actions if a["status"] == "completed"])
    high_priority = len([a for a in actions if a["priority"] == "high" and a["status"] == "pending"])

    print("\n# Action Statistics\n")
    print(f"- Total: {len(actions)}")
    print(f"- Pending: {pending}")
    print(f"- Completed: {completed}")
    print(f"- High Priority Pending: {high_priority}")

    if actions:
        completion_rate = completed / len(actions) * 100
        print(f"- Completion Rate: {completion_rate:.1f}%")


def main():
    parser = argparse.ArgumentParser(description="Track retrospective action items")
    parser.add_argument("--add", help="Add new action (description)")
    parser.add_argument("--priority", choices=["high", "medium", "low"], default="medium")
    parser.add_argument("--owner", default="Team")
    parser.add_argument("--category", choices=["process", "technical", "team"], default="process")
    parser.add_argument("--list", action="store_true", help="List actions")
    parser.add_argument("--status", choices=["pending", "completed", "all"], default="all")
    parser.add_argument("--complete", help="Complete action by ID")
    parser.add_argument("--export", action="store_true", help="Export actions")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--stats", action="store_true", help="Show statistics")

    args = parser.parse_args()

    if args.add:
        add_action(args.add, args.priority, args.owner, args.category)
    elif args.list:
        list_actions(args.status)
    elif args.complete:
        complete_action(args.complete)
    elif args.export:
        export_actions(args.format)
    elif args.stats:
        get_stats()
    else:
        list_actions()


if __name__ == "__main__":
    main()
