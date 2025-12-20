# Security Scoring Methodology

CVSS-based scoring system for vulnerability prioritization and risk assessment.

## CVSS v3.1 Severity Ratings

| Score Range | Severity | Color | Action Timeline |
|-------------|----------|-------|-----------------|
| 9.0 - 10.0 | Critical | Red | 24 hours |
| 7.0 - 8.9 | High | Orange | 7 days |
| 4.0 - 6.9 | Medium | Yellow | 30 days |
| 0.1 - 3.9 | Low | Blue | Quarterly |
| 0.0 | None | Gray | Optional |

## Risk Score Calculation

### Base Score Formula

```
raw_score = Σ(critical × 10) + Σ(high × 7) + Σ(medium × 4) + Σ(low × 1)
normalized_score = min(100, raw_score)
```

### Severity Weights

| Severity | Weight | Rationale |
|----------|--------|-----------|
| Critical | 10 | Immediate exploitation risk |
| High | 7 | Significant impact potential |
| Medium | 4 | Moderate risk |
| Low | 1 | Minimal impact |

### Modifiers

Apply these modifiers to the base score:

| Condition | Modifier | Applied When |
|-----------|----------|--------------|
| Exploited in Wild | +20% | CISA KEV listed |
| Public Exploit | +15% | ExploitDB/Metasploit |
| Network Accessible | +10% | AV:N in CVSS |
| No Auth Required | +10% | PR:N in CVSS |
| Patch Available | -10% | Fix exists |
| Compensating Control | -15% | Mitigation in place |

### Final Score

```
final_score = base_score × (1 + Σmodifiers)
risk_level = categorize(final_score)
```

| Final Score | Risk Level |
|-------------|------------|
| 80-100 | Critical |
| 60-79 | High |
| 40-59 | Medium |
| 20-39 | Low |
| 0-19 | Minimal |

## Quality Thresholds by Level

### Level 1: Quick Check

| Metric | Threshold |
|--------|-----------|
| Min Findings | 5 |
| Intel Sources | 3 |
| Scan Coverage | 40% (2 categories) |
| Report Type | Basic MD |
| Max Duration | 5 min |

### Level 2: Standard Audit

| Metric | Threshold |
|--------|-----------|
| Min Findings | 10 |
| Intel Sources | 5 |
| Scan Coverage | 60% (3 categories) |
| Report Type | Standard MD |
| Max Duration | 15 min |

### Level 3: Thorough Review

| Metric | Threshold |
|--------|-----------|
| Min Findings | 15 |
| Intel Sources | 10 |
| Scan Coverage | 100% (5 categories) |
| Report Type | Expert HTML |
| Max Duration | 30 min |

### Level 4: Deep Assessment

| Metric | Threshold |
|--------|-----------|
| Min Findings | 20 |
| Intel Sources | 15 |
| Scan Coverage | 100% (5 categories) |
| Report Type | Expert HTML |
| Max Duration | 45 min |

### Level 5: Compliance Audit

| Metric | Threshold |
|--------|-----------|
| Min Findings | 25+ |
| Intel Sources | 20+ |
| Scan Coverage | 100% + manual |
| Report Type | Expert HTML |
| Max Duration | 60+ min |

## Compliance Mapping Weights

### OWASP Top 10 2025

| Category | Weight | Description |
|----------|--------|-------------|
| A01 Broken Access Control | 15% | Authorization failures |
| A02 Cryptographic Failures | 12% | Weak crypto |
| A03 Injection | 15% | SQL, XSS, Command |
| A04 Insecure Design | 10% | Architecture flaws |
| A05 Security Misconfiguration | 12% | Config errors |
| A06 Vulnerable Components | 12% | Outdated deps |
| A07 Auth Failures | 10% | Identity issues |
| A08 Data Integrity | 7% | Software updates |
| A09 Logging Failures | 4% | Audit gaps |
| A10 SSRF | 3% | Server-side request |

### CIS Benchmarks

| Category | Weight |
|----------|--------|
| Account Management | 15% |
| Access Control | 15% |
| Audit and Logging | 10% |
| Network Configuration | 15% |
| System Maintenance | 10% |
| File System | 10% |
| Services | 15% |
| Additional Hardening | 10% |

### NIST CSF

| Function | Weight |
|----------|--------|
| Identify | 15% |
| Protect | 30% |
| Detect | 20% |
| Respond | 20% |
| Recover | 15% |

## Prioritization Matrix

### Impact vs Likelihood

```
         │ Rare    Possible  Likely
─────────┼─────────────────────────
Critical │ High    Critical  Critical
Major    │ Medium  High      Critical
Moderate │ Low     Medium    High
Minor    │ Low     Low       Medium
```

### Remediation Priority

| Priority | Criteria | SLA |
|----------|----------|-----|
| P0 | Critical + Exploited + Network | 4 hours |
| P1 | Critical OR (High + Exploited) | 24 hours |
| P2 | High OR (Medium + Exploited) | 7 days |
| P3 | Medium | 30 days |
| P4 | Low | 90 days |

## Data Quality Score

Assess the quality of scan and intel data:

```
quality_score = (
  source_credibility × 0.3 +
  data_freshness × 0.25 +
  coverage_completeness × 0.25 +
  cross_validation × 0.2
)
```

| Component | Calculation |
|-----------|-------------|
| Source Credibility | % from verified scanners |
| Data Freshness | Age < 30 days = 1.0, degrade by 0.1/month |
| Coverage | categories_scanned / total_categories |
| Cross Validation | % findings confirmed by 2+ sources |

### Quality Thresholds

| Quality Score | Interpretation |
|---------------|----------------|
| 0.9 - 1.0 | Excellent - high confidence |
| 0.7 - 0.89 | Good - actionable |
| 0.5 - 0.69 | Fair - needs review |
| < 0.5 | Poor - rerun scans |

## Agent Performance Metrics

Track agent effectiveness:

| Metric | Target |
|--------|--------|
| Intel Agent Relevance | > 80% relevant CVEs |
| Scan Agent Coverage | > 90% of target |
| Analysis Accuracy | < 5% false positives |
| Synthesis Clarity | Executive-readable |
| Visualization Load | < 3s render time |
