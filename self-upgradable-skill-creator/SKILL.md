---
name: self-upgradable-skill-creator
description: "4-D 인지적 엔지니어링 기반 스킬 생성기. claude-code-guide로 최신 기능 자동 학습 후 스킬 생성. Use when: 'create skill', 'new skill', 'skill development', '스킬 만들어', '스킬 생성', '새 스킬', 'upgrade skill', '스킬 개선'. Includes: analyze_skill.py (4-D rubric), create_skill.py (one-click), upgrade_knowledge.py."
---

# Self-Upgradable Skill Creator

4-D 인지적 엔지니어링 + 자동 지식 업데이트 기반 스킬 생성 워크플로우.

## Activation

워크플로우 시작 시:

```
TodoWrite([
  {content: "Self-Upgrade: 최신 기능 학습", status: "pending"},
  {content: "Requirements: 요구사항 수집", status: "pending"},
  {content: "Generate: 스킬 파일 생성", status: "pending"},
  {content: "Validate & Install: 검증 및 설치", status: "pending"}
])
```

## Phase 1: Self-Upgrade

최신 기능 학습 (매 스킬 생성 전):

```
Task(
  subagent_type='claude-code-guide',
  prompt='Get latest: SKILL.md format, Slash Commands, Hooks, Subagents, MCP',
  description='Upgrade knowledge',
  model='sonnet'
)
```

학습 후 `references/` 업데이트.

## Phase 2: Requirements Gathering

```
AskUserQuestion([{
  question: "스킬 패턴을 선택하세요",
  header: "Pattern",
  options: [
    {label: "Workflow-Based", description: "순차적 프로세스"},
    {label: "Task-Based", description: "독립적 작업 모음"},
    {label: "Reference", description: "가이드라인/스펙"},
    {label: "Capabilities", description: "통합 시스템"}
  ],
  multiSelect: false
}])
```

수집 항목:

- 스킬 이름 (hyphen-case)
- 트리거 키워드
- 필요한 scripts/references/assets

## Phase 3: Generation

1. **scripts/** - 실행 코드 생성
2. **references/** - 문서화
3. **SKILL.md** - 메인 워크플로우

```bash
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <name> --path .
```

## Phase 4: Validate & Install

```bash
# 분석
python3 scripts/analyze_skill.py ./<skill-name>

# 검증
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py ./<skill-name>

# 패키징 & 설치
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./<skill-name> .
unzip -o <skill-name>.zip -d ~/.claude/skills/
```

## Quick Start (One-Click)

```bash
# 원클릭 스킬 생성 (init → analyze → validate → package)
python3 scripts/create_skill.py my-skill

# 설치
unzip -o my-skill.zip -d ~/.claude/skills/
```

## Scripts Reference

| Script                 | Purpose         | Usage                              |
| ---------------------- | --------------- | ---------------------------------- |
| `create_skill.py`      | 원클릭 생성     | `create_skill.py <name> [dir]`     |
| `analyze_skill.py`     | 4-D 루브릭 분석 | `analyze_skill.py <path> [--json]` |
| `upgrade_knowledge.py` | 지식 업데이트   | `upgrade_knowledge.py [--check]`   |

## 4-D Rubric Scoring

| 차원          | 평가 기준                              | 점수 |
| ------------- | -------------------------------------- | ---- |
| Clarity       | frontmatter 완성도, description 명확성 | /10  |
| Specificity   | 라인 수 제한, 구체적 지시              | /10  |
| Actionability | scripts/ 존재, 실행 가능성             | /10  |
| Automation    | AskUserQuestion, TodoWrite, Task 활용  | /10  |

## Critical Requirements

- **SKILL.md**: Under 200 lines, valid YAML frontmatter
- **Naming**: Hyphen-case only (e.g., `my-skill`)
- **Description**: WHAT + WHEN (max 1024 chars)
- **Scripts**: Under 200 lines each

## Related

- [Latest Features](references/latest_features.md)
- [Skill Patterns](references/skill_patterns.md)
- [Hook Integration](references/hooks_integration.md)
