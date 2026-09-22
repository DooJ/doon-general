---
name: refining-implemented-ui
description: "Use when a web or app product already has a first-pass UI and core functions, and the user wants a source- and data-grounded UI/UX improvement review with mock reconstruction, revision history, an integrated final reference, and post-implementation parity verification."
---

# Refining Implemented UI

1차 구현이 끝난 제품을 운영 코드에서 바로 반복 수정하지 않고 별도 리뷰 스튜디오에서 검토한다. `source-faithful baseline → reviewed proposal → integrated final → implemented actual`을 추적해 디자인 결정과 실제 개발 사이의 누락을 막는다.

## 적용 경계

다음 의도가 있으면 사용한다.

- 기존 UI 소스와 데이터 구조를 근거로 모의 화면을 다시 만든다.
- 화면 또는 기능 단위로 UI/UX를 순차 리뷰하고 요구·결정 이력을 남긴다.
- 확정된 세부 수정안을 하나의 최종 통합 화면에 반영한다.
- 실제 UI 수정 후 최종 기준과 비교해 누락을 검수한다.

다음에는 사용하지 않는다.

- 최초 제품 콘셉트나 첫 시안 탐색: `ui-concept-director`
- 스크린샷 한 장의 간단한 비평 또는 작은 CSS 조정: `design-generalist` 또는 현재 구현 루프
- 토큰과 컴포넌트 거버넌스 자체가 목적: `design-system-curator`
- 구현 근거가 없는 가상의 리디자인

## 관련 규칙과 스킬

- 항상 `.agentic_base/rules/04_design_rules.md`를 적용한다.
- 웹은 `05_web_design_rules.md`, 모바일·태블릿 앱은 `06_app_design_rules.md`를 추가로 적용한다.
- 현재 구조가 불명확하면 먼저 `feature-analyzer`로 화면·라우트·데이터 흐름을 파악한다.
- 화면 목록과 내비게이션 재구성이 핵심이면 `information-architect`, 상태 전이가 핵심이면 `interaction-designer`, 세부 디자인 판단과 handoff에는 `design-generalist`를 필요한 범위만 연결한다.
- 사용자가 독립 팀원, 교차 검토, 하네스 진행을 명시했을 때만 `huggies`와 `.agentic_base/harness/design_review_protocol.md`를 연결한다. 실제 팀원이 없으면 사람 이름의 의견을 꾸며내지 말고 `정보 구조`, `인터랙션`, `시각 완성도` 같은 전문 렌즈로 표시한다.

## 시작 전 확인

기존 파일을 먼저 조사하고 이미 확인 가능한 내용을 사용자에게 다시 묻지 않는다.

1. 운영 소스와 리뷰용 산출물의 저장소·경계를 확인한다.
2. UI entry point, route/navigation, component, style/token, 상태와 권한 정책을 찾는다.
3. DB schema, API response, fixture 또는 백업에서 화면에 필요한 데이터의 형태와 길이 분포를 확인한다.
4. 실제 고객 데이터는 직접 노출하지 않고 익명화하거나 같은 분포의 합성 데이터로 바꾼다.
5. 현재 git 변경을 확인하고 사용자 변경을 덮어쓰지 않는다.

근거가 부족하면 추측으로 기준본을 만들지 않는다. 확인한 사실, 합성한 부분, 제안한 부분을 각각 `faithful`, `synthetic`, `proposed`로 구분한다.

## 핵심 작업 흐름

### Gate 1. Evidence

화면별로 다음 근거를 연결한다.

- source route와 UI component
- 상태와 role/permission 분기
- style/token과 주요 asset
- 데이터 source, schema 또는 합성 규칙
- 런타임에서 확인한 사실과 아직 확인하지 못한 사실

근거 맵 없이 리뷰 스튜디오 제작을 시작하지 않는다.

### Gate 2. Inventory

다음 축을 조사해 리뷰 매트릭스를 만든다.

- `surface`: 웹 어드민, 사이니지, 매니저 앱처럼 독립된 제품 표면
- `screen/unit`: 전체 구조와 sidebar, 상세, 목록, 설정처럼 별도 결정이 필요한 단위
- `role`: 일반 사용자, 관리자, 슈퍼 관리자처럼 UI나 데이터가 달라지는 권한
- `viewport`: desktop, tablet, mobile
- `orientation`: portrait, landscape
- `state`: loading, empty, ready, long-content, offline, error와 도메인 상태

모든 조합을 기계적으로 만들지 않는다. 레이아웃, 노출 정보, 과업이 실제로 달라지는 조합만 variant로 등록하고 제외 사유를 남긴다. sidebar, 탭, 화면 목록은 실제 navigation을 근거로 하되 리뷰 순서는 전체 구조에서 세부 단위로 정한다.

상세 registry와 셸 규칙이 필요하면 [review-studio-contract.md](references/review-studio-contract.md)를 읽는다.

### Gate 3. Baseline

운영 코드와 분리된 리뷰 스튜디오에 `source-faithful baseline`을 만든다.

- 캡처 이미지를 나열하지 말고 실제 소스가 만드는 구조와 상태를 코드로 재현한다.
- baseline은 리뷰 시작 시점의 immutable snapshot이다. 제안 반영을 위해 baseline을 덮어쓰지 않는다.
- 제안은 `proposal-r1`, `proposal-r2`처럼 별도 revision으로 추가한다.
- 고정 seed와 현실적인 긴 텍스트, 빈 데이터, 오류, 미디어 유무를 포함한다.
- 리뷰 스튜디오 때문에 운영 코드, 운영 DB, 인증 상태를 바꾸지 않는다.

리뷰 서버를 띄웠다면 사용자가 리뷰 종료를 선언할 때까지 접근 가능한 상태를 유지한다. 프로세스가 중단되면 다음 리뷰 전에 다시 올리고 URL을 유지한다.

### Gate 4. Sequential Review

한 번에 한 리뷰 단위를 진행한다.

1. 기준본과 현재 근거를 보여준다.
2. 독립 팀원이 있으면 출처가 분리된 의견을, 없으면 명시적인 전문 렌즈 의견을 기록한다.
3. 사용자 의견을 별도 기록한다. 이전 의견을 지우지 않는다.
4. 디자인 리드 관점에서 충돌, 우선순위, 구현 영향을 종합한다.
5. 수정안을 스튜디오에 반영하고 변경 전후를 함께 볼 수 있게 한다.
6. 사용자가 확정하면 `confirmed`로 바꾸고 다음 단위로 이동한다.

문서에만 요구를 적고 화면은 그대로 두지 않는다. 시각적으로 확인할 수 있는 요구는 수정안에 먼저 반영한 뒤 확정을 요청한다. 사용자가 확정 단위를 다시 열면 `reopened`와 새 revision을 남긴다.

역할, viewport, orientation, 리뷰 단위를 전환해도 기준본·수정안 선택과 비교 맥락을 가능한 범위에서 유지한다.

### Gate 5. Integration

세부 화면의 확정만으로 완료하지 않는다.

- 모든 confirmed decision을 전체 콘셉트의 최종 통합본에 다시 병합한다.
- 필요한 role, desktop/mobile, portrait/landscape 최종 variant를 만든다.
- 세부안에서는 맞지만 통합 화면에서 생기는 밀도, scroll, sticky, modal, navigation 충돌을 다시 검토한다.
- `decision → proposal revision → final 위치` coverage를 작성한다.
- 최종본에 들어가지 않은 결정은 명시적인 제외 사유와 사용자 승인이 있어야 한다.

기존 단계별 화면은 결정 이력으로 보존하고 최종본으로 대체하지 않는다.

### Gate 6. Development Handoff

사용자가 실제 UI 구현을 요청하면 확정된 최종본을 구현 루프의 입력으로 전달한다. 각 항목에 다음을 연결한다.

- requirement/decision ID
- final surface, screen, variant, component 위치
- 실제 route, component, style, data target
- interaction과 responsive 규칙
- acceptance criteria와 검증 상태

최종본 확정 전에는 운영 화면을 미리 수정하지 않는다. 단, 사용자가 리뷰와 구현을 동시에 요청한 경우에도 review 기준을 먼저 고정하고 그 기준을 따라 구현한다.

### Gate 7. Parity

실제 구현 뒤 최종본과 운영 UI를 같은 variant와 상태로 비교한다.

- `match`: 기준과 일치
- `partial`: 일부만 반영
- `missing`: 누락
- `diverged`: 합의 없이 다르게 구현
- `approved-change`: 비교 중 사용자와 합의해 변경
- `blocked`: 환경 또는 데이터 때문에 검수 불가

정적 코드만 보고 끝내지 말고 가능한 경우 실제 렌더링과 상호작용을 확인한다. role, breakpoint, orientation, 긴 텍스트, 빈/오류 상태, media 유무, scroll/sticky/collapse, filter/pagination, 선택 상태 보존을 비교한다.

`partial`, `missing`, 미합의 `diverged`, `blocked`가 하나라도 남으면 완료로 보고하지 않는다. `approved-change`는 최종 기준과 결정 이력을 함께 갱신한 뒤 닫는다.

## 산출물과 상태

기존 프로젝트 문서 구조를 우선하고, 없으면 `docs/design-review/` 아래에 둔다.

- 근거·대상 inventory와 review matrix
- 실행 가능한 리뷰 스튜디오와 variant registry
- 팀/전문 렌즈 의견, 사용자 의견, 디자인 리드 종합
- 요구·결정·revision 이력
- 최종 통합본과 decision coverage
- 개발 handoff와 acceptance criteria
- final 대 actual parity report

리뷰 스튜디오의 기본 형태가 필요하면 브라우저에서 [self-contained HTML 예제](assets/examples/review-studio-sample.html)를 연다. 예제의 `desktop`, `mobile`, `baseline ↔ proposal`, `integrated final` 장면과 role·mode 선택 유지 방식을 참고하되, 화면과 fixture를 대상 프로젝트에 그대로 복제하지 않는다. 실제 source, navigation, role, viewport, orientation, data schema를 다시 조사해 구성한다.

복사 가능한 필드와 예시는 [artifact-templates.md](references/artifact-templates.md)를 읽는다. 이번 방식의 최초 실전 사례에서 일반화한 판단이 필요하면 [first-implementation-review-reference.md](references/first-implementation-review-reference.md)를 읽되 화면명과 수치를 다른 프로젝트에 복제하지 않는다.

## 완료 판정

다음을 모두 만족해야 완료다.

- 필요한 surface, screen, role, viewport, orientation, state가 inventory에 있거나 제외 사유가 있다.
- baseline과 proposal revision이 분리되어 있다.
- 사용자 확정과 재개방 이력이 보존되어 있다.
- 모든 confirmed decision이 최종본 또는 승인된 제외 사유에 연결된다.
- 실제 구현과 최종본의 parity 검수가 끝났다.
- 열린 `partial`, `missing`, 미합의 `diverged`, `blocked`가 0건이다.
- 리뷰 스튜디오가 운영 기능과 고객 데이터를 의도치 않게 변경하지 않았다.
