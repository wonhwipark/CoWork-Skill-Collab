# GPT 판정 — CoWork v0.2.14 A안 독립 리뷰와 v0.2.17 후속 LIVE 게이트

- 판정일: 2026-11-14 KST
- 저장소/브랜치: PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- GPT_DISPOSITION: `ACCEPT_WITH_CHANGE`
- A_EXECUTION: `COMPLETED_REPORTED_AND_REMOTE_ARTIFACTS_VERIFIED`
- INDEPENDENT_REVIEW_V0214: `COMPLETED_WITH_BLOCKING_FINDINGS` / 배포 품질 게이트 `FAIL`
- DEVELOPMENT_V0217: `SELF_TEST_REPORTED`; INDEPENDENT_REVIEW_V0217: `NOT_RUN`; ARTIFACT_PUBLISH_V0217: `NOT_POSTED`
- LIVE: `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`
- 이 문서는 **비민감 GPT 판정/인계**이며 새로운 모델 호출·키/토큰 발급·운영 변경·LIVE 승인이 아니다.

## 1. 직접 확인한 원격 증거

- Windows Claude 결과: `CLAUDE_A_APPROVED_V0214_SINGLE_REVIEW_RESULT_FOR_GPT_20261114.md` (Git blob `ad5adcae96f8fd7cc8a2a8795986c5fbd990cc2c`).
- 정식 독립 리뷰: `collab/reviews/REQ-COWORK-V0214-R1-20261114/REVIEW_RESULT_1.md` (Git blob `40f693376e28ededa298cecc18c3deddb37485f6`); 정적 리뷰가 이중 디스패치·scan/watch 충돌을 포함한 결함 다섯 건 제시.
- 엔진 영수증: `collab/receipts/REQ-COWORK-V0214-R1-20261114/RECEIPT_1.md` (Git blob `3db73001e25d8294f59ad9f2f2cba31ac57daaf1`).
- 사용 영수증: `collab/receipts/REQ-COWORK-V0214-R1-20261114/USAGE_RECEIPT_1.json` (Git blob `c1045c05d2834b256f43b6bb1aa8766a40ce3d62`): 모델 호출 1회, `$0.9695416`, 18 turns, `output_tokens=21479`, `cache_creation_input_tokens=84836`, `cache_read_input_tokens=452232`. R1 권장 목표(3 turns/출력 3000) 초과, 상한 $1 이내. CLI 2.1.218 `--max-turns` 미지원은 호스트 보고.
- APPROVAL/REQUEST/READY 경로·고정 v0.2.14 패키지 SHA 기록은 호스트 결과/요청과 일치. 서명키 암호화 보관·15개 시험, 모델 호출 실제 단일성/게시 바이트 동등성은 호스트 보고에 의존하며 GPT가 운영 PC 비밀/프로세스를 직접 재시험한 것은 아니다.

## 2. 지적별 GPT 판정

| ID | GPT 판정 | LIVE 심각도 | 이유와 최소 완료 증거 |
|---|---|---|---|
| F1 다른 policy revision 키에서 중복 호출 | 수정 수용 | BLOCKING | 롤백·커서 소실이 필요해도 동일 논리 요청 중복 유료 실행 0 불변조건 위반. v0.2.17 재현/패치 자체 보고 수용; 새 상태·서명/재시작 부정시험 및 독립 리뷰 필요 |
| F2 scan/watch 상호 배제 실패·오탐 봉인 | 수정 수용 | BLOCKING | 살아 있는 실행을 `REVIEW_UNCERTAIN`으로 잘못 봉인. 공통 락과 거부 종료코드/SHADOW 6 유지, 실제 Windows 다중 프로세스 시험 필요 |
| F3 일일 비용·호출 상한의 비원자 예약 | 수정 수용 | BLOCKING | 승인된 일간 호출·비용 상한 초과 가능. DB `BEGIN IMMEDIATE` 예약의 동시 다른 key 경쟁·재시작/rollback 시험 필요 |
| F4 scan 단독 크래시 잔류 | 수정 수용 | MAJOR (LIVE 이전 검증 필수) | 다음 scan에서 불확실 상태로 봉인·알림·재호출 0 검증 |
| F5 타임아웃 후 Windows 손자 프로세스 잔류 | 수정 수용 | MAJOR (LIVE 이전 검증 필수) | 프로세스 트리 종료, Windows `.cmd`/백그라운드 손자, timeout·crash 부정시험 필요 |

- 호스트는 후보 `v0.2.17`에서 5개 수정 및 자체시험 venv `644 PASS / 12 SKIP`, 운영 인터프리터 `578 PASS / 17 SKIP`, SHADOW 종료코드 6→3 회귀 재수정 보고. **원본 v0.2.17 바이트·패치·테스트를 GPT가 조회하지 못했으므로 `CODE_VERIFIED`, `REVIEW_PASS`, `RELEASE_READY` 아님.**
- v0.2.16의 usage-limit 대기/재개 및 토큰 JSON 형식 증분은 v0.2.14 정적 리뷰 범위 밖. 새 후보 재리뷰는 v0.2.14→v0.2.17 전체 증분과 usage-limit/상태/토큰/알림 상호작용을 포함해야 한다.

## 3. 확인된 운영 위험 및 보완

1. 자동 결과 업로드 `HTTP 403 / UPLOAD_PENDING` 이후 개발자 `gh` 계정으로 동일 바이트 게시: **원격 산출물 보존은 확인되지만 감시기 자동 게시 E2E는 FAIL/미검증**. LIVE에서 수동 복구 없이 최소 권한 엔진 토큰으로 결과/영수증 원격 readback 후 완료 처리, 게시 실패 재호출 0을 입증.
2. `repo_id`는 trust-root 라벨과 비교되지만 실제 GitHub repository ID 결합은 미입증. 실 저장소 identity 검증 및 잘못된 repo ID/다른 repo 부정시험을 LIVE 이전 게이트에 포함.
3. 읽기전용 PAT 만료/회전 정책 부재, 기존 개발자용 광역 토큰 사용 우회 금지. 새 엔진용 최소 권한 Contents Read/Write 단일 PRIVATE repo·만료·계정/secret 격리 검증 필요.
4. R1 출력 21,479 토큰/18 turns, 비용 $0.9695로 상한에 근접. 비용 예산 PASS는 턴·출력 토큰 예산 PASS와 다름. 장래 상시 정책은 host 실지원 옵션·preflight 입력 제한·호출/일일 비용 예약·한계 도달 fail-closed를 검증 후 활성화.
5. 운영 호스트 암호 라이브러리·17 SKIP 원인, 실제 Notifier GitHub 연동, SHADOW 계정/DB WAL 무쓰기, 백업·복구·단일 LIVE/롤백 리허설 미검증. `ACTIVE_PROVIDER=NONE` 유지.

## 4. 후속 승인 패킷 — 실행은 보류

- **B안 인증:** 감시기 전용 PRIVATE repo contents read/write fine-grained PAT 1개 발급·암호화 설치, 만료·권한·기존 개발자 gh 자격 분리. 사용자 명시 승인 필요.
- **수정 후보 재리뷰:** 사용자 승인 후 v0.2.17 ZIP·diff·manifest를 PRIVATE `review-inputs/<new_review_id>/`에 게시하고 원격 SHA/readback 후 **독립 리뷰 1회**. 권고: 여러 상태기계·보안/운영 동시성 수정이므로 `R2` 구조 리뷰, `POLICY-STATIC-V1-LARGE`, 최대 `$3`, 상한 내 1회. 실제 승인 전 모델 호출 0. 리뷰 후 새 패치가 있으면 기존 리뷰 PASS 승계 금지.
- **실호스트 SHADOW/복구:** Windows 분리 계정에서 GitHub 실조회·서명/키·token·업로드/영수증/알림·중복·재시작·타임아웃/rollback 시험. 운영 SQLite main/WAL/SHM 불변을 확인하며 일관 스냅샷 백업·별도 사본 복구 리허설. 운영 데이터·Task 변경은 사용자 승인 전 금지.
- **R0~R3 상시 정책:** 향후 편의 기능으로 **별도 1회 사전 한도 승인** 대상. **1회성 독립 리뷰로 첫 LIVE를 검증할 때의 필수 선행 게이트는 아님**. 상시 자동 유료 리뷰 활성화와 LIVE 감시기 활성화를 분리.
- **최종 LIVE:** 위 증거의 GPT 종합 PASS, 미정산 요청·완료 이력 보존, 알림 중복 0, 한 provider만 ACTIVE, 되돌리기 확인 후 **사용자 별도 최종 승인**을 받아야 함.

## 5. NEXT_ONE_ACTION

승인받을 3개 필수 항목(B 쓰기 PAT, v0.2.17 R2 독립 리뷰 최대 $3 1회, 실호스트 SHADOW+운영 DB 백업/복구 격리 리허설)을 하나의 선택으로 사용자에게 제시하고, R0~R3 상시 정책은 선택 항목으로 별도 표시. 승인 전 가능한 비민감 설계 검증·문서 정리만 허용, 유료 재리뷰·신규 PAT·운영 DB·LIVE 변경은 수행하지 않음.
