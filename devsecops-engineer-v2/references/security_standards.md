# Security Standards Reference

Quick reference for security frameworks and compliance requirements.

## OWASP Top 10 2025

| Rank | Category | Description | Check Method |
|------|----------|-------------|--------------|
| A01 | Broken Access Control | Unauthorized access to resources | Review auth/authz logic |
| A02 | Security Misconfiguration | Default configs, verbose errors | Config audit |
| A03 | Software Supply Chain Failures | Vulnerable dependencies, compromised packages | SBOM + SCA |
| A04 | Cryptographic Failures | Weak encryption, exposed secrets | Crypto audit |
| A05 | Injection | SQL, NoSQL, OS command injection | SAST + DAST |
| A06 | Insecure Design | Missing security controls | Threat modeling |
| A07 | Identification & Auth Failures | Weak authentication | Auth testing |
| A08 | Software & Data Integrity Failures | Unsigned code, insecure deserialization | Integrity checks |
| A09 | Security Logging & Monitoring Failures | Missing audit trails | Log review |
| A10 | Mishandling of Exceptional Conditions | Improper error handling | Error path testing |

## CIS Benchmarks Quick Checks

### Linux Server Hardening

```bash
# Check file permissions
stat -c %a /etc/passwd    # Should be 644
stat -c %a /etc/shadow    # Should be 640

# Check SSH configuration
grep "PermitRootLogin" /etc/ssh/sshd_config    # Should be "no"
grep "PasswordAuthentication" /etc/ssh/sshd_config  # Should be "no"

# Check running services
systemctl list-units --type=service --state=running

# Check open ports
ss -tuln
```

### macOS Security Checks

```bash
# FileVault status
fdesetup status

# Firewall status
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# SIP status
csrutil status

# Check for unsigned apps
spctl --assess --type exec /path/to/app
```

## NIST Cybersecurity Framework Alignment

| Function | Category | Subcategory |
|----------|----------|-------------|
| Identify | Asset Management | ID.AM-1: Physical devices inventoried |
| Protect | Access Control | PR.AC-1: Identities managed |
| Detect | Anomalies | DE.AE-1: Network baseline established |
| Respond | Response Planning | RS.RP-1: Response plan executed |
| Recover | Recovery Planning | RC.RP-1: Recovery plan executed |

## Severity Ratings

### CVSS v3.1 Score Mapping

| Score | Severity | Action Timeline |
|-------|----------|-----------------|
| 9.0-10.0 | Critical | Immediate (24h) |
| 7.0-8.9 | High | Priority (1 week) |
| 4.0-6.9 | Medium | Planned (1 month) |
| 0.1-3.9 | Low | As resources permit |

### Risk Prioritization Matrix

```
Impact
  High   | Medium | High   | Critical |
  Medium | Low    | Medium | High     |
  Low    | Low    | Low    | Medium   |
         +---------+---------+---------+
           Low     Medium    High
                 Likelihood
```

## Compliance Automation

### Pre-Commit Checks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: detect-private-key
      - id: detect-aws-credentials
  - repo: https://github.com/gitleaks/gitleaks
    hooks:
      - id: gitleaks
```

### CI/CD Security Gates

```yaml
# Required security checks before merge
security_gates:
  - sast_scan: required
  - dependency_check: required
  - secret_scan: required
  - container_scan: required (if Dockerfile present)
```

## Common Vulnerability Patterns

### Dependency Vulnerabilities

| Ecosystem | Scanner | Command |
|-----------|---------|---------|
| npm | npm audit | `npm audit --json` |
| Python | pip-audit | `pip-audit --format json` |
| Go | govulncheck | `govulncheck ./...` |
| Ruby | bundler-audit | `bundle audit check` |
| Java | OWASP Dep Check | `dependency-check --scan .` |

### Secret Patterns to Detect

| Type | Pattern Example |
|------|-----------------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` |
| GitHub Token | `ghp_[A-Za-z0-9]{36}` |
| Slack Token | `xox[baprs]-[0-9A-Za-z]` |
| Private Key | `-----BEGIN.*PRIVATE KEY-----` |
| JWT | `eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+` |

## Reference Links

- OWASP Top 10: https://owasp.org/Top10/
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- NIST CSF: https://www.nist.gov/cyberframework
- NVD Database: https://nvd.nist.gov/
- GitHub Security Advisories: https://github.com/advisories
