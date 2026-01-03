---
description: Quick code lookup mode - fast answers with minimal workers (TYPE_A)
allowed-tools: Bash, Read, Grep
model: sonnet
---

# Quick Lookup Mode

You are now in QUICK mode for fast open source research.

## Configuration

- **Workers**: 3 (minimal)
- **Focus**: Documentation + single code reference
- **Output**: Concise bilingual summary

## Execution Protocol

1. **Single Code Search**

   ```bash
   mcp-cli call gitmvp/search_code_in_repo '{"owner":"$1","repo":"$2","query":"$ARGUMENTS"}'
   ```

2. **Quick Doc Lookup**

   ```bash
   mcp-cli call plugin_context7_context7/query-docs '{"libraryId":"/$1/$2","query":"$ARGUMENTS","tokens":2000}'
   ```

3. **Fast Response**
   - 1-2 sentence English summary
   - 1-2 문장 한국어 요약
   - Single permalink evidence

## Output Format

````markdown
## Quick Answer (빠른 답변)

**EN**: [Concise answer]
**KO**: [간결한 답변]

**Evidence**: [Single permalink]

```[lang]
[Key code - max 10 lines]
```
````

```

## When to Use

- Simple "how to" questions
- Quick API lookups
- Single function/class queries
- Time-sensitive requests

## Constraints

- Skip git history research
- Single repository focus
- No comprehensive validation
- Fast over thorough
```
