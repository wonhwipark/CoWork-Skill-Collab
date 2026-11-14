# CLAUDE GitHub LIVE 컷오버 실행 결과 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-14 KST). **Claude 자체 보고**, GPT 판정 전 canonical 아님.
- 근거 인계서: `GPT_GITHUB_LIVE_CUTOVER_USER_APPROVAL_AND_GATED_ONE_SHOT_r0001_20261114.md`
- **결론: 컷오버는 실행하지 않았다(`CUTOVER_STATE=NOT_CUTOVER`, `ACTIVE_PROVIDER=NONE`).** 사용자의 LIVE 전환 승인은 그대로 반영했고 재질문하지 않았다. 전환을 막은 것은 승인 여부가 아니라 인계서가 정한 필수 게이트 3개이며, 아래 표의 `BLOCKED` 항목이다. 허용된 사전 작업(결함 수정·시험·후보 고정·후보 입력 게시·Notifier 비발송 리허설)은 모두 끝냈다.
- 실행하지 않은 것: 유료 모델 호출·신규 리뷰·신규 READY/서명/승인 생성, 운영 DB·Task·Notifier 변경, 운영 인터프리터 설치, 실 알림 발송, PUBLIC 게시, 비밀 발급/교체. Classic PAT는 그대로 사용(논의 없음).

## 1. 필수 표

| 항목 | 결과 | 증거 종류 / 구체 원인 |
|---|---|---|
| USER_LIVE_APPROVAL | **APPROVED** | 인계서 기록. 재확인 요청 0 |
| DEVELOPMENT | **PASS** | 격리 후보 `v0.2.19` 구현·고정(운영 설치본·기존 ZIP 불변) |
| SELF_TEST | **PASS** | 자체 시험(실측). 시험 venv 673 passed/12 skipped, 운영 인터프리터 606/17, 고정 ZIP을 풀어 673/12 재확인 |
| INDEPENDENT_REVIEW | **BLOCKED** (`BLOCKED_PAID_REVIEW_APPROVAL`) | `v0.2.19`에 대한 독립 리뷰가 없다. 확정된 대상 SHA·리뷰 ID·예산·호출 횟수에 대한 별도 승인이 없어 모델 호출 0. 동일 세션 자체 시험을 PASS로 승격하지 않음. v0.2.17 R2 결과는 소급 적용 불가 |
| N1_CRASH_DUPLICATE_0 | **PASS(자체 시험)** | §2. 크래시 주입 7지점 × 로컬 상태 유지/소실, 구 백업 복원. 실제 GitHub에서 예약 기록 원시 동작 확인 |
| N2_REPO_BINDING | **PASS(자체 시험)** | v0.2.18부터 서버 숫자 ID 결합, v0.2.19에 유지. 실제 서버 ID = 신뢰 루트 `repo_id` 일치 |
| CRYPTO_OPERATING | **BLOCKED** (`BLOCKED_OPERATIONAL_APPROVAL`) | 운영 인터프리터(Python 3.11.9)에 `cryptography` 없음 → 승인 검증 불가(fail-closed, 모델 0). 운영 패키지 설치에 대한 개별 승인 없음. 격리 venv 68개 실서명 시험은 이를 대신하지 않음 |
| PENDING_REQUEST_PRESERVED | **PASS** | §4. 운영 DB 원본 main/WAL 해시 불변, pending 1건·완료 60건·CONFLICT 1건 그대로 |
| NOTIFIER_MIGRATION | **PARTIAL**: 리허설 PASS / 설치 **BLOCKED** (`BLOCKED_OPERATIONAL_APPROVAL`) | §5. 비발송 리허설 통과, 운영 Notifier 변경 승인 없음 |
| ROLLBACK_TEST | **PASS(격리)** | 원본 DB 바이트 복사→격리 사본 무결성 ok→복원본 동일. 호스트 롤백 = 새 provider를 설치하지 않았으므로 현 상태 유지 자체가 롤백 상태 |
| HOST_INSTALL | **NOT_RUN** | 게이트 미통과. 설치 시도 0 |
| TASK_APPLIED | **NOT_RUN** | GitHub watcher Task 없음, 기존 Task 변경 0 |
| ACTIVE_PROVIDER | **NONE** | 변경 없음 |
| CUTOVER_STATE | **NOT_CUTOVER** | `LIVE`·`HOST_APPLIED`·`ROLLBACK_READY(호스트 적용)` 표시하지 않음 |
| MODEL_CALLS_DELTA | **0** | |
| PAID_COST | **$0** | |
| BLOCKED_REASONS | 3개 | ① v0.2.19 독립 리뷰 미승인 ② 운영 `cryptography` 설치 미승인 ③ 운영 Notifier 변경(+GitHub watcher Task/설정 설치) 미승인 |

## 2. 결함 수정: N1 잔여 갭 (v0.2.19)

- **갭(v0.2.18까지)**: 모델 호출 뒤 결과 업로드 전에 로컬 DB·로컬 결과가 사라지면, 원격에 아무 기록이 없어 같은 승인으로 2차 유료 호출이 가능했다. 크래시 주입으로 재현: v0.2.18에서 "모델 진행 중 / 결과 저장 전 / 게시 전 / 게시 실패 후" 4지점 + 상태 소실이 실패.
- **수정**: 모델을 시작하기 **직전**(클레임·스냅샷 뒤, REVIEW_RUNNING 전)에 원격 `dispatch/<요청ID>/DISPATCH_<revision>.md`를 **생성 전용**으로 기록. 서명·SOURCE_PIN·정책·횟수/비용 게이트 → 논리 키 확인 → 예약 → 모델 순서.
  - 기록 성공 → 진행. 기록이 있고 이 job의 것이며 로컬에 이전 시도(사용량 한도 거부) 이력 있음 → 진행. 기록이 있는데 로컬 이력 없음 → `REVIEW_UNCERTAIN`, 모델 0. 쓰기/조회 실패 → VALIDATED로 되돌리고 대기, 모델 0.
  - **동작 변화**: 원격 쓰기가 안 되면 유료 리뷰가 시작되지 않는다(Classic PAT 쓰기 가능 확인됨). 이 가정을 두던 기존 시험 2개를 "결과 업로드만 실패"로 바로잡고 "쓰기 전부 실패 → 모델 0" 시험을 추가.
- **시험(합성, 모델 0)**: 크래시 7지점(디스패치 직전, 예약 직후, 모델 진행 중, 결과 저장 전, 저장 후 게시 전, 게시 실패 `UPLOAD_PENDING`, 완료) × 로컬 상태 유지/소실, 구 백업 복원, 예약 쓰기 불가/조회 불가/타인 기록, 예약 1회 기록. 19개 통과. 모든 조합에서 모델 시작 횟수가 한 번을 넘지 않고 job이 사라지지 않음. **v0.2.18에서는 12개 실패**(회귀 증명).
- 이전 시험 통합: N2, v0.2.17 R1/R2 회귀(F1~F5, usage-limit 대기/재개), 실서명 68개, Windows `.cmd` 타임아웃/taskkill, publish-only 멱등성 — 전체 스위트에 포함되어 통과.
- 실제 GitHub(임시 브랜치, Classic PAT, 신규 요청·READY·모델 없음): 첫 예약 `RESERVED`, 로컬 이력 없는 감시기는 `FOREIGN`, 다른 revision은 독립 예약, 기록에 비밀 필드 없음, `main`에는 없음, 브랜치 삭제 확인.
- **정직한 한계**: 예약 직후~모델 시작 전에 죽으면 유료 작업 없이 예약만 남아 그 요청은 새 revision이 필요하다(fail-closed로 수용). 예약 기록 전에 DB가 사라지면 모델이 아직 시작되지 않았으므로 새로 디스패치하는 것이 맞다. 로컬 상태 소실로 `ALREADY_OURS` 재시도 가능성이 사라지는 경우는 안전 방향(`FOREIGN`)이다.

## 3. 후보 v0.2.19 (고정, `development_not_for_deployment`)

- `skill-collab-watcher_v0_2_19_1114_DEV_NOT_FOR_DEPLOYMENT.zip` **239,143 B**, sha256 `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`, 93개 파일, ZIP 무결성(CRC) OK, 경로 이탈 0, 비밀 스캔 findings 0, 재빌드 바이트 동일.
- v0.2.18 대비 변경 파일 6개(소스 `orchestrator.py`·`__init__.py`, 런북 제목, 시험 3). 이전 후보 ZIP(v0.2.17 `824f26c4…`, v0.2.18 `519c70e3…`) 바이트 불변.
- 이름 규칙: 정규명 `<skill>_v<major>_<minor>_<patch>_<MMDD>.zip` 대비 개발용 접미사 `_DEV_NOT_FOR_DEPLOYMENT`를 붙여 배포 후보와 구분(리뷰·승인 후 정규명으로 재생성 필요).
- PRIVATE 게시(입력만, 요청/READY/`packages/` 없음, 원격 바이트·CRC 일치): `review-inputs/REV-COWORK-V0219-20261114/` {ZIP `ee44e80898c5`, `REVIEW_MANIFEST.md` `264713d3d1c6`, `diff_v0_2_17_to_v0_2_19.patch` `58d8bb7f0691`}. 이 게시는 리뷰 신호가 아니며 모델 호출을 만들지 않는다.

## 4. 호스트 기준선 (무변경 확인)

- 운영 DB: 바이트 복사 방식(원본 SQLite 미개방). 원본 main 1,896,448 B sha256 `4e8bc33a6f6e…`, WAL 2,331,952 B `59de75073464…`, 최종 재확인까지 **불변**. 복사본 무결성 ok, jobs 61(COMPLETED 60, CONFLICT 1), audit_log 22,907, 진행 중 0, pending 1건(`L1-KNOWLEDGE-ROADMAP-DESIGN-20261109-001`, Dropbox 시절 요청), 백업=복원본 바이트 동일.
- Task: `Claude-Review-Watcher`·`Dashboard-Deploy-Bridge`·`Dashboard-Updater` 모두 Disabled, `Notifier` Running — 시작·종료와 동일, 변경 0. Python 프로세스는 Notifier의 venv 런처+자식 한 쌍뿐이며 감시기/리뷰어 프로세스 없음. GitHub watcher Task 없음.
- 관측: 이번 셸은 **관리자 권한**이다. 필요한 승인이 있다면 운영 변경 실행이 기술적으로 가능하다는 뜻이며 승인 대체가 아니다(운영 변경 0).
- pending 1건: 원본 DB에 그대로 보존. GitHub 감시기는 새 상태 폴더를 쓰도록 설계되어 이 요청은 **이행되지 않으며**, 필요하면 GitHub 요청으로 다시 제출해야 한다(무손실 격리 보존 상태).

## 5. Notifier 이행 리허설 (비발송, 운영 Notifier 불변)

- 설치된 Notifier는 실행·중지·수정하지 않고 파일만 읽어 임시 사본으로 시험. `send()`는 기록기로 대체해 Telegram 요청 불가.
- **발견(LIVE 전환 시 실제 사고 경로)**: 현재 Notifier는 DB 경로 1개 + `last_id` 워터마크 1개다. GitHub용 **새 상태 DB**로 바꾸면 id가 1부터 시작해 기존 `last_id`(22,907)보다 작아 **새 알림이 조용히 전부 누락**된다. 재현 통과.
- 격리 후보(DB별 워터마크, 설치 안 함, `notifier_candidate`): 기존 DB는 기존 워터마크 유지(이력 재전송 0), 새 DB는 현재 끝에서 시작(과거 3행 재전송 0), 새 DB 첫 실이벤트는 전송, 반복/재시작/원래 DB 복귀 시 중복 0, 워터마크는 DB 식별자별 저장. 11개 점검 통과(현재 코드 2 + 후보 9). 운영 DB 경로는 환경변수로 지정.
- 남음: 운영 Notifier 교체·재시작은 **미승인**(`BLOCKED_OPERATIONAL_APPROVAL`). 설치 시 단일 인스턴스 잠금은 기존대로.

## 6. 컷오버에 필요한 다음 사용자 결정 (한 번에)

1. `v0.2.19`(sha256 `6e7fee33…`, 입력은 PRIVATE에 게시됨) **독립 리뷰 1회**의 대상 SHA·리뷰 ID·정책·최대 예산·호출 횟수 승인. 권고: `POLICY-STATIC-V1-LARGE`(R2), 최대 $3, 1회, 변경 범위가 작아 v0.2.17→v0.2.19 diff 중심.
2. 운영 변경 승인 3종: ① 운영 인터프리터에 `cryptography` 설치(잠금 파일 해시 고정), ② 운영 Notifier를 DB별 워터마크 후보로 교체(워터마크 백업 후), ③ GitHub 감시기 상태 폴더·설정·Task 등록(기존 Dropbox 감시기는 재활성화하지 않음, 단일 provider).
3. 위 세 승인이 있으면 같은 인계 하나로 [리뷰 → 설치 → 최소 2주기+재시작 중복 0 확인 → 전환]을 이어서 실행할 수 있다. 하나라도 빠지면 해당 단계에서 정지하고 `ACTIVE_PROVIDER=NONE`을 유지한다.

## 7. 한계

- N1 수정과 v0.2.19는 **자체 시험**이며 독립 리뷰가 아니다. 새 후보의 독립 리뷰 전에는 LIVE 불가라는 인계서 조건을 그대로 적용했다.
- 실제 Claude 사용량 한도 문자열은 여전히 미관측(NOT_VERIFIED). 별도 계정 enforce SHADOW·장기 SHADOW는 이번에 실행하지 않았다(필수 독립 증거인 "운영 DB 무변경·별도 상태·GET-only SHADOW"는 앞선 단계의 통과 결과를 유지).
- Windows 전용. 비밀값·토큰·경로·계정명은 이 문서에 없다.
