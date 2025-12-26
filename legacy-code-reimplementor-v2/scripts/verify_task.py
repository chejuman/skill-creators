#!/usr/bin/env python3
"""
Task Verification for Legacy Code Reimplementor v2.
Verifies task implementation status before providing next task.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_status(docs_path: str) -> Dict:
    """Load completion status."""
    status_path = os.path.join(docs_path, 'tracking', 'completion_status.json')
    if os.path.exists(status_path):
        with open(status_path, 'r') as f:
            return json.load(f)
    return None


def save_status(status: Dict, docs_path: str) -> None:
    """Save completion status."""
    status['last_updated'] = datetime.now().isoformat()
    status_path = os.path.join(docs_path, 'tracking', 'completion_status.json')
    with open(status_path, 'w') as f:
        json.dump(status, f, indent=2)


def load_task(task_id: str, docs_path: str) -> Optional[Dict]:
    """Load task details from markdown file."""
    task_path = os.path.join(docs_path, 'tasks', f'{task_id}.md')
    if not os.path.exists(task_path):
        return None

    with open(task_path, 'r') as f:
        content = f.read()

    # Parse task metadata from markdown
    task = {'id': task_id, 'raw_content': content}

    # Extract target files
    target_match = re.search(r'## Target Files.*?\n\|.*?\n\|.*?\n((?:\|.*?\n)+)', content, re.DOTALL)
    if target_match:
        target_lines = target_match.group(1).strip().split('\n')
        task['target_files'] = []
        for line in target_lines:
            parts = line.split('|')
            if len(parts) >= 2:
                file_path = parts[1].strip().strip('`')
                if file_path:
                    task['target_files'].append(file_path)

    # Extract acceptance criteria
    criteria_match = re.search(r'## Acceptance Criteria\n((?:- \[[ x]\].*?\n)+)', content)
    if criteria_match:
        criteria_lines = criteria_match.group(1).strip().split('\n')
        task['acceptance_criteria'] = [line.strip('- []x ') for line in criteria_lines]

    # Extract dependencies
    deps_match = re.search(r'\| Dependencies \| ([^|]+) \|', content)
    if deps_match:
        deps_str = deps_match.group(1).strip()
        if deps_str != 'None':
            task['dependencies'] = [d.strip() for d in deps_str.split(',')]
        else:
            task['dependencies'] = []

    return task


def load_config(docs_path: str) -> Dict:
    """Load project configuration."""
    config_path = os.path.join(docs_path, 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def check_files_exist(repo_b: str, target_files: List[str]) -> Tuple[bool, List[str], List[str]]:
    """Check if target files exist in Repo B."""
    existing = []
    missing = []

    for file_path in target_files:
        full_path = os.path.join(repo_b, file_path)
        if os.path.exists(full_path):
            existing.append(file_path)
        else:
            missing.append(file_path)

    return len(missing) == 0, existing, missing


def check_functions_implemented(repo_b: str, target_files: List[str]) -> Tuple[bool, int, int]:
    """Check if functions are implemented in target files."""
    total_functions = 0
    non_empty_files = 0

    for file_path in target_files:
        full_path = os.path.join(repo_b, file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Count functions
                    func_count = len(re.findall(r'(?:def|function|func|fn)\s+\w+', content))
                    total_functions += func_count
                    if len(content.strip()) > 50:  # More than just boilerplate
                        non_empty_files += 1
            except:
                pass

    passed = non_empty_files > 0 and total_functions > 0
    return passed, total_functions, non_empty_files


def check_tests_exist(repo_b: str, target_files: List[str]) -> Tuple[bool, List[str]]:
    """Check if test files exist for target files."""
    test_files_found = []

    for file_path in target_files:
        file_name = Path(file_path).stem
        dir_path = os.path.dirname(file_path)

        # Common test file patterns
        test_patterns = [
            os.path.join(repo_b, 'tests', dir_path, f'test_{file_name}.py'),
            os.path.join(repo_b, 'tests', dir_path, f'{file_name}_test.py'),
            os.path.join(repo_b, 'test', dir_path, f'test_{file_name}.py'),
            os.path.join(repo_b, dir_path, f'test_{file_name}.py'),
            os.path.join(repo_b, '__tests__', f'{file_name}.test.ts'),
            os.path.join(repo_b, '__tests__', f'{file_name}.test.js'),
        ]

        for test_path in test_patterns:
            if os.path.exists(test_path):
                test_files_found.append(os.path.relpath(test_path, repo_b))
                break

    # Pass if at least some tests exist (not strictly all)
    passed = len(test_files_found) >= len(target_files) * 0.5
    return passed, test_files_found


def verify_task(task_id: str, docs_path: str, repo_b: str = None) -> Dict:
    """Verify a single task's implementation status."""
    task = load_task(task_id, docs_path)
    if not task:
        return {'error': f'Task {task_id} not found', 'passed': False}

    config = load_config(docs_path)
    if not repo_b:
        repo_b = config.get('repo_b')

    if not repo_b or not os.path.exists(repo_b):
        return {
            'task_id': task_id,
            'error': 'Repo B path not configured or does not exist',
            'passed': False,
            'needs_repo_b': True
        }

    target_files = task.get('target_files', [])

    # Run checks
    files_passed, existing_files, missing_files = check_files_exist(repo_b, target_files)
    funcs_passed, func_count, non_empty = check_functions_implemented(repo_b, target_files)
    tests_passed, test_files = check_tests_exist(repo_b, target_files)

    # Calculate overall pass
    # Require files to exist and have implementation
    overall_passed = files_passed and funcs_passed

    result = {
        'task_id': task_id,
        'verified_at': datetime.now().isoformat(),
        'passed': overall_passed,
        'checks': {
            'files_exist': {
                'passed': files_passed,
                'existing': existing_files,
                'missing': missing_files
            },
            'implementation': {
                'passed': funcs_passed,
                'function_count': func_count,
                'non_empty_files': non_empty
            },
            'tests': {
                'passed': tests_passed,
                'test_files': test_files
            }
        },
        'gaps': []
    }

    # Identify gaps
    if missing_files:
        result['gaps'].extend([f"Missing file: {f}" for f in missing_files])
    if not funcs_passed:
        result['gaps'].append("No implementation found in target files")
    if not tests_passed:
        result['gaps'].append("Missing or insufficient test coverage")

    return result


def verify_dependencies(task_id: str, docs_path: str) -> Tuple[bool, List[str]]:
    """Check if all dependencies of a task are completed."""
    task = load_task(task_id, docs_path)
    if not task:
        return False, [f"Task {task_id} not found"]

    status = load_status(docs_path)
    if not status:
        return False, ["No status file found"]

    dependencies = task.get('dependencies', [])
    incomplete = []

    for dep_id in dependencies:
        dep_status = status.get('tasks', {}).get(dep_id, {}).get('status', 'pending')
        if dep_status != 'completed':
            incomplete.append(dep_id)

    return len(incomplete) == 0, incomplete


def update_task_status(task_id: str, passed: bool, verification: Dict, docs_path: str) -> None:
    """Update task status based on verification result."""
    status = load_status(docs_path)
    if not status:
        return

    new_status = 'completed' if passed else 'pending'
    old_status = status.get('tasks', {}).get(task_id, {}).get('status', 'pending')

    status['tasks'][task_id] = {
        'status': new_status,
        'last_verification': verification,
        'verified_at': datetime.now().isoformat()
    }

    # Update summary
    task_statuses = [t.get('status', 'pending') for t in status['tasks'].values()]
    status['summary'] = {
        'total_tasks': len(status['tasks']),
        'completed': task_statuses.count('completed'),
        'in_progress': task_statuses.count('in_progress'),
        'pending': task_statuses.count('pending'),
        'blocked': task_statuses.count('blocked')
    }

    save_status(status, docs_path)

    # Log status change
    if old_status != new_status:
        log_verification(task_id, passed, verification.get('gaps', []), docs_path)


def log_verification(task_id: str, passed: bool, gaps: List[str], docs_path: str) -> None:
    """Log verification result."""
    log_path = os.path.join(docs_path, 'tracking', 'verification_log.md')

    result = '✅ PASSED' if passed else '❌ FAILED'
    notes = '; '.join(gaps[:3]) if gaps else 'All checks passed'

    entry = f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | {task_id} | {result} | {notes} |\n"

    with open(log_path, 'a') as f:
        f.write(entry)

    # If failed, add to gaps report
    if not passed and gaps:
        add_to_gaps_report(task_id, gaps, docs_path)


def add_to_gaps_report(task_id: str, gaps: List[str], docs_path: str) -> None:
    """Add failed verification to gaps report."""
    gaps_path = os.path.join(docs_path, 'tracking', 'gaps_report.md')

    content = load_gaps_report(docs_path)
    if not content:
        content = "# Implementation Gaps Report\n\n## Current Gaps\n\n"

    # Add new gap entry
    gap_entry = f"""### {task_id} - {datetime.now().strftime('%Y-%m-%d')}

**Gaps Found:**
"""
    for gap in gaps:
        gap_entry += f"- {gap}\n"

    gap_entry += "\n**Resolution:** Pending\n\n"

    # Insert after "## Current Gaps" header
    if "## Current Gaps" in content:
        parts = content.split("## Current Gaps", 1)
        content = parts[0] + "## Current Gaps\n\n" + gap_entry + parts[1].lstrip()
    else:
        content += "\n## Current Gaps\n\n" + gap_entry

    with open(gaps_path, 'w') as f:
        f.write(content)


def load_gaps_report(docs_path: str) -> Optional[str]:
    """Load gaps report content."""
    gaps_path = os.path.join(docs_path, 'tracking', 'gaps_report.md')
    if os.path.exists(gaps_path):
        with open(gaps_path, 'r') as f:
            return f.read()
    return None


def get_next_task(docs_path: str, repo_b: str = None, skip_verify: bool = False) -> Dict:
    """Get the next task to work on, with pre-verification."""
    status = load_status(docs_path)
    if not status:
        return {'error': 'No status file found'}

    # Find tasks in order
    all_tasks = list(status.get('tasks', {}).keys())
    all_tasks.sort()  # TASK-001, TASK-002, etc.

    # Find current in-progress task
    current_task = None
    for task_id in all_tasks:
        task_status = status['tasks'][task_id].get('status', 'pending')
        if task_status == 'in_progress':
            current_task = task_id
            break

    # If there's a current task and not skipping verify, verify it first
    if current_task and not skip_verify:
        verification = verify_task(current_task, docs_path, repo_b)
        update_task_status(current_task, verification['passed'], verification, docs_path)

        if not verification['passed']:
            return {
                'verification_failed': True,
                'task_id': current_task,
                'verification': verification,
                'message': f"Task {current_task} not complete. Fix gaps before continuing."
            }

    # Find next pending task with all dependencies completed
    for task_id in all_tasks:
        task_status = status['tasks'][task_id].get('status', 'pending')
        if task_status == 'pending':
            deps_ok, incomplete_deps = verify_dependencies(task_id, docs_path)
            if deps_ok:
                # Mark as in progress
                status['tasks'][task_id]['status'] = 'in_progress'
                save_status(status, docs_path)

                task = load_task(task_id, docs_path)
                return {
                    'next_task': task_id,
                    'task': task,
                    'message': f"Next task: {task_id}"
                }
            else:
                # Task is blocked
                status['tasks'][task_id]['status'] = 'blocked'
                status['tasks'][task_id]['blocked_by'] = incomplete_deps

    # All tasks complete
    return {
        'all_complete': True,
        'message': 'All tasks completed! Run final validation.'
    }


def generate_verification_report(result: Dict) -> str:
    """Generate human-readable verification report."""
    if 'error' in result:
        return f"# Verification Error\n\n{result['error']}"

    status_icon = '✅ PASSED' if result['passed'] else '❌ FAILED'

    report = f"""# Verification Report: {result['task_id']}

**Status:** {status_icon}
**Verified:** {result['verified_at']}

## Check Results

| Check | Status | Details |
|-------|--------|---------|
| Files Exist | {'✅' if result['checks']['files_exist']['passed'] else '❌'} | {len(result['checks']['files_exist']['existing'])}/{len(result['checks']['files_exist']['existing']) + len(result['checks']['files_exist']['missing'])} files |
| Implementation | {'✅' if result['checks']['implementation']['passed'] else '❌'} | {result['checks']['implementation']['function_count']} functions in {result['checks']['implementation']['non_empty_files']} files |
| Tests | {'✅' if result['checks']['tests']['passed'] else '⚠️'} | {len(result['checks']['tests']['test_files'])} test files |

"""

    if result['checks']['files_exist']['missing']:
        report += "### Missing Files\n\n"
        for f in result['checks']['files_exist']['missing']:
            report += f"- `{f}`\n"
        report += "\n"

    if result['gaps']:
        report += "### Gaps to Address\n\n"
        for gap in result['gaps']:
            report += f"- {gap}\n"
        report += "\n"

    if result['passed']:
        report += "**Status:** Task implementation verified. Ready for next task.\n"
    else:
        report += "**Action Required:** Address the gaps above before proceeding.\n"

    return report


def main():
    parser = argparse.ArgumentParser(description='Verify task implementation')
    parser.add_argument('--task', '-t', help='Task ID to verify')
    parser.add_argument('--next', '-n', action='store_true', help='Get next task')
    parser.add_argument('--skip-verify', action='store_true', help='Skip verification')
    parser.add_argument('--all', '-a', action='store_true', help='Verify all tasks')
    parser.add_argument('--docs-path', '-d', default='.reimpl-docs')
    parser.add_argument('--repo-b', '-b', help='Path to Repo B')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if args.next:
        result = get_next_task(args.docs_path, args.repo_b, args.skip_verify)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if 'verification_failed' in result:
                print(generate_verification_report(result['verification']))
            elif 'next_task' in result:
                task = result['task']
                print(f"## Next Task: {result['next_task']}\n")
                print(task.get('raw_content', 'Task content not available'))
            else:
                print(result.get('message', 'Unknown state'))

    elif args.task:
        result = verify_task(args.task, args.docs_path, args.repo_b)
        update_task_status(args.task, result['passed'], result, args.docs_path)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(generate_verification_report(result))

    elif args.all:
        status = load_status(args.docs_path)
        if status:
            print("# Full Verification Report\n")
            for task_id in sorted(status.get('tasks', {}).keys()):
                result = verify_task(task_id, args.docs_path, args.repo_b)
                icon = '✅' if result['passed'] else '❌'
                print(f"{icon} {task_id}: {'Passed' if result['passed'] else 'Failed'}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
