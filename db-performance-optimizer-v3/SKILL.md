---
name: db-performance-optimizer-v3
description: Premium enterprise-grade database optimization system with Level 7 hierarchical multi-agent architecture (15+ parallel workers). Features pg-aiguide MCP integration for real-time PostgreSQL docs, TimescaleDB optimization, AI-powered tuning, and JSON API output. Triggers on "DB 최적화", "database optimization", "query performance", "N+1 문제", "인덱스 추천", "slow query", "PostgreSQL tuning", "TimescaleDB", "시계열 최적화".
---

# DB Performance Optimizer V3

Premium enterprise database optimization with Level 7 hierarchical multi-agent architecture.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DBA ORCHESTRATOR (Principal Engineer)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Phase 1: DISCOVER (5 workers) ──► Profile + MCP Docs Lookup                │
│   ├── QueryProfiler Agent ──► pg_stat_statements analysis                   │
│   ├── IndexAnalyzer Agent ──► Index usage and bloat detection               │
│   ├── TableStatsCollector Agent ──► Table sizes, dead tuples                │
│   ├── PostgresDocsAgent Agent ──► pg-aiguide MCP real-time docs             │
│   └── TimescaleDiscovery Agent ──► Hypertable detection, compression        │
│                                                                             │
│ Phase 2: ANALYZE (5 workers) ──► Expert Deep Analysis                       │
│   ├── PostgreSQLEngine Agent ──► Partial/Covering/GIN indexes, Vacuum       │
│   ├── SQLAlchemyORM Agent ──► N+1, Bulk ops, Session management             │
│   ├── QueryExecution Agent ──► EXPLAIN, CTE, Locks                          │
│   ├── TimescaleExpert Agent ──► Chunks, Compression, CAggs                  │
│   └── ArchitectureExpert Agent ──► Pooling, Replicas, Scaling               │
│                                                                             │
│ Phase 3: OPTIMIZE (4 workers) ──► AI-Powered Recommendations                │
│   ├── IndexAdvisor Agent ──► CREATE/DROP index statements                   │
│   ├── QueryRewriter Agent ──► Optimized SQL/ORM code                        │
│   ├── ConfigTuner Agent ──► postgresql.conf, SQLAlchemy settings            │
│   └── AITuningAdvisor Agent ──► ML-based predictions, Cloud-native          │
│                                                                             │
│ Phase 4: DELIVER (3 workers) ──► Structured Output                          │
│   ├── JSONAPIGenerator Agent ──► Structured JSON API response               │
│   ├── ReportSynthesizer Agent ──► Executive summary, priorities             │
│   └── ImplementationPlanner Agent ──► Rollout plan, risk assessment         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Full optimization with JSON output
/db-optimize-v3 --full --output json

# TimescaleDB-focused analysis
/db-optimize-v3 --mode timescale --db-url postgresql://user:pass@host/db

# Expert deep analysis (level 7)
/db-optimize-v3 --depth 7

# Quick scan with MCP docs
/db-optimize-v3 --quick --with-docs
```

## Depth Levels (Progressive Workers)

| Level | Workers | Focus                | Use Case                     |
| ----- | ------- | -------------------- | ---------------------------- |
| 1     | 5       | Quick scan           | Health check                 |
| 2     | 7       | Basic analysis       | Development debugging        |
| 3     | 9       | Standard             | Regular optimization         |
| 4     | 11      | Deep analysis        | Production tuning            |
| 5     | 13      | Expert comprehensive | Major performance overhaul   |
| 6     | 15      | Enterprise           | Multi-database orchestration |
| 7     | 17+     | Ultra (AI-Powered)   | Full AI tuning + TimescaleDB |

## MCP Integration: pg-aiguide

Real-time PostgreSQL documentation lookup via MCP:

```
# PostgreSQL Docs Lookup
mcp-cli call plugin_pg_pg-aiguide/semantic_search_postgres_docs '{
  "version": "17",
  "limit": 10,
  "prompt": "partial index optimization WHERE clause"
}'

# TimescaleDB/Tiger Cloud Docs
mcp-cli call plugin_pg_pg-aiguide/semantic_search_tiger_docs '{
  "limit": 10,
  "prompt": "continuous aggregates refresh policy"
}'
```

## Phase 1: DISCOVER

Launch 5 parallel workers for comprehensive profiling.

### Worker Configuration

```
# Worker 1: Query Profiler
Task(
  subagent_type='general-purpose',
  description='Profile database queries',
  prompt='''Profile PostgreSQL queries via pg_stat_statements.

  Analyze:
  1. Top 20 slowest queries by total_exec_time
  2. Queries with high calls but low efficiency
  3. Sequential scan patterns
  4. Cache hit ratio

  Return JSON: {"phase":"DISCOVER","agent":"query_profiler",...}
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 2: Index Analyzer
Task(
  subagent_type='general-purpose',
  description='Analyze index usage',
  prompt='''Analyze PostgreSQL index effectiveness.

  Find:
  1. Unused indexes (idx_scan = 0)
  2. Duplicate/redundant indexes
  3. Missing indexes from seq_scan patterns
  4. Index bloat estimation

  Return JSON: {"phase":"DISCOVER","agent":"index_analyzer",...}
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 3: Table Stats Collector
Task(
  subagent_type='general-purpose',
  description='Collect table statistics',
  prompt='''Collect PostgreSQL table statistics.

  Gather:
  1. Table sizes and row counts
  2. Dead tuple ratios (vacuum candidates)
  3. Table bloat estimation
  4. Partitioning candidates

  Return JSON: {"phase":"DISCOVER","agent":"table_stats",...}
  ''',
  model='haiku',
  run_in_background=true
)

# Worker 4: PostgreSQL Docs Agent (MCP)
Task(
  subagent_type='general-purpose',
  description='Lookup PostgreSQL docs via MCP',
  prompt='''Use pg-aiguide MCP to lookup relevant PostgreSQL documentation.

  Based on profile findings, search for:
  1. Index optimization techniques
  2. Vacuum and autovacuum best practices
  3. Query planning improvements
  4. Configuration recommendations

  Execute: mcp-cli call plugin_pg_pg-aiguide/semantic_search_postgres_docs

  Return JSON: {"phase":"DISCOVER","agent":"postgres_docs",...}
  ''',
  model='sonnet',
  run_in_background=true
)

# Worker 5: TimescaleDB Discovery
Task(
  subagent_type='general-purpose',
  description='Discover TimescaleDB usage',
  prompt='''Detect and analyze TimescaleDB usage.

  Find:
  1. Hypertables and chunk intervals
  2. Compression policies
  3. Continuous aggregates
  4. Retention policies
  5. Time-series query patterns

  If no TimescaleDB, report potential use cases.

  Return JSON: {"phase":"DISCOVER","agent":"timescale_discovery",...}
  ''',
  model='haiku',
  run_in_background=true
)
```

### Synchronization Point

```
# Collect all DISCOVER results
results = await Promise.all([
  TaskOutput(task_id=worker1_id, block=true),
  TaskOutput(task_id=worker2_id, block=true),
  TaskOutput(task_id=worker3_id, block=true),
  TaskOutput(task_id=worker4_id, block=true),
  TaskOutput(task_id=worker5_id, block=true)
])

phase1_output = {
  "phase": "DISCOVER",
  "timestamp": now(),
  "query_analysis": results[0],
  "index_analysis": results[1],
  "table_analysis": results[2],
  "postgres_docs": results[3],
  "timescale_discovery": results[4]
}
```

## Phase 2: ANALYZE

Launch 5 expert agents for deep analysis.

See [references/phase2_analyze.md](references/phase2_analyze.md) for detailed agent configurations.

### Expert Categories

1. **PostgreSQL Engine** - Partial/Covering/GIN indexes, Vacuum, Partitioning
2. **SQLAlchemy ORM** - N+1, Bulk operations, Session management
3. **Query Execution** - EXPLAIN ANALYZE, CTE, Lock contention
4. **TimescaleDB Expert** - Chunks, Compression, Continuous Aggregates
5. **Architecture** - Connection pooling, Read replicas, Cloud scaling

## Phase 3: OPTIMIZE

Launch 4 optimization agents with AI-powered recommendations.

See [references/phase3_optimize.md](references/phase3_optimize.md) for detailed configurations.

### Optimization Categories

1. **Index Advisor** - CREATE/DROP statements with impact estimates
2. **Query Rewriter** - Optimized SQL and SQLAlchemy code
3. **Config Tuner** - postgresql.conf and SQLAlchemy settings
4. **AI Tuning Advisor** - ML-based predictions, cloud-native scaling

## Phase 4: DELIVER

Generate structured JSON API output.

### JSON API Schema

See [assets/json_api_schema.json](assets/json_api_schema.json) for complete schema.

```json
{
  "apiVersion": "v3",
  "metadata": {
    "generated": "ISO8601",
    "depth": 7,
    "database": "db_name",
    "workersUsed": 17
  },
  "summary": {
    "healthScore": 0-100,
    "categories": {
      "indexing": {"score": 0-25, "issues": N},
      "queryPerf": {"score": 0-25, "issues": N},
      "maintenance": {"score": 0-25, "issues": N},
      "architecture": {"score": 0-25, "issues": N}
    },
    "metrics": {
      "avgQueryTime": {"current": "ms", "projected": "ms", "improvement": "%"},
      "cacheHitRatio": {"current": "%", "projected": "%", "improvement": "%"},
      "n1Queries": {"current": N, "projected": N, "improvement": "%"}
    }
  },
  "recommendations": {
    "p1_critical": [...],
    "p2_high": [...],
    "p3_medium": [...]
  },
  "implementation": {
    "sql": {...},
    "python": {...},
    "config": {...}
  },
  "timescale": {
    "hypertables": [...],
    "compression": [...],
    "aggregates": [...]
  }
}
```

## Scripts

| Script                  | Purpose                              |
| ----------------------- | ------------------------------------ |
| `vacuum_analyzer.py`    | Analyze table bloat and vacuum needs |
| `partition_advisor.py`  | Recommend partitioning strategy      |
| `lock_monitor.py`       | Monitor lock contention              |
| `index_advisor.py`      | Advanced index recommendations       |
| `n1_detector.py`        | SQLAlchemy N+1 detection             |
| `query_profiler.py`     | Profile and analyze queries          |
| `timescale_analyzer.py` | TimescaleDB optimization analysis    |
| `json_report.py`        | Generate JSON API output             |

## References

- [phase2_analyze.md](references/phase2_analyze.md) - Phase 2 agent configs
- [phase3_optimize.md](references/phase3_optimize.md) - Phase 3 agent configs
- [postgresql_expert.md](references/postgresql_expert.md) - PostgreSQL deep dive
- [timescale_expert.md](references/timescale_expert.md) - TimescaleDB optimization
- [ai_tuning.md](references/ai_tuning.md) - AI-powered recommendations

## Trigger Phrases

- "DB 최적화" / "database optimization"
- "쿼리 성능" / "query performance"
- "N+1 문제" / "N+1 problem"
- "인덱스 추천" / "index recommendation"
- "slow query" / "느린 쿼리"
- "PostgreSQL 튜닝" / "PostgreSQL tuning"
- "TimescaleDB 최적화" / "TimescaleDB optimization"
- "시계열 데이터" / "time-series data"
- "AI 튜닝" / "AI tuning"
- "JSON API 리포트"
