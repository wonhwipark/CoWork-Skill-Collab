# ACE·PEC-HOP·ACON: Workflow v1.6.73 실제 통합 개발 ZIP·CI·PUBLIC 배포 게이트 판정

- 기준: 2026-11-19 KST; 사용자 지시 “진행해 배포할때까지 스탑하지마”
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- **종합 상태:** `WORKFLOW_SKILL_DEV_ZIP_BUILT=PASS`; `ACTUAL_PACKAGED_MODULE_SYNTHETIC_TEST=20_PASS`; `EXISTING_MSC_CONTRACT=PASS`; `REPRODUCIBLE_ZIP=PASS`; `FINAL_PUBLIC_RELEASE=BLOCKED_NOT_POSTED`; `BUSINESS_INSTALL=NOT_RUN`.
- 기존 ACE·PEC-HOP·ACON 설계 R1 `ACCEPT_WITH_CHANGE/CLOSED`와 합성 26 PASS는 보존. 이번 개발 **코드 독립 리뷰 아님**.

## 1. 실제 구현과 기존 기능 보존

- 기존 PRIVATE Workflow `v1.6.70` ZIP을 SHA256 `1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb`로 고정해 기존 `v1.6.72` MSC opt-in 후속 패치를 정확히 재적용.
- 기존 Workflow 패키지 내 **`l1_fix_workflow/ace_pec_acon_readonly.py`**에 `ace_decision_candidate`, `pec_verify_excerpt`, `acon_compare_existing_results` 순수 함수를 추가하고 SKILL.md에 적용 책임과 HOLD/FAIL/금지 조건을 설명. 별도 스킬·Kernel schema·Git writer·Knowledge Updater writer, 자동 모델/Job/Watcher/README state engine 추가 0.
- ACON 압축본 일부 실행에서 누락된 Evidence를 “모든 실행에서 누락”이라고 오독할 수 있는 필드명 결함을 `evidence_missing_from_any_compressed_run`으로 수정하고 1개 단위시험 추가.
- 후보는 새 함수의 존재/내부 import 및 조건별 결과를 검증한 **개발 패키지**이며 업무 LLM/기존 Workflow 진입에서 자동 실행되는 ACE 통합 E2E는 **NOT_RUN**. Updater는 업무 전용이므로 회사 원본 반출/수정 0.

## 2. 실제 고정 소스

| 파일 | PRIVATE main 경로(모두 이 Work /dev/) | Git blob | SHA256 · UTF-8 bytes |
|---|---|---|---|
| 읽기용 모듈 | [ace_pec_acon_readonly.py](dev/ace_pec_acon_readonly.py) | `7ebdfb884e24aabad662bbdea5d0bb98e58e0d4d` | `6c7fe329fd1d4b88b1a063200ab84bd29993a27ebcd74cb274df4b6dd98ad9fa` · 5,710 B |
| 단위시험 | [test_ace_pec_acon_readonly.py](dev/test_ace_pec_acon_readonly.py) | `410fe83786816e696e4d95cd9d5ba832ea96e5c2` | `855db77cd12baab29dd33e077ec68df702ad1911b5d14a606cd40213763bbad2` · 4,652 B |
| 고정 ZIP 빌더 | [build_ace_pec_acon_workflow_v1673_1119.py](dev/build_ace_pec_acon_workflow_v1673_1119.py) | `f90a5489538fbffbb35a02792988e08186db886c` | `9d83dd7bbf5b1802f24c4b4de67165d0101a1b2b43ee6d77112e614f02d93d95` · 6,203 B |

## 3. 실제 빌드/시험·배송 바이트

- **[CoWork main Actions 44422077963](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44422077963)**, head `1c64a666eb0e93f27742e94d0b273f49cf80a9bb`, **SUCCESS**; 실행 단계 `Build ACE PEC ACON packaged Workflow read-only development candidate` / 독립 두 번 빌드 `cmp` **PASS**.
- ZIP: **`l1-fix-workflow_v1_6_73_1119.zip`**, **760,970 bytes**, SHA256 **`4e435a165a692f9c77c816067d6dd7d11f920def4c808d4ecb06b44b613a5c77`**, 311 members / 310 manifest covered, ZIP CRC/버전/매니페스트/컴파일/경로 검사 **PASS**.
- 실제 패키지에서 추출된 **그 모듈을 import해 Python `unittest` 20건 PASS**. ACE 7, PEC-HOP 7, ACON 6. 기존 Workflow MSC plan-only/ISSUE HTML opt-in handoff 3개 PASS. 두 독립 ZIP 바이트 완전 일치.
- [PRIVATE Actions artifact](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44422077963) `ace-pec-acon-workflow-development-1119` (ID `14482227360`, 일시 보관); 만료 후에도 위 코드+기준 ZIP pin으로 재현 가능.
- **중요**: `.skill-release.json.channel=development_not_for_deployment`. 위 해시는 **개발 후보** 바이트 해시이며 새 채널/메타의 실제 최종 ZIP SHA로 재사용하면 안 됨.

## 4. 공개 배포 보류 사유(확인된 사실과 미실행 구분)

1. **신규 코드 독립 리뷰 미실행.** 디자인 R1은 신규 v1.6.73 소스/통합 빌더의 리뷰/영수증이 아님.
2. **Linux 설치본/기존 writer 안전 G0 미확인.** raw Git shared credential 및 동시 writer/CAS/Group Knowledge 권한 경계의 기존 차단이 해소됐다는 호스트 근거가 없음. 설치된 Workflow/Kernel/Analyzer 활성 version과 이 후보 통합 호환도 미검증.
3. **최종 릴리스 메타데이터·독립 보안/호환성 전체 시험 미완료.** 현재 채널 자체가 deployment 금지이며 사용자 승인만으로 FAIL/NOT_RUN 게이트를 면제할 수 없음.
4. 따라서 `L1WORK_PUBLIC_SKILL_ZIP=BLOCKED_NOT_POSTED`. 기존 PUBLIC ZIP 보호, 신규 README/상태 문서와 ZIP 자체 업로드는 구별. 새 운영 Agent·모델/Watcher 호출·REQUEST/READY/서명·사용자 지식 변경 0.

## 5. 독립 리뷰와 업무 G0 인계 — 추가 확장 없이 후속 연결

- 기존 [Windows Claude Code 코드 리뷰·배포 게이트 원샷](ACE_PEC_ACON_WORKFLOW_V1673_INDEPENDENT_CODE_REVIEW_AND_RELEASE_GATES_r0001_20261119_KST.md) (PRIVATE main). 정식 리뷰 생성은 실제 LIVE 정책·보호 위임 preflight가 PASS일 때만; 사용자 승인 USD3 문서와 Windows 현재 보호 설정 차이를 무시하지 않음. 불충족은 유료 호출 0.
- 기존 [업무 GPT 공개 §9~11](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)의 관련 설치본/Reader/Writer 비민감 G0만 재사용하고 원본/SKILL.md 등 업무 자료 반출 금지.
- **완료 순서:** 정확한 Code review/G0를 회수 → 필요 최소 수정·기존 테스트/보안/호환 확인 → 릴리스 게이트 PASS로 새 최종 ZIP 생성 → `wonhwipark/L1Work/main` 루트에 유일한 신규 파일 게시 → raw download와 SHA256/readback → 별도 업무 Linux 설치/동작 확인.
- **현재 NEXT_ONE_ACTION:** Windows에서 이 v1.6.73 변경 diff의 LIVE preflight/독립 코드 리뷰 가능성 확인과 업무 GPT의 기존 설치 환경 비민감 G0 결과 회수. 모델 호출/호스트 조작을 GPT가 직접 했다고 보고하지 않음.
