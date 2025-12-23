# Product Definition

## Overview

Claude Code 스킬을 개발, 테스트, 패키징하는 워크스페이스. 새로운 스킬을 만들고 `~/.claude/skills/`에 설치하기 전 개발 및 검증을 수행한다.

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

### Future Features
1. 스킬 자동 테스트 프레임워크
2. 스킬 버전 관리

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
