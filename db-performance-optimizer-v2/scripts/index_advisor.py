#!/usr/bin/env python3
"""
Index Advisor for PostgreSQL/SQLAlchemy Applications
Analyzes query patterns and recommends optimal indexes.

Usage:
    python3 index_advisor.py --db-url postgresql://user:pass@host/db
    python3 index_advisor.py --db-url postgresql://... --analyze-queries
    python3 index_advisor.py --db-url postgresql://... --output report.md
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
class IndexRecommendation:
    """Index recommendation with rationale."""
    table: str
    columns: list[str]
    index_type: str
    reason: str
    impact: str
    create_statement: str
    priority: int  # 1=highest


# SQL to analyze missing indexes
MISSING_INDEX_SQL = """
WITH table_scans AS (
    SELECT
        schemaname,
        relname as table_name,
        seq_scan,
        seq_tup_read,
        idx_scan,
        CASE WHEN (seq_scan + idx_scan) > 0
            THEN round(100.0 * idx_scan / (seq_scan + idx_scan), 2)
            ELSE 0
        END as idx_usage_percent
    FROM pg_stat_user_tables
    WHERE seq_scan > 0
)
SELECT * FROM table_scans
WHERE idx_usage_percent < 90
  AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC
LIMIT :limit;
"""

# SQL to find unused indexes
UNUSED_INDEX_SQL = """
SELECT
    schemaname,
    relname as table_name,
    indexrelname as index_name,
    idx_scan as scans,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE 'pg_%'
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT :limit;
"""

# SQL to find duplicate indexes
DUPLICATE_INDEX_SQL = """
SELECT
    indrelid::regclass as table_name,
    array_agg(indexrelid::regclass) as indexes,
    array_agg(pg_get_indexdef(indexrelid)) as definitions
FROM pg_index
GROUP BY indrelid, indkey
HAVING count(*) > 1
LIMIT :limit;
"""

# SQL to analyze slow queries and suggest indexes
SLOW_QUERY_PATTERNS_SQL = """
SELECT
    queryid,
    calls,
    round(mean_exec_time::numeric, 2) as mean_ms,
    round(total_exec_time::numeric, 2) as total_ms,
    query
FROM pg_stat_statements
WHERE calls > 10
  AND mean_exec_time > 100
ORDER BY total_exec_time DESC
LIMIT :limit;
"""

# SQL to get current indexes
CURRENT_INDEXES_SQL = """
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
"""


def get_tables_needing_indexes(engine, limit: int = 20) -> list[dict]:
    """Find tables with poor index usage."""
    with Session(engine) as session:
        result = session.execute(text(MISSING_INDEX_SQL), {"limit": limit})
        return [dict(row._mapping) for row in result]


def get_unused_indexes(engine, limit: int = 20) -> list[dict]:
    """Find indexes that are never used."""
    with Session(engine) as session:
        result = session.execute(text(UNUSED_INDEX_SQL), {"limit": limit})
        return [dict(row._mapping) for row in result]


def get_duplicate_indexes(engine, limit: int = 10) -> list[dict]:
    """Find duplicate/redundant indexes."""
    try:
        with Session(engine) as session:
            result = session.execute(text(DUPLICATE_INDEX_SQL), {"limit": limit})
            return [dict(row._mapping) for row in result]
    except Exception:
        return []


def get_slow_query_patterns(engine, limit: int = 20) -> list[dict]:
    """Get slow queries for analysis."""
    try:
        with Session(engine) as session:
            result = session.execute(text(SLOW_QUERY_PATTERNS_SQL), {"limit": limit})
            return [dict(row._mapping) for row in result]
    except Exception:
        return []


def analyze_query_for_indexes(query: str) -> list[IndexRecommendation]:
    """Analyze a query and suggest indexes based on patterns."""
    recommendations = []
    query_lower = query.lower()

    # Extract table names (basic heuristic)
    import re

    # Find WHERE clause columns
    where_match = re.search(r'where\s+(.+?)(?:order|group|limit|$)', query_lower, re.DOTALL)
    if where_match:
        where_clause = where_match.group(1)

        # Find column = value patterns
        eq_matches = re.findall(r'(\w+)\s*=', where_clause)

        # Find LIKE patterns
        like_matches = re.findall(r'(\w+)\s+(?:i?like)', where_clause)

        # Find range patterns (>, <, >=, <=, BETWEEN)
        range_matches = re.findall(r'(\w+)\s*(?:[<>]=?|between)', where_clause)

        # Combine for index recommendation
        if eq_matches:
            recommendations.append(IndexRecommendation(
                table="(from query)",
                columns=eq_matches[:3],  # Limit to 3 columns
                index_type="btree",
                reason=f"Equality conditions on: {', '.join(eq_matches[:3])}",
                impact="High - equality lookups benefit most from indexes",
                create_statement=f"CREATE INDEX idx_{{table}}_{'_'.join(eq_matches[:3])} ON {{table}} ({', '.join(eq_matches[:3])});",
                priority=1
            ))

        if like_matches:
            for col in like_matches[:2]:
                recommendations.append(IndexRecommendation(
                    table="(from query)",
                    columns=[col],
                    index_type="gin_trgm",
                    reason=f"LIKE/ILIKE pattern on: {col}",
                    impact="High - trigram index for pattern matching",
                    create_statement=f"CREATE INDEX idx_{{table}}_{col}_trgm ON {{table}} USING gin ({col} gin_trgm_ops);",
                    priority=2
                ))

    # Find ORDER BY columns
    order_match = re.search(r'order\s+by\s+(\w+)', query_lower)
    if order_match:
        col = order_match.group(1)
        recommendations.append(IndexRecommendation(
            table="(from query)",
            columns=[col],
            index_type="btree",
            reason=f"ORDER BY on: {col}",
            impact="Medium - speeds up sorting",
            create_statement=f"CREATE INDEX idx_{{table}}_{col}_sort ON {{table}} ({col});",
            priority=3
        ))

    return recommendations


def generate_recommendations(engine, limit: int = 20) -> dict:
    """Generate comprehensive index recommendations."""
    tables_needing = get_tables_needing_indexes(engine, limit)
    unused = get_unused_indexes(engine, limit)
    duplicates = get_duplicate_indexes(engine, limit)
    slow_queries = get_slow_query_patterns(engine, limit)

    # Analyze slow queries for index opportunities
    query_recommendations = []
    for sq in slow_queries:
        recs = analyze_query_for_indexes(sq.get("query", ""))
        for rec in recs:
            rec.reason += f" (query called {sq.get('calls', 0)} times, avg {sq.get('mean_ms', 0)}ms)"
            query_recommendations.append(rec)

    return {
        "timestamp": datetime.now().isoformat(),
        "tables_needing_indexes": tables_needing,
        "unused_indexes": unused,
        "duplicate_indexes": duplicates,
        "slow_queries": slow_queries,
        "recommendations": [vars(r) for r in query_recommendations],
    }


def format_markdown(data: dict) -> str:
    """Format recommendations as markdown."""
    lines = [
        "# Index Advisor Report",
        f"**Generated:** {data['timestamp']}",
        "",
        "## Summary",
        "",
        f"- Tables needing indexes: {len(data['tables_needing_indexes'])}",
        f"- Unused indexes (consider dropping): {len(data['unused_indexes'])}",
        f"- Duplicate indexes: {len(data['duplicate_indexes'])}",
        f"- Slow queries analyzed: {len(data['slow_queries'])}",
        f"- Recommendations generated: {len(data['recommendations'])}",
        "",
    ]

    # Tables needing indexes
    if data["tables_needing_indexes"]:
        lines.extend([
            "## Tables with Poor Index Usage",
            "",
            "| Table | Seq Scans | Seq Tuples | Index Usage % |",
            "|-------|-----------|------------|---------------|",
        ])
        for t in data["tables_needing_indexes"]:
            lines.append(
                f"| {t['table_name']} | {t['seq_scan']:,} | "
                f"{t['seq_tup_read']:,} | {t['idx_usage_percent']}% |"
            )
        lines.append("")

    # Unused indexes
    if data["unused_indexes"]:
        lines.extend([
            "## Unused Indexes (Consider Dropping)",
            "",
            "| Table | Index | Size |",
            "|-------|-------|------|",
        ])
        for idx in data["unused_indexes"]:
            lines.append(f"| {idx['table_name']} | {idx['index_name']} | {idx['size']} |")
        lines.append("")
        lines.append("```sql")
        for idx in data["unused_indexes"]:
            lines.append(f"DROP INDEX IF EXISTS {idx['index_name']};")
        lines.append("```")
        lines.append("")

    # Recommendations from slow queries
    if data["recommendations"]:
        lines.extend([
            "## Recommended Indexes",
            "",
        ])
        for i, rec in enumerate(data["recommendations"][:10], 1):
            lines.append(f"### {i}. {rec['index_type'].upper()} Index")
            lines.append(f"- **Columns:** {', '.join(rec['columns'])}")
            lines.append(f"- **Reason:** {rec['reason']}")
            lines.append(f"- **Impact:** {rec['impact']}")
            lines.append(f"- **Priority:** {rec['priority']}")
            lines.append("```sql")
            lines.append(rec['create_statement'])
            lines.append("```")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze and recommend indexes")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--limit", type=int, default=20, help="Max items per category")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    engine = create_engine(args.db_url)
    data = generate_recommendations(engine, args.limit)

    if args.format == "json":
        output = json.dumps(data, indent=2, default=str)
    else:
        output = format_markdown(data)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
