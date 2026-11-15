# Procedure/Feature MD의 MSC 링크 — 독립 정적 의견 반영 설계 r0002

- 2026-11-16 KST / Work `L1-WORKSPACE-RAG-20261111-001`.
- **부모 설계 r0001:** [원안](MSC_MD_LINK_SKILL_SUPPORT_REVIEW_AND_PROPOSAL_r0001_20261115_KST.md). 그 문서는 요청 `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001` rev 1의 고정 입력으로 **수정하지 않음**.
- **검토/판정:** [Claude 대화형 정적 리뷰](CLAUDE_MSC_MD_LINK_STRUCTURE_INTERACTIVE_REVIEW_FOR_GPT_20261115.md) → [GPT 판정](GPT_MSC_MD_LINK_STRUCTURE_REVIEW_DISPOSITION_r0001_20261116_KST.md) `ACCEPT_WITH_CHANGE`.
- **목적 유지:** 두 진입 모두 같은 업무용 `l1-workspace` Work에 분석·원본·Evidence·초안과 MSC 표현 보존. 검증·승인된 그룹 지식만 `l1sw-dev-knowledge`의 실제 그룹 writer로 반영. 해당 Procedure/Feature MD에서 MSC 미리보기·열람/다운로드를 제공하며 스킬·저장소/원장 신설은 기본안에서 제외.
- 아래는 **설계·검증 계약 후보**. 설치 기능 지원·실행 PASS로 간주하지 않음.

## 1. 변경된 생성 책임과 입력 클래스

```text
Workflow 진입 ─┐
                ├→ code-analyzer: 사실·source revision·기존 MSC 참조
Updater 직접 ─┘                   ↓
                         doc-converter: 기존 승인된 MSC 입력/변환,
                         원본·SVG·SVG 내장 단일 HTML·manifest
                                   ↓
                        두 진입 각각 같은 Work 저장
                   (Kernel / 허용 Workspace writer)
                                   ↓ (선택·유효 승인)
                            Updater / 그룹 writer
                                   ↓
                    대상 MD MSC 절·게시 경로 링크 확정
                                   ↓
                   readback + 열람 가능/폴백 상태 기록
                                   ↓
                       원래 Work revision/결정 연결
```

입력 클래스는 **실제 producer→converter I/O 확인 후** 다음의 분기를 고정.

| 입력 클래스 | 변환 계약 및 원본 | SVG·HTML | Phase·단계 이동 | source revision |
|---|---|---|---|---|
| 검증 시나리오 IR | 기존 `require_verified_scenario_ir` 계약 충족 시 기존 시나리오 package 경로 | renderer 정상일 때 생성; 단일 HTML은 별도 후보 구현 | IR의 검증 Phase와 SVG의 정확히 한 번 매칭한 라벨만 사용; 실패하면 이동 OFF | 분석 원본/Work의 검증 메타에서 전달 |
| code-analyzer semantic spec | 사실·MSC 참조 재사용; **시나리오 IR 여부 미확인**, 직접 package 경로 강제 금지 | 지원되는 기존 exporter/adapter를 설치 원문에서 확인 후 진행 | Phase가 입증되지 않으면 이동 OFF | 기존 code-analyzer/Work 메타에 있는 경우만 기록 |
| 기존 원본 PUML | 확인된 `msc-export` 등 기존 지원 경로로 SVG 렌더·HTML 생성 가능 여부 확인; PUML만으로 검증 IR이라고 주장 금지 | SVG 성공 시 HTML 후보. 실패 시 원본만 보존 | 기본 OFF, 검증된 단계 라벨이 실제 SVG에 있을 때만 ON | PUML에서 추측하지 않고 Work/분석 메타에서 가져옴 |

- **Procedure/Feature의 기본 경로:** 이미 검증된 기존 MSC/원본을 재사용, renderer/exporter 계약을 확인해 SVG와 단일 HTML을 생성; 별도 IR 전환이 필수인 경로를 입증하기 전까지 자동 재분석을 요구하지 않음.
- 표현기는 `markdown_to_html` 하나로 B 뷰어가 만들어진다고 주장하지 않음. B 템플릿은 SVG 내장·스크롤/확대·선택적 단계 이동용 산출물이며, 기존 converter의 renderer/style/manifest 계약과 연결을 우선 확인.
- 정제 파일명은 호출 시 고유 ASCII scenario ID 우선. 정제 후 파일명·대상 경로 **중복은 사전 차단**(`DIAGRAM_NAME_DUPLICATE` 등 명확한 오류) 또는 검증된 결정적 unique mapping. 한글 다른 이름이 같은 `_`로 충돌해 덮어쓰기 없도록 한다.

## 2. 게시 자산·상대 링크·부분 실패 계약

1. 기존 publisher/export의 **실제 `published_path` 매핑**, 원본 input/reference, 각 파일의 SHA/size를 조회. 신규 마커나 manifest 필드 신설을 전제하지 않고 기존 기능을 우선 사용한다.
2. doc-converter는 원본/검증 상태·SVG·SVG를 **내장한 단일 HTML**/필요한 추적 파일을 만들되, 원본 Evidence의 해시 의미를 바꿔 재게시하지 않는다. 최종 대상 writer가 게시된 경로에 맞는 MSC 절 파생본과 링크를 만든다.
3. 최소 변경 대안: HTML은 기존 허용 `.html` 자산 경로, 별도 MD 미리보기용 `.svg` 게시 요구가 입증된 경우 **`.svg` 한 종의 제한·size gate·복사 결과 검증**만 Kernel 수정 후보. `.puml`을 무조건 허용하거나 모든 파일 복사 상한을 풀지 않는다.
4. **예상 목록과 게시/readback 목록·해시를 대조**. 파일 크기 상한·복사 누락·이름 변경으로 참조가 깨졌다면 해당 출력만 미완료 처리하고 MSC 절에 실패한 URL을 만들지 않는다.
5. 비동일 원본→파생 링크 파일은 각 출처·revision 관계를 남기고, 가능한 기존 트랜잭션으로 묶는다. 여러 commit이 필요한 경우 파일 게시/readback 후 **링크 절을 마지막에 연결**. 그룹 게시 뒤 Workspace 역링크 실패는 역링크만 복구, 기존 분석·모델/Job 재실행 금지.

## 3. MD의 MSC 절 소유권과 호스팅 폴백

- **Workspace MD:** Workflow/Updater의 각 저장 진입이 Kernel/허용 대상 writer를 호출. **그룹 MD:** 승인된 Updater/그룹 writer만 대상 MSC 절을 갱신. 표현 converter는 대상 원장/MD의 최종 writer가 아님.
- 대상 writer가 **마커 한 쌍**으로 MSC 절을 소유하고, 현재 source/analysis revision과 표시 revision을 비교한다. marker·수동 본문 보존 기능은 **설치 원문으로 확인 전까지 가정하지 않음**. 없으면 Preview/diff·충돌/HOLD로 처리해 자동 덮어쓰지 않는다.
- 기존 수동 문단·다른 MSC·기존 Procedure/Feature 본문은 유지. 입력·링크 불변 시 중복 append 없이 **idempotent**. revision 불일치는 `STALE_SOURCE`/“오래됨”으로 표시하거나 게시 보류.
- 호스팅/독자 접근은 개인 Work와 그룹 각각 검사. 개인 비공개 뷰어 URL을 그룹에 그대로 복제하지 않음.

| 조회/렌더 확인 수준 | 사용자에게 보이는 표시 | 완료 기준 |
|---|---|---|
| 실제 렌더링 URL·독자 접근·그림 표시 PASS | 미리보기 + **MSC 확대 보기** + 존재하는 원본 링크 | **완전 열람**; URL/readback + 브라우저의 이미지 표시 검증 |
| HTML 렌더 URL 없음·스크립트 차단, SVG는 보임 | **SVG 미리보기/직접 보기**, **단일 HTML 다운로드**(‘바로 열람’ 라벨 금지) | **폴백 열람**; 존재하는 링크만, 브라우저 B 뷰어 PASS는 아님 |
| SVG도 없고 PUML/원본만 있음 | 원본 링크와 **그림 미완료** | **원본 보존/렌더 미완료** |
| 사용할 원본도 없음 | 빈 MSC 절을 만들지 않고 **자료 미확보** 상태 기록 | MSC 링크 단계 미완료 |

- 단계 이동: SVG의 divider 라벨 위치를 실제 렌더 결과에서 찾아 **정확히 하나**와 연결된 경우에만 활성화. 고정 샘플 y 좌표·검증되지 않은 Phase를 재사용 금지. 중복·미일치·CSP 차단 시 확대/스크롤/다운로드 등 가능한 기능만 유지한다.
- Procedure/Feature는 **목적·트리거·흐름·결과·근거·미확인** 중심 표기. AS-IS-only 입력에는 ‘문제/핵심 변경/기대 효과’ 같은 이슈 전용 문구를 무조건 만들지 않음. `MSC_DELTA.md` 등 선택 자료는 실제 생성·게시된 경우만 링크.

## 4. 단계별 검증 · 승인 경계

| 검증층 | 필수 확인 | 상태 |
|---|---|---|
| 입력·표현 (합성) | 3종 입력 분기, 한글명 충돌, 단일 HTML, missing Phase, duplicate SVG label, 없는 DELTA 링크 | NOT_RUN |
| 게시 (합성) | `.svg` 필터, rename, HTML 크기 초과, 기대/실제 목록 대조, hash/revision 링크 생성 | NOT_RUN |
| 문서 갱신 (합성) | marker/Preview, 재게시 중복 0, 사람이 쓴 문단 보존, 오래된 source 알림 | NOT_RUN |
| 두 진입 × 개인 Work 저장 | Workflow와 Updater 모두 같은 Work를 지속 갱신; 원본·Evidence 보존 | NOT_VERIFIED / E2E NOT_RUN |
| 각 진입 × 승인된 그룹 반영 | Workspace 성공 뒤 그룹 writer 게시; 그룹 대상 MD/자산 같은 접근 권한 검증 | NOT_VERIFIED / E2E NOT_RUN |
| 정상 웹 열람 | 게시 URL·권한·HTML·SVG 표시·필요 시 `naturalWidth>0` | PUBLIC 가상 샘플만 과거 PASS / 업무 E2E NOT_RUN |
| 폴백 열람 | URL/렌더 없음·CSP 차단·원본-only의 정확한 문구·빈 링크 0 | NOT_RUN |
| 실패 격리/회수 | 부분 게시·Work 역링크 재시도, 분석/Job 재실행 0 | NOT_RUN |

- 동일 renderer/config/정규화가 통제된 합성 환경이면 동일 입력의 **manifest·SVG hash 불변**을 검증. 서로 다른 renderer에 대해 바이트 동일을 전제로 하지 않는다.
- 정상 경로의 “링크 3개 열림”과 폴백의 “존재하지 않는 링크 0”을 **각기 다른 PASS 조건**으로 정의한다.
- 공개 B UI 샘플 PASS는 스킬이 자동 HTML을 만들었다는 증거가 아님. 업무 설치/G0, 실제 분석 호출/G1, 업무 Workspace·그룹 게시, RAG 소비는 각각 구분.
- **NEXT_ONE_ACTION:** 업무 GPT/허용 로컬 Agent가 기존 설치본·G0 결과를 읽기 전용 대조(Updater/그룹 writer, converter 입력·경로, Kernel 복사·원장/마커, 호스팅/권한)한 다음 실제 입증된 GAP만 기존 스킬에 최소 반영 제안. 모델 재분석·정식 리뷰 실행·LIVE 변경을 이 문서 게시로 지시하지 않는다.
