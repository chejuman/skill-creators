# Parallel Execution Rules

Critical rules for true parallel agent execution in Claude Code.

## The Golden Rule

**All worker Task calls MUST be in ONE message for parallel execution.**

```python
# CORRECT - True parallel (single message)
Task(subagent_type='general-purpose', prompt='Worker 1...', model='haiku')
Task(subagent_type='general-purpose', prompt='Worker 2...', model='haiku')
Task(subagent_type='general-purpose', prompt='Worker 3...', model='haiku')

# INCORRECT - Sequential (multiple messages)
message1: Task(worker1)
message2: Task(worker2)  # Waits for message1
message3: Task(worker3)  # Waits for message2
```

## Execution Order

```
1. Planning Agent    ──► Sequential (must complete first)
2. Worker Agents     ──► PARALLEL (same message)
3. Analysis Agent    ──► Sequential (waits for workers)
4. Synthesis Agent   ──► Sequential
5. Visualization     ──► Sequential (optional)
```

## Task Tool Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| subagent_type | string | Agent type (Plan, Explore, general-purpose) |
| prompt | string | Task instructions |
| description | string | Short task description |
| model | string | haiku, sonnet, opus |
| run_in_background | bool | Run async (use TaskOutput to get result) |

## Parallel Execution Pattern

```python
# In SKILL.md, instruct Claude:

### Step 2: Parallel Worker Execution

Spawn ALL workers in a SINGLE message with multiple Task calls:

Task(
  subagent_type='general-purpose',
  prompt='Worker 1: Security analysis of authentication code...',
  description='Security worker',
  model='haiku'
)
Task(
  subagent_type='general-purpose',
  prompt='Worker 2: Performance analysis of database queries...',
  description='Performance worker',
  model='haiku'
)
Task(
  subagent_type='general-purpose',
  prompt='Worker 3: Code style and convention check...',
  description='Style worker',
  model='haiku'
)
```

## Background Execution

For long-running workers:

```python
Task(
  subagent_type='general-purpose',
  prompt='Long-running analysis...',
  run_in_background=True
)

# Later, get results:
TaskOutput(task_id='...', block=True)
```

## Model Selection for Speed

| Model | Latency | Use Case |
|-------|---------|----------|
| haiku | Fast | Workers, visualization |
| sonnet | Medium | Analysis, synthesis |
| opus | Slow | Complex reasoning |

## Common Mistakes

### Mistake 1: Sequential Worker Calls
```python
# BAD - Each call waits for previous
for worker in workers:
    Task(prompt=worker.prompt)
```

### Mistake 2: Dependencies in Parallel
```python
# BAD - Worker 2 depends on Worker 1
Task(prompt='Get data...')  # Worker 1
Task(prompt='Analyze Worker 1 results...')  # Worker 2 - will fail
```

### Mistake 3: Too Many Parallel Agents
```python
# BAD - Context limits, diminishing returns
Task(worker1), Task(worker2), ..., Task(worker20)
```

**Recommended:** 3-5 parallel workers per phase.

## Quality Assurance

After parallel execution, verify:

```python
def verify_parallel_results(results):
    # Check all workers returned
    assert len(results) == expected_workers

    # Check minimum findings
    total_findings = sum(len(r.findings) for r in results)
    assert total_findings >= min_findings_for_level

    # Check for gaps
    gaps = [r.gaps for r in results]
    if significant_gaps(gaps):
        spawn_additional_workers()
```
