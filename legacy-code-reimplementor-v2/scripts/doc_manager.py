#!/usr/bin/env python3
"""
Document Manager for Legacy Code Reimplementor v2.
Handles document persistence, indexing, and retrieval in .reimpl-docs/ directory.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib


DOCS_DIR = '.reimpl-docs'
INDEX_FILE = 'index.md'
CONFIG_FILE = 'config.json'


def init_docs_structure(base_path: str = '.') -> str:
    """Initialize the .reimpl-docs directory structure."""
    docs_path = os.path.join(base_path, DOCS_DIR)

    directories = [
        'analysis',
        'plans',
        'tasks',
        'tracking'
    ]

    for dir_name in directories:
        os.makedirs(os.path.join(docs_path, dir_name), exist_ok=True)

    # Create initial config
    config = {
        'project_id': hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12],
        'created_at': datetime.now().isoformat(),
        'repo_a': None,
        'repo_b': None,
        'tech_stack': {},
        'status': 'initialized'
    }
    save_config(config, docs_path)

    # Create initial tracking files
    status = {
        'project_id': config['project_id'],
        'last_updated': datetime.now().isoformat(),
        'summary': {
            'total_tasks': 0,
            'completed': 0,
            'in_progress': 0,
            'pending': 0,
            'blocked': 0
        },
        'tasks': {}
    }
    save_status(status, docs_path)

    # Create verification log
    log_content = f"""# Verification Log

Created: {datetime.now().isoformat()}

## Log Entries

| Timestamp | Task ID | Result | Notes |
|-----------|---------|--------|-------|
"""
    save_document(log_content, 'tracking/verification_log.md', docs_path)

    # Create gaps report
    gaps_content = """# Implementation Gaps Report

This document tracks tasks that failed verification and were added back to the plan.

## Current Gaps

*No gaps recorded yet.*

## Gap History

| Date | Task ID | Gap Description | Resolution |
|------|---------|-----------------|------------|
"""
    save_document(gaps_content, 'tracking/gaps_report.md', docs_path)

    # Create initial index
    update_index(docs_path)

    print(f"Initialized documentation structure at: {docs_path}")
    return docs_path


def save_document(content: str, relative_path: str, docs_path: str = None) -> str:
    """Save a document to the docs directory."""
    if docs_path is None:
        docs_path = DOCS_DIR

    full_path = os.path.join(docs_path, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return full_path


def load_document(relative_path: str, docs_path: str = None) -> Optional[str]:
    """Load a document from the docs directory."""
    if docs_path is None:
        docs_path = DOCS_DIR

    full_path = os.path.join(docs_path, relative_path)

    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def save_config(config: dict, docs_path: str = None) -> None:
    """Save project configuration."""
    if docs_path is None:
        docs_path = DOCS_DIR

    config['last_updated'] = datetime.now().isoformat()
    config_path = os.path.join(docs_path, CONFIG_FILE)

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_config(docs_path: str = None) -> Optional[dict]:
    """Load project configuration."""
    if docs_path is None:
        docs_path = DOCS_DIR

    config_path = os.path.join(docs_path, CONFIG_FILE)

    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_status(status: dict, docs_path: str = None) -> None:
    """Save completion status."""
    if docs_path is None:
        docs_path = DOCS_DIR

    status['last_updated'] = datetime.now().isoformat()
    status_path = os.path.join(docs_path, 'tracking', 'completion_status.json')

    with open(status_path, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


def load_status(docs_path: str = None) -> Optional[dict]:
    """Load completion status."""
    if docs_path is None:
        docs_path = DOCS_DIR

    status_path = os.path.join(docs_path, 'tracking', 'completion_status.json')

    if os.path.exists(status_path):
        with open(status_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def update_index(docs_path: str = None) -> None:
    """Update the searchable index of all documents."""
    if docs_path is None:
        docs_path = DOCS_DIR

    index_content = f"""# Documentation Index

**Last Updated:** {datetime.now().isoformat()}

## Quick Links

- [Configuration](config.json)
- [Completion Status](tracking/completion_status.json)
- [Verification Log](tracking/verification_log.md)
- [Gaps Report](tracking/gaps_report.md)

## Analysis Documents

"""

    # List analysis documents
    analysis_dir = os.path.join(docs_path, 'analysis')
    if os.path.exists(analysis_dir):
        for f in sorted(os.listdir(analysis_dir)):
            if f.endswith('.md'):
                title = f.replace('.md', '').replace('_', ' ').title()
                index_content += f"- [{title}](analysis/{f})\n"

    index_content += "\n## Planning Documents\n\n"

    # List planning documents
    plans_dir = os.path.join(docs_path, 'plans')
    if os.path.exists(plans_dir):
        for f in sorted(os.listdir(plans_dir)):
            if f.endswith('.md'):
                title = f.replace('.md', '').replace('_', ' ').title()
                index_content += f"- [{title}](plans/{f})\n"

    index_content += "\n## Tasks\n\n"

    # List task documents
    tasks_dir = os.path.join(docs_path, 'tasks')
    if os.path.exists(tasks_dir):
        task_files = sorted([f for f in os.listdir(tasks_dir) if f.endswith('.md')])
        for f in task_files[:20]:  # Show first 20
            task_id = f.replace('.md', '')
            index_content += f"- [{task_id}](tasks/{f})\n"
        if len(task_files) > 20:
            index_content += f"- ... and {len(task_files) - 20} more tasks\n"

    index_content += f"""
## Search

Use `/reimpl-search <query>` to search across all documents.

## Statistics

"""

    # Add statistics
    status = load_status(docs_path)
    if status:
        summary = status.get('summary', {})
        index_content += f"""| Metric | Value |
|--------|-------|
| Total Tasks | {summary.get('total_tasks', 0)} |
| Completed | {summary.get('completed', 0)} |
| In Progress | {summary.get('in_progress', 0)} |
| Pending | {summary.get('pending', 0)} |
| Blocked | {summary.get('blocked', 0)} |
"""

    save_document(index_content, INDEX_FILE, docs_path)


def list_documents(docs_path: str = None, category: str = None) -> List[Dict]:
    """List all documents, optionally filtered by category."""
    if docs_path is None:
        docs_path = DOCS_DIR

    documents = []
    categories = [category] if category else ['analysis', 'plans', 'tasks', 'tracking']

    for cat in categories:
        cat_path = os.path.join(docs_path, cat)
        if os.path.exists(cat_path):
            for f in os.listdir(cat_path):
                file_path = os.path.join(cat_path, f)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    documents.append({
                        'name': f,
                        'category': cat,
                        'path': f"{cat}/{f}",
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })

    return documents


def get_task_file_path(task_id: str, docs_path: str = None) -> str:
    """Get the file path for a task document."""
    if docs_path is None:
        docs_path = DOCS_DIR
    return os.path.join(docs_path, 'tasks', f'{task_id}.md')


def append_to_log(entry: str, log_file: str = 'tracking/verification_log.md', docs_path: str = None) -> None:
    """Append an entry to a log file."""
    if docs_path is None:
        docs_path = DOCS_DIR

    log_path = os.path.join(docs_path, log_file)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(entry + '\n')


def main():
    parser = argparse.ArgumentParser(description='Manage reimplementor documentation')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize docs structure')
    init_parser.add_argument('--path', '-p', default='.', help='Base path')

    # List command
    list_parser = subparsers.add_parser('list', help='List documents')
    list_parser.add_argument('--category', '-c', help='Filter by category')
    list_parser.add_argument('--docs-path', '-d', default=DOCS_DIR)

    # Update index command
    index_parser = subparsers.add_parser('update-index', help='Update document index')
    index_parser.add_argument('--docs-path', '-d', default=DOCS_DIR)

    args = parser.parse_args()

    if args.command == 'init':
        init_docs_structure(args.path)

    elif args.command == 'list':
        docs = list_documents(args.docs_path, args.category)
        for doc in docs:
            print(f"{doc['category']}/{doc['name']} ({doc['size']} bytes)")

    elif args.command == 'update-index':
        update_index(args.docs_path)
        print("Index updated.")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
