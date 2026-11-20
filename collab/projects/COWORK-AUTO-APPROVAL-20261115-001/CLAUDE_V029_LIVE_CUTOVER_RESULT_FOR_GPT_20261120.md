# CLAUDE v0.2.29 LIVE 컷오버 실행 결과 (GPT 판정용)

- 실행: Windows Claude Code 세션, 2026-11-20 KST 20:43~21:08. 근거: `GPT_V029_LIVE_CUTOVER_AUTHORIZED_ONESHOT_r0001_20261120_KST.md`, `LIVE_ENABLE_EXECUTION_REQUEST_V029_20261120_KST.md`, 사용자의 이 원샷 실행 지시.
- **결론: 컷오버 성공. 운영 watcher는 v0.2.29로 가동 중이고 `POLICY-STATIC-V1` 등록 USD 3.00 + 보호 위임 `max_request_usd` USD 3.0 + 신규 `enabled_at` 2026-11-20T21:03:18+09:00이 적용됐다.** 시작 후 2주기, 재시작 1회, 재시작 후 2주기 관찰에서 이상 0건. 구 요청에 대한 서명·READY·모델 호출 0.
- **단, 5번째 시도에서 성공했다.** 앞선 4번은 모두 자동 롤백됐고(전부 바이트 검증됨), 4번 모두 **실제 안전 문제가 아니라 제 사전·관찰 검증 코드의 오탐**이었다(§3). 최종 상태의 판정은 오탐을 고친 규칙과 독립 최종 검증(§2)에 근거한다.
- 신규 유료 리뷰·REQUEST/READY·서명·모델 호출 0, 기존 REQUEST 재처리 0.

## 1. 상태표

```
OPERATING_APPROVAL=USER_CONFIRMED_20261120 (사용자의 이 원샷 지시 + 요청서 인계 기록의 "그래"), 운영자·롤백 최종 책임=사용자, 실행 주체=Windows Claude Code
HOST_OPERATOR_AUTH=PASS (관리자 상승 없이 운영자 계정 권한으로 가능: 위임·설정 파일 r+b 열기 성공, 설치 폴더 수정 가능, 작업 정지·시작 성공. 새 키·토큰·서명 사용 없음)
PRECHECK=PASS (중복 컷오버 없음, ZIP 310753 B·SHA c67bc342…·CRC·경로 검사, 운영 트리·설정·위임 SHA 기록값 일치, job 전부 COMPLETED·in-flight 0, DB integrity ok)
BACKUP_SHA/ACL=PASS (기존 번들 117개 파일, 매니페스트 d23b5206… = 이전에 GitHub에 게시한 값과 일치, DB 스냅샷 111c85ab… 일치, 개인키·암호문 0, 번들 ACL의 Authenticated Users:(M)는 GitHub 기록과의 독립 대조로 무결성 확립) + 컷오버 직전 정지 상태 새 번들(최종: backup_v0_2_25_cutover_20261120_210313, 매니페스트 a4bcb685…)
LEGACY_CLASSIFICATION=PASS (요청 18건: 이력 있음 13, 비활성 중 첫 관측 3, UNCERTAIN claim 1(Guard), 이력 없는 DESIGN 1. STATIC·이력 없음·활성 중 관측 = 0, 컷오버 전후 분류 동일)
INSTALL_ZIP_SHA=c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f (310753 B), PREV_LIVE_SHA=트리 f691bcf808cbf81e9c2c2a9be65335e527c2df99ea4d54a427665e4c90045c9f (v0.2.25), 이전 설정 fbce30a9…, 이전 위임 ddead4e4…
INSTALLED_TREE_SHA=b0134258e2a0f7397a3b6a7888fc60df7a401814aa918253c3b197550e36b2c3 (118개 파일 = ZIP 114 + 보존 4), 신규 설정 SHA 2ead4007…, 신규 위임 SHA 6d826672…
WINDOWS_TASK_STATUS=GitHub watcher Running, Notifier Running(건드리지 않음), Dropbox 시대 3개 Disabled 유지
STATIC_POLICY_USD3=PASS (등록 POLICY-STATIC-V1 1.5 → 3.0, 설정 변경은 이 한 줄뿐, LARGE·DESIGN 3.0 등록은 유지하되 v0.2.29가 자동 서명에서 제외)
AUTO_DELEGATION_USD3=PASS (max_request_usd 1.0 → 3.0, 위임 변경은 상한과 enabled_at 두 값뿐)
ENABLED_AT_NEW=2026-11-20T21:03:18+09:00 (이전 2026-11-16T19:47:50+09:00보다 늦고, 만료 2026-12-16T19:47:50+09:00보다 이르고, 모든 기존 REQUEST 최초 커밋(최신 18:19 KST)보다 늦음)
SIGNER_SCOPE_EXPIRY=변경 없음 (계열 COWORK-·L1-WORKSPACE-, skill 3종, 만료 2026-12-16, repo_id "1451933830", 신뢰 루트·승인키·ACL 불변)
HOST_LOAD/PRESTART_CHECK=PASS (설치 바이트 = ZIP, 정합된 설정·위임 동시 로드 max_request_cents 300, config-check version 0.2.29, 실제 설정에서 gate select unified POLICY_COMPATIBLE_NOT_APPROVED / check PASS_PREPUBLICATION_ONLY, 구 요청 18/18 신규 enabled_at 이전, 분리 DB SHADOW 18건 PASS)
TWO_CYCLES_RESTART=PASS (시작 후 2주기 86초 이상 0, 재시작 1회, 재시작 후 누적 4주기 91초 이상 0)
OLD_REQUEST_SIGN_READY_MODEL_ZERO=PASS (컷오버 이후 서명·READY·예약·claim·디스패치·비용·완료 이벤트 0, 새 모델 호출 0, jobs 9 COMPLETED·auto_claims 3(READY_POSTED 2, UNCERTAIN 1) 불변, 원격 요청 18건·이력 불변)
PROVIDER_SINGLE=PASS (provider_lease=github 불변, watcher 프로세스 쌍 1개: venv 런처 + 자식)
ROLLBACK_REQUIRED=최종 상태에서는 아님. 도중 자동 롤백 4회 실행, 4회 모두 트리·설정·위임 SHA가 원래 값으로 복원됨을 바이트로 확인하고 v0.2.25 재가동까지 실측(§3)
LIVE_VERSION=0.2.29 (WATCH_START 이벤트와 설치 파일 모두 확인)
LIVE_ENABLE=PASS
LIVE_PAID_E2E=NOT_RUN (컷오버 이후 새 외부 REQUEST가 도착하지 않음)
MODEL_CALLS_NEW=0, COST_NEW=0
SECURITY_RACE_SU_L1=OFF/UNRESOLVED (watcher 런타임 참조 0, 연결 금지 유지, 관측 실패 원인 미확정)
DEVELOPMENT_LABEL_RELEASE_DECISION=APPROVED_AND_APPLIED (조건부 운영 전환 승인에 따라 정확한 SHA c67bc342…가 설치됨, ZIP 내부 문자열은 변경하지 않음, 외부 정본인 이 기록으로 추적)
설치 시각=2026-11-20 21:03 KST(최종 설치·정합 적용), 재가동 21:04 KST, 대상 번들 경로=D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_25_cutover_20261120_210313
```

## 2. 독립 최종 검증 (읽기 전용, `FINAL_LIVE_STATE_OK=true`, 21:08 KST)

- 설치 트리는 단계 4에서 검증한 트리와 동일하고 ZIP의 114개 파일이 모두 바이트 일치, `package/` 3개 파일과 운영 설정 보존. 설정·위임 SHA는 적용 직후의 값과 동일.
- 최근 `WATCH_START` 두 건이 모두 `0.2.29`(21:04, 21:06 KST). 실행 중인 프로세스는 옛 `skill-collab-watcher\.venv`의 `pythonw.exe` 런처와 그 자식 한 쌍. 옛 인터프리터 폴더는 손대지 않았다.
- DB: `integrity_check=ok`, jobs 9 COMPLETED, auto_claims 3, auto_seen 11, lease github. 최종 기준선 이후 이벤트는 `SCAN`, `WATCH_START`, 신뢰 루트 로드·경고, 기존과 같은 만료 승인 거부 쌍, 구 요청 차단(`AUTO_NOT_ELIGIBLE` 소급, `AUTO_PRE_EXISTING_REQUEST`), `WAIT_INPUT`뿐이며 서명·READY·디스패치·claim·비용 이벤트는 0.
- 원격 요청 18건, 분류 요약이 컷오버 전후 동일.
- `config-check`: version 0.2.29, STATIC·LARGE·DESIGN 모두 3.0, 위임 "per review 300 c; no daily/monthly aggregate limits".

## 3. 정직한 기록: 자동 롤백 4회 (모두 제 검증 코드의 오탐)

| 시도 | 멈춘 지점 | 원인 | 롤백 |
| --- | --- | --- | --- |
| 1 (20:45) | 재시작 전 검증 `unified gate` | 게이트 `check` 출력은 `status` 필드가 JSON 끝에 있는데, 저는 160자로 잘라 저장한 뒤 그 안에서 `PASS_PREPUBLICATION_ONLY`를 찾았다. 실제 게이트는 통과였다. | 트리·설정·위임 SHA 복원 확인. watcher는 아직 시작 전이라 정지 상태 유지 |
| 2 (20:49) | 재시작 후 관찰 | v0.2.29는 정상 기동(`WATCH_START 0.2.29`). `lease changed`는 DB에서 읽은 튜플과 JSON에서 읽은 리스트를 비교해 항상 다르게 나온 비교 버그. lease 값은 실제로 불변. | 복원 확인 후 v0.2.25 재가동 |
| 3 (20:53) | 재시작 후 관찰 | `VALIDATED` + `APPROVAL_REJECTED(APPROVAL_EXPIRED)`를 이상으로 판정. 이는 `REQ-COWORK-V0214-R1`의 만료 승인 때문에 2026-11-14부터 **모든 버전의 모든 시작마다** 반복돼 온 기존 동작이며 CLAIMED·디스패치는 한 번도 없었다. | 복원 확인 후 v0.2.25 재가동 |
| 4 (20:58) | 재시작 후 단계 | `TRANSPORT_ERROR`(URLError)를 이름에 `ERROR`가 있다고 이상 판정. 이 일시적 네트워크 오류는 11-15 이후 44건(URLError·RemoteDisconnected·GitHub HTTP 5xx) 반복돼 온 기존 배경 잡음이고 job·claim·lease 불변. | 복원 확인 후 v0.2.25 재가동 |

- **수정:** 감시 규칙을 별도 모듈로 분리해 **과거 감사 로그의 모든 이벤트 이름 26종과 모든 `TRANSPORT_ERROR` 상세 44건**으로 시험했다(7개 시험 PASS). 이 과정에서 반대 방향의 결함도 발견해 고쳤다: 이전 규칙은 `AUTO_SIGNED_LOCAL`과 `AUTO_READY_POSTED`를 통과로 판정했다. 새 규칙은 서명·READY·예약·claim·디스패치·완료·비용·인증·실패 계열을 모두 이상으로 보고, 만료 승인 쌍과 일시적 네트워크 오류는 이력으로 입증된 경우에만 허용한다.
- 영향: 작업 정지는 시도마다 수 분이고 전체 소요는 약 24분(20:43~21:08). 이 사이 새 REQUEST는 오지 않았다(원격 요청 18건 일정). 4번의 롤백 모두 이전 v0.2.25 상태를 바이트로 복원해 실제 사고는 없었다. 감사 로그에는 시도마다 `WATCH_START`가 남아 있다(보존).
- **의미:** 이 롤백 4회는 문서의 롤백 절차(정지 → 번들로 트리·설정·위임 복원 → SHA 대조 → 재가동)가 실제 운영에서 4번 작동했다는 증거이기도 하다.

## 4. 미검증·남은 한계

- **`LIVE_PAID_E2E=NOT_RUN`:** 컷오버 후 새 외부 REQUEST가 없어 자동 서명 → READY → 실제 리뷰 1회 → 영수증은 관측하지 못했다. 이제 범위 안의 정상 STATIC 요청이 도착하면 **요청당 최대 USD 3까지 자동으로 서명·실행**된다(사용자가 승인한 범위). 첫 실제 요청에서 영수증·비용·READY를 확인하기 전에는 E2E를 검증된 것으로 표기하지 않는다.
- Notifier는 건드리지 않았고 Running만 확인했다. 새 이벤트 이름은 추가되지 않았다.
- 배경 잡음으로 반복되는 `VALIDATED → APPROVAL_EXPIRED`(V0214 요청)와 일시적 네트워크 오류는 v0.2.29에서도 그대로다. 이 요청에 대한 정리는 이번 범위가 아니다.
- 설정 파일과 설치 폴더의 `Authenticated Users:(M)` 상속 권한, 신뢰 루트 독립성 경고는 변경하지 않았다.
- `su_l1`은 비활성·미연결이며 관측 실패의 원인은 UNRESOLVED.
- 보존: 기존 번들 1개 + 컷오버 번들 4개(`backup_v0_2_25_cutover_20261120_204447`, `_205203`, `_205702`, `_210313`)가 `skill-collab-watcher-dist` 아래에 있다. **향후 롤백은 최종 컷오버 번들 `_210313`의 트리·설정·위임 사본**을 쓰고, DB는 컷오버 후 유료 job이 없을 때만 복원한다. 옛 `D:\User\whpark\skill-collab-watcher` 폴더(`.venv`)는 이동·삭제 금지.

## 5. 다음 한 동작

새 STATIC 요청이 실제로 도착하면 `LIVE_PAID_E2E`를 관측해 기록한다(영수증 비용·READY 순서·중복 0). 그 전까지는 추가 운영 조치가 필요하지 않다. 컷오버 상태를 되돌리려면 위 §4의 `_210313` 번들 절차를 따른다.
