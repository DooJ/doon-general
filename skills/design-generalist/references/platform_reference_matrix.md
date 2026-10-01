# Platform Reference Matrix

갱신일: 2026-10-01

이 문서는 사용자가 제공한 레퍼런스와 공식 자료를 작업 기준으로 정리한 것이다. 개별 사이트의 최신 화면, 멤버십, 검색 기능, 공개 범위가 중요한 작업이면 웹 검색이나 실제 접속으로 현재성을 확인한다.

이 문서는 웹/앱 디자인 작업을 시작할 때 플랫폼과 목적에 맞는 레퍼런스를 고르는 기준이다. 레퍼런스는 복제 대상이 아니라 정보 구조, interaction, density, component, content tone을 비교하기 위한 판단 재료다.

## 사용 원칙
- 먼저 현재 프로젝트 내부 화면, 컴포넌트, CSS, 디자인 문서를 확인한다.
- 외부 레퍼런스는 `무엇을 참고하는지`를 명시한다: navigation, density, CTA, form, table, onboarding, payment, empty state 등.
- 2-3개 후보를 고를 때는 색상만 다른 예시를 고르지 말고 구조와 상호작용이 다른 예시를 고른다.
- 레퍼런스 후보는 스타일 프리셋이 아니다. 서비스 도메인, 사용 빈도, 감정 톤, 데이터 밀도에 맞는 구조를 고르는 출발점이다.
- 기본 SaaS/카드형/대시보드형 레이아웃을 선택할 때는 왜 그 구조가 해당 서비스에 맞는지 근거를 남긴다.
- 최신 공개 사례가 중요한 작업이면 웹 검색으로 현재 화면과 URL을 확인하고 출처를 남긴다.
- 유료/로그인형 레퍼런스는 접근 가능한 범위만 근거로 삼고, 보이지 않는 화면은 확정 사실처럼 쓰지 않는다.
- 레퍼런스 사이트를 고를 때는 `표면 유형`, `UX flow`, `컴포넌트`, `브랜드/인터랙션`, `프로세스/케이스스터디` 중 무엇이 필요한지 먼저 정한다.
- Dribbble, Awwwards처럼 시각적 완성도가 강한 레퍼런스는 실제 상태, 긴 데이터, 접근성, 구현 비용을 별도로 검증한다.
- 실제 검색이나 열람을 했다면 `reference_evidence_log.md` 형식으로 검색어/URL/title/관찰/반영/배제를 기록한다.
- 실제 화면을 확인하지 않았다면 사이트명을 근거처럼 쓰지 말고 `사이트 성격만 참고`, `실화면 미확인`으로 표시한다.

## 자료의 역할과 적용 순서

| 자료 유형 | 사용 시점 | 산출물에 반영할 것 |
|---|---|---|
| 플랫폼 가이드 | 대상 플랫폼과 기본 동작을 정할 때 | iOS는 Apple HIG, Android는 Material 3의 탐색·시스템 동작·접근성 기대치. 웹은 제품 유형과 브라우저 사용 맥락을 함께 판단한다. |
| 실제 제품 사례 | 정보 구조와 사용자 흐름을 비교할 때 | Mobbin 등에서 확인한 화면·상태·흐름의 관찰 결과와 우리 제품에 맞게 바꿀 이유. |
| 컴포넌트 구현 자료 | 재사용 단위와 상태를 설계할 때 | 현재 코드의 컴포넌트를 우선 조사하고, 필요할 때 daisyUI 같은 라이브러리의 이름·변형·상태를 참고한다. daisyUI는 Tailwind 기반 컴포넌트 클래스 라이브러리이며 디자인 기준 자체를 대신하지 않는다. |
| 아이콘·모션 자료 | 기능 의미와 상호작용이 정해진 뒤 | 아래 후보 목록에서 시각 일관성·동작 목적·기술 적합성을 확인한다. 후보를 나열했다는 이유만으로 설치하거나 혼용하지 않는다. |

선택한 기준은 화면 구조·상태·반응형·접근성·구현 조건으로 번역한다. `DESIGN.md` 작성 요청이 있으면 `design-system-curator`의 [DESIGN.md 작성 기준](../../design-system-curator/references/design_md_playbook.md)에 연결하고, 실제 구현과 대조해 적용 가능성을 확인한다.

## 아이콘 참고 정보

먼저 제품에 이미 쓰인 아이콘 세트를 확인한다. 새 세트가 필요하면 한 화면과 주요 상태에서 획 두께, 크기, 채움/윤곽 스타일, 은유의 명확성, 플랫폼 관습, 프레임워크 지원을 비교한다. 접근 가능한 이름이 필요한 아이콘 버튼과 장식용 아이콘의 처리를 구분하고, 선택한 컬렉션의 라이선스를 확인한다. 기본 세트 하나를 정하고 예외는 이유를 남긴다.

| 후보 | 살펴볼 이유 | 공식 자료 |
|---|---|---|
| Heroicons | 윤곽선·채움 스타일을 비교할 때 | https://heroicons.com/ |
| Phosphor | 다양한 굵기와 채움 표현이 필요할 때 | https://phosphoricons.com/ |
| Tabler Icons | 넓은 아이콘 목록에서 기능 은유를 찾을 때 | https://tabler.io/icons |
| Iconify | 여러 컬렉션을 탐색할 때. 실제 채택할 컬렉션의 라이선스와 시각 일관성을 별도로 확인한다. | https://iconify.design/ |
| Lucide | 단순한 선형 아이콘 체계를 검토할 때 | https://lucide.dev/ |

## 모션 참고 정보

모션은 상태 변화, 공간 관계, 피드백을 이해하는 데 필요한지 먼저 판단한다. 지속 시간·완급·반복·축소 동작 설정을 화면 및 컴포넌트 규칙에 남긴다. 라이브러리는 구현 환경과 필요한 상호작용이 확인된 뒤 선택한다.

| 후보 | 살펴볼 상황 | 공식 자료 |
|---|---|---|
| Anime.js | 타임라인, SVG, 스크롤과 연결된 연출을 검토할 때 | https://animejs.com/documentation/ |
| Motion | React·JavaScript·Vue 환경의 상태 전환, 제스처, 레이아웃 애니메이션을 검토할 때 | https://motion.dev/docs |

## 실무 레퍼런스 사이트별 사용법
| 사이트 | 먼저 쓰는 상황 | 분석할 것 | 주의할 것 |
|---|---|---|---|
| Mobbin | SaaS, 관리자 페이지, dashboard, 앱 UI, 로그인/회원가입/결제/설정/프로필 같은 UX flow 분석 | 실제 서비스 화면의 flow 순서, navigation, form 단계, paywall, settings, profile, empty/error state | 화면을 그대로 복제하지 말고 서비스 도메인, 권한, 데이터 밀도, 플랫폼 관습 차이를 분리한다. |
| Awwwards | 기업 홈페이지, 브랜드 사이트, 랜딩페이지, 인터랙션 중심 웹 | hero 연출, scroll interaction, motion timing, visual storytelling, brand memory | 업무 화면, admin, 반복 사용 UI에는 과한 motion과 장식을 그대로 가져오지 않는다. |
| Dribbble | UI 스타일, 컬러, 컴포넌트, 아이콘, 카드, dashboard visual treatment | 버튼/카드/배지/아이콘 스타일, color pairing, illustration tone, component polish | 단일 shot은 실제 flow, 상태, 반응형, 접근성이 빠질 수 있으므로 시스템 기준으로 재검증한다. |
| Behance | UX process, 포트폴리오, 브랜딩, 디자인 시스템, case study | 문제 정의, 리서치, IA, 디자인 시스템, 브랜드 확장, before/after rationale | 발표용 서사와 실제 제품 제약을 구분하고, 근거 없는 장식적 프로세스를 그대로 따르지 않는다. |
| Land-book | SaaS, AI 서비스, 스타트업, 기업 홈페이지, 마케팅 랜딩페이지 | hero message, product shot, social proof, pricing, CTA rhythm, industry pattern | 랜딩의 marketing rhythm을 앱 내부 화면이나 운영툴에 가져오지 않는다. |

## 플랫폼별 1차 기준
| 플랫폼/표면 | 먼저 볼 기준 | 레퍼런스 후보 | 참고할 포인트 |
|---|---|---|---|
| iOS 앱 | Apple HIG | https://developer.apple.com/design/human-interface-guidelines/ | navigation, sheet, safe area, gesture, permission, system component |
| Android 앱 | Material Design 3 | https://m3.material.io/ | navigation bar/rail, FAB, snackbar, bottom sheet, adaptive layout |
| 크로스플랫폼 앱 | Apple HIG + Material 3 + 실제 앱 패턴 | https://mobbin.com/ | 공통 IA와 플랫폼별 차이, onboarding, paywall, settings, profile |
| 로그인 후 고객용 홈 | 실제 고객 포털·웹 앱 흐름 + 현재 제품 화면 | https://mobbin.com/ | 고객이 관리하는 대상의 현재 상태, 대표 작업 진입, 최근 변경, 도움이 필요한 상태. 운영용 목록은 필요한 깊이에 배치 |
| 모바일 플로우 | 실제 앱 화면/흐름 | https://pageflows.com/ | signup, checkout, subscription, search, cancellation, notification flow |
| 웹 앱/SaaS | 실제 SaaS 제품 + component library + UX flow reference | https://mobbin.com/, https://www.radix-ui.com/, https://ui.shadcn.com/ | dashboard, form, dialog, table, settings, billing, onboarding, empty/error state |
| 관리자/운영툴 | enterprise design system + 실제 admin flow | https://mobbin.com/, https://ant.design/, https://atlassian.design/, https://carbondesignsystem.com/ | table, filter, batch action, status, permission, audit-friendly layout |
| 대시보드/데이터 | enterprise system + chart guideline + 실제 dashboard 사례 | https://mobbin.com/, https://carbondesignsystem.com/, https://atlassian.design/ | KPI, filter scope, chart/table pairing, data density, empty state |
| 랜딩/마케팅 웹 | 공개 웹 갤러리 + 실제 제품 사이트 | https://land-book.com/, https://www.awwwards.com/, https://www.landingfolio.com/, https://www.siteinspire.com/ | hero, proof, CTA, pricing, trust signal, section rhythm |
| 브랜드/에디토리얼 웹 | visual inspiration gallery + case study | https://www.awwwards.com/, https://www.behance.net/, https://www.siteinspire.com/, https://recent.design/ | editorial rhythm, typography, image treatment, interaction, brand memory |
| Microsoft/업무 생태계 | Fluent 2 | https://fluent2.microsoft.design/ | web/iOS/Android/Windows component consistency, accessibility tooling |

## 서비스 형태별 분기 기준
| 서비스 형태 | 먼저 볼 구조 | 피할 자동 수렴 |
|---|---|---|
| 커머스/예약 | 탐색, 비교, 조건 확인, 결제 신뢰, 취소/환불 흐름 | 상품/예약 단위를 모두 같은 정보 카드로만 나열 |
| 콘텐츠/미디어 | 읽기 흐름, 편집 리듬, 추천, 저장, 공유 | 대시보드 KPI처럼 콘텐츠를 요약 카드로만 처리 |
| 커뮤니티/소셜 | 작성, 반응, 알림, 신뢰/신고, 관계 맥락 | 정적 리스트와 관리자형 필터만 강조 |
| 생산성/협업 | 작업 상태, 소유자, 변경 이력, 빠른 입력, 단축 경로 | 랜딩식 hero나 과한 브랜드 장식 |
| AI/자동화 도구 | 입력 의도, 실행 상태, 검토/수정, 로그, 실패 복구 | 결과만 보여주고 제어권과 검증 경로를 숨김 |
| 금융/부동산/건강 | 신뢰, 근거, 위험 표시, 비교, 결정 보류 | 친근한 카드 UI로 위험 정보를 약하게 표현 |
| 교육/학습 | 단계, 피드백, 복습, 성취, 집중 모드 | 관리자 대시보드처럼 학습 경험을 차갑게 표현 |
| 엔터테인먼트/게임 | 몰입, 즉각 피드백, 진행감, 시각적 기억점 | 업무툴처럼 지나치게 절제된 중립 화면 |

## 웹 작업 레퍼런스 선택
### 로그인 후 고객용 홈
- 먼저 고객이 들어와서 확인할 제품 대상과 바로 실행할 행동을 정한다. 이번에 제공하는 기능과 이후 확장할 기능을 구분한다.
- 참고 후보: 실제 고객용 웹 앱의 홈, Mobbin의 유사 흐름, 현재 제품의 화면과 브랜드 자산.
- 볼 것: 현재 상태나 결과의 표현, 작업 진입, 최근 변경, 도움·오류 복구, 상세 관리 화면으로 내려가는 경로.
- 피할 것: 고객의 첫 화면을 내부 운영자의 전체 현황 표와 필터로 시작하거나, 소개용 랜딩의 메시지를 로그인 후 작업 화면에 그대로 적용하는 것.

### SaaS / Web App
- 참고 후보: Mobbin, Land-book, Radix UI, shadcn/ui, Atlassian Design, Ant Design, 실제 SaaS 제품의 공개 화면
- 볼 것: side navigation, top bar, command/search, settings, billing, team management, empty state, loading skeleton
- 피할 것: 랜딩 페이지의 과한 hero나 시각 효과를 업무 화면에 그대로 가져오는 것

### Dashboard / Analytics
- 참고 후보: Mobbin, Carbon Design System, Atlassian Design, Ant Design Charts, 실제 analytics 제품 공개 데모
- 볼 것: KPI card, chart + table pairing, filter scope, date range, drill-down, annotation, data freshness
- 피할 것: 차트 종류만 화려하고 지표 정의, 기간, 단위, 비교 기준이 없는 화면

### Admin / Internal Tool
- 참고 후보: Mobbin, Ant Design, Atlassian Design, Carbon, Polaris
- 볼 것: table density, bulk action, status badge, permission, audit trail, destructive action confirmation
- 피할 것: 모든 항목을 카드로 만들거나 운영자가 반복 처리해야 할 작업을 모달 안에 숨기는 것

### Landing / Marketing
- 참고 후보: Land-book, Awwwards, Landingfolio, Siteinspire, Framer Gallery
- 볼 것: hero message, product shot, proof, pricing, FAQ, CTA repetition, section rhythm
- 피할 것: 브랜드 분위기만 강하고 제품 사용 상태나 전환 행동이 보이지 않는 화면

### Branding / Portfolio / Case Study
- 참고 후보: Behance, Awwwards, Dribbble
- 볼 것: brand system extension, typography, visual identity, icon style, process rationale, before/after
- 피할 것: 포트폴리오용 표현을 실제 사용 빈도가 높은 제품 화면에 그대로 적용하는 것

### Component / Visual Polish
- 참고 후보: Dribbble, Mobbin, 디자인 시스템 문서
- 볼 것: button hierarchy, card rhythm, icon metaphor, color pairing, state treatment, density
- 피할 것: 단일 컴포넌트 shot을 상태 matrix 없이 시스템 규칙으로 승격하는 것

## 앱 작업 레퍼런스 선택
### iOS
- 참고 후보: Apple HIG, Mobbin iOS screens, Pageflows mobile flow
- 볼 것: tab bar, navigation stack, sheet detent, action sheet, permission prompt, onboarding, paywall
- 피할 것: Android FAB이나 system back 전제를 iOS에 그대로 가져오는 것

### Android
- 참고 후보: Material Design 3, Mobbin Android screens, Pageflows mobile flow
- 볼 것: top app bar, navigation bar/rail, FAB, snackbar, bottom sheet, system back, adaptive layout
- 피할 것: iOS modal/navigation 관습을 Android back behavior와 충돌하게 만드는 것

### Cross-platform
- 참고 후보: Apple HIG, Material 3, Fluent 2, Mobbin, Pageflows
- 볼 것: 공통 IA, 플랫폼별 picker/permission/share, typography 차이, navigation 차이, dark mode
- 피할 것: 한 플랫폼의 component look을 모든 플랫폼에 통일하는 것

## 레퍼런스 기록 템플릿
| 항목 | 내용 |
|---|---|
| 레퍼런스 이름/URL | |
| 기록 수준 | L0 외부 없음, L1 사이트 성격만 참고, L2 검색 기반, L3 결정 매핑 |
| 검색어/탐색 경로 | |
| 기준일/접근 범위 | |
| 적용 플랫폼 | Web, iOS, Android, Cross-platform 등 |
| 참고할 요소 | navigation, layout, component, flow, copy, visual tone 등 |
| 그대로 쓰면 안 되는 이유 | 도메인 차이, 데이터 밀도, 브랜드 차이, 구현 비용 등 |
| 우리 작업에 반영할 원칙 | |
| 보류할 요소 | |

상세 기록은 `reference_evidence_log.md`를 사용한다.

## 출력 예시
```markdown
레퍼런스 선택:
- Apple HIG: iOS sheet와 permission 요청 타이밍 기준
- Mobbin의 onboarding flow: 단계 수와 progressive disclosure 참고
- Radix UI: 웹 관리자 화면의 dialog, dropdown, form state 참고

반영 원칙:
- iOS에서는 tab bar를 최상위 목적 4개로 제한
- 웹 운영툴은 card grid 대신 table + detail drawer 사용
- 랜딩 hero의 시각 톤은 참고하되, 앱 내부 업무 화면에는 적용하지 않음
```
