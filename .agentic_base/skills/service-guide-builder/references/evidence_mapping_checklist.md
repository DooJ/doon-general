# Evidence Mapping Checklist

가이드 설명은 화면별이 아니라 설명 포인트별로 근거를 남기는 것이 좋다.

## 근거 수집 표

| 항목 | 확인할 것 |
|---|---|
| 화면 이름 | 실제 라우트, Activity, Fragment, Screen, Component 이름 |
| UI 구조 | XML, Compose, SwiftUI, JSX/TSX, HTML, 캡쳐 이미지 |
| 문자열 | `strings.xml`, i18n JSON, locale 파일, 하드코딩 문구 |
| 동작 코드 | Controller, ViewModel, handler, service, repository |
| 상태 데이터 | mock 데이터, API schema, local storage, config 파일 |
| 리소스 | 아이콘, 이미지, 폰트, 색상 토큰 |
| 미구현 범위 | mock, 예정, 미연결, 수동 처리 |

## 설명 포인트별 근거

각 핫스팟 또는 단계마다 다음을 채운다.

```text
target: new-job
title: 새 작업 만들기
visible: 사용자가 보는 버튼/카드/상태
action: 클릭하거나 선택했을 때의 동작
result: 다음 화면, 저장 상태, API 호출, 오류 처리
condition: 권한, 연결 상태, 입력값, 모드
sources:
  - components/content-job/content-factory-app.tsx · NewJobDialog
  - lib/validation/content-job.ts
mock_state: 없음 / mock / 예정 / 미연결
```

## 충돌 판단

- 시각적 배치가 코드와 캡쳐에서 다르면 캡쳐를 우선한다.
- 동작과 데이터 흐름이 코드와 설명에서 다르면 코드를 우선한다.
- 제품 코드가 바뀌어야 맞는 경우, 가이드 수정과 앱 수정 범위를 분리해서 사용자에게 말한다.

## 산출물에 드러내기

- 우측 상세 패널에 source를 짧게 표시한다.
- README에는 화면별 주요 근거 파일을 표로 남긴다.
- mock/예정/미연결은 배지나 주의 항목으로 표시한다.
- 변환 스크립트가 있으면 README의 소스 기준에 적는다.
