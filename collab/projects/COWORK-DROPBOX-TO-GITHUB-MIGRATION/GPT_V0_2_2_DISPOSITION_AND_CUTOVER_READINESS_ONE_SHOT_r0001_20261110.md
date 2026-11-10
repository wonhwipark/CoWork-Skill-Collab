# CoWork GitHub migration — GPT v0.2.2 판정 + 운영 전 최종 통합 검증 원샷 r0001
2026-11-10 KST | NO_PR | CURRENT_PROVIDER=DROPBOX_LIVE | STATUS=HANDOFF_PREPARED_NOT_EXECUTED
작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION

## 0. 최신 사용자 전달 결과의 증거 수준
- Windows Claude Code 후속 보고를 사용자가 전달함: 격리 DB 사본과 실 GitHub 저장소 기반 전환/롤백 리허설, 전체 pytest **314 PASS / 0 FAIL / 13 SKIP**, WAL read-only mode=ro 수정, provider별 cursor key 분리.
- 후보 **skill-collab-watcher_v0_2_2_1110.zip**, **126729 bytes**, SHA-256 **7ec4f63e175b582ceec1f809281fba003f4248331a3f296689e7e19981323410**, Windows local dist_phase2에만 있다는 보고. **GPT는 ZIP 원본 바이트/실 소스를 읽거나 자체 pytest를 재실행하지 못함.**
- v0.2.2 리뷰/결과 원문은 아직 GitHub에 게시하지 않았다는 사용자 전달. PRIVATE main에는 앞선 v0.2.1용 CLAUDE_PHASE2_END_TO_END_RESULT_FOR_GPT_20261110.md (312 PASS/13 SKIP)가 이미 있음. 둘을 혼동하거나 기존 보고서를 overwrite 금지.
- **GPT 판정: ACCEPT_WITH_CHANGE / PARTIAL.** 운영 설치·LIVE/CUTOVER·정식 유료 독립 리뷰 NOT_APPROVED. 읽기 전용 리허설 성공은 실제 운영 전환 성공을 뜻하지 않음.
- 새로운 blocking: (C-1) 롤백 리허설 중 원래 Dropbox pending 요청 1건이 GitHub 조회 후 사라짐; (C-2) 새 notifier 첫 시작 시 과거 event 65건 재전송 위험. (C-3) 실제 Ed25519 미검증; (C-4) Dropbox 실샘플 B-6 SHA 미대조; (C-5) 운영 DB 최초 개방 시 테이블 3개 추가와 백업/승인 필요.
- B-3 재시작 상태 봉인·B-4 provider 단일 LIVE·B-5 논리중복·B-2 basename·T08 충돌·N-2 Telegram 안전은 계속 회귀 대상.

## 1. 사용자 승인에 대한 해석
사용자는 여러 번 중간 승인/지시를 하지 않고, 가능한 모든 검증과 **GitHub PRIVATE 결과 게시까지 한 번**에 끝내길 원함.
이미 PHASE2 통합 실행 프롬프트에서 **격리 전용 venv에 한정한 암호 라이브러리 설치 및 폐기 가능한 TEST Ed25519 키 생성/폐기**를 조건부 허용했음. 따라서 사용자가 이 원샷 실행을 Claude Code에 명시적으로 전달하는 경우 같은 테스트 범위로 진행 가능. 다만 Claude Code/OS 권한 프롬프트에서 설치가 차단되면 사용자 승인 없이 우회하거나 전역 권한을 바꾸지 말 것. 실제 권한 획득 불가 시 CRYPTO_REAL=NOT_RUN을 기록하고 다른 작업 계속.
운영 venv 라이브러리 설치, 실제 신뢰키/개인키/PAT 생성, 운영 DB/스케줄러 변경, GitHub watcher 운영 SHADOW/LIVE, 실제 유료 reviewer 실행, PUBLIC 배포는 **승인되지 않음**.

## 2. Windows Claude Code 단일 원샷 수행 (허용된 작업 끝까지)
1. PRIVATE main에서 START_HERE, NO_PR_COLLABORATION_V1, REVIEW_TRANSPORT_V1, CURRENT, 설계 r0002, 시험표 48건, GPT_PHASE1_DISPOSITION_AND_PHASE2_GATE_r0001, 기존 CLAUDE_PHASE2_END_TO_END_RESULT_FOR_GPT_20261110.md(구 v0.2.1)를 읽음. 로컬 v0.2.2 ZIP의 bytes/SHA를 보고값과 대조. 기존 v0.2.0/0.2.1/0.2.2 원본과 실제 Dropbox 운영 프로그램/DB/Task/Telegram은 **불변 보존**.
2. **C-1 pending 1건 소실은 릴리스 차단**: Dropbox, GitHub 각각 pending/claimed/completed/review uncertain의 수와 ID/상태를 provider와 epoch별로 분리. cursor 조회만으로 queue가 삭제/누락/소비되지 않도록 설계. 전환 전 backlog reconciliation manifest와 오프셋 pin, non-destructive drain 또는 각 pending 요청의 명시적 transfer/hold 상태로 소실 0 증명. 신규 GitHub READY 없는 과거 Dropbox 요청 자동 재리뷰 0. pending=0은 단순 화면에서 사라진 수가 아니라 **소실·미정산 0**을 의미. 이 조건을 만족하지 않으면 LIVE 승인 불가.
3. **C-2 과거 65건 알림 폭주 차단**: notifier bootstrap에서 provider+epoch별 durable high-watermark/notification receipt 식별자 사용. 기존에 알림 완료된 과거 이벤트는 replay하지 말되 과거 미발송된 중요 이벤트를 증거 없이 무조건 skip하지 않음. 신규 완료/REVIEW_UNCERTAIN event 1회 알림, crash/restart/rollback 시 중복 0. fake notifier로만 시험, 실제 Telegram 보내지 않음.
4. **C-3 실제 Ed25519**: 오직 격리 venv에 dependency version 및 hash pin 후 설치, 폐기 가능한 test-only Ed25519 keypair 생성; 서명 S01~S10 real-backend 검증, 만료·tamper·replay·revocation·clock skew tests. 저장소나 보고서에 secret/private test key 절대 저장하지 않음. 권한 실패 시 NOT_RUN/차단 메시지만 기록하고 계속. 운영 trust root/keys 미생성.
5. **C-4 기존 Dropbox B-6 대조**: 운영 데이터 읽기 전용 접근이 허용되는 경우에만 실제 기존 REQUEST/READY 샘플의 원본 바이트 SHA와 텍스트 재인코딩 SHA, BOM/CRLF, validator/READY 작성기 호환성을 계산, 파일 원문과 비밀 데이터는 외부 게시 금지. 읽기 불가면 NOT_RUN, 기존 승인 경로를 우회하지 않음. GitHub raw bytes pin은 유지.
6. **C-5 DB schema 3 테이블 이행**: 운영 DB는 변경하지 않고 SQLite 안전한 백업 사본(WAL 동시성 포함)을 생성 가능한 권한 범위에서만 확보. WAL read-only DB open/close 전후 main/db-wal/db-shm 메타데이터 및 Hash 비교, 정해진 작업 중 실제 서비스가 DB를 갱신할 수 있음을 인지. 사본에서 migration을 정확히 한 번 실행하고 PRAGMA integrity_check, 데이터 row/cardinality, idempotent re-open, 이전 버전 rollback 절차/복구 가능한 backup 검증. 운영 DB에 실제 table 추가, 마이그레이션, 파일 교체 금지. 직접 db 파일 복사 중 WAL 일관성이 불확실하면 online backup/snapshot로 안전하게 수행.
7. 기존 Dropbox 호환/유효 READY 제한/비용정책/CLAIMED·REVIEW_RUNNING seal/중복키/PROVIDER lease/rollback cursor/ZIP 안전 검사/N-2 알림을 포함하여 통합 pytest; 가능하면 새 오류 재현을 명시적 테스트로 승격. 이전 보고의 **314 PASS/13 SKIP**와 비교하고 원인 없는 추가 SKIP은 PASS로 판정하지 않음. 48개 T01~T38/S01~S10에 대해 PASS(REAL)/PASS(SYNTH)/PARTIAL/NOT_RUN을 구별. 실제 GitHub 읽기 시험은 기존 승인된 연결에서만 읽기 전용. Private 실제 테스트 READY 생성·운영 모델 실행 금지.
8. 기존 v0.2.2 ZIP 보존하고 신규 버전명 **skill-collab-watcher_v0_2_3_1110.zip** (필요 시 후속 patch)로 후보 packaging; CRC/Zip Slip/sha256/bytes/checksum/version/secret+prohibited-data 검사. 배포 적합성은 증거로만 판단. 인증/권한 부재로 미검증이 남으면 development_not_for_deployment 유지.

## 3. 매우 중요한 종료조건: GitHub에 원문 업로드
- **이번 v0.2.2에 대한 미게시된 Windows 상세 리허설 보고서가 로컬에 있다면 별도 보존하고**, 새로운 수정/검증 결과는 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_CUTOVER_READINESS_RESULT_FOR_GPT_20261110.md`라는 고유 파일로 PRIVATE main에 **PR 없이 직접 게시**.
- 서식: 현재 상태/변경 및 diff/테스트 입력·명령·PASS FAIL SKIP·48건 상세 매핑/실서명 및 실 API 확인/두 결함 재현·수정 증거/pending 1건 회계·rollback 증거/알림 65건 처리/운영 DB 읽기 전후 검증/새 ZIP 전체 SHA·bytes/미검증/운영 전환 승인 차단 요건/다음 한 동작.
- 보고서와 GitHub 게시 내용에는 개인·사내 금지 자료, 토큰·개인키·절대 운영 경로·실 로그 원문을 넣지 않음. commit SHA, 원격 재조회 내용 bytes SHA-256을 확인하여 보고. 기존 v0.2.1 보고서 및 CURRENT 이력 삭제·덮어쓰기 금지. 새로운 CURRENT 최신단락에 v0.2.2/신규 후보 및 결과 게시 상태를 갱신.
- 보고만 GitHub에 올려도 **독립 Claude Code 리뷰가 완료된 것은 아님**. 이번 개발 Claude의 자체 시험은 SELF_TEST_REPORTED, 정식 REQUEST/READY와 리뷰 영수증은 INDEPENDENT_REVIEW=NOT_RUN.
- GitHub 업로드가 실패하더라도 로컬 결과는 남기고 NOT_POSTED라고 보고한다. 업로드 위해 임의로 인증·권한 변경하거나 PUBLIC로 전환하지 않음.

## 4. 운영 전환 전 필수 게이트 (사용자 개입을 최소화하되 무단 전환 금지)
- pending 요청이 0 또는 개별 보존/명시적 상태 이관 완료, 무손실 reconciliation; 예전 완료 리뷰 중복 0; notifier backlog/중복 0.
- 실 Ed25519 검증, 정확한 trust root/bootstrap, B-6 기존 샘플 호환, schema backup/rollback integrity, provider cursor/lease, SHADOW 실제 검증, 명시적 리뷰 요청과 독립 결과/영수증, 최소권한 연결 및 실제 사용자 운영 LIVE 승인.
- 위 사항을 **개발자 self-test만으로 최종 승인하지 않으며**, 사용자에게 또 작은 작업을 요구하지 말고 가용 범위에서 구현·시험·ZIP·보고서 게시까지 연속 수행.
- 다음 사용자 한 번의 행동: Windows Claude Code에서 이 문서를 읽고 실행하도록 지시한다. 완료 후 사용자는 GPT에게 “GitHub 최종 결과 판정” 한마디만 하면 됨.
