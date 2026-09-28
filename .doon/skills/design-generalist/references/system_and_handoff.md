# System And Handoff

## Token Layers

- 최소한 아래 계층은 분리해서 사고합니다.
  - color
  - typography
  - spacing
  - radius
  - shadow
  - motion
- token은 화면 단위 값이 아니라 시스템 단위 규칙이어야 합니다.
- 색상은 역할 기준으로 이름 붙입니다.
  - 예: `surface`, `surface-muted`, `text-primary`, `accent`, `danger`

## Component Rules

- 주요 컴포넌트는 variant와 state를 함께 정의합니다.
  - 기본/강조/보조
  - default/hover/focus/active/disabled/loading/error
- 컴포넌트 설명은 외형보다 역할 중심으로 씁니다.
  - 어떤 상황에 쓰는지
  - 어떤 우선순위를 가지는지
  - 어떤 상태를 반드시 지원해야 하는지
- form control은 helper text, validation, success/error message, keyboard focus를 기본으로 포함합니다.

## Layout Rules

- 8px 또는 4px 계열 spacing rhythm처럼 일관된 간격 체계를 정합니다.
- 콘텐츠 폭, grid column, section spacing, card padding을 서로 연결된 규칙으로 둡니다.
- dense 화면과 spacious 화면을 섞을 때는 의도된 레벨 차이로 보이게 해야지, 제각각처럼 보이면 안 됩니다.

## Content And Data

- copy는 의도와 행동을 분명하게 써야 합니다.
- 비어 있는 Lorem Ipsum보다 현실적인 label, value, warning copy를 넣는 편이 검토 품질이 높습니다.
- 숫자, 날짜, 상태값이 중요한 제품이라면 formatting rule까지 같이 정의합니다.

## Handoff Output

- 구현팀에 넘길 때는 아래 항목을 우선 제공합니다.
  - design goal
  - reference evidence when external references shaped decisions
  - layout summary
  - token or variable naming
  - component inventory
  - state matrix
  - responsive rule
  - accessibility note
- 프론트엔드 산출물이 포함되면 CSS variable, breakpoint, state class, spacing scale을 코드에 드러냅니다.
- acceptance criteria는 "예뻐 보인다"가 아니라 관찰 가능한 동작 기준으로 씁니다.
- 레퍼런스 기반 handoff는 검색어/URL/title을 장식처럼 나열하지 말고, 어떤 관찰이 어떤 layout, component, copy, motion 결정으로 이어졌는지 연결합니다.
