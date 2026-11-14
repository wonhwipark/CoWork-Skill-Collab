# CoWork Skill Collaboration (PRIVATE)

**협업 최신 상태·승인 범위는 각 프로젝트 CURRENT 기준.** 아래 공통 브리프에서 요청별 경로를 선택하세요.

This repository is a **private collaboration workspace**, not a deployment repository and not an approved location for restricted corporate materials.

## 새 창 시작 — 공통 맥락 한 번에 파악

**[공통 맥락 브리프 열기](collab/CONTEXT_BRIEF.md)** → 요청별 **CURRENT** → 필요한 계약·스킬 원문. 협업 운용·L1 지식 방향·관리 스킬·현재 업무를 한 파일에서 먼저 읽습니다. 자료의 현재성은 브리프 source blob과 해당 CURRENT로 확인합니다.

이 연결은 저장소 문서를 읽는 세션의 시작 경로입니다. 새 창의 자동 선조회나 ChatGPT 프로젝트 설정을 변경한 것은 아닙니다.

## 기본 대시보드 — 클릭하면 바로 열리는 HTML (GitHub Pages)

**[CoWork Executive v4 · 진행 업무 목적·상태 기본 대시보드 열기](https://wonhwipark.github.io/L1Work/cowork-dashboard/)** — **기본 확인 경로**. PC·모바일에서 업무 목적·확인 기록·남은 작업을 먼저 보고, 관심 업무만 상세 보기로 펼쳐 확인. 기술 진단은 하단에 분리.

- 공개 화면은 PRIVATE 최신 상태에서 **공개 허용목록으로 선별·검증한 상위 요약**을 자동 갱신합니다. 원문 요청·리뷰·영수증·식별자·비밀 정보는 게시하지 않습니다.
- **[PRIVATE 상세 HTML](collab/dashboard/index.html)** — 최신 GitHub 기록을 Actions로 재생성. GitHub HTML blob은 다운로드 후 브라우저에서 확인할 수 있습니다.
- [PRIVATE HTML 보존 스냅샷](collab/dashboard/snapshots/CoWork_협업흐름_STATUS_20261112.html) · [GitHub 네이티브 요약](collab/dashboard/VIEW.md)
- **자동 갱신 검증 PASS:** 프로젝트/Work 변경 → PRIVATE 상태 생성·검증 → PUBLIC `status.json` 원격 게시 → GitHub Pages 자동 배포. 페이지를 열어둔 상태에서는 **2분마다 재확인**, 탭 복귀 시 즉시 확인. [실제 단계 변경 E2E 및 실패 복구 검증](collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/AUTO_PUBLIC_HTML_REFRESH_E2E_20261113.md).
- [병렬 스킬별 Work ID 등록·자동 추적 계약](collab/dashboard/WORK_TRACKER_GUIDE.md) — l1-fix-workflow/l1-github 개별 진행 시 사용
- [대시보드 최신 작업 현황](collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md)

## Start here
- [새 창 공통 맥락 브리프 — 먼저 읽기](collab/CONTEXT_BRIEF.md)
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
- **PUBLIC [L1Work](https://github.com/wonhwipark/L1Work):** separately approved final ZIPs and an approved allowlist-filtered, auto-updated public work-status HTML dashboard, preserving existing anonymous ZIP download paths. PRIVATE collaboration files must not be published.

## Current safety status
- 최신 이관 `CURRENT.md` 기준 `ACTIVE_PROVIDER=NONE` (2026-11-12 기존 reviewer watcher Disable·Stop 보고). PRIVATE 상태 생성기의 과거 LIVE 문구는 최신 운영 근거가 아닙니다.
- PRIVATE → PUBLIC 허용 상태 요약의 자동 갱신은 E2E PASS 기록이 있습니다. 이는 리뷰 모델·Windows watcher GitHub LIVE 전환과 별개의 기능입니다. `MIGRATION_NOT_CUTOVER` 유지.
- GitHub LIVE 운영 및 Claude 독립 리뷰 완료는 미검증/`NOT_RUN`; 민감 코드·고객정보·토큰을 저장소로 반출하지 않습니다. 실제 상세 상태는 [최신 이관 CURRENT](collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md)를 우선합니다.
- GitHub branch protection and Windows reviewer GitHub authorization require separate verification before any LIVE workflow.
