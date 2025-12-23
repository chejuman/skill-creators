---
name: conductor
description: Context-Driven Development 워크플로우. 프로젝트 컨텍스트를 .claude/conductor/에 영구 저장하고, Track 기반 작업 관리, 멀티에이전트 병렬 실행, TodoWrite 통합을 제공. Use when starting new projects, creating feature specs, implementing tracked tasks, or when .claude/conductor/ directory exists. Triggers on "conductor", "컨덕터", "새 프로젝트 설정", "트랙 생성", "컨텍스트 기반 개발".
---

# Conductor - Context-Driven Development

프로젝트 컨텍스트를 영구 마크다운 파일로 관리하여 일관된 AI 협업 환경을 구축.

## Core Workflow

```
/conductor:setup → /conductor:newTrack → /conductor:implement
       ↓                   ↓                    ↓
   Context 구축        Spec & Plan         TodoWrite 연동
```

## 명령어 요약

| 명령어 | 설명 |
|-------|------|
| `/conductor:setup` | 프로젝트 초기화 - product, tech-stack, workflow 설정 |
| `/conductor:newTrack [설명]` | 새 기능/버그픽스 Track 생성 |
| `/conductor:implement` | 현재 Track의 다음 태스크 구현 |
| `/conductor:status` | 프로젝트 및 Track 진행 상황 |
| `/conductor:revert` | 논리적 작업 단위로 롤백 |

## 자동 감지

`.claude/conductor/` 디렉토리 감지 시 자동 활성화:
- `product.md` 존재 → 프로젝트 컨텍스트 로드
- `tracks/` 존재 → 활성 Track 확인
- `workflow.md` 존재 → 워크플로우 설정 적용

## Context 디렉토리 구조

```
.claude/conductor/
├── product.md              # 제품 정의, 목표, 페르소나
├── product-guidelines.md   # 브랜드/스타일 가이드라인
├── tech-stack.md           # 기술 스택 및 제약사항
├── workflow.md             # 팀 워크플로우 (TDD, 코드리뷰 등)
├── code-styleguides/       # 언어별 코딩 컨벤션
│   ├── typescript.md
│   └── python.md
├── tracks.md               # Track 인덱스
└── tracks/                 # 개별 Track 디렉토리
    └── <track-id>/
        ├── spec.md         # 요구사항 명세
        ├── plan.md         # 단계별 구현 계획
        └── metadata.json   # Track 메타데이터
```

## Track 시스템

Track은 하나의 기능 또는 버그 수정 단위:

### Track 상태
- `planning` - 스펙/플랜 작성 중
- `ready` - 구현 준비 완료
- `in_progress` - 구현 진행 중
- `blocked` - 외부 의존성 대기
- `completed` - 완료

### Plan 구조
```markdown
## Phase 1: 기반 구축
- [ ] Task 1.1: 데이터 모델 정의
- [ ] Task 1.2: API 엔드포인트 설계

## Phase 2: 핵심 구현
- [ ] Task 2.1: 비즈니스 로직 구현
- [ ] Task 2.2: 테스트 작성
```

## TodoWrite 통합

Track의 plan.md와 Claude의 TodoWrite 자동 동기화:

1. `/conductor:implement` 시 plan.md의 태스크를 TodoWrite로 로드
2. 태스크 완료 시 plan.md와 TodoWrite 동시 업데이트
3. Phase 경계에서 수동 검증 체크포인트

## 멀티에이전트 실행

복잡한 구현 시 병렬 에이전트 활용:

```
Orchestrator
├── Explore Agent → 코드베이스 분석
├── Plan Agent → 구현 전략 수립
├── Implementation Agents (PARALLEL)
│   ├── Frontend Agent
│   ├── Backend Agent
│   └── Test Agent
└── Review Agent → 코드 리뷰
```

## Git 통합

Track과 Git 브랜치 연동:
- Track 생성 시 `feature/<track-id>` 브랜치 생성 옵션
- 구현 완료 시 커밋 메시지에 Track ID 포함
- `/conductor:revert`는 Track 단위로 롤백

## 스크립트

- [init_conductor.py](scripts/init_conductor.py) - 프로젝트 초기화
- [create_track.py](scripts/create_track.py) - Track 생성
- [sync_todos.py](scripts/sync_todos.py) - TodoWrite 동기화

## 리퍼런스

- [workflow_patterns.md](references/workflow_patterns.md) - 워크플로우 패턴
- [agent_prompts.md](references/agent_prompts.md) - 에이전트 프롬프트 템플릿

## 템플릿

- [product.md.template](assets/product.md.template)
- [tech-stack.md.template](assets/tech-stack.md.template)
- [workflow.md.template](assets/workflow.md.template)
- [spec.md.template](assets/spec.md.template)
- [plan.md.template](assets/plan.md.template)
