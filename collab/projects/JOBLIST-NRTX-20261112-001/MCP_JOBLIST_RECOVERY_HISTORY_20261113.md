# MCP ↔ Job-list 분석·복구 작업 히스토리 — 2026-11-13
- Work: `JOBLIST-NRTX-20261112-001`
- Repository: `wonhwipark/CoWork-Skill-Collab`; branch: `main`
- Classification: **HISTORY_AND_HANDOFF_ONLY** (문서 기록은 운영 실행·수정·승인이 아님)

## 목적
기존에 동작했던 두 개의 Linux MCP 연결 — **Run Error Fix Workflow**, **Skill-Updater** — 을 실측 기준으로 삼아, **Job-list v0.4.36**에 재사용 가능한 안전한 MCP 요청·상태·결과 조회 인터페이스가 있는지 확인한다. 부족한 경우 최소 인터페이스를 격리 환경에서만 구현·회귀시험한다. 별도로 설치 후 활성화/Registry/Runner 실패 원인을 추적한다.

## 확인된 사실과 한계
- 사용자 제공 Agent MCP 조회(2026-11-12 07:44 KST): 설치 Job-list 0.4.36 관찰, Catalog active, Registry 대상 ID 누락, Queue `DONE/SUCCESS`이지만 `run_id=null`, `worker_started_at=null`; `activate --launch` `PARTIAL_SUCCESS`; MCP `job_result_read=RESULT_UNSUPPORTED`. 전역 activation 결과가 이 Job의 원인인지는 미확정.
- 후속 사용자 제공 숫자 응답: `3 1 1 2 2 2 2 5` (Registry/Runner/조회 증상), `3 6 5 3 5` (소스 수준 원인 분석 접근 차단·원인 미확정·격리시험 미실행). 단순 숫자 보고는 함수/호스트 증거가 아님.
- **MCP 연결 누락 가능성과 설치 후 자동 활성화 실패는 서로 다른 결함 경계.** MCP Job-list 인터페이스 미구현 여부와 원인은 로컬 소스에서 아직 확인하지 못함.
- 사용자 보고: 이전 요청이 6시간 이상 끝나지 않음. 실제 어떤 Agent/프로세스가 실행됐는지·지속되는지는 **NOT_VERIFIED**. 이전 GPT의 `STOPPED / PENDING` 표현은 호스트 프로세스 종료 확인이 아니라 추가 작업 중단 선언이었음.
- 사용자 명시 요청에 따라 추가 확장을 중단했고 기존 Job 재실행·운영 설정 변경을 수행하지 않음.

## 사용자에게 제공한 원샷 MD 파일
- Filename: `MCP_JobList_Analysis_Recovery_OneShot_20261113.md`
- Document version: `r0001`, 2026-11-13 KST
- Created as a **conversation-delivered Markdown attachment** (본 GitHub 경로에 원문 자체를 게시했다고 주장하지 않음).
- Scope: Linux 로컬 Agent가 기존 두 MCP tool/entrypoint/스키마를 코드와 기록으로 비교 → Job-list MCP 연동 유무 평가 → Skill-Updater post-install/Registry/Queue/Runner/결과 조회 경계 분리 → 필요한 최소 격리 변경과 회귀시험 → 비민감 로컬 보고서 보존.
- Execution control requested in prompt: 최대 45분, 같은 조회 무한 반복 금지, 도구·권한 부족 시 해당 항목 BLOCKED 후 종료. **프롬프트의 45분 제한은 지시사항일 뿐 실제 프로세스 강제 종료 장치가 아니므로 종료 보증 아님.**
- Final feedback contract: 10개 숫자(`A~J`): 파일/명령 접근, 기존 두 MCP 비교, Job-list MCP 요청 도구, 조회, updater→activation, Registry→Runner, 첫 오류, 격리 수정, 격리시험, 후속 조치. 증거는 Linux 로컬 보고서에 남김.

## 승인 및 보존 게이트
- **호스트 실제 개발/수정/시험: NOT_RUN.** **Linux 운영 설치/활성화/기존 Job 재실행: NOT_RUN.** **독립 리뷰: NOT_RUN.**
- 운영 MCP 서버·스케줄러·Registry·Queue·DB·원본 `/home/whpark/Project/smp1900`·OpenCode Web 설정 변경 금지. 소비된 ID `JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01` 재큐잉·재활성화 금지.
- 호스트에서만 다룰 원문 소스/로그/비밀자료를 GitHub PRIVATE·PUBLIC에 올리지 말 것. PUBLIC `wonhwipark/L1Work` ZIP 변경 없음. CoWork `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE` 유지.
- 경로(사용자 확인): MCP `/home/whpark/whpark-mcp`; 프로젝트 `/home/whpark/Project/smp1900`. Skill-Updater `/home/whpark/l1sw-private-skills/skill-updater`와 Job-list `/home/whpark/l1sw-private-skills/job-list`는 설치 위치 **예상값**, 실제 호출 경로는 미확인.
- NEXT_ONE_ACTION (명시적 재개 요청이 있을 때): Linux 파일·명령 접근 가능한 로컬 Agent로 기존 두 MCP 연결을 실측 비교하고 필요한 격리 변경·시험만 수행해 숫자 A~J 및 로컬 증거를 전달. **GitHub 문서 게시만으로 Agent 자동 실행되지 않음**.

## 기존 기준
- `collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md`
- `collab/projects/JOBLIST-NRTX-20261112-001/SKILL_UPDATER_TO_JOBLIST_PATH_DIAG_20261112.md`
