# CoWork — GitHub 협업 진입점
기준: 2026-11-10 KST | **MIGRATION_NOT_CUTOVER / DROPBOX_LIVE**
성격: **고정 진입점**. 특정 Phase, 요청자 전달 대기, ZIP PASS 등 수시 상태를 이 문서에 고정하지 않는다.

## 단일 최신 정본 위치
1. **프로젝트 실행 상태:** [`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) — 언제나 최신 상태가 기록된 마지막 섹션과 실측 증거를 우선한다. 오래된 이력 절의 NOT_STARTED/NOT_RUN은 당시 관찰값으로 보존.
2. **협업 안전 계약:** `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md` (DRAFT, 실제 key/서명 세부는 최신 설계·판정을 우선).
3. **현재 설계/시험:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md`, `ACCEPTANCE_TEST_MATRIX_r0001_20261110.md`.
4. **보안 기준:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md` (설계 초안, 운영 승인/설치 아님).
5. **실제 운용 원본:** 기존 Dropbox `/SKILL-COLLAB/`의 LIVE 요청·결과·영수증·운영 규칙. GitHub에 전부 복제되지 않았고, 운영 실행 기준으로 계속 살아있다.

## 역할 및 저장소
- GPT: 개발·요구정의·보안/호환성 검토·실측/자체시험·리뷰 판정·최종 정본 관리. Windows 전용 원본은 접근 허용되는 경우에만 작업 가능.
- Windows Claude Code: 독립 리뷰어가 기본이지만 필요한 로컬 개발 실행도 할 수 있음. **개발 세션 자기 시험 ≠ 독립 리뷰**. 토큰/연결 장애 시 GPT는 가능한 개발/시험/문서화를 계속하고 `INDEPENDENT_REVIEW=NOT_RUN/PENDING` 기록.
- Python watcher: 유효한 승인 서명·파일·repo ID·정책·비용·중복 확인 후 **정식 REQUEST/READY**가 있을 때만 리뷰 호출. 파일 게시 자체는 실행 신호 아님.
- PRIVATE: `wonhwipark/CoWork-Skill-Collab` — 새 협업 문서/판정/인계/영수증의 기준 저장소. 민감/반출금지 자료는 PRIVATE에도 게시 불가.
- **스킬 ZIP 전달 SSOT:** [Job-list/Skill-Updater PUBLIC 배송 계약](ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md). 실제 사내 Skill-Updater가 받는 최종 ZIP은 **PUBLIC `wonhwipark/L1Work` `main` 루트**. PRIVATE 후보/문서 게시로 배송·사내 실행을 완료했다고 보고하지 않는다. 후보·독립 리뷰·호스트·배포 게이트 미충족 시 PUBLIC 게시 BLOCKED.
- PUBLIC: `wonhwipark/L1Work` — 승인된 최종 ZIP 다운로드 및 **별도 사용자 승인된 공개 허용 목록 기반 HTML Pages 상태 요약**. 개발 후보/REQUEST/영수증/PRIVATE 원문은 공개 금지. Pages 기본 URL: `https://wonhwipark.github.io/L1Work/cowork-dashboard/`. 공개 범위는 `collab/dashboard/PUBLIC_PAGES_DEFAULT_POLICY.md` 참조.
- 기존 LIVE: Dropbox `/SKILL-COLLAB/` — **전환 명시 승인 전 운영 변경/중지하지 않는다**.

## 후속 메모·대화형 노트

- [메모 처리 지침](ops/CONTRACTS/FOLLOWUP_NOTES_V1.md): 기록·후속 확인을 요청한 비민감 메모는 PRIVATE 프로젝트 `notes/`에 저장하고 해당 `CURRENT.md`에 대기 상태·조건·다음 행동을 연결한다. 이미 승인된 프로젝트 범위에서 문서만 처리하며 파일 사본 제공으로 정본 등록을 대신하지 않는다.
- 최신 상태 확인 때 열린 메모, 관련 `*_FOR_GPT_*`·`INTERACTIVE_ADDENDUM_*`, 결과·영수증을 함께 읽고 근거별로 판정한다. 메모 게시로 기존 실행·리뷰·PUBLIC 배포·자동 감시를 시작하거나 진행 중 인계서를 대체하지 않는다.

- **실행 프롬프트 용어 기본 규칙:** [환경 중립 표현 계약](ops/CONTRACTS/EXECUTION_PROMPT_TERMINOLOGY_V1.md). CoWork 스킬·Job-list·Agent MCP 등 복사용/실행용 프롬프트에는 망·위치 구분 표현을 기본적으로 넣지 않고 역할/호스트/승인 기준으로 작성한다. 사용자의 반복 요청은 요구하지 않는다.
## 기본 원샷 흐름 (핑퐁 최소화)
사용자 실행 지시 1회 → 접근 가능한 원본/최근 변경분 확인 → 허용된 범위의 수정·재시험 반복 → 신규 후보 ZIP·SHA-256/시험 증거 → 비민감 결과 MD를 PRIVATE `main`에 **PR 없이** 직접 게시·remote readback → GPT 종합 판정. 권한/인증/모델 장애로 막힌 항목은 해당 항목만 BLOCKED/NOT_RUN으로 남기고 나머지 계속.
- 사용자에게 제공하는 실행 프롬프트는 항상 **정확한 저장소·브랜치·인계 파일 상대 경로**를 포함해야 한다.
- 외부 게시·운영 DB 수정·신뢰키/PAT 발급·유료 reviewer·LIVE/SHADOW 호스트 설치·PUBLIC 배포는 각각 별도 명시적 승인.
- REQUEST/READY 없거나 위조·만료·중복·비용 초과 시 reviewer 모델 호출 **0**. 재리뷰는 새로운 유효 요청으로만.
- GitHub PRIVATE의 결과 게시/보고서는 **Windows Claude Code 자동 실행도, GPT 백그라운드 실행도 발생시키지 않는다**.

## LIVE 전환 안전 게이트
운영 trust root/서명 실제 검증, Dropbox 기존 미정산 요청 개별 정산 또는 승인된 무손실 보존, 과거 완료 재호출 0, 제공자별 cursor/lease/단일 LIVE, notifier watermark/중복 0, 운영 DB WAL 무쓰기 백업과 마이그레이션/복원, 호스트 SHADOW, 정식 독립 리뷰/영수증, 운영 rollback 계획, 사용자 최종 명시 승인. **합성시험 및 개발 후보 PASS만으로 전환을 선언하지 않는다.**

## 금지 사항
- `/AI-CONTINUITY/` 변경 금지. 실제 Windows watcher·운영 SQLite/WAL/SHM·예약작업·Bridge/Dashboard/Telegram 구성 승인 전 변경 금지.
- 사내 전달물에 사외 협업 서비스 명칭·경로·토큰 의존성 주입 금지. 운영 신뢰키·개인키/토큰/회사 반출 금지 자료 저장소 업로드 금지.
- GitHub PR은 정규 리뷰에 불필요. `MIGRATION_NOT_CUTOVER` 유지 중 Dropbox LIVE를 종료하지 않는다.
