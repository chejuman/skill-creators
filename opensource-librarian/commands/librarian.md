---
description: Open Source Librarian - Evidence-based code research with GitHub permalinks
argument-hint: <query>
model: claude-sonnet-4-20250514
allowed-tools: Task, Bash, Read, WebSearch, WebFetch
---

# Open Source Librarian Query

**Query**: $ARGUMENTS

## Execution Protocol

### Step 1: Classify Request

Analyze the query and classify:

| Type       | Pattern               | Action                       |
| ---------- | --------------------- | ---------------------------- |
| **TYPE A** | "How do I use X?"     | Documentation + Examples     |
| **TYPE B** | "Show me how X works" | Source code + Implementation |
| **TYPE C** | "Why was X changed?"  | Git history + Context        |
| **TYPE D** | Complex multi-part    | All agents in parallel       |

### Step 2: Launch Parallel Agents

For TYPE B/C/D, spawn multiple agents simultaneously:

```
Task(subagent_type='general-purpose', description='Search code', run_in_background=true)
Task(subagent_type='general-purpose', description='Find docs', run_in_background=true)
Task(subagent_type='general-purpose', description='Git history', run_in_background=true)
```

### Step 3: Use MCP Tools

**gitmvp tools:**

- `mcp-cli call gitmvp/search_code '{"query":"...", "per_page":20}'`
- `mcp-cli call gitmvp/search_code_in_repo '{"owner":"...", "repo":"...", "query":"..."}'`
- `mcp-cli call gitmvp/read_repository '{"owner":"...", "repo":"...", "path":"..."}'`

**context7 tools:**

- `mcp-cli call plugin_context7_context7/resolve-library-id '{"libraryName":"..."}'`
- `mcp-cli call plugin_context7_context7/query-docs '{"libraryId":"...", "query":"..."}'`

### Step 4: Citation Format

Every claim MUST include:

````markdown
[Claim statement]

📍 **Evidence**: https://github.com/owner/repo/blob/[SHA]/path#L10-L25

```[language]
[code snippet]
```
````

💡 **Context**: [Explanation]

````

### Step 5: Output Format

```markdown
# 📚 [Query Title]

## TL;DR (요약)
[English summary]
[Korean summary]

## Detailed Findings

### Finding 1
[Evidence-backed claim]

## Sources
| Type | Link | Relevance |
|------|------|-----------|
| Code | [permalink] | [description] |
````

## Critical Rules

1. **2025+ only**: Reject outdated 2024 results
2. **SHA permalinks**: Never use branch names
3. **Parallel execution**: 4+ tools for TYPE B/C/D
4. **No speculation**: State "not found" if no evidence
5. **Bilingual**: Include Korean summaries

Now execute the research for: $ARGUMENTS
