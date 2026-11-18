# ACE·PEC-HOP·SAFE — 실제 후보 스킬 소스 G0 / 인터페이스·보존·읽기 전용 경계 대조 r0001

- 기준: 2026-11-18 KST / 기존 Work `COWORK-SKILL-DISCOVERY-20261112-001`
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / branch `main`
- 사용자 실행 지시: “진행” — 앞선 [26건 비민감 합성 계약 시험](GPT_ACE_PEC_SAFE_SYNTHETIC_REGRESSION_RESULT_r0001_20261118_KST.md)의 **실제 스킬 reader/Evidence/권한 소스 G0 대조**. 사용자 요청에 없는 설치·호스트 변경·업무 코드 조회·새 유료 리뷰/LLM 호출은 하지 않음.
- 설계 기준: [통합 설계 r0002](ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0002_20261118_KST.md), SHA-256 `8959c5785da37d0a7f48687fbbe17576c4f0f517be93ffcd9befc029a1c6def1`.
- **판정:** `SOURCE_CANDIDATE_G0=PASS_SCOPE_LIMITED`; `LIVE_INSTALLED_G0=NOT_VERIFIED`; `REAL_FUNCTIONAL_INTEGRATION=NOT_RUN`; `DEPLOYMENT_READY=NO`. 개별 메서드 존재/정적 조건만 확인. G0는 실제 호스트 설치·실행 검증과 구별.

## 1. 조회·증빙 범위

GitHub PRIVATE의 실제 ZIP raw bytes(base64 다운로드)에서 ZIP 중앙 디렉터리를 조회하고 관심 모듈의 DEFLATE 멤버를 추출. 각 멤버의 비압축 바이트 길이를 ZIP 메타데이터와 대조하여 PASS. 리포트에는 업무 제한 코드·개인 데이터·토큰·상세 MSC를 옮기지 않고 **공개 가능한 함수 시그니처·비민감 조건/판정**만 기록.

| 소스 스냅샷 | GitHub PRIVATE 실제 경로 | raw ZIP size / Git blob SHA (SHA-256 아님) | 검증 |
|---|---|---|---|
| Workflow 개발 후보 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_70_1117.zip` | 758,117 B / `5849cbdc8f3191c038fe66755caceac38d8225ab` | CENTRAL_DIR+관련 모듈 추출 크기 PASS |
| Kernel 개발 후보 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/work-ledger-kernel_v0_7_43_1117.zip` | 319,793 B / `cbfaa05e568802663f41d33b42c6f791897cbc40` | CENTRAL_DIR+관련 모듈 추출 크기 PASS |
| Code Analyzer 개발 후보 | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/code-analyzer_v0_15_3_1114.zip` | 574,469 B / `a661219a0c6c909bd2cb71fa849a81d795b93547` | CENTRAL_DIR+관련 모듈 추출 크기 PASS |

**주의:** 셋 모두 PRIVATE 개발 후보이며 실제 업무 Linux 설치본과 버전·해시·활성화 상태가 일치한다는 증거가 아님. `code-analyzer`의 기존 L1Work PUBLIC 버전과 PRIVATE 후보 버전을 혼동하지 말 것. 조회한 G0는 Python 코드 **정적 검토**, Python 실행/Windows/Linux/업무 설치 G0는 NOT_RUN.

## 2. 요구-기존 함수·검증·부작용 매핑

| 요구/시나리오 | 후보 내부 **실제 함수** 및 관측 소스 | 기존 기능 판단 | 아직 없는 증거 / 차단 |
|---|---|---|---|
| ACE-02 Work 이력 조회 | Workflow `l1_fix_workflow/work_inspection.py:260` `inspect_work(kernel, request, *, execution=None)`에서 `kernel.load_record`, `status`, `work_resume(...)` 조회, decisions/최근 이벤트·evidence/다음 액션 취합 | **REUSE** — 조회 출력 경로 존재; 혼합 read/write 요청은 `READ_WRITE_AMBIGUOUS`로 거부(263행) | 실제 기록 기반 최신 결정·승인 유효 범위/append 순서의 **결정형 판별기** 존재 미확인. `brief.decisions` 원문이 누락됐을 때 날짜·ref가 `None`인 파생 항목을 추가(314~318행)하므로 이 항목만으로 최신 판정 불가→HOLD |
| ACE-02 워크 재개·원본 출처 | Kernel `work_ledger_kernel/continuity.py`의 `TLContinuity.resume(work_id)`, `work_refs.py`의 `WorkReferences.read(work_id)`·`find(query)`; Workflow `work_router.py`의 `probe_local_work_list_read_only` | **REUSE** — Work ID·Jira 참조 및 최근 상태 조회 계열 실존 | 일치하지 않는 참조/오래된 승인·동일 Work 충돌 시 실제 출력·보존은 설치본으로 시험 필요. `resume`과 그 하위 IO가 읽기 전용인지 파일 diff로 확인 전 E2E PASS 금지 |
| PEC-01/03 기존 Evidence 유입 | Workflow `l1_fix_workflow/feature_evidence.py:15~71` `attach_evidence(kernel, *, work_id, source_path, provider, provider_version, code_rev, evidence_kind, summary, apply=False, expected_sha256=None, expected_revision=None, ...)` | **REUSE/CONNECT** — 기존 승인 provider/registry 검증, symlink 금지, MD/JSON/Mermaid/TXT 및 5MiB 제한, `read_bytes`→전체 SHA-256, 이미 기록된 digest+provider+kind 중복 차단, `apply=False` 시 `FEATURE_EVIDENCE_PREVIEW`; `apply=True`는 writer+기대 SHA/revision 검사 후 Kernel 기록 | **현재 ZIP의 이 함수는 전체 파일 SHA만 계산(39~40행)**. 특정 `byte_offset/byte_length` 발췌 digest와 비교하는 기능은 관찰되지 않음. `apply=False` 모드는 승인 없는 최종 기록을 하지 않지만 Kernel 생성/하위 조회 부수효과 전체는 별도 G0 |
| PEC Evidence 정본 필드 | Kernel `work_ledger_kernel/validation.py:92~99` `validate_evidence_meta`: `id,kind,stage,path,sha256,provider,provider_version,code_rev,created_at,summary,confidence_state` 등 필수 | **REUSE** — 출처/전체 digest/confidence 보존 필드 이미 존재. 별도 Kernel schema 추가 불필요 | Evidence meta `sha256`은 발췌 byte-range 보증이라고 과장 금지. 발췌 무결성이 필요한 경우 **기존 provider raw bytes로 별도 읽기 전용 비교** 후 기존 evidence pointer와 연결; 입증된 필요 전 신규 persistent field 추가 금지 |
| PEC 반복 분석 방지/고정 source | Code Analyzer `scripts/ca_core/reuse_validator.py:20~82` `validate(manifest,resolution,requested_baseline=None)`: source fingerprint/build context digest/dependency snapshot 대조; `REUSE_UNKNOWN/REFRESH_REQUIRED/PARTIAL_REUSE/EXACT_REUSE/COMPATIBLE_REUSE` 반환 | **REUSE/CONNECT** — 기존 source/build 재사용 판정 존재 | 해당 비교는 파일군 fingerprint·build context 수준이며 인용구간 byte 검증과 동일하지 않음. `provenance_resolver.resolve(...)`는 P4 조회/결과 기록 경로도 있으므로 무검증 G0에서 직접 호출 금지 |
| SAFE-01 무변경 Work 조회 | Workflow `work_inspection.py:260~263` 함수 설명에 “Only kernel reads” 명시. `continuity_flow.py:47~75`는 자연어 write intent를 감지하면 실행하지 않고 명시적 checkpoint/switch/review operation을 요구 | **REUSE 후보** — 조회/수정 분리 근거 존재 | `kernel.load_record/status/work_resume`가 신규 데이터/복구 파일을 쓰는지와 세션 초기화 작업은 별도 실제 스냅샷 검증 필요 |
| SAFE-01 부수효과 반례(중요) | Kernel `work_ledger_kernel/storage.py:13~17` `LedgerStorage.__init__`은 `self.root.mkdir(parents=True, exist_ok=True)` 호출. `read_json`(47~53), `read_journal`(81~93)은 조회 코드; `atomic_write_json`·`append_journal`은 명시적인 쓰기 | **G0 확인된 위험 경계:** 단순 `Kernel` 객체 생성만으로도 root가 없는 경로에는 디렉터리 생성 가능. “read-only” 명령의 이름만으로 쓰기 0이라고 판단 불가 | 실제 읽기 전용 파일럿은 **기존 읽기 전용 fixture / 삭제 가능한 격리 루트**에서 실행 전후 트리·mtime·SHA 대조. root 미존재에 직접 객체 생성·업무 데이터 경로 임의 지정 금지. 기존 빈 폴더 생성 여부를 포함해 일체의 변경 관찰 시 FAIL |
| SAFE-03 완료 리뷰 중복 방지 | CoWork의 기존 `APPROVAL_SIG.json/READY.md/DISPATCH_1.md/REVIEW_RESULT_1.md/RECEIPT_1.md` 체인 검증은 기존 Work에서 완료 | **REUSE** — 기존 watcher 운송/서명/완료 이력 변경 없이 유지 | L1 Work 조회 시험의 안전성으로 CoWork watcher 서명 검증을 대체하지 않음; 기존 R1 재큐잉 금지 |

### PEC-HOP 최소 연결 판정

기존 Evidence `sha256`은 **파일 전체** 검증에 재사용. §4.1의 발췌 문자열/IPC/조건을 **원본 bytes의 정확한 범위와 비교**하는 로직이 필요하면, 먼저 Code Analyzer/Workflow가 실제 추출 결과에 원본 file revision·byte offset/length를 이미 제공하는지 설치본에서 조회. 없으면 `PARTIAL_EVIDENCE/HOLD`로 두고, 추후 기존 producer/검증 호출부에만 최소 read-only 연결을 검토. 원문/metadata가 없다는 이유로 새 Kernel field/영속 원장/자동 analyzer 호출을 만들지 않음.

### ACE 결정 판별 최소 연결 판정

`inspect_work()`가 제공하는 `decisions`의 항목들은 승인/원문 순서가 완전히 보존된다는 보장이 없음. ACE-02는 **원래 Work decision/context journal의 timestamp 외 정본 append/revision 순서와 사용자 승인 범위**를 유효하게 확인할 때만 최신 결론 선택. `brief.decisions`에서 ref/date를 잃은 파생 항목을 최신 결정으로 승격하지 않음. source revision/승인 범위·원본 이력이 누락되면 HOLD.

## 3. 실제 기능·호스트 시험으로 연결하는 최소 G0 절차 (미실행)

1. **실제 Linux 설치 사실 먼저 고정:** 업무 GPT/Agent가 허용된 호스트에서 실제 `l1-fix-workflow`, `work-ledger-kernel`, `code-analyzer`의 설치 경로/버전/원본 SHA·import resolution·활성 provider를 **READ_ONLY**로 확인. 개발 후보와 다른 경우 별도 diff/호환 검토, 설치 덮어쓰기·자동 updater 금지.
2. **ACE Work 읽기:** 회사 자료가 아닌 승인된 비민감 합성 Work/격리 fixture만 사용. `inspect_work`·Kernel resume/read calls를 실제 import 경로로 실행. 입력 전/후 전체 fixture tree/모든 파일 SHA/mtime/디렉터리 목록을 비교, 생성·변경이 있으면 FAIL. 원본 결정/append 순서, 승인 범위 부재 시 HOLD.
3. **PEC raw byte:** fixture에 합성 CL/PR/IPC·Unicode 포함한 정상 발췌/1-byte 오염·offset 미상·권한 없는 경로를 준비. 기존 `attach_evidence(apply=False)`의 `FEATURE_EVIDENCE_PREVIEW`와 digest 검증을 실행할 때는 **실제 기존 registry/provider/profile의 허용 범위** 확인 선행. 쓰기 권한/등록이 없어 거부되면 NOT_RUN/BLOCKED로 구분. **절대 `apply=True` 금지**; 원문 바이트 구간 검사는 기존 producer와 별도 read-only 검증으로 대조.
4. **SAFE:** 정상 조회에서 어떤 파일·폴더·Job·READY·모델 호출도 발생하지 않는지 호스트 로깅/fixture 전후 SHA와 함께 검증. `LedgerStorage.__init__`의 root mkdir 가능성을 미리 포함. 실제 업무 Work, group writer, Git/P4 작업 변경 0.
5. **결과:** 각 시험 `PASS/FAIL/SKIP/NOT_RUN`, 실행 호스트/설치 경로·버전·대상 스냅샷 revision, 입력 synthetic ID, 전후 file digest, 오류/접근 차단, 민감정보 제외한 결과만 **기존 Work**로 회수. 실패 시 기능 변경보다 원인·재현 범위·필요 승인부터 판정. 재리뷰/유료 재호출 없이 동일 Work에서만 보완.

## 4. 범위별 최종 결론

| 항목 | 판정 | 다음 한 행동 |
|---|---|---|
| 기존 Work/참조/Decision reader | `SOURCE_G0=PASS_SCOPE_LIMITED` | 실제 설치본에서 `inspect_work/work_resume` 결과 및 append 순서의 참조 유지 확인 |
| 기존 Evidence writer/preview | `SOURCE_G0=PASS_SCOPE_LIMITED` | 기존 `attach_evidence(apply=False)`와 registry/provider 지원 확인 |
| 원문 **구간** SHA 판별 | `CONNECT_GAP_POSSIBLE` / 구현 미확정 | 실제 producer가 byte offset/length를 제공하는지 G0, 없으면 HOLD |
| source revision/fingerprint 재사용 | `SOURCE_G0=PASS_SCOPE_LIMITED` | Code Analyzer 실제 활성 경로/매니페스트·dependency snapshot 고정 |
| 'read-only' side effect | `SOURCE_RISK_CONFIRMED` (`LedgerStorage` mkdir) | 실제 fixture 전후 파일·디렉터리 트리 동일성 시험 |
| 업무 Updater 설치/그룹 writer / G0 | `NOT_VERIFIED` | 업무 GPT 별도 G0 회신; CoWork에서 설치/Knowledge write 금지 |
| ACON baseline/compressed 각 3회 | `NOT_RUN` | 유효 비용/모델 호출 승인 전 실행 금지 |
| 기존 독립 리뷰 R1 | `CLOSED` | 동일 REQUEST/ZIP/READY/영수증 무수정·재실행 0 |

**NEXT_ONE_ACTION:** 실제 Linux 설치본에 대해 업무 GPT/허용된 Agent의 **비민감 synthetic fixture 읽기 전용 G0**를 수행하여 `inspect_work`·`attach_evidence(apply=False)`·Kernel resume와 source excerpt 연결 경계를 실측. 결과가 오면 같은 Work에서 기능 통합 시험의 실제 재사용 가능성 및 최소 변경 여부를 판정. 현재 CoWork 도구로는 업무용 Linux 파일·설치 환경에 접근할 수 없으므로 `HOST_G0=NOT_RUN`. 자동 호출·새 유료 리뷰·운영 배포 없음.
