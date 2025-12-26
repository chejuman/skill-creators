#!/usr/bin/env python3
"""
Document Search for Legacy Code Reimplementor v2.
Full-text search across all documentation in .reimpl-docs/.
"""

import argparse
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def search_file(file_path: str, query: str, context_lines: int = 1) -> List[Dict]:
    """Search for query in a single file."""
    matches = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except:
        return matches

    query_lower = query.lower()
    query_pattern = re.compile(re.escape(query), re.IGNORECASE)

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            # Get context
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context = ''.join(lines[start:end]).strip()

            # Highlight match
            highlighted = query_pattern.sub(f'**{query}**', line.strip())

            matches.append({
                'line_number': i + 1,
                'line': line.strip(),
                'highlighted': highlighted,
                'context': context
            })

    return matches


def search_docs(docs_path: str, query: str, category: str = None,
                max_results: int = 50, context_lines: int = 1) -> Dict:
    """Search across all documentation."""
    results = {
        'query': query,
        'total_matches': 0,
        'files_matched': 0,
        'results': defaultdict(list)
    }

    categories = [category] if category else ['analysis', 'plans', 'tasks', 'tracking']

    for cat in categories:
        cat_path = os.path.join(docs_path, cat)
        if not os.path.exists(cat_path):
            continue

        for file_name in os.listdir(cat_path):
            file_path = os.path.join(cat_path, file_name)
            if not os.path.isfile(file_path):
                continue

            # Skip non-text files
            if not file_name.endswith(('.md', '.json', '.txt')):
                continue

            matches = search_file(file_path, query, context_lines)
            if matches:
                rel_path = f"{cat}/{file_name}"
                results['results'][rel_path] = matches
                results['total_matches'] += len(matches)
                results['files_matched'] += 1

                if results['total_matches'] >= max_results:
                    results['truncated'] = True
                    break

        if results.get('truncated'):
            break

    # Also search index and config
    for special_file in ['index.md', 'config.json']:
        file_path = os.path.join(docs_path, special_file)
        if os.path.exists(file_path):
            matches = search_file(file_path, query, context_lines)
            if matches:
                results['results'][special_file] = matches
                results['total_matches'] += len(matches)
                results['files_matched'] += 1

    return results


def format_results(results: Dict, verbose: bool = False) -> str:
    """Format search results for display."""
    if results['total_matches'] == 0:
        return f"No results found for '{results['query']}'"

    output = f"""# Search Results for "{results['query']}"

**Matches:** {results['total_matches']} in {results['files_matched']} files

"""

    for file_path, matches in results['results'].items():
        output += f"## {file_path} ({len(matches)} matches)\n\n"

        for match in matches[:10]:  # Limit per file
            output += f"- **Line {match['line_number']}:** {match['highlighted']}\n"
            if verbose and match.get('context'):
                output += f"  ```\n  {match['context']}\n  ```\n"

        if len(matches) > 10:
            output += f"- ... and {len(matches) - 10} more matches\n"

        output += "\n"

    if results.get('truncated'):
        output += f"\n*Results truncated. Showing first {results['total_matches']} matches.*\n"

    return output


def search_tasks(docs_path: str, query: str) -> List[Dict]:
    """Search specifically in task files."""
    tasks_path = os.path.join(docs_path, 'tasks')
    if not os.path.exists(tasks_path):
        return []

    matching_tasks = []
    query_lower = query.lower()

    for file_name in sorted(os.listdir(tasks_path)):
        if not file_name.endswith('.md'):
            continue

        file_path = os.path.join(tasks_path, file_name)
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            if query_lower in content.lower():
                # Extract task ID and name
                task_id = file_name.replace('.md', '')
                name_match = re.search(r'# (TASK-\d+): (.+)', content)
                name = name_match.group(2) if name_match else 'Unknown'

                # Count matches
                match_count = len(re.findall(re.escape(query), content, re.IGNORECASE))

                matching_tasks.append({
                    'task_id': task_id,
                    'name': name,
                    'match_count': match_count,
                    'file': f"tasks/{file_name}"
                })
        except:
            pass

    return matching_tasks


def search_features(docs_path: str, query: str) -> List[Dict]:
    """Search in feature catalog."""
    catalog_path = os.path.join(docs_path, 'analysis', 'feature_catalog.json')
    if not os.path.exists(catalog_path):
        return []

    try:
        import json
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
    except:
        return []

    matching_features = []
    query_lower = query.lower()

    for feature in catalog.get('features', []):
        # Search in feature name, description, and files
        searchable = f"{feature['name']} {feature['description']} {' '.join(feature.get('source_files', []))}"
        if query_lower in searchable.lower():
            matching_features.append({
                'feature_id': feature['id'],
                'name': feature['name'],
                'category': feature['category'],
                'files': feature.get('source_files', [])[:3]
            })

    return matching_features


def main():
    parser = argparse.ArgumentParser(description='Search documentation')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--docs-path', '-d', default='.reimpl-docs')
    parser.add_argument('--category', '-c', help='Search specific category')
    parser.add_argument('--tasks', '-t', action='store_true', help='Search tasks only')
    parser.add_argument('--features', '-f', action='store_true', help='Search features only')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show context')
    parser.add_argument('--max', '-m', type=int, default=50, help='Max results')
    args = parser.parse_args()

    if args.tasks:
        tasks = search_tasks(args.docs_path, args.query)
        if tasks:
            print(f"# Tasks matching '{args.query}'\n")
            for task in tasks:
                print(f"- **{task['task_id']}**: {task['name']} ({task['match_count']} matches)")
        else:
            print(f"No tasks found matching '{args.query}'")

    elif args.features:
        features = search_features(args.docs_path, args.query)
        if features:
            print(f"# Features matching '{args.query}'\n")
            for feat in features:
                print(f"- **{feat['feature_id']}**: {feat['name']} ({feat['category']})")
        else:
            print(f"No features found matching '{args.query}'")

    else:
        results = search_docs(args.docs_path, args.query, args.category, args.max)
        print(format_results(results, args.verbose))


if __name__ == '__main__':
    main()
