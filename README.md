# CoWork Skill Collaboration (PRIVATE)

**State: INITIALIZED / MIGRATION_NOT_CUTOVER — 2026-11-10**

This repository is a **private collaboration workspace**, not a deployment repository and not an approved location for restricted corporate materials.

## 대시보드 바로가기

- **[CoWork 협업 흐름·최신 STATUS 대시보드 (PRIVATE)](collab/dashboard/VIEW.md)** — GitHub에서 도식(Mermaid)·실행 주체·운영 상태·리뷰/피드백 확인
- **[CoWork 공개 샘플 대시보드 (웹페이지)](https://wonhwipark.github.io/L1Work/cowork-dashboard/)** — 브라우저에서 HTML 직접 보기, 실제 업무 데이터 없는 샘플
- [대시보드 최신 작업 현황](collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md) — 개발·검증·공개 현황

## Start here
- [운영 진입점](collab/START_HERE.md)
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
