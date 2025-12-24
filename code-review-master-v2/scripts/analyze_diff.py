#!/usr/bin/env python3
"""
Analyze git diff for code review context.
Outputs file statistics, complexity estimation, and language detection.
"""

import subprocess
import sys
import json
import re
from pathlib import Path
from collections import defaultdict

# Language detection by extension
LANGUAGE_MAP = {
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript',
    '.js': 'JavaScript',
    '.jsx': 'JavaScript',
    '.py': 'Python',
    '.go': 'Go',
    '.java': 'Java',
    '.rs': 'Rust',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.c': 'C',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
}

# Framework detection patterns
FRAMEWORK_PATTERNS = {
    'React': [r'import.*from [\'"]react[\'"]', r'<.*/>'],
    'Next.js': [r'from [\'"]next', r'getServerSideProps', r'getStaticProps'],
    'Vue': [r'import.*from [\'"]vue[\'"]', r'<template>'],
    'Angular': [r'@Component', r'@Injectable'],
    'Django': [r'from django', r'models\.Model'],
    'FastAPI': [r'from fastapi', r'@app\.(get|post|put|delete)'],
    'Express': [r'express\(\)', r'app\.(get|post|use)'],
    'Spring': [r'@SpringBootApplication', r'@RestController'],
}


def run_git_command(args: list[str]) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr}", file=sys.stderr)
        return ""


def get_staged_diff() -> str:
    """Get diff of staged changes."""
    return run_git_command(['diff', '--cached', '--stat'])


def get_unstaged_diff() -> str:
    """Get diff of unstaged changes."""
    return run_git_command(['diff', '--stat'])


def get_pr_diff(pr_number: str) -> str:
    """Get diff for a GitHub PR."""
    # Try to fetch PR diff using gh CLI
    try:
        result = subprocess.run(
            ['gh', 'pr', 'diff', pr_number],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Could not fetch PR diff. Ensure 'gh' CLI is installed.", file=sys.stderr)
        return ""


def get_file_diff(files: list[str]) -> str:
    """Get diff for specific files."""
    return run_git_command(['diff', '--stat'] + files)


def parse_diff_stats(diff_output: str) -> list[dict]:
    """Parse git diff --stat output into structured data."""
    files = []
    lines = diff_output.strip().split('\n')

    for line in lines:
        # Match pattern like: " src/file.ts | 42 +++---"
        match = re.match(r'\s*(.+?)\s*\|\s*(\d+)\s*([+-]*)', line)
        if match:
            filepath = match.group(1).strip()
            changes = int(match.group(2))
            files.append({
                'path': filepath,
                'changes': changes,
                'extension': Path(filepath).suffix,
            })

    return files


def detect_language(files: list[dict]) -> dict[str, int]:
    """Detect languages from file extensions."""
    languages = defaultdict(int)
    for f in files:
        ext = f['extension']
        lang = LANGUAGE_MAP.get(ext, 'Other')
        languages[lang] += f['changes']
    return dict(languages)


def detect_frameworks(content: str) -> list[str]:
    """Detect frameworks from diff content."""
    detected = []
    for framework, patterns in FRAMEWORK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, content):
                detected.append(framework)
                break
    return detected


def calculate_complexity(files: list[dict], total_lines: int) -> int:
    """
    Calculate complexity score (1-5) based on:
    - Number of files
    - Total lines changed
    - File types
    """
    file_count = len(files)

    # Base score from line count
    if total_lines < 50:
        score = 1
    elif total_lines < 150:
        score = 2
    elif total_lines < 400:
        score = 3
    elif total_lines < 800:
        score = 4
    else:
        score = 5

    # Adjust for file count
    if file_count > 10:
        score = min(5, score + 1)
    elif file_count > 20:
        score = 5

    return score


def suggest_depth(complexity: int) -> int:
    """Suggest review depth based on complexity."""
    return min(5, max(1, complexity))


def analyze(args: list[str]) -> dict:
    """Main analysis function."""
    # Determine what to analyze
    if '--staged' in args:
        diff_stat = get_staged_diff()
        diff_content = run_git_command(['diff', '--cached'])
        mode = 'staged'
    elif '--pr' in args:
        pr_idx = args.index('--pr')
        pr_number = args[pr_idx + 1] if pr_idx + 1 < len(args) else None
        if not pr_number:
            return {'error': 'PR number required after --pr'}
        diff_stat = run_git_command(['diff', '--stat', 'origin/main...HEAD'])
        diff_content = run_git_command(['diff', 'origin/main...HEAD'])
        mode = f'pr-{pr_number}'
    elif args and not args[0].startswith('-'):
        files = [a for a in args if not a.startswith('-')]
        diff_stat = get_file_diff(files)
        diff_content = run_git_command(['diff'] + files)
        mode = 'files'
    else:
        # Default: staged + unstaged
        diff_stat = get_staged_diff() or get_unstaged_diff()
        diff_content = run_git_command(['diff', '--cached']) or run_git_command(['diff'])
        mode = 'working'

    # Parse stats
    files = parse_diff_stats(diff_stat)
    total_lines = sum(f['changes'] for f in files)

    # Detect languages and frameworks
    languages = detect_language(files)
    frameworks = detect_frameworks(diff_content)

    # Calculate metrics
    complexity = calculate_complexity(files, total_lines)
    suggested_depth = suggest_depth(complexity)

    return {
        'mode': mode,
        'file_count': len(files),
        'total_lines': total_lines,
        'files': [f['path'] for f in files],
        'languages': languages,
        'frameworks': frameworks,
        'complexity': complexity,
        'suggested_depth': suggested_depth,
        'depth_agents': {
            1: ['combined'],
            2: ['security', 'practices'],
            3: ['security', 'performance', 'architecture', 'practices'],
            4: ['security', 'performance', 'architecture', 'practices'],
            5: ['security', 'performance', 'architecture', 'practices'],
        }[suggested_depth]
    }


def main():
    """CLI entry point."""
    args = sys.argv[1:]

    if '-h' in args or '--help' in args:
        print("""
Usage: analyze_diff.py [options] [files...]

Options:
  --staged      Analyze staged changes only
  --pr NUMBER   Analyze GitHub PR
  -h, --help    Show this help

Examples:
  analyze_diff.py                    # Analyze working changes
  analyze_diff.py --staged           # Analyze staged changes
  analyze_diff.py --pr 123           # Analyze PR #123
  analyze_diff.py src/auth/*.ts      # Analyze specific files
        """)
        return

    result = analyze(args)

    if 'error' in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Pretty print for humans, JSON for machines
    if sys.stdout.isatty():
        print(f"\n📊 Code Review Analysis")
        print(f"{'=' * 40}")
        print(f"Mode: {result['mode']}")
        print(f"Files: {result['file_count']} ({result['total_lines']} lines)")
        print(f"Languages: {', '.join(result['languages'].keys())}")
        if result['frameworks']:
            print(f"Frameworks: {', '.join(result['frameworks'])}")
        print(f"\n🎯 Complexity: {result['complexity']}/5")
        print(f"📋 Suggested Depth: Level {result['suggested_depth']}")
        print(f"🤖 Agents: {', '.join(result['depth_agents'])}")
        print()
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
