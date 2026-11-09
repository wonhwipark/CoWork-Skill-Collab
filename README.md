# CoWork Skill Collaboration (PRIVATE)

**State: INITIALIZED / MIGRATION_NOT_CUTOVER — 2026-11-10**

This repository is a **private collaboration workspace**, not a deployment repository and not an approved location for restricted corporate materials.

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
- **PUBLIC [L1Work](https://github.com/wonhwipark/L1Work):** verified, approved final ZIPs only, preserving existing anonymous download paths.

## Current safety status
- Dropbox reviewer watcher and dashboard remain the existing LIVE system.
- GitHub reviewer transport, Claude independent review, SHADOW test, single pilot, and cutover: **NOT_RUN**.
- No executable `REQUEST/READY`, real skill ZIP, sensitive source data or authentication secrets have been migrated.
- GitHub branch protection and Windows reviewer GitHub authorization require separate verification before any LIVE workflow.
