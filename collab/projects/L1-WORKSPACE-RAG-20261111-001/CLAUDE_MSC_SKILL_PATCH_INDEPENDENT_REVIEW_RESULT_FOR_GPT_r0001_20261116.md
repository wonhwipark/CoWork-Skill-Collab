# CLAUDE 독립 코드·패치 리뷰 결과 — MSC 개발 후보 2종 (GPT 판정용)

- Review ID: `L1-MSC-SKILL-PATCH-20261116-001` / Work `L1-WORKSPACE-RAG-20261111-001` / 작성: Windows Claude Code, 2026-11-16 KST
- 요청서: `CLAUDE_MSC_SKILL_PATCH_INDEPENDENT_REVIEW_REQUEST_r0001_20261116.md`, 고정 입력 commit `29aadbaeb524`.
- **형식:** 사용자가 이 세션에서 직접 요청한 대화형 독립 리뷰다. 감시기 `REQUEST/APPROVAL_SIG/READY` 경로의 정식 리뷰가 아니며 별도 유료 호출은 0이다. 개발자(GPT)와 분리된 세션이고 후보 코드는 한 줄도 수정하지 않았다.
- 증거 등급: **[직접 실행]** 이 PC에서 직접 실행, **[직접 코드]** 고정 ZIP 코드 열람, **[GPT 주장]** 요청서·QA 문서의 주장, **[미실행]**.

## 최종 판정: REVISE

Kernel v0.7.40에 **BLOCKING 회귀 1건**이 있다. doc-converter v0.2.23은 구조가 타당하고 브라우저 검증은 통과했지만 MAJOR 2건·MINOR 3건이 있어 수정 후 재검토가 필요하다. 자체시험 19/19는 두 BLOCKING/MAJOR 결함을 모두 놓쳤다.

## 입력 확인 [직접 실행]

| 대상 | 크기 | SHA-256 | 요청서 일치 |
|---|---:|---|---|
| doc-converter v0.2.23 | 210,426 | `43805ae0…ce23e` | 일치 |
| work-ledger-kernel v0.7.40 | 410,922 | `b8077fd7…df7ce` | 일치 |
| 비교 기준 Kernel v0.7.39 | 409,355 | (blob은 요청서와 같은 commit에서 받음) | — |
| 비교 기준 doc-converter | PUBLIC v0.2.21 `ef5d1d9e…1039a` | 일치(요청서에 적힌 PRIVATE v0.2.22 ZIP은 고정 commit의 `candidates/`에 없음) | 아래 참고 |

참고: 요청서가 보존했다고 한 `doc-converter_v0_2_22_1116.zip`은 commit `29aadbae`의 `candidates/` 목록에 없어(404) v0.2.21→v0.2.23 직접 diff로 검토했다. v0.2.22 중간 diff는 NOT_RUN.

## 지적 (심각도 순)

### 1. [BLOCKING] Kernel v0.7.40: SVG Evidence가 있는 Work의 `export_docs` 전체가 실패한다 — work-ledger-kernel
- 위치: `work_ledger_kernel/work_ux.py` `export_docs`의 복사 조건(843~845행)과 `work_ledger_kernel/artifact_names.py` `name_for`(30~31행).
- 원인 [직접 코드]: 패치가 복사 허용 확장자에 `.svg`를 추가했지만 `name_for`는 `.md/.txt/.html/.json`만 허용하고 그 외는 `ValueError('UNSUPPORTED_PUBLISHED_ARTIFACT')`를 낸다. `export_docs`는 이를 `KernelError("ARTIFACT_NAME_INVALID")`로 바꿔 던진다.
- 재현 [직접 실행]: 같은 합성 Work(SVG Evidence 1개 + MD Evidence 1개)에 `export_docs`를 호출. **v0.7.39: 정상 종료, MD만 게시(SVG 무시). v0.7.40: `ARTIFACT_NAME_INVALID | UNSUPPORTED_PUBLISHED_ARTIFACT`로 실패하고 정상이던 MD도 게시되지 않음.**
- 영향: 기능이 동작하지 않을 뿐 아니라 기존에 정상이던 Work의 문서 내보내기가 깨지는 회귀다. MSC가 아닌 SVG(예: 첨부 그림)에도 같다.
- 자체시험이 놓친 이유 [직접 코드]: `tests/test_msc_svg_export_v0740.py`는 `inspect.getsource(WorkUX.export_docs)`에 문자열 `'MSC_SVG_TOO_LARGE'`, `'".svg"'`, `'ARTIFACT_MAP_CONFLICT'`가 있는지만 검사한다. 동작을 실행하지 않아 위 실패를 잡을 수 없다.
- 최소 수정: ① `name_for` 허용 확장자에 `.svg` 추가(또는 SVG 전용 이름 규칙). ② 크기 초과 예외와 복사는 MSC 계열 Evidence kind로 한정해 무관한 SVG가 전체 내보내기를 막지 않게 한다(기존 `.html/.md` 큰 파일의 조용한 건너뜀은 유지). ③ 행동 시험 3종: SVG 정상 게시와 `published_path`/해시 매핑, 상한 초과 거부, 비 MSC SVG 처리. ④ 복사되는 SVG는 `<script>`·`on*=`·외부 href가 없는지 확인하는 단계를 검토(뷰어는 `<img>` data URL이라 안전하지만 게시된 SVG 파일을 직접 여는 호스트에서는 아님). 담당: work-ledger-kernel.
- 제안: 수정 수용 / 수정 후 재검토 필수.

### 2. [MAJOR] doc-converter: 등록된 관리 실행 정책 경로에서는 `--view-mode`를 쓸 수 없다 — doc-converter
- 위치: `skillsilent/policy.json`의 `msc-package`, `msc-scenario-build` 액션 `allowed_flags`(둘 다 `--view-mode` 없음), `scripts/scenario_ir_adapter.py`(`view_mode` 전달 없음).
- 근거 [직접 코드/실행]: dc23 policy에서 `view-mode` 출현 0건(dc21과 같음). `msc-scenario-build`는 어댑터가 payload에 `view_mode`를 넣지 않고 정책이 플래그도 막아 **Procedure/Feature 모드에 도달할 방법이 없다.** `msc-package`는 입력 JSON에 `view_mode`를 직접 넣을 때만 가능.
- 자체시험이 놓친 이유: 신규 시험이 `msc_tool.py`를 직접 호출해 정책 게이트를 거치지 않는다.
- 영향: 요청서 질문 4의 "scenario-build/package의 `--view-mode` API"가 실제 호출 경로(`skillsilent run`)에서는 사용 불가. 이슈 모드 기본 동작은 보존된다.
- 최소 수정: 두 액션에 `--view-mode` 값 플래그를 추가하고 어댑터가 값을 payload로 전달. 정책 경유 시험 1개(두 액션에서 PROCEDURE_FEATURE가 실제로 적용됨)를 추가. 담당: doc-converter.

### 3. [MAJOR] doc-converter: 대소문자만 다른 이름은 Windows에서 조용히 덮어쓴다 — doc-converter
- 위치: `msc_tool.py` `cmd_package`의 이름 정규화와 `name in specs_by_name` 중복 검사(대소문자 구분).
- 재현 [직접 실행, Windows NTFS]: 이름 `["Init","init"]` → **종료 코드 0, status `PARTIAL`, diagram 2건, `.puml` 파일 1개(`Init.puml`)** — 두 번째가 첫째를 덮어쓴다. 렌더러가 있으면 SVG/HTML도 같다. 같은 시험에서 한글 이름 2개는 해시 접미사로 구분됐고 동일 이름은 정상적으로 `BLOCKED`.
- 영향: 요청서 질문 2의 "같은 정규화 결과로 덮어쓰지 않는지"에 대한 반례. 수정된 한글 처리와 별개의 경로다.
- 최소 수정: 중복 검사를 `name.casefold()`로 하고 충돌 시 기존과 같이 `DIAGRAM_NAME_DUPLICATE`로 hard fail. 시험 추가. 담당: doc-converter.

### 4. [MINOR] 패키지 무결성·버전 메타가 서로 맞지 않는다
- doc-converter [직접 실행]: `PACKAGE_CONTENTS.sha256`의 3개 항목(`.skill-release.json`, `VERSION`, `scripts/msc_tool.py`) 해시 불일치, 5개 파일 미등재(`msc_b_viewer.py`, 신규 시험 2개, `DEVELOPMENT_*` 2개). `VERSION`·`.skill-release.json`은 0.2.23이나 `SKILL.md`·`VERSION.md`·`skillsilent/manifest.json`은 0.2.21.
- Kernel: `MANIFEST_SHA256.json`은 163개 전부 일치·미등재 0이고 `VERSION` 0.7.40-dev.1. 단 `SKILL.md`는 `0.7.38-dev.1`.
- 영향: 이 목록으로 설치 무결성을 검증하는 소비자가 있으면 실패한다. 코드에서 `PACKAGE_CONTENTS.sha256`을 참조하는 곳은 찾지 못했다. 사내 설치기·Updater의 사용 여부는 **추가 확인**.
- 최소 수정: 릴리스 빌드 단계에서 목록·버전을 재생성. 담당: 각 스킬 릴리스 절차.

### 5. [MINOR] 같은 한글 이름이 유니코드 정규화에 따라 다른 파일 이름이 된다 — doc-converter
- 재현 [직접 실행]: `한글초기화`의 NFC와 NFD가 각각 `diagram_e0f60216d4`, `diagram_98ed374656`. 해시가 `raw_name`을 정규화 없이 만든다.
- 영향: 같은 이름을 다른 입력 경로(예: 다른 OS 입력)로 다시 게시하면 파일 이름·링크가 달라져 멱등성이 깨지고, 서로 다른 형식으로 들어온 동일 이름은 중복으로 잡히지 않는다.
- 최소 수정: 해시 전에 `unicodedata.normalize('NFC', ...)` 적용. 시험 1개. 담당: doc-converter.

### 6. [MINOR] B HTML의 단계 버튼 누락이 보이지 않는다 / 실제 렌더 SVG 미확인 — doc-converter
- 근거 [직접 코드/실행]: 단계 라벨이 SVG의 다른 텍스트와 같으면(예: 참가자·메시지와 동일) 버튼이 조용히 빠진다. 안전한 동작이나 사용자와 manifest에 이유가 남지 않는다. 또 이 PC에는 PlantUML 렌더러가 없어(`RENDERER_MISSING`) 패키지 경유 HTML 생성 경로는 실행하지 못했고, 실제 PlantUML SVG의 divider 텍스트 형식은 **미확인**.
- 최소 수정: manifest에 `html_phase_buttons: n/m` 같은 요약 기록. 실제 렌더러가 있는 환경에서 패키지 경유 1회 시험(NOT_RUN 해소). 담당: doc-converter.

## 독립 검증과 자체시험 구분 (요청서 질문 3·7)

| 항목 | 상태 |
|---|---|
| 자체시험(Actions 3.10/3.11 표적 19/19, Chromium synthetic screenshot) | **[GPT 주장]** 이 PC에서 재현하지 않음. 그 시험은 위 지적 1·2·3을 잡지 못했다 |
| 신규 시험 5건(doc-converter) 재실행 | **[직접 실행]** 5 passed (Python 3.11, venv) |
| Kernel 신규 시험 1건 | 문자열 존재 검사. 동작 증명 아님 — 지적 1 |
| B HTML 실제 브라우저(Edge headless, CDP) | **[직접 실행]** 적대적 제목(`"><img onerror>`)·SVG 내 `<script>` 입력에서 스크립트 추가 실행 0, `window.__pwn` 미설정, 주입된 `img` 없음(`<img>` 1개만), CSP 위반·콘솔 오류 0, 이미지 로드(naturalWidth 800), 단계 클릭 시 스크롤 2117(식 기대값과 일치), 확대 125%, 최소 50%, 중복 라벨·없는 라벨 버튼 비생성. 한계: 위치 기대값은 같은 공식이라 부분적으로 순환적이고, 단계 이동의 시각적 정렬(글자가 화면 맨 위에 오는지)과 실제 PlantUML SVG는 미확인 |
| Kernel 실제 `export_docs`(SVG Evidence) | **[직접 실행]** 지적 1 재현 |
| 대소문자·NFC/NFD 이름 | **[직접 실행]** 지적 3·5 재현 |
| Python 3.10 | **[미실행]** 이 PC는 3.11만 있음 |
| 기존 전체 pytest, Phase click의 모바일/다른 브라우저, 실제 원격 `published_path`/Markdown writer/업무 host E3 | **[미실행]** |

## 질문별 판정 (R1~R7)

1. 기존 동작 보존·최소성: **수정 수용.** 이슈 모드 기본은 시험 1건으로 보존되나 Kernel은 회귀(지적 1). `.svg` 허용만 추가한 방향(기존 export 재사용)은 타당하고 더 단순한 대안은 지적 1의 수정 외에 없다.
2. 이름 충돌/경로: **수정 수용.** 한글·동일 이름은 개선됐으나 대소문자(지적 3)와 NFC/NFD(지적 5)가 남는다.
3. B HTML 보안/정확성: **수용(조건부).** 브라우저 검증을 통과. 호스트에 HTML 실행 URL이 없을 때의 SVG→다운로드→원본 순서 폴백 판정은 호스트 정책 미확인이라 **보류**. 렌더러 있는 실제 SVG 확인 필요(지적 6).
4. AS-IS·모드/manifest: **수정 수용.** 이슈 문구와 없는 `MSC_DELTA.md` 링크 억제는 코드에서 확인. `--view-mode` 정책 경로 미연결(지적 2). 렌더 실패 시 `VIEWER_FAILED`로 hard fail, 2 MiB 초과 거부는 코드에서 확인(실행은 미실행).
5. Kernel SVG: **거절(현 상태).** 지적 1.
6. 두 진입×두 목적지: **보류.** writer G0 미접근이라 입증되지 않은 구현을 요구하지 않는다. 필요 계약은 이전 구조 리뷰(`CLAUDE_MSC_MD_LINK_STRUCTURE_INTERACTIVE_REVIEW_FOR_GPT_20261115.md`) 지적 5와 같다.
7. 시험의 반증: **수행.** 지적 1·2·3·5가 자체시험이 놓친 반례다.

## 수용하지 않은 것 / 한계

- 코드 수정 없음, 설치 없음, PUBLIC 배포 없음, 별도 유료 호출 없음. 후보 ZIP은 원본 바이트 그대로 읽었다.
- 이 리뷰의 독립 근거는 위 [직접 실행] 항목에 한정된다. Linux, 사내 소형 LLM, 업무 호스트 설치본, 실제 writer는 검토하지 않았다.
- 수정은 GPT 판정 뒤 동일 Work에서 개발하고, 수정자가 아닌 세션이 재검토하는 것이 요청서 조건이다.
