#!/usr/bin/env python3
"""
Task Tracker for Wireframe Design Studio
Manages task status, progress tracking, and verification.

Usage:
    python3 task_tracker.py status
    python3 task_tracker.py next
    python3 task_tracker.py update --task TASK-001 --status completed
    python3 task_tracker.py verify --task TASK-001
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


WIREFRAME_DOCS_DIR = ".wireframe-docs"


def get_docs_path(base_path: str = ".") -> Path:
    return Path(base_path) / WIREFRAME_DOCS_DIR


def load_status(base_path: str = ".") -> dict:
    """Load completion status."""
    status_path = get_docs_path(base_path) / "tracking" / "completion_status.json"
    if status_path.exists():
        with open(status_path) as f:
            return json.load(f)
    return {"tasks": {}, "summary": {"total_tasks": 0, "completed": 0, "in_progress": 0, "pending": 0}}


def save_status(status: dict, base_path: str = "."):
    """Save completion status."""
    status_path = get_docs_path(base_path) / "tracking" / "completion_status.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    with open(status_path, "w") as f:
        json.dump(status, f, indent=2)


def update_task_status(task_id: str, new_status: str, base_path: str = ".") -> dict:
    """Update status for a specific task."""
    status = load_status(base_path)

    if task_id not in status["tasks"]:
        status["tasks"][task_id] = {}

    status["tasks"][task_id]["status"] = new_status
    status["tasks"][task_id]["updated_at"] = datetime.now().isoformat()

    if new_status == "in_progress":
        status["tasks"][task_id]["started_at"] = datetime.now().isoformat()
    elif new_status == "completed":
        status["tasks"][task_id]["completed_at"] = datetime.now().isoformat()

    # Update summary
    statuses = [t.get("status", "pending") for t in status["tasks"].values()]
    status["summary"] = {
        "total_tasks": len(statuses),
        "completed": statuses.count("completed"),
        "in_progress": statuses.count("in_progress"),
        "pending": statuses.count("pending")
    }
    status["last_updated"] = datetime.now().isoformat()

    save_status(status, base_path)
    return {"task_id": task_id, "status": new_status, "summary": status["summary"]}


def get_next_task(base_path: str = ".") -> Optional[dict]:
    """Get next pending task."""
    status = load_status(base_path)
    tasks_dir = get_docs_path(base_path) / "tasks"

    if not tasks_dir.exists():
        return None

    task_files = sorted(tasks_dir.glob("TASK-*.md"))

    for task_file in task_files:
        task_id = task_file.stem
        task_status = status["tasks"].get(task_id, {}).get("status", "pending")
        if task_status == "pending":
            return {
                "task_id": task_id,
                "file": str(task_file),
                "status": task_status
            }

    return None


def get_current_task(base_path: str = ".") -> Optional[dict]:
    """Get current in-progress task."""
    status = load_status(base_path)

    for task_id, task_data in status["tasks"].items():
        if task_data.get("status") == "in_progress":
            return {"task_id": task_id, **task_data}

    return None


def verify_task(task_id: str, base_path: str = ".") -> dict:
    """Verify task completion by checking files."""
    task_path = get_docs_path(base_path) / "tasks" / f"{task_id}.md"

    if not task_path.exists():
        return {"passed": False, "message": f"Task file not found: {task_id}"}

    with open(task_path) as f:
        content = f.read()

    # Check acceptance criteria
    criteria_checked = content.count("[x]")
    criteria_total = content.count("[ ]") + criteria_checked

    passed = criteria_total > 0 and criteria_checked == criteria_total

    return {
        "task_id": task_id,
        "passed": passed,
        "criteria_met": criteria_checked,
        "criteria_total": criteria_total,
        "message": "All criteria met" if passed else f"{criteria_total - criteria_checked} criteria remaining"
    }


def generate_status_report(base_path: str = ".") -> str:
    """Generate status report."""
    status = load_status(base_path)
    summary = status.get("summary", {})

    total = summary.get("total_tasks", 0)
    completed = summary.get("completed", 0)
    in_progress = summary.get("in_progress", 0)
    pending = summary.get("pending", 0)

    progress_pct = (completed / total * 100) if total > 0 else 0

    report = f"""# Wireframe Implementation Status

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Progress

| Metric      | Count |
| ----------- | ----- |
| Total Tasks | {total} |
| Completed   | {completed} |
| In Progress | {in_progress} |
| Pending     | {pending} |

**Progress:** {progress_pct:.1f}%

```
[{'=' * int(progress_pct / 5)}{'.' * (20 - int(progress_pct / 5))}] {progress_pct:.1f}%
```

## Task Details

"""

    for task_id, task_data in sorted(status.get("tasks", {}).items()):
        task_status = task_data.get("status", "pending")
        icon = {"completed": "[x]", "in_progress": "[-]", "pending": "[ ]"}.get(task_status, "[ ]")
        report += f"- {icon} **{task_id}**: {task_status}\n"

    current = get_current_task(base_path)
    if current:
        report += f"\n## Current Task\n\n**{current['task_id']}** (in progress)\n"

    next_task = get_next_task(base_path)
    if next_task:
        report += f"\n## Next Task\n\n**{next_task['task_id']}** is ready to start.\n"
    elif completed == total and total > 0:
        report += "\n## Status\n\nAll tasks completed!\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Track wireframe tasks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Show status report")
    status_parser.add_argument("--path", default=".", help="Base path")
    status_parser.add_argument("--format", choices=["json", "markdown"], default="markdown")

    next_parser = subparsers.add_parser("next", help="Get next task")
    next_parser.add_argument("--path", default=".", help="Base path")

    current_parser = subparsers.add_parser("current", help="Get current task")
    current_parser.add_argument("--path", default=".", help="Base path")

    update_parser = subparsers.add_parser("update", help="Update task status")
    update_parser.add_argument("--task", required=True, help="Task ID")
    update_parser.add_argument("--status", required=True, choices=["pending", "in_progress", "completed"])
    update_parser.add_argument("--path", default=".", help="Base path")

    verify_parser = subparsers.add_parser("verify", help="Verify task completion")
    verify_parser.add_argument("--task", required=True, help="Task ID")
    verify_parser.add_argument("--path", default=".", help="Base path")

    args = parser.parse_args()

    if args.command == "status":
        if args.format == "json":
            print(json.dumps(load_status(args.path), indent=2))
        else:
            print(generate_status_report(args.path))
    elif args.command == "next":
        task = get_next_task(args.path)
        if task:
            print(json.dumps(task, indent=2))
        else:
            print("No pending tasks")
    elif args.command == "current":
        task = get_current_task(args.path)
        if task:
            print(json.dumps(task, indent=2))
        else:
            print("No task in progress")
    elif args.command == "update":
        result = update_task_status(args.task, args.status, args.path)
        print(json.dumps(result, indent=2))
    elif args.command == "verify":
        result = verify_task(args.task, args.path)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
