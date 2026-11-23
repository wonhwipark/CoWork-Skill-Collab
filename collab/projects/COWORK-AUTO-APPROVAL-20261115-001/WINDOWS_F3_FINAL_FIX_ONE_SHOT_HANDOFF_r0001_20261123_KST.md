# Windows Claude Code — F3 최종 보완 원샷 인계
작성: 2026-11-23 KST
정본: wonhwipark/CoWork-Skill-Collab / main
Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
상태: 실행 지시 준비. 문서 게시 자체는 Windows 실행 트리거가 아님.

## 시작 시 최신 확인
1. collab/CONTEXT_BRIEF.md, 이 Work의 CURRENT.md **최상단 최신 상태**, CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md §12, GPT_V033_R2_INDEPENDENT_REVIEW_DISPOSITION_r0001_20261122_KST.md 및 최신 결과/영수증 확인.
2. 동일 목적 기존 Work에서 이어서 진행. r2 독립 리뷰(REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122)의 REQUEST/APPROVAL/READY/DISPATCH/RESULT/RECEIPT 재실행 금지.
3. v0.2.34 후보 SHA256 ecb071c4a57b48d9d3ff00e713df35fc086db7c1127b5dc31ef00c358f4f2160 (304880 B) 및 기존 112개 매니페스트를 출발점으로 확인. 기존 ZIP 보존. 실제 후보 원본 확인 실패 시 임의 대체 금지.

## 이번 한 번의 개발·시험 범위
A. F3: 현재 _intent_scope가 Commit A에서만 의도 파일을 찾는 구조를 수정. Commit A의 REQUEST+ZIP 원본 고정과 후속 의도 파일의 경로별 Git 커밋 이력 조회를 분리. 최초 검증한 정확한 후속 스냅샷 C의 SHA/경로/원문 해시/바인딩을 고정 기록하고 재검증 시 그 고정본을 재검사. HEAD 최신값을 무조건 신뢰하지 말 것. C가 A의 후손인지, 요청 revision/ZIP/SOURCE_PIN/서명/만료/키/위임이 일치하는지 검증. 불명확·다중 후보·변조·조회 실패는 fail-closed, 모델 호출 0. GitHub commits?path= 지원은 기존 전송 계층에 최소 확장, 가짜 GitHub도 동일 계약만 확장. 최초 승인/nonce 소비의 원자성과 READY LAST 보존. 보안 경계를 변경해야 할 경우 구현 전 차단 근거 기록.
B. 시험: 실제 로컬 Git 리포지토리에서 A→C 정상, C 전/후 거절, C 바꿔치기, 잘못된 조상, revision/ZIP 불일치, 만료/키 철회, 동시 프로세스 경쟁, 재시작/UNCERTAIN, nonce 중복을 검증. GitHub 원격 쓰기 경합은 승인 없이 수행하지 말고 NOT_RUN.
C. 기존 Windows 스크립트 시험 SKIP 4건: 후보 폴더의 .venv 조건을 충족하는 격리 환경에서 실행. 실제 실행 결과만 PASS. GUI 옵트인 8건은 필요성과 안전성을 판단하여 실행하지 않으면 SKIP 근거 기록.
D. QA28과 F1/F2 보존 시험, 관련 회귀, 전체 회귀. 기존 시험 결과는 증거로 재사용하고 수정 영향 범위는 재시험. 실패는 원인 수정 후 동일 범위 재시험.
E. 신규 버전 후보 ZIP(기존 명명 규칙), 릴리스 매니페스트/CRC/SHA256/크기/경로탈출/링크/민감정보/중복 검증. 코드 ZIP의 PUBLIC 게시나 운영 설치는 별도 승인 없이는 금지. 패키지 전달 허용 범위 확인.
F. PRIVATE main 기존 Work에 결과 문서와 CURRENT 최상단 현재 요약, 필요한 TRACKER 현행 필드만 갱신. 원격 commit/readback/실제 바이트 검증. 자세한 증거는 결과 문서에 기록.

## 독립 리뷰 및 LIVE 경계
- 개발 세션 자체시험은 독립 리뷰가 아님. 기존 r2 리뷰를 새 ZIP에 승계하여 PASS로 표시하지 않음.
- 신규 후보 리뷰는 최신 고정 입력·유효 보호 위임·서명·READY 및 실제 실행 계약이 충족되는 경우에만 별도 독립 리뷰 1회 요청. 유효 승인 범위를 벗어나면 REVIEW=PENDING/BLOCKED로 남기고 유료 호출 금지. '유료 리뷰' 별도 유형이나 비용 게이트 재도입 금지; 비용은 사후 영수증으로 기록.
- LIVE 호스트 설치 SHADOW, 실제 GitHub 쓰기 경합, 운영 DB review_intent_nonces 이행, Task/Notifier/키/위임/설정 변경, LIVE 컷오버는 현재 승인 범위 확인 전 수행 금지.
- 비용 상한 제거의 위험 수용과 운영 변경 승인은 최종 게이트에서 명시적으로 확인. 보호 정책의 원본/서명/만료/중복 검증을 우회하지 말 것.
- 불가 항목만 BLOCKED/NOT_RUN, 나머지는 계속. 재리뷰는 신규 유효 요청으로만 처리. 결과 게시 실패를 이유로 모델/Job 재실행 금지.

## 최종 보고
현재 상태 → 변경 사항 → 실제 시험(PASS/FAIL/SKIP/NOT_RUN) → 독립 리뷰 여부 → 미검증/차단 및 승인 → 후보 ZIP 정확한 경로·SHA256·크기 → PRIVATE commit·원격 검증 → LIVE_READY 판정 → 다음 한 동작.
목표는 기술 차단 F3를 해소해 최종 LIVE 승인 직전까지 불필요한 반복 없이 진행하는 것. LIVE_READY=YES는 모든 필수 게이트의 실제 증거가 있을 때만 사용.
