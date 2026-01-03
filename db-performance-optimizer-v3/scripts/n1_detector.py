#!/usr/bin/env python3
"""
N+1 Query Detector for SQLAlchemy Applications
Detects N+1 query patterns in Python/SQLAlchemy code.

Usage:
    python3 n1_detector.py --path ./src
    python3 n1_detector.py --path ./src --format json
    python3 n1_detector.py --file ./src/models.py
"""

import argparse
import ast
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class N1Issue:
    """Represents a potential N+1 query issue."""
    file: str
    line: int
    code: str
    issue_type: str
    severity: str
    recommendation: str


class N1Detector(ast.NodeVisitor):
    """AST visitor to detect N+1 query patterns."""

    def __init__(self, filename: str, source: str):
        self.filename = filename
        self.source_lines = source.split("\n")
        self.issues: list[N1Issue] = []
        self.in_for_loop = False
        self.loop_depth = 0

    def get_line(self, lineno: int) -> str:
        """Get source line by line number."""
        if 0 < lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def visit_For(self, node):
        """Track for loop context."""
        self.in_for_loop = True
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_for_loop = False

    def visit_Attribute(self, node):
        """Detect lazy-loaded relationship access in loops."""
        if self.in_for_loop:
            # Check for common relationship patterns
            attr_name = node.attr
            # Common relationship attribute names
            relationship_patterns = [
                "orders", "items", "users", "posts", "comments",
                "children", "parent", "related", "tags", "categories",
                "products", "customers", "reviews", "messages"
            ]

            if attr_name in relationship_patterns:
                self.issues.append(N1Issue(
                    file=self.filename,
                    line=node.lineno,
                    code=self.get_line(node.lineno),
                    issue_type="lazy_loading_in_loop",
                    severity="high",
                    recommendation=f"Use joinedload() or selectinload() for '{attr_name}'"
                ))

        self.generic_visit(node)

    def visit_Call(self, node):
        """Detect query calls inside loops."""
        if self.in_for_loop:
            # Check for .query() or session.query() inside loops
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                dangerous_methods = ["query", "get", "filter", "filter_by", "first", "all"]

                if method_name in dangerous_methods:
                    self.issues.append(N1Issue(
                        file=self.filename,
                        line=node.lineno,
                        code=self.get_line(node.lineno),
                        issue_type="query_in_loop",
                        severity="critical",
                        recommendation="Move query outside loop or use batch loading"
                    ))

            # Check for session.execute() inside loops
            if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
                self.issues.append(N1Issue(
                    file=self.filename,
                    line=node.lineno,
                    code=self.get_line(node.lineno),
                    issue_type="execute_in_loop",
                    severity="critical",
                    recommendation="Batch queries or use CTE/subquery"
                ))

        self.generic_visit(node)


def detect_loading_patterns(source: str, filename: str) -> list[N1Issue]:
    """Detect loading strategy issues using regex."""
    issues = []

    # Pattern: .all() followed by iteration accessing relationships
    all_pattern = re.compile(r"\.all\(\)")
    for i, line in enumerate(source.split("\n"), 1):
        # Check for missing eager loading hints
        if ".query(" in line and ".all()" in line:
            if "joinedload" not in line and "selectinload" not in line:
                # Look ahead for loop patterns
                issues.append(N1Issue(
                    file=filename,
                    line=i,
                    code=line.strip(),
                    issue_type="potential_n1",
                    severity="medium",
                    recommendation="Consider adding eager loading if iterating relationships"
                ))

    return issues


def detect_lazy_relationship_definitions(source: str, filename: str) -> list[N1Issue]:
    """Detect relationship definitions without loading strategy."""
    issues = []

    # Pattern: relationship() without lazy parameter or with lazy='select'
    rel_pattern = re.compile(r"relationship\([^)]+\)")

    for i, line in enumerate(source.split("\n"), 1):
        match = rel_pattern.search(line)
        if match:
            rel_def = match.group(0)
            # Check if lazy loading strategy is defined
            if "lazy=" not in rel_def:
                issues.append(N1Issue(
                    file=filename,
                    line=i,
                    code=line.strip(),
                    issue_type="undefined_loading_strategy",
                    severity="low",
                    recommendation="Explicitly define lazy loading strategy"
                ))
            elif "lazy='select'" in rel_def or 'lazy="select"' in rel_def:
                issues.append(N1Issue(
                    file=filename,
                    line=i,
                    code=line.strip(),
                    issue_type="default_lazy_loading",
                    severity="info",
                    recommendation="Consider 'selectin' or 'joined' for frequently accessed relationships"
                ))

    return issues


def analyze_file(filepath: str) -> list[N1Issue]:
    """Analyze a single Python file for N+1 issues."""
    try:
        with open(filepath, "r") as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

    issues = []

    # AST-based detection
    try:
        tree = ast.parse(source)
        detector = N1Detector(filepath, source)
        detector.visit(tree)
        issues.extend(detector.issues)
    except SyntaxError as e:
        print(f"Syntax error in {filepath}: {e}")

    # Regex-based detection
    issues.extend(detect_loading_patterns(source, filepath))
    issues.extend(detect_lazy_relationship_definitions(source, filepath))

    return issues


def analyze_directory(dirpath: str) -> list[N1Issue]:
    """Analyze all Python files in a directory."""
    all_issues = []

    for root, dirs, files in os.walk(dirpath):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in [
            "__pycache__", ".git", "node_modules", "venv", ".venv", "dist"
        ]]

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                issues = analyze_file(filepath)
                all_issues.extend(issues)

    return all_issues


def format_markdown(issues: list[N1Issue]) -> str:
    """Format issues as markdown report."""
    lines = [
        "# N+1 Query Detection Report",
        "",
        f"**Total Issues Found:** {len(issues)}",
        "",
    ]

    # Group by severity
    critical = [i for i in issues if i.severity == "critical"]
    high = [i for i in issues if i.severity == "high"]
    medium = [i for i in issues if i.severity == "medium"]
    low = [i for i in issues if i.severity in ("low", "info")]

    if critical:
        lines.extend(["## Critical Issues", ""])
        for issue in critical:
            lines.append(f"### {issue.file}:{issue.line}")
            lines.append(f"```python\n{issue.code}\n```")
            lines.append(f"**Issue:** {issue.issue_type}")
            lines.append(f"**Recommendation:** {issue.recommendation}")
            lines.append("")

    if high:
        lines.extend(["## High Severity Issues", ""])
        for issue in high:
            lines.append(f"- **{issue.file}:{issue.line}** - {issue.issue_type}")
            lines.append(f"  - `{issue.code[:60]}...`")
            lines.append(f"  - Fix: {issue.recommendation}")

    if medium:
        lines.extend(["", "## Medium Severity Issues", ""])
        for issue in medium:
            lines.append(f"- {issue.file}:{issue.line} - {issue.recommendation}")

    if low:
        lines.extend(["", "## Suggestions", ""])
        for issue in low:
            lines.append(f"- {issue.file}:{issue.line} - {issue.recommendation}")

    if not issues:
        lines.append("No N+1 query issues detected.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Detect N+1 query patterns")
    parser.add_argument("--path", help="Directory to scan")
    parser.add_argument("--file", help="Single file to scan")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    if args.file:
        issues = analyze_file(args.file)
    elif args.path:
        issues = analyze_directory(args.path)
    else:
        print("Error: Provide --path or --file")
        return

    if args.format == "json":
        output = json.dumps([vars(i) for i in issues], indent=2)
    else:
        output = format_markdown(issues)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
