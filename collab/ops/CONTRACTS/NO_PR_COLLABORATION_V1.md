# CoWork GitHub 협업 — NO_PR 기본 계약 V1
기준일: 2026-11-10 KST
상태: PROCESS_DECISION_CONFIRMED / GITHUB_WATCHER_NOT_ACTIVE

## 사용자 결정
- GPT ↔ Windows Claude Code의 **정규 협업 절차에 GitHub Pull Request(PR)를 사용하지 않는다**.
- 기존 Dropbox의 GPT → REQUEST/READY → watcher → Claude Code → REVIEW_RESULT/RECEIPT → Telegram → GPT 판정·수정·재시험 절차를 동일하게 보존한다.
- GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`이 신규 협업 자료의 정본이며, PUBLIC `wonhwipark/L1Work`는 별도 승인된 최종 스킬 ZIP 배포 전용이다.
- PR은 코드를 병합·검토할 별도 필요가 있는 경우에만 선택적으로 허용한다. 일반 리뷰와 작업 인계에는 요구하지 않는다.

## PR 없는 실행 계약
1. GPT가 개발·시험한 후보와 승인 가능한 비밀 제외 자료를 PRIVATE 저장소의 `collab/packages/`, `collab/requests/<id>/`에 기록한다. 기존 REQUEST V1 YAML 및 실행 모드 사이드카 호환을 우선한다.
2. **Commit A**: ZIP·REQUEST·정책/지식 참조 게시 → 실제 원격 바이트·파일 크기·SHA-256·커밋 pin 확인. 모든 검증 실패는 모델 호출 0.
3. **Commit B**: 외부 신뢰 루트에 근거한 승인 서명과 커밋·파일 pin을 검증할 수 있게 준비한 뒤, READY를 마지막에 게시한다. GitHub 파일 쓰기 권한이나 READY 존재만으로 실행 승인을 추정하지 않는다.
4. Windows watcher는 PRIVATE `main`의 READY를 **발견 후보**로만 취급하며, 서명·고정된 repo ID·정책 버전 및 해시·비용·mode·ZIP·요청/커밋 SHA·중복키·실행 횟수·만료 등을 검증하고 나서만 Claude Code에 1회 전달한다.
5. Claude Code 독립 리뷰 후 `collab/reviews/`의 REVIEW_RESULT, `collab/receipts/`의 RECEIPT를 재조회/검증한다. 게시 실패 시 재게시만 허용, **모델 재호출 금지**. 중단/불확실이면 REVIEW_UNCERTAIN 상태를 봉인한다.
6. 검증된 완료만 Telegram 통지 → GPT가 지적별 수용·수정수용·거절·보류·추가정보필요를 판정 → 재시험 후 필요 시 **신규 명시적 요청**으로 재리뷰.
7. 승인된 최종 ZIP만 별도 안전 검증 및 배포 승인을 거쳐 PUBLIC L1Work에 게시한다.

## 운영 가드
- 현재 GitHub watcher는 설치/SHADOW/LIVE 검증 전 단계. **지금 이 문서를 게시해도 REQUEST/READY나 Claude 자동 실행을 일으키지 않는다.**
- 단일 ACTIVE_PROVIDER 유지. 전환 승인 전 Dropbox LIVE 유지; GitHub 경로는 개발·정적검토·승인된 읽기전용 시험까지만.
- READY 없음, 승인 서명 부재/위조, 대상 SHA 불일치, 만료·중복이면 Claude 호출 0.
- 사내 반출 금지 자료, 토큰, 서명 개인키는 PRIVATE에도 게시 금지. /AI-CONTINUITY/ 변경 금지.
- 현재 우선 결함: B-2(실제 watcher 사이드카 명칭), B-5(처리키/정책 버전), B-3(REVIEW_UNCERTAIN 봉인). 원문과 실제 코드 대조 후 수정한다.
- T01–T38 및 S01–S10 테스트는 각각 번호별 근거로 판정. 기존 41 PASS는 합성 오프라인 보고이며 Windows 재검증·GitHub 통합 PASS가 아니다.
- 현재 Claude Code의 대화형 정적 검토 결과는 사용자 요약 접수 상태. 정식 REQUEST/READY 리뷰/영수증과 구별한다.

## 다음 한 동작
Windows Claude Code가 작성한 `CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md` 원문을 **GitHub PRIVATE**의 이관 프로젝트 영역에 제출하고, GPT가 B-2/B-5/B-3 및 시험 번호별 판정을 확정한다. 원문 게시 시 민감정보·경로·자격증명 재검증. 이관 중 별도 PR 생성 금지. 승인 없이 watcher LIVE 활성화 금지.

관련 계약: `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`.