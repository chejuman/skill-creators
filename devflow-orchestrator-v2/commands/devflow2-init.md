# /devflow2-init

Initialize premium DevFlow V2 project with intelligent domain detection.

## Usage

```
/devflow2-init <idea> [domain] [complexity]
```

## Arguments

- `idea` (required): Project idea or concept
- `domain` (optional): Override auto-detected domain
- `complexity` (optional): Override complexity level (1-5)

## What This Does

### Step 1: Domain Detection

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/master.py detect "<idea>"
```

Auto-detects domain from keywords: devops, security, webdev, dataops, mobile, enterprise.

### Step 2: Complexity Assessment

Analyzes idea for complexity indicators:

- Level 1-2: Simple/basic projects
- Level 3: Standard projects
- Level 4-5: Complex/enterprise projects

### Step 3: Project Initialization

```bash
python3 ~/.claude/skills/devflow-orchestrator-v2/scripts/orchestrators/master.py init "<idea>" "<domain>" <complexity>
```

Creates enhanced `.devflow/` structure with:

- Research directories per domain
- Analytics tracking
- Knowledge base initialization
- Quality gate configuration

### Step 4: Interactive Confirmation

```
AskUserQuestion(questions=[
  {
    "question": "Confirm detected settings?",
    "header": "Settings",
    "options": [
      {"label": "Yes, proceed (Recommended)", "description": "Use detected domain and complexity"},
      {"label": "Change domain", "description": "Override detected domain"},
      {"label": "Change complexity", "description": "Override complexity level"}
    ],
    "multiSelect": false
  }
])
```

### Output

```markdown
# DevFlow V2 Project Initialized

## Project Details

| Field       | Value                    |
| ----------- | ------------------------ |
| Idea        | {idea}                   |
| Domain      | {domain} (auto-detected) |
| Complexity  | Level {level}/5          |
| Agent Count | {count}                  |
| Version     | v0.0 (Idea Stage)        |
| Target      | v10.0+                   |

## Premium Features Enabled

- [x] Hierarchical multi-agent research
- [x] Quality gates at each phase
- [x] Predictive analytics
- [x] Knowledge accumulation
- [x] Source credibility tracking

## Next Steps

1. `/devflow2-research` - Run hierarchical research
2. `/devflow2-status` - View analytics dashboard
```

## Example

```
/devflow2-init "AI-powered code review tool with security scanning" devops

/devflow2-init "Real-time collaboration platform for remote teams"
```
