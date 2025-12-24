# Severity Labels Reference

Standard labels for code review comments.

## Severity Levels

### Critical (Blocking)

**Emoji:** `🔴`
**Label:** `[Critical]`
**Action:** Must fix before merge

**Use for:**

- Security vulnerabilities (RCE, injection, auth bypass)
- Data loss or corruption risks
- Production-breaking bugs
- Compliance violations

**Example:**

```
🔴 [Security/Critical] SQL Injection Vulnerability
File: src/db/users.ts:42
This code is vulnerable to SQL injection attacks.
```

### High Priority

**Emoji:** `🟠`
**Label:** `[High]`
**Action:** Should fix before merge, discuss if disagree

**Use for:**

- Major bugs
- Significant performance issues
- Security issues (non-critical)
- Architectural violations

**Example:**

```
🟠 [Performance/High] N+1 Query Pattern
File: src/services/orders.ts:89
This loop generates N+1 database queries.
```

### Medium Priority

**Emoji:** `🟡`
**Label:** `[Medium]`
**Action:** Should address, may defer with justification

**Use for:**

- Code smells
- Maintainability issues
- Minor performance concerns
- Missing error handling

**Example:**

```
🟡 [Architecture/Medium] SRP Violation
File: src/controllers/user.ts:15
This controller handles both auth and user management.
```

### Low Priority

**Emoji:** `🟢`
**Label:** `[Low]`
**Action:** Nice to have, not blocking

**Use for:**

- Minor improvements
- Style suggestions
- Documentation gaps
- Naming improvements

**Example:**

```
🟢 [Practices/Low] Variable Naming
File: src/utils/calc.ts:23
Consider renaming 'x' to 'priceBeforeTax' for clarity.
```

### Info (Educational)

**Emoji:** `💡`
**Label:** `[Info]`
**Action:** FYI, no action required

**Use for:**

- Alternative approaches
- Learning opportunities
- Future considerations
- Context sharing

**Example:**

```
💡 [Practices/Info] Alternative Approach
File: src/utils/format.ts:45
You could also use Intl.DateTimeFormat here for i18n support.
```

### Praise

**Emoji:** `🎉`
**Label:** `[Praise]`
**Action:** Recognition of good work

**Use for:**

- Excellent code quality
- Good pattern usage
- Thorough error handling
- Clear documentation

**Example:**

```
🎉 [Practices/Praise] Excellent Error Handling
File: src/api/client.ts:67
Great job implementing retry logic with exponential backoff!
```

## Category Labels

### Security

- `[Security/Injection]` - SQL, NoSQL, Command injection
- `[Security/Auth]` - Authentication/Authorization
- `[Security/XSS]` - Cross-site scripting
- `[Security/CSRF]` - Cross-site request forgery
- `[Security/Exposure]` - Sensitive data exposure
- `[Security/Config]` - Security misconfiguration

### Performance

- `[Performance/Complexity]` - Algorithmic complexity
- `[Performance/Database]` - Database queries
- `[Performance/Memory]` - Memory efficiency
- `[Performance/IO]` - I/O operations
- `[Performance/Bundle]` - Bundle size (frontend)

### Architecture

- `[Architecture/SOLID]` - SOLID principle violation
- `[Architecture/Pattern]` - Design pattern issue
- `[Architecture/Layer]` - Layer violation
- `[Architecture/Coupling]` - Tight coupling
- `[Architecture/API]` - API design

### Best Practices

- `[Practices/Readability]` - Code readability
- `[Practices/Errors]` - Error handling
- `[Practices/Types]` - Type safety
- `[Practices/DRY]` - Code duplication
- `[Practices/Tests]` - Testing
- `[Practices/Docs]` - Documentation

## Inline Comment Format

````
📍 {file}:{line}
{emoji} [{category}/{severity}] {title}
   {description}

   Current:
   ```{lang}
   {current_code}
````

Suggested:

```{lang}
{suggested_code}
```

Reference: {cwe_or_doc_link}

```

## Quick Reference

| Severity | Emoji | Blocking | Action |
|----------|-------|----------|--------|
| Critical | 🔴 | Yes | Must fix |
| High | 🟠 | Yes | Should fix |
| Medium | 🟡 | No | Should address |
| Low | 🟢 | No | Nice to have |
| Info | 💡 | No | FYI only |
| Praise | 🎉 | No | Recognition |
```
