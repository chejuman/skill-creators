# PostgreSQL Expert Reference

Advanced PostgreSQL optimization techniques for expert-level database tuning.

## Indexing Strategies

### Partial Index

Create indexes on frequently queried subsets to reduce size and improve performance.

```sql
-- Index only active orders (70% reduction in index size)
CREATE INDEX idx_orders_active ON orders (user_id, created_at)
WHERE status = 'active';

-- Index recent data only
CREATE INDEX idx_logs_recent ON logs (created_at, level)
WHERE created_at > '2024-01-01';

-- Exclude NULL values
CREATE INDEX idx_users_email ON users (email)
WHERE email IS NOT NULL;
```

**When to use:**

- Filter conditions appear in > 70% of queries
- Subset is < 30% of total rows
- Need to reduce index maintenance overhead

### Covering Index (Index Only Scan)

Include all required columns to avoid heap access.

```sql
-- Include columns for Index Only Scan
CREATE INDEX idx_orders_covering ON orders (user_id)
INCLUDE (total_amount, status, created_at);

-- Query satisfied entirely from index
EXPLAIN ANALYZE
SELECT user_id, total_amount, status
FROM orders
WHERE user_id = 123;
-- Output: Index Only Scan
```

**When to use:**

- SELECT columns are known and limited
- High read frequency
- Table row size is large

### GIN Index

For JSONB, full-text search, and array operations.

```sql
-- JSONB containment queries
CREATE INDEX idx_data_gin ON documents USING GIN (data);
SELECT * FROM documents WHERE data @> '{"status": "active"}';

-- Full-text search
CREATE INDEX idx_content_fts ON articles USING GIN (to_tsvector('english', content));
SELECT * FROM articles WHERE to_tsvector('english', content) @@ to_tsquery('database & optimization');

-- Trigram for LIKE/ILIKE
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_name_trgm ON users USING GIN (name gin_trgm_ops);
SELECT * FROM users WHERE name ILIKE '%john%';
```

**GIN vs GiST:**

- GIN: Faster reads, slower writes, larger size
- GiST: Balanced, good for range queries

## Vacuuming & Bloat Management

### Understanding MVCC Bloat

```sql
-- Check table bloat
SELECT
    schemaname, relname,
    n_live_tup, n_dead_tup,
    round(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_ratio,
    last_vacuum, last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Check bloat estimation (pgstattuple extension)
CREATE EXTENSION pgstattuple;
SELECT * FROM pgstattuple('your_table');
```

### Autovacuum Tuning

```sql
-- Aggressive autovacuum for high-churn tables
ALTER TABLE orders SET (
    autovacuum_vacuum_scale_factor = 0.05,  -- Default 0.2
    autovacuum_vacuum_threshold = 50,        -- Default 50
    autovacuum_analyze_scale_factor = 0.02,  -- Default 0.1
    autovacuum_vacuum_cost_delay = 10        -- Default 2ms
);

-- Global settings for busy databases
ALTER SYSTEM SET autovacuum_max_workers = 6;
ALTER SYSTEM SET autovacuum_naptime = '15s';
SELECT pg_reload_conf();
```

### Manual Vacuum Strategy

```sql
-- Regular vacuum (non-blocking)
VACUUM (VERBOSE, ANALYZE) orders;

-- Full vacuum (blocking, reclaims space)
-- Use during maintenance window only
VACUUM FULL orders;

-- Parallel vacuum (PostgreSQL 13+)
VACUUM (PARALLEL 4) large_table;
```

## Declarative Partitioning

### Range Partitioning (Time-Series)

```sql
-- Create partitioned table
CREATE TABLE events (
    id BIGSERIAL,
    event_time TIMESTAMPTZ NOT NULL,
    event_type TEXT,
    payload JSONB,
    PRIMARY KEY (id, event_time)
) PARTITION BY RANGE (event_time);

-- Create monthly partitions
CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE events_2024_02 PARTITION OF events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Automatic partition creation (pg_partman)
CREATE EXTENSION pg_partman;
SELECT partman.create_parent(
    p_parent_table := 'public.events',
    p_control := 'event_time',
    p_type := 'native',
    p_interval := 'monthly',
    p_premake := 3
);
```

### Hash Partitioning (Distribution)

```sql
-- Hash partitioning for load distribution
CREATE TABLE users (
    id BIGSERIAL,
    email TEXT,
    data JSONB
) PARTITION BY HASH (id);

CREATE TABLE users_p0 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE users_p3 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

### List Partitioning (Categories)

```sql
-- List partitioning by region
CREATE TABLE sales (
    id BIGSERIAL,
    region TEXT,
    amount DECIMAL
) PARTITION BY LIST (region);

CREATE TABLE sales_na PARTITION OF sales FOR VALUES IN ('US', 'CA', 'MX');
CREATE TABLE sales_eu PARTITION OF sales FOR VALUES IN ('UK', 'DE', 'FR');
CREATE TABLE sales_asia PARTITION OF sales FOR VALUES IN ('JP', 'KR', 'CN');
CREATE TABLE sales_default PARTITION OF sales DEFAULT;
```

## Planner Statistics

### Manual Statistics Update

```sql
-- Analyze specific table
ANALYZE VERBOSE orders;

-- Analyze specific columns with higher granularity
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;
ANALYZE orders (status);

-- Extended statistics for correlated columns
CREATE STATISTICS orders_stats (dependencies, ndistinct)
ON user_id, status FROM orders;
ANALYZE orders;
```

### pg_stat_statements

```sql
-- Enable pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Find slowest queries
SELECT
    queryid,
    round(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    round(mean_exec_time::numeric, 2) as mean_ms,
    round((100 * total_exec_time / sum(total_exec_time) over())::numeric, 2) as percent,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Reset statistics
SELECT pg_stat_statements_reset();
```

## Configuration Recommendations

### Memory Settings

```sql
-- Shared buffers: 25% of RAM (max ~8GB)
ALTER SYSTEM SET shared_buffers = '4GB';

-- Work memory: Per-operation, be careful
ALTER SYSTEM SET work_mem = '256MB';

-- Maintenance work memory
ALTER SYSTEM SET maintenance_work_mem = '1GB';

-- Effective cache size: 75% of RAM
ALTER SYSTEM SET effective_cache_size = '12GB';
```

### Write Performance

```sql
-- WAL settings for write-heavy workloads
ALTER SYSTEM SET wal_buffers = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET max_wal_size = '4GB';

-- Synchronous commit (trade durability for speed)
SET synchronous_commit = off;  -- Per session only!
```

### Query Planning

```sql
-- Random page cost (lower for SSD)
ALTER SYSTEM SET random_page_cost = 1.1;  -- Default 4, SSD: 1.1

-- Parallel query settings
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
ALTER SYSTEM SET parallel_tuple_cost = 0.01;
```
