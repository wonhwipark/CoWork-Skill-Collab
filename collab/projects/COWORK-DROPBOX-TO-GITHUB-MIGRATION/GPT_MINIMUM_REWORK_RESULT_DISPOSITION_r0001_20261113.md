# GPT 판정 — GitHub LIVE 최소 반복 통합 실행 결과
기준일: 2026-11-13 KST | rev: r0001
REPO: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
WORK_ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
DISPOSITION: **ACCEPT_WITH_LIMITATIONS / DEVELOPMENT_READY_FOR_NEXT_APPROVAL_GATES**
ACTIVE_PROVIDER: **NONE** | CUTOVER: **MIGRATION_NOT_CUTOVER**
DEVELOPMENT: **SELF_TEST_REPORTED** | INDEPENDENT_REVIEW: **NOT_RUN**
문서 게시만으로 Windows/모델/스케줄러가 실행되거나 운영 승인되는 것은 아니다.

## 1. GPT 원격 확인 증거
- `CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md` (commit `d80064781c7cbb12a382faadd2b24db2a5f09426`, blob `113583de3bf63a6de84c145bcd12410a1038a47d`), `CURRENT.md` 최상단 및 `TRACKER.json` 실제 원격 fetch.
- `CLAUDE_DROPBOX_BRIDGE_UPDATER_RETIRE_RESULT_FOR_GPT_20261113.md` (blob `7df4fe4fb3430dead0c4bb600a65281ef2485894`) 원격 fetch; 감시기·Bridge·Dropbox updater 모두 Disabled / PID 0, notifier unchanged Running. 사용자 관리자 셸 1회 실행은 **이 별도 종료 작업**에서 수행됨. 통합 마스터 세션의 관리자 실행 0회와 구분.
- `tools/etw_attribution_preflight_r0002.py` (blob `eed64261bbe1641c6ecd3022de0688f6c59b5070`) 및 신규 테스트 (blob `7c79f8addd7e28904d55c4158ee26d99fdb87997`) 게시 확인. 실제 Windows 20 PASS/하드링크·8.3 시험은 Claude **자체 보고**이며 GPT는 Windows 호스트 ETW·NTFS 실데이터를 독립 재시험하지 않았다.
- 후보 v0.2.10 ZIP 174,745 bytes, SHA-256 `67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108`은 **Windows 로컬 보존만**, GPT 원본 bytes 미접근. 코드의 전량 독립 검증/사외 반출 승인 불가.

## 2. 항목별 최종 GPT 판정
| 항목 | GPT 판정 | 근거·제약 |
|---|---|---|
| Dropbox watcher | ACCEPT_PASS_REPORTED | 예약 작업 Disabled/PID0/데이터 보존. 후속 재부팅 유지 미시험 |
| Bridge + Dropbox updater | ACCEPT_PASS_REPORTED | 실제 Windows 사용자 관리자 셸 실행 1회, 두 작업 Disabled/PID0, notifier 변경 없음. 스크립트 notifier 표시는 PowerShell 대소문자 변수 충돌로 오출력; 별도 사후 확인 정상. 장기/재부팅 미시험 |
| Notifier process | KEEP | 과거 감사 로그 30초 DB 폴링 계속; shared Telegram 전송 모듈·비밀/노트 알림 보호 |
| v0.2.10 candidate | SELF_TEST_REPORTED / NOT_DEPLOYABLE | 527 PASS 12 SKIP(venv), 492 PASS 14 SKIP(운영 interpreter) 기존 자체시험 증거, ZIP 로컬만 |
| ETW 진단 r0002 | ACCEPT_DELTA_SELF_TEST | 수명 밖 이벤트 fail-closed, 8.3 alias, file-id proof 보강, 신규 20 PASS 보고. raw ETL 시간·PID 정규화 문제 미해결 |
| C 실제 GitHub GET | REUSE_PREVIOUS_HOST_PASS | 이전 비관리자 3회 GET-only 7 calls 보고; 이번 마스터에서 새로 실측하지 않음 |
| C 운영 파일 무접근 | PARTIAL / NOT_PROVEN | ETW `FAIL_UNTRUSTED_MEASUREMENT` 유지; `C_ALT_EVIDENCE=PROPOSED_ONLY` |
| B 실운영 Ed25519 서명키/root | BLOCKED_SIGNER_DEVICE | 시험키 PASS를 실서명으로 소급 금지 |
| D ZIP 반출 | BLOCKED_EXPORT_CLASSIFICATION | 70 items = UNCHANGED 34 + CHANGED 12 + NEW 24; 기존 유래 46개는 원소유권·반출 승인 필요. NEW 24개도 정책 확인 필요 |
| E 정식 Claude 독립 리뷰 | NOT_RUN | 개발 Claude 자체 구현/시험과 독립 reviewer 구분. 비용·서명 READY·영수증 없음 |
| 롤백 시나리오 | PASS_SYNTHETIC_ON_SNAPSHOT_COPY | 기존 운영 DB 자체가 아니라 시점이 다른 사본; 실제 Windows 설치/롤백 NOT_RUN |
| 운영 readiness | NOT_APPROVED | ACTIVE_PROVIDER=NONE, GitHub LIVE 전환 명시 승인/최종 운영시험 없음 |

## 3. 최소 반복 C 기준에 대한 GPT 제안
- 현재 반복 관리자 ETW trace를 다시 채집하는 것은 우선순위 낮음. **가능하면 사전 확보한 파일·ACL/비관리자 증거를 기반으로 대체 증거의 보안 수락 계약을 먼저 명확히 심사**. 다음은 별도 사용자 승인 전 **PROPOSED_ONLY**.
- 제안 불변조건: (1) GitHub SHADOW 전용 실행 계정이 운영 DB/main/WAL/SHM/lock 및 운영 secrets에 대해 Windows 실효 ACL 읽기/쓰기 거부, (2) 별도 state dir 및 파일 identity/8.3·hardlink/NT alias 상호격리, (3) 실행 call path와 runtime privilege 상승·자식 프로세스 범위를 증명, (4) 파일 접근 거부 양성 대조/의도된 SHADOW I/O를 증명, (5) 독립 리뷰에서 재현·승인된 evidence contract. 시스템이 파일 접근을 못하게 하는 것과 ETW 사건이 0건이라는 명제는 다르므로 `C_ETW=NOT_PROVEN`을 여전히 병기.
- 위 조건 실제 충족 근거가 불완전하면 `C=PARTIAL`; 계약 변경 승인이 있더라도 증거 없이 자동 PASS 전환 금지.
- 반대 선택지: 기존 ETL 보존본 재해독/직접 ETL parser로 양성대조 입증 후 필요한 경우 **승인된 1회만** 관리자 C 실측. 동일 실패 명령 반복 금지.

## 4. 최소 승인 패킷 — 사용자에게 묻는 항목
1. **B**: 운영 signer로 사용할 **감시기 PC와 다른 기기 지정**. 개인키는 해당 기기 내부에서 사용자 직접 생성하고 이 PC에는 공개키/pin만 관리자 승인 하 설치. 키 값은 채팅/GitHub/로그에 넣지 않음.
2. **C**: (추천) 4가지 독립 증거 기반의 새로운 C 수락 기준 **검토·적용을 승인할지**, 아니면 보존 ETL 재분석/관리자 1회 측정 경로인지 선택. 승인 시에도 보완시험 및 독립 검증 통과가 필요.
3. **D**: **기존 v0.1.5 유래 34 UNCHANGED + 12 CHANGED**와 NEW 24의 코드 소유권·사외 반출 가능 여부를 정식 확인(특히 PRIVATE GitHub도 사외). 거부되면 해당 파일 업로드 금지; 부분·메타 요약 검토 결과는 전체 ZIP 독립 리뷰가 아님.
4. **GitHub 읽기 토큰**: 임시 토큰으로 과거 실 GET 시험은 했으나 시험계정 전용 장기 보관처에 repo Contents:read-only 인증이 없다는 신규 보고. 해당 최소 권한 토큰의 **사용자 발급·안전 설치** 필요. 채팅 공유 금지.
5. **E**: B/C/D 충족 후 독립 Claude reviewer runner와 정식 REQUEST/READY+영수증, 1회 비용 상한(기본 STATIC $1) 명시 승인. 서명되지 않은 임의 요청은 reviewer 호출 0.
6. **LIVE**: 마지막에 별도의 Windows 운영 GitHub watcher 설치/DB 이행·롤백 시험·provider 단일 활성화 **명시 승인**. `ACTIVE_PROVIDER=NONE`을 승인 없이 변경 금지.
7. **잔여 알림기**: 현재 유지. GitHub notifier 이행/retire은 LIVE 경로 설계 확정 후 별도.

우선 사용자에게 **B / C / D / 토큰**을 한 번에 확인받아 기존 차단을 해소하고, E+LIVE는 필수 전제 확인 후 별도 안전 승인으로 진행. 다른 인계서를 계속 만들거나 동일 테스트를 반복하지 않는다.

## 5. 한 동작
사용자의 B 기기 지정·C 수락경로 선택·D 권한 확인·GitHub read-only credential 준비 상태를 한 묶음으로 받아 정본 CURRENT와 승인 체크리스트를 갱신. 정식 서명·유료 리뷰·출처 불분명한 ZIP 업로드·GitHub LIVE는 여전히 NOT_RUN.
