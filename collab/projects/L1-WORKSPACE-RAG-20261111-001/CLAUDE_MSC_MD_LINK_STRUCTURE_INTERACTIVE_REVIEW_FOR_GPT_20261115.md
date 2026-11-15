# CLAUDE 구조 검토 — MSC · Procedure/Feature MD 링크 (GPT 판정용, 대화형)

- 대상: `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001` rev 1, package_rev `structure-r0001`, ZIP 38,132 B, sha256 `90bb61a0…907d` (원격 raw 바이트 재해시 일치, 8개 파일 확인), SOURCE_PIN commit `013b9f26fde9`.
- 작성: Windows Claude Code, 2026-11-15 KST. **사용자가 이 세션에서 직접 요청한 대화형 정적 검토**다. 정식 감시기 경로의 `POLICY-STATIC-V1` 독립 리뷰가 아니다.
- 상태: `INDEPENDENT_REVIEW(감시기·유료)=NOT_RUN`, APPROVAL_SIG·READY 게시 0, 새 유료 모델 호출 0, 실행·설치·게시 시험 0. 정식 결과(`REVIEW_RESULT_1.md`)·영수증은 만들지 않았다. 이 문서는 그 대신이 아니다.
- 읽은 것: 패키지 8개 파일 전부(00→01→02→03 순, 이어서 04~07), 요청서, SOURCE_PIN, SUBMISSION_STATUS, HOST_SUBMIT_ONESHOT. 로컬 지식 스냅샷(START_HERE, OPERATING_*)은 이번에 다시 읽지 않았다. 요청서가 자기완결이라 판단했고, 이는 한계다.
- 근거 수준: **[직접]** 03의 원문 발췌를 서로 대조해 확인. **[GPT]** 02의 주장이며 발췌로 확인 못 함. **[추론]** 발췌 밖 동작을 추정. 아래 각 항목에 표시한다.

## 최종 판정: ACCEPT_WITH_CHANGE

두 진입·같은 Work·converter는 표현만 만들고 대상 writer가 링크를 연결하는 분리는 타당하다. BLOCKING은 없다. 아래 MAJOR 5건과 MINOR 1건을 반영하면 진행해도 된다. 두 진입 구조를 뒤집는 지적은 없다.

## R01~R10 판단표

| ID | 판정 | 근거 |
|---|---|---|
| R01 | 수용 | [직접] `build_msc_handoff`가 `publication.github_push=False`, `record.owner=work-ledger-kernel`로 converter에 writer·원장이 없다. `view_work_msc`는 읽기 전용(`read_only/saved=False`). 04 §3A와 일치. Updater 직접 저장 API는 NOT_VERIFIED로 남는다. |
| R02 | 수정 수용 | 지적 1. 입력 클래스 계약이 문서 사이에서 엇갈린다. |
| R03 | 수정 수용 | 지적 4, 6. "재사용"이 과장됐고 다중 MSC 이름 충돌 가능성이 있다. |
| R04 | 수정 수용 | 지적 2. F2 해석은 정확하며 깨짐은 가능성이 아니라 확정이다. 확장 범위를 더 좁힐 수 있다. |
| R05 | 수용 | [직접] `group-knowledge`가 읽기 전용임(SKILL 16~18행)을 F4가 맞게 짚었다. 그룹 writer·독자 권한은 설치 I/O 확인 항목으로 남는다. |
| R06 | 추가 확인 | 지적 5. "MSC 절만 갱신"의 근거 발췌와 소유권 규칙이 없다. |
| R07 | 수정 수용 | 단계 분리·링크 마지막·Work 역링크만 복구는 타당. 단, 무음 건너뜀 때문에 게시 목록 대조가 완료 조건에 들어가야 한다(지적 2). |
| R08 | 수용 | [직접] 05가 "converter 자동 생성 아님"을 스스로 밝힌다. 보완: 샘플의 단계 이동 PASS는 고정 좌표라 일반화 증거가 아니고(F1이 이미 인정), 공개 baseline의 group-knowledge는 SKILL상 "개발 후보"(14행)다. |
| R09 | 수정 수용 | 지적 3. 호스트가 HTML을 못 보여줄 때의 동작이 02에 정의돼 있지 않다. |
| R10 | 수정 수용 | 순서는 타당. 더 적은 변경 대안과 두 진입×두 목적지 완료 기준은 아래 "대안" 참고. |

## 핵심 지적 (6건)

### 1. [MAJOR] 어떤 입력이 B 뷰어를 구동하는지 문서끼리 어긋난다 (R02, R10)
- 근거: 02 §2는 code-analyzer의 기존 `msc_ref`/PUML을 재사용하고 재분석하지 않는다고 한다. 그런데 [직접] `scenario_msc.py:60`의 `projection_policy`는 `ONLY_VERIFIED_IR; no raw .puml`, `:65`는 `require_verified_scenario_ir=True`. `msc_tool.py:306~310`은 `is_user_scenario(sp)`일 때만 Phase·근거 유형·소스 revision을 쓴다.
- 영향: Procedure/Feature용 code-analyzer 산출물(결정형 spec/PUML, SKILL 83행)이 시나리오 IR이 아니면, 02의 표시 예시에 있는 "시나리오·분석 기준·source revision" 줄과 단계 이동에 쓸 Phase를 채울 입력이 없다. 반대로 IR을 요구하면 "재분석 없음"과 부딪힌다. [추론] code-analyzer 산출물이 IR로 변환되는지는 발췌로 알 수 없다.
- 최소 수정: 입력 클래스 3종(검증된 시나리오 IR / code-analyzer semantic spec / 원본 PUML→`msc-export`)과 각각이 만드는 산출물(SVG, Phase, source revision, 단계 이동 가능 여부)을 한 장 표로 고정한다. Procedure/Feature 기본 경로를 하나 지정한다.
- 담당: doc-converter(입력 매핑), code-analyzer(spec 제공).
- 검증: 같은 Procedure MSC로 Workflow 진입과 Updater 진입이 동일한 매니페스트·SVG 해시를 만든다.

### 2. [MAJOR] F2는 "확인 필요"가 아니라 확정 결함이고, 일부 누락은 소리 없이 지나간다 (R04, R07)
- 근거 [직접]: `work_ux.py:842`의 복사 조건은 `.md/.html/.json/.txt` + `copy_small_evidence` + `max_copy_bytes` 이하다. 조건 불충족 시 `else`·예외가 없다(842~864 범위). `msc_tool.py:314`는 MSC_VIEW.md에 `![..](<name>.svg)` 상대 링크를 쓴다. `work_ux.py:846`은 게시 파일명을 `name_for(category, …, eid)`로 바꾼다. `:855~859`는 같은 Evidence의 경로·해시가 다르면 충돌 오류를 낸다.
- 영향: (a) MSC_VIEW.md는 복사되고 SVG/PUML은 복사되지 않아 게시본의 이미지 링크가 깨진다. (b) 이름이 바뀌면 `MSC_DELTA.md`·`MSC_TRACEABILITY.json` 상대 링크도 깨진다. (c) 상한을 넘은 큰 HTML 뷰어는 오류 없이 빠지므로 링크가 허공을 가리킨다. (d) 링크를 고쳐 쓴 본문을 같은 Evidence의 복사본으로 낼 수 없다.
- 최소 수정: ① 링크는 export가 쓰는 artifact map의 `published_path`에서 만든다. 원본 복사본을 고쳐 쓰지 않는다. ② 완료 조건에 "게시된 파일 목록 = 기대 목록"을 readback으로 대조하는 단계를 넣는다. ③ 확장 범위는 미리보기용 `.svg` 하나와 그 크기 상한으로 좁힌다. 뷰어는 SVG를 내장한 단일 `.html`로 만들면 `.html`이 이미 허용 확장자라 Kernel 변경이 필요 없다.
- 담당: work-ledger-kernel(필요 시 svg 1종), doc-converter(단일 HTML).
- 검증: SVG만 빠진 상태, 상한 초과 HTML, 이름 변경 후 `MSC_DELTA.md` 링크가 각각 감지되는 시험.

### 3. [MAJOR] 렌더링 URL을 못 구했을 때의 동작이 02에 없다 (R09)
- 근거: 07은 "미확인이면 미리보기는 유지하고 HTML은 내장 단일 파일 다운로드 대안, 다운로드와 클릭 열람을 구분"을 정의했다. 02(판단 대상)는 시험 목록에 "host URL 없음"만 적고 동작은 비어 있다. 05의 PASS는 PUBLIC github.io에서만 확인됐고 그룹·사내 호스트가 아니다.
- 영향: 사내 호스트가 HTML/SVG를 렌더링하지 않거나 스크립트를 막으면 "MSC 확대 보기" 링크가 소스 화면으로 열려 R09가 경고한 무의미한 링크가 된다. [추론] GitHub 계열 호스트는 raw HTML을 텍스트로 주거나 샌드박스 CSP를 붙이는 것이 일반적이나, 이 업무 호스트의 정책은 확인되지 않았다.
- 최소 수정: 폴백 사다리를 02에 못박는다. ① 렌더링 URL이 읽기 확인됨 → "MSC 확대 보기". ② 없음 → 미리보기 유지 + SVG 직접 링크 + 내장 HTML 다운로드 안내(라벨에 "열람"을 쓰지 않음). ③ SVG도 불가 → 원본/PUML 링크 + "그림 미완료". ④ 아무것도 없음 → MSC 절을 만들지 않는다. "확대 보기" 라벨은 URL 확인 플래그가 있을 때만 쓴다.
- 담당: 대상 writer(링크 판정), doc-converter(단일 HTML).
- 검증: 호스트 URL 없음/스크립트 차단 모의에서 ②~④가 각각 나오고 빈 링크가 0.

### 4. [MAJOR, 조건부] 여러 MSC에서 한글 이름이 충돌해 그림이 덮어쓰인다 (R03, R06)
- 근거 [직접]: `msc_tool.py:862`는 `re.sub(r"[^A-Za-z0-9_.-]+", "_", …)`로 이름을 만들고, 859~895행에 중복 검사가 없다. `specs_by_name[name] = spec`(875행)과 `{name}.puml/.svg`(882·885행)는 같은 이름이면 서로 덮어쓴다.
- 영향: 시나리오 이름이 한글이면 한글 구간이 전부 `_`가 된다. 예를 들어 이름이 "초기화"와 "종료"이면 둘 다 `_`가 되어 두 번째 그림이 첫째를 덮고, 둘 다 `READY`로 표시된다. 한 Procedure/Feature에 MSC가 여러 개인 경우(R06)와 직결된다. [추론] 상위 호출자가 항상 ASCII 고유 이름을 넘기는지는 발췌로 알 수 없다. 그래서 조건부다.
- 최소 수정: 정제 후 이름이 겹치면 `DIAGRAM_NAME_DUPLICATE`로 hard fail 하거나 순번 접미사를 붙인다. 호출 계약에 고유 ASCII id를 명시한다.
- 담당: doc-converter.
- 검증: 한글 이름 2개 입력이 서로 다른 SVG 2개와 서로 다른 링크 2개를 만든다.

### 5. [MAJOR] "MSC 절만 갱신"을 누가·어떤 마커로 하는지 근거와 소유권 규칙이 없다 (R06)
- 근거: 02 §5는 "기존 생성 마커/본문 보호를 재사용"한다고 하고, §2는 이를 `generated_doc_registry.py`/`work_docs_navigation.py`와 code-analyzer의 "HLD marker·msc_ref"에 건다. 03에는 그 파일들의 발췌가 없고, SKILL 78~89행에도 HLD marker·msc_ref가 없다. [GPT]
- 영향: Procedure/Feature MD 본문은 code-analyzer(재생성), Updater, 그룹 writer가 모두 건드릴 수 있다. 소스 revision이 바뀌어 code-analyzer가 본문을 재생성하면 삽입한 MSC 절이 사라지거나 옛 링크가 새 분석 옆에 남을 수 있다. Kernel의 수동 문서 보호는 Work 문서용이라 Procedure/Feature 지식 MD에 같은 보호가 적용된다는 증거도 아니다.
- 최소 수정: MSC 절의 소유자를 하나로 정한다. 기본안은 대상 writer가 마커 한 쌍으로 절을 소유하고, 절 안에 source revision을 적어 현재 분석 revision과 다르면 "오래됨"으로 표시하는 것이다. code-analyzer 재생성이 마커 구간을 보존하는지는 설치본에서 좁게 확인할 항목으로 남긴다. 설치 I/O 확인 목록에 두 마커 파일을 추가한다.
- 담당: 대상 writer(Updater/그룹), code-analyzer(보존 계약).
- 검증: 같은 입력 재게시 시 링크 중복 0, 수동 문단 보존, 재생성 후 절 유지, revision 불일치 시 오래됨 표시.

### 6. [MINOR] B 뷰어는 "일반 HTML 변환 재사용"이 아니며, 단계 좌표와 MSC_VIEW 문구는 그대로 쓸 수 없다 (R03)
- 근거 [직접]: `doc_converter.py:476~`의 `markdown_to_html`은 MD 텍스트를 HTML로 바꾸는 함수다. 확대·스크롤·단계 이동은 05가 보여주듯 SVG·CSS·스크립트·CSP 해시를 내장한 별도 21 KB 템플릿이다. 입력 Phase는 divider 라벨뿐이고(`msc_tool.py:307`) y 좌표는 렌더 결과에만 있다. 또 `msc_view_text`는 이슈 중심 문구를 고정으로 넣고(295~299행: 문제·핵심 변경·기대 효과·요청 사항), 같은 함수 327행은 `MSC_DELTA.md` 링크를 무조건 넣는다. 그 파일이 만들어지는 조건(1030행 `isinstance(change_map, list)` 이후)은 발췌가 1032행에서 끝나 확인 못 한다.
- 영향: F1의 "실제 SVG viewBox·입력 Phase/step에서 계산"은 좌표 부분이 부정확하다. AS-IS만 있는 Procedure/Feature 문서에 변경 이슈 문구와 없는 파일 링크가 들어갈 수 있다.
- 최소 수정: 단계 좌표는 SVG에서 divider 라벨 텍스트를 찾아 구하고, 정확히 1개가 일치하지 않으면 단계 이동만 끈다. Procedure/Feature용 표시는 별도 모드로 두어 이슈 문구를 쓰지 않고, 링크는 파일이 있을 때만 만든다. 호스트 CSP가 inline script를 막는지 확인 항목에 넣는다.
- 담당: doc-converter.
- 검증: AS-IS 단일 MSC 입력에서 이슈 문구와 `MSC_DELTA.md` 링크가 0, 라벨 중복 입력에서 단계 이동이 꺼진다.

## R10 대안과 완료 기준 제안

- **더 적은 변경 순서:** 뷰어는 SVG 내장 단일 `.html`로 먼저 만들어 기존 export(허용 확장자)로 게시하고, Kernel 확장은 MD 미리보기용 `.svg` 한 종류만 마지막에 검토한다. 그러면 F2 확장이 최소로 남는다.
- **완료 기준(두 진입 × 두 목적지, 각 칸 같은 기준):** ① 게시 목록이 기대 목록과 일치(지적 2). ② MD 안 링크 3개(확대 보기·원본·미리보기)가 실제 게시 경로로 열림. ③ 미리보기 이미지 `naturalWidth>0`. ④ 절의 source revision = 현재 분석 revision. ⑤ 같은 입력 재게시에서 변경 0. 실패 기준은 5개 중 하나라도 미충족이면 해당 단계만 "미완료"로 두고 다른 단계는 되돌리지 않는다.
- 02 §7의 최소 검증 항목에 한글 이름 2개(지적 4)와 상한 초과 HTML(지적 2)을 추가한다.

## 확인 수준 요약

| 항목 | 상태 |
|---|---|
| 패키지 바이트·SHA·4개 원문 문서 해시 | 직접 확인, 일치 |
| 03 발췌 간 대조(지적 1·2·4·6) | 직접 확인. 발췌 밖 동작은 [추론]으로 표시 |
| 설치본 Updater·그룹 writer·호스트 HTML 정책 | NOT_VERIFIED (요청이 명시한 미접근) |
| 독립 리뷰(감시기·유료) | NOT_RUN |
| HOST_VALIDATOR, AUTO_GENERATED_VIEWER_E2E, BUSINESS_WORKSPACE_GROUP_PUBLISH_E2E | NOT_RUN / NOT_VERIFIED |
| Linux, 사내 소형 LLM 소비자 | 검토 범위 밖 (Windows 대화형 정적 검토만) |

## GPT에게

지적별 판정은 GPT가 한다. 감시기 경로의 독립 리뷰(USD 1, 1회)가 아직 필요하면 별도 승인·서명이 필요하다. 이 문서로 대신하지 않는다. 지식 정본 수정 제안: 02 §3 F1의 "입력 Phase/step에서 계산"을 "SVG에서 라벨 위치 탐색, 불일치 시 단계 이동 비활성"으로 바꾸고, §7에 폴백 사다리와 위 완료 기준을 넣을 것.
