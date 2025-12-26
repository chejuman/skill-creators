#!/usr/bin/env python3
"""
Task Generator for Legacy Code Reimplementor v2.
Generates individual task files from feature catalog.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def load_feature_catalog(docs_path: str) -> Dict:
    """Load feature catalog from docs."""
    catalog_path = os.path.join(docs_path, 'analysis', 'feature_catalog.json')
    if os.path.exists(catalog_path):
        with open(catalog_path, 'r') as f:
            return json.load(f)
    return None


def load_config(docs_path: str) -> Dict:
    """Load project configuration."""
    config_path = os.path.join(docs_path, 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def estimate_target_files(source_files: List[str], target_lang: str, architecture: str) -> List[Dict]:
    """Estimate target file paths based on source and architecture."""
    target_files = []

    arch_patterns = {
        'Clean Architecture': {
            'model': 'src/domain/entities/',
            'repository': 'src/infrastructure/repositories/',
            'service': 'src/application/services/',
            'api': 'src/presentation/api/',
            'config': 'src/core/',
            'util': 'src/core/utils/',
            'default': 'src/'
        },
        'Hexagonal': {
            'model': 'src/core/domain/',
            'repository': 'src/adapters/outbound/',
            'service': 'src/core/usecases/',
            'api': 'src/adapters/inbound/',
            'config': 'src/config/',
            'default': 'src/'
        }
    }

    patterns = arch_patterns.get(architecture, arch_patterns['Clean Architecture'])

    ext_map = {
        'Python': '.py',
        'TypeScript': '.ts',
        'JavaScript': '.js',
        'Go': '.go',
        'Java': '.java',
        'Kotlin': '.kt'
    }

    target_ext = ext_map.get(target_lang, '.py')

    for source in source_files[:5]:  # Limit to 5 files
        source_name = Path(source).stem
        source_lower = source.lower()

        # Determine category
        for category, path_prefix in patterns.items():
            if category in source_lower:
                target_path = f"{path_prefix}{source_name}{target_ext}"
                target_files.append({
                    'path': target_path,
                    'purpose': f"Migrated from {source}"
                })
                break
        else:
            target_path = f"{patterns['default']}{source_name}{target_ext}"
            target_files.append({
                'path': target_path,
                'purpose': f"Migrated from {source}"
            })

    return target_files


def generate_acceptance_criteria(feature: Dict, category: str) -> List[str]:
    """Generate acceptance criteria based on feature type."""
    base_criteria = [
        "All source functionality preserved",
        "Unit tests with 80%+ coverage",
        "No security vulnerabilities introduced",
        "Code follows target language conventions"
    ]

    category_criteria = {
        'config': [
            "Configuration loads from environment variables",
            "Supports multiple environments (dev, staging, prod)",
            "Validation of required settings on startup"
        ],
        'model': [
            "All fields and types correctly mapped",
            "Validation rules preserved",
            "Serialization/deserialization works correctly"
        ],
        'repository': [
            "CRUD operations fully functional",
            "Query methods match original behavior",
            "Transaction handling implemented"
        ],
        'service': [
            "Business logic correctly implemented",
            "Error handling matches original",
            "Edge cases properly handled"
        ],
        'api': [
            "API contracts match original (or documented changes)",
            "Request/response validation implemented",
            "Error responses properly formatted"
        ],
        'auth': [
            "Authentication flow works correctly",
            "Token handling secure and correct",
            "Permission checks enforced"
        ]
    }

    return base_criteria + category_criteria.get(category, [])


def generate_task_file(task: Dict, docs_path: str) -> str:
    """Generate a single task markdown file."""
    deps_str = ', '.join(task['dependencies']) if task['dependencies'] else 'None'
    blocks_str = ', '.join(task['blocks']) if task.get('blocks') else 'None'

    source_table = "\n".join([f"| `{f}` | Source file |" for f in task['source_files'][:5]])
    target_table = "\n".join([f"| `{f['path']}` | {f['purpose']} |" for f in task['target_files'][:5]])
    criteria_list = "\n".join([f"- [ ] {c}" for c in task['acceptance_criteria']])

    content = f"""# {task['id']}: {task['name']}

## Metadata

| Field | Value |
|-------|-------|
| ID | {task['id']} |
| Feature | {task['feature_id']} |
| Category | {task['category'].title()} |
| Priority | {task['priority']} |
| Complexity | {task['complexity'].title()} |
| Status | pending |
| Dependencies | {deps_str} |
| Blocks | {blocks_str} |

## Description

{task['description']}

## Source Reference (Repo A)

| File | Purpose |
|------|---------|
{source_table}

**Key Functions:** {', '.join(task.get('functions', [])[:10])}

**Key Classes:** {', '.join(task.get('classes', [])[:5]) if task.get('classes') else 'None'}

## Target Files (Repo B)

| File | Purpose |
|------|---------|
{target_table}

## Acceptance Criteria

{criteria_list}

## Implementation Notes

- Reference original implementation for exact behavior
- Follow target language/framework conventions
- Use dependency injection where appropriate
- Write tests alongside implementation

## Tests Required

- [ ] Unit tests for all public functions
- [ ] Edge case tests based on original
- [ ] Integration tests if dependencies exist
- [ ] Error handling tests

## Verification Command

```bash
python3 ~/.claude/skills/legacy-code-reimplementor-v2/scripts/verify_task.py --task {task['id']}
```

---

**Created:** {task['created_at']}
**Last Updated:** {task['created_at']}
"""

    # Save task file
    tasks_dir = os.path.join(docs_path, 'tasks')
    os.makedirs(tasks_dir, exist_ok=True)
    task_path = os.path.join(tasks_dir, f"{task['id']}.md")

    with open(task_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return task_path


def generate_all_tasks(docs_path: str) -> Dict:
    """Generate all tasks from feature catalog."""
    catalog = load_feature_catalog(docs_path)
    config = load_config(docs_path)

    if not catalog:
        print("No feature catalog found. Run build_feature_catalog.py first.")
        return None

    target_lang = config.get('tech_stack', {}).get('target_lang', 'Python')
    architecture = config.get('tech_stack', {}).get('architecture', 'Clean Architecture')

    tasks = []
    task_id = 1

    # Sort features by priority and dependencies
    sorted_features = sorted(catalog['features'], key=lambda x: (x['priority'], len(x['dependencies'])))

    # Build reverse dependency map (what each feature blocks)
    blocks_map = {}
    for feature in sorted_features:
        for dep_id in feature['dependencies']:
            if dep_id not in blocks_map:
                blocks_map[dep_id] = []
            blocks_map[dep_id].append(feature['id'])

    for feature in sorted_features:
        # Generate tasks for each feature (split large features)
        num_tasks = feature['estimated_tasks']
        files_per_task = max(1, len(feature['source_files']) // num_tasks)

        for i in range(num_tasks):
            start_idx = i * files_per_task
            end_idx = start_idx + files_per_task if i < num_tasks - 1 else len(feature['source_files'])
            task_files = feature['source_files'][start_idx:end_idx]

            if not task_files:
                continue

            task_suffix = f" (Part {i+1}/{num_tasks})" if num_tasks > 1 else ""

            task = {
                'id': f'TASK-{task_id:03d}',
                'feature_id': feature['id'],
                'name': f"{feature['name']}{task_suffix}",
                'category': feature['category'],
                'priority': feature['priority'],
                'complexity': feature['complexity'],
                'description': f"Implement {feature['description']}{task_suffix}",
                'source_files': task_files,
                'target_files': estimate_target_files(task_files, target_lang, architecture),
                'functions': feature.get('functions', [])[(i*5):((i+1)*5)],
                'classes': feature.get('classes', [])[(i*2):((i+1)*2)],
                'dependencies': [f'TASK-{j:03d}' for j in range(1, task_id) if task_id > 1][-3:] if i == 0 else [f'TASK-{task_id-1:03d}'],
                'blocks': blocks_map.get(feature['id'], []),
                'acceptance_criteria': generate_acceptance_criteria(feature, feature['category']),
                'created_at': datetime.now().isoformat()
            }

            tasks.append(task)
            generate_task_file(task, docs_path)
            task_id += 1

    # Update completion status
    status = {
        'project_id': config.get('project_id', 'unknown'),
        'last_updated': datetime.now().isoformat(),
        'summary': {
            'total_tasks': len(tasks),
            'completed': 0,
            'in_progress': 0,
            'pending': len(tasks),
            'blocked': 0
        },
        'tasks': {t['id']: {'status': 'pending', 'dependencies': t['dependencies']} for t in tasks}
    }

    status_path = os.path.join(docs_path, 'tracking', 'completion_status.json')
    with open(status_path, 'w') as f:
        json.dump(status, f, indent=2)

    # Generate task breakdown document
    generate_task_breakdown(tasks, docs_path)

    # Generate implementation plan
    generate_implementation_plan(tasks, catalog, config, docs_path)

    print(f"Generated {len(tasks)} tasks in {docs_path}/tasks/")
    return {'tasks': tasks, 'count': len(tasks)}


def generate_task_breakdown(tasks: List[Dict], docs_path: str) -> None:
    """Generate task breakdown document."""
    content = f"""# Task Breakdown

**Generated:** {datetime.now().isoformat()}
**Total Tasks:** {len(tasks)}

## Overview

| Priority | Category | Count |
|----------|----------|-------|
"""

    # Count by priority and category
    from collections import Counter
    by_priority = Counter(t['priority'] for t in tasks)
    by_category = Counter(t['category'] for t in tasks)

    for p in sorted(by_priority.keys()):
        content += f"| {p} | Various | {by_priority[p]} |\n"

    content += "\n### By Category\n\n"
    for cat, count in sorted(by_category.items()):
        content += f"- **{cat.title()}**: {count} tasks\n"

    content += "\n## All Tasks\n\n"
    content += "| ID | Name | Category | Priority | Complexity | Dependencies |\n"
    content += "|-----|------|----------|----------|------------|-------------|\n"

    for task in tasks:
        deps = ', '.join(task['dependencies'][:3]) if task['dependencies'] else '-'
        content += f"| {task['id']} | {task['name'][:30]} | {task['category']} | {task['priority']} | {task['complexity']} | {deps} |\n"

    plans_dir = os.path.join(docs_path, 'plans')
    os.makedirs(plans_dir, exist_ok=True)

    with open(os.path.join(plans_dir, 'task_breakdown.md'), 'w') as f:
        f.write(content)


def generate_implementation_plan(tasks: List[Dict], catalog: Dict, config: Dict, docs_path: str) -> None:
    """Generate master implementation plan."""
    tech = config.get('tech_stack', {})

    content = f"""# Implementation Plan

**Generated:** {datetime.now().isoformat()}

## Project Overview

| Aspect | Value |
|--------|-------|
| Source Repository | `{catalog.get('repo_path', 'Not set')}` |
| Source Language | {catalog.get('language', 'Unknown')} |
| Source Framework | {catalog.get('framework', 'Unknown')} |
| Target Language | {tech.get('target_lang', 'Not selected')} |
| Target Framework | {tech.get('framework', 'Not selected')} |
| Architecture | {tech.get('architecture', 'Not selected')} |

## Summary

| Metric | Value |
|--------|-------|
| Total Features | {catalog['summary']['total_features']} |
| Total Tasks | {len(tasks)} |
| Est. Total Lines | {catalog['summary']['total_lines']:,} |

## Implementation Phases

"""

    # Group tasks by priority
    phases = {}
    for task in tasks:
        p = task['priority']
        if p not in phases:
            phases[p] = []
        phases[p].append(task)

    phase_names = {
        1: 'Foundation (Config, Utils, Core)',
        2: 'Data Layer (Models, Repositories)',
        3: 'Business Logic (Services)',
        4: 'Interface Layer (APIs, Controllers)',
        5: 'Integration & Polish'
    }

    for priority in sorted(phases.keys()):
        phase_tasks = phases[priority]
        phase_name = phase_names.get(priority, f'Phase {priority}')

        content += f"""### Phase {priority}: {phase_name}

**Tasks:** {len(phase_tasks)}

| Task ID | Name | Complexity |
|---------|------|------------|
"""
        for task in phase_tasks:
            content += f"| {task['id']} | {task['name'][:40]} | {task['complexity']} |\n"

        content += "\n"

    content += """## Execution Guidelines

1. **Follow dependency order** - Check task dependencies before starting
2. **Verify before next** - Use `/reimpl-check` after each task
3. **Document gaps** - If blocked, document in gaps_report.md
4. **Test continuously** - Write tests alongside implementation

## Commands Reference

- `/reimpl-next` - Get next task (with verification)
- `/reimpl-check --task TASK-XXX` - Verify specific task
- `/reimpl-search <query>` - Search documentation

## Progress Tracking

Status is tracked in `.reimpl-docs/tracking/completion_status.json`

Run `/reimpl-check --all` for full progress report.
"""

    with open(os.path.join(docs_path, 'plans', 'implementation_plan.md'), 'w') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description='Generate task files from feature catalog')
    parser.add_argument('--docs-path', '-d', default='.reimpl-docs', help='Documentation path')
    args = parser.parse_args()

    generate_all_tasks(args.docs_path)


if __name__ == '__main__':
    main()
