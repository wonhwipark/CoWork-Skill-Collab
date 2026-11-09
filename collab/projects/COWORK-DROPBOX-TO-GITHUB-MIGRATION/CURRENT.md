# COWORK-DROPBOX-TO-GITHUB-MIGRATION — 현재 상태
관찰일: 2026-11-10 KST | work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION

## 현재 상태
- P0-A 대상 구조: **PRIVATE + 기존 PUBLIC** 확정.
- P1 PRIVATE 저장소 생성/ChatGPT 연결: **PASS** — `wonhwipark/CoWork-Skill-Collab`, visibility `private`, default branch `main`, GPT `pull/push/admin` 확인.
- P1 기본 운영 폴더/안내 문서: **PASS** — README/START_HERE/운영 기준/계약/빈 이관 Manifest/리뷰·영수증·요청·패키지·대시보드 자리표시자 등 14개 파일이 PRIVATE main에 존재하고 원격 readback 확인. 실제 ZIP 및 요청 데이터는 0건.
- P0-B Dropbox 인벤토리: PARTIAL. 운영규칙 r0010/r0009/r0008, 게시 가드 확인. 원본 ZIP raw SHA와 전체 항목 분류는 NOT_RUN.
- P0-C ZIP/문서 공개 적합성 검사: 합성 입력 오프라인 단위시험 18 PASS(이전 실행), 실제 운영 ZIP 샘플 E2E NOT_RUN.
- Windows watcher 실제 설치 버전/SQLite/CLI/토큰/Telegram: NOT_VERIFIED.
- GitHub transport adapter 구현/배포: NOT_RUN. 독립 Claude 리뷰: NOT_RUN.
- 실 GitHub 리뷰 파일럿/SHADOW/CUTOVER: NOT_RUN.
- PUBLIC L1Work 배포·사내 다운로드: 이번 이관 작업에서 NOT_RUN.
- Dashboard GitHub adapter/모바일: NOT_RUN.
- DEFAULT_REVIEW_MODE: SEMI_AUTO, Work AUTO_PENDING_SETUP 유지.

## 이번 단계 범위
실제 PRIVATE repo ACL 확인 및 무해한 초기 안내 문서 게시. 기존 Dropbox 요청/READY/영수증·watcher/Bridge/Dashboard/Telegram의 변경 없음. 공개 ZIP 게시 없음.

## 차단 및 승인
- Windows watcher 읽기 전용 호스트 진단 필요.
- 파일별 반출 분류/원본 ZIP 실제 bytes 및 SHA-256 필요.
- 새 GitHub watcher를 LIVE로 바꾸려면 독립 Claude 리뷰/회귀시험 및 사용자 명시 승인 필요.
- PRIVATE `main` 브랜치 보호는 아직 확인/설정되지 않았으며 자동 운영 전 보강 필요.

## 다음 한 동작
기존 Windows Claude Code 호스트에서 **읽기 전용** watcher 설치·버전·상태/인증 가능 여부를 확인하고 결과를 PRIVATE 프로젝트 문서로 제출(비밀 값/회사 소스 제외). 운영 서비스는 그대로 둔다.
