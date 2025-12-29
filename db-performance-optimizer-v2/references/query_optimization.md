# Query Optimization Reference

Advanced SQL execution and query optimization techniques.

## EXPLAIN ANALYZE

### Reading Execution Plans

```sql
-- Full analysis with timing and buffers
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.*, o.total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active';
```

### Key Plan Components

| Component        | Meaning              | Action               |
| ---------------- | -------------------- | -------------------- |
| Seq Scan         | Full table scan      | Add index            |
| Index Scan       | Using index          | Good                 |
| Index Only Scan  | All data from index  | Optimal              |
| Bitmap Heap Scan | Index + table access | Acceptable for OR    |
| Nested Loop      | Row-by-row join      | Watch for high loops |
| Hash Join        | Build hash table     | Good for large sets  |
| Merge Join       | Sorted merge         | Good for sorted data |

### Common Issues

```sql
-- Problem: Seq Scan on large table
Seq Scan on orders  (cost=0.00..35000.00 rows=1000000 width=100)
  Filter: (status = 'active')
  Rows Removed by Filter: 900000
-- Solution: CREATE INDEX idx_orders_status ON orders (status);

-- Problem: Nested Loop with high loops
Nested Loop  (cost=0.43..8000.00 rows=10000 width=200)
  ->  Index Scan on users  (rows=100)
  ->  Index Scan on orders  (rows=100 loops=100)  -- 100 x 100!
-- Solution: Use Hash Join or add composite index

-- Problem: Sort with external merge
Sort  (cost=50000.00..51000.00 rows=500000 width=200)
  Sort Key: created_at
  Sort Method: external merge  Disk: 100MB
-- Solution: Increase work_mem or add index on sort column
```

## Cost-Based Optimization

### Understanding Costs

```sql
-- Cost format: (startup_cost..total_cost rows=X width=Y)
-- startup_cost: Time before first row
-- total_cost: Time for all rows
-- rows: Estimated row count
-- width: Average row size in bytes

-- Example analysis
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Index Scan (cost=0.43..8.45 rows=1 width=128)
--            startup=0.43, total=8.45, 1 row, 128 bytes
```

### Cost Parameters

```sql
-- View current settings
SHOW seq_page_cost;      -- 1.0 (sequential page read)
SHOW random_page_cost;   -- 4.0 (random page read, 1.1 for SSD)
SHOW cpu_tuple_cost;     -- 0.01 (processing each row)
SHOW cpu_index_tuple_cost; -- 0.005 (processing index entry)

-- Optimize for SSD
ALTER SYSTEM SET random_page_cost = 1.1;
SELECT pg_reload_conf();
```

### Forcing Plan Choices

```sql
-- Hint-like behavior (use sparingly)
SET enable_seqscan = off;  -- Force index usage
SET enable_hashjoin = off; -- Force nested loop

-- Better: Use index hints via column order
-- Index on (a, b) - these are NOT equivalent:
SELECT * FROM t WHERE a = 1 AND b = 2;  -- Uses index
SELECT * FROM t WHERE b = 2 AND a = 1;  -- May not use efficiently
```

## CTE Materialization

### MATERIALIZED vs NOT MATERIALIZED

```sql
-- MATERIALIZED: Execute once, store result
WITH active_users AS MATERIALIZED (
    SELECT id, name FROM users WHERE status = 'active'
)
SELECT * FROM active_users a1
JOIN active_users a2 ON a1.id != a2.id;
-- CTE computed once even though used twice

-- NOT MATERIALIZED: Inline as subquery (PostgreSQL 12+)
WITH recent_orders AS NOT MATERIALIZED (
    SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '1 day'
)
SELECT * FROM recent_orders WHERE status = 'pending';
-- Planner can push WHERE into CTE
```

### When to Use Each

| Scenario                 | Use              | Reason                   |
| ------------------------ | ---------------- | ------------------------ |
| CTE used multiple times  | MATERIALIZED     | Avoid recomputation      |
| CTE with external filter | NOT MATERIALIZED | Allow predicate pushdown |
| Recursive CTE            | (automatic)      | Always materialized      |
| Complex aggregation      | MATERIALIZED     | Cache result             |

## Lock Contention

### Understanding Lock Types

```sql
-- View current locks
SELECT
    l.locktype,
    l.relation::regclass,
    l.mode,
    l.granted,
    a.usename,
    a.query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted;
```

### Lock Modes (Least to Most Restrictive)

1. ACCESS SHARE (SELECT)
2. ROW SHARE (SELECT FOR UPDATE)
3. ROW EXCLUSIVE (INSERT, UPDATE, DELETE)
4. SHARE UPDATE EXCLUSIVE (VACUUM, CREATE INDEX CONCURRENTLY)
5. SHARE (CREATE INDEX)
6. SHARE ROW EXCLUSIVE (CREATE TRIGGER)
7. EXCLUSIVE (REFRESH MATERIALIZED VIEW CONCURRENTLY)
8. ACCESS EXCLUSIVE (ALTER TABLE, DROP)

### Avoiding Deadlocks

```sql
-- Pattern 1: Consistent ordering
-- Always access tables in same order: orders -> order_items

-- Pattern 2: Short transactions
BEGIN;
UPDATE orders SET status = 'shipped' WHERE id = 1;
COMMIT;  -- Commit ASAP

-- Pattern 3: NOWAIT for timeout
SELECT * FROM orders WHERE id = 1 FOR UPDATE NOWAIT;
-- Fails immediately if locked

-- Pattern 4: SKIP LOCKED for queues
SELECT * FROM job_queue
WHERE status = 'pending'
ORDER BY created_at
FOR UPDATE SKIP LOCKED
LIMIT 10;
-- Skips locked rows, great for worker queues

-- Pattern 5: Advisory locks for application-level locking
SELECT pg_advisory_lock(hashtext('user:' || user_id));
-- ... do work ...
SELECT pg_advisory_unlock(hashtext('user:' || user_id));
```

### Transaction Timeout

```sql
-- Prevent long-running transactions
SET statement_timeout = '30s';
SET lock_timeout = '10s';
SET idle_in_transaction_session_timeout = '5min';

-- Per-query timeout
SET LOCAL statement_timeout = '5s';
SELECT * FROM slow_query;
```

## Query Rewriting Patterns

### Subquery to JOIN

```sql
-- Before: Correlated subquery
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.status = 'active'
);

-- After: JOIN (often faster)
SELECT DISTINCT u.* FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.status = 'active';
```

### NOT IN to NOT EXISTS

```sql
-- Before: NOT IN (problematic with NULLs)
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM banned_users);

-- After: NOT EXISTS (NULL-safe, often faster)
SELECT * FROM users u
WHERE NOT EXISTS (SELECT 1 FROM banned_users b WHERE b.user_id = u.id);
```

### UNION ALL vs UNION

```sql
-- UNION: Removes duplicates (requires sort)
-- UNION ALL: Keeps duplicates (faster)

-- If duplicates OK or impossible:
SELECT * FROM orders_2023
UNION ALL
SELECT * FROM orders_2024;
```

### Batch Processing

```sql
-- Instead of: DELETE FROM logs WHERE created_at < '2024-01-01';
-- Use batched deletes:
DO $$
DECLARE
    deleted INT;
BEGIN
    LOOP
        DELETE FROM logs
        WHERE id IN (
            SELECT id FROM logs
            WHERE created_at < '2024-01-01'
            LIMIT 10000
        );
        GET DIAGNOSTICS deleted = ROW_COUNT;
        EXIT WHEN deleted = 0;
        COMMIT;
    END LOOP;
END $$;
```

## Performance Monitoring

### pg_stat_statements

```sql
-- Top queries by total time
SELECT
    queryid,
    round(total_exec_time::numeric, 2) as total_ms,
    calls,
    round(mean_exec_time::numeric, 2) as mean_ms,
    round(stddev_exec_time::numeric, 2) as stddev_ms,
    rows,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Queries with high variance (unstable performance)
SELECT query, mean_exec_time, stddev_exec_time,
       stddev_exec_time / mean_exec_time as cv
FROM pg_stat_statements
WHERE calls > 100
ORDER BY cv DESC
LIMIT 10;
```

### auto_explain

```sql
-- Log slow queries with execution plans
ALTER SYSTEM SET auto_explain.log_min_duration = '1s';
ALTER SYSTEM SET auto_explain.log_analyze = on;
ALTER SYSTEM SET auto_explain.log_buffers = on;
SELECT pg_reload_conf();
```
