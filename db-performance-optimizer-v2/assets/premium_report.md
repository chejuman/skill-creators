# Database Optimization Report V2

**Generated:** {{timestamp}}
**Mode:** {{mode}}
**Depth Level:** {{depth}}/5
**Database:** {{database}}
**Workers Used:** {{workers}}

---

## Executive Summary

{{executive_summary}}

### Key Metrics

| Metric           | Current        | Projected      | Improvement    |
| ---------------- | -------------- | -------------- | -------------- |
| Avg Query Time   | {{curr_qtime}} | {{proj_qtime}} | {{impr_qtime}} |
| Cache Hit Ratio  | {{curr_cache}} | {{proj_cache}} | {{impr_cache}} |
| N+1 Queries      | {{curr_n1}}    | {{proj_n1}}    | {{impr_n1}}    |
| Index Coverage   | {{curr_idx}}   | {{proj_idx}}   | {{impr_idx}}   |
| Dead Tuple Ratio | {{curr_dead}}  | {{proj_dead}}  | {{impr_dead}}  |
| Connection Usage | {{curr_conn}}  | {{proj_conn}}  | {{impr_conn}}  |

### Overall Score

```
┌─────────────────────────────────────────────┐
│ Database Health Score: {{health_score}}/100 │
├─────────────────────────────────────────────┤
│ Indexing:     {{idx_bar}} {{idx_score}}/25  │
│ Query Perf:   {{qry_bar}} {{qry_score}}/25  │
│ Maintenance:  {{mnt_bar}} {{mnt_score}}/25  │
│ Architecture: {{arc_bar}} {{arc_score}}/25  │
└─────────────────────────────────────────────┘
```

---

## Priority Actions

### P1: Critical (Immediate Action Required)

{{#each p1_actions}}

#### {{@index}}. {{title}}

**Impact:** {{impact}}
**Effort:** {{effort}}

```sql
{{code}}
```

**Expected Result:** {{expected}}

---

{{/each}}

### P2: High Priority (This Sprint)

{{#each p2_actions}}

- **{{title}}**: {{description}}
  ```sql
  {{code}}
  ```
  {{/each}}

### P3: Medium Priority (Backlog)

{{#each p3_actions}}

- {{description}}
  {{/each}}

---

## Detailed Analysis

### 1. PostgreSQL Engine Optimization

#### Partial Index Opportunities

{{#each partial_indexes}}
| Table | Condition | Size Reduction | Priority |
| ----- | --------- | -------------- | -------- |
| {{table}} | {{condition}} | {{reduction}} | P{{priority}} |

```sql
{{create_statement}}
```

{{/each}}

#### Covering Index Opportunities

{{#each covering_indexes}}
| Table | Columns | Include | Benefit |
| ----- | ------- | ------- | ------- |
| {{table}} | {{columns}} | {{include}} | Index Only Scan |
{{/each}}

#### GIN Index Candidates

{{#each gin_indexes}}

- **{{table}}.{{column}}**: {{type}} - {{reason}}
  {{/each}}

#### Vacuum & Bloat Issues

| Table | Dead Tuples | Ratio | Last Vacuum | Action |
| ----- | ----------- | ----- | ----------- | ------ |

{{#each vacuum_issues}}
| {{table}} | {{dead_tuples}} | {{ratio}}% | {{last_vacuum}} | {{action}} |
{{/each}}

#### Partition Candidates

{{#each partition_candidates}}

- **{{table}}**: {{rows}} rows, {{size}}
  - Partition By: {{partition_type}} on `{{partition_key}}`
  - Interval: {{interval}}
    {{/each}}

---

### 2. SQLAlchemy ORM Optimization

#### N+1 Query Issues

{{#each n1_issues}}

##### {{file}}:{{line}}

**Severity:** {{severity}}

**Current Code:**

```python
{{current_code}}
```

**Fixed Code:**

```python
{{fixed_code}}
```

**Impact:** {{impact}}

---

{{/each}}

#### Bulk Operation Opportunities

{{#each bulk_ops}}
| File | Line | Current Pattern | Recommended | Speedup |
| ---- | ---- | --------------- | ----------- | ------- |
| {{file}} | {{line}} | {{current}} | {{recommended}} | {{speedup}} |
{{/each}}

#### Session Management Issues

{{#each session_issues}}

- **{{file}}:{{line}}**: {{issue}}
  - Fix: {{fix}}
    {{/each}}

---

### 3. Query Execution Optimization

#### EXPLAIN ANALYZE Issues

{{#each explain_issues}}

##### Query: {{query_snippet}}

| Metric         | Value             | Issue     |
| -------------- | ----------------- | --------- |
| Execution Time | {{exec_time}}     | {{issue}} |
| Rows Scanned   | {{rows_scanned}}  |           |
| Rows Returned  | {{rows_returned}} |           |

**Recommendation:** {{recommendation}}

---

{{/each}}

#### CTE Materialization Recommendations

{{#each cte_recommendations}}

- **{{query_name}}**: Change to `{{recommended}}` - {{reason}}
  {{/each}}

#### Lock Contention Patterns

{{#each lock_issues}}
| Table | Lock Type | Avg Wait | Recommendation |
| ----- | --------- | -------- | -------------- |
| {{table}} | {{lock_type}} | {{avg_wait}} | {{recommendation}} |
{{/each}}

---

### 4. Architecture Optimization

#### Connection Pool Settings

**Current Configuration:**

```python
{{current_pool_config}}
```

**Recommended Configuration:**

```python
{{recommended_pool_config}}
```

#### Read Replica Candidates

{{#each replica_candidates}}

- **{{query_pattern}}**: {{read_percent}}% reads - Route to replica
  {{/each}}

#### Denormalization Opportunities

{{#each denormalization}}
| Type | Name | Source Tables | Refresh Strategy |
| ---- | ---- | ------------- | ---------------- |
| {{type}} | {{name}} | {{sources}} | {{refresh}} |
{{/each}}

---

## Implementation Scripts

### Index Changes

```sql
-- Priority 1: Critical indexes
{{p1_index_sql}}

-- Priority 2: High priority indexes
{{p2_index_sql}}

-- Drop unused indexes
{{drop_index_sql}}
```

### Vacuum Commands

```sql
-- Immediate vacuum needs
{{vacuum_sql}}

-- Autovacuum tuning
{{autovacuum_sql}}
```

### PostgreSQL Configuration

```sql
-- postgresql.conf changes
{{postgresql_config}}
```

### SQLAlchemy Configuration

```python
{{sqlalchemy_config}}
```

---

## Monitoring Setup

### pg_stat_statements

```sql
-- Enable if not already
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Query for monitoring
{{monitoring_query}}
```

### Recommended Alerts

| Metric            | Threshold | Action              |
| ----------------- | --------- | ------------------- |
| Query time > 1s   | Warning   | Review slow queries |
| Cache hit < 90%   | Critical  | Check memory config |
| Dead tuples > 20% | Warning   | Run vacuum          |
| Connections > 80% | Critical  | Scale pool          |

---

## Next Steps

1. [ ] Apply P1 critical fixes
2. [ ] Run `ANALYZE` on affected tables
3. [ ] Verify improvements with benchmark
4. [ ] Schedule P2 fixes for next sprint
5. [ ] Set up monitoring alerts
6. [ ] Review in 1 week

---

_Generated by db-performance-optimizer-v2_
_Premium hierarchical multi-agent analysis_
