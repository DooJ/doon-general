# 산출물 템플릿

프로젝트의 기존 문서 형식이 있으면 그것을 우선한다. 아래 템플릿은 필요한 필드가 빠지지 않게 하는 최소 계약이다.

## 1. Source map과 데이터 근거

| Evidence ID | Surface/Screen | Source path or route | Source revision | Data evidence | Role/State | Provenance | 확인 상태 |
|---|---|---|---|---|---|---|---|
| EV-001 | 웹/전체 구조 | `src/...` | commit/build ID | DATA-001 | 일반/ready | faithful | 확인 |

`Provenance`는 `faithful`, `synthetic`, `proposed`, `unknown` 중 하나를 사용한다.

| Data ID | 종류 | 위치와 버전 | schema/query | 기준 시각 | 합성 규칙/분포 | 민감정보 처리 |
|---|---|---|---|---|---|---|
| DATA-001 | API/DB/fixture | endpoint, table 또는 backup ID | field 또는 집계 query | ISO timestamp | 고정 seed와 길이 분포 | 익명화 |

## 2. Review matrix

```yaml
review_units:
  - id: WA-01
    surface: web-admin
    title: 전체 구조
    status: reviewing
    baseline:
      id: baseline-v1
      source_revision: commit-or-build-id
      snapshot_at: 2026-07-23T12:00:00+09:00
      fixture_seed: project-review-v1
      content_hash: sha256:example
    variants:
      - id: super-desktop
        role: super-admin
        viewport: desktop
        orientation: landscape
        states: [ready, long-content]
      - id: super-mobile
        role: super-admin
        viewport: mobile
        orientation: portrait
        states: [ready, menu-open]
    excluded_variants:
      - variant: user-tablet-landscape
        reason: tablet 전용 구조가 없고 desktop 규칙과 동일
        evidence: EV-003
```

리뷰 상태는 `queued`, `reviewing`, `confirmed`, `reopened`, `integrated`, `verified`를 사용한다.

## 3. Decision history

| Decision ID | Review unit | Revision | 의견 출처 | 문제/영향 | 요청 또는 결정 | 반영 위치 | 상태 | Superseded by |
|---|---|---|---|---|---|---|---|---|
| D-001 | WA-01 | proposal-r1 | 사용자 | 상태 의미가 모호함 | 역할별 요약 지표 분리 | summary row | confirmed | - |

사용자 원문 전체를 복사하기보다 의미를 보존한 요약을 남긴다. 팀 의견과 사용자 의견을 같은 출처로 합치지 않는다.

## 4. Review unit record

```yaml
id: WA-01
baseline: baseline-v1
active_proposal: proposal-r2
evidence: [EV-001, EV-002]
opinions:
  structure: OP-001
  interaction: OP-002
  visual: OP-003
  user: UO-001
lead_synthesis: LS-001
decisions: [D-001, D-004]
confirmation:
  status: confirmed
  confirmed_at: 2026-07-23
  confirmed_by: user
  evidence_ref: conversation-or-approval-id
  applies_to_variants: [super-desktop, super-mobile]
revisions:
  - id: proposal-r1
    decisions: [D-001]
  - id: proposal-r2
    decisions: [D-001, D-004]
```

## 5. Final integration coverage

| Decision ID | Proposal 위치 | Final surface/screen | Final variant | Final component | 반영 | 제외 사유/승인 |
|---|---|---|---|---|---|---|
| D-001 | WA-01 summary | 웹/전체 구조 | super-desktop, super-mobile | account summary | Yes | - |

모든 confirmed decision이 한 행을 가져야 한다. `반영=No`이면 사유와 사용자 승인이 모두 있어야 한다.

## 6. Development handoff

| Decision ID | Final reference | Actual target | 적용 조건 | Interaction/responsive | Acceptance criteria | 구현 상태 |
|---|---|---|---|---|---|---|
| D-001 | `final?screen=...` | `src/.../Summary.*` | super-admin | mobile 2행, desktop 1행 | 역할별 수치와 순서 일치 | pending |

실제 target은 가능한 경우 route, component, style, data binding을 모두 적는다.

## 7. Parity report

| Check ID | Decision ID | Variant/State | Final evidence | Actual evidence | Actual revision/build | 환경 | Fixture/seed | Checked at/by | 결과 | 차이와 조치 | 재검수 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-001 | D-001 | super-mobile/ready | final URL 또는 캡처 | 실제 URL 또는 캡처 | commit/build ID | browser/device와 정확한 viewport/orientation | fixture ID | timestamp/reviewer | partial | 두 번째 지표 누락 | open |

결과는 `match`, `partial`, `missing`, `diverged`, `approved-change`, `blocked` 중 하나다.

`approved-change`는 승인 근거, 새 decision ID, 갱신한 final revision을 `차이와 조치`에 연결해야 한다.

## 8. Preview server manifest

```yaml
preview:
  root: docs/design-review/studio
  start_command: project-specific-command
  health_url: http://127.0.0.1:PORT/
  restart_command: project-specific-command
  state_file: docs/design-review/review-state.json
```

명령은 프로젝트에서 실제로 실행한 값으로 기록한다. 장기 세션에서 프로세스가 사라져도 같은 URL과 state를 복원할 수 있어야 한다.

## 9. Completion summary

```yaml
coverage:
  required_variant_state_ids:
    - WA-01:super-desktop:ready
    - WA-01:super-desktop:long-content
    - WA-01:super-mobile:ready
    - WA-01:super-mobile:menu-open
  covered_variant_state_ids:
    - WA-01:super-desktop:ready
    - WA-01:super-desktop:long-content
    - WA-01:super-mobile:ready
    - WA-01:super-mobile:menu-open
  missing_variant_state_ids: []
  inventory_required: 18
  inventory_covered: 18
  confirmed_decisions: 27
  decisions_in_final: 27
parity:
  match: 25
  approved_change: 2
  partial: 0
  missing: 0
  diverged: 0
  blocked: 0
completion: verified
```

`inventory_required`는 registry의 필수 `review-unit:variant:state` ID를 열거해 계산하고 임의의 숫자로 적지 않는다. `missing_variant_state_ids`가 비어 있지 않거나 `partial`, `missing`, `diverged`, `blocked` 중 하나라도 0이 아니면 `completion`은 `verified`가 될 수 없다.
