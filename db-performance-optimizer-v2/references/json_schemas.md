# JSON Communication Schemas

Inter-agent communication schemas for the db-performance-optimizer-v2 skill.

## Phase 1: PROFILE Output

### Query Profiler Agent

```json
{
  "phase": "PROFILE",
  "agent": "query_profiler",
  "timestamp": "2025-12-28T10:30:00Z",
  "status": "complete",
  "data": {
    "slow_queries": [
      {
        "queryid": 12345678,
        "query": "SELECT * FROM orders WHERE user_id = $1",
        "total_time_ms": 15000.5,
        "calls": 10000,
        "mean_ms": 1.5,
        "max_ms": 250.0,
        "rows": 50000,
        "percent_total": 15.5
      }
    ],
    "cache_hit_ratio": 95.5,
    "seq_scan_queries": [
      {
        "query": "SELECT * FROM logs WHERE level = 'error'",
        "table": "logs",
        "seq_scan_count": 5000,
        "rows_read": 10000000
      }
    ]
  },
  "recommendations": [
    "Add index on orders(user_id)",
    "Consider partitioning logs table"
  ]
}
```

### Index Analyzer Agent

```json
{
  "phase": "PROFILE",
  "agent": "index_analyzer",
  "timestamp": "2025-12-28T10:30:00Z",
  "status": "complete",
  "data": {
    "unused_indexes": [
      {
        "table": "users",
        "index_name": "idx_users_old_email",
        "size": "256 MB",
        "scans": 0
      }
    ],
    "duplicate_indexes": [
      {
        "table": "orders",
        "indexes": ["idx_orders_user", "idx_orders_user_id"],
        "recommendation": "DROP INDEX idx_orders_user_id"
      }
    ],
    "missing_indexes": [
      {
        "table": "orders",
        "column": "status",
        "seq_scans": 50000,
        "recommendation": "CREATE INDEX idx_orders_status ON orders (status)"
      }
    ],
    "index_bloat": [
      {
        "table": "orders",
        "index": "orders_pkey",
        "bloat_ratio": 25.5,
        "recommendation": "REINDEX INDEX orders_pkey"
      }
    ]
  }
}
```

### Table Stats Agent

```json
{
  "phase": "PROFILE",
  "agent": "table_stats",
  "timestamp": "2025-12-28T10:30:00Z",
  "status": "complete",
  "data": {
    "table_sizes": [
      {
        "table": "events",
        "rows": 150000000,
        "size": "45 GB",
        "index_size": "12 GB"
      }
    ],
    "vacuum_candidates": [
      {
        "table": "orders",
        "dead_tuples": 500000,
        "dead_ratio": 15.5,
        "last_vacuum": "2025-12-25T00:00:00Z"
      }
    ],
    "bloat_estimates": [
      {
        "table": "users",
        "estimated_bloat": "20%",
        "wasted_bytes": 104857600
      }
    ],
    "partition_candidates": [
      {
        "table": "events",
        "reason": "150M rows, time-series data",
        "partition_key": "created_at",
        "partition_type": "RANGE"
      }
    ]
  }
}
```

## Phase 2: ANALYZE Output

### PostgreSQL Engine Agent

```json
{
  "phase": "ANALYZE",
  "agent": "postgresql_engine",
  "timestamp": "2025-12-28T10:35:00Z",
  "status": "complete",
  "data": {
    "partial_indexes": [
      {
        "table": "orders",
        "columns": ["user_id", "created_at"],
        "condition": "status = 'active'",
        "estimated_size_reduction": "70%",
        "create_statement": "CREATE INDEX idx_orders_active ON orders (user_id, created_at) WHERE status = 'active'",
        "priority": 1
      }
    ],
    "covering_indexes": [
      {
        "table": "users",
        "columns": ["email"],
        "include_columns": ["name", "created_at"],
        "create_statement": "CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (name, created_at)",
        "priority": 2
      }
    ],
    "gin_indexes": [
      {
        "table": "products",
        "column": "metadata",
        "type": "JSONB",
        "create_statement": "CREATE INDEX idx_products_metadata ON products USING GIN (metadata)",
        "priority": 2
      }
    ],
    "vacuum_issues": [
      {
        "table": "orders",
        "issue": "High dead tuple ratio",
        "severity": "high",
        "action": "VACUUM ANALYZE orders"
      }
    ],
    "partition_recommendations": [
      {
        "table": "events",
        "partition_type": "RANGE",
        "partition_key": "created_at",
        "interval": "monthly",
        "migration_script": "..."
      }
    ]
  }
}
```

### SQLAlchemy ORM Agent

```json
{
  "phase": "ANALYZE",
  "agent": "sqlalchemy_orm",
  "timestamp": "2025-12-28T10:35:00Z",
  "status": "complete",
  "data": {
    "n1_issues": [
      {
        "file": "app/services/user_service.py",
        "line": 45,
        "code": "for user in users: print(user.orders)",
        "severity": "critical",
        "fix": "Use selectinload(User.orders) in query",
        "fixed_code": "users = session.query(User).options(selectinload(User.orders)).all()"
      }
    ],
    "bulk_opportunities": [
      {
        "file": "app/tasks/import_users.py",
        "line": 78,
        "current": "for row in data: session.add(User(**row))",
        "recommended": "session.bulk_insert_mappings(User, data)",
        "estimated_speedup": "10x"
      }
    ],
    "session_issues": [
      {
        "file": "app/api/routes.py",
        "line": 23,
        "issue": "Session not closed properly",
        "recommendation": "Use context manager or scoped_session"
      }
    ],
    "hybrid_candidates": [
      {
        "file": "app/models/order.py",
        "property": "total_with_tax",
        "current": "@property def total_with_tax(self): return self.subtotal * 1.1",
        "recommendation": "Convert to @hybrid_property for SQL-side filtering"
      }
    ]
  }
}
```

### Query Execution Agent

```json
{
  "phase": "ANALYZE",
  "agent": "query_execution",
  "timestamp": "2025-12-28T10:35:00Z",
  "status": "complete",
  "data": {
    "plan_issues": [
      {
        "query": "SELECT * FROM orders WHERE status = 'active'",
        "issue": "Sequential Scan",
        "rows_scanned": 1000000,
        "rows_returned": 5000,
        "recommendation": "Add index on status column"
      }
    ],
    "cost_optimizations": [
      {
        "query": "SELECT * FROM users u JOIN orders o ON ...",
        "current_cost": 50000,
        "issue": "Nested Loop with high loops count",
        "recommendation": "Force Hash Join or add composite index"
      }
    ],
    "cte_recommendations": [
      {
        "query": "WITH active_users AS (...) SELECT * FROM active_users WHERE ...",
        "current": "default (MATERIALIZED)",
        "recommended": "NOT MATERIALIZED",
        "reason": "Allow predicate pushdown into CTE"
      }
    ],
    "lock_issues": [
      {
        "pattern": "Long UPDATE on orders table",
        "avg_duration": "5.2s",
        "recommendation": "Batch updates in smaller transactions"
      }
    ]
  }
}
```

### Architecture Agent

```json
{
  "phase": "ANALYZE",
  "agent": "architecture",
  "timestamp": "2025-12-28T10:35:00Z",
  "status": "complete",
  "data": {
    "pooling_recommendations": [
      {
        "current": "SQLAlchemy pool_size=5",
        "recommended": "pool_size=20, max_overflow=30",
        "reason": "High connection wait times detected"
      },
      {
        "type": "PgBouncer",
        "recommended": true,
        "config": {
          "pool_mode": "transaction",
          "default_pool_size": 20,
          "max_client_conn": 1000
        }
      }
    ],
    "replica_candidates": [
      {
        "query_type": "Dashboard aggregations",
        "read_percentage": 95,
        "recommendation": "Route to read replica"
      }
    ],
    "denormalization": [
      {
        "type": "materialized_view",
        "name": "daily_sales_summary",
        "source_tables": ["orders", "order_items"],
        "refresh_strategy": "CONCURRENTLY every hour"
      }
    ],
    "scaling_recommendations": [
      {
        "type": "serverless",
        "provider": "Neon",
        "benefit": "Auto-scaling, pay-per-use"
      }
    ]
  }
}
```

## Phase 3: OPTIMIZE Output

### Index Advisor Agent

```json
{
  "phase": "OPTIMIZE",
  "agent": "index_advisor",
  "timestamp": "2025-12-28T10:40:00Z",
  "status": "complete",
  "data": {
    "recommendations": [
      {
        "type": "partial",
        "table": "orders",
        "create_statement": "CREATE INDEX idx_orders_active ON orders (user_id, created_at) WHERE status = 'active';",
        "drop_statement": null,
        "estimated_improvement": "10x faster for active order queries",
        "storage_impact": "+50 MB",
        "priority": 1,
        "risk": "low"
      },
      {
        "type": "drop_unused",
        "table": "users",
        "create_statement": null,
        "drop_statement": "DROP INDEX idx_users_old_email;",
        "estimated_improvement": "Save 256 MB storage",
        "storage_impact": "-256 MB",
        "priority": 2,
        "risk": "medium"
      }
    ]
  }
}
```

## Phase 4: DELIVER Output

### Final Report Structure

```json
{
  "phase": "DELIVER",
  "agent": "synthesizer",
  "timestamp": "2025-12-28T10:45:00Z",
  "report": {
    "executive_summary": {
      "issues_found": 15,
      "critical": 3,
      "high": 5,
      "medium": 7,
      "estimated_improvement": "10x average query speed"
    },
    "metrics": {
      "current": {
        "avg_query_time_ms": 150,
        "cache_hit_ratio": 85,
        "n1_queries": 23,
        "index_coverage": 60
      },
      "projected": {
        "avg_query_time_ms": 15,
        "cache_hit_ratio": 98,
        "n1_queries": 0,
        "index_coverage": 95
      }
    },
    "priority_actions": {
      "p1_critical": [
        {
          "type": "index",
          "action": "CREATE INDEX idx_orders_status ON orders (status);",
          "impact": "Reduce query time from 2s to 20ms"
        }
      ],
      "p2_high": [],
      "p3_medium": []
    },
    "implementation_scripts": {
      "indexes": "-- SQL script for all index changes",
      "vacuum": "-- Vacuum commands",
      "config": "-- PostgreSQL config changes"
    }
  }
}
```
