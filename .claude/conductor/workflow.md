# Workflow Configuration

## Development Methodology

- [ ] TDD (Test-Driven Development)
- [ ] BDD (Behavior-Driven Development)
- [ ] Trunk-Based Development
- [x] Feature Branch Workflow

## Git Workflow (Slash Commands) - 완전 자동

### 작업 순서

```
/dev:git-start  →  (개발)  →  /dev:git-push  →  /dev:git-pr --merge
```

### Step 1: 브랜치 생성
```bash
/dev:git-start feature/<description>
```
- main에서 새 브랜치 생성
- 브랜치 네이밍 검증
- 최신 main 동기화

### Step 2: 개발 작업
- 코드 작성 및 수정
- 로컬 커밋 (수동 또는 Claude 요청)
- 커밋 메시지: `<type>(<scope>): <subject>`

### Step 3: 원격 푸시
```bash
/dev:git-push
```
- 변경사항 커밋 확인
- 원격 브랜치 생성/업데이트
- upstream 설정

### Step 4: PR 생성 + 자동 병합
```bash
/dev:git-pr --merge
```
자동으로 수행되는 작업:
1. PR 제목/본문 자동 생성
2. GitHub PR 생성
3. **Squash Merge 실행**
4. **원격 브랜치 삭제**
5. **로컬 main 동기화**
6. **로컬 feature 브랜치 삭제**

### 완료 후 상태
- main 브랜치에 변경사항 반영됨
- feature 브랜치 정리 완료
- 다음 작업 준비 완료

## Code Review

### Required Reviewers
- Self-review (1인 개발)

### Review Checklist
- [x] 코드 스타일 준수
- [ ] 테스트 커버리지
- [x] 보안 검토
- [ ] 성능 고려
- [x] 문서화

## Git Conventions

### Branch Naming
- Feature: `feature/<description>`
- Bugfix: `fix/<description>`
- Hotfix: `hotfix/<description>`

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types**: feat, fix, docs, style, refactor, test, chore

## Testing Requirements

### Coverage Targets
- Unit: 수동 테스트
- Integration: N/A
- E2E: N/A

### Test Naming
- 수동 검증 위주

## Documentation

### Required Docs
- [x] README
- [ ] API Documentation
- [ ] Architecture Decision Records (ADR)
- [ ] Changelog

### Documentation Location
- 각 스킬 디렉토리 내 SKILL.md
- 워크스페이스 루트 CLAUDE.md

## Phase Validation

### Automatic Checks
- quick_validate.py 실행
- package_skill.py 검증

### Manual Checks (Phase Boundary)
- SKILL.md 내용 검토
- 설치 후 기능 테스트

## AI Collaboration

### Preferred Patterns
- skill-creator 스킬 활용
- Conductor Track 기반 작업 관리
- 점진적 개발 및 검증

### Avoided Patterns
- 검증 없이 바로 설치
- 200줄 이상의 단일 파일

### Review Points
- AI 생성 코드 수동 검토
- 보안 관련 코드 특별 주의
- SKILL.md 가이드라인 준수 확인
