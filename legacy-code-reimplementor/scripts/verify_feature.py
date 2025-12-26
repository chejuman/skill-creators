#!/usr/bin/env python3
"""
Feature Verification for Legacy Code Reimplementor.
Compares a specific feature implementation between Repo A and Repo B.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def load_context(context_path: str) -> Optional[dict]:
    """Load reimplementation context."""
    if os.path.exists(context_path):
        with open(context_path, 'r') as f:
            return json.load(f)
    return None


def extract_functions(file_path: str) -> List[Dict]:
    """Extract function signatures from a file."""
    functions = []
    if not os.path.exists(file_path):
        return functions

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return functions

    # Multi-language function patterns
    patterns = [
        # Python
        (r'(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*([^:]+))?:', 'python'),
        # JavaScript/TypeScript
        (r'(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)', 'js'),
        (r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>)', 'js'),
        # Java/Kotlin
        (r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(([^)]*)\)', 'java'),
        # Go
        (r'func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(([^)]*)\)', 'go'),
    ]

    for pattern, lang in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            func_name = match.group(1)
            params = match.group(2) if len(match.groups()) > 1 else ''
            if func_name and not func_name.startswith('_'):
                functions.append({
                    'name': func_name,
                    'params': params.strip(),
                    'line': content[:match.start()].count('\n') + 1
                })

    return functions


def extract_classes(file_path: str) -> List[Dict]:
    """Extract class definitions from a file."""
    classes = []
    if not os.path.exists(file_path):
        return classes

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return classes

    patterns = [
        r'class\s+(\w+)',
        r'interface\s+(\w+)',
        r'type\s+(\w+)\s+struct',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            classes.append({
                'name': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })

    return classes


def compare_feature_files(repo_a: str, repo_b: str, files_a: List[str], files_b: List[str] = None) -> Dict:
    """Compare specific feature files between repos."""

    # Collect functions and classes from Repo A
    funcs_a = {}
    classes_a = {}
    for file_path in files_a:
        full_path = os.path.join(repo_a, file_path)
        for func in extract_functions(full_path):
            funcs_a[func['name']] = {'file': file_path, **func}
        for cls in extract_classes(full_path):
            classes_a[cls['name']] = {'file': file_path, **cls}

    # Determine Repo B files to check
    if not files_b:
        # Try to find corresponding files in Repo B
        files_b = []
        for file_a in files_a:
            # Look for similar file names in Repo B
            file_name = Path(file_a).stem
            for root, _, files in os.walk(repo_b):
                for f in files:
                    if file_name.lower() in f.lower():
                        files_b.append(os.path.relpath(os.path.join(root, f), repo_b))

    # Collect functions and classes from Repo B
    funcs_b = {}
    classes_b = {}
    for file_path in files_b:
        full_path = os.path.join(repo_b, file_path)
        for func in extract_functions(full_path):
            funcs_b[func['name']] = {'file': file_path, **func}
        for cls in extract_classes(full_path):
            classes_b[cls['name']] = {'file': file_path, **cls}

    # Compare
    funcs_matched = set(funcs_a.keys()) & set(funcs_b.keys())
    funcs_missing = set(funcs_a.keys()) - set(funcs_b.keys())
    funcs_new = set(funcs_b.keys()) - set(funcs_a.keys())

    classes_matched = set(classes_a.keys()) & set(classes_b.keys())
    classes_missing = set(classes_a.keys()) - set(classes_b.keys())
    classes_new = set(classes_b.keys()) - set(classes_a.keys())

    func_coverage = len(funcs_matched) / len(funcs_a) * 100 if funcs_a else 100
    class_coverage = len(classes_matched) / len(classes_a) * 100 if classes_a else 100

    return {
        'repo_a_files': files_a,
        'repo_b_files': files_b,
        'functions': {
            'total_a': len(funcs_a),
            'total_b': len(funcs_b),
            'matched': list(funcs_matched),
            'missing': list(funcs_missing),
            'new': list(funcs_new),
            'coverage_pct': round(func_coverage, 1)
        },
        'classes': {
            'total_a': len(classes_a),
            'total_b': len(classes_b),
            'matched': list(classes_matched),
            'missing': list(classes_missing),
            'new': list(classes_new),
            'coverage_pct': round(class_coverage, 1)
        }
    }


def verify_feature(context_path: str, feature_id: int, unit_id: int = None,
                   repo_a: str = None, repo_b: str = None) -> Dict:
    """Verify a specific feature implementation."""

    context = load_context(context_path)
    if not context and not (repo_a and repo_b):
        return {'error': 'No context file or repo paths provided'}

    if context:
        repo_a = repo_a or context['repo_a']
        repo_b = repo_b or context['repo_b']
        features = context.get('features', [])
    else:
        features = []

    # Find the feature
    feature = next((f for f in features if f['id'] == feature_id), None)

    if not feature:
        return {'error': f'Feature {feature_id} not found'}

    # Get files to verify
    if unit_id:
        unit = next((u for u in feature.get('units', []) if u['id'] == unit_id), None)
        if not unit:
            return {'error': f'Unit {unit_id} not found in feature {feature_id}'}
        files_to_verify = unit.get('files', [])
    else:
        # Verify all units
        files_to_verify = []
        for unit in feature.get('units', []):
            files_to_verify.extend(unit.get('files', []))

    # Run comparison
    comparison = compare_feature_files(repo_a, repo_b, files_to_verify)

    # Determine overall status
    func_cov = comparison['functions']['coverage_pct']
    class_cov = comparison['classes']['coverage_pct']
    avg_coverage = (func_cov + class_cov) / 2

    if avg_coverage >= 90:
        status = 'passed'
        status_icon = '✅'
    elif avg_coverage >= 70:
        status = 'partial'
        status_icon = '⚠️'
    else:
        status = 'failed'
        status_icon = '❌'

    result = {
        'feature_id': feature_id,
        'feature_name': feature.get('name', 'Unknown'),
        'unit_id': unit_id,
        'status': status,
        'status_icon': status_icon,
        'coverage': {
            'functions': func_cov,
            'classes': class_cov,
            'average': round(avg_coverage, 1)
        },
        'comparison': comparison,
        'verified_at': datetime.now().isoformat()
    }

    return result


def generate_verification_report(result: Dict) -> str:
    """Generate human-readable verification report."""
    if 'error' in result:
        return f"# Verification Error\n\n{result['error']}"

    unit_str = f", Unit {result['unit_id']}" if result.get('unit_id') else " (all units)"

    report = f"""# Feature Verification Report

**Feature {result['feature_id']}:** {result['feature_name']}{unit_str}
**Status:** {result['status_icon']} {result['status'].upper()}
**Verified:** {result['verified_at']}

## Coverage Summary

| Metric | Coverage |
|--------|----------|
| Functions | {result['coverage']['functions']}% |
| Classes | {result['coverage']['classes']}% |
| **Average** | **{result['coverage']['average']}%** |

## Function Comparison

| Metric | Count |
|--------|-------|
| Repo A functions | {result['comparison']['functions']['total_a']} |
| Repo B functions | {result['comparison']['functions']['total_b']} |
| Matched | {len(result['comparison']['functions']['matched'])} |

"""

    if result['comparison']['functions']['missing']:
        report += "### Missing Functions (need implementation)\n\n"
        for func in result['comparison']['functions']['missing'][:10]:
            report += f"- `{func}`\n"
        if len(result['comparison']['functions']['missing']) > 10:
            report += f"- ... and {len(result['comparison']['functions']['missing']) - 10} more\n"
        report += "\n"

    if result['comparison']['functions']['new']:
        report += "### New Functions (added in Repo B)\n\n"
        for func in result['comparison']['functions']['new'][:10]:
            report += f"- `{func}`\n"
        report += "\n"

    report += """## Recommendation

"""

    if result['status'] == 'passed':
        report += "Feature implementation is complete. Proceed to next feature.\n"
    elif result['status'] == 'partial':
        report += "Feature implementation is mostly complete but has gaps. Review missing functions.\n"
    else:
        report += "Feature implementation needs more work. Focus on implementing missing functions.\n"

    return report


def main():
    parser = argparse.ArgumentParser(description='Verify feature implementation')
    parser.add_argument('--feature', '-f', type=int, required=True, help='Feature ID to verify')
    parser.add_argument('--unit', '-u', type=int, help='Specific unit ID (optional)')
    parser.add_argument('--context', '-c', default='.reimpl-context.json', help='Context file path')
    parser.add_argument('--repo-a', help='Path to original repository')
    parser.add_argument('--repo-b', help='Path to new repository')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    result = verify_feature(
        context_path=args.context,
        feature_id=args.feature,
        unit_id=args.unit,
        repo_a=args.repo_a,
        repo_b=args.repo_b
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(generate_verification_report(result))


if __name__ == '__main__':
    main()
