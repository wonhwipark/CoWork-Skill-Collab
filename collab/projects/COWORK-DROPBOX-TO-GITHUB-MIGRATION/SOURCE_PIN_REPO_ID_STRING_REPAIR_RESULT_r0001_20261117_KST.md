# SOURCE_PIN.json repo_id 문자열 포맷 수정·실제 두 요청 보정 결과

- 일자: 2026-11-17 KST
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: 협업 운송 `COWORK-DROPBOX-TO-GITHUB-MIGRATION` / 연계 L1 리뷰 `L1-WORKSPACE-RAG-20261111-001`
- 출처: Windows Claude Code가 사용자에게 전달한 `approval.py` `REPO_ID_MISMATCH` 증상·원인·수정 제안. GPT가 GitHub에 게시된 두 SOURCE_PIN 원본을 직접 조회해 타입 오류 독립 확인.
- 작업 지시: 사용자 "수정해줘". 수정 범위는 SOURCE_PIN 생성·검증과 해당 두 오류 파일의 `repo_id` JSON 타입만. 새 승인/READY, 유료 독립 리뷰, Windows 설치·운영 설정 변경·모델 재호출은 요청/실행하지 않음.

## 1. 확인 원인과 안전 판정

- 실제 GitHub repository numeric ID는 `1451933830`. 신뢰 루트에서는 문자열 `"1451933830"`을 사용. 두 오류 요청은 `repo_id: 1451933830`(JSON 숫자), 이전 정상 요청은 `repo_id: "1451933830"`(JSON 문자열).
- `SKILL_COLLAB_SOURCE_PIN_V1` 필드·schema는 유지. 생성 시 `str(repo_id)`를 적용. **이미 게시된 숫자형 pin의 자동 강제변환은 하지 않고 거부**해 watcher의 fail-closed 동작 유지.
- Windows 보고: `REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117` 자동 서명 시도 1회, `AUTO_SIGNING_UNCERTAIN`, 서명/READY/모델 호출 미발생. `REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117`도 같은 타입 문제. **호스트 SQLite/local audit는 GPT 직접 접근·검증 불가**, `AUTO_SIGNING_UNCERTAIN`이 TYPE 수정으로 자동 해제되었다고 주장하지 않음.
- 고정 REQUEST/패키지 SHA/Commit A·이전 Git blob과 모든 다른 이력은 불변. 변경 전 원본 SOURCE_PIN의 Git blob·commit은 Git 이력에 보존.

## 2. 실제 PRIVATE main 수정

| 파일/대상 | 내용 | 게시 commit | 최종 SHA-256 |
|---|---|---|---|
| `collab/ops/source_pin.py` | 공통 V1 JSON 생성기·검증기; `repo_id`를 문자열로 직렬화, 기존 숫자형은 거부, 로컬 생성 시 덮어쓰기 금지, 전체 요청 pin 읽기 전용 감사 | `c995e8db4720`, `fb86244ea6fa` | `878ef5330e9d1b66d9539a49eb04c02423e585ac9afc356a41789ad8eaea1bf6` |
| `collab/ops/tests/test_source_pin.py` | 문자열 인코딩·기존 숫자형 차단·repo mismatch·schema/commit·덮어쓰기 금지·전체 pin 감사 13개 회귀 | `e2bf811457eb`, `d04dcf0b9b35` | `2540b9ab33d7f18ef247ece5446776cec5c7f96d1f0c1b7776fa9adb6217ed37` |
| `.github/workflows/cowork-dashboard.yml` | 기존 PRIVATE Action에 13개 시험 + 전체 `SOURCE_PIN.json` 타입/ID 감사 추가; source_pin 도구 변경 시에도 재실행 | `ecce77e03f4f`, `780f25f77d1b` | `237cc92cd57f0628286ac6ef4bd450244e1415cb643eb6c6803a0ac90bae441c` |
| Guard 코드 R1 `SOURCE_PIN.json` | `repo_id` 숫자 → 문자열, commit `b2edf8b090b292163864cfbf670c77d1ad09c058` 및 schema 유지 | `75a7842bf16f` | `b34ec49a4f9b6cd9bea425581903c290304c9539f97ab70719fe81f807aa7c0e` |
| MSC 설계 R1 `SOURCE_PIN.json` | `repo_id` 숫자 → 문자열, commit `939b5b9f4c59534d908bc48ced59cfd25a4e8f64` 및 schema 유지 | `e09affba5e71` | `d1f9c614b3dfd3a98c5804d69f81877fc598c4dea1dae6ffe583edf6e6080bcf` |
| `collab/START_HERE.md` | 차후 모든 SOURCE_PIN 생성·게시 전 문자형 검증을 고정 절차로 기록 | `b88459480fce` | `cf5dabe21065cf256b3adffb0be2dd393fefd3c7fded9191cf2d6e5917fc1882` |

- **원본 보존:** Guard pin 변경 전 Git blob `dd9c2984c743d7d73f56b42ef5dc88f8ca740659`; MSC 변경 전 Git blob `2ebb6f9d8264b6420a46c03de59eb8cb0a6c0d06`. 두 파일은 사용자의 명시적 포맷 수정 지시로 **해당 JSON 필드 타입만** 바뀌었으며 원본 바이트 이력은 보존됨.
- **변경 전 선행 확인:** 두 요청 모두 `APPROVAL_SIG.json`, `READY.md`, `DISPATCH_1.md`, `REVIEW_RESULT_1.md`, `RECEIPT_1.md` 원격 미발견. 변경 이후 같은 파일들의 원격 디렉터리 확인에서도 여전히 미발견. 이 미발견을 Windows watcher 실제 로컬 DB/예약 상태 미존재라고 단정하지 않음.
- 최종 SOURCE_PIN JSON은 정확히 `{"schema":"SKILL_COLLAB_SOURCE_PIN_V1","commit":"<원래 Commit A>","repo_id":"1451933830"}` 형태. **GPT가 승인 서명/READY를 만들거나 리뷰를 재실행한 적 없음**.

## 3. 시험·증빙

- 로컬 Python `unittest`: `13/13 PASS`, 생성기 구문 검사 PASS, 네트워크·watcher·LLM 호출 0.
- PRIVATE Actions [run #43983008308](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43983008308): `completed/success`.
- 해당 실제 Actions job 로그: `SOURCE_PIN` 회귀 `13/13 PASS`, GitHub PRIVATE에 존재하는 **11개 SOURCE_PIN 전부** V1 schema / `repo_id` JSON 문자열·`1451933830` 일치 검사 PASS. 대시보드 `77/77 PASS`, PUBLIC preview `8/8 PASS`.
- 결과 파일·수정 파일 모두 GitHub PRIVATE `main` 원격 readback과 실제 UTF-8 SHA-256 확인.
- 사용자 승인된 기존 자동 리뷰 위임은 **watcher 로컬 정책·남은 일/월 비용·중복·불확실 상태를 모두 통과한 경우**만 유효. GitHub 수정만으로 실제 재서명·자동 리뷰 완료를 주장하지 않음.

## 4. 정확한 후속 경계

- `SOURCE_PIN_FORMAT_FIX=PASS_REMOTE_VERIFIED`, `SOURCE_PIN_GLOBAL_AUDIT=PASS_11`, `LOCAL_TEST=PASS_13`, `GITHUB_ACTIONS=PASS`.
- `AUTO_SIGNING_UNCERTAIN_HOST_STATE=USER_REPORTED_UNRESOLVED`, `APPROVAL_SIG_READY=NOT_OBSERVED_AT_CHECK`, `REVIEW_RESULT_RECEIPT=NOT_RECEIVED_AT_CHECK`, `WINDOWS_HOST_TEST=NOT_RUN`.
- `NEW_GPT_CREATED_READY=0`, `NEW_GPT_APPROVED_CALLS=0`, `GPT_TRIGGERED_CLAUDE_REVIEWS=0`, `WINDOWS_OPERATIONAL_CHANGE=0`. 감시기가 미래에 기존 유효 위임 범위 내에서 수행할지 여부는 **별도 실제 결과로 판정**.
- **NEXT_ONE_ACTION:** Windows Claude Code가 Guard의 `AUTO_SIGNING_UNCERTAIN` 로컬 예약·서명 시도·호출 이력(0 여부)과 MSC 기존 상태를 **읽기 전용으로 먼저 정산**. GitHub 두 SOURCE_PIN 원격 readback을 확인하고, 불확실/중복 기록이 남아 있으면 **자동 재큐잉·모델 재호출 금지**. watcher의 정상 신규 처리 조건을 충족할 때만 기승인 범위의 기존 리뷰 1사이클 진행. GPT는 실제 REVIEW_RESULT/RECEIPT 도착 시 기존 Work에서 1회 판정.
