#!/usr/bin/env python3
"""
Auto-Citation Hook

Automatically formats GitHub code findings with proper citation format.
Ensures consistent permalink and snippet presentation.
"""

import json
import os
import re
import sys


def format_citation(permalink: str, snippet: str = None) -> str:
    """
    Format a GitHub permalink as a proper citation.

    Returns:
        Formatted citation string
    """
    # Extract components from permalink
    match = re.match(
        r'https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+?)(?:#L(\d+)(?:-L(\d+))?)?$',
        permalink
    )

    if not match:
        return permalink

    owner, repo, sha, path, start_line, end_line = match.groups()

    citation = f"""
**Evidence**: [{path}]({permalink})
- Repository: `{owner}/{repo}`
- SHA: `{sha[:7]}`
- Lines: L{start_line}{f'-L{end_line}' if end_line else ''}
"""

    if snippet:
        # Detect language from file extension
        ext = path.split('.')[-1] if '.' in path else ''
        lang_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'go': 'go',
            'rs': 'rust',
            'rb': 'ruby',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
        }
        lang = lang_map.get(ext, ext)

        citation += f"""
```{lang}
{snippet.strip()}
```
"""

    return citation


def main():
    """Main hook entry point."""
    # Get tool output
    tool_output = os.environ.get("TOOL_OUTPUT", "")
    if not tool_output:
        try:
            tool_output = sys.stdin.read()
        except Exception:
            tool_output = ""

    # Find GitHub permalinks that might need citation formatting
    permalinks = re.findall(
        r'https://github\.com/[^/]+/[^/]+/blob/[a-f0-9]{7,40}/[^\s\'")\]]+#L\d+(?:-L\d+)?',
        tool_output
    )

    if permalinks:
        # Log found permalinks for potential formatting
        result = {
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "citationsFound": len(permalinks),
                "permalinks": permalinks[:5]  # Limit to first 5
            }
        }
        print(json.dumps(result))
    else:
        print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
