# 📚 {{QUERY_TITLE}}

## TL;DR (요약)

{{ENGLISH_SUMMARY}}

{{KOREAN_SUMMARY}}

## Request Classification

| Field          | Value            |
| -------------- | ---------------- |
| **Type**       | {{REQUEST_TYPE}} |
| **Libraries**  | {{LIBRARIES}}    |
| **Complexity** | {{COMPLEXITY}}   |

## Detailed Findings (상세 발견)

### Finding 1: {{FINDING_1_TITLE}}

{{FINDING_1_CLAIM}}

📍 **Evidence**: {{FINDING_1_PERMALINK}}

```{{FINDING_1_LANGUAGE}}
{{FINDING_1_CODE}}
```

💡 **Context**: {{FINDING_1_CONTEXT}}

---

### Finding 2: {{FINDING_2_TITLE}}

{{FINDING_2_CLAIM}}

📍 **Evidence**: {{FINDING_2_PERMALINK}}

```{{FINDING_2_LANGUAGE}}
{{FINDING_2_CODE}}
```

💡 **Context**: {{FINDING_2_CONTEXT}}

---

## Historical Context (역사적 맥락)

{{#IF_HAS_HISTORY}}

### Timeline

{{HISTORY_TIMELINE}}

### Key Decisions

{{HISTORY_DECISIONS}}

{{/IF_HAS_HISTORY}}

## Official Documentation (공식 문서)

{{#IF_HAS_DOCS}}

**Source**: {{DOCS_SOURCE}}

{{DOCS_SUMMARY}}

{{/IF_HAS_DOCS}}

## Sources (출처)

| Type | Link | Relevance |
| ---- | ---- | --------- |

{{#SOURCES}}
| {{SOURCE_TYPE}} | {{SOURCE_LINK}} | {{SOURCE_RELEVANCE}} |
{{/SOURCES}}

---

_Research completed: {{TIMESTAMP}}_
_Classification: {{REQUEST_TYPE}}_
_Agents used: {{AGENTS_USED}}_
