#!/usr/bin/env python3
"""
Feature Extractor for Legacy Code Reimplementor.
Analyzes codebase and extracts atomic, independently-implementable features.
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Set


def detect_language(repo_path: str) -> str:
    """Detect primary programming language."""
    ext_counts = defaultdict(int)
    lang_map = {
        '.py': 'python', '.java': 'java', '.js': 'javascript',
        '.ts': 'typescript', '.go': 'go', '.rs': 'rust',
        '.rb': 'ruby', '.php': 'php', '.cs': 'csharp', '.kt': 'kotlin'
    }

    for root, _, files in os.walk(repo_path):
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', 'venv']):
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in lang_map:
                ext_counts[ext] += 1

    if not ext_counts:
        return 'unknown'

    top_ext = max(ext_counts.items(), key=lambda x: x[1])[0]
    return lang_map.get(top_ext, 'unknown')


def extract_modules(repo_path: str) -> List[Dict]:
    """Extract top-level modules/packages from codebase."""
    modules = []
    code_extensions = {'.py', '.java', '.js', '.ts', '.go', '.rs', '.rb', '.php', '.cs', '.kt'}

    for item in os.listdir(repo_path):
        item_path = os.path.join(repo_path, item)
        if os.path.isdir(item_path) and not item.startswith('.') and item not in {'node_modules', '__pycache__', 'venv', 'dist', 'build', 'test', 'tests', '__tests__'}:
            files = []
            lines = 0
            for root, _, fs in os.walk(item_path):
                for f in fs:
                    if Path(f).suffix.lower() in code_extensions:
                        file_path = os.path.join(root, f)
                        rel_path = os.path.relpath(file_path, repo_path)
                        files.append(rel_path)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                                lines += sum(1 for _ in fp)
                        except:
                            pass

            if files:
                modules.append({
                    'name': item,
                    'path': item,
                    'files': files,
                    'lines': lines
                })

    return modules


def extract_endpoints(repo_path: str, language: str) -> List[Dict]:
    """Extract API endpoints from codebase."""
    endpoints = []
    patterns = {
        'python': [
            r'@(?:app|router|api)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
            r'@(?:app|router)\.(route)\s*\(\s*["\']([^"\']+)["\']',
        ],
        'java': [
            r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\s*\(\s*["\']?([^"\')\s]+)',
        ],
        'javascript': [
            r'(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
        ],
        'typescript': [
            r'@(Get|Post|Put|Delete|Patch)\s*\(\s*["\']([^"\']+)["\']',
            r'(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
        ],
        'go': [
            r'(?:Handle|HandleFunc)\s*\(\s*["\']([^"\']+)["\']',
            r'\.(GET|POST|PUT|DELETE|PATCH)\s*\(\s*["\']([^"\']+)["\']',
        ]
    }

    lang_patterns = patterns.get(language, patterns['python'])
    code_ext = {'.py', '.java', '.js', '.ts', '.go'}

    for root, _, files in os.walk(repo_path):
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', 'venv']):
            continue
        for f in files:
            if Path(f).suffix.lower() in code_ext:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        for pattern in lang_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                method = match[0].upper() if len(match) > 1 else 'GET'
                                path = match[1] if len(match) > 1 else match[0]
                                endpoints.append({
                                    'method': method,
                                    'path': path,
                                    'file': os.path.relpath(file_path, repo_path)
                                })
                except:
                    pass

    return endpoints


def extract_models(repo_path: str, language: str) -> List[Dict]:
    """Extract data models/entities from codebase."""
    models = []
    patterns = {
        'python': [
            r'class\s+(\w+)\s*\([^)]*(?:Base|Model|Schema|Entity)',
            r'class\s+(\w+)\s*\(\s*(?:BaseModel|SQLModel)\s*\)',
        ],
        'java': [
            r'@Entity[^}]*class\s+(\w+)',
            r'class\s+(\w+)\s+(?:extends|implements)[^{]*(?:Entity|Model)',
        ],
        'typescript': [
            r'(?:export\s+)?(?:interface|class)\s+(\w+)(?:Model|Entity|Schema)',
            r'@Entity\s*\([^)]*\)\s*(?:export\s+)?class\s+(\w+)',
        ]
    }

    lang_patterns = patterns.get(language, patterns.get('python', []))
    code_ext = {'.py', '.java', '.js', '.ts', '.go', '.kt'}

    for root, _, files in os.walk(repo_path):
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', 'venv']):
            continue
        for f in files:
            if Path(f).suffix.lower() in code_ext:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        for pattern in lang_patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                models.append({
                                    'name': match,
                                    'file': os.path.relpath(file_path, repo_path)
                                })
                except:
                    pass

    return models


def categorize_feature(name: str, files: List[str]) -> str:
    """Categorize a feature based on its name and files."""
    name_lower = name.lower()
    files_str = ' '.join(files).lower()

    categories = [
        ('config', ['config', 'setting', 'env', 'constant']),
        ('auth', ['auth', 'login', 'session', 'jwt', 'oauth', 'permission']),
        ('user', ['user', 'account', 'profile']),
        ('data', ['model', 'entity', 'schema', 'dto']),
        ('repository', ['repo', 'dao', 'store', 'persistence']),
        ('service', ['service', 'usecase', 'business']),
        ('api', ['controller', 'handler', 'route', 'endpoint', 'view']),
        ('util', ['util', 'helper', 'tool', 'common']),
        ('integration', ['client', 'adapter', 'external', 'integration']),
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
                    # Look for imports from other modules
                    for other_module in modules:
                        if other_module['name'] != module_name:
                            # Check for import patterns
                            patterns = [
                                rf'from\s+{other_module["name"]}',
                                rf'import\s+{other_module["name"]}',
                                rf'require\s*\(["\'].*{other_module["name"]}',
                            ]
                            for pattern in patterns:
                                if re.search(pattern, content):
                                    dependencies[module_name].add(other_module['name'])
                                    break
            except:
                pass

    return dict(dependencies)


def generate_features(repo_path: str, output_path: str = None) -> List[Dict]:
    """Generate feature list from codebase analysis."""
    language = detect_language(repo_path)
    modules = extract_modules(repo_path)
    endpoints = extract_endpoints(repo_path, language)
    models = extract_models(repo_path, language)
    dependencies = build_dependency_graph(modules, repo_path)

    features = []
    feature_id = 1

    # Priority ordering based on typical dependency flow
    priority_order = ['config', 'util', 'data', 'repository', 'auth', 'service', 'api', 'integration', 'other']

    # Group modules by category
    categorized = defaultdict(list)
    for module in modules:
        category = categorize_feature(module['name'], module['files'])
        categorized[category].append(module)

    # Create features in dependency order
    for category in priority_order:
        for module in categorized.get(category, []):
            # Create units from files (group small files, split large ones)
            units = []
            unit_id = 1
            current_unit_files = []
            current_unit_lines = 0

            for file_path in sorted(module['files']):
                full_path = os.path.join(repo_path, file_path)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_lines = sum(1 for _ in f)
                except:
                    file_lines = 50  # Default estimate

                # If adding this file would exceed 200 lines, create new unit
                if current_unit_lines + file_lines > 200 and current_unit_files:
                    units.append({
                        'id': unit_id,
                        'name': Path(current_unit_files[0]).stem if len(current_unit_files) == 1 else f"unit_{unit_id}",
                        'files': current_unit_files,
                        'lines': current_unit_lines
                    })
                    unit_id += 1
                    current_unit_files = []
                    current_unit_lines = 0

                current_unit_files.append(file_path)
                current_unit_lines += file_lines

            # Add remaining files as last unit
            if current_unit_files:
                units.append({
                    'id': unit_id,
                    'name': Path(current_unit_files[0]).stem if len(current_unit_files) == 1 else f"unit_{unit_id}",
                    'files': current_unit_files,
                    'lines': current_unit_lines
                })

            # Determine feature dependencies
            feature_deps = []
            for dep in dependencies.get(module['name'], []):
                # Find feature ID for this dependency
                for f in features:
                    if f['module'] == dep:
                        feature_deps.append(f['id'])
                        break

            features.append({
                'id': feature_id,
                'name': module['name'].replace('_', ' ').replace('-', ' ').title(),
                'module': module['name'],
                'category': category,
                'description': f"{category.title()} module: {module['name']}",
                'units': units,
                'unit_count': len(units),
                'total_lines': module['lines'],
                'dependencies': feature_deps,
                'priority': priority_order.index(category) + 1,
                'status': 'pending',
                'completed_units': 0
            })
            feature_id += 1

    # Add API endpoints as features if not already covered
    endpoint_modules = set()
    for endpoint in endpoints:
        endpoint_dir = os.path.dirname(endpoint['file']).split(os.sep)[0] if os.sep in endpoint['file'] else ''
        if endpoint_dir and endpoint_dir not in endpoint_modules:
            endpoint_modules.add(endpoint_dir)

    result = {
        'language': language,
        'total_modules': len(modules),
        'total_features': len(features),
        'total_endpoints': len(endpoints),
        'total_models': len(models),
        'features': features,
        'endpoints': endpoints[:20],  # Limit for readability
        'models': models[:20]
    }

    if output_path:
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Features extracted to: {output_path}")

    return features


def print_feature_summary(features: List[Dict]) -> None:
    """Print human-readable feature summary."""
    print("\n# Extracted Features\n")
    print(f"Total: {len(features)} features\n")

    for f in features:
        deps = f', depends on: {f["dependencies"]}' if f['dependencies'] else ''
        print(f"## Feature {f['id']}: {f['name']}")
        print(f"   Category: {f['category']}")
        print(f"   Units: {f['unit_count']} ({f['total_lines']} lines){deps}")
        for unit in f['units'][:3]:  # Show first 3 units
            print(f"   - Unit {unit['id']}: {unit['name']} ({len(unit['files'])} files)")
        if len(f['units']) > 3:
            print(f"   - ... and {len(f['units']) - 3} more units")
        print()


def main():
    parser = argparse.ArgumentParser(description='Extract features from codebase')
    parser.add_argument('repo_path', help='Path to repository to analyze')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--summary', '-s', action='store_true', help='Print summary only')
    args = parser.parse_args()

    output = args.output or os.path.join(os.path.dirname(args.repo_path), 'features.json')
    features = generate_features(args.repo_path, output if not args.summary else None)

    if args.summary or not args.output:
        print_feature_summary(features)


if __name__ == '__main__':
    main()
