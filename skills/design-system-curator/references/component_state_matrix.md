# Component State Matrix

디자인 시스템, 컴포넌트 기준, 토큰, handoff, visual QA 기준을 만들 때 사용한다. 기존 UI를 정리하거나 새 컴포넌트 패턴을 정의할 때 읽는다.

## 1. Token Inventory

| 토큰 | 현재 값 | 사용 위치 | 역할 | 변경 위험 | 후보 이름 |
|---|---|---|---|---|---|
| color.primary |  |  | action/brand/status | high/medium/low |  |
| typography.body |  |  |  |  |  |
| spacing.4 |  |  |  |  |  |
| radius.sm |  |  |  |  |  |

토큰 기준:

- 이름은 값이 아니라 역할을 표현한다.
- 색상은 brand, surface, text, border, action, status로 분리한다.
- spacing과 radius는 화면마다 새 값을 만들기 전에 기존 scale에 맞춘다.
- Dribbble이나 Behance에서 본 색감/카드/아이콘 스타일은 바로 토큰으로 승격하지 말고 실제 component state, 접근성, 브랜드 역할을 통과한 뒤 이름 붙인다.

## 2. Component Inventory

| 컴포넌트 | 용도 | 변형 | 필수 상태 | 접근성 | 구현 위치 | 문서화 우선순위 |
|---|---|---|---|---|---|---|
| Button | 주요 행동 | primary/secondary/danger/icon | default/hover/focus/disabled/loading | name, focus |  | P0 |

## 3. State Matrix

| 컴포넌트 | Default | Hover | Focus | Disabled | Loading | Error | Selected | Empty |
|---|---|---|---|---|---|---|---|---|
| Button |  |  |  |  |  | n/a | n/a | n/a |
| Input |  |  |  |  | n/a |  | n/a | n/a |
| Table |  | row hover | focus row/control |  | skeleton | error row/state | selected row | empty state |

상태 정의 기준:

- focus는 hover와 별도로 키보드 사용자가 볼 수 있어야 한다.
- disabled는 왜 비활성인지 필요할 때 설명할 수 있어야 한다.
- loading은 layout shift를 만들지 않아야 한다.
- error는 색상만으로 전달하지 않는다.

## 4. Pattern Library

| 패턴 | 포함 컴포넌트 | 사용 상황 | 금지 상황 | QA 포인트 |
|---|---|---|---|---|
| Form | input, select, validation, submit | 데이터 입력 | 단순 확인 화면 | validation, keyboard, error |
| Filter table | filter, table, pagination, bulk action | 반복 업무 | 항목 수가 매우 적음 | default sort, empty result |
| Destructive action | confirm/undo/toast/log | 삭제/발송/결제 | 복구 쉬운 단순 변경 | 영향 범위, 권한 |

레퍼런스 사용 기준:

- Mobbin에서 본 flow는 onboarding, settings, billing, profile 같은 pattern 후보로 분해한다.
- Land-book과 Awwwards에서 본 landing/brand interaction은 제품 내부 component 규칙과 분리한다.
- Dribbble의 component shot은 state matrix와 responsive QA를 통과할 때만 reusable component 기준으로 삼는다.
- Behance의 design system case study는 inventory와 naming 참고로 쓰되, 현재 코드와 충돌하는 새 체계를 무리하게 도입하지 않는다.

## 5. Handoff 기준

- 컴포넌트 이름, variant, state, responsive rule을 함께 남긴다.
- 데이터 길이, 빈 값, 오류, 권한 부족, 모바일 viewport 사례를 포함한다.
- 디자인 의도와 구현 제약이 충돌하면 어느 쪽을 우선할지 명시한다.
- 새 규칙이 기존 화면과 충돌하면 migration 범위와 예외를 분리한다.

## 시각 예시로 옮길 때

아래 항목은 고정 체크리스트가 아니라 제품에서 실제 쓰는 컴포넌트를 골라 전시할 때의 기준이다. 승인된 로고나 자산이 없으면 임의로 만들지 않고 미정 또는 후보로 표시한다. 목록·폼·첨부 등이 제품에 없으면 해당 행을 생략한다.

| 영역 | 최소한 눈으로 보여줄 것 | 실제 동작 확인 |
|---|---|---|
| 브랜드 | 승인된 로고의 밝은/어두운 배경 사용, 핵심 색상 견본 | 로고 파일 로드, 색상 값과 사용 역할 |
| 타이포그래피 | 대표 제목, 페이지·섹션·카드 제목, 본문·메타 | 긴 이름의 줄바꿈, 모바일 크기 |
| 버튼·링크 | primary/secondary/text와 hover/focus/disabled/loading | 키보드 focus, 최소 터치 영역, 중복 제출 방지 |
| 카드·목록 | 기본/hover/선택, 미리보기·본문·상태·메타의 순서 | 선택 표시, 검색 결과 없음, 다수 항목 스크롤 |
| 폼·피드백 | 라벨·도움말·입력·오류, 첨부, 성공/실패 | 오류 문구, 파일명, 로딩/실패 단계 |

시각 가이드는 확정된 제품 토큰과 자산을 공유하거나 후보 값의 근거·미확정 상태를 명시한다. 예시 화면의 동작과 아직 구현되지 않은 계약을 구분하고, 가이드 링크와 스크린샷을 handoff에 포함한다. 자세한 제작 절차는 [시각 디자인 가이드 제작 기준](./visual_design_guide_playbook.md)을 따른다.

## 6. Visual QA

| 항목 | 확인 |
|---|---|
| 긴 텍스트 | 말줄임, 줄바꿈, 높이 확장 기준 |
| 좁은 화면 | navigation, table, modal, toolbar 재배치 |
| 상태 | loading, empty, error, success, disabled |
| 접근성 | contrast, focus, keyboard, label |
| 데이터 | 0개, 1개, 많은 항목, 권한별 차이 |
