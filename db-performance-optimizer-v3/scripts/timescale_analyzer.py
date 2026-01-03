#!/usr/bin/env python3
"""
TimescaleDB Analyzer - Analyze hypertables, compression, and continuous aggregates.

Usage:
    python timescale_analyzer.py --db-url postgresql://user:pass@host/db
    python timescale_analyzer.py --db-url $DATABASE_URL --format json
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("Error: psycopg2 required. Install with: pip install psycopg2-binary")
    sys.exit(1)


def get_connection(db_url: str):
    """Create database connection."""
    return psycopg2.connect(db_url, cursor_factory=RealDictCursor)


def check_timescale_installed(conn) -> bool:
    """Check if TimescaleDB extension is installed."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS(
                SELECT 1 FROM pg_extension WHERE extname = 'timescaledb'
            ) as installed
        """)
        return cur.fetchone()["installed"]


def analyze_hypertables(conn) -> list:
    """Analyze all hypertables."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                h.hypertable_schema,
                h.hypertable_name,
                d.column_name as time_column,
                d.time_interval as chunk_interval,
                (SELECT COUNT(*) FROM timescaledb_information.chunks c
                 WHERE c.hypertable_name = h.hypertable_name) as chunk_count,
                h.compression_enabled,
                pg_size_pretty(hypertable_size(format('%I.%I',
                    h.hypertable_schema, h.hypertable_name)::regclass)) as total_size
            FROM timescaledb_information.hypertables h
            LEFT JOIN timescaledb_information.dimensions d
                ON h.hypertable_name = d.hypertable_name
                AND d.dimension_type = 'Time'
        """)
        return cur.fetchall()


def analyze_compression(conn) -> list:
    """Analyze compression status and opportunities."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                hypertable_name,
                chunk_name,
                is_compressed,
                pg_size_pretty(before_compression_total_bytes) as before_size,
                pg_size_pretty(after_compression_total_bytes) as after_size,
                CASE
                    WHEN before_compression_total_bytes > 0 THEN
                        ROUND(100 - (after_compression_total_bytes::numeric /
                              before_compression_total_bytes * 100), 2)
                    ELSE 0
                END as compression_ratio
            FROM timescaledb_information.compressed_chunk_stats
            WHERE is_compressed = true
            ORDER BY before_compression_total_bytes DESC
            LIMIT 20
        """)
        return cur.fetchall()


def analyze_continuous_aggregates(conn) -> list:
    """Analyze continuous aggregates."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                view_name,
                view_definition,
                materialized_only,
                compression_enabled,
                (SELECT pg_size_pretty(hypertable_size(materialization_hypertable::regclass)))
                    as materialization_size
            FROM timescaledb_information.continuous_aggregates
        """)
        return cur.fetchall()


def analyze_retention_policies(conn) -> list:
    """Analyze retention policies."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                j.hypertable_name,
                j.config->>'drop_after' as retention_period,
                j.schedule_interval,
                j.next_start
            FROM timescaledb_information.jobs j
            WHERE j.proc_name = 'policy_retention'
        """)
        return cur.fetchall()


def get_optimization_recommendations(hypertables, compression, aggregates) -> list:
    """Generate optimization recommendations."""
    recommendations = []

    for ht in hypertables:
        # Check compression
        if not ht.get("compression_enabled"):
            recommendations.append({
                "type": "compression",
                "priority": "P2",
                "table": ht["hypertable_name"],
                "recommendation": "Enable compression for storage savings",
                "sql": f"""ALTER TABLE {ht['hypertable_schema']}.{ht['hypertable_name']} SET (
    timescaledb.compress,
    timescaledb.compress_orderby = '{ht['time_column']} DESC'
);
SELECT add_compression_policy('{ht['hypertable_schema']}.{ht['hypertable_name']}', INTERVAL '7 days');"""
            })

        # Check chunk count (too many = performance issue)
        if ht.get("chunk_count", 0) > 1000:
            recommendations.append({
                "type": "chunk_interval",
                "priority": "P1",
                "table": ht["hypertable_name"],
                "recommendation": f"Too many chunks ({ht['chunk_count']}). Consider larger chunk interval.",
                "sql": f"SELECT set_chunk_time_interval('{ht['hypertable_name']}', INTERVAL '1 week');"
            })

    return recommendations


def format_output(data: dict, format_type: str) -> str:
    """Format output as JSON or Markdown."""
    if format_type == "json":
        return json.dumps(data, indent=2, default=str)

    # Markdown format
    md = ["# TimescaleDB Analysis Report\n"]
    md.append(f"**Generated:** {data['generated']}\n")

    if not data.get("timescale_installed"):
        md.append("\n## TimescaleDB Not Installed\n")
        md.append("TimescaleDB extension is not installed in this database.\n")
        md.append("Consider installing for time-series workloads.\n")
        return "\n".join(md)

    # Hypertables
    md.append("\n## Hypertables\n")
    md.append("| Table | Time Column | Chunk Interval | Chunks | Compression | Size |")
    md.append("|-------|-------------|----------------|--------|-------------|------|")
    for ht in data.get("hypertables", []):
        md.append(f"| {ht['hypertable_name']} | {ht['time_column']} | "
                  f"{ht['chunk_interval']} | {ht['chunk_count']} | "
                  f"{'Yes' if ht['compression_enabled'] else 'No'} | {ht['total_size']} |")

    # Compression Stats
    if data.get("compression"):
        md.append("\n## Compression Statistics\n")
        md.append("| Table | Chunk | Before | After | Ratio |")
        md.append("|-------|-------|--------|-------|-------|")
        for c in data["compression"][:10]:
            md.append(f"| {c['hypertable_name']} | {c['chunk_name']} | "
                      f"{c['before_size']} | {c['after_size']} | {c['compression_ratio']}% |")

    # Recommendations
    if data.get("recommendations"):
        md.append("\n## Recommendations\n")
        for rec in data["recommendations"]:
            md.append(f"\n### [{rec['priority']}] {rec['type'].title()}: {rec['table']}\n")
            md.append(f"{rec['recommendation']}\n")
            md.append(f"```sql\n{rec['sql']}\n```\n")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Analyze TimescaleDB configuration")
    parser.add_argument("--db-url", required=True, help="PostgreSQL connection URL")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    db_url = args.db_url if args.db_url != "$DATABASE_URL" else os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: Database URL required")
        sys.exit(1)

    conn = get_connection(db_url)

    result = {
        "generated": datetime.now().isoformat(),
        "timescale_installed": check_timescale_installed(conn)
    }

    if result["timescale_installed"]:
        result["hypertables"] = [dict(h) for h in analyze_hypertables(conn)]
        result["compression"] = [dict(c) for c in analyze_compression(conn)]
        result["continuous_aggregates"] = [dict(a) for a in analyze_continuous_aggregates(conn)]
        result["retention_policies"] = [dict(r) for r in analyze_retention_policies(conn)]
        result["recommendations"] = get_optimization_recommendations(
            result["hypertables"],
            result["compression"],
            result["continuous_aggregates"]
        )

    print(format_output(result, args.format))
    conn.close()


if __name__ == "__main__":
    main()
