# 상시 문서 패키지 매트릭스
기획 외 상시 문서를 만들거나, 여러 문서군을 함께 정리할 때 사용한다. 기본 루트는 `docs/`이며, 하네스 승격 문서는 `30_artifacts/living_docs/` 아래 같은 구조를 따른다.

## 공통 원칙
- 단일 문서 요청이 아니면 목적별로 문서를 분리한다.
- 현재 기준으로 갱신되는 문서만 만든다. 날짜별 분석과 회고는 snapshot report로 보낸다.
- 실제 코드가 있으면 관련 파일, 설정, 테스트, 배포 스크립트에서 사실을 검증한다.
- 코드가 없거나 확인이 어려우면 `가정`, `미정`, `사용자 확인 필요`를 분리한다.
- 각 문서에는 `관련 문서`, `갱신 트리거`, `검증 방법`을 둔다.

## 문서군
| 문서군 | 기본 문서 | 목적 |
|---|---|---|
| 의사결정 | `docs/project/decision-log.md` | 현재 채택된 제품, 디자인, 기술, 운영 결정을 한곳에 모은다. |
| 의사결정 | `docs/project/decision-index.md` | formal ADR, 회의록, 보고서에 흩어진 결정을 찾기 위한 색인이다. |
| 진행 상태 | `docs/project/current-status.md` | 현재 완료, 진행 중, 막힌 일, 다음 행동을 정리한다. |
| 진행 상태 | `docs/project/roadmap.md` | 단기/중기 방향, 마일스톤, 출시 기준을 정리한다. |
| 진행 상태 | `docs/project/risk-register.md` | 제품, 기술, 일정, 운영 리스크와 대응을 관리한다. |
| 운영/배포 | `docs/operations/runbook.md` | 운영자가 반복 작업과 장애 대응을 수행하게 한다. |
| 운영/배포 | `docs/operations/deployment.md` | 환경별 배포 절차, 검증, 롤백 기준을 정한다. |
| 운영/배포 | `docs/operations/monitoring.md` | 로그, 지표, 알림, 대시보드, 이상 징후 판단 기준을 정한다. |
| 온보딩/인수인계 | `docs/onboarding/project-overview.md` | 처음 보는 사람이 프로젝트 목적과 구조를 빠르게 이해하게 한다. |
| 온보딩/인수인계 | `docs/onboarding/local-setup.md` | 로컬 실행, 환경변수, 테스트 실행, 흔한 실패를 정리한다. |
| 온보딩/인수인계 | `docs/onboarding/code-map.md` | 주요 모듈, 진입점, 데이터 흐름, 변경 포인트를 찾게 한다. |
| 코드 역기획 | `docs/planning/feature-catalog.md` | 코드에서 확인한 기능군, 진입점, 구현 상태, 관련 문서를 목록화한다. |
| QA/테스트 | `docs/qa/test-strategy.md` | 자동/수동 테스트 범위, 테스트 우선순위, 책임을 정한다. |
| QA/테스트 | `docs/qa/regression-matrix.md` | 변경 영역별 회귀 위험과 확인 범위를 정리한다. |
| QA/테스트 | `docs/qa/release-checklist.md` | 릴리즈 전 필수 확인, 승인, 롤백 준비를 관리한다. |
| 사용자/서비스 | `docs/service/user-guide.md` | 최종 사용자 또는 운영자가 기능을 사용하는 방법을 설명한다. |
| 사용자/서비스 | `docs/service/admin-guide.md` | 관리자 기능, 권한, 운영 절차를 설명한다. |
| 사용자/서비스 | `docs/service/faq.md` | 반복 질문과 답변을 최신 기준으로 관리한다. |
| 사용자/서비스 | `docs/service/known-issues.md` | 알려진 문제, 영향, 우회 방법, 해결 예정 기준을 관리한다. |
| 사용자/서비스 | `docs/service/changelog.md` | 사용자에게 의미 있는 변경 이력을 최신 기준으로 정리한다. |
| 데이터/보안/정책 | `docs/data/data-dictionary.md` | 주요 데이터 항목, 의미, 출처, 민감도를 정의한다. |
| 데이터/보안/정책 | `docs/data/retention-policy.md` | 수집, 보관, 삭제, 백업, 파기 기준을 정한다. |
| 데이터/보안/정책 | `docs/security/access-control.md` | 역할, 권한, 접근 경로, 감사 기준을 정한다. |
| 데이터/보안/정책 | `docs/security/privacy-notes.md` | 개인정보 처리, 노출 위험, 사용자 고지 필요성을 정리한다. |
| 디자인 시스템/콘텐츠 | `docs/design-system/components.md` | 재사용 컴포넌트, 상태, 사용 금지 패턴을 정한다. |
| 디자인 시스템/콘텐츠 | `docs/design-system/tokens.md` | 색상, 타이포그래피, 간격, 반응형 토큰을 정한다. |
| 디자인 시스템/콘텐츠 | `docs/content/voice-and-tone.md` | 제품 문구의 톤, 금지 표현, 상황별 문장 기준을 정한다. |
| 디자인 시스템/콘텐츠 | `docs/content/microcopy.md` | 버튼, 오류, 빈 상태, 안내 문구를 관리한다. |
| 비즈니스/성과 | `docs/business/business-model.md` | 고객, 가치, 채널, 비용, 수익 구조를 정리한다. |
| 비즈니스/성과 | `docs/business/pricing.md` | 가격 정책, 과금 단위, 예외, 실험 기준을 정리한다. |
| 비즈니스/성과 | `docs/analytics/kpi-definition.md` | 핵심 지표, 계산식, 해석 주의사항을 정한다. |
| 비즈니스/성과 | `docs/analytics/event-taxonomy.md` | 이벤트 이름, 속성, 발생 위치, 수집 목적을 정한다. |
| 문서 운영 | `docs/doc-map.md` | 어떤 상황에서 어떤 문서를 봐야 하는지 안내한다. |
| 문서 운영 | `docs/glossary.md` | 제품, 기술, 도메인 용어를 통일한다. |
| 문서 운영 | `docs/stale-docs.md` | 낡은 문서, 대체 문서, 삭제/보류 사유를 관리한다. |

## 목적별 최소 세트
- 현재 상황 정리: `current-status.md`, `roadmap.md`, `risk-register.md`, `decision-log.md`
- 프로젝트 전체 역기획: `project-overview.md`, `code-map.md`, `feature-catalog.md`, `requirements.md`, `technical-design.md`, `current-status.md`
- 인수인계: `project-overview.md`, `local-setup.md`, `code-map.md`, `decision-log.md`
- 운영 준비: `deployment.md`, `runbook.md`, `monitoring.md`, `release-checklist.md`
- 사용자 공개 준비: `user-guide.md`, `faq.md`, `known-issues.md`, `changelog.md`
- 데이터/보안 정리: `data-dictionary.md`, `retention-policy.md`, `access-control.md`, `privacy-notes.md`
- 성과 측정 준비: `kpi-definition.md`, `event-taxonomy.md`, `business-model.md`

## 만들지 말아야 할 것
- 구현이 없는데 실제 설정값, 실제 URL, 실제 장애 대응 번호를 지어내지 않는다.
- 사용자 가이드에 내부 구현 세부사항을 과하게 노출하지 않는다.
- 보안/개인정보 문서를 법률 자문처럼 단정하지 않는다. 확인이 필요한 항목은 `사용자 확인 필요`로 둔다.
- changelog를 날짜별 작업 일지로 만들지 않는다. 사용자에게 의미 있는 변경만 기록한다.
- decision-log를 회의록 원문으로 채우지 않는다. 현재 결론과 근거 링크만 남긴다.
