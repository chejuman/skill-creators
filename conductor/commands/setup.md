---
allowed-tools: Read, Write, Bash, Glob, Grep, Edit, AskUserQuestion, TodoWrite
description: Conductor 프로젝트 초기화 - product, tech-stack, workflow 설정
---

# Conductor Setup

프로젝트에 Conductor를 초기화합니다.

## 단계

### 1. 초기화 스크립트 실행

```bash
python3 ~/.claude/skills/conductor/scripts/init_conductor.py .
```

### 2. 프로젝트 정보 수집

AskUserQuestion으로 다음 정보 수집:

1. **프로젝트 이름과 목적**
2. **주요 기술 스택** (언어, 프레임워크, DB)
3. **개발 방법론** (TDD, Feature Branch 등)
4. **팀 규모와 협업 방식**

### 3. 컨텍스트 파일 작성

수집한 정보로 다음 파일 업데이트:
- `.claude/conductor/product.md` - 제품 정의
- `.claude/conductor/tech-stack.md` - 기술 스택
- `.claude/conductor/workflow.md` - 워크플로우 설정

### 4. 완료 보고

```markdown
## ✅ Conductor 초기화 완료

| 파일 | 상태 |
|-----|------|
| product.md | ✅ 생성됨 |
| tech-stack.md | ✅ 생성됨 |
| workflow.md | ✅ 생성됨 |
| tracks.md | ✅ 생성됨 |

### 다음 단계
- `/conductor:newTrack [설명]` - 새 기능/버그 Track 생성
- `/conductor:status` - 현재 상태 확인
```

## 주의사항

- 이미 `.claude/conductor/` 존재 시 덮어쓰지 않음
- 기존 설정 업데이트는 수동으로 진행
