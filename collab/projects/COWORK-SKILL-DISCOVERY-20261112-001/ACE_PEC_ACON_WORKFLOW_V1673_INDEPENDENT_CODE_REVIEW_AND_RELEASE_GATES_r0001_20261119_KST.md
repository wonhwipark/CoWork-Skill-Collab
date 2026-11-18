# ACE·PEC-HOP·ACON — Workflow v1.6.73 개발 패키지 독립 코드 리뷰·L1Work 릴리스 게이트 인계

- Work: `COWORK-SKILL-DISCOVERY-20261112-001` (동일 목적 기존 Work 재개)
- 사용자 최신 지시: **“진행해 배포할때까지 스탑하지마”**. 최종 허용 PUBLIC 목적지 `wonhwipark/L1Work/main` 루트, 검증 통과한 새 ZIP의 반복 배송 승인 불필요.
- 정본: `wonhwipark/CoWork-Skill-Collab` PRIVATE `main`, Windows Claude Code는 **기본 독립 코드 리뷰어**, 업무 GPT/허용된 Linux Agent는 업무 설치본/Writer G0.
- 현재 상태: `DEV_ZIP_BUILT=PASS` / `ACTUAL_PACKAGED_SYNTHETIC_TESTS=20_PASS` / `SOURCE_PIN_REPRODUCIBILITY=PASS` / `INDEPENDENT_CODE_REVIEW=NOT_RUN` / `HOST_G0=NOT_VERIFIED` / `PUBLIC_RELEASE=BLOCKED_NOT_POSTED`. 실제 Windows/업무 호스트 실행을 한 것으로 표시 금지.

## A. 고정 입력·실제 빌드

| 항목 | 정확한 경로/근거 |
|---|---|
| 기준 Workflow 개발 ZIP | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_70_1117.zip` / pinned SHA256 `1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb` |
| 재사용한 MSC 선행 패치 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/dev/msc_dual_entry_candidate.py::patch_workflow`, v1.6.72 동작 보존 |
| 실제 ACE·PEC-HOP·ACON 연결 코드 | `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/dev/ace_pec_acon_readonly.py` (전달 시 최신 main blob 및 SHA pin) |
| 20개 단위시험 | `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/dev/test_ace_pec_acon_readonly.py` |
| v1.6.73 통합·재현 빌더 | `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/dev/build_ace_pec_acon_workflow_v1673_1119.py` |
| 실제 GitHub CI | [run 44422077963](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44422077963), commit `1c64a666eb0e93f27742e94d0b273f49cf80a9bb`, conclusion **success** |
| 정확한 개발 ZIP | `l1-fix-workflow_v1_6_73_1119.zip` / **760,970 bytes** / SHA256 `4e435a165a692f9c77c816067d6dd7d11f920def4c808d4ecb06b44b613a5c77` / **311 members**, manifest 310 entries |
| 임시 PRIVATE CI artifact | artifact `ace-pec-acon-workflow-development-1119`, ID `14482227360`, run `44422077963`, 기한 2026-11-25 UTC. 파일이 유실돼도 위 고정 빌더+입력으로 **재현 가능** |
| 실제 Python 검증 | 개발 패키지 내부로 import한 모듈에 대한 **20 PASS / 0 FAIL**, 기존 MSC 기능 3개 계약 PASS, Python compile/CRC/전파일 manifest/버전 검사 PASS, ZIP 2회 재빌드 바이트 비교 PASS |

- 후보 ZIP 내부 `.skill-release.json.channel=development_not_for_deployment`. 운영에 설치하거나 PUBLIC에 최종 ZIP으로 업로드하지 말 것.
- **ACON 자체시험 수정:** compressed 3회 중 한 회에서 Evidence가 누락됐을 때 “모든 실행에서 누락”으로 오해될 수 있는 출력 필드를 `evidence_missing_from_any_compressed_run`으로 수정하고 제20 단위시험으로 확인. 모델 추가 호출 0.
- 개발 ZIP은 기존 Workflow 코드에 작은 **읽기 전용** 함수를 추가하며 자동 실행/워크 원장·Kernel schema·Git writer·그룹 Knowledge writer 변경 없음. “이미 모든 업무에서 ACE가 동작”했다고 주장하지 말고 후속 실제 호출 연결/업무 검증과 구별.

## B. Windows Claude Code — 기존 협업 계약을 따른 독립 코드 리뷰 원샷

1. PRIVATE `main`에서 기존 `CONTEXT_BRIEF.md`, 이 Work `CURRENT.md`, 설계 `ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0002_20261118_KST.md`와 빌더·코드·시험·CI/ZIP을 읽는다. **종료된 설계 리뷰 R1을 재큐잉하지 말고** 이 v1.6.73 신규 코드/빌더 diff만 별도로 검토. 코드 변경(ACE 원본 결정·권한 신뢰 가정, PEC raw byte 동일성·offset, ACON 결과 필드·인과 오인)과 메타데이터/MSC 호환·개인 Knowledge 변경 무관성 확인.
2. 신규 유료 요청의 실호스트 **LIVE 정책·protected delegation/승인 만료·요청/리뷰 중복**을 먼저 `collab/ops/review_request_gate.py select/check --intent unified` 및 해당 Windows 운영 signer의 지원되는 읽기 전용 절차로 확인. 사용자 문서상 신규 리뷰 USD3 허용과 Windows 운영 보호 위임/정책의 실제 반영을 **별개**로 판단. 현재 CoWork 정본은 USD3 위임/LIVE 적용을 **BLOCKED**로 보고: **호스트 정책 호환 PASS와 유효 승인 모두 없으면 formal REQUEST/패키지 고정·서명·READY·유료 호출 0**.
3. 정책 호환 및 유효 승인 범위가 실제 확인된 경우에만 사용자 지정 이 개발 ZIP의 정확한 바이트와 바뀐 스크립트·19→20 테스트·기존 v1.6.72 경로가 포함된 **신규 고정 리뷰 입력**을 작성. 정식 `collab/requests/<NEW_UNIQUE_ID>/REQUEST.md`, `collab/packages/<PINNED_INPUT>.zip`, `SOURCE_PIN.json`은 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`의 실 LIVE preflight 및 실제 remote byte check 이후 작성. 서명/READY는 허용된 Windows 승인 경로에서 **마지막**, watcher 유효 처리 1회만. 동일 기존 R1의 REQUEST/영수증/READY 재사용 불가.
4. 리뷰 결과에서 `BLOCKING/MAJOR/MINOR` 및 재현 가능 반례, 최소 보완, 검사 범위, **독립 검증된 것과 호스트 미확인**을 분리. 결과·영수증·원격 hash를 기존 `COWORK-SKILL-DISCOVERY-20261112-001`의 CURRENT와 연결. 개발한 GPT의 20개 자체시험을 독립 리뷰로 기재 금지.
5. 리뷰가 실제 보류/차단되더라도 기존 빌드/시험/정본을 보존. 무단 POLICY/위임 상향, 미승인 유료 모델 재호출, 기존 UNCERTAIN/완료 리뷰 재큐잉·호스트 키·DB 직접 수정 금지.

## C. 업무 GPT / Linux Agent — 설치·권한 최소 G0

- 실제 사용 중인 Workflow/Kernel/Analyzer 설치 버전·바이트/동작 또는 source pin(확인 가능 범위만), Updater 지원 기능과 연결 제약을 **비민감 요약으로 회신**. `l1-knowledge-updater` 코드는 업무 전용; SKILL.md/원본·회사 상세 코드·로그·MSC를 CoWork/L1Work 반출하지 않음.
- 실제 기존 Git writer/raw Git/OS credential 분리·동시 writer lock/CAS·그룹 승인/게시 경계가 변경 후보의 WRITE 경로에 영향을 주는지 확인. **코드가 읽기 전용이라는 이유만으로 설치된 전체 Workflow 권한 안전 PASS 선언 금지**.
- 허용된 비민감 synthetic Work fixture에서 ACE 결정 순서/HOLD, PEC 근거 byte offset/변조, Kernel read side effect (root mkdir 가능), ACON 모델 호출 0 및 기존 MSC 계약을 확인. 업무 원본 분석/지식 writer 호출·그룹 게시·무단 설치 금지.

## D. 최종 배포 게이트 및 게시 경로

- 통합 소스 Pin / 현재 버전 호환: 미실측 호스트 설치 버전을 가정하지 않으며 v1.6.72 변경을 버리지 않는다.
- **필수 릴리스 판정:** 원본 pin, 신규 최종 version/manifest·CRC·경로/심링크·민감정보 검사, 기존 호출/보안/회귀, 독립 코드 리뷰 결과·GPT 판정, 유효 공개 배송 승인. 미달 시 `BLOCKED_NOT_POSTED`; 이미 통과한 단계 재실행 강제 금지.
- 최종 `development_not_for_deployment` 해제는 위 게이트를 충족한 **새 최종 bytes**에만 적용. 개발 후보 ZIP을 이름만 바꾸어 PUBLIC 배송 금지.
- 완료 시 **`wonhwipark/L1Work` branch `main` 루트**에 `l1-fix-workflow_v1_6_73_1119.zip`을 처음으로 게시(최종릴리스 bytes의 SHA/크기 기록). 기존 공개 파일 덮어쓰기 금지. API 게시 후 PUBLIC raw ZIP 재다운로드 SHA-256 대조. 공개본 `POSTED`와 업무 Linux `INSTALLED/HOST_VERIFIED`는 별도.
- PRIVATE `CURRENT.md`, `TRACKER.json`에 최종 코드/실시험/리뷰/호스트/배송 상태와 commit·원격 내용·SHA-256을 확인해 갱신.

**현재 다음 한 동작:** Windows Claude Code의 **실 LIVE preflight + 지원되는 독립 코드 리뷰**와 업무 GPT 비민감 G0를 받아 병목을 해소. 실제 호스트 연결/정상 승인 증거 없으면 `INDEPENDENT_CODE_REVIEW=NOT_RUN`/`HOST_G0=NOT_VERIFIED`/`PUBLIC_RELEASE=BLOCKED_NOT_POSTED`; 이는 중단 선언이 아니라 기존 QA 성공·개발 후보를 보존한 정확한 운영 상태.
