# Security Checklist

Comprehensive security review checklist based on OWASP and CWE.

## OWASP Top 10 (2021)

### A01: Broken Access Control

```
[ ] Authorization checks on every endpoint
[ ] Deny by default, allow explicitly
[ ] No CORS misconfiguration
[ ] No direct object reference (IDOR) vulnerabilities
[ ] Rate limiting on sensitive endpoints
[ ] Session invalidation on logout
```

**Patterns to detect:**

```typescript
// BAD: Missing authorization
app.get("/admin/users", (req, res) => {
  return db.getAllUsers(); // No auth check!
});

// GOOD: Proper authorization
app.get("/admin/users", requireRole("admin"), (req, res) => {
  return db.getAllUsers();
});
```

### A02: Cryptographic Failures

```
[ ] No sensitive data in URL parameters
[ ] HTTPS enforced for all data in transit
[ ] Strong encryption for data at rest (AES-256)
[ ] Secure password hashing (bcrypt, argon2)
[ ] No deprecated algorithms (MD5, SHA1 for security)
[ ] Proper key management
```

**Patterns to detect:**

```python
# BAD: Weak hashing
password_hash = hashlib.md5(password.encode()).hexdigest()

# GOOD: Strong hashing
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### A03: Injection

```
[ ] SQL queries use parameterized statements
[ ] NoSQL queries properly escaped
[ ] Command execution avoids shell interpolation
[ ] LDAP queries sanitized
[ ] XPath queries escaped
```

**Patterns to detect:**

```javascript
// BAD: SQL injection
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// GOOD: Parameterized query
db.query("SELECT * FROM users WHERE id = $1", [userId]);
```

### A04: Insecure Design

```
[ ] Threat modeling performed
[ ] Security requirements defined
[ ] Defense in depth implemented
[ ] Fail-secure mechanisms
[ ] Resource quotas and limits
```

### A05: Security Misconfiguration

```
[ ] No default credentials
[ ] Error messages don't leak information
[ ] Security headers configured (CSP, HSTS, etc.)
[ ] Unnecessary features disabled
[ ] Dependencies up to date
```

### A06: Vulnerable Components

```
[ ] Dependencies scanned for vulnerabilities
[ ] Components from trusted sources
[ ] Unused dependencies removed
[ ] Component versions tracked
```

### A07: Authentication Failures

```
[ ] Strong password policy enforced
[ ] Multi-factor authentication available
[ ] Brute force protection (rate limiting, lockout)
[ ] Secure session management
[ ] Password recovery is secure
```

### A08: Data Integrity Failures

```
[ ] Code/data integrity verified
[ ] CI/CD pipeline secured
[ ] Unsigned serialized data not trusted
[ ] Critical data has integrity checks
```

### A09: Logging & Monitoring

```
[ ] Security events logged
[ ] Logs don't contain sensitive data
[ ] Alerting configured
[ ] Logs protected from tampering
```

### A10: SSRF

```
[ ] URL inputs validated
[ ] Allowlists for external calls
[ ] Internal services not accessible via user input
[ ] DNS rebinding protection
```

## Language-Specific Vulnerabilities

### JavaScript/TypeScript

| Vulnerability       | Pattern                    | Fix                              |
| ------------------- | -------------------------- | -------------------------------- |
| XSS                 | `innerHTML = userInput`    | `textContent` or sanitize        |
| Prototype Pollution | `merge(obj, userInput)`    | Freeze prototypes, validate keys |
| eval()              | `eval(userCode)`           | Use safer alternatives           |
| ReDoS               | Complex regex + user input | Limit input, timeout regex       |

### Python

| Vulnerability   | Pattern                   | Fix                          |
| --------------- | ------------------------- | ---------------------------- |
| Pickle RCE      | `pickle.loads(userData)`  | Use JSON, validate source    |
| exec/eval       | `exec(userCode)`          | Never execute user input     |
| Shell injection | `os.system(f"cmd {arg}")` | `subprocess.run([...])`      |
| Path traversal  | `open(user_path)`         | Validate path, use allowlist |

### Go

| Vulnerability  | Pattern                | Fix                    |
| -------------- | ---------------------- | ---------------------- |
| Race condition | Concurrent map access  | sync.Mutex or sync.Map |
| Panic exposure | Unhandled panic        | recover() in handlers  |
| SQL injection  | String concat in query | Parameterized queries  |
| SSRF           | Unvalidated URL fetch  | Validate hostname      |

### Java

| Vulnerability   | Pattern                      | Fix                           |
| --------------- | ---------------------------- | ----------------------------- |
| Deserialization | ObjectInputStream.readObject | Validate class, use allowlist |
| JNDI injection  | lookup(userInput)            | Disable remote lookup         |
| XXE             | DOM parsing                  | Disable DTD                   |
| SQL injection   | Statement.execute            | PreparedStatement             |

## Quick Reference Severity

| Finding                     | Severity |
| --------------------------- | -------- |
| RCE (Remote Code Execution) | Critical |
| SQL/NoSQL Injection         | Critical |
| Authentication Bypass       | Critical |
| Hardcoded Secrets           | High     |
| XSS (Stored)                | High     |
| XSS (Reflected)             | Medium   |
| Missing rate limiting       | Medium   |
| Verbose error messages      | Low      |
| Missing security headers    | Low      |
