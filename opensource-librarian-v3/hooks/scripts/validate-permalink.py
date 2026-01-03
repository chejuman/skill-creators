#!/usr/bin/env python3
"""
Validate GitHub Permalinks Hook

Validates that all GitHub URLs in tool output contain proper SHA references
instead of branch names. Warns if branch names are detected.
"""

import json
import os
import re
import sys


def validate_permalink(url: str) -> tuple[bool, str]:
    """
    Validate that a GitHub URL contains SHA instead of branch name.

    Returns:
        (is_valid, message)
    """
    if not url.startswith("https://github.com/"):
        return True, ""  # Not a GitHub URL, skip

    # Extract the blob/SHA part
    match = re.search(r'/blob/([^/]+)/', url)
    if not match:
        return True, ""  # Not a file URL, skip

    ref = match.group(1)

    # Branch names to reject
    branch_names = ["main", "master", "develop", "dev", "HEAD", "release", "staging"]

    if ref in branch_names:
        return False, f"Branch name '{ref}' used instead of SHA in: {url}"

    # Check if it looks like a SHA (7-40 hex chars)
    if not re.match(r'^[a-f0-9]{7,40}$', ref):
        return False, f"Invalid SHA format '{ref}' in: {url}"

    # Check for line numbers
    if '#L' not in url:
        return False, f"Missing line numbers in: {url}"

    return True, ""


def main():
    """Main hook entry point."""
    # Get tool output from environment or stdin
    tool_output = os.environ.get("TOOL_OUTPUT", "")
    if not tool_output:
        try:
            tool_output = sys.stdin.read()
        except Exception:
            tool_output = ""

    # Find all GitHub URLs
    urls = re.findall(r'https://github\.com/[^\s\'")\]]+', tool_output)

    issues = []
    for url in urls:
        is_valid, message = validate_permalink(url)
        if not is_valid:
            issues.append(message)

    if issues:
        result = {
            "continue": True,
            "systemMessage": "Permalink validation warnings:\n" + "\n".join(f"- {i}" for i in issues)
        }
        print(json.dumps(result))
    else:
        print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
