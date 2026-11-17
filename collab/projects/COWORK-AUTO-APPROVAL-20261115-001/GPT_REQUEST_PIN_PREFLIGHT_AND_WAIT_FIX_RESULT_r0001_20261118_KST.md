# REQUEST pin·승인 보류 재발 방지 구현·검증 결과

- 작성: GPT / 2026-11-18 KST
- 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `COWORK-AUTO-APPROVAL-20261115-001`; MSC 결과 연결: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 지시: 승인 서명/READY 보류 원인·재발 방지 대책 제시 후 “해결하라고”.
- 범위: 실제 코드 수정·격리 회귀·후보 패키징·PRIVATE 게시·기존 MSC 완료 원문 확인. 운영 호스트 접근/설치를 실행한 것으로 표시하지 않음.

## 1. 현재 결과

**기존 MSC 설계 리뷰는 완료됐다.** 작업 중 새로 게시된 [REVIEW_RESULT_1.md](../../reviews/REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117/REVIEW_RESULT_1.md), 서명/READY/DISPATCH/실행 RECEIPT 및 [기존 GPT 판정](../L1-WORKSPACE-RAG-20261111-001/GPT_MSC_DUAL_ENTRY_R1_DISPOSITION_r0001_20261118_KST.md)을 직접 읽었다. ID/revision·패키지 SHA·REQUEST/READY 실제 바이트 해시·processing_key·승인 유효 시간 내 예약을 대조해 PASS. `COMPLETED / ok=true / ACCEPT_WITH_CHANGE / 차단 0 / 비차단 권고 2 / REVIEW_CYCLE=CLOSED`. 이 확인은 이미 종료된 판정의 수신·재확인으로 새 리뷰/재판정이 아님.

별도로 **재발 방지 v0.2.26 코드와 개발 ZIP을 실제 작성**했고 새 회귀 61개 포함 **974 PASS**를 확인했다. Linux 범위의 35 SKIP, 기준본에서 실패한 34개는 별도 제외/기록. 전체 시험 또는 Windows 운영 PASS로 승격하지 않음. 후보는 **development_not_for_deployment**.

`WINDOWS_INSTALL=NOT_RUN`, `OPERATING_NOTIFIER_APPLIED=NOT_VERIFIED`, `INDEPENDENT_REVIEW_V026=NOT_RUN`. 기존 v0.2.25의 조건부 배포 승인·고정 SHA는 유지하며 이 후보로 무단 대체하지 않는다.

## 2. 확인 원인과 실제 코드 수정

| 문제 | 실제 수정 |
|---|---|
| 자동 승인 사전검사는 숫자 repo_id를 str()로 변환해 통과, 최종 승인검사는 원래 JSON 타입을 비교해 거부 | `approval.validate_source_pin`을 추가해 정확 V1 필드/schema·문자열 numeric repo_id·40자리 commit을 엄격 검사. 자동 예약 **전**, 최종 승인 검증, signer 입력이 같은 함수를 사용. 게시된 숫자형은 자동 보정하지 않음 |
| 잘못된 pin이 이미 예약된 후 UNCERTAIN으로 남을 수 있음 | 원본에서 같은 numeric ID를 숫자형으로 투입해 예약 생성/실패를 재현. 수정본은 `PIN_REPO_ID_TYPE`으로 예약·signer 전에 차단. 잘못된 입력으로 예약이 생성되지 않은 경우만 수정된 정상 입력을 처리; 기존 UNCERTAIN은 보존·자동 재시도 금지 |
| AutoResult를 무시하고 READY 성공 뒤에도 일반 WAIT_INPUT을 기록 | 기존 orchestrator가 실제 status/reason을 기존 audit detail에 연결. READY 게시 성공 주기에는 'READY 없음' WAIT를 남기지 않음 |
| 대기 알림에 원인·다음 행동이 없고 누적 비용 0으로 오해 가능 | 기존 `notify_events.run_once`/메시지 함수에서 단계·오류 코드·다음 조치 1개 표시. 이번 승인 단계의 모델 미호출과 기존 실행/누적 비용 미확인을 구분. 예외 원문은 출력하지 않음 |
| 같은 대기 반복·수정 후 이미 READY인 과거 대기 알림 | 기존 watermark/delivered 재사용. 같은 단계/원인은 1회, 원인 변경은 1회. 기존 auto_claims/jobs를 **읽기만** 하여 READY/실행 결과에 뒤처진 대기 알림 억제. 주 불확실 알림과 이중 발송 억제 |
| PRIVATE에만 있고 실제 후보 ZIP에서 누락된 사전 검사 도구 | 정본 `collab/ops/source_pin.py`·`review_request_gate.py` 원문을 변경 없이 패키지 tools/에 포함, 기존 시험 36개도 모듈 import 경로만 맞춰 포함. 신규 REQUEST는 실제 LIVE config로 select/check 후 게시해야 함. 검사 도구 존재와 실제 호스트 연결/실행을 동일시하지 않음 |

기존 요청·입력 핀·서명·READY·DB·위임·비용 정책·중복 방지는 변경하지 않았다. 새 엔진/원장/DB schema/운영 서비스는 만들지 않았다. 신규 REQUEST 작성 절차는 기존 AGENTS/예산 계약의 사전 게이트를 그대로 유지한다. 직접 GitHub API 쓰기 전부를 이 변경이 기술적으로 차단한다는 주장은 하지 않는다.

## 3. 실제 시험

| 검사 | 결과 |
|---|---|
| v0.2.25 원본 ZIP·버전 검증 | 283930 bytes / SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228` 일치 |
| 원본에 현실적인 numeric GitHub ID fixture + 새 pin 회귀 적용 | 11 FAIL / 1 PASS. 특히 숫자형 pin이 예약까지 생성됨을 재현. 운영 입력/키/호출을 사용한 재현 아님 |
| 새 pin 계약/기존 UNCERTAIN 보존/알림/동봉 도구 회귀 | **61 PASS**. 임시 키·가짜 GitHub·가짜 runner·가짜 sender를 사용한 격리 시험 |
| 원본 전체 Linux 실행 | **913 PASS / 34 FAIL / 35 SKIP**, 261.40초. Windows msvcrt/cmd/플랫폼 차이 및 v0.2.25에 남은 과거 집계 상한/fixture 기대값 실패를 확인 |
| 수정본의 실행 가능한 회귀 | **974 PASS / 35 SKIP / 원본 실패 34개 deselected**, 13.14초. 추가된 회귀 61개 모두 PASS. 기준 실패를 숨기거나 전체 PASS로 표시하지 않음 |
| ZIP CRC·113개 경로·113개 파일 전집합 manifest·비밀 패턴 검사 | PASS. manifest는 자기 항목 제외 112개 hash 기록, 외부 ZIP SHA가 manifest 자체를 고정 |
| 동일 소스 두 번 패키징 | 동일 bytes/SHA PASS |
| Windows 보호 signer·LIVE·Notifier 어댑터·운영 설치 | **NOT_RUN / NOT_VERIFIED** |
| 이 새 후보의 Windows Claude 독립 리뷰 | **NOT_RUN**. 신규 REQUEST 사전 게이트/실제 보호 승인 없이 새 유료 리뷰를 만들지 않음 |

상세 node ID·제외 항목: [VALIDATION.json](artifacts/v0_2_26/VALIDATION.json). 제외 34개를 SKIP/PASS로 바꾸지 않았다. 기존 원본 대비 새로 발생한 실패(버전 제목/비현실적 문자열 repo-ID 테스트 fixture)는 실제 계약에 맞게 수정하고 최종 범위에서 재시험했다. 제품의 Windows lock/프로세스 제어·집계 비용 정책을 Linux 시험 통과 목적으로 바꾸지 않았다.

격리 의존성: Python 3.12, pytest 8.4.2, 기존 PyYAML/cryptography 및 requirements 범위의 Dropbox SDK/requests. 운영 Python/venv·키/토큰에는 손대지 않았다. 실제 유료 모델 호출 0, 운영 signer 호출 0, 운영 키 생성 0. 시험용 임시 키/가짜 서명·가짜 READY와 실제 운영 인증 산출물을 구분한다.

## 4. 산출물·무결성

| 산출물 | 정확한 PRIVATE main 경로 |
|---|---|
| 개발 후보 ZIP | `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_26/skill-collab-watcher_v0_2_26_1118.zip` |
| 코드·시험 diff | `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_26/diff_v0_2_25_to_v0_2_26.patch` |
| 후보 metadata/QA/배포 차단 | `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_26/CANDIDATE_MANIFEST.json` |
| 범위·원본 실패 node IDs | `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_26/VALIDATION.json` |
| 기존 MSC 완료 bytes·결속 확인 | `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_26/MSC_CHAIN_VERIFICATION.json` |

후보: **308737 bytes / SHA-256 `f08adb6099d06daf494362ed7e33ea66aabcbf749cfd2c027a7f70bcba5540fe` / Git blob `d788d196e66acb1ae95a9495e55f562644fa11a4` / 113 members**. 구버전 원본은 그대로 보존. 이 ZIP은 PUBLIC 배송/운영 설치/독립 리뷰 완료본이 아니다.

기존 MSC 결과 SHA-256 `19208aa837cfff73186cd9b8f7efe369014bbc5daaac3833cf025f0465743c81`; 실행 영수증 SHA-256 `813d8ca4a2716d98e0263243b9bdd8507d3a18756f6964e0bfdf5f5f99593f68`. 상세는 연결 JSON. 보호 공개키·Windows DB에 직접 접근하지 않아 암호학적 서명 재검증/비용 독립 확인은 하지 않았다.

## 5. 운영 잔여와 다음 한 동작

- 기존 MSC는 이미 **1사이클 종료**. 재요청·재서명·재리뷰·기존 입력 수정 없음. Guard의 불확실 요청은 다른 상태로 보존.
- 이 개발 후보의 runtime 방어와 알림 라이브러리 수정은 완료했지만 실제 Windows 설치/별도 Notifier 어댑터 연결은 미실행. Notifier 자체 설치 스크립트를 보지 못했으므로 '실제 Telegram 오류 안내 적용'까지 완료로 보고하지 않는다.
- 진행 중인 기존 v0.2.25 조건부 운영 배포 승인 원본을 바꾸지 않는다. **다음 한 행동:** Windows가 그 기존 운영 작업 상태를 먼저 확인하고, 이 후보의 실제 플랫폼 시험·별도 Notifier의 기존 라이브러리 호출 가능 여부를 읽기 전용 확인해 같은 Work에 결과를 회수. 유효 운영 범위와 독립/회귀 게이트가 충족되기 전 후보 설치 0. 이 문서가 호스트를 기동하거나 새 유료 리뷰를 승인하는 신호가 아님.
