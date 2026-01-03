#!/usr/bin/env python3
"""
Vacuum Analyzer for PostgreSQL
Analyzes table bloat, dead tuples, and vacuum effectiveness.

Usage:
    python3 vacuum_analyzer.py --db-url postgresql://user:pass@host/db
    python3 vacuum_analyzer.py --db-url postgresql://... --threshold 10
"""

import argparse
import json
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
class VacuumIssue:
    """Vacuum-related issue."""
    table: str
    dead_tuples: int
    live_tuples: int
    dead_ratio: float
    last_vacuum: Optional[str]
    last_autovacuum: Optional[str]
    severity: str
    recommendation: str


# SQL queries for vacuum analysis
TABLE_BLOAT_SQL = """
SELECT
    schemaname,
    relname as table_name,
    n_live_tup as live_tuples,
    n_dead_tup as dead_tuples,
    CASE WHEN n_live_tup > 0
        THEN round(100.0 * n_dead_tup / (n_live_tup + n_dead_tup), 2)
        ELSE 0
    END as dead_ratio,
    last_vacuum,
    last_autovacuum,
    vacuum_count,
    autovacuum_count,
    pg_size_pretty(pg_total_relation_size(relid)) as table_size
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY n_dead_tup DESC
LIMIT :limit;
"""

BLOAT_ESTIMATION_SQL = """
SELECT
    current_database() as db,
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) as table_size,
    pg_size_pretty(pg_indexes_size(schemaname || '.' || tablename::regclass)) as index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
LIMIT :limit;
"""

AUTOVACUUM_SETTINGS_SQL = """
SELECT
    name,
    setting,
    unit,
    short_desc
FROM pg_settings
WHERE name LIKE 'autovacuum%'
ORDER BY name;
"""

VACUUM_PROGRESS_SQL = """
SELECT
    p.pid,
    p.datname,
    p.relid::regclass as table_name,
    p.phase,
    p.heap_blks_total,
    p.heap_blks_scanned,
    CASE WHEN p.heap_blks_total > 0
        THEN round(100.0 * p.heap_blks_scanned / p.heap_blks_total, 2)
        ELSE 0
    END as progress_percent
FROM pg_stat_progress_vacuum p
JOIN pg_stat_activity a ON p.pid = a.pid;
"""


def get_table_bloat(engine, limit: int = 20, threshold: float = 10.0) -> list[VacuumIssue]:
    """Get tables with significant dead tuple bloat."""
    issues = []
    with Session(engine) as session:
        result = session.execute(text(TABLE_BLOAT_SQL), {"limit": limit})
        for row in result:
            r = dict(row._mapping)
            dead_ratio = float(r.get("dead_ratio", 0) or 0)

            if dead_ratio >= threshold:
                severity = "critical" if dead_ratio > 30 else "high" if dead_ratio > 20 else "medium"
                recommendation = f"VACUUM ANALYZE {r['table_name']};"
                if dead_ratio > 30:
                    recommendation = f"VACUUM FULL {r['table_name']}; -- High bloat, consider off-peak"

                issues.append(VacuumIssue(
                    table=r["table_name"],
                    dead_tuples=r["dead_tuples"],
                    live_tuples=r["live_tuples"],
                    dead_ratio=dead_ratio,
                    last_vacuum=str(r["last_vacuum"]) if r["last_vacuum"] else None,
                    last_autovacuum=str(r["last_autovacuum"]) if r["last_autovacuum"] else None,
                    severity=severity,
                    recommendation=recommendation
                ))
    return issues


def get_autovacuum_settings(engine) -> dict:
    """Get current autovacuum settings."""
    settings = {}
    with Session(engine) as session:
        result = session.execute(text(AUTOVACUUM_SETTINGS_SQL))
        for row in result:
            r = dict(row._mapping)
            settings[r["name"]] = {
                "value": r["setting"],
                "unit": r["unit"],
                "description": r["short_desc"]
            }
    return settings


def get_vacuum_progress(engine) -> list[dict]:
    """Get currently running vacuum operations."""
    with Session(engine) as session:
        try:
            result = session.execute(text(VACUUM_PROGRESS_SQL))
            return [dict(row._mapping) for row in result]
        except Exception:
            return []


def generate_autovacuum_recommendations(issues: list[VacuumIssue], settings: dict) -> list[str]:
    """Generate autovacuum tuning recommendations."""
    recommendations = []

    if len([i for i in issues if i.severity == "critical"]) > 3:
        recommendations.append(
            "-- Too many tables with critical bloat. Consider tuning autovacuum:\n"
            "ALTER SYSTEM SET autovacuum_vacuum_scale_factor = 0.05;  -- Default 0.2\n"
            "ALTER SYSTEM SET autovacuum_vacuum_threshold = 25;  -- Default 50\n"
            "SELECT pg_reload_conf();"
        )

    current_workers = int(settings.get("autovacuum_max_workers", {}).get("value", 3))
    if len(issues) > current_workers * 5:
        recommendations.append(
            f"-- Consider increasing autovacuum workers:\n"
            f"ALTER SYSTEM SET autovacuum_max_workers = {min(current_workers + 2, 8)};\n"
            f"-- Requires restart"
        )

    return recommendations


def format_markdown(issues: list[VacuumIssue], settings: dict, recommendations: list[str]) -> str:
    """Format as markdown report."""
    lines = [
        "# Vacuum Analysis Report",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Tables with bloat issues: {len(issues)}",
        f"- Critical issues: {len([i for i in issues if i.severity == 'critical'])}",
        f"- High issues: {len([i for i in issues if i.severity == 'high'])}",
        "",
    ]

    if issues:
        lines.extend([
            "## Tables Needing Vacuum",
            "",
            "| Table | Dead Tuples | Dead Ratio | Severity | Last Vacuum |",
            "|-------|-------------|------------|----------|-------------|",
        ])
        for issue in issues:
            lines.append(
                f"| {issue.table} | {issue.dead_tuples:,} | {issue.dead_ratio}% | "
                f"{issue.severity} | {issue.last_vacuum or 'Never'} |"
            )
        lines.append("")

        lines.extend(["## Recommended Actions", ""])
        for issue in issues:
            if issue.severity in ("critical", "high"):
                lines.append(f"```sql\n{issue.recommendation}\n```")
        lines.append("")

    if recommendations:
        lines.extend(["## Autovacuum Tuning", ""])
        for rec in recommendations:
            lines.append(f"```sql\n{rec}\n```")
            lines.append("")

    lines.extend([
        "## Current Autovacuum Settings",
        "",
        "| Setting | Value | Description |",
        "|---------|-------|-------------|",
    ])
    for name, info in settings.items():
        lines.append(f"| {name} | {info['value']} | {info['description'][:50]}... |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze vacuum needs")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--threshold", type=float, default=10.0, help="Dead ratio threshold (%)")
    parser.add_argument("--limit", type=int, default=20, help="Max tables to analyze")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    engine = create_engine(args.db_url)

    issues = get_table_bloat(engine, args.limit, args.threshold)
    settings = get_autovacuum_settings(engine)
    recommendations = generate_autovacuum_recommendations(issues, settings)

    if args.format == "json":
        output = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "issues": [vars(i) for i in issues],
            "settings": settings,
            "recommendations": recommendations
        }, indent=2, default=str)
    else:
        output = format_markdown(issues, settings, recommendations)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
