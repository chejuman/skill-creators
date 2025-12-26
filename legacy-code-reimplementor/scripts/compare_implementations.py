#!/usr/bin/env python3
"""
Compare Repo A (original) vs Repo B (new implementation) at each stage.
Generates detailed comparison report with functionality coverage metrics.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


def extract_functions(file_path: str, language: str) -> list:
    """Extract function/method signatures from a file."""
    functions = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return functions

    patterns = {
        'python': r'(?:async\s+)?def\s+(\w+)\s*\([^)]*\)',
        'java': r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\([^)]*\)',
        'javascript': r'(?:async\s+)?(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
        'typescript': r'(?:async\s+)?(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
        'go': r'func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(',
    }

    pattern = patterns.get(language.lower(), patterns['python'])
    matches = re.findall(pattern, content)

    for match in matches:
        if isinstance(match, tuple):
            func_name = next((m for m in match if m), None)
        else:
            func_name = match
        if func_name and not func_name.startswith('_'):
            functions.append(func_name)

    return functions


def extract_classes(file_path: str, language: str) -> list:
    """Extract class definitions from a file."""
    classes = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return classes

    patterns = {
        'python': r'class\s+(\w+)',
        'java': r'(?:public|private)?\s*class\s+(\w+)',
        'javascript': r'class\s+(\w+)',
        'typescript': r'(?:export\s+)?(?:abstract\s+)?class\s+(\w+)',
        'go': r'type\s+(\w+)\s+struct',
    }

    pattern = patterns.get(language.lower(), patterns['python'])
    classes = re.findall(pattern, content)

    return classes


def detect_language(repo_path: str) -> str:
    """Detect primary programming language."""
    ext_lang = {
        '.py': 'python', '.java': 'java', '.js': 'javascript',
        '.ts': 'typescript', '.go': 'go', '.rs': 'rust',
        '.rb': 'ruby', '.php': 'php', '.cs': 'csharp', '.kt': 'kotlin'
    }

    counts = defaultdict(int)
    for root, _, files in os.walk(repo_path):
        if '.git' in root or 'node_modules' in root:
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in ext_lang:
                counts[ext_lang[ext]] += 1

    return max(counts.items(), key=lambda x: x[1])[0] if counts else 'python'


def analyze_repo(repo_path: str, language: str = None) -> dict:
    """Analyze repository structure and extract metrics."""
    if not language:
        language = detect_language(repo_path)

    code_extensions = {'.py', '.java', '.js', '.ts', '.go', '.rs', '.rb', '.php', '.cs', '.kt'}

    analysis = {
        'language': language,
        'files': [],
        'total_files': 0,
        'total_lines': 0,
        'functions': [],
        'classes': [],
        'modules': set()
    }

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', 'venv', 'dist', 'build'}]

        for f in files:
            if Path(f).suffix.lower() in code_extensions:
                file_path = os.path.join(root, f)
                rel_path = os.path.relpath(file_path, repo_path)

                analysis['files'].append(rel_path)
                analysis['total_files'] += 1

                # Count lines
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        analysis['total_lines'] += sum(1 for _ in fp)
                except:
                    pass

                # Extract functions and classes
                funcs = extract_functions(file_path, language)
                classes = extract_classes(file_path, language)

                analysis['functions'].extend(funcs)
                analysis['classes'].extend(classes)

                # Track modules
                parts = rel_path.split(os.sep)
                if len(parts) > 1:
                    analysis['modules'].add(parts[0])

    analysis['modules'] = list(analysis['modules'])
    return analysis


def compare_repos(repo_a_path: str, repo_b_path: str, stage: int = None) -> dict:
    """Compare two repositories and generate metrics."""

    analysis_a = analyze_repo(repo_a_path)
    analysis_b = analyze_repo(repo_b_path)

    funcs_a = set(analysis_a['functions'])
    funcs_b = set(analysis_b['functions'])
    classes_a = set(analysis_a['classes'])
    classes_b = set(analysis_b['classes'])

    comparison = {
        'stage': stage,
        'timestamp': datetime.now().isoformat(),
        'repo_a': {
            'path': os.path.abspath(repo_a_path),
            'language': analysis_a['language'],
            'files': analysis_a['total_files'],
            'lines': analysis_a['total_lines'],
            'functions': len(funcs_a),
            'classes': len(classes_a),
            'modules': len(analysis_a['modules'])
        },
        'repo_b': {
            'path': os.path.abspath(repo_b_path),
            'language': analysis_b['language'],
            'files': analysis_b['total_files'],
            'lines': analysis_b['total_lines'],
            'functions': len(funcs_b),
            'classes': len(classes_b),
            'modules': len(analysis_b['modules'])
        },
        'coverage': {
            'functions_covered': len(funcs_a & funcs_b),
            'functions_missing': list(funcs_a - funcs_b)[:20],
            'functions_new': list(funcs_b - funcs_a)[:20],
            'classes_covered': len(classes_a & classes_b),
            'classes_missing': list(classes_a - classes_b),
            'classes_new': list(classes_b - classes_a),
            'function_coverage_pct': round(len(funcs_a & funcs_b) / len(funcs_a) * 100 if funcs_a else 0, 1),
            'class_coverage_pct': round(len(classes_a & classes_b) / len(classes_a) * 100 if classes_a else 0, 1)
        }
    }

    return comparison


def generate_comparison_report(comparison: dict, output_path: str):
    """Generate markdown comparison report."""

    stage_str = f"Stage {comparison['stage']}" if comparison['stage'] else "Full"

    report = f"""# Implementation Comparison Report

**{stage_str} Analysis**
**Generated:** {comparison['timestamp']}

## Repository Summary

| Metric | Repo A (Original) | Repo B (New) | Delta |
|--------|-------------------|--------------|-------|
| Language | {comparison['repo_a']['language']} | {comparison['repo_b']['language']} | - |
| Files | {comparison['repo_a']['files']} | {comparison['repo_b']['files']} | {comparison['repo_b']['files'] - comparison['repo_a']['files']:+d} |
| Lines | {comparison['repo_a']['lines']:,} | {comparison['repo_b']['lines']:,} | {comparison['repo_b']['lines'] - comparison['repo_a']['lines']:+,d} |
| Functions | {comparison['repo_a']['functions']} | {comparison['repo_b']['functions']} | {comparison['repo_b']['functions'] - comparison['repo_a']['functions']:+d} |
| Classes | {comparison['repo_a']['classes']} | {comparison['repo_b']['classes']} | {comparison['repo_b']['classes'] - comparison['repo_a']['classes']:+d} |

## Coverage Analysis

| Metric | Value | Status |
|--------|-------|--------|
| Function Coverage | {comparison['coverage']['function_coverage_pct']}% | {'✅' if comparison['coverage']['function_coverage_pct'] >= 80 else '⚠️' if comparison['coverage']['function_coverage_pct'] >= 50 else '❌'} |
| Class Coverage | {comparison['coverage']['class_coverage_pct']}% | {'✅' if comparison['coverage']['class_coverage_pct'] >= 80 else '⚠️' if comparison['coverage']['class_coverage_pct'] >= 50 else '❌'} |
| Functions Implemented | {comparison['coverage']['functions_covered']}/{comparison['repo_a']['functions']} | - |
| Classes Implemented | {comparison['coverage']['classes_covered']}/{comparison['repo_a']['classes']} | - |

"""

    if comparison['coverage']['functions_missing']:
        report += f"""## Missing Functions (Not Yet Implemented)

```
{chr(10).join(comparison['coverage']['functions_missing'])}
{'...' if len(comparison['coverage']['functions_missing']) >= 20 else ''}
```

"""

    if comparison['coverage']['classes_missing']:
        report += f"""## Missing Classes

```
{chr(10).join(comparison['coverage']['classes_missing'])}
```

"""

    if comparison['coverage']['functions_new']:
        report += f"""## New Functions (Added in Repo B)

```
{chr(10).join(comparison['coverage']['functions_new'])}
{'...' if len(comparison['coverage']['functions_new']) >= 20 else ''}
```

"""

    overall_coverage = (comparison['coverage']['function_coverage_pct'] + comparison['coverage']['class_coverage_pct']) / 2
    status = '✅ On Track' if overall_coverage >= 80 else '⚠️ Needs Attention' if overall_coverage >= 50 else '❌ Behind Schedule'

    report += f"""## Stage Status: {status}

### Next Steps
"""

    if comparison['coverage']['functions_missing']:
        report += f"1. Implement remaining {len(comparison['coverage']['functions_missing'])} functions\n"
    if comparison['coverage']['classes_missing']:
        report += f"2. Implement remaining {len(comparison['coverage']['classes_missing'])} classes\n"

    report += """3. Run test suite to verify functionality
4. Conduct security review
5. Update stage progress in TodoWrite

---
*Generated by legacy-code-reimplementor*
"""

    with open(output_path, 'w') as f:
        f.write(report)

    # Also save JSON for programmatic access
    json_output = output_path.replace('.md', '.json')
    with open(json_output, 'w') as f:
        json.dump(comparison, f, indent=2)

    print(f"Comparison report generated: {output_path}")
    print(f"Comparison data (JSON): {json_output}")


def main():
    parser = argparse.ArgumentParser(description='Compare Repo A vs Repo B implementations')
    parser.add_argument('--repo-a', required=True, help='Path to original repository')
    parser.add_argument('--repo-b', required=True, help='Path to new implementation')
    parser.add_argument('--stage', '-s', type=int, help='Current stage number')
    parser.add_argument('--output', '-o', default='comparison_report.md', help='Output file path')
    args = parser.parse_args()

    comparison = compare_repos(args.repo_a, args.repo_b, args.stage)
    generate_comparison_report(comparison, args.output)


if __name__ == '__main__':
    main()
