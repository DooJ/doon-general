# DooN General 플러그인 운영 안내

최종 확인: 2026-09-30 · 대상 버전: 4.4.0

기획·디자인·문서화·여행 조사·일반 자문 스킬을 목적별로 선택하기 위한 안내입니다. 설치 명령과 25개 스킬의 한 줄 설명은 [저장소 README](../README.md)를 보세요. 모든 스킬은 함께 설치되지만, 사용 여부는 설치 후 별도로 설정합니다.

## 목적별 구성

| 영역 | 주요 스킬 | 결과의 경계 |
|---|---|---|
| 제품·디자인 | `product-planner` → `requirements-analyst` → `information-architect`·`interaction-designer` → `ui-concept-director`·`design-generalist`·`design-system-curator` | 문제·요구사항·화면 흐름·시각 규칙을 단계별로 구분. 필요한 단계만 사용 |
| 조사·콘텐츠 | `ux-researcher`, `content-strategist`, `refining-implemented-ui`, `service-guide-builder` | 가설 검증, 문구, 구현 UI 개선, 실제 서비스 안내는 서로 다른 근거를 사용 |
| 문서 | `living-doc-writer`, `project-work-checkpoint`, `snapshot-report-writer` | 계속 갱신할 현재 문서, 작업별 상태 정리와 특정 시점의 고정 보고서를 구분 |
| 여행 | `travel-planner`와 6개 전문 스킬 | 상위 계획과 항공·숙소·목적지·장소·교통·일정 조립을 분리 |
| 자문 | `project-legal-advisor`, `stock-analyst`, `real-estate-expert`, `pt-trainer` | 시점·출처·전제와 불확실성을 밝히는 참고 분석. 전문 자격자의 개별 판단을 대체하지 않음 |
| 유지 | `general-skill-versioning` | 이 저장소의 스킬 버전·출처·검증 |

`product-planner` 등은 권장 작업 순서일 뿐 자동 활성화 묶음은 아닙니다. 해당 요청에 실제로 필요한 스킬만 사용합니다.

## 여행 스킬의 상위·하위 계약

`travel-planner`가 상위 스킬이고, `travel-destination-research`, `travel-flight-search`, `travel-lodging-search`, `travel-place-search`, `travel-transport-search`, `travel-itinerary-builder`가 하위입니다. 전체 여행 설계는 상위가 입력·제약·결과를 합성합니다. “항공편만 찾아줘” 같은 부분 요청은 해당 전문 스킬을 직접 사용할 수 있습니다.

상위를 끄면 여섯 하위도 함께 사용하지 않습니다. 상위가 켜져 있으면 하위를 개별적으로 끌 수 있고, 상위를 다시 켜도 그 개별 설정은 유지됩니다. 꺼진 스킬을 몰래 재활성화하지 않습니다. 필요한 기능이 없으면 상위는 동등한 활성 기능이 있는지 확인하고, 없으면 에이전트의 일반 도구로 대체할 수 있습니다. 대체 방식(`preferred`, `equivalent`, `tool_fallback`)과 못 채운 항목은 결과에 명시합니다. 실제 예약, 결제, 가격·입국 조건은 확인 시점과 출처를 남기고 사용자가 최종 확인해야 합니다.

## 설치·사용 설정·복구

저장소 루트의 `bash scripts/plugin.sh install`은 설치된 Codex·Claude Code·Antigravity를 감지합니다. `setup`은 설정 재적용, `repair`는 현재 파일로 복구, `update`는 Git 최신화 후 재설정, `test`는 패키지·버전·테스트 검증, `status`는 상태 확인입니다.

```bash
bash scripts/plugin.sh skills status
bash scripts/plugin.sh skills disable travel-flight-search
bash scripts/plugin.sh skills disable travel-planner
bash scripts/plugin.sh skills enable travel-planner
bash scripts/plugin.sh test
```

스킬 사용 중지는 설치 파일 삭제와 다릅니다. Codex·Claude에는 새 세션부터 적용됩니다. Antigravity는 플러그인 단위 켜기·끄기와 달리 스킬별 차단이 아직 검증되지 않았습니다.

## 원본·갱신 기준

원본은 `skills/*/SKILL.md`, `catalog.json`, `scripts/plugin.sh`, 각 에이전트의 manifest입니다. 여행의 구체적인 입력·출력 계약은 각 여행 스킬, 특히 `travel-planner/SKILL.md`에서 확인합니다. 스킬 변경 시 `general-skill-versioning`을 따릅니다. 스킬·활성화 묶음, 대체 경로, 설치 방식, 자문 범위가 바뀌면 이 문서를 갱신합니다. 여행 가격·일정이나 법률·시장 정보처럼 변동 가능한 사실을 이 문서에 고정값으로 기록하지 않습니다.
