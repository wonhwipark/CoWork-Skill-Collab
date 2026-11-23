# Windows Claude Code — v0.2.36 신규 독립 리뷰로 Runner 완료 감지 E2E 검증
작성 2026-11-23 KST | wonhwipark/CoWork-Skill-Collab main | 기존 Work collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
## 목적과 최신 지시
사용자는 기존 v0.2.35 완료 결과 재생 대신, **실제 최소 변경이 있는 새 버전 v0.2.36**으로 **정식 독립 리뷰 1건**을 진행해 Claude 리뷰 완료 → GitHub 게시 → Actions Runner 이벤트/판정 연결을 검증하도록 요청함. Issue #3의 무모델 재생 시험은 superseded/closed. 이 인계서 게시 자체는 Windows Claude Code 실행이나 REQUEST/READY가 아님.
## 시작
`collab/CONTEXT_BRIEF.md`, `collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md`, `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md`, 이 Work CURRENT 최상단과 §14 결과, `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`, `.github/workflows/cowork-gpt-disposition.yml`, 기존 REQUEST/RESULT/RECEIPT/Actions Runs 최신 상태 확인. 기존 완료 `REQ-COWORK-V035-WATCHER-REVIEW-20261123` 재실행 금지. 동일 Work 재사용, 새 Work 금지.
## 원샷 개발·시험
1. Windows에서 v0.2.35 정확 SHA256 `658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740` 로컬 원본을 확인. 기존 ZIP 보존. 단순 version bump만을 위한 무의미한 변경 금지.
2. 완료 감지 경로를 실제 확인: Windows 결과 게시 GitHub credential/actor 및 이벤트 종류, GitHub Actions `push` 발생 여부, 경로 필터, Actions 활성화, `GITHUB_TOKEN` 푸시로 인한 workflow 미발생 여부, Runner GPT API 플래그 및 기존 Telegram 알림 구분. **Claude 결과 게시 직후 Runner가 자동으로 시작될 수 있는 최소한의 실질적 변경**만 v0.2.36에 반영. 불필요한 신규 봇·엔진·스키마·모델 재시도 구현 금지. 명시적 `workflow_dispatch`나 `repository_dispatch`가 필요하면 지원·권한·중복 방지·실행 영수증을 기존 계약과 대조하고 허용된 방법으로만 사용. 단순 Issue 생성은 트리거로 간주 금지.
3. 관련 단위·회귀·Windows 호스트 시험. 결과 게시 → GitHub Runner 실제 Run ID 생성/로그 → offline 검증을 새 완료 이벤트로 확인. GPT API 호출은 유효한 별도 권한·플래그가 확인될 때만; API OFF이면 `GPT_DISPOSITION=NOT_RUN`으로 명시, Runner 감지 PASS와 혼동 금지. Telegram은 기존 설정/승인 범위 내에서만 검증. 이미 실행된 Run이 있으면 재트리거 금지.
4. v0.2.36 후보 ZIP을 기존 명명 규칙으로 생성. SHA256/크기/CRC/매니페스트/경로 탈출/민감정보 검증. 실제 새 ZIP과 manifest 원본이 없으면 `FORMAL_REQUEST=BLOCKED_SOURCE`로 종료하고 가짜 ZIP/SHA/REQUEST를 게시하지 말 것.
5. **정식 신규 독립 리뷰 1건:** 기존 `collab/ops/submit_review_request.py`와 PIN 계약으로 REQUEST+실제 ZIP Commit A → SOURCE_PIN Commit B, 각각 원격 바이트 확인. 공개 ZIP 게시 허용 범위는 이전 사용자 승인에서 **v0.2.35의 정확 SHA 한 건만**이었음. v0.2.36 ZIP을 PUBLIC에 게시하려면 **새 ZIP의 실제 SHA/크기와 민감정보 검증 결과를 제시하여 새 공개 승인**을 받아야 함. 별도 보호 signer/위임/승인·READY는 실제 유효 권한에서만. 승인 없으면 `REVIEW=BLOCKED_AUTH`, 모델 호출 0. 유료 리뷰 별도 유형/금액 상한 게이트 재도입 금지. 비용/영수증은 사후 기록.
6. 새 리뷰 완료 → 결과·영수증 GitHub 게시 → Actions Run/판정/알림 흐름 검증. 모델 실행·GitHub 결과 게시·Runner·GPT 판정·Telegram 각각 실제 근거 분리. 모델 호출 불확실 시 재실행 금지.
7. 결과와 CURRENT 최상단, 필요시 migration CURRENT만 갱신하여 main 게시/원격 바이트 검증. 코드 ZIP의 공개는 새 승인 전 금지.
## LIVE 경계
v0.2.35 운영 컷오버 승인으로 v0.2.36 설치 승인이 자동 확장되지 않음. 이번 목표는 신규 리뷰 이벤트 E2E 검증이며 운영 v0.2.29 보존. 실제 GitHub 경합 및 운영 설치는 별도 승인 범위/필수 게이트 확인 후 처리. 무단 LIVE/키/설정/Task/Notifier/DB 변경 금지.
## 최종 보고
변경 파일/의미 → 자체시험 PASS/FAIL/SKIP/NOT_RUN → ZIP 경로/실제 SHA/크기 → PUBLIC 승인 여부 → 정식 REQUEST/승인/READY/독립 리뷰 상태 → Runner Run ID/이벤트/결과 → GPT 판정·Telegram 상태 → 원격 commit/readback → 차단과 다음 한 동작. 독립 리뷰 완료와 GPT 판정은 분리.
