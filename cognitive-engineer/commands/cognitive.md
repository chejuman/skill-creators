# /cognitive - 인지적 엔지니어링 4-D 워크플로우

프롬프트/쿼리를 4-D 프레임워크로 분석하고 최적화한다.

## Usage

```
/cognitive [쿼리 또는 프롬프트]
```

## Examples

```
/cognitive Python 코드 리뉴얼 워크플로우 설계해줘
/cognitive 이 프롬프트 개선해줘: "좋은 블로그 글 써줘"
/cognitive 복잡한 API 설계 방법론 알려줘
```

## Workflow

**실행 시 자동으로:**

1. **DECONSTRUCT** - 쿼리 분해 및 의도 추출
   - 핵심 의도/엔티티/제약 조건 테이블 생성
   - 소크라테스 질문 3개 제시

2. **DIAGNOSE** - 모호성 진단
   - 명확성/구체성 루브릭 평가 (1-10)
   - 갭 식별 및 해결 방안 제시
   - 필요시 자동 웹 검색

3. **DEVELOP** - 4대 역량 적용 솔루션 설계
   - RCTS 구조 프롬프트 설계
   - 멀티-에이전트 오케스트레이션 (복잡 쿼리)
   - Self-critique 적용

4. **DELIVER** - 최적화 결과 전달
   - 최적화된 프롬프트 코드 블록
   - Mermaid 워크플로우 다이어그램
   - 검증 루브릭 점수표
   - 다음 단계 선택지 제공

## Output Format

```markdown
## 요약 인사이트

[핵심 발견 1문단]

## 4-D 분석 결과

[단계별 분석 테이블]

## 최적화된 프롬프트

[프롬프트 코드 블록]

## 워크플로우 다이어그램

[Mermaid 다이어그램]

## 검증 루브릭

[점수표]

## 다음 단계

[선택지]
```

## Options

인자 없이 `/cognitive` 실행 시 현재 컨텍스트의 마지막 쿼리를 분석한다.

## Related

- `cognitive-engineer` skill: 자동 트리거 (키워드 기반)
- [4-D Framework](../references/4d_framework.md)
- [Evaluation Rubrics](../references/rubrics.md)
