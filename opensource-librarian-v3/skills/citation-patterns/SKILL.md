---
name: citation-patterns
description: Standards for evidence citation and bilingual output. Use when formatting research findings, creating permalinks, or generating bilingual (EN/KR) responses. Includes JSON API v3 schema.
---

# Citation Patterns Skill

Standards for evidence-based citations and bilingual output.

## Permalink Format (MANDATORY)

Every claim requires SHA-based permalink:

```
https://github.com/{owner}/{repo}/blob/{SHA}/{path}#L{start}-L{end}
```

### Valid Examples

```
https://github.com/fastapi/fastapi/blob/abc123def/fastapi/routing.py#L45-L67
https://github.com/facebook/react/blob/def456abc/packages/react/src/React.js#L1-L25
```

### Invalid Examples

```
https://github.com/fastapi/fastapi/blob/main/fastapi/routing.py  # No SHA
https://github.com/fastapi/fastapi/blob/abc123def/fastapi/routing.py  # No line numbers
```

## Bilingual Output Template

````markdown
# [Query Title]

## TL;DR (요약)

**English**: [2-3 sentence summary with key insight]

**한국어**: [핵심 통찰을 포함한 2-3문장 요약]

## Detailed Findings (상세 발견)

### Finding 1: [Topic]

**English Claim**: [Statement]
**한국어 주장**: [진술]

**Evidence (증거)**:
[GitHub Permalink]

```[lang]
[Code snippet - max 20 lines]
```
````

**Context (맥락)**: [Why this proves the claim]
**맥락 설명**: [이 코드가 주장을 증명하는 이유]

**Confidence**: [0.0-1.0]

## Sources (출처)

| Type | Link | Title | Relevance |
| ---- | ---- | ----- | --------- |

````

## JSON API v3 Schema

```json
{
  "apiVersion": "v3",
  "metadata": {
    "generated": "ISO8601",
    "query": "original query",
    "classification": "TYPE_A|B|C|D",
    "workersUsed": 15,
    "validationPassed": true
  },
  "summary": {
    "en": "English summary (max 500)",
    "ko": "한국어 요약 (max 500)"
  },
  "findings": [
    {
      "id": "F001",
      "claim": {"en": "...", "ko": "..."},
      "evidence": {
        "permalink": "https://github.com/...",
        "sha": "abc123...",
        "repository": "owner/repo",
        "path": "file.py",
        "lines": {"start": 10, "end": 20}
      },
      "snippet": "code...",
      "confidence": 0.95,
      "validated": true
    }
  ],
  "history": {
    "timeline": [],
    "keyDecisions": [],
    "contributors": []
  },
  "sources": [],
  "validation": {
    "passed": true,
    "issues": [],
    "qualityScore": 0.95
  }
}
````

## Confidence Scoring

| Score   | Meaning                               |
| ------- | ------------------------------------- |
| 0.9-1.0 | Direct evidence with exact match      |
| 0.7-0.9 | Strong evidence with clear connection |
| 0.5-0.7 | Moderate evidence, some inference     |
| <0.5    | Weak evidence, mark as [unverified]   |

## Quality Checklist

Before delivery:

- [ ] Every claim has SHA permalink
- [ ] Line numbers included
- [ ] Bilingual summary present
- [ ] Confidence scores assigned
- [ ] Sources table complete
