#!/usr/bin/env python3
"""
JSON Report Generator - Generate structured JSON API output for DB optimization.

Usage:
    python json_report.py --input analysis.json --output report.json
    python json_report.py --db-url postgresql://... --depth 5
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any


def calculate_health_score(analysis: dict) -> dict:
    """Calculate overall health score and category scores."""
    scores = {
        "indexing": 25,
        "queryPerf": 25,
        "maintenance": 25,
        "architecture": 25
    }
    issues = {
        "indexing": 0,
        "queryPerf": 0,
        "maintenance": 0,
        "architecture": 0
    }

    # Deduct points for issues
    if "index_analysis" in analysis:
        unused = len(analysis["index_analysis"].get("unused_indexes", []))
        missing = len(analysis["index_analysis"].get("missing_indexes", []))
        issues["indexing"] = unused + missing
        scores["indexing"] = max(0, 25 - (unused * 2) - (missing * 3))

    if "n1_issues" in analysis:
        n1_count = len(analysis.get("n1_issues", []))
        issues["queryPerf"] = n1_count
        scores["queryPerf"] = max(0, 25 - (n1_count * 5))

    if "vacuum_candidates" in analysis:
        vacuum_count = len(analysis.get("vacuum_candidates", []))
        issues["maintenance"] = vacuum_count
        scores["maintenance"] = max(0, 25 - (vacuum_count * 3))

    if "pooling_recommendations" in analysis:
        arch_issues = len(analysis.get("pooling_recommendations", []))
        issues["architecture"] = arch_issues
        scores["architecture"] = max(0, 25 - (arch_issues * 2))

    total = sum(scores.values())

    return {
        "healthScore": total,
        "categories": {
            k: {"score": scores[k], "issues": issues[k]}
            for k in scores
        }
    }


def extract_metrics(analysis: dict) -> dict:
    """Extract key metrics with current/projected/improvement."""
    return {
        "avgQueryTime": {
            "current": analysis.get("avg_query_time", "N/A"),
            "projected": "10ms",
            "improvement": "10x"
        },
        "cacheHitRatio": {
            "current": analysis.get("cache_hit_ratio", "N/A"),
            "projected": "99%",
            "improvement": "+5%"
        },
        "n1Queries": {
            "current": str(len(analysis.get("n1_issues", []))),
            "projected": "0",
            "improvement": "-100%"
        },
        "deadTupleRatio": {
            "current": analysis.get("dead_tuple_ratio", "N/A"),
            "projected": "< 1%",
            "improvement": "-90%"
        },
        "connectionUsage": {
            "current": analysis.get("connection_usage", "N/A"),
            "projected": "< 80%",
            "improvement": "optimized"
        }
    }


def prioritize_recommendations(analysis: dict) -> dict:
    """Categorize recommendations by priority."""
    p1 = []  # Critical
    p2 = []  # High
    p3 = []  # Medium

    # N+1 issues are always P1
    for i, issue in enumerate(analysis.get("n1_issues", [])):
        p1.append({
            "id": f"n1-{i+1:03d}",
            "type": "orm",
            "title": f"Fix N+1 query in {issue.get('file', 'unknown')}",
            "description": issue.get("fix", "Add eager loading"),
            "impact": "High - reduces query count by 100x",
            "effort": "low",
            "risk": "low",
            "code": issue.get("optimized_code", "")
        })

    # Missing indexes are P1 or P2
    for i, idx in enumerate(analysis.get("missing_indexes", [])):
        priority = p1 if idx.get("priority") == "P1" else p2
        priority.append({
            "id": f"idx-{i+1:03d}",
            "type": "index",
            "title": f"Create index on {idx.get('table', 'unknown')}",
            "description": idx.get("reason", "Improve query performance"),
            "impact": idx.get("estimated_improvement", "5x faster"),
            "effort": "low",
            "risk": "low",
            "code": idx.get("create_statement", "")
        })

    # Vacuum issues are P2
    for i, vac in enumerate(analysis.get("vacuum_candidates", [])):
        p2.append({
            "id": f"vac-{i+1:03d}",
            "type": "vacuum",
            "title": f"Vacuum {vac.get('table', 'unknown')}",
            "description": f"Dead tuple ratio: {vac.get('dead_ratio', 'N/A')}%",
            "impact": "Reclaim space, improve performance",
            "effort": "low",
            "risk": "low",
            "code": f"VACUUM (ANALYZE, VERBOSE) {vac.get('table', '')};"
        })

    # Config recommendations are P3
    for i, cfg in enumerate(analysis.get("config_recommendations", [])):
        p3.append({
            "id": f"cfg-{i+1:03d}",
            "type": "config",
            "title": cfg.get("setting", "Configuration change"),
            "description": cfg.get("reason", ""),
            "impact": cfg.get("impact", "Performance improvement"),
            "effort": "medium",
            "risk": "medium",
            "code": cfg.get("apply_statement", "")
        })

    return {
        "p1_critical": p1,
        "p2_high": p2,
        "p3_medium": p3
    }


def generate_implementation(recommendations: dict) -> dict:
    """Generate implementation scripts from recommendations."""
    sql_indexes = []
    sql_vacuum = []
    sql_config = []
    orm_fixes = []

    for rec in recommendations["p1_critical"] + recommendations["p2_high"]:
        if rec["type"] == "index" and rec.get("code"):
            sql_indexes.append(rec["code"])
        elif rec["type"] == "vacuum" and rec.get("code"):
            sql_vacuum.append(rec["code"])
        elif rec["type"] == "config" and rec.get("code"):
            sql_config.append(rec["code"])
        elif rec["type"] == "orm" and rec.get("code"):
            orm_fixes.append({
                "file": rec.get("title", "").split(" in ")[-1] if " in " in rec.get("title", "") else "unknown",
                "original": "",
                "fixed": rec["code"],
                "explanation": rec.get("description", "")
            })

    return {
        "sql": {
            "indexes": sql_indexes,
            "vacuum": sql_vacuum,
            "config": sql_config
        },
        "python": {
            "orm_fixes": orm_fixes
        },
        "config": {}
    }


def build_api_response(analysis: dict, metadata: dict) -> dict:
    """Build complete JSON API response."""
    health = calculate_health_score(analysis)
    metrics = extract_metrics(analysis)
    recommendations = prioritize_recommendations(analysis)
    implementation = generate_implementation(recommendations)

    response = {
        "apiVersion": "v3",
        "metadata": {
            "generated": datetime.now().isoformat(),
            "depth": metadata.get("depth", 3),
            "database": metadata.get("database", "unknown"),
            "workersUsed": metadata.get("workers", 9),
            "pgVersion": metadata.get("pg_version", ""),
            "timescaleVersion": metadata.get("timescale_version", ""),
            "mode": metadata.get("mode", "full")
        },
        "summary": {
            "healthScore": health["healthScore"],
            "categories": health["categories"],
            "metrics": metrics
        },
        "recommendations": recommendations,
        "implementation": implementation
    }

    # Add TimescaleDB section if applicable
    if analysis.get("timescale"):
        response["timescale"] = analysis["timescale"]

    # Add AI insights if available
    if analysis.get("ai_insights"):
        response["aiInsights"] = analysis["ai_insights"]

    return response


def main():
    parser = argparse.ArgumentParser(description="Generate JSON API report")
    parser.add_argument("--input", help="Input analysis JSON file")
    parser.add_argument("--output", help="Output JSON file (stdout if not specified)")
    parser.add_argument("--depth", type=int, default=3, help="Analysis depth level")
    parser.add_argument("--database", default="unknown", help="Database name")
    args = parser.parse_args()

    # Load analysis data
    if args.input and os.path.exists(args.input):
        with open(args.input) as f:
            analysis = json.load(f)
    else:
        # Empty analysis for demo
        analysis = {
            "n1_issues": [],
            "missing_indexes": [],
            "vacuum_candidates": [],
            "config_recommendations": []
        }

    metadata = {
        "depth": args.depth,
        "database": args.database,
        "workers": 5 + (args.depth * 2)
    }

    response = build_api_response(analysis, metadata)

    output = json.dumps(response, indent=2, default=str)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
