# GPT 판정 — CoWork Classic PAT 쓰기 E2E, v0.2.18 후보, LIVE 준비 게이트
- 기준: 2026-11-14 KST / r0001
- 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- 소스: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_CLASSIC_PAT_GITHUB_WRITE_E2E_AND_LIVE_PREFLIGHT_RESULT_FOR_GPT_20261114.md`
- GitHub 소스 blob: `c0a6061eb13215076d612aed0577e78bd8923e56`; commit `53d2abf12623f19169ed0bc5346e7f4a08a2ce2f`
- **GPT_DISPOSITION = ACCEPT_WITH_CHANGE**
- `CLASSIC_PAT_USER_DECISION=ACCEPTED_CONTINUING` (사용자 확정 기본 인증. 종류·만료·교체 관련 일반 논의 반복 금지)
- `CLASSIC_PAT_GITHUB_WRITE_E2E = HOST_REPORTED_PASS`
- `WATCHER_FIRST_UPLOAD_E2E = HOST_REPORTED_PASS_ISOLATED`
- `DEVELOPMENT_V0218 = SELF_TEST_REPORTED`
- `INDEPENDENT_REVIEW_V0218 = NOT_RUN`
- `LIVE_READY=NO`, `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`
- 이 문서는 실제 운영 설치·모델 재리뷰·새 READY·LIVE 승인 자체가 아님.

## 1. 직접 확인한 증거 및 한계

- Windows Claude Code가 작성한 결과 원문을 PRIVATE main에서 직접 조회. `CURRENT.md` 최신 최상단, `TRACKER.json`, 최근 게시 commit도 조회. 결과 원문과 프로젝트 최신 상태의 버전·시험 건수·해시는 일치.
- Classic PAT에 대한 실제 API 쓰기·읽기/바이트 비교와 감시기 최초 publish/멱등/충돌 시험은 **Windows 호스트 자체 보고**이며, GPT는 Windows secret·프로세스·임시 브랜치 실행 로그를 별도 재실행하지 않았음. 이미 삭제된 두 임시 브랜치를 현재 상태만으로 실시간 복구 검증했다고 주장하지 않는다.
- 대상 `v0.2.17`의 독립 R2 정적 리뷰가 종료됐음은 이전 REVIEW_RESULT·RECEIPT 확인. **이번 `v0.2.18` 패키지는 아직 PRIVATE에 게시되지 않았으며 실제 ZIP 바이트/CRC를 GPT가 직접 확인할 수 없음**. 완료된 과거 리뷰를 새 버전 리뷰 PASS로 소급하지 않는다.

## 2. 항목별 GPT 판정

| 항목 | GPT 판단 | 근거 및 잔여 조치 |
|---|---|---|
| Classic PAT 사용자 정책 | 수용·확정 | 기존 Classic 사용을 정상 경로로 지원; PAT 형식을 이유로 재발급 요청하지 않음 |
| 격리 브랜치 Contents write/readback/cleanup | 수용 (HOST PASS) | 감시기 Classic PAT로 create·update·readback, 서버 SHA/바이트 일치, 임시 브랜치 2개 삭제 후 404, main 불변 보고 |
| Watcher 최초 자동 게시 E2E | 수용 (HOST PASS, SCOPE_LIMITED) | 격리 원장·임시 브랜치로 `UPLOAD_PENDING→COMPLETED`와 결과/영수증 PUT 2회, 모델 호출 0. **새 리뷰의 end-to-end 디스패치·운영 원장은 시험 범위 밖** |
| 멱등·충돌·재시작 | 수용 (HOST PASS) | 반복 GET만/중복 PUT 0, 원격 충돌 `CONFLICT`/덮어쓰기 0 보고. 운영 재시작·상태 소실 모든 경로가 검증됐다는 뜻 아님 |
| N1 결과 존재 가드 | **수정 수용, 잔여 LIVE BLOCKER** | `v0.2.18`에서 원격 REVIEW_RESULT/RECEIPT가 있으면 같은 논리 요청 재실행 방지, 원격 장애 시 fail-closed. 그러나 **모델이 이미 유료 실행됐으나 원격 게시 전 로컬 DB·결과가 소실되면** 원격 확인만으로 과거 호출 사실을 알 수 없음. 또 조회→디스패치 간 원자성/동시 실행 불변식 점검 필요. 미정산 유료 호출 방지 0을 전 경로에서 보장한 것은 아님. 대안: 보존된 `REVIEW_DISPATCHED` 저널/별도 독립 영속 이력, 회복 시 `REVIEW_UNCERTAIN` 보류, 비용 카운터/중복 디스패치의 고정 fail-closed 시험 |
| N2 runtime 실제 repo ID 바인딩 | 수정 수용 (SELF_TEST), 독립 확인 보류 | GitHub 실제 ID `1451933830`을 신뢰 root와 비교, 일치/불일치/ID 누락/403/timeout 테스트 호스트 PASS. v0.2.18 신뢰 검증 코드 독립 리뷰·호스트 시험 필요 |
| Q8 복합 회귀 | 수용 (SYNTHETIC PASS) | usage-limit 거부 → restart → policy revision/rollback → cursor 손실 → 복수 scan → 상태 DB 소실 이후 `v0.2.18` 테스트 PASS 보고. 첫 거부 runner 호출과 **실제 유료 리뷰 1회**를 구분하여 보고; 실 Claude CLI 한도 메시지 재현은 NOT_VERIFIED |
| S1/S2 | 수정 수용 (비차단) | 미사용 함수 제거, `taskkill` 실패 경고 추가. 다음 독립 리뷰에서 영향 범위 확인 |
| v0.2.18 패키징 | 수용 (SELF_TEST_REPORTED) | 로컬 ZIP `skill-collab-watcher_v0_2_18_1114_DEV_NOT_FOR_DEPLOYMENT.zip`, 235650 B, sha256 `519c70e3eabbe9722621afa5bf6365b93d99803c76fee2fe078722a0835522cd`, 92 파일; CRC·path/secret 검사 호스트 보고. PRIVATE/PUBLIC 모두 미게시, 독립 리뷰 미수행 |
| Notifier 2개 프로세스 | **기존 중복 실행 판단 정정 수용** | venv launcher parent→기본 interpreter child 관계/Task 하나·`IgnoreNew`·락·워터마크 관찰. 중복 Notifier 2개로 단정 금지. **GitHub 상태/워터마크 전환·실 알림은 미시험** |
| 격리 cryptography 시험 | 수용 (SELF_TEST) | Ed25519 관련 68 PASS 보고; 운영 Python 3.11.9에 라이브러리 없어 운영 실서명 불가, 운영 환경 변경 미승인 |
| Host 변경 경계 | 수용 (REPORT_ONLY) | 운영 DB main/WAL 해시 불변, Task/Notifier·Telegram/운영 인터프리터 변경 0 보고. 별도 계정 SHADOW/네이티브 추적/장기 시험 NOT_RUN |

## 3. LIVE 차단 게이트 — 우선순위

1. **v0.2.18 독립 리뷰 아직 `NOT_RUN`**: 현재 후보는 `development_not_for_deployment`. 신규 고정 ZIP과 v0.2.17→18 diff를 PRIVATE에 게시·원격 raw bytes SHA/CRC 검증하고, N1/원격 상태·N2 repository-bound approval/재시작·동시 실행/원격 장애 경계에 대한 *별도 명시적 유료 리뷰 승인*을 받은 뒤 독립 리뷰 1회. 리뷰 없는 코드 변경품을 배포 가능 판정하지 않음.
2. **N1 pre-publish DB/결과 소실**: 결과가 없을 때 과거 유료 디스패치 존재를 판별할 영속 증거가 없다면 fail-closed로 막거나, recovery 시 operator intervention 요구하는 보완 필요. 실제 비용 0의 합성/장애 주입 시험으로 증명; 수정 후 고정 재리뷰 범위와 일치해야 함.
3. **운영 Python cryptography**: 변경 권한 별도 승인 후 운영 호스트 서명 검증 E2E·호환성 시험. 샌드박스 venv PASS ≠ 운영 Python PASS.
4. **GitHub Notifier 연동/미정산 pending**: 프로세스 2개가 정상 부모·자식임은 수용. 단 provider별 DB·워터마크 분리, 1건 미정산 요청 보존, Telegram 중복 0·알림 이행 비발송 리허설 및 컷오버 롤백 확인 필요. 운영 Task/Notifier·LIVE 변경은 별도 승인.
5. **Windows SHADOW 격리/운영 전환**: 별도 계정 격리·호스트 특성의 확인되지 않은 부정경계는 남긴다. 단일 사용자 SU-SIMPLE 운영 지침에 따라 무조건 신규 설계/비용을 늘리지 않고, 필요한 수준에서 운영 변경 없는 단계적 실측·실패 시 분리 보고. 최종 단일 ACTIVE_PROVIDER 및 롤백 리허설 이후에도 사용자 LIVE 최종 승인 필요.
6. **실 CLI usage-limit 문자열**: 아직 미관측. 사용량 한도 소진을 인위적으로 유발하는 유료 시험은 실시하지 않음.

## 4. 다음 한 동작 및 금지 경계

- **권장 다음 작업:** Windows Claude Code에서 `v0.2.18` N1 잔여 pre-publish 영속 중복 차단에 대한 최소 보완 설계·코드/합성 회귀를 **격리 복사본에서 먼저 수행**, 그 후 최종 리뷰 대상 ZIP/manifest/diff를 PRIVATE review-inputs에 신규 게시·SHA/CRC remote readback 확인. 여기까지는 유료 모델 호출 없이 가능.
- **추가 유료 독립 리뷰는 별도 명시적 승인 이후 정확히 1회**. 변경 후 새 버전 또는 신규 SHA이면 리뷰 이전 고정 바이트를 재확인하고 같은 리뷰 승인으로 여러 번 자동 재호출하지 않는다.
- 운영 DB·WAL/SHM, 기존 Task/Bridge/Notifier 설정, 실알림, 운영 cryptography 설치, PUBLIC 릴리스, LIVE 전환은 현재 범위에 포함되지 않음.
- 문서·CURRENT/TRACKER 원격 게시 자체는 Windows 호스트 자동 작업/모델 호출 트리거가 아님.

## 5. 현재 상태 / 다음 행동

`GPT_DISPOSITION=ACCEPT_WITH_CHANGE` · `CLASSIC_PAT_WRITE_E2E=HOST_PASS` · `WATCHER_UPLOAD_E2E=HOST_PASS_ISOLATED` · `V0218_SELF_TEST=REPORTED_PASS` · `V0218_INDEPENDENT_REVIEW=NOT_RUN` · `N1_LIVE_INVARIANT=NOT_PROVEN` · `LIVE_READY=NO` · `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.

다음 한 동작: **N1 pre-publish 상태 소실 방지 검증을 동반한 최종 격리 후보 준비**. 사용자의 다음 명시 승인 이후 독립 리뷰·운영 설치/전환을 별도 단계로 수행.
