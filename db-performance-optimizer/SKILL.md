---
name: db-performance-optimizer
description: Senior database performance engineer skill for SQLAlchemy, PostgreSQL, and ORM optimization. Provides comprehensive performance analysis, query optimization, and 2025 best practices including AI-driven tuning. Use when optimizing database queries, fixing N+1 problems, tuning PostgreSQL, or analyzing slow queries. Triggers on "database performance", "slow query", "SQLAlchemy optimization", "PostgreSQL tuning", "N+1 problem", "query optimization".
---

# Database Performance Optimizer

Expert-level database performance engineering for Python/SQLAlchemy/PostgreSQL environments.

## Persona

```
You are a senior database performance engineer with 15+ years of experience in:
- Python-based applications using SQLAlchemy ORM
- Raw SQL optimization and query planning
- PostgreSQL administration and tuning
- 2025 trends: AI-integrated query optimization, cloud-native scaling
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                 DB PERFORMANCE ORCHESTRATOR                          │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 1: PROFILE ──► Analyze current performance                    │
│   └── QueryProfiler Agent (background)                              │
│   └── SchemaAnalyzer Agent (background)                             │
│   └── IndexScanner Agent (background)                               │
│ Phase 2: DIAGNOSE ──► Identify bottlenecks                          │
│   └── N1Detector Agent (background)                                 │
│   └── SlowQueryAnalyzer Agent (background)                          │
│   └── ConnectionPoolAnalyzer Agent (background)                     │
│ Phase 3: OPTIMIZE ──► Generate recommendations                      │
│   └── QueryRewriter Agent (background)                              │
│   └── IndexAdvisor Agent (background)                               │
│   └── ConfigTuner Agent (background)                                │
│ Phase 4: IMPLEMENT ──► Apply fixes with code examples               │
│   └── CodeGenerator Agent                                           │
│   └── MigrationBuilder Agent                                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Analyze current database performance
/db-optimize --profile

# Fix N+1 query problems
/db-optimize --fix-n1

# Get index recommendations
/db-optimize --indexes

# Full optimization report
/db-optimize --full
```

## Depth Levels

| Level | Agents | Focus              | Use Case                |
| ----- | ------ | ------------------ | ----------------------- |
| 1     | 3      | Quick query review | Single slow query       |
| 2     | 5      | N+1 and loading    | ORM relationship issues |
| 3     | 7      | Full profile       | Standard optimization   |
| 4     | 9      | Deep analysis      | Production tuning       |
| 5     | 10+    | Comprehensive      | Architecture review     |

---

## Section 1: Introduction - Core Principles

### Why Database Performance Matters

```
Performance Impact Chain:
Slow Query → High Latency → Poor UX → Lost Revenue → System Failure
     ↓
I/O Bottleneck → Resource Exhaustion → Connection Pool Exhaustion
```

### Key Principles

| Principle                 | Description                      | Priority |
| ------------------------- | -------------------------------- | -------- |
| **Reduce I/O**            | Minimize disk reads, use indexes | Critical |
| **Efficient Queries**     | Fetch only needed data           | High     |
| **Connection Management** | Pool connections, avoid leaks    | High     |
| **Batch Operations**      | Group writes, reduce round-trips | Medium   |
| **Caching**               | Cache frequent queries           | Medium   |

### Performance Baseline Metrics

```python
# Target metrics for healthy database
METRICS = {
    "query_time_p95": "<100ms",      # 95th percentile
    "query_time_p99": "<500ms",      # 99th percentile
    "connection_pool_usage": "<70%", # Pool saturation
    "index_hit_ratio": ">99%",       # Index efficiency
    "cache_hit_ratio": ">95%",       # Buffer cache
    "n1_queries_per_request": 0,     # N+1 problems
}
```

---

## Section 2: Core Optimization Techniques

### 2.1 Query Optimization

#### EXPLAIN ANALYZE Workflow

```sql
-- Step 1: Get query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM orders
WHERE user_id = 123
AND created_at > '2025-01-01';

-- Key metrics to check:
-- - Seq Scan vs Index Scan
-- - Rows estimated vs actual
-- - Buffer hits vs reads
-- - Planning vs Execution time
```

#### Indexing Strategies

```python
from sqlalchemy import Index

# B-Tree: Default, good for equality and range
Index('idx_user_email', User.email)

# Partial Index: Reduce size by 80%
Index('idx_active_users', User.id,
      postgresql_where=User.is_active == True)

# GIN for JSONB
Index('idx_metadata', User.metadata,
      postgresql_using='gin')

# Expression Index
Index('idx_lower_email', func.lower(User.email))

# Covering Index (include columns)
Index('idx_order_user', Order.user_id,
      postgresql_include=['status', 'total'])
```

#### Anti-Pattern: N+1 Queries

```python
# BAD: N+1 Problem (1 + N queries)
users = session.query(User).all()
for user in users:
    print(user.orders)  # Each access = new query!

# GOOD: Eager Loading with joinedload
from sqlalchemy.orm import joinedload

users = session.query(User)\
    .options(joinedload(User.orders))\
    .all()

# GOOD: Subquery loading for large collections
from sqlalchemy.orm import subqueryload

users = session.query(User)\
    .options(subqueryload(User.orders))\
    .all()

# GOOD: Selectin loading (SQLAlchemy 1.4+)
from sqlalchemy.orm import selectinload

users = session.query(User)\
    .options(selectinload(User.orders))\
    .all()
```

### 2.2 ORM-Specific Optimizations

#### Load Only Required Columns

```python
from sqlalchemy.orm import load_only

# BAD: Load all columns
users = session.query(User).all()

# GOOD: Load only needed columns
users = session.query(User)\
    .options(load_only(User.id, User.name, User.email))\
    .all()

# BETTER: Use Core for read-heavy operations
from sqlalchemy import select

stmt = select(User.id, User.name, User.email)
results = session.execute(stmt).fetchall()
```

#### Bypass ORM for Bulk Operations

```python
# BAD: ORM for bulk insert (slow)
for item in items:
    session.add(Model(**item))
session.commit()

# GOOD: Core bulk insert
from sqlalchemy.dialects.postgresql import insert

stmt = insert(Model).values(items)
session.execute(stmt)
session.commit()

# BEST: PostgreSQL COPY (fastest)
import io
from sqlalchemy import text

buffer = io.StringIO()
for item in items:
    buffer.write(f"{item['col1']}\t{item['col2']}\n")
buffer.seek(0)

raw_conn = session.connection().connection
with raw_conn.cursor() as cur:
    cur.copy_from(buffer, 'table_name', columns=('col1', 'col2'))
raw_conn.commit()
```

#### Read Replicas for Scalability

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Primary for writes
primary_engine = create_engine("postgresql://primary:5432/db")

# Read replicas for queries
replica_engine = create_engine("postgresql://replica:5432/db")

PrimarySession = sessionmaker(bind=primary_engine)
ReplicaSession = sessionmaker(bind=replica_engine)

# Usage
def get_users():
    with ReplicaSession() as session:  # Read from replica
        return session.query(User).all()

def create_user(data):
    with PrimarySession() as session:  # Write to primary
        session.add(User(**data))
        session.commit()
```

### 2.3 PostgreSQL Tuning

#### Right Column Types

```sql
-- BAD: Oversized types
CREATE TABLE orders (
    id VARCHAR(255),           -- Use UUID or BIGINT
    amount VARCHAR(50),        -- Use NUMERIC
    created_at VARCHAR(100)    -- Use TIMESTAMPTZ
);

-- GOOD: Optimal types
CREATE TABLE orders (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    amount NUMERIC(12,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Memory Configuration

```ini
# postgresql.conf optimizations

# Shared buffers: 25% of RAM (max ~8GB)
shared_buffers = 4GB

# Work memory: RAM / max_connections / 4
work_mem = 256MB

# Maintenance work memory
maintenance_work_mem = 1GB

# Effective cache size: 75% of RAM
effective_cache_size = 12GB

# WAL configuration
wal_buffers = 64MB
checkpoint_completion_target = 0.9

# Connection pooling (use PgBouncer instead of high max_connections)
max_connections = 100
```

#### Connection Pooling with PgBouncer

```ini
# pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
pool_mode = transaction  # Best for most apps
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
```

```python
# SQLAlchemy with PgBouncer
engine = create_engine(
    "postgresql://user:pass@pgbouncer:6432/mydb",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections
    pool_recycle=3600    # Recycle after 1 hour
)
```

### 2.4 Scalability Best Practices

#### Handling High Traffic

```python
# 1. Use connection pooling
engine = create_engine(url, pool_size=20, max_overflow=40)

# 2. Async SQLAlchemy for high concurrency
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host/db",
    pool_size=20
)

async with AsyncSession(async_engine) as session:
    result = await session.execute(select(User))
    users = result.scalars().all()

# 3. Disable autocommit for batch operations
with engine.begin() as conn:
    conn.execute(text("SET synchronous_commit = off"))
    # Batch operations here
    conn.execute(text("SET synchronous_commit = on"))

# 4. Use UNLOGGED tables for temporary data
# CREATE UNLOGGED TABLE temp_imports (...);
```

---

## Section 3: 2025 Trends

### AI-Powered Query Optimization

```python
# Integration with pganalyze for AI recommendations
# https://pganalyze.com/

# AQO (Adaptive Query Optimization) extension
# https://github.com/postgrespro/aqo

# Enable AQO
# CREATE EXTENSION aqo;
# SET aqo.mode = 'intelligent';  # Auto ML optimization
```

### Tools Landscape 2025

| Tool                                                        | Purpose                             | Integration |
| ----------------------------------------------------------- | ----------------------------------- | ----------- |
| [pganalyze](https://pganalyze.com/)                         | AI index advisor, workload analysis | SaaS        |
| [AQO](https://github.com/postgrespro/aqo)                   | Adaptive query optimization         | Extension   |
| [EverSQL/Aiven](https://aiven.io/tools/sql-query-optimizer) | AI query rewriting                  | SaaS        |
| [pgvector](https://github.com/pgvector/pgvector)            | Vector similarity for AI            | Extension   |

### Cloud-Native Patterns

```yaml
# Kubernetes PostgreSQL with connection pooling
apiVersion: v1
kind: ConfigMap
metadata:
  name: pgbouncer-config
data:
  pgbouncer.ini: |
    [databases]
    * = host=postgres-primary port=5432
    [pgbouncer]
    pool_mode = transaction
    max_client_conn = 1000
    default_pool_size = 25
```

### ZSTD Compression (PostgreSQL 15+)

```sql
-- Enable ZSTD for large tables
ALTER TABLE logs SET (
    toast_compression = 'lz4'  -- or 'pglz'
);

-- For new tables
CREATE TABLE events (
    id BIGINT,
    payload JSONB COMPRESSION lz4
);
```

---

## Section 4: Implementation Steps

### Step-by-Step Framework

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. BASELINE ──► Measure current performance                    │
│    └── Enable pg_stat_statements                                │
│    └── Set up slow query logging                                │
│    └── Record key metrics                                       │
├─────────────────────────────────────────────────────────────────┤
│ 2. PROFILE ──► Identify slow queries                            │
│    └── Run scripts/query_profiler.py                            │
│    └── Analyze EXPLAIN output                                   │
│    └── Check N+1 patterns                                       │
├─────────────────────────────────────────────────────────────────┤
│ 3. OPTIMIZE ──► Apply fixes                                     │
│    └── Add missing indexes                                      │
│    └── Rewrite inefficient queries                              │
│    └── Adjust loading strategies                                │
├─────────────────────────────────────────────────────────────────┤
│ 4. VALIDATE ──► Confirm improvements                            │
│    └── Compare before/after metrics                             │
│    └── Load test with production data                           │
│    └── Monitor for regressions                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Monitoring Setup

```python
# Enable pg_stat_statements
# postgresql.conf: shared_preload_libraries = 'pg_stat_statements'

# Query to find slow queries
SLOW_QUERY_SQL = """
SELECT
    round(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    round(mean_exec_time::numeric, 2) as mean_time_ms,
    round((100 * total_exec_time / sum(total_exec_time) over ())::numeric, 2) as percent,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
"""
```

---

## Section 5: Conclusion

### Key Takeaways

| Priority | Action                             | Impact              |
| -------- | ---------------------------------- | ------------------- |
| 1        | Fix N+1 queries with eager loading | 10-100x faster      |
| 2        | Add missing indexes                | 50-300x faster      |
| 3        | Use connection pooling             | Prevents exhaustion |
| 4        | Load only needed columns           | 2-5x faster         |
| 5        | Batch bulk operations              | 10-50x faster       |

### Starting Points for Beginners

1. Enable `pg_stat_statements` and slow query logging
2. Learn to read EXPLAIN ANALYZE output
3. Use `selectinload()` instead of lazy loading
4. Run `scripts/query_profiler.py` on your project

### Resources

- [SQLAlchemy 2.0 Performance](https://docs.sqlalchemy.org/en/20/faq/performance.html)
- [PostgreSQL Tuning](https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server)
- [pganalyze Blog](https://pganalyze.com/blog)
- [Use The Index, Luke](https://use-the-index-luke.com/)

## Scripts

- `scripts/query_profiler.py` - Profile SQLAlchemy queries
- `scripts/n1_detector.py` - Detect N+1 query patterns
- `scripts/index_advisor.py` - Recommend missing indexes
- `scripts/benchmark.py` - Run performance benchmarks

## Trigger Phrases

- "database performance", "DB 성능"
- "slow query", "느린 쿼리"
- "SQLAlchemy optimization", "SQLAlchemy 최적화"
- "PostgreSQL tuning", "PostgreSQL 튜닝"
- "N+1 problem", "N+1 문제"
- "query optimization", "쿼리 최적화"
- "connection pool", "커넥션 풀"
- "index recommendation", "인덱스 추천"
