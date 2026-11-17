# Windows Claude Code 독립 설계 리뷰 인계 — L1 Workspace 로컬 정본 + 웹 뷰어 안전 전환

- 일시: 2026-11-18 KST / 신규 논점, 기존 Work `L1-WORKSPACE-RAG-20261111-001` 내 후속 설계
- 저장소: **GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`**, PR 없이 게시/결과 확인
- REVIEW_KIND: `INDEPENDENT_DESIGN`; 아직 `INDEPENDENT_REVIEW=NOT_RUN`, 비용/Windows 실행/모델 호출/REQUEST/READY/서명 `NOT_RUN`.
- 입력 기준 설계: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_SAFE_TRANSITION_DESIGN_r0001_20261118_KST.md` (Git blob `14ee7fc194737ab489cb86dd5d5dd9340e13e028`, 실제 원격 readback 완료).
- 협업 규칙: `collab/CONTEXT_BRIEF.md`, 위 Work `CURRENT.md` 최신 섹션, `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md`, 현재 자동 승인·signer 정책/보호 위임은 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`와 **실제 Windows 설정·select/check 결과**에서 확인.
- 비교해야 할 기존 승인된 설계: `L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md`, `L1_WORKSPACE_KNOWLEDGE_34_SKILL_CHANGE_REVIEW_r0001_20261116_KST.md`, `GPT_MSC_DUAL_ENTRY_G0_LINK_AND_REPRO_VALIDATION_RESULT_r0001_20261118_KST.md` (모두 동일 Work 안).
- 스킬 코드 근거: 개발 ZIP Kernel v0.7.45, Workflow v1.6.72. 원문 접근 불가하면 코드 지원을 확인했다고 쓰지 말 것. 업무 Linux 설치본/회사 코드·상세 MSC·그룹 writer는 Windows 호스트에서 접근할 수 있다고 가정하지 않음.

## 0. 리뷰 요청 전에 반드시 할 일

1. 기존 Work 리뷰 결과/영수증·현재 status를 읽고 **완료된 MSC R1 설계 리뷰 재요청/재결제 금지**. 본 리뷰는 로컬-first 전환 설계라는 **별개 델타**만 대상.
2. Windows LIVE 정책/보호 위임의 실제 `max_request_usd`, `POLICY-DESIGN` 지원/실제 모델 예산, pin repo ID 타입, 원격 SOURCE_PIN/check, 현재 중복/uncertain 예약 상태를 읽기 전용 확인. 
3. **모든 정식 요청 게이트가 PASS이고 유효 승인 범위 이내일 때만** 기존 정식 REQUEST/SOURCE_PIN/서명/READY 계약을 사용해 정확히 1회 리뷰 실행. 승인·예산/서명/정책이 미확인이면 REQUEST/READY를 부분 게시하거나 인위적으로 승인 서명하지 말고, `PREFLIGHT_BLOCKED/INDEPENDENT_REVIEW=NOT_RUN`만 기록.
4. 본 HANDOFF 게시 자체는 유료 리뷰 자동 트리거가 아님. Windows 호스트 직접 실행 권한·전달 성공이 없으면 `WINDOWS_DELIVERY=NOT_VERIFIED` 보존. 비민감 문서만 검토하며 운영 설치·스킬 교체·Git/DB/Key/Task 변경은 금지.

## 1. 독립 구조·보안 리뷰 항목 R01~R22

| 번호 | 독립적으로 반례를 찾아야 할 관점 |
|---|---|
| R01 | 개인 `l1-workspace`의 Work 원장, 그룹 Knowledge 정본, 웹 파생 사이트 **3개 정본/복제본 소유**가 명확한가? |
| R02 | 기존 `work_docs_export()`가 로컬 비Git 폴더에서 동작하는 자체 시험을 실제 호스트 support로 과장하지 않았는가? |
| R03 | Workflow `docs_sync`의 등록 remote/identity/clean tree/동기화·migration preflight를 local-mode에서 무턱대고 제거하지 않는가? |
| R04 | `docs_push`의 commit/push/remote-readback과 원본 provenance를 로컬 Git+백업/해시/복원으로 대체할 경우 **동등한 실패/중복·동시성 보호**를 설계했는가? |
| R05 | Kernel export의 legacy migration, in-place 삭제/이동, Work 수 1000 limit, Evidence 최대 5 MiB 등의 기존 한계를 충분히 다루는가? |
| R06 | Kernel 원본 `LEDGER_ROOT`/Work와 `VIEWER_STAGING`의 파일 권한 분리·경로 고정/원본 무변조가 실현 가능한가? |
| R07 | 개인 `knowledge/`의 Updater 전용 content WRITE, Workflow READ_ONLY, 공통 Git writer/raw Git push 우회 차단이 전환 과정에 유지되는가? |
| R08 | HTML/SVG/Markdown에서 script/URL/데이터 반출, CSP, sandbox, search index 누출, cache/ETag를 다뤘는가? |
| R09 | 외부 origin/file:// 링크와 `published_path` 간 상대 파일명 변경, root 안내 vs 상세 Converter MD 링크 불일치가 해결 또는 HOLD 처리되는가? |
| R10 | 안전한 path 검사(절대/../encoded traversal/symlink/hardlink/casefold/NFC)와 allowlist 파일 타입/최소 공개가 충분한가? |
| R11 | 인증 없는 개인 공개·공용 LAN/SSO·동료 권한/조직 승인 없이 웹 서버 포트/SSL/방화벽을 열지 못하도록 되어 있는가? |
| R12 | private viewer / shared viewer 각각의 문서 root, 검색 인덱스, 브라우저 자산/URL 영역이 **분리**되어 있는가? |
| R13 | 개인 PC 전원·주소 변경·휴가 시 동료 URL 가용성이 분리 관리되는가? |
| R14 | Kernel-export 복사본만을 viewer에서 열람하게 하고 GitHub/원장·문서/설계 원본이 그대로 남는가? |
| R15 | 두 진입: Updater 직접/Workflow 기존 Work에서 Source Revision·Evidence/MSC와 Work ID가 보존되고 그룹 후보 단계에서 분석을 중복 호출하지 않는가? |
| R16 | Group writer 승인/CAS/readback/고정 revision과 개인 로컬 Work 역링크를 둘로 판정하고 성공 불명확 시 재게시를 금지하는가? |
| R17 | 동료가 Work 초안을 최신 그룹 정본으로 오해하지 않도록 `PREVIEW/UNVERIFIED`와 `GROUP_POSTED` 표현을 분리했는가? |
| R18 | 0/1/2단계 SHADOW → TEAM PILOT → AUTHORITY CUTOVER 각 gate에 명시적 사용자 승인과 실패 시 STOP이 있는가? |
| R19 | Git remote를 먼저 제거/수정하는 실수, diverged, dirty/untracked, 다중 host merge 중 원본 증거 손상을 막는가? |
| R20 | 오프호스트 백업·복원/암호화·비용·RPO/RTO·host 장애/리뷰 불가 상황을 local-only 구조의 전제조건으로 충분히 반영했는가? |
| R21 | 기존 서비스 REUSE/CONNECT 가능성을 확인하지 않고 MkDocs/새 DB/새 index/서비스를 필수 설치 대상으로 확정하지 않았는가? |
| R22 | 가용성·동료 접근·운영 유지비 관점에서 (A) 현재 Git SSOT+로컬 viewer, (B) local Git SSOT+offhost 백업, (C) 공용 서버 viewer 분리의 트레이드오프를 균형 평가했는가? |

## 2. 검증/운영 게이트와 심각도

- G0 설치본/로컬 Git 권한/백업/기존 Viewer·Group writer는 **업무 Linux에서만 확인**. Windows 설계 리뷰가 호스트 G0 PASS를 대체하지 않음.
- G1 합성 `work_docs_export`/중복 export, G2 경로·HTML/Markdown 링크/민감 공유 차단, G3 개인 web, G4 동료 web, G5 local authority/rollback, G6 group Knowledge E3를 **각각 독립** 판정.
- 반드시 검토할 부정시험: Legacy TL_REVIEW, legacy migration/in-place remove, 상대 URL 깨짐, staged/committed knowledge 보호 우회, root로부터의 symlink, 검색 색인 유출, HTML 공격성 script, 그룹 CAS/게시 성공 후 역링크 실패, RPO 이내 복원 실패, 2개 writer, 동료 비인가 접근, site staging 생성 중 실패.
- 인계 설계의 기술적 누락을 실제 코드 결함으로 단정하지 말고 DESIGN_DEFECT / SOURCE_EVIDENCE_GAP / HOST_G0_REQUIRED로 구분. 결함 개수 강제 금지, 근거/반례 없는 PASS·FAIL 금지.

## 3. 필요한 리뷰 결과 형식

- `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD` 중 하나와 핵심 근거. R01~R22 각 번호별 `PASS / RISK / NOT_VERIFIED / N/A`와 가장 중요한 **차단/비차단** 구분.
- 조치 후보를 `REUSE / CONNECT / 최소 EXTEND / DEFER`로 연결하고 실제 책임 스킬·정확한 현재 계약/버전/호스트 검증·호환성 시험 범위 기록.
- **안전한 최소 단계**(현재 GitHub mode 유지+개인 SHADOW)와 **최종 authority 전환**을 별도 승인·코드/회귀/위험으로 보고.
- 결과 문서는 PRIVATE main의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_DESIGN_REVIEW_RESULT_FOR_GPT_r0001_20261118_KST.md`, 실제 입력 고정/결과 커밋/원격 바이트/별도 리뷰 세션·비용 기록은 같은 폴더의 `CLAUDE_L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_DESIGN_REVIEW_EVIDENCE_r0001_20261118_KST.json`. 실제 수행하지 않으면 출력 파일을 **완료인 척 생성 금지**, 상태 메모만 남김.
- 결과 게시 실패로 모델/분석/Job을 재호출하지 않음. 기존 REQUEST/READY/리뷰·영수증·UNCERTAIN 건을 수정/삭제하지 않음. CODE/Windows LIVE/업무 Linux/그룹 Knowledge 변경 0.

## 4. Windows Claude Code에 전달할 최종 한 문장

GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_INDEPENDENT_DESIGN_REVIEW_HANDOFF_r0001_20261118_KST.md`를 읽고 본문 정책/입력 검증을 수행한 뒤, 유효 승인된 독립 리뷰 계약이 확인되는 범위에서만 리뷰 1회를 처리해줘. 승인·signer·예산·중복 확인이 막히면 REQUEST/READY를 만들지 말고 사유를 정확히 기록해줘. 실제 업무/Windows 호스트 변경 없이 리뷰 결과와 영수증만 PRIVATE `main`에 PR 없이 게시·원격 readback해줘.
