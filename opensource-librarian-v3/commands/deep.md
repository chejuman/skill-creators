---
description: Deep research mode - comprehensive analysis with 15+ parallel workers (TYPE_D)
allowed-tools: Bash, Read, Grep, Glob, Task, TodoWrite
model: opus
---

# Deep Research Mode

You are now in DEEP mode for comprehensive open source research.

## Configuration

- **Workers**: 15+ (maximum)
- **Focus**: Full parallel research across all sources
- **Output**: Complete JSON API v3 response

## Execution Protocol

### Phase 1: Parallel Dispatch

Launch ALL workers simultaneously:

```
Task(prompt=CODE_HUNTER_1, model='sonnet', run_in_background=true)
Task(prompt=CODE_HUNTER_2, model='sonnet', run_in_background=true)
Task(prompt=CODE_HUNTER_3, model='sonnet', run_in_background=true)
Task(prompt=GIT_ARCHAEOLOGIST_1, model='haiku', run_in_background=true)
Task(prompt=GIT_ARCHAEOLOGIST_2, model='haiku', run_in_background=true)
Task(prompt=DOC_RESEARCHER_1, model='haiku', run_in_background=true)
Task(prompt=DOC_RESEARCHER_2, model='haiku', run_in_background=true)
Task(prompt=EVIDENCE_VALIDATOR, model='haiku', run_in_background=true)
```

### Phase 2: Synchronize

Wait for all workers with `TaskOutput(block=true)`.

### Phase 3: Validate

Run evidence-validator on all findings.

### Phase 4: Synthesize

Combine into comprehensive bilingual response.

### Phase 5: Deliver

Generate full JSON API v3 output.

## Output Format

```json
{
  "apiVersion": "v3",
  "metadata": {
    "classification": "TYPE_D",
    "workersUsed": 15,
    "validationPassed": true
  },
  "summary": {"en": "...", "ko": "..."},
  "findings": [...],
  "history": {...},
  "sources": [...],
  "validation": {...}
}
```

## When to Use

- Complex architecture questions
- Multi-repository analysis
- Historical investigation
- Comprehensive documentation
- Production research reports

## Features

- Full git history timeline
- Multiple code implementations
- Cross-referenced documentation
- Complete validation
- JSON API v3 output
