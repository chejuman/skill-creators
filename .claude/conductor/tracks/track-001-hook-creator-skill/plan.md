# Implementation Plan: hook-creator skill

## Overview

- **Track ID**: track-001-hook-creator-skill
- **Status**: planning
- **Dependencies**: Python 3.8+, skill-creator scripts

## Phase 1: Foundation (Skill Structure)

스킬 기본 구조 생성

- [ ] Task 1.1: init_skill.py로 hook-creator 스킬 초기화
- [ ] Task 1.2: 디렉토리 구조 정리 (불필요한 예제 파일 삭제)
- [ ] Task 1.3: SKILL.md 기본 프레임워크 작성

**검증 포인트:**
- quick_validate.py 통과
- 디렉토리 구조 확인

## Phase 2: Core Scripts

핵심 스크립트 구현

- [ ] Task 2.1: generate_hook.py - hook 설정 생성기
  - CLI 인터페이스 (--event, --matcher, --command)
  - JSON 출력 생성
  - 템플릿 기반 생성

- [ ] Task 2.2: validate_hook.py - hook 검증기
  - JSON 스키마 검증
  - matcher 패턴 검증
  - 스크립트 경로 존재 확인

- [ ] Task 2.3: merge_hooks.py - 기존 설정에 병합
  - 기존 settings.json 읽기
  - 충돌 감지 및 처리
  - 백업 생성

**검증 포인트:**
- 각 스크립트 독립 실행 가능
- 200줄 이내 유지

## Phase 3: References & Templates

참조 문서 및 템플릿

- [ ] Task 3.1: events_reference.md - 8가지 이벤트 상세 문서
  - 각 이벤트의 input/output 스키마
  - matcher 지원 여부
  - 사용 사례

- [ ] Task 3.2: matchers_reference.md - matcher 패턴 가이드
  - 패턴 문법 설명
  - 일반적인 도구명 목록
  - 예제 패턴

- [ ] Task 3.3: examples_catalog.md - 사용 사례별 예제
  - Auto-formatter (PostToolUse)
  - Secret detector (PreToolUse)
  - Context injector (SessionStart)
  - Commit validator (PreToolUse + Bash)

- [ ] Task 3.4: assets/templates/ - JSON 및 스크립트 템플릿
  - hook_template.json
  - format_script.py
  - validate_script.py

**검증 포인트:**
- 각 문서 200줄 이내
- 예제가 실제 동작 가능

## Phase 4: SKILL.md Workflow

메인 워크플로우 완성

- [ ] Task 4.1: SKILL.md 워크플로우 작성
  - 대화형 hook 생성 가이드
  - 스크립트 사용법
  - 검증 및 설치 단계

- [ ] Task 4.2: 빠른 시작 섹션 추가
  - 3가지 일반적인 사용 사례
  - 복사-붙여넣기 가능한 예제

**검증 포인트:**
- SKILL.md 200줄 이내
- 명확한 단계별 지침

## Phase 5: Validation & Packaging

검증 및 패키징

- [ ] Task 5.1: quick_validate.py 실행
- [ ] Task 5.2: package_skill.py로 패키징
- [ ] Task 5.3: ~/.claude/skills/에 설치
- [ ] Task 5.4: 실제 hook 생성 테스트

**검증 포인트:**
- 패키지 생성 성공
- 설치 후 스킬 동작 확인

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| JSON 스키마 변경 | 생성된 hook 무효화 | 공식 문서 참조, 버전 체크 |
| 복잡한 matcher 패턴 | 사용자 혼란 | 예제 중심 문서화 |
| 설정 파일 손상 | 사용자 환경 영향 | 항상 백업 생성 |

## Notes

- Claude Code hooks는 세션 시작 시 캡처되므로 변경 후 재시작 필요
- exit code 의미: 0=성공, 2=차단, 기타=비차단 오류
- prompt 타입 hook은 Haiku 모델 사용

## History

| Date | Action | Notes |
|------|--------|-------|
| 2025-12-23 | Created | Initial plan based on research |
