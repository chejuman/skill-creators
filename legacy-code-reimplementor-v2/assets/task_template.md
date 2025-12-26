# {{TASK_ID}}: {{TASK_NAME}}

## Metadata

| Field        | Value            |
| ------------ | ---------------- |
| ID           | {{TASK_ID}}      |
| Feature      | {{FEATURE_ID}}   |
| Category     | {{CATEGORY}}     |
| Priority     | {{PRIORITY}}     |
| Complexity   | {{COMPLEXITY}}   |
| Status       | {{STATUS}}       |
| Dependencies | {{DEPENDENCIES}} |
| Blocks       | {{BLOCKS}}       |

## Description

{{DESCRIPTION}}

## Source Reference (Repo A)

| File | Purpose |
| ---- | ------- |

{{#SOURCE_FILES}}
| `{{FILE_PATH}}` | {{PURPOSE}} |
{{/SOURCE_FILES}}

**Key Functions:** {{FUNCTIONS}}

**Key Classes:** {{CLASSES}}

## Target Files (Repo B)

| File | Purpose |
| ---- | ------- |

{{#TARGET_FILES}}
| `{{FILE_PATH}}` | {{PURPOSE}} |
{{/TARGET_FILES}}

## Acceptance Criteria

{{#ACCEPTANCE_CRITERIA}}

- [ ] {{CRITERION}}
      {{/ACCEPTANCE_CRITERIA}}

## Implementation Notes

- Reference original implementation for exact behavior
- Follow target language/framework conventions
- Use dependency injection where appropriate
- Write tests alongside implementation

## Tests Required

- [ ] Unit tests for all public functions
- [ ] Edge case tests based on original
- [ ] Integration tests if dependencies exist
- [ ] Error handling tests

## Verification Command

```bash
python3 ~/.claude/skills/legacy-code-reimplementor-v2/scripts/verify_task.py --task {{TASK_ID}}
```

---

**Created:** {{CREATED_AT}}
**Last Updated:** {{UPDATED_AT}}
