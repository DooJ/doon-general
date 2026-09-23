# Reference Evidence Log

디자인 산출물이 외부 레퍼런스, 검색 결과, 사용자 제공 이미지, 기존 제품 화면을 근거로 만들어졌을 때 사용한다. 목적은 “어떤 사이트 스타일을 막연히 따라 했다”가 아니라 “어떤 키워드와 자료를 보고 어떤 디자인 판단으로 번역했는지”를 남기는 것이다.

## 기록 수준

| 수준 | 의미 | 기록 방식 |
|---|---|---|
| `L0: No external reference` | 외부 레퍼런스를 쓰지 않고 기존 제품/요구사항만 사용 | 외부 레퍼런스 없음, 근거가 된 내부 파일/화면만 적는다. |
| `L1: Reference heuristic` | 사이트의 일반적 성격만 기준으로 삼고 실제 화면은 확인하지 않음 | `실화면 미확인`을 표시하고, Mobbin=UX flow, Awwwards=interaction처럼 판단 기준만 적는다. |
| `L2: Search-backed reference` | 키워드 검색이나 사이트 탐색으로 후보를 확인함 | 사이트, 검색어, 후보 URL/title, 확인일, 관찰 포인트를 적는다. |
| `L3: Decision-backed reference` | 특정 화면/케이스가 구체적 디자인 결정에 연결됨 | “자료 -> 관찰 -> 우리 결정 -> 버린 요소”까지 연결한다. |

## 최소 기록 항목

- `기준일`: YYYY-MM-DD와 시간대
- `작업 범위`: 화면, flow, component, landing, brand, design system 중 무엇인지
- `레퍼런스 탐색 목적`: flow, layout, component, color, interaction, copy, proof, pricing 등
- `검색/탐색 경로`: 사용한 사이트, 검색어, 필터, 직접 URL, 사용자 제공 파일
- `선택 자료`: title 또는 화면명, URL 또는 로컬 파일 경로, 접근 가능 범위
- `관찰한 요소`: navigation, hierarchy, density, CTA, state, motion, visual tone 등
- `반영한 결정`: 우리 화면에서 바꾼 layout, component, token, copy, interaction
- `버린 요소`: 도메인 차이, 접근성, 데이터 밀도, 구현 비용, 브랜드 불일치 때문에 제외한 것
- `불확실성`: 유료/로그인 화면, 스크린샷 미확인, 최신성 미확인, 추론 여부

## 기록 템플릿

```markdown
### 레퍼런스 근거

- 기준일: YYYY-MM-DD, Asia/Seoul
- 기록 수준: L0/L1/L2/L3
- 탐색 목적: <flow/layout/component/brand/interaction 등>

| 출처 | 검색어/경로 | 확인 자료 | 관찰한 요소 | 반영한 결정 | 버린 요소/주의점 |
|---|---|---|---|---|---|
| Mobbin | `saas billing settings` | <URL 또는 title> | settings flow, step order | billing tab 구조와 empty state 반영 | paywall copy는 도메인 불일치로 제외 |
| Land-book | `AI SaaS landing` | <URL 또는 title> | hero proof rhythm | hero 아래 proof strip 배치 | 과한 gradient background 제외 |

결정 매핑:
- `<디자인 결정>`: `<자료명/URL>`에서 관찰한 `<패턴>`을 `<우리 맥락>`에 맞춰 `<적용 방식>`으로 변환.
- `<제외 결정>`: `<자료명/URL>`의 `<패턴>`은 `<이유>` 때문에 적용하지 않음.
```

## 작성 원칙

- 레퍼런스를 실제로 검색하거나 열람하지 않았다면 URL을 꾸며내지 않는다.
- 검색 결과 제목이나 썸네일만 본 경우 `후보 확인 수준`으로 표시하고, 구체적 결정 근거로 쓰지 않는다.
- 로그인/유료 화면처럼 직접 확인하지 못한 자료는 `접근 제한` 또는 `실화면 미확인`으로 적는다.
- 사용자가 제공한 스크린샷, Figma, 이미지, 문서는 외부 사이트보다 우선 근거로 삼고 로컬 경로나 파일명을 남긴다.
- 저작권이 있는 화면을 장문으로 베끼지 않는다. 링크, 짧은 관찰 요약, 우리 작업에 반영한 원칙만 남긴다.
- 최종 답변이나 handoff에는 전체 탐색 과정을 길게 쓰지 말고, 사용자가 검증할 수 있는 핵심 자료와 결정 매핑만 압축해 포함한다.
