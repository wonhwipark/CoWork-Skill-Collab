# CoWork Skill Collaboration (PRIVATE)

**State: INITIALIZED / MIGRATION_NOT_CUTOVER — 2026-11-10**

This repository is a **private collaboration workspace**, not a deployment repository and not an approved location for restricted corporate materials.

## 기본 대시보드 — 클릭하면 바로 열리는 HTML (GitHub Pages)

**[CoWork 협업 흐름·현재 STATUS 웹페이지 바로 열기](https://wonhwipark.github.io/L1Work/cowork-dashboard/)** — **기본 확인 경로**. PC·모바일 브라우저에서 즉시 HTML 화면으로 표시됩니다.

- 공개 화면은 2026-11-12 기준 PRIVATE 기록에서 선별·검증한 상위 상태 요약입니다. 원문 요청·리뷰·영수증·식별자·비밀 정보는 게시하지 않습니다.
- **[PRIVATE 상세 HTML](collab/dashboard/index.html)** — 최신 GitHub 기록을 Actions로 재생성. GitHub HTML blob은 다운로드 후 브라우저에서 확인할 수 있습니다.
- [PRIVATE HTML 보존 스냅샷](collab/dashboard/snapshots/CoWork_협업흐름_STATUS_20261112.html) · [GitHub 네이티브 요약](collab/dashboard/VIEW.md)
- **갱신 구분:** GitHub Pages는 PUBLIC HTML 변경 시 자동 배포되지만 PRIVATE 실무 데이터를 PUBLIC으로 자동 동기화하지 않습니다. 실제 상태는 공개 가능 항목 확인 후 갱신합니다.
- [대시보드 최신 작업 현황](collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md)

## Start here
- [운영 진입점](collab/START_HERE.md)
- [공통 스킬 기능 목록](collab/knowledge/SKILL_CAPABILITY_CATALOG.md) — 새 요청의 기존 기능·연결 가능성을 먼저 확인
- [새 창 스킬 발견·재사용 절차](collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md)
- [이관 현재 상태](collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md)
- [운영 기준](collab/knowledge/OPERATING_BASELINE.md)
- [GitHub 리뷰 운송 계약](collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md)
- [최종 ZIP 공개 배포 게이트](collab/ops/CONTRACTS/PUBLIC_RELEASE_GATE.md)
- [이관 Manifest](collab/inventory/MIGRATION_MANIFEST.json)
- [이관 변경 이력](docs/MIGRATION_LOG.md)
- [Windows 호스트 읽기 전용 점검 인계](collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/NEXT_WINDOWS_READONLY_HANDOFF.md)

## Repository roles
- **PRIVATE here:** non-restricted design, candidate artifacts, reviews, receipts, status and dashboard — only after explicit source classification/approval.
- **PUBLIC [L1Work](https://github.com/wonhwipark/L1Work):** separately approved final ZIPs and the explicitly approved synthetic-only dashboard HTML sample, preserving existing anonymous ZIP download paths. PRIVATE collaboration files must not be published.

## Current safety status
- Dropbox reviewer watcher and dashboard remain the existing LIVE system.
- GitHub reviewer transport, Claude independent review, SHADOW test, single pilot, and cutover: **NOT_RUN**.
- No executable `REQUEST/READY`, real skill ZIP, sensitive source data or authentication secrets have been migrated.
- GitHub branch protection and Windows reviewer GitHub authorization require separate verification before any LIVE workflow.
