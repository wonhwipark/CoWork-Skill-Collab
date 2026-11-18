# L1 Workspace r0004 · Knowledge 책임 및 Viewer UX 델타 — Windows Claude Code 독립 설계 리뷰 입력 r0001
- Work: `L1-WORKSPACE-RAG-20261111-001`; 작성 2026-11-19 KST; PRIVATE `wonhwipark/CoWork-Skill-Collab/main`.
- **기존 완료 리뷰 재사용:** `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118` rev1은 REQUEST/APPROVAL_SIG/READY/REVIEW_RESULT/RECEIPT를 실제 조회했고, Claude `ACCEPT_WITH_CHANGE` 및 receipt `ok=true`. 구 r0002 설계 재실행·재과금 금지. 아래는 기존 입력에 없던 **신규 델타**만 별도 리뷰 후보.
- **새 리뷰 요청 범위:** ① `L1_WORKSPACE_KNOWLEDGE_UPDATER_OWNERSHIP_AND_VIEWER_UX_DELTA_r0004_20261118_KST.md`의 Updater 관리 책임·업무 GPT 현장 메타정보 설계 주체·Workflow/Kernel/Group writer 경계, ② r0003 개인 Knowledge 탐색 표시와 read-only Viewer 충돌 위험, ③ 사용자가 보고한 실제 웹 열람 가독성 저하에 대한 **현재 설계의 탐색/레이아웃 UX**. 모든 자료는 비민감 설계·합성 샘플로 제한.
- **기존 리뷰 보존:** 경로 containment B1, embedded secret screening B2, MSC active content origin B3는 별도 G2/G3 선행 필수로 유지. 같은 지적을 새로 발견한 것처럼 중복 계수하지 않으며, 신규 UX 선택으로 해당 결함이 악화되는지 점검.
- **원본 경로:** `collab/projects/L1-WORKSPACE-RAG-20261111-001/` 아래 `CURRENT.md`, `L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md`, `L1_WORKSPACE_VIEWER_PERSONAL_KNOWLEDGE_TOBE_DELTA_r0003_20261118_KST.md`, `L1_WORKSPACE_KNOWLEDGE_UPDATER_OWNERSHIP_AND_VIEWER_UX_DELTA_r0004_20261118_KST.md`.
- **리뷰용 HTML:** 이 Work의 `VIEWER_CURRENT_DESIGN_LAYOUT_REVIEW_SAMPLE_r0001_20261119_KST.html`는 설계상의 **축약 3영역 구조 예시**일 뿐 실제 Linux 호스트 화면·완전한 15KB 사용자 대화 시안과 동일 바이트가 아님. 실제 사용자가 본 운영 화면·URL·CSS/JS revision은 **NOT_VERIFIED**. 이 샘플의 외관에서 실운영 결함을 확정하지 말 것.

## 리뷰 질문 (신규 R28~R35)
| ID | 검토 질문 |
|---|---|
| R28 | Updater 단일 지식 관리 책임과 업무 GPT 메타정보 설계 / Kernel 원장 / Workflow Work 기록 / 그룹 writer의 역할 충돌·중복 저장·권한 상속 위험은? |
| R29 | 개인 Knowledge `Module→Feature→Scenario` 탐색과 Works/Evidence 폴더 트리 탐색을 혼동하지 않고, Procedure 교차 진입을 최소 UI로 표현할 수 있는가? |
| R30 | 사용자가 처음 진입한 5초 안에 **무엇을 보고 있는지, 현재 Work와 Knowledge 차이, 다음 클릭**을 구분할 수 있는 정보 구조인가? |
| R31 | 3영역(폴더/본문/정보) 구조의 문서 폭·제목/경로 위계·표/코드/목차·긴 파일명·모바일에서 구체 개선점과 회귀 위험은? |
| R32 | 6~12 participant, 장문 MSC에서 확대/접기/다중 화면·현재 단계 안내를 기존 `doc-converter` B형 뷰어와 충돌 없이 개선 가능한가? |
| R33 | 검색은 경로/제목/본문, Work vs Knowledge, 최근/상태 필터의 의미를 어떻게 최소화할 것인가? 신규 검색 DB/권한 강제 없이 가능한 경계는? |
| R34 | 개인 후보 PREVIEW/검증/그룹 게시 revision 상태는 단일 눈에 띄는 표시로 어떻게 전달하고, 미확인 값을 사실로 오인하지 않게 할 것인가? |
| R35 | 보안 B1~B3와 G0/E3, 읽기 전용 보호를 유지하면서 기존 renderer/layout REUSE→CONNECT→입증된 최소 EXTEND 순으로 우선순위를 평가하라. |

## 기대 출력 / 게이트
- R28~R35별 `PASS/RISK/BLOCKED/NOT_VERIFIED`, severity(BLOCKING/MAJOR/MINOR), 구체 근거, 변경 최소안, 테스트·접근성 검증, 미해결을 한국어 보고.
- 비교 대상은 (A) 현 3영역 탐색형 (B) 업무 중심 대시보드→문서 독서 화면의 2단계 UX (C) 현재 구조 유지+세부 가독성 개선. **최소 수정·안전성·실사용성** 기준으로 판단하고 미검증 호스트 지원을 확정 금지.
- 사용자 실제 화면 확인 전 `HOST_UI_EQUALS_SAMPLE=NO`. 리뷰는 설계 정적 검토이며 Linux 설치·URL·동료 접근·원본 수정/그룹 게시/유료 추가 실행과 다름.
- 이 문서 게시는 watcher용 REQUEST/서명/READY가 아니며 정식 리뷰 완료를 의미하지 않음.