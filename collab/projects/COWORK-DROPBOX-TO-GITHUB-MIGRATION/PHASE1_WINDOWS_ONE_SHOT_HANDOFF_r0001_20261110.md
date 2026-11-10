# CoWork GitHub 이관 — PHASE 1 Windows Claude Code 원샷 개발·검증 인계
작성: 2026-11-10 KST | 상태: PREPARED_NOT_DELIVERED | 처리방식: NO_PR
작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION
중요: **이 문서를 GitHub에 게시한 것만으로 Windows Claude Code는 실행되지 않는다.** 사용자가 Claude Code 대화에 전달하기 전까지 Windows 개발은 NOT_STARTED다.

## 최종 목표와 기본 운영
기존 Dropbox CoWork를 기능과 사용자 경험 그대로 GitHub로 이전한다. 즉 GPT가 후보 ZIP·REQUEST·READY 준비 → Windows watcher가 유효성/비용/중복 확인 → Claude Code가 독립 리뷰 → PRIVATE 저장소의 REVIEW_RESULT/RECEIPT → Telegram → GPT 판정·수정·재시험. 일반 협업에는 PR을 사용하지 않는다.
- PRIVATE 정본: wonhwipark/CoWork-Skill-Collab
- PUBLIC wonhwipark/L1Work: 승인된 최종 스킬 ZIP의 기존 다운로드 경로만.
- 현재 유일한 LIVE: 기존 Dropbox watcher. 새 GitHub watcher는 구현·격리시험만. 기존 운영 변경/전환하지 않는다.
- 기본 SEMI_AUTO, AUTO_PENDING_SETUP 미검증 유지. 유효한 REQUEST/READY 없으면 자동 Claude 모델 호출 0.

## 단일 실행 목표 — 질문/중간보고로 끊지 않고 수행할 것
**이 작업 전체를 하나의 개발·검증 묶음으로 수행한다.** 단, 명시적 승인 없이는 인증키·토큰 생성, 운영 환경 설치, 실제 유료 리뷰 호출, LIVE 전환, 외부 공개 배포를 수행하지 않는다. 차단된 부분은 NOT_RUN으로 분리하고 가능한 작업은 계속한다.

1. PRIVATE main에서 아래 기준 문서를 먼저 읽고 실제 Windows watcher 설치 소스와 차이를 확인한다. 리포지토리의 문서가 실제 코드와 다르면 실측 근거 및 최소 수정 원칙을 기록한다.
   - collab/START_HERE.md
   - collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md
   - collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md
   - collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md
   - collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/ACCEPTANCE_TEST_MATRIX_r0001_20261110.md
   - collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md
2. Windows의 기존 설치판 버전과 실제 모듈을 읽기 전용으로 확인한다. 운영 코드는 절대 수정하지 않고, **새 격리 디렉터리의 원본 복사본**에서만 코드를 수정·시험한다. 이전 v0.1.5 실측은 참고이며 오늘 버전을 가정하지 않는다.
3. 기존 watcher의 validator, policy/budget, SQLite, Claude runner, Telegram을 최대한 REUSE한다. Transport 계약을 사용해 Dropbox 전송만 별도의 GitHub adapter로 교체할 수 있도록 구현한다. GitHub main ETag/conditional polling, commit-pinned raw file byte fetch, SHA/size, CAS no-overwrite 결과 게시를 구현하고 Dropbox provider는 보존한다. 네트워크 인증이 없으면 합성 fake API와 테스트만 수행하여 NOT_RUN을 기록한다.
4. Claude 리뷰 결함 B-1~B-7 모두를 추적한다. **우선 B-2(BEGIN SIDECARE 이름은 APPROVAL_SIG.json/SOURCE_PIN.json), B-5(현재 실제 처리키의 local_policy_revision/정책 변경에 따른 재호출 0), B-3(잔존 REVIEW_RUNNING을 REVIEW_UNCERTAIN 봉인, 재호출 0)**을 수정한다. 그 뒤 B-4(provider/epoch·단일 LIVE), B-6(raw byte LF/CRLF/BOM)를 보강한다. B-1/B-7은 사용자 별도 승인 전 운영 venv에 cryptography 설치/키 발급하지 않고 인터페이스와 거부 테스트까지만 구현한다.
5. 기존 Dropbox 회귀시험을 먼저 돌리고 새 GitHub 격리 합성시험을 수행한다. 번호별 T01~T38/S01~S10의 입력/기대/실측/로그·evidence를 비교하여 PASS/FAIL/NOT_RUN으로 정직하게 기록한다. **S01~S10 실제 서명 검사에 라이브러리/신뢰키가 필요한 항목은 NOT_RUN**. 무 READY, SHA/승인 불일치, 정책 개정, 재시작, 결과 게시 실패, 두 provider 동시 실행의 모델 재호출 차단을 우선 검증한다. 정상 흐름의 runner는 FakeRunner이고 **실제 유료 Claude 리뷰 모델 호출 0회**다.
6. 수정 후보를 ZIP으로 패키징할 때 버전 규칙 `skill-collab-watcher_v<major>_<minor>_<patch>_<MMDD>.zip`을 지킨다. 기존 ZIP과 설치본은 불변 보존한다. ZIP CRC·경로 안전·필수 파일·크기·원본 SHA-256·변경 파일 목록을 검증한다. 실제 설치 가능한 완성본인지 development_not_for_deployment인지 분리한다.
7. **한 번의 종료 보고**에 [현재 상태 / 실제 변경 / 실제 시험(pass/fail/not_run) / 미검증·필요 승인 / 후보 ZIP 경로·바이트·SHA-256 / 다음 한 동작]을 담는다. 장문의 로그 원문 대신 diff와 재현 근거 중심으로 작성한다. 요구된 코드/시험을 마치지 못했으면 무리하게 완료 처리하지 말고 PARTIAL 및 사유를 남긴다.
8. 비민감한 작업 결과 MD는 PRIVATE main의 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/`에 **PR 없이** 원격 원본 재조회 및 SHA 확인 후 게시할 수 있다. 비밀/반출 금지 자료·사용자 경로·인증 출력이 포함되면 게시하지 말고 로컬 경로와 REDACTION_REQUIRED만 보고한다. 소스 ZIP 게시도 파일별 보안/반출 분류가 확실히 허용된 경우에 한정하고, 승인 불명확하면 로컬 산출물로 보존한다. `collab/requests/`의 REQUEST/READY를 시험용으로라도 게재하지 않는다.

## 중단시키지 않아도 되는 부분과 승인 경계
- 사용자에게 작은 단계마다 다시 지시받지 말고 위 범위에서 개발/시험/패키징/보고를 연속 수행.
- 기존 Dropbox watcher/Windows scheduled task/SQLite 운영 DB/Bridge/Dashboard/Telegram 설정을 건드리지 말 것. OS 인증/환경 수정·새 PAT·서명키·암호 라이브러리 설치/실모델 호출/SHADOW 설치/LIVE/컷오버/PUBLIC 게시/PR 생성은 이번 작업의 권한 밖.
- SHADOW_READ_ONLY도 실제 운영 호스트에 설치하거나 돌리는 행위는 후속 별도 승인·검증 후.
- /AI-CONTINUITY/는 현재 작업 공간으로 사용하지 말고 변경 금지.

## GPT에 전달할 완료 신호
CLAUDE_PHASE1_IMPLEMENTATION_RESULT_FOR_GPT_20261110.md 를 비민감 범위에서 PRIVATE main에 게시하고, 짧게 다음처럼 보고하라.
`PHASE1_STATUS: PASS|PARTIAL|BLOCKED ; candidate_zip: <safe_basename_or_NONE> ; size: <bytes_or_NOT_RUN> ; sha256: <sha256_or_NOT_RUN> ; tests: <P/F/NR> ; model_review_calls: 0 ; production_host_changed: false ; result_git_path: <path_or_NOT_POSTED> ; blockers: ...`
이 신호를 GPT가 읽고 실측 시험·리뷰 상태를 판정한 후, 별도의 독립 리뷰 및 운영 전환 게이트를 진행한다. Claude가 구현한 코드를 같은 세션에서 '독립 리뷰 완료'로 표시하지 말 것.
