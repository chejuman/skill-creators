#!/usr/bin/env python3
"""
Metrics Collector for Retrospective V2
Collects git and code metrics from repository for retrospective analysis.

Usage:
    python3 metrics_collector.py [--scope HEAD~10] [--format json|table] [--output FILE]
"""

import subprocess
import json
import argparse
import os
from datetime import datetime
from collections import defaultdict


def run_git(cmd: list[str]) -> str:
    """Execute git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_commit_stats(scope: str) -> dict:
    """Get commit statistics for the given scope."""
    # Get commit count
    log_output = run_git(["log", "--oneline", scope])
    commits = log_output.split("\n") if log_output else []
    commit_count = len([c for c in commits if c])

    # Get author stats
    author_output = run_git(["shortlog", "-sn", scope])
    authors = []
    for line in author_output.split("\n"):
        if line.strip():
            parts = line.strip().split("\t")
            if len(parts) == 2:
                authors.append({
                    "name": parts[1],
                    "commits": int(parts[0].strip())
                })

    # Get date range
    first_date = run_git(["log", "--format=%ai", "--reverse", scope, "-1"])
    last_date = run_git(["log", "--format=%ai", scope, "-1"])

    # Get commit frequency by day
    day_output = run_git(["log", "--format=%ad", "--date=format:%A", scope])
    by_day = defaultdict(int)
    for day in day_output.split("\n"):
        if day:
            by_day[day] += 1

    return {
        "commit_count": commit_count,
        "date_range": {
            "start": first_date[:10] if first_date else None,
            "end": last_date[:10] if last_date else None
        },
        "authors": authors,
        "by_day": dict(by_day)
    }


def get_file_stats(scope: str) -> dict:
    """Get file change statistics."""
    # Get changed files
    diff_output = run_git(["diff", "--name-only", scope])
    files = [f for f in diff_output.split("\n") if f]

    # Count by extension
    by_extension = defaultdict(int)
    for f in files:
        ext = os.path.splitext(f)[1] or "no-ext"
        by_extension[ext] += 1

    # Get hotspots (most frequently changed)
    hotspot_output = run_git([
        "log", "--format=", "--name-only", scope
    ])
    hotspot_count = defaultdict(int)
    for f in hotspot_output.split("\n"):
        if f:
            hotspot_count[f] += 1

    hotspots = sorted(
        [{"file": f, "changes": c} for f, c in hotspot_count.items()],
        key=lambda x: x["changes"],
        reverse=True
    )[:10]

    return {
        "files_changed": len(files),
        "by_extension": dict(by_extension),
        "hotspots": hotspots
    }


def get_test_coverage_ratio() -> dict:
    """Calculate test file to source file ratio."""
    # Find test files
    test_patterns = ["*test*", "*spec*", "*_test.*", "*.test.*"]
    test_files = 0
    source_files = 0

    for root, dirs, files in os.walk("."):
        # Skip node_modules, .git, etc.
        dirs[:] = [d for d in dirs if d not in [
            "node_modules", ".git", "dist", "build", "__pycache__"
        ]]
        for f in files:
            if any(ext in f for ext in [".ts", ".tsx", ".js", ".jsx", ".py"]):
                if any(pattern.replace("*", "") in f.lower() for pattern in ["test", "spec"]):
                    test_files += 1
                else:
                    source_files += 1

    ratio = test_files / source_files if source_files > 0 else 0

    return {
        "test_files": test_files,
        "source_files": source_files,
        "ratio": round(ratio, 2)
    }


def get_merge_revert_stats(scope: str) -> dict:
    """Get merge and revert statistics."""
    log_output = run_git(["log", "--oneline", scope])
    lines = log_output.split("\n") if log_output else []

    merges = len([l for l in lines if "merge" in l.lower()])
    reverts = len([l for l in lines if "revert" in l.lower()])

    return {
        "merge_count": merges,
        "revert_count": reverts
    }


def collect_all_metrics(scope: str) -> dict:
    """Collect all metrics and return as structured JSON."""
    return {
        "phase": "COLLECT",
        "agent_id": "metrics-collector",
        "timestamp": datetime.now().isoformat(),
        "scope": scope,
        "data": {
            "commits": get_commit_stats(scope),
            "files": get_file_stats(scope),
            "test_coverage": get_test_coverage_ratio(),
            "merge_reverts": get_merge_revert_stats(scope)
        },
        "confidence": 0.9
    }


def format_table(metrics: dict) -> str:
    """Format metrics as a readable table."""
    data = metrics["data"]
    lines = [
        "# Retrospective Metrics",
        f"**Scope:** {metrics['scope']}",
        f"**Collected:** {metrics['timestamp'][:10]}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Commits | {data['commits']['commit_count']} |",
        f"| Files Changed | {data['files']['files_changed']} |",
        f"| Authors | {len(data['commits']['authors'])} |",
        f"| Test Ratio | {data['test_coverage']['ratio']:.0%} |",
        f"| Merges | {data['merge_reverts']['merge_count']} |",
        f"| Reverts | {data['merge_reverts']['revert_count']} |",
        "",
        "## Top Hotspots",
        "",
        "| File | Changes |",
        "|------|---------|",
    ]

    for h in data['files']['hotspots'][:5]:
        lines.append(f"| {h['file']} | {h['changes']} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Collect retrospective metrics")
    parser.add_argument("--scope", default="HEAD~10", help="Git scope (default: HEAD~10)")
    parser.add_argument("--format", choices=["json", "table"], default="json")
    parser.add_argument("--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    metrics = collect_all_metrics(args.scope)

    if args.format == "json":
        output = json.dumps(metrics, indent=2, ensure_ascii=False)
    else:
        output = format_table(metrics)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Metrics written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
