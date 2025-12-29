#!/usr/bin/env python3
"""
Search Docs for Feature Spec Dev 2
Full-text search across all .spec-docs/ documentation.

Usage:
    python3 search_docs.py --query "authentication"
    python3 search_docs.py --query "API" --phase requirements
"""

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


SPEC_DOCS_DIR = ".spec-docs"


@dataclass
class SearchResult:
    file_path: str
    line_number: int
    line_content: str
    context_before: list
    context_after: list


def get_docs_path(base_path: str = ".") -> Path:
    return Path(base_path) / SPEC_DOCS_DIR


def search_file(file_path: Path, query: str, context_lines: int = 2) -> list:
    """Search a single file for the query."""
    results = []

    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError):
        return results

    query_lower = query.lower()

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)

            results.append(SearchResult(
                file_path=str(file_path),
                line_number=i + 1,
                line_content=line.strip(),
                context_before=[l.strip() for l in lines[start:i]],
                context_after=[l.strip() for l in lines[i+1:end]]
            ))

    return results


def search_docs(query: str, base_path: str = ".", phase: Optional[str] = None,
                context_lines: int = 2, limit: int = 50) -> dict:
    """Search all documentation for the query."""
    docs = get_docs_path(base_path)

    if not docs.exists():
        return {"error": ".spec-docs directory not found", "results": []}

    if phase:
        search_dirs = [docs / phase]
    else:
        search_dirs = [
            docs / "discovery",
            docs / "requirements",
            docs / "design",
            docs / "tasks",
            docs / "tracking"
        ]

    all_results = []
    files_searched = 0
    files_with_matches = set()

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for file_path in search_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".md", ".json"]:
                files_searched += 1
                results = search_file(file_path, query, context_lines)

                if results:
                    files_with_matches.add(str(file_path))
                    all_results.extend(results)

                    if len(all_results) >= limit:
                        break

        if len(all_results) >= limit:
            break

    return {
        "query": query,
        "files_searched": files_searched,
        "files_with_matches": len(files_with_matches),
        "total_matches": len(all_results),
        "results": all_results[:limit]
    }


def format_results(search_result: dict) -> str:
    """Format search results as markdown."""
    output = f"""# Search Results for "{search_result['query']}"

**Files Searched:** {search_result['files_searched']}
**Files with Matches:** {search_result['files_with_matches']}
**Total Matches:** {search_result['total_matches']}

---

"""

    if not search_result["results"]:
        output += "No results found.\n"
        return output

    by_file = {}
    for result in search_result["results"]:
        file_path = result.file_path if isinstance(result, SearchResult) else result["file_path"]
        if file_path not in by_file:
            by_file[file_path] = []
        by_file[file_path].append(result)

    for file_path, results in by_file.items():
        rel_path = file_path.replace(SPEC_DOCS_DIR + "/", "")
        output += f"## {rel_path} ({len(results)} matches)\n\n"

        for result in results[:5]:
            if isinstance(result, SearchResult):
                line_num = result.line_number
                line_content = result.line_content
            else:
                line_num = result["line_number"]
                line_content = result["line_content"]

            output += f"**Line {line_num}:**\n"
            output += f"```\n{line_content}\n```\n\n"

        if len(results) > 5:
            output += f"*...and {len(results) - 5} more matches*\n\n"

        output += "---\n\n"

    return output


def main():
    parser = argparse.ArgumentParser(description="Search spec documentation")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--path", default=".", help="Base path")
    parser.add_argument("--phase", choices=["discovery", "requirements", "design", "tasks", "tracking"],
                        help="Limit to specific phase")
    parser.add_argument("--context", type=int, default=2, help="Context lines")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    results = search_docs(
        query=args.query,
        base_path=args.path,
        phase=args.phase,
        context_lines=args.context,
        limit=args.limit
    )

    if args.format == "json":
        json_results = {
            **results,
            "results": [
                {
                    "file_path": r.file_path,
                    "line_number": r.line_number,
                    "line_content": r.line_content,
                    "context_before": r.context_before,
                    "context_after": r.context_after
                } if isinstance(r, SearchResult) else r
                for r in results["results"]
            ]
        }
        print(json.dumps(json_results, indent=2))
    else:
        print(format_results(results))


if __name__ == "__main__":
    main()
