# Travel Planner Service

`travel-planner` 스킬의 날짜 후보 산정, 과거 날씨 비교, 실제 항공/숙소 검색 결과 수집을 API 서버로 제공하는 도구입니다. CLI도 유지하지만 Docker의 기본 실행 방식은 FastAPI 서버입니다.

## Docker 서버 실행

```bash
cd .agentic_base/skills/travel-planner/tools/travel-planner-cli
docker compose up -d --build
curl -s "http://127.0.0.1:8765/health"
```

프론트 페이지:

```text
http://127.0.0.1:8765/
```

Swagger 문서는 아래에서 확인합니다.

```text
http://127.0.0.1:8765/docs
```

## API

### 단계형 플래너 판단

현재 입력된 나라, 시기, 지역, 날짜, 항공/숙소 확정 여부를 보고 다음 여행 설계 단계를 반환합니다. 이 API는 저장, Playwright 수집, 외부 조회를 하지 않는 순수 판단 API입니다.

```bash
curl -s -X POST "http://127.0.0.1:8765/planner/steps" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "일본",
    "region": "후쿠오카",
    "period": "9월",
    "nights": 3,
    "departure_date": "2026-09-04",
    "return_date": "2026-09-07",
    "airline_priority": "full_service",
    "flight_style": "direct",
    "flight_confirmed": false,
    "lodging_confirmed": false,
    "travel_purpose": ["식도락", "쇼핑"],
    "evidence": {
      "date_candidates": 3,
      "weather_status": "done",
      "flight_items": 2,
      "lodging_items": 0
    }
  }'
```

`/plan/step` 별칭도 같은 응답을 반환합니다.

### 통합 탐색

날짜 후보를 만들고, 후보별 과거 날씨를 병렬로 비교하며, 선택하면 항공권 스냅샷까지 함께 수집합니다.

```bash
curl -s -X POST "http://127.0.0.1:8765/research/run" \
  -H "Content-Type: application/json" \
  -d '{
    "period": "9월",
    "nights": 3,
    "destination": "후쿠오카",
    "weekend": "prefer",
    "max_candidates": 3,
    "weather": true,
    "lat": 33.5902,
    "lon": 130.4017,
    "include_flights": true,
    "flight_url": "https://example.com/search?from=ICN&to=FUK&depart={depart_date}&return={return_date}",
    "flight_card_selector": ".result-card",
    "airline_priority": "full_service",
    "save": true
  }'
```

`airline_priority`는 `balanced`, `full_service`, `lcc`, `price`, `schedule`을 지원합니다.

### 날짜 후보 추천

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

호환용 GET 엔드포인트도 유지합니다.

```bash
curl -s "http://127.0.0.1:8765/dates?period=9월&nights=3&destination=후쿠오카&weekend=prefer&max=3"
```

### 과거 날씨 비교

```bash
curl -s -X POST "http://127.0.0.1:8765/weather/history" \
  -H "Content-Type: application/json" \
  -d '{
    "departure_date": "2026-09-04",
    "nights": 3,
    "lat": 33.5902,
    "lon": 130.4017,
    "years_back": 5
  }'
```

### 실제 항공/숙소 검색 스냅샷 수집

사이트별 검색 URL 또는 URL 템플릿을 넣으면 Playwright가 렌더링된 페이지를 열고, 결과 카드 또는 본문에서 가격/시간 후보를 추출해 JSON으로 저장합니다. 프론트의 기본 URL은 기능 검증용 `data:text/html` 샘플이며, 네이버 항공권 같은 실제 사이트는 사이트별 브라우저 조작 어댑터를 별도로 붙이는 것이 안전합니다.

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

숙소도 같은 방식입니다.

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

### 수집 산출물 조회

```bash
curl -s "http://127.0.0.1:8765/artifacts"
curl -s "http://127.0.0.1:8765/artifacts/date_candidates_YYYYMMDD_HHMMSS.json"
```

## CLI 사용

서버 없이 CLI로 직접 실행할 수도 있습니다.

```bash
python3 .agentic_base/skills/travel-planner/tools/travel-planner-cli/travel_planner_cli.py dates \
  --period "9월" \
  --nights 3 \
  --destination "후쿠오카" \
  --weekend prefer \
  --output publish/travel/research/fukuoka_date_candidates.json
```

컨테이너 안에서 CLI를 실행하려면:

```bash
docker compose exec travel-planner-service python /app/travel_planner_cli.py dates --period "9월" --nights 3 --destination "후쿠오카"
```

## 주의

- 실제 사이트는 자동화 차단, 로그인, 개인화 가격, 약관 제한이 있을 수 있습니다.
- 수집 결과는 예약 확정 정보가 아니라 `실제 검색 시점의 후보 스냅샷`입니다.
- 수하물, 세금, 취소 규정, 잔여 좌석/객실은 원 사이트에서 최종 확인합니다.
- 로그인, 결제, 예약 확정, 개인정보 입력은 자동화하지 않습니다.
