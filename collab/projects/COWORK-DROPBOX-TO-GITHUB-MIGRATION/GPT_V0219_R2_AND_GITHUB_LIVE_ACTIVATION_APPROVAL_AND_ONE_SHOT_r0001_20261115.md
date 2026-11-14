# GPT → Windows Claude Code 원샷 — v0.2.19 독립 R2 1회 + GitHub LIVE 활성화

- 개정: `r0001`, 2026-11-15 KST
- **GitHub PRIVATE**: `wonhwipark/CoWork-Skill-Collab`
- **Branch**: `main`
- **이 문서의 정확한 상대 경로**: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_APPROVAL_AND_ONE_SHOT_r0001_20261115.md`
- **Work ID**: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- **사용자 통합 명시 승인**: "A안 v0.2.19 독립 R2 리뷰 1회(최대 $3)와 B안 Windows 운영 변경 3종을 모두 승인해. 기존 GitHub LIVE 전환 승인 유지. 필수 검증 통과 후 원샷으로 전환해줘."
- **승인 상태**: `A_R2_APPROVED=YES`, `B_OPERATING_CHANGES_APPROVED=YES`, `LIVE_CUTOVER_APPROVED=YES`, `CLASSIC_PAT_CONTINUED=YES`.
- **작성 시점 실제 실행 상태**: `WINDOWS_EXECUTION=NOT_RUN`, `NEW_REVIEW_MODEL_CALLS=0`, `HOST_INSTALL=NOT_RUN`, `ACTIVE_PROVIDER=NONE`, `CUTOVER_STATE=MIGRATION_NOT_CUTOVER`. **이 GitHub 문서 게시만으로 Windows Claude Code 또는 watcher가 실행되지는 않음.**

## 1. 최신 정본과 고정 대상

1. `collab/START_HERE.md`; `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` 최상단; `TRACKER.json`; `GPT_V0219_LIVE_CUTOVER_DISPOSITION_AND_FINAL_APPROVAL_BUNDLE_r0001_20261114.md`를 확인. 이번 원샷 승인 문서는 위 파일의 미승인 부분을 **이번 사용자 지시 범위에 한해서 해제**. 과거 전환/Classic PAT 승인 재질문 금지.
2. 정확한 **R2 리뷰 요청 ID**: `REQ-COWORK-V0219-R2-20261114`, 신규 요청 rev 1, 승인 모델 호출 **정확히 최대 1회**, 정책 `POLICY-STATIC-V1-LARGE`, 최대 비용 `USD 3.00`, 자동 재시도/재리뷰 없음.
3. 정확한 **후보 ZIP**: `skill-collab-watcher_v0_2_19_1114_DEV_NOT_FOR_DEPLOYMENT.zip`, 원본 바이트 기준 **239143 bytes**, `SHA-256=6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0`. PRIVATE `main`의 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0219-20261114/` 안 ZIP·`REVIEW_MANIFEST.md`·`diff_v0_2_17_to_v0_2_19.patch`를 사용.
4. GPT는 리뷰 매니페스트를 원격에서 확인했지만 **ZIP 원시 바이트 SHA/CRC는 직접 읽기 실패**함. Windows 호스트에서 원본 ZIP/원격 ZIP을 **각각 raw bytes로 재조회**, 크기·SHA·ZIP CRC·필수 파일·경로 이탈·비밀 스캔을 비교한 뒤 **전부 일치할 때만** 리뷰로 진행. 후보 ZIP이 다르면 중단하고 다른 SHA에 이번 유료 승인을 전용하지 말 것.
5. 실제 GitHub repo ID는 `1451933830`(GPT repository metadata 조회 확인). 검증 대상 v0.2.19에는 N1 원격 create-only dispatch reservation, N2 원격 repo ID 결합, Notifier는 별도 Windows 코드가 포함됨.
6. 이전 v0.2.17 독립 R2는 완료됐지만 v0.2.19에 승계되지 않음. 이전 `REQ-COWORK-V0217-R2-20261114`를 **절대 재호출하지 말 것**.

## 2. A — **새 독립 R2 리뷰 1회 실행 승인**

1. Windows의 기존 승인 서명 신뢰 루트/키와 정식 `REQUEST/APPROVAL_SIG/SOURCE_PIN/READY` 계약을 그대로 사용. **원본 ZIP·manifest·diff를 고정 commit A로 확인한 후**, 정식 승인 서명과 바인딩을 검증해 `READY`를 마지막 commit으로 게시. GitHub 게시나 GPT 판정 문서 자체는 실행 승인 서명을 대체하지 않음. **개인키·토큰·운영 신뢰파일은 게시하지 않는다.**
2. 개발 세션과 분리된 **독립 Claude Code 리뷰 세션**을 실행. reviewer의 입출력은 v0.2.17→v0.2.19 diff와 N1/N2·변경점의 호출 경계 중심으로 압축. `max_model_calls=1`, `max_cost_usd=3`, 사용 가능한 CLI budget stop 제어를 적용. 미지원 옵션은 우회하지 말고 부분 적용을 정직하게 기록.
3. 필수 독립 리뷰 논점: 원격 dispatch reservation 생성 원자성·중복 키/서명 결합·동시 워커/클레임·백업 복원 및 로컬 이력 분실·사용량 한도 후 `ALREADY_OURS` 재개·`FOREIGN` 분류·원격 읽기/쓰기 오류·N2 타 저장소 거부·비용 상한/재시작 후 재디스패치 방지·SHADOW 무쓰기. 리뷰어는 구현자가 **같은 개발 세션에서 스스로 시험한 결과를 독립 리뷰로 계산하지 않는다**.
4. 모델 호출은 신규 승인 요청 **1회까지만**. `REVIEW_UNCERTAIN`, CLI 사용량 제한, 네트워크/게시 실패/불명 상태에서는 **새 유료 호출 0**, 기존 완료 결과가 있으면 `publish-only`로 영수증·결과 remote readback. 비용이 $3 이상이거나 감시기가 통제하지 못하면 추가 실행하지 않음. 원격 리뷰 결과+receipt+usage receipt를 원본 바이트/정확 request id/revision/SHA로 검증하고 GitHub readback 완료.
5. `BLOCKING` 결함이 있거나 독립 리뷰 자체가 `NOT_RUN/PARTIAL/UNCERTAIN`이면 운영 설치·LIVE 전환 **STOP**. 허용 범위에서 격리 코드 수정·합성시험·새 후보를 준비할 수 있으나 **변경된 ZIP을 승인된 같은 1회 리뷰로 재실행 금지**; 비용 추가 발생 작업은 차단 기록.

## 3. B — **Windows 운영 변경 3종 명시 승인**, A PASS 이후 순차 적용

**이번 승인 범위에서만 운영 변경을 허용**한다. 대상·백업/복원·시험 증거를 기록하고, 요청 외 운영 DB·기존 Dropbox watcher·Dashboard·Bridge·기타 Task/기밀은 그대로 둔다.

1. **B1: 운영 Python 3.11.9에 `cryptography` 적용** — 실행 호스트 실제 interpreter를 확인, 현재 구성/의존성 백업 및 고정 버전/해시 검사 후 설치. Ed25519 정식 승인(정상/위조/만료/저장소 불일치/소스 핀 불일치)의 **실호스트** E2E와 watcher 회귀 확인. 실패하면 변경분 되돌리고 LIVE 금지.
2. **B2: Notifier provider별 DB·워터마크 개선** — Windows 기존 Notifier 설정/코드/단일 인스턴스 잠금/현재 `last_id`를 백업. 사전 비발송 후보(기존 보고서 `notifier_candidate`)의 기존 DB 알림 재발송 0·GitHub 새 DB 첫 이벤트 누락 0·반복/재시작 중복 0을 격리 재시험. 검증된 코드·설정만 운영에 적용. 프로그램을 재시작해야 하면 기존 단일 인스턴스 중지→적용→기동 순서로, rollback 가능성을 유지. **과거 메시지 일괄 발송/테스트 Telegram 발송 금지**. 실운영 신규 승인 이벤트에 대한 정상 알림만 전환 후 허용.
3. **B3: GitHub watcher 설치·Task 및 단일 LIVE 전환** — A PASS한 **동일 SHA의 확정 ZIP**만 배포 경로로 승격(파일명을 정규명으로 변경하더라도 **실제 ZIP 바이트 불변** 확인). 별도 안전한 GitHub 상태 폴더와 config/Task/신뢰 서명 검사, 기존 Classic PAT 사용. 기존 Dropbox watcher/DB·백업·Task 상태(Disabled)는 보존, 동시 활성 provider는 하나 이하. 신청된 GitHub Task 실행 시 실모드, 서명, repo ID·중복 키·비용 게이트를 점검. 다른 운영 Task/Bridge/Dashboard는 승인 범위 밖.

**운영 DB/사용자 데이터 이행은 승인되지 않았다.** 기존 Dropbox DB의 `pending_requests=1`(`L1-KNOWLEDGE-ROADMAP-DESIGN-20261109-001`), `COMPLETED=60`, `CONFLICT=1`은 원본/바이트 보존·격리 기록. 이 pending 건을 임의 재리뷰 또는 자동 신규 요청으로 이행하지 않는다. 별도 이관 없이 보존 상태와 조회 경로를 결과에 명시.

## 4. 공통 필수 게이트 및 최종 LIVE 활성화

- 사전 백업: 운영 DB main/WAL/SHM과 Notifier 설정/워터마크, Task/config, 설치 패키지·trust root의 **사용 가능한 복구 기준선**. Source 운영 DB를 읽기용 SQLite로 직접 열어 SHM을 변경하지 말고, 기존 승인된 바이트 복사→격리 사본 검사 방식 사용. 조정 과정에서 원본이 변하면 원인을 조사하고 LIVE 중단.
- PASS 필수: 고정 후보 바이트, 새 R2 독립 리뷰 및 영수증, N1/N2 포함 critical findings 0(또는 GPT 판정과 모순 없는 명시 수용), 실호스트 cryptography Ed25519/부정시험, Notifier 새 DB 첫 알림 누락 0·기존 중복 0, 기존 pending 무손실 보존, Task/복구·단일 provider·서명 검증. 감시기 설정의 추가 비용/서명/승인 조건 우회 금지.
- **최종 순서:** 기존 provider 비활성 상태 확인 → 신규 GitHub Task 단독 기동 → 두 번의 scan/watch 주기 및 재시작 후 모델/알림 중복 0·정상 API 경로·request 승인 정책·readback 확인 → 필요하면 publish-only/비유료 synthetic test로 확인. 신규 유료 reviewer 호출은 A의 승인된 1회 외 **0**.
- **실제 호스트가 전환됐고 상태를 검증했을 때에만** `ACTIVE_PROVIDER=GITHUB`, `CUTOVER=LIVE`, `HOST_APPLIED=PASS`로 기록. 코드·MD 게시만으로 LIVE 완료 금지.
- 실패 시 새 GitHub provider를 **즉시 정지**, 완료 이력·pending·영수증/워터마크·설치/rollback 파일을 보존, 사용자가 승인하지 않은 Dropbox 자동 재활성화는 금지. 상태를 `ACTIVE_PROVIDER=NONE`, `CUTOVER=BLOCKED/ROLLED_BACK`로 실제 실측에 맞게 보고.

## 5. 기록 및 종료 조건

- **Windows 결과 파일 (정확한 경로)**: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md`.
- 보고 표: `PAID_REVIEW_APPROVED`, `REVIEW_ID`, `REVIEW_TARGET_SHA`, `REVIEW_MODEL_CALLS`, `ACTUAL_COST_USD`, `INDEPENDENT_REVIEW`, `HOST_DEPENDENCY`, `NOTIFIER_WATERMARK_MIGRATION`, `PENDING_PRESERVED`, `ROLLBACK_REHEARSAL`, `GITHUB_WATCHER_TASK`, `ACTIVE_PROVIDER`, `CUTOVER`, `ACTUAL_MODEL_CALLS`, `TELEGRAM_DUPLICATES`, `FILES_SHA_READBACK`, blocked/errors. `PASS/FAIL/SKIP/NOT_RUN/BLOCKED`로 상태별 분리, 개발자 자체 시험과 독립 리뷰 구분.
- 결과, 리뷰/영수증, 증거 해시, 운영 변경 전후 상태를 PRIVATE `main`에 **PR 없이 직접 게시**하고 commit+remote readback. `CURRENT.md` **최상단**과 `TRACKER.json`을 최신 실측으로 갱신, 기존 이력 삭제 금지.
- 비밀·토큰·개인키·운영 DB/로그·회사 L1 코드·고객 자료는 PRIVATE에도 게시 금지. `/AI-CONTINUITY/` 불변. PUBLIC 스킬 ZIP 배포/정책 확대 금지.
- **핑퐁 최소화:** 위 명시 승인에 포함된 리뷰 1회 및 운영 변경 3종과 LIVE 활성화는 별도 재질문 없이 끝까지 수행. 독립 BLOCKING/미검증·한도/키·환경 장애가 발생하면 그 항목만 `BLOCKED`, 나머지 허용된 무비용 검증/문서화를 계속해 마지막에 한 번 보고.

## Windows Claude Code 실행 프롬프트 (전달용)

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_APPROVAL_AND_ONE_SHOT_r0001_20261115.md를 읽고 그대로 원샷 실행해줘. 사용자 A 승인=고정 SHA6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0 v0.2.19 독립 R2 리뷰 1회 최대 $3, B 승인=운영 Python cryptography 설치·Notifier provider별 watermark 적용·GitHub watcher 별도 상태/Task 설치 및 단일 LIVE 활성화. 기존 LIVE 승인 유지. 먼저 원격 ZIP raw SHA/크기/CRC 검사 후 유효 서명 REQUEST/READY로 정확히 1회 독립 리뷰, 영수증 확인. PASS일 때만 백업/복구 확인하며 B1→B2→B3를 실행하고 두 주기+재시작·중복/서명/상태·알림 검증. 실패/독립 BLOCKING/불확실 상태면 즉시 fail-closed 및 기존 운영 데이터 보존, 유료 재호출 금지. Classic PAT 지속 사용 확정. 결과 CLAUDE_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_RESULT_FOR_GPT_20261115.md, CURRENT.md, TRACKER.json을 PRIVATE main PR 없이 게시하고 원격 readback까지 확인해줘. 이미 받은 승인을 다시 묻지 마.
```
