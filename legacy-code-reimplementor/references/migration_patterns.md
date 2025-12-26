# Migration Patterns & Anti-Patterns

Best practices for iterative codebase reimplementation.

## Proven Migration Patterns

### 1. Strangler Fig Pattern

Gradually replace legacy components while keeping system functional.

```
Phase 1: New code handles new features
Phase 2: Redirect existing features to new code
Phase 3: Sunset legacy components
```

**When to use:** Production systems that can't have downtime.

### 2. Big Bang with Parallel Run

Build complete new system, run both in parallel, switch over.

```
Phase 1: Complete new implementation
Phase 2: Run both systems, compare outputs
Phase 3: Cutover with rollback plan
```

**When to use:** Smaller systems or major architectural changes.

### 3. Feature-by-Feature Migration

Migrate one feature/module at a time to new stack.

```
Stage 1: Core utilities and config
Stage 2: Data layer and repositories
Stage 3: Business logic services
Stage 4: API/presentation layer
Stage 5: Integration and migration scripts
```

**When to use:** Most reimplementation projects (this skill's default).

## Module Dependency Order

Always migrate in dependency order to avoid circular issues:

```
1. Pure utilities (no dependencies)
2. Configuration/constants
3. Domain models/entities
4. Repository interfaces
5. Repository implementations
6. Service interfaces
7. Service implementations
8. Controllers/handlers
9. Integration layers
10. Entry points
```

## Anti-Patterns to Avoid

### 1. Big Rewrite Without Analysis

**Problem:** Starting to code without understanding the original.
**Solution:** Complete Phase 1 analysis before any implementation.

### 2. Changing Too Much at Once

**Problem:** New language + new framework + new architecture + new patterns.
**Solution:** Change one major thing at a time when possible.

### 3. Ignoring Edge Cases

**Problem:** Missing obscure but critical functionality from original.
**Solution:** Extract ALL edge cases during analysis, test each explicitly.

### 4. Premature Optimization

**Problem:** Over-engineering the new system before it works.
**Solution:** First make it work, then make it right, then make it fast.

### 5. Skipping Tests

**Problem:** No way to verify functionality matches original.
**Solution:** Write tests BEFORE implementing each module.

### 6. Manual Translation

**Problem:** Copy-paste-translate loses intent and introduces bugs.
**Solution:** Understand the intent, implement idiomatically in new language.

## Test Strategy

### Test Pyramid for Migration

```
         /\
        /  \  E2E (few, critical paths)
       /----\
      /      \ Integration (API contracts)
     /--------\
    /          \ Unit (comprehensive)
   /-----------+\
```

### Golden Master Testing

1. Capture original system outputs for all inputs
2. Run same inputs through new implementation
3. Compare outputs programmatically
4. Document and justify any differences

## Security During Migration

### Must Verify

- [ ] Authentication mechanisms work identically
- [ ] Authorization rules enforced correctly
- [ ] Input validation at least as strict
- [ ] No new injection vulnerabilities
- [ ] Secrets handling improved (not degraded)
- [ ] Audit logging maintained

### Common Security Upgrades

| Legacy Pattern     | Modern Pattern              |
| ------------------ | --------------------------- |
| MD5/SHA1 passwords | bcrypt/argon2               |
| Hardcoded secrets  | Environment variables/vault |
| Session cookies    | JWT with refresh tokens     |
| SQL string concat  | Parameterized queries       |
| eval/exec          | Safe alternatives           |

## Progress Tracking Template

```markdown
## Stage N Progress

### Completed

- [x] Module A implemented
- [x] Module A tests passing
- [x] Module B implemented

### In Progress

- [ ] Module B tests (80% done)

### Blocked

- Module C waiting on external API spec

### Metrics

- Functions: 45/60 implemented (75%)
- Tests: 120 passing, 5 failing
- Coverage: 82%
```

## Rollback Strategy

Always maintain ability to rollback:

1. Keep original system running until validation complete
2. Use feature flags for gradual rollout
3. Maintain database compatibility during transition
4. Document rollback procedures for each stage
