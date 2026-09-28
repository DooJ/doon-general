# 리뷰 스튜디오 계약

## 목적

리뷰 스튜디오는 운영 UI를 캡처해 모아두는 갤러리가 아니다. 실제 소스 구조와 데이터 특성을 재현하고, 같은 화면의 기준본·수정안·최종본·실제 구현을 전환하며 결정 이력을 검증하는 별도 작업면이다.

## 인벤토리 순서

1. 저장소 안에서 독립 실행 surface와 UI entry point를 찾는다.
2. 각 surface의 route, sidebar, top navigation, tab, modal, drawer를 수집한다.
3. 화면을 전체 콘셉트와 별도 결정이 필요한 세부 단위로 나눈다.
4. 인증과 데이터 권한을 읽어 실제 UI 차이가 있는 role만 남긴다.
5. breakpoint와 기기 방향에 따라 구조가 달라지는 variant를 찾는다.
6. 정상 장면뿐 아니라 긴 콘텐츠, empty, loading, offline, error를 등록한다.

`mobile`과 `portrait`은 같은 말이 아니다. 모바일은 viewport/사용 환경이고 portrait는 방향이다. 데스크톱 모니터를 세로로 돌린 화면과 휴대폰 화면의 navigation, touch target, 정보 배치는 별도로 판단한다.

## 리뷰 단위

처음에는 전체 구조를 보고, 이후 sidebar/navigation, 주요 상세, 핵심 목록·관리, 설정, 보조 modal 순으로 세분화한다. 세부 단계에서 확정한 결정은 마지막 전체 구조에 다시 반영한다.

한 카드 안에 역할이나 방향을 모두 억지로 넣지 않는다. 다음 중 하나가 달라지면 variant로 분리한다.

- 사용자가 수행하는 핵심 과업
- navigation 또는 정보 위계
- 노출 가능한 데이터와 action
- responsive layout과 scroll ownership
- 가로·세로에서의 콘텐츠 재생 또는 배치 방식

## 스튜디오 셸

기본 셸은 다음 영역을 제공한다.

### 탐색

- surface 그룹
- 순번이 있는 review unit 목록
- `queued`, `reviewing`, `confirmed`, `reopened`, `integrated`, `verified` 상태
- 미확정 수와 parity 누락 수

### variant 제어

- role
- viewport 또는 device class
- orientation
- 핵심 state

존재하지 않는 조합은 disabled 처리하거나 제외 사유를 보여준다. 선택 가능한 것처럼 보인 뒤 빈 화면을 내지 않는다.

### 비교 모드

- `baseline`: 리뷰 시작 시점의 source-faithful 장면
- `proposal-rN`: 사용자 피드백이 반영된 수정안
- `final`: confirmed decision을 합친 통합 기준
- `actual`: 실제 구현 또는 그 검수 장면

기준본과 수정안은 같은 review unit과 variant에서 이어져야 한다. 사용자가 role이나 방향을 바꾼 뒤 돌아와도 비교 모드를 보존한다. 다른 unit에 해당 revision이 없으면 가장 가까운 유효 모드를 사용하되 전환 사실을 표시한다.

### 의견과 결정

- 팀 또는 전문 렌즈 의견
- 사용자 의견
- 디자인 리드 종합
- 현재 revision에서 반영된 decision
- 확정, 재개방, 제외 이력

실제 독립 팀원이 참여하지 않았다면 팀원 이름이나 합의가 있었던 것처럼 표시하지 않는다.

## 기준본과 revision

- baseline 파일 또는 registry record는 제안 작업에서 수정하지 않는다.
- baseline의 오류를 발견하면 `baseline-correction`으로 원인을 남기고 새 snapshot을 만들며 이전 snapshot을 보존한다.
- proposal은 append-only revision으로 관리한다.
- 사용자의 새 의견이 이전 결정을 뒤집으면 이전 decision을 삭제하지 않고 `superseded_by`로 연결한다.
- final은 마지막 proposal의 별칭이 아니라 모든 confirmed decision을 통합한 별도 장면이다.

## 데이터와 출처 표시

각 장면은 다음 provenance를 구분한다.

- `faithful`: 운영 소스나 확인된 런타임 동작을 그대로 반영
- `synthetic`: 실제 schema와 길이·분포를 따르지만 값은 합성
- `proposed`: 아직 운영에 없는 디자인 또는 기능
- `unknown`: 근거를 찾지 못해 검토가 필요한 부분

실제 DB row, 고객명, 리뷰 원문, 장비 식별자, credential은 기본적으로 복사하지 않는다. 데이터가 레이아웃에 미치는 특성만 유지한다.

## 리뷰 접근성

- baseline과 proposal을 색상만으로 구분하지 않는다.
- 긴 텍스트, 키보드 focus, 확대, touch target, modal focus 이동을 검토한다.
- collapse, sticky, auto-scroll, crossfade 같은 동작은 reduced motion과 사용 중단 경로를 고려한다.
- 모바일에서는 desktop을 축소하지 말고 navigation, scroll owner, 고정 영역을 다시 설계한다.

## 운영 연속성

- 리뷰 스튜디오가 정적 파일이어도 가능하면 로컬 서버로 제공해 동일 URL을 유지한다.
- 사용자가 리뷰를 진행 중이면 서버를 임의로 종료하지 않는다.
- 화면, role, 비교 모드, orientation 선택은 refresh 또는 unit 전환 뒤에도 가능한 범위에서 유지한다.
- 운영 API가 없어도 고정 fixture로 장면이 재현되어야 한다.

## 최종 통합 확인

각 confirmed decision에 final 장면의 위치를 연결한다. 다음 충돌을 다시 본다.

- 세부 카드의 높이 변경이 전체 화면 밀도를 깨뜨리는가
- header, filter, content, pagination 중 누가 scroll owner인가
- desktop sticky 규칙이 mobile에서 잘못 유지되는가
- role별 action이 권한과 맞는가
- modal이 media 유무와 긴 콘텐츠에서 적절한 크기인가
- 설정 option과 preview가 동일한 의미를 전달하는가

coverage가 100%가 아니면 handoff로 넘어가지 않는다.

