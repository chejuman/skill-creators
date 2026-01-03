# Output Template

Standard bilingual output format for Open Source Librarian V2.

---

# [Query Title]

## TL;DR (요약)

**English**: [2-3 sentence summary with key insight and primary evidence link]

**한국어**: [핵심 통찰과 주요 증거 링크를 포함한 2-3문장 요약]

---

## Detailed Findings (상세 발견)

### Finding 1: [Topic/Claim Title]

**English Claim**: [Clear statement of what was discovered]

**한국어 주장**: [발견된 내용의 명확한 진술]

**Evidence (증거)**:
[GitHub Permalink with SHA]

```[language]
[Relevant code snippet - max 20 lines]
```

**Context (맥락)**: [Why this code proves the claim]
**맥락 설명**: [이 코드가 주장을 증명하는 이유]

**Confidence**: [0.0-1.0] | **신뢰도**: [0.0-1.0]

---

### Finding 2: [Topic/Claim Title]

[Same structure as Finding 1]

---

## Historical Context (역사적 맥락)

_Only include if git history was researched (TYPE_C or TYPE_D)_

### Timeline (타임라인)

| Date       | Event           | Reference | Summary           |
| ---------- | --------------- | --------- | ----------------- |
| YYYY-MM-DD | Issue/PR/Commit | #N        | Brief description |

### Key Decisions (주요 결정)

1. **Decision**: [What was decided]
   - **Rationale**: [Why, from discussion]
   - **Evidence**: [Link to discussion/PR]

### Contributors (기여자)

| Name   | Role    | Contributions |
| ------ | ------- | ------------- |
| Author | Primary | N commits     |

---

## Sources (출처)

| Type  | Link            | Title        | Relevance      |
| ----- | --------------- | ------------ | -------------- |
| Code  | [SHA Permalink] | file.py      | [Why relevant] |
| Docs  | [URL]           | [Page title] | [Why relevant] |
| Issue | [URL]           | #N: Title    | [Why relevant] |
| PR    | [URL]           | #N: Title    | [Why relevant] |

---

## Research Metadata (연구 메타데이터)

- **Query**: [Original query]
- **Classification**: TYPE [A/B/C/D] - [Category]
- **Workers Used**: [N]
- **Execution Time**: [N]ms
- **Generated**: [ISO8601 timestamp]

---

_Research conducted by Open Source Librarian V2_
_Level 7 Multi-Agent Architecture_
