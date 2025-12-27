# /skill-create - Self-Upgrading Skill Creator

최신 Claude Code 기능을 학습한 후 스킬을 생성한다.

## Usage

```
/skill-create [skill-name] [description]
```

## Examples

```
/skill-create pdf-editor PDF 편집 및 병합 도구
/skill-create api-tester REST API 테스트 자동화
/skill-create code-reviewer 코드 리뷰 워크플로우
```

## Workflow

실행 시 자동으로:

1. **Self-Upgrade** - claude-code-guide 에이전트로 최신 기능 학습
2. **Requirements** - AskUserQuestion으로 요구사항 수집
3. **Analysis** - 유사 기존 스킬 분석
4. **Generation** - 스킬 파일 생성 (SKILL.md, scripts/, references/)
5. **Validation** - quick_validate.py로 검증
6. **Installation** - ~/.claude/skills/에 설치

## Interactive Flow

```
┌─ /skill-create api-tester ─────────────────────┐
│                                                 │
│  [Phase 1: Self-Upgrade]                       │
│  claude-code-guide로 최신 기능 학습 중...      │
│                                                 │
│  [Phase 2: Requirements]                       │
│  ┌─ 스킬 패턴 선택 ─────────────────────┐     │
│  │ ○ Workflow-Based (순차적 프로세스)    │     │
│  │ ● Task-Based (독립적 작업 모음)       │     │
│  │ ○ Reference (가이드라인/스펙)         │     │
│  └───────────────────────────────────────┘     │
│                                                 │
│  [Phase 3: Generation]                         │
│  ✓ SKILL.md 생성                              │
│  ✓ scripts/run_test.py 생성                   │
│  ✓ references/api_guide.md 생성               │
│                                                 │
│  [Phase 4: Validation]                         │
│  ✅ Skill is valid!                            │
│                                                 │
│  [Phase 5: Install]                            │
│  ✅ Installed to ~/.claude/skills/api-tester/  │
└─────────────────────────────────────────────────┘
```

## Options

| Option            | Description                 |
| ----------------- | --------------------------- |
| `--analyze-first` | 기존 유사 스킬 분석 후 생성 |
| `--no-install`    | 생성만 하고 설치 안함       |
| `--upgrade-only`  | 지식 베이스만 업데이트      |

## Related

- `self-upgradable-skill-creator` skill
- [Skill Patterns](../references/skill_patterns.md)
- [Latest Features](../references/latest_features.md)
