# Workspace 분석 문서 → HTML → MSC 열람 구조 검토 — r0001

- 확인: 2026-11-15 KST / 기존 Work `L1-WORKSPACE-RAG-20261111-001`
- 사용자 요구: Updater/Workflow의 분석 MSC를 개인 업무용 `l1-workspace`에서 바로 탐색. 분석 문서의 링크로 HTML을 열고 그 안에서 MSC 이미지를 열람.
- 피드백 판정: **수용 / 기존 B HTML+SVG 방향 재사용**. 실제 업무용 폴더·호스팅은 아직 미확인.

## 확인한 근거와 접근 범위

- `L1_WORKSPACE_RAG_DESIGN_r0002_20261111.md` blob `44d7bc056f203b1c7d82b44532ef7be410e82d33` §4 및 기존 Kernel 정적 계약: 루트 README, `works/<Work-ID>/`, Work의 README/문서안내·분석 문서·artifacts/state, `index/active.json`·`latest.json` 구조.
- 해당 문서의 구조는 **설계/과거 패키지 정적 확인**이며 업무용 저장소의 최신 원격 tree 실측이 아님. 실제 `artifacts/analysis`, `module-library` 존재나 현재 설치 API 지원을 확정하지 않음.
- 같은 문서는 기존 Kernel `WorkUX.export_docs()`의 루트 README/index 생성과 `work_docs_navigation.py`의 존재하는 `CODE_FACTS.md`·`MSC_VIEW.md` 안내를 기술. 원장/export를 우회하는 별도 목차 생성기나 README 수동 덮어쓰기를 기본 도입하지 않음.
- PUBLIC 인계서 `wonhwipark/L1Work/main/handoffs/L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md` §1.3·3·5·7: HTML 안의 SVG, 확대·스크롤·단계 이동, 문서의 MSC 보기 링크, 생성/게시/렌더링 URL의 분리.
- 업무용 `l1-workspace`의 실제 호스트/URL·현재 tree·설치본·기존 HTML 호스팅 경로는 이번 세션에서 조회하지 못함. GitHub.com의 동명 저장소를 대체 조회하지 않음.

## 추천: 문서에서 미리보기 + HTML에서 확대 열람

1. Work README/문서안내 → 분석 문서(`CODE_FACTS.md` 등 실제 기존 문서)로 진입.
2. 분석 문서에 핵심 설명·짧은 MSC 미리보기와 **MSC 확대 보기** 링크를 함께 제공. 미리보기는 같은 입력의 SVG 또는 호환 출력 이미지.
3. HTML은 같은 source revision/분석 개정의 MSC SVG를 내장하고 확대·가로/세로 스크롤·시나리오/단계 이동·분석 문서 돌아가기를 제공.
4. 여러 MSC가 있는 Work는 기존 안내기가 인식하는 `MSC_VIEW.md`를 우선 검토. 시나리오·AS-IS/TO-BE·source 기준·검증 상태·뷰어 링크를 표로 제공.
5. Work 목록/업무 문서 연결은 기존 Kernel export 경로에서 유지. Updater·Workflow 모두 같은 converter 결과와 같은 Work 참조를 사용.

### 배치 예시 — 실제 경로 확정 전 제안

| Work 기준 상대 위치 | 내용 |
|---|---|
| `README.md` / `문서안내.md` | 기존 Work 진입·분석 문서 및 MSC 목록 연결 |
| `CODE_FACTS.md` 등 기존 분석 문서 | 설명·출처·MSC 미리보기·HTML 뷰어 링크 |
| `MSC_VIEW.md` (없다면 기존 계약으로 생성 가능 여부 확인) | 여러 시나리오의 MSC 목록·기준 revision·뷰어 진입 |
| `artifacts/analysis/msc/<scenario>/<analysis-revision>/viewer.html` | SVG를 포함한 HTML 열람본 |
| 같은 출력 묶음의 `msc.svg` | Git 문서 미리보기·독립 그림 |
| 같은 출력 묶음의 기존 MSC 원본 | 재변환·분석 재사용용 텍스트/구조/PUML 등 실제 converter 출력 |

파일명·상세 하위 경로는 예시. 설치된 converter/Kernel의 출력 경로·등록 계약을 먼저 적용. HTML·SVG·원본을 같은 입력에서 생성하는 표현 산출물로 묶고 수동으로 서로 다른 내용을 유지하지 않음. `module-library` 등 새 상위 구조를 이번 요구만으로 만들지 않음.

## HTML ‘파일 링크’와 ‘열람 URL’의 차이

Git 저장소의 HTML 파일 화면과 HTML/CSS/JS를 제공하는 웹 호스팅은 별개. 기존 B 인계서도 소스 화면/raw/download와 렌더링된 URL을 구분하도록 명시. HTML을 저장했다는 이유만으로 문서의 클릭 열람 완료를 선언하지 않음.

- 기존 업무 GitHub Pages 또는 승인된 문서/정적 웹 경로가 **이미 있고 접근 범위가 맞는 경우**: 문서의 확대 보기 링크를 실제 렌더링 URL로 연결.
- 그러한 경로가 미확인/사용 불가한 경우: 문서의 MSC 미리보기는 유지하고 HTML은 SVG를 내장한 단일 파일로 내려받아 열람하는 대안 제공. 다운로드 방식은 ‘웹에서 클릭 즉시 뷰어’와 구분.
- 개인 PRIVATE 저장소라는 이유만으로 Pages도 동일한 비공개 범위라고 추정하지 않음. 실제 제품 버전·조직 설정·인증/접근 범위를 확인. 새 호스팅·권한/공개 설정 변경은 이번 검토에서 수행하지 않음.
- 회사 코드·상세 MSC를 PUBLIC 대시보드나 CoWork PRIVATE에 복제하지 않음. 본 메모에는 비민감 구조·역할 제안만 기록.

공식 참고:
- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax (상대 링크·이미지)
- https://github.com/github/markup (GitHub 문서 렌더링·HTML 정리)
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages (HTML/CSS/JS 웹 호스팅)
- https://docs.github.com/en/enterprise-server@3.19/admin/configuring-settings/configuring-user-applications-for-your-enterprise/configuring-github-pages-for-your-enterprise (환경에 따라 Pages/공개 범위 설정이 다름; 현재 업무 호스트 버전 확인 결과 아님)

## 역할과 다음 한 동작

`code-analyzer` = 분석 사실·MSC 근거, `doc-converter` = 같은 입력의 MSC 원본·SVG·HTML 표현, 두 호출 스킬 = 자기 결과의 Workspace 갱신·연결, Kernel = 기존 Work/Evidence/안내 export, 기존 Git/호스팅 제공자 = 실제 파일·렌더링 URL·접근 확인.

다음 한 동작은 업무 GPT/로컬 Agent가 **기존 Work 하나**로 실제 폴더와 converter 출력을 읽기 전용 확인하고, 분석 문서 → HTML URL → 내장 MSC 표시를 브라우저에서 확인 가능한 경로에 매핑하는 것. 이미 유효한 분석을 열람 확인 때문에 다시 실행하지 않음.

판정: `DOCUMENT_STRUCTURE_REVIEW=COMPLETE`, `LIVE_WORKSPACE_TREE=NOT_VERIFIED`, `HTML_HOSTING=NOT_VERIFIED`, `DOC_TO_HTML_TO_MSC_E2E=NOT_RUN`. 이번 범위는 검토·제안·비민감 기록이며 스킬 구현/설치·업무 저장소 변경·분석/Job 재실행·새 유료 리뷰·PUBLIC 게시 없음.
