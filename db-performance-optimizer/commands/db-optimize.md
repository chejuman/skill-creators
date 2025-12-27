---
allowed-tools:
  [Read, Bash(python3:*, psql:*), Grep, Glob, Task, TaskOutput, AskUserQuestion]
description: Database performance optimization command for SQLAlchemy/PostgreSQL. Analyzes queries, detects N+1 problems, recommends indexes.
---

## Context

- Python files: !`find . -name "*.py" -type f | head -10`
- SQLAlchemy models: !`grep -r "class.*Model\|relationship\|Column" --include="*.py" -l 2>/dev/null | head -5`
- Database config: !`grep -r "DATABASE_URL\|postgresql\|create_engine" --include="*.py" -l 2>/dev/null | head -3`

## Arguments

Parse from $ARGUMENTS:

- `--profile`: Run full database profiling
- `--fix-n1`: Detect and fix N+1 query patterns
- `--indexes`: Get index recommendations
- `--full`: Complete optimization report
- `--level N`: Depth level 1-5 (default: 3)
- `--db-url URL`: Database connection URL

## Execution Protocol

### Step 1: Determine Operation Mode

```python
if "--profile" in args:
    mode = "profile"
elif "--fix-n1" in args:
    mode = "n1_detection"
elif "--indexes" in args:
    mode = "index_advisor"
elif "--full" in args:
    mode = "full"
else:
    # Ask user
    AskUserQuestion(...)
```

### Step 2: Run Analysis (Parallel Agents)

#### For Profile Mode:

```
# Agent 1: Query Profiler
Task(
  subagent='Explore',
  description='Profile database queries',
  prompt='Run query profiler on database. Identify slow queries, cache hit ratio, connection stats.',
  run_in_background=true
)

# Agent 2: Schema Analyzer
Task(
  subagent='Explore',
  description='Analyze database schema',
  prompt='Analyze table structures, relationships, and current indexes.',
  run_in_background=true
)
```

#### For N+1 Detection:

```
# Run N+1 detector script
python3 ~/.claude/skills/db-performance-optimizer/scripts/n1_detector.py --path .

# Agent: Code Analyzer
Task(
  subagent='Explore',
  description='Find N+1 patterns',
  prompt='Search for lazy loading in loops, missing eager loading, query patterns in for loops.',
  run_in_background=true
)
```

#### For Index Advisor:

```
# If DB URL provided, run script
python3 ~/.claude/skills/db-performance-optimizer/scripts/index_advisor.py --db-url $DB_URL

# Otherwise analyze code for index opportunities
Task(
  subagent='Explore',
  description='Analyze index needs',
  prompt='Find queries with WHERE, ORDER BY, GROUP BY clauses that might need indexes.',
  run_in_background=true
)
```

### Step 3: Synthesize Results

Combine agent findings into actionable report:

```markdown
# Database Performance Report

## Executive Summary

[Key findings and top 3 recommendations]

## Query Analysis

| Query | Time (ms) | Calls | Issue | Fix |
| ----- | --------- | ----- | ----- | --- |
| ...   | ...       | ...   | ...   | ... |

## N+1 Issues Found

[List with file:line and recommended fix]

## Index Recommendations

[Prioritized list with CREATE INDEX statements]

## Configuration Suggestions

[PostgreSQL and SQLAlchemy settings]

## Code Examples

[Before/after code for top issues]
```

### Step 4: Generate Fixes

For each issue, provide:

1. Problem description
2. Current code (if applicable)
3. Fixed code
4. Expected improvement

## Output Format

```markdown
# Database Optimization Report

**Date:** [timestamp]
**Mode:** [profile|n1|indexes|full]
**Level:** [1-5]

## Quick Wins (Do Now)

1. [High-impact, low-effort fix]
2. [High-impact, low-effort fix]

## Critical Issues

### Issue 1: N+1 Query in user_list.py:45

**Current:**

\`\`\`python
users = session.query(User).all()
for user in users:
print(user.orders) # N+1!
\`\`\`

**Fixed:**

\`\`\`python
users = session.query(User).options(selectinload(User.orders)).all()
for user in users:
print(user.orders) # Single query
\`\`\`

**Impact:** 50x faster for 100 users

### Issue 2: Missing Index on orders.user_id

\`\`\`sql
CREATE INDEX idx_orders_user_id ON orders (user_id);
\`\`\`

**Impact:** Query time 2000ms → 20ms

## Performance Metrics

| Metric         | Before | After (Est.) |
| -------------- | ------ | ------------ |
| Avg Query Time | 150ms  | 15ms         |
| N+1 Queries    | 12     | 0            |
| Index Coverage | 60%    | 95%          |

## Next Steps

1. [ ] Apply critical fixes
2. [ ] Run benchmark
3. [ ] Monitor with pg_stat_statements
```

## Examples

```bash
# Quick N+1 detection
/db-optimize --fix-n1

# Full analysis with database connection
/db-optimize --full --db-url postgresql://user:pass@localhost/mydb

# Index recommendations only
/db-optimize --indexes

# Profile with depth level 5
/db-optimize --profile --level 5
```
