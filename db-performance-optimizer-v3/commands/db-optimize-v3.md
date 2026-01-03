---
allowed-tools:
  [
    Read,
    Bash(python3:*,
    psql:*,
    mcp-cli:*),
    Grep,
    Glob,
    Task,
    TaskOutput,
    AskUserQuestion,
  ]
description: Premium database optimization command with Level 7 hierarchical multi-agent architecture (17+ workers). Features pg-aiguide MCP integration, TimescaleDB optimization, AI-powered tuning, and JSON API output.
---

## Context

- Python files: !`find . -name "*.py" -type f | head -10`
- SQLAlchemy models: !`grep -r "class.*Model\|relationship\|Column" --include="*.py" -l 2>/dev/null | head -5`
- Database config: !`grep -r "DATABASE_URL\|postgresql\|create_engine" --include="*.py" -l 2>/dev/null | head -3`

## Arguments

Parse from $ARGUMENTS:

| Argument      | Description             | Default |
| ------------- | ----------------------- | ------- |
| `--mode`      | Operation mode          | full    |
| `--depth`     | Analysis depth 1-7      | 3       |
| `--db-url`    | Database URL            | (env)   |
| `--output`    | Output format (json/md) | json    |
| `--with-docs` | Enable MCP docs lookup  | false   |
| `--quick`     | Quick scan (depth 1)    | false   |
| `--full`      | Full analysis (depth 7) | false   |

### Mode Options

- `profile`: Database metrics profiling
- `indexes`: Index recommendations
- `n1`: N+1 query detection
- `vacuum`: Vacuum and bloat analysis
- `locks`: Lock contention monitoring
- `partition`: Partition recommendations
- `connections`: Connection pool analysis
- `explain`: Query plan analysis
- `timescale`: TimescaleDB optimization
- `full`: Complete optimization (all modes)

## Execution Protocol

### Step 1: Determine Depth Level

```python
if "--quick" in args:
    depth = 1
    workers = 5
elif "--full" in args:
    depth = 7
    workers = 17
else:
    depth = parse_depth(args)  # 1-7
    workers = 5 + (depth * 2)  # 5, 7, 9, 11, 13, 15, 17+
```

### Step 2: Phase 1 - DISCOVER (5 workers)

Launch parallel profiling agents:

```
# Worker 1: Query Profiler
Task(
  subagent_type='general-purpose',
  description='Profile queries',
  prompt='Profile PostgreSQL queries. Get top slow queries, cache ratio, seq scans. Return JSON.',
  model='haiku',
  run_in_background=true
)

# Worker 2: Index Analyzer
Task(
  subagent_type='general-purpose',
  description='Analyze indexes',
  prompt='Find unused indexes, duplicates, missing indexes. Return JSON.',
  model='haiku',
  run_in_background=true
)

# Worker 3: Table Stats
Task(
  subagent_type='general-purpose',
  description='Collect table stats',
  prompt='Get table sizes, dead tuple ratios, partition candidates. Return JSON.',
  model='haiku',
  run_in_background=true
)

# Worker 4: PostgreSQL Docs (MCP) - if --with-docs
Task(
  subagent_type='general-purpose',
  description='Lookup PostgreSQL docs',
  prompt='Use pg-aiguide MCP for relevant docs. Execute:
    mcp-cli call plugin_pg_pg-aiguide/semantic_search_postgres_docs
  Return JSON.',
  model='sonnet',
  run_in_background=true
)

# Worker 5: TimescaleDB Discovery - if --mode timescale or --full
Task(
  subagent_type='general-purpose',
  description='Discover TimescaleDB',
  prompt='Detect hypertables, compression, continuous aggregates. Return JSON.',
  model='haiku',
  run_in_background=true
)
```

Wait for all DISCOVER workers:

```
phase1_results = await Promise.all([worker1, worker2, worker3, worker4, worker5])
```

### Step 3: Phase 2 - ANALYZE (5 workers, depth >= 3)

Launch expert category agents:

```
# PostgreSQL Engine Expert
Task(
  subagent_type='general-purpose',
  description='PostgreSQL engine analysis',
  prompt='Analyze: Partial/Covering/GIN indexes, Vacuum issues, Partitioning.
  Profile Data: {phase1_output}. Return JSON.',
  model='sonnet',
  run_in_background=true
)

# SQLAlchemy ORM Expert
Task(
  subagent_type='Explore',
  description='SQLAlchemy analysis',
  prompt='Find N+1 issues, bulk operation opportunities, session problems.
  Search *.py files. Return JSON.',
  model='sonnet',
  run_in_background=true
)

# Query Execution Expert (depth >= 4)
Task(
  subagent_type='general-purpose',
  description='Query execution analysis',
  prompt='Analyze EXPLAIN plans, CTE materialization, lock contention.
  Return JSON.',
  model='sonnet',
  run_in_background=true
)

# TimescaleDB Expert (depth >= 4, mode=timescale)
Task(
  subagent_type='general-purpose',
  description='TimescaleDB analysis',
  prompt='Optimize chunks, compression, continuous aggregates, retention.
  Use MCP for Tiger docs. Return JSON.',
  model='sonnet',
  run_in_background=true
)

# Architecture Expert (depth >= 5)
Task(
  subagent_type='general-purpose',
  description='Architecture analysis',
  prompt='Analyze connection pooling, read replicas, cloud scaling.
  Return JSON.',
  model='sonnet',
  run_in_background=true
)
```

### Step 4: Phase 3 - OPTIMIZE (4 workers)

```
# Index Advisor
Task(
  subagent_type='general-purpose',
  description='Generate index recommendations',
  prompt='Generate CREATE/DROP INDEX statements with priority, impact, risk.
  Analysis: {phase2_output}. Return JSON.',
  model='sonnet',
  run_in_background=true
)

# Query Rewriter
Task(
  subagent_type='general-purpose',
  description='Rewrite queries',
  prompt='Optimize SQL and SQLAlchemy code. Show before/after.
  Return JSON.',
  model='sonnet',
  run_in_background=true
)

# Config Tuner
Task(
  subagent_type='general-purpose',
  description='Tune configurations',
  prompt='Generate postgresql.conf, SQLAlchemy, PgBouncer settings.
  Return JSON.',
  model='sonnet',
  run_in_background=true
)

# AI Tuning Advisor (depth >= 6)
Task(
  subagent_type='general-purpose',
  description='AI tuning recommendations',
  prompt='Provide ML-based predictions, cloud-native scaling, cost optimization.
  Return JSON.',
  model='sonnet',
  run_in_background=true
)
```

### Step 5: Phase 4 - DELIVER (3 workers)

```
# JSON API Generator
Task(
  subagent_type='general-purpose',
  description='Generate JSON API',
  prompt='Create structured JSON API response per schema.
  All phases: {all_outputs}. Return JSON.',
  model='sonnet'
)

# Report Synthesizer
Task(
  subagent_type='general-purpose',
  description='Synthesize report',
  prompt='Create executive summary and priority actions.
  Return JSON.',
  model='sonnet',
  run_in_background=true
)

# Implementation Planner
Task(
  subagent_type='general-purpose',
  description='Plan implementation',
  prompt='Create rollout plan with risk assessment.
  Return JSON.',
  model='sonnet',
  run_in_background=true
)
```

## Script Execution

```bash
# Query profiling
python3 ~/.claude/skills/db-performance-optimizer-v3/scripts/query_profiler.py \
  --db-url $DB_URL --top 20

# Index recommendations
python3 ~/.claude/skills/db-performance-optimizer-v3/scripts/index_advisor.py \
  --db-url $DB_URL --limit 20

# N+1 detection
python3 ~/.claude/skills/db-performance-optimizer-v3/scripts/n1_detector.py \
  --path . --format json

# TimescaleDB analysis
python3 ~/.claude/skills/db-performance-optimizer-v3/scripts/timescale_analyzer.py \
  --db-url $DB_URL --format json

# Generate JSON report
python3 ~/.claude/skills/db-performance-optimizer-v3/scripts/json_report.py \
  --input analysis.json --output report.json --depth 5
```

## MCP Integration

```bash
# PostgreSQL docs lookup
mcp-cli call plugin_pg_pg-aiguide/semantic_search_postgres_docs '{
  "version": "17",
  "limit": 10,
  "prompt": "partial index optimization"
}'

# TimescaleDB docs lookup
mcp-cli call plugin_pg_pg-aiguide/semantic_search_tiger_docs '{
  "limit": 10,
  "prompt": "continuous aggregates refresh policy"
}'
```

## Output Format

### JSON API Response

```json
{
  "apiVersion": "v3",
  "metadata": {
    "generated": "2025-01-01T12:00:00Z",
    "depth": 7,
    "database": "mydb",
    "workersUsed": 17
  },
  "summary": {
    "healthScore": 75,
    "categories": {...},
    "metrics": {...}
  },
  "recommendations": {
    "p1_critical": [...],
    "p2_high": [...],
    "p3_medium": [...]
  },
  "implementation": {...},
  "timescale": {...},
  "aiInsights": {...}
}
```

## Examples

```bash
# Quick health check with JSON output
/db-optimize-v3 --quick --output json

# Full optimization with MCP docs
/db-optimize-v3 --full --with-docs --db-url postgresql://user:pass@localhost/mydb

# TimescaleDB-focused analysis
/db-optimize-v3 --mode timescale --depth 5 --db-url postgresql://...

# N+1 detection only
/db-optimize-v3 --mode n1 --output json

# Level 7 enterprise analysis
/db-optimize-v3 --depth 7 --with-docs --output json
```
