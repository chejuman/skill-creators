# Technical Debt Analysis Report v4

**Target:** {TARGET}
**Date:** {DATE}
**Level:** {LEVEL}/5
**Generator:** resolve-debt-v4 (10 workers)

---

## Executive Summary

### Financial Impact

| Metric               |                Value | Industry Benchmark |
| -------------------- | -------------------: | -----------------: |
| Total Annual Cost    | ${TOTAL_ANNUAL_COST} |                  - |
| Remediation Cost     |  ${REMEDIATION_COST} |                  - |
| Technical Debt Ratio |               {TDR}% |       42% (Stripe) |
| Rating               |     **{TDR_RATING}** |                  - |

### Issue Overview

| Priority  |       Count       |              Cost |               % |
| --------- | :---------------: | ----------------: | --------------: |
| Critical  | {CRITICAL_COUNT}  |  ${CRITICAL_COST} | {CRITICAL_PCT}% |
| High      |   {HIGH_COUNT}    |      ${HIGH_COST} |     {HIGH_PCT}% |
| Medium    |  {MEDIUM_COUNT}   |    ${MEDIUM_COST} |   {MEDIUM_PCT}% |
| **Total** | **{TOTAL_ITEMS}** | **${TOTAL_COST}** |            100% |

### DevEx Impact

| Metric                  |               Value |
| ----------------------- | ------------------: |
| Hours Lost Weekly       |       {HOURS_LOST}h |
| Productivity Tax        |         {PROD_TAX}% |
| Annual Opportunity Cost | ${OPPORTUNITY_COST} |

---

## Issues by Category

| Category       |    Count     |  Critical   |    High     |   Medium   |         Cost |
| -------------- | :----------: | :---------: | :---------: | :--------: | -----------: |
| Code Quality   |  {CQ_COUNT}  |  {CQ_CRIT}  |  {CQ_HIGH}  |  {CQ_MED}  |   ${CQ_COST} |
| Dependencies   | {DEP_COUNT}  | {DEP_CRIT}  | {DEP_HIGH}  | {DEP_MED}  |  ${DEP_COST} |
| Architecture   | {ARCH_COUNT} | {ARCH_CRIT} | {ARCH_HIGH} | {ARCH_MED} | ${ARCH_COST} |
| Test Coverage  | {TEST_COUNT} | {TEST_CRIT} | {TEST_HIGH} | {TEST_MED} | ${TEST_COST} |
| Performance    | {PERF_COUNT} | {PERF_CRIT} | {PERF_HIGH} | {PERF_MED} | ${PERF_COST} |
| Security       | {SEC_COUNT}  | {SEC_CRIT}  | {SEC_HIGH}  | {SEC_MED}  |  ${SEC_COST} |
| Documentation  | {DOC_COUNT}  | {DOC_CRIT}  | {DOC_HIGH}  | {DOC_MED}  |  ${DOC_COST} |
| Type Safety    | {TYPE_COUNT} | {TYPE_CRIT} | {TYPE_HIGH} | {TYPE_MED} | ${TYPE_COST} |
| AI Code        |  {AI_COUNT}  |  {AI_CRIT}  |  {AI_HIGH}  |  {AI_MED}  |   ${AI_COST} |
| Knowledge Silo | {SILO_COUNT} | {SILO_CRIT} | {SILO_HIGH} | {SILO_MED} | ${SILO_COST} |

---

## Root Causes

### Top 3 Root Causes

1. **{ROOT_1}** - Impacts {ROOT_1_COUNT} issues, ${ROOT_1_COST} annual cost
2. **{ROOT_2}** - Impacts {ROOT_2_COUNT} issues, ${ROOT_2_COST} annual cost
3. **{ROOT_3}** - Impacts {ROOT_3_COUNT} issues, ${ROOT_3_COST} annual cost

---

## Knowledge Risks

### Bus Factor Analysis

| Module   | Bus Factor | Primary Owner | Last Active   | Risk Level |
| -------- | :--------: | ------------- | ------------- | :--------: |
| {MODULE} |    {BF}    | {OWNER}       | {LAST_ACTIVE} |   {RISK}   |

### Critical Knowledge Silos

- **{SILO_1}**: {SILO_1_DESC}
- **{SILO_2}**: {SILO_2_DESC}

---

## Critical Issues

### {ID}: {TITLE}

- **Category:** {CATEGORY}
- **Location:** `{FILE_PATH}:{LINE}`
- **RICE Score:** {RICE_SCORE}
- **Annual Cost:** ${ANNUAL_COST}
- **ROI:** {ROI}%

**Problem:**
{PROBLEM_DESCRIPTION}

**Business Impact:**
{IMPACT_DESCRIPTION}

**Solution:**
{SOLUTION_STEPS}

**Verification:**
{VERIFICATION_STEPS}

---

## Quick Wins

|  #  | Fix     | Location  |  Effort  |  Savings |      ROI |
| :-: | ------- | --------- | :------: | -------: | -------: |
|  1  | {FIX_1} | `{LOC_1}` | {EFF_1}h | ${SAV_1} | {ROI_1}% |
|  2  | {FIX_2} | `{LOC_2}` | {EFF_2}h | ${SAV_2} | {ROI_2}% |
|  3  | {FIX_3} | `{LOC_3}` | {EFF_3}h | ${SAV_3} | {ROI_3}% |

**Total Quick Win Investment:** ${QW_TOTAL}
**Expected Annual Savings:** ${QW_SAVINGS}
**Payback:** {PAYBACK} weeks

---

## Auto-Fix Patches

{AUTOFIX_COUNT} patches generated for quick wins.

### Patch 1: {PATCH_1_TITLE}

**File:** `{PATCH_1_FILE}`

```diff
{PATCH_1_DIFF}
```

**Verification:** {PATCH_1_VERIFY}

---

## Implementation Roadmap

### Phase 1: Foundation (Critical Fixes)

**Investment:** ${PHASE_1_COST} | **Savings:** ${PHASE_1_SAVINGS}/year

```
{FOUNDATION_FIX_1}
    └── Unblocks: {DEPS_1}

{FOUNDATION_FIX_2}
    └── Unblocks: {DEPS_2}
```

### Phase 2: Knowledge Transfer

**Investment:** ${PHASE_2_COST} | **Risk Reduction:** {PHASE_2_RISK}%

- Document {SILO_MODULE_1}
- Cross-train on {SILO_MODULE_2}
- Update CODEOWNERS

### Phase 3: Systematic Cleanup

**Investment:** ${PHASE_3_COST} | **Savings:** ${PHASE_3_SAVINGS}/year

---

## Metrics to Track

| Metric                |     Current      |      Target      | Method       |
| --------------------- | :--------------: | :--------------: | ------------ |
| TDR                   |  {TDR_CURRENT}%  |       <25%       | This tool    |
| Code Coverage         |  {COV_CURRENT}%  |  >{COV_TARGET}%  | Jest/pytest  |
| Cyclomatic Complexity |   {CC_CURRENT}   |   <{CC_TARGET}   | SonarQube    |
| Security CVEs         |  {CVE_CURRENT}   |        0         | npm audit    |
| Bus Factor (avg)      |   {BF_CURRENT}   |   >{BF_TARGET}   | Git analysis |
| DevEx Hours Lost      | {DEVEX_CURRENT}h | <{DEVEX_TARGET}h | Survey       |

---

## Trend Analysis

| Metric       |   Previous    |    Current    |     Change     |
| ------------ | :-----------: | :-----------: | :------------: |
| Total Issues | {PREV_ISSUES} | {CURR_ISSUES} | {DELTA_ISSUES} |
| Annual Cost  | ${PREV_COST}  | ${CURR_COST}  |  {DELTA_COST}  |
| TDR          |  {PREV_TDR}%  |  {CURR_TDR}%  |  {DELTA_TDR}   |

**Trajectory:** {TRAJECTORY}

**New Issues:** {NEW_ISSUES_COUNT}
**Resolved:** {RESOLVED_COUNT}

---

## Validation Summary

| Metric                  |             Value |
| ----------------------- | ----------------: |
| Items Validated         | {VALIDATED_COUNT} |
| False Positives Removed |   {REMOVED_COUNT} |
| Severity Adjusted       |  {ADJUSTED_COUNT} |
| Needs Review            |    {REVIEW_COUNT} |

---

## Appendix: Worker Statistics

| Worker         |    Issues    |  Duration   | Cost Identified |
| -------------- | :----------: | :---------: | --------------: |
| Code Quality   |  {CQ_COUNT}  |  {CQ_MS}ms  |      ${CQ_COST} |
| Dependencies   | {DEP_COUNT}  | {DEP_MS}ms  |     ${DEP_COST} |
| Architecture   | {ARCH_COUNT} | {ARCH_MS}ms |    ${ARCH_COST} |
| Test Coverage  | {TEST_COUNT} | {TEST_MS}ms |    ${TEST_COST} |
| Performance    | {PERF_COUNT} | {PERF_MS}ms |    ${PERF_COST} |
| Security       | {SEC_COUNT}  | {SEC_MS}ms  |     ${SEC_COST} |
| Documentation  | {DOC_COUNT}  | {DOC_MS}ms  |     ${DOC_COST} |
| Type Safety    | {TYPE_COUNT} | {TYPE_MS}ms |    ${TYPE_COST} |
| AI Code        |  {AI_COUNT}  |  {AI_MS}ms  |      ${AI_COST} |
| Knowledge Silo | {SILO_COUNT} | {SILO_MS}ms |    ${SILO_COST} |

**Total Analysis Duration:** {TOTAL_DURATION}ms

---

_Generated by resolve-debt-v4 enterprise multi-agent system_
