# AI-Powered Database Tuning Reference

Advanced ML-based optimization and cloud-native tuning for 2025.

## Workload Analysis

### Classification Patterns

```
OLTP (Online Transaction Processing)
├── Short transactions (< 100ms)
├── High concurrency (1000+ connections)
├── Point queries (WHERE id = ?)
├── Small result sets (< 100 rows)
└── Write-heavy (> 30% writes)

OLAP (Online Analytical Processing)
├── Long queries (seconds to minutes)
├── Low concurrency (< 50 concurrent)
├── Aggregations and JOINs
├── Large result sets (millions of rows)
└── Read-heavy (> 95% reads)

Mixed Workload
├── Both patterns present
├── Time-based variation
├── May benefit from read replicas
└── Consider workload isolation
```

### Query Clustering

```python
# Pattern: Cluster queries by characteristics
clusters = {
    "point_lookups": {
        "pattern": "SELECT * FROM table WHERE id = ?",
        "optimization": "Ensure PK index, consider covering index"
    },
    "range_scans": {
        "pattern": "SELECT * FROM table WHERE date BETWEEN ? AND ?",
        "optimization": "Partial index on date, BRIN for large tables"
    },
    "aggregations": {
        "pattern": "SELECT COUNT/SUM/AVG FROM table GROUP BY",
        "optimization": "Materialized views, continuous aggregates"
    },
    "joins": {
        "pattern": "SELECT FROM a JOIN b JOIN c",
        "optimization": "Join order, hash vs nested loop"
    }
}
```

## Cloud-Native Optimization (2025)

### AWS RDS / Aurora

```python
# Performance Insights API
recommendations = {
    "aurora_serverless_v2": {
        "when": "Variable workload, cost optimization",
        "min_acu": 0.5,
        "max_acu": 128,
        "scaling": "Auto-scales in seconds"
    },
    "aurora_io_optimized": {
        "when": "I/O-heavy workloads",
        "savings": "Up to 40% on I/O costs"
    },
    "rds_proxy": {
        "when": "Lambda/serverless connections",
        "benefit": "Connection pooling, failover"
    }
}

# RDS Configuration
rds_tuning = {
    "db.r6g.xlarge": {
        "shared_buffers": "4GB",  # 25% of 16GB RAM
        "effective_cache_size": "12GB",  # 75%
        "work_mem": "256MB",
        "max_connections": 200
    }
}
```

### Google Cloud SQL / AlloyDB

```python
# AlloyDB Recommendations
alloydb_features = {
    "columnar_engine": {
        "when": "Analytical queries on OLTP data",
        "speedup": "100x for aggregations"
    },
    "ai_assistance": {
        "index_recommendations": True,
        "query_insights": True,
        "anomaly_detection": True
    }
}

# Cloud SQL flags
cloudsql_flags = {
    "max_connections": 500,
    "shared_preload_libraries": "pg_stat_statements,auto_explain",
    "log_min_duration_statement": 1000  # Log queries > 1s
}
```

### Azure Database for PostgreSQL

```python
azure_recommendations = {
    "flexible_server": {
        "burstable_tier": "Development, low traffic",
        "general_purpose": "Production workloads",
        "memory_optimized": "High-performance analytics"
    },
    "intelligent_performance": {
        "query_store": True,  # Query performance insights
        "automatic_tuning": True,  # Auto index recommendations
        "query_performance_insight": True
    }
}
```

### Neon Serverless

```python
neon_config = {
    "compute_size": "autoscaling",
    "autoscaling_limits": {
        "min_cu": 0.25,  # Scale to zero
        "max_cu": 8
    },
    "branching": {
        "use_case": "Dev/test environments",
        "cost_savings": "Up to 90%"
    },
    "connection_pooling": {
        "built_in": True,
        "max_connections": 10000
    }
}
```

## Machine Learning Insights

### Query Regression Detection

```python
# Detect performance degradation
def detect_regression(query_stats):
    """
    Alert when query performance degrades significantly.

    Triggers:
    - Mean execution time increased > 50%
    - P95 latency increased > 100%
    - Error rate increased > 5%
    """
    thresholds = {
        "mean_time_increase": 1.5,  # 50% slower
        "p95_increase": 2.0,  # 100% slower
        "error_rate_threshold": 0.05
    }
    return analyze_trends(query_stats, thresholds)
```

### Anomaly Detection

```python
# Identify unusual patterns
anomaly_types = {
    "sudden_spike": {
        "description": "Query time suddenly increased",
        "causes": ["Lock contention", "Statistics stale", "Plan change"]
    },
    "gradual_degradation": {
        "description": "Slow performance decline over time",
        "causes": ["Table bloat", "Index bloat", "Data growth"]
    },
    "periodic_pattern": {
        "description": "Performance issues at specific times",
        "causes": ["Backup jobs", "Batch processing", "Peak traffic"]
    }
}
```

### Auto-Scaling Thresholds

```python
# Intelligent scaling triggers
scaling_config = {
    "scale_up": {
        "cpu_threshold": 80,  # % utilization
        "connection_threshold": 0.8,  # % of max
        "latency_threshold_ms": 100,
        "cooldown_seconds": 300
    },
    "scale_down": {
        "cpu_threshold": 20,
        "idle_time_minutes": 30,
        "cooldown_seconds": 600
    },
    "predictive": {
        "enabled": True,
        "forecast_window_hours": 24,
        "pre_scale_minutes": 15
    }
}
```

## Cost Optimization

### Resource Right-Sizing

```python
def calculate_optimal_instance():
    """
    Analyze workload and recommend optimal instance size.
    """
    metrics = {
        "avg_cpu": 45,  # %
        "peak_cpu": 85,  # %
        "avg_memory": 60,  # %
        "iops": 5000,
        "storage_gb": 500
    }

    # Recommendation logic
    if metrics["peak_cpu"] < 50:
        return "Consider downsizing (save 30-50%)"
    elif metrics["avg_cpu"] > 80:
        return "Consider upsizing for headroom"
    else:
        return "Current sizing appropriate"
```

### Reserved Capacity

```python
reserved_recommendations = {
    "1_year_reserved": {
        "savings": "30-40%",
        "when": "Stable, predictable workload"
    },
    "3_year_reserved": {
        "savings": "50-60%",
        "when": "Long-term commitment possible"
    },
    "savings_plans": {
        "compute": "Flexible across instance types",
        "commitment": "$/hour commitment"
    }
}
```

## Integration Points

### MCP Documentation Lookup

```bash
# Get latest PostgreSQL configuration docs
mcp-cli call plugin_pg_pg-aiguide/semantic_search_postgres_docs '{
  "version": "17",
  "limit": 10,
  "prompt": "autovacuum tuning high transaction workload"
}'

# TimescaleDB compression best practices
mcp-cli call plugin_pg_pg-aiguide/semantic_search_tiger_docs '{
  "limit": 10,
  "prompt": "compression policy segmentby orderby optimization"
}'
```

### Monitoring Integration

```python
monitoring_stack = {
    "prometheus": {
        "exporter": "postgres_exporter",
        "metrics": ["pg_stat_statements", "pg_locks", "replication_lag"]
    },
    "grafana": {
        "dashboards": ["PostgreSQL Overview", "Query Performance", "Replication"]
    },
    "alerting": {
        "pagerduty": True,
        "slack": True,
        "thresholds": "Based on ML baseline"
    }
}
```
