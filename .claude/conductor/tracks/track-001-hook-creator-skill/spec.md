# Specification: hook-creator skill

## Summary

Claude Code hooks 설정 파일을 대화형으로 생성하고 관리하는 스킬

## Background

### 문제 정의
Claude Code hooks는 강력한 자동화 기능을 제공하지만, JSON 설정 파일을 수동으로 작성해야 한다:
- 복잡한 JSON 스키마 구조 (events, matchers, hooks 배열)
- 8가지 이벤트 타입과 각각의 input/output 스키마
- matcher 패턴 문법 (정규식, 도구명, 와일드카드)
- 올바른 exit code 및 JSON output 형식

### 동기
개발자가 hooks의 강력한 기능을 쉽게 활용할 수 있도록 가이드와 자동화 도구 제공

## Goals

### Must Have
1. 대화형 hook 생성 워크플로우 (이벤트 선택 → 설정 → 검증)
2. 8가지 hook 이벤트에 대한 템플릿 제공
3. hooks.json 파일 자동 생성 및 병합
4. 생성된 hook 검증 스크립트

### Should Have
1. 일반적인 사용 사례별 예제 (formatter, validator, context injector)
2. hook 스크립트 템플릿 (Python, Bash)
3. matcher 패턴 빌더 헬퍼

### Won't Have (이번 범위 외)
1. GUI 기반 편집기
2. 원격 hook 저장소
3. hook 실행 모니터링 대시보드

## User Stories

### Story 1
- **As a**: Claude Code 사용자
- **I want**: 코드 저장 시 자동 포맷팅 hook 생성
- **So that**: 일관된 코드 스타일 유지

### Story 2
- **As a**: 팀 리더
- **I want**: 커밋 전 보안 검사 hook 생성
- **So that**: 민감 정보 유출 방지

### Story 3
- **As a**: 개발자
- **I want**: 세션 시작 시 컨텍스트 주입 hook 생성
- **So that**: 프로젝트 상태 자동 로드

## Technical Design

### Architecture Overview
```
hook-creator/
├── SKILL.md                    # 메인 워크플로우 가이드
├── scripts/
│   ├── generate_hook.py        # hook 설정 생성기
│   ├── validate_hook.py        # hook 검증기
│   └── merge_hooks.py          # 기존 설정에 병합
├── references/
│   ├── events_reference.md     # 8가지 이벤트 상세
│   ├── matchers_reference.md   # matcher 패턴 가이드
│   └── examples_catalog.md     # 사용 사례별 예제
└── assets/
    ├── templates/              # hook JSON 템플릿
    └── scripts/                # 실행 스크립트 템플릿
```

### Hook JSON Schema
```json
{
  "hooks": {
    "EventName": [{
      "matcher": "ToolPattern",
      "description": "설명",
      "priority": 100,
      "enabled": true,
      "hooks": [{
        "type": "command|prompt",
        "command": "실행 명령",
        "timeout": 60
      }]
    }]
  }
}
```

### Supported Events
| Event | Matcher | Use Case |
|-------|---------|----------|
| PreToolUse | Yes | 도구 실행 전 검증/수정 |
| PostToolUse | Yes | 도구 실행 후 포맷팅/검증 |
| PermissionRequest | Yes | 권한 자동 승인/거부 |
| UserPromptSubmit | No | 프롬프트 검증/컨텍스트 주입 |
| Stop | No | 완료 조건 검증 |
| SubagentStop | No | 서브에이전트 결과 검증 |
| SessionStart | Yes | 세션 초기화/컨텍스트 로드 |
| PreCompact | Yes | 컨텍스트 압축 전 백업 |

### Dependencies
- Python 3.8+
- jq (JSON 처리, optional)

## Acceptance Criteria

### Functional
- [ ] generate_hook.py로 유효한 hooks.json 생성
- [ ] 8가지 이벤트 타입 모두 지원
- [ ] matcher 패턴 유효성 검증
- [ ] 기존 설정 파일에 안전하게 병합
- [ ] 생성된 스크립트 실행 가능

### Non-Functional
- [ ] 스킬 SKILL.md 200줄 이내
- [ ] 각 스크립트 200줄 이내
- [ ] 명확한 에러 메시지

## Edge Cases

1. 이미 동일한 matcher가 있는 hook 존재 시 → 사용자 확인 후 병합/교체
2. 잘못된 JSON 형식의 기존 설정 → 백업 후 새로 생성 제안
3. 스크립트 경로가 존재하지 않음 → 경고 및 생성 안내

## Testing Strategy

### Unit Tests
- generate_hook.py: 각 이벤트 타입별 출력 검증
- validate_hook.py: 유효/무효 JSON 케이스

### Integration Tests
- 실제 .claude/settings.json에 병합 테스트
- 생성된 스크립트 실행 테스트

## Rollout Plan

### Phase 1: Core
- SKILL.md 워크플로우
- generate_hook.py 스크립트
- 기본 템플릿 (PostToolUse formatter)

### Phase 2: Complete
- 모든 이벤트 타입 지원
- 예제 카탈로그
- 스크립트 템플릿

## References

- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Claude Blog: How to configure hooks](https://claude.com/blog/how-to-configure-hooks)
