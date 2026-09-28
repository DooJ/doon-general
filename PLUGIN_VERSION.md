# DooN General 플러그인 버전

현재 버전: `v3.1.0`

## 출처

| ID | 분류 | 자료 | 반영 범위 |
|---|---|---|---|
| `P1` | 자체 생성 | 2026-09-23 사용자 요청과 기존 스킬 저장소 | 저장소별 플러그인 그룹과 기존 독립 스킬 구성 |
| `P2` | 외부 참고 | [OpenAI 플러그인 패키징 문서](https://developers.openai.com/plugins/build/plugins), 2026-09-23 조회 | `.codex-plugin/plugin.json`, `skills/` 패키징과 마켓플레이스 호환 구조 |
| `P3` | 자체 생성 | 2026-09-23 사용자 요청 | DooN 브랜드, DO:ON 로고와 범용 플러그인 README 구성 |
| `P4` | 자체 생성 | 2026-09-24 사용자 승인 DooN 기술 이름 전환 | plugin ID, 저장소와 core source 식별자의 DooN 전환 |

| `P5` | 자체 생성 | 2026-09-28 사용자 요청 | canonical 내부 폴더를 `.doon`으로 전환하고 이전 경로 폴백을 제거 |
| `P6` | 외부 참고 | [Claude Code 플러그인 문서](https://code.claude.com/docs/en/plugins), 2026-09-28 조회 | `.claude-plugin/plugin.json`, `skills/` 기반 Claude 네이티브 패키징 |

| `P7` | 자체 생성 | 2026-09-28 사용자 승인 DooN Core 통합 설계 | 개별 플러그인의 `.doon` 의존 제거, portable manifest와 Core export 계약 |

## 버전 이력

| 버전 | 날짜 | 변경 요약 | 출처 ID |
|---|---|---|---|
| `v3.1.0` | 2026-09-28 | Core 없이 독립 설치할 수 있도록 portable manifest를 추가하고 플러그인 내부의 legacy `.doon` 복제 구조를 제거했다. | `P7` |
| `v3.0.0` | 2026-09-28 | canonical 내부 경로를 `.doon`으로 전환하고 Claude Code 네이티브 플러그인 manifest를 추가했다. | `P5`, `P6` |
| `v2.0.0` | 2026-09-24 | plugin ID와 저장소 식별자를 `doon-general`과 `DooJ/doon-core` 체계로 전환했다. 기존 설치와 구분되는 breaking 변경이다. | `P4` |
| `v1.0.1` | 2026-09-23 | 사용자 표시명을 DooN General로 바꾸고 DO:ON 로고, 상징 이미지, 영역 중심 README를 추가했다. 기술 plugin ID와 저장소명은 유지했다. | `P3` |
| `v1.0.0` | 2026-09-23 | 기존 스킬 모음을 하나의 설치·활성화 단위로 묶고 내부 스킬을 개별적으로 노출하는 플러그인 구조를 처음 등록했다. | `P1`, `P2` |
