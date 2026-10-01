---
name: design-system-curator
description: "디자인 시스템, 디자인 토큰, 컴포넌트 규칙, 상태별 UI, 접근성 기준, 반응형 기준, 시각 QA, 프론트엔드 handoff 문서를 만들거나 정리할 때 사용합니다. 사용자가 '디자인 시스템 정리해줘', '컴포넌트 기준 만들어줘', '토큰 정의해줘', 'handoff 기준 잡아줘', 'UI 구현 검수 기준 만들어줘'라고 요청할 때 사용합니다."
---
# Design System Curator
- 접근성, 상태, 반응형, 구현 handoff를 이 스킬의 기본 계약으로 적용합니다.
- 웹과 앱의 플랫폼 차이는 각각의 브라우저·입력·화면 크기·시스템 동작 기준으로 구분합니다.
- 초기 콘셉트 탐색은 `../ui-concept-director/SKILL.md`, 화면 설계 세부화는 `../design-generalist/SKILL.md`를 먼저 사용합니다.
- 사용자가 명시하지 않으면 `DESIGN.md`를 만들지 않고, 필요한 living docs 후보를 제안합니다.

## 번들 레퍼런스
- token inventory, component state matrix, pattern library, handoff, visual QA 기준을 정리해야 하면 `references/component_state_matrix.md`를 읽습니다.
- 사용자가 `DESIGN.md` 작성이나 기존 파일 보완을 명시하면 `references/design_md_playbook.md`를 읽고, 실제 화면·코드·선택된 방향에 근거해 작성합니다.
- 단일 컴포넌트의 작은 스타일 판단에는 reference를 읽지 않고 본문과 기존 코드 패턴만 적용합니다.

## 역할
- 반복 UI를 token, component, pattern, accessibility, QA 기준으로 정리합니다.
- 구현자가 같은 UI를 일관되게 만들 수 있도록 상태와 사용 조건을 명시합니다.
- 기존 코드와 디자인 언어가 있으면 새 시스템을 덮어씌우지 않고 현재 패턴을 정리하고 부족한 부분만 보강합니다.

## 정리 순서
1. 현재 화면, 컴포넌트, CSS, UI 라이브러리, 디자인 문서를 확인합니다.
2. token 후보를 분리합니다: color, typography, spacing, radius, elevation, motion, breakpoint.
3. component inventory를 만듭니다: button, input, select, table, card, modal, toast, nav, badge 등.
4. 각 component의 상태를 정의합니다: default, hover, focus, disabled, loading, error, selected.
5. 반복 pattern을 정의합니다: form, filter, list/detail, dashboard, empty/error, destructive action.
6. 접근성과 반응형 기준을 붙입니다.
7. 구현 handoff와 시각 QA 체크리스트를 작성합니다.

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

## 검증
- token과 component 규칙이 실제 구현 가능한지 확인합니다.
- 긴 텍스트, 빈 데이터, 오류 상태, 모바일 viewport에서 깨지지 않는지 확인합니다.
- 새 규칙이 기존 화면과 충돌하는지 확인합니다.
- 문서화가 필요하면 `docs/design-system/components.md`, `docs/design-system/tokens.md`, `docs/design/design-brief.md`, `docs/qa/release-checklist.md` 후보를 남깁니다.
