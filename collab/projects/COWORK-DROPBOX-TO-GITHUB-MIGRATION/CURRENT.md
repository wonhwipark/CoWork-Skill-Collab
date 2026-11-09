# COWORK-DROPBOX-TO-GITHUB-MIGRATION — 현재 상태
관찰일: 2026-11-10 KST | work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION

## 현재 상태
- P0-A 대상 구조: **PRIVATE + 기존 PUBLIC** 확정.
- P1 PRIVATE 저장소 생성/ChatGPT 연결: **PASS** — `wonhwipark/CoWork-Skill-Collab`, visibility `private`, default branch `main`, GPT `pull/push/admin` 확인.
- P1 기본 운영 폴더/안내 문서: **PASS** — README/START_HERE/운영 기준/계약/빈 이관 Manifest/리뷰·영수증·요청·패키지·대시보드 자리표시자 등 16개 파일(Windows 호스트 READ_ONLY 스크립트/인계 포함)이 PRIVATE main에 존재하고 원격 readback 확인. 실제 ZIP 및 요청 데이터는 0건.
- P0-B Dropbox 인벤토리: PARTIAL. 운영규칙 r0010/r0009/r0008, 게시 가드 확인. 원본 ZIP raw SHA와 전체 항목 분류는 NOT_RUN.
- P0-C ZIP/문서 공개 적합성 검사: 합성 입력 오프라인 단위시험 18 PASS(이전 실행), 실제 운영 ZIP 샘플 E2E NOT_RUN.
- Windows watcher 실제 설치 버전/SQLite/CLI/토큰/Telegram: NOT_VERIFIED.
- GitHub transport adapter **Windows 실제 통합 구현/배포: NOT_RUN**. GPT의 보안 게이트 오프라인 후보 41 PASS는 기존 보고값이며 Windows 독립 재검증 NOT_RUN.
- Windows Claude Code **대화형 정적 검토: 수행 보고 접수** (HOST_AUDIT_STATUS: PARTIAL, B-2/B-5/B-3 결함 지적). 리뷰 원문 미입수, 정식 REQUEST/READY 독립 리뷰/영수증: NOT_RUN.
- 실 GitHub 리뷰 파일럿/SHADOW/CUTOVER: NOT_RUN.
- PUBLIC L1Work 배포·사내 다운로드: 이번 이관 작업에서 NOT_RUN.
- Dashboard GitHub adapter/모바일: NOT_RUN.
- DEFAULT_REVIEW_MODE: SEMI_AUTO, Work AUTO_PENDING_SETUP 유지.

## 2026-11-10 운영 절차 결정
- **정규 협업에서 PR을 필수 절차로 사용하지 않음.** PRIVATE main의 직접 파일 게시+Commit A/B+서명/커밋/중복 검증으로 Dropbox와 동일한 REQUEST/READY 흐름을 구현한다.
- `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`를 이 결정의 계약으로 사용한다. PR #1은 이전 설계 검토 자료로만 보존한다.
- Claude 정적 리뷰 지적 우선순위: B-2(사이드카 이름), B-5(처리키/정책), B-3(REVIEW_UNCERTAIN). T01~T38, S01~S10 시험 번호별 PASS 판정은 아직 미완료.

## 이번 단계 범위
실제 PRIVATE repo ACL 확인 및 무해한 초기 안내 문서 게시. 기존 Dropbox 요청/READY/영수증·watcher/Bridge/Dashboard/Telegram의 변경 없음. 공개 ZIP 게시 없음.

## 차단 및 승인
- Windows watcher 읽기 전용 호스트 진단 필요.
- 파일별 반출 분류/원본 ZIP 실제 bytes 및 SHA-256 필요.
- 새 GitHub watcher를 LIVE로 바꾸려면 독립 Claude 리뷰/회귀시험 및 사용자 명시 승인 필요.
- PRIVATE `main` 브랜치 보호는 아직 확인/설정되지 않았으며 자동 운영 전 보강 필요.

## 다음 한 동작
Windows Claude Code의 `CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md` 원문을 **GitHub PRIVATE 프로젝트**에 게시하여 GPT가 결함 B-2/B-5/B-3을 실제 근거로 확정하고 설계/시험 계약에 반영한다. 토큰·회사 소스는 제외한다. 운영 watcher는 그대로 둔다.
