# ACE·PEC-HOP·ACON 읽기 전용 연결 후보 개발 및 L1Work 배포 게이트 판정 r0001

- 기준일: 2026-11-19 KST
- 사용자 지시: “적용해줘” → “진행하자” → “L1Work 에 배포까지해줘”
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001` (새 Work/스킬/원장 없음)
- 코드 기준: [설계 r0002](ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0002_20261118_KST.md), 기존 [소스 G0 인터페이스](GPT_ACE_PEC_SAFE_SOURCE_G0_INTERFACE_MAPPING_r0001_20261118_KST.md), 완료 R1 판정 `ACCEPT_WITH_CHANGE/CLOSED`
- **총괄 판정:** `DEV_READONLY_CONNECTOR=PASS_SCOPE_LIMITED`; `LOCAL_SYNTHETIC_TEST=19_PASS_0_FAIL`; `SOURCE_PACKAGE_INTEGRATED=NO`; `PUBLIC_SKILL_ZIP=BLOCKED_NOT_POSTED`; `BUSINESS_HOST_INSTALL=NOT_RUN`.
- 기본 경계: `l1-knowledge-updater`는 업무 전용 스킬로 코드·SKILL.md/업무 데이터 GitHub 반출 요구 0. 업무 Linux 설치 실측과 GitHub 개발 후보의 버전/실행은 별도.

## 1. 실제 개발 파일과 무결성

| 대상 | PRIVATE main 경로 | 원격 commit/검증 | UTF-8 bytes · SHA-256 |
|---|---|---|---|
| 읽기 전용 순수 연결 후보 | [dev/ace_pec_acon_readonly.py](dev/ace_pec_acon_readonly.py) | 최종 `fbb7246a585cb87004ca8993fc2eece7538b1e64`; blob `0be43253e6d4ae2e845f72c7da1052f398c072df` | **5,711 B** · `98517157a572115bf8cbe24ff05ca2e0d178e51a4cffb4b6c0156b88f929b234` |
| 합성 단위시험 | [dev/test_ace_pec_acon_readonly.py](dev/test_ace_pec_acon_readonly.py) | `07bebeeb1a6e81f0db4209ee60405966f2c05d40`; blob `2db1a67ddacc9baa6c4a48f8da0aba86d1082160` | **4,255 B** · `3b55d23dff307d4a137497ec5bd778122e948ee1052b13663da0383a376c6561` |

- GPT 격리 환경에서 실제 파일을 생성해 Python 표준 `unittest`를 실행하고 로컬 SHA-256 및 Git blob SHA-1을 계산. 두 파일 모두 **GitHub PRIVATE main에서 직접 다시 조회한 blob**과 로컬 `git hash-object`가 정확히 일치.
- 구현은 `pure Python` 데이터 변환으로만 구성. 프로그램이 업무 파일·네트워크·Git·MCP·지식/Kernel writer·Watcher·READY·모델 API에 접근하지 않음. 새 스킬 등록/실제 Workflow import·기존 스킬 ZIP 수정도 하지 않음.
- Python 모듈은 아직 `l1-fix-workflow`, `work-ledger-kernel`, `code-analyzer`의 배포 package에 통합되지 않았으므로 독립 스킬이나 설치 가능한 최종 ZIP이 아님.

## 2. 코드 동작(제한적)과 실제 시험

| 원리 | 순수 함수·내용 | 실행 시험 |
|---|---|---|
| ACE | `ace_decision_candidate()`: 동일 Work/범위/주제와 호스트가 사전 검증한 출처·권한·append-index를 사용해 선택 **후보**만 반환. 권한·순서 모호하면 HOLD. 결정을 실제 승인하거나 원장을 쓰지 않음 | 7 PASS |
| PEC-HOP | `pec_verify_excerpt()`: pinned revision/원본 파일 SHA/실제 raw byte offset·length·발췌 raw bytes 비교. 변조 FAIL, 권한/원본/offset 누락 HOLD | 7 PASS |
| ACON | `acon_compare_existing_results()`: 동일 고정 모델·revision의 **이미 있는** baseline/compressed 결과 각 3회 이상을 비교하고 인용 Evidence 누락을 보고. 실행 호출 0, 압축 실패 인과관계 자동 확정 금지 | 5 PASS |
| 전체 | 총 19건 Python `unittest`, 실패/예외 0 | **19 PASS** |

- **동일성/격리:** 합성 입력만 사용, 실제 회사 원본·단일 Installed Skill·그룹 writer·Git checkout 경합은 실행하지 않음. 기존 별도 순수 JS 26/26 PASS는 그대로 유지하고 실제 기능 통합 45건 PASS로 합산 승격하지 않음.
- **실행한 호출:** 개발 후보 Python 합성 시험 19건만. 신규 Claude/모델·Job/READY·Linux 설치·Group WRITE·PUBLIC ZIP 0.
- **독립 코드 리뷰:** NOT_RUN. 설계 R1의 완료/비용을 신규 Python 코드 리뷰 결과로 재활용하지 않음.

## 3. L1Work 최종 ZIP 배포 게이트

확인한 [PUBLIC 릴리스 계약](../../ops/CONTRACTS/PUBLIC_RELEASE_GATE.md) 및 [기존 Knowledge Guard 차단](../L1-WORKSPACE-RAG-20261111-001/GPT_KNOWLEDGE_GUARDS_CANDIDATE_QA_PUBLIC_GATE_r0001_20261117_KST.md), [추가 하드닝 결과](../L1-WORKSPACE-RAG-20261111-001/GPT_KNOWLEDGE_GUARDS_HARDENING_RESULT_r0002_20261117_KST.md)를 동일 범위에 적용.

1. 실제 Workflow/Kernel/Analyzer의 최신 배포 소스 및 활성 설치본이 **미확인**이며 순수 후보가 아직 패키지 내부에 편입되지 않았음. ZIP 새 버전으로 강행하면 기존 v1.6.68~v1.6.72·Kernel 등 선행 기능을 유실할 위험. `SOURCE_INTEGRATION=NOT_RUN`.
2. 관련 PRIVATE `l1-fix-workflow v1.6.70`, `work-ledger-kernel v0.7.43`, `l1-github v0.3.59`의 개발 후보는 `development_not_for_deployment`. 이미 commit된 Knowledge diff outbound 방어는 일부 보완됐지만 **raw Git/credential 분리, 동시 writer/CAS, 호스트 WRITE 경계 및 전체 회귀** 미확인. 범위가 다른 Job-list READ_ONLY 전달 예외를 적용하지 않음.
3. 본 코드와 통합 패키지는 `INDEPENDENT_CODE_REVIEW=NOT_RUN`, `HOST_G0=NOT_RUN`, `FULL_REGRESSION=NOT_RUN`; 사용자 공개 배송 지시가 실패한 필수 게이트 자동 면제는 아님.
4. `PUBLIC_DELIVERY=BLOCKED_NOT_POSTED`. 이미 공개된 L1Work ZIP, 업무 스킬·그룹 지식, PACKAGE/PIN/REQUEST/READY/모델 영수증을 덮어쓰지 않음.

**현재 PUBLIC 자산:** 기존 [업무 GPT ACE·PEC-HOP·ACON 인계서 §§9~10](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)만 이미 게시·원격 확인 완료. 공개 인계서가 새로운 ZIP 설치·업무 스킬 적용을 의미하지 않음.

## 4. 실제 배포를 위한 최소 후속(새 기능 확장 금지)

- 정확한 실제 활성 Workflow/Kernel/Analyzer 스킬 revision과 허용된 read-only G0 계약을 업무 GPT/Agent에서 **비민감 요약**으로 확인. 업무 전용 Updater 원본/직접 코드는 받지 않음.
- 현재 통합 대상 스킬의 **정확한 전체 소스 ZIP/호환 대상**을 고정하고 위 pure function 중 실제 필요 기능만 기존 reader/packet 경로에 최소 CONNECT. 기존 Kernel Evidence/decision writer·Knowledge writer·보호 가드 무변경 우선. 어떤 통합도 검증 전 `development_not_for_deployment` 상태 유지.
- 기존 미충족 writer/경합/권한 게이트를 원래 Knowledge Work 책임에서 해결하고 필요한 **독립 코드 리뷰와 전체 회귀·배포 원본/SHA/CRC/정보등급 검사** 수행. 정상 확인된 최종 새 버전 ZIP만 L1Work/main 루트에 게시하고 원격 재다운로드 SHA를 확인.
- 실제 Linux 호스트에서 `skill-updater` 설치/활성화는 별도 승인·권한·호스트 실행 결과로만 완료 판정. 사용자에게 공개 ZIP 링크와 실호스트 설치를 같은 완료로 보고하지 않음.

**NEXT_ONE_ACTION:** 기존 업무 GPT [PUBLIC 인계서 §9~10](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)의 *미확인 항목만* READ_ONLY 회수 → 현재 배포 대상 스킬 소스/기존 보호 경계 확정 → 후보 최소 통합·회귀·독립 코드 리뷰·최종 L1Work 공개 Gate 재판정. 실제 결과가 없으면 공개 ZIP/업무 설치 BLOCKED 유지.
