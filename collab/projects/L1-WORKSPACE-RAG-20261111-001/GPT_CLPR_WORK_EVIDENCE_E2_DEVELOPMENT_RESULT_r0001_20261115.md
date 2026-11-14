# CL/PR 기존 Work 참조 저장 연결 — 실제 격리 구현·시험 결과 r0001

- Work: `L1-WORKSPACE-RAG-20261111-001`
- Date: 2026-11-15 KST
- Stage: `P0_A_SOURCE_REF_LINK=IMPLEMENTED_IN_DEV_CANDIDATE`; `E2_SYNTHETIC_TEST=PASS`; `WORK_EVIDENCE_FULL_E2E=NOT_COMPLETE`; `HOST_E3=NOT_RUN`; `PUBLIC_RELEASE=BLOCKED`
- User direction: remaining CL/PR analysis work step-by-step. No operations/Job/DB/installed skill/Knowledge/LIVE mutation; no additional paid independent review or REQUEST/READY.
- Baseline: [r0002 remaining handoff](CLPR_REMAINING_IMPLEMENTATION_HOST_HANDOFF_r0002_20261114.md), [prior 3.10/3.11 CI report](GPT_CLPR_ISOLATED_PY310_PY311_VALIDATION_RESULT_r0001_20261114.md).
- Isolated development branch: `clpr-e2-work-evidence-20261115`; final tested commit `8a87782db36f7261768f0b24a7f6fe444e9792cf`.
- [Python 3.10/3.11 E2 CI run](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43609598995); [PRIVATE main persistence/readback CI run](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43609821708).

## 1. 확인된 코드 결함과 최소 변경

1. 기존 `l1-fix-workflow`의 `lookup_clpr_existing_work`는 `kernel.work_reference_find`를 호출하나, 당시 `work-ledger-kernel v0.7.38` 공개 facade에는 해당 메서드가 없어 실제 연결 호출 시 `AttributeError`가 재현되었음. 기존 내부 `WorkReferences.find`는 존재함. Kernel v0.7.39 개발 후보에 **공개 읽기 전용 delegation** `work_reference_find(query,include_archived,limit)`를 추가. Registry/schema/record.json/index 변경 없음.
2. Workflow v1.6.69 개발 후보에 `clpr_existing_work_link.py`를 추가. 명시된 이슈 후보의 **기존 Work 1개만** 연결. 먼저 Jira/P4/PR reference를 재조회하고 다중 Work/부분 조회/미검색/잘못된 ref에서 fail-closed. Archived Work도 참조 충돌 사전 점검. 기존 `work_reference_add`로만 기록; 원본 Work 기록 및 근거 없는 Evidence는 쓰지 않음.
3. 기존 읽기 전용 `clpr-issue-plan` 유지. 별도 `clpr-existing-work-link` CLI 추가. 기본 preview(쓰기 0), 명시적 `--commit`일 때만 대상 Work 참조 저장. MCP read-only 환경에서 commit 차단. Work 생성, Work 자동 병합, Provider 실행, Knowledge 게시 기능 추가 없음.
4. **제한:** Kernel의 개별 Work lock이 여러 Work를 가로지르는 동시성 유일성을 보장하지는 않음. 따라서 실제 업무 호스트 배치 전 단일 writer/직렬 처리·경합 검증 필요. 부분 쓰기 시 재시도 복구 계약도 E3 대상. 추가 Evidence는 실제 분석 결과/코드 anchor/등록 provider-kind-stage 검증 전까지 `NOT_RUN`.

개발용 텍스트 패치·시험·패키징 근거는 `clpr-e2-work-evidence-20261115` 브랜치의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/devtools/` 에 보존. 독립 리뷰 아님.

## 2. 실제 CI 시험 증거

| 단계 | Python 3.10 | Python 3.11 |
|---|---|---|
| 수정 API/Workflow Work refs 연결 6개 합성 통합시험 | PASS 6/6 | PASS 6/6 |
| 기존 Work 조회 및 재사용, preview write 0 | PASS | PASS |
| ref write/readback, 재정렬·추가 소스·반복 입력 중복 0 | PASS | PASS |
| 충돌 Work/누락 Work/잘린 검색/잘못된 입력 차단 | PASS | PASS |
| CLI 기본 preview/명시 commit 파싱 | PASS | PASS |
| 두 신규 개발용 ZIP CRC·Python parse·manifest 일치 | PASS | PASS |
| 두 버전에서 생성된 ZIP 바이트 SHA-256 일치 | PASS | PASS |

위 테스트는 **임시 디렉터리의 합성 Work 원장**만 사용. 실제 업무 `l1-workspace`, Mango MCP, P4 revision, 실제 PR/코드 분석, 근거 Evidence 등록·재조회·원인 확정은 검증하지 않음. 기존 9개 suite 중 2개 baseline FAIL 이력은 해소되지 않았고, 이번 신규 ZIP에 대한 전체 회귀시험 또한 `NOT_COMPLETE`. 위 CI의 SUCCESS는 E2 부분시험 결과만 뜻함.

## 3. 새 PRIVATE 개발 후보 2종 — PUBLIC 금지

| 파일 (PRIVATE `main` `candidates/`) | 실제 크기 | SHA-256 | manifest |
|---|---:|---|---:|
| [l1-fix-workflow_v1_6_69_1115.zip](candidates/l1-fix-workflow_v1_6_69_1115.zip) | 866671 B | `d4ba119298cd5763fd18ace2d54223fff010a8d2a1703ebab80eb4fa1b35846b` | 309 entries PASS |
| [work-ledger-kernel_v0_7_39_1115.zip](candidates/work-ledger-kernel_v0_7_39_1115.zip) | 409355 B | `24184fe760c058a6fbc4f79c8d2d3e580978c05bde4597155e81fa3d6f23885a` | 161 entries PASS |

- ZIP 내부 `.skill-release.json`은 `development_not_for_deployment`. VERSION 및 archive명 갱신. 원본 5종 후보와 PUBLIC 원본 모두 그대로 보존.
- PRIVATE `main`에 신규 파일만 생성한 커밋: Workflow `d7babf84cf0889708e1b633c023e79aaeefcdbc0`, Kernel `5a6125f1aac1cdb0094289d5521bf0b32360adf4`.
- CI가 신규 ZIP의 실제 바이트·SHA-256을 고정 확인 후 PRIVATE `main`에 생성했고, API 원격 GET으로 다시 읽어 동일 SHA-256/크기를 확인. 이후 GPT가 `main` 두 blob 재조회로 존재 재확인.
- FULL SECURITY SCAN, 전 환경 호환성, 운영 rollback, 독립 패치 리뷰는 아직 PASS하지 않음. **새 버전 ZIP 2개를 공식 배포본으로 표시하거나 PUBLIC에 게시하지 않음.**

## 4. 남은 P0/B/C 및 차단 판정

- `WORK/EVIDENCE`: Work source reference 저장·재조회까지 **합성 E2 PASS**. 실제 Code Analyzer 결과 + 등록 Evidence 슬롯에 대한 검증된 write/readback과 Work/Artifact/Export 비교는 `NOT_RUN`.
- `P4_HISTORICAL_BEFORE_AFTER`: 실제 허가된 Mango MCP describe/files/integration + rev/from_rev 계약을 확인할 사내 호스트 접근이 없어 `BLOCKED/NOT_VERIFIED`. 임의 P4 CLI/sync나 PRIVATE로 사내 자료 반출 없음.
- `FULL_REGRESSION`: 이번 신규 ZIP에 대한 전체 기존 suite 및 C01–C12, 이전 두 baseline FAIL의 독립 결함 처리 `NOT_COMPLETE`; CI E2 PASS로 대체하지 않음.
- `HOST_E3`: 실제 MCP/PR target, authorized Work/Evidence, 0 duplicates, cross-work concurrency, source drift, rollback `NOT_RUN`.
- `INDEPENDENT_PATCH_REVIEW`: `NOT_RUN`; 이전 설계 리뷰를 코드 리뷰로 소급하지 않고, 추가 유료 호출/READY 0.
- `PUBLIC_FINAL_ZIP`: `BLOCKED/NOT_POSTED`. 업무 호스트·보안·독립 검증·배포 게이트 충족 전 PUBLIC 배포 금지.
- `OPERATIONS`: 설치본/운영 원장·DB/Watcher/Job/Knowledge/LIVE 변경 0. CoWork LIVE 상태 자체는 본 작업에서 변경하거나 재판정하지 않음.

**NEXT_ONE_ACTION:** PRIVATE의 새 개발 후보 2종을 기준으로 기존 Workflow/Kernel 전체 관련 회귀(C01–C12)와 CLI write 경계·Evidence 계약을 추가 검증. 실 Mango/업무 Host E3는 승인된 해당 호스트에서만 진행. 각 차단을 개별로 해제한 뒤 최종 PUBLIC 배포 판정.
