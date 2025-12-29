#!/usr/bin/env python3
"""
Status Update for Feature Spec Dev
Updates task status and generates progress reports.

Usage:
    python3 update_status.py --task TASK-001 --status completed
    python3 update_status.py --report
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"


def get_spec_docs_path(base_path: str = ".") -> Path:
    """Get the .spec-docs directory path."""
    return Path(base_path) / SPEC_DOCS_DIR


def load_completion_status(base_path: str = ".") -> dict:
    """Load completion status JSON."""
    status_path = get_spec_docs_path(base_path) / "tracking" / "completion_status.json"
    if status_path.exists():
        with open(status_path) as f:
            return json.load(f)
    return {"tasks": {}, "summary": {"total_tasks": 0, "completed": 0, "in_progress": 0, "pending": 0}}


def save_completion_status(status: dict, base_path: str = "."):
    """Save completion status JSON."""
    status_path = get_spec_docs_path(base_path) / "tracking" / "completion_status.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    with open(status_path, "w") as f:
        json.dump(status, f, indent=2)


def update_task_status(task_id: str, status: str, base_path: str = ".") -> dict:
    """Update status for a specific task."""
    completion = load_completion_status(base_path)

    if task_id not in completion["tasks"]:
        completion["tasks"][task_id] = {}

    completion["tasks"][task_id]["status"] = status
    completion["tasks"][task_id]["updated_at"] = datetime.now().isoformat()

    if status == "in_progress":
        completion["tasks"][task_id]["started_at"] = datetime.now().isoformat()
    elif status == "completed":
        completion["tasks"][task_id]["completed_at"] = datetime.now().isoformat()

    # Update summary
    statuses = [t.get("status", "pending") for t in completion["tasks"].values()]
    completion["summary"] = {
        "total_tasks": len(statuses),
        "completed": statuses.count("completed"),
        "in_progress": statuses.count("in_progress"),
        "pending": statuses.count("pending")
    }
    completion["last_updated"] = datetime.now().isoformat()

    save_completion_status(completion, base_path)

    return {
        "task_id": task_id,
        "status": status,
        "summary": completion["summary"]
    }


def get_next_task(base_path: str = ".") -> Optional[str]:
    """Get the next pending task in order."""
    completion = load_completion_status(base_path)
    tasks_dir = get_spec_docs_path(base_path) / "tasks"

    if not tasks_dir.exists():
        return None

    # Get all task files sorted
    task_files = sorted(tasks_dir.glob("TASK-*.md"))

    for task_file in task_files:
        task_id = task_file.stem
        task_status = completion["tasks"].get(task_id, {}).get("status", "pending")
        if task_status == "pending":
            return task_id

    return None


def generate_progress_report(base_path: str = ".") -> str:
    """Generate a progress report."""
    completion = load_completion_status(base_path)
    summary = completion.get("summary", {})

    total = summary.get("total_tasks", 0)
    completed = summary.get("completed", 0)
    in_progress = summary.get("in_progress", 0)
    pending = summary.get("pending", 0)

    progress_pct = (completed / total * 100) if total > 0 else 0

    report = f"""# Implementation Progress Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary

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

    for task_id, task_data in sorted(completion.get("tasks", {}).items()):
        status = task_data.get("status", "pending")
        status_icon = {"completed": "[x]", "in_progress": "[-]", "pending": "[ ]"}.get(status, "[ ]")
        report += f"- {status_icon} **{task_id}**: {status}\n"

    next_task = get_next_task(base_path)
    if next_task:
        report += f"\n## Next Task\n\n**{next_task}** is ready to start.\n"
    elif completed == total and total > 0:
        report += "\n## Status\n\nAll tasks completed!\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Update task status")
    parser.add_argument("--task", help="Task ID (e.g., TASK-001)")
    parser.add_argument("--status", choices=["pending", "in_progress", "completed"], help="New status")
    parser.add_argument("--path", default=".", help="Base path")
    parser.add_argument("--report", action="store_true", help="Generate progress report")
    parser.add_argument("--next", action="store_true", help="Get next pending task")
    args = parser.parse_args()

    if args.report:
        print(generate_progress_report(args.path))
    elif args.next:
        next_task = get_next_task(args.path)
        if next_task:
            print(f"Next task: {next_task}")
        else:
            print("No pending tasks")
    elif args.task and args.status:
        result = update_task_status(args.task, args.status, args.path)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
