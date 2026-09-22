#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import calendar
import json
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_OUTPUT_DIR = Path("publish") / "travel" / "research"
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
PRICE_PATTERN = re.compile(
    r"(?:₩\s*[\d,]+|KRW\s*[\d,]+|[\d,]+\s*원|(?:USD|JPY|EUR)\s*[\d,]+)",
    re.IGNORECASE,
)
TIME_PATTERN = re.compile(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b")


@dataclass
class Period:
    label: str
    start: date
    end: date


@dataclass
class WeatherSummary:
    status: str
    years: List[int] = field(default_factory=list)
    avg_temp_c: Optional[float] = None
    min_temp_c: Optional[float] = None
    max_temp_c: Optional[float] = None
    avg_trip_precip_mm: Optional[float] = None
    avg_rainy_days: Optional[float] = None
    sample_count: int = 0
    note: str = ""


@dataclass
class DateCandidate:
    rank: int
    departure_date: str
    return_date: str
    nights: int
    days: int
    weekday_label: str
    pattern: str
    includes_weekend: bool
    weekend_days: int
    leave_days_estimate: int
    score: float
    score_reasons: List[str]
    confirmation_prompt: str
    weather: Optional[WeatherSummary] = None


@dataclass
class CollectionItem:
    index: int
    text: str
    prices: List[str]
    times: List[str]


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def month_end(year: int, month: int) -> date:
    return date(year, month, calendar.monthrange(year, month)[1])


def normalize_month_year(month: int, today: date) -> int:
    year = today.year
    if month < today.month:
        year += 1
    return year


def parse_period(value: str, today: Optional[date] = None) -> Period:
    today = today or date.today()
    raw = value.strip()
    compact = raw.replace(" ", "")

    range_match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})(?:\.\.|~|부터|에서)(\d{4}-\d{2}-\d{2})", compact)
    if range_match:
        start = parse_iso_date(range_match.group(1))
        end = parse_iso_date(range_match.group(2))
        if end < start:
            raise ValueError("period range end is before start")
        return Period(raw, start, end)

    month_match = re.fullmatch(r"(\d{4})-(\d{2})", compact)
    if month_match:
        year = int(month_match.group(1))
        month = int(month_match.group(2))
        return Period(raw, date(year, month, 1), month_end(year, month))

    date_match = re.fullmatch(r"\d{4}-\d{2}-\d{2}", compact)
    if date_match:
        exact = parse_iso_date(compact)
        return Period(raw, exact, exact)

    korean_month_range_match = re.fullmatch(r"(\d{1,2})(?:월)?(?:-|~|부터|에서)(\d{1,2})월", compact)
    if korean_month_range_match:
        start_month = int(korean_month_range_match.group(1))
        end_month = int(korean_month_range_match.group(2))
        if not 1 <= start_month <= 12 or not 1 <= end_month <= 12:
            raise ValueError("month must be between 1 and 12")
        start_year = normalize_month_year(start_month, today)
        end_year = start_year + 1 if end_month < start_month else start_year
        return Period(raw, date(start_year, start_month, 1), month_end(end_year, end_month))

    korean_month_match = re.fullmatch(r"(\d{1,2})월(?:쯤|경|말|초|중순)?", compact)
    if korean_month_match:
        month = int(korean_month_match.group(1))
        if not 1 <= month <= 12:
            raise ValueError("month must be between 1 and 12")
        year = normalize_month_year(month, today)
        return Period(raw, date(year, month, 1), month_end(year, month))

    if compact in {"이번달", "이달"}:
        return Period(raw, today, month_end(today.year, today.month))

    if compact == "다음달":
        year = today.year + 1 if today.month == 12 else today.year
        month = 1 if today.month == 12 else today.month + 1
        return Period(raw, date(year, month, 1), month_end(year, month))

    seasons = {
        "봄": (3, 5),
        "spring": (3, 5),
        "여름": (6, 8),
        "summer": (6, 8),
        "가을": (9, 11),
        "autumn": (9, 11),
        "fall": (9, 11),
        "연말": (12, 12),
    }
    if compact.lower() in seasons:
        start_month, end_month = seasons[compact.lower()]
        year = normalize_month_year(start_month, today)
        return Period(raw, date(year, start_month, 1), month_end(year, end_month))

    if compact in {"겨울", "winter"}:
        start_year = today.year if today.month <= 12 else today.year + 1
        if today.month in {1, 2}:
            start_year = today.year - 1
        start = date(start_year, 12, 1)
        end = month_end(start_year + 1, 2)
        if end < today:
            start = date(today.year, 12, 1)
            end = month_end(today.year + 1, 2)
        return Period(raw, start, end)

    raise ValueError(
        "Unsupported period. Use YYYY-MM, YYYY-MM-DD..YYYY-MM-DD, YYYY-MM-DD, '9월', '가을', or '다음달'."
    )


def trip_dates(departure: date, nights: int) -> List[date]:
    return [departure + timedelta(days=offset) for offset in range(nights + 1)]


def weekday_name(value: date) -> str:
    names = ["월", "화", "수", "목", "금", "토", "일"]
    return names[value.weekday()]


def date_label(value: date) -> str:
    return f"{value.isoformat()}({weekday_name(value)})"


def short_date_label(value: date) -> str:
    return f"{value.month}/{value.day}({weekday_name(value)})"


def weekday_sequence(days: List[date]) -> str:
    return "".join(weekday_name(item) for item in days)


def week_index_for_period(value: date, period: Period) -> int:
    return ((value - period.start).days // 7) + 1


def count_weekend_days(days: Iterable[date]) -> int:
    return sum(1 for item in days if item.weekday() >= 5)


def count_weekdays(days: Iterable[date]) -> int:
    return sum(1 for item in days if item.weekday() < 5)


def describe_pattern(days: List[date], weekend_days: int, leave_days: int) -> str:
    if weekend_days == 0:
        return "평일 중심"
    if weekend_days >= 2 and leave_days <= 2:
        return "주말 압축형"
    if days[0].weekday() == 4 or days[-1].weekday() == 0:
        return "주말 브릿지형"
    return "주말 포함형"


def score_candidate(days: List[date], weekend_mode: str) -> Tuple[float, List[str]]:
    weekend_days = count_weekend_days(days)
    leave_days = count_weekdays(days)
    score = 100.0
    reasons: List[str] = []

    if weekend_mode == "require":
        if weekend_days:
            score += 30
            reasons.append("주말 포함 조건 충족")
        else:
            score -= 120
            reasons.append("주말 포함 조건 미충족")
    elif weekend_mode == "prefer":
        score += weekend_days * 12
        score -= leave_days * 2
        reasons.append("주말을 끼워 연차 부담 완화")
    elif weekend_mode == "avoid":
        score -= weekend_days * 20
        score += (len(days) - weekend_days) * 3
        reasons.append("평일 중심 선호 반영")
    else:
        score -= abs(weekend_days - 1) * 4
        reasons.append("주말/평일 균형")

    if days[0].weekday() in {4, 5}:
        score += 8
        reasons.append("출발일이 금/토라 이동 리듬이 자연스러움")
    if days[-1].weekday() in {0, 6}:
        score += 8
        reasons.append("귀국/귀가일이 일/월이라 복귀 리듬이 좋음")
    if leave_days >= 5:
        score -= 15
        reasons.append("평일 사용일이 많아 연차 부담 큼")

    return score, reasons


def safe_same_month_day(year: int, source: date) -> date:
    try:
        return date(year, source.month, source.day)
    except ValueError:
        return date(year, 2, 28)


def fetch_weather_for_range(
    latitude: float,
    longitude: float,
    start: date,
    end: date,
    timeout: int = 20,
) -> Optional[Dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "daily": "temperature_2m_mean,temperature_2m_min,temperature_2m_max,precipitation_sum",
            "timezone": "auto",
        }
    )
    request = urllib.request.Request(
        f"{OPEN_METEO_ARCHIVE_URL}?{params}",
        headers={"User-Agent": "AgenticBaseTravelPlanner/0.1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def summarize_historical_weather(
    departure: date,
    nights: int,
    latitude: Optional[float],
    longitude: Optional[float],
    years_back: int,
    timeout: int,
) -> WeatherSummary:
    if latitude is None or longitude is None:
        return WeatherSummary(status="skipped", note="lat/lon not provided")

    current_year = date.today().year
    candidate_years = list(range(current_year - years_back, current_year))
    mean_temps: List[float] = []
    min_temps: List[float] = []
    max_temps: List[float] = []
    trip_precips: List[float] = []
    rainy_days: List[int] = []
    sampled_years: List[int] = []

    for year in candidate_years:
        start = safe_same_month_day(year, departure)
        end = start + timedelta(days=nights)
        payload = fetch_weather_for_range(latitude, longitude, start, end, timeout=timeout)
        daily = payload.get("daily") if payload else None
        if not isinstance(daily, dict):
            continue

        temps = [value for value in daily.get("temperature_2m_mean", []) if isinstance(value, (int, float))]
        lows = [value for value in daily.get("temperature_2m_min", []) if isinstance(value, (int, float))]
        highs = [value for value in daily.get("temperature_2m_max", []) if isinstance(value, (int, float))]
        precips = [value for value in daily.get("precipitation_sum", []) if isinstance(value, (int, float))]
        if not temps and not precips:
            continue

        sampled_years.append(year)
        if temps:
            mean_temps.append(statistics.mean(temps))
        if lows:
            min_temps.append(min(lows))
        if highs:
            max_temps.append(max(highs))
        if precips:
            trip_precips.append(sum(precips))
            rainy_days.append(sum(1 for value in precips if value >= 1.0))

    if not sampled_years:
        return WeatherSummary(status="unavailable", note="Open-Meteo archive fetch failed or returned no daily data")

    return WeatherSummary(
        status="ok",
        years=sampled_years,
        avg_temp_c=round(statistics.mean(mean_temps), 1) if mean_temps else None,
        min_temp_c=round(statistics.mean(min_temps), 1) if min_temps else None,
        max_temp_c=round(statistics.mean(max_temps), 1) if max_temps else None,
        avg_trip_precip_mm=round(statistics.mean(trip_precips), 1) if trip_precips else None,
        avg_rainy_days=round(statistics.mean(rainy_days), 1) if rainy_days else None,
        sample_count=len(sampled_years),
        note="same month/day windows from previous years",
    )


def weather_score_delta(weather: Optional[WeatherSummary]) -> Tuple[float, List[str]]:
    if weather is None or weather.status != "ok":
        return 0.0, []

    delta = 0.0
    reasons: List[str] = []
    if weather.avg_temp_c is not None:
        temp_penalty = min(35.0, abs(weather.avg_temp_c - 22.0) * 1.2)
        delta += 24.0 - temp_penalty
        reasons.append(f"과거 평균기온 {weather.avg_temp_c}C")
    if weather.avg_trip_precip_mm is not None:
        rain_penalty = min(25.0, weather.avg_trip_precip_mm * 0.35)
        delta += 12.0 - rain_penalty
        reasons.append(f"과거 평균 강수량 {weather.avg_trip_precip_mm}mm")
    return delta, reasons


def recommend_dates(
    period: Period,
    nights: int,
    weekend_mode: str,
    max_candidates: int,
    destination: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    include_weather: bool = False,
    years_back: int = 5,
    weather_timeout: int = 20,
) -> List[DateCandidate]:
    if nights < 0:
        raise ValueError("nights must be zero or greater")
    latest_departure = period.end - timedelta(days=nights)
    if latest_departure < period.start:
        raise ValueError("period is shorter than the requested trip length")

    candidates: List[DateCandidate] = []
    cursor = period.start
    while cursor <= latest_departure:
        days = trip_dates(cursor, nights)
        weekend_days = count_weekend_days(days)
        leave_days = count_weekdays(days)
        base_score, reasons = score_candidate(days, weekend_mode)
        weather: Optional[WeatherSummary] = None
        if include_weather:
            weather = summarize_historical_weather(cursor, nights, latitude, longitude, years_back, weather_timeout)
            delta, weather_reasons = weather_score_delta(weather)
            base_score += delta
            reasons.extend(weather_reasons)

        pattern = describe_pattern(days, weekend_days, leave_days)
        if weekend_days:
            decision_question = "주말을 끼는 이 방향으로 확정할까요, 아니면 평일 중심의 한산한 일정으로 다시 좁힐까요?"
        else:
            decision_question = "평일 중심의 한산한 방향으로 확정할까요, 아니면 주말을 끼는 일정으로 다시 좁힐까요?"
        prompt = (
            f"{destination or '목적지'} 여행을 {date_label(days[0])} 출발, {date_label(days[-1])} 복귀로 보면 "
            f"{pattern}, 예상 평일 사용 {leave_days}일입니다. {decision_question}"
        )
        candidates.append(
            DateCandidate(
                rank=0,
                departure_date=days[0].isoformat(),
                return_date=days[-1].isoformat(),
                nights=nights,
                days=nights + 1,
                weekday_label=f"{weekday_name(days[0])} 출발/{weekday_name(days[-1])} 복귀",
                pattern=pattern,
                includes_weekend=weekend_days > 0,
                weekend_days=weekend_days,
                leave_days_estimate=leave_days,
                score=round(base_score, 2),
                score_reasons=reasons,
                confirmation_prompt=prompt,
                weather=weather,
            )
        )
        cursor += timedelta(days=1)

    ranked = sorted(candidates, key=lambda item: item.score, reverse=True)[:max_candidates]
    for index, candidate in enumerate(ranked, start=1):
        candidate.rank = index
    return ranked


def candidates_to_payload(args: argparse.Namespace, period: Period, candidates: List[DateCandidate]) -> Dict[str, Any]:
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "period": {"label": period.label, "start": period.start.isoformat(), "end": period.end.isoformat()},
        "destination": args.destination,
        "nights": args.nights,
        "weekend_mode": args.weekend,
        "candidates": [candidate_to_dict(candidate, period) for candidate in candidates],
    }


def candidate_to_dict(candidate: DateCandidate, period: Optional[Period] = None) -> Dict[str, Any]:
    data = asdict(candidate)
    if candidate.weather is None:
        data["weather"] = None
    departure = parse_iso_date(candidate.departure_date)
    trip_days = trip_dates(departure, candidate.nights)
    data["weekday_sequence"] = weekday_sequence(trip_days)
    data["date_range_label"] = f"{short_date_label(trip_days[0])} - {short_date_label(trip_days[-1])}"
    data["select_label"] = f"{data['date_range_label']} · {data['weekday_sequence']}"
    if period is not None:
        week_index = week_index_for_period(departure, period)
        data["week_index"] = week_index
        data["week_label"] = f"{week_index}주차"
    return data


def format_weather_markdown(weather: Optional[WeatherSummary]) -> str:
    if weather is None:
        return "-"
    if weather.status == "skipped":
        return "좌표 미입력"
    if weather.status != "ok":
        return "조회 실패"
    bits: List[str] = []
    if weather.avg_temp_c is not None:
        bits.append(f"평균 {weather.avg_temp_c}C")
    if weather.avg_trip_precip_mm is not None:
        bits.append(f"강수 {weather.avg_trip_precip_mm}mm")
    if weather.avg_rainy_days is not None:
        bits.append(f"비 {weather.avg_rainy_days}일")
    if weather.years:
        bits.append(f"{min(weather.years)}-{max(weather.years)}")
    return ", ".join(bits) if bits else "데이터 부족"


def print_candidates_markdown(period: Period, candidates: List[DateCandidate], destination: str) -> None:
    print(f"# {destination or '여행'} 날짜 후보")
    print()
    print(f"> 기준 생성 시각: {datetime.now().isoformat(timespec='seconds')}")
    print(f"> 탐색 범위: {period.start.isoformat()} ~ {period.end.isoformat()} ({period.label})")
    print()
    print("| 순위 | 출발 | 복귀 | 패턴 | 평일 사용 | 점수 | 과거 날씨 | 확인 질문 |")
    print("|---:|---|---|---|---:|---:|---|---|")
    for candidate in candidates:
        print(
            "| {rank} | {departure} | {return_date} | {pattern} | {leave_days}일 | {score} | {weather} | {prompt} |".format(
                rank=candidate.rank,
                departure=date_label(parse_iso_date(candidate.departure_date)),
                return_date=date_label(parse_iso_date(candidate.return_date)),
                pattern=candidate.pattern,
                leave_days=candidate.leave_days_estimate,
                score=candidate.score,
                weather=format_weather_markdown(candidate.weather),
                prompt=candidate.confirmation_prompt,
            )
        )
    print()
    print("다음 단계: 사용자가 날짜 후보를 고르면 해당 출발/복귀일로 항공권과 숙소 검색 URL을 고정해 실제 데이터를 수집합니다.")


def save_json_payload(payload: Dict[str, Any], output: Optional[str], default_name: str) -> Path:
    path = Path(output).expanduser() if output else DEFAULT_OUTPUT_DIR / default_name
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")
    return path


def load_candidate_from_file(path_value: str, rank: int) -> Dict[str, Any]:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError("candidate file has no candidates list")
    for item in candidates:
        if isinstance(item, dict) and int(item.get("rank", -1)) == rank:
            return item
    raise ValueError(f"candidate rank {rank} not found")


def fill_url_template(url: str, args: argparse.Namespace) -> str:
    replacements = {
        "origin": args.origin or "",
        "destination": args.destination or "",
        "depart_date": args.depart_date or "",
        "return_date": args.return_date or "",
        "adults": str(args.adults or 1),
        "rooms": str(args.rooms or 1),
    }
    filled = url
    for key, value in replacements.items():
        filled = filled.replace("{" + key + "}", urllib.parse.quote(str(value), safe=""))
    return filled


def parse_collection_items(texts: List[str]) -> List[CollectionItem]:
    items: List[CollectionItem] = []
    for index, text in enumerate(texts, start=1):
        compact = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if not compact:
            continue
        prices = list(dict.fromkeys(match.group(0).strip() for match in PRICE_PATTERN.finditer(compact)))
        times = list(dict.fromkeys(match.group(0).strip() for match in TIME_PATTERN.finditer(compact)))
        items.append(CollectionItem(index=index, text=compact[:2000], prices=prices[:8], times=times[:8]))
    return items


async def collect_with_playwright(args: argparse.Namespace) -> Dict[str, Any]:
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise RuntimeError(
            "playwright is not installed. Install requirements or run through the provided Docker image."
        ) from exc

    url = fill_url_template(args.url, args)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=not args.headed,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = await browser.new_page(
            viewport={"width": args.width, "height": args.height},
            user_agent=args.user_agent,
        )
        await page.goto(url, wait_until=args.wait_until, timeout=args.timeout_ms)
        if args.wait_selector:
            await page.wait_for_selector(args.wait_selector, timeout=args.timeout_ms)
        if args.settle_ms:
            await page.wait_for_timeout(args.settle_ms)

        if args.card_selector:
            locator = page.locator(args.card_selector)
            count = min(await locator.count(), args.max_items)
            texts = [await locator.nth(index).inner_text(timeout=args.timeout_ms) for index in range(count)]
        else:
            body_text = await page.locator("body").inner_text(timeout=args.timeout_ms)
            texts = [body_text]

        title = await page.title()
        screenshot_path: Optional[str] = None
        if args.screenshot:
            screenshot = Path(args.screenshot).expanduser()
            if not screenshot.is_absolute():
                screenshot = Path.cwd() / screenshot
            screenshot.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(screenshot), full_page=True)
            screenshot_path = str(screenshot)
        await browser.close()

    items = parse_collection_items(texts)
    return {
        "collected_at": datetime.now().isoformat(timespec="seconds"),
        "kind": args.kind,
        "url": url,
        "title": title,
        "adapter": args.adapter,
        "selectors": {
            "card_selector": args.card_selector,
            "wait_selector": args.wait_selector,
        },
        "search_context": {
            "origin": args.origin,
            "destination": args.destination,
            "depart_date": args.depart_date,
            "return_date": args.return_date,
            "adults": args.adults,
            "rooms": args.rooms,
        },
        "screenshot": screenshot_path,
        "items": [asdict(item) for item in items],
        "notes": [
            "This is a rendered-page snapshot. Verify booking terms, baggage, cancellation, and taxes on the source site before treating data as final.",
            "Some travel sites restrict automation or personalize prices. Use official or trusted booking channels and respect site terms.",
        ],
    }


def command_dates(args: argparse.Namespace) -> int:
    period = parse_period(args.period)
    candidates = recommend_dates(
        period=period,
        nights=args.nights,
        weekend_mode=args.weekend,
        max_candidates=args.max_candidates,
        destination=args.destination,
        latitude=args.lat,
        longitude=args.lon,
        include_weather=args.weather,
        years_back=args.years_back,
        weather_timeout=args.weather_timeout,
    )
    payload = candidates_to_payload(args, period, candidates)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_candidates_markdown(period, candidates, args.destination)

    if args.output:
        path = save_json_payload(payload, args.output, "date_candidates.json")
        print(f"\nSaved: {path}", file=sys.stderr)
    return 0


def command_collect(args: argparse.Namespace) -> int:
    if args.candidate_file:
        candidate = load_candidate_from_file(args.candidate_file, args.candidate_rank)
        args.depart_date = args.depart_date or candidate.get("departure_date")
        args.return_date = args.return_date or candidate.get("return_date")

    payload = asyncio.run(collect_with_playwright(args))
    default_name = f"{args.kind}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = save_json_payload(payload, args.output, default_name)
    print(json.dumps({"saved": str(path), "items": len(payload.get("items", [])), "url": payload["url"]}, ensure_ascii=False))
    return 0


def command_serve(args: argparse.Namespace) -> int:
    class Handler(BaseHTTPRequestHandler):
        def send_payload(self, status: int, payload: Dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            try:
                if parsed.path == "/health":
                    self.send_payload(200, {"status": "ok", "service": "travel-planner-cli"})
                    return
                if parsed.path == "/dates":
                    period_text = params.get("period", ["다음달"])[0]
                    nights = int(params.get("nights", ["3"])[0])
                    weekend = params.get("weekend", ["prefer"])[0]
                    destination = params.get("destination", [""])[0]
                    max_candidates = int(params.get("max", ["5"])[0])
                    lat = float(params["lat"][0]) if "lat" in params else None
                    lon = float(params["lon"][0]) if "lon" in params else None
                    weather = params.get("weather", ["0"])[0] in {"1", "true", "yes"}
                    period = parse_period(period_text)
                    candidates = recommend_dates(
                        period=period,
                        nights=nights,
                        weekend_mode=weekend,
                        max_candidates=max_candidates,
                        destination=destination,
                        latitude=lat,
                        longitude=lon,
                        include_weather=weather,
                        years_back=5,
                        weather_timeout=20,
                    )
                    self.send_payload(
                        200,
                        {
                            "period": {
                                "label": period.label,
                                "start": period.start.isoformat(),
                                "end": period.end.isoformat(),
                            },
                            "destination": destination,
                            "candidates": [candidate_to_dict(candidate, period) for candidate in candidates],
                        },
                    )
                    return
                self.send_payload(404, {"error": "not_found", "paths": ["/health", "/dates"]})
            except Exception as exc:  # pragma: no cover - defensive server boundary
                self.send_payload(400, {"error": str(exc)})

        def log_message(self, format: str, *args: Any) -> None:
            if not getattr(args_namespace, "quiet", False):
                super().log_message(format, *args)

    args_namespace = args
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"travel-planner-cli server listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Travel planner date and real-data collection CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dates = subparsers.add_parser("dates", help="recommend concrete travel date windows from a rough period")
    dates.add_argument("--period", required=True, help="YYYY-MM, YYYY-MM-DD..YYYY-MM-DD, 9월, 가을, 다음달")
    dates.add_argument("--nights", type=int, default=3)
    dates.add_argument("--destination", default="")
    dates.add_argument("--weekend", choices=["prefer", "require", "avoid", "either"], default="prefer")
    dates.add_argument("--max-candidates", type=int, default=5)
    dates.add_argument("--weather", action="store_true", help="compare same date windows from previous years")
    dates.add_argument("--lat", type=float, default=None)
    dates.add_argument("--lon", type=float, default=None)
    dates.add_argument("--years-back", type=int, default=5)
    dates.add_argument("--weather-timeout", type=int, default=20)
    dates.add_argument("--format", choices=["markdown", "json"], default="markdown")
    dates.add_argument("--output", help="save JSON payload to this path")
    dates.set_defaults(func=command_dates)

    collect = subparsers.add_parser("collect", help="collect rendered flight/lodging search results with Playwright")
    collect.add_argument("--kind", choices=["flight", "lodging"], required=True)
    collect.add_argument("--url", required=True, help="search URL or URL template with {depart_date}/{return_date}")
    collect.add_argument("--adapter", default="generic")
    collect.add_argument("--origin", default="")
    collect.add_argument("--destination", default="")
    collect.add_argument("--depart-date", default="")
    collect.add_argument("--return-date", default="")
    collect.add_argument("--adults", type=int, default=1)
    collect.add_argument("--rooms", type=int, default=1)
    collect.add_argument("--candidate-file", help="JSON generated by the dates command")
    collect.add_argument("--candidate-rank", type=int, default=1)
    collect.add_argument("--card-selector", help="CSS selector for result cards. If omitted, body text is captured.")
    collect.add_argument("--wait-selector", help="CSS selector to wait for before extracting")
    collect.add_argument("--max-items", type=int, default=20)
    collect.add_argument("--wait-until", choices=["load", "domcontentloaded", "networkidle", "commit"], default="networkidle")
    collect.add_argument("--settle-ms", type=int, default=2000)
    collect.add_argument("--timeout-ms", type=int, default=45000)
    collect.add_argument("--width", type=int, default=1440)
    collect.add_argument("--height", type=int, default=1200)
    collect.add_argument("--headed", action="store_true")
    collect.add_argument("--screenshot", help="optional screenshot path")
    collect.add_argument("--output", help="save collected JSON to this path")
    collect.add_argument(
        "--user-agent",
        default=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
    )
    collect.set_defaults(func=command_collect)

    serve = subparsers.add_parser("serve", help="run a tiny HTTP server for Docker health checks and date candidates")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=int(os.environ.get("TRAVEL_PLANNER_PORT", "8765")))
    serve.add_argument("--quiet", action="store_true")
    serve.set_defaults(func=command_serve)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
