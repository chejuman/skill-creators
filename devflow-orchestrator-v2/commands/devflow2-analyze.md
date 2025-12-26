# /devflow2-analyze

Run multi-perspective analysis with feasibility scoring.

## Usage

```
/devflow2-analyze [--perspectives <list>]
```

## Options

- `--perspectives`: Comma-separated perspectives (user,technical,business,risk)

## What This Does

### Step 1: Load Research Context

Analysis Coordinator loads synthesized research findings.

### Step 2: Generate Analysis Agents

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/analysis_coordinator.py generate
```

### Step 3: Launch 4 Perspective Agents in Parallel

```
# User Perspective Agent
Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='User perspective analysis',
     prompt='Analyze from user viewpoint: UX, accessibility, needs...')

# Technical Perspective Agent
Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Technical perspective analysis',
     prompt='Evaluate technical feasibility: scalability, maintainability...')

# Business Perspective Agent
Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Business perspective analysis',
     prompt='Evaluate market viability: market fit, ROI, growth...')

# Risk Perspective Agent
Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
     description='Risk perspective analysis',
     prompt='Identify risks: security, compliance, technical debt...')
```

### Step 4: Collect and Synthesize

Collect all perspective analyses and calculate weighted feasibility score:

- User: 25%
- Technical: 30%
- Business: 25%
- Risk: 20%

### Step 5: Generate Risk Matrix

Create risk heatmap with likelihood × impact scoring.

### Step 6: Save Analysis

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/analysis_coordinator.py save "<content>"
```

### Step 7: Quality Gate Check

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/analyzers/quality_gate.py run analysis_complete
```

### Output

```markdown
## Multi-Perspective Analysis Complete

### Feasibility Score: 7.2/10 (72%)

| Perspective | Score | Key Finding         |
| ----------- | ----- | ------------------- |
| User        | 7/10  | Strong UX potential |
| Technical   | 6/10  | Moderate complexity |
| Business    | 8/10  | Good market fit     |
| Risk        | 5/10  | Security concerns   |

### Recommendation

**GO** - Good feasibility with minor concerns

### Risk Matrix

| Risk          | Likelihood | Impact | Priority |
| ------------- | ---------- | ------ | -------- |
| Security gaps | High       | High   | Critical |
| Tech debt     | Medium     | Medium | Medium   |

### Quality Gate: analysis_complete

Status: ✅ PASSED (100%)

### Next Steps

1. `/devflow2-suggest` - Get feature suggestions
2. `/devflow2-gate analysis_complete` - Verify gate
```

## Example

```
/devflow2-analyze

/devflow2-analyze --perspectives user,technical
```
