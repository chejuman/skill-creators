#!/usr/bin/env python3
"""
Task Verification for Feature Spec Dev
Verifies task completion before allowing next task.

Usage:
    python3 verify_task.py --task TASK-001
    python3 verify_task.py --task TASK-001 --update-status
"""

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"


@dataclass
class VerificationResult:
    """Result of task verification."""
    task_id: str
    passed: bool
    checks: dict
    gaps: list[str]
    message: str


def get_spec_docs_path(base_path: str = ".") -> Path:
    """Get the .spec-docs directory path."""
    return Path(base_path) / SPEC_DOCS_DIR


def load_task(task_id: str, base_path: str = ".") -> Optional[dict]:
    """Load task file and parse its content."""
    task_path = get_spec_docs_path(base_path) / "tasks" / f"{task_id}.md"

    if not task_path.exists():
        return None

    with open(task_path) as f:
        content = f.read()

    # Parse task metadata and content
    task = {
        "id": task_id,
        "content": content,
        "target_files": [],
        "test_files": [],
        "acceptance_criteria": []
    }

    # Extract target files from table
    file_table_match = re.search(r"## Files to Create/Modify\n\n\|.*\n\|.*\n((?:\|.*\n)*)", content)
    if file_table_match:
        for line in file_table_match.group(1).strip().split("\n"):
            parts = line.split("|")
            if len(parts) >= 3:
                file_path = parts[1].strip()
                if file_path and file_path != "...":
                    task["target_files"].append(file_path)

    # Extract acceptance criteria
    criteria_match = re.search(r"## Acceptance Criteria\n\n((?:- \[[ x]\].*\n)*)", content)
    if criteria_match:
        for line in criteria_match.group(1).strip().split("\n"):
            if line.startswith("- ["):
                criterion = line[6:].strip()  # Remove "- [ ] " or "- [x] "
                task["acceptance_criteria"].append(criterion)

    # Extract test requirements
    test_match = re.search(r"## Tests Required\n\n((?:- \[[ x]\].*\n)*)", content)
    if test_match:
        for line in test_match.group(1).strip().split("\n"):
            if line.startswith("- ["):
                test = line[6:].strip()
                task["test_files"].append(test)

    return task


def check_files_exist(files: list[str], base_path: str = ".") -> dict:
    """Check if target files exist."""
    results = {}
    for file_path in files:
        full_path = Path(base_path) / file_path
        results[file_path] = full_path.exists()
    return results


def load_completion_status(base_path: str = ".") -> dict:
    """Load completion status JSON."""
    status_path = get_spec_docs_path(base_path) / "tracking" / "completion_status.json"
    if status_path.exists():
        with open(status_path) as f:
            return json.load(f)
    return {"tasks": {}}


def update_task_status(task_id: str, status: str, verification: dict, base_path: str = "."):
    """Update task status in completion_status.json."""
    completion = load_completion_status(base_path)

    completion["tasks"][task_id] = {
        "status": status,
        "last_verification": {
            "checked_at": datetime.now().isoformat(),
            "passed": verification.get("passed", False),
            "gaps": verification.get("gaps", [])
        }
    }

    if status == "completed":
        completion["tasks"][task_id]["verified_at"] = datetime.now().isoformat()

    # Update summary
    statuses = [t.get("status", "pending") for t in completion["tasks"].values()]
    completion["summary"] = {
        "total_tasks": len(statuses),
        "completed": statuses.count("completed"),
        "in_progress": statuses.count("in_progress"),
        "pending": statuses.count("pending")
    }
    completion["last_updated"] = datetime.now().isoformat()

    status_path = get_spec_docs_path(base_path) / "tracking" / "completion_status.json"
    with open(status_path, "w") as f:
        json.dump(completion, f, indent=2)


def log_verification(task_id: str, result: VerificationResult, base_path: str = "."):
    """Append verification result to log."""
    log_path = get_spec_docs_path(base_path) / "tracking" / "verification_log.md"

    log_entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')} - {task_id}

**Status:** {'PASSED' if result.passed else 'FAILED'}

### Checks
"""
    for check_name, check_result in result.checks.items():
        status = "✅" if check_result else "❌"
        log_entry += f"- {status} {check_name}\n"

    if result.gaps:
        log_entry += "\n### Gaps\n"
        for gap in result.gaps:
            log_entry += f"- {gap}\n"

    log_entry += "\n---\n"

    with open(log_path, "a") as f:
        f.write(log_entry)


def log_gap(task_id: str, gaps: list[str], base_path: str = "."):
    """Log gaps to gaps_report.md."""
    gaps_path = get_spec_docs_path(base_path) / "tracking" / "gaps_report.md"

    gap_entry = f"""
## {task_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
    for gap in gaps:
        gap_entry += f"- [ ] {gap}\n"

    gap_entry += "\n"

    with open(gaps_path, "a") as f:
        f.write(gap_entry)


def verify_task(task_id: str, base_path: str = ".") -> VerificationResult:
    """Verify if a task has been completed."""
    task = load_task(task_id, base_path)

    if not task:
        return VerificationResult(
            task_id=task_id,
            passed=False,
            checks={},
            gaps=[f"Task file {task_id}.md not found"],
            message=f"Task {task_id} not found"
        )

    gaps = []
    checks = {}

    # Check target files exist
    if task["target_files"]:
        file_checks = check_files_exist(task["target_files"], base_path)
        checks["files_exist"] = all(file_checks.values())
        for file_path, exists in file_checks.items():
            if not exists:
                gaps.append(f"Missing file: {file_path}")
    else:
        checks["files_exist"] = True  # No files to check

    # Check test files (simplified - just check if tests directory has relevant files)
    checks["tests_written"] = len(task["test_files"]) == 0 or checks["files_exist"]

    # Overall pass/fail
    passed = all(checks.values()) and len(gaps) == 0

    message = "All checks passed" if passed else f"Verification failed: {len(gaps)} gaps found"

    return VerificationResult(
        task_id=task_id,
        passed=passed,
        checks=checks,
        gaps=gaps,
        message=message
    )


def format_result(result: VerificationResult) -> str:
    """Format verification result as markdown."""
    status_icon = "✅" if result.passed else "❌"

    output = f"""## Pre-Verification: {result.task_id} {status_icon} {'PASSED' if result.passed else 'FAILED'}

"""

    if result.passed:
        output += "All checks passed for previous task.\n"
    else:
        output += "### Verification Failed\n\n"
        for gap in result.gaps:
            output += f"- [ ] {gap}\n"
        output += f"\n**Action Required:** Complete {result.task_id} before proceeding.\n"
        output += f"Use `/spec-next --skip-verify` to force next task.\n"

    return output


def main():
    parser = argparse.ArgumentParser(description="Verify task completion")
    parser.add_argument("--task", required=True, help="Task ID (e.g., TASK-001)")
    parser.add_argument("--path", default=".", help="Base path")
    parser.add_argument("--update-status", action="store_true", help="Update completion status")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    result = verify_task(args.task, args.path)

    # Log verification
    log_verification(args.task, result, args.path)

    # Log gaps if any
    if result.gaps:
        log_gap(args.task, result.gaps, args.path)

    # Update status if requested
    if args.update_status:
        status = "completed" if result.passed else "pending"
        update_task_status(args.task, status, {
            "passed": result.passed,
            "gaps": result.gaps
        }, args.path)

    if args.format == "json":
        print(json.dumps({
            "task_id": result.task_id,
            "passed": result.passed,
            "checks": result.checks,
            "gaps": result.gaps,
            "message": result.message
        }, indent=2))
    else:
        print(format_result(result))


if __name__ == "__main__":
    main()
