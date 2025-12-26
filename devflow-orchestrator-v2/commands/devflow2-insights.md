# /devflow2-insights

Query and manage the knowledge base.

## Usage

```
/devflow2-insights <command> [args]
```

## Commands

- `query <term>`: Search knowledge base
- `patterns`: List accumulated patterns
- `recommend`: Get recommendations
- `add-pattern`: Add new pattern
- `add-insight`: Add domain insight

## What This Does

### Query Knowledge

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/knowledge_base.py query "<term>"
```

### List Patterns

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/knowledge_base.py list patterns
```

### Get Recommendations

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/knowledge_base.py recommend
```

### Output (Query)

```markdown
## Knowledge Query: "authentication"

### Matching Patterns

| ID      | Pattern            | Confidence | Domain   |
| ------- | ------------------ | ---------- | -------- |
| PAT-003 | JWT Token Strategy | 0.9        | security |
| PAT-007 | Session Management | 0.8        | webdev   |

### Matching Anti-Patterns

| ID       | Anti-Pattern         | Consequence     |
| -------- | -------------------- | --------------- |
| ANTI-002 | Plain Text Passwords | Security breach |

### Domain Insights

- "OAuth 2.0 preferred for third-party auth" (source: research v2.0)
- "MFA becoming standard requirement" (source: security research)
```

### Output (Recommendations)

```markdown
## Knowledge Recommendations

### Patterns to Apply

1. **PAT-001**: Research-First Approach
   - Confidence: 0.95
   - Used: 5 times
   - Context: Start with comprehensive research

2. **PAT-002**: RICE++ Scoring
   - Confidence: 0.90
   - Used: 4 times
   - Context: Feature prioritization

### Anti-Patterns to Avoid

1. **ANTI-001**: Scope Creep
   - Consequence: Timeline delays
   - Alternative: Fixed scope per version

### Domain Insights (webdev)

1. React + TypeScript dominates frontend (2025)
2. Server components gaining adoption
3. Edge computing for performance

### Source Credibility Summary

| Source Type       | Count | Avg Rating |
| ----------------- | ----- | ---------- |
| Official Docs     | 15    | 1.0        |
| Tech Publications | 23    | 0.8        |
| Community         | 12    | 0.6        |
```

### Interactive Pattern Addition

```
AskUserQuestion(questions=[
  {
    "question": "Pattern category?",
    "header": "Category",
    "options": [
      {"label": "Architecture", "description": "System design patterns"},
      {"label": "Process", "description": "Workflow patterns"},
      {"label": "Technical", "description": "Implementation patterns"},
      {"label": "Research", "description": "Research methodology"}
    ],
    "multiSelect": false
  }
])
```

Then:

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/generators/knowledge_base.py pattern "<name>" "<description>" "<context>"
```

## Example

```
/devflow2-insights query authentication

/devflow2-insights patterns

/devflow2-insights recommend

/devflow2-insights add-pattern "API Versioning" "Use URL versioning for APIs" "REST API design"
```
