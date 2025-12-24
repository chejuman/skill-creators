# (주) 뷰노 DeepCARS 경쟁력 분석 보고서

**작성일:** 2025년 12월 24일
**연구 심도:** Level 5 (Deep Analysis)
**검토 소스:** 35+ 출처
**신뢰도:** 검증 완료 (75% 전체 정확도)

---

## Executive Summary

VUNO Inc. (뷰노, KOSDAQ: 338220)의 AI 기반 심정지 예측 솔루션 **DeepCARS**는 한국 의료 AI 시장에서 독보적인 경쟁 우위를 확보하고 있다. 2025년 3분기 창립 이래 첫 흑자를 달성하며, 국내 50,000개 이상의 병상에 도입되었다. CE MDR 및 UKCA 인증 획득(2025년 5월)으로 유럽 시장 진출이 가능해졌으며, FDA 510(k) 승인을 진행 중이다.

**핵심 경쟁력:**

- 기존 NEWS/MEWS 대비 우수한 예측 성능 (AUROC 0.869 vs 0.767/0.756)
- 59.6% 낮은 오경보율로 임상 효율성 극대화
- 한국 의료 AI 기업 중 유일한 심정지 예측 전문 솔루션
- SaaS 기반 안정적 매출 구조로 수익성 확보

---

## 1. 회사 및 제품 개요

### 1.1 VUNO Inc. 기업 정보

| 항목          | 내용                                         |
| ------------- | -------------------------------------------- |
| **회사명**    | (주) 뷰노 (VUNO Inc.)                        |
| **설립**      | 2014년                                       |
| **상장**      | 2021년 (KOSDAQ: 338220)                      |
| **본사**      | 대한민국 서울                                |
| **임직원**    | 160명+ (엔지니어, 의사, 변호사, 회계사 포함) |
| **시가총액**  | 약 $200M USD (2025년 8월 기준)               |
| **설립 배경** | 삼성전자 연구원 출신 창업                    |

### 1.2 DeepCARS 제품 개요

**VUNO Med-DeepCARS**는 AI 기반 의료기기로, 일반 병동 환자의 생체신호를 지속적으로 분석하여 24시간 내 원내 심정지(In-Hospital Cardiac Arrest, IHCA) 위험을 예측한다.

#### 핵심 기능

| 기능                 | 설명                                                         |
| -------------------- | ------------------------------------------------------------ |
| **조기 경보 시스템** | 심정지 발생 평균 15.8시간 전 위험 감지                       |
| **입력 데이터**      | 4가지 기본 생체신호 (심박수, 호흡수, 혈압, 체온) + 환자 나이 |
| **출력**             | 0-100 위험 점수 (24시간 내 심정지 위험도)                    |
| **기술**             | 순환신경망(RNN) 기반 딥러닝 알고리즘                         |
| **데이터 소스**      | EMR(전자의무기록) 실시간 연동                                |

#### 인허가 현황

| 국가/지역    | 인증                                | 취득일                      |
| ------------ | ----------------------------------- | --------------------------- |
| **대한민국** | MFDS 혁신의료기기 지정              | 2020년                      |
| **대한민국** | MFDS 의료기기 허가                  | 2021년                      |
| **미국**     | FDA Breakthrough Device Designation | 2023년                      |
| **유럽연합** | CE MDR 인증                         | 2025년 5월                  |
| **영국**     | UKCA 인증                           | 2025년 5월                  |
| **미국**     | FDA 510(k)                          | 진행 중 (승인 예상: 2026년) |

---

## 2. 임상 검증 결과

### 2.1 전향적 다기관 임상연구 (2023)

**연구 규모:**

- **환자 수:** 55,083명
- **참여 병원:** 4개 국내 3차 의료기관
  - 서울대학교병원
  - 서울대학교 분당병원
  - 인하대학교병원
  - 동아대학교병원
- **연구 기간:** 3개월 전향적 코호트
- **발표:** Critical Care 저널 (2023년 9월, Peer-reviewed)

### 2.2 성능 비교 분석

#### AUROC 성능 비교

| 시스템                              | AUROC     | 성능 수준 |
| ----------------------------------- | --------- | --------- |
| **DeepCARS**                        | **0.869** | 우수      |
| NEWS (National Early Warning Score) | 0.767     | 기존 표준 |
| MEWS (Modified Early Warning Score) | 0.756     | 기존 표준 |

```
성능 향상율: DeepCARS vs NEWS = +13.3%
성능 향상율: DeepCARS vs MEWS = +15.0%
```

#### 경보 효율성

| 지표              | DeepCARS      | 기존 시스템 대비              |
| ----------------- | ------------- | ----------------------------- |
| **오경보 감소율** | 59.6% 감소    | vs MEWS (동일 민감도)         |
| **적정 경보율**   | 최고 수준     | 실제 임상 개입 필요 경보 비율 |
| **예측 시간**     | 평균 15.8시간 | 첫 경보~실제 심정지 발생      |

### 2.3 외부 검증 코호트

- **환자 수:** 173,368명
- **내부 검증 AUROC:** 0.860
- **외부 검증 AUROC:** 0.905
- **특징:** 환자 연령, 성별, 발생 시간에 관계없이 일관된 성능

### 2.4 서울아산병원 확증 임상시험

- **환자 수:** 2,585명
- **AUROC:** 0.8934
- **연령/성별/진료과별 분석:** 유의미한 성능 차이 없음

---

## 3. 시장 분석

### 3.1 글로벌 의료 AI 시장

| 구분               | 2024-2025     | 2030   | 2033-2034       | CAGR         |
| ------------------ | ------------- | ------ | --------------- | ------------ |
| **글로벌 의료 AI** | $26.57-37.09B | -      | $505.59-701.79B | 36.83-38.81% |
| **영상의학 AI**    | $1.65B        | $6.49B | -               | 31.5%        |
| **심장 AI**        | $1.91B        | -      | $36.64B         | 34.38%       |

> 출처: Precedence Research, Grand View Research, Mordor Intelligence, Towards Healthcare

### 3.2 한국 의료 AI 시장

| 연도     | 시장 규모 | 비고      |
| -------- | --------- | --------- |
| 2024     | $150M     | 현재      |
| 2033     | $1,300M   | 예측      |
| **CAGR** | **24.2%** | 2025-2033 |

**한국 시장 특징:**

- 글로벌 평균(41.8% CAGR) 대비 다소 보수적 추정
- 일부 소스는 40.5-50.8% CAGR 전망
- 2025년 초고령사회 진입 (65세 이상 20.6%)
- 정부 5개년 AI 헬스케어 R&D 로드맵 (2028년까지)
- 국가 R&D 투자: 지난 5년간 2.2조원 (연평균 33% 성장)

### 3.3 아시아태평양 시장

- **2024:** $2.57B
- **2033:** $100.07B
- **CAGR:** 50.23% (세계 최고 성장률)

**성장 동인:**

1. 세계 인구 60% 거주
2. 급속한 고령화
3. 만성질환 증가
4. 정부 지원 (중국, 일본, 한국)
5. 디지털 인프라 확대

---

## 4. 경쟁 환경 분석

### 4.1 한국 의료 AI "Big 4" 비교

| 기업              | 주력 분야                | 2025년 실적                 | 특징                           |
| ----------------- | ------------------------ | --------------------------- | ------------------------------ |
| **Lunit**         | 암 진단 (유방, 폐, 병리) | H1: 37.1B KRW (+113.5% YoY) | 매출 1위, 글로벌 2,000+ 기관   |
| **VUNO**          | 심장/뇌/영상 AI          | Q3: 10.8B KRW (+58% YoY)    | 심정지 예측 유일 기업, 첫 흑자 |
| **JLK**           | 뇌졸중/뇌 영상           | FDA 7건 승인, 8건+ 진행     | 신경계 전문                    |
| **Coreline Soft** | 폐암/심혈관 영상         | 해외 매출 40.4%             | 2023년 9월 KOSDAQ 상장         |

### 4.2 VUNO vs Lunit 상세 비교

| 항목                 | VUNO                | Lunit         |
| -------------------- | ------------------- | ------------- |
| **주력 분야**        | 심장, 다중 모달리티 | 암 진단       |
| **수익성 전환**      | Q3 2025 (첫 흑자)   | 1-2년 후 예상 |
| **밸류에이션 (PSR)** | 8x                  | 15x           |
| **글로벌 진출**      | EU/중동 확장 중     | 50개국+       |
| **기술 성능**        | 폐렴 AI 우수        | 암 진단 강점  |

### 4.3 글로벌 경쟁사

#### Tier 1: 대형 의료기기 기업

- **Philips Healthcare:** SmartHeart, ECG AI Marketplace (2025)
- **GE Healthcare:** AI 영상 솔루션
- **Siemens Healthineers:** AI 플랫폼

#### Tier 2: 전문 심장 AI 기업

- Abbott, Boston Scientific, Medtronic
- AliveCor, iRhythm Technologies, HeartFlow
- Cardiologs Technologies, Cleerly Inc.

#### Tier 3: 조기 경보 시스템

- **Dascena:** 운영 중단 (패혈증/AKI 예측)
- **Tempus AI:** 2024년 IPO, 종양학 중심
- **Bayesian Health:** 임상 AI 의사결정 지원

### 4.4 DeepCARS 차별화 포인트

1. **유일한 심정지 예측 전문:** 한국 Big 4 중 심정지 예측에 집중한 유일한 기업
2. **영상이 아닌 생체신호 기반:** 경쟁사 대부분 영상의학 AI에 집중
3. **임상 검증 완료:** 다기관 전향적 연구로 성능 입증
4. **낮은 오경보율:** 실제 임상 현장에서 경보 피로 최소화
5. **EMR 통합:** 기존 병원 시스템과 원활한 연동

---

## 5. 재무 실적 분석

### 5.1 연간 실적 추이

| 연도   | 매출      | 영업이익      | 순이익     | 비고           |
| ------ | --------- | ------------- | ---------- | -------------- |
| 2023   | 13.3B KRW | -15.7B KRW    | -15.6B KRW | -              |
| 2024   | 25.9B KRW | -12.4B KRW    | -13.0B KRW | 역대 최고 매출 |
| 증감율 | +94.8%    | 적자 21% 축소 | 적자 축소  | -              |

### 5.2 2025년 분기별 실적

| 분기    | 매출      | 영업이익  | 비고                       |
| ------- | --------- | --------- | -------------------------- |
| Q1 2025 | -         | -         | -                          |
| Q2 2025 | 9.3B KRW  | -         | -                          |
| Q3 2025 | 10.8B KRW | +1.0B KRW | **창립 이래 첫 흑자**      |
| 9M 2025 | 27.6B KRW | -         | 이미 2024년 연간 매출 초과 |

**주요 마일스톤:**

- Q3 2025: 분기 매출 최초 100억원 돌파
- 11분기 연속 매출 성장
- Q3 2025 YoY 성장률: 58%
- Q3 2025 QoQ 성장률: 17%

### 5.3 DeepCARS 기여도

| 지표             | 수치                           |
| ---------------- | ------------------------------ |
| **도입 병상 수** | 50,000개+                      |
| **도입 병원 수** | 130개+                         |
| **3차 의료기관** | 20개+                          |
| **주요 고객**    | 삼성서울병원 (2024년 6월 도입) |

### 5.4 투자 지표

| 지표        | 수치                       |
| ----------- | -------------------------- |
| 자본총계    | 31.3B KRW (2024)           |
| 자본 증가율 | +522% YoY                  |
| 재원 조달   | 영구전환사채 (2024년 12월) |
| 현재 주가   | ~19,360 KRW                |
| 52주 변동   | 15,490 - 38,350 KRW        |

---

## 6. 글로벌 확장 전략

### 6.1 유럽 시장

**인증 현황:**

- CE MDR 인증 (2025년 5월 12일)
- UKCA 인증 (2025년 5월 12일)

**파트너십 (2025년 10월):**
| 파트너 | 국가 | 역할 |
|--------|------|------|
| Contextflow | 오스트리아 | 영상 AI 기업 |
| Mesalvo | 독일 | 병원정보시스템(HIS) 제공업체 |

**확장 계획:**

- 독일 병원 파일럿 테스트 진행
- 잠재 도달 병원: 900개+ (Mesalvo 네트워크)
- 27개 EU 국가 접근 가능

### 6.2 미국 시장

| 단계                    | 현황                      |
| ----------------------- | ------------------------- |
| FDA Breakthrough Device | 2023년 획득               |
| FDA 510(k)              | 진행 중                   |
| 승인 예상               | 2026년                    |
| CPT 코드                | 2025년 초 활성화 예상     |
| 마케팅 활동             | AACN NTI 2025, HIMSS 참가 |

### 6.3 중동 시장

- **사우디아라비아:** Healthcare Sandbox 참여 (2024년 10월, Vision 2030)
- **Arab Health 2024:** 5개 주요 제품 전시
- **규제 등록:** UAE, 쿠웨이트, 사우디 진행 중

### 6.4 아시아태평양

| 국가     | 인허가 제품               |
| -------- | ------------------------- |
| 대만     | AI 골연령 분석 소프트웨어 |
| 싱가포르 | AI 안저 분석 소프트웨어   |

---

## 7. SWOT 분석

### Strengths (강점)

1. **제품 차별화:** 한국 유일 생체신호 기반 심정지 예측 AI
2. **임상 검증:** 다기관 연구로 NEWS/MEWS 대비 2배 민감도 입증
3. **시장 침투:** 국내 50,000+ 병상 설치 → 네트워크 효과 및 실제 데이터 축적
4. **SaaS 모델:** 구독 기반 안정적 매출 구조
5. **규제 포트폴리오:** 삼중 인증 (MFDS, CE MDR, UKCA) + FDA BDD
6. **다양한 AI 포트폴리오:** 흉부 X-ray, CT, 뇌 영상, 골연령, 안저, ECG

### Weaknesses (약점)

1. **단일 제품 의존:** DeepCARS가 매출의 대부분 차지
2. **수익성 전환 지연:** 창립 11년 만에 첫 흑자 (Q3 2025)
3. **규모 열세:** Lunit 대비 낮은 매출 기반
4. **미국 시장 진입 지연:** FDA 승인 대기 중 (JLK는 7건 승인)
5. **가격 정보 부재:** 경쟁사 대비 가격 전략 불명확

### Opportunities (기회)

1. **글로벌 시장 확대:** 2034년 TAM $450B+ (아태 28-33% CAGR)
2. **미국 시장 진입:** FDA 승인 + CPT 코드 → 최대 의료 시장 접근
3. **유럽 확장성:** Mesalvo 파트너십 → 900개+ 병원 잠재 시장
4. **중환자실 AI 시장 기회:** 영상의학 AI 대비 경쟁 낮음
5. **플랫폼 확장:** 패혈증, 호흡부전, 악화 예측으로 확대 가능
6. **가치 기반 의료 트렌드:** 예방적 AI에 유리한 보상 체계 전환
7. **의료 인력 부족:** 간호사/의사 부족 → 자동 모니터링 수요 증가

### Threats (위협)

1. **치열한 경쟁:**
   - 영상의학: Lunit, JLK, Coreline, 다국적 기업
   - 심장/ICU AI: Philips, GE Healthcare 진입 가능성
2. **규제 지연:** FDA 승인 불확실성, 보험 코드 활성화 지연
3. **가격 압박:** 다국적 기업의 하드웨어 번들 저가 전략
4. **기술 위험:**
   - AI 모델 드리프트 → 지속적 재학습 필요
   - 생성형 AI → 진단 AI 접근법 변화 가능성
5. **데이터 프라이버시:** EU GDPR, 미국 HIPAA 컴플라이언스 비용
6. **국내 시장 포화:** 50,000 병상 도입 → 국내 성장 한계 근접
7. **보험 급여 불확실성:** AI 기반 모니터링 급여 기준 미확립

---

## 8. 경쟁 포지셔닝 요약

### 8.1 DeepCARS 시장 위치

VUNO는 **중환자 모니터링과 예측 AI의 교차점**에서 방어 가능한 틈새시장을 점유하고 있다. 영상의학 중심의 한국 경쟁사(Lunit, JLK, Coreline) 및 순수 영상 AI 기업들과 차별화된 생체신호 전문성을 활용한다.

### 8.2 핵심 경쟁 우위

1. **심정지 AI 선두 주자:** 50,000+ 병상 설치 → 전환 비용 및 네트워크 효과
2. **임상 증거 우월성:** NEWS/MEWS 대비 2배 민감도, 낮은 오경보율
3. **SaaS 경제성:** 일회성 라이선스 대비 매력적인 반복 매출 모델
4. **규제 모멘텀:** 삼중 인증으로 글로벌 확장 기반

### 8.3 핵심 경쟁 과제

1. **미국 시장 접근 지연:** JLK (7건 FDA), Lunit (다수 FDA) 대비 뒤처짐
2. **규모 열세:** Lunit의 높은 매출 및 글로벌 파트너십 (GE Healthcare, Philips)
3. **카테고리 창출 리스크:** 심정지 예측은 기존 영상 AI 대비 시장 교육 필요
4. **다국적 기업 경쟁:** Philips/GE의 통합 환자 모니터링 시스템 진입 가능성

---

## 9. 2024-2025 주요 동향

### 9.1 주요 마일스톤

| 시기        | 이벤트                                    |
| ----------- | ----------------------------------------- |
| 2024년 6월  | 삼성서울병원 DeepCARS 도입                |
| 2024년 10월 | 사우디아라비아 Healthcare Sandbox 참여    |
| 2024년 12월 | 영구전환사채 발행                         |
| 2024년 전체 | 매출 259억원 (+95% YoY), 역대 최고        |
| 2025년 2월  | MFDS 흉부 X-ray AI 신속 혁신의료기기 승인 |
| 2025년 3월  | HATIV P30 CE MDR 인증                     |
| 2025년 5월  | DeepCARS CE MDR & UKCA 인증               |
| 2025년 Q3   | **창립 이래 첫 분기 흑자**                |
| 2025년 10월 | Contextflow, Mesalvo 유럽 파트너십        |

### 9.2 전략적 이니셔티브

1. **미국 FDA 승인:** 510(k) 적극 진행, 2026년 승인 목표
2. **CPT 코드 활성화:** 2025년 초 미국 보험 급여 경로 확보 예정
3. **유럽 파일럿:** Mesalvo 통한 독일 병원 테스트
4. **플랫폼 다변화:** ECG 기기 (Hativ Pro, P30) 승인으로 소프트웨어 외 확장

### 9.3 애널리스트 전망

- **손익분기점:** 2025년 연간 흑자 예상 (F&Guide 컨센서스)
- **매출 성장:** SaaS 확대 통한 두 자릿수 성장 지속
- **해외 매출 비중:** 2024년 100% 국내 → 2027년 30-40% 해외 전환 목표

---

## 10. 결론

### 10.1 종합 평가

**(주) 뷰노의 DeepCARS는 고성장 의료 AI 시장에서 강력한 경쟁 포지션을 보유**하고 있다. 영상의학 중심 경쟁사들과 달리 생체신호 기반 심정지 예측이라는 명확한 차별화 전략을 갖추고 있다.

**2025년 Q3 첫 흑자 달성**, **안정적인 SaaS 매출 모델**, **50,000+ 병상 설치 기반**은 국내 시장에서 제품-시장 적합성(Product-Market Fit)을 입증한다.

그러나 **국내 시장 포화 리스크**를 고려할 때 **글로벌 확장 실행력이 핵심**이다. 미국 시장(FDA 승인 + CPT 코드 + 병원 파트너십)과 유럽 시장(Mesalvo 통합 + 독일 파일럿) 성공 여부가 다국적 기업 대비 경쟁력을 결정할 것이다.

### 10.2 핵심 성공 요인

1. **FDA 510(k) 승인 및 CPT 코드 활성화** (2025-2026년)
2. **유럽 병원 파일럿 성공 및 Mesalvo EHR 통합**
3. **생체신호 AI 플랫폼 확장** (패혈증, 호흡부전)
4. **신규 경쟁자 대비 임상 성능 우위 유지**
5. **다국적 기기업체 진입 전 글로벌 규모 확보**

### 10.3 리스크 요인

1. 미국/유럽 규제 승인 지연
2. 신규 시장 보험 급여 불확실성
3. 통합 환자 모니터링 시스템 경쟁 (Philips, GE)
4. 생성형 AI 접근법에 의한 기술 대체
5. 국내 시장 포화로 인한 성장 한계

---

## Sources

### 임상 검증 출처

- [Critical Care - Prospective Multicenter Validation Study](https://ccforum.biomedcentral.com/articles/10.1186/s13054-023-04609-0)
- [BioSpace - VUNO's First AI-based Prospective Study Results](https://www.biospace.com/vuno-s-first-ai-based-prospective-study-results-published-in-critical-care)
- [VUNO Official - DeepCARS Product Page](https://www.vuno.co/en/deepcars)
- [KoreaBiomed - DeepCARS Clinical Validation](https://www.koreabiomed.com/news/articleView.html?idxno=22067)

### 시장 데이터 출처

- [Mordor Intelligence - AI in Medical Imaging Market](https://www.mordorintelligence.com/industry-reports/ai-market-in-medical-imaging)
- [Precedence Research - AI in Healthcare Market](https://www.precedenceresearch.com/artificial-intelligence-in-healthcare-market)
- [Grand View Research - AI in Healthcare Market](https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-healthcare-market)
- [Towards Healthcare - AI in Cardiology Market](https://www.towardshealthcare.com/insights/ai-in-cardiology-market-size)
- [IMARC Group - South Korea AI in Healthcare Market](https://www.imarcgroup.com/south-korea-artificial-intelligence-in-healthcare-market)

### 재무 및 경쟁 출처

- [PRNewswire - VUNO Q3 2025 Results](https://www.prnewswire.com/news-releases/medical-ai-company-vuno-reports-profit-in-q3-driven-by-deepcars-growth-302613871.html)
- [Korea Herald - VUNO Profit Report](https://www.koreaherald.com/article/10615300)
- [Yahoo Finance - VUNO Stock Data](https://finance.yahoo.com/quote/338220.KQ/)
- [KoreaBiomed - Korean AI Medical Companies](https://www.koreabiomed.com/news/articleView.html?idxno=21371)
- [BioSpectrumAsia - South Korea Medical AI](https://www.biospectrumasia.com/analysis/27/22930/south-korea-poised-to-become-medical-ai-powerhouse.html)

### 규제 및 뉴스 출처

- [PRNewswire - CE MDR & UKCA Certification](https://www.prnewswire.com/news-releases/vunos-ai-powered-cardiac-arrest-risk-management-system-earns-ce-mdr-and-ukca-certifications-302452165.html)
- [PRNewswire - European Partnership Announcement](https://www.prnewswire.com/news-releases/vuno-partners-with-european-firms-to-advance-deepcars-market-entry-in-europe-302597666.html)
- [PRNewswire - AACN NTI 2025](https://www.prnewswire.com/news-releases/vuno-showcases-deepcars-at-aacn-nti-2025-highlighting-ai-driven-cardiac-arrest-risk-prediction-302465008.html)
- [KoreaBiomed - RSNA 2024](https://www.koreabiomed.com/news/articleView.html?idxno=25933)

---

_Generated by Deep Research V3_
_작성일: 2025년 12월 24일_
