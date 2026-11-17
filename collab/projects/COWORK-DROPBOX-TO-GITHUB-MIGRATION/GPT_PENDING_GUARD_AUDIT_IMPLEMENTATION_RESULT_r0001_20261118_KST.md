# pending·Guard 조치 코드·시험·Windows 연결 결과
- 기준: 2026-11-18 KST / GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab/main`.
- 사용자 실행 지시: “이제 조치해줘”. 기존 Work `COWORK-DROPBOX-TO-GITHUB-MIGRATION` 재사용.
- **현재:** READ_ONLY_AUDIT_CODE=IMPLEMENTED, LOCAL_TEST=PASS(17×2), WINDOWS_HOST_EXECUTION=NOT_RUN, LIVE_DISPLAY_FIX=NOT_RUN, GUARD_REVIEW=NOT_RUN_BY_GPT. 실제 운영 9건의 정산/수정 완료로 표시하지 않음.

## 변경과 재사용
기존 watcher의 `reconcile`/StateStore.reconciliation_manifest·read_only=True·실제 jobs/auto_claims와 canonical REQUEST parser를 재사용. 운영 코드/DB schema/요청/서명/READY·스케줄을 바꾸지 않는 [정산 도구](../../ops/pending_requests_audit.py)를 구현.
- 원시 추적 건수와 완료·보류·대기·미확인 분리. 현재 REQUEST의 id/revision/ZIP SHA와 맞는 로컬 COMPLETED만 완료로 분리. 다른 revision/ZIP·입력 부재를 과거 완료로 감추지 않음.
- UNCERTAIN/실행·게시 중/충돌은 HELD로 남기고 requeue_allowed=false·manual_signing_admission=NOT_ASSESSED. 승인/실행 판단을 대신하지 않음.
- provider scope 분리, SQLite 한 읽기 스냅샷, SELECT/BEGIN/ROLLBACK만 사용. claim 원문/승인/READY/예외 원문·설치 경로·토큰을 출력하지 않음.
- 기존 PRIVATE dashboard CI에 2개 코드 경로를 연결, 기존 요구 PyYAML만 격리 test-deps에 준비해 v0.2.25/0.2.23 두 실제 패키지의 API 회귀를 수행하도록 수정. 권한·운영 provider·스케줄·모델 호출 없음.
- Windows 실제 정산→기존 공식 signer 지원 범위에서 Guard의 기존 1회 완료 가능성 판정→실제 표시 소스 최소 수정→근거/영수증 게시를 [원샷 실행서](GPT_PENDING_GUARD_WINDOWS_ONE_SHOT_r0001_20261118_KST.md)에 연결. 문서 게시 자체는 호스트 실행 아님.

## 실제 시험
Python 3.12.14 / Linux / 가짜 요청·SQLite. 운영 키·DB·모델·호스트 사용 없음.

| 검사 | 결과 |
|---|---|
| 기존 v0.2.25 원격 ZIP bytes/SHA/크기/CRC/경로 | PASS: 283930 B / 26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228 |
| 기존 v0.2.23 원격 ZIP bytes/SHA/크기/CRC/경로 | PASS: 282340 B / f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7 |
| v0.2.25 실제 StateStore/parser·CLI subprocess | **17 PASS** |
| v0.2.23 실제 StateStore/parser·CLI subprocess | **17 PASS** |
| 9행 합성 사례 | 추적9/완료4/보류1/대기4/미해결5; pending 9행·jobs·claim 보존. 실제 Windows 실측 아님 |
| 다른 revision/ZIP·provider·원문 부재·UNCERTAIN·부분 게시·민감 필드·symlink·잘못된 YAML/DB | PASS, 17개 회귀에 포함 |
| SQL read-only·DB main/WAL bytes·audit/claim 보존, 없는 DB 생성 차단 | PASS, 합성 고정 데이터 범위. 실호스트 WAL/SHM 직접 불변 검증 아님 |
| Workflow YAML/기존 권한 유지 | 정적 PASS. 실제 main CI는 게시 뒤 결과로 별도 확인 |
| Windows 운영 DB/실제 표시 변경/Guard 수동 처리·리뷰 | **NOT_RUN**: 현재 GPT 연결에 Windows 명령/DB 실행 도구 없음 |
| 이번 도구 독립 리뷰 | NOT_RUN. 새 유료 요청/자동 재리뷰 0 |

로컬 재현:
```text
python -m unittest discover -s collab/ops/tests -p test_pending_requests_audit.py -v
WATCHER_PACKAGE_VERSION=0.2.23 python -m unittest discover -s collab/ops/tests -p test_pending_requests_audit.py -v
```
두 번째 명령은 Linux env-prefix 표기. Windows는 같은 환경 변수를 해당 셸 방식으로 설정.

## 산출물 SHA-256
| 경로 | bytes | SHA-256 |
|---|---:|---|
| `collab/ops/pending_requests_audit.py` | 8196 | `b21cdbe571b0da0090ab303d0d91ae786f86f3c51bbb47b4cb0756c44ebb4911` |
| `collab/ops/tests/test_pending_requests_audit.py` | 10797 | `7aa7674eaa2ffd9f854a4c46312f7cdde7e4c587cb9e81e8caa11304d4229196` |
| `.github/workflows/cowork-dashboard.yml` | 3875 | `164997d77c4c211a4a2846055254b99092cd3a929ac2403d80156e15304d744d` |

## 최신 병행 작업·미검증
작업 중 다른 세션이 기존 자동 승인 Work에 v0.2.26 pin/WAIT 원인·알림 후보를 게시한 최신 CURRENT와 [결과](../COWORK-AUTO-APPROVAL-20261115-001/GPT_REQUEST_PIN_PREFLIGHT_AND_WAIT_FIX_RESULT_r0001_20261118_KST.md)를 확인. 그 개발·별도 974 PASS/한계·후보 상태를 이번 정산 도구와 합산하지 않음. 기존 승인된 v0.2.25 배포 SHA·새 v0.2.26 개발 ZIP 모두 변경하지 않음. 새 v0.2.26 설치/Notifier 연결을 이번 코드 시험으로 PASS로 바꾸지 않음.

**NEXT_ONE_ACTION:** Windows Claude Code에서 정확한 PRIVATE/main/[원샷 실행서](GPT_PENDING_GUARD_WINDOWS_ONE_SHOT_r0001_20261118_KST.md)를 한 번 실행해 실제 Guard/추적 DB/표시 상태를 정산·가능한 공식 처리·결과 게시까지 완료. 기존 승인 범위는 유지하며 현재 GPT 세션에는 호스트 직접 기동 수단이 없어 HOST_ACTION=NOT_RUN.
