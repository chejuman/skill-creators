#!/usr/bin/env python3
"""
Connection Pool Analyzer for PostgreSQL/SQLAlchemy
Analyzes connection usage patterns and recommends pool settings.

Usage:
    python3 connection_analyzer.py --db-url postgresql://user:pass@host/db
    python3 connection_analyzer.py --db-url postgresql://... --watch
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
class ConnectionStats:
    """Connection statistics."""
    total_connections: int
    active: int
    idle: int
    idle_in_transaction: int
    waiting: int
    max_connections: int
    reserved_connections: int
    usage_percent: float


@dataclass
class PoolRecommendation:
    """Pool configuration recommendation."""
    setting: str
    current_value: str
    recommended_value: str
    reason: str
    implementation: str


# SQL queries
CONNECTION_STATS_SQL = """
SELECT
    count(*) as total_connections,
    count(*) FILTER (WHERE state = 'active') as active,
    count(*) FILTER (WHERE state = 'idle') as idle,
    count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction,
    count(*) FILTER (WHERE state = 'idle in transaction (aborted)') as idle_in_transaction_aborted,
    count(*) FILTER (WHERE wait_event_type = 'Client') as waiting_for_client,
    count(*) FILTER (WHERE wait_event_type IS NOT NULL AND wait_event_type != 'Client') as waiting
FROM pg_stat_activity
WHERE datname = current_database();
"""

MAX_CONNECTIONS_SQL = """
SELECT
    setting::int as max_connections
FROM pg_settings
WHERE name = 'max_connections';
"""

SUPERUSER_RESERVED_SQL = """
SELECT
    setting::int as superuser_reserved_connections
FROM pg_settings
WHERE name = 'superuser_reserved_connections';
"""

CONNECTION_WAIT_SQL = """
SELECT
    client_addr,
    usename,
    state,
    age(now(), state_change) as state_duration,
    age(now(), query_start) as query_duration,
    wait_event_type,
    wait_event,
    query
FROM pg_stat_activity
WHERE datname = current_database()
  AND pid != pg_backend_pid()
ORDER BY state_change
LIMIT :limit;
"""

CLIENT_CONNECTIONS_SQL = """
SELECT
    client_addr,
    usename,
    count(*) as connection_count,
    count(*) FILTER (WHERE state = 'active') as active,
    count(*) FILTER (WHERE state = 'idle') as idle
FROM pg_stat_activity
WHERE datname = current_database()
GROUP BY client_addr, usename
ORDER BY connection_count DESC
LIMIT :limit;
"""


def get_connection_stats(engine) -> ConnectionStats:
    """Get current connection statistics."""
    with Session(engine) as session:
        stats = session.execute(text(CONNECTION_STATS_SQL)).fetchone()
        max_conn = session.execute(text(MAX_CONNECTIONS_SQL)).fetchone()
        reserved = session.execute(text(SUPERUSER_RESERVED_SQL)).fetchone()

        stats_dict = dict(stats._mapping)
        max_connections = max_conn[0] if max_conn else 100
        reserved_connections = reserved[0] if reserved else 3
        available = max_connections - reserved_connections

        return ConnectionStats(
            total_connections=stats_dict["total_connections"],
            active=stats_dict["active"],
            idle=stats_dict["idle"],
            idle_in_transaction=stats_dict["idle_in_transaction"],
            waiting=stats_dict["waiting"],
            max_connections=max_connections,
            reserved_connections=reserved_connections,
            usage_percent=round(100.0 * stats_dict["total_connections"] / available, 2)
        )


def get_client_connections(engine, limit: int = 20) -> list[dict]:
    """Get connections grouped by client."""
    with Session(engine) as session:
        result = session.execute(text(CLIENT_CONNECTIONS_SQL), {"limit": limit})
        return [dict(row._mapping) for row in result]


def get_connection_details(engine, limit: int = 50) -> list[dict]:
    """Get detailed connection information."""
    with Session(engine) as session:
        result = session.execute(text(CONNECTION_WAIT_SQL), {"limit": limit})
        return [dict(row._mapping) for row in result]


def generate_recommendations(stats: ConnectionStats, clients: list[dict]) -> list[PoolRecommendation]:
    """Generate pool configuration recommendations."""
    recommendations = []

    # High usage warning
    if stats.usage_percent > 80:
        recommendations.append(PoolRecommendation(
            setting="max_connections",
            current_value=str(stats.max_connections),
            recommended_value=str(int(stats.max_connections * 1.5)),
            reason=f"Connection usage at {stats.usage_percent}%",
            implementation=f"ALTER SYSTEM SET max_connections = {int(stats.max_connections * 1.5)};\n-- Requires restart"
        ))

    # Idle in transaction
    if stats.idle_in_transaction > stats.total_connections * 0.2:
        recommendations.append(PoolRecommendation(
            setting="idle_in_transaction_session_timeout",
            current_value="0 (disabled)",
            recommended_value="30min",
            reason=f"{stats.idle_in_transaction} connections idle in transaction",
            implementation="ALTER SYSTEM SET idle_in_transaction_session_timeout = '30min';\nSELECT pg_reload_conf();"
        ))

    # SQLAlchemy pool recommendations
    active_ratio = stats.active / max(stats.total_connections, 1)
    recommended_pool = max(5, min(20, stats.active * 2))

    recommendations.append(PoolRecommendation(
        setting="SQLAlchemy pool_size",
        current_value="(check your code)",
        recommended_value=str(recommended_pool),
        reason=f"Based on {stats.active} active connections",
        implementation=f"""engine = create_engine(
    DATABASE_URL,
    pool_size={recommended_pool},
    max_overflow={recommended_pool},
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)"""
    ))

    # PgBouncer recommendation
    if stats.total_connections > 50:
        recommendations.append(PoolRecommendation(
            setting="PgBouncer",
            current_value="Not configured",
            recommended_value="Install PgBouncer",
            reason=f"{stats.total_connections} connections suggest pooler needed",
            implementation="""# /etc/pgbouncer/pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_port = 6432
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20"""
        ))

    # Too many clients from single source
    if clients:
        top_client = clients[0]
        if top_client.get("connection_count", 0) > stats.total_connections * 0.5:
            recommendations.append(PoolRecommendation(
                setting="Connection limit per client",
                current_value="Unlimited",
                recommended_value=str(int(stats.max_connections * 0.3)),
                reason=f"Client {top_client.get('client_addr')} using {top_client['connection_count']} connections",
                implementation="-- Limit connections per user:\nALTER USER app_user CONNECTION LIMIT 50;"
            ))

    return recommendations


def format_markdown(stats: ConnectionStats, clients: list[dict],
                   details: list[dict], recommendations: list[PoolRecommendation]) -> str:
    """Format as markdown report."""
    lines = [
        "# Connection Pool Analysis Report",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Current Status",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Connections | {stats.total_connections} |",
        f"| Active | {stats.active} |",
        f"| Idle | {stats.idle} |",
        f"| Idle in Transaction | {stats.idle_in_transaction} |",
        f"| Waiting | {stats.waiting} |",
        f"| Max Connections | {stats.max_connections} |",
        f"| **Usage** | **{stats.usage_percent}%** |",
        "",
    ]

    # Status indicator
    if stats.usage_percent > 80:
        lines.append("> ⚠️ **WARNING:** Connection usage is high!")
    elif stats.idle_in_transaction > 5:
        lines.append("> ⚠️ **WARNING:** Multiple idle-in-transaction connections detected")
    else:
        lines.append("> ✅ Connection pool is healthy")
    lines.append("")

    if clients:
        lines.extend([
            "## Connections by Client",
            "",
            "| Client | User | Total | Active | Idle |",
            "|--------|------|-------|--------|------|",
        ])
        for client in clients[:10]:
            addr = client.get("client_addr") or "local"
            lines.append(
                f"| {addr} | {client.get('usename', 'N/A')} | "
                f"{client['connection_count']} | {client['active']} | {client['idle']} |"
            )
        lines.append("")

    if recommendations:
        lines.extend(["## Recommendations", ""])
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"### {i}. {rec.setting}")
            lines.append(f"- **Current:** {rec.current_value}")
            lines.append(f"- **Recommended:** {rec.recommended_value}")
            lines.append(f"- **Reason:** {rec.reason}")
            lines.append(f"```\n{rec.implementation}\n```")
            lines.append("")

    return "\n".join(lines)


def watch_mode(engine, interval: int = 5):
    """Continuous monitoring mode."""
    print(f"Watching connections every {interval}s. Press Ctrl+C to stop.")
    try:
        while True:
            stats = get_connection_stats(engine)
            status = "⚠️" if stats.usage_percent > 80 else "✅"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {status} "
                  f"Total: {stats.total_connections} | Active: {stats.active} | "
                  f"Idle: {stats.idle} | IdleTxn: {stats.idle_in_transaction} | "
                  f"Usage: {stats.usage_percent}%")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="Analyze connection pool usage")
    parser.add_argument("--db-url", required=True, help="Database connection URL")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--watch", action="store_true", help="Continuous monitoring")
    parser.add_argument("--interval", type=int, default=5, help="Watch interval")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    engine = create_engine(args.db_url)

    if args.watch:
        watch_mode(engine, args.interval)
        return

    stats = get_connection_stats(engine)
    clients = get_client_connections(engine)
    details = get_connection_details(engine)
    recommendations = generate_recommendations(stats, clients)

    if args.format == "json":
        output = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "stats": vars(stats),
            "clients": clients,
            "recommendations": [vars(r) for r in recommendations]
        }, indent=2, default=str)
    else:
        output = format_markdown(stats, clients, details, recommendations)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
