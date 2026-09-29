# 스냅샷 리포트 패키지 매트릭스
리포트 범위와 목적에 맞는 보고서 구조를 선택한다. 기본 출력 루트는 `results/`이고, 없으면 `reports/`를 사용한다.

## 공통 원칙
- 파일명은 `<YYYYMMDD>_<topic>.md`를 기본으로 한다.
- 보고서 첫 부분에 기준일, 분석 범위, 사용한 근거를 둔다.
- 사실, 추론, 판단, 권장 조치를 분리한다.
- 상시 문서처럼 덮어쓰지 않는다.
- 리빙독으로 승격할 내용은 보고서 본문이 아니라 `Living Docs 반영 후보`로 따로 정리한다.

## 부분 리포트
| 유형 | 예시 파일명 | 필수 내용 |
|---|---|---|
| 기능 프로세스 분석 | `YYYYMMDD_feature_process_analysis.md` | 대상 기능, 진입점, 정상/실패 흐름, 데이터/외부 연동, 근거 파일 |
| API/인터페이스 딥다이브 | `YYYYMMDD_api_deep_dive.md` | 엔드포인트, request/response, 에러, 권한, 호출자, 리스크 |
| 장애/이슈 원인 분석 | `YYYYMMDD_issue_rca.md` | 현상, 재현 조건, 원인, 영향, 해결안, 검증 방법 |
| 리팩토링 검토 | `YYYYMMDD_refactor_review.md` | 현재 구조, 문제, 대안, 비용, 리스크, 단계적 적용안 |
| ADR | `YYYYMMDD_adr_<decision>.md` | context, decision, options, consequences, rollback plan |

## 전체 리포트
| 유형 | 예시 파일명 | 필수 내용 |
|---|---|---|
| 프로젝트 전체 구조 분석 | `YYYYMMDD_project_structure_report.md` | 도메인, 모듈, 진입점, 데이터, 외부 연동, 운영/테스트 단서 |
| 현재 상태 보고 | `YYYYMMDD_project_status_report.md` | 완료, 진행 중, 막힘, 리스크, 다음 액션, 사용자 확인 필요 |
| 기술부채 리뷰 | `YYYYMMDD_technical_debt_review.md` | 주요 부채, 영향, 우선순위, 개선안, 하지 않을 때 리스크 |
| 릴리즈 준비도 | `YYYYMMDD_release_readiness_report.md` | 기능, QA, 운영, 롤백, 문서, 승인 상태 |
| 운영 준비도 | `YYYYMMDD_operations_readiness_report.md` | 배포, 설정, 모니터링, 장애 대응, 온콜/운영 책임 |
| 보안/데이터 리스크 | `YYYYMMDD_security_data_risk_report.md` | 권한, 개인정보, 데이터 보존, 로그 노출, 감사 필요 |
| QA 준비도 | `YYYYMMDD_qa_readiness_report.md` | 테스트 범위, 회귀 위험, 자동화 갭, 수동 검수 포인트 |
| 온보딩 갭 분석 | `YYYYMMDD_onboarding_gap_report.md` | 새 참여자가 막힐 지점, 문서 갭, 로컬 실행, 코드 맵 필요 |

## 보고서 세트가 필요한 경우
- 전체 프로젝트를 여러 관점으로 검토하라고 하면 종합 보고서 1개를 먼저 만들고, 필요할 때 세부 보고서를 추가한다.
- 하네스 회의 결과를 보고서로 남기는 경우 meeting별 보고서는 시점 기록으로 두고, 최신 결론은 living docs 반영 후보로 분리한다.
- 사용자가 "간단히"라고 하면 전체 세트를 만들지 않고 핵심 종합 보고서 1개로 축소한다.

## 전체 리포트 공통 섹션
- 핵심 결론
- 기준일과 분석 범위
- 확인한 근거
- 현재 상태
- 주요 리스크
- 선택지 또는 권장 조치
- 다음 액션
- Living Docs 반영 후보
