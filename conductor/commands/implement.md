---
allowed-tools: Read, Write, Bash, Glob, Grep, Edit, TodoWrite, Task
description: 현재 Track의 다음 태스크 구현
---

# Implement

현재 활성 Track의 다음 pending 태스크를 구현합니다.

## 단계

### 1. 활성 Track 확인

```bash
# 가장 최근 in_progress 또는 ready 상태 Track 찾기
ls -t .claude/conductor/tracks/*/metadata.json | head -1
```

Track의 metadata.json에서 상태 확인.

### 2. 컨텍스트 로드

다음 파일 읽기:
- `.claude/conductor/product.md`
- `.claude/conductor/tech-stack.md`
- `.claude/conductor/workflow.md`
- `.claude/conductor/tracks/<track-id>/spec.md`
- `.claude/conductor/tracks/<track-id>/plan.md`

### 3. 다음 태스크 확인

```bash
python3 ~/.claude/skills/conductor/scripts/sync_todos.py \
    .claude/conductor/tracks/<track-id>/plan.md --next
```

### 4. TodoWrite 동기화

plan.md의 현재 Phase 태스크를 TodoWrite로 로드:

```python
todos = [
    {"content": "[Phase X] Task description", "status": "pending", "activeForm": "Implementing..."},
    ...
]
```

### 5. 태스크 구현

1. **분석**: Task(subagent_type='Explore')로 관련 코드 파악
2. **구현**: 코드 작성/수정
3. **테스트**: 워크플로우 설정에 따라 테스트 실행
4. **검증**: lint, type check, 테스트 통과 확인

### 6. 태스크 완료 처리

1. plan.md에서 `- [ ]`를 `- [x]`로 변경
2. TodoWrite에서 해당 태스크 completed로 변경

### 7. Phase 경계 확인

현재 Phase의 모든 태스크 완료 시:
- 자동 검증 (테스트, 빌드)
- 수동 검증 체크포인트 안내
- 다음 Phase 진행 여부 확인

### 8. 진행 상황 보고

```markdown
## 📊 구현 진행 상황

### 완료된 태스크
- [x] Task 1.1: ...

### 현재 태스크
- [ ] Task 1.2: ... (in_progress)

### 진행률
Phase 1: ████████░░ 80%
전체: ██████░░░░ 60%

### 다음 단계
- 계속 구현: `/conductor:implement`
- 상태 확인: `/conductor:status`
- 롤백: `/conductor:revert`
```

## 멀티에이전트 실행

복잡한 태스크는 병렬 에이전트로 분업:

```python
# 프론트엔드 + 백엔드 + 테스트 병렬 구현
Task(subagent_type='general-purpose', prompt='Implement frontend...', run_in_background=True)
Task(subagent_type='general-purpose', prompt='Implement backend...', run_in_background=True)
Task(subagent_type='general-purpose', prompt='Write tests...', run_in_background=True)
```

## 중단 및 재개

- 작업 중단 시 현재 상태가 plan.md에 저장됨
- 다음 세션에서 `/conductor:implement` 재실행으로 이어서 진행
