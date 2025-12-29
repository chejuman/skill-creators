#!/usr/bin/env python3
"""
Task Generator for Feature Spec Dev
Generates individual task files from implementation plan.

Usage:
    python3 generate_tasks.py --plan implementation_plan.json
    python3 generate_tasks.py --task-data '{"id": "TASK-001", ...}'
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"


TASK_TEMPLATE = """# {task_id}: {title}

## Metadata

| Field        | Value |
| ------------ | ----- |
| ID           | {task_id} |
| Feature      | {feature} |
| Priority     | {priority} |
| Complexity   | {complexity} |
| Status       | pending |
| Dependencies | {dependencies} |
| Blocks       | {blocks} |

## Description

{description}

## Files to Create/Modify

| File | Action | Purpose |
| ---- | ------ | ------- |
{files_table}

## Acceptance Criteria

{acceptance_criteria}

## Implementation Notes

{implementation_notes}

## Tests Required

{tests_required}

## Reference

- Requirements: {requirement_refs}
- Design: {design_refs}
"""


def get_spec_docs_path(base_path: str = ".") -> Path:
    """Get the .spec-docs directory path."""
    return Path(base_path) / SPEC_DOCS_DIR


def format_files_table(files: list) -> str:
    """Format files list as markdown table rows."""
    if not files:
        return "| - | - | - |"

    rows = []
    for f in files:
        if isinstance(f, dict):
            rows.append(f"| `{f.get('path', '')}` | {f.get('action', 'Create')} | {f.get('purpose', '')} |")
        else:
            rows.append(f"| `{f}` | Create | - |")
    return "\n".join(rows)


def format_criteria(criteria: list) -> str:
    """Format acceptance criteria as checkboxes."""
    if not criteria:
        return "- [ ] Implementation complete"
    return "\n".join(f"- [ ] {c}" for c in criteria)


def format_tests(tests: list) -> str:
    """Format test requirements as checkboxes."""
    if not tests:
        return "- [ ] Unit tests written"
    return "\n".join(f"- [ ] {t}" for t in tests)


def generate_task_file(task_data: dict, base_path: str = ".") -> dict:
    """Generate a single task file."""
    task_id = task_data.get("id", "TASK-001")

    content = TASK_TEMPLATE.format(
        task_id=task_id,
        title=task_data.get("title", "Untitled Task"),
        feature=task_data.get("feature", "unknown"),
        priority=task_data.get("priority", 1),
        complexity=task_data.get("complexity", "Medium"),
        dependencies=", ".join(task_data.get("dependencies", [])) or "-",
        blocks=", ".join(task_data.get("blocks", [])) or "-",
        description=task_data.get("description", "No description provided."),
        files_table=format_files_table(task_data.get("files", [])),
        acceptance_criteria=format_criteria(task_data.get("acceptance_criteria", [])),
        implementation_notes=task_data.get("implementation_notes", "Follow project conventions."),
        tests_required=format_tests(task_data.get("tests", [])),
        requirement_refs=task_data.get("requirement_refs", "-"),
        design_refs=task_data.get("design_refs", "-")
    )

    # Save task file
    task_path = get_spec_docs_path(base_path) / "tasks" / f"{task_id}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)

    with open(task_path, "w") as f:
        f.write(content)

    # Update completion status
    status_path = get_spec_docs_path(base_path) / "tracking" / "completion_status.json"
    if status_path.exists():
        with open(status_path) as f:
            status = json.load(f)
    else:
        status = {"tasks": {}, "summary": {}}

    status["tasks"][task_id] = {"status": "pending", "created_at": datetime.now().isoformat()}

    # Update summary
    statuses = [t.get("status", "pending") for t in status["tasks"].values()]
    status["summary"] = {
        "total_tasks": len(statuses),
        "completed": statuses.count("completed"),
        "in_progress": statuses.count("in_progress"),
        "pending": statuses.count("pending")
    }
    status["last_updated"] = datetime.now().isoformat()

    with open(status_path, "w") as f:
        json.dump(status, f, indent=2)

    return {
        "task_id": task_id,
        "path": str(task_path),
        "status": "created"
    }


def generate_from_plan(plan_path: str, base_path: str = ".") -> dict:
    """Generate all tasks from a plan JSON file."""
    with open(plan_path) as f:
        plan = json.load(f)

    tasks = plan.get("tasks", [])
    results = []

    for task_data in tasks:
        result = generate_task_file(task_data, base_path)
        results.append(result)

    return {
        "total_generated": len(results),
        "tasks": results
    }


def generate_task_breakdown(tasks: list, base_path: str = ".") -> str:
    """Generate task_breakdown.md from task list."""
    content = f"""# Task Breakdown

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Total Tasks:** {len(tasks)}

## Dependency Graph

```mermaid
graph TD
"""

    # Add nodes
    for task in tasks:
        task_id = task.get("id", "TASK-XXX")
        title = task.get("title", "")[:30]
        content += f"    {task_id}[\"{task_id}: {title}\"]\n"

    # Add edges
    for task in tasks:
        task_id = task.get("id")
        for dep in task.get("dependencies", []):
            content += f"    {dep} --> {task_id}\n"

    content += "```\n\n## Task List\n\n"

    # Group by priority
    by_priority = {}
    for task in tasks:
        priority = task.get("priority", 99)
        if priority not in by_priority:
            by_priority[priority] = []
        by_priority[priority].append(task)

    for priority in sorted(by_priority.keys()):
        content += f"### Priority {priority}\n\n"
        for task in by_priority[priority]:
            content += f"- **{task.get('id')}**: {task.get('title')}\n"
            content += f"  - Complexity: {task.get('complexity', 'Medium')}\n"
            deps = task.get("dependencies", [])
            if deps:
                content += f"  - Dependencies: {', '.join(deps)}\n"
        content += "\n"

    # Save breakdown
    breakdown_path = get_spec_docs_path(base_path) / "plans" / "task_breakdown.md"
    breakdown_path.parent.mkdir(parents=True, exist_ok=True)

    with open(breakdown_path, "w") as f:
        f.write(content)

    return str(breakdown_path)


def main():
    parser = argparse.ArgumentParser(description="Generate task files")
    parser.add_argument("--plan", help="Path to plan JSON file")
    parser.add_argument("--task-data", help="Single task JSON data")
    parser.add_argument("--path", default=".", help="Base path")
    parser.add_argument("--breakdown", action="store_true", help="Generate task breakdown")
    args = parser.parse_args()

    if args.plan:
        result = generate_from_plan(args.plan, args.path)
        print(json.dumps(result, indent=2))

        # Generate breakdown
        with open(args.plan) as f:
            plan = json.load(f)
        breakdown_path = generate_task_breakdown(plan.get("tasks", []), args.path)
        print(f"Task breakdown: {breakdown_path}")

    elif args.task_data:
        task_data = json.loads(args.task_data)
        result = generate_task_file(task_data, args.path)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
