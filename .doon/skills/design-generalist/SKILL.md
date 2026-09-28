---
name: "design-generalist"
description: "선택된 제품 디자인 방향을 화면 구조, 시각 위계, 반응형, 접근성, 구현 handoff로 구체화하거나 기존 UI를 종합 리뷰할 때 사용하는 범용 디자인 스킬입니다. 초기 콘셉트 탐색은 ui-concept-director를 우선합니다. IA 전용, 상태 전이 전용, 디자인 시스템 전용 요청은 제외하고 각각 information-architect, interaction-designer, design-system-curator로 라우팅합니다."
---

# Design Generalist

- 모든 디자인 작업은 `.doon/rules/04_design_rules.md`를 기본으로 적용합니다.
- 브라우저 기반 웹 앱, SaaS, 대시보드, 관리자 도구, 랜딩, 콘텐츠 사이트 작업이면 `.doon/rules/05_web_design_rules.md`를 추가로 적용합니다.
- iOS, Android, cross-platform, mobile web, tablet 앱 작업이면 `.doon/rules/06_app_design_rules.md`를 추가로 적용합니다.
- 기존 제품, 코드베이스, 브랜드 자산이 있으면 새로운 취향을 덮어씌우지 말고 현재 언어를 읽고 확장합니다.
- 사용자가 단순히 "예쁘게"를 원하더라도 목표, 사용자, 제약, 상태, 접근성, 구현 가능성을 먼저 정리합니다.
- 사용자가 화면 목적만 말하고 "대략 먼저 만들어봐", "참고 디자인을 골라줘", "포지션을 바꾸며 맞춰가자"처럼 초기 시안 탐색을 원하면 `../ui-concept-director/SKILL.md`를 먼저 사용합니다.
- 디자인 방향을 정할 때는 표면 유형뿐 아니라 서비스 도메인, 감정 톤, 사용 빈도, 사용자 숙련도, 콘텐츠/데이터 밀도를 함께 분류합니다.
- 사용자가 별도 레퍼런스를 주지 않았더라도 모든 산출물을 같은 카드형 SaaS/대시보드 미감으로 수렴시키지 않습니다.
- 레퍼런스가 필요한 작업은 `references/platform_reference_matrix.md`에서 Mobbin, Awwwards, Dribbble, Behance, Land-book 같은 사이트를 표면 유형과 목적에 맞게 고르고, `무엇을 참고할지`와 `그대로 가져오면 안 되는 것`을 함께 남깁니다.
- 레퍼런스를 실제로 검색하거나 열람해 디자인을 만든 경우 `references/reference_evidence_log.md` 기준으로 검색어, URL/title, 관찰 요소, 반영한 결정, 버린 요소를 기록합니다.
- 디자인 산출물이 코드 구현으로 이어질 가능성이 있으면 spacing, type scale, component state, responsive behavior까지 함께 설계합니다.
- 화면 개선 작업에서는 가능하면 현재 화면, 스크린샷, CSS/컴포넌트 구조, 실제 데이터 밀도를 먼저 확인합니다.
- 1차 UI와 기능 구현 이후 별도 리뷰 스튜디오에서 기준본·수정안·최종 통합본·실제 구현을 끝까지 비교하는 작업이면 `../refining-implemented-ui/SKILL.md`를 우선하고, 이 스킬은 세부 디자인 판단과 handoff 렌즈로 사용합니다.
- `DESIGN.md` 같은 디자인 시스템 파일 생성은 사용자가 명시적으로 요청했을 때만 별도 작업으로 다룹니다.

## 이 스킬이 맞는 요청

- 웹 앱, 모바일 앱, SaaS 대시보드, 랜딩 페이지, 내부 운영툴, 마케팅 페이지, 브랜딩 요소를 설계하거나 개선할 때
- 기존 화면이나 제품의 UX/UI를 리뷰하고 구조적 문제와 개선 방향을 짚을 때
- 화면 설계에 필요한 component state, layout principle, interaction pattern을 종합 handoff로 정리할 때
- 디자이너 없이도 구현 가능한 수준의 화면 가이드나 프론트엔드 디자인 브리프가 필요할 때
- 이미 선택된 콘셉트나 첫 시안을 더 구체적인 규칙, 상태, 반응형, 구현 handoff로 다듬을 때

## 제외 및 전문 스킬 우선

- 사이트맵, navigation, 검색/필터 같은 IA만 필요하면 `information-architect`를 사용합니다.
- 상태 전이, 오류 복구, 입력 피드백만 필요하면 `interaction-designer`를 사용합니다.
- token, component governance, versioning, visual regression처럼 디자인 시스템 자체가 목적이면 `design-system-curator`를 사용합니다.

## 작업 모드 선택

1. `Direction`: 문제 정의, 대상 사용자, 톤, 핵심 메시지, 시각적 방향을 잡습니다.
2. `Structure`: 정보 구조, user flow, navigation, layout hierarchy를 정리합니다.
3. `Interface`: token, component, density, motion, state 규칙을 구체화합니다.
4. `Review`: 기존 디자인을 진단하고 우선순위가 있는 개선안을 제시합니다.
5. `Handoff`: 구현 가이드, acceptance criteria, responsive rule까지 정리합니다.

- 요청이 모호하면 greenfield 작업은 `Direction -> Structure`, 기존 화면 개선은 `Review`, 코드 구현이 포함되면 `Handoff`까지 기본으로 포함합니다.
- 단, 사용자가 아직 콘셉트를 고르지 않았고 "첫 시안", "레퍼런스", "대략적인 화면"을 원하면 `ui-concept-director`의 후보 방향과 초안 생성 흐름을 먼저 거친 뒤 이 스킬로 세부화합니다.

## 기본 워크플로우

1. 산출물의 유형을 확정합니다.
   - 화면 설계, redesign, critique, design system, prototype, brand direction 중 무엇인지 먼저 정합니다.
   - 초기 탐색인지, 확정된 방향의 구체화인지 구분합니다.
2. 맥락과 제약을 수집합니다.
   - 대상 사용자, 핵심 태스크, 비즈니스 목표, 브랜드 톤, 사용 환경, 기술 제약, 일정 제약을 확인합니다.
   - 서비스 도메인, 감정 톤, 데이터 밀도, 사용 빈도, 사용자 숙련도를 함께 확인합니다.
3. 기존 자산을 읽습니다.
   - 현재 화면, 컴포넌트, typography, color, copy tone, 데이터 밀도, responsive behavior를 파악합니다.
4. 핵심 디자인 축을 정합니다.
   - 표현 키워드 3개 안팎, 정보 밀도, 강조 방식, 상호작용 톤, 우선순위 구조를 명확히 합니다.
   - 선택한 레퍼런스나 도메인 관습에서 가져올 요소와 버릴 요소를 분리합니다.
   - Mobbin은 실제 UX flow, Awwwards는 브랜드/인터랙션, Dribbble은 컴포넌트 polish, Behance는 프로세스/브랜딩, Land-book은 랜딩 구조처럼 레퍼런스의 용도를 구분합니다.
   - 실제 검색 기반이라면 검색어, 후보 자료, 선택/배제 사유를 `레퍼런스 근거`로 남깁니다.
5. 요청에 맞는 산출물을 작성합니다.
   - 단순 예시보다 실제 구현과 연결되는 layout, state, content hierarchy를 우선합니다.
6. 마지막에 검증합니다.
   - empty/loading/error/success, desktop/mobile 대응, accessibility baseline, handoff 명확성을 점검합니다.
- 구현 산출물이라면 주요 breakpoint와 실제 긴 텍스트, 빈 데이터, 에러 메시지, hover/focus/disabled 상태까지 포함합니다.

## 핵심 원칙

- 장식보다 명확성을 우선합니다.
- 화면 하나보다 시스템 일관성을 우선합니다.
- 시스템 일관성은 동일한 화면 형태의 반복이 아니라 사용자가 예측 가능한 규칙을 유지하는 것입니다.
- 밀도 높은 인터페이스는 무작위 카드 남발보다 grid, grouping, contrast, spacing rhythm으로 정리합니다.
- 카드, hero, sidebar, dashboard, gradient, neutral palette 같은 기본 패턴은 서비스 목적에 맞을 때만 선택합니다.
- 마케팅/브랜딩 표면은 더 대담해질 수 있지만 메시지 위계를 흐리면 안 됩니다.
- 모바일을 데스크톱처럼, 데스크톱을 모바일처럼 다루지 않습니다. 플랫폼 기대치를 존중합니다.
- placeholder보다 현실적인 copy와 데이터 예시를 사용합니다.
- motion은 의미가 있을 때만 사용하고, 상태 변화나 계층 인지를 돕는 쪽에 씁니다.
- 접근성은 후순위가 아니라 기본값입니다.
- CTA, navigation, 필터, 입력 폼, table, card, modal, toast 같은 반복 패턴은 사용자가 이미 아는 관습을 우선합니다.
- 시각적 콘셉트는 사용자 과업을 가리지 않아야 하며, 콘텐츠가 바뀌어도 무너지지 않는 시스템이어야 합니다.

## 출력 규칙

- 가능한 한 아래 순서로 정리합니다.
  - 문제 또는 목표
  - 대상 사용자와 사용 맥락
  - 핵심 디자인 방향 3~5개
  - 화면/플로우/시스템 제안
  - 상태 처리와 responsive 규칙
  - 구현 메모 또는 handoff 포인트
- 리뷰 요청이면 미감 평가보다 문제, 영향, 개선 방향을 먼저 적습니다.
- 코드 기반 산출물이 필요하면 reusable token, CSS variable, layout rule, state naming을 명시합니다.
- 여러 콘셉트를 제안할 때는 색상만 바꾸지 말고 정보 구조, 밀도, 브랜드 태도, interaction posture까지 달라지게 만듭니다.
- 새 서비스나 리디자인 산출물에는 가능하면 `레퍼런스 선택`, `반영할 요소`, `버릴 요소`, `획일화 방지 판단`을 짧게 포함합니다.
- 레퍼런스 이름을 언급할 때는 사이트명만 쓰지 말고 flow, layout, component, visual tone, motion, case study 중 어느 관찰을 가져왔는지 적습니다.
- 레퍼런스를 찾아서 작업한 경우 최종 산출물 또는 handoff에 `레퍼런스 근거`를 포함합니다. 여기에는 검색어/경로, URL 또는 자료명, 관찰한 요소, 반영한 결정, 버린 요소를 짧게 적습니다.
- 실제 화면을 확인하지 않고 사이트의 일반 성격만 참고했다면 `실화면 미확인` 또는 `heuristic`으로 표시합니다.
- 리뷰 결과는 문제, 사용자 영향, 수정 우선순위, 구현 난이도 순으로 정리합니다.
- 구현 handoff는 컴포넌트별 책임, 상태, 반응형 동작, 접근성 요구사항, acceptance criteria를 포함합니다.

## 참고 자료

- 웹 앱, 모바일, 랜딩 페이지, 운영툴 같은 매체별 설계 관점은 `references/surface_patterns.md`를 읽습니다.
- 플랫폼 선택과 샘플 레퍼런스가 필요하면 `references/platform_reference_matrix.md`를 읽습니다.
- 레퍼런스를 검색하거나 특정 자료를 근거로 디자인 결정을 남겨야 하면 `references/reference_evidence_log.md`를 읽습니다.
- token, component, handoff 정리가 필요하면 `references/system_and_handoff.md`를 읽습니다.
- 기존 디자인 리뷰나 진단은 `references/design_review_checklist.md`를 읽습니다.
