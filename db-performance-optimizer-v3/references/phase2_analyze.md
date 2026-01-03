# Phase 2: ANALYZE - Expert Agent Configurations

Deep analysis phase with 5 expert category agents.

## PostgreSQL Engine Agent

```
Task(
  subagent_type='general-purpose',
  description='Analyze PostgreSQL engine',
  prompt='''You are a PostgreSQL engine expert with 15+ years experience.

  Profile Data: {phase1_output}
  PostgreSQL Docs: {postgres_docs_findings}

  Analyze and recommend:

  1. **Partial Index Opportunities**
     - WHERE clauses filtering < 30% of rows
     - CREATE INDEX ... WHERE condition;
     - Estimated size reduction

  2. **Covering Index Opportunities**
     - SELECT columns not in index
     - INCLUDE columns for Index Only Scan
     - Heap access elimination

  3. **GIN Index Candidates**
     - JSONB containment queries (@>, ?)
     - Full-text search columns (tsvector)
     - Array columns with ANY/ALL

  4. **Vacuuming Issues**
     - dead_tuple_ratio > 10%
     - autovacuum_count analysis
     - Table bloat estimation

  5. **Partitioning Candidates**
     - Tables > 10GB or > 100M rows
     - Time-series data patterns
     - Hot/cold data separation

  Return JSON:
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

## SQLAlchemy ORM Agent

```
Task(
  subagent_type='Explore',
  description='Analyze SQLAlchemy patterns',
  prompt='''You are a SQLAlchemy 2.0 optimization expert.

  Search the codebase for SQLAlchemy patterns:

  1. **N+1 Query Detection**
     - Lazy loading in loops (severity: critical)
     - Missing eager loading (joinedload, selectinload)
     - Relationship access patterns

  2. **Bulk Operation Opportunities**
     - Loops with session.add()
     - Sequential update/delete patterns
     - Replace with insert().values([...])

  3. **Session Management Issues**
     - Long-running sessions
     - Missing context managers
     - Unnecessary flush/commit calls

  4. **Hybrid Attribute Candidates**
     - Python properties used in WHERE
     - Computed columns in filters

  Search patterns: "relationship(", "session.query", "select(", "joinedload"

  Return JSON:
  {
    "phase": "ANALYZE",
    "agent": "sqlalchemy_orm",
    "n1_issues": [{
      "file": "...", "line": N, "code": "...",
      "severity": "critical|high|medium",
      "fix": "selectinload(Model.relation)"
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

## Query Execution Agent

```
Task(
  subagent_type='general-purpose',
  description='Analyze query execution',
  prompt='''You are a query execution specialist.

  Profile Data: {phase1_output}

  Analyze:

  1. **EXPLAIN ANALYZE Interpretation**
     - Seq Scan → Index Scan opportunities
     - Nested Loop inefficiencies (high loops)
     - Sort/Hash operations in memory

  2. **Cost Optimization**
     - High-cost operations (> 10000)
     - Join order issues
     - Missing statistics

  3. **CTE Materialization**
     - CTEs reused multiple times → MATERIALIZED
     - CTEs with external filters → NOT MATERIALIZED

  4. **Lock Contention**
     - Long-running transactions
     - UPDATE/DELETE causing locks
     - Deadlock-prone patterns
     - SKIP LOCKED opportunities

  Return JSON:
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

## TimescaleDB Expert Agent

```
Task(
  subagent_type='general-purpose',
  description='Analyze TimescaleDB usage',
  prompt='''You are a TimescaleDB expert.

  TimescaleDB Discovery: {timescale_discovery}
  Tiger Docs: Use pg-aiguide MCP for TimescaleDB docs

  Analyze:

  1. **Chunk Optimization**
     - Chunk interval sizing (1 hour to 1 week)
     - Chunk count per hypertable
     - Over-chunking detection

  2. **Compression Policies**
     - Segmentby column selection
     - Orderby optimization
     - Compression ratio analysis

  3. **Continuous Aggregates**
     - Materialized view opportunities
     - Refresh policies
     - Real-time aggregation settings

  4. **Retention Policies**
     - Data lifecycle management
     - Drop_chunks automation
     - Archive strategies

  5. **Time-Series Query Patterns**
     - time_bucket() optimization
     - First/last aggregates
     - Interpolation functions

  MCP Lookup: mcp-cli call plugin_pg_pg-aiguide/semantic_search_tiger_docs

  Return JSON:
  {
    "phase": "ANALYZE",
    "agent": "timescale_expert",
    "chunk_recommendations": [...],
    "compression_policies": [...],
    "continuous_aggregates": [...],
    "retention_policies": [...],
    "query_patterns": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Architecture Expert Agent

```
Task(
  subagent_type='general-purpose',
  description='Analyze architecture',
  prompt='''You are a database architecture expert.

  Profile Data: {phase1_output}

  Analyze:

  1. **Connection Pooling**
     - Current pool configuration
     - PgBouncer recommendations
     - Connection wait times
     - Pool sizing formula

  2. **Read Replica Candidates**
     - Read-heavy query patterns (> 80% reads)
     - Queries suitable for replica routing
     - Replication lag tolerance

  3. **Denormalization Opportunities**
     - Frequently joined tables
     - Aggregation query patterns
     - Materialized view candidates

  4. **Cloud-Native Scaling (2025)**
     - Serverless options (Neon, Aurora Serverless v2)
     - Auto-scaling configurations
     - Multi-region strategies

  5. **Caching Strategies**
     - Redis integration points
     - Application-level caching
     - Query result caching

  Return JSON:
  {
    "phase": "ANALYZE",
    "agent": "architecture",
    "pooling_recommendations": [...],
    "replica_candidates": [...],
    "denormalization": [...],
    "scaling_recommendations": [...],
    "caching_strategies": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Phase 2 Synchronization

```
# Wait for all ANALYZE agents
analyze_results = await Promise.all([
  TaskOutput(task_id=pg_engine_id, block=true),
  TaskOutput(task_id=sqlalchemy_id, block=true),
  TaskOutput(task_id=query_exec_id, block=true),
  TaskOutput(task_id=timescale_id, block=true),
  TaskOutput(task_id=architecture_id, block=true)
])

phase2_output = {
  "phase": "ANALYZE",
  "timestamp": now(),
  "postgresql_engine": analyze_results[0],
  "sqlalchemy_orm": analyze_results[1],
  "query_execution": analyze_results[2],
  "timescale": analyze_results[3],
  "architecture": analyze_results[4]
}
```
