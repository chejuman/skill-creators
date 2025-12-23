# Workflow Configuration

## Development Methodology

- [ ] TDD (Test-Driven Development)
- [ ] BDD (Behavior-Driven Development)
- [ ] Trunk-Based Development
- [x] Feature Branch Workflow

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
- Feature: `feature/<track-id>-<description>`
- Bugfix: `fix/<track-id>-<description>`
- Hotfix: `hotfix/<description>`

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
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
