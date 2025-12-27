# Retrospective Frameworks Reference

Detailed guide for each retrospective framework supported by retrospective-v2.

## Framework Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│ Quick sprint reflection?                                    │
│   YES → Start-Stop-Continue                                 │
│   NO ↓                                                      │
├─────────────────────────────────────────────────────────────┤
│ Focus on learning and growth?                               │
│   YES → 4 Ls                                                │
│   NO ↓                                                      │
├─────────────────────────────────────────────────────────────┤
│ Process optimization needed?                                │
│   YES → DAKI                                                │
│   NO ↓                                                      │
├─────────────────────────────────────────────────────────────┤
│ Incident/failure analysis?                                  │
│   YES → 5 Whys                                              │
│   NO ↓                                                      │
├─────────────────────────────────────────────────────────────┤
│ Technical debt focus?                                       │
│   YES → Code Quality                                        │
│   NO → Start-Stop-Continue (default)                        │
└─────────────────────────────────────────────────────────────┘
```

## 1. Start-Stop-Continue (SSC)

**ID:** `ssc`
**Best For:** Quick sprints, action-oriented teams
**Time Required:** 15-30 minutes

### Structure

| Category | Question                    | Action Focus      |
| -------- | --------------------------- | ----------------- |
| START    | What should we begin doing? | New practices     |
| STOP     | What should we stop doing?  | Eliminate waste   |
| CONTINUE | What's working well?        | Reinforce success |

### Example Output

```markdown
#### START

- **Automated testing for API endpoints**
  - Evidence: 3 bugs in production from untested endpoints
  - Impact: High - Reduces production incidents
  - Action: Add integration tests for /api/v2/\* routes

#### STOP

- **Manual deployment to staging**
  - Evidence: Average 45 min per deployment, 2 failed deploys this sprint
  - Impact: Medium - Saves time, reduces errors
  - Action: Implement CI/CD pipeline for staging

#### CONTINUE

- **Daily standups at 9:30 AM**
  - Evidence: Team alignment improved, blockers resolved faster
  - Impact: High - Maintain team synchronization
  - Action: Keep format, consider async option for remote days
```

### When to Use

- Sprint retrospectives
- Quick team check-ins
- Agile ceremonies
- New team formation

---

## 2. Four L's (4Ls)

**ID:** `4ls`
**Best For:** Learning focus, capability development
**Time Required:** 30-45 minutes

### Structure

| Category   | Question                | Focus                |
| ---------- | ----------------------- | -------------------- |
| LIKED      | What did we enjoy?      | Positive experiences |
| LEARNED    | What did we learn?      | Knowledge gained     |
| LACKED     | What was missing?       | Gaps identified      |
| LONGED FOR | What do we wish we had? | Future desires       |

### Example Output

```markdown
#### LIKED

- **Pair programming on complex features**
  - Evidence: Auth module completed 30% faster than estimated
  - Insight: Knowledge sharing accelerated development

#### LEARNED

- **GraphQL subscriptions for real-time updates**
  - Evidence: Implemented WebSocket fallback pattern
  - Insight: Document patterns for future reference

#### LACKED

- **Clear acceptance criteria for user stories**
  - Evidence: 40% of stories required clarification mid-sprint
  - Gap: Product-dev communication

#### LONGED FOR

- **Dedicated time for technical exploration**
  - Desire: Innovation sprints or 20% time
  - Benefit: Reduce tech debt, improve morale
```

### When to Use

- Team development
- Onboarding retrospectives
- Skill gap analysis
- Quarterly reviews

---

## 3. DAKI (Drop-Add-Keep-Improve)

**ID:** `daki`
**Best For:** Process optimization, workflow refinement
**Time Required:** 30-45 minutes

### Structure

| Category | Action            | Focus           |
| -------- | ----------------- | --------------- |
| DROP     | Remove completely | Eliminate waste |
| ADD      | Introduce new     | New practices   |
| KEEP     | Maintain as-is    | Preserve value  |
| IMPROVE  | Enhance existing  | Optimize        |

### Example Output

```markdown
#### DROP

- **Weekly status report emails**
  - Reason: Duplicates Jira dashboard information
  - Impact: Save 2 hours/week team-wide

#### ADD

- **Pre-commit hooks for linting**
  - Reason: Catch style issues before PR review
  - Impact: Reduce PR review cycles by 40%

#### KEEP

- **Friday demo sessions**
  - Reason: Stakeholder visibility, team morale
  - Value: Maintains alignment with business

#### IMPROVE

- **Code review turnaround time**
  - Current: 24-48 hours average
  - Target: < 4 hours during business hours
  - How: Rotate primary reviewer daily
```

### When to Use

- Process audits
- Workflow optimization
- Team efficiency reviews
- Continuous improvement cycles

---

## 4. Five Whys (Root Cause Analysis)

**ID:** `5whys`
**Best For:** Incident post-mortems, failure analysis
**Time Required:** 45-60 minutes

### Structure

Recursively ask "Why?" to reach root cause:

```
Problem → Why? (L1) → Why? (L2) → Why? (L3) → Why? (L4) → Why? (L5) → Root Cause
```

### Example Output

```markdown
#### Issue: Production outage on Dec 15

**Why 1:** Database connection pool exhausted
**Why 2:** Connections not being released properly
**Why 3:** Exception handler missing connection cleanup
**Why 4:** Error handling pattern inconsistent across codebase
**Why 5:** No established error handling guidelines

**Root Cause:** Missing architectural standards for error handling

**Preventive Actions:**

1. [ ] Create error handling guidelines document
2. [ ] Add connection cleanup to base repository class
3. [ ] Implement connection pool monitoring alerts
4. [ ] Add integration test for connection leak scenarios
```

### Facilitation Tips

- Focus on systems, not people
- Stop when you reach actionable root cause
- May not always need exactly 5 levels
- Document the chain for future reference

### When to Use

- Production incidents
- Major bugs
- Missed deadlines
- Process failures

---

## 5. Code Quality Focus

**ID:** `quality`
**Best For:** Technical debt, architecture review
**Time Required:** 45-60 minutes

### Structure

| Area          | Assessment                 | Focus           |
| ------------- | -------------------------- | --------------- |
| Architecture  | Design patterns, coupling  | Structure       |
| Testing       | Coverage, quality, speed   | Confidence      |
| Documentation | Completeness, accuracy     | Maintainability |
| Performance   | Bottlenecks, optimization  | Efficiency      |
| Security      | Vulnerabilities, practices | Safety          |

### Example Output

```markdown
#### Architecture Assessment

- **Pattern Consistency:** 7/10
  - Issue: Mixed MVC and service layer patterns
  - Recommendation: Standardize on service layer pattern

- **Coupling Score:** 6/10
  - Issue: UserService directly depends on 5 other services
  - Recommendation: Extract shared logic to domain events

#### Testing Assessment

- **Coverage:** 65%
  - Gap: API integration tests missing for /payments/\*
  - Action: Add integration test suite

- **Test Quality:** 7/10
  - Issue: Many tests mock too much, brittle
  - Recommendation: Use test containers for DB tests

#### Technical Debt Inventory

| Item                | Severity | Effort | Priority |
| ------------------- | -------- | ------ | -------- |
| Replace legacy auth | High     | L      | P1       |
| Database indexing   | Medium   | S      | P2       |
| API versioning      | Low      | M      | P3       |
```

### Metrics to Track

- Test coverage percentage
- Cyclomatic complexity
- Code duplication
- Dependency freshness
- Build/deploy time

### When to Use

- Tech debt sprints
- Architecture reviews
- Major refactoring planning
- Team technical health checks

---

## Framework Comparison Matrix

| Aspect    | SSC       | 4Ls       | DAKI      | 5 Whys     | Quality   |
| --------- | --------- | --------- | --------- | ---------- | --------- |
| Time      | 15-30 min | 30-45 min | 30-45 min | 45-60 min  | 45-60 min |
| Focus     | Actions   | Learning  | Process   | Root cause | Technical |
| Depth     | Shallow   | Medium    | Medium    | Deep       | Deep      |
| Team size | Any       | 3-8       | 3-10      | 3-6        | 2-5       |
| Frequency | Weekly    | Bi-weekly | Monthly   | As needed  | Quarterly |

## Combining Frameworks

For comprehensive retrospectives, combine frameworks:

1. **Quick + Deep:** SSC (15 min) → 5 Whys on top issue (30 min)
2. **Learning + Action:** 4Ls (30 min) → SSC for actions (15 min)
3. **Technical + Process:** Quality (45 min) → DAKI for fixes (30 min)
