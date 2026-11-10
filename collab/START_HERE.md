# CoWork — GitHub 협업 진입점
기준일: 2026-11-10 KST | 상태: PRIVATE_REPO_BOOTSTRAPPED / MIGRATION_NOT_CUTOVER

## 위치와 역할
- PRIVATE 정본 후보: 이 저장소 `wonhwipark/CoWork-Skill-Collab`; 협업 문서·개발 후보·리뷰·영수증 전용.
- PUBLIC 배포처: `wonhwipark/L1Work`의 기존 ZIP 다운로드 경로; **승인된 최종 ZIP에 한해 별도 게시**.
- 현행 LIVE 리뷰 운송 채널은 기존 Dropbox `/SKILL-COLLAB/`. GitHub watcher는 아직 설치/활성화되지 않음.

## 협업 방식 결정
- **PR 없이 직접 GitHub PRIVATE 파일 기반 REQUEST/READY로 협업**한다. PR은 선택적 코드 검토용일 뿐 리뷰 실행 조건이 아니다.
- 정규 협업 계약: `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`. 이 문서의 게시만으로 모델 실행이 일어나지 않는다.

## 최신 구현 기준 (2026-11-10)
- 전체 설계: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md`
- 48개 수락시험: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/ACCEPTANCE_TEST_MATRIX_r0001_20261110.md`
- Windows 개발 인계: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/NEXT_WINDOWS_CLAUDE_ADAPTER_IMPLEMENTATION_HANDOFF_r0001_20261110.md`
- Claude Code 정적 리뷰 원문: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md`
- **문서 게시만 완료. GitHub watcher 구현/실행/공식 리뷰/LIVE는 완료되지 않음.**

## 현재 사용자 전달 대기 작업
- **PHASE1 통합 원샷:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/PHASE1_WINDOWS_ONE_SHOT_HANDOFF_r0001_20261110.md`
- 상태: `PREPARED_NOT_DELIVERED`. 이전 Claude Code 프롬프트도 사용자가 아직 전달하지 않았음. Windows 개발/시험/ZIP = `NOT_STARTED`.
- 사용자가 개인 Windows PC의 Claude Code 대화에서 위 MD를 읽고 전체 수행하도록 **한 번만** 요청하면 됨. GitHub 게시 자체는 PC에서 자동 실행되지 않음.
- 다른 이전 NEXT_WINDOWS_* 인계서는 역사/세부 참고이며 **새 원샷 문서가 이번 실행 지시 우선순위**.

## 순서
1. `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`에서 최신 진행상태 확인.
2. `collab/knowledge/OPERATING_BASELINE.md`와 `collab/ops/CONTRACTS/`의 안전·권한 원칙 확인.
3. 이관 대상을 `collab/inventory/MIGRATION_MANIFEST.json`에 분류하고 원본 ZIP/문서 **실제 바이트 SHA-256**와 공개 적합성 승인 이후에만 복제.
4. Windows watcher/Claude Code 원본·권한을 read-only로 확인 → 독립 리뷰와 E2E → 단일 LIVE cutover.

## 절대 금지
- 사내 반출 금지 소스·로그·고객자료·토큰은 PRIVATE GitHub에도 올리지 않음.
- 검증된 `REQUEST/READY` 없이 리뷰 모델 호출 금지; 아직 GitHub에는 READY를 게시하지 않음.
- PRIVATE ZIP을 PUBLIC으로 자동 복사하지 않음. `/AI-CONTINUITY/` 변경 금지.
- 기존 Dropbox watcher/대시보드/Telegram을 중지·교체하지 않음.
