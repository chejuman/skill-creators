#!/usr/bin/env python3
"""Documentation validator for generated docs.

Validates markdown documentation for broken links, formatting issues,
and cross-reference consistency.

Usage:
    python validate_docs.py /path/to/docs [--fix]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def extract_links(content: str) -> list[tuple[str, str, int]]:
    """Extract all markdown links with line numbers."""
    links = []
    for i, line in enumerate(content.splitlines(), 1):
        # [text](link)
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', line):
            links.append((match.group(1), match.group(2), i))
        # Reference links [text][ref]
        for match in re.finditer(r'\[([^\]]+)\]\[([^\]]+)\]', line):
            links.append((match.group(1), f"ref:{match.group(2)}", i))
    return links


def extract_headings(content: str) -> list[tuple[str, int, int]]:
    """Extract all headings with level and line number."""
    headings = []
    for i, line in enumerate(content.splitlines(), 1):
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((text, level, i))
    return headings


def validate_internal_links(doc_path: Path, all_docs: list[Path]) -> list[dict[str, Any]]:
    """Validate internal links resolve to existing files."""
    issues = []
    content = doc_path.read_text()
    links = extract_links(content)
    doc_dir = doc_path.parent

    doc_names = {d.name.lower() for d in all_docs}
    doc_stems = {d.stem.lower() for d in all_docs}

    for text, link, line in links:
        # Skip external links
        if link.startswith(("http://", "https://", "mailto:", "#", "ref:")):
            continue

        # Resolve relative path
        link_path = link.split("#")[0]  # Remove anchor
        if not link_path:
            continue

        target = (doc_dir / link_path).resolve()

        if not target.exists():
            # Check if it's a relative doc reference
            if link_path.lower() not in doc_names and link_path.replace(".md", "").lower() not in doc_stems:
                issues.append({
                    "file": doc_path.name,
                    "line": line,
                    "type": "broken_link",
                    "message": f"Link target not found: {link}",
                    "link_text": text
                })

    return issues


def validate_headings(doc_path: Path) -> list[dict[str, Any]]:
    """Validate heading hierarchy and duplicates."""
    issues = []
    content = doc_path.read_text()
    headings = extract_headings(content)

    if not headings:
        return issues

    # Check for H1
    h1_headings = [h for h in headings if h[1] == 1]
    if len(h1_headings) == 0:
        issues.append({
            "file": doc_path.name,
            "line": 1,
            "type": "missing_h1",
            "message": "Document missing H1 heading"
        })
    elif len(h1_headings) > 1:
        issues.append({
            "file": doc_path.name,
            "line": h1_headings[1][2],
            "type": "multiple_h1",
            "message": f"Multiple H1 headings found (second at line {h1_headings[1][2]})"
        })

    # Check heading hierarchy (no skipping levels)
    prev_level = 0
    for text, level, line in headings:
        if level > prev_level + 1 and prev_level > 0:
            issues.append({
                "file": doc_path.name,
                "line": line,
                "type": "heading_skip",
                "message": f"Heading level skipped: H{prev_level} to H{level}"
            })
        prev_level = level

    return issues


def validate_code_blocks(doc_path: Path) -> list[dict[str, Any]]:
    """Validate code blocks have language tags."""
    issues = []
    content = doc_path.read_text()
    lines = content.splitlines()

    in_code_block = False
    code_block_start = 0

    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_start = i
                # Check for language tag
                lang = line.strip()[3:].strip()
                if not lang:
                    issues.append({
                        "file": doc_path.name,
                        "line": i,
                        "type": "missing_lang",
                        "message": "Code block missing language tag"
                    })
            else:
                in_code_block = False

    if in_code_block:
        issues.append({
            "file": doc_path.name,
            "line": code_block_start,
            "type": "unclosed_code",
            "message": "Unclosed code block"
        })

    return issues


def validate_mermaid(doc_path: Path) -> list[dict[str, Any]]:
    """Basic validation of Mermaid diagrams."""
    issues = []
    content = doc_path.read_text()

    # Find mermaid blocks
    mermaid_pattern = r'```mermaid\n(.*?)```'
    for match in re.finditer(mermaid_pattern, content, re.DOTALL):
        diagram = match.group(1)
        start_line = content[:match.start()].count('\n') + 1

        # Check for common issues
        if not diagram.strip():
            issues.append({
                "file": doc_path.name,
                "line": start_line,
                "type": "empty_mermaid",
                "message": "Empty Mermaid diagram"
            })
            continue

        # Check diagram type
        valid_types = ["graph", "flowchart", "sequenceDiagram", "classDiagram",
                      "stateDiagram", "erDiagram", "gantt", "pie", "journey"]
        first_word = diagram.strip().split()[0] if diagram.strip() else ""
        if first_word not in valid_types:
            issues.append({
                "file": doc_path.name,
                "line": start_line,
                "type": "invalid_mermaid_type",
                "message": f"Unknown Mermaid diagram type: {first_word}"
            })

    return issues


def validate_markers(doc_path: Path) -> list[dict[str, Any]]:
    """Find ASSUMPTION and NEEDS INPUT markers."""
    issues = []
    content = doc_path.read_text()

    for i, line in enumerate(content.splitlines(), 1):
        if "[ASSUMPTION]" in line:
            issues.append({
                "file": doc_path.name,
                "line": i,
                "type": "assumption_marker",
                "message": "Contains assumption that may need verification",
                "severity": "warning"
            })
        if "[NEEDS INPUT]" in line:
            issues.append({
                "file": doc_path.name,
                "line": i,
                "type": "needs_input_marker",
                "message": "Requires additional information",
                "severity": "warning"
            })

    return issues


def validate_docs(docs_path: str) -> dict[str, Any]:
    """Main validation function."""
    path = Path(docs_path).resolve()

    if not path.exists():
        return {"error": f"Path does not exist: {docs_path}"}

    # Find all markdown files
    if path.is_file():
        md_files = [path]
    else:
        md_files = list(path.glob("**/*.md"))

    if not md_files:
        return {"error": "No markdown files found"}

    all_issues = []
    for doc in md_files:
        all_issues.extend(validate_internal_links(doc, md_files))
        all_issues.extend(validate_headings(doc))
        all_issues.extend(validate_code_blocks(doc))
        all_issues.extend(validate_mermaid(doc))
        all_issues.extend(validate_markers(doc))

    # Categorize issues
    errors = [i for i in all_issues if i.get("severity") != "warning"]
    warnings = [i for i in all_issues if i.get("severity") == "warning"]

    return {
        "valid": len(errors) == 0,
        "issues": all_issues,
        "summary": {
            "total_docs": len(md_files),
            "docs_checked": [d.name for d in md_files],
            "total_issues": len(all_issues),
            "errors": len(errors),
            "warnings": len(warnings)
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Validate documentation")
    parser.add_argument("path", help="Path to docs directory or file")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()
    result = validate_docs(args.path)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        summary = result["summary"]
        print(f"Validation Results")
        print(f"=" * 40)
        print(f"Documents checked: {summary['total_docs']}")
        print(f"Total issues: {summary['total_issues']}")
        print(f"  Errors: {summary['errors']}")
        print(f"  Warnings: {summary['warnings']}")
        print()

        if result["issues"]:
            print("Issues found:")
            for issue in result["issues"]:
                severity = issue.get("severity", "error")
                icon = "⚠️" if severity == "warning" else "❌"
                print(f"  {icon} {issue['file']}:{issue['line']} - {issue['message']}")

        print()
        print("✅ Valid" if result["valid"] else "❌ Invalid")

    sys.exit(0 if result.get("valid", False) else 1)


if __name__ == "__main__":
    main()
