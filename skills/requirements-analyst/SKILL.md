---
name: requirements-analyst
description: "PRD, 기능 요구사항, 비기능 요구사항, 사용자 시나리오, 예외/오류 흐름, 정책, 권한, acceptance criteria, QA 연결 기준을 정리할 때 사용합니다. 사용자가 '요구사항 정의해줘', 'PRD 작성해줘', '기능 명세로 쪼개줘', 'acceptance criteria 만들어줘', '예외 케이스 정리해줘', 'QA 가능한 요구사항으로 바꿔줘'라고 요청할 때 사용합니다."
---
# Requirements Analyst
- 이 스킬의 요구사항·정책·검증 계약만으로 전체 분석을 진행합니다.
- 제품 목표나 MVP가 아직 불명확하면 `../product-planner/SKILL.md`를 먼저 사용합니다.
- 화면 구조나 인터랙션 세부가 필요하면 `../information-architect/SKILL.md` 또는 `../interaction-designer/SKILL.md`로 연결합니다.

## 번들 레퍼런스
- PRD, 요구사항 표, acceptance criteria, QA 연결 기준을 산출물로 만들어야 하면 `references/acceptance_criteria_matrix.md`를 읽습니다.
- 작은 기능 설명을 검토하는 수준이면 reference를 읽지 말고 본문 기준으로만 처리합니다.

## 역할
- 기획 의도를 PRD와 개발, 디자인, QA가 검증 가능한 요구사항으로 바꿉니다.
- 정상 흐름뿐 아니라 예외, 권한, 빈 상태, 오류, 재시도, 완료 조건을 빠뜨리지 않습니다.
- 요구사항, 정책, 제약, 가정, 미정을 분리합니다.

## 요구사항 분해 순서
1. 대상 기능과 사용자 목표를 확인합니다.
2. POC/MVP 범위와 PRD 상태를 확인합니다.
3. 사용자 유형과 권한을 분리합니다.
4. 정상 흐름을 단계별로 씁니다.
5. 실패 흐름, 예외 조건, 경계값, 재시도 조건을 씁니다.
6. 데이터 입력, 검증 규칙, 상태값, 알림, 로그 필요성을 정리합니다.
7. 기능 요구사항과 비기능 요구사항을 분리합니다.
8. 각 요구사항에 acceptance criteria를 붙입니다.
9. QA 체크리스트로 바꿀 수 있는 검증 항목을 남깁니다.

## Acceptance Criteria 형식
- `Given`: 전제 조건
- `When`: 사용자의 행동 또는 시스템 이벤트
- `Then`: 기대 결과
- `And`: 상태 변화, 로그, 알림, 권한, 오류 메시지 같은 추가 검증

## 산출물 기준
- 요구사항 표: ID, 사용자, 목표, 조건, 기대 결과, 우선순위, 상태
- PRD 상태: draft, active, deferred 및 지연 사유
- 예외/오류 흐름
- 권한과 정책
- 비기능 요구사항: 성능, 보안, 접근성, 운영, 로깅
- acceptance criteria
- QA 연결 체크리스트
- 미정 및 사용자 확인 필요

## 검증
- 요구사항이 “좋게”, “쉽게”, “빠르게” 같은 모호한 표현으로 끝나지 않았는지 확인합니다.
- PRD가 필요한 규모인데 요구사항 표만 있고 사용자 문제, non-goals, release criteria가 빠지지 않았는지 확인합니다.
- 각 핵심 요구사항이 최소 하나의 검증 가능한 기준을 가지는지 확인합니다.
- UI 상태, API 상태, 데이터 상태, 운영 상태가 서로 충돌하지 않는지 확인합니다.
- 문서화가 필요하면 `docs/planning/requirements.md`, `docs/planning/user-scenarios.md`, `docs/qa/test-strategy.md` 후보를 남깁니다.
