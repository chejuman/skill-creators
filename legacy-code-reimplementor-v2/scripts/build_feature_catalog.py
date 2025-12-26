#!/usr/bin/env python3
"""
Feature Catalog Builder for Legacy Code Reimplementor v2.
Extracts features from codebase and builds comprehensive catalog with dependencies.
"""

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


def detect_language(repo_path: str) -> Tuple[str, str]:
    """Detect primary language and framework hints."""
    ext_counts = defaultdict(int)
    framework_hints = []

    lang_map = {
        '.py': 'Python', '.java': 'Java', '.js': 'JavaScript',
        '.ts': 'TypeScript', '.go': 'Go', '.rs': 'Rust',
        '.rb': 'Ruby', '.php': 'PHP', '.cs': 'C#', '.kt': 'Kotlin'
    }

    framework_patterns = {
        'package.json': ['express', 'fastify', 'nest', 'react', 'vue', 'next', 'angular'],
        'requirements.txt': ['django', 'flask', 'fastapi', 'tornado', 'aiohttp'],
        'pom.xml': ['spring', 'quarkus', 'micronaut'],
        'build.gradle': ['spring', 'ktor'],
        'go.mod': ['gin', 'echo', 'fiber', 'chi'],
        'Cargo.toml': ['actix', 'axum', 'rocket']
    }

    for root, _, files in os.walk(repo_path):
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', 'venv']):
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in lang_map:
                ext_counts[ext] += 1

            # Check for framework files
            if f in framework_patterns:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read().lower()
                        for fw in framework_patterns[f]:
                            if fw in content:
                                framework_hints.append(fw)
                except:
                    pass

    if not ext_counts:
        return 'Unknown', 'Unknown'

    top_ext = max(ext_counts.items(), key=lambda x: x[1])[0]
    language = lang_map.get(top_ext, 'Unknown')
    framework = framework_hints[0].title() if framework_hints else 'Unknown'

    return language, framework


def extract_modules(repo_path: str) -> List[Dict]:
    """Extract top-level modules from codebase."""
    modules = []
    code_extensions = {'.py', '.java', '.js', '.ts', '.go', '.rs', '.rb', '.php', '.cs', '.kt'}
    skip_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'dist', 'build', 'test', 'tests'}

    for item in os.listdir(repo_path):
        item_path = os.path.join(repo_path, item)
        if os.path.isdir(item_path) and not item.startswith('.') and item not in skip_dirs:
            files = []
            lines = 0
            functions = []
            classes = []

            for root, _, fs in os.walk(item_path):
                if any(skip in root for skip in skip_dirs):
                    continue
                for f in fs:
                    if Path(f).suffix.lower() in code_extensions:
                        file_path = os.path.join(root, f)
                        rel_path = os.path.relpath(file_path, repo_path)
                        files.append(rel_path)

                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                                content = fp.read()
                                lines += content.count('\n')

                                # Extract functions
                                func_matches = re.findall(r'(?:def|function|func)\s+(\w+)', content)
                                functions.extend(func_matches)

                                # Extract classes
                                class_matches = re.findall(r'class\s+(\w+)', content)
                                classes.extend(class_matches)
                        except:
                            pass

            if files:
                modules.append({
                    'name': item,
                    'path': item,
                    'files': files,
                    'lines': lines,
                    'functions': functions[:20],  # Limit
                    'classes': classes[:10]
                })

    return modules


def categorize_module(name: str, files: List[str]) -> str:
    """Categorize module by name and file patterns."""
    name_lower = name.lower()
    files_str = ' '.join(files).lower()

    categories = [
        ('config', ['config', 'setting', 'env', 'constant']),
        ('util', ['util', 'helper', 'tool', 'common', 'shared', 'lib']),
        ('model', ['model', 'entity', 'schema', 'dto', 'domain']),
        ('repository', ['repo', 'dao', 'store', 'persistence', 'database']),
        ('service', ['service', 'usecase', 'business', 'logic']),
        ('api', ['api', 'controller', 'handler', 'route', 'endpoint', 'view']),
        ('auth', ['auth', 'login', 'session', 'jwt', 'oauth', 'permission']),
        ('integration', ['client', 'adapter', 'external', 'integration']),
        ('core', ['core', 'base', 'foundation']),
    ]

    for category, keywords in categories:
        if any(kw in name_lower or kw in files_str for kw in keywords):
            return category

    return 'other'


def build_dependency_graph(modules: List[Dict], repo_path: str) -> Dict[str, Set[str]]:
    """Build dependency graph between modules."""
    dependencies = defaultdict(set)

    for module in modules:
        module_name = module['name']
        for file_path in module['files']:
            full_path = os.path.join(repo_path, file_path)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for other in modules:
                        if other['name'] != module_name:
                            patterns = [
                                rf'from\s+\.?{other["name"]}',
                                rf'import\s+\.?{other["name"]}',
                                rf'require\s*\(["\'].*{other["name"]}',
                                rf'from\s+["\'].*{other["name"]}',
                            ]
                            for pattern in patterns:
                                if re.search(pattern, content, re.IGNORECASE):
                                    dependencies[module_name].add(other['name'])
                                    break
            except:
                pass

    return {k: list(v) for k, v in dependencies.items()}


def build_feature_catalog(repo_path: str, docs_path: str = '.reimpl-docs') -> Dict:
    """Build comprehensive feature catalog."""
    language, framework = detect_language(repo_path)
    modules = extract_modules(repo_path)
    dependencies = build_dependency_graph(modules, repo_path)

    # Priority order for implementation
    priority_order = ['config', 'util', 'core', 'model', 'repository', 'auth', 'service', 'api', 'integration', 'other']

    features = []
    feature_id = 1

    # Group by category and assign priorities
    categorized = defaultdict(list)
    for module in modules:
        category = categorize_module(module['name'], module['files'])
        categorized[category].append(module)

    for category in priority_order:
        for module in categorized.get(category, []):
            # Calculate complexity
            lines = module['lines']
            if lines < 200:
                complexity = 'low'
            elif lines < 500:
                complexity = 'medium'
            elif lines < 1000:
                complexity = 'high'
            else:
                complexity = 'very_high'

            # Estimate tasks (1 task per ~150 lines, minimum 1)
            estimated_tasks = max(1, lines // 150)

            # Get dependencies as feature IDs
            module_deps = dependencies.get(module['name'], [])
            dep_feature_ids = []
            for dep in module_deps:
                for f in features:
                    if f['module'] == dep:
                        dep_feature_ids.append(f['id'])
                        break

            feature = {
                'id': f'FEAT-{feature_id:03d}',
                'name': module['name'].replace('_', ' ').replace('-', ' ').title(),
                'module': module['name'],
                'category': category,
                'description': f"{category.title()} module: {module['name']}",
                'source_files': module['files'][:10],
                'functions': module['functions'],
                'classes': module['classes'],
                'lines': lines,
                'complexity': complexity,
                'estimated_tasks': estimated_tasks,
                'dependencies': dep_feature_ids,
                'priority': priority_order.index(category) + 1
            }
            features.append(feature)
            feature_id += 1

    catalog = {
        'generated_at': datetime.now().isoformat(),
        'repo_path': os.path.abspath(repo_path),
        'language': language,
        'framework': framework,
        'summary': {
            'total_features': len(features),
            'total_tasks_estimated': sum(f['estimated_tasks'] for f in features),
            'total_lines': sum(f['lines'] for f in features),
            'by_category': {cat: len(mods) for cat, mods in categorized.items() if mods},
            'by_complexity': {
                'low': len([f for f in features if f['complexity'] == 'low']),
                'medium': len([f for f in features if f['complexity'] == 'medium']),
                'high': len([f for f in features if f['complexity'] == 'high']),
                'very_high': len([f for f in features if f['complexity'] == 'very_high'])
            }
        },
        'features': features,
        'dependency_graph': dependencies
    }

    # Save catalog
    os.makedirs(os.path.join(docs_path, 'analysis'), exist_ok=True)
    catalog_path = os.path.join(docs_path, 'analysis', 'feature_catalog.json')
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    # Generate markdown version
    md_content = generate_feature_markdown(catalog)
    md_path = os.path.join(docs_path, 'analysis', 'feature_extraction.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    # Generate dependency graph
    dep_content = generate_dependency_markdown(catalog)
    dep_path = os.path.join(docs_path, 'analysis', 'dependency_graph.md')
    with open(dep_path, 'w', encoding='utf-8') as f:
        f.write(dep_content)

    print(f"Feature catalog saved to: {catalog_path}")
    print(f"Feature extraction: {md_path}")
    print(f"Dependency graph: {dep_path}")

    return catalog


def generate_feature_markdown(catalog: Dict) -> str:
    """Generate markdown documentation for features."""
    content = f"""# Feature Extraction Report

**Generated:** {catalog['generated_at']}
**Repository:** `{catalog['repo_path']}`
**Language:** {catalog['language']}
**Framework:** {catalog['framework']}

## Summary

| Metric | Value |
|--------|-------|
| Total Features | {catalog['summary']['total_features']} |
| Estimated Tasks | {catalog['summary']['total_tasks_estimated']} |
| Total Lines | {catalog['summary']['total_lines']:,} |

### By Category

| Category | Count |
|----------|-------|
"""

    for cat, count in catalog['summary']['by_category'].items():
        content += f"| {cat.title()} | {count} |\n"

    content += """
### By Complexity

| Complexity | Count |
|------------|-------|
"""

    for comp, count in catalog['summary']['by_complexity'].items():
        content += f"| {comp.replace('_', ' ').title()} | {count} |\n"

    content += "\n## Features\n\n"

    for feature in catalog['features']:
        deps = ', '.join(feature['dependencies']) if feature['dependencies'] else 'None'
        content += f"""### {feature['id']}: {feature['name']}

| Field | Value |
|-------|-------|
| Category | {feature['category'].title()} |
| Priority | {feature['priority']} |
| Complexity | {feature['complexity'].title()} |
| Lines | {feature['lines']:,} |
| Est. Tasks | {feature['estimated_tasks']} |
| Dependencies | {deps} |

**Source Files:** {', '.join(feature['source_files'][:5])}{'...' if len(feature['source_files']) > 5 else ''}

**Key Functions:** {', '.join(feature['functions'][:5])}{'...' if len(feature['functions']) > 5 else ''}

**Classes:** {', '.join(feature['classes'][:5]) if feature['classes'] else 'None'}

---

"""

    return content


def generate_dependency_markdown(catalog: Dict) -> str:
    """Generate dependency graph documentation."""
    content = f"""# Dependency Graph

**Generated:** {catalog['generated_at']}

## Module Dependencies

```
"""

    # Simple ASCII dependency visualization
    deps = catalog['dependency_graph']
    features = {f['module']: f for f in catalog['features']}

    for feature in catalog['features']:
        module = feature['module']
        module_deps = deps.get(module, [])
        if module_deps:
            content += f"{module}\n"
            for i, dep in enumerate(module_deps):
                prefix = "└──" if i == len(module_deps) - 1 else "├──"
                content += f"    {prefix}► {dep}\n"
            content += "\n"

    content += """```

## Implementation Order

Based on dependencies, implement in this order:

"""

    # Sort features by priority and dependencies
    sorted_features = sorted(catalog['features'], key=lambda x: (x['priority'], len(x['dependencies'])))

    for i, feature in enumerate(sorted_features, 1):
        deps_str = f" (after: {', '.join(feature['dependencies'])})" if feature['dependencies'] else ""
        content += f"{i}. **{feature['id']}**: {feature['name']}{deps_str}\n"

    return content


def main():
    parser = argparse.ArgumentParser(description='Build feature catalog from codebase')
    parser.add_argument('repo_path', help='Path to repository')
    parser.add_argument('--docs-path', '-d', default='.reimpl-docs', help='Documentation path')
    args = parser.parse_args()

    build_feature_catalog(args.repo_path, args.docs_path)


if __name__ == '__main__':
    main()
