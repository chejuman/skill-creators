#!/usr/bin/env python3
"""
Query Profiler for SQLAlchemy Applications
Profiles and analyzes database queries for performance optimization.

Usage:
    python3 query_profiler.py --db-url postgresql://user:pass@host/db
    python3 query_profiler.py --db-url postgresql://... --top 20
    python3 query_profiler.py --db-url postgresql://... --format json
"""

import argparse
import json
from datetime import datetime
from typing import Optional

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import Session
except ImportError:
    print("Error: SQLAlchemy not installed. Run: pip install sqlalchemy psycopg2-binary")
    exit(1)


# Queries for pg_stat_statements analysis
SLOW_QUERIES_SQL = """
SELECT
    queryid,
    round(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    round(mean_exec_time::numeric, 2) as mean_time_ms,
    round(max_exec_time::numeric, 2) as max_time_ms,
    round((100 * total_exec_time / sum(total_exec_time) over ())::numeric, 2) as percent_total,
    rows,
    round((rows::numeric / NULLIF(calls, 0))::numeric, 2) as avg_rows,
    query
FROM pg_stat_statements
WHERE userid = (SELECT usesysid FROM pg_user WHERE usename = current_user)
ORDER BY total_exec_time DESC
LIMIT :limit;
"""

INDEX_USAGE_SQL = """
SELECT
    schemaname,
    relname as table_name,
    indexrelname as index_name,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC
LIMIT :limit;
"""

TABLE_STATS_SQL = """
SELECT
    schemaname,
    relname as table_name,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    round(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_ratio
FROM pg_stat_user_tables
ORDER BY seq_scan DESC
LIMIT :limit;
"""

MISSING_INDEXES_SQL = """
SELECT
    schemaname,
    relname as table_name,
    seq_scan,
    seq_tup_read,
    idx_scan,
    CASE WHEN seq_scan > 0
        THEN round((seq_tup_read::numeric / seq_scan)::numeric, 2)
        ELSE 0
    END as avg_seq_tup_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100
  AND idx_scan < seq_scan
  AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC
LIMIT :limit;
"""

CACHE_HIT_RATIO_SQL = """
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit)  as heap_hit,
    round(sum(heap_blks_hit)::numeric / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0) * 100, 2) as cache_hit_ratio
FROM pg_statio_user_tables;
"""

CONNECTION_STATS_SQL = """
SELECT
    count(*) as total_connections,
    count(*) FILTER (WHERE state = 'active') as active,
    count(*) FILTER (WHERE state = 'idle') as idle,
    count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction,
    count(*) FILTER (WHERE wait_event_type IS NOT NULL) as waiting
FROM pg_stat_activity
WHERE datname = current_database();
"""


def get_slow_queries(engine, limit: int = 10) -> list:
    """Get slowest queries from pg_stat_statements."""
    try:
        with Session(engine) as session:
            result = session.execute(text(SLOW_QUERIES_SQL), {"limit": limit})
            return [dict(row._mapping) for row in result]
    except Exception as e:
        print(f"Warning: pg_stat_statements not available: {e}")
        return []


def get_index_usage(engine, limit: int = 20) -> list:
    """Get index usage statistics."""
    with Session(engine) as session:
        result = session.execute(text(INDEX_USAGE_SQL), {"limit": limit})
        return [dict(row._mapping) for row in result]


def get_table_stats(engine, limit: int = 20) -> list:
    """Get table access statistics."""
    with Session(engine) as session:
        result = session.execute(text(TABLE_STATS_SQL), {"limit": limit})
        return [dict(row._mapping) for row in result]


def get_missing_indexes(engine, limit: int = 10) -> list:
    """Identify tables that might need indexes."""
    with Session(engine) as session:
        result = session.execute(text(MISSING_INDEXES_SQL), {"limit": limit})
        return [dict(row._mapping) for row in result]


def get_cache_hit_ratio(engine) -> dict:
    """Get buffer cache hit ratio."""
    with Session(engine) as session:
        result = session.execute(text(CACHE_HIT_RATIO_SQL))
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return {}


def get_connection_stats(engine) -> dict:
    """Get connection statistics."""
    with Session(engine) as session:
        result = session.execute(text(CONNECTION_STATS_SQL))
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return {}


def generate_report(engine, limit: int = 10) -> dict:
    """Generate comprehensive performance report."""
    return {
        "timestamp": datetime.now().isoformat(),
        "slow_queries": get_slow_queries(engine, limit),
        "index_usage": get_index_usage(engine, limit * 2),
        "table_stats": get_table_stats(engine, limit * 2),
        "missing_indexes": get_missing_indexes(engine, limit),
        "cache_hit_ratio": get_cache_hit_ratio(engine),
        "connection_stats": get_connection_stats(engine),
    }


def format_markdown(report: dict) -> str:
    """Format report as markdown."""
    lines = [
        "# Database Performance Report",
        f"**Generated:** {report['timestamp']}",
        "",
        "## Cache Hit Ratio",
        "",
    ]

    cache = report.get("cache_hit_ratio", {})
    if cache:
        ratio = cache.get("cache_hit_ratio", 0)
        status = "Good" if ratio and ratio > 95 else "Needs attention"
        lines.append(f"- **Ratio:** {ratio}% ({status})")
        lines.append(f"- **Heap Read:** {cache.get('heap_read', 0):,}")
        lines.append(f"- **Heap Hit:** {cache.get('heap_hit', 0):,}")
    else:
        lines.append("- No data available")

    lines.extend(["", "## Connection Stats", ""])
    conn = report.get("connection_stats", {})
    if conn:
        lines.append(f"- **Total:** {conn.get('total_connections', 0)}")
        lines.append(f"- **Active:** {conn.get('active', 0)}")
        lines.append(f"- **Idle:** {conn.get('idle', 0)}")
        lines.append(f"- **Idle in Transaction:** {conn.get('idle_in_transaction', 0)}")

    lines.extend(["", "## Slow Queries (Top 10)", ""])
    slow = report.get("slow_queries", [])
    if slow:
        lines.append("| Total Time (ms) | Calls | Mean (ms) | % Total | Query |")
        lines.append("|-----------------|-------|-----------|---------|-------|")
        for q in slow[:10]:
            query = q.get("query", "")[:50].replace("\n", " ")
            lines.append(
                f"| {q.get('total_time_ms', 0):,.2f} | "
                f"{q.get('calls', 0):,} | "
                f"{q.get('mean_time_ms', 0):.2f} | "
                f"{q.get('percent_total', 0):.1f}% | "
                f"`{query}...` |"
            )
    else:
        lines.append("No slow query data (enable pg_stat_statements)")

    lines.extend(["", "## Tables Needing Indexes", ""])
    missing = report.get("missing_indexes", [])
    if missing:
        lines.append("| Table | Seq Scans | Seq Tuples Read | Index Scans | Recommendation |")
        lines.append("|-------|-----------|-----------------|-------------|----------------|")
        for t in missing:
            lines.append(
                f"| {t.get('table_name', '')} | "
                f"{t.get('seq_scan', 0):,} | "
                f"{t.get('seq_tup_read', 0):,} | "
                f"{t.get('idx_scan', 0):,} | "
                f"Add index |"
            )
    else:
        lines.append("No obvious missing indexes detected")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Profile database performance")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--top", type=int, default=10, help="Number of top items")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    engine = create_engine(args.db_url)
    report = generate_report(engine, args.top)

    if args.format == "json":
        output = json.dumps(report, indent=2, default=str)
    else:
        output = format_markdown(report)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
