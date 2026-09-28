# 개발 착수 문서 패키지 기준
사용자가 "앱 만들자", "POC 만들자", "MVP 개발하자", "PRD 만들어줘", "개발 착수 문서 만들어줘", "요구사항/화면/API/일정/QA 문서 만들어줘"처럼 개발 실행을 전제로 요청하면 이 기준을 따른다.

## 기본 원칙
- 회의록 생성을 명시하지 않았다면 회의록은 만들지 않는다. 사용자 발화, 회의 요약, 아이디어/디자인 기획 문서를 입력 자료로 삼아 개발 착수 문서로 변환한다.
- 개발, 디자인, QA, 일정 관리의 독자와 갱신 주기가 달라질 때 문서를 분리한다. 요청 범위가 작고 한 문서에서 관리할 수 있으면 통합한다.
- 모든 문서는 `확정`, `가정`, `미정`, `사용자 확인 필요`를 구분한다.
- 실제 코드가 없는 초기 기획 단계에서는 코드 경로를 억지로 만들지 않는다. 대신 근거 자료와 추후 검증 방법을 남긴다.
- 문서 수의 하한은 두지 않는다. 아래 표는 선택 가능한 문서 세트이며, 요청의 성공 기준에 필요한 항목만 만들거나 기존 문서에 통합한다.
- 아이디어 자체나 디자인 방향이 아직 불명확하면 먼저 `idea_planning_package.md` 또는 `design_planning_package.md`로 돌아간다.

## 표준 문서 세트
기본 경로는 `docs/`이다.

| 순서 | 문서 | 경로 | 목적 |
|---|---|---|---|
| 1 | 프로젝트 정의서 | `docs/project/project-brief.md` | 왜, 누구를 위해, 무엇을 만들지 정한다. |
| 2 | 결정 로그 | `docs/project/decision-log.md` | 현재까지 확정된 제품/기술/일정 결정을 최신 기준으로 모은다. |
| 3 | POC 계획 | `docs/planning/poc-plan.md` | 검증할 가설, 최소 실험, 성공/중단 기준을 정한다. |
| 4 | MVP 범위 | `docs/planning/mvp-scope.md` | 첫 사용자 가치, 포함, 후속, 제외 범위와 출시 최소 기준을 정한다. |
| 5 | PRD | `docs/planning/prd.md` | 제품 문제, 목표, non-goals, 요구사항, 정책, 출시 판단 기준을 정한다. |
| 6 | 요구사항 정의서 | `docs/planning/requirements.md` | 기능, 비기능, 권한, 정책, 예외, acceptance criteria를 정한다. |
| 7 | 사용자 시나리오 | `docs/planning/user-scenarios.md` | 주요 사용자 여정과 성공/실패 분기를 설명한다. |
| 8 | 화면 명세서 | `docs/planning/screen-spec.md` | 화면 목록, 상태, 입력, 버튼, 전환, 오류 처리를 정의한다. |
| 9 | 디자인 문서 | `docs/design/design-brief.md` | 디자인 방향, 레이아웃 원칙, 컴포넌트, 반응형, 접근성, handoff 기준을 정한다. |
| 10 | 기술 설계서 | `docs/architecture/technical-design.md` | 구현 구조, 레이어, 모듈 책임, 주요 기술 선택을 정한다. |
| 11 | 시스템 구성 문서 | `docs/architecture/system-configuration.md` | 프론트엔드, 백엔드, DB, 외부 연동, 배포 구성을 정한다. |
| 12 | 데이터 모델 | `docs/data/data-model.md` | 엔티티, 필드, 관계, 상태값, 저장 정책을 정의한다. |
| 13 | API 명세서 | `docs/interfaces/api-spec.md` | 엔드포인트, request/response, 에러, 인증 정책을 정의한다. |
| 14 | 개발 일정 | `docs/project/milestone-plan.md` | MVP, 마일스톤, 우선순위, 담당 영역, 리스크를 정한다. |
| 15 | QA 문서 | `docs/qa/qa-checklist.md` | 기능별 검수, 경계 조건, 회귀 테스트, 릴리즈 체크를 정의한다. |

## 상황별 축소와 확장
- 백엔드가 없는 정적 웹, 개인 도구, 프로토타입은 `api-spec.md`를 제외하거나 `해당 없음` 사유를 manifest에 남긴다.
- 데이터 저장이 없는 도구는 `data-model.md`를 제외하거나 "로컬 상태만 사용"처럼 범위를 명시한다.
- 운영 절차, 배포, 장애 대응이 필요한 서비스는 `docs/operations/runbook.md`를 추가한다.
- 법무, 개인정보, 결제, 관리자 권한이 중요한 서비스는 `docs/project/policy-and-risk.md`를 추가한다.
- 기존 코드가 있는 프로젝트는 `feature-analyzer`로 확인한 사실을 각 문서의 근거로 연결한다.

## 생성 순서
1. `project-brief.md`로 목적, 사용자, 문제, 성공 기준을 먼저 고정한다.
2. `poc-plan.md`로 POC 필요 여부와 검증할 가장 위험한 가설을 정한다.
3. `mvp-scope.md`에서 MVP, 후속, 제외 범위를 정한다.
4. `prd.md`에서 제품 요구사항과 출시 판단 기준을 정하거나 `deferred` 사유를 남긴다.
5. `requirements.md`에서 기능 요구사항과 acceptance criteria를 QA 가능한 수준으로 쪼갠다.
6. `user-scenarios.md`와 `screen-spec.md`로 화면과 흐름을 구체화한다.
7. `design-brief.md`로 화면 구현에 필요한 디자인 판단을 고정한다.
8. `technical-design.md`, `system-configuration.md`, `data-model.md`, `api-spec.md`로 구현 계약을 만든다.
9. `milestone-plan.md`와 `qa-checklist.md`로 개발과 검수 실행 기준을 만든다.
10. `docs/README.md` manifest에 생성 문서, 최종 갱신일, 비고를 반영한다.

## 완료 기준
- 문서 세트가 POC, MVP, PRD, 요구사항, 화면, 디자인, 기술, 일정, QA를 모두 다룬다.
- 요구사항과 화면 문서에 "정상 흐름"뿐 아니라 오류, 빈 상태, 권한, 예외가 포함되어 있다.
- 디자인 문서가 단순 분위기 설명이 아니라 구현 가능한 레이아웃, 컴포넌트, 상태, 반응형 기준을 포함한다.
- 기술 문서가 선택한 구조와 선택하지 않은 대안, 변경 가능 지점을 설명한다.
- QA 문서가 요구사항과 화면 흐름을 검증할 수 있는 체크리스트로 연결된다.
