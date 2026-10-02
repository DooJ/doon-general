---
name: design-system-curator
description: "디자인 시스템, DESIGN.md, 시각 디자인 가이드, 디자인 토큰, 컴포넌트 규칙, 상태별 UI, 접근성·반응형·시각 QA와 프론트엔드 handoff를 만들거나 정리할 때 사용합니다. 사용자가 '디자인 시스템 정리해줘', '디자인 가이드 보여줘', '컴포넌트 기준 만들어줘', '토큰 정의해줘', 'UI 구현 검수 기준 만들어줘'라고 요청할 때 사용합니다."
---
# Design System Curator
- 접근성, 상태, 반응형, 구현 handoff를 이 스킬의 기본 계약으로 적용합니다.
- 웹과 앱의 플랫폼 차이는 각각의 브라우저·입력·화면 크기·시스템 동작 기준으로 구분합니다.
- 초기 콘셉트 탐색은 `../ui-concept-director/SKILL.md`, 화면 설계 세부화는 `../design-generalist/SKILL.md`를 먼저 사용합니다.
- 사용자가 명시하지 않으면 `DESIGN.md`를 만들지 않고, 필요한 living docs 후보를 제안합니다.
- 사용자가 웹 디자인 가이드를 요청하면 문서만 요청한 경우를 제외하고 브라우저에서 열리는 컴포넌트 가이드를 기본 산출물로 만듭니다. 앱은 해당 플랫폼의 렌더링 가능한 미리보기나 컴포넌트 카탈로그를 선택합니다.
- `DESIGN.md`의 텍스트 규칙, 작업 흐름을 설명하는 디자인 가이드 문서, 시각 컴포넌트 가이드는 서로 역할이 다릅니다. 하나를 만들었다는 이유로 요청된 다른 산출물을 생략하지 않습니다.

## 번들 레퍼런스
- token inventory, component state matrix, pattern library, handoff, visual QA 기준을 정리해야 하면 `references/component_state_matrix.md`를 읽습니다.
- 사용자가 `DESIGN.md` 작성이나 기존 파일 보완을 명시하면 `references/design_md_playbook.md`를 읽고, 실제 화면·코드·선택된 방향에 근거해 작성합니다.
- 시각 디자인 가이드, 컴포넌트 전시 화면, HTML/Storybook 가이드를 요청하면 `references/visual_design_guide_playbook.md`를 읽습니다.
- 단일 컴포넌트의 작은 스타일 판단에는 reference를 읽지 않고 본문과 기존 코드 패턴만 적용합니다.

## 역할
- 반복 UI를 token, component, pattern, accessibility, QA 기준으로 정리합니다.
- 구현자가 같은 UI를 일관되게 만들 수 있도록 상태와 사용 조건을 명시합니다.
- 기존 코드와 디자인 언어가 있으면 새 시스템을 덮어씌우지 않고 현재 패턴을 정리하고 부족한 부분만 보강합니다.

## 정리 순서
1. 사용자가 원하는 산출물을 구분합니다: 결정 기준 문서(`DESIGN.md`), 상세 사용 규칙, 눈으로 비교할 수 있는 가이드. 기존 제품은 현재 화면·브랜드 자산·컴포넌트·CSS·기존 문서를 확인하고, 신규 제품은 선택된 콘셉트와 확정·미정 항목을 확인합니다.
2. token 후보를 분리합니다: color, typography, spacing, radius, elevation, motion, breakpoint.
3. component inventory를 만듭니다: button, input, select, table, card, modal, toast, nav, badge 등.
4. 각 component의 상태를 정의합니다: default, hover, focus, disabled, loading, error, selected.
5. 반복 pattern을 정의합니다: form, filter, list/detail, dashboard, empty/error, destructive action.
6. 접근성과 반응형 기준을 붙입니다.
7. 시각 가이드가 범위에 있으면 승인된 자산·토큰·제품 스타일과 실제 쓰는 컴포넌트의 주요 상태를 렌더링합니다. 신규 제품에서 확정되지 않은 값은 후보로 표시하고, 예시를 채우려고 쓰지 않는 컴포넌트나 없는 로고를 만들지 않습니다. 구현된 상태와 향후 계약을 구분합니다.
8. 구현 handoff와 시각 QA 체크리스트를 작성하고 문서·가이드·제품 화면을 서로 연결합니다.

## 산출물 기준
- 디자인 원칙
- token 목록
- component inventory
- component state matrix
- pattern library
- 접근성 기준
- responsive rule
- 구현 handoff
- visual QA checklist
- 시각 가이드 요청 시 브라우저나 해당 플랫폼에서 직접 볼 수 있는 관련 컴포넌트 예시, 접근 경로와 미리보기

## 검증
- token과 component 규칙이 실제 구현 가능한지 확인합니다.
- 긴 텍스트, 빈 데이터, 오류 상태, 모바일 viewport에서 깨지지 않는지 확인합니다.
- 새 규칙이 기존 화면과 충돌하는지 확인합니다.
- 시각 가이드는 실제 렌더링을 데스크톱과 좁은 화면에서 확인하고, 존재하는 로고·확정된 색상·간격·상태가 기준 문서 및 제품 화면과 일치하는지 대조합니다. 신규 제품의 후보 값은 미확정 표시를 확인합니다. Markdown 표만으로 시각 가이드 요청을 완료로 보지 않습니다.
- 문서화가 필요하면 `docs/design-system/components.md`, `docs/design-system/tokens.md`, `docs/design/design-brief.md`, `docs/qa/release-checklist.md` 후보를 남깁니다.
