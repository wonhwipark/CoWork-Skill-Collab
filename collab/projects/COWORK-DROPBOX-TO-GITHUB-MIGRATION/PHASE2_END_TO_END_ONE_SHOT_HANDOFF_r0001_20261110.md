# CoWork GitHub 이전 — PHASE2 통합 개발·검증·결과 게시 원샷 인계 r0001
작성: 2026-11-10 KST | 운영: NO_PR | 상태: PREPARED_NOT_EXECUTED
작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION

## 0. 요청 취지와 실행 조건
사용자는 당분간 중간 피드백을 하기 어려우므로, 남은 개발 보완 → 가능한 통합·회귀 검증 → ZIP 재패키징 → 결과 MD GitHub PRIVATE 게시와 원격 재확인을 **하나의 Windows Claude Code 작업**으로 요청했다. 사소한 질문·중간 승인·프롬프트 왕복 없이 허용된 범위 전체를 연속 수행한다. 한 항목이 차단되면 그 항목을 NOT_RUN/BLOCKED로 남기고 나머지 작업을 계속한다.

**중요:** 이 GitHub 문서를 게시하는 것은 Windows Claude Code 실행 명령이나 유료 리뷰 승인 신호가 아니다. 사용자가 Windows Claude Code 대화에 실행 명령을 직접 입력한 후에만 시작한다. 이 문서만으로 watcher/모델을 자동 기동하지 않는다.

## 1. 기준 문서 — PRIVATE main에서 읽고 최신과 대조
- collab/START_HERE.md
- collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md
- collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md
- collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md
- collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md
- collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/ACCEPTANCE_TEST_MATRIX_r0001_20261110.md
- collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_PHASE1_IMPLEMENTATION_RESULT_FOR_GPT_20261110.md
- collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_PHASE1_DISPOSITION_AND_PHASE2_GATE_r0001_20261110.md

시작 기준: PHASE1은 PARTIAL/ACCEPT_WITH_CHANGE. 격리 소스 v0.2.0 후보 108,936B / SHA-256 `1003c1aba21b8e6ac4db0ca599cadb9ba83950097e8eb82d97c9849a24b7ba52` 로 보고됨. 272 PASS/0 FAIL/12 SKIP은 Claude 자체 보고값. T/S 48개 중 완성형 번호별 미실행 27개. 실제 운영 검증이나 독립 리뷰로 과장하지 말 것. 작업 시작 때 로컬 실파일/해시 대조; 불일치는 원인과 관측값 기록.

## 2. 이번 **한 번의 작업**에 포함할 범위
### A. 개발·호환성·운영 안전성 보완
1. Windows 운영 watcher v0.1.5, 운영 DB, 예정 작업, 기존 Dropbox LIVE는 **READ_ONLY** 유지. 반드시 기존 v0.2.0의 **격리 복사본**에서만 수정·시험한다. /AI-CONTINUITY/ 변경 금지.
2. 기존 Dropbox validator/policy/SQLite/review_runner/Telegram 등 최대 재사용, GitHub는 transport adapter 중심. B-2~B-7 추적표를 만들고 B-2 과거 READY 파일명 분류 변경에 따른 과거 요청 재검출/재리뷰 0 확인.
3. B-3: 실행 중인 프로세스/lease를 확인하지 않고 DB 행을 일괄 봉인하는 구현 수정. 운영 DB는 읽기 전용 인벤토리만; 실제 DB 변경 금지. 격리 DB fixture에서 잔존 CLAIMED/REVIEW_RUNNING → REVIEW_UNCERTAIN 및 알림 1회·재실행 0, 복구/재큐잉 경로 차단 시험.
4. B-4: provider/epoch/단일 LIVE lease, SHADOW 읽기 전용, 동시 프로세스와 cutover/rollback **합성 시뮬레이션**. 운영 상태·실제 전환 변경 금지.
5. B-5/T07/T08/T21: 정책 revision 변경만으로 중복 재리뷰 0, 동일 ID+revision/서로 다른 ZIP 충돌, 다른 request_id 반복 신청 정책, 과거 Dropbox 완료 원장 이관 호환.
6. B-6: 실제 기존 Dropbox REQUEST/READY의 byte SHA와 텍스트 재인코딩 SHA를 **민감정보 비반출·읽기 전용**으로 대조. GitHub API raw bytes pin·CRLF/BOM 동작 분리. 형식/서명 canonical bytes 규칙 명시하고 회귀입력 생성.
7. N-2/T20/T22: Telegram provider-specific 링크·문구/중복·불확실 알림을 격리 fake notifier로 검증, 실제 Telegram 알림은 보내지 않는다. 이전 232 PASS/12 SKIP과 기준 236 PASS/8 SKIP 차이의 파일별 SKIP 목록·원인을 설명한다.
8. 암호·승인(B-1/B-7): 운영 라이브러리 설치, 운영 trust root·키·토큰 발급은 금지. **사용자가 이 통합 지시를 Claude Code에 명시적으로 전달할 때에만** 격리 전용 venv에 버전/해시 고정된 검증 라이브러리 설치와 폐기 가능한 시험용 Ed25519 키 생성·폐기를 허용한다. 이 경우 실제 Ed25519 S01~S10과 키 폐기/회전/만료/replay 시험을 실시한다. 라이브러리 설치/시험키 생성에 별도 앱 승인 또는 실제 권한이 필요하면 무단 우회하지 말고 NOT_RUN 기록 후 다른 시험 계속.
9. 가능한 경우 기존 승인된 인증을 **읽기 전용**으로 사용하여 실 GitHub API GET/HEAD/ETag/commit-pinned byte read만 격리 경로에서 시험할 수 있다. 신규 PAT·토큰·권한 상승 금지. 실 GitHub에 시험 REQUEST/READY를 게시하거나 reviewer를 호출하지 않는다. 결과 보고 MD의 PRIVATE main 직접 게시만 별도 허용(§3).
10. T01~T38, S01~S10 48건 각 번호별로 합성/실측/NOT_RUN과 예상·실제·증거를 채운다. Public 게시, 실제 컷오버, 유료 리뷰, 실제 운영 DB/Windows 스케줄러 관련 시험은 요구되는 권한 없으면 NOT_RUN이 맞다. 모든 가능한 격리 합성시험, 기존 Dropbox 회귀, 새 서명/중복/장애/복구 시험은 한 번에 연속 수행한다.

### B. 결과 검증·후보 ZIP
- 모든 필요한 코드 수정 후 전체 pytest, 기존 Dropbox regression, 48개 테스트 대응표 수행. 0 FAIL이라도 SKIP/NOT_RUN을 별도 판정.
- 새 버전 ZIP을 `skill-collab-watcher_v<major>_<minor>_<patch>_1110.zip` 규칙으로 **기존 v0.2.0 불변 보존** 후 별도 dist에 생성. 실제 ZIP entry·CRC·경로 안전·파일별 민감정보 검사·bytes·SHA-256 검증. 운영 배포 가능 여부는 증거가 만족하지 않으면 `development_not_for_deployment`.
- 실제 GitHub 통신 성공 여부/서명 실제 PASS 여부/운영 영향 여부를 근거와 함께 구분. 어떤 범위든 이미 완료한 것 이상으로 '전체 통합 PASS'라고 쓰지 말 것.

## 3. 후속 질문 없이 **GitHub PRIVATE에 결과 게시까지 완료**
1. 성공/부분완료/실패 여부와 관계없이, 인증정보·개인키·토큰·개인/사내 반출 금지 자료·절대 사용자 경로를 제거한 **단일 결과 원문** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_PHASE2_END_TO_END_RESULT_FOR_GPT_20261110.md` 작성.
2. 반드시 결과 MD에: 현재 상태 PASS|PARTIAL|BLOCKED; B-1~B-7 판정/수정(diff 중심); 전체 회귀 pass/fail/skip 및 이전 수치 차이; T01~T38/S01~S10 **48건 상세 매핑 및 독립 증거**; 실제 Ed25519 사용 여부/실 GitHub GET 여부; 모델 리뷰 호출 수; 생산 운영 무변경 증거; 새 ZIP basename/bytes/완전한 SHA-256/로컬 보관처(민감 경로 제거); 남은 운영 게이트; 권장 다음 한 동작.
3. 결과 MD는 PRIVATE `main`에 **PR 없이** create/update 후, commit SHA와 원격 재조회 파일 바이트 SHA-256 일치까지 검증. 기존 결과가 있다면 임의 덮어쓰지 말고 버전/리비전 분리. 게시 실패 시 로컬에 보존하고 `NOT_POSTED`를 명시하되, 게시를 위해 모델 리뷰를 다시 실행하지 말 것.
4. PRIVATE에 결과 보고서를 게시하는 것은 정식 Claude **독립 리뷰**가 아니다. 같은 Claude 개발 세션의 구현·자체 시험 보고는 `SELF_TEST_REPORTED`로 표기한다. 별도 유효한 REQUEST/READY 및 독립 reviewer 실행·영수증이 없는 한 `INDEPENDENT_REVIEW=NOT_RUN`.
5. 결과 파일 게시 성공 시 `CURRENT.md`에 PHASE2 실행 상태와 결과 문서 경로를 업데이트하고 원격 readback. 상태 수정도 일반 문서 커밋일 뿐 READY 신호가 아니다.
6. 로그·README에 PUBLIC 배포, 실제 운영 설치, 실 유료 Claude 리뷰 실행, GitHub watcher LIVE 전환을 완료했다고 쓰지 않는다. 다음 사용자 개입은 **운영 전환 관련 명시 승인** 또는 실제 인증권한·연결이 필요한 예외에 집중한다.

## 4. 작업 경계
- 기존 Dropbox LIVE와 운영 watcher/SQLite DB/작업 스케줄러/Telegram 실제 설정 **절대 변경 금지**.
- 실 REQUEST/READY 신규 생성·게시, watcher GitHub LIVE/SHADOW 운영 설치, 유료 Claude 리뷰, 사용자 추가 과금, PUBLIC L1Work 게시 **금지**.
- 운영 신뢰키·운영 개인키·신규 PAT 생성, 연결 권한 변경·인증 우회, private data 외부 전송 **금지**.
- 리뷰어 자기 검토를 '독립 리뷰'로 표시 금지.
- 블로커가 있어도 허용된 나머지 개발·시험·게시를 모두 수행 후 **한 번만 최종 보고**.

## 5. 최종 완료 신호 형식
`PHASE2_STATUS: PASS|PARTIAL|BLOCKED ; tests: X_PASS/Y_FAIL/Z_SKIP ; acceptance: n_PASS/m_PARTIAL/k_NOT_RUN ; crypto_real: PASS|NOT_RUN ; github_readonly_real: PASS|NOT_RUN ; model_review_calls: 0 ; production_changed: false ; candidate_zip: <basename> ; candidate_size: <bytes> ; candidate_sha256: <full_sha256> ; result_git_path: <path|NOT_POSTED> ; result_commit: <sha|NOT_RUN> ; result_remote_sha256: <sha256|NOT_RUN> ; independent_review: NOT_RUN ; blockers: ...`

작업 종료 후 사용자는 긴 로그를 중간 전달할 필요가 없다. GPT는 PRIVATE main의 결과 원문을 재조회하여 판정하고 운영 준비 단계로 진행한다. 단, 이 문서 게시만으로 GPT의 다음 세션 또는 Windows Claude Code가 자동으로 실행되지는 않는다.
