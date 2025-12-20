# Emergency Response Procedures

Rapid response protocols for critical security incidents.

## Emergency Classification

| Level | Criteria | Response Time | Escalation |
|-------|----------|---------------|------------|
| P0 | Active breach, data exfiltration | Immediate | All hands |
| P1 | Critical CVE, zero-day | 4 hours | Security lead |
| P2 | High severity vulnerability | 24 hours | Team lead |
| P3 | Medium severity | 1 week | Normal workflow |

## Immediate Response Protocol

### Step 1: Contain

```bash
# Isolate affected system (if network breach suspected)
# Linux - block all outbound except SSH
sudo iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -j DROP

# Capture current state
ps aux > /tmp/process_snapshot.txt
netstat -tulpn > /tmp/network_snapshot.txt
last -100 > /tmp/login_snapshot.txt
```

### Step 2: Preserve Evidence

```bash
# Create forensic snapshot
tar -czvf /tmp/forensic_$(date +%s).tar.gz \
  /var/log/auth.log \
  /var/log/syslog \
  /var/log/secure \
  ~/.bash_history

# Calculate hashes for integrity
sha256sum /tmp/forensic_*.tar.gz > /tmp/evidence_hashes.txt
```

### Step 3: Assess Impact

Use Claude to analyze with WebSearch:
- Search for CVE details and exploitation vectors
- Find available patches or workarounds
- Identify affected systems and scope

## Workaround Strategies

### When Patches Not Available

| Scenario | Mitigation |
|----------|------------|
| Network service vulnerability | Firewall rules to restrict access |
| Library vulnerability | Virtual patching, WAF rules |
| Authentication bypass | Additional auth layer, IP whitelist |
| RCE in application | Sandbox, container isolation |
| Data exposure | Access control, encryption at rest |

### Temporary Hardening

```bash
# Restrict service to localhost only
sudo sed -i 's/bind 0.0.0.0/bind 127.0.0.1/' /etc/service/config

# Add rate limiting (nginx example)
# limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

# Enable additional logging
sudo auditctl -a always,exit -F arch=b64 -S execve

# Increase monitoring sensitivity
# Lower thresholds for alerts
```

## CVE Response Checklist

```
[ ] 1. Confirm CVE affects our systems
    - Check versions in use
    - Verify vulnerable configuration

[ ] 2. Assess exposure
    - Internet-facing?
    - Internal access only?
    - Exploitation in the wild?

[ ] 3. Find mitigation
    - Official patch available?
    - Workaround documented?
    - Compensating controls possible?

[ ] 4. Implement fix
    - Test in staging first
    - Document all changes
    - Verify fix effectiveness

[ ] 5. Verify remediation
    - Re-scan for vulnerability
    - Monitor for exploit attempts
    - Update knowledge base
```

## Communication Templates

### Internal Alert

```
SECURITY ALERT - [P-LEVEL]

Issue: [Brief description]
CVE: [CVE-ID if applicable]
Affected: [Systems/services]
Status: [Investigating/Mitigating/Resolved]
Action Required: [Specific actions for team]

Lead: [Name]
ETA for Update: [Time]
```

### External Communication

```
Security Advisory

We have identified and are addressing a security issue
affecting [general description].

Impact: [Customer impact]
Action Required: [Steps customers should take]
Timeline: [Expected resolution]

Updates will be provided at [location].
```

## Post-Incident Actions

1. **Root Cause Analysis**
   - What was the vulnerability?
   - How was it introduced?
   - Why wasn't it detected earlier?

2. **Knowledge Base Update**
   - Add new detection patterns
   - Update scanning rules
   - Document lessons learned

3. **Process Improvement**
   - Update security checklist
   - Add new automated checks
   - Adjust monitoring thresholds

## Emergency Contacts

| Role | Contact Method |
|------|----------------|
| Security Lead | [Configure in .env] |
| On-call Engineer | [Configure in .env] |
| Management | [Configure in .env] |
| Legal/Compliance | [Configure in .env] |

## Quick Reference Commands

```bash
# Check for active connections
ss -tunapl | grep ESTABLISHED

# Find recently modified files (last 24h)
find / -type f -mtime -1 2>/dev/null

# Check for unusual processes
ps aux --sort=-%cpu | head -20

# Review authentication logs
grep -i "failed\|invalid\|error" /var/log/auth.log | tail -50

# Check for rootkits (if rkhunter installed)
rkhunter --check --skip-keypress

# Quick malware scan (if clamav installed)
clamscan -r /home /tmp --infected
```
