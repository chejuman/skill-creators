# Research Report: {{QUERY}}

**Generated:** {{DATE}}
**Sources Analyzed:** {{SOURCE_COUNT}}
**Research Depth:** {{DEPTH_LEVELS}} levels
**Total Insights:** {{INSIGHT_COUNT}}

---

## Executive Summary

{{EXECUTIVE_SUMMARY}}

---

## Key Findings (Relevance >= 0.8)

{{#KEY_FINDINGS}}
### {{INDEX}}. {{FINDING_TITLE}}

{{FINDING_CONTENT}}

> **Relevance:** {{RELEVANCE_SCORE}} | **Source:** [{{SOURCE_TITLE}}]({{SOURCE_URL}})

{{/KEY_FINDINGS}}

---

## Supporting Information (0.5 <= Relevance < 0.8)

{{#SUPPORTING_INFO}}
- **{{FINDING_TITLE}}** ({{RELEVANCE_SCORE}})
  {{FINDING_CONTENT}}
  > Source: [{{SOURCE_TITLE}}]({{SOURCE_URL}})

{{/SUPPORTING_INFO}}

---

## Supplementary Context (Relevance < 0.5)

{{#SUPPLEMENTARY}}
- {{FINDING_CONTENT}} — [{{SOURCE_TITLE}}]({{SOURCE_URL}})
{{/SUPPLEMENTARY}}

---

## Contradictions & Conflicts

{{#CONTRADICTIONS}}
### {{TOPIC}}

**Source A says:** {{SOURCE_A_CLAIM}}
> [{{SOURCE_A_TITLE}}]({{SOURCE_A_URL}})

**Source B says:** {{SOURCE_B_CLAIM}}
> [{{SOURCE_B_TITLE}}]({{SOURCE_B_URL}})

**Resolution/Note:** {{RESOLUTION}}

{{/CONTRADICTIONS}}

---

## Research Gaps

{{#GAPS}}
- {{GAP_DESCRIPTION}}
{{/GAPS}}

---

## Follow-Up Queries (for deeper investigation)

{{#FOLLOW_UPS}}
1. {{FOLLOW_UP_QUERY}}
{{/FOLLOW_UPS}}

---

## Sources Consulted

{{#SOURCES}}
1. [{{SOURCE_TITLE}}]({{SOURCE_URL}}) — Insights: {{INSIGHT_COUNT}}, Avg Relevance: {{AVG_RELEVANCE}}
{{/SOURCES}}

---

## Methodology

1. **Query Decomposition:** Broke research question into {{SUBTASK_COUNT}} sub-tasks
2. **Search Strategy:** Used {{SEARCH_ENGINE}} with {{QUERY_COUNT}} optimized queries
3. **Depth:** Explored {{DEPTH_LEVELS}} levels with {{FOLLOW_UP_COUNT}} follow-up queries
4. **Validation:** Cross-referenced {{VALIDATED_CLAIMS}} claims across multiple sources

---

## Recommendations

{{#RECOMMENDATIONS}}
1. {{RECOMMENDATION}}
{{/RECOMMENDATIONS}}

---

*This report was generated using the deep-researcher skill.*
