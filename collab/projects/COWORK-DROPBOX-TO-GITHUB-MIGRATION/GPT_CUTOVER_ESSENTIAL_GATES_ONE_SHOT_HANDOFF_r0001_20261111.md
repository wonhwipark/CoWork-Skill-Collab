# CoWork GitHub LIVE 전환 필수 게이트 — Windows 단일 원샷 인계 r0001

- 기준일: 2026-11-11 KST
- Repository: **GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`**
- Branch: **`main`**
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- 상태: **`HANDOFF_PREPARED_NOT_EXECUTED / MIGRATION_NOT_CUTOVER`**
- 작업 목적: **GitHub LIVE 전환에 실제 필요한 차단 조건만 해결·검증하고, 별도 사용자 승인 직전의 판정 자료를 하나의 결과 MD로 마련한다.**
- 절대 구별: **인계 게시 = 실행 신호 아님; 개발자 자체 시험 ≠ 독립 리뷰; SHADOW ≠ LIVE; 사용자의 '원샷 준비/진행' ≠ 운영 변경·유료 리뷰·공개 게시·LIVE 승인**.

## 1. 진입점·실제 정본·버전 선택

1. 시작할 때 `collab/START_HERE.md`, **이 작업의 `CURRENT.md` 전체 중 최신 판정**, `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, `GPT_V0_2_4_FINAL_GATE_DISPOSITION_r0001_20261111.md`, `GPT_NO_LOGON_START_COMPAT_DISPOSITION_r0001_20261111.md`를 재조회. 기존 `GPT_STAGE1_SHADOW_TRUST_REVIEW_ONE_SHOT_r0001_20261111.md`의 **S-1/S-2 검사 요구를 상속**한다.
2. **기준 운영본:** Windows에 설치된 Dropbox watcher v0.1.5 (불변). **기준 개발 후보:** Windows 로컬 `skill-collab-watcher_v0_2_5_1110.zip` 보고값 **155,288 bytes**, SHA256 `40a1a944ec55d7414051374a67e264fd4fe03dadfcdead449ff37bac86dd93e6`, 448 PASS/0 FAIL/12 SKIP은 Claude 개발 자체 보고. **v0.2.4**는 이전 SHADOW/신뢰 루트 기준 후보(146,879 bytes; SHA256 `854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20`). 서로 다른 ZIP을 같은 버전으로 취급하지 않는다.
3. 실제 Windows ZIP의 바이트·파일 크기·ZIP 구조·파일별 SHA를 로컬에서 다시 확인하고, 없거나 다르면 `BLOCKED_SOURCE`로 표시. **기존 후보와 운영본 덮어쓰기 금지**. 코드 변경이 꼭 필요하면 격리 복사본에서 새 버전으로 패키징; 재시험과 SHA/크기 기록.
4. 실제 GitHub HEAD/다른 세션이 새로 게시한 결과를 우선한다. 이전 인계가 이미 수행됐다면 **반복 시험·새 리뷰 호출·중복 설치 금지**; 변경분만 수행.

## 2. 이번 원샷의 필수 수행 범위 (승인 없이 허용되는 부분)

**G0. 안전한 사전 확인**
- 기존 감시기·작업·Notifier·Bridge/Dashboard·설정·운영 DB main/WAL/SHM·기존 Dropbox 요청/영수증은 **실제 수정·재시작·중지 금지**. 스케줄러 정보·파일 메타데이터·호스트 권한을 읽기 전용으로 확인하고 민감값/사용자 이름/로컬 절대 경로를 PRIVATE에 올리지 않는다.
- SQLite `mode=ro`라도 WAL `-shm`에 영향이 있을 수 있으므로 **SHADOW 검증용 프로세스는 운영 DB 파일 세 개를 열지 않도록** 설계. 파일 해시가 우연히 같다고 운영 DB 접근 0이라고 주장하지 않는다.
- 대기 중인 F1=WAIT_INPUT(READY 없는 정상 요청 1건)을 **Dropbox에 보존**. F2 완료 및 G1–G3 REJECTED는 임의 재큐잉/삭제 금지. 상태 확인이 운영 DB를 열어야만 가능하면 이 항목은 `NOT_RUN` 유지.

**G1. 코드·안전 게이트 보완**
- v0.2.5의 GitHub adapter 승인/서명 검증, 처리키 idempotency, 정책·비용 상한, `REVIEW_UNCERTAIN` 봉인, 재게시시 모델 재호출 방지, Dropbox pending 분리, Telegram 중복 차단, 롤백·동시 LIVE 방지를 diff 중심으로 검토.
- 기존 v0.2.4 SHADOW 이슈 S-1을 **운영 DB를 전혀 열지 않는 별도 shadow_state_dir/DB/lock/log/cursor** 방식으로 수정하고 합성·격리 시험. Windows junction/reparse point, UNC alias, parent/child path, file identity/ACL 가드를 확인. fail-closed; 안전한 분리 입증 불가시 `BLOCKED_SHADOW`.
- `SHADOW`는 GitHub GET만, 모델 0, 원격 write 0, Telegram 0, Dropbox write 0, 운영 DB/lease touch 0. **호스트에 실제 SHADOW를 설치·기동하는 작업은 별도 승인 전 NOT_RUN**.
- B-7 서명자/고정 trust root/핀의 권한 독립, 버전 ratchet, revocation, clock rollback 및 signer 도구 준비 수준을 **시험 키·격리 사본**에서 점검. 운영 승인키/신뢰키/토큰 **생성·배치 금지**. 공개키 핀과 루트 변경 권한이 동일하면 보안 게이트 `BLOCKED_TRUST`.

**G2. 회귀시험과 패키징**
- 변경 파일·이미 아는 결함 중심으로 테스트 먼저, 기존 전체 suite, T01–T38/S01–S10을 실제 가능한 범위에서 재실행. `PASS/FAIL/SKIP/NOT_RUN`, `SYNTHETIC/REAL_API_READ_ONLY/OPERATING_HOST`을 구분. 장비·인증·예산 차단 항목은 `BLOCKED` 처리하고 다른 허용 시험은 계속.
- 후보 ZIP은 **새 버전의 새 경로**, ZIP CRC, zip-slip, symlink, nesting, 비밀·반출 금지 파일, dependency lock, raw SHA256/bytes, manifest 검증. 실패 시 `development_not_for_deployment` 유지; 이전 버전 덮어쓰기·PUBLIC 배포 금지.
- 운영 데이터·소스·토큰의 외부 반출 적합성을 파일별로 판정. **반출 허용이 확인되지 않은 실제 ZIP은 PRIVATE에도 업로드 금지**. 로컬에서 검증한 해시와 비민감 요약만 보고.

**G3. 정식 독립 리뷰 준비**
- `REVIEW_INPUT_MANIFEST_v0_2_5_FOR_GPT_20261111.md`에 변경분/S-1/B-7 핵심 질문·회귀 명령·known defects·모델 호출 0 경계 추가 필요 여부 평가.
- 리뷰 요청용 `REQUEST/READY`가 아니라 **미실행 REVIEW_PREP**만 준비. GitHub watcher 서명/고정 커밋/실제 source ZIP·비용 승인이 없다면 `INDEPENDENT_REVIEW=NOT_RUN` 유지. 자기 구현 시험과 독립 리뷰가 같은 세션이라면 독립으로 간주 금지.
- 정식 유료 리뷰 1회, REQUEST/READY 발행, 승인자 서명키 생성, 신규 토큰 생성, ZIP PRIVATE 게시, 원격 SHADOW 운용은 **각각 명시 승인 후** 실행. 기존 모델 정책 기본 상한 STATIC $1, LARGE $3, XLARGE $6; 자동 예산 증액 및 같은 리뷰 재호출 금지.

**G4. 전환 리허설 자료와 최종 승인 게이트**
- 운영 DB 스키마/백업/복원/복귀, F1 대기·커서·provider 구분·영수증 정산, notifier 워터마크, 단일 LIVE, 실패시 Dropbox rollback을 **격리 복사본에서 재시험**; 실제 운영 DB 이행·기존 watcher 정지·GitHub LIVE 활성화는 NOT_RUN.
- 실 운영 LIVE 전환을 승인해도 되는 판정 조건을 명시: ① 호스트 SHADOW read-only 검증 ② 신뢰 루트·승인 서명·최소 권한 실제 검증 ③ 비민감 소스 반출 분류/원격 바이트 정합성 ④ 정식 별도 독립 리뷰와 영수증 ⑤ 미정산 F1 보존/정산 ⑥ 운영 DB 백업·복원·rollback 시나리오 ⑦ LIVE 단일 provider 및 알림 중복 0 ⑧ 사용자 최종 명시 승인.
- **재부팅 후 로그온 없는 시작(S4U/Password), 일일 상한 설정, Windows 자동 로그인, Notifier 신기능 연결은 LIVE 전환 필수 게이트가 아님.** 별도 개선 트랙으로 두고 작업 스케줄러/운영 notifier 변경 금지.

## 3. 승인 없이는 실행하지 않는 작업 (차단 후 계속)
- GitHub PRIVATE에 실제 ZIP 업로드, 내부 자료 반출, PUBLIC ZIP 게시.
- 운영 신뢰키·실서명 승인자 도구 배치, GitHub PAT/보안 키 생성, 유료 Claude 독립 리뷰, 실행 가능한 REQUEST/READY 게시.
- 실제 Windows 운영 호스트 SHADOW 설치·가동, 새 스케줄러 작업/자동 로그인, 운영 watcher 교체·중지·재시작, DB live/backup/scheme 전환 및 로그·알림 설정 변경.
- GitHub LIVE 전환, Dropbox LIVE 중지/폐기, 실제 전환·롤백 시험으로 운영계 변경.
- 명확한 허가 범위에 속하는 개발 사본 수정·시험·문서 게시를 끝낸 뒤 **승인 항목은 한 번에 최종 사용자 결정 묶음**으로 보고. 승인 차단 하나 때문에 허용된 나머지 작업을 중단하지 말 것.

## 4. 종료 시 결과 MD 1개 및 원격 검증
- 새 결과 파일: **`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_CUTOVER_ESSENTIAL_GATES_RESULT_FOR_GPT_20261111.md`**.
- 실행자가 Windows Claude Code 개발자이면 `DEVELOPMENT=SELF_TEST_REPORTED`, `INDEPENDENT_REVIEW=NOT_RUN` 명시. 정식 독립 리뷰가 **별도의 유효 승인** 아래 수행되어 실제 receipt가 생긴 경우에만 상태 변경.
- 표로 `G0–G4` 각각의 코드 변경/시험증거/실패 원인/완료/차단/승인 필요, 최종 ZIP filename/bytes/SHA/개별 증거, SHADOW 동작/DB main-WAL-SHM 접근 0 증거, F1 HOLD 처리 여부, 모델 호출수·비용·원격 게시/재조회 결과, 필요한 승인 묶음을 기록.
- 비밀/사내 반출자료 제거 후 **PRIVATE `main`에 PR 없이 직접 게시 → commit SHA + 원격 본문/바이트 readback 검증**. 결과 게시 실패로 모델 리뷰를 재호출하지 않는다. 공개 금지자료를 제거할 수 없다면 `NOT_POSTED/REDACTION_REQUIRED` 보고하고 로컬 보관.
- `CURRENT.md`에는 가장 위에 **하나의 최신 실행 상태 단락**만 보완하고 과거 완료/미완료 기록을 보존. 다른 세션의 최신 변경을 덮어쓰지 말 것.
- 목표 결과 상태: `PRE_CUTOVER_READINESS=PASS|PARTIAL|BLOCKED`, `INDEPENDENT_REVIEW=NOT_RUN|PENDING|PASS(with receipt)`, `HOST_SHADOW=NOT_RUN|PARTIAL|PASS`, `DB_LIVE_MIGRATION=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`, `PRODUCTION_CHANGED=false`.
- 마지막 한 동작은 **필요 승인 1회분을 종합 보고**. Windows에서 실제 권한/비밀·운영변경이 필요해 멈춘 항목만 승인 후 새 단일 실행을 하도록 인계.

## 5. 사용자 전달용 실행 프롬프트 (Windows Claude Code)
`GitHub PRIVATE wonhwipark/CoWork-Skill-Collab 의 main 브랜치 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_CUTOVER_ESSENTIAL_GATES_ONE_SHOT_HANDOFF_r0001_20261111.md 를 먼저 읽어. 기존 중복 인계나 수행된 결과는 최신 CURRENT.md로 확인한 후, G0–G4의 승인 없이 가능한 안전 수정·격리시험·회귀·ZIP 검증/후보 생성·결과 MD PRIVATE main 직접 게시·원격 readback까지 원샷으로 진행해. 운영 watcher/DB/예약작업/알림/키/토큰·모델호출·REQUEST/READY·실 호스트 SHADOW·PUBLIC·LIVE는 변경하지 마. 차단 항목은 NOT_RUN으로 모아서 보고하고, 개발자 자기시험을 독립 리뷰로 표시하지 마.`
