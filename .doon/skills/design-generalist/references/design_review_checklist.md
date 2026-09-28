# Design Review Checklist

## Review Order

1. 사용자가 이 화면에서 무엇을 해야 하는지 즉시 보이는가
2. 정보 위계와 시선 흐름이 자연스러운가
3. 주요 action이 충분히 강조되고 secondary action이 과도하게 경쟁하지 않는가
4. empty/loading/error/success 상태가 설계되어 있는가
5. 반응형과 접근성 문제가 숨어 있지 않은가
6. 기존 제품의 tone, token, component rule과 충돌하지 않는가
7. 구현 복잡도 대비 효과가 적절한가
8. 선택한 레퍼런스가 이 서비스의 표면 유형, 도메인, 사용 빈도, 데이터 밀도에 맞는가

## Common Failure Modes

- 화면이 예쁘지만 첫 행동이 무엇인지 모호함
- 카드, 배지, 그림자, 색상을 과도하게 써서 hierarchy가 오히려 흐려짐
- 데이터 제품인데 시각적 장식이 데이터 가독성을 해침
- CTA가 많아 우선순위가 사라짐
- 모바일에서 spacing과 touch target이 무너짐
- empty/error 상태를 생략해 실제 사용 시 어색함
- 기존 design system과 다른 토큰을 즉흥적으로 추가함
- Mobbin flow를 보면서도 실제 권한, 데이터, 상태 차이를 분석하지 않고 화면 형태만 따라 함
- Awwwards식 motion이나 브랜드 장식을 반복 업무 화면에 과하게 적용함
- Dribbble shot의 색감과 카드 polish를 상태 matrix 없이 제품 시스템으로 승격함
- Behance case study의 발표용 프로세스를 실제 제품 제약 검증 없이 그대로 따름
- Land-book 랜딩 구조를 앱 내부 화면이나 admin flow에 무리하게 가져옴

## Review Output Format

- `문제`: 무엇이 혼란, 마찰, 불일치를 만드는지
- `영향`: 사용성, 전환, 운영 효율, 구현 비용에 어떤 영향을 주는지
- `개선`: 레이아웃, hierarchy, component, copy, state 기준으로 어떻게 고칠지
- `레퍼런스 적합성`: 참고한 사이트/화면, 검색어/경로, 반영할 요소와 버릴 요소
- `우선순위`: 지금 바로 수정할 항목과 나중에 다듬어도 되는 항목을 구분합니다.
