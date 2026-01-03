---
name: code-research
description: Provides guidance on open source code research methodology. Use when analyzing codebases, finding implementations, or understanding library internals. Covers request classification, parallel research patterns, and evidence synthesis.
---

# Code Research Skill

Expert methodology for evidence-based open source code research.

## Request Classification System

Before starting research, classify every request:

| Type       | Pattern               | Approach               | Min Workers |
| ---------- | --------------------- | ---------------------- | ----------- |
| **TYPE_A** | "How do I use X?"     | Docs + examples        | 3           |
| **TYPE_B** | "Show me how X works" | Code + implementation  | 5           |
| **TYPE_C** | "Why was X changed?"  | History + discussions  | 6           |
| **TYPE_D** | Complex multi-part    | Full parallel research | 10+         |

## Research Phases

### Phase 1: Scope Definition

1. Identify target library/repo
2. Determine specific question focus
3. Set evidence requirements

### Phase 2: Parallel Discovery

Launch multiple search strategies simultaneously:

- Code search (function, class, pattern)
- Documentation lookup
- Git history exploration
- Issue/PR research

### Phase 3: Evidence Collection

For each finding:

- SHA-based permalink
- Relevant code snippet (max 25 lines)
- Context explanation

### Phase 4: Synthesis

Combine findings into coherent answer:

- English summary
- Korean summary (한국어 요약)
- Source table

## Search Strategy Matrix

| Finding Type   | Primary Tool               | Fallback           |
| -------------- | -------------------------- | ------------------ |
| Implementation | gitmvp/search_code_in_repo | gitmvp/search_code |
| Documentation  | context7/query-docs        | WebSearch          |
| History        | gh search issues/prs       | gh api commits     |
| Structure      | gitmvp/get_file_tree       | gh api trees       |

## Quality Standards

### Permalink Requirements

```
VALID: https://github.com/owner/repo/blob/abc123def/path/file.py#L10-L20
INVALID: https://github.com/owner/repo/blob/main/path/file.py
```

### Evidence Hierarchy

1. Source code with SHA permalink (highest)
2. Official documentation
3. Merged PR discussions
4. Issue discussions
5. Community guides (lowest)

## Common Patterns

### Finding Function Implementation

```
1. Search: gitmvp/search_code_in_repo query="def function_name"
2. Read: gitmvp/read_repository path="found/file.py"
3. SHA: gh api repos/owner/repo/commits/HEAD --jq '.sha'
4. Build permalink with line numbers
```

### Tracing Feature History

```
1. Search PRs: gh search prs "[feature]" --repo owner/repo
2. Get PR details: gh pr view [number] --json
3. Find introducing commit
4. Build timeline
```
