# Windows Claude Code 원샷 — CoWork 사전 위임 자동 서명/READY 최소 구현·후보 검증

- 작성: 2026-11-15 KST · r0001
- **정확한 저장소/브랜치:** GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- **정확한 상대 경로:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md`
- **대상 Work ID:** `COWORK-AUTO-APPROVAL-20261115-001` (기존 GitHub LIVE 이관 Work와 별도)
- **설계 정본:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md`
- **GPT 작성 검증 참고:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/prototype/auto_policy.py`, `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/prototype/test_auto_policy.py` — Python 격리 25/25 PASS, remote/local Git blob 일치. **운영 코드로 무검증 복사하지 말 것.**
- 목적: **사용자 → GPT REQUEST → GitHub PRIVATE → Windows 기존 signer의 위임 범위 내 자동 승인·서명·READY 마지막 게시 → 기존 v0.2.20 LIVE watcher 리뷰 1회 → 결과/영수증 → GPT 판정**.
- 기본 방식: 정상 요청마다 Telegram 버튼 없음, Windows Claude Code 수동 서명 없음. 처음 사용자 위임 정책 등록·최종 운영 후보 적용은 별도 1회 승인 게이트.
- 이 인계서는 **개발/시험/후보 준비 실행 지시**로 취급하고, 기존 운영 프로그램의 설치·Task·DB·키/권한·자동 서명 활성화·유료 모델 리뷰 호출/READY 게시 승인이 아님. 현재 `AUTO_SIGNING=OFF` 유지.

## A. 시작 1회 정본 확인 (진단 후 즉시 계속)

1. PRIVATE `collab/START_HERE.md`, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` 최신 첫 섹션, 새 Work 설계/프로토타입, 기존 운영 v0.2.20 서명/Validator/Orchestrator/N1 중복·Signer CLI·설정·Task/Notifier·README 원본을 확인. 과거 r0001 Telegram 버튼 설계는 **이번 기본안이 아님**. 현재 GitHub provider는 이미 LIVE.
2. Windows 실제 설치 소스/후보 ZIP·서명 호출 API, 승인 개인키 ACL/현재 Task 실행 계정 접근·기존 SQLite 원장 atomic claim 및 비용 장부 경계를 **읽기 전용** 확인. `APPROVAL_SIG` 서명 payload가 `ready_sha256`을 포함하므로 READY 바이트를 먼저 구성해야 함. SOURCE_PIN/기존 승인 서명/신뢰 루트/매 호출 repo ID GET 재검증 필수.
3. 변경 필요 파일/함수·최소 diff/호환성/비밀·제약을 문서화. 부족한 원본이 있어도 접근 가능한 부분의 격리 구현·시험부터 계속. READ_ONLY라고 부르는 DB 연결도 main/WAL/SHM 쓰기를 유발하지 않게 **복사본에서** 확인.
4. 기존 구버전/운영 설치/Windows Tasks/Dropbox DB 및 pending 1건/Notifier 설정 보존. 사용자가 다시 승인해야 하는 것은 실제 운영 설치·auto signer 활성화와 미래 자동 위임 scope뿐; 이번 개발 중간 단계는 재질문하지 말 것.

## B. 최소 구현 — 격리 복사본에서 원샷 수행

1. 가능한 경우 기존 **동일 GitHub watcher scan loop**에 `REQUEST 존재, READY 없음` pre-READY 탐색을 추가한다. 실행 중인 유료 모델과 무관한 계약만 검사. 새 watcher Task·두 번째 GitHub provider·Telegram callback listener·별도 서비스는 기본 추가 금지.
2. 로컬 보호 `AUTO_DELEGATION_V1` 정책 reader 및 scope 검사 구현. **enabled=false를 기본으로 유지**; GitHub REQUEST/승인 MD/임의 CI 쓰기만으로 자동 승인 정책 활성화 불가. 사용자 위임 scope·예산·유효기간 및 로컬 key/trust boundary가 실제로 검증 가능한지 확인.
3. 기존 signed approval 구현 재사용: Request·source pin·ZIP/원시 SHA/commit A/repo ID/정책/cost를 재조회; 새/과거 pending/중복/REVIEW_UNCERTAIN을 구분; **원자 예약 후 READY 문구를 먼저 결정**, signer에 ready_sha256와 ZIP/REQUEST pin 포함하여 실제 서명. `APPROVAL_SIG.json` create-only·remote readback 후 `READY.md` create-only **마지막 게시**. 실패한 repo HEAD race를 무한 재시도하지 말고 충돌/불확실 시 STOP.
4. 기존 v0.2.20 Watcher의 `READY` 최종 독립 검증과 기존 N1 reservation, 모델 1회, RESULT/RECEIPT/USAGE·Notifier 동작은 변경 최소. 승인 정책이 거부되면 **서명·READY·Claude 모델 호출 0**.
5. Cost 보호는 기존 Watcher `POLICY-STATIC-V1` 최대 $1·기존 운영 일일 2회/$3보다 **완화하지 않는 정책**. 월 $10 및 30일 만료는 사용자 미승인 제안값이며 후보에서 로컬 정책 disabled 상태. 실제 owner 승인 없는 LIVE 활성화 금지.
6. pre-READY 로컬 원장·비용 예약의 crash recovery 시 사용자 데이터/원본 이력/기존 dispatch 키를 변경하지 말 것. 정확한 원격 결과를 확인한 **publish-only 정산** 외 새로운 서명/READY/모델 호출 자동 재시도 금지.
7. 기존 출처가 명시된 CODE/ZIP과 허용된 비민감 설계 자료만 사용. 업무 제한 코드·토큰·개인키·운영 DB 원본/로그를 PRIVATE/PUBLIC로 업로드 금지.

## C. 필요한 시험 — 개발 한 회차에 최대한 해결

| 범주 | 필수 실측 |
|---|---|
| 정책 오프라인 | GPT 제공 25건 직접 재실행, 프로젝트/skill/branch/repo ID/policy/attempt/시간·비용/중복·변조 |
| 실제 계약 | 공식 v0.2.20 Validator + signer/approval verifier, prepare READY bytes → signed `ready_sha256` 일치, SOURCE_PIN·commit A 고정 |
| 격리 통합 | fake GitHub transport/fake signer/이벤트로 요청 탐색 → atomic claim → APPROVAL → READY LAST 순서·ID별 1회 보장 |
| 중복·병렬 | 두 scan/thread/process, 두 REQUEST, 기존 v0.2.20 R1 완료 요청·Work→Knowledge 11/15 READY 미게시 요청은 **소급 자동 실행 0** |
| 장애·복구 | crash-before-claim, claim 후·PUT 이전, SIG 후 READY 전, READY 후 watcher 전, N1 dispatch 후 영수증 게시 실패, GitHub 409/422/timeout, local DB restore·WAL 처리 |
| 보안·비용 | 사용자 위임 disabled/expired, GitHub 오염 문구, ZIP/REQUEST/commit/repo spoof, ACL/서명 신뢰루트 실패, daily 2회/$3·월 제안 $10 경계 |
| LIVE SHADOW | **기존 운영 Task 그대로**, 격리 temp repo/파일/DB 또는 완전 fake transport, 실제 remote write·Telegram 발송·실 signer·paid Claude model 모두 0 |
| 호환성 | 운영 Windows Python 3.11.9 및 기존 전체 v0.2.20 회귀, 새 테스트; 필수 파일·ZIP CRC/zip-slip/symlink/secrets; 롤백 준비·복원 격리 리허설 |

오류는 **해당 결함 수정→동일 회차 재시험**으로 묶어 처리. 결함을 발견할 때마다 GPT에게 프롬프트·재승인을 요구하지 말 것. 실제 호스트에만 있는 원본은 격리 사본에서 구현, 자가시험 결과는 `SELF_TEST_REPORTED`; 자체 리뷰를 `INDEPENDENT_REVIEW=PASS`로 표시 금지. Claude가 구현한 세션과 분리된 독립 리뷰는 유효 REQUEST/READY·영수증·비용 승인 후 별도 실행; 본 승인으로 임의 모델 리뷰 호출 불가.

## D. 결과·후보 패키지·readback (PR 없이 PRIVATE main)

1. 실제 변경 소스·diff·시험 증거·설치 영향·기존 기능 회귀·운영 서명 ACL 확인 여부·rollback/복구 시험을 요약해, 허용된 코드만 PRIVATE에 신규 `candidates/auto-approval/` 또는 프로젝트 artifacts 폴더에 게시. 현 운영 ZIP을 덮어쓰지 말 것. 반출 허용이 검증되지 않는 파일은 **Windows 로컬 보존·NOT_POSTED**.
2. 신규 후보 명명 규칙 `skill-collab-watcher_v0_2_21_1115.zip`은 예시일 뿐, 실제 버전/날짜/기존 파일 이름 충돌 점검 후 결정. **후보 배포 상태는 `development_not_for_deployment`**, 실제 ZIP raw SHA-256/크기/CRC/파일명·경로 이탈·민감 포함 검사. 신규 버전을 만들지 못하면 정확히 NOT_RUN.
3. 결과 문서: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_AUTO_APPROVAL_ONE_SHOT_RESULT_FOR_GPT_20261115.md`. 반드시: **현재 상태 → 변경 파일/diff → 실제 tests PASS/FAIL/SKIP/NOT_RUN → Windows ACL/Signer SHADOW/rollback 결과 → 미완료/승인 필요 → 후보 ZIP 크기/SHA/위치 → 다음 한 동작** 순서. 테스트 명령/원시 출력 요약과 미검증을 구분.
4. 본 Work `CURRENT.md`·`TRACKER.json`을 사용해 이번 자동 승인 개발의 최신 상태를 기록한다. 이전 이관 Work의 `COMPLETE/GITHUB LIVE` 판정 자체는 뒤집지 말 것. README·dashboard를 수정해야 한다면 실측 결함과 변경 이유를 함께 증명; 권한 없는 PUBLIC 게시 금지.
5. 최종 파일·commit·raw bytes SHA-256·ZIP CRC를 **GitHub에서 다시 읽어** 검증. readback 실패는 `NOT_POSTED/UNVERIFIED`, 숨기지 말고 보고. Windows watcher/DB·Task/Notifier·키/서명 임의 변경 0, 모델 유료 호출 0.

## E. GPT가 받을 최종 판정 입력과 LIVE 적용 게이트

호스트 결과가 올라오면 GPT는 추가 요구를 흩어 보내지 말고 **단일 통합 판정**으로 패키징·회귀·독립 리뷰 필요사항·최종 위임 범위(허용 Work/skill, 요청당 $1, 일 2회/$3, 월 $10 제안, 30일 제안)와 운영 설치/롤백 계획을 묶는다. 실제 설치 및 AUTO_SIGNING 활성화는 **사용자의 한 번의 명시 승인** 후에만 실행. 그 뒤 Windows에서는 `Task backup → 기존 LIVE 보전 → 후보 적용 → 새 REQUEST부터 bounded auto-sign enabled → 2주기+재시작+실서비스/기존 리뷰 동작 검증 → 실패시 disable/rollback → GitHub 최종 결과/readback` 한 회차로 완료. LIVE 전환은 provider 전환이 아니라 기존 GitHub LIVE **자동 서명 기능의 활성화**임. 신규 유료 리뷰를 smoke test 명목으로 생성하지 말 것.

**이 인계의 다음 한 동작:** Windows Claude Code에 아래 문구 한 번 입력해 개발·시험·후보 결과 게시까지 수행.

```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab / main의 collab/projects/COWORK-AUTO-APPROVAL-20261115-001/WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md를 최신 단일 실행 지시로 읽어줘. 사용자 목표는 GPT REQUEST 게시만으로 Windows가 사전 위임 범위를 자동 검증·서명·READY LAST 게시하고 기존 GitHub LIVE Watcher가 독립 Claude 리뷰 1회를 실행하는 것. Telegram 추가 승인 버튼과 Windows Claude Code 수동 서명은 기본 흐름에서 제거해. 기존 v0.2.20 signer/READY SHA 계약, SOURCE_PIN/중복·비용·REVIEW_UNCERTAIN/N1 및 단일 LIVE를 유지하며, 격리 복사본에서 실제 코드 확인→최소 구현→기존 전체 회귀·보안/장애/rollback SHADOW 시험→DEV ZIP/SHA→PRIVATE 결과/원격 readback까지 중간 질문 없이 원샷 실행해줘. 시험 실패는 같은 작업에서 수정·재시험하고 못하는 부분만 BLOCKED. 운영 Task/DB/키/Notifier/토큰/기존 서명 정책 변경, 실제 READY 게시·새 유료 모델 리뷰/자동 서명 LIVE enable·PUBLIC 배포는 하지 마. 결과는 정확히 collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_AUTO_APPROVAL_ONE_SHOT_RESULT_FOR_GPT_20261115.md 및 CURRENT.md/TRACKER.json에 게시하고 remote readback 확인해줘.
```
