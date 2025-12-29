---
allowed-tools:
  [Read, Bash(python3:*, psql:*), Grep, Glob, Task, TaskOutput, AskUserQuestion]
description: Premium database optimization command with hierarchical multi-agent architecture. Supports PostgreSQL/SQLAlchemy expert-level analysis including partial indexes, vacuuming, partitioning, N+1 detection, and lock contention monitoring.
---

## Context

- Python files: !`find . -name "*.py" -type f | head -10`
- SQLAlchemy models: !`grep -r "class.*Model\|relationship\|Column" --include="*.py" -l 2>/dev/null | head -5`
- Database config: !`grep -r "DATABASE_URL\|postgresql\|create_engine" --include="*.py" -l 2>/dev/null | head -3`

## Arguments

Parse from $ARGUMENTS:

| Argument   | Description             | Default |
| ---------- | ----------------------- | ------- |
| `--mode`   | Operation mode          | full    |
| `--depth`  | Analysis depth 1-5      | 3       |
| `--db-url` | Database URL            | (env)   |
| `--output` | Output file             | stdout  |
| `--quick`  | Quick scan (depth 1)    | false   |
| `--full`   | Full analysis (depth 5) | false   |

### Mode Options

- `profile`: Database metrics profiling
- `indexes`: Index recommendations
- `n1`: N+1 query detection
- `vacuum`: Vacuum and bloat analysis
- `locks`: Lock contention monitoring
- `partition`: Partition recommendations
- `connections`: Connection pool analysis
- `explain`: Query plan analysis
- `full`: Complete optimization (all modes)

## Execution Protocol

### Step 1: Determine Depth Level

```python
if "--quick" in args:
    depth = 1
    workers = 4
elif "--full" in args:
    depth = 5
    workers = 12
else:
    depth = parse_depth(args)  # 1-5
    workers = 4 + (depth * 2)  # 4, 6, 8, 10, 12
```

### Step 2: Phase 1 - PROFILE

Launch parallel profiling agents:

```
# Worker 1: Query Profiler (all depths)
Task(
  subagent_type='general-purpose',
  description='Profile queries',
  prompt='Profile PostgreSQL queries. Get top slow queries, cache ratio, seq scans.',
  model='haiku',
  run_in_background=true
)

# Worker 2: Index Analyzer (depth >= 2)
Task(
  subagent_type='general-purpose',
  description='Analyze indexes',
  prompt='Find unused indexes, duplicates, missing indexes.',
  model='haiku',
  run_in_background=true
)

# Worker 3: Table Stats (depth >= 3)
Task(
  subagent_type='general-purpose',
  description='Collect table stats',
  prompt='Get table sizes, dead tuple ratios, partition candidates.',
  model='haiku',
  run_in_background=true
)
```

Wait for all PROFILE workers:

```
query_result = TaskOutput(task_id=worker1, block=true)
index_result = TaskOutput(task_id=worker2, block=true)
table_result = TaskOutput(task_id=worker3, block=true)

phase1_output = merge_results([query_result, index_result, table_result])
```

### Step 3: Phase 2 - ANALYZE (depth >= 3)

Launch expert category agents:

```
# PostgreSQL Engine Expert
Task(
  subagent_type='general-purpose',
  description='PostgreSQL engine analysis',
  prompt='''Analyze PostgreSQL engine opportunities:
  - Partial Index candidates
  - Covering Index opportunities
  - GIN Index for JSONB/FTS
  - Vacuum issues
  - Partition recommendations
  Profile Data: {phase1_output}
  ''',
  model='sonnet',
  run_in_background=true
)

# SQLAlchemy ORM Expert
Task(
  subagent_type='Explore',
  description='SQLAlchemy analysis',
  prompt='''Analyze SQLAlchemy patterns:
  - N+1 query detection
  - Bulk operation opportunities
  - Session management issues
  - Hybrid attribute candidates
  Search *.py files.
  ''',
  model='sonnet',
  run_in_background=true
)

# Query Execution Expert (depth >= 4)
Task(
  subagent_type='general-purpose',
  description='Query execution analysis',
  prompt='''Analyze query execution:
  - EXPLAIN ANALYZE issues
  - Cost optimization
  - CTE materialization
  - Lock contention patterns
  ''',
  model='sonnet',
  run_in_background=true
)

# Architecture Expert (depth >= 5)
Task(
  subagent_type='general-purpose',
  description='Architecture analysis',
  prompt='''Analyze architecture:
  - Connection pooling
  - Read replica candidates
  - Denormalization opportunities
  - Cloud-native scaling options
  ''',
  model='sonnet',
  run_in_background=true
)
```

### Step 4: Phase 3 - OPTIMIZE

Generate prioritized recommendations:

```
Task(
  subagent_type='general-purpose',
  description='Generate recommendations',
  prompt='''Generate prioritized recommendations:

  Analysis: {phase2_output}

  For each issue:
  1. CREATE/DROP/ALTER statement
  2. Priority (P1/P2/P3)
  3. Estimated improvement
  4. Risk level
  5. Implementation notes

  Return JSON format.
  ''',
  model='sonnet'
)
```

### Step 5: Phase 4 - DELIVER

Synthesize final report:

```
Task(
  subagent_type='general-purpose',
  description='Synthesize report',
  prompt='''Create final report:

  All Analysis: {all_phase_outputs}

  Include:
  1. Executive summary
  2. Metrics comparison (before/after)
  3. Priority action list
  4. Detailed findings by category
  5. Implementation scripts
  6. Monitoring recommendations

  Format as markdown using template.
  ''',
  model='sonnet'
)
```

## Script Execution

### Run Analysis Scripts

```bash
# Vacuum analysis
python3 ~/.claude/skills/db-performance-optimizer-v2/scripts/vacuum_analyzer.py \
  --db-url $DB_URL --threshold 10

# Partition recommendations
python3 ~/.claude/skills/db-performance-optimizer-v2/scripts/partition_advisor.py \
  --db-url $DB_URL --min-size 1GB

# Lock monitoring
python3 ~/.claude/skills/db-performance-optimizer-v2/scripts/lock_monitor.py \
  --db-url $DB_URL

# Connection analysis
python3 ~/.claude/skills/db-performance-optimizer-v2/scripts/connection_analyzer.py \
  --db-url $DB_URL

# N+1 detection (code analysis)
python3 ~/.claude/skills/db-performance-optimizer-v2/scripts/n1_detector.py \
  --path . --format markdown

# Index recommendations
python3 ~/.claude/skills/db-performance-optimizer-v2/scripts/index_advisor.py \
  --db-url $DB_URL --limit 20

# Query profiling
python3 ~/.claude/skills/db-performance-optimizer-v2/scripts/query_profiler.py \
  --db-url $DB_URL --top 20
```

## Output Format

````markdown
# Database Optimization Report V2

**Generated:** {timestamp}
**Mode:** {mode}
**Depth:** {depth}/5
**Database:** {db_name}

## Executive Summary

| Metric           | Current | Projected | Improvement |
| ---------------- | ------- | --------- | ----------- |
| Avg Query Time   | {curr}  | {proj}    | {impr}      |
| Cache Hit Ratio  | {curr}  | {proj}    | {impr}      |
| N+1 Queries      | {curr}  | {proj}    | {impr}      |
| Index Coverage   | {curr}  | {proj}    | {impr}      |
| Dead Tuple Ratio | {curr}  | {proj}    | {impr}      |

## Priority Actions

### P1: Critical (Do Now)

[List with SQL/Python code]

### P2: High (This Sprint)

[List with SQL/Python code]

### P3: Medium (Backlog)

[List]

## Detailed Analysis

### 1. PostgreSQL Engine

[Indexes, Vacuum, Partitioning]

### 2. SQLAlchemy ORM

[N+1, Bulk ops, Session]

### 3. Query Execution

[EXPLAIN, CTE, Locks]

### 4. Architecture

[Pooling, Replicas, Denorm]

## Implementation Scripts

```sql
-- Index changes
{index_scripts}

-- Vacuum commands
{vacuum_scripts}

-- Configuration
{config_scripts}
```
````

## Monitoring Setup

[pg_stat_statements, logging, alerts]

````

## Examples

```bash
# Quick health check
/db-optimize-v2 --quick

# Full optimization analysis
/db-optimize-v2 --full --db-url postgresql://user:pass@localhost/mydb

# Specific mode
/db-optimize-v2 --mode vacuum --db-url postgresql://...

# N+1 detection only
/db-optimize-v2 --mode n1

# Deep analysis with output file
/db-optimize-v2 --depth 5 --output report.md --db-url postgresql://...

# Index recommendations
/db-optimize-v2 --mode indexes --db-url postgresql://...

# Lock monitoring
/db-optimize-v2 --mode locks --db-url postgresql://...
````
