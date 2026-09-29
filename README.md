<p align="center">
  <img src="./assets/brand/doon-logo.svg" alt="DooN — DO:ON" width="720">
</p>

<p align="center"><strong>Turn broad ideas into useful, finished work.</strong></p>

<p align="center">
  <img src="./assets/brand/doon-hero.png" alt="DooN General skill network" width="100%">
</p>

# DooN General

**DooN General**은 기획, 디자인, 조사, 문서화와 일상 업무를 실행 가능한 결과로 연결하는 공개 Codex·Claude Code 플러그인입니다. 플러그인 전체와 내부 스킬을 각각 활성화할 수 있어 필요한 역할만 조합해 사용할 수 있습니다.

## 포함된 영역

| 영역 | 주요 스킬 |
|---|---|
| 제품 기획 | `product-planner`, `requirements-analyst`, `content-strategist` |
| UX·정보 구조 | `ux-researcher`, `information-architect`, `interaction-designer` |
| UI·디자인 시스템 | `ui-concept-director`, `design-generalist`, `design-system-curator`, `refining-implemented-ui` |
| 문서와 서비스 안내 | `living-doc-writer`, `snapshot-report-writer`, `service-guide-builder` |
| 조사와 전문 판단 | `stock-analyst`, `real-estate-expert`, `project-legal-advisor` |
| 여행 | `travel-planner`와 항공·숙박·장소·교통·일정 조사 스킬 |
| 개인 활동 | `pt-trainer` |

## 동작 방식

요청의 목적과 필요한 결과물을 먼저 정리한 뒤, 적합한 전문 스킬이 조사·구조화·작성·검토를 맡습니다. 여러 스킬이 함께 쓰일 때도 각 역할의 입력과 산출물을 분리해 결과가 어디에서 만들어졌는지 추적할 수 있게 합니다.

제품·디자인·문서 스킬을 기본 영역으로 두고, 여행과 전문 생활 영역은 필요한 스킬만 선택해 활성화하는 구성을 권장합니다. 모든 스킬은 Core 없이 동작하며, DooN Core가 연결된 경우 공통 규칙을 추가로 적용합니다.

## 설치와 설정

### DooN Core와 함께 설치

여러 DooN 플러그인을 함께 사용할 때 권장하는 방식입니다. GitHub CLI에 로그인한 뒤 Core를 clone하고 bootstrap을 한 번 실행합니다.

```bash
gh auth login
git clone https://github.com/DooJ/doon-core.git DooN
cd DooN
bash scripts/bootstrap_doon.sh
```

처음 설치하면서 `doon-general`만 고르려면 마지막 명령에 `--interactive`를 붙이고, 이 저장소는 전체 선택하고 나머지는 건너뜁니다. bootstrap은 Codex에 플러그인을 설치하고 Claude Code가 있으면 Claude에도 설치합니다. 완료 후 새 Codex 또는 Claude 세션을 시작하면 되며, 작업 프로젝트에 `.doon`을 복사할 필요는 없습니다.

이후 소스와 Codex·Claude 설치 상태를 함께 최신화하려면 Core에서 bootstrap을 다시 실행합니다. 기존 플러그인 선택은 그대로 유지됩니다.

```bash
cd /path/to/DooN
bash scripts/bootstrap_doon.sh
```

### 이 저장소만 개발·시험

Core 없이 소스만 확인하거나 Claude Code에서 바로 시험할 수 있습니다.

```bash
git clone https://github.com/DooJ/doon-general.git
cd doon-general
claude plugin validate .
claude --plugin-dir "$PWD"
```

`--plugin-dir`는 해당 Claude 세션에만 적용됩니다. Codex에 지속 설치하려면 이 저장소를 가리키는 marketplace 항목이 필요하며, DooN 사용 환경에서는 위 Core bootstrap이 그 항목과 설치 상태를 자동으로 관리합니다. 별도 환경에서는 조직 또는 개인 marketplace에 `doon-general`을 등록한 뒤 `codex plugin add doon-general@your-marketplace`로 설치합니다.

## 구조

- `.codex-plugin/plugin.json`: 플러그인 메타데이터와 `skills/` 등록
- `.claude-plugin/plugin.json`: Claude Code 네이티브 플러그인 메타데이터
- `skills/<이름>/`: 실제 스킬 원본, 버전, references, scripts, assets
- `catalog.json`: 저장소와 스킬 소유권을 확인하는 카탈로그
- `PLUGIN_VERSION.md`: 플러그인 단위 변경 이력과 출처

각 스킬의 버전과 출처는 해당 폴더의 `VERSION.md`에서 관리합니다. 외부 원문을 포함한 스킬의 개별 라이선스도 함께 보존합니다.

> 이 저장소는 DooN Core 없이 독립 실행할 수 있으며 프로젝트에 `.doon`을 생성하지 않습니다. Core 사용자는 이 플러그인을 동일한 plugin ID로 통합 관리합니다.
