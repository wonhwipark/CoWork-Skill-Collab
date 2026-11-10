# CoWork Dropbox→GitHub — 1차 안전검증 통합 실행 인계 r0001
작성: 2026-11-11 KST | 상태: GPT_PREPARED / WINDOWS_HOST_NOT_RUN
repo: **PRIVATE `wonhwipark/CoWork-Skill-Collab` / branch `main`**
task: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
**현재 LIVE: Dropbox /SKILL-COLLAB/**. GitHub LIVE cutover, Dropbox stop, 운영 DB/예약작업/Telegram 수정은 본 작업에 포함하지 않는다.
이 문서와 시험 파일 게시는 REQUEST/READY, 유료 reviewer 승인 서명 또는 호스트 자동 실행 신호가 아니다.

## 0. 진입점 및 이번 '진행'의 범위
- 최신 상태 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`와 `collab/START_HERE.md`, 기존 GPT v0.2.4 판정 `GPT_V0_2_4_FINAL_GATE_DISPOSITION_r0001_20261111.md`, Claude 결과 `CLAUDE_FINAL_PRE_CUTOVER_GATE_RESULT_FOR_GPT_20261110.md`, `REVIEW_INPUT_MANIFEST_v0_2_4_FOR_GPT_20261110.md`, 검증 계약, B-7 설계를 모두 읽을 것.
- **사용자의 '진행'은 앞서 설명된 1차 전환 전 안전 검증의 진행 지시로 처리.** 중간 핑퐁 없이 허용된 설계/격리 개발/테스트/안전한 결과 게시까지 끝까지 수행. 그러나 운영 key/토큰 실제 배치, 운영 DB/WAL/SHM 변경, 외부 반출 및 실 유료 reviewer는 보안·비용·권한 게이트를 우회하는 의미로 해석하지 않는다.
- 소스 후보 `skill-collab-watcher_v0_2_4_1110.zip`, Claude report 146879 bytes, SHA-256 `854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20`; **Windows 로컬에만 존재하므로 GPT는 source를 받지 못했으며 직접 patch/전체 회귀 불가**. 로컬 후보 바이트를 검증하고 원본을 보존.
- `INDEPENDENT_REVIEW=NOT_RUN` 유지. Claude 개발 세션 자체 테스트는 독립 리뷰 영수증이 아니다.

## 1. GPT 직접 수행한 사전 검증
- 합성 Python 스크립트: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/tools/shadow_isolation_preflight_r0001.py`.
- 파일 **4541 bytes**, 실제 실행 SHA-256 `0550d4ddba6766ffa643f9fcf604a12271ebd5f7852e6b309046523525b7f811`; GitHub remote blob `e040804a79623449ff904198b98ae0f7c027bf84`, 로컬 git hash-object도 같은 값으로 확인.
- GPT 현 환경 CPython 3.13.5/SQLite 3.46.1; `python shadow_isolation_preflight_r0001.py` → **5 PASS / 0 FAIL** (별도 WAL/SHM 생성, disjoint path, nested/parent/symlink 경계 거부, 완전 분리된 shadow 상태 DB를 사용해 원본 main/WAL/SHM hash 모두 불변).
- **증거의 한계:** 실제 v0.2.4 watcher를 실행한 시험이 아닌 별도 synthetic topology 테스트. Windows junction/ACL/프로세스 핸들, Dropbox 원본, 운영 DB, 실제 GitHub GET/로그인/Telegram/모델 호출 등은 이 GPT 시험에 포함되지 않음. `5 PASS`를 Windows 410 PASS에 합산 금지.

## 2. S-1 SHM 변화 해결 — 새 기본 설계 선택
배경: Claude v0.2.4의 사본 SHADOW는 운영 DB 사본 main·WAL 동일, SHM **변경 관측**. SQLite `mode=ro`는 SQLite WAL `-shm` read-mark/공유 메모리 상호작용을 금지하지 않는다. 별도 실 호스트 게이트로 승격 금지.

**우선 구현안: 운영 DB를 SHADOW watcher가 아예 열지 않는 완전 분리 상태저장 방식.**
1. 새 SHADOW는 GitHub **읽기 전용 transport**와 전용 `shadow_state_dir`만 사용. 운영 `state_dir`, `jobs DB`, 운영 `-wal/-shm`, 운영 process lock을 열거나 SQLite backup을 생성하는 코드를 SHADOW startup 및 scan path에서 완전히 분리한다. SHADOW 상태/임시 파일/락/로그/커서는 모두 별도 전용 폴더. 운영의 F1 pending 및 job complete 이력은 SHADOW에서 조회/재평가/재실행 금지.
2. 런타임 경로 가드: canonical path, Windows reparse point/junction/symlink 및 file identity 검사, cross-volume/UNC alias 검사, live root와 shadow root containment/overlap 차단. 경계 확인 불능은 **fail-closed SHADOW 시작 0**. 단순 문자열 prefix만으로 검증 불가.
3. SHADOW에는 모델/approval dispatch **0**, GitHub write 0, Dropbox write 0, Telegram 0, 운영 DB write/read 0, 단일 LIVE lease write 0. git token은 별도 contents-read-only 최소 권한. `provider_mode=SHADOW`라는 환경 변수만으로 보호됨을 주장하지 말고 **실제 호출 경로**를 검토.
4. 과거 요청 및 롤백 실데이터가 필요하다면 운영 라이브 DB를 직접 열지 말고, **별도 승인된 일관된 SQLite online backup 또는 검증된 운영 snapshot의 격리 복사본**을 사용. 이 snapshot 생성 과정은 SHADOW와 **분리된 운영 호스트 작업**이며, 원본 read-only 연결조차 SHM/lock에 영향이 있을 수 있으므로 자체 운영 영향 검사/승인 전 자동 실행 금지. WAL 파일을 단순 OS 파일 복사로 합성해 일관된 백업이라고 주장하지 말 것. `immutable=1`로 활성 DB가 안 변하는 것처럼 취급 금지.
5. Windows 실제 검증 기준: 기존 Dropbox LIVE 그대로, 세 사이클 이상 GitHub GET만, model_runner/Telegram/remote write 0, 운영 DB 3종 main/WAL/SHM 파일에 신규 SHADOW 프로세스가 접근/쓰기하지 않는 것(실행 경로 및 OS 파일 핸들/파일 I/O 추적), 운영 스케줄러/DB schema/rows/lease/lock 변화 없음(기존 LIVE의 정상 움직임은 별도 구분). 단순 전후 hash만으로 운영 writer의 변경분과 SHADOW 기여분을 혼동하지 말 것.
6. Windows 설치/토큰 발급 권한 및 host shadow 기동이 불가하면 해당 항목만 `NOT_RUN`. 허용된 격리 회귀시험·코드 변경·ZIP 생성·결과 게시 계속.
7. `shadow_state_dir`에 전용 메타데이터가 남더라도 모델 0이면 안전하다고 단정 금지: 실제 PRIVATE repo access가 read-only인지, source commit/ref 고정/서명/READY가 실제 reviewer에게 도달하지 않는지 확인.

## 3. B-7 운영 신뢰 루트 안전 검증
- 운영 private signer key는 **승인자 장치에만** 저장, watcher는 고정 public trust root만. watcher와 signer가 서로 분리된 ACL/권한/운영 변경 경계를 가짐을 증명.
- 공개 루트와 `trust_root_sha256` 핀이 같은 사용자/같은 쓰기 ACL로 동시에 바뀔 수 있다면 핀만으로 보안 승인 경계를 보장하지 못한다. pin/서명자/루트 승인 주체를 분리한 권한 매트릭스와 rollback/rotation/revocation/version ratchet/clock rollback/frozen 테스트를 보완한다.
- 테스트 key는 격리 공간에서 생성·삭제 가능. **운영 signer private key, 운영 PAT, 운영 trust root의 실제 생성·설치**는 별도 운영 보안 절차/권한으로 확인한다. 개인키·자격증명은 GitHub PRIVATE에도 업로드 금지.
- Ed25519 시험 S01–S10과 운용 signer의 진짜 승인자 권한은 별도 상태. sign tool 미구현 시 유효 READY/정식 리뷰 실행은 **BLOCKED**.

## 4. ZIP·독립 리뷰 게이트
- 출처가 분명한 v0.2.4 ZIP을 실제로 읽어 보고된 bytes/SHA, ZIP CRC, 위험 경로, 동적 시험, dependency hashes, 민감정보를 재검증. 모든 파일의 반출 가능성이 확인되지 않으면 로컬에 보존하고 PRIVATE에도 올리지 않는다.
- 보안상 승인된 파일만 PRIVATE `collab/packages/` 새 이름으로, 기존 파일 덮어쓰기 없이 올리고 원격 raw byte SHA readback. 원본 업로드가 차단되면 `NOT_POSTED / BLOCKED_EXPORT_CLASSIFICATION`.
- 정식 독립 리뷰는 **구현자 자기평가와 분리된 별도의 독립 실행 및 영수증** 필요. `REQUEST/READY`는 운영 승인권자의 실제 서명과 고정 정책/커밋/ZIP SHA, 1회 호출 예산이 확인된 이후에만 새로 작성. 문서/zip 업로드만으로 리뷰 호출 금지.
- 현재 비용 단계: `STATIC $1`, `LARGE $3`, `XLARGE $6` **상한**. 해당 ZIP과 리뷰 범위가 상한을 넘길 것으로 예상되면 `NOT_RUN/COST_APPROVAL_REQUIRED`. 자동 증액 및 같은 reviewer 재호출 금지. 사용자 '진행'만으로 예산 상한을 올리거나 유료 호출 조건 충족을 가정하지 않는다.
- 어떤 조건이 막혀도 가능한 코드는 격리사본에서 수정·재시험하고, 필요 시 v0.2.5 ZIP을 **신규 발행**하되 v0.2.4/운영 v0.1.5 보존. 실제 수정 없으면 ZIP 버전 임의 증가 금지.
- 리뷰 원문 공개는 금지. 허용된 비민감 결과·diff 목록·실제 통과 시험 수·미수행을 요약해서 PRIVATE 결과 MD로 게시.

## 5. Windows 원샷 종료조건, 리포트 형식
**중간 승인을 요구해 작업을 쪼개지 말 것**: S-1 분석/격리 구현/재시험/패키지/키 정책·접근권한 준비/SHADOW 가능 범위 시험/리뷰 조건점검/최종 결과 게시까지 한 작업.
- 새 결과 위치: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_STAGE1_HOST_SECURITY_RESULT_FOR_GPT_20261111.md`.
- 보고서에 필수: 자체 개발 `SELF_TEST_REPORTED`, DB 3종 접근·쓰기 분석, 실제 Process/file I/O 실측 여부, 기존 LIVE 영향, B-7 루트/키와 signer 준비 수준, ZIP 실제 SHA/크기, 테스트 번호·PASS/FAIL/SKIP/NOT_RUN, 실제 requester/READY/독립 리뷰 및 영수증 여부, GitHub commit·readback 결과, 권한·인증·비용 차단을 한곳에 요약.
- 이 결과 MD는 PRIVATE main에 **PR 없이 직접 게시**, `CURRENT.md` 최신 단락 1개 갱신 후 원격 SHA/readback. 실패 시 로컬에 결과 보존, NOT_POSTED.
- 호스트 작업이 불가한 항목을 실행했다고 쓰지 않는다. 독립 리뷰 사용 가능하더라도 실제 sign/cost/호스트 승인 조건 실패 시 모델 호출 0.
- **2차 단계**(운영 DB 실제 이행, F1 hold/재정산, Dropbox 종료, GitHub LIVE 전환/실제 롤백)는 별도 사용자 명시 승인 없이는 절대 실행하지 않음.

## 6. 사용자의 다음 단일 실행 지시
Windows Claude Code에 아래 정확한 문서 한 개를 지정하도록 한다. GitHub 문서 게시 자체로 Windows Claude Code가 실행되지 않는다.
`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_STAGE1_SHADOW_TRUST_REVIEW_ONE_SHOT_r0001_20261111.md`
