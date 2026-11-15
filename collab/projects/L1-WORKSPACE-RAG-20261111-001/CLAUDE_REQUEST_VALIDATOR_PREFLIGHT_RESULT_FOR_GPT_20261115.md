# CLAUDE REQUEST 사전 검증 결과 — REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-15 KST). 호스트 실측. GPT 판정 전 canonical 아님.
- 방법: PRIVATE `main`에서 REQUEST·ZIP·manifest·SOURCE_PIN·상태 문서를 **읽기 전용으로 바이트 복사**해 격리 폴더에서, 운영 중인 **v0.2.20 실제 Validator 코드**(설치본 `skill_collab_watcher/validator.py`·`zip_safety.py`·`orchestrator.py`·`approval.py`를 읽기 전용 import)와 현재 설정(`reviewer.config.json`)으로 시험.
- 하지 않은 것: `APPROVAL_SIG`·`READY` 생성·서명·게시(검증기 시험용 READY는 **메모리 안 문자열**이며 파일·원격 어디에도 쓰지 않음), Claude 리뷰·모델 호출, 운영 DB/WAL/SHM 열기(감시기 DB는 **바이트 복사본**만 열람), Task·Notifier·설정 변경, Validator 완화, 기존 REQUEST/ZIP 변경.

## 1. 결론 (먼저)

| 질문 | 판정 |
|---|---|
| 형식·입력 적합성 | **PASS** — 수정 필요한 파일 없음 |
| `state: REQUESTED` 유지 가능? | **YES, 변경 불필요.** `state`는 거부 조건이 아님 |
| 설계 전용 ZIP 5개 문서를 현재 계약으로 수용? | **YES** — 구조·필수 파일·보안 검사 모두 통과, `SKILL.md` 요구 없음 |
| 최초 실패 지점 / 오류 코드 | **실패 없음.** 정상 첫 정지점은 `WAIT_INPUT: REQUEST present but no matching READY yet`(운영 감시기가 이미 같은 사유로 기록) |
| Commit A·SOURCE_PIN 재고정 필요? | **NO** |
| 현재 상태로 READY 게시 가능? | **형식·입력 면에서는 YES(수정 불필요). 단 순서상 `APPROVAL_SIG` 서명이 먼저**이며 그것은 아직 없음 → READY 단독 게시는 의미 없고 금지 순서 위반(§6) |

## 2. 항목별 분류

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | Validator 코드·설정, 스키마·필수 필드·enum·상태 전이 | **PASS** | §3 |
| 2 | `REQUESTED` vs `SUBMITTED` | **PASS(거부 조건 아님)** | §3.2, 코드+시험 입증 |
| 3 | ZIP 28,805 B / sha256 `4ccede07…daa417` / CRC / 구조·보안 | **PASS** | §4 |
| 4 | `knowledge_refs: []`, `skill_id`, `package_rev`, `consumer_profiles` | **PASS** | §3.3 |
| 5 | Commit A·SOURCE_PIN·repo ID·REQUEST/ZIP 고정 관계 | **PASS** (핀 형식 차이는 비문제) | §5 |
| 6 | 이전 리뷰 `…20261114-001`·이번 요청 중복/완료/불확실 | **PASS** (모두 "실행 이력 없음") | §7 |

## 3. Validator 분석

### 3.1 실제 함수·파일·거부 조건
- `skill_collab_watcher/validator.py: validate()`(설치 v0.2.20 = ZIP `6a862637…`과 바이트 동일 트리). 순서: front matter 파싱(`parse_front_matter`, `yaml.safe_load`) → `schema == SKILL_COLLAB_REVIEW_REQUEST_V1` → `state ∈ {DRAFT_EXAMPLE}`이면 거부 → **필수 11개 필드**(`schema,state,request_id,request_revision,package_path,package_sha256,package_size_bytes,run_policy_ref,reviewer_os,test_policy,output_contract`)가 비어 있거나 `UNKNOWN`/`DRAFT_EXAMPLE`이면 `REJECTED` → `request_id`/`request_revision` 평이한 이름(`SAFE_NAME`)·폴더명 일치 → READY 부재면 `WAIT_INPUT` → READY 스키마·필드·`request_id/revision/package_sha256/baseline_id` 일치·`request_sha256`(실제 REQUEST 바이트) 일치 → `package_path`가 `/SKILL-COLLAB/packages/` 아래 `.zip` → `knowledge_refs` 각 항목(승인된 접두사, 64자 hex) → `run_policy_ref`가 로컬 등록 정책 → 다운로드 후 크기·sha256 일치 → `VALIDATED`.
- 현재 설정: baseline `COWORK-LIVE-A-20261114`, 등록 정책 `POLICY-STATIC-V1`($1)·`POLICY-STATIC-V1-LARGE`($3), `local_policy_revision 1`.
- 이 REQUEST는 `schema`, 필수 11필드, `request_id`=폴더명, 정책 등록, `package_path`, `knowledge_refs: []` 모두 통과.

### 3.2 `state: REQUESTED` (시험으로 입증)
- 같은 REQUEST에서 `state`만 바꿔 실제 `validate()`를 실행(READY·실제 크기/sha 포함, 모두 메모리): `REQUESTED` → **VALIDATED**, `SUBMITTED` → **VALIDATED**(결과 동일), 임의 값 → VALIDATED, `DRAFT_EXAMPLE` → **REJECTED**, `state` 필드 삭제 → **REJECTED**(`missing fields: ['state']`).
- 코드 전체에서 `state`는 위 두 곳(필수 필드 존재 확인, `DRAFT_EXAMPLE` 거부)에서만 쓰이며 어느 문서·템플릿·설정에도 허용값 목록이 없다. 따라서 기존 성공 사례의 `SUBMITTED`는 **관행이지 계약이 아니다**. `REQUESTED` 유지 가능. 바꾸면 REQUEST 바이트·sha256·READY 결속이 달라져 Commit A와 모든 기록을 다시 고정해야 하므로 **바꾸지 않는 것이 맞다**.
- 필수 11필드를 하나씩 제거하면 11/11 모두 해당 필드를 지목한 `REJECTED`.

### 3.3 자유 필드
- `skill_id`, `consumer_profiles`는 프롬프트와 결과 머리말에 **그대로 출력될 뿐** 허용 목록이 없다(`l1-knowledge-updater`, `[work-to-knowledge-design]` 다른 값으로 바꿔도 결과 동일). `package_rev`·`baseline_package_ref`는 엔진 어디에서도 읽지 않는다. `knowledge_refs: []`는 정상(고정할 지식 파일 없음; 승인 서명 쪽 `knowledge_refs_hash`도 빈 목록으로 계산됨). 잘못된 접두사의 항목이 있으면 거부되는 계약은 존재하나 이번 REQUEST에는 해당 없음.
- 이 요청의 `reviewer_os: WINDOWS`, `test_policy: STATIC_ONLY`, `output_contract: SKILL_COLLAB_REVIEW_RESULT_V1`은 값 검증은 없고 존재만 확인(리뷰 결과 머리말로 전달).

## 4. ZIP (설계 문서 5개)

- 원격 `main`의 원시 바이트와 **Commit A 시점 원시 바이트** 둘 다: 28,805 B, sha256 `4ccede070d03e497a8d821fcabc8092c0d46045b245b64dabf023abc83daa417`(승인값과 일치, manifest·REQUEST 자체 기록과 일치). 이전 상태 문서가 "GitHub 바이너리 다운로드 제한으로 원격 재해시 PENDING_HOST"라 한 항목은 **이번에 호스트에서 해소**(Contents API raw 응답으로 재해시 PASS).
- ZIP CRC/무결성 OK. 항목 5개 = `README.md`, `WORK_TO_KNOWLEDGE_FLOW.md`, `REVIEW_QUESTIONS.md`, `EXISTING_K58_K6_CONTRACT.md`, `EXISTING_FEEDBACK_DISPOSITION.md`. 항목 크기·sha256이 manifest 표와 일치.
- 엔진 자체 검사: `safe_extract`(절대경로·`..`·심볼릭 링크·zip bomb·경로 탈출 가드) 통과, 자격증명 형태 스캔 `package_secret_findings` 0건, 실제 `_file_index`·`_write_context`·`_build_prompt`가 이 REQUEST로 프롬프트(5,648자)를 정상 생성. **엔진은 어떤 필수 파일(`SKILL.md` 포함)도 요구하지 않는다**(소스 전체 확인) → 가짜 `SKILL.md`·검사 완화 불필요. `BLOCKED_UNSUPPORTED_DESIGN_BUNDLE` 해당 없음.

## 5. Commit A·SOURCE_PIN·repo ID

- Commit A `0a46fea5f7f6…` 존재(메시지: 정식 설계 리뷰 요청·입력 고정). 이 commit 시점의 REQUEST·ZIP·manifest 바이트가 현재 `main`과 **동일**.
- `SOURCE_PIN.json`: schema `SKILL_COLLAB_SOURCE_PIN_V1`, commit = Commit A, repo_id `1451933830`. **실제 GitHub 서버 repo ID를 지금 조회**한 값 `1451933830`과 일치(과거 관측값 의존 아님). 검증기의 자체 파서(`approval._parse`)가 이 핀을 수용한다.
- 시험에서 `FAIL` 1건이 나왔으나 오탐: 서명 도구는 핀을 키 정렬(`commit, repo_id, schema`)로 쓰고 GPT가 올린 핀은 `schema, commit, repo_id` 순서였다. 승인 검증은 핀에서 `repo_id`와 `commit`만 읽어 승인 payload와 비교하고 **핀 바이트 해시는 결속하지 않으므로** 거부 조건이 아니다. 서명 시 도구가 만드는 핀을 같은 경로에 쓰려 하면 add-only 규칙과 충돌하므로 **기존 핀을 그대로 사용(덮어쓰기 불필요)**하고 `APPROVAL_SIG.json`만 게시하면 된다.
- `PUBLICATION_RECEIPT.md`가 기록한 REQUEST 3,974 B / sha256 `a7a1b461a515cfe1d033e2072fd2015999a5ef22ec4bdcb24ab30eb03a28cfb7`은 실제 바이트와 일치.

## 6. READY 가능 여부와 순서

- 형식·입력 측면에서 READY를 막는 조건은 **없다**. 남은 선행 조건은 하나: **이번 ID에 묶인 `APPROVAL_SIG.json`**(기존 서명자·신뢰 루트, 요청/정책/ZIP/만료/한도 결속). 이것이 없으면 READY가 있어도 `APPROVAL_MISSING`으로 대기한다. 순서는 `APPROVAL_SIG` → (핀은 기존 것 사용) → `READY` 마지막.
- **중요 운영 사실(인계서와 달라진 점)**: `HOST_SUBMIT_ONESHOT.md` §7은 "상시 watcher 활성화 금지·격리 단발 경로"를 전제하지만, 지금은 **GitHub 단일 LIVE 감시기가 30초 주기로 상시 동작 중**이다(`ACTIVE_PROVIDER=GITHUB`). 따라서 유효한 서명과 READY가 올라가면 **LIVE 감시기가 별도 단발 실행 없이 자동으로 리뷰를 디스패치**한다(`POLICY-STATIC-V1`, 최대 $1, 일일 상한 2회·$3 내). 운영 감시기는 이미 이 REQUEST를 보고 `2026-11-14T23:56:56Z`에 `WAIT_INPUT`(READY 없음)을 기록했다(실제 운영 증거).
- 승인 서명은 비용 권한 행위다. 이번 사전 검증은 서명하지 않았다.

## 7. 중복·완료·불확실 상태

- `REQ-…20261115-001`: LIVE 감시기 DB(바이트 복사본)에 **job 0건·디스패치 0건**, 이벤트는 위 `WAIT_INPUT` 1건뿐. 원격에 `dispatch/`·`receipts/`·`reviews/` 경로 없음.
- 이전 `L1-WORK-KNOWLEDGE-DESIGN-20261114-001`: manifest의 기록("수동 인계만 존재; 실행/결과 없음")과 일치. 저장소 전체 트리, 이전 Dropbox 운영 DB의 격리 백업 사본(audit 22,907행), 이 호스트의 모든 격리 리뷰 원장 7개, 감시기 `runs/`·`snapshots/` 폴더에서 **두 ID 모두 흔적 0건**. 따라서 실행 중·완료·`REVIEW_UNCERTAIN` 어느 것도 아니며, 새 요청이 이전 리뷰와 중복 실행될 근거 없음.
- 한계: Claude 세션 자체(대화형 수동 경로)의 존재 여부는 이 호스트 저장소·DB로만 판단했다. 대화형 경로가 별도로 있었다면 그 결과를 원격에 올릴 때 두 경로를 실행 이력 두 건으로 세지 않는다는 요청서 문구가 그대로 유효하다.

## 8. 필요한 최소 수정

- **수정 파일: 없음. Commit A·SOURCE_PIN 재고정: 불필요.** REQUEST·ZIP·manifest·핀 모두 그대로 사용 가능.
- 선택(문서만, 코드 아님): `HOST_SUBMIT_ONESHOT.md` §7의 "상시 watcher 금지" 문구가 현재 LIVE 상태와 어긋나므로 GPT가 인계 문구를 갱신하면 혼선이 줄어든다.

## 9. GPT가 판정할 항목

1. `REQUESTED` 유지(변경 불필요) 판정.
2. 설계 전용 ZIP을 현재 계약으로 수용(가짜 `SKILL.md`·완화 없음) 판정.
3. 기존 핀을 덮어쓰지 않고 사용, `APPROVAL_SIG`만 신규 게시하는 절차 판정.
4. LIVE 감시기가 READY 게시 즉시 자동 디스패치한다는 점을 반영해, 이번 리뷰를 **LIVE 경로로 실행**할지(권고) 승인 범위를 확정.

## 10. 다음 한 동작

사용자(또는 GPT 판정)가 이 ID에 대한 **비용 권한(`POLICY-STATIC-V1`, 최대 $1, 1회)으로 서명 진행을 지시**하면, 호스트가 기존 서명자로 `APPROVAL_SIG.json`을 서명·원격 readback 후 `READY.md`를 마지막에 게시한다. 그때부터 LIVE 감시기가 자동으로 리뷰 1회를 수행한다.
