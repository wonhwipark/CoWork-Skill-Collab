# CoWork — GitHub 협업 진입점
기준일: 2026-11-10 KST | 상태: PRIVATE_REPO_BOOTSTRAPPED / MIGRATION_NOT_CUTOVER

## 위치와 역할
- PRIVATE 정본 후보: 이 저장소 `wonhwipark/CoWork-Skill-Collab`; 협업 문서·개발 후보·리뷰·영수증 전용.
- PUBLIC 배포처: `wonhwipark/L1Work`의 기존 ZIP 다운로드 경로; **승인된 최종 ZIP에 한해 별도 게시**.
- 현행 LIVE 리뷰 운송 채널은 기존 Dropbox `/SKILL-COLLAB/`. GitHub watcher는 아직 설치/활성화되지 않음.

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
