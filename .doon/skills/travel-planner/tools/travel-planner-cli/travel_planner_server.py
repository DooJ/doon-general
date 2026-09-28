from __future__ import annotations

import argparse
import asyncio
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from travel_planner_cli import (
    DEFAULT_OUTPUT_DIR,
    candidate_to_dict,
    collect_with_playwright,
    parse_iso_date,
    parse_period,
    recommend_dates,
    save_json_payload,
    summarize_historical_weather,
)


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
FULL_SERVICE_AIRLINES = [
    "대한항공",
    "korean air",
    "아시아나",
    "asiana",
    "ana",
    "all nippon",
    "jal",
    "japan airlines",
]
LCC_AIRLINES = [
    "제주항공",
    "jeju air",
    "진에어",
    "jin air",
    "티웨이",
    "tway",
    "t'way",
    "에어부산",
    "air busan",
    "에어서울",
    "air seoul",
    "peach",
    "피치",
    "zipair",
]

app = FastAPI(
    title="Travel Planner Service",
    version="0.1.0",
    description="날짜 후보 산정, 과거 날씨 비교, Playwright 기반 항공/숙소 검색 스냅샷 수집 서버",
)
FRONTEND_INDEX = Path("/app/frontend/index.html")


class DateRecommendRequest(BaseModel):
    period: str = Field(..., description="YYYY-MM, YYYY-MM-DD..YYYY-MM-DD, 9월, 가을, 다음달")
    nights: int = Field(3, ge=0)
    destination: str = ""
    weekend: Literal["prefer", "require", "avoid", "either"] = "prefer"
    max_candidates: int = Field(5, ge=1, le=31)
    weather: bool = False
    lat: Optional[float] = None
    lon: Optional[float] = None
    years_back: int = Field(5, ge=1, le=30)
    weather_timeout: int = Field(20, ge=1, le=120)
    save: bool = False
    output: Optional[str] = None


class WeatherHistoryRequest(BaseModel):
    departure_date: str = Field(..., description="YYYY-MM-DD")
    nights: int = Field(3, ge=0)
    lat: float
    lon: float
    years_back: int = Field(5, ge=1, le=30)
    timeout: int = Field(20, ge=1, le=120)


class CollectRequest(BaseModel):
    kind: Literal["flight", "lodging"]
    url: str
    adapter: str = "generic"
    origin: str = ""
    destination: str = ""
    depart_date: str = ""
    return_date: str = ""
    adults: int = Field(1, ge=1)
    rooms: int = Field(1, ge=1)
    card_selector: Optional[str] = None
    wait_selector: Optional[str] = None
    max_items: int = Field(20, ge=1, le=200)
    wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] = "networkidle"
    settle_ms: int = Field(2000, ge=0, le=30000)
    timeout_ms: int = Field(45000, ge=1000, le=180000)
    width: int = Field(1440, ge=320, le=3840)
    height: int = Field(1200, ge=320, le=4000)
    headed: bool = False
    screenshot: Optional[str] = None
    output: Optional[str] = None
    save: bool = True
    user_agent: str = DEFAULT_USER_AGENT
    airline_priority: Literal["balanced", "full_service", "lcc", "price", "schedule"] = "balanced"


class ResearchRunRequest(BaseModel):
    period: str = Field(..., description="YYYY-MM, YYYY-MM-DD..YYYY-MM-DD, 9월, 가을, 다음달")
    nights: int = Field(3, ge=0)
    destination: str = ""
    weekend: Literal["prefer", "require", "avoid", "either"] = "prefer"
    max_candidates: int = Field(5, ge=1, le=31)
    weather: bool = True
    lat: Optional[float] = None
    lon: Optional[float] = None
    years_back: int = Field(5, ge=1, le=30)
    weather_timeout: int = Field(20, ge=1, le=120)
    include_flights: bool = False
    flight_url: Optional[str] = None
    flight_card_selector: Optional[str] = None
    flight_wait_selector: Optional[str] = None
    flight_candidates: int = Field(1, ge=1, le=3)
    airline_priority: Literal["balanced", "full_service", "lcc", "price", "schedule"] = "balanced"
    save: bool = True
    output: Optional[str] = None


class PlannerStepRequest(BaseModel):
    country: str = ""
    region: str = ""
    destination: str = ""
    period: str = ""
    nights: int = Field(3, ge=0)
    weekend: Literal["prefer", "require", "avoid", "either"] = "prefer"
    departure_date: str = ""
    return_date: str = ""
    travel_purpose: List[str] = Field(default_factory=list)
    airline_priority: Literal["balanced", "full_service", "lcc", "price", "schedule"] = "balanced"
    flight_style: Literal["direct", "transit_ok", "either"] = "either"
    flight_confirmed: bool = False
    lodging_confirmed: bool = False
    lodging_area: str = ""
    evidence: Dict[str, Any] = Field(default_factory=dict)


def date_candidates_payload(request: DateRecommendRequest) -> Dict[str, Any]:
    period = parse_period(request.period)
    candidates = recommend_dates(
        period=period,
        nights=request.nights,
        weekend_mode=request.weekend,
        max_candidates=request.max_candidates,
        destination=request.destination,
        latitude=request.lat,
        longitude=request.lon,
        include_weather=request.weather,
        years_back=request.years_back,
        weather_timeout=request.weather_timeout,
    )
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "period": {
            "label": period.label,
            "start": period.start.isoformat(),
            "end": period.end.isoformat(),
        },
        "destination": request.destination,
        "nights": request.nights,
        "weekend_mode": request.weekend,
        "candidates": [candidate_to_dict(candidate, period) for candidate in candidates],
    }


def output_name(prefix: str) -> str:
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"


def namespace_from_collect_request(request: CollectRequest) -> argparse.Namespace:
    return argparse.Namespace(
        kind=request.kind,
        url=request.url,
        adapter=request.adapter,
        origin=request.origin,
        destination=request.destination,
        depart_date=request.depart_date,
        return_date=request.return_date,
        adults=request.adults,
        rooms=request.rooms,
        candidate_file=None,
        candidate_rank=1,
        card_selector=request.card_selector,
        wait_selector=request.wait_selector,
        max_items=request.max_items,
        wait_until=request.wait_until,
        settle_ms=request.settle_ms,
        timeout_ms=request.timeout_ms,
        width=request.width,
        height=request.height,
        headed=request.headed,
        screenshot=request.screenshot,
        output=request.output,
        user_agent=request.user_agent,
    )


def price_number(value: str) -> Optional[int]:
    digits = re.sub(r"\D", "", value)
    return int(digits) if digits else None


def first_price(item: Dict[str, Any]) -> Optional[int]:
    for value in item.get("prices") or []:
        number = price_number(str(value))
        if number is not None:
            return number
    return None


def first_departure_minutes(item: Dict[str, Any]) -> Optional[int]:
    times = item.get("times") or []
    if not times:
        return None
    try:
        hour, minute = str(times[0]).split(":", 1)
        return int(hour) * 60 + int(minute)
    except (TypeError, ValueError):
        return None


def airline_family(text: str) -> str:
    normalized = text.lower()
    if any(name in normalized for name in FULL_SERVICE_AIRLINES):
        return "full_service"
    if any(name in normalized for name in LCC_AIRLINES):
        return "lcc"
    return "unknown"


def airline_priority_score(item: Dict[str, Any], priority: str) -> float:
    family = item.get("airline_family") or "unknown"
    price = first_price(item)
    minutes = first_departure_minutes(item)
    if priority == "full_service":
        return {"full_service": 0, "unknown": 1, "lcc": 2}.get(family, 3)
    if priority == "lcc":
        return {"lcc": 0, "unknown": 1, "full_service": 2}.get(family, 3)
    if priority == "price":
        return float(price if price is not None else 999_999_999)
    if priority == "schedule":
        return float(minutes if minutes is not None else 9_999)
    family_score = {"full_service": 0, "lcc": 1, "unknown": 2}.get(family, 3)
    price_score = min((price or 999_999_999) / 100_000, 20)
    return family_score + price_score


def enrich_flight_items(payload: Dict[str, Any], airline_priority: str) -> Dict[str, Any]:
    if payload.get("kind") != "flight":
        return payload
    for item in payload.get("items") or []:
        text = str(item.get("text") or "")
        item["airline_family"] = airline_family(text)
        item["priority_score"] = airline_priority_score(item, airline_priority)
    payload["items"] = sorted(payload.get("items") or [], key=lambda item: item.get("priority_score", 9999))
    payload["airline_priority"] = airline_priority
    payload["airline_priority_note"] = {
        "balanced": "대형항공사 안정성과 가격을 함께 봅니다.",
        "full_service": "대한항공, 아시아나, ANA, JAL 같은 대형항공사를 우선합니다.",
        "lcc": "제주항공, 진에어, 티웨이, 에어부산, 에어서울 같은 LCC를 우선합니다.",
        "price": "가격이 낮은 후보를 우선합니다.",
        "schedule": "이른 출발 시간 순으로 우선합니다.",
    }.get(airline_priority, "")
    return payload


def compact(value: str) -> str:
    return str(value or "").strip()


def has_text(value: str) -> bool:
    return bool(compact(value))


def region_value(request: PlannerStepRequest) -> str:
    return compact(request.region) or compact(request.destination)


def evidence_count(request: PlannerStepRequest, key: str) -> int:
    value = request.evidence.get(key, 0)
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def seasonal_region_recommendations(period: str = "") -> List[Dict[str, str]]:
    label = compact(period) or "시기 미정"
    return [
        {
            "title": "일본 후쿠오카",
            "why": f"{label}에도 2-4일 짧은 일정과 식도락 여행으로 좁히기 쉽습니다.",
            "next": "일본을 선택하면 9-11월, 3-5월, 1-2월 중 적정 시기를 비교합니다.",
        },
        {
            "title": "대만 타이베이",
            "why": "도심 이동이 쉽고 가족/친구/커플 여행 모두 식당과 쇼핑 동선이 안정적입니다.",
            "next": "시기 선택 후 우천 대체 동선과 야시장/근교 범위를 정합니다.",
        },
        {
            "title": "베트남 다낭",
            "why": "휴식형 리조트와 관광형 일정이 모두 가능해 여행 목적에 맞춰 분기하기 좋습니다.",
            "next": "건기/우기와 숙소 권역을 먼저 좁힙니다.",
        },
        {
            "title": "태국 방콕",
            "why": "쇼핑, 식도락, 마사지, 야시장 중심으로 목적 기반 계획을 만들기 쉽습니다.",
            "next": "더위와 우천 리스크를 보고 실내/야간 중심 여부를 정합니다.",
        },
        {
            "title": "대한민국 제주",
            "why": "항공편 선택지가 많고 렌터카/택시/대중교통 중 여행 강도를 조절하기 쉽습니다.",
            "next": "동쪽/서쪽/서귀포 권역과 렌터카 여부를 정합니다.",
        },
    ]


def timing_recommendations(country: str) -> List[Dict[str, str]]:
    normalized = compact(country).lower()
    if "일본" in country or "japan" in normalized:
        return [
            {"title": "9-11월", "why": "더위가 줄고 도시 여행, 식도락, 근교 이동 균형이 좋습니다.", "next": "후쿠오카, 오사카/교토, 홋카이도를 비교합니다."},
            {"title": "3-5월", "why": "벚꽃과 봄 날씨가 강점이지만 항공/숙소 가격이 빨리 오를 수 있습니다.", "next": "벚꽃 목적이면 예약 난이도를 먼저 봅니다."},
            {"title": "1-2월", "why": "온천, 눈, 겨울 먹거리 목적에 좋고 남부 도시는 짧은 일정이 가능합니다.", "next": "삿포로/후쿠오카/유후인 축을 비교합니다."},
        ]
    if "대만" in country or "taiwan" in normalized:
        return [
            {"title": "10-12월", "why": "덥고 습한 시기를 지나 도심 관광과 야시장 동선이 편합니다.", "next": "타이베이와 타이중/가오슝을 비교합니다."},
            {"title": "3-4월", "why": "짧은 봄 여행에 적합하나 비 예보를 같이 봐야 합니다.", "next": "실내 대체안을 같이 둡니다."},
            {"title": "1-2월", "why": "겨울 도피 여행으로 좋지만 명절 기간 혼잡을 피해야 합니다.", "next": "항공/숙소 성수기 여부를 먼저 확인합니다."},
        ]
    return [
        {"title": "봄", "why": "도시 관광과 자연 일정의 균형을 잡기 쉽습니다.", "next": "비용과 성수기 여부를 비교합니다."},
        {"title": "가을", "why": "날씨 안정성과 걷기 좋은 동선이 강점입니다.", "next": "주말 포함 날짜 후보를 만듭니다."},
        {"title": "겨울", "why": "온천, 휴식, 실내 콘텐츠 중심으로 목적이 선명해집니다.", "next": "날씨 리스크와 항공 가격을 확인합니다."},
    ]


def region_recommendations(country: str, period: str) -> List[Dict[str, str]]:
    normalized = compact(country).lower()
    period_label = compact(period) or "선택 시기"
    if "일본" in country or "japan" in normalized:
        return [
            {"title": "후쿠오카", "why": f"{period_label} 짧은 일정, 식도락, 쇼핑, 근교 온천을 섞기 좋습니다.", "next": "3박 기준 금-월/목-일 후보를 봅니다."},
            {"title": "오사카/교토", "why": "관광과 식도락 밀도가 높고 첫 일본 여행에도 선택지가 많습니다.", "next": "도시 이동량과 숙소 권역을 먼저 정합니다."},
            {"title": "홋카이도", "why": "계절감이 뚜렷하고 자연/먹거리 목적이 강할 때 만족도가 높습니다.", "next": "렌터카/철도 여부와 항공 시간을 같이 봅니다."},
        ]
    if "대만" in country or "taiwan" in normalized:
        return [
            {"title": "타이베이", "why": "도심, 야시장, 근교를 3-4일 안에 안정적으로 묶을 수 있습니다.", "next": "비 예보와 실내 대체 동선을 같이 봅니다."},
            {"title": "타이중", "why": "카페, 감성 숙소, 근교 자연을 섞기 좋습니다.", "next": "고속철/전용차 필요 여부를 확인합니다."},
            {"title": "가오슝", "why": "남부의 느슨한 분위기와 항구/야시장 중심 일정에 맞습니다.", "next": "더위와 이동수단을 먼저 확인합니다."},
        ]
    return [
        {"title": "대표 수도권 도시", "why": "항공과 숙소 선택지가 많아 첫 계획을 잡기 쉽습니다.", "next": "도심 숙소 권역과 여행 목적을 정합니다."},
        {"title": "휴양 권역", "why": "휴식, 리조트, 가족 여행에 적합합니다.", "next": "숙소 등급과 이동수단을 먼저 정합니다."},
        {"title": "근교 포함 권역", "why": "관광과 자연을 함께 넣을 수 있습니다.", "next": "하루 이동 강도와 교통편을 확인합니다."},
    ]


def flight_recommendations(priority: str, flight_style: str) -> List[Dict[str, str]]:
    style_note = {
        "direct": "직항 중심으로 피로도와 첫날 활용 시간을 우선합니다.",
        "transit_ok": "경유 허용으로 가격을 낮추되 환승 대기와 지연 리스크를 확인합니다.",
        "either": "직항/경유를 모두 열고 가격, 시간, 피로도를 비교합니다.",
    }.get(flight_style, "")
    priority_note = {
        "full_service": "대형항공사 우선: 수하물, 지연 대응, 가족/부모님 동행 안정성을 봅니다.",
        "lcc": "LCC 우선: 총액, 위탁수하물, 공항 접근 시간을 반드시 같이 봅니다.",
        "price": "가격 우선: 최저가가 실제 총액인지 세금/수하물 포함 여부를 확인합니다.",
        "schedule": "시간 우선: 이른 출발과 늦은 복귀로 체류 시간을 늘립니다.",
        "balanced": "균형: 시간, 가격, 수하물, 피로도를 함께 봅니다.",
    }.get(priority, "")
    return [
        {"title": "대형항공사 후보", "why": priority_note or "운항 안정성과 포함 조건을 비교합니다.", "next": style_note},
        {"title": "LCC 후보", "why": "가격 경쟁력이 있지만 수하물/좌석/시간대 조건 확인이 필요합니다.", "next": "총액 기준으로 비교합니다."},
        {"title": "경유/대체 공항 후보", "why": "직항 가격이 높거나 시간대가 나쁠 때 대안이 됩니다.", "next": "환승 시간과 첫날 피로도를 확인합니다."},
    ]


def lodging_recommendations(region: str) -> List[Dict[str, str]]:
    where = compact(region) or "선택 지역"
    return [
        {"title": "가성비 중심", "why": f"{where}의 주요 역/정류장 접근성과 1박 단가를 우선합니다.", "next": "짐 보관과 체크인 시간을 확인합니다."},
        {"title": "테마 중심", "why": "온천, 뷰, 가족 객실, 감성 숙소처럼 여행 목적에 맞춥니다.", "next": "가격보다 경험 우선순위를 확인합니다."},
        {"title": "동선 중심", "why": "Day별 출발/복귀와 식당/쇼핑 접근성을 우선합니다.", "next": "숙소 확정 후 관광 순서를 재배치합니다."},
    ]


def downstream_recommendations(region: str, purposes: List[str]) -> Dict[str, List[Dict[str, str]]]:
    purpose_text = ", ".join([compact(item) for item in purposes if compact(item)]) or "관광/식도락/휴식"
    where = compact(region) or "선택 지역"
    return {
        "attractions": [
            {"title": "오전 핵심 관광지", "why": f"{where}에서 대기와 혼잡이 적은 시간대를 우선합니다.", "next": "방문 소요와 이동 방향을 일정에 넣습니다."},
            {"title": "오후 실내/쇼핑 권역", "why": f"{purpose_text} 목적에 맞춰 날씨 영향을 줄입니다.", "next": "카페/쇼핑과 이어지는 동선으로 배치합니다."},
            {"title": "저녁 산책/야경 권역", "why": "식사 뒤 무리 없는 이동으로 하루를 닫습니다.", "next": "숙소 복귀 교통을 확인합니다."},
        ],
        "restaurants": [
            {"title": "동선상 점심 후보", "why": "오전 관광 종료 위치와 가까운 곳을 우선합니다.", "next": "예약/대기 가능성을 확인합니다."},
            {"title": "저녁 대표 메뉴 후보", "why": "지역 대표 음식과 이동 피로도를 함께 봅니다.", "next": "마감 시간과 숙소 복귀를 확인합니다."},
            {"title": "카페/간식 후보", "why": "비거나 지치는 시간대의 완충 지점으로 둡니다.", "next": "비 오는 날 대체안으로도 둡니다."},
        ],
        "shopping": [
            {"title": "지역 특산품", "why": "선물/기념품으로 실패 확률이 낮은 항목을 우선합니다.", "next": "귀국 전 짐 증가를 고려해 구매일을 정합니다."},
            {"title": "필수 구매템", "why": "마트/드럭스토어/로컬 브랜드를 목적별로 나눕니다.", "next": "면세/택스프리 조건을 확인합니다."},
            {"title": "선택 쇼핑", "why": "예산과 캐리어 여유가 있을 때만 넣습니다.", "next": "비용 장부의 선택 경비로 분리합니다."},
        ],
    }


def build_step(
    key: str,
    title: str,
    status: str,
    summary: str,
    recommendations: Optional[List[Dict[str, str]]] = None,
    next_action: Optional[Dict[str, str]] = None,
    impact_checks: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "key": key,
        "title": title,
        "status": status,
        "summary": summary,
        "recommendations": recommendations or [],
        "next_action": next_action,
        "impact_checks": impact_checks or [],
    }


def planner_steps_payload(request: PlannerStepRequest) -> Dict[str, Any]:
    country = compact(request.country)
    region = region_value(request)
    period = compact(request.period)
    date_selected = has_text(request.departure_date) and has_text(request.return_date)
    date_candidates = evidence_count(request, "date_candidates")
    flight_items = evidence_count(request, "flight_items")
    lodging_items = evidence_count(request, "lodging_items")
    has_purpose = any(compact(item) for item in request.travel_purpose)
    has_flight_anchor = request.flight_confirmed or flight_items > 0
    has_lodging_anchor = request.lodging_confirmed or lodging_items > 0 or has_text(request.lodging_area)

    steps: List[Dict[str, Any]] = []
    impact_checks: List[str] = []
    flight_impact_checks: List[str] = []
    lodging_impact_checks: List[str] = []
    questions: List[str] = []
    missing_fields: List[str] = []
    next_action: Dict[str, str] = {
        "kind": "review_plan",
        "label": "현재 입력으로 다음 결정 확인",
        "endpoint": "/planner/steps",
        "method": "POST",
    }

    if request.flight_confirmed:
        flight_impact_checks = [
            "항공 도착시간 기준으로 첫날 체크인 전 짐 처리와 저녁 일정을 다시 봅니다.",
            "귀국편 시간 기준으로 마지막 날 체크아웃, 공항 이동, 수하물 버퍼를 다시 봅니다.",
        ]
        impact_checks.extend(flight_impact_checks)
    if request.lodging_confirmed:
        lodging_impact_checks = [
            "숙소 위치 기준으로 Day별 출발/복귀 동선과 식당 권역을 다시 봅니다.",
            "체크인/체크아웃, 짐 보관 가능 여부가 첫날과 마지막 날 일정을 바꿀 수 있습니다.",
        ]
        impact_checks.extend(lodging_impact_checks)

    country_status = "done" if country else "active"
    steps.append(
        build_step(
            "country_or_region_discovery",
            "1. 나라/지역 탐색",
            country_status,
            "나라가 정해지지 않았으면 시기별로 가기 좋은 지역 top5부터 봅니다.",
            seasonal_region_recommendations(period) if not country else [],
            {"kind": "choose_country", "label": "나라 또는 넓은 지역 선택", "endpoint": "/planner/steps", "method": "POST"} if not country else None,
        )
    )
    if not country:
        questions.append("어느 나라나 권역이 끌리나요? 없으면 위 후보 중 하나를 고르면 됩니다.")
        missing_fields.append("country")
        next_action = {"kind": "choose_country", "label": "시기별 지역 top5 중 나라/권역 선택", "endpoint": "/planner/steps", "method": "POST"}

    timing_status = "queued"
    if country and not period:
        timing_status = "active"
        questions.append("여행 시기를 먼저 정할까요, 아니면 성수기/날씨/가격 기준으로 추천받을까요?")
        missing_fields.append("period")
        next_action = {"kind": "choose_period", "label": f"{country} 여행 시기 top3 선택", "endpoint": "/planner/steps", "method": "POST"}
    elif country and period:
        timing_status = "done"
    steps.append(
        build_step(
            "timing_selection",
            "2. 시기 선택",
            timing_status,
            "나라가 정해졌으면 날씨, 가격, 혼잡도를 기준으로 시기 top3를 좁힙니다.",
            timing_recommendations(country) if country and not period else [],
            {"kind": "choose_period", "label": "시기 top3 중 선택", "endpoint": "/planner/steps", "method": "POST"} if country and not period else None,
        )
    )

    region_status = "queued"
    if country and period and not region:
        region_status = "active"
        questions.append("이 시기에 맞는 도시/권역을 먼저 고를까요?")
        missing_fields.append("region")
        next_action = {"kind": "choose_region", "label": f"{country} {period} 지역 top3 선택", "endpoint": "/planner/steps", "method": "POST"}
    elif country and region:
        region_status = "done"
    steps.append(
        build_step(
            "region_selection",
            "3. 지역/도시 선택",
            region_status,
            "나라와 시기가 정해졌으면 실제 이동 가능한 지역 top3를 고릅니다.",
            region_recommendations(country, period) if country and period and not region else [],
            {"kind": "choose_region", "label": "지역 top3 중 선택", "endpoint": "/planner/steps", "method": "POST"} if country and period and not region else None,
        )
    )

    date_status = "queued"
    if country and region and period and not date_selected:
        date_status = "active" if date_candidates == 0 else "ready"
        questions.append("지역과 시기가 정해졌으니 주말 포함 여부를 보고 날짜 후보 top3를 만들 차례입니다.")
        next_action = {
            "kind": "run_research",
            "label": "적정 날짜 top3와 과거 날씨 비교",
            "endpoint": "/research/run",
            "method": "POST",
        }
    elif date_selected:
        date_status = "done"
    steps.append(
        build_step(
            "date_weather",
            "4. 날짜와 날씨",
            date_status,
            "지역과 시기가 정해지면 출발/복귀 날짜, 주말 포함, 과거 동일 날짜대 날씨를 함께 봅니다.",
            [
                {"title": "주말 포함 후보", "why": "연차 부담을 줄이고 이동 리듬이 자연스럽습니다.", "next": "금-월 또는 목-일 후보를 확인합니다."},
                {"title": "평일 중심 후보", "why": "항공/숙소 가격과 혼잡도를 낮출 수 있습니다.", "next": "휴가 사용일을 확인합니다."},
                {"title": "균형 후보", "why": "가격과 연차 부담을 함께 봅니다.", "next": "후보별 날씨 리스크를 비교합니다."},
            ] if country and region and period and not date_selected else [],
            {"kind": "run_research", "label": "날짜/날씨 후보 만들기", "endpoint": "/research/run", "method": "POST"} if country and region and period and not date_selected else None,
        )
    )

    flight_status = "queued"
    if country and date_selected and not has_flight_anchor:
        flight_status = "active"
        questions.append("선택 날짜로 항공 후보를 대형항공사, LCC, 가격, 시간, 경유 기준으로 비교할까요?")
        next_action = {"kind": "collect_flight", "label": "선택 날짜로 항공 검색", "endpoint": "/collect", "method": "POST"}
    elif has_flight_anchor:
        flight_status = "confirmed" if request.flight_confirmed else "ready"
    steps.append(
        build_step(
            "flight_search",
            "5. 항공/장거리 이동",
            flight_status,
            "날짜가 잡히면 실제 검색 시점의 항공 후보를 시간, 가격, 항공사, 경유 기준으로 비교합니다.",
            flight_recommendations(request.airline_priority, request.flight_style) if country and date_selected and not request.flight_confirmed else [],
            {"kind": "collect_flight", "label": "항공 후보 수집", "endpoint": "/collect", "method": "POST"} if country and date_selected and not has_flight_anchor else None,
            flight_impact_checks if request.flight_confirmed else [],
        )
    )

    purpose_status = "queued"
    if country and has_flight_anchor and not has_purpose:
        purpose_status = "active"
        questions.append("항공 시간이 잡혔으니 관광, 식도락, 쇼핑, 휴식 중 우선순위를 정해야 합니다.")
        missing_fields.append("travel_purpose")
        next_action = {"kind": "choose_purpose", "label": "상세 관광 목적과 지역 범위 선택", "endpoint": "/planner/steps", "method": "POST"}
    elif has_purpose:
        purpose_status = "done"
    steps.append(
        build_step(
            "purpose_scope",
            "6. 목적과 지역 범위",
            purpose_status,
            "항공 도착/출발 시간에 맞춰 관광 목적과 하루에 다닐 권역 범위를 정합니다.",
            [
                {"title": "식도락 중심", "why": "식사 예약과 동선을 먼저 고정합니다.", "next": "점심/저녁 후보를 권역별로 나눕니다."},
                {"title": "관광 중심", "why": "방문 시간대와 이동 버퍼가 중요합니다.", "next": "오전/오후 핵심 관광지를 나눕니다."},
                {"title": "휴식 중심", "why": "숙소 위치와 체크인 이후 시간을 중시합니다.", "next": "숙소 테마와 주변 산책권을 봅니다."},
            ] if country and has_flight_anchor and not has_purpose else [],
        )
    )

    lodging_status = "queued"
    if country and date_selected and has_flight_anchor and not has_lodging_anchor:
        lodging_status = "active"
        questions.append("항공 후보가 잡혔으니 숙소를 가성비/테마/동선 기준 top3로 좁힐 차례입니다.")
        next_action = {"kind": "collect_lodging", "label": "숙소 후보 top3 수집/정리", "endpoint": "/collect", "method": "POST"}
    elif has_lodging_anchor:
        lodging_status = "confirmed" if request.lodging_confirmed else "ready"
    steps.append(
        build_step(
            "lodging_selection",
            "7. 숙소 선택",
            lodging_status,
            "숙소는 이름보다 권역, 가격대, 테마, 체크인/짐 보관, Day별 동선 영향을 먼저 봅니다.",
            lodging_recommendations(region) if country and date_selected and has_flight_anchor and not request.lodging_confirmed else [],
            {"kind": "collect_lodging", "label": "숙소 후보 수집", "endpoint": "/collect", "method": "POST"} if country and date_selected and has_flight_anchor and not has_lodging_anchor else None,
            lodging_impact_checks if request.lodging_confirmed else [],
        )
    )

    downstream = downstream_recommendations(region, request.travel_purpose)
    route_status = "active" if country and has_lodging_anchor and has_purpose else ("queued" if country and has_lodging_anchor else "locked")
    steps.append(
        build_step(
            "attraction_route",
            "8. 관광지와 동선",
            route_status,
            "숙소가 정해지면 목적과 이동 방향에 맞춰 관광지 방문 시간대를 일정에 넣습니다.",
            downstream["attractions"] if country and has_lodging_anchor else [],
        )
    )
    steps.append(
        build_step(
            "restaurant_route",
            "9. 식당 추천",
            "queued" if route_status in {"active", "queued"} else "locked",
            "동선이 잡히면 점심, 저녁, 카페 후보를 각 위치와 시간대에 맞춰 top3로 둡니다.",
            downstream["restaurants"] if country and has_lodging_anchor else [],
        )
    )
    steps.append(
        build_step(
            "shopping_local_goods",
            "10. 특산품/구매템",
            "queued" if country and has_lodging_anchor else "locked",
            "지역 특산품과 필수 구매템은 쇼핑 예산과 캐리어 여유, 구매일을 함께 봅니다.",
            downstream["shopping"] if country and has_lodging_anchor else [],
        )
    )
    steps.append(
        build_step(
            "safety_support",
            "11. 안전/보험/병원",
            "queued" if country and region else "locked",
            "영사관, 현지 긴급전화, 병원, 보험 보장 범위는 출발 전 최신 공식 출처로 확인합니다.",
            [
                {"title": "영사/긴급 연락", "why": "여권 분실, 사고, 질병 상황의 연락 경로를 미리 둡니다.", "next": "공식 외교부/공관 페이지 기준으로 갱신합니다."},
                {"title": "병원/약국", "why": "숙소 권역 기준으로 야간/응급 대응 가능 지점을 봅니다.", "next": "보험사 제휴 병원 여부를 확인합니다."},
                {"title": "보험", "why": "지연, 수하물, 질병, 취소 보장 범위를 확인합니다.", "next": "가입 전 약관과 예외를 봅니다."},
            ] if country and region else [],
        )
    )
    steps.append(
        build_step(
            "packing_checklist",
            "12. 준비물",
            "queued" if country and date_selected else "locked",
            "필수/선택 준비물은 날씨, 항공 수하물, 결제/통신, 상비약 기준으로 나눕니다.",
            [
                {"title": "필수", "why": "여권, 결제수단, 예약 정보, 통신 수단은 출발 전 고정합니다.", "next": "문서화 단계에서 체크리스트로 변환합니다."},
                {"title": "선택", "why": "날씨, 쇼핑, 숙소 시설에 따라 필요한 물품만 추가합니다.", "next": "짐 무게와 캐리어 여유를 확인합니다."},
            ] if country and date_selected else [],
        )
    )

    active_step = next((step for step in steps if step["status"] in {"active", "ready"}), steps[-1])
    if not questions and active_step["next_action"]:
        next_action = active_step["next_action"]
    elif not questions:
        next_action = {"kind": "draft_itinerary", "label": "현재 확정 정보로 예상 일정 초안 작성", "endpoint": "/planner/steps", "method": "POST"}

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stage": active_step["key"],
        "status": active_step["status"],
        "missing_fields": missing_fields,
        "questions": questions[:3],
        "next_action": next_action,
        "enabled_actions": [
            {"kind": "plan_steps", "label": "다음 단계 판단", "endpoint": "/planner/steps", "method": "POST"},
            {"kind": "run_research", "label": "날짜/날씨/항공 통합 탐색", "endpoint": "/research/run", "method": "POST"},
            {"kind": "collect", "label": "항공/숙소 스냅샷 수집", "endpoint": "/collect", "method": "POST"},
        ],
        "impact_checks": impact_checks,
        "steps": steps,
        "summary": {
            "country": country or "미정",
            "period": period or "미정",
            "region": region or "미정",
            "date_selected": date_selected,
            "flight_status": "확정" if request.flight_confirmed else ("후보 있음" if flight_items else "미수집"),
            "lodging_status": "확정" if request.lodging_confirmed else ("후보 있음" if lodging_items else "미수집"),
        },
    }


async def weather_for_candidate(candidate: Dict[str, Any], request: ResearchRunRequest) -> Dict[str, Any]:
    if request.lat is None or request.lon is None:
        candidate["weather"] = {"status": "skipped", "note": "lat/lon not provided"}
        return candidate
    departure = parse_iso_date(str(candidate["departure_date"]))
    summary = await asyncio.to_thread(
        summarize_historical_weather,
        departure,
        request.nights,
        request.lat,
        request.lon,
        request.years_back,
        request.weather_timeout,
    )
    candidate["weather"] = summary.__dict__
    return candidate


async def collect_flight_for_candidate(candidate: Dict[str, Any], request: ResearchRunRequest) -> Dict[str, Any]:
    collect_request = CollectRequest(
        kind="flight",
        url=request.flight_url or "",
        destination=request.destination,
        depart_date=str(candidate["departure_date"]),
        return_date=str(candidate["return_date"]),
        card_selector=request.flight_card_selector,
        wait_selector=request.flight_wait_selector,
        save=False,
        airline_priority=request.airline_priority,
    )
    payload = await collect_with_playwright(namespace_from_collect_request(collect_request))
    payload = enrich_flight_items(payload, request.airline_priority)
    payload["candidate_rank"] = candidate.get("rank")
    payload["depart_date"] = candidate.get("departure_date")
    payload["return_date"] = candidate.get("return_date")
    return payload


def artifact_root() -> Path:
    path = Path.cwd() / DEFAULT_OUTPUT_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_artifact_path(name: str) -> Path:
    if "/" in name or "\\" in name or name.startswith("."):
        raise HTTPException(status_code=400, detail="artifact name must be a plain file name")
    path = artifact_root() / name
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="artifact not found")
    return path


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "service": "travel-planner-service"}


@app.get("/", include_in_schema=False)
async def frontend() -> FileResponse:
    if not FRONTEND_INDEX.exists():
        raise HTTPException(status_code=404, detail="frontend not found")
    return FileResponse(FRONTEND_INDEX)


@app.get("/dates")
async def legacy_dates(
    period: str = Query("다음달"),
    nights: int = Query(3, ge=0),
    destination: str = "",
    weekend: Literal["prefer", "require", "avoid", "either"] = "prefer",
    max: int = Query(5, ge=1, le=31),  # noqa: A002
    weather: bool = False,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> Dict[str, Any]:
    request = DateRecommendRequest(
        period=period,
        nights=nights,
        destination=destination,
        weekend=weekend,
        max_candidates=max,
        weather=weather,
        lat=lat,
        lon=lon,
    )
    try:
        return date_candidates_payload(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/dates/recommend")
async def recommend_date_endpoint(request: DateRecommendRequest) -> Dict[str, Any]:
    try:
        payload = date_candidates_payload(request)
        if request.save or request.output:
            path = save_json_payload(payload, request.output, output_name("date_candidates"))
            payload["saved_path"] = str(path)
        return payload
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/weather/history")
async def weather_history_endpoint(request: WeatherHistoryRequest) -> Dict[str, Any]:
    try:
        departure = parse_iso_date(request.departure_date)
        summary = summarize_historical_weather(
            departure=departure,
            nights=request.nights,
            latitude=request.lat,
            longitude=request.lon,
            years_back=request.years_back,
            timeout=request.timeout,
        )
        return {
            "departure_date": request.departure_date,
            "return_date": (departure + timedelta(days=request.nights)).isoformat(),
            "nights": request.nights,
            "weather": summary.__dict__,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/collect")
async def collect_endpoint(request: CollectRequest) -> Dict[str, Any]:
    try:
        payload = await collect_with_playwright(namespace_from_collect_request(request))
        payload = enrich_flight_items(payload, request.airline_priority)
        if request.save or request.output:
            path = save_json_payload(payload, request.output, output_name(request.kind))
            payload["saved_path"] = str(path)
        return payload
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/planner/steps")
async def planner_steps_endpoint(request: PlannerStepRequest) -> Dict[str, Any]:
    try:
        return planner_steps_payload(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/plan/step")
async def plan_step_alias_endpoint(request: PlannerStepRequest) -> Dict[str, Any]:
    try:
        return planner_steps_payload(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/research/run")
async def research_run_endpoint(request: ResearchRunRequest) -> Dict[str, Any]:
    try:
        date_payload = date_candidates_payload(
            DateRecommendRequest(
                period=request.period,
                nights=request.nights,
                destination=request.destination,
                weekend=request.weekend,
                max_candidates=request.max_candidates,
                weather=False,
            )
        )
        candidates = date_payload["candidates"]
        phases: List[Dict[str, Any]] = [
            {"name": "dates", "status": "done", "items": len(candidates)},
        ]

        if request.weather:
            weather_tasks = [weather_for_candidate(candidate, request) for candidate in candidates]
            candidates = await asyncio.gather(*weather_tasks)
            date_payload["candidates"] = candidates
            phases.append({"name": "weather", "status": "done", "items": len(candidates), "parallel": True})
        else:
            phases.append({"name": "weather", "status": "skipped"})

        flight_payloads: List[Dict[str, Any]] = []
        if request.include_flights:
            if not request.flight_url:
                phases.append({"name": "flights", "status": "skipped", "reason": "flight_url missing"})
            else:
                flight_targets = candidates[: request.flight_candidates]
                flight_tasks = [collect_flight_for_candidate(candidate, request) for candidate in flight_targets]
                flight_payloads = await asyncio.gather(*flight_tasks)
                phases.append(
                    {
                        "name": "flights",
                        "status": "done",
                        "items": sum(len(payload.get("items") or []) for payload in flight_payloads),
                        "candidate_windows": len(flight_payloads),
                        "parallel": True,
                        "airline_priority": request.airline_priority,
                    }
                )
        else:
            phases.append({"name": "flights", "status": "skipped"})

        payload: Dict[str, Any] = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "mode": "integrated_research",
            "phases": phases,
            "dates": date_payload,
            "flights": flight_payloads,
        }
        if request.save or request.output:
            path = save_json_payload(payload, request.output, output_name("research"))
            payload["saved_path"] = str(path)
        return payload
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/artifacts")
async def list_artifacts() -> Dict[str, List[Dict[str, Any]]]:
    root = artifact_root()
    files = []
    for path in sorted(root.glob("*.json")):
        files.append(
            {
                "name": path.name,
                "path": str(path),
                "bytes": path.stat().st_size,
                "updated_at": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            }
        )
    return {"artifacts": files}


@app.get("/artifacts/{name}")
async def get_artifact(name: str) -> Dict[str, Any]:
    path = safe_artifact_path(name)
    try:
        return {"name": path.name, "path": str(path), "data": path.read_text(encoding="utf-8")}
    except OSError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
