# 리포트 리빙독 브리지
스냅샷 리포트는 특정 시점의 근거 기록이고, 리빙독은 현재 신뢰본이다. 보고서에서 나온 결론을 바로 덮어쓰지 말고 반영 후보로 분리한다.

## 기본 원칙
- 보고서 본문은 시점 기록으로 보존한다.
- 리빙독 갱신은 사용자가 명시하거나 결론이 확정되었을 때 `living-doc-writer`로 수행한다.
- 보고서의 추론, 가설, 제안은 확정 전까지 리빙독에 확정 사실처럼 넣지 않는다.
- 리빙독 반영 후보에는 대상 문서, 반영할 결론, 보류할 가정, 사용자 확인 필요를 구분한다.

## 보고서 -> 리빙독 매핑
| 리포트 내용 | 반영 후보 문서 |
|---|---|
| 현재 상태, 진행률, 막힘 | `docs/project/current-status.md` |
| 의사결정, ADR 결론 | `docs/project/decision-log.md`, `docs/project/decision-index.md` |
| 프로젝트 구조 분석 | `docs/onboarding/project-overview.md`, `docs/onboarding/code-map.md` |
| 기능/프로세스 분석 | `docs/planning/requirements.md`, `docs/planning/user-scenarios.md`, `docs/planning/screen-spec.md` |
| 아키텍처 딥다이브 | `docs/architecture/technical-design.md`, `docs/architecture/system-configuration.md` |
| API/데이터 분석 | `docs/interfaces/api-spec.md`, `docs/data/data-model.md`, `docs/data/data-dictionary.md` |
| QA/릴리즈 준비도 | `docs/qa/test-strategy.md`, `docs/qa/release-checklist.md`, `docs/qa/regression-matrix.md` |
| 운영 준비도 | `docs/operations/deployment.md`, `docs/operations/runbook.md`, `docs/operations/monitoring.md` |
| 보안/데이터 리스크 | `docs/security/access-control.md`, `docs/security/privacy-notes.md`, `docs/data/retention-policy.md` |
| 온보딩 갭 | `docs/onboarding/local-setup.md`, `docs/onboarding/code-map.md`, `docs/doc-map.md` |

## 보고서 필수 섹션
보고서 마지막에 아래 섹션을 둔다.

```markdown
## Living Docs 반영 후보

| 대상 문서 | 반영할 결론 | 근거 | 상태 |
|---|---|---|---|

### 아직 반영하면 안 되는 항목
- 

### 사용자 확인 필요
- 
```

## 상태 값
- `confirmed`: 코드, 로그, 사용자 결정으로 확인되어 반영 가능
- `candidate`: 반영 후보지만 검토 필요
- `defer`: 추론 또는 제안이라 아직 반영 보류
- `not-applicable`: 리빙독으로 옮길 내용 없음
