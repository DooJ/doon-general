# 하네스 리빙독 브리지
하네스 회의 결과를 최신 상시 문서로 정리할 때 사용한다.

## 입력으로 볼 수 있는 자료
- `publish/harness/10_projects/<project-slug>/10_meetings/Mxxx-<topic>/README.md`
- `publish/harness/10_projects/<project-slug>/10_meetings/Mxxx-<topic>/report.md`
- `publish/harness/10_projects/<project-slug>/20_deliverables/Mxxx-<topic>/`
- `publish/harness/10_projects/<project-slug>/30_artifacts/artifact_index.md`
- `publish/harness/10_projects/<project-slug>/30_artifacts/living_docs/README.md`

## 기본 출력 위치
하네스 프로젝트 안에서 문서 승격을 요청받으면 기본 문서 루트는 아래다.

```text
publish/harness/10_projects/<project-slug>/30_artifacts/living_docs/
```

실제 소스 프로젝트의 `docs/`를 갱신하라고 사용자가 명시하거나 `02_source_map.md`에 허용되어 있으면, 소스 프로젝트의 `docs/`도 갱신할 수 있다. 이 경우 하네스 `living_docs/README.md`에는 소스 프로젝트 문서 경로를 링크한다.

## 승격 규칙
- 회의별 `report.md`는 시점 기록이다. 그대로 복사하지 않는다.
- agent 개별 의견은 원문이 아니라 `합의`, `남은 이견`, `사용자 확인 필요`, `오케스트레이터 종합`으로 압축한다.
- `20_deliverables/`의 채택 산출물은 현재 문서의 근거로 연결한다.
- 확정되지 않은 항목은 `미정` 또는 `사용자 확인 필요`에 둔다.
- 이전 문서를 대체하면 `30_artifacts/artifact_index.md`의 대체 관계를 갱신한다.

## run_type 매핑
| run_type | 우선 문서 패키지 |
|---|---|
| `planning` | `idea_planning_package.md` 또는 `planning_document_package.md` |
| `design` | `design_planning_package.md`와 개발용 디자인 문서 |
| `development` | 기술 설계, 시스템 구성, API, 데이터 모델, QA, 운영/배포, 온보딩 문서 |
| `mixed` | 열린 cycle별 문서 패키지를 통합 |
| `advisory` | 결정 로그, 현재 상태, 리스크, 선택지 비교, 후속 액션. 개발 문서 확정은 보류 |
| `marketing` | 포지셔닝, 메시지, 실험 계획, KPI, 이벤트 정의. 제품 문서에는 확정 결정만 연결 |

## 문서 필수 메타 정보
하네스에서 승격된 각 문서 상단 또는 하단에는 아래를 둔다.

- 출처 회의
- 근거 산출물
- 반영한 결정
- 남은 이견
- 사용자 확인 필요
- 다음 갱신 트리거

## 인덱스 갱신
`30_artifacts/living_docs/README.md`에는 아래 표를 갱신한다.

- 현재 먼저 볼 문서
- 사용자 확인 필요
- 최신 문서 목록
- 단계별 분류

`30_artifacts/artifact_index.md`에는 living doc 문서를 `유형: living_doc`으로 등록한다.
