# 문서 목적 라우터
넓은 "문서 만들어줘" 요청은 바로 기획 문서로 보내지 않는다. 먼저 문서가 어떤 일을 해야 하는지 분류한다.

## 상시 문서와 시점 기록 구분
- 계속 최신 상태로 관리해야 하면 `living-doc-writer` 대상이다.
- 날짜가 중요한 분석, 제안서, 포스트모템, 회고, 특정 시점 ADR은 `snapshot-report-writer`가 더 적합하다.
- 회의록은 시점 기록이다. 사용자가 회의록을 명시하지 않으면 회의 내용을 상시 문서의 근거로만 사용한다.
- formal ADR이 필요하면 snapshot report로 남기고, living docs에는 `decision-log.md`나 `decision-index.md`로 현재 결론만 요약한다.

## 목적별 분류
| 목적 | 사용자 표현 | 우선 reference | 대표 문서 |
|---|---|---|---|
| 기획 | 기획 문서, 아이디어, 디자인 방향, 개발 착수, 요구사항 | `document_intake_router.md` | 아이디어/디자인/개발 착수 문서 |
| 의사결정 | 결정 정리, 왜 이렇게 했는지, 선택지 비교, 현재 기준 | `living_document_package_matrix.md` | `docs/project/decision-log.md` |
| 진행 상태 | 지금 어디까지, 다음 할 일, 로드맵, 리스크 | `living_document_package_matrix.md` | `docs/project/current-status.md`, `roadmap.md`, `risk-register.md` |
| 운영/배포 | 운영 문서, 배포 절차, runbook, 장애 대응 | `living_document_package_matrix.md` | `docs/operations/runbook.md`, `deployment.md` |
| 온보딩/인수인계 | 새 개발자 문서, 코드 맵, 로컬 실행, handoff | `living_document_package_matrix.md` | `docs/onboarding/project-overview.md`, `local-setup.md`, `code-map.md` |
| 코드 역기획 | 프로젝트 분석, 전체 구조 분석, 코드 기반 문서화, 역기획 | `living_document_package_matrix.md` | `docs/planning/feature-catalog.md`, `docs/onboarding/code-map.md` |
| QA/테스트 | 테스트 전략, 회귀 범위, 릴리즈 체크 | `living_document_package_matrix.md` | `docs/qa/test-strategy.md`, `regression-matrix.md` |
| 사용자/서비스 | 사용 설명서, 관리자 가이드, FAQ, 알려진 문제 | `living_document_package_matrix.md` | `docs/service/user-guide.md`, `faq.md` |
| 데이터/보안/정책 | 개인정보, 권한, 데이터 보존, 정책, 감사 | `living_document_package_matrix.md` | `docs/data/data-dictionary.md`, `docs/security/access-control.md` |
| 디자인 시스템/콘텐츠 | 컴포넌트 기준, 토큰, 문구 톤, microcopy | `living_document_package_matrix.md` | `docs/design-system/components.md`, `docs/content/voice-and-tone.md` |
| 비즈니스/성과 | 수익 모델, 가격, KPI, 이벤트 정의 | `living_document_package_matrix.md` | `docs/business/business-model.md`, `docs/analytics/kpi-definition.md` |
| 문서 운영 | 문서 구조 정리, 인덱스, 용어집, 오래된 문서 | `living_document_package_matrix.md` | `docs/doc-map.md`, `docs/glossary.md` |

## 자동 판별 규칙
1. 사용자가 "만들고 싶은 것"을 설명하면 기획으로 본다.
2. 사용자가 "현재 상태"나 "다음 일"을 묻거나 장기 작업의 최신 상황을 정리하려 하면 진행 상태로 본다.
3. 사용자가 "어떻게 실행/배포/운영"을 묻으면 운영/배포로 본다.
4. 사용자가 "처음 보는 사람이 이해"해야 한다고 말하면 온보딩/인수인계로 본다.
5. 사용자가 기존 코드나 프로젝트 전체를 분석해 문서화하라고 하면 코드 역기획으로 본다.
6. 사용자가 "사용자가 보는 설명"을 원하면 사용자/서비스 문서로 본다.
7. 사용자가 "데이터, 권한, 개인정보, 보안"을 언급하면 데이터/보안/정책으로 본다.
8. 하나의 요청에 여러 목적이 섞이면 사용자가 당장 보려는 결론을 첫 문서로 두고, 나머지는 관련 문서로 분리한다.

## 애매할 때 묻는 방식
- 질문은 1-3개만 한다.
- 추천 분류를 먼저 제시한다.
- 답이 없어도 낮은 위험으로 진행할 수 있으면 `가정`과 `미정`으로 나누고 초안을 만든다.

```markdown
이 요청은 세 방향으로 나눌 수 있습니다.

- 현재 상태 문서: 지금 어디까지 왔고 다음에 뭘 할지 정리
- 온보딩 문서: 새로 보는 사람이 프로젝트를 이해하고 실행하게 정리
- 운영 문서: 배포, 설정, 장애 대응 기준 정리

현재 표현만 보면 현재 상태 문서가 먼저 맞아 보입니다. 이 기준으로 초안을 만들까요?
```
