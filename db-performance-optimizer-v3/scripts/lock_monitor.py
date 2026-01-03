#!/usr/bin/env python3
"""
Lock Monitor for PostgreSQL
Monitors lock contention, blocking queries, and deadlock patterns.

Usage:
    python3 lock_monitor.py --db-url postgresql://user:pass@host/db
    python3 lock_monitor.py --db-url postgresql://... --watch
"""

import argparse
import json
import time
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
class LockInfo:
    """Lock information."""
    blocked_pid: int
    blocked_query: str
    blocking_pid: int
    blocking_query: str
    lock_type: str
    blocked_duration: str
    table_name: Optional[str]


@dataclass
class LongTransaction:
    """Long-running transaction."""
    pid: int
    duration: str
    state: str
    query: str
    wait_event: Optional[str]


# SQL queries
BLOCKING_QUERIES_SQL = """
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query,
    blocked.locktype AS lock_type,
    age(now(), blocked.query_start) AS blocked_duration,
    blocked.relation::regclass AS table_name
FROM pg_locks blocked
JOIN pg_stat_activity blocked_act ON blocked.pid = blocked_act.pid
JOIN pg_locks blocking ON blocked.locktype = blocking.locktype
    AND blocked.relation = blocking.relation
    AND blocked.pid != blocking.pid
JOIN pg_stat_activity blocking_act ON blocking.pid = blocking_act.pid
WHERE NOT blocked.granted
ORDER BY blocked_duration DESC
LIMIT :limit;
"""

LONG_TRANSACTIONS_SQL = """
SELECT
    pid,
    age(now(), xact_start) AS duration,
    state,
    query,
    wait_event_type || ': ' || wait_event AS wait_event
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
  AND state != 'idle'
  AND pid != pg_backend_pid()
  AND age(now(), xact_start) > interval ':threshold seconds'
ORDER BY xact_start
LIMIT :limit;
"""

LOCK_STATISTICS_SQL = """
SELECT
    locktype,
    mode,
    count(*) as lock_count,
    count(*) FILTER (WHERE granted) as granted,
    count(*) FILTER (WHERE NOT granted) as waiting
FROM pg_locks
GROUP BY locktype, mode
HAVING count(*) FILTER (WHERE NOT granted) > 0
ORDER BY waiting DESC;
"""

DEADLOCK_LOG_SQL = """
SELECT
    log_time,
    message,
    detail
FROM pg_catalog.pg_read_file('log/postgresql.log') AS log
WHERE log LIKE '%deadlock detected%'
LIMIT 10;
"""

TABLE_LOCK_SQL = """
SELECT
    c.relname as table_name,
    l.mode as lock_mode,
    count(*) as lock_count,
    count(*) FILTER (WHERE l.granted) as granted,
    count(*) FILTER (WHERE NOT l.granted) as waiting
FROM pg_locks l
JOIN pg_class c ON l.relation = c.oid
WHERE c.relkind = 'r'
GROUP BY c.relname, l.mode
HAVING count(*) > 1
ORDER BY waiting DESC, lock_count DESC
LIMIT :limit;
"""


def get_blocking_queries(engine, limit: int = 20) -> list[LockInfo]:
    """Get currently blocking queries."""
    locks = []
    with Session(engine) as session:
        try:
            result = session.execute(text(BLOCKING_QUERIES_SQL), {"limit": limit})
            for row in result:
                r = dict(row._mapping)
                locks.append(LockInfo(
                    blocked_pid=r["blocked_pid"],
                    blocked_query=r["blocked_query"][:200] if r["blocked_query"] else "",
                    blocking_pid=r["blocking_pid"],
                    blocking_query=r["blocking_query"][:200] if r["blocking_query"] else "",
                    lock_type=r["lock_type"],
                    blocked_duration=str(r["blocked_duration"]),
                    table_name=str(r["table_name"]) if r["table_name"] else None
                ))
        except Exception:
            pass
    return locks


def get_long_transactions(engine, threshold: int = 60, limit: int = 20) -> list[LongTransaction]:
    """Get long-running transactions."""
    transactions = []
    with Session(engine) as session:
        # Use parameterized query properly
        sql = f"""
        SELECT
            pid,
            age(now(), xact_start) AS duration,
            state,
            query,
            wait_event_type || ': ' || wait_event AS wait_event
        FROM pg_stat_activity
        WHERE xact_start IS NOT NULL
          AND state != 'idle'
          AND pid != pg_backend_pid()
          AND age(now(), xact_start) > interval '{threshold} seconds'
        ORDER BY xact_start
        LIMIT {limit};
        """
        try:
            result = session.execute(text(sql))
            for row in result:
                r = dict(row._mapping)
                transactions.append(LongTransaction(
                    pid=r["pid"],
                    duration=str(r["duration"]),
                    state=r["state"],
                    query=r["query"][:200] if r["query"] else "",
                    wait_event=r["wait_event"]
                ))
        except Exception:
            pass
    return transactions


def get_lock_statistics(engine) -> list[dict]:
    """Get lock statistics."""
    with Session(engine) as session:
        try:
            result = session.execute(text(LOCK_STATISTICS_SQL))
            return [dict(row._mapping) for row in result]
        except Exception:
            return []


def get_table_locks(engine, limit: int = 20) -> list[dict]:
    """Get per-table lock information."""
    with Session(engine) as session:
        try:
            result = session.execute(text(TABLE_LOCK_SQL), {"limit": limit})
            return [dict(row._mapping) for row in result]
        except Exception:
            return []


def generate_recommendations(locks: list[LockInfo], transactions: list[LongTransaction]) -> list[str]:
    """Generate recommendations based on lock analysis."""
    recommendations = []

    if locks:
        recommendations.append(
            "-- Kill blocking query (use with caution):\n"
            f"SELECT pg_terminate_backend({locks[0].blocking_pid});"
        )

        if len(locks) > 5:
            recommendations.append(
                "-- Multiple blocking queries detected. Consider:\n"
                "-- 1. Review transaction isolation levels\n"
                "-- 2. Add indexes to reduce lock duration\n"
                "-- 3. Use SELECT ... FOR UPDATE NOWAIT or SKIP LOCKED"
            )

    if transactions:
        long_pids = [t.pid for t in transactions if "hour" in t.duration]
        if long_pids:
            recommendations.append(
                "-- Terminate very long transactions:\n" +
                "\n".join([f"SELECT pg_terminate_backend({pid});" for pid in long_pids[:3]])
            )

    recommendations.append(
        "-- Prevent deadlocks:\n"
        "-- 1. Always access tables in consistent order\n"
        "-- 2. Keep transactions short\n"
        "-- 3. Use statement_timeout for protection\n"
        "SET statement_timeout = '30s';"
    )

    return recommendations


def format_markdown(locks: list[LockInfo], transactions: list[LongTransaction],
                   stats: list[dict], table_locks: list[dict],
                   recommendations: list[str]) -> str:
    """Format as markdown report."""
    lines = [
        "# Lock Monitor Report",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Blocking queries: {len(locks)}",
        f"- Long transactions: {len(transactions)}",
        f"- Lock types with waiting: {len(stats)}",
        "",
    ]

    if locks:
        lines.extend([
            "## Blocking Queries",
            "",
            "| Blocked PID | Blocking PID | Lock Type | Duration | Table |",
            "|-------------|--------------|-----------|----------|-------|",
        ])
        for lock in locks:
            lines.append(
                f"| {lock.blocked_pid} | {lock.blocking_pid} | "
                f"{lock.lock_type} | {lock.blocked_duration} | {lock.table_name or 'N/A'} |"
            )
        lines.append("")

    if transactions:
        lines.extend([
            "## Long-Running Transactions",
            "",
            "| PID | Duration | State | Wait Event |",
            "|-----|----------|-------|------------|",
        ])
        for txn in transactions:
            lines.append(
                f"| {txn.pid} | {txn.duration} | {txn.state} | {txn.wait_event or 'None'} |"
            )
        lines.append("")

    if table_locks:
        lines.extend([
            "## Per-Table Lock Contention",
            "",
            "| Table | Lock Mode | Total | Granted | Waiting |",
            "|-------|-----------|-------|---------|---------|",
        ])
        for tl in table_locks:
            lines.append(
                f"| {tl['table_name']} | {tl['lock_mode']} | "
                f"{tl['lock_count']} | {tl['granted']} | {tl['waiting']} |"
            )
        lines.append("")

    if recommendations:
        lines.extend(["## Recommendations", ""])
        for rec in recommendations:
            lines.append(f"```sql\n{rec}\n```")
            lines.append("")

    return "\n".join(lines)


def watch_mode(engine, interval: int = 5):
    """Continuous monitoring mode."""
    print(f"Watching locks every {interval}s. Press Ctrl+C to stop.")
    try:
        while True:
            locks = get_blocking_queries(engine, 5)
            print(f"\n[{datetime.now().isoformat()}] Blocking: {len(locks)}")
            for lock in locks:
                print(f"  PID {lock.blocking_pid} -> {lock.blocked_pid} ({lock.lock_type})")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="Monitor lock contention")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--threshold", type=int, default=60, help="Long transaction threshold (seconds)")
    parser.add_argument("--limit", type=int, default=20, help="Max items per category")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--watch", action="store_true", help="Continuous monitoring mode")
    parser.add_argument("--interval", type=int, default=5, help="Watch interval (seconds)")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    engine = create_engine(args.db_url)

    if args.watch:
        watch_mode(engine, args.interval)
        return

    locks = get_blocking_queries(engine, args.limit)
    transactions = get_long_transactions(engine, args.threshold, args.limit)
    stats = get_lock_statistics(engine)
    table_locks = get_table_locks(engine, args.limit)
    recommendations = generate_recommendations(locks, transactions)

    if args.format == "json":
        output = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "blocking_queries": [vars(l) for l in locks],
            "long_transactions": [vars(t) for t in transactions],
            "lock_statistics": stats,
            "table_locks": table_locks,
            "recommendations": recommendations
        }, indent=2, default=str)
    else:
        output = format_markdown(locks, transactions, stats, table_locks, recommendations)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
