---
allowed-tools: Read, Write, Bash, Glob, Grep, Edit, AskUserQuestion
argument-hint: [track-id 또는 task-id]
description: 논리적 작업 단위로 롤백
---

# Revert

Track 또는 태스크 단위로 변경사항을 롤백합니다.

**입력**: $ARGUMENTS (선택적 - 없으면 마지막 작업 롤백)

## 롤백 단위

| 단위 | 설명 | 예시 |
|-----|------|-----|
| Task | 단일 태스크 | `/conductor:revert task-1.2` |
| Phase | 전체 Phase | `/conductor:revert phase-2` |
| Track | 전체 Track | `/conductor:revert track-001` |
| Last | 마지막 작업 | `/conductor:revert` |

## 단계

### 1. 롤백 대상 확인

$ARGUMENTS가 없으면:
- 가장 최근 완료된 태스크 확인
- 사용자에게 롤백 범위 확인

$ARGUMENTS가 있으면:
- 지정된 대상 유효성 검증

### 2. 영향 분석

```markdown
## ⚠️ 롤백 영향 분석

### 롤백 대상
- Task 2.1: 로그인 구현
- Task 2.2: 회원가입 구현

### 영향받는 파일
- src/auth/login.ts (삭제)
- src/auth/signup.ts (삭제)
- tests/auth.test.ts (삭제)

### Git 커밋
- abc1234: feat: add login
- def5678: feat: add signup

### 의존성 확인
- Task 2.3은 Task 2.1, 2.2에 의존
- 롤백 시 Task 2.3도 pending으로 변경됨
```

### 3. 사용자 확인

AskUserQuestion으로 롤백 진행 확인:
- 롤백 범위 재확인
- 백업 생성 여부
- 진행 확인

### 4. 백업 생성 (선택적)

```bash
# Git stash로 현재 상태 백업
git stash push -m "conductor-backup-$(date +%Y%m%d-%H%M%S)"
```

### 5. 롤백 실행

#### Git 기반 롤백
```bash
# Track 시작 지점으로 롤백
git reset --hard <track-start-commit>

# 또는 특정 커밋들만 revert
git revert <commit1> <commit2> --no-commit
git commit -m "revert: rollback task 2.1, 2.2"
```

#### Plan 업데이트
```python
# plan.md에서 태스크 상태 변경
# [x] → [ ]
```

### 6. 완료 보고

```markdown
## ✅ 롤백 완료

### 롤백된 항목
- [x] → [ ] Task 2.1: 로그인 구현
- [x] → [ ] Task 2.2: 회원가입 구현

### 삭제된 파일
- src/auth/login.ts
- src/auth/signup.ts

### Git 상태
- 브랜치: feature/track-001-auth
- 커밋: reverted to abc1234

### 복구 방법
```bash
# stash에서 복구
git stash pop

# 또는 revert 취소
git revert --abort
```

### 다음 단계
- 다시 구현: `/conductor:implement`
- 상태 확인: `/conductor:status`
```

## 안전장치

- **main/master 브랜치 보호**: feature 브랜치에서만 롤백 허용
- **원격 push된 커밋**: force push 필요 시 경고
- **다른 Track 의존성**: 영향받는 Track 목록 표시
