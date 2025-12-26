# /reimpl-continue

Continue the reimplementation from saved context.

## Usage

```
/reimpl-continue [context-path]
```

## Arguments

- `context-path` (optional): Path to context file or base64-encoded context
  - Default: `.reimpl-context.json` in current directory

## Workflow

This command resumes from the last saved state and implements the next feature/unit.

### 1. Load Context

```bash
python3 ~/.claude/skills/legacy-code-reimplementor/scripts/context_manager.py status --context {context-path}
```

### 2. Determine Next Work

Based on context state:

- If `current_phase` is `implementation`:
  - Get current feature and unit from context
  - Continue implementation cycle

### 3. Feature/Unit Implementation Cycle

For the current unit:

```
TodoWrite(todos=[
  {"content": "F{N}.U{M}: Implement {unit_name}", "status": "in_progress", "activeForm": "Implementing {unit_name}"},
  {"content": "F{N}.U{M}: Write tests", "status": "pending", "activeForm": "Writing tests"},
  {"content": "F{N}.U{M}: Verify implementation", "status": "pending", "activeForm": "Verifying"}
])
```

**Step 1: Implement**

```
Task(subagent_type='general-purpose', model='sonnet',
  prompt='Implement Feature {N}, Unit {M}: {unit_name}

          Context:
          - Source files: {repo_a_files}
          - Target path: {repo_b_path}
          - Tech stack: {tech_stack}
          - Completed units: {completed_units}

          Requirements:
          - Match original functionality exactly
          - Use modern {target_lang} patterns
          - Include error handling
          - Make testable',
  description='Implement F{N}.U{M}')
```

**Step 2: Write Tests**

```
Task(subagent_type='general-purpose', model='sonnet',
  prompt='Create tests for Feature {N}, Unit {M}

          Reference original edge cases from Repo A.
          Include: unit tests, integration tests, error cases.',
  description='Test F{N}.U{M}')
```

**Step 3: Verify**

```bash
python3 ~/.claude/skills/legacy-code-reimplementor/scripts/verify_feature.py \
  --feature {N} --unit {M} --context .reimpl-context.json
```

### 4. Update Context & Output

After each unit completion:

1. Update context with completion status
2. Save updated context
3. Generate continuation command

### Output Format

```
## Progress Update

Feature {N} ({feature_name}): Unit {M} of {total_units} completed
Overall: {completed}/{total} features ({pct}%)

### Verification Result
{verification_summary}

### Next Step

To continue with {next_work_description}, run:

/reimpl-continue

Context saved to: .reimpl-context.json
```

### When All Features Complete

If all features are done, automatically trigger final validation:

```
## All Features Complete!

Running final validation...

[Parallel validation agents: tests, security, performance]

Final report generated: migration_report.md
```

## State Transitions

```
                    ┌─────────────────┐
                    │  Load Context   │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
    ┌─────────────────┐           ┌─────────────────┐
    │ More units in   │           │ Feature done,   │
    │ current feature │           │ more features   │
    └────────┬────────┘           └────────┬────────┘
             │                             │
             ▼                             ▼
    ┌─────────────────┐           ┌─────────────────┐
    │ Implement next  │           │ Start next      │
    │ unit            │           │ feature         │
    └────────┬────────┘           └────────┬────────┘
             │                             │
             └──────────────┬──────────────┘
                            ▼
                  ┌─────────────────┐
                  │ Save context    │
                  │ Output continue │
                  └─────────────────┘
```

## Example

```
User: /reimpl-continue
```
