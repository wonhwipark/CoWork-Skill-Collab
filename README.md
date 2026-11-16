# CoWork Skill Collaboration (PRIVATE)

**협업 최신 상태·승인 범위는 각 프로젝트 CURRENT 기준.** 아래 공통 브리프에서 요청별 경로를 선택하세요.

This repository is a **private collaboration workspace**, not a deployment repository and not an approved location for restricted corporate materials.

## 새 창 시작 — 공통 맥락 한 번에 파악

**[공통 맥락 브리프 열기](collab/CONTEXT_BRIEF.md)** → 요청별 **CURRENT** → 필요한 계약·스킬 원문. 브리프는 역할·정본 위치·작업 경로를 안내하고, 진행 상태는 해당 CURRENT와 최신 근거에서 확인합니다.

**[L1Work 스킬 현황 바로 확인](collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/L1WORK_PUBLIC_SKILL_RELEASE_ANALYSIS_r0001_20261117_KST.md)** — PUBLIC ZIP·관리 스킬별 역할·공개본과 개발 후보·검증 경계. [스킬 관리 CURRENT](collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md)에서 해당 작업의 최신 상태를 확인하며, 실제 PUBLIC HEAD와 비교합니다.

작업한 GPT/Agent가 결과·피드백을 기록하고 해당 CURRENT의 요약·근거 링크·다음 행동을 갱신한 뒤 PRIVATE 게시·원격 재조회까지 확인합니다. 구조·경로 변경 때만 브리프, 스킬 책임·입출력 변경 때만 카탈로그를 수정합니다. 상세 기준은 [지속 갱신·피드백 절차](collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md)를 따릅니다.

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

## 실행·게시 경계

- provider·LIVE·승인·실제 실행 상태는 [해당 이관 CURRENT](collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md)와 연결된 최신 결과/영수증에서 확인합니다. README에 상태값을 반복 복사하지 않습니다.
- 문서 게시, 독립 리뷰, PUBLIC 전달, 호스트 설치와 LIVE 변경은 각각 구분하며 관련 계약·사용자 승인 범위를 확인합니다.
- 공개 대시보드는 승인된 허용목록을 따르는 파생 요약입니다. PRIVATE의 상세 상태·리뷰·영수증과 구분합니다.
- 회사 코드·고객자료·비밀·반출 미승인 자료는 PRIVATE에도 게시하지 않습니다.
