# CoWork Dropbox→GitHub 이관 — GPT 단독 진행 결과·전환 위험 판정 r0001
작성: 2026-11-10 KST | EXECUTOR=GPT | STATUS=PARTIAL_READY_FOR_HOST_GATES | MIGRATION_NOT_CUTOVER
GitHub PRIVATE: `wonhwipark/CoWork-Skill-Collab` branch `main`. PR 사용 안 함.

## 1. 현재 상태·증거 계층
- **현재 유일한 운영 LIVE**: 기존 Dropbox watcher v0.1.5 (Windows Claude Code 이전 보고; 본 세션에서 Windows 운영 프로세스 직접 확인 불가).
- 최신 Windows 개발 후보(Claude 보고): `skill-collab-watcher_v0_2_3_1110.zip`, 131400 bytes, SHA-256 `9a4201295156ea93b572f4a7d0f8bc6b566130c31c1cae72c55d6c8c8489cf41`, 348 PASS / 0 FAIL / 12 SKIP. C-1·C-2·C-3·C-5는 사본/격리 시험, C-4는 추후 실 Dropbox 63쌍 조회로 ACCEPT.
- **현재 GPT의 새 작업은 코드·운영 설치 아님.** v0.2.3 ZIP은 Windows 로컬에만 있다는 보고. GPT는 GitHub `collab/packages/`, Dropbox `/SKILL-COLLAB/packages/`, 현재 샌드박스를 확인했으나 v0.2.3 원본 바이트를 확보하지 못했음. 다운로드·소스 수정·ZIP 재패키징·v0.2.3 실제 회귀=NOT_RUN. 이전 v0.1.0 GPT **별도 보안 게이트 프로토타입**만 로컬 실행 가능.
- Claude Code 현재 토큰 이용 불가: `INDEPENDENT_REVIEW=NOT_RUN`. 개발자 Claude 자기 시험/추가 GPT 오프라인 시험은 독립 리뷰로 소급하지 않음. 운영 DB, watcher, 사용자 예약 작업, Telegram, LIVE 전환 및 PUBLIC 배포 변경하지 않음.

## 2. GPT Dropbox 원격 메타데이터 직접 조사 — 실측
대상: `/SKILL-COLLAB/requests/`, `reviews/`, `receipts/` (연결된 Dropbox 도구의 list_folder, recursive, 읽기 전용). 모든 페이지 완료(`has_more=false`).
- requests의 **폴더 65개** 직접 열람: REQUEST 1개 + READY 1개 = **63개**, REQUEST 1개 + READY 0개 = **2개**. REQUEST/READY 포함 유사 이름의 보조 사이드카 0개. 기존 Claude 실샘플 C-4 63쌍 계수와 부합.
- **예외 유형 A**: REQUEST 1개, READY 없음, 요청 디렉터리 내 다른 파일 없음. 같은 폴더명이 있는 리뷰 폴더와 영수증 폴더가 존재하며 각각 결과형/영수증형 파일 1개가 있음. 그러나 결과 진위, receipt ok=true, DB COMPLETED, 과거 READY 삭제 여부는 메타데이터로 확인 불가. **이미 정산됐다고 단정 금지**.
- **예외 유형 B**: REQUEST 1개, READY 없음, 요청 디렉터리에 다른 MD 1개 추가. 같은 폴더명의 리뷰·영수증 디렉터리 없음. 새 READY를 합법적으로 발행해야 하는지는 미확인. **미정산 1건이라고 단정 금지**.
- reviews의 최상위 폴더 63개, receipts 최상위 폴더 60개 및 파일 1개를 관측. 결손 여부·성공 여부를 단순 파일 수로 해석하지 않음.
- **읽은 것은 파일명 및 파일 메타데이터만**. REQUEST/READY 원문·고객 데이터·ID·저장소 비밀을 출력하거나 GitHub에 복제하지 않음. Dropbox 쓰기/삭제/READY 작성·모델 호출 0.
- Windows 운영 SQLite에는 `pending_requests=1`이라는 **과거 Claude 보고**만 있으며 GPT는 그 운영 DB를 열 수 없다. 예외 A/B와 DB 미정산 1건의 연결 관계: `UNKNOWN`.
- 보수적 회계: 사용자 승인 전 REQUEST의 두 예외와 DB pending 1건을 삭제/재호출/자동 이관하지 않고 **PENDING_RECONCILIATION_REQUIRED**로 유지. repo 파일 존재만으로 queue 정산이나 완료 처리 금지.

## 3. GPT B-7 신뢰 루트·보안 설계 완료
게시: `GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md`.
- 개별 신뢰 signer(Ed25519 private key)와 GitHub 쓰기자/Windows 검증자 권한 분리, GitHub 밖 보호된 Windows 운영 루트에 numeric repo ID·공개키 fingerprint·revocation·mode·policy hash·budget 고정.
- 서명 승인/nonce/RAW bytes/Commit A SHA/READY last, unique logical request id, 원장 crash/replay 차단, 시계 역행·만료 fail-closed, 운영 trust root 승인·감사·폐기·회전, 운영 token 분리. GitHub 문서 게시만으로 신뢰 루트 생성/키 배포 또는 reviewer 기동하지 않음.
- 설계 상태 `READY_FOR_REVIEW` (정책 초안); `OPERATING_ROOT_INSTALLED=NOT_RUN`, `FINAL_SECURITY_APPROVAL=NOT_RUN`.

## 4. GPT 오프라인 합성 시험 실실행 — **서로 다른 제품과 구분**
테스트 대상: 이 대화에 연결된 샌드박스의 **과거 GPT 단독 `skill-collab-github-review-gate_v0_1_0_1110.zip`**, 최신 Windows watcher v0.2.3이 **아님**.
- 코드 아카이브 압축 해제 후 PYTHONPATH 환경 지정, `python -m pytest tests/test_gate.py -q`: **41 PASS, 0 FAIL**, 약 0.25초. 최초 미설정 PYTHONPATH에서는 import collection ERROR가 발생했으며 수정 후 실제 PASS; 사용자 운영 환경은 영향 없음.
- 추가 시간 역행 진단: 동일 시험 서명은 만료 이후 시간에서 `APPROVAL_EXPIRED_OR_FUTURE`로 거부되지만, **과거로 되돌린 시간값**을 주면 다시 수용됨. 구형 프로토타입에는 `last_trusted_time` 영속 검사 없음. 이는 **구형 별도 gate의 설계 결손 확인**이지 Windows v0.2.3의 결함을 실증한 결과는 아니다. 최신 Windows verifier에도 같은 문제가 없는지 호스트 시험 필요.
- 이 41 PASS·시간역행 시험은 운영 watcher의 348 PASS에 합산하지 않는다. 정식 GitHub REQUEST/READY와 reviewer 실제 모델 호출 0.

## 5. 정본/계약 정리
- `collab/START_HERE.md`: 이전 Phase1 `NOT_STARTED` 등을 현재 상태처럼 표현하던 고정 문구 제거; **`CURRENT.md` 최신 섹션을 단일 상태 진입점**으로 변경. `MIGRATION_NOT_CUTOVER` 유지.
- `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`: DRAFT에 오래된 `review_attempt` 키를 운영 처리키로 오해하지 않도록 보충. 실 Windows v0.1.5 키 `request_id|revision|package_sha256|local_policy_revision` 보고와 최신 불변 logical ID를 명시. READY sidecars/Commit B 원자성의 Contents API 제약 명시. 운영 계약 활성화 없음.
- 원본 이력/기존 v0.2.3 ZIP/PROJECT 설정 변경 없음.

## 6. 전환 차단 게이트 및 다음의 '단일 승인 묶음'
| 게이트 | 현재 | 사전 확인/다음 실행 주체 |
|---|---|---|
| Dropbox 63쌍 C-4 | `ACCEPTED_REAL_READONLY_REPORTED` | 신규 BOM/CRLF 실표본은 0; 합성 보완 외 실데이터 없음 |
| 예외 A/B와 운영 pending 1건 | `PARTIAL` | Windows host가 운영 DB 읽기 전용 ID·receipt 연결 대조 및 **개별 정산/승인된 hold**; 무단 변경 불가 |
| B-7 운영 서명·trust root | `DESIGNED_NOT_DEPLOYED` | 별도 signer, trust root/ACL/시간/회전 실검증·승인 필요 |
| v0.2.3 실제 소스/ZIP 독립 검증 | `NOT_RUN` | Windows 로컬 원본 및 반출 허용된 자료 확보 필요 |
| 호스트 GitHub SHADOW | `NOT_RUN` | 사용자 승인 아래 Windows 읽기 전용 실행; DB main/WAL/SHM·원격·Telegram·모델 쓰기 0 실증 |
| Claude 정식 독립 리뷰/영수증 | `NOT_RUN` | Claude 복구 및 **신규 유효 REQUEST/READY, 비용·서명·별도 독립 세션** 필요 |
| 운영 SQLite schema 3 table 이행 | `COPY_REHEARSAL_PASS_REPORTED`, 운영 NOT_RUN | 승인된 백업, 정지 시점, 정산, 복원, 운영 이행 별도 허가 |
| GitHub LIVE/cutover/rollback | `NOT_APPROVED` | 상위 게이트 실측 후 사용자 명시 승인, 단일 LIVE 유지 |
| PUBLIC 패키지 게시 | `NOT_APPROVED` | 독립 리뷰 및 최종 스킬 배포 승인; 운영 watcher 자체를 PUBLIC에 자동 게시 금지 |

## 7. 다음 한 동작
Claude Code 불가 시 GPT는 **추가 인계 반복 없이** 문서/정책/외부 원격 읽기 전용 분석까지 완료. 이후 Windows 호스트 접근·소스 제공·독립 reviewer·운영 권한이 재개되면 **한 번의 통합 호스트 검증+독립 리뷰 요청**으로 처리. 그 전에는 운영 LIVE/DB/토큰/키 변경 금지.

GPT 단독 최종 상태: `ANALYSIS=PASS`; `DROPBOX_FOLDER_METADATA=PASS_READONLY`; `B7_POLICY_DRAFT=COMPLETE`; `OLD_GATE_41_PYTEST=PASS_SYNTHETIC`; `V0_2_3_SOURCE_RETEST=NOT_RUN`; `DB_PENDING_ID_MATCH=UNKNOWN`; `INDEPENDENT_REVIEW=NOT_RUN`; `CUTOVER=MIGRATION_NOT_CUTOVER`.
