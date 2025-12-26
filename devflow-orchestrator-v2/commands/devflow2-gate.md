# /devflow2-gate

Run quality gate validation for workflow phases.

## Usage

```
/devflow2-gate <gate_name> [--report]
```

## Arguments

- `gate_name` (required): Gate to validate
  - `research_complete`: Validate research phase
  - `analysis_complete`: Validate analysis phase
  - `plan_validated`: Validate planning phase
  - `version_ready`: Validate version readiness

## Options

- `--report`: Generate full quality report

## What This Does

### Step 1: Run Gate Checks

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/quality_gate.py run <gate_name>
```

### Step 2: Evaluate Checks

Each gate has specific checks:

**research_complete**:

- [ ] Tech stack research exists
- [ ] Market trends research exists
- [ ] Open source research exists
- [ ] Security research exists
- [ ] Competitor research exists
- [ ] Synthesis exists (optional)

**analysis_complete**:

- [ ] User perspective analysis
- [ ] Technical perspective analysis
- [ ] Business perspective analysis
- [ ] Risk perspective analysis
- [ ] Feasibility score calculated

**plan_validated**:

- [ ] Features selected
- [ ] Tasks generated
- [ ] Dependencies mapped
- [ ] Risks identified (optional)
- [ ] Effort estimated

**version_ready**:

- [ ] All previous gates passed
- [ ] Retrospective done (optional)
- [ ] Knowledge updated (optional)

### Step 3: Calculate Pass Rate

Gate passes if:

1. All required checks pass
2. Overall pass rate >= minimum threshold

### Output (Pass)

```markdown
## Quality Gate: research_complete

### Status: ✅ PASSED

| Check                  | Status | Required |
| ---------------------- | ------ | -------- |
| tech_stack_research    | ✅     | Yes      |
| market_trends_research | ✅     | Yes      |
| open_source_research   | ✅     | Yes      |
| security_research      | ✅     | Yes      |
| competitor_research    | ✅     | Yes      |
| synthesis_exists       | ❌     | No       |

### Summary

- Pass Rate: 83.3%
- Required Rate: 80%
- All Required Checks: ✅

### Next Phase

Proceed to `/devflow2-analyze`
```

### Output (Fail)

```markdown
## Quality Gate: research_complete

### Status: ❌ FAILED

| Check                  | Status | Required |
| ---------------------- | ------ | -------- |
| tech_stack_research    | ✅     | Yes      |
| market_trends_research | ❌     | Yes      |
| open_source_research   | ❌     | Yes      |
| security_research      | ✅     | Yes      |
| competitor_research    | ❌     | Yes      |

### Summary

- Pass Rate: 40%
- Required Rate: 80%
- Missing Required: market_trends, open_source, competitor

### Action Required

Complete missing research before proceeding:

1. Run `/devflow2-research --focus market`
2. Run `/devflow2-research --focus opensource`
3. Run `/devflow2-research --focus competitors`

Then retry: `/devflow2-gate research_complete`
```

### Full Report (--report)

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/quality_gate.py report
```

## Example

```
/devflow2-gate research_complete

/devflow2-gate analysis_complete --report

/devflow2-gate version_ready
```
