# Evaluation Rubrics

## Query Quality Assessment

### Dimension 1: Clarity (명확성)

| Score | Description                   | Example                                 |
| ----- | ----------------------------- | --------------------------------------- |
| 10    | 완벽히 명확, 해석 여지 없음   | "React 18에서 useEffect 무한 루프 수정" |
| 8     | 명확하나 세부 1-2개 추론 필요 | "React 훅 버그 수정해줘"                |
| 6     | 대략 파악 가능, 질문 필요     | "프론트엔드 버그 고쳐줘"                |
| 4     | 모호함, 다수 해석 가능        | "코드 고쳐줘"                           |
| 2     | 해석 불가                     | "이거 좀"                               |

### Dimension 2: Specificity (구체성)

| Score | Description         | Example                            |
| ----- | ------------------- | ---------------------------------- |
| 10    | 수치/범위/예시 완비 | "500자 이내, 3문단, 예시 2개 포함" |
| 8     | 대부분 구체적       | "짧게, 예시 포함"                  |
| 6     | 절반 구체적         | "적당한 길이로"                    |
| 4     | 대부분 추상적       | "좋게"                             |
| 2     | 완전 추상적         | (제약 없음)                        |

### Dimension 3: Actionability (실행가능성)

| Score | Description       | Indicator             |
| ----- | ----------------- | --------------------- |
| 10    | 즉시 실행 가능    | 복사-붙여넣기로 동작  |
| 8     | 약간 수정 후 실행 | 변수 1-2개 치환 필요  |
| 6     | 적응 작업 필요    | 도메인 맞춤 수정 필요 |
| 4     | 상당한 작업 필요  | 구조적 재작성 필요    |
| 2     | 재작성 필요       | 처음부터 다시         |

### Dimension 4: Innovation (혁신성)

| Score | Description   | Indicator           |
| ----- | ------------- | ------------------- |
| 10    | 패러다임 전환 | 새로운 접근법 제시  |
| 8     | 의미있는 개선 | 기존 대비 30%+ 효율 |
| 6     | 점진적 개선   | 소소한 최적화       |
| 4     | 동등 수준     | 기존과 비슷         |
| 2     | 퇴보          | 기존보다 못함       |

## Prompt Quality Assessment

### Overall Score Formula

```
Total = (Clarity × 0.3) + (Specificity × 0.25) +
        (Actionability × 0.25) + (Innovation × 0.2)
```

### Score Interpretation

| Total | Grade | Action            |
| ----- | ----- | ----------------- |
| 9-10  | A     | 즉시 사용         |
| 7-8.9 | B     | 소폭 조정 후 사용 |
| 5-6.9 | C     | 특정 단계 재작업  |
| 3-4.9 | D     | 대폭 수정 필요    |
| 1-2.9 | F     | 전면 재설계       |

## Self-Critique Protocol

### Weakness Detection Questions

1. "이 프롬프트가 실패할 가능성이 가장 높은 시나리오는?"
2. "AI가 이 지시를 오해할 여지는?"
3. "출력 품질 저하 요인은?"

### Improvement Suggestion Template

```markdown
**약점**: [식별된 약점]
**원인**: [근본 원인]
**개선안**: [구체적 수정 제안]
**예상 효과**: [개선 후 점수 변화]
```

## Iteration Trigger Criteria

| Condition         | Action                 |
| ----------------- | ---------------------- |
| Clarity < 6       | DECONSTRUCT 재실행     |
| Specificity < 6   | 제약조건 추가 질문     |
| Actionability < 6 | 예시/템플릿 보강       |
| Innovation < 6    | 대안 접근법 탐색       |
| Total < 7         | 전체 워크플로우 재실행 |
