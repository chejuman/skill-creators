# Best Practices Reference

Guidelines for spec-driven development workflow.

## Intent Discovery

### Ask the Right Questions

1. **Core Purpose** - Why does this feature exist?
2. **Target Users** - Who will use it?
3. **Success Criteria** - How do we measure success?
4. **Constraints** - What limitations exist?

### Listen for Implicit Needs

| User Says            | Might Mean                       |
| -------------------- | -------------------------------- |
| "Simple login"       | OAuth + session + remember me    |
| "Fast API"           | < 100ms p99, caching, CDN        |
| "Secure payment"     | PCI compliance, encryption       |
| "User-friendly form" | Validation, error handling, a11y |

## Requirements Writing

### DO

- One requirement per statement
- Use measurable terms (numbers, not adjectives)
- Include all edge cases
- Reference related requirements

### DON'T

- Combine multiple requirements
- Use vague terms ("fast", "easy", "user-friendly")
- Assume context
- Skip error scenarios

### Quality Metrics

| Metric       | Target |
| ------------ | ------ |
| Clarity      | 9/10   |
| Testability  | 9/10   |
| Completeness | 8/10   |
| Consistency  | 9/10   |

## Design Principles

### Architecture Decisions

Document every significant decision:

```markdown
## ADR-001: Use JWT for Authentication

### Context

Need stateless authentication for microservices.

### Decision

Use JWT with RS256 signing.

### Consequences

- Pro: Stateless, scalable
- Con: Token revocation complexity
```

### Component Design

- Single Responsibility
- Clear interfaces
- Dependency injection
- Error boundaries

## Task Breakdown

### Atomic Tasks

Each task should:

- Have ONE clear objective
- Take 1-2 hours maximum
- Be independently testable
- Produce visible progress

### Dependencies

- Minimize cross-task dependencies
- Identify parallel opportunities
- Document blocking relationships
- Plan for failure scenarios

## Verification

### Pre-Task Checklist

- [ ] Previous task completed?
- [ ] Dependencies resolved?
- [ ] Context loaded?
- [ ] Tests defined?

### Post-Task Checklist

- [ ] All files created?
- [ ] Tests passing?
- [ ] Acceptance criteria met?
- [ ] Documentation updated?

## Common Pitfalls

| Pitfall               | Solution                  |
| --------------------- | ------------------------- |
| Scope creep           | Strict out-of-scope list  |
| Vague requirements    | Use EARS format           |
| Missing edge cases    | Research + user questions |
| Over-engineering      | MVP mindset               |
| Skipping verification | Enforce pre-task checks   |
| Ignoring research     | WebSearch before spec     |

## Research Integration

### When to Research

- Before writing requirements
- Before design decisions
- When encountering unfamiliar domain
- When multiple approaches exist

### What to Research

- Best practices 2025
- Common implementation patterns
- Security considerations
- Performance benchmarks
- Similar open-source implementations
