# Product Definition

## Overview

Claude Code 스킬을 개발, 테스트, 패키징하는 워크스페이스. 새로운 스킬을 만들고 `~/.claude/skills/`에 설치하기 전 개발 및 검증을 수행한다.

---

## ⚠️⚠️ 중요: 스킬 선택 필수 ⚠️⚠️

### `/conductor:implement` 실행 시 반드시 AskUserQuestion으로 스킬 선택

**구현 작업 전 반드시 다음 중 하나를 선택해야 함:**

| 옵션 | 스킬 | 설명 |
|------|------|------|
| 1 | `self-upgradable-skill-creator` | 최신 문서 자동 학습 후 스킬 생성 |
| 2 | `multi-agent-skill-creator` | 병렬 에이전트 기반 스킬 생성 |
| 3 | 직접 구현 | 스킬 없이 수동 구현 |

### ⚠️ 필수 규칙

1. **AskUserQuestion 필수**: implement 시작 시 반드시 사용자에게 물어볼 것
2. **선택된 스킬만 사용**: 사용자가 선택한 스킬의 워크플로우만 따를 것
3. **임의 변경 금지**: 사용자 승인 없이 다른 스킬로 전환하지 말 것

---

## Goals

### Primary Goals
1. 새로운 Claude Code 스킬을 체계적으로 개발
2. 스킬 검증 및 패키징 워크플로우 제공
3. 스킬 품질 표준 유지

### Success Metrics
- 스킬 검증 통과율
- 설치 후 정상 동작 여부
- SKILL.md 가이드라인 준수

## User Personas

### Primary User
- **이름**: 스킬 개발자
- **역할**: Claude Code 확장 기능 개발
- **목표**: 재사용 가능한 스킬을 빠르게 개발하고 배포
- **Pain Points**: 스킬 구조 파악, 검증 프로세스, 디버깅

## Features

### Core Features (MVP)
1. 스킬 초기화 (init_skill.py)
2. 스킬 검증 (quick_validate.py)
3. 스킬 패키징 (package_skill.py)

### Available Skill Creators
1. **self-upgradable-skill-creator**: claude-code-guide로 최신 문서 학습
2. **multi-agent-skill-creator**: 병렬 에이전트로 스킬 생성

## Constraints

### Technical
- SKILL.md 200줄 이하
- 스크립트/레퍼런스 각 200줄 이하
- hyphen-case 명명 규칙

### Business
- 개인 개발 프로젝트

## Non-Goals

명시적으로 범위에서 제외되는 것:
1. 이 워크스페이스 자체를 스킬로 배포
2. 스킬 레지스트리/마켓플레이스 구축
