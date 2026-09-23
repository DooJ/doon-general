<p align="center">
  <img src="./assets/brand/doon-logo.svg" alt="DooN — DO:ON" width="720">
</p>

<p align="center"><strong>Turn broad ideas into useful, finished work.</strong></p>

<p align="center">
  <img src="./assets/brand/doon-hero.png" alt="DooN General skill network" width="100%">
</p>

# DooN General

**DooN General**은 기획, 디자인, 조사, 문서화와 일상 업무를 실행 가능한 결과로 연결하는 공개 Codex 플러그인입니다. 플러그인 전체와 내부 스킬을 각각 활성화할 수 있어 필요한 역할만 조합해 사용할 수 있습니다.

## 포함된 영역

| 영역 | 주요 스킬 |
|---|---|
| 제품 기획 | `product-planner`, `requirements-analyst`, `content-strategist` |
| UX·정보 구조 | `ux-researcher`, `information-architect`, `interaction-designer` |
| UI·디자인 시스템 | `ui-concept-director`, `design-generalist`, `design-system-curator`, `refining-implemented-ui` |
| 문서와 서비스 안내 | `living_doc_writer`, `snapshot_report_writer`, `service-guide-builder` |
| 조사와 전문 판단 | `stock-analyst`, `real-estate-expert`, `project-legal-advisor` |
| 여행 | `travel-planner`와 항공·숙박·장소·교통·일정 조사 스킬 |
| 개인 활동 | `pt-trainer` |

## 동작 방식

요청의 목적과 필요한 결과물을 먼저 정리한 뒤, 적합한 전문 스킬이 조사·구조화·작성·검토를 맡습니다. 여러 스킬이 함께 쓰일 때도 각 역할의 입력과 산출물을 분리해 결과가 어디에서 만들어졌는지 추적할 수 있게 합니다.

## 구조

- `.codex-plugin/plugin.json`: 플러그인 메타데이터와 `skills/` 등록
- `skills/<이름>/`: 실제 스킬 원본, 버전, references, scripts, assets
- `catalog.json`: 저장소와 스킬 소유권을 확인하는 카탈로그
- `PLUGIN_VERSION.md`: 플러그인 단위 변경 이력과 출처

각 스킬의 버전과 출처는 해당 폴더의 `VERSION.md`에서 관리합니다. 외부 원문을 포함한 스킬의 개별 라이선스도 함께 보존합니다.
