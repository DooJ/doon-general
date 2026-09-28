# Surface Patterns

이 문서는 표면 유형별 빠른 판단 기준입니다. 더 상세한 규칙은 웹 작업에서 `.doon/rules/05_web_design_rules.md`, 앱 작업에서 `.doon/rules/06_app_design_rules.md`를 함께 봅니다. 샘플 사이트와 플랫폼별 레퍼런스는 `platform_reference_matrix.md`를 사용합니다.

## Web App / SaaS

- 핵심은 "이 화면에서 사용자가 가장 자주 하는 일"을 가장 짧은 경로로 만드는 것입니다.
- navigation depth를 늘리기보다 section hierarchy, filter, quick action, inline feedback를 먼저 정리합니다.
- 데이터가 많으면 카드만 늘리지 말고 table, segmented control, sticky summary, density toggle을 고려합니다.
- 필수 상태:
  - loading skeleton
  - empty state with next action
  - error state with retry or fallback
  - permission/state badge
- 자주 쓰는 레퍼런스 축:
  - Mobbin의 실제 SaaS/Web App flow
  - Land-book의 SaaS/AI landing 구조
  - SaaS settings, billing, team management
  - dashboard summary, table, filter, saved view
  - dialog, drawer, toast, command/search

## Mobile App

- thumb reach, safe area, keyboard 등장 시 레이아웃 변화, 네트워크 제약을 먼저 고려합니다.
- 첫 화면에 모든 기능을 밀어 넣기보다 progressive disclosure를 사용합니다.
- bottom navigation은 3~5개 수준에서 의미가 있을 때만 씁니다.
- 스크롤 중 맥락을 잃지 않도록 sticky summary, step indicator, inline validation을 활용합니다.
- 데스크톱 패턴을 그대로 축소하지 말고 입력 길이, 집중 흐름, gesture 충돌을 점검합니다.
- iOS와 Android는 navigation, back behavior, permission, sheet/dialog, picker 관습을 분리합니다.
- 앱 작업은 offline, push notification, deep link, 권한 거절 후 대안을 기본 상태로 봅니다.

## Landing / Marketing Page

- 서사는 보통 `Promise -> Proof -> Feature/Benefit -> How it works -> CTA` 구조가 안정적입니다.
- 첫 화면은 메시지, 대상 사용자, 주요 행동을 5초 안에 이해할 수 있어야 합니다.
- 비주얼은 대담할 수 있지만 CTA, proof, trust signal보다 앞서면 안 됩니다.
- 스크롤마다 완전히 다른 스타일을 쓰기보다 반복되는 rhythm을 만들어 브랜드 기억점을 만듭니다.
- proof, pricing, FAQ, demo/product shot, trust signal을 장식보다 먼저 확인합니다.
- Land-book은 SaaS/AI/스타트업 랜딩 구조, Awwwards는 브랜드 인터랙션과 motion, Behance는 브랜딩 case study를 볼 때 우선합니다.

## Admin / Internal Tool

- 화려함보다 속도, 가시성, 실수 방지, batch action이 중요합니다.
- 상태와 권한 차이를 눈에 잘 띄게 표현하고, destructive action은 확인 절차를 명확히 둡니다.
- 운영툴은 card grid보다 table, filter, search, bulk edit, audit trail이 더 중요한 경우가 많습니다.
- 긴 폼은 section group, sticky action bar, autosave/dirty state 표기로 부담을 줄입니다.
- destructive action, 권한 변경, 고객 알림 발송은 confirmation, preview, log, undo 가능성을 함께 설계합니다.
- Mobbin은 settings, profile, billing, admin flow처럼 실제 반복 업무 흐름을 확인할 때 우선하고, Dribbble의 dashboard shot은 visual polish 참고로만 사용합니다.

## Design Direction by Surface

- Web app:
  - 명확한 hierarchy, 빠른 task completion, 상태 가시성 중심
- Mobile app:
  - 집중된 flow, 짧은 입력, 한 손 사용성 중심
- Landing page:
  - 메시지 전달, 차별점, 신뢰, CTA 전환 중심
- Internal tool:
  - 처리 속도, 데이터 정확성, 운영 안정성 중심
