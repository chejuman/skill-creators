# Output Templates

Use one of these formats based on requested mode.

## Report-only

```
# Technical Debt Report

## Scope
- Area: <path or repo>
- Constraints: <notes>

## Findings (Prioritized)
1. <Category> — <short title>
   - Location: <path:line>
   - Impact: <high|medium|low>
   - Effort: <high|medium|low>
   - Confidence: <high|medium|low>
   - Rationale: <1-2 lines>

## Backlog
- <item> — <impact/effort/confidence>

## Suggested Next Steps
- <step>
```

## Fix-now

```
# Technical Debt Fix Summary

## Scope
- Area: <path or repo>
- Constraints: <notes>

## Fixes Applied
1. <Category> — <short title>
   - Files: <list>
   - Change: <1-2 lines>
   - Tests: <ran|skipped> <command>

## Remaining Debt
- <item> — <reason>

## Risks / Follow-ups
- <risk>
```

## Hybrid

```
# Technical Debt Report + Fixes

## Fixes Applied (Top 1–2)
1. <Category> — <short title>
   - Files: <list>
   - Change: <1-2 lines>
   - Tests: <ran|skipped> <command>

## Prioritized Backlog
1. <Category> — <short title> (impact/effort/confidence)
2. <...>

## Next Steps
- <step>
```
