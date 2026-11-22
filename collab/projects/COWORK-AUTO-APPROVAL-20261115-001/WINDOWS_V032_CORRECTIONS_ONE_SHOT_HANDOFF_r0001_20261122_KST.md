# r2 동결 후보 — PUBLIC 게시 허용 확인 / 정식 리뷰 접수·실행
저장소: wonhwipark/CoWork-Skill-Collab
브랜치: main
Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
최신 판정: GPT_V033_R2_DISPOSITION_AND_REVIEW_GATE_r0001_20261122_KST.md
기존 Windows 결과 §10의 개발·회귀·백업/사본 리허설은 보고 범위로 수용. 1014 PASS/0 FAIL/12 SKIP. 완료 시험·복사·백업은 새 실패/변경 근거 없이 반복하지 않는다.

## 정확한 입력
D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33_r2_intent_wired_candidate.zip
SHA-256: 23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206
301136 B/111항목. 기존 ZIP 4개 보존. 이 입력을 구 r1 ZIP과 혼동하지 않는다.

## 재개 조건·정식 접수
**사용자 추가 허용 확인(2026-11-22 KST):** GPT가 위 r2 ZIP의 PUBLIC CoWork 게시 허용 한 건을 물었고 사용자가 “허용”으로 답했다. 이 정확한 SHA/301136 B/111항목의 CoWork 자체 코드 ZIP을 wonhwipark/CoWork-Skill-Collab/main에 리뷰 입력으로 게시하는 범위다. 같은 자료 게시 승인을 다시 묻지 않는다. 다른 ZIP/다른 SHA·L1Work 배포·운영 설치·보호 키/정책 변경으로 확대하지 않는다.
Windows에서 실제 bytes·SHA/크기·CRC·민감정보·기존 요청/영수증/UNCERTAIN을 검증하고 기존 collab/ops/submit_review_request.py와 PRE_READY 계약으로 정식 A/B를 게시한다. 원본 불일치/검사 실패 시 게시하지 않고 정확한 차단을 기록한다. 이미 완료한 시험·원본 ZIP을 재생성하지 않는다.
승인된 게시 대상: collab/packages/v0_2_33_r2_intent_wired_candidate.zip (실제 게시·readback 전까지 NOT_POSTED).
REQUEST+ZIP Commit A→원격 bytes 검증→SOURCE_PIN Commit B(repo_id 문자열)→원격 검증. 요청 게시와 실제 보호 승인을 구분하며 Windows 가격/위임 선검사를 출판 차단 조건으로 재도입하지 않는다.
독립 리뷰 대상은 이 r2 감시기 코드다. 기존 정식 형식으로 정확한 skill_id=cowork-review-watcher와 독립 리뷰 단일 유형을 사용하며, 입력 검사 전에 이미 존재하는 동일 후보 요청을 대조해 하나만 재사용/생성한다. 독립 리뷰 1회 요청 의도는 이미 존재한다. 같은 승인을 반복 질문하지 말고 실제 보호 signer의 기존 유효 승인·위임·만료·원본/중복 게이트를 재사용한다. 충족하면 보호 서명→READY 마지막→현행 설치본의 별도 독립 리뷰 1회. 없으면 해당 경계에서 BLOCKED_AUTH/모델 0.
후보 설치·새 키/정책/위임·스킬 명의 변경으로 리뷰를 열지 않는다. 기존 R1 재실행·자동 2회 리뷰·불확실 재큐잉 금지. 결과·영수증·고정 SHA를 확인한다. 게시 실패는 게시만 복구한다.

## 정정·보존
감사 행 증가 원인을 watcher 기록으로 단정한 상수 출력은 UNVERIFIED. 실제 귀속 확인 증거로 쓰지 않는다. 사본 SHADOW PASS와 설치/Task 기반 호스트 SHADOW NOT_RUN 구분 유지.
운영 nonce 테이블 삭제를 일반 롤백으로 채택하지 않는다. 현재 DB/소비 이력을 보존하고 호환 구 코드만 복원하는 계획이 기본. 비호환이면 무손실 방안과 별도 승인 전 보류. 옛 DB 교체·운영 DB 이행/테이블 삭제는 미실행.
반출 금지 자료·운영 DB/백업을 게시하지 않는다.

## 결과·종료
같은 CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md에 후속 절로 정식 요청/고정 입력·A/B·보호 승인/READY·결과/영수증 또는 정확한 차단을 추가. CURRENT/TRACKER를 실제 상태와 맞춰 main 게시·원격 bytes SHA 검증. 과거 결과 보존.
GPT가 실제 결과/영수증을 읽고 판정할 때까지 통합 판정 완료로 쓰지 않는다.
LIVE 설치/활성화·운영 DB 이행·키/정책/위임/Task/Notifier 변경·비용 무상한 LIVE 위험 수용·컷오버는 별도 최종 확인 전 미실행. LIVE_READY=NO 유지.
