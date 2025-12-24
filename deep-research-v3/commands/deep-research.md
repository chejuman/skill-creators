---
allowed-tools: WebSearch, WebFetch, Task, Read, Write
argument-hint: [query] [--depth 1-5] [--summary brief|standard|detailed]
description: Run deep research on a topic with multi-agent analysis
---

# Deep Research Command

Run comprehensive research using the deep-research-v3 skill.

## Arguments

- `$1`: Research query (required)
- `$2`: Depth level (optional, default: 4)
  - `--depth 1-2`: Quick research, 2 agents
  - `--depth 3`: Standard research, 3 agents
  - `--depth 4-5`: Deep analysis, 5+ agents
- `$3`: Summary level (optional, default: detailed)
  - `--summary brief`: Executive summary only
  - `--summary standard`: Key findings + summary
  - `--summary detailed`: Full report

## Examples

```
/deep-research "AI 코딩 어시스턴트 시장 분석"
/deep-research "SaaS pricing strategies" --depth 5
/deep-research "competitor analysis Cursor vs Claude Code" --summary brief
```

## Execution

Invoke the deep-research-v3 skill with:

- Query: $ARGUMENTS
- Depth: Parse --depth flag or use default 4
- Summary: Parse --summary flag or use default detailed

## Output

- Markdown report saved to current directory
- HTML report (if detailed level)
- Source citations with credibility scores
- Follow-up research questions

## Context

Current date for search relevance: !`date +%Y-%m-%d`
