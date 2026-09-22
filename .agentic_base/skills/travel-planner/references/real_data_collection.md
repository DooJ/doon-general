# 날짜 후보 산정과 실제 데이터 수집
이 문서는 사용자가 대략적인 여행 시기를 말했을 때 날짜 후보를 잡고, 해당 날짜의 항공권과 숙소 검색 결과를 실제 데이터 스냅샷으로 수집할 때 읽는다.

## 1. 날짜 후보 산정
사용자가 "9월쯤", "가을", "추석 이후", "주말 끼고", "평일에 조용하게"처럼 느슨한 시기를 말하면 바로 항공권이나 숙소를 찾기 전에 여행 날짜 후보를 먼저 만든다.

날짜 후보에는 아래 항목을 포함한다.

- 출발일과 복귀일
- 출발/복귀 요일
- n박 m일
- 주말 포함 여부
- 예상 평일 사용일
- 주말 압축형, 주말 브릿지형, 평일 중심 같은 패턴
- 사용자가 다시 결정해야 할 확인 질문

질문은 아래처럼 구체적인 선택 기준으로 묻는다.

```markdown
이 후보는 2026-09-18(금) 출발, 2026-09-21(월) 복귀의 주말 브릿지형이고 예상 평일 사용은 2일입니다.
주말을 끼는 이 방향으로 확정할까요, 아니면 평일 중심의 한산한 일정으로 다시 좁힐까요?
```

## 2. 과거 날씨 비교
목적지 좌표를 알 수 있으면 날짜 후보마다 과거 동일 월/일 구간의 날씨를 비교한다.

- 기본 비교 범위는 최근 5년이다.
- 평균기온, 최저/최고기온 경향, 여행 기간 평균 강수량, 비가 온 일수를 본다.
- 폭염, 장마, 태풍, 한파, 강풍처럼 여행 경험에 큰 영향을 주는 리스크를 별도로 표시한다.
- 과거 날씨는 확률적 참고자료로만 쓰고, 출발 임박 단계에서는 최신 예보로 다시 갱신한다.
- 과거 날씨 데이터 조회가 실패하면 실패를 숨기지 말고 `조회 실패` 또는 `좌표 미입력`으로 표시한다.

## 3. 서버 API 사용
날짜 후보 산정과 실제 데이터 수집은 FastAPI 서버를 우선 사용한다.

```bash
cd .agentic_base/skills/travel-planner/tools/travel-planner-cli
docker compose up -d --build
curl -s "http://127.0.0.1:8765/health"
```

날짜 후보 추천:

```bash
curl -s -X POST "http://127.0.0.1:8765/dates/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "period": "9월",
    "nights": 3,
    "destination": "후쿠오카",
    "weekend": "prefer",
    "max_candidates": 3,
    "save": true
  }'
```

과거 날씨 비교:

```bash
curl -s -X POST "http://127.0.0.1:8765/weather/history" \
  -H "Content-Type: application/json" \
  -d '{
    "departure_date": "2026-09-04",
    "nights": 3,
    "lat": 33.5902,
    "lon": 130.4017
  }'
```

서버 없이 단독 실행할 때만 CLI를 사용한다.

```bash
python3 .agentic_base/skills/travel-planner/tools/travel-planner-cli/travel_planner_cli.py dates \
  --period "9월" \
  --nights 3 \
  --destination "후쿠오카" \
  --weekend prefer \
  --output publish/travel/research/fukuoka_date_candidates.json
```

과거 날씨 비교가 필요하면 좌표와 `--weather`를 추가한다.

```bash
python3 .agentic_base/skills/travel-planner/tools/travel-planner-cli/travel_planner_cli.py dates \
  --period "2026-09" \
  --nights 3 \
  --destination "후쿠오카" \
  --weekend prefer \
  --weather \
  --lat 33.5902 \
  --lon 130.4017
```

지원하는 `--weekend` 값은 아래와 같다.

| 값 | 의미 |
|---|---|
| `prefer` | 주말을 끼워 연차 부담을 줄이는 후보를 우선한다 |
| `require` | 주말이 반드시 포함된 후보만 강하게 선호한다 |
| `avoid` | 평일 중심의 한산한 후보를 우선한다 |
| `either` | 주말/평일 균형형으로 본다 |

## 4. 실제 항공권 수집
날짜 후보가 정해지면 출발일과 복귀일을 검색 URL에 넣어 실제 검색 결과를 수집한다.

서버 API:

```bash
curl -s -X POST "http://127.0.0.1:8765/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "kind": "flight",
    "url": "https://example.com/search?from=ICN&to=FUK&depart={depart_date}&return={return_date}",
    "origin": "ICN",
    "destination": "FUK",
    "depart_date": "2026-09-04",
    "return_date": "2026-09-07",
    "card_selector": ".result-card",
    "save": true
  }'
```

CLI:

```bash
python3 .agentic_base/skills/travel-planner/tools/travel-planner-cli/travel_planner_cli.py collect \
  --kind flight \
  --candidate-file publish/travel/research/fukuoka_date_candidates.json \
  --candidate-rank 1 \
  --url "https://example.com/search?from=ICN&to=FUK&depart={depart_date}&return={return_date}" \
  --card-selector ".result-card" \
  --output publish/travel/research/fukuoka_flights.json
```

항공권 후보는 아래 기준으로 정리한다.

- 출발 공항과 도착 공항
- 출발/도착 시간
- 총액과 세금 포함 여부
- 위탁수하물 포함 여부
- 직항/환승
- 첫날 활용 가능 시간
- 마지막 날 공항 도착 버퍼
- 취소/변경 조건 확인 필요 여부

## 5. 실제 숙소 수집
숙소도 같은 날짜를 체크인/체크아웃으로 넣어 수집한다.

서버 API:

```bash
curl -s -X POST "http://127.0.0.1:8765/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "kind": "lodging",
    "url": "https://example.com/hotels?destination={destination}&checkin={depart_date}&checkout={return_date}",
    "destination": "Fukuoka",
    "depart_date": "2026-09-04",
    "return_date": "2026-09-07",
    "card_selector": ".property-card",
    "save": true
  }'
```

CLI:

```bash
python3 .agentic_base/skills/travel-planner/tools/travel-planner-cli/travel_planner_cli.py collect \
  --kind lodging \
  --candidate-file publish/travel/research/fukuoka_date_candidates.json \
  --candidate-rank 1 \
  --url "https://example.com/hotels?destination={destination}&checkin={depart_date}&checkout={return_date}" \
  --destination "Fukuoka" \
  --card-selector ".property-card" \
  --output publish/travel/research/fukuoka_lodging.json
```

숙소 후보는 아래 기준으로 정리한다.

- 숙소명과 권역
- 1박 가격과 총액
- 세금/봉사료 포함 여부
- 무료 취소 가능 여부
- 체크인/체크아웃 시간
- 짐 보관 가능성
- 주요 일정 권역과의 이동 시간
- 후기 수와 최근 후기 경향

## 6. Playwright 수집 원칙
- 특정 사이트의 약관, 자동화 차단, 로그인, 지역/계정별 개인화 가격을 존중한다.
- 수집 결과는 예약 확정 정보가 아니라 `실제 검색 시점의 후보 스냅샷`으로 표시한다.
- 가격, 잔여 좌석, 객실, 수하물, 세금, 취소 조건은 원 사이트에서 최종 확인한다.
- 사이트별 selector가 안정적이지 않으면 본문 스냅샷을 저장하고 수동 확인 대상으로 둔다.
- 로그인, 결제, 예약 확정, 개인정보 입력은 자동화하지 않는다.
- 예약번호, 여권번호, 연락처, 결제정보 같은 민감정보는 저장하지 않는다.

## 7. 출력 반영 기준
예약 전 기획안이나 예상 일정에는 수집 결과를 아래처럼 분리한다.

| 구분 | 표시 방식 |
|---|---|
| 실제 검색 후보 | 검색 시각, 사이트, 가격/시간, 주요 조건을 표시 |
| 확인 필요 | 수하물, 세금, 취소 조건, 좌석/객실 잔여 여부 |
| 확정 정보 | 사용자가 실제 예약했다고 알려준 뒤에만 확정으로 승격 |
| 변동 가능 | 가격, 환율, 잔여 좌석/객실, 프로모션 조건 |

실제 데이터가 있으면 "오전 출발 후보" 같은 추상 표현 대신 항공편/숙소 후보별 시간과 가격을 우선 표시한다. 다만 검색 결과 스냅샷만으로 예약 확정을 단정하지 않는다.
