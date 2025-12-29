#!/usr/bin/env python3
"""
Task Generator for Feature Spec Dev 2
Generates individual task files from design specifications.

Usage:
    python3 task_generator.py --title "Setup project structure" --priority 1
    python3 task_generator.py --from-breakdown tasks/task_breakdown.md
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"

TASK_TEMPLATE = """# {task_id}: {title}

## Metadata

| Field | Value |
|-------|-------|
| ID | {task_id} |
| Feature | {feature} |
| Phase | {phase} |
| Priority | {priority} |
| Complexity | {complexity} |
| Status | pending |
| Dependencies | {dependencies} |
| Blocks | {blocks} |

## Description

{description}

## Implementation Steps

{steps}

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
{files_table}

## Acceptance Criteria

{acceptance_criteria}

## Research References

{research_refs}

## Requirement Traceability

{requirements}
"""


def get_docs_path(base_path: str = ".") -> Path:
    return Path(base_path) / SPEC_DOCS_DIR


def get_next_task_id(base_path: str = ".") -> str:
    """Get next available task ID."""
    tasks_dir = get_docs_path(base_path) / "tasks"

    if not tasks_dir.exists():
        return "TASK-001"

    existing = list(tasks_dir.glob("TASK-*.md"))
    if not existing:
        return "TASK-001"

    max_num = 0
    for f in existing:
        try:
            num = int(f.stem.split("-")[1])
            max_num = max(max_num, num)
        except (IndexError, ValueError):
            continue

    return f"TASK-{max_num + 1:03d}"


def load_config(base_path: str = ".") -> Optional[dict]:
    """Load project configuration."""
    config_path = get_docs_path(base_path) / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return None


def generate_task(title: str, description: str, priority: int = 1,
                  complexity: str = "Medium", dependencies: str = "None",
                  blocks: str = "-", steps: list = None, files: list = None,
                  criteria: list = None, requirements: list = None,
                  base_path: str = ".") -> dict:
    """Generate a task file."""
    config = load_config(base_path)
    feature = config.get("feature", "Unknown") if config else "Unknown"

    task_id = get_next_task_id(base_path)

    # Format steps
    if steps:
        steps_str = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
    else:
        steps_str = "1. [Add implementation steps]"

    # Format files table
    if files:
        files_table = "\n".join([f"| `{f['path']}` | {f['action']} | {f['purpose']} |" for f in files])
    else:
        files_table = "| `src/...` | Create | [Purpose] |"

    # Format acceptance criteria
    if criteria:
        criteria_str = "\n".join([f"- [ ] {c}" for c in criteria])
    else:
        criteria_str = "- [ ] [Add acceptance criteria]"

    # Format requirements
    if requirements:
        req_str = "\n".join([f"- {r}" for r in requirements])
    else:
        req_str = "- [Add requirement references]"

    phase = {1: "Foundation", 2: "Core", 3: "Enhancement", 4: "Polish"}.get(priority, "Core")

    content = TASK_TEMPLATE.format(
        task_id=task_id,
        title=title,
        feature=feature,
        phase=phase,
        priority=priority,
        complexity=complexity,
        dependencies=dependencies,
        blocks=blocks,
        description=description,
        steps=steps_str,
        files_table=files_table,
        acceptance_criteria=criteria_str,
        research_refs="- [Add research references from discovery phase]",
        requirements=req_str
    )

    # Save task file
    tasks_dir = get_docs_path(base_path) / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)

    task_path = tasks_dir / f"{task_id}.md"
    with open(task_path, "w") as f:
        f.write(content)

    # Update completion status
    status_path = get_docs_path(base_path) / "tracking" / "completion_status.json"
    if status_path.exists():
        with open(status_path) as f:
            status = json.load(f)

        status["tasks"][task_id] = {
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }

        # Recalculate summary
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
        "status": "created",
        "task_id": task_id,
        "path": str(task_path)
    }


def main():
    parser = argparse.ArgumentParser(description="Generate task files")
    parser.add_argument("--title", required=True, help="Task title")
    parser.add_argument("--description", default="", help="Task description")
    parser.add_argument("--priority", type=int, default=1, help="Priority (1-4)")
    parser.add_argument("--complexity", default="Medium", choices=["Low", "Medium", "High"])
    parser.add_argument("--dependencies", default="None", help="Dependency task IDs")
    parser.add_argument("--blocks", default="-", help="Tasks this blocks")
    parser.add_argument("--path", default=".", help="Base path")
    args = parser.parse_args()

    result = generate_task(
        title=args.title,
        description=args.description if args.description else f"Implement {args.title}",
        priority=args.priority,
        complexity=args.complexity,
        dependencies=args.dependencies,
        blocks=args.blocks,
        base_path=args.path
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
