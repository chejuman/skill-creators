---
name: tech-debt-workflow
description: Analyze a codebase for technical debt and implement prioritized fixes using a multi-pass workflow. Use when asked to identify tech debt, refactor, clean up legacy code, reduce complexity, remove duplication, improve maintainability, or reduce long-term risk.
---

# Technical Debt Workflow

Analyze a repo for technical debt, prioritize fixes, and apply safe, incremental changes.

## Quick triage

1. Confirm scope: whole repo vs specific area.
2. Confirm change appetite: report-only vs fix-now.
3. Confirm constraints: time budget, testing requirements, risk tolerance.
4. Ask about frozen areas (files or dirs you must not touch).

## Workflow

### 1) Discovery pass

- Read AGENTS.md and project docs for constraints.
- Check git status to avoid unintentional changes.
- Collect signals:
  - `rg -n "TODO|FIXME|HACK|XXX"`
  - `rg -n "deprecated|legacy|workaround"`
  - Find hotspots: large files, deep nesting, duplicated logic.
- Summarize current debt surface in categories (see references).

### 2) Prioritization pass

Score each debt item using:
- Impact (user risk, stability, security)
- Effort (estimated time, files touched)
- Confidence (clarity of fix)

Select top 3–5 items for action unless user requests full report.

### 3) Plan pass

For each chosen item:
- Define target behavior
- Identify files to change
- Choose minimal safe refactor
- Define tests or verification steps

### 4) Fix pass

Apply changes in small, reviewable commits:
- Keep scope tight
- Preserve behavior
- Update tests or add coverage where needed
 - Avoid introducing new dependencies unless approved

### 5) Review pass

Check for:
- Regressions or behavior changes
- Style/consistency issues
- Missing tests

### 6) Report

Provide:
- Debt items found
- What was fixed
- Remaining risks
- Suggested next steps
 - Clear install/verification notes if new scripts were added

## Multi-pass roles (single session)

Simulate multi-agent work by running structured passes in sequence. Use compact, deterministic outputs. See `references/agent_prompts.md`.

## Output formats

- **Report-only**: findings + prioritized backlog
- **Fix-now**: apply top items + tests
- **Hybrid**: fix top 1–2 items, backlog the rest

## Safety rules

- Avoid large refactors without explicit approval.
- Do not delete functionality unless requested.
- Prefer small, reversible changes.
- Run tests when available; note if skipped.
 - Avoid touching generated files unless necessary.
 - If risk is unclear, return a report-only recommendation.

## References

- `references/debt_checklist.md` for debt categories and signals.
- `references/agent_prompts.md` for role-based passes.
- `references/output_templates.md` for report formats.
