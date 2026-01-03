# Phase 3: OPTIMIZE - Recommendation Agent Configurations

Optimization phase with 4 specialized agents including AI-powered recommendations.

## Index Advisor Agent

```
Task(
  subagent_type='general-purpose',
  description='Generate index recommendations',
  prompt='''Generate prioritized index recommendations.

  Analysis Data: {phase2_output}
  PostgreSQL Docs: {mcp_postgres_findings}

  For each index recommendation:

  1. **CREATE INDEX Statement**
     - Exact DDL with proper naming convention
     - CONCURRENTLY option when applicable
     - Partial index conditions

  2. **Impact Estimation**
     - Query time reduction (Nx faster)
     - Affected query count
     - Write overhead increase

  3. **Storage Cost**
     - Estimated index size (MB/GB)
     - Maintenance overhead

  4. **Priority Assignment**
     - P1: Critical (> 10x improvement, high traffic)
     - P2: High (5-10x improvement)
     - P3: Medium (2-5x improvement)

  5. **Risk Assessment**
     - low: Standard B-tree on small table
     - medium: Large table, may lock briefly
     - high: Concurrent build on very large table

  Return JSON:
  {
    "phase": "OPTIMIZE",
    "agent": "index_advisor",
    "recommendations": [{
      "id": "idx-001",
      "type": "partial|covering|gin|btree",
      "table": "schema.table",
      "create_statement": "CREATE INDEX CONCURRENTLY ...",
      "drop_statement": "DROP INDEX IF EXISTS ...",
      "estimated_improvement": "10x faster",
      "affected_queries": 15,
      "storage_impact": "+50 MB",
      "write_overhead": "+5%",
      "priority": "P1",
      "risk": "low|medium|high",
      "rollback": "DROP INDEX ..."
    }],
    "unused_indexes_to_drop": [...],
    "duplicate_indexes": [...]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Query Rewriter Agent

```
Task(
  subagent_type='general-purpose',
  description='Rewrite inefficient queries',
  prompt='''Rewrite inefficient queries and SQLAlchemy code.

  Analysis Data: {phase2_output}

  For each optimization:

  1. **Original Code/Query**
     - File location and line number
     - Full code snippet

  2. **Optimized Version**
     - Refactored code
     - Explanation of changes

  3. **Performance Gain**
     - Estimated speedup (Nx)
     - Memory reduction
     - Query count reduction

  4. **SQLAlchemy Patterns**
     - N+1 → selectinload/joinedload
     - Loop inserts → bulk_insert_mappings
     - Raw SQL → optimized ORM

  Return JSON:
  {
    "phase": "OPTIMIZE",
    "agent": "query_rewriter",
    "rewrites": [{
      "id": "qry-001",
      "file": "src/services/users.py",
      "line": 45,
      "type": "n1_fix|bulk_op|query_opt|session_fix",
      "original": "for user in users:\\n  orders = user.orders",
      "optimized": "users = session.execute(\\n  select(User).options(selectinload(User.orders))\\n)",
      "explanation": "Replace lazy loading loop with eager loading",
      "estimated_gain": "100x",
      "priority": "P1"
    }],
    "sql_rewrites": [{
      "original_query": "SELECT ...",
      "optimized_query": "SELECT ...",
      "changes": ["Added index hint", "Reordered joins"],
      "estimated_gain": "5x"
    }]
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Config Tuner Agent

```
Task(
  subagent_type='general-purpose',
  description='Tune configurations',
  prompt='''Generate configuration recommendations.

  Analysis Data: {phase2_output}
  PostgreSQL Docs: {mcp_postgres_findings}

  Provide recommendations for:

  1. **PostgreSQL Settings (postgresql.conf)**
     - Memory: shared_buffers, work_mem, effective_cache_size
     - Autovacuum: scale_factor, threshold, cost_delay
     - Checkpoints: checkpoint_completion_target, max_wal_size
     - Parallelism: max_parallel_workers_per_gather

  2. **SQLAlchemy Engine Settings**
     - pool_size, max_overflow
     - pool_timeout, pool_recycle
     - pool_pre_ping

  3. **PgBouncer Settings**
     - pool_mode (transaction recommended)
     - max_client_conn, default_pool_size
     - reserve_pool_size

  4. **TimescaleDB Settings**
     - timescaledb.max_background_workers
     - chunk_time_interval recommendations

  Return JSON:
  {
    "phase": "OPTIMIZE",
    "agent": "config_tuner",
    "postgresql": {
      "memory": {
        "shared_buffers": {"current": "128MB", "recommended": "4GB", "reason": "..."},
        "work_mem": {...},
        "effective_cache_size": {...}
      },
      "autovacuum": {...},
      "checkpoints": {...},
      "parallelism": {...}
    },
    "sqlalchemy": {
      "pool_size": {"current": 5, "recommended": 20, "reason": "..."},
      "max_overflow": {...}
    },
    "pgbouncer": {...},
    "timescaledb": {...},
    "apply_script": "ALTER SYSTEM SET shared_buffers = '4GB';\\n..."
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## AI Tuning Advisor Agent

```
Task(
  subagent_type='general-purpose',
  description='AI-powered tuning recommendations',
  prompt='''Provide AI-powered database tuning recommendations.

  All Phase Data: {all_phase_outputs}
  PostgreSQL Version: {pg_version}
  Cloud Provider: {cloud_provider}

  Generate intelligent recommendations:

  1. **Workload Pattern Analysis**
     - OLTP vs OLAP vs Mixed classification
     - Peak hours identification
     - Query pattern clustering

  2. **Predictive Recommendations**
     - Anticipated growth impact
     - Scaling trigger points
     - Proactive optimization

  3. **Cloud-Native Optimization (2025)**
     - AWS RDS Performance Insights integration
     - Google AlloyDB recommendations
     - Azure Hyperscale suggestions
     - Neon serverless sizing

  4. **Machine Learning Insights**
     - Query regression detection
     - Anomaly identification
     - Auto-scaling thresholds

  5. **Cost Optimization**
     - Resource right-sizing
     - Reserved capacity recommendations
     - Spot instance opportunities

  Return JSON:
  {
    "phase": "OPTIMIZE",
    "agent": "ai_tuning",
    "workload_analysis": {
      "classification": "OLTP|OLAP|Mixed",
      "peak_hours": ["09:00-12:00", "14:00-18:00"],
      "query_clusters": [...]
    },
    "predictions": {
      "growth_rate": "15% monthly",
      "scaling_trigger": "3 months",
      "proactive_actions": [...]
    },
    "cloud_native": {
      "provider": "AWS|GCP|Azure",
      "recommendations": [...],
      "cost_impact": {...}
    },
    "ml_insights": {
      "regressions": [...],
      "anomalies": [...],
      "auto_scaling": {...}
    },
    "cost_optimization": {
      "current_monthly": "$X",
      "projected_savings": "$Y",
      "recommendations": [...]
    }
  }
  ''',
  model='sonnet',
  run_in_background=true
)
```

## Phase 3 Synchronization

```
# Wait for all OPTIMIZE agents
optimize_results = await Promise.all([
  TaskOutput(task_id=index_advisor_id, block=true),
  TaskOutput(task_id=query_rewriter_id, block=true),
  TaskOutput(task_id=config_tuner_id, block=true),
  TaskOutput(task_id=ai_tuning_id, block=true)
])

phase3_output = {
  "phase": "OPTIMIZE",
  "timestamp": now(),
  "index_advisor": optimize_results[0],
  "query_rewriter": optimize_results[1],
  "config_tuner": optimize_results[2],
  "ai_tuning": optimize_results[3]
}
```
