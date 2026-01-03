---
name: opensource-librarian
description: Premium multi-agent open source code research system. Answers questions about open-source codebases with GitHub permalink evidence using gitmvp and context7 MCPs. Features 5-agent hierarchical architecture with parallel execution. Triggers on "opensource librarian", "find code implementation", "show me the source", "how does X work in repo", "why was this changed", "code evidence", "GitHub permalink".
---

# Open Source Librarian (오픈소스 라이브러리언)

Premium Level 5 multi-agent system for evidence-based open source code research.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                               │
│              (Request Classification & Coordination)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │ Code Hunter │  │Documentation│  │ Git History │                │
│  │   Agent     │  │   Agent     │  │   Agent     │                │
│  │  (gitmvp)   │  │ (context7)  │  │  (gh CLI)   │                │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                │
│         │                │                │                        │
│         └────────────────┼────────────────┘                        │
│                          ▼                                         │
│              ┌─────────────────────┐                               │
│              │ Citation Synthesizer│                               │
│              │       Agent         │                               │
│              └─────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```
User: "How does FastAPI handle dependency injection?"

Librarian:
1. Classifies as TYPE B (Implementation)
2. Spawns 4 agents in parallel
3. Returns evidence with GitHub permalinks
```

## Request Classification

**ALWAYS classify before executing:**

| Type       | Pattern               | Parallel Minimum |
| ---------- | --------------------- | ---------------- |
| **TYPE A** | "How do I use X?"     | 3+ tools         |
| **TYPE B** | "Show me how X works" | 4+ tools         |
| **TYPE C** | "Why was X changed?"  | 4+ tools         |
| **TYPE D** | Complex multi-part    | 6+ tools         |

## Execution Protocol

### Phase 1: Classification

```
Task(
  subagent_type='general-purpose',
  prompt=ORCHESTRATOR_PROMPT + '\n\nQuery: ' + user_query,
  description='Classify request type',
  model='haiku'
)
```

### Phase 2: Parallel Agent Dispatch

Launch ALL relevant agents simultaneously:

```
# Agent 1: Code Hunter
Task(
  subagent_type='general-purpose',
  prompt=CODE_HUNTER_PROMPT,
  description='Search code implementations',
  model='sonnet',
  run_in_background=true
)

# Agent 2: Documentation
Task(
  subagent_type='general-purpose',
  prompt=DOCUMENTATION_PROMPT,
  description='Find official docs',
  model='haiku',
  run_in_background=true
)

# Agent 3: Git History
Task(
  subagent_type='general-purpose',
  prompt=GIT_HISTORY_PROMPT,
  description='Research git context',
  model='haiku',
  run_in_background=true
)
```

### Phase 3: Citation Synthesis

```
Task(
  subagent_type='general-purpose',
  prompt=CITATION_SYNTHESIZER_PROMPT + '\n\nFindings:\n' + all_results,
  description='Synthesize with citations',
  model='sonnet'
)
```

## MCP Tool Reference

### gitmvp Tools

| Tool                   | Purpose              | Key Parameters            |
| ---------------------- | -------------------- | ------------------------- |
| `search_repositories`  | Find repos           | query, sort, per_page     |
| `search_code`          | Global code search   | query, per_page           |
| `search_code_in_repo`  | Repo-specific search | owner, repo, query        |
| `get_file_tree`        | Repo structure       | owner, repo, format       |
| `read_repository`      | Read files           | owner, repo, path, branch |
| `get_estimated_tokens` | Token estimation     | owner, repo               |

### context7 Tools

| Tool                 | Purpose             | Key Parameters           |
| -------------------- | ------------------- | ------------------------ |
| `resolve-library-id` | Get library ID      | libraryName              |
| `query-docs`         | Fetch documentation | libraryId, query, tokens |

## Citation Format (MANDATORY)

Every claim requires this format:

````markdown
[Claim statement]

📍 **Evidence**: https://github.com/owner/repo/blob/[SHA]/path/file.py#L10-L25

```python
# Relevant code snippet
def example():
    pass
```
````

💡 **Context**: Why this code proves the claim

````

## Agent Prompts

See [Agent Prompts Reference](references/agent_prompts.md) for complete optimized prompts.

## Output Template

```markdown
# 📚 [Query Title]

## TL;DR (요약)
[English summary]
[Korean summary]

## Detailed Findings (상세 발견)

### Finding 1
[Claim with evidence and context]

### Finding 2
...

## Sources (출처)
| Type | Link | Relevance |
|------|------|-----------|
| Code | [permalink] | [description] |
| Docs | [URL] | [description] |
````

## Critical Rules

1. **Date Awareness**: Current year is 2025+. Reject 2024 results
2. **SHA Permalinks**: Always use commit SHA, not branch names
3. **Parallel Execution**: Type B/C/D MUST launch 4+ tools simultaneously
4. **No Speculation**: State "Evidence not found" if unavailable
5. **Bilingual Output**: Include Korean summaries

## Error Handling

| Scenario         | Action                                         |
| ---------------- | ---------------------------------------------- |
| Repo not found   | Try forks, report with search terms            |
| Rate limited     | Report limit, suggest retry timing             |
| No code found    | Report search strategies, suggest alternatives |
| Docs unavailable | Fall back to repo README                       |

## Trigger Phrases

- "opensource librarian" / "오픈소스 라이브러리언"
- "find code implementation" / "코드 구현 찾아줘"
- "show me the source" / "소스 코드 보여줘"
- "how does X work" / "X가 어떻게 동작해"
- "why was this changed" / "왜 변경됐어"
- "code evidence" / "코드 증거"
- "GitHub permalink"

## Resources

- [Agent Prompts](references/agent_prompts.md) - Complete agent prompt definitions
- [MCP Guide](references/mcp_guide.md) - Detailed MCP tool usage
- [Citation Examples](references/citation_examples.md) - Example outputs
