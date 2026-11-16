# CLAUDE v0.2.23 자동 승인 LIVE 전환 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-16 KST. 호스트 실측과 자체 시험을 구분한다. GPT 판정 전 canonical 아님.
- 근거: `GPT_V023_AUTO_APPROVAL_LIVE_CLOSEOUT_CORRECTION_r0001_20261116.md`, `GPT_V023_R2_FINAL_DISPOSITION_AND_LIVE_EVIDENCE_GATE_r0001_20261116.md`.

## 결론

**`AUTO_SIGNING_LIVE=PASS_HOST_VERIFIED`** — 운영 감시기를 v0.2.20에서 v0.2.23(고정 SHA)로 전환했고, 보호된 로컬 위임을 승인 범위 그대로 활성화했다(2026-11-16 19:47:50 KST). 설치·회귀·보안·활성화·2주기·재시작·소급 차단·Notifier·롤백 준비 게이트가 모두 PASS다.
**별도 표시: `FIRST_LIVE_AUTO_SIGNED_REQUEST=NOT_OBSERVED`.** 지시에 따라 시험용 유료 요청을 만들지 않았으므로, 활성화 뒤 허용 범위의 실제 새 요청이 자동 서명·READY까지 가는 모습은 아직 관측되지 않았다. 허용 밖 요청의 차단과 중복 방지는 설치본(운영 인터프리터)의 자동 승인 시험으로 검증했고(아래), 운영에서 실제로 차단된 사례는 소급 차단 3건이다.

## 1. 증빙 정합성 (모델 호출 0)

- **MINOR 개수 정정(`COUNT_CORRECTION`):** R2 원문 `REVIEW_RESULT_1.md`(sha256 `7834c201…148d1`)의 MINOR는 **2건**이다. ① `_FAMILY` 7자 하한은 소유자 목록 절충. ② `state_store.py::_auto_usage_locked`가 비객체 `detail` JSON에서 `AttributeError`(변경 전부터 있던 결함, 출시 블로커 아님). 제가 `CLAUDE_V023_R2_AND_CONDITIONAL_AUTO_SIGN_LIVE_RESULT_FOR_GPT_20261115.md`와 해당 CURRENT·TRACKER에 쓴 "MINOR 3"과 "세 번째 항목은 본문 참조"는 **호스트 요약 오기이며 3번째 지적은 없다.** 원문은 변경하지 않았고, 이 항목으로 리뷰를 다시 실행하지 않았다.
- **`USAGE_RECEIPT_1.json` 계약:** 운영 v0.2.20 소스(`skill_collab_watcher/*.py`, 문서, 시험)에는 이 파일을 만드는 코드와 참조가 **0건**이다. 감시기는 `RECEIPT_<rev>.md`(결과·영수증·디스패치)만 게시한다. 이전 요청(V0219-R2, V0220-R1)의 `USAGE_RECEIPT_1.json`은 호스트가 개발자 gh 로그인으로 덧붙인 보충물이었다. 판정: **`NOT_REQUIRED_BY_V0220`**.
- **비용 근거(DB `REVIEW_COST`, id 4090):** `total_cost_usd` 0.5244525, `num_turns` 11, `max_budget_usd` 3.0, `effort` medium, `output_tokens` 10347, `cache_write_tokens` 54700, `cache_read_tokens` 127845, `package_size_bytes` 282340. `REVIEW_DISPATCHED`(4089)는 정책 `POLICY-STATIC-V1-LARGE`, 예산 3.0. 같은 processing key의 `COMPLETED`(4091). 모델 호출 1회, 새 지출 0.
- **보충 영수증:** 위 DB 사실만으로 `collab/receipts/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/USAGE_RECEIPT_1.json`을 add-only로 게시했다(이전 요청의 보충과 같은 방식, 추정 필드 없음, 아래 게시 목록 참고).

## 2. 승인·권한 확인 (재요청 없음)

- 사용자 승인: `GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md`와 v0.2.23 승인 변경 기록의 조건부 승인(R2 PASS·GPT PASS 후 위임 범위로 운영 적용). 이번 세션에서도 사용자가 같은 범위의 실행을 명시 지시했다. 비용·서명을 다시 요구하지 않았다.
- 보호 로컬 위임(`%LOCALAPPDATA%\cowork-approver\auto_delegation.json`, GitHub 문구가 아니라 호스트가 작성): 파일 ACL은 SYSTEM과 사용자 계정만(Users·Everyone 없음), 엔진의 Win32 DACL 검사 통과.
  - repo `wonhwipark/CoWork-Skill-Collab`, branch `main`, repo_id `1451933830`, 정책 `POLICY-STATIC-V1`만.
  - 프로젝트 가족 `COWORK-`, `L1-WORKSPACE-`(개별 프로젝트 목록 0). 스킬 정확히 `cowork-review-watcher`, `cowork-dashboard`, `l1-knowledge-updater`.
  - 요청당 1회·USD 1, 하루 2회·USD 3, 월 USD 10. `enabled_at` 2026-11-16T19:47:50+09:00, `expires_at` 2026-12-16T19:47:50+09:00(30일). R2/LARGE/XLARGE 자동 승인 불가.
- 서명 키 `cowork-approver-1`(DPAPI)과 신뢰 루트, 토큰 파일은 변경하지 않았다(해시 전후 동일, 값 미출력).

## 3. 운영 보존과 롤백

- 백업(`D:\User\whpark\cowork-phase1\live\backup_20261116\`): 감시기 정지 후 DB main/WAL/SHM 바이트 복사본(원본과 해시 동일, 복사본 `integrity_check=ok`, audit 5210행), v0.2.20 트리 복사본, 두 예약 작업 XML, Notifier 상태 파일.
- 롤백 대상 트리는 **삭제하지 않고 이름만 변경**: `D:\User\whpark\skill-collab-watcher-github.v0_2_20`(v0.2.20 ZIP 바이트와 동일 확인, 설정에 `auto_approval` 없음). 롤백 명령: `live_install.py rollback`(감시기 정지, 두 폴더 이름 교체, ZIP 일치 확인). 즉시 해제: `disable_delegation.py`(`enabled=false`, 서명 직전·게시 사이에도 재확인됨).
- 설치 전 격리 롤백 리허설 ALL_PASS(운영 트리 복사본에서 업그레이드→롤백 바이트 동일). Dropbox DB·승인 키·토큰·Notifier 파일 해시는 설치 전후 동일.
- 운영 설정 `config/reviewer.config.json`은 `auto_approval` 섹션(위임 파일 경로, 서명기 경로·키 ID, 값 비밀 없음)만 추가했다. 정지 구간 동안 새 요청은 큐에 남았고 재시작 후 정상 스캔됐다.

## 4. 설치와 시험 (운영 호스트 실측)

- ZIP `skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip` 282,340 B, sha256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`. CRC OK, 경로 이탈 0, 설치 트리가 ZIP 항목과 바이트 동일(설정·`package/` 제외), `package/`에 정식 이름 복사본 추가.
- 기능 OFF(위임 `enabled=false`, 서명기 설정됨) 상태로 먼저 시작해 1주기 이상 돌렸다. 그동안 대기 중이던 요청 3건이 `auto_seen`에 "OFF일 때 본 요청"(`enabled_at_first_seen=0`)으로 기록돼 영구 제외됐다.
- 운영 인터프리터(Python 3.11.9, 운영 venv) 전체 회귀: **967 passed, 12 skipped**(`tests/` 902건 = 890+12 과 `su_l1` 77건, 실패 0). 활성화 뒤 자동 승인 시험 4개 파일 **191 passed**(허용 밖 프로젝트·스킬, `COWORK-`/`L1-WORKSPACE-` 호환, 예산·일일 한도, 소급 금지, 중복·경합 M1, 서명 UNCERTAIN, 게시 순서 APPROVAL→READY 마지막 포함).
- 한계: 자체 시험이며 이번에도 변이 시험은 v0.2.23에서 재실행하지 않았다. 독립 리뷰는 정적(R2).

## 5. 활성화 뒤 운영 검증 (실측)

- 활성화 직후 2주기: `AUTO_PRE_EXISTING_REQUEST` 3건(기존 대기 요청, 소급 차단), `auto_claims` 0, 서명·`APPROVAL_SIG`·READY 게시 0, 원격 승인 폴더 수 변화 없음(5/8), 모델 호출 0, `dispatched` 0.
- 재시작(작업 정지→시작) 후 2주기: 같은 동작. `auto_seen` 3건 유지, `auto_claims` 0, 새 승인 0, 감시기 프로세스 2개 정상.
- 오래된 대기 요청 4건은 위임 활성화 전에 있었으므로 영구히 자동 승인 대상이 아니다(수동 승인 경로 `approve_request.py`는 그대로 사용 가능).
- 오늘(KST) 남은 한도: R2가 이미 1회·USD 0.52를 썼으므로 자동 리뷰는 오늘 1회(USD 2.48 이내)까지다. 감시기의 기존 일일 상한(2회·USD 3)도 그대로 유지된다.

## 6. Notifier (운영 변경, 백업 `aa\ops_backup_notifier\`)

- 설치본 sha256 `7ac3eb85bae050e2b33cd65595dc0fafaccdb89f4e357579521e02ae3da30920`. 추가한 알림: `AUTO_READY_POSTED`(자동 승인 게시, 요청당 USD 1 상한 안내), `AUTO_SIGNING_UNCERTAIN`, `AUTO_POLICY_STOPPED`, 승인 대기(`WAIT_INPUT` 중 READY 없음) 요청별 1회. 비발송 시험 21건 ALL_PASS(재기록된 대기 알림의 중복 억제 포함).
- **부작용 공개:** 감시기 재시작이 오래된 대기 요청 3건의 `WAIT_INPUT`을 다시 기록했고, 중복 억제 기능을 넣기 전에 Notifier가 처리해 **오래된 요청 3건에 대한 `[승인 대기]` 텔레그램이 갔을 가능성이 있다**(발송 여부는 텔레그램 쪽에서 확인하지 못함). 중복 억제와 4건 시드 적용 뒤에는 재시작해도 반복되지 않는다. 이후 재시작에서 알림 0건이 정상이다.

## 7. NOT_RUN / 한계

- 활성화 뒤 실제 새 요청 1건의 자동 서명·READY·1회 리뷰: **NOT_OBSERVED**(시험용 유료 요청 미생성). 첫 실제 요청에서 `AUTO_READY_POSTED` 알림과 감시기 이벤트 순서(`AUTO_RESERVED`→`AUTO_SIGNED_LOCAL`→`AUTO_APPROVAL_POSTED`→`AUTO_READY_POSTED`)로 확인해야 한다.
- 비판적 평가 R0~R3 프롬프트 적용·fake-runner 시험(§E): 이번 전환과 분리, **NOT_RUN**(v0.2.23 ZIP 바이트 변경 없음).
- MINOR #2(`_auto_usage_locked` 비객체 JSON)는 결함 메모로 유지, 수정 후보. 자동 승인 신호는 같은 Windows 계정의 감시기 프로세스에서 일어난다는 알려진 한계(문서화됨)는 그대로다.
- Linux·사내 소형 LLM은 범위 밖.

## 8. 게시한 것 (PRIVATE main, PR 없음)

`USAGE_RECEIPT_1.json`(R2 영수증 폴더), 이 결과 문서, 같은 Work의 `CURRENT.md` 최상단 한 단락과 `TRACKER.json` 현행 필드. 커밋·해시는 아래 "게시 확인" 단락에 기록한다.

## 9. 다음 한 동작

GPT가 이 결과를 판정한다. 호스트는 다음 허용 범위 새 요청이 올 때 첫 실제 자동 서명을 관측해 알려주고, 이상(`AUTO_SIGNING_UNCERTAIN`, 한도 도달)이 생기면 즉시 `disable_delegation.py`로 해제하거나 `live_install.py rollback`으로 복구할 수 있다.
