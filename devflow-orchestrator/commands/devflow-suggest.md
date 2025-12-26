# /devflow-suggest

Get AI-generated feature suggestions with RICE/MoSCoW scoring.

## Usage

```
/devflow-suggest [--count N]
```

## Options

- `--count N`: Number of suggestions (default: 5)

## What This Does

### Step 1: Load Context

Load project state and research findings from `.devflow/`.

### Step 2: Analyze Research

Synthesize research to identify feature opportunities:

- Market gaps
- Competitor weaknesses
- User needs
- Technical possibilities

### Step 3: Generate Suggestions

Generate 5-10 feature suggestions with initial RICE scores.

### Step 4: Interactive Selection

Use AskUserQuestion for feature selection:

```
AskUserQuestion(questions=[
  {
    "question": "Select features for next version:",
    "header": "Features",
    "options": [
      {
        "label": "Feature A (Recommended)",
        "description": "RICE: 150 | Must-have for MVP"
      },
      {
        "label": "Feature B",
        "description": "RICE: 120 | High user impact"
      },
      {
        "label": "Feature C",
        "description": "RICE: 100 | Competitive advantage"
      },
      {
        "label": "Feature D",
        "description": "RICE: 80 | Nice to have"
      }
    ],
    "multiSelect": true
  },
  {
    "question": "MoSCoW priority for selected features?",
    "header": "Priority",
    "options": [
      {"label": "Must have", "description": "Critical for this version"},
      {"label": "Should have", "description": "Important but not vital"},
      {"label": "Could have", "description": "Nice to have"}
    ],
    "multiSelect": false
  }
])
```

### Step 5: Save to Backlog

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/feature_scorer.py add "<name>" "<description>" <reach> <impact> <confidence> <effort> <moscow>
```

### Step 6: Log Decision

```bash
python3 ~/.claude/skills/devflow-orchestrator/scripts/state_manager.py log_decision "<selected features>" "<user rationale>"
```

### Output

```markdown
## Feature Suggestions for v{X}.0

| Feature   | RICE | Priority | Status   |
| --------- | ---- | -------- | -------- |
| Feature A | 150  | Must     | Selected |
| Feature B | 120  | Should   | Selected |
| Feature C | 100  | Could    | -        |

### Selected for v{X}.0

1. **Feature A** - [description]
2. **Feature B** - [description]

### Next Steps

1. `/devflow-plan` - Generate development plan
2. `/devflow-suggest` - Get more suggestions
```

## Example

```
User: /devflow-suggest

User: /devflow-suggest --count 10
```
