# /devflow2-suggest

Get AI-powered feature suggestions with RICE++ scoring and interactive refinement.

## Usage

```
/devflow2-suggest [--count N] [--refine]
```

## Options

- `--count N`: Number of suggestions (default: 5)
- `--refine`: Enable multi-turn refinement loop

## What This Does

### Step 1: Load Context

Load research synthesis, analysis results, and existing backlog.

### Step 2: Generate Feature Suggestions

AI synthesizes research and analysis to suggest features:

- Gap opportunities from competitor analysis
- User needs from UX analysis
- Technical capabilities from tech research
- Market trends from market analysis

### Step 3: RICE++ Scoring

Enhanced scoring with confidence intervals:

```
RICE++ = (Reach × Impact × Confidence × Urgency) / (Effort × Risk)

Where:
- Reach: 1-1000 users affected
- Impact: 0.25-3 effect per user
- Confidence: 0-100% certainty
- Urgency: 0.5-2.0 time sensitivity
- Effort: 1-12 person-months
- Risk: 0.5-2.0 implementation risk
```

### Step 4: Interactive Feature Selection

```
AskUserQuestion(questions=[
  {
    "question": "Select features for next version:",
    "header": "Features",
    "options": [
      {"label": "Feature A (RICE++: 180)", "description": "Must-have: Core functionality"},
      {"label": "Feature B (RICE++: 150)", "description": "Should-have: High user impact"},
      {"label": "Feature C (RICE++: 120)", "description": "Could-have: Competitive advantage"},
      {"label": "Feature D (RICE++: 90)", "description": "Could-have: Nice to have"}
    ],
    "multiSelect": true
  }
])
```

### Step 5: Refinement Loop (if --refine)

```
AskUserQuestion(questions=[
  {
    "question": "Refine selected features?",
    "header": "Refine",
    "options": [
      {"label": "Finalize selection", "description": "Proceed with current selection"},
      {"label": "Add more features", "description": "See additional suggestions"},
      {"label": "Remove features", "description": "Reduce scope"},
      {"label": "Adjust priorities", "description": "Change MoSCoW priorities"}
    ],
    "multiSelect": false
  }
])
```

### Step 6: Save to Backlog

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/feature_scorer.py add ...
```

### Output

```markdown
## Feature Suggestions for v{X}.0

### Top Recommendations

| Rank | Feature   | RICE++ | Urgency | Risk   | Priority |
| ---- | --------- | ------ | ------- | ------ | -------- |
| 1    | Feature A | 180    | High    | Low    | Must     |
| 2    | Feature B | 150    | Medium  | Low    | Should   |
| 3    | Feature C | 120    | Low     | Medium | Could    |

### Selected Features

1. **Feature A** [Must]
   - RICE++: 180 (Confidence: 85%)
   - Description: ...
   - User Value: ...

2. **Feature B** [Should]
   - RICE++: 150 (Confidence: 70%)
   - Description: ...
   - User Value: ...

### Selection Summary

- Total Features: 2
- Combined Effort: 4 person-months
- Expected Impact: High

### Next Steps

1. `/devflow2-plan` - Generate development plan
2. `/devflow2-suggest --refine` - Refine selection
```

## Example

```
/devflow2-suggest

/devflow2-suggest --count 10 --refine
```
