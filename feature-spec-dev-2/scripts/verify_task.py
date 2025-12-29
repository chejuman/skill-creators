#!/usr/bin/env python3
"""
Task Verifier for Feature Spec Dev 2
Verifies task completion before providing next task.

Usage:
    python3 verify_task.py --task TASK-001
    python3 verify_task.py --task TASK-001 --project-path ./my-project
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"


def get_docs_path(base_path: str = ".") -> Path:
    return Path(base_path) / SPEC_DOCS_DIR


def load_task(task_id: str, base_path: str = ".") -> Optional[dict]:
    """Load task details from task file."""
    task_path = get_docs_path(base_path) / "tasks" / f"{task_id}.md"

    if not task_path.exists():
        return None

    with open(task_path) as f:
        content = f.read()

    # Parse task metadata and acceptance criteria
    task = {
        "id": task_id,
        "content": content,
        "files": [],
        "acceptance_criteria": [],
        "status": "pending"
    }

    # Extract files to create/modify
    files_match = re.search(r"## Files to Create/Modify\n\n(.*?)\n\n##", content, re.DOTALL)
    if files_match:
        file_lines = files_match.group(1).split("\n")
        for line in file_lines:
            if "|" in line and "File" not in line and "---" not in line:
                parts = line.split("|")
                if len(parts) >= 2:
                    file_path = parts[1].strip().strip("`")
                    if file_path:
                        task["files"].append(file_path)

    # Extract acceptance criteria
    criteria_match = re.search(r"## Acceptance Criteria\n\n(.*?)(?:\n\n##|$)", content, re.DOTALL)
    if criteria_match:
        criteria_lines = criteria_match.group(1).split("\n")
        for line in criteria_lines:
            if line.strip().startswith("- ["):
                checked = "[x]" in line.lower()
                text = re.sub(r"- \[.\] ", "", line.strip())
                task["acceptance_criteria"].append({
                    "text": text,
                    "checked": checked
                })

    return task


def check_files_exist(project_path: str, files: list) -> dict:
    """Check if required files exist in project."""
    project = Path(project_path)
    results = {}

    for file_path in files:
        full_path = project / file_path
        results[file_path] = full_path.exists()

    return results


def verify_task(task_id: str, project_path: str = ".", base_path: str = ".") -> dict:
    """Verify task completion."""
    task = load_task(task_id, base_path)

    if not task:
        return {
            "task_id": task_id,
            "passed": False,
            "error": f"Task {task_id} not found"
        }

    checks = {
        "files_created": check_files_exist(project_path, task["files"]),
        "acceptance_criteria": {
            c["text"]: c["checked"] for c in task["acceptance_criteria"]
        }
    }

    files_ok = all(checks["files_created"].values()) if checks["files_created"] else True
    criteria_ok = all(checks["acceptance_criteria"].values()) if checks["acceptance_criteria"] else True

    passed = files_ok and criteria_ok

    gaps = []
    for file_path, exists in checks["files_created"].items():
        if not exists:
            gaps.append(f"Missing file: {file_path}")

    for criterion, met in checks["acceptance_criteria"].items():
        if not met:
            gaps.append(f"Unmet criterion: {criterion}")

    result = {
        "task_id": task_id,
        "passed": passed,
        "checks": checks,
        "gaps": gaps,
        "verified_at": datetime.now().isoformat()
    }

    # Update verification log
    log_verification(task_id, result, base_path)

    return result


def log_verification(task_id: str, result: dict, base_path: str = "."):
    """Log verification result."""
    log_path = get_docs_path(base_path) / "tracking" / "verification_log.md"

    log_entry = f"""
## {task_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Status:** {"PASSED" if result["passed"] else "FAILED"}

"""

    if result["gaps"]:
        log_entry += "**Gaps:**\n"
        for gap in result["gaps"]:
            log_entry += f"- [ ] {gap}\n"

    log_entry += "\n---\n"

    if log_path.exists():
        with open(log_path, "a") as f:
            f.write(log_entry)
    else:
        with open(log_path, "w") as f:
            f.write("# Verification Log\n\n")
            f.write(log_entry)


def update_task_status(task_id: str, status: str, base_path: str = "."):
    """Update task status in completion_status.json."""
    status_path = get_docs_path(base_path) / "tracking" / "completion_status.json"

    if not status_path.exists():
        return

    with open(status_path) as f:
        data = json.load(f)

    if task_id not in data["tasks"]:
        data["tasks"][task_id] = {}

    data["tasks"][task_id]["status"] = status
    data["tasks"][task_id]["updated_at"] = datetime.now().isoformat()

    # Recalculate summary
    statuses = [t.get("status", "pending") for t in data["tasks"].values()]
    data["summary"] = {
        "total_tasks": len(statuses),
        "completed": statuses.count("completed"),
        "in_progress": statuses.count("in_progress"),
        "pending": statuses.count("pending")
    }
    data["last_updated"] = datetime.now().isoformat()

    with open(status_path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Verify task completion")
    parser.add_argument("--task", required=True, help="Task ID (e.g., TASK-001)")
    parser.add_argument("--project-path", default=".", help="Path to project directory")
    parser.add_argument("--spec-path", default=".", help="Path to .spec-docs")
    parser.add_argument("--update-status", action="store_true", help="Update status based on verification")
    args = parser.parse_args()

    result = verify_task(args.task, args.project_path, args.spec_path)

    if args.update_status:
        if result["passed"]:
            update_task_status(args.task, "completed", args.spec_path)
            result["status_updated"] = "completed"
        else:
            update_task_status(args.task, "pending", args.spec_path)
            result["status_updated"] = "pending (re-added)"

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
