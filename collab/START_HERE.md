# CoWork — GitHub 협업 진입점
기준: 2026-11-15 KST | **GitHub 단일 LIVE 전환 완료(Windows 호스트 보고·GPT 리뷰/영수증 검증)**. 이후 최신 상태는 각 프로젝트 `CURRENT.md` 최상단 우선.
성격: **고정 진입점**. 특정 Phase, 요청자 전달 대기, ZIP PASS 등 수시 상태를 이 문서에 고정하지 않는다.

## 2026-11-15 CoWork 운영 채널 최신 판정
- **현재 CoWork 독립 리뷰 운송 채널:** GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` `ACTIVE_PROVIDER=GITHUB / CUTOVER=LIVE`. Windows Claude Code 호스트 실측: `skill-collab-watcher v0.2.20`, 독립 R1 `BLOCKING=0`, B1 운영 Python crypto·B2 Notifier DB별 워터마크·B3 GitHub Watcher Task 반영, 30초 7주기+재시작 및 단일 provider 확인. 기존 Dropbox watcher는 Disabled, 이력 및 레거시 pending 1건 보존.
- **원격 GPT 정본:** [GitHub LIVE 최종 판정](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_CUTOVER_FINAL_DISPOSITION_r0001_20261115.md) 및 [최신 CURRENT](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md). 신규 리뷰는 **유효한 승인 서명과 REQUEST/READY**를 요구하고, 파일 업로드만으로 유료 모델 리뷰를 호출하지 않음. Classic PAT 사용자 확정 방식 유지.
- **범위 구분:** 이번 전환은 **실운영 호스트 보고를 GPT가 리뷰/receipt 원문으로 대조한 판정**. GPT가 Windows GUI를 직접 관찰한 것은 아님. 새 LIVE watcher로 신규 유료 리뷰 첫 수행, Telegram 실제 수신, 장기 지속가동·재로그온은 미검증. rollback은 준비 및 격리 시험 수준.
- 아래 `2026-11-12~14 ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` 서술은 **작성 당시 이력**으로 보존. 최신 상태로 다시 해석하지 말 것. 과도기 프로젝트 설정 문구의 자동 개정·동기화는 별도 절차이며, GitHub 문서 갱신 자체가 Windows 재설치/모델 호출/정책 우회는 아님.

## 신규 개선 Work — 제한적 사전 위임 자동 서명 (2026-11-15)
- [AUTO_APPROVAL CURRENT](projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md), [설계 정본](projects/COWORK-AUTO-APPROVAL-20261115-001/AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md), [Windows 개발·시험·후보 원샷](projects/COWORK-AUTO-APPROVAL-20261115-001/WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md).
- **기존 GitHub LIVE 유지.** 새 Work는 GPT REQUEST 이후 Windows signer·READY를 자동화하기 위한 **격리 개발 단계**, 순수 정책 25/25 PASS. `AUTO_SIGNING=OFF`, Windows 구현/독립 리뷰/운영 적용 NOT_RUN. 기본 흐름에 Telegram 승인 버튼 없음. 별도 위임 범위·누적 비용/실운영 설치 승인 전에 실제 유료 자동 실행 금지.
- 이전 CoWork 이관 Work의 `COMPLETE` 상태나 레거시 pending 1건을 이 개선 Work로 소급 변경·자동 디스패치하지 않는다.

## 새 창에서 먼저 읽을 한 파일

**[공통 맥락 브리프](CONTEXT_BRIEF.md)**에서 협업 운용·L1 지식·관리 스킬을 먼저 파악하고 요청별 CURRENT로 이동한다. 이 파일은 상세 정책 진입점으로 유지한다. 브리프를 이미 읽었으면 반복 조회하지 않으며 실제 작업에 필요한 계약만 추가 확인한다. 문서 연결만으로 프로젝트 설정·백그라운드 선조회를 변경하지 않음.

## 공통 용어·저장소 접근 지침

- [용어·저장소·실행 환경 표기 원칙](ops/CONTRACTS/TERMINOLOGY_AND_ACCESS_SCOPE_V1.md): 지역/망을 가르는 접두어 대신 실제 도구 이름, **GitHub PRIVATE/PUBLIC**, 작업 PC·Linux 실행 호스트, 업무용 Git 역할로 설명한다. 기존 경로·파일명·증거는 보존한다.
- 표현 변경은 회사 코드·상세 MSC·인증정보의 게시 허용이나 설치·호출·PUBLIC 배포·LIVE 전환 승인이 아니다.

## CoWork 단일 사용자 자동 리뷰 간소화 설계 (2026-11-14 / 설계 기준)

- CoWork watcher를 **사용자 1명**이 운영하고, Windows Claude Code·Watcher PC에는 **회사 L1 소스코드 접근권이 없음**. 모바일은 해당 PC 원격 조작 용도.
- 일반 CoWork 스킬 개발·독립 리뷰의 신규 설계 우선순위는 [SU-SIMPLE 간소화 규칙](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_COWORK_SINGLE_USER_SIMPLIFIED_COLLAB_RULES_r0001_20261114.md). **별도 서명자 PC, 로컬 LLM 설치, ETW·네트워크 격리 4축 입증, 새로운 복잡한 서명 계약을 기본 필수 조건으로 요구하지 않음.** 기존 독립 Claude 리뷰 재사용과 원샷 협업 우선.
- 이는 `REVIEW_TRANSPORT_V1`의 **운영 중 적용된 승인/검사 구현을 자동 해제하는 계약이 아님**. 실제 서명·요청 전송 규칙 변경이나 LIVE 전환은 별도 사용자 승인/host 검증 후. CoWork 코드의 외부 리뷰 전송 허용 범위도 확인 전에는 확대 금지.
- 사용자/모델이 새 작업을 인계할 때는 단일 사용자 SU-SIMPLE 최신 `CURRENT.md`를 먼저 보고 과거 LOCAL_ONLY/별도 서명자 PC의 **설계 가정**을 현재 필수 승인 게이트라고 반복 요구하지 않음.
- 회사 업무 코드/고객자료·비밀은 GitHub PRIVATE/PUBLIC 게시 금지. PUBLIC 최종 ZIP은 `L1Work/main` 루트, 업무용 GPT/Agent Handoff 프롬프트 MD는 `L1Work/main/handoffs/`로 구분.
- 2026-11-14 당시 상태 `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`. 이 참고 추가는 Windows 시스템에 어떠한 변경·코드 업로드·모델 리뷰 요청도 실행하지 않음.

## GitHub 링크 기반 독립 리뷰 자료 전달 — 사용자 승인 (2026-11-14)

- 사용자 승인: **CoWork 감시기 자체 소스·후보 ZIP**은 회사 L1 코드·고객자료·토큰을 제외하고 **CoWork PRIVATE**에 리뷰용 게시 가능. **L1Work PUBLIC에 이미 게시된 스킬 ZIP과 `handoffs/` MD**는 실제 GitHub 파일 링크를 Claude 독립 리뷰에 제공 가능. 사용자 지시한 링크 기반 전달 절차는 [상세 계약](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LINK_REVIEW_TRANSPORT_APPROVAL_AND_ONE_SHOT_r0001_20261114.md)을 기준으로 한다.
- 별도 서명자 PC·로컬 LLM 확보는 일반 단일 사용자 CoWork 리뷰의 선행 의무가 아님. **실제 유료 리뷰 요청/READY·PUBLIC 신규 ZIP 게시·운영 watcher/LIVE 변경은 이 자료 전달 승인과 별개**. GitHub file URL이 곧 리뷰 실행 트리거가 아님.
- 기존 공개 릴리스 ZIP은 `L1Work/main` **루트**에 유지. 배포되지 않은 후보 ZIP은 **PRIVATE 리뷰용으로만** 게시. 업무 PC용 Handoff MD 최종본은 `L1Work/main/handoffs/`. PRIVATE/PUBLIC 게시 시 실제 원격 commit·bytes/sha·파일 링크 검증, 업무 호스트 설치/Job 실행은 별도 영수증 필요.
- `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`는 기존 실측 상태이며, 이 문서 추가는 Windows 실행·모델 리뷰 호출·GitHub LIVE 전환이 아님.

## 단일 최신 정본 위치
1. **프로젝트 실행 상태:** [`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) — 최상단 현재 요약·이후 새 결과/영수증을 우선한다. 끝에만 새 기록이 있는 과거 형식은 날짜·근거를 대조하며 과거 상태를 현재로 복사하지 않는다.
2. **협업 안전 계약:** `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md` (DRAFT, 실제 key/서명 세부는 최신 설계·판정을 우선).
3. **현재 설계/시험:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md`, `ACCEPTANCE_TEST_MATRIX_r0001_20261110.md`.
4. **보안 기준:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md` (설계 초안, 운영 승인/설치 아님).
5. **보존된 이력 원본:** 기존 Dropbox `/SKILL-COLLAB/`의 요청·결과·영수증·운영 규칙. GitHub에 전부 복제되지 않았음. **2026-11-12 감시기 Disable 실측 보고 후 `ACTIVE_PROVIDER=NONE`이며, 현재 상태는 프로젝트 `CURRENT.md` 최상단을 우선 확인.**

## 신규 Work/스킬별 병렬 작업 등록 (기본)

- 작업 시작 시 해당 작업의 고유 `Work ID`와 `CURRENT.md`를 확인하고, `collab/projects/<WORK_ID>/TRACKER.json`을 함께 등록·갱신한다. 서로 다른 스킬·이슈가 병렬 진행되면 개별 Work ID로 분리한다. 실제 미등록 작업을 진행 중으로 추정하지 않는다.
- **계약과 예시:** [Work Tracker V1](dashboard/WORK_TRACKER_GUIDE.md), **PRIVATE 자동 상태:** [HTML](dashboard/index.html) / [VIEW](dashboard/VIEW.md). `TRACKER.json`과 `CURRENT.md` 변경 시 GitHub PRIVATE Action만 갱신.
- **사용자 기본 대시보드:** [Executive HTML Pages](https://wonhwipark.github.io/L1Work/cowork-dashboard/) (클릭 즉시 열기). **PUBLIC 자동 게시 E2E PASS**: PRIVATE 성공 Action → 허용목록 상태 JSON → L1Work Pages 배포. 프로젝트 내 피드백·인계 문서 변경까지 실행 감지; 화면은 2분 주기 및 탭 복귀 시 최신 공개 상태 확인. 승인되지 않은 새 Work 이름은 자동 공개하지 않음. [실측 검증](projects/COWORK-GITHUB-DASHBOARD-20261111-001/AUTO_PUBLIC_HTML_REFRESH_E2E_20261113.md).
- 단계, 테스트, 리뷰, 패키징, PUBLIC 게시, Windows 호스트 적용, LIVE 전환은 서로 다른 상태. 등록된 `PASS` 문자열만으로 독립 리뷰 또는 실제 운영 완료를 인정하지 않는다.

## 역할 및 저장소
- GPT: 개발·요구정의·보안/호환성 검토·실측/자체시험·리뷰 판정·최종 정본 관리. Windows 전용 원본은 접근 허용되는 경우에만 작업 가능.
- Windows Claude Code: 독립 리뷰어가 기본이지만 필요한 로컬 개발 실행도 할 수 있음. **개발 세션 자기 시험 ≠ 독립 리뷰**. 토큰/연결 장애 시 GPT는 가능한 개발/시험/문서화를 계속하고 `INDEPENDENT_REVIEW=NOT_RUN/PENDING` 기록.
- Python watcher: 유효한 승인 서명·파일·repo ID·정책·비용·중복 확인 후 **정식 REQUEST/READY**가 있을 때만 리뷰 호출. 파일 게시 자체는 실행 신호 아님.
- PRIVATE: `wonhwipark/CoWork-Skill-Collab` — 새 협업 문서/판정/인계/영수증의 기준 저장소. 민감/반출금지 자료는 PRIVATE에도 게시 불가.
- **스킬 ZIP 전달 SSOT:** [Job-list/Skill-Updater PUBLIC 배송 계약](ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md). 작업 PC의 Skill-Updater가 받는 최종 ZIP은 **PUBLIC `wonhwipark/L1Work` `main` 루트**. PRIVATE 후보/문서 게시로 배송·실행 호스트 동작을 완료했다고 보고하지 않는다. 일반 정식 배포는 사전 게이트를 유지하되 **2026-11-15 사용자 승인된 NR Tx Job-list v0.4.38 읽기 전용 디버깅 ZIP은 계약 8절에 따라 배포 전 보안·회귀시험, 배포 후 Claude 독립 리뷰·Linux 호스트 G0/종단 검증**으로 운영한다. 사후 결함은 새 버전으로만 재발행하며 같은 ZIP/기존 소비 Job을 재사용하지 않는다.
- **Issue Analyzer 1차 PUBLIC 배포 지정:** [작업 CURRENT](projects/ISSUE-ANALYZER-20261114-001/CURRENT.md) 기준, 첫 ZIP도 PUBLIC `wonhwipark/L1Work/main` 루트에만 전달. PRIVATE ZIP으로 배송 대체 금지. v0.11.50은 로컬 패키지 검증 후보이며 GitHub ZIP 게시 `NOT_POSTED`, 전체 회귀·독립 리뷰·실호스트 검증 미완료로 구분. [전달 계약](ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md) 7절 참조.
- PUBLIC: `wonhwipark/L1Work` — 승인된 최종 ZIP 다운로드 및 **별도 사용자 승인된 공개 허용 목록 기반 HTML Pages 상태 요약**. 개발 후보/REQUEST/영수증/PRIVATE 원문은 공개 금지. Pages 기본 URL: `https://wonhwipark.github.io/L1Work/cowork-dashboard/`. 공개 범위는 `collab/dashboard/PUBLIC_PAGES_DEFAULT_POLICY.md` 참조.
- 기존 Dropbox reviewer watcher: 2026-11-12 사용자 승인으로 예약작업 Disable·Stop 완료 보고, 이력 및 로컬 백업 보존. **ACTIVE_PROVIDER=NONE**, GitHub LIVE 승인·가동 아님. 다른 updater/notifier/Bridge는 변경 승인 전 유지.

## L1 담당 모듈·이슈 분석 범위 공통 사전지식

- [L1_CHANNEL 담당 4개 모듈 및 Knowledge 분류 공통 컨텍스트](knowledge/L1_CHANNEL_MODULE_SCOPE_COMMON_r0001_20261113.md) — NR BCH(= NR L1 Channel), NR L1 Tx, LTE ChCfg, LTE L1 Tx의 **사용자 확인 담당 범위**와 Procedure(A)/Technical(B) 분류. 지식 업데이트/모듈 간 이슈 조사 시작 시 관련 범위부터 확인.
- [최신 Confluence 분류 검토표 v0.9](knowledge/references/L1_NR_LTE_Confluence_Module_Procedure_Feature_Table_v0_9_20261113_KST.md) — **P120/F95, 총215개 검토행**. 실제 ID·지원·구현·담당자 승인과 구분. [v0.7 181행 원본](knowledge/references/L1_NR_LTE_OWNER_REVIEW_CLASSIFICATION_v0_7_20261113.md)은 보존.
- [L1 지식 최신 상태](projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) · [2026-11-14 피드백 판정](projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md): r0005 유지, G0 일부 확인 보고 확보. 실제 저장·source/MSC/Evidence·게시/역링크·RAG 입력은 첫 실제 분석 후 검증하며 현재 분류/연계 설계의 완료 차단으로 취급하지 않음.
- 범위를 확인할 때 **사용자 확인 담당 영역**과 **추후 코드 검증할 세부 시나리오**를 분리하고, 다른 모듈의 실제 알고리즘까지 자동 확대하지 않는다. GitHub 게시만으로 코드 분석·Job 실행·Knowledge write는 시작되지 않음.

## 새 창·새 기능 요청: 보유 스킬부터 확인

- [개선 검토 원본](projects/COWORK-SKILL-DISCOVERY-20261112-001/NEW_CHAT_CONTEXT_BOOTSTRAP_REVIEW_r0001_20261114.md)의 최소 문서안을 적용: 공통 브리프 → 관련 CURRENT → 필요한 원문. 자동 로더/프로젝트 설정 변경과 구분.

1. [공통 맥락 브리프](CONTEXT_BRIEF.md)의 역할·요청별 경로·source blob을 확인한다.
2. 해당 CURRENT·열린 메모·새 결과/영수증을 확인하고, 요청에 관련된 [스킬 상세 목록](knowledge/SKILL_CAPABILITY_CATALOG.md)·실제 계약만 추가로 읽는다. 사용자에게 스킬명을 다시 요구하지 않는다.
3. **REUSE / CONNECT / 입증된 최소 EXTEND / DEFER·추가 확인**을 판단한다. 미확인을 기능 부재로 취급하지 않고, 첫 분석 후속을 현재 설계 누락으로 승격하지 않는다.
4. CURRENT·정책·카탈로그를 변경하면 브리프의 해당 요약·출처·확인일을 함께 갱신하거나 재확인 대상으로 표시한다.

상세: [스킬 발견·재사용 시작 절차](ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md) · [현재 보강 상태](projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md). 목록은 탐색 포인터이며 설치·호출 검증이 아니다. 사용자 확인한 18개는 패키지 정적 확인을 완료했고, 17개 SKILL 확인·skillsilent 원본 추가 확인으로 구분한다. 실제 설치·호스트 검증은 별도다. 이 연결이 ChatGPT 프로젝트 설정이나 다른 창의 문서 자동 로드를 변경하지는 않는다.

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
- 업무용 스킬·프롬프트·전달물에 협업 저장소 명칭·경로·토큰 의존성 주입 금지. 운영 신뢰키·개인키/토큰/회사 반출 금지 자료 저장소 업로드 금지.
- GitHub PR은 정규 리뷰에 불필요. `MIGRATION_NOT_CUTOVER` 유지 중 Dropbox LIVE를 종료하지 않는다.
