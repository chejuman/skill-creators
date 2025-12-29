---
name: db-performance-optimizer-v2
description: Premium hierarchical multi-agent database optimization system for PostgreSQL/SQLAlchemy. Features phase-isolated architecture with 4-12 parallel workers, expert-level analysis (Partial/Covering/GIN indexes, Vacuuming, Partitioning, N+1 detection, Lock contention, Connection pooling), and AI-powered recommendations. Triggers on "DB 최적화", "database optimization", "query performance", "N+1 문제", "인덱스 추천", "slow query", "PostgreSQL tuning".
---

# DB Performance Optimizer V2

Premium database optimization skill with hierarchical multi-agent architecture for PostgreSQL and SQLAlchemy applications.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DBA ORCHESTRATOR (Senior 15+ Years)                  │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 1: PROFILE ──► Collect metrics, identify bottlenecks             │
│   └── QueryProfiler Agent (background)                                  │
│   └── IndexAnalyzer Agent (background)                                  │
│   └── TableStatsCollector Agent (background)                            │
│ Phase 2: ANALYZE ──► Deep analysis of 4 expert categories              │
│   └── PostgreSQLEngine Agent (background)                               │
│   └── SQLAlchemyORM Agent (background)                                  │
│   └── QueryExecution Agent (background)                                 │
│   └── Architecture Agent (background)                                   │
│ Phase 3: OPTIMIZE ──► Generate recommendations                          │
│   └── IndexAdvisor Agent (background)                                   │
│   └── QueryRewriter Agent (background)                                  │
│   └── ConfigTuner Agent (background)                                    │
│ Phase 4: DELIVER ──► Synthesize actionable report                       │
│   └── ReportSynthesizer Agent                                           │
│   └── CodeGenerator Agent                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Full optimization analysis
/db-optimize-v2 --full

# Specific mode
/db-optimize-v2 --mode indexes --db-url postgresql://user:pass@host/db

# Expert deep analysis (level 5)
/db-optimize-v2 --depth 5 --mode vacuum

# Quick check (level 1-2)
/db-optimize-v2 --quick
```

## Depth Levels (Progressive Disclosure)

| Level | Workers | Focus                | Use Case                   |
| ----- | ------- | -------------------- | -------------------------- |
| 1     | 4       | Quick scan           | Health check               |
| 2     | 5       | Basic analysis       | Development debugging      |
| 3     | 7       | Standard (default)   | Regular optimization       |
| 4     | 10      | Deep analysis        | Production tuning          |
| 5     | 12      | Expert comprehensive | Major performance overhaul |

## Expert Categories

### 1. PostgreSQL Engine Optimization

| Technique          | Purpose                               | When to Use                |
| ------------------ | ------------------------------------- | -------------------------- |
| **Partial Index**  | Index subset of rows                  | Frequent queries on subset |
| **Covering Index** | Include all columns (Index Only Scan) | Avoid table heap access    |
| **GIN Index**      | JSONB, Full-text, Arrays              | Complex data type searches |
| **Vacuuming**      | Remove dead tuples, prevent bloat     | High UPDATE/DELETE tables  |
| **Partitioning**   | Split large tables                    | Tables > 100M rows         |
| **Planner Stats**  | Update statistics for optimal plans   | After bulk data changes    |

### 2. SQLAlchemy ORM Optimization

| Technique              | Purpose                                 | Code Pattern                |
| ---------------------- | --------------------------------------- | --------------------------- |
| **Joined Loading**     | Single JOIN query                       | `joinedload(User.profile)`  |
| **Selectin Loading**   | Efficient batch loading                 | `selectinload(User.orders)` |
| **Subquery Loading**   | Subquery for collections                | `subqueryload(User.items)`  |
| **Bulk Operations**    | Mass insert/update without ORM overhead | `insert().values([...])`    |
| **Session Management** | Optimize Unit of Work                   | Context managers, scoped    |
| **Hybrid Attributes**  | SQL + Python expression                 | `@hybrid_property`          |

### 3. SQL Execution & Query Optimization

| Technique               | Purpose                        | Tool/Method                         |
| ----------------------- | ------------------------------ | ----------------------------------- |
| **EXPLAIN ANALYZE**     | Actual execution plan analysis | `EXPLAIN (ANALYZE, BUFFERS)`        |
| **Cost Optimization**   | Reduce query cost estimates    | Index hints, join order             |
| **CTE Materialization** | Control WITH clause caching    | `MATERIALIZED` / `NOT MATERIALIZED` |
| **Lock Contention**     | Reduce blocking and deadlocks  | `NOWAIT`, advisory locks            |

### 4. Architecture & Infrastructure

| Technique                 | Purpose                      | Implementation              |
| ------------------------- | ---------------------------- | --------------------------- |
| **Connection Pooling**    | Reduce connection overhead   | PgBouncer, SQLAlchemy pool  |
| **Read Replicas**         | Scale read operations        | Read-write splitting        |
| **Denormalization**       | Trade storage for read speed | Materialized views, caching |
| **AI Query Optimization** | Automatic performance tuning | 2025 ML-based advisors      |

## Phase 1: PROFILE

Collect comprehensive metrics using parallel background workers.

### Worker Configuration

```
# Worker 1: Query Profiler
Task(
  subagent_type='general-purpose',
  description='Profile database queries',
  prompt='''Profile PostgreSQL queries using pg_stat_statements.

  Execute these analyses:
  1. Identify top 20 slowest queries by total_exec_time
  2. Find queries with high calls but low efficiency
  3. Detect queries causing sequential scans
  4. Calculate cache hit ratio

  Return JSON format:
  {
    "phase": "PROFILE",
    "agent": "query_profiler",
    "slow_queries": [
      {"queryid": N, "query": "...", "total_time_ms": N, "calls": N, "mean_ms": N}
    ],
    "cache_hit_ratio": N,
    "seq_scan_queries": [...],
    "recommendations": [...]
  }
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 2: Index Analyzer
Task(
  subagent_type='general-purpose',
  description='Analyze index usage',
  prompt='''Analyze PostgreSQL index usage and effectiveness.

  Execute these analyses:
  1. Find unused indexes (idx_scan = 0)
  2. Identify duplicate/redundant indexes
  3. Detect tables with poor index usage
  4. Find missing indexes based on seq_scan patterns

  Return JSON format:
  {
    "phase": "PROFILE",
    "agent": "index_analyzer",
    "unused_indexes": [...],
    "duplicate_indexes": [...],
    "missing_indexes": [...],
    "index_bloat": [...]
  }
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 3: Table Stats Collector
Task(
  subagent_type='general-purpose',
  description='Collect table statistics',
  prompt='''Collect PostgreSQL table statistics for optimization.

  Execute these analyses:
  1. Table sizes and row counts
  2. Dead tuple ratios (vacuum candidates)
  3. Table bloat estimation
  4. Partitioning candidates (large tables)

  Return JSON format:
  {
    "phase": "PROFILE",
    "agent": "table_stats",
    "table_sizes": [...],
    "vacuum_candidates": [...],
    "bloat_estimates": [...],
    "partition_candidates": [...]
  }
  ''',
  model='haiku',
  run_in_background=true
)
```

### Synchronization Point

```
# Collect all PROFILE results
query_result = TaskOutput(task_id=worker1_id, block=true)
index_result = TaskOutput(task_id=worker2_id, block=true)
table_result = TaskOutput(task_id=worker3_id, block=true)

# Merge into phase output
phase1_output = {
  "phase": "PROFILE",
  "timestamp": now(),
  "query_analysis": query_result.data,
  "index_analysis": index_result.data,
  "table_analysis": table_result.data
}
```

## Phase 2: ANALYZE

Deep analysis using 4 expert category agents.

### PostgreSQL Engine Agent

```
Task(
  subagent_type='general-purpose',
  description='Analyze PostgreSQL engine',
  prompt='''You are a PostgreSQL engine expert. Analyze:

  Profile Data: {phase1_output}

  Focus on:
  1. Partial Index opportunities
     - Find WHERE clauses that filter < 30% of rows
     - Suggest: CREATE INDEX idx_name ON table (col) WHERE condition;

  2. Covering Index opportunities
     - Find queries with SELECT columns not in index
     - Suggest INCLUDE columns for Index Only Scans

  3. GIN Index candidates
     - JSONB columns with containment queries (@>, ?)
     - Full-text search columns
     - Array columns

  4. Vacuuming issues
     - Tables with dead_tuple_ratio > 10%
     - autovacuum_count vs expected

  5. Partitioning candidates
     - Tables > 10GB or > 100M rows
     - Time-series data patterns

  Return JSON format:
  {
    "phase": "ANALYZE",
    "agent": "postgresql_engine",
    "partial_indexes": [{
      "table": "...", "columns": [...], "condition": "...",
      "estimated_size_reduction": "N%", "create_statement": "..."
    }],
    "covering_indexes": [...],
    "gin_indexes": [...],
    "vacuum_issues": [...],
    "partition_recommendations": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

### SQLAlchemy ORM Agent

```
Task(
  subagent_type='Explore',
  description='Analyze SQLAlchemy patterns',
  prompt='''You are a SQLAlchemy optimization expert. Analyze the codebase:

  1. N+1 Query Detection
     - Find lazy loading in loops
     - Identify missing eager loading
     - Check relationship definitions

  2. Bulk Operation Opportunities
     - Find loops with session.add()
     - Identify batch update patterns
     - Detect inefficient deletes

  3. Session Management Issues
     - Long-running sessions
     - Missing context managers
     - Unnecessary flush/commit

  4. Hybrid Attribute Candidates
     - Python properties used in filters
     - Computed columns in queries

  Search for patterns in *.py files.

  Return JSON format:
  {
    "phase": "ANALYZE",
    "agent": "sqlalchemy_orm",
    "n1_issues": [{
      "file": "...", "line": N, "code": "...",
      "severity": "critical|high|medium",
      "fix": "Use selectinload(Model.relation)"
    }],
    "bulk_opportunities": [...],
    "session_issues": [...],
    "hybrid_candidates": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

### Query Execution Agent

```
Task(
  subagent_type='general-purpose',
  description='Analyze query execution',
  prompt='''You are a query execution expert. Analyze:

  Profile Data: {phase1_output}

  Focus on:
  1. EXPLAIN ANALYZE interpretation
     - Identify Seq Scan vs Index Scan
     - Find Nested Loop inefficiencies
     - Detect Sort and Hash operations

  2. Cost Optimization
     - High-cost operations
     - Join order issues
     - Missing statistics

  3. CTE Materialization
     - Find CTEs that should be MATERIALIZED
     - Identify CTEs that should NOT be materialized

  4. Lock Contention
     - Long-running transactions
     - UPDATE/DELETE patterns causing locks
     - Deadlock-prone patterns

  Return JSON format:
  {
    "phase": "ANALYZE",
    "agent": "query_execution",
    "plan_issues": [...],
    "cost_optimizations": [...],
    "cte_recommendations": [...],
    "lock_issues": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

### Architecture Agent

```
Task(
  subagent_type='general-purpose',
  description='Analyze architecture',
  prompt='''You are a database architecture expert. Analyze:

  Profile Data: {phase1_output}

  Focus on:
  1. Connection Pooling
     - Current pool configuration
     - PgBouncer recommendations
     - Connection wait times

  2. Read Replica Candidates
     - Read-heavy query patterns
     - Queries suitable for replica routing

  3. Denormalization Opportunities
     - Frequently joined tables
     - Aggregation queries
     - Materialized view candidates

  4. Cloud-Native Scaling (2025)
     - Serverless options (Neon, Aurora Serverless)
     - Auto-scaling configurations

  Return JSON format:
  {
    "phase": "ANALYZE",
    "agent": "architecture",
    "pooling_recommendations": [...],
    "replica_candidates": [...],
    "denormalization": [...],
    "scaling_recommendations": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Phase 3: OPTIMIZE

Generate prioritized recommendations.

### Index Advisor Agent

```
Task(
  subagent_type='general-purpose',
  description='Generate index recommendations',
  prompt='''Generate prioritized index recommendations.

  Analysis Data: {phase2_output}

  For each recommendation:
  1. Provide exact CREATE INDEX statement
  2. Estimate impact (query time reduction)
  3. Estimate storage cost
  4. Priority (1-5, 1=highest)
  5. Risk assessment

  Return JSON format:
  {
    "phase": "OPTIMIZE",
    "agent": "index_advisor",
    "recommendations": [{
      "type": "partial|covering|gin|btree",
      "table": "...",
      "create_statement": "CREATE INDEX ...",
      "drop_statement": "DROP INDEX ...",  // for unused
      "estimated_improvement": "Nx faster",
      "storage_impact": "+N MB",
      "priority": 1-5,
      "risk": "low|medium|high"
    }]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

### Query Rewriter Agent

```
Task(
  subagent_type='general-purpose',
  description='Rewrite inefficient queries',
  prompt='''Rewrite inefficient queries and SQLAlchemy code.

  Analysis Data: {phase2_output}

  For each issue:
  1. Show original code/query
  2. Provide optimized version
  3. Explain the improvement
  4. Estimate performance gain

  Return JSON format:
  {
    "phase": "OPTIMIZE",
    "agent": "query_rewriter",
    "rewrites": [{
      "file": "...",
      "line": N,
      "original": "...",
      "optimized": "...",
      "explanation": "...",
      "estimated_gain": "Nx"
    }]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

### Config Tuner Agent

```
Task(
  subagent_type='general-purpose',
  description='Tune configurations',
  prompt='''Generate configuration recommendations.

  Analysis Data: {phase2_output}

  Provide recommendations for:
  1. PostgreSQL settings (postgresql.conf)
     - shared_buffers, work_mem, effective_cache_size
     - autovacuum settings
     - checkpoint settings

  2. SQLAlchemy Engine settings
     - pool_size, max_overflow
     - pool_timeout, pool_recycle

  3. PgBouncer settings (if applicable)
     - pool_mode, max_client_conn

  Return JSON format:
  {
    "phase": "OPTIMIZE",
    "agent": "config_tuner",
    "postgresql": {...},
    "sqlalchemy": {...},
    "pgbouncer": {...}
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Phase 4: DELIVER

Synthesize all findings into actionable report.

### Report Template

See [assets/premium_report.md](assets/premium_report.md) for full template.

```markdown
# Database Optimization Report V2

**Generated:** {timestamp}
**Depth Level:** {level}
**Database:** {db_name}

## Executive Summary

| Metric          | Current | Projected | Improvement |
| --------------- | ------- | --------- | ----------- |
| Avg Query Time  | 150ms   | 15ms      | 10x         |
| Cache Hit Ratio | 85%     | 98%       | +13%        |
| N+1 Queries     | 23      | 0         | -100%       |
| Index Coverage  | 60%     | 95%       | +35%        |

## Priority Actions

### P1: Critical (Do Now)

1. [Index] Create partial index on orders.status
2. [Code] Fix N+1 in user_list.py:45

### P2: High (This Sprint)

...

### P3: Medium (Backlog)

...

## Detailed Analysis

### PostgreSQL Engine

[Partial indexes, Covering indexes, GIN, Vacuum, Partitioning]

### SQLAlchemy ORM

[N+1 fixes, Bulk operations, Session management]

### Query Execution

[EXPLAIN analysis, CTE optimization, Lock fixes]

### Architecture

[Connection pooling, Read replicas, Denormalization]

## Implementation Scripts

[Generated SQL and Python code]

## Monitoring Setup

[pg_stat_statements, query logging, alerting]
```

## Scripts

| Script                   | Purpose                              |
| ------------------------ | ------------------------------------ |
| `vacuum_analyzer.py`     | Analyze table bloat and vacuum needs |
| `partition_advisor.py`   | Recommend partitioning strategy      |
| `lock_monitor.py`        | Monitor lock contention              |
| `index_advisor.py`       | Advanced index recommendations       |
| `n1_detector.py`         | SQLAlchemy N+1 detection             |
| `query_profiler.py`      | Profile and analyze queries          |
| `explain_analyzer.py`    | Parse EXPLAIN ANALYZE output         |
| `connection_analyzer.py` | Analyze connection pool usage        |

## References

- [postgresql_expert.md](references/postgresql_expert.md) - PostgreSQL deep dive
- [sqlalchemy_expert.md](references/sqlalchemy_expert.md) - SQLAlchemy patterns
- [query_optimization.md](references/query_optimization.md) - Query tuning
- [architecture_patterns.md](references/architecture_patterns.md) - Scaling patterns
- [json_schemas.md](references/json_schemas.md) - Agent communication

## Trigger Phrases

- "DB 최적화" / "database optimization"
- "쿼리 성능" / "query performance"
- "N+1 문제" / "N+1 problem"
- "인덱스 추천" / "index recommendation"
- "slow query" / "느린 쿼리"
- "PostgreSQL 튜닝" / "PostgreSQL tuning"
- "SQLAlchemy 최적화"
- "데드락" / "deadlock"
- "커넥션 풀" / "connection pool"
