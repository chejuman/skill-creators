---
name: opensource-librarian-v2
description: Premium Level 7 hierarchical multi-agent open source code research system with 15+ parallel workers. Features gitmvp and context7 MCP integration, SHA-based GitHub permalinks, AI synthesis, Git history archaeology, and JSON API v2 output. Triggers on "opensource librarian", "find code implementation", "show me the source", "how does X work in repo", "why was this changed", "code evidence", "GitHub permalink", "오픈소스 라이브러리언".
---

# Open Source Librarian V2

Premium Level 7 multi-agent system for evidence-based open source code research.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRINCIPAL ORCHESTRATOR (Level 7)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Phase 1: CLASSIFY ──► Request type detection (A/B/C/D)                      │
│                                                                             │
│ Phase 2: DISPATCH (15+ parallel workers)                                    │
│   ├── Code Hunter Agents (3-5) ──► gitmvp MCP code search                  │
│   ├── Documentation Agents (2) ──► context7 MCP docs                       │
│   ├── Git History Agents (3-5) ──► gh CLI archaeology                      │
│   ├── Validation Agents (2) ──► Evidence verification                      │
│   └── Web Research Agents (2) ──► Latest documentation                     │
│                                                                             │
│ Phase 3: SYNCHRONIZE ──► Collect all worker results                         │
│                                                                             │
│ Phase 4: SYNTHESIZE ──► AI Synthesis Agent (bilingual EN/KR)               │
│                                                                             │
│ Phase 5: DELIVER ──► JSON API v2 Generator                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```
User: "How does FastAPI handle dependency injection?"

Librarian V2:
1. Classifies as TYPE B (Implementation) → 8 workers
2. Dispatches workers IN PARALLEL (run_in_background=true)
3. Synthesizes findings with AI
4. Returns JSON API v2 response with GitHub permalinks
```

## Request Classification

**ALWAYS classify before dispatching:**

| Type       | Pattern               | Workers | Description            |
| ---------- | --------------------- | ------- | ---------------------- |
| **TYPE A** | "How do I use X?"     | 5       | Conceptual/usage       |
| **TYPE B** | "Show me how X works" | 8       | Implementation details |
| **TYPE C** | "Why was X changed?"  | 10      | Historical context     |
| **TYPE D** | Complex multi-part    | 15+     | Comprehensive research |

## Execution Protocol

### Phase 1: Classification

```
Task(
  subagent_type='general-purpose',
  prompt='Classify this query: ' + user_query + '\n\nReturn: TYPE A/B/C/D with reason',
  description='Classify request type',
  model='haiku'
)
```

### Phase 2: Parallel Worker Dispatch

Launch ALL workers simultaneously with `run_in_background=true`:

```
# Code Hunter Workers (parallel)
Task(subagent_type='general-purpose', prompt=CODE_HUNTER_PROMPT, model='sonnet', run_in_background=true)
Task(subagent_type='general-purpose', prompt=CODE_HUNTER_PROMPT_2, model='sonnet', run_in_background=true)

# Git History Workers (parallel)
Task(subagent_type='general-purpose', prompt=GIT_HISTORY_PROMPT, model='haiku', run_in_background=true)

# Documentation Workers (parallel)
Task(subagent_type='general-purpose', prompt=DOCUMENTATION_PROMPT, model='haiku', run_in_background=true)
```

### Phase 3: Synchronization

```
# Wait for all workers
results = []
for agent_id in dispatched_agents:
    result = TaskOutput(task_id=agent_id, block=true)
    results.append(result)
```

### Phase 4: AI Synthesis

```
Task(
  subagent_type='general-purpose',
  prompt=AI_SYNTHESIS_PROMPT + '\n\nFindings:\n' + json.dumps(results),
  description='Synthesize findings',
  model='sonnet'
)
```

### Phase 5: JSON API Output

```
Task(
  subagent_type='general-purpose',
  prompt=JSON_API_PROMPT + '\n\nSynthesis:\n' + synthesis_result,
  description='Generate JSON API v2',
  model='sonnet'
)
```

## MCP Integration

### gitmvp Tools

| Tool                  | Purpose           | Usage                                                    |
| --------------------- | ----------------- | -------------------------------------------------------- |
| `search_repositories` | Find repos        | `{"query":"react","sort":"stars"}`                       |
| `search_code`         | Global search     | `{"query":"useEffect"}`                                  |
| `search_code_in_repo` | Repo search       | `{"owner":"facebook","repo":"react","query":"useState"}` |
| `get_file_tree`       | Explore structure | `{"owner":"fastapi","repo":"fastapi"}`                   |
| `read_repository`     | Read files        | `{"owner":"...","repo":"...","path":"src/main.py"}`      |

### context7 Tools

| Tool                 | Purpose        | Usage                                                |
| -------------------- | -------------- | ---------------------------------------------------- |
| `resolve-library-id` | Get library ID | `{"libraryName":"fastapi"}`                          |
| `query-docs`         | Fetch docs     | `{"libraryId":"/fastapi/fastapi","query":"routing"}` |

See [MCP Guide](references/mcp_guide.md) for complete usage.

## Permalink Format (MANDATORY)

Every claim requires SHA-based permalink:

```
https://github.com/{owner}/{repo}/blob/{SHA}/{path}#L{start}-L{end}
```

**Correct**: `https://github.com/fastapi/fastapi/blob/abc123/fastapi/routing.py#L45-L67`
**Wrong**: `https://github.com/fastapi/fastapi/blob/main/fastapi/routing.py` (no SHA)

## JSON API v2 Output

```json
{
  "apiVersion": "v2",
  "metadata": {
    "generated": "2025-01-02T10:30:00Z",
    "query": "How does FastAPI handle dependency injection?",
    "classification": "TYPE_B",
    "workersUsed": 8
  },
  "summary": {
    "en": "FastAPI uses Depends() for DI...",
    "ko": "FastAPI는 Depends()를 사용하여 DI를 구현합니다..."
  },
  "findings": [...],
  "history": {...},
  "sources": [...]
}
```

See [JSON Schema](assets/json_schema.json) for complete schema.

## Depth Levels

| Level | Workers | Use Case               |
| ----- | ------- | ---------------------- |
| 3     | 5       | Quick lookup           |
| 5     | 10      | Standard research      |
| 7     | 15+     | Comprehensive analysis |

## Critical Rules

1. **Date Awareness**: Current year is 2025+. Prioritize recent results
2. **SHA Permalinks**: Always use commit SHA, not branch names
3. **Parallel Execution**: Type B/C/D MUST use parallel workers
4. **Evidence Required**: No speculation without "[unverified]" qualifier
5. **Bilingual Output**: Include both English and Korean

## Error Handling

| Scenario       | Recovery                           |
| -------------- | ---------------------------------- |
| Repo not found | Try forks, report search terms     |
| Rate limited   | Report limit, suggest retry timing |
| No code found  | Broaden search, try synonyms       |
| Private repo   | Report access limitation           |

## Trigger Phrases

- "opensource librarian" / "오픈소스 라이브러리언"
- "find code implementation" / "코드 구현 찾아줘"
- "show me the source" / "소스 코드 보여줘"
- "how does X work" / "X가 어떻게 동작해"
- "why was this changed" / "왜 변경됐어"
- "code evidence" / "코드 증거"
- "GitHub permalink"
- "JSON API research"

## Resources

- [Agent Prompts](references/agent_prompts.md) - Optimized agent prompts
- [MCP Guide](references/mcp_guide.md) - MCP tool usage
- [JSON Schema](assets/json_schema.json) - API v2 schema
- [Output Template](assets/output_template.md) - Response format
