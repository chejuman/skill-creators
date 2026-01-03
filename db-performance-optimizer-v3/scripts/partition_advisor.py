#!/usr/bin/env python3
"""
Partition Advisor for PostgreSQL
Analyzes tables and recommends partitioning strategies.

Usage:
    python3 partition_advisor.py --db-url postgresql://user:pass@host/db
    python3 partition_advisor.py --db-url postgresql://... --min-size 1GB
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
class PartitionCandidate:
    """Table recommended for partitioning."""
    table: str
    row_count: int
    table_size: str
    size_bytes: int
    partition_key: Optional[str]
    partition_type: str
    reason: str
    create_statement: str
    priority: int


# SQL queries
LARGE_TABLES_SQL = """
SELECT
    schemaname,
    relname as table_name,
    n_live_tup as row_count,
    pg_size_pretty(pg_total_relation_size(relid)) as table_size,
    pg_total_relation_size(relid) as size_bytes
FROM pg_stat_user_tables
WHERE pg_total_relation_size(relid) > :min_size
ORDER BY pg_total_relation_size(relid) DESC
LIMIT :limit;
"""

TABLE_COLUMNS_SQL = """
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = :table_name
ORDER BY ordinal_position;
"""

TIME_COLUMN_PATTERNS = [
    "created_at", "created", "timestamp", "date", "time",
    "inserted_at", "updated_at", "event_time", "log_time"
]

ID_COLUMN_PATTERNS = [
    "id", "user_id", "account_id", "tenant_id", "customer_id"
]


def parse_size(size_str: str) -> int:
    """Parse size string like '1GB' to bytes."""
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    match = re.match(r"(\d+(?:\.\d+)?)\s*([A-Z]+)", size_str.upper())
    if match:
        value, unit = match.groups()
        return int(float(value) * units.get(unit, 1))
    return int(size_str)


def get_large_tables(engine, min_size: int, limit: int = 20) -> list[dict]:
    """Get tables larger than min_size."""
    with Session(engine) as session:
        result = session.execute(text(LARGE_TABLES_SQL), {
            "min_size": min_size,
            "limit": limit
        })
        return [dict(row._mapping) for row in result]


def get_table_columns(engine, table_name: str) -> list[dict]:
    """Get columns for a table."""
    with Session(engine) as session:
        result = session.execute(text(TABLE_COLUMNS_SQL), {"table_name": table_name})
        return [dict(row._mapping) for row in result]


def suggest_partition_key(columns: list[dict]) -> tuple[Optional[str], str]:
    """Suggest best partition key and type."""
    # Look for time-based columns (best for RANGE partitioning)
    for col in columns:
        col_name = col["column_name"].lower()
        col_type = col["data_type"].lower()

        if any(pattern in col_name for pattern in TIME_COLUMN_PATTERNS):
            if "timestamp" in col_type or "date" in col_type:
                return col["column_name"], "RANGE"

    # Look for ID columns (good for HASH partitioning)
    for col in columns:
        col_name = col["column_name"].lower()
        col_type = col["data_type"].lower()

        if any(pattern in col_name for pattern in ID_COLUMN_PATTERNS):
            if "int" in col_type or "uuid" in col_type:
                return col["column_name"], "HASH"

    # Look for status/type columns (good for LIST partitioning)
    for col in columns:
        col_name = col["column_name"].lower()
        if any(x in col_name for x in ["status", "type", "category", "region"]):
            return col["column_name"], "LIST"

    return None, "RANGE"


def generate_partition_sql(table: str, key: str, partition_type: str) -> str:
    """Generate CREATE TABLE statement for partitioned table."""
    if partition_type == "RANGE":
        return f"""-- Partition by RANGE on {key}
-- Step 1: Create new partitioned table
CREATE TABLE {table}_partitioned (
    LIKE {table} INCLUDING ALL
) PARTITION BY RANGE ({key});

-- Step 2: Create partitions (example: monthly)
CREATE TABLE {table}_y2024m01 PARTITION OF {table}_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE {table}_y2024m02 PARTITION OF {table}_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
-- Add more partitions as needed...

-- Step 3: Migrate data
INSERT INTO {table}_partitioned SELECT * FROM {table};

-- Step 4: Swap tables
ALTER TABLE {table} RENAME TO {table}_old;
ALTER TABLE {table}_partitioned RENAME TO {table};

-- Step 5: (Optional) Drop old table after verification
-- DROP TABLE {table}_old;"""

    elif partition_type == "HASH":
        return f"""-- Partition by HASH on {key}
CREATE TABLE {table}_partitioned (
    LIKE {table} INCLUDING ALL
) PARTITION BY HASH ({key});

-- Create hash partitions (4 partitions)
CREATE TABLE {table}_p0 PARTITION OF {table}_partitioned
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE {table}_p1 PARTITION OF {table}_partitioned
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE {table}_p2 PARTITION OF {table}_partitioned
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE {table}_p3 PARTITION OF {table}_partitioned
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- Migrate and swap (same as RANGE)"""

    else:  # LIST
        return f"""-- Partition by LIST on {key}
CREATE TABLE {table}_partitioned (
    LIKE {table} INCLUDING ALL
) PARTITION BY LIST ({key});

-- Create list partitions (customize based on your values)
CREATE TABLE {table}_active PARTITION OF {table}_partitioned
    FOR VALUES IN ('active', 'pending');
CREATE TABLE {table}_inactive PARTITION OF {table}_partitioned
    FOR VALUES IN ('inactive', 'deleted');
CREATE TABLE {table}_default PARTITION OF {table}_partitioned
    DEFAULT;

-- Migrate and swap (same as RANGE)"""


def analyze_tables(engine, min_size: int, limit: int) -> list[PartitionCandidate]:
    """Analyze tables and generate partition recommendations."""
    candidates = []
    large_tables = get_large_tables(engine, min_size, limit)

    for table in large_tables:
        table_name = table["table_name"]
        columns = get_table_columns(engine, table_name)

        partition_key, partition_type = suggest_partition_key(columns)

        if partition_key:
            reason = f"Table size {table['table_size']} with {table['row_count']:,} rows"
            priority = 1 if table["size_bytes"] > 10 * 1024**3 else 2  # > 10GB = P1

            candidates.append(PartitionCandidate(
                table=table_name,
                row_count=table["row_count"],
                table_size=table["table_size"],
                size_bytes=table["size_bytes"],
                partition_key=partition_key,
                partition_type=partition_type,
                reason=reason,
                create_statement=generate_partition_sql(table_name, partition_key, partition_type),
                priority=priority
            ))

    return sorted(candidates, key=lambda x: x.priority)


def format_markdown(candidates: list[PartitionCandidate]) -> str:
    """Format as markdown report."""
    lines = [
        "# Partition Advisor Report",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Tables analyzed: {len(candidates)}",
        f"- Priority 1 (> 10GB): {len([c for c in candidates if c.priority == 1])}",
        "",
    ]

    if candidates:
        lines.extend([
            "## Partition Candidates",
            "",
            "| Table | Size | Rows | Partition Type | Key |",
            "|-------|------|------|----------------|-----|",
        ])
        for c in candidates:
            lines.append(
                f"| {c.table} | {c.table_size} | {c.row_count:,} | "
                f"{c.partition_type} | {c.partition_key} |"
            )
        lines.append("")

        lines.extend(["## Implementation Scripts", ""])
        for c in candidates:
            lines.append(f"### {c.table}")
            lines.append(f"**Priority:** P{c.priority} | **Type:** {c.partition_type}")
            lines.append(f"```sql\n{c.create_statement}\n```")
            lines.append("")
    else:
        lines.append("No tables require partitioning at current thresholds.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze partition opportunities")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--min-size", default="1GB", help="Minimum table size (e.g., 1GB)")
    parser.add_argument("--limit", type=int, default=20, help="Max tables to analyze")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    engine = create_engine(args.db_url)
    min_size = parse_size(args.min_size)

    candidates = analyze_tables(engine, min_size, args.limit)

    if args.format == "json":
        output = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "candidates": [vars(c) for c in candidates]
        }, indent=2, default=str)
    else:
        output = format_markdown(candidates)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
