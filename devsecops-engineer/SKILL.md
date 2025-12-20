---
name: devsecops-engineer
description: Professional DevSecOps engineer workflow for comprehensive security assessments with automated patch application. Use when performing security audits, vulnerability scanning, applying security patches, compliance checks, threat intelligence gathering, emergency security response, or generating security reports. Triggers on security scan, pentest, vulnerability, compliance audit, CVE, threat analysis, security report, hardening, patch application, or incident response tasks.
---

# DevSecOps Engineer Workflow

Professional security assessment and response system with real-time threat intelligence, automated patching, and self-upgrading capabilities.

## Workflow Overview

```
1. Intelligence Gathering → 2. Target Assessment → 3. Security Scanning → 4. Interactive Patching → 5. Reporting → 6. Self-Upgrade
```

## Phase 1: Real-Time Intelligence Gathering (MANDATORY)

Before any security assessment, gather latest threat intelligence:

```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/threat_intel.py
```

Also use WebSearch to collect:
- Latest CVE advisories for target technologies
- Zero-day alerts from security vendors
- Current attack patterns and TTPs
- Emergency patches and workarounds

Store findings in session context for analysis.

## Phase 2: Target Assessment

### Local Machine Scanning
```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/security_scanner.py --target local --output ./security-reports
```

Checks performed:
- OS security configuration audit
- Installed software vulnerability scan
- Network port exposure analysis
- Secret/credential detection
- Dependency vulnerabilities (npm, pip, gem)
- SSH key and config audit

### Remote Server Scanning (SSH)
```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/security_scanner.py --target ssh --host <hostname> --output ./security-reports
```

Checks performed:
- System hardening verification (CIS benchmarks)
- User and permission audit
- Service exposure analysis
- Log analysis for indicators of compromise
- Firewall and network security

## Phase 3: Security Scanning Categories

| Category | Tools Used | Output |
|----------|------------|--------|
| Vulnerability Scan | Trivy, npm audit, pip-audit | CVE list with severity |
| Secret Detection | TruffleHog, detect-secrets | Exposed credentials |
| Config Audit | Lynis, CIS-CAT | Compliance score |
| Dependency Check | OWASP Dependency-Check | SBOM + vulnerabilities |
| Container Security | Trivy, Hadolint | Image vulnerabilities |

## Phase 4: Interactive Patch Application

After scanning, apply security patches with user approval:

### Analyze and Plan Patches
```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/auto_patch.py \
  --scan-report ./security-reports/scan_local_*.json --dry-run
```

### Interactive Patching (Recommended)
```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/auto_patch.py \
  --scan-report ./security-reports/scan_local_*.json
```

For each vulnerability:
1. Display package, severity, and fix version
2. **Ask user confirmation** before applying
3. Create backup before any changes
4. Apply patch and verify success
5. Offer rollback option if failed

### Rollback to Pre-Patch State
```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/auto_patch.py \
  --rollback ./patch-backups/<backup-dir>
```

### Patch Priorities

| Severity | Action | Recommendation |
|----------|--------|----------------|
| Critical | Immediate | Apply within 24 hours |
| High | Urgent | Apply within 1 week |
| Medium | Planned | Include in next release |
| Low | Optional | Evaluate risk/benefit |

## Phase 5: Emergency Response Protocol

When critical vulnerabilities are found without available patches:

1. **Immediate Assessment**: Evaluate exploitability and impact
2. **Mitigation Search**: Use WebSearch for temporary workarounds
3. **Apply Workarounds**: Implement without waiting for official patches
4. **Document Actions**: Record all mitigation steps taken

See [emergency_response.md](references/emergency_response.md) for detailed procedures.

## Phase 6: Report Generation

### Standard Reports (Markdown/HTML)
```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/report_generator.py \
  --input ./security-reports --format markdown,html --output ./final-reports
```

### Expert-Level Reports (Recommended)
```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/expert_report.py \
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

## Phase 7: Self-Upgrade Mechanism

After each assessment, capture learnings:

```bash
python3 ~/.claude/skills/devsecops-engineer/scripts/self_upgrade.py --findings ./security-reports
```

This process:
1. Extracts new threat patterns from findings
2. Updates local threat intelligence database
3. Enhances scanning rules based on discoveries
4. Records lessons learned for future assessments

## Quick Commands

| Task | Command |
|------|---------|
| Full local scan | `/devsecops scan-local` |
| Remote server scan | `/devsecops scan-ssh <host>` |
| Dependency audit | `/devsecops deps` |
| **Apply patches** | `/devsecops patch` |
| Dry-run patches | `/devsecops patch --dry-run` |
| Rollback patches | `/devsecops rollback <backup-dir>` |
| Emergency response | `/devsecops emergency <CVE-ID>` |
| Generate report | `/devsecops report` |

## Security Standards Reference

See [security_standards.md](references/security_standards.md) for:
- OWASP Top 10 2025 mappings
- CIS Benchmark requirements
- NIST Cybersecurity Framework alignment

## Requirements

Install dependencies:
```bash
pip install -r ~/.claude/skills/devsecops-engineer/scripts/requirements.txt
```

Optional tools (enhanced scanning):
- trivy: Container/filesystem vulnerability scanner
- lynis: System auditing tool
- trufflehog: Secret detection

## Output Location

Reports are saved to:
- `./security-reports/` - Raw scan outputs
- `./final-reports/` - Formatted reports (MD/HTML)
