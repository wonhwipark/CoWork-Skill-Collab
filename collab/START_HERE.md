# CoWork — GitHub 협업 진입점
개정 기준: 2026-11-21 KST | 고정 운영 규칙·계약 진입점. CoWork 저장소 공개 상태 PUBLIC (GitHub 실조회).
프로젝트별 상태·버전·승인 대기·다음 행동은 해당 `CURRENT.md`와 결과/영수증에서 조회한다.

- 협업 provider·LIVE·운영 판정: [이관 CURRENT](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md).
- 자동 승인·서명 개선: [별도 개선 CURRENT](projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md). 이관 완료와 개선 구현·운영 적용을 같은 상태로 해석하지 않는다.
- 이전 진입점의 날짜별 상태는 Git 이력과 해당 프로젝트 결과에 보존되어 있다. 고정 진입점에 현재 실행 상태를 복사하지 않는다.

## 새 창에서 먼저 읽을 한 파일

**[공통 맥락 브리프](CONTEXT_BRIEF.md)**에서 협업 운용·L1 지식·관리 스킬을 먼저 파악하고 요청별 CURRENT로 이동한다. 이 파일은 상세 정책 진입점으로 유지한다. 브리프를 이미 읽었으면 반복 조회하지 않으며 실제 작업에 필요한 계약만 추가 확인한다. 문서 연결만으로 프로젝트 설정·백그라운드 선조회를 변경하지 않음.

- 협업 개발·독립 리뷰·전달과 L1 업무 Work→분석·Evidence→지식 후보·게시·역링크→피드백의 **단일 통합도는 브리프 상단**에 있고, 상세 정본/인계 표는 [통합 탑뷰 r0001](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_TOPVIEW_r0001_20261115_KST.md)에서 조회한다. 과거 아키텍처의 provider·그룹/개인 정책은 현행 상태로 복사하지 않음.

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

- 사용자 최신 지시로 저장소가 PUBLIC 전환됨. **CoWork 감시기 자체 소스·후보 ZIP**은 회사 L1 코드·고객자료·토큰을 제외한 허용 자료만 공개 저장소에 게시. 앞선 CoWork PRIVATE 게시 범위는 당시 이력. **L1Work PUBLIC에 이미 게시된 스킬 ZIP과 `handoffs/` MD**는 실제 GitHub 파일 링크를 Claude 독립 리뷰에 제공 가능. 사용자 지시한 링크 기반 전달 절차는 [상세 계약](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LINK_REVIEW_TRANSPORT_APPROVAL_AND_ONE_SHOT_r0001_20261114.md)을 기준으로 한다.
- 별도 서명자 PC·로컬 LLM 확보는 일반 단일 사용자 CoWork 리뷰의 선행 의무가 아님. **실제 유료 리뷰 요청/READY·PUBLIC 신규 ZIP 게시·운영 watcher/LIVE 변경은 이 자료 전달 승인과 별개**. GitHub file URL이 곧 리뷰 실행 트리거가 아님.
- 기존 공개 릴리스 ZIP은 `L1Work/main` **루트**에 유지. 배포되지 않은 후보 ZIP은 **PRIVATE 리뷰용으로만** 게시. 업무 PC용 Handoff MD 최종본은 `L1Work/main/handoffs/`. PRIVATE/PUBLIC 게시 시 실제 원격 commit·bytes/sha·파일 링크 검증, 업무 호스트 설치/Job 실행은 별도 영수증 필요.
- 위 자료 전달 승인은 2026-11-14 당시 기록이다. 당시 provider 값은 Git 이력에 보존하며 현재 상태는 이관 CURRENT에서 확인한다. 자료 전달 승인 자체는 Windows 실행·모델 리뷰 호출·LIVE 전환이 아니다.

## 단일 최신 정본 위치
1. **프로젝트 실행 상태:** [`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`](projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) — 최상단 현재 요약·이후 새 결과/영수증을 우선한다. 끝에만 새 기록이 있는 과거 형식은 날짜·근거를 대조하며 과거 상태를 현재로 복사하지 않는다.
2. **협업 안전 계약:** `collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md` (DRAFT, 실제 key/서명 세부는 최신 설계·판정을 우선).
3. **보존된 설계/시험 참고(최신 실행 기준은 CURRENT):** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md`, `ACCEPTANCE_TEST_MATRIX_r0001_20261110.md`.
4. **보안 기준:** `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md` (설계 초안, 운영 승인/설치 아님).
5. **보존된 이력 원본:** 기존 Dropbox `/SKILL-COLLAB/`의 요청·결과·영수증·운영 규칙. GitHub에 전부 복제되지 않았음. 과거 provider 기록은 현재 상태로 재사용하지 않으며 해당 CURRENT와 최신 결과/영수증을 확인한다.

## 신규 Work/스킬별 병렬 작업 등록 (기본)

**예외 없이 확인할 공통 정합성:** 같은 Viewer/스킬/패키지의 UI·Write 등 여러 개발창은 신규 Work를 분리하지 않고 동일 Work의 stream으로 추적. [병렬 개발 통합 게이트 V1](ops/CONTRACTS/PARALLEL_CHANGE_INTEGRATION_GATE_V1.md)에서 작업별 소스 고정, 변경 중복, 합본 ZIP 및 교차시험을 게시 전에 검증한다. 검사 스크립트가 모든 게시 경로에 자동 연결된 것은 아니며, 사용자가 중지한 자동 Actions는 복구하지 않음.

- 작업 시작 시 해당 작업의 고유 `Work ID`와 `CURRENT.md`를 확인하고, `collab/projects/<WORK_ID>/TRACKER.json`을 함께 등록·갱신한다. 서로 다른 스킬·이슈가 병렬 진행되면 개별 Work ID로 분리한다. 실제 미등록 작업을 진행 중으로 추정하지 않는다.
- **계약과 예시:** [Work Tracker V1](dashboard/WORK_TRACKER_GUIDE.md), **CoWork 저장소의 자동 상태:** [HTML](dashboard/index.html) / [VIEW](dashboard/VIEW.md). `TRACKER.json`과 `CURRENT.md` 변경 시 기존 상태 갱신 작업과 별도의 GPT 자동 판정 작업을 구분.
- **사용자 기본 대시보드:** [Executive HTML Pages](https://wonhwipark.github.io/L1Work/cowork-dashboard/) (클릭 즉시 열기). **PUBLIC 자동 게시 E2E PASS**: PRIVATE 성공 Action → 허용목록 상태 JSON → L1Work Pages 배포. 프로젝트 내 피드백·인계 문서 변경까지 실행 감지; 화면은 2분 주기 및 탭 복귀 시 최신 공개 상태 확인. 승인되지 않은 새 Work 이름은 자동 공개하지 않음. [실측 검증](projects/COWORK-GITHUB-DASHBOARD-20261111-001/AUTO_PUBLIC_HTML_REFRESH_E2E_20261113.md).
- 단계, 테스트, 리뷰, 패키징, PUBLIC 게시, Windows 호스트 적용, LIVE 전환은 서로 다른 상태. 등록된 `PASS` 문자열만으로 독립 리뷰 또는 실제 운영 완료를 인정하지 않는다.

## 역할 및 저장소
- GPT: 개발·요구정의·보안/호환성 검토·실측/자체시험·리뷰 판정·최종 정본 관리. Windows 전용 원본은 접근 허용되는 경우에만 작업 가능.
- Windows Claude Code: 독립 리뷰어가 기본이지만 필요한 로컬 개발 실행도 할 수 있음. **개발 세션 자기 시험 ≠ 독립 리뷰**. 토큰/연결 장애 시 GPT는 가능한 개발/시험/문서화를 계속하고 `INDEPENDENT_REVIEW=NOT_RUN/PENDING` 기록.
- Python watcher: 유효한 승인 서명·파일·repo ID·정책·비용·중복 확인 후 **정식 REQUEST/READY**가 있을 때만 리뷰 호출. 파일 게시 자체는 실행 신호 아님.
- PUBLIC: `wonhwipark/CoWork-Skill-Collab` — 협업 설계·요청·리뷰·판정·영수증의 기준 저장소. **신규 비밀·업무 제한 자료 업로드 금지**. 공개 상태 전환은 LIVE 설정·유료 GPT API 호출 승인 아님.
- **스킬 ZIP 전달 SSOT:** [Job-list/Skill-Updater PUBLIC 배송 계약](ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md). 작업 PC의 Skill-Updater가 받는 최종 ZIP은 **PUBLIC `wonhwipark/L1Work` `main` 루트**. PRIVATE 후보/문서 게시로 배송·실행 호스트 동작을 완료했다고 보고하지 않는다. 일반 정식 배포는 사전 게이트를 유지하되 **2026-11-15 사용자 승인된 NR Tx Job-list v0.4.38 읽기 전용 디버깅 ZIP은 계약 8절에 따라 배포 전 보안·회귀시험, 배포 후 Claude 독립 리뷰·Linux 호스트 G0/종단 검증**으로 운영한다. 사후 결함은 새 버전으로만 재발행하며 같은 ZIP/기존 소비 Job을 재사용하지 않는다.
- **Issue Analyzer 1차 PUBLIC 배포 지정:** [작업 CURRENT](projects/ISSUE-ANALYZER-20261114-001/CURRENT.md)와 [전달 계약](ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md) 7절 기준, 첫 ZIP도 PUBLIC `wonhwipark/L1Work/main` 루트에 전달. PRIVATE 후보를 배송 완료로 대체하지 않는다. 버전·시험·독립 리뷰·게시·호스트 상태는 해당 CURRENT에서 각각 확인한다.
- PUBLIC: `wonhwipark/L1Work` — 승인된 최종 ZIP 다운로드 및 **별도 사용자 승인된 공개 허용 목록 기반 HTML Pages 상태 요약**. 개발 후보/REQUEST/영수증/PRIVATE 원문은 공개 금지. Pages 기본 URL: `https://wonhwipark.github.io/L1Work/cowork-dashboard/`. 공개 범위는 `collab/dashboard/PUBLIC_PAGES_DEFAULT_POLICY.md` 참조.
- 기존 Dropbox reviewer watcher의 종료·보존 및 현재 provider는 이관 CURRENT와 해당 결과/영수증에서 확인한다. 다른 updater/notifier/Bridge 변경은 별도 승인 범위를 따른다.

## L1 담당 모듈·이슈 분석 범위 공통 사전지식

- [L1_CHANNEL 담당 4개 모듈 및 Knowledge 분류 공통 컨텍스트](knowledge/L1_CHANNEL_MODULE_SCOPE_COMMON_r0001_20261113.md) — NR BCH(= NR L1 Channel), NR L1 Tx, LTE ChCfg, LTE L1 Tx의 **사용자 확인 담당 범위**와 Procedure(A)/Technical(B) 분류. 지식 업데이트/모듈 간 이슈 조사 시작 시 관련 범위부터 확인.
- [최신 Confluence 분류 검토표 v0.9](knowledge/references/L1_NR_LTE_Confluence_Module_Procedure_Feature_Table_v0_9_20261113_KST.md) — **P120/F95, 총215개 검토행**. 실제 ID·지원·구현·담당자 승인과 구분. [v0.7 181행 원본](knowledge/references/L1_NR_LTE_OWNER_REVIEW_CLASSIFICATION_v0_7_20261113.md)은 보존.
- [L1 지식 CURRENT](projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md)에서 적용 설계·G0 근거·미실행 검증·다음 행동을 확인한다. [2026-11-14 피드백 판정](projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md)은 해당 시점의 근거로 보존한다. 첫 분석 후속 검증을 확인된 결함으로 바꾸거나 검증 전 완료로 승격하지 않는다.
- 범위를 확인할 때 **사용자 확인 담당 영역**과 **추후 코드 검증할 세부 시나리오**를 분리하고, 다른 모듈의 실제 알고리즘까지 자동 확대하지 않는다. GitHub 게시만으로 코드 분석·Job 실행·Knowledge write는 시작되지 않음.

## 새 창·새 기능 요청: 보유 스킬부터 확인

- [개선 검토 원본](projects/COWORK-SKILL-DISCOVERY-20261112-001/NEW_CHAT_CONTEXT_BOOTSTRAP_REVIEW_r0001_20261114.md)의 최소 문서안을 적용: 공통 브리프 → 관련 CURRENT → 필요한 원문. 자동 로더/프로젝트 설정 변경과 구분.

1. [공통 맥락 브리프](CONTEXT_BRIEF.md)의 역할·목적별 정본 경로를 확인하고 해당 CURRENT에서 현재 상태를 조회한다.
2. 해당 CURRENT·열린 메모·새 결과/영수증을 확인하고, 요청에 관련된 [스킬 상세 목록](knowledge/SKILL_CAPABILITY_CATALOG.md)·실제 계약만 추가로 읽는다. 사용자에게 스킬명을 다시 요구하지 않는다.
3. **REUSE / CONNECT / 입증된 최소 EXTEND / DEFER·추가 확인**을 판단한다. 미확인을 기능 부재로 취급하지 않고, 첫 분석 후속을 현재 설계 누락으로 승격하지 않는다.
4. 일반 진행·결과·피드백은 해당 결과/결정/notes와 CURRENT만 갱신한다. 구조·역할·정본 경로 변경 때만 브리프를, 스킬 책임·입출력·연결 계약 변경 때만 카탈로그를 수정한다. 기존 TRACKER는 해당 CURRENT의 현행 추적 필드만 맞춘다. 작업한 GPT/Agent가 게시와 원격 재조회를 확인한다.

상세: [스킬 발견·재사용 시작 절차](ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md) · [맥락 운용 CURRENT](projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md). 목록은 탐색 포인터이며 설치·호출 검증이 아니다. 과거 패키지 정적 감사는 [해당 시점의 감사 원문](projects/COWORK-SKILL-DISCOVERY-20261112-001/SKILL_18_PACKAGE_AUDIT_20261112.md)에서 확인하고 현재 설치·호스트 검증과 구분한다. 이 연결이 ChatGPT 프로젝트 설정이나 다른 창의 문서 자동 로드를 변경하지는 않는다.

## 지속 갱신·피드백·다음 창 재개

[스킬 발견·재사용 절차의 갱신 기준](ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md)을 단일 기준으로 사용한다. 공통 지도 → 관련 CURRENT·근거 → 필요한 스킬 → 결과·피드백 판정 → 같은 Work 보완 또는 정본 갱신 → 원격 확인 → 다음 창 조회로 이어간다. 문서 이력·스킬 원문·기존 실행 보호 장치는 그대로 구분한다.

## 후속 메모·대화형 노트

- **[GPT 공통 투두](GPT_TODO.md):** 전체 운용의 개선 후보·우선순위·GPT 의견·상세 문서 링크를 한곳에서 조회. 사용자의 해당 항목 실행·협업 요청 시 기존 Work/정식 REQUEST로 연결한다. 후보 상태는 목록이 정본이며 등록만으로 실제 수정·리뷰를 시작하지 않음.
- [메모 처리 지침](ops/CONTRACTS/FOLLOWUP_NOTES_V1.md): 기록·후속 확인을 요청한 비민감 메모는 PRIVATE 프로젝트 `notes/`에 저장하고 해당 `CURRENT.md`에 대기 상태·조건·다음 행동을 연결한다. 이미 승인된 프로젝트 범위에서 문서만 처리하며 파일 사본 제공으로 정본 등록을 대신하지 않는다.
- 최신 상태 확인 때 열린 메모, 관련 `*_FOR_GPT_*`·`INTERACTIVE_ADDENDUM_*`, 결과·영수증을 함께 읽고 근거별로 판정한다. 메모 게시로 기존 실행·리뷰·PUBLIC 배포·자동 감시를 시작하거나 진행 중 인계서를 대체하지 않는다.

- **실행 프롬프트 용어 기본 규칙:** [환경 중립 표현 계약](ops/CONTRACTS/EXECUTION_PROMPT_TERMINOLOGY_V1.md). CoWork 스킬·Job-list·Agent MCP 등 복사용/실행용 프롬프트에는 망·위치 구분 표현을 기본적으로 넣지 않고 역할/호스트/승인 기준으로 작성한다. 사용자의 반복 요청은 요구하지 않는다.

## SOURCE_PIN.json 필수 직렬화·검증 규칙 (2026-11-17 KST)

- `SKILL_COLLAB_SOURCE_PIN_V1` 유지. `repo_id`는 GitHub numeric repository ID를 의미하지만 **JSON 타입은 반드시 문자열**. 예: `"repo_id": "1451933830"`. Python 작성 시 `str(repo_id)`로 직렬화.
- 새 정식 REQUEST의 SOURCE_PIN 생성 시 `collab/ops/source_pin.py create --repo-id <실제 GitHub ID> --commit <검증된 Commit A>` 활용. 게시 전 `collab/ops/source_pin.py check <후보 SOURCE_PIN.json> --expected-repo-id <신뢰 루트 ID>` 검증하고 원격 readback. 기존 승인·서명·READY 생성 기능이 아니며 새 요청을 실행하지 않음.
- PRIVATE GitHub Actions는 SOURCE_PIN 전체 파일의 JSON 타입·schema·repo ID를 읽기 전용 감사. 숫자형/불일치 값은 fail-closed. 기존 REQUEST·pin·APPROVAL_SIG·READY·실행 이력을 임의 변경·소급 재큐잉하지 않음. `AUTO_SIGNING_UNCERTAIN`은 Windows 로컬 audit·상태 판정과 분리하며 포맷 보정만으로 해제되었다고 주장하지 않음.

## 기본 원샷 흐름 (핑퐁 최소화)
사용자 실행 지시 1회 → 접근 가능한 원본/최근 변경분 확인 → 허용된 범위의 수정·재시험 반복 → 신규 후보 ZIP·SHA-256/시험 증거 → 비민감 결과 MD를 PRIVATE `main`에 **PR 없이** 직접 게시·remote readback → GPT 종합 판정. 권한/인증/모델 장애로 막힌 항목은 해당 항목만 BLOCKED/NOT_RUN으로 남기고 나머지 계속.
- 사용자에게 제공하는 실행 프롬프트는 항상 **정확한 저장소·브랜치·인계 파일 상대 경로**를 포함해야 한다.
- 외부 게시·운영 DB 수정·신뢰키/PAT 발급·유료 reviewer·LIVE/SHADOW 호스트 설치·PUBLIC 배포는 각각 별도 명시적 승인.
- REQUEST/READY 없거나 위조·만료·중복·비용 초과 시 reviewer 모델 호출 **0**. 재리뷰는 새로운 유효 요청으로만.
- GitHub 결과/보고서 일반 게시 자체는 **Windows Claude Code 자동 실행 또는 GPT API 호출 승인이 아니다**. 다만 별도 승인·활성화된 Actions workflow가 검증된 리뷰 완료 파일 push를 감지하는 흐름은 Issue #2의 독립 트리거로 구분한다.

## LIVE 전환 안전 게이트
운영 trust root/서명 실제 검증, Dropbox 기존 미정산 요청 개별 정산 또는 승인된 무손실 보존, 과거 완료 재호출 0, 제공자별 cursor/lease/단일 LIVE, notifier watermark/중복 0, 운영 DB WAL 무쓰기 백업과 마이그레이션/복원, 호스트 SHADOW, 정식 독립 리뷰/영수증, 운영 rollback 계획, 사용자 최종 명시 승인. **합성시험 및 개발 후보 PASS만으로 전환을 선언하지 않는다.**

## 금지 사항
- `/AI-CONTINUITY/` 변경 금지. 실제 Windows watcher·운영 SQLite/WAL/SHM·예약작업·Bridge/Dashboard/Telegram 구성 승인 전 변경 금지.
- 업무용 스킬·프롬프트·전달물에 협업 저장소 명칭·경로·토큰 의존성 주입 금지. 운영 신뢰키·개인키/토큰/회사 반출 금지 자료 저장소 업로드 금지.
- GitHub PR은 정규 리뷰에 불필요. `MIGRATION_NOT_CUTOVER` 유지 중 Dropbox LIVE를 종료하지 않는다.
