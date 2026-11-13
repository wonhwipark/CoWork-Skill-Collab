# CoWork 단일 사용자 LOCAL_ONLY → GitHub LIVE 최소 핑퐁 통합 마스터
기준일: 2026-11-14 KST | r0001 | **DESIGN_AND_SINGLE_SHOT_DEVELOPMENT_HANDOFF / NOT_LIVE_APPROVED**
Repository: GitHub PRIVATE **`wonhwipark/CoWork-Skill-Collab`**
Branch: **`main`**
정확한 상대 경로: **`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_SINGLE_USER_LOCAL_ONLY_LIVE_FASTTRACK_MASTER_r0001_20261114.md`**
WORK_ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`

## 0. 사용자 요구와 위임 범위
- 운영자·승인자·결과 판정자는 **사용자 1명**. 모바일은 Windows Claude Code/Watcher PC를 원격 조작하는 UI일 뿐 독립 신뢰 경계나 승인자 키 보관 장치가 아님.
- 목표는 **필요 없는 별도 서명자 PC 요구·매번 신규 인계 문서·반복 자체시험을 제거**하고, 단일 Windows 작업 1회에서 승인 전 가능한 구현·실제 시험·수정 반복·로컬 ZIP 후보·결과 게시까지 끝내는 것.
- 사용자 확정 선택 `B=1,C=1,D=2,Token=2`: 4축 격리 검토, **회사 코드/ZIP 반출 금지 LOCAL_ONLY**, 기존 과권한 토큰 사용 금지. 2026-11-14 추가 의사: **단일 사용자 보안 계약 간소화 및 LIVE 목표까지 Claude Code 왕복 최소화**.
- 이 요청은 **설계 변경·격리 후보 구현·자체시험·비민감 PRIVATE 결과 게시까지 위임**. 운영키 발급, PAT 발급/설치, 실제 Windows 계정·ACL/예약 작업·운영 DB 이행, 비용 있는 리뷰, 리뷰 요청 READY, 외부 LLM에 코드 전송, 최종 GitHub LIVE 전환은 **추후 1회의 통합 명시 승인 없이는 실행하지 않는다**.
- 현재 `ACTIVE_PROVIDER=NONE`(구 Dropbox watcher/Bridge/updater Disabled, notifier 유지), `MIGRATION_NOT_CUTOVER`. 문서 게시가 Windows 실행/리뷰 호출을 자동으로 시작하지 않는다.

## 1. 사전 확인 — 기존 결과 재사용
`collab/START_HERE.md`, 해당 `CURRENT.md` **맨 위**, `TRACKER.json`, `GPT_LOCAL_ONLY_BLOCKERS_DELTA_DISPOSITION_r0001_20261114.md`, `CLAUDE_LOCAL_ONLY_BLOCKERS_DELTA_RESULT_FOR_GPT_20261114.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, `tools/local_only_contract_r0002.py`, `tools/reviewer_isolation_probe_r0001.py`를 확인.
- v0.2.12 watcher candidate: 원본 ZIP+실 해시+크기는 **로컬에서만** 기록/검증. 기존 제품 566 PASS/12 SKIP (venv) 및 518 PASS/15 SKIP×3 (운영 interpreter), ETW·token mock·installer synthetic, local-only r0002 26 PASS·10/10 변이, reviewer probe 12 PASS는 **Claude 자체 보고**로 재사용. 실제 독립 E 미실행. 실 사용자 운영 계정은 old Dropbox DB에 접근 가능하므로 4축 C 전체 PASS 아님.
- 이 Windows PC에는 로컬 LLM runner 관측 없음, reviewer egress probe `NOT_ISOLATED`. 조직에서 허용된 별도 로컬 모델 호스트/사람 reviewer 존재 미확인. 기존 GitHub CLI OAuth는 과권한. 반복 probing/진단에 시간을 쓰지 않는다.

## 2. 새로운 단일 사용자 보안 계약 SU-L1 (PROPOSED, 기존 운영 서명 체계 아직 대체 안 됨)
**승인/보호 대상은 단일 Windows PC 안의 정책과 상태**. 별도 승인자 하드웨어·Ed25519 운영키는 신규 `SU-L1 LOCAL_ONLY` 모드에서 **필수 설계 조건 후보에서 제외**한다. 기존 다중 사용자/유료 API/외부 ZIP 리뷰 모드는 서명 인증 체계를 해제하지 않고 별도 보존한다.
1. **명시적 온호스트 허용 정책**: 관리자만 변경 가능한 로컬 `review-policy`에서 원격 repo ID, branch, allowed work IDs, approved local artifact directory, reviewer command/runner identity, allowed execution principal, `LOCAL_ONLY` mode, `cost_cap_usd=0.00`, max 1 active job, max attempts 1, expiry, disable/kill switch, immutable policy epoch를 고정. 내용/ACL 실측 전 FAIL_CLOSED. GitHub READY·커밋·작성자·쓰기 권한 **단독으로 실행 승인 불가**. 원격은 요청 후보와 상태/영수증 통로에 한정.
2. **일회 사용자 승인 → 미리 합의된 범위 자동 실행**: 사용자가 Windows에서 허용 정책과 자동 실행 한도를 **한 번 명시적으로 승인/설치**하면 허용목록 요청만 자동 처리. 추가 업무·정책 개정·비용 상승·외부 모델 사용·민감 코드 전송은 재승인. 승인 모드는 승인된 로컬 정책 + 사용자 OS 권한으로 한정하며 **모바일 원격 접속을 별도 서명 장치로 계산하지 않음**. 개인키를 같은 PC에서 새로 만들어 서명하는 '독립 승인'이라는 표현 금지.
3. **실제 격리**: 승인 시 별도 비관리자 Windows 서비스 계정과 GitHub 전용 state 디렉터리, old Dropbox 운영 DB/main/WAL/SHM/secret 접근권 0을 적용. 서버의 관리자/사용자 전체 권한은 **동일 호스트 침해 위험**으로 인정. 승인 이전에는 SHADOW 샌드박스만, LIVE 계정·ACL/Task 수정 0.
4. **코드 반출 제어**: 코드·원본 ZIP·diff·시험 로그·실 SHA·크기·파일 이름·내부 경로를 외부 GitHub/Claude API에 제출 금지. GitHub에는 조직이 허용한 **opaque ID/솔트 커밋먼트/검증된 비식별 status·receipt**만; 다이제스트/크기/파일명 기게시 이력은 별도 분류. 내부 artifact ZIP과 salt는 내부 호스트에 보존.
5. **실행 주체 검증**: 조직 승인 **온프레미스 모델 런타임 또는 실제 사람 reviewer**가 필요. 개발자가 사용한 Claude Code 세션은 독립 리뷰 E로 인정 안 됨. 사람 reviewer만 존재하면 **무인 자동 실행과 독립 검토를 동일시하지 않음** — 별도 자동 runner가 없으면 `AUTO_REVIEW=BLOCKED_NO_LOCAL_AUTOMATED_RUNNER`. 외부 API Claude는 Windows에서 호출해도 LOCAL_ONLY 불충족. Claude Code의 백엔드 자체가 외부 서비스라면 **회사 제한 코드가 모델에 전송되는지 즉시 정책 확인**; 확인 전 기밀 코드 원문을 새로운 외부 모델 요청에 투입하지 않음.
6. **중복·오류·비용 차단**: 비밀 없는 `request_id`/opaque commitment/policy epoch로 확정한 logical idempotency key, 관리자 보호 DB의 **원자 예약** 및 프로세스 잠금, nonce·영수증 단일 수락·reboot 이후 보존. crash·publish 실패·토큰 만료·state loss는 `REVIEW_UNCERTAIN` 봉인, 모델 자동 재호출 0. 최대 1 리뷰 실행/요청, 비용 0, 모니터링 주기/Rate limit 제한, Telegram/알림 중복 방지.
7. **GitHub 최소 권한**: watcher read는 선택 저장소 1개 Contents Read-only fine-grained 토큰. 기존 과권한 `repo,workflow` OAuth 재사용 금지. 결과 write가 필요하면 **별도 제한된 쓰기 경로와 자격/Actions 범위를 설계**, 조회용 토큰으로 write를 시도하지 않는다. GitHub read/write, 내부 리뷰, 알림을 각자 인증·정책·FAIL_CLOSED로 격리.
8. **신뢰 한계 고지**: 단일 PC에 관리자, watcher, local policy가 함께 있어 **그 PC 관리자 계정이 침해되면 승인 분리로 방어하지 못함**. 사용자 단독·로컬 무과금 운영의 단순화 선택이며, 동일 장치 키를 외부 독립 서명으로 격상하거나 모든 보안 위험 제거로 표현 금지.
9. **향후 모드 확대는 별도 계약**: 외부 유료 모델/다중 사용자/다른 호스트 자동 실행은 기존 외부 pinned trust root + 서명 승인 체계가 다시 필요할 수 있음. SU-L1 무서명을 해당 모드에 일반화 금지.

## 3. Claude Code 통합 구현·시험 — 중간 질문 없이 허용범위 수행
Lane A **계약/상태 원장 hardening** (가장 우선):
- 이미 직접 검토된 `tools/local_only_contract_r0002.py`의 두 운영 위험을 **실제로 수정**: (a) 동일 nonce/영수증 2프로세스 동시 승인 race와 고정 `.tmp` 충돌 (b) 기존 state 파일 분실 후 빈 상태로 초기화하여 replay 수락.
- 기존 watcher의 검증된 SQLite/잠금·epoch·복구 제공자를 우선 재사용. 새 엔진/DB schema 중복 생성보다 호환성 우선. 변경이 필요하면 **새 파일 `local_only_contract_r0003`**로 보존하고 로컬 상태 마이그레이션·초기 genesis/rollback 절차 마련. 최초 한 번 bootstrap을 명시적 오프라인 승인·seed 상태 증명과 구분, 재기동에서 파일 없음=FAIL_CLOSED.
- 필수 delta 시험: 동일 nonce/같은 receipt **2개 이상의 병렬 프로세스 정확히 1 accept**, 재시작 후 replay 0, state delete/corrupt/rollback 이후 새 리뷰 호출 0, atomic replace/torn write/lock ownership/crash/recovery/uncertain 중복 0. 변경 제품 경로까지 연결된 증거가 없으면 `CONTRACT_INTEGRATION=NOT_RUN`으로 표시.
Lane B **single-user local policy engine**:
- 외부 승인용 Ed25519 운영키를 원샷 필수 게이트에서 제거한 `SU-L1` 프로토타입, 관리자 보호 policy read verification, repo ID pin, local work ID/artifact commitment binding, local OS user auth, zero cost, per-job cap, policy version, disable switch, failing closed on invalid/expired/missing admin-protected config. **원격 GitHub 문서만으로 자동 허용 안 됨**.
- ACL/OS 권한 변경은 실제 운영 PC에서 하지 말고 test-local sandbox 계정 또는 합성 mocking·정적 증거로 시험. 실제 host service principal은 별도 승인까지 `NOT_APPLIED`.
- 기존 signing/live flow는 손대지 않고 뒤 호환을 보존. SU-L1 모드를 별도 feature flag 기본 OFF로 구현. 금전·외부 모델/공개 게시 경로에 연결하지 않는다.
Lane C **로컬 reviewer 실제 경로**:
- 허가된 범위의 호스트 정보만 이용해 **모델 runtime/사람 reviewer candidate/접근권 여부를 1회** 식별. 현재 PC는 로컬 모델 미설치·외부 접속 가능 보고이므로 반복 스캔 금지. 가능한 **조직 승인 온프레미스 host 또는 리뷰어 제공이 확인될 때만** 네트워크 격리 도구 r0001 1회 + 소유/권한/네트워크 구성을 검증.
- 실제 reviewer 없으면 **`E=BLOCKED_LOCAL_REVIEWER`, `AUTO_REVIEW=NOT_RUN`**. 기존 개발 세션의 Claude 자체 검토로 대체하지 않는다. 사용자에게 유효한 리뷰어 종류/위치 정보를 한 번에 문의하는 조건만 결과서에 적고 나머지는 계속.
- 실제 내부 runner가 있으면 코드의 외부 전송 0을 조직 정책으로 확인, 리뷰 입력/오류 경로/출력 보안 검증, **진짜 독립 리뷰 한 번**은 실행 권한·비용/조직정책 승인 전까지 `NOT_RUN`.
Lane D **운영 분리/토큰/전환 준비**:
- GitHub LIVE 전용 최소권한 비관리자 서비스 계정과 신규 state dir/secret/DB/ACL 분리 계획·정확한 host apply/rollback 명령·사전/사후 검사표를 준비. 실제 계정 생성/Windows scheduler 변경/old DB I/O는 승인 전 금지.
- 신규 fine-grained PAT 사용자 직접 발급 UI 8항목과 안전 설치, `github_token_check_r0002`의 GET-only/NOT_PROVEN 조건, 결과 게시 write service의 별도 최소 범위 설계. 기존 broad OAuth 금지. 실제 token 생성/설치·자격 파일 읽기/쓰기 0.
- `LOCAL_ONLY` v2/v3 영수증을 공개 허용된 최소 필드로 GitHub에 게시하는 **simulation**, 원격 metadata readback, offline source SHA binding은 내부 원본 소유 측에서만. 기존 `ZIP+READY` 외부 업로드 계약은 D2에서 실행 금지.
- 다수 미정산 Dropbox 이전 작업의 승인된 보존 방식, single LIVE, restart/re-login, task/notification watermark, rollback/uncertain 정산 계획을 개발 문서와 격리시험으로 검증. 실제 migration/rollback LIVE 작동은 NOT_RUN.

## 4. 핑퐁 최소화 / 결과 판정 구조
- Windows Claude Code의 **이번 작업 1개**에서 A~D의 개발·결함 수정·관련 회귀시험·로컬 ZIP 후보·호환성 확인을 끝까지 반복. 구현 중 발견된 미해결 결함도 동일 작업 안에서 수정. 기존 500+ 제품·26개 계약·ETW·34 token mock을 목적 없이 매번 실행하지 않음; 변경 모듈 관련 regressions만.
- 외부 API/로컬 tool 호출에 코드 입력이 D2 정책을 위반할 수 있으면 그 코드 단계만 BLOCKED. 민감 정보는 로컬에만 저장, GitHub PRIVATE도 코드/실 raw SHA/경로/원본 로그 게시 금지. 허용된 비민감 summary·test count·opaque ID·정책 상태는 게시.
- 최종 Claude 결과 MD **하나만**: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_SINGLE_USER_LIVE_FASTTRACK_RESULT_FOR_GPT_20261114.md`; 필요 시 CURRENT.md 최상단, TRACKER.json 유효 enum과 함께 PRIVATE main에 **PR 없이** 게시·원격 bytes/hash readback.
- 결과 보고: (1) 현재 상태 (2) 구현 변경·diff 요약 (3) HOST_REAL/SYNTHETIC/SELF_TEST PASS/FAIL/SKIP/NOT_RUN (4) 제품 ZIP 로컬 검증(금지 원시 해시 비게시) (5) GitHub readback/commit (6) 독립 REVIEW 상태 (7) **실제 LIVE로 가기 위한 사용자 승인 묶음 딱 한 번**.
- GPT는 한 번에 통합 판정하고 Claude의 수정 가능 delta는 **한 묶음에만** 보낸다. `READY`, 모델 호출, LIVE 활성화가 진행된 것처럼 보고 금지.
- 승인 게이트는 코드개발과 별개. **사용자 확인 필요한 항목만**: (i) 실제 승인 온프레미스 reviewer 또는 사람·무인 runner 유무 (ii) 신규 read-only token 발급/설치 (iii) 비관리자 Windows 계정/ACL/작업 적용 (iv) SU-L1 policy activation과 운영 데이터 이행/rollback (v) 실제 독립 검토 및 최종 LIVE 전환. 개별 결재를 한 번의 패킷에서 설명하되, 서로 다른 행위의 명시 승인을 보존.
- LIVE의 수락 기준: 최소권한 인증/호스트 격리 HOST_REAL PASS, 신규 원장 race·loss·crash/restart 회귀 PASS, **실 독립 reviewer 및 source locality** PASS, local-only v2/v3 승인·검증/receipt 원격 readback, 재실행 0, notification dedup, 미정산 이력 보존, rollback/backup HOST_REAL, **ACTIVE_PROVIDER는 단일 1개**, 최종 사용자 LIVE 승인. 불충족 시 `DEVELOPMENT_READY_NOT_FOR_DEPLOYMENT`, `ACTIVE_PROVIDER=NONE`.

## 5. Windows Claude Code에게 전달하는 단일 실행 문구
```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main에서
collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_SINGLE_USER_LOCAL_ONLY_LIVE_FASTTRACK_MASTER_r0001_20261114.md
를 유일한 실행 인계로 읽고, 단일 사용자 SU-L1 LOCAL_ONLY(코드·ZIP 외부 전송 금지) 모드로 B 별도 서명자 PC 필수 조건을 설계에서 제거해줘. Lane A~D의 허용된 로컬 격리 구현·결함수정·delta 시험·후보 ZIP 보존까지 중간 질문 없이 원샷 진행하고, 기존 성공 시험은 재사용해줘. 특히 장부 2프로세스 중복 수락 및 state 분실 후 replay를 확실히 보완하고, 독립 로컬 리뷰어가 실제 없으면 그것만 BLOCKED로 격리해줘. 실키/PAT 발급·운영 계정/DB/Task 변경·외부 코드/모델 전송·유료 리뷰·READY·LIVE 전환은 실행하지 마. CLAUDE_SINGLE_USER_LIVE_FASTTRACK_RESULT_FOR_GPT_20261114.md 하나와 CURRENT.md/TRACKER.json을 PRIVATE main에 PR 없이 게시하고 원격 readback 후, 최종 LIVE 승인 필요사항만 한 번에 보고해줘.
```
