#!/usr/bin/env python3
"""
Generate implementation stages based on codebase analysis.
Creates modular, dependency-aware stage plan for iterative migration.
"""

import argparse
import json
import os
import re
from pathlib import Path
from collections import defaultdict


def detect_modules(repo_path: str) -> dict:
    """Detect logical modules in codebase."""
    modules = defaultdict(lambda: {'files': [], 'lines': 0, 'imports': set()})
    code_extensions = {'.py', '.java', '.js', '.ts', '.go', '.rs', '.rb', '.php', '.cs', '.kt'}

    for root, dirs, files in os.walk(repo_path):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'dist', 'build'}]

        rel_root = os.path.relpath(root, repo_path)
        if rel_root == '.':
            continue

        # Get top-level module name
        module_name = rel_root.split(os.sep)[0]

        for f in files:
            if Path(f).suffix.lower() in code_extensions:
                file_path = os.path.join(root, f)
                modules[module_name]['files'].append(os.path.relpath(file_path, repo_path))

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        modules[module_name]['lines'] += content.count('\n')
                        # Extract imports (simplified)
                        imports = re.findall(r'(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                        modules[module_name]['imports'].update(imports)
                except:
                    pass

    # Convert sets to lists for JSON serialization
    for mod in modules.values():
        mod['imports'] = list(mod['imports'])

    return dict(modules)


def categorize_module(name: str, files: list) -> str:
    """Categorize module by common patterns."""
    name_lower = name.lower()
    file_str = ' '.join(files).lower()

    categories = {
        'core': ['core', 'common', 'shared', 'base', 'foundation'],
        'utils': ['util', 'helper', 'tool', 'lib'],
        'config': ['config', 'setting', 'env', 'constant'],
        'data': ['model', 'entity', 'schema', 'dto', 'domain'],
        'repository': ['repo', 'dao', 'store', 'persistence', 'database'],
        'service': ['service', 'business', 'logic', 'usecase'],
        'api': ['api', 'controller', 'handler', 'route', 'endpoint', 'view'],
        'integration': ['integration', 'external', 'client', 'adapter'],
        'test': ['test', 'spec', '__test__']
    }

    for category, keywords in categories.items():
        if any(kw in name_lower or kw in file_str for kw in keywords):
            return category

    return 'other'


def create_stage_plan(modules: dict, num_stages: int = 4) -> list:
    """Create dependency-aware stage plan."""

    # Categorize all modules
    categorized = {}
    for name, data in modules.items():
        category = categorize_module(name, data['files'])
        if category not in categorized:
            categorized[category] = []
        categorized[category].append({
            'name': name,
            'files': len(data['files']),
            'lines': data['lines']
        })

    # Define stage order (dependencies flow down)
    stage_order = [
        ['core', 'utils', 'config'],           # Foundation
        ['data', 'repository'],                 # Data layer
        ['service'],                            # Business logic
        ['api', 'integration'],                 # Interfaces
        ['test', 'other']                       # Final
    ]

    # Build stages
    stages = []
    total_lines = sum(m['lines'] for m in modules.values())
    cumulative_lines = 0

    for i, categories in enumerate(stage_order[:num_stages]):
        stage_modules = []
        stage_lines = 0

        for cat in categories:
            if cat in categorized:
                stage_modules.extend(categorized[cat])
                stage_lines += sum(m['lines'] for m in categorized[cat])

        # Handle last stage - include remaining categories
        if i == num_stages - 1:
            for cat, mods in categorized.items():
                if cat not in [c for cats in stage_order[:num_stages] for c in cats]:
                    stage_modules.extend(mods)
                    stage_lines += sum(m['lines'] for m in mods)

        cumulative_lines += stage_lines
        coverage = round((cumulative_lines / total_lines * 100) if total_lines > 0 else 0)

        stages.append({
            'id': i + 1,
            'coverage': f"{min(coverage, 100)}%",
            'categories': categories,
            'modules': [m['name'] for m in stage_modules],
            'files_count': sum(m['files'] for m in stage_modules),
            'lines_count': stage_lines,
            'focus': get_stage_focus(categories)
        })

    return stages


def get_stage_focus(categories: list) -> str:
    """Get human-readable stage focus description."""
    focus_map = {
        'core': 'Core infrastructure and shared utilities',
        'utils': 'Helper functions and common tools',
        'config': 'Configuration management',
        'data': 'Data models and domain entities',
        'repository': 'Data persistence and storage',
        'service': 'Business logic and services',
        'api': 'API endpoints and controllers',
        'integration': 'External service integrations',
        'test': 'Test suites and fixtures',
        'other': 'Miscellaneous components'
    }

    focuses = [focus_map.get(cat, cat.title()) for cat in categories if cat in focus_map]
    return '; '.join(focuses) if focuses else 'General implementation'


def generate_stage_plan(repo_path: str, output_path: str, num_stages: int = 4):
    """Generate complete stage plan document."""
    modules = detect_modules(repo_path)
    stages = create_stage_plan(modules, num_stages)

    report = f"""# Implementation Stage Plan

**Repository:** {os.path.abspath(repo_path)}
**Total Stages:** {len(stages)}

## Stage Overview

| Stage | Coverage | Modules | Files | Lines | Focus |
|-------|----------|---------|-------|-------|-------|
"""

    for stage in stages:
        report += f"| {stage['id']} | {stage['coverage']} | {len(stage['modules'])} | {stage['files_count']} | {stage['lines_count']:,} | {stage['focus'][:40]}... |\n"

    report += "\n## Detailed Stage Breakdown\n\n"

    for stage in stages:
        report += f"""### Stage {stage['id']}: {stage['focus'].split(';')[0]}

- **Coverage Target:** {stage['coverage']}
- **Categories:** {', '.join(stage['categories'])}
- **Modules:** {', '.join(stage['modules']) if stage['modules'] else 'None detected'}
- **Estimated Scope:** {stage['files_count']} files, {stage['lines_count']:,} lines

**Implementation Tasks:**
1. Migrate {', '.join(stage['categories'])} components
2. Write unit tests for migrated code
3. Validate against Repo A functionality
4. Generate stage comparison report

---
"""

    report += """
## Stage Dependencies

```
Stage 1 (Foundation) ──► Stage 2 (Data) ──► Stage 3 (Services) ──► Stage 4 (API)
```

## TodoWrite Template

```json
"""

    todos = []
    for stage in stages:
        todos.append({
            "content": f"Stage {stage['id']}: Implement {stage['focus'].split(';')[0]}",
            "status": "pending",
            "activeForm": f"Implementing stage {stage['id']}"
        })

    report += json.dumps(todos, indent=2)
    report += """
```

---
*Generated by legacy-code-reimplementor*
"""

    with open(output_path, 'w') as f:
        f.write(report)

    # Also output JSON for programmatic use
    json_output = output_path.replace('.md', '.json')
    with open(json_output, 'w') as f:
        json.dump({'modules': modules, 'stages': stages}, f, indent=2)

    print(f"Stage plan generated: {output_path}")
    print(f"Stage data (JSON): {json_output}")
    return stages


def main():
    parser = argparse.ArgumentParser(description='Generate implementation stage plan')
    parser.add_argument('repo_path', help='Path to repository to analyze')
    parser.add_argument('--output', '-o', default='stage_plan.md', help='Output file path')
    parser.add_argument('--stages', '-s', type=int, default=4, help='Number of stages (3-5)')
    args = parser.parse_args()

    num_stages = max(3, min(5, args.stages))
    generate_stage_plan(args.repo_path, args.output, num_stages)


if __name__ == '__main__':
    main()
