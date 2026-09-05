# 수출거래 AI 금융진단 — 제출 원고 기준

## 한 문장

수출거래 AI 금융진단은 계약서·PO·재무제표와 회사 자금계획을 구조화하고, 결정론적 금융엔진이 거래 수익성·회사 전체 유동성·외화노출·Stress·대응안을 계산한 뒤, 읽기 전용 AI가 현재 근거의 의미만 설명하는 B2B 계약 전 금융의사결정 지원 서비스다.

---

## 문제 정의

수출거래는 매출액과 표면 마진만으로 판단하기 어렵다.

기업은 계약 체결 후 실제 수금까지 생산비·외화 원재료·물류비를 먼저 지급해야 하고, 같은 시기에 급여·세금·설비대금 등 기존 회사 자금계획도 집행된다. 여기에 USD/JPY 환율, 조달금리, 수금지연이 겹치면 거래 자체는 흑자여도 특정 시점의 회사 현금이 부족할 수 있다.

특히 중소·중견 수출기업은 대기업처럼 전담 Treasury 조직과 통합 시스템을 갖추기 어렵다. 선물환·환변동보험·운전자금·매출채권 금융 등 금융수단은 이미 존재하지만, 어떤 거래에서 언제 얼마가 부족하고 어떤 위험을 먼저 검토해야 하는지를 계약 전에 수치화하는 일은 여전히 기업의 부담이다.

본 서비스는 이 공백을 새로운 금융상품이 아니라 `계약 전 사전진단` 문제로 정의한다.

---

## 현장 문제의식

제조·엔지니어링 프로젝트에서는 설계, 조달, 생산일정, 협력사 지급과 같은 요소가 연결될 때 개별 숫자보다 전체 일정과 자원의 흐름을 함께 보는 것이 중요하다.

이 관점을 수출거래에 적용했다. 수출대금, 외화원가, 국내 생산비, 지급일, 수금일, 회사 기존 현금계획을 하나의 타임라인으로 연결하면 계약의 실제 금융 부담을 더 정확하게 볼 수 있다.

---

## 시장·문헌 검토

본 아이디어의 필요성이 개인적 문제의식에 그치지 않는지 확인하기 위해 무역·중소기업 관련 조사, 연구기관 자료와 기업용 FX/Treasury 상용사례를 검토했다.

핵심 확인 내용:

- 한국무역협회 조사에서 수출기업 46.7%가 전 분기 대비 자금사정 악화를 경험했고, 매출 50억원 미만 기업은 57.4%로 더 높았다. 환율변동도 자금사정 악화의 주요 원인으로 조사됐다.
- 환율 상승은 단순한 수출 호재가 아니다. 직접효과만 보면 수익성이 개선되는 수출기업 비중이 61.8%였지만, 수입원가·물가 등 장기 간접효과까지 반영하면 19.9%로 크게 낮아진다는 연구가 있다.
- 중소기업은 대기업 대비 환율 예측·대응 역량과 전략적 헤지 활용이 상대적으로 제한적이라는 연구가 있다.
- Kantox, Kyriba 등 글로벌 기업용 서비스는 ERP/TMS에서 외화노출과 현금흐름을 수집해 FX·Treasury 의사결정을 자동화하고 있다. 이는 기업 금융데이터를 통합해 사전에 위험을 보는 수요가 이미 상용화되고 있음을 보여주는 참고사례다.

따라서 초기 적용 범위를 전체 TMS가 아니라 `한국 수출기업의 단일 계약 사전진단`으로 좁혔다.

---

## 서비스 컨셉과 차별성

### 1. 회사 전체 자금계획 반영

거래 단독 필요자금만 보지 않는다.

현재 MVP는 다음 관계를 한 화면에서 보여준다.

```text
이번 거래 필요 외부자금      6,900만원
        ↓ 회사 기존 일정 포함
회사 전체 최대 자금부족      8,900만원
        ↓ 현재 미사용 한도 7,000만원
현재 한도 반영 후 남는 부족  1,900만원
```

가장 부족한 날은 `2026-11-03 / D+60`이다.

### 2. 금융 숫자는 결정론적으로 계산

AI가 마진, 자금부족액, 환노출이나 금융비용을 계산하지 않는다.

모든 권위 있는 금융수치는 Python 결정론적 엔진이 계산한다.

### 3. AI는 문서 구조화와 설명에 한정

AI 역할은 정확히 세 가지다.

1. Trade Document Financialization
2. Financial Statement Financialization
3. Single Deal Review Agent

Agent는 네 개의 읽기 전용 근거도구를 사용하고, 성공 시 두 번의 모델 요청으로 현재 계산근거의 의미만 설명한다. 금융상품 추천, 승인예측, 환율예측, 실제 금융실행은 하지 않는다.

### 4. 결과 우선 UX

사용자는 처음 접속하면 `분석` 화면에서 기본 가상사례의 결과를 먼저 본다.

원시 숫자 입력은 필요한 경우에만 `입력`에서 수정하며, preset Stress는 별도 계산버튼 없이 선택만으로 Base 대비 변화를 확인한다.

---

## 현재 MVP 구현 기능

- 거래조건 직접 입력 및 수정
- Sales Contract / USD Supplier PO / JPY Supplier PO PDF 업로드와 AI 구조화
- bundled fictional financial statement AI 구조화
- ERP export CSV 및 회사 자금계획 편집
- Deal economics / dated cashflow / financing-adjusted Deal Margin
- company-wide liquidity timeline
- working-capital line 반영 후 residual gap 계산
- USD / JPY exposure와 natural offset 분석
- USD -5%, JPY +10%, 금리 +1%p, 회수 +30일, 복합 악화 Stress 비교
- deterministic target / break-even USD/KRW threshold
- O/A receivable early purchase 비교
- user-assumption Forward Hedge simulation
- Banker's Usance financing comparison
- optional K-SURE aggregate payment context
- 4개 read-only tool 기반 Single Deal Review Agent
- 현재 근거 기반 인메모리 PDF 보고서
- `입력 | 분석 | 보고서` responsive web UI

---

## 사용자 흐름

1. 공개 URL에 접속하면 `분석` 화면에서 기본 가상사례의 현재 결과를 확인한다.
2. `USD -5%`, `복합 악화` 등 preset Stress를 선택해 Base 대비 마진·자금·회수 변화를 확인한다.
3. `대응안 비교`에서 기존 운전자금, 매출채권 조기 현금화, 선물환, Banker's Usance의 `현재 → 대안 → 변화`를 확인한다.
4. 필요하면 `입력`에서 거래·회사 정보를 수정하거나 거래서류를 불러온다.
5. `보고서`에서 선택적으로 AI 거래 검토를 실행한다.
6. 현재 조건의 PDF 보고서를 다운로드한다.

---

## 심사위원 검증 포인트

| Action | Expected Result |
|---|---|
| URL 접속 | `분석` 기본 진입, 현재 마진 14.64% |
| 현재 자금관계 확인 | 거래 필요자금 6,900만원 → 회사 최대부족 8,900만원 → 한도 후 남는 부족 1,900만원 |
| `USD -5%` 선택 | 마진 11.20% |
| `복합 악화` 선택 | 마진 8.83%, 회수 D+120 |
| `매출채권 조기 현금화` 확인 | D+90 → D+65 및 자금·비용 변화 |
| `Banker's Usance` 확인 | 일반 운전자금 부담 감소, 총 은행원금은 사라지지 않음을 비교 |
| `보고서` → `이 조건으로 거래 검토` | 4개 read-only tool 기반 현재 거래 검토 |
| `보고서 다운로드` | 현재 조건 기반 `수출거래 AI 금융진단 보고서` 생성 |

---

## 활용 데이터와 외부 데이터 경계

현재 MVP 데이터:

- 가상의 Sales Contract / USD PO / JPY PO
- 가상의 KRW financial statement
- 가상의 ERP cash-plan CSV
- 사용자 직접 입력
- 사용자가 명시적으로 조회한 K-SURE 국가·업종 결제완료 집계정보

K-SURE는 개별 바이어 부도확률이나 신용점수가 아니며 거래조건을 자동 변경하지 않는다.

한국수출입은행 reference-FX adapter는 로컬 검증됐지만 공개 Streamlit 환경에서의 신뢰성을 입증하지 못해 public core path에서는 비활성화했다.

한국은행 ECOS와 OpenDART는 현재 MVP에 연결하지 않았다.

이 결정은 외부 API 장애가 핵심 금융계산을 중단시키지 않도록 하기 위한 것이다.

---

## 공개 MVP 보안·데이터 처리 고지

심사용 기본 문서는 모두 가상 데이터다.

현재 공개 MVP는 별도 영구 데이터베이스와 사용자 인증을 제공하지 않는다.

사용자가 Trade Document AI 또는 Financial Statement AI를 명시적으로 실행하면 선택된 PDF 내용은 구조화 처리를 위해 설정된 OpenAI API로 전송되며, 해당 요청은 `store=False`로 수행된다.

따라서 공개 심사용 배포환경에는 실제 영업비밀, 개인정보 또는 기밀 기업문서 업로드를 권장하지 않는다.

금융계산은 OpenAI나 외부 공공데이터 키 없이도 결정론적으로 동작한다.

---

## 기대 효과

### 기업

- 거래 수익성과 회사 전체 유동성을 계약 전에 함께 확인
- 환율·원부자재·금융비용·수금지연이 결합된 Stress 확인
- 금융수단의 비용과 자금효과를 실행 전에 비교
- 전담 Treasury 조직이 없는 기업의 사전 의사결정 부담 완화

### 금융기관

- 기업과 Corporate RM이 거래마진, 최대 자금부족 시점, 현재 한도 반영 후 잔여부족, 통화별 외화노출을 동일한 근거로 공유
- 운전자금·매출채권 금융·Trade Finance·FX 상담의 출발점 표준화에 활용 가능

본 서비스는 금융기관의 승인·심사·실행을 대체하지 않는다.

---

## 상용화 방향

### 기업 실증

- 공식 reference data의 출처·기준일·실패상태 관리
- ERP / 회계 / TMS API 또는 SFTP 연계
- 여러 거래의 Exposure 및 현금흐름 통합

### AI 확장

- Invoice, L/C, 선적서류, 은행조건서 등 문서 구조화 범위 확대
- 계약·ERP·은행조건 간 불일치 탐지
- 현재 Exposure 구조를 바탕으로 확인할 Stress 조건 제안
- Corporate RM 상담용 사전자료 작성

AI가 제안하더라도 권위 있는 숫자는 계속 결정론적 엔진이 계산한다.

### 금융기관 연계

기업 진단결과와 금융기관의 상담·상품조건을 연결하되, 실제 승인·계약·헤지·대출·송금은 사람과 금융기관의 최종 확인 후 실행한다.

### 보안·거버넌스

상용화 시 다음을 별도 설계한다.

- 기업별 데이터 분리
- 전송·저장 암호화
- 역할 기반 권한관리
- 감사로그와 보존·삭제정책
- Secret / Key 관리
- 모델·클라우드 공급자 거버넌스
- Prompt Injection 등 AI 보안성 검증과 레드팀 테스트

금융 AI는 업무 보조수단으로 사용하고 사람의 최종 책임과 결정을 유지한다.

---

## 현재 MVP 제한사항

현재 MVP에 포함하지 않는 기능:

- 실제 금융상품 신청·승인·실행
- 실제 송금·선물환 주문·대출 실행
- 은행 승인 또는 바이어 부도 예측
- 환율·금리 예측
- full L/C / UPAS / D/A / D/P workflow
- 보험·보증 실행
- 실시간 ERP / 은행 연동
- public Eximbank FX / BOK ECOS / OpenDART 연동
- database / authentication
- RAG / arbitrary web search
- multi-agent
- EUR / CNY engine expansion

---

## 제출 기준

Current canonical product is the code and behavior defined by `docs/product-spec.md`.

No submission document may claim an unimplemented feature.
