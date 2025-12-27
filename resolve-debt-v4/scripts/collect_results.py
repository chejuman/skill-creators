#!/usr/bin/env python3
"""Collect and aggregate results from parallel analysis workers."""

import json
import sys
from typing import Any


def aggregate_results(worker_results: dict[str, list]) -> dict:
    """Aggregate results from all workers into unified structure."""
    all_issues = []
    stats = {}

    # Process each worker's results
    for worker_name, results in worker_results.items():
        if not results:
            stats[worker_name] = {"count": 0, "critical": 0, "high": 0, "medium": 0}
            continue

        worker_issues = results if isinstance(results, list) else []
        all_issues.extend(worker_issues)

        # Calculate stats
        critical = sum(1 for i in worker_issues if i.get("severity", 0) >= 5)
        high = sum(1 for i in worker_issues if 3 <= i.get("severity", 0) < 5)
        medium = sum(1 for i in worker_issues if i.get("severity", 0) < 3)

        stats[worker_name] = {
            "count": len(worker_issues),
            "critical": critical,
            "high": high,
            "medium": medium
        }

    # Sort all issues by severity (descending)
    all_issues.sort(key=lambda x: x.get("severity", 0), reverse=True)

    # Calculate totals
    total_critical = sum(s["critical"] for s in stats.values())
    total_high = sum(s["high"] for s in stats.values())
    total_medium = sum(s["medium"] for s in stats.values())

    return {
        "all_issues": all_issues,
        "total_count": len(all_issues),
        "critical_count": total_critical,
        "high_count": total_high,
        "medium_count": total_medium,
        "worker_stats": stats
    }


def calculate_effort(issues: list) -> dict:
    """Calculate total effort estimates."""
    total_hours = sum(i.get("effort_hours", 1) for i in issues)
    quick_wins = [i for i in issues if i.get("effort_hours", 1) <= 2 and i.get("severity", 0) >= 3]

    return {
        "total_hours": total_hours,
        "quick_win_count": len(quick_wins),
        "quick_win_hours": sum(i.get("effort_hours", 1) for i in quick_wins)
    }


def prioritize_issues(issues: list, correlations: dict = None) -> list:
    """Prioritize issues using RICE scoring."""
    prioritized = []

    for issue in issues:
        severity = issue.get("severity", 1)
        effort = issue.get("effort_hours", 1)
        churn = issue.get("churn_score", 1)

        # RICE-like scoring
        reach = min(10, severity * 2)  # Severity implies reach
        impact = severity * 2
        confidence = 0.8  # Default confidence
        effort_adjusted = max(0.5, effort)

        rice_score = (reach * impact * confidence) / effort_adjusted

        # Boost for root causes
        if correlations:
            for rc in correlations.get("root_causes", []):
                if issue.get("id") in rc.get("symptoms", []):
                    rice_score *= 1.5
                    break

        prioritized.append({
            **issue,
            "rice_score": round(rice_score, 2),
            "priority": "critical" if rice_score >= 50 else "high" if rice_score >= 20 else "medium"
        })

    # Sort by RICE score
    prioritized.sort(key=lambda x: x["rice_score"], reverse=True)
    return prioritized


def main():
    """Main entry point - reads JSON from stdin."""
    input_data = json.load(sys.stdin)

    worker_results = input_data.get("worker_results", {})
    correlations = input_data.get("correlations")

    # Aggregate
    aggregated = aggregate_results(worker_results)

    # Calculate effort
    effort = calculate_effort(aggregated["all_issues"])
    aggregated["effort"] = effort

    # Prioritize
    aggregated["prioritized_issues"] = prioritize_issues(
        aggregated["all_issues"],
        correlations
    )

    # Extract quick wins
    aggregated["quick_wins"] = [
        i for i in aggregated["prioritized_issues"]
        if i.get("effort_hours", 1) <= 2 and i.get("rice_score", 0) >= 20
    ]

    print(json.dumps(aggregated, indent=2))


if __name__ == "__main__":
    main()
