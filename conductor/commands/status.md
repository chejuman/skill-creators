---
allowed-tools: Read, Bash, Glob
description: 프로젝트 및 Track 진행 상황 확인
---

# Status

Conductor 프로젝트와 Track의 현재 상태를 표시합니다.

## 단계

### 1. Conductor 초기화 확인

`.claude/conductor/` 디렉토리 존재 확인.

### 2. 프로젝트 개요 수집

```bash
# 메타데이터 읽기
cat .claude/conductor/metadata.json

# Track 목록 확인
ls -la .claude/conductor/tracks/
```

### 3. Track별 상태 분석

각 Track의 metadata.json과 plan.md 분석:

```bash
python3 ~/.claude/skills/conductor/scripts/sync_todos.py \
    .claude/conductor/tracks/<track-id>/plan.md
```

### 4. 상태 보고서 생성

```markdown
## 📊 Conductor Status

### 프로젝트 정보
| 항목 | 값 |
|-----|---|
| 프로젝트 | {project_name} |
| 초기화 | {created_date} |
| 활성 Track | {active_count} |

### Active Tracks

| Track | 설명 | 상태 | 진행률 |
|-------|-----|------|-------|
| track-001 | 사용자 인증 | in_progress | 60% |
| track-002 | API 최적화 | planning | 0% |

### 상세: track-001

**Phase 1: Foundation** ██████████ 100%
- [x] Task 1.1: 데이터 모델
- [x] Task 1.2: API 설계

**Phase 2: Implementation** ████░░░░░░ 40%
- [x] Task 2.1: 로그인 구현
- [ ] Task 2.2: 회원가입 구현 ← 현재
- [ ] Task 2.3: 테스트 작성

**Phase 3: Integration** ░░░░░░░░░░ 0%
- [ ] Task 3.1: 프론트엔드 연동
- [ ] Task 3.2: E2E 테스트

### Git 상태
| 브랜치 | Track | 상태 |
|-------|-------|-----|
| feature/track-001-auth | track-001 | 5 commits ahead |
| feature/track-002-api | track-002 | not created |

### Completed Tracks

| Track | 설명 | 완료일 |
|-------|-----|-------|
| track-000 | 초기 설정 | 2025-01-15 |

### 다음 단계
- 구현 계속: `/conductor:implement`
- 새 Track: `/conductor:newTrack [설명]`
- 롤백: `/conductor:revert`
```

## 간단 출력 모드

상세 정보 없이 간단히:

```
Conductor: project-name
Active: 2 tracks, 1 in_progress
Current: track-001 "사용자 인증" (Phase 2, 60%)
```
