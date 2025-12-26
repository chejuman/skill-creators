# /reimpl-plan

Start full analysis and generate implementation plan (NO implementation).

## Usage

```
/reimpl-plan <repo-a-path> [repo-b-path]
```

## Arguments

- `repo-a-path` (required): Path to the original/legacy codebase
- `repo-b-path` (optional): Path for the new implementation (for verification later)

## What This Does

This command executes Phases 1-4 of the planning workflow:

### Phase 1: Deep Codebase Analysis

Launch 3 parallel analysis agents:

```
# Agent 1: Structure Analysis
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Analyze codebase structure: modules, packages, dependencies, entry points.',
  description='Structure analysis')

# Agent 2: Feature Extraction
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Extract atomic features: APIs, services, models, utilities.',
  description='Feature extraction')

# Agent 3: Issue Detection
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Identify issues: security, deprecated, tech debt.',
  description='Issue detection')
```

### Phase 2: Technology Selection

Interactive technology selection:

```
AskUserQuestion(questions=[
  {"question": "Target language?", "header": "Language", "options": [...]},
  {"question": "Target framework?", "header": "Framework", "options": [...]},
  {"question": "Architecture pattern?", "header": "Architecture", "options": [...]}
])
```

### Phase 3: Feature Catalog & Dependencies

```bash
python3 ~/.claude/skills/legacy-code-reimplementor-v2/scripts/build_feature_catalog.py {repo-a-path}
```

### Phase 4: Task Generation

```bash
python3 ~/.claude/skills/legacy-code-reimplementor-v2/scripts/generate_tasks.py
```

## Output

All documentation saved to `.reimpl-docs/`:

```
.reimpl-docs/
├── analysis/
│   ├── structure_analysis.md
│   ├── feature_extraction.md
│   ├── feature_catalog.json
│   └── dependency_graph.md
├── plans/
│   ├── implementation_plan.md
│   └── task_breakdown.md
├── tasks/
│   ├── TASK-001.md
│   ├── TASK-002.md
│   └── ...
└── tracking/
    ├── completion_status.json
    └── verification_log.md
```

## Next Steps

After planning is complete:

```
/reimpl-next  # Get first task
/reimpl-search <query>  # Search documentation
```

## Example

```
User: /reimpl-plan ./legacy-java-app ./new-python-app
```
