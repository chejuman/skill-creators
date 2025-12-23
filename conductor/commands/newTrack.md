---
allowed-tools: Read, Write, Bash, Glob, Grep, Edit, AskUserQuestion, TodoWrite, Task
argument-hint: [기능 또는 버그 설명]
description: 새로운 기능/버그픽스 Track 생성
---

# New Track

새로운 기능 또는 버그 수정을 위한 Track을 생성합니다.

**입력**: $ARGUMENTS

## 단계

### 1. Conductor 초기화 확인

```bash
if [ ! -d ".claude/conductor" ]; then
    echo "Error: Conductor not initialized. Run /conductor:setup first."
    exit 1
fi
```

### 2. Track 생성

```bash
python3 ~/.claude/skills/conductor/scripts/create_track.py "$ARGUMENTS"
```

### 3. 요구사항 분석 (선택적)

설명이 충분하지 않으면 AskUserQuestion으로 상세 요구사항 수집:
- 해결하려는 문제
- 예상 사용자
- 성공 기준
- 기술적 제약

### 4. Spec 작성

Task(subagent_type='Explore')로 관련 코드 분석 후 spec.md 작성:
- 기존 패턴 파악
- 영향 범위 분석
- 통합 지점 확인

### 5. Plan 작성

Task(subagent_type='Plan')으로 구현 계획 수립:
- Phase 분리
- 태스크 세분화
- 의존성 정리

### 6. Git 브랜치 생성 (선택적)

```bash
git checkout -b feature/<track-id>
```

### 7. 완료 보고

```markdown
## ✅ Track 생성 완료

| 항목 | 값 |
|-----|---|
| Track ID | track-XXX |
| 설명 | $ARGUMENTS |
| 상태 | planning |
| 브랜치 | feature/track-XXX-... |

### 생성된 파일
- `.claude/conductor/tracks/<track-id>/spec.md`
- `.claude/conductor/tracks/<track-id>/plan.md`
- `.claude/conductor/tracks/<track-id>/metadata.json`

### 다음 단계
1. spec.md 검토 및 수정
2. plan.md 검토 및 수정
3. `/conductor:implement` 실행
```
