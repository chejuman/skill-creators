# /spec-dev Command

Start new feature specification with deep intent analysis.

## Usage

```bash
/spec-dev <feature-idea>
/spec-dev --resume
/spec-dev --status
```

## Arguments

| Argument      | Description                          |
| ------------- | ------------------------------------ |
| `<idea>`      | Feature description in any format    |
| `--resume`    | Resume existing spec from .spec-docs |
| `--status`    | Show current phase and progress      |
| `--depth 1-5` | Analysis depth (default: 3)          |

## Workflow

### 1. Initialize

```bash
python3 scripts/doc_manager.py init --feature {feature-name}
```

Creates `.spec-docs/` structure.

### 2. Deep Intent Analysis

Use AskUserQuestion to understand user's true intent:

```
AskUserQuestion(questions=[
  {
    "question": "이 기능의 핵심 목적은 무엇인가요?",
    "header": "Core Purpose",
    "options": [
      {"label": "새로운 비즈니스 기능", "description": "매출/사용자 가치 창출"},
      {"label": "기존 기능 개선", "description": "성능/UX 향상"},
      {"label": "기술 부채 해결", "description": "리팩토링/마이그레이션"},
      {"label": "보안/규정 준수", "description": "필수 요구사항"}
    ],
    "multiSelect": false
  }
])
```

### 3. Real-Time Research

Before generating specs, research:

```
WebSearch(query="{domain} best practices 2025")
WebSearch(query="{feature_type} implementation patterns")
```

### 4. Generate Spec

With research-informed content using EARS format.

### 5. Generate Tasks

Atomic implementation tasks with dependencies.

## Examples

```bash
# Start new feature
/spec-dev "사용자 인증 시스템"

# With depth level
/spec-dev --depth 4 "결제 처리 기능"

# Resume existing
/spec-dev --resume

# Check status
/spec-dev --status
```

## Output

All outputs saved to `.spec-docs/`:

- `discovery/` - Intent analysis, research findings
- `specs/{feature}/` - Requirements, design documents
- `plans/` - Implementation plan, task breakdown
- `tasks/` - Individual TASK-XXX.md files
- `tracking/` - Completion status, verification log

## Related Commands

| Command        | Purpose                         |
| -------------- | ------------------------------- |
| `/spec-next`   | Get next task with verification |
| `/spec-check`  | Verify task completion          |
| `/spec-search` | Search documentation            |
| `/spec-status` | Show progress report            |
