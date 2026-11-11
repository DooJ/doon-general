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

## 개발 착수용 화면 시안

- 앱 코드 작성 전에 화면 ID를 기준으로 주요 사용자·관리자 화면, 이동·입력·결과와 중요한 예외 상태의 실제 배치를 보여 주는 산출물을 준비한다. 작은 MVP는 로컬에서 열리는 HTML 한 파일 또는 주석 와이어프레임으로 통합할 수 있다. 구현과 구분되는 시안 경로에 저장하고 디자인 문서에서 연결한다.
- 가이드에는 가시성·반응형·접근성 규칙을, 시안에는 실제 화면 배치를 담는다. 시안을 열어 볼 수 있고 이번 UI 범위를 대표하는지 확인한 다음 구현으로 넘긴다. 앱 렌더와 최종 시안 검수는 해당 단계에서 별도로 기록한다.
- 아래 에셋 목록을 구현 전 작성한다. 기존 아이콘·시스템 폰트·CSS 등으로 충분하면 사용할 자원과 추가 파일이 필요 없는 이유를 목록에 적는다. 새 에셋이 필요한 경우 사용 화면과 준비 상태를 표시한다.

## 최종 화면 시안

- 이번 구현 범위의 화면 ID별로 필요한 상태(기본·로딩·빈·오류·성공·권한 부족 중 해당 항목)와 지원 기기·화면 크기, 사용 목적이나 권한에 따라 달라지는 변형을 정한다. 동작과 레이아웃이 같은 부분은 공통 컴포넌트·시안으로 재사용한다.
- 디자인 문서에 가이드와 함께 화면 시안의 편집 가능한 정본·열람 위치, 초안/확정/후속 상태, 필요한 변형을 남긴다. 최종으로 표시하기 전에 해당 시안을 열어 화면·상태·화면 크기의 일치 여부와 주요 이동·복구를 확인한다. 아직 정하지 않은 부분은 이유와 구현에 미치는 영향을 남긴다.

## 디자인 에셋 인도

- 구현에 실제로 필요한 로고·아이콘·이미지·폰트·모션만 목록에 넣는다. 각 항목에 이름 또는 ID, 사용 화면·컴포넌트, 원본 위치, 전달 파일 또는 재사용 경로, 포맷·치수/배율(해당 시), 출처·사용 조건을 기록한다.
- 새로 인도하는 파일은 프로젝트의 기존 자산 위치와 이름 규칙을 사용한다. 기존 라이브러리나 시스템 폰트는 정확한 식별자와 참조를 남긴다. 전달 전에 파일 또는 링크를 열 수 있는지, 필요한 변형을 사용할 수 있는지 확인하고 미확정·누락 항목은 표시한다.
- 작은 작업은 디자인 문서에 표를 넣고, 재사용 자산이 많아 별도로 관리할 때는 에셋 목록의 정본을 링크한다.

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
- 제품 화면만 렌더링한 결과는 재사용 가능한 디자인 가이드와 다릅니다. 사용자가 시스템화를 요청하면 `design-system-curator`에 넘겨 `DESIGN.md`의 결정·토큰, 상세 가이드의 치수·상태, 브라우저/플랫폼에서 볼 수 있는 컴포넌트 예시를 서로 연결합니다. 구체적인 전시 항목과 QA는 그 스킬의 `references/visual_design_guide_playbook.md`를 따릅니다.
