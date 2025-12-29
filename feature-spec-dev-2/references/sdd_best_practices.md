# Spec-Driven Development Best Practices 2025

## Core Principles

### 1. Specs Before Code

- Write specifications FIRST, then generate code
- Specs become the executable source of truth
- Version control specifications like code

### 2. Precise Intent Capture

- Capture explicit AND implicit requirements
- Define success criteria measurably
- Document assumptions and constraints

### 3. Iterative Refinement

- Expect 2-3 iterations for production quality
- Break work into 3-4 task chunks
- Request code review every 3-4 tasks

## Workflow Phases

```
┌──────────────────────────────────────────────┐
│ 1. WRITE SPEC    Define scope, intent       │
├──────────────────────────────────────────────┤
│ 2. GENERATE PLAN Derive implementation steps│
├──────────────────────────────────────────────┤
│ 3. EXECUTE       Perform tasks safely       │
├──────────────────────────────────────────────┤
│ 4. VERIFY        Validate against spec      │
└──────────────────────────────────────────────┘
```

## Intent Analysis Techniques

### Surface-Level

- What the user explicitly stated
- Direct feature requests

### Implicit Requirements

- Industry standards compliance
- Security best practices
- Error handling expectations
- Testing requirements

### Deep Intent

- Business goals behind the request
- Future scalability needs
- Integration requirements
- Non-functional expectations

## Common Pitfalls

| Pitfall               | Solution                     |
| --------------------- | ---------------------------- |
| Vague specs           | Use EARS format              |
| Missing edge cases    | Enumerate failure modes      |
| Outdated specs        | Maintain as living documents |
| Over-engineering      | Focus on current needs       |
| Skipping verification | Always validate completion   |

## Research Integration

Before finalizing any spec phase:

1. **Tech Trends**: Search "{domain} best practices 2025"
2. **Similar Cases**: Find open source implementations
3. **API Docs**: Research relevant libraries

## Verification Checklist

- [ ] All acceptance criteria checkable
- [ ] Files exist and are non-empty
- [ ] Tests written and passing
- [ ] No TypeScript/lint errors
- [ ] Matches project conventions
