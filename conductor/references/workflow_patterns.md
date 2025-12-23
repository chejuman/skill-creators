# Workflow Patterns

Conductor에서 사용하는 개발 워크플로우 패턴 가이드.

## 1. Spec-First Development

스펙을 먼저 작성하고, 스펙에 따라 구현:

```
1. 요구사항 정리 → spec.md
2. 구현 계획 수립 → plan.md
3. Plan 검토/승인
4. 단계별 구현
5. 검증 및 완료
```

### Spec 작성 요소
- **목표**: 무엇을 달성하려는가?
- **범위**: 포함/제외되는 것
- **사용자 스토리**: As a..., I want..., So that...
- **수용 기준**: 완료 조건
- **제약사항**: 기술적/비기술적 제한

## 2. TDD Workflow

테스트 주도 개발 워크플로우:

```
1. 실패하는 테스트 작성
2. 최소한의 구현으로 테스트 통과
3. 리팩토링
4. 반복
```

### 구현 순서
```markdown
- [ ] 테스트 케이스 정의
- [ ] 실패하는 테스트 작성
- [ ] 구현
- [ ] 테스트 통과 확인
- [ ] 리팩토링
```

## 3. Feature Branch Workflow

Git 브랜치 전략:

```
main
 └── feature/track-001-user-auth
      ├── commit: "feat: add login form"
      ├── commit: "feat: implement auth API"
      └── commit: "test: add auth tests"
```

### 브랜치 네이밍
- `feature/<track-id>-<description>` - 기능 개발
- `fix/<track-id>-<description>` - 버그 수정
- `hotfix/<description>` - 긴급 수정

## 4. Phase-based Implementation

단계별 구현 패턴:

### Phase 구조
```markdown
## Phase 1: Foundation
- [ ] 데이터 모델 설계
- [ ] 기본 인프라 설정

## Phase 2: Core Implementation
- [ ] 핵심 비즈니스 로직
- [ ] API 엔드포인트

## Phase 3: Integration
- [ ] 프론트엔드 연동
- [ ] E2E 테스트

## Phase 4: Polish
- [ ] 에러 핸들링
- [ ] 문서화
```

### Phase 경계 규칙
- 각 Phase 완료 시 수동 검증 체크포인트
- Phase 간 의존성 명시
- 롤백 지점 확보

## 5. Multi-Agent Collaboration

복잡한 기능 구현 시 에이전트 분업:

### Orchestrator 패턴
```
Orchestrator (Plan Agent)
├── Analysis Phase
│   └── Explore Agents (PARALLEL)
│       ├── Codebase Analyzer
│       ├── Dependency Checker
│       └── Pattern Identifier
├── Implementation Phase
│   └── Implementation Agents (PARALLEL)
│       ├── Frontend Developer
│       ├── Backend Developer
│       └── Test Writer
└── Review Phase
    └── Review Agent
```

### 에이전트 할당 기준
| 복잡도 | 에이전트 수 | 패턴 |
|-------|-----------|-----|
| 낮음 | 1 | 단일 에이전트 |
| 중간 | 2-3 | 순차 실행 |
| 높음 | 4+ | 병렬 실행 |

## 6. Checkpoint & Validation

품질 게이트 패턴:

### 자동 검증
- Lint 통과
- 테스트 통과
- 빌드 성공

### 수동 검증 (Phase 경계)
- 코드 리뷰
- 기능 검증
- 성능 확인

### 롤백 트리거
- 테스트 실패
- 빌드 실패
- 명시적 요청 (`/conductor:revert`)
