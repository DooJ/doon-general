<p align="center">
  <img src="./assets/brand/doon-logo.svg" alt="DooN — DO:ON" width="720">
</p>

<p align="center"><strong>Turn broad ideas into useful, finished work.</strong></p>

<p align="center">
  <img src="./assets/brand/doon-hero.png" alt="DooN General skill network" width="100%">
</p>

# DooN General

**DooN General**은 기획, 디자인, 조사, 문서화와 일상 업무를 실행 가능한 결과로 연결하는 공개 Codex·Claude Code·Antigravity 플러그인입니다. 설치 시 모든 스킬을 포함하며, 설치 후 사용하지 않을 스킬을 개별적으로 끌 수 있습니다.

스킬별 목적, 여행 상위·하위 관계와 대체 동작은 [플러그인 운영 안내](docs/README.md)에 정리했습니다.

## 포함된 스킬

| 스킬 | 설명 |
|---|---|
| `product-planner` | 아이디어를 문제, 사용자, 가치, POC와 MVP 범위로 구체화합니다. |
| `requirements-analyst` | PRD와 기능·비기능 요구사항, 예외 흐름, acceptance criteria를 정리합니다. |
| `ux-researcher` | 인터뷰, 설문, 사용성 테스트와 사용자 가설 검증 계획을 설계합니다. |
| `information-architect` | 사이트맵, 내비게이션, 화면 목록과 정보 분류 체계를 설계합니다. |
| `interaction-designer` | 사용자 흐름, 상태 전이, 입력 피드백과 오류 복구 동작을 설계합니다. |
| `content-strategist` | UX writing, 버튼·상태 문구, 브랜드 voice and tone을 만듭니다. |
| `ui-concept-director` | 디자인 레퍼런스를 바탕으로 여러 UI 방향과 첫 화면 콘셉트를 제안합니다. |
| `design-generalist` | 선택된 디자인 방향을 레이아웃, 반응형, 접근성과 구현 handoff로 구체화합니다. |
| `design-system-curator` | 디자인 토큰, 컴포넌트 상태, 패턴과 시각 QA 기준을 정리합니다. |
| `refining-implemented-ui` | 구현된 UI를 기준 화면과 비교해 개선안과 구현 일치 여부를 검토합니다. |
| `living-doc-writer` | 요구사항, 운영, 온보딩 등 계속 갱신할 최신 문서를 작성합니다. |
| `snapshot-report-writer` | 특정 시점의 프로젝트 상태, 구조, 리스크와 준비도를 보고서로 남깁니다. |
| `service-guide-builder` | 실제 화면과 코드를 근거로 클릭형 서비스 사용 가이드를 만듭니다. |
| `travel-planner` | 여러 여행 조사 결과를 조율해 일정, 비용과 대체안으로 합성합니다. |
| `travel-destination-research` | 목적지의 날씨, 입국, 결제, 통신과 안전 정보를 조사합니다. |
| `travel-flight-search` | 항공·철도·버스 등 장거리 이동수단의 시간과 비용을 비교합니다. |
| `travel-lodging-search` | 숙박 권역과 후보의 가격, 취소 조건과 동선 적합성을 비교합니다. |
| `travel-place-search` | 관광지, 체험, 식당, 카페와 쇼핑 장소를 동선 기준으로 조사합니다. |
| `travel-transport-search` | 공항 이동과 현지 대중교통·택시·렌터카 방법을 비교합니다. |
| `travel-itinerary-builder` | 확정된 예약과 조사 결과를 날짜별 실행 일정으로 조립합니다. |
| `stock-analyst` | 시장 흐름과 종목의 실적, 밸류에이션, 기술적 흐름과 리스크를 분석합니다. |
| `real-estate-expert` | 지역 호재, 교통·학군·상권과 아파트 가격·공급 리스크를 분석합니다. |
| `project-legal-advisor` | 앱·웹·AI 프로젝트의 개인정보, 약관, 저작권과 사업 법률 리스크를 검토합니다. |
| `pt-trainer` | 목표, 운동 경험, 부상, 장비와 일정에 맞는 안전한 훈련 루틴을 제안합니다. |
| `general-skill-versioning` | General 저장소의 스킬 버전, 출처, 내용 지문과 플러그인 버전을 검증합니다. |

## 동작 방식

요청의 목적과 필요한 결과물을 먼저 정리한 뒤, 적합한 전문 스킬이 조사·구조화·작성·검토를 맡습니다. 여러 스킬이 함께 쓰일 때도 각 역할의 입력과 산출물을 분리해 결과가 어디에서 만들어졌는지 추적할 수 있게 합니다.

제품·디자인·문서 스킬을 기본 영역으로 두고, 여행과 전문 생활 영역은 사용하지 않을 스킬을 설치 후 끄는 구성을 권장합니다. 모든 스킬은 이 저장소 안의 지침과 자료만으로 동작합니다.

여행 그룹에서는 `travel-planner`가 상위 스킬입니다. 플래너를 끄면 여섯 하위 여행 스킬도 함께 사용하지 않습니다. 플래너가 켜져 있으면 하위 스킬을 각각 끌 수 있고, 그 선택은 플래너를 껐다가 다시 켜도 유지됩니다.

```bash
bash scripts/plugin.sh skills status
bash scripts/plugin.sh skills disable travel-planner
bash scripts/plugin.sh skills enable travel-planner
bash scripts/plugin.sh skills disable travel-flight-search
bash scripts/plugin.sh skills enable travel-flight-search
```

이 명령은 플러그인 파일을 삭제하지 않고 사용 상태를 저장합니다. Codex의 스킬 설정과 Claude Code의 스킬 실행 거부 규칙을 갱신하며, 새 세션에서 적용됩니다. Antigravity는 현재 플러그인 단위 켜기·끄기만 공식 지원하므로 개별 스킬 차단은 검증 전입니다.

## 설치와 설정

```bash
git clone https://github.com/DooJ/doon-general.git
cd doon-general
bash scripts/plugin.sh install
```

관리 스크립트가 컴퓨터에 설치된 Codex, Claude Code, Antigravity를 자동으로 찾아 각각 필요한 형식으로 설치합니다. 설치되지 않은 에이전트는 건너뜁니다. 같은 플러그인이 다른 마켓플레이스로 이미 설치되어 있으면 중복 설치하지 않습니다.

### 관리 명령

| 목적 | 명령 |
|---|---|
| 설치·에이전트 설정 | `bash scripts/plugin.sh install` |
| 설정 다시 적용 | `bash scripts/plugin.sh setup` |
| Git과 모든 에이전트 최신화 | `bash scripts/plugin.sh update` |
| 현재 파일로 설치 복구 | `bash scripts/plugin.sh repair` |
| 패키지·버전·테스트 검증 | `bash scripts/plugin.sh test` |
| Git·에이전트 상태 확인 | `bash scripts/plugin.sh status` |

특정 에이전트를 제외하려면 설치·설정·최신화·복구 명령에 `--skip-codex`, `--skip-claude`, `--skip-antigravity`를 붙입니다. 적용 후에는 해당 에이전트의 새 세션을 시작합니다.

## 구조

- `.codex-plugin/plugin.json`: 플러그인 메타데이터와 `skills/` 등록
- `.claude-plugin/plugin.json`: Claude Code 네이티브 플러그인 메타데이터
- `antigravity/plugin.json`: Antigravity 전용 manifest
- `scripts/build_antigravity_plugin.py`: 설치 가능한 Antigravity 패키지 생성기
- `scripts/plugin.sh`: 설치, 설정, 최신화, 복구, 테스트 통합 명령
- `skills/<이름>/`: 실제 스킬 원본, 버전, references, scripts, assets
- `catalog.json`: 저장소와 스킬 소유권을 확인하는 카탈로그
- `PLUGIN_VERSION.md`: 플러그인 단위 변경 이력과 출처
- `.agents/plugins/marketplace.json`: Codex 로컬 marketplace
- `.claude-plugin/marketplace.json`: Claude Code 로컬 marketplace

각 스킬의 버전과 출처는 해당 폴더의 `VERSION.md`에서 관리합니다. 외부 원문을 포함한 스킬의 개별 라이선스도 함께 보존합니다. 이 저장소는 설치 대상 프로젝트에 별도 런타임 폴더를 생성하지 않습니다.
