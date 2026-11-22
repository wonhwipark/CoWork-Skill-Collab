# 기술 마무리 원샷 — 최종 LIVE 승인 별도
저장소: wonhwipark/CoWork-Skill-Collab
브랜치: main
Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
2026-11-22 KST 사용자 “진행해줘”: 기술 마무리→최종 승인·LIVE의 두 묶음 중 기술 마무리 수행 요청.
범위: 누락 시험·보완·회귀·패키징→유효 보호 승인하의 독립 리뷰 1회→읽기 전용 SHADOW·사본 복구 검증→통합 보고. 이전 1~3 한정 지시는 이 범위로 대체. 보호 승인·원본 고정·최종 LIVE 확인은 유지.

## 재개·입력
CURRENT.md, GPT_V033_PARTIAL_ACCEPTANCE_AND_REMAINING_TESTS_r0001_20261122_KST.md, CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md §9 이후를 읽고 기존 요청·영수증·UNCERTAIN을 대조한다.
후보: D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33
ZIP: 같은 candidates의 v0_2_33_intent_wired_candidate.zip
SHA-256: 4dc3c701a83c22b2615e244a9dfeca8bd07ef89e9456c1b182a7ec3c01293cda
297249 B/109항목. 실물·소스 대응 확인. 기존 1007 PASS/12 SKIP·복사·v0.2.29 백업143개는 반복하지 않는다.

## 1. 남은 시험·후보 동결
GPT v0.2.33 판정의 “기존 승인 범위에서 먼저 끝낼 시험” 1~3 수행:
- 별도 OS 프로세스 watcher 2개·서로 다른 temp DB·동일 ID/revision/PIN/ZIP으로 둘 다 claim barrier 도달. 원자적 공유 fake claim에서 runner 합계 1 이하, 패자/재스캔 0. nonce 경합/스레드로 대체 금지.
- 승인·서명/READY·디스패치 전체 경로에서 nonce 소비 후/claim 후 중단→새 프로세스 재기동. replay·다른 revision/SHA·모델 시작 불명에서 권한 확대/추가 호출 0.
- _revalidate에서 소비 기록이 현재 권한·만료/키 해지·정확한 입력 바인딩을 대체하지 않는지 확인.
fake runner/test key/temp DB로 최소 수정·관련 재시험. 변경 시 최종 후보 전체 회귀 1회. 12 SKIP 사유·명령/로그·빌드/입력 SHA·PID·시점 연결. 실제 GitHub 경쟁 쓰기 시험은 NOT_RUN 유지.
ZIP bytes가 바뀌면 구 ZIP 보존·새 후보 revision/SHA 동결. CRC/중복/경로/링크/필수 파일/민감정보/크기/트리 SHA 검사. 리뷰 입력은 이 최종 코드 ZIP 한 개.

## 2. 독립 리뷰 1회
이번 요청 의도와 실제 보호 승인은 구분한다. 현행 공식 signer/watcher의 승인·위임·만료·중복을 검증·재사용하며 같은 승인은 반복 질문하지 않는다. 후보를 설치하거나 키·trust root·정책/위임을 바꿔 리뷰를 열지 않는다. 실제 권한이 없으면 해당 단계만 BLOCKED_AUTH.
정확한 ZIP의 GitHub 게시·검토자 전달 허용을 확인한다. 없으면 해당 차단만 기록, 나머지 기술 검증 계속. 회사 제한 자료·비밀·운영 DB/백업 게시 금지.
collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md 및 collab/ops/submit_review_request.py 재사용:
실물 게이트→REQUEST+ZIP Commit A→원격 bytes 검증→SOURCE_PIN Commit B(repo_id 문자열)→원격 확인→유효 보호 서명→READY 마지막→1회 dispatch.
게시자 가격 선검사를 재도입하지 않으며 운영 보호 게이트는 우회하지 않는다. 개발 세션과 분리된 기존 독립 리뷰 경로만 사용하고 결과·영수증·입력 SHA 확인. 기존 R1 재실행/새 ID 남발/불확실 재큐잉 금지.
게시 실패는 게시만 복구. 리뷰 지적은 같은 범위 수정·시험까지 묶되 자동 2회 리뷰 금지. 수정 후 새 SHA를 이전 리뷰 완료로 승격하지 않는다.

## 3. 읽기 전용 SHADOW·복구
기존 검증 모드 재사용. 실제 호스트 SHADOW와 DB 사본 검증을 구분한다. SHADOW 자체 모델/업무 쓰기/알림 0, 운영 DB 읽기 전용, LIVE provider 1개. 설치/Task/보호 설정 변경이 필요하면 해당 부분 BLOCKED. watcher/Notifier 명령·PID는 읽기 전용 확인.
v0.2.29 백업과 최신 DB의 격리 사본으로 복원·schema 호환·완료/실패/UNCERTAIN/claim/회계/알림 이력 보존·재실행 0 확인. 옛 DB로 운영 DB 교체 금지. review_intent_nonces 이행은 temp DB 리허설·적용/복구 계획까지만.
승인 리뷰의 통상 원장·서명·READY·claim·결과 기록은 현행 경로대로 처리하고 요청 ID/시각으로 SHADOW 쓰기와 구별한다.

## 4. 통합 보고·종료
기존 CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md에 새 절로 명령·증거·시험·최종 ZIP SHA/크기·리뷰 ID/결과/영수증·SHADOW/복구·차단·운영 전후를 추가한다. CURRENT/TRACKER를 맞춰 main 직접 게시·commit/원격 bytes SHA 확인, 과거 이력 보존.
차단만 모아 보고하고 가능한 작업은 끝까지 수행한다. 도구 거부 우회 금지. 문서 게시를 GPT 통합 판정으로 대신하지 않으며 GPT가 실제 결과·영수증을 읽고 판정한다.
LIVE 설치/활성화·운영 DB 이행·키/정책/위임/Task/Notifier 변경·비용 무상한 LIVE 위험 수용·컷오버는 별도 최종 사용자 확인 전 미실행. 검증 미충족이면 LIVE_READY=NO.
