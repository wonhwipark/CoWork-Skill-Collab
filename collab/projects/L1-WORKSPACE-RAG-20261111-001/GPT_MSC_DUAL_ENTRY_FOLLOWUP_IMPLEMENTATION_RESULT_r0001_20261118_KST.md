# MSC 두 독립 진입 — 후속 스킬 구현·시험 결과 r0001

- 기준: 2026-11-18 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 설계 입력: [L1_MSC_DUAL_ENTRY_DOCUMENT_DESIGN_r0001_20261117_KST.md](L1_MSC_DUAL_ENTRY_DOCUMENT_DESIGN_r0001_20261117_KST.md)
- 수용 판정: [GPT_MSC_DUAL_ENTRY_R1_DISPOSITION_r0001_20261118_KST.md](GPT_MSC_DUAL_ENTRY_R1_DISPOSITION_r0001_20261118_KST.md), `REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117` COMPLETED / ACCEPT_WITH_CHANGE / 리뷰 사이클 CLOSED. 이전 리뷰 재요청·재실행 없음.
- 범위: 접근 가능한 실제 공개 Converter와 기존 PRIVATE Workflow 후보를 고정 입력으로 하여 *최소 HTML opt-in 및 이슈 handoff 전달* 개발·회귀. Updater/Kernel/지식 writer 변경·업무 호스트 설치·PUBLIC 릴리스는 이번 범위 밖.

## 1. 실제 수정·재사용

| 스킬 | 기준 원본 | 후속 개발 후보 및 실제 변경 |
|---|---|---|
| `doc-converter` | PUBLIC `doc-converter_v0_2_26_1117.zip`, SHA-256 `b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c` | `v0.2.27`. 기존 `msc_tool.py`의 B HTML 생성 조건을 `PROCEDURE_FEATURE` **또는** 명시적 `--html-viewer`로 확장. 기존 `msc-package` / `msc-scenario-build` parser, 내부 Namespace forwarding, 실제 `skillsilent/policy.json` 2개 action의 allowed/boolean flags 동기화. `ISSUE`의 본문 의미·기본 출력과 기존 `PROCEDURE_FEATURE` 기본 HTML은 유지. 렌더 성공 때만 HTML/manifest 기록. gateway 자체·새 엔진·스키마·writer 변경 없음. |
| `l1-fix-workflow` | PRIVATE 기존 개발 후보 `l1-fix-workflow_v1_6_70_1117.zip`, SHA-256 `1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb` | `v1.6.71`. `scenario_msc.py`의 기존 `build_msc_handoff` 결과 `artifact_pipeline.convert`에 `view_mode=ISSUE`, `html_viewer_flag=--html-viewer`, `html_viewer_opt_in=True` 전달. **계획/호출 계약만** 작성, 승인된 기존 Agent/runner를 대신 실행하지 않음. Updater 선행 호출·지식 자동 기록·임의 새 Work 발급 없음. |

검증된 공통 책임은 Converter가 MSC 산출물을 생성하고 Workflow는 기존 Work에서 요청을 조정하는 구조. Updater 직접 지식 생성도 `doc-converter`의 동일 opt-in을 활용할 수 있지만, **실제 Updater 설치본 원문/기존 개인·그룹 writer G0 미확인으로 Updater 코드는 변경하지 않았음**.

R1 비차단 2건: (1) Work-root `MSC_VIEW.md`는 ‘MSC 작업 안내’, Converter 상세 `MSC_VIEW.md`는 ‘MSC 상세 원본’으로 용도 구별, HTML은 게시 형태 확인 후 ‘MSC HTML 확대 보기’/‘MSC HTML 다운로드’로 표기하는 규칙을 후보 SKILL 문서에 반영. 실제 Kernel writer의 모든 링크 생성 변경을 완료했다는 의미는 아님. (2) Work 문서=기존 Kernel writer, 개인 Knowledge=Updater가 연결한 기존 Workspace writer, 그룹 지식=기존 group writer 단일 소유. 마커 부재/중복·수동 편집·충돌은 Preview/HOLD, 자동 덮어쓰기 금지. **해당 실 writer 패치·G0/E3는 별도 검증 대상**. Converter가 어떤 저장소에도 자동 게시하지 않음.

## 2. 시험과 산출물

- 실제 PRIVATE main source: [개발·검증 빌더](dev/msc_dual_entry_candidate.py) (고정 원본 SHA 대조, fail-closed anchored patch, metadata/manifest 재생성, 기능 실행·compile, ZIP CRC/버전/전파일 SHA gate).
- 실제 PRIVATE main CI: [CoWork skill release quality gate run 44125496802](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44125496802) **SUCCESS**. 해당 commit `3814e189433d2ba440fac655de726c8d6cafb8d5`의 새 후보 빌드/회귀 step 및 기존 릴리스 gate·Kernel SVG Evidence 회귀 모두 PASS. 각 성공 조건은 실제 runner 실행 기준.
- 신규 Converter 회귀 **4개 PASS**: `ISSUE` 기본 HTML 없음, `ISSUE --html-viewer` HTML/manifest 있음 + ISSUE 문제 설명 유지, `PROCEDURE_FEATURE` 기본 HTML 유지, `scenario-build` opt-in 파라미터 보존. 두 관리 action policy/gateway 허용 및 비허용 flag 검사도 PASS.
- 신규 Workflow 회귀 **3개 PASS**: 기존 Work의 plan-only, 암묵적 publisher 없음, `ISSUE` HTML opt-in handoff.
- Builder 결과: `MSC_DUAL_ENTRY_BUILD_SUCCESS`. 후보 두 ZIP의 내부 파일 전체 manifest/버전/CRC 게이트 PASS. **후보는 정식 배포 금지** `development_not_for_deployment`.
- Actions 아티팩트 `msc-dual-entry-development-1118` ID `14348015313`, [run artifact](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44125496802), 2026-11-24 16:25 UTC 만료 예정. 실행 재현 가능한 빌더는 PRIVATE main에 보존. Actions artifact 보관은 PRIVATE 리포지토리 내 영구 ZIP 게시와 구분.

| 개발 ZIP | bytes | SHA-256 |
|---|---:|---|
| `doc-converter_v0_2_27_1118.zip` | 169567 | `4bc457794a5de80c19559d27c83f79485be579dd15da05b88b86bc8908232558` |
| `l1-fix-workflow_v1_6_71_1118.zip` | 758424 | `d47605f234fccda7e5941caddf3404eac668d2dfc3e5ba5e2faf6928aa5f6615` |

해당 아티팩트 다운로드 후 컨테이너에서 두 ZIP의 정확한 파일 크기·SHA-256, ZIP 90/310개 멤버 CRC 검증 PASS. `MSC_DUAL_ENTRY_BUILD_RESULT.json` 해시 `4bc1b222d16d09e32f197791916dda1cfff36661fc5bbab5c13a7dd3c84caf7f`.

## 3. 판정·차단·다음 한 행동

`CODE_BUILDER=PRIVATE_MAIN_POSTED` / `DEVELOPMENT_ZIPS=ACTION_ARTIFACT_AVAILABLE` / `EXECUTABLE_TARGETED_TEST=PASS` / `RELEASE_GATE=PASS` / `CI=PASS`.

`INDEPENDENT_CODE_REVIEW=NOT_RUN`, `UPDATER_WRITER_G0=NOT_VERIFIED`, `KERNEL_LINK_WRITER_E3=NOT_RUN`, `ACTUAL_WORKFLOW_RUNNER=NOT_RUN`, `BUSINESS_E3=NOT_RUN`, `PUBLIC_DELIVERY=NOT_RUN`, `HOST_INSTALL=NOT_RUN`, `GROUP_KNOWLEDGE_WRITE=NOT_RUN`. 본 설계의 종료된 R1을 재큐잉/추가 리뷰하지 않음. 기존 Guard 불확실 승인 이력·다른 Work·승인 범위 보존.

**NEXT_ONE_ACTION:** 접근 가능한 업무 환경에서 기존 Updater/Kernel 최종 writer의 G0 API·마커·published_path를 확인하고, 승인된 샘플 Work의 실제 `ISSUE --html-viewer` 연결·수동 편집 충돌/부분 실패를 검증. 그 전에는 본 개발 ZIP을 PUBLIC 최종 릴리스·설치본으로 승격하지 않음.
