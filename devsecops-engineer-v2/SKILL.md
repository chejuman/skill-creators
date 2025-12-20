---
name: devsecops-engineer-v2
description: Multi-agent DevSecOps security assessment system with parallel execution. Spawns parallel Intel Agents for threat intelligence, Scan Agents for vulnerability detection, Analysis Agent for CVSS scoring, Remediation Agent for patching, and Report Agent for expert reporting. Use when performing security audits, vulnerability scanning, compliance checks, or generating security reports. Triggers on "security scan", "pentest", "vulnerability audit", "compliance check", security levels (1-5), or "security assessment".
---

# DevSecOps Engineer v2.0

Hierarchical multi-agent security assessment system with parallel execution and expert reporting.

## Architecture

```
Orchestrator (this skill)
    │
    ├─► Planning Agent ──► Scope analysis & task decomposition
    │
    ├─► Intel Agents (PARALLEL) ──► Threat intelligence gathering
    │       ├── Intel Agent #1: CVE/Zero-day monitoring
    │       ├── Intel Agent #2: Technology-specific threats
    │       └── Intel Agent #3: Compliance updates
    │
    ├─► Scan Agents (PARALLEL) ──► Security scanning
    │       ├── Scan Agent #1: Vulnerability scanning
    │       ├── Scan Agent #2: Secret detection
    │       ├── Scan Agent #3: Configuration audit
    │       ├── Scan Agent #4: Dependency checking
    │       └── Scan Agent #5: Container security
    │
    ├─► Analysis Agent ──► CVSS scoring & prioritization
    │
    ├─► Remediation Agent ──► Interactive patching (sequential)
    │
    ├─► Report Agent ──► Expert report generation (MD/HTML)
    │
    └─► Self-Upgrade ──► Capture learnings
```

## Security Levels

| Level | Depth | Intel | Scans | Analysis | Report | Use Case |
|-------|-------|-------|-------|----------|--------|----------|
| 1 | Quick | 1 | 2 | Inline | Basic MD | Health check |
| 2 | Standard | 2 | 3 | 1 agent | Standard MD | Regular audit |
| 3 | Thorough | 3 | 5 | 1 agent | Expert HTML | Quarterly review |
| 4 | Deep | 3 | 5 | 1 agent | Expert HTML | Pre-deployment |
| 5 | Exhaustive | 3 | 5+ | 1 agent | Expert HTML | Compliance audit |

## Execution Workflow

### Phase 1: Planning

Spawn Planning Agent to analyze scope:

```
Task(
  subagent_type='Plan',
  prompt='Analyze security assessment scope and decompose into parallel tasks...',
  description='Plan security assessment'
)
```

**Planning Agent Output:**
```json
{
  "target": "local|ssh|container",
  "technologies": ["nodejs", "python", "docker"],
  "scan_categories": ["vulnerability", "secrets", "config", "deps", "container"],
  "intel_queries": ["CVE alerts", "tech threats", "compliance"],
  "expected_findings": 20
}
```

### Phase 2: Intelligence Gathering (PARALLEL)

Spawn Intel Agents simultaneously in a SINGLE message:

```
# CRITICAL: All Task calls in ONE message for true parallelism
Task(subagent_type='Explore', prompt='Search for latest CVE advisories...', description='Intel: CVE monitoring', model='haiku')
Task(subagent_type='Explore', prompt='Search for technology-specific threats...', description='Intel: Tech threats', model='haiku')
Task(subagent_type='Explore', prompt='Search for compliance updates...', description='Intel: Compliance', model='haiku')
```

**Intel Agent Prompt Template:**
```
You are an Intel Agent gathering threat intelligence.

FOCUS: {intel_type}
TECHNOLOGIES: {tech_list}

Instructions:
1. Use WebSearch for latest security advisories (last 30 days)
2. Focus on CVEs with CVSS >= 7.0
3. Return findings in JSON format:

{
  "intel_type": "{type}",
  "findings": [
    {
      "cve_id": "CVE-XXXX-XXXXX",
      "severity": "critical|high|medium|low",
      "cvss_score": 9.8,
      "affected": ["package@version"],
      "description": "...",
      "patch_available": true,
      "source_url": "..."
    }
  ],
  "zero_days": [...],
  "attack_patterns": [...]
}
```

### Phase 3: Security Scanning (PARALLEL)

Spawn 5 Scan Agents simultaneously:

```
# All in ONE message for parallel execution
Task(subagent_type='general-purpose', prompt='Run vulnerability scan...', description='Scan: Vulnerabilities', model='haiku')
Task(subagent_type='general-purpose', prompt='Run secret detection...', description='Scan: Secrets', model='haiku')
Task(subagent_type='general-purpose', prompt='Run config audit...', description='Scan: Config', model='haiku')
Task(subagent_type='general-purpose', prompt='Run dependency check...', description='Scan: Dependencies', model='haiku')
Task(subagent_type='general-purpose', prompt='Run container scan...', description='Scan: Container', model='haiku')
```

**Scan Agent Output:**
```json
{
  "scan_type": "vulnerability|secrets|config|deps|container",
  "target": "...",
  "findings": [
    {
      "id": "...",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0-10.0,
      "title": "...",
      "description": "...",
      "location": "file:line",
      "remediation": "...",
      "references": ["..."]
    }
  ],
  "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0}
}
```

### Phase 4: Analysis

Spawn Analysis Agent to process all findings:

```
Task(
  subagent_type='general-purpose',
  prompt='Analyze security findings, calculate CVSS scores, prioritize remediation...',
  description='Analyze security findings'
)
```

**Analysis Agent Tasks:**
- Calculate composite risk score (CVSS-weighted)
- Cross-reference with threat intelligence
- Identify false positives
- Prioritize by exploitability and impact
- Map to compliance frameworks

**Analysis Output:**
```json
{
  "risk_score": 75,
  "risk_level": "high",
  "critical_findings": [...],
  "high_findings": [...],
  "medium_findings": [...],
  "low_findings": [...],
  "compliance_gaps": {
    "owasp_2025": [...],
    "cis": [...],
    "nist_csf": [...]
  },
  "remediation_priority": [...]
}
```

### Phase 5: Interactive Remediation

Remediation Agent presents patches for user approval:

```bash
python3 scripts/auto_patch.py --scan-report ./security-reports/analysis.json
```

For each finding:
1. Display severity, CVSS score, and fix
2. **Ask user confirmation** before applying
3. Create backup before changes
4. Apply patch and verify
5. Offer rollback on failure

### Phase 6: Report Generation

Spawn Report Agent to generate expert-level reports:

```
Task(
  subagent_type='general-purpose',
  prompt='Generate comprehensive security report using expert_report.py...',
  description='Generate expert report'
)
```

**Standard Reports (Markdown/HTML):**
```bash
python3 scripts/report_generator.py \
  --input ./security-reports --format markdown,html --output ./final-reports
```

**Expert-Level Reports (Recommended):**
```bash
python3 scripts/expert_report.py \
  --input ./security-reports --output ./final-reports
```

Expert reports include:
- Visual risk score dashboard with severity charts
- CVSS-weighted risk calculation methodology
- Executive summary for C-suite audiences
- Real-time threat intelligence context
- Risk matrix visualization (Impact vs Likelihood)
- Compliance mapping (OWASP 2025, CIS, NIST CSF)
- Prioritized remediation timeline
- Evidence and artifact documentation

**Report Structure:**
```markdown
# Security Assessment Report

**Date:** {date} | **Target:** {target} | **Level:** {level}
**Risk Score:** {score}/100 | **Agents Used:** {count}

## Executive Summary
{2-3 paragraph overview for leadership}

## Critical Findings (CVSS >= 9.0)
{Detailed findings with remediation steps}

## High Priority Findings (CVSS 7.0-8.9)
{Findings requiring immediate attention}

## Compliance Status
| Framework | Score | Gaps |
|-----------|-------|------|
| OWASP 2025 | X% | ... |
| CIS Benchmarks | X% | ... |
| NIST CSF | X% | ... |

## Remediation Timeline
| Priority | Finding | Action | SLA |
|----------|---------|--------|-----|
| P0 | ... | ... | 24h |
| P1 | ... | ... | 7d |

## Threat Intelligence Context
{Related CVEs, attack patterns, zero-days}

## Sources & References
{Full source list}
```

### Phase 7: Self-Upgrade

After assessment, capture learnings:

```bash
python3 scripts/self_upgrade.py --findings ./security-reports
```

This process:
1. Extracts new threat patterns from findings
2. Updates local threat intelligence database
3. Enhances scanning rules based on discoveries
4. Records lessons learned for future assessments

## Orchestration Rules

### Parallel Execution Pattern

All Task calls in ONE message for true parallelism:

```python
# CORRECT - True parallel
message:
  - Task(intel_1)
  - Task(intel_2)
  - Task(intel_3)

# INCORRECT - Sequential
message1: Task(intel_1)
message2: Task(intel_2)
```

### Agent Coordination

1. **Planning Agent** runs FIRST (sequential)
2. **Intel Agents** run in PARALLEL (same message)
3. **Scan Agents** run in PARALLEL (same message)
4. **Analysis Agent** runs after ALL scans complete
5. **Remediation Agent** runs interactively (sequential)
6. **Report Agent** runs after remediation
7. **Self-Upgrade** runs LAST

### Tool Usage by Agent

| Agent | Tools | Model |
|-------|-------|-------|
| Planning | Glob, Grep, Read | sonnet |
| Intel | WebSearch, WebFetch | haiku |
| Scan | Bash, Read, Grep | haiku |
| Analysis | Read, Grep | sonnet |
| Remediation | Bash, Read, Write | sonnet |
| Report | Bash, Read, Write | sonnet |

## Quality Metrics

| Level | Min Findings | Intel Sources | Scan Coverage | Expert Report |
|-------|-------------|---------------|---------------|---------------|
| 1 | 5 | 3 | 40% | No |
| 2 | 10 | 5 | 60% | No |
| 3 | 15 | 10 | 80% | Yes |
| 4 | 20 | 15 | 90% | Yes |
| 5 | 25+ | 20+ | 100% | Yes |

## Quick Commands

| Task | Command |
|------|---------|
| Level 3 scan | `/devsecops-v2 scan --level 3` |
| Local scan | `/devsecops-v2 scan-local` |
| Remote scan | `/devsecops-v2 scan-ssh <host>` |
| Dependency audit | `/devsecops-v2 deps` |
| Apply patches | `/devsecops-v2 patch` |
| Dry-run patches | `/devsecops-v2 patch --dry-run` |
| Rollback patches | `/devsecops-v2 rollback <backup-dir>` |
| Emergency CVE | `/devsecops-v2 emergency <CVE-ID>` |
| Generate report | `/devsecops-v2 report` |

## Resources

- [Agent Prompts](references/agent_prompts.md) - All agent prompt templates
- [Security Scoring](references/security_scoring.md) - CVSS scoring methodology
- [Security Standards](references/security_standards.md) - Compliance mappings
- [Emergency Response](references/emergency_response.md) - Incident procedures

## Trigger Phrases

- "security scan level X" / "보안 스캔 레벨 X"
- "security assessment" / "보안 평가"
- "vulnerability audit" / "취약점 감사"
- "compliance check" / "컴플라이언스 점검"
- "pentest" / "침투 테스트"
- "with expert report" / "전문가 보고서로"
