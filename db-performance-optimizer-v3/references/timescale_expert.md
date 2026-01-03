# TimescaleDB Expert Reference

Advanced TimescaleDB optimization techniques for time-series workloads.

## Hypertable Optimization

### Chunk Interval Sizing

```sql
-- View current chunk intervals
SELECT hypertable_name, chunk_interval
FROM timescaledb_information.dimensions
WHERE dimension_type = 'Time';

-- Optimal chunk sizing (target: 25% of memory)
-- Rule: Each chunk should be 10-25% of shared_buffers
-- For 4GB shared_buffers: 400MB-1GB per chunk

-- Adjust chunk interval
SELECT set_chunk_time_interval('metrics', INTERVAL '1 day');
-- Small chunks (1 hour): High insert, many short queries
-- Medium chunks (1 day): Balanced workloads
-- Large chunks (1 week): Analytical, bulk inserts
```

### Chunk Analysis

```sql
-- Chunk statistics
SELECT
    hypertable_name,
    chunk_name,
    range_start,
    range_end,
    pg_size_pretty(total_bytes) as size,
    total_bytes
FROM timescaledb_information.chunks
ORDER BY range_start DESC
LIMIT 20;

-- Chunk count per hypertable
SELECT
    hypertable_name,
    COUNT(*) as chunk_count,
    pg_size_pretty(SUM(total_bytes)) as total_size
FROM timescaledb_information.chunks
GROUP BY hypertable_name;
```

## Compression Policies

### Enable Compression

```sql
-- Enable compression on hypertable
ALTER TABLE metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'device_id',
    timescaledb.compress_orderby = 'time DESC'
);

-- Segmentby selection rules:
-- - Use columns with low cardinality
-- - Commonly used in WHERE clauses
-- - Example: device_id, sensor_type, region

-- Orderby selection:
-- - Primary time column (always DESC for recent data)
-- - Secondary ordering columns for range scans
```

### Compression Policy

```sql
-- Add compression policy
SELECT add_compression_policy('metrics', INTERVAL '7 days');

-- View compression policies
SELECT * FROM timescaledb_information.jobs
WHERE proc_name = 'policy_compression';

-- Manual compression
SELECT compress_chunk(c.chunk_name)
FROM timescaledb_information.chunks c
WHERE c.hypertable_name = 'metrics'
  AND c.is_compressed = false
  AND c.range_end < NOW() - INTERVAL '7 days';

-- Check compression stats
SELECT
    hypertable_name,
    chunk_name,
    before_compression_total_bytes,
    after_compression_total_bytes,
    ROUND(100 - (after_compression_total_bytes::numeric /
          before_compression_total_bytes * 100), 2) as compression_ratio
FROM timescaledb_information.compressed_chunk_stats;
```

## Continuous Aggregates

### Create Continuous Aggregate

```sql
-- Materialized view with automatic refresh
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    device_id,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value,
    COUNT(*) as sample_count
FROM metrics
GROUP BY bucket, device_id
WITH NO DATA;

-- Add refresh policy
SELECT add_continuous_aggregate_policy('metrics_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);

-- Enable real-time aggregation (combine with raw data)
ALTER MATERIALIZED VIEW metrics_hourly SET (
    timescaledb.materialized_only = false
);
```

### Hierarchical Aggregates

```sql
-- Daily aggregate from hourly
CREATE MATERIALIZED VIEW metrics_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', bucket) AS day,
    device_id,
    AVG(avg_value) as avg_value,
    MIN(min_value) as min_value,
    MAX(max_value) as max_value,
    SUM(sample_count) as sample_count
FROM metrics_hourly
GROUP BY day, device_id
WITH NO DATA;
```

## Retention Policies

### Automated Data Lifecycle

```sql
-- Drop old chunks automatically
SELECT add_retention_policy('metrics', INTERVAL '90 days');

-- Tiered retention: Move to cold storage
-- 1. Compress after 7 days
-- 2. Move to S3 after 30 days (with pg_tier extension)
-- 3. Drop after 90 days

-- View retention policies
SELECT * FROM timescaledb_information.jobs
WHERE proc_name = 'policy_retention';

-- Manual cleanup
SELECT drop_chunks('metrics', older_than => INTERVAL '90 days');
```

## Query Optimization

### Time Bucket Functions

```sql
-- Standard time bucketing
SELECT
    time_bucket('5 minutes', time) AS bucket,
    AVG(value)
FROM metrics
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY bucket
ORDER BY bucket;

-- Time bucket with timezone
SELECT
    time_bucket('1 day', time, 'America/New_York') AS day,
    SUM(value)
FROM metrics
GROUP BY day;

-- Time bucket with origin (align to specific time)
SELECT
    time_bucket('1 week', time, TIMESTAMP '2024-01-01') AS week,
    AVG(value)
FROM metrics
GROUP BY week;
```

### Specialized Aggregates

```sql
-- First/Last aggregates (efficient for time-series)
SELECT
    device_id,
    first(value, time) as first_value,
    last(value, time) as last_value,
    max(time) - min(time) as duration
FROM metrics
WHERE time > NOW() - INTERVAL '1 day'
GROUP BY device_id;

-- Time-weighted average
SELECT
    device_id,
    time_weight('Linear', time, value) as weighted_avg
FROM metrics
GROUP BY device_id;

-- Approximate percentiles (faster than exact)
SELECT
    time_bucket('1 hour', time) AS hour,
    approx_percentile(0.95, percentile_agg(value)) as p95
FROM metrics
GROUP BY hour;
```

### Gap Filling

```sql
-- Fill missing time buckets
SELECT
    time_bucket_gapfill('5 minutes', time) AS bucket,
    device_id,
    locf(avg(value)) as value  -- Last observation carried forward
FROM metrics
WHERE time BETWEEN '2024-01-01' AND '2024-01-02'
GROUP BY bucket, device_id
ORDER BY bucket;

-- Interpolation
SELECT
    time_bucket_gapfill('5 minutes', time) AS bucket,
    interpolate(avg(value)) as value  -- Linear interpolation
FROM metrics
WHERE time BETWEEN '2024-01-01' AND '2024-01-02'
GROUP BY bucket;
```

## Best Practices Summary

| Aspect                | Recommendation                                            |
| --------------------- | --------------------------------------------------------- |
| Chunk interval        | 10-25% of shared_buffers per chunk                        |
| Compression           | Enable after 7 days, segment by low-cardinality columns   |
| Continuous Aggregates | Use for dashboards, enable real-time for freshness        |
| Retention             | Automate with policies, tier data for cost savings        |
| Indexes               | Create on (time, device_id), use partial for recent data  |
| Queries               | Use time_bucket(), first/last aggregates, avoid SELECT \* |
