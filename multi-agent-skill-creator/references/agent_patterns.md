# Multi-Agent Patterns

Proven patterns from deep-researcher-v2 and devsecops-engineer-v2.

## Pattern 1: Hierarchical Orchestration

```
Orchestrator (SKILL.md)
    ├─► Planning Agent (sequential)
    ├─► Worker Agents (parallel)
    ├─► Analysis Agent (sequential)
    ├─► Synthesis Agent (sequential)
    └─► Visualization Agent (optional)
```

**Key principles:**
- Planning runs FIRST to decompose the task
- Workers run in PARALLEL for speed
- Analysis waits for ALL workers
- Synthesis produces final output

## Pattern 2: Agent Type Selection

| Phase | subagent_type | Model | Purpose |
|-------|---------------|-------|---------|
| Planning | Plan | sonnet | Scope analysis |
| Research | Explore | haiku | Fast web search |
| Execution | general-purpose | haiku | Domain tasks |
| Analysis | general-purpose | sonnet | Complex reasoning |
| Synthesis | general-purpose | sonnet | Report writing |

## Pattern 3: Depth Level Scaling

Scale agent count and thoroughness by level:

```python
LEVEL_CONFIG = {
    1: {"workers": 1, "sources": 3,  "analysis": "inline"},
    2: {"workers": 2, "sources": 5,  "analysis": "1 agent"},
    3: {"workers": 3, "sources": 10, "analysis": "1 agent"},
    4: {"workers": 4, "sources": 15, "analysis": "1 agent"},
    5: {"workers": 5, "sources": 25, "analysis": "1 agent"},
}
```

## Pattern 4: JSON Communication

All agents use structured JSON for data exchange:

```json
{
  "agent_id": "worker-1",
  "status": "complete",
  "findings": [...],
  "metadata": {
    "timestamp": "...",
    "duration_ms": 1234
  }
}
```

## Pattern 5: Quality Metrics

Track quality per level:

| Level | Min Findings | High-Priority | Coverage |
|-------|-------------|---------------|----------|
| 1 | 3 | 1 | 40% |
| 2 | 5 | 2 | 60% |
| 3 | 10 | 3 | 80% |
| 4 | 15 | 5 | 90% |
| 5 | 25 | 8 | 100% |

## Pattern 6: Report Generation

Two-phase output:
1. **Synthesis Agent** → Markdown report
2. **Visualization Agent** → HTML with styling

```bash
# Convert markdown to HTML
python3 scripts/md_to_html.py report.md -o report.html
```

## Pattern 7: Self-Upgrade Loop

After execution, capture learnings:

```python
def self_upgrade(findings):
    # Extract new patterns
    # Update knowledge base
    # Enhance prompts
    pass
```

## Anti-Patterns to Avoid

1. **Sequential worker execution** - Always parallel
2. **Nested subagents** - Subagents cannot spawn subagents
3. **Missing quality checks** - Verify minimum findings
4. **Unbounded context** - Use progressive disclosure
