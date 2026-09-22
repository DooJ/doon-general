# 여행 복합 스킬 오케스트레이션 계약

## 사용 조건

전체 여행 계획, 서로 다른 두 개 이상의 여행 조사 영역, 확정 예약과 후보를 함께 재배치하는 요청에서 이 계약을 사용합니다. 항공편만, 숙소만처럼 독립 부분 요청 하나로 끝나는 경우에는 해당 전문 스킬로 직접 라우팅하고 이 전체 그래프를 만들지 않습니다.

## 정규화된 컨텍스트

오케스트레이터는 다음 값을 가능한 범위에서 구성합니다.

```yaml
context_revision: 1
origin: null
destination: null
dates:
  start: null
  end: null
  flexibility: null
travelers: []
companion_type: null
priorities: []
budget: null
mobility_preferences: []
constraints: []
confirmed_reservations: []
requested_capabilities: []
output_preference: chat
```

사용자가 날짜, 인원, 목적지, 확정 예약, 숙소 권역, 핵심 장소처럼 결과를 바꾸는 값을 수정할 때마다 `context_revision`을 올립니다. 이전 revision에 의존하는 결과는 `freshness: stale`로 표시하고 영향받은 작업과 그 하위 의존 작업만 다시 실행합니다.

## 전문 스킬 라우팅

| 요청 범위 | 스킬 | 기본 종료점 |
|---|---|---|
| 항공·배·장거리 열차 검색 | `travel-flight-search` | 이동편 비교 |
| 숙소 권역·호텔 검색 | `travel-lodging-search` | 권역 및 숙소 비교 |
| 날씨·입국·결제·통신·안전 | `travel-destination-research` | 현지 정보 브리핑 |
| 관광지·식당·카페·쇼핑 | `travel-place-search` | 권역별 장소 후보 |
| 공항 접근·도시 내 구간 이동 | `travel-transport-search` | 구간별 교통 비교 |
| 조사 결과·예약의 일정화 | `travel-itinerary-builder` | 실행 일정과 검증 |

요청한 범위에 필요한 스킬만 선택합니다. 부분 요청에 전체 여행 일정을 붙이지 않으며, 여러 부분을 요청했더라도 일정 합성을 원하지 않으면 조사 결과만 제공합니다.

## 전체 요청과 도메인 커버리지

도시·지역과 날짜 또는 박수가 주어진 "여행 일정", "여행 계획", "코스 짜줘" 요청은 사용자가 범위를 줄이지 않은 한 **전체 여행 요청**입니다. 예를 들어 "9월 26일 방콕 3박 4일 여행 일정"은 관광지만 배치하는 요청으로 축소하지 않습니다.

오케스트레이터는 실행 전에 다음 도메인 커버리지 표를 만들고 최종 결과까지 상태를 유지합니다.

```yaml
coverage:
  long_distance_transport: ready | confirmed_input | user_excluded | partial | blocked
  lodging: ready | confirmed_input | user_excluded | partial | blocked
  destination: ready | confirmed_input | user_excluded | partial | blocked
  place: ready | confirmed_input | user_excluded | partial | blocked
  local_transport: ready | confirmed_input | user_excluded | partial | blocked
  itinerary: ready | partial | blocked
```

- 항공·장거리 이동: 해외는 항공·국제철도·페리, 국내는 항공·철도·시외버스·자가용·렌터카 등 실제 선택지를 비교합니다.
- 숙소: 권역 차이만 설명하고 끝내지 않고 대표 숙소를 붙이거나 사용자의 권역 선택 질문 하나를 남깁니다.
- 목적지 정보: 날씨·공휴일과 국내외 안전 정보, 해외면 입국·결제·통신을 포함합니다.
- 장소: 관광지와 동선별 식당·카페를 포함합니다.
- 현지 교통: 도착 거점, 숙소, 장소 사이의 실제 이동을 포함합니다.
- 일정 합성: 앞선 결과를 시간·위치·비용 체인으로 검증합니다.

필수 도메인을 조용히 생략할 수 없습니다. 일부만 확인한 도메인은 `partial`, 실행하지 못한 도메인은 `blocked`와 해소 방법을 기록하고 전체 결과를 `partial`로 유지합니다. 사용자가 명시적으로 제외한 도메인만 `user_excluded`로 처리하며, 에이전트가 편의를 위해 이 값을 만들지 않습니다. 작업을 시작했다는 사실만으로 `ready`를 기록하지 않습니다.

## 부족한 정보 결정

1. 결과를 크게 바꾸는 필수 값이 하나 없으면 질문 하나를 합니다. 출발지가 없으면 출발 도시·공항·역을 묻는 것이 우선입니다.
2. 질문에 의존하지 않는 도메인 조사는 먼저 수행할 수 있습니다.
3. 초안을 바로 제공하는 편이 유용하면 성인 2명, 일반 예산, 표준 체력처럼 명시적 일반 가정을 선언합니다.
4. 일반 가정은 `assumed`이며 검색 사실이나 예약 사실로 승격하지 않습니다.
5. 출발지·인원·예산이 없다는 이유로 해당 도메인을 조용히 생략하지 않습니다. 정확한 실검색이 불가능하면 일반 후보와 필요한 확인 질문을 함께 제공합니다.

## 작업 단위

각 worker 작업은 다음 계약을 사용합니다.

```yaml
task_id: trip-001-flight
capability: flight
context_revision: 1
scope: "요청에서 허용한 조사 범위"
inputs: {}
dependencies: []
expected_output: DomainResult
done_criteria: []
verification: []
failure_policy: partial | block
```

- `dependencies`가 비어 있고 동일한 `context_revision`을 읽는 작업만 독립 작업으로 봅니다.
- `failure_policy: partial`이면 확인된 결과와 누락 영향을 반환하고 다른 독립 작업을 계속합니다.
- `failure_policy: block`이면 의존 작업을 실행하지 않고 차단 사유와 해소 방법을 반환합니다.

## 병렬 실행 조건

다음 조건을 모두 만족할 때만 실제 서브 에이전트를 통한 병렬 수집을 사용합니다.

1. 현재 runtime에 실제 서브 에이전트 실행 도구가 있습니다.
2. 실행할 독립 작업이 둘 이상입니다.
3. 각 작업의 입력, 완료 조건, 검증 방법과 출력 계약을 분리할 수 있습니다.
4. 모든 작업이 동일한 `context_revision`을 사용합니다.
5. 작업들이 같은 파일이나 전역 상태를 동시에 수정하지 않습니다.

실행 뒤에는 각 서브 에이전트의 실제 도구 호출 증거, 역할, 결과 상태를 기록합니다. 도구가 목록에 있다는 사실, 프롬프트에 역할을 나눠 썼다는 사실, 동시에 시작했다고 추정한 사실만으로 병렬 실행을 주장하지 않습니다.

서브 에이전트 worker는 다음 행동을 하지 않습니다.

- 사용자에게 독립적으로 질문
- 예약·결제·로그인 또는 개인정보 입력
- 최종 여행 문서 작성
- 다른 worker 결과 변경
- 전역 상태, `context_revision`, 선택 상태 수정

## 순차 대체 실행

서브 에이전트 기능이 없거나 독립성을 보장할 수 없으면 결과에 `single-agent sequential fallback`을 표시하고 다음 순서로 실행합니다.

```text
목적지/날짜 -> 항공 -> 숙소 -> 장소 -> 교통 -> 일정 합성
```

- 사용자 예약으로 확정된 영역은 조사 단계를 건너뛰고 검증 입력으로 사용합니다.
- 사용자가 요청하지 않은 부분 영역은 건너뜁니다.
- 교통은 숙소·장소 후보가 선택된 뒤 실행합니다.
- 일정 합성은 필요한 조사 결과와 확정 예약이 준비된 뒤 실행합니다.
- 순차 대체는 품질 저하 모드가 아니라 실행 방식의 차이입니다. 같은 `DomainResult`와 완료 게이트를 사용합니다.

## DomainResult

각 조사 worker는 다음 필드의 의미를 보존합니다.

```yaml
domain: flight | lodging | destination | place | transport
status: ready | partial | blocked | skipped
freshness: current | stale
input_revision: 1
as_of: 2026-09-17T10:00:00+09:00
facts: []
candidates: []
recommendation: null
assumptions: []
conflicts: []
unresolved_questions: []
evidence:
  - source_type: official | primary | booking | map | review | historical | user
    source: "URL 또는 사용자 제공 정보"
    retrieved_at: 2026-09-17T10:00:00+09:00
    confidence: high | medium | low
costs:
  - amount: 0
    currency: KRW
    basis: per_person | per_room | per_group | per_ride | per_night | total
    tax_included: true | false | unknown
    status: confirmed | estimated | variable | optional
```

## 선택·예약 상태

상태는 다음 방향으로만 진행합니다.

```text
unknown -> assumed -> candidate -> selected -> booked
```

- 에이전트는 사용자 확인이나 예약 증거 없이 `selected`를 `booked`로 바꾸지 않습니다.
- 검색 결과가 있다는 사실만으로 `candidate`를 `selected`로 바꾸지 않습니다.
- 사용자 명시 선택 전에는 숙소·항공·장소 추천을 `candidate`로 유지하고, 에이전트의 1순위 추천을 자동 확정하지 않습니다.
- 사용자가 후보를 고르면 `selected`, 예약번호·바우처·결제 완료 같은 예약 증거를 제공하면 `booked`로 바꿉니다.
- 입력 변경으로 더 이상 유효하지 않은 결과는 선택·예약 `status`를 바꾸지 않고 `freshness: stale`을 붙여 재검증합니다.
- 사용자가 제공한 확정 예약과 조사 추천이 충돌하면 예약을 유지하고 `conflicts`와 일정 영향을 제시합니다.

## 반복 대화와 의사결정 장부

계획은 한 번에 끝나는 산출물이 아니라 같은 대화에서 후보를 비교하고 선택을 반영하는 반복 작업입니다. 오케스트레이터는 다음 의사결정 장부를 유지합니다.

```yaml
decision_ledger:
  - revision: 2
    domain: lodging
    item: "숙소 권역"
    from: candidate
    to: selected
    user_choice: "아속"
    affected_domains: [lodging, local_transport, place, itinerary, costs]
```

- 사용자 명시 선택 또는 조건 변경마다 `context_revision`을 올립니다.
- 변경된 입력에 직접 의존하는 영향받는 하위 결과만 `freshness: stale`로 표시합니다.
- 독립적이고 여전히 유효한 날씨·입국·일반 현지 정보는 다시 조사하지 않습니다.
- 전체를 처음부터 다시 만들지 않고 변경 요약, 무효화된 후보, 갱신 결과, 다음 선택 질문 순으로 보여줍니다.
- worker는 의사결정 장부를 직접 수정하지 않고 후보와 영향 정보만 반환합니다.

## 결과 통합

1. 현재 revision과 일치하지 않는 결과를 제외합니다.
2. 각 도메인의 `facts`, `assumptions`, `conflicts`, `unresolved_questions`를 잃지 않고 모읍니다.
3. 비용의 통화, 1인·객실·그룹 기준, 세금 포함 상태를 정규화합니다.
4. 항공·숙소·장소의 `booked`와 `selected`를 고정점으로 둡니다.
5. `travel-transport-search`로 실제 구간을 검증합니다.
6. `travel-itinerary-builder`로 일정, 비용 장부, 플랜 B와 완료 게이트를 처리합니다.
7. 도메인 커버리지에서 `partial`·`blocked`가 남았거나 필수 도메인 행 자체가 없으면 `complete`로 종료하지 않습니다.

필수 도메인이 `partial` 또는 `blocked`면 전체 계획도 같은 제약을 표시합니다. 확인된 일정은 제공할 수 있지만 완성됐다고 표현하지 않습니다.

## 실행 기록

최종 결과 또는 내부 작업 요약에 다음을 남깁니다.

- 사용한 `context_revision`
- 요청된 capability와 실제 실행·건너뜀 목록
- `parallel subagents` 또는 `single-agent sequential fallback`
- 실제 서브 에이전트 도구 호출 증거가 있을 때만 역할별 실행 요약
- 도메인별 `status: ready | partial | blocked | skipped`와 `freshness: current | stale`
- 기준 시각과 미해결 질문
