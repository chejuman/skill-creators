#!/usr/bin/env python3
"""
Context Manager for Legacy Code Reimplementor.
Manages session persistence, context encoding/decoding, and state transitions.
"""

import argparse
import base64
import json
import os
import uuid
import zlib
from datetime import datetime
from pathlib import Path
from typing import Optional


DEFAULT_CONTEXT_FILE = '.reimpl-context.json'


def create_context(repo_a: str, repo_b: str, output_path: str = DEFAULT_CONTEXT_FILE) -> dict:
    """Create a new reimplementation context."""
    context = {
        'session_id': str(uuid.uuid4()),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'repo_a': os.path.abspath(repo_a),
        'repo_b': os.path.abspath(repo_b) if repo_b else os.path.abspath(f"{repo_a}-reimpl"),
        'tech_stack': {
            'source_lang': None,
            'target_lang': None,
            'framework': None,
            'architecture': None
        },
        'features': [],
        'current_feature_id': None,
        'current_unit_id': None,
        'current_phase': 'init',  # init, analysis, tech_selection, implementation, validation, complete
        'analysis': {
            'completed': False,
            'structure': None,
            'issues': None
        },
        'next_prompt': 'Run analysis on the original codebase.',
        'history': []
    }

    save_context(context, output_path)
    return context


def load_context(path: str = DEFAULT_CONTEXT_FILE) -> Optional[dict]:
    """Load context from file or base64 encoded string."""
    # Check if it's a base64 encoded string
    if not os.path.exists(path) and len(path) > 50:
        try:
            return decode_context(path)
        except:
            pass

    # Load from file
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)

    return None


def save_context(context: dict, path: str = DEFAULT_CONTEXT_FILE) -> None:
    """Save context to file."""
    context['updated_at'] = datetime.now().isoformat()
    with open(path, 'w') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)
    print(f"Context saved to: {path}")


def encode_context(context: dict) -> str:
    """Encode context to base64 compressed string for CLI transfer."""
    # Create minimal context for transfer
    minimal = {
        'sid': context['session_id'][:8],
        'ra': context['repo_a'],
        'rb': context['repo_b'],
        'ts': context['tech_stack'],
        'cf': context['current_feature_id'],
        'cu': context.get('current_unit_id'),
        'ph': context['current_phase'],
        'np': context['next_prompt'][:200] if context.get('next_prompt') else None
    }

    json_str = json.dumps(minimal, separators=(',', ':'))
    compressed = zlib.compress(json_str.encode('utf-8'))
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    return encoded


def decode_context(encoded: str) -> dict:
    """Decode base64 compressed context string."""
    compressed = base64.urlsafe_b64decode(encoded.encode('ascii'))
    json_str = zlib.decompress(compressed).decode('utf-8')
    minimal = json.loads(json_str)

    # Reconstruct full context from minimal
    context = {
        'session_id': minimal['sid'],
        'repo_a': minimal['ra'],
        'repo_b': minimal['rb'],
        'tech_stack': minimal['ts'],
        'current_feature_id': minimal['cf'],
        'current_unit_id': minimal.get('cu'),
        'current_phase': minimal['ph'],
        'next_prompt': minimal.get('np', ''),
        'features': [],  # Will need to reload from file
        'analysis': {'completed': True}
    }
    return context


def update_phase(context: dict, new_phase: str, next_prompt: str = None) -> dict:
    """Update the current phase and optionally set next prompt."""
    valid_phases = ['init', 'analysis', 'tech_selection', 'implementation', 'validation', 'complete']
    if new_phase not in valid_phases:
        raise ValueError(f"Invalid phase: {new_phase}. Must be one of {valid_phases}")

    context['current_phase'] = new_phase
    if next_prompt:
        context['next_prompt'] = next_prompt

    # Add to history
    context.setdefault('history', []).append({
        'timestamp': datetime.now().isoformat(),
        'phase': new_phase,
        'action': 'phase_transition'
    })

    return context


def set_tech_stack(context: dict, source_lang: str, target_lang: str,
                   framework: str, architecture: str) -> dict:
    """Set the technology stack after user selection."""
    context['tech_stack'] = {
        'source_lang': source_lang,
        'target_lang': target_lang,
        'framework': framework,
        'architecture': architecture
    }
    return context


def add_features(context: dict, features: list) -> dict:
    """Add extracted features to context."""
    context['features'] = features
    if features:
        context['current_feature_id'] = features[0]['id']
        context['current_unit_id'] = 1
    return context


def start_feature(context: dict, feature_id: int) -> dict:
    """Start working on a specific feature."""
    for f in context['features']:
        if f['id'] == feature_id:
            f['status'] = 'in_progress'
            f['started_at'] = datetime.now().isoformat()
            context['current_feature_id'] = feature_id
            context['current_unit_id'] = 1
            break
    return context


def complete_unit(context: dict, feature_id: int, unit_id: int, tests_passed: bool = True) -> dict:
    """Mark a unit as complete and advance to next."""
    for f in context['features']:
        if f['id'] == feature_id:
            f['completed_units'] = f.get('completed_units', 0) + 1

            # Check if feature is complete
            if f['completed_units'] >= f.get('units', 1):
                f['status'] = 'completed'
                f['tests_passed'] = tests_passed
                f['completed_at'] = datetime.now().isoformat()

                # Find next pending feature
                next_feature = next((feat for feat in context['features']
                                    if feat['status'] == 'pending'), None)
                if next_feature:
                    context['current_feature_id'] = next_feature['id']
                    context['current_unit_id'] = 1
                    next_feature['status'] = 'in_progress'
                else:
                    context['current_phase'] = 'validation'
            else:
                context['current_unit_id'] = unit_id + 1
            break

    return context


def get_progress(context: dict) -> dict:
    """Get current progress statistics."""
    features = context.get('features', [])
    total = len(features)
    completed = len([f for f in features if f.get('status') == 'completed'])
    in_progress = len([f for f in features if f.get('status') == 'in_progress'])

    current_feature = next((f for f in features if f['id'] == context.get('current_feature_id')), None)

    return {
        'total_features': total,
        'completed_features': completed,
        'in_progress_features': in_progress,
        'pending_features': total - completed - in_progress,
        'completion_pct': round(completed / total * 100 if total > 0 else 0, 1),
        'current_feature': current_feature,
        'current_unit': context.get('current_unit_id'),
        'phase': context.get('current_phase')
    }


def generate_status_report(context: dict) -> str:
    """Generate a human-readable status report."""
    progress = get_progress(context)

    report = f"""# Reimplementation Status

**Session:** {context.get('session_id', 'Unknown')[:8]}...
**Phase:** {progress['phase']}
**Updated:** {context.get('updated_at', 'Unknown')}

## Repositories

- **Original (Repo A):** `{context.get('repo_a', 'Not set')}`
- **New (Repo B):** `{context.get('repo_b', 'Not set')}`

## Technology Stack

| Aspect | Value |
|--------|-------|
| Source Language | {context['tech_stack'].get('source_lang', 'Not selected')} |
| Target Language | {context['tech_stack'].get('target_lang', 'Not selected')} |
| Framework | {context['tech_stack'].get('framework', 'Not selected')} |
| Architecture | {context['tech_stack'].get('architecture', 'Not selected')} |

## Progress

| Metric | Value |
|--------|-------|
| Total Features | {progress['total_features']} |
| Completed | {progress['completed_features']} |
| In Progress | {progress['in_progress_features']} |
| Pending | {progress['pending_features']} |
| Completion | {progress['completion_pct']}% |

## Features

"""

    for f in context.get('features', []):
        status_icon = {'completed': '✅', 'in_progress': '🔄', 'pending': '⏳'}.get(f.get('status'), '❓')
        units_info = f"{f.get('completed_units', 0)}/{f.get('units', '?')} units" if 'units' in f else ''
        report += f"- {status_icon} **Feature {f['id']}:** {f.get('name', 'Unknown')} {units_info}\n"

    if progress['current_feature']:
        cf = progress['current_feature']
        report += f"""
## Current Work

**Feature {cf['id']}:** {cf.get('name', 'Unknown')}
**Unit:** {progress['current_unit']} of {cf.get('units', '?')}
**Description:** {cf.get('description', 'No description')}

## Next Step

{context.get('next_prompt', 'No next prompt defined.')}

---

To continue: `/reimpl-continue`
"""

    return report


def generate_continuation_command(context: dict, context_path: str = DEFAULT_CONTEXT_FILE) -> str:
    """Generate the continuation command for next session."""
    encoded = encode_context(context)

    return f"""## Next Step

To continue implementation, run:

```
/reimpl-continue
```

Context file: `{context_path}`

Or use encoded context (for sharing):
```
/reimpl-continue {encoded}
```
"""


def main():
    parser = argparse.ArgumentParser(description='Manage reimplementation context')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create new context')
    create_parser.add_argument('repo_a', help='Path to original repository')
    create_parser.add_argument('--repo-b', help='Path to new repository')
    create_parser.add_argument('--output', '-o', default=DEFAULT_CONTEXT_FILE)

    # Status command
    status_parser = subparsers.add_parser('status', help='Show current status')
    status_parser.add_argument('--context', '-c', default=DEFAULT_CONTEXT_FILE)

    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode context to base64')
    encode_parser.add_argument('--context', '-c', default=DEFAULT_CONTEXT_FILE)

    # Progress command
    progress_parser = subparsers.add_parser('progress', help='Get progress as JSON')
    progress_parser.add_argument('--context', '-c', default=DEFAULT_CONTEXT_FILE)

    args = parser.parse_args()

    if args.command == 'create':
        ctx = create_context(args.repo_a, args.repo_b, args.output)
        print(f"Created new context: {ctx['session_id'][:8]}...")
        print(generate_continuation_command(ctx, args.output))

    elif args.command == 'status':
        ctx = load_context(args.context)
        if ctx:
            print(generate_status_report(ctx))
        else:
            print(f"No context found at: {args.context}")

    elif args.command == 'encode':
        ctx = load_context(args.context)
        if ctx:
            print(encode_context(ctx))
        else:
            print(f"No context found at: {args.context}")

    elif args.command == 'progress':
        ctx = load_context(args.context)
        if ctx:
            print(json.dumps(get_progress(ctx), indent=2))
        else:
            print(f"No context found at: {args.context}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
