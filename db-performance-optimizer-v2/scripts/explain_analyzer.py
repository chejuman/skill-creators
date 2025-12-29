#!/usr/bin/env python3
"""
EXPLAIN ANALYZE Parser for PostgreSQL
Parses and analyzes query execution plans for optimization opportunities.

Usage:
    python3 explain_analyzer.py --db-url postgresql://... --query "SELECT ..."
    python3 explain_analyzer.py --file query.sql --db-url postgresql://...
    cat query.sql | python3 explain_analyzer.py --db-url postgresql://... --stdin
"""

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import Session
except ImportError:
    print("Error: SQLAlchemy not installed. Run: pip install sqlalchemy psycopg2-binary")
    exit(1)


@dataclass
class PlanNode:
    """Execution plan node."""
    node_type: str
    actual_time: float
    actual_rows: int
    planned_rows: int
    loops: int
    cost: float
    width: int
    issues: list[str]
    children: list


@dataclass
class PlanIssue:
    """Identified issue in execution plan."""
    severity: str  # critical, high, medium, low
    issue_type: str
    description: str
    recommendation: str
    node_info: str


# Issue detection patterns
ISSUE_PATTERNS = [
    {
        "pattern": r"Seq Scan on (\w+)",
        "severity": "high",
        "type": "sequential_scan",
        "description": "Sequential scan on table {table}",
        "recommendation": "Consider adding an index. Check WHERE clause columns."
    },
    {
        "pattern": r"Nested Loop.*rows=(\d+).*loops=(\d+)",
        "severity": "medium",
        "type": "nested_loop",
        "description": "Nested Loop with {rows} rows, {loops} loops",
        "recommendation": "May cause N+1 pattern. Consider JOIN optimization or batch loading."
    },
    {
        "pattern": r"Sort.*Sort Method: external",
        "severity": "high",
        "type": "external_sort",
        "description": "Sort operation spilled to disk",
        "recommendation": "Increase work_mem or add covering index with ORDER BY columns."
    },
    {
        "pattern": r"Hash.*Batches: (\d+)",
        "severity": "medium",
        "type": "hash_batches",
        "description": "Hash operation used {batches} batches",
        "recommendation": "Multiple batches indicate memory pressure. Increase work_mem."
    },
    {
        "pattern": r"Rows Removed by Filter: (\d+)",
        "severity": "medium",
        "type": "filter_removal",
        "description": "{rows} rows removed by filter",
        "recommendation": "Consider adding partial index or reviewing query selectivity."
    },
    {
        "pattern": r"actual.*rows=(\d+).*planned.*rows=(\d+)",
        "severity": "low",
        "type": "estimate_mismatch",
        "description": "Row estimate mismatch (actual vs planned)",
        "recommendation": "Run ANALYZE to update statistics."
    }
]


def run_explain_analyze(engine, query: str) -> tuple[str, list[dict]]:
    """Run EXPLAIN ANALYZE and return text and JSON output."""
    with Session(engine) as session:
        # Get text output
        text_result = session.execute(text(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) {query}"))
        text_output = "\n".join([row[0] for row in text_result])

        # Get JSON output for structured parsing
        json_result = session.execute(text(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"))
        json_output = json_result.fetchone()[0]

    return text_output, json_output


def detect_issues(explain_text: str) -> list[PlanIssue]:
    """Detect issues in execution plan."""
    issues = []

    for pattern_info in ISSUE_PATTERNS:
        matches = re.finditer(pattern_info["pattern"], explain_text, re.IGNORECASE)
        for match in matches:
            groups = match.groups() if match.groups() else ()

            # Format description with captured groups
            desc = pattern_info["description"]
            if groups:
                if "{table}" in desc and groups:
                    desc = desc.format(table=groups[0])
                elif "{rows}" in desc and "{loops}" in desc and len(groups) >= 2:
                    desc = desc.format(rows=groups[0], loops=groups[1])
                elif "{batches}" in desc and groups:
                    desc = desc.format(batches=groups[0])
                elif "{rows}" in desc and groups:
                    desc = desc.format(rows=groups[0])

            issues.append(PlanIssue(
                severity=pattern_info["severity"],
                issue_type=pattern_info["type"],
                description=desc,
                recommendation=pattern_info["recommendation"],
                node_info=match.group(0)[:100]
            ))

    # Check for row estimate mismatches
    actual_vs_planned = re.findall(r"actual.*?rows=(\d+).*?(?:rows=(\d+))?", explain_text)
    for actual, planned in actual_vs_planned:
        if planned and int(actual) > 0:
            ratio = int(planned) / max(int(actual), 1)
            if ratio > 10 or ratio < 0.1:
                issues.append(PlanIssue(
                    severity="medium",
                    issue_type="estimate_mismatch",
                    description=f"Large row estimate mismatch: actual={actual}, planned={planned}",
                    recommendation="Run ANALYZE to update statistics",
                    node_info=f"Ratio: {ratio:.2f}x"
                ))

    return issues


def parse_json_plan(plan: list[dict]) -> dict:
    """Parse JSON execution plan for metrics."""
    if not plan:
        return {}

    root = plan[0].get("Plan", {})

    def extract_metrics(node: dict) -> dict:
        metrics = {
            "node_type": node.get("Node Type", "Unknown"),
            "actual_total_time": node.get("Actual Total Time", 0),
            "actual_rows": node.get("Actual Rows", 0),
            "plan_rows": node.get("Plan Rows", 0),
            "shared_hit_blocks": node.get("Shared Hit Blocks", 0),
            "shared_read_blocks": node.get("Shared Read Blocks", 0),
        }

        children = node.get("Plans", [])
        metrics["children"] = [extract_metrics(c) for c in children]

        return metrics

    return {
        "execution_time": plan[0].get("Execution Time", 0),
        "planning_time": plan[0].get("Planning Time", 0),
        "root": extract_metrics(root)
    }


def calculate_cache_ratio(plan_metrics: dict) -> float:
    """Calculate buffer cache hit ratio from plan."""
    def sum_blocks(node: dict) -> tuple[int, int]:
        hits = node.get("shared_hit_blocks", 0)
        reads = node.get("shared_read_blocks", 0)

        for child in node.get("children", []):
            child_hits, child_reads = sum_blocks(child)
            hits += child_hits
            reads += child_reads

        return hits, reads

    root = plan_metrics.get("root", {})
    hits, reads = sum_blocks(root)
    total = hits + reads

    if total > 0:
        return round(100.0 * hits / total, 2)
    return 100.0


def format_markdown(explain_text: str, plan_metrics: dict, issues: list[PlanIssue]) -> str:
    """Format as markdown report."""
    lines = [
        "# EXPLAIN ANALYZE Report",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Execution Summary",
        "",
        f"- **Execution Time:** {plan_metrics.get('execution_time', 'N/A')} ms",
        f"- **Planning Time:** {plan_metrics.get('planning_time', 'N/A')} ms",
        f"- **Cache Hit Ratio:** {calculate_cache_ratio(plan_metrics)}%",
        "",
    ]

    if issues:
        # Group by severity
        critical = [i for i in issues if i.severity == "critical"]
        high = [i for i in issues if i.severity == "high"]
        medium = [i for i in issues if i.severity == "medium"]

        if critical or high:
            lines.extend([
                "## Critical/High Priority Issues",
                "",
            ])
            for issue in critical + high:
                lines.append(f"### {issue.issue_type.replace('_', ' ').title()}")
                lines.append(f"**Severity:** {issue.severity.upper()}")
                lines.append(f"**Issue:** {issue.description}")
                lines.append(f"**Recommendation:** {issue.recommendation}")
                lines.append("")

        if medium:
            lines.extend([
                "## Medium Priority Issues",
                "",
            ])
            for issue in medium:
                lines.append(f"- **{issue.issue_type}:** {issue.description}")
                lines.append(f"  - Fix: {issue.recommendation}")

    lines.extend([
        "",
        "## Full Execution Plan",
        "",
        "```",
        explain_text,
        "```",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze EXPLAIN ANALYZE output")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--query", help="SQL query to analyze")
    parser.add_argument("--file", help="File containing SQL query")
    parser.add_argument("--stdin", action="store_true", help="Read query from stdin")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    # Get query
    if args.query:
        query = args.query
    elif args.file:
        with open(args.file) as f:
            query = f.read()
    elif args.stdin:
        import sys
        query = sys.stdin.read()
    else:
        print("Error: Provide --query, --file, or --stdin")
        return

    engine = create_engine(args.db_url)

    try:
        explain_text, json_plan = run_explain_analyze(engine, query)
        issues = detect_issues(explain_text)
        plan_metrics = parse_json_plan(json_plan)

        if args.format == "json":
            output = json.dumps({
                "timestamp": datetime.now().isoformat(),
                "query": query[:500],
                "metrics": plan_metrics,
                "issues": [vars(i) for i in issues],
                "explain_text": explain_text
            }, indent=2, default=str)
        else:
            output = format_markdown(explain_text, plan_metrics, issues)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Report written to {args.output}")
        else:
            print(output)

    except Exception as e:
        print(f"Error analyzing query: {e}")


if __name__ == "__main__":
    main()
