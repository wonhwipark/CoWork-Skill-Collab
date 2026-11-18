# L1 Workspace — Knowledge Updater 책임 명확화 및 웹 뷰어 UX 재논의 델타 r0004

- 작성: 2026-11-18 KST
- Work: `L1-WORKSPACE-RAG-20261111-001` (기존 Work 유지)
- 기준: [Viewer r0002](L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md), [개인 Knowledge r0003](L1_WORKSPACE_VIEWER_PERSONAL_KNOWLEDGE_TOBE_DELTA_r0003_20261118_KST.md)
- 변경 근거: 2026-11-18 사용자 후속 협의 — 개인 지식·메타정보·그룹 반영은 실제 스킬과 업무 소스 접근권을 가진 업무 GPT 주도로 설계, `l1-knowledge-updater` 전담. 사용자가 확인한 웹 뷰어 페이지의 가독성 저하를 별도 재논의 대상으로 접수.
- 성격: **책임/업무 GPT 인계 설계 보완 + UX 문제 기록**. 코드 구현·설치·그룹 게시·뷰어 UI 변경·동료 접속 승인 아님.
- 판정: `DESIGN_SCOPE_ACCEPTED_WITH_GATES`; `HOST_INSTALLED_CAPABILITIES=NOT_VERIFIED`; `VIEWER_UX_ISSUE=USER_REPORTED/OPEN`.

## 1. 기존 설계를 유지하면서 조정할 핵심

1. `l1-knowledge-updater`가 **지식 관리 기능의 단일 책임 주체**다. 기존 분석(K0~K8), 개인 Knowledge 후보(D-1~D-4) 축적·갱신·검색/탐색용 연결, 개인→그룹 분류 대조/Preview/선별 변환, 승인된 그룹 게시와 게시 후 결과 연결을 관리한다. 실제 구현 가능성과 권한은 현장 확인 전에는 확정하지 않는다.
2. **업무 GPT가 구체 설계 주체**다. 실제 설치된 Knowledge Updater·그룹 `l1sw-dev-knowledge`·`l1-fix-workflow`·`work-ledger-kernel` 및 연결된 업무 Work/Evidence의 기존 계약을 읽기 전용으로 조사하고, 메타정보/분류/저장 경로/권한을 **기존 구현을 우선 재사용하는 방식**으로 설계한다. CoWork가 새로운 메타데이터 필드·폴더 스키마·API를 선결정하지 않는다.
3. **Updater는 기존 Workspace에서 나온 이슈 분석·설계·MSC·Work/Evidence를 허용된 권한으로 읽고 후보화**한다. Workflow나 Kernel의 분석/기록 책임까지 Updater로 이관하지 않는다. 기존 Work 원본과 Evidence를 옮기거나 덮어쓰지 않고 참조한다.
4. `l1sw-dev-knowledge`는 **기존 그룹 기술 지식 정본**이다. Updater가 개인 후보의 검증된 기술 내용과 그룹에 필요한 메타정보만 기존 분류·포맷에 매핑하여 Preview를 제시하고, 유효한 승인·writer 권한 확인 후 `l1-github`를 통해 게시·readback·고정 revision/원래 Work 연결을 수행하도록 설계한다. **동시 접근 가능성은 사용자 가정이며 실측 전 미확인**이다. 자동 게시·승인 우회 금지.
5. 웹 뷰어는 **저장된 Workspace/Knowledge를 읽기 전용으로 탐색·렌더**하는 프레젠테이션 계층이다. 지식 생성·메타정보 수정·저장·그룹 게시 API를 웹 뷰어에 추가하지 않는다.

## 2. 업무 GPT 설계·현장 점검 계약

| 현장 대상 | 확인할 사실 | 산출/판정 |
|---|---|---|
| Knowledge Updater 설치본 | 현재 스킬/버전, 기존 후보·Preview·D-1~D-4·K5.8/K7/K8, 허용된 개인 Knowledge 저장·재열람 경로 | `REUSE / CONNECT / EXTEND_PROVEN_GAP / NOT_VERIFIED` |
| Workflow + Work Ledger Kernel | Work ID·이슈/분석·Evidence·source revision·decision·Coverage·저장/역링크, 기존 조회 인터페이스와 권한 | 원본 불변의 참조/연계안; 중복 원장·신규 스키마 지양 |
| 개인 Knowledge | 실제 루트·존재·writer 주체·기존 디렉터리/링크·Module→Feature→Scenario와 Procedure 교차 탐색 | 기존 구조와의 차이·변경 최소 범위; 임의 물리 경로 확정 금지 |
| 그룹 Knowledge + Git writer | 정본 분류/필수 메타정보, 상세 HLD·MSC·Issue의 기존 수용 규칙, 승인/Preview/게시/readback/충돌·복구 | **업무 GPT가 현장 계약을 보고 필요한 메타정보 매핑표 작성**; 그룹 구조 불변 |
| Workflow 쓰기 경계 | 기존 `works/`·Evidence 쓰기는 유지, `knowledge/` 직접 WRITE 차단의 실제 구현 여부 | 권한 분리 재사용 또는 검증된 최소 보호 보완 |
| 웹 뷰어 | 실 서비스 여부·URL/읽기 전용 접근 증거·사용자 관찰의 가독성 문제 및 보안/HTML 격리/검색 | 아래 UX 논의 대기 목록. 실제 화면·호스트 기동 상태는 이번 GPT가 검증한 것이 아님 |

**메타정보 설계 원칙:** 이름/필드를 미리 확정하는 대신 업무 GPT가 설치본과 그룹 정본에서 제공하는 기존 식별자·revision·Work/Evidence 연결·검증/게시 상태를 대조하여 (a) 기존 원천값 (b) 기존 연결만 필요한 값 (c) 입증된 결손 (d) 그룹 게시에 필요한 최소 필드를 분리한다. 원본 근거와 개인 진행 메타정보를 그룹에 무차별 복제하지 않는다. 미확인 실제 API/DB/필드는 `NOT_VERIFIED`로 둔다.

**업무 GPT 역할 경계:** 업무 GPT는 현장 설계·판정·지시 주체이며, 실제 파일/코드 확인 및 허용된 시험은 업무 LLM·Linux Agent/MCP의 실제 접근·권한과 근거를 통해 수행한다. 이 문서 자체가 Agent 실행이나 게시 자동화 트리거는 아니다.

## 3. 웹 뷰어 가독성 문제 — 사용자 보고, 별도 설계 논의 대기

- **관찰:** 사용자가 실제 웹 페이지를 열람했을 때 **가독성이 낮고 보기에 불편했다**고 보고. 이번 대화에 뷰어의 검증된 URL/실제 화면·구현 revision/호스트 시험 근거는 제공되지 않아, 원인을 단정하거나 HOST G0/E3를 PASS로 처리하지 않는다. 기존 문서의 `HOST_G0=NOT_VERIFIED`와 양립한다.
- **상태:** `UX_READABILITY=USER_REPORTED_ISSUE`, `UX_DISCUSSION=PENDING`, `UI_CHANGE=NOT_RUN`. 화면 재설계·HTML/CSS 수정·설치·재기동 금지.
- **후속 논의에서 평가할 영역:** 트리/Work/Knowledge 위치 찾기, 경로·제목·본문의 시각적 위계, Markdown 본문 너비·줄간격·목차/코드블록·표 스크롤, MSC HTML/SVG의 확대·레이아웃, 모바일/PC 별 사용성, 검색·필터·브레드크럼·직접 링크, 현재 페이지/선택 상태 표시, 비밀자료/읽기 전용 보호.
- **다음 UX 논의의 입력:** 가능하면 업무 호스트에서 제한 정보가 제거된 화면 예시 또는 합성 샘플, 사용 불편 사례, 우선 개선 2~3개. 기존 웹 서비스나 doc-converter 출력 문제인지 구분하고, 우선 기존 renderer/UI를 재사용하며 필요 증거가 있는 최소 수정만 제안. 이는 **요청 사항**이지 새로운 화면 구조 승인이나 의무 제출이 아니다.
- **기존 Viewer 목표 유지:** 전체 업무 트리 접근, Markdown 즉시 렌더, MSC B형 HTML/SVG 등 형식별 열람, 원본 무변조·읽기 전용, 안전한 인증/경로 보호. UX 논의가 끝나기 전까지 r0002의 기능 수락과 시각적 가독성 수락을 구분한다.

## 4. 변경 영향 및 실행 게이트

- **유지:** r0002 Viewer E0~E5/G0~G6, r0003 개인 Knowledge 범위, K0~K8/K5.8/Classification Baseline v0.9.1, `works/`·Evidence 원본과 Kernel, 기존 Group Knowledge 정본, Claude 독립 리뷰 생략(`INDEPENDENT_REVIEW=NOT_RUN`).
- **조정:** 메타정보·개인 저장/그룹 게시 상세 설계의 Owner를 **업무 GPT/Knowledge Updater**로 명시. 기존 r0003 PK-G01~G08·PK-T01~T10의 항목은 폐기하지 않고 **업무 GPT가 실제 스킬에 대조해야 하는 검토 입력**으로 재해석.
- **추가 OPEN:** 실제로 관찰한 Viewer UX 개선. 디자인 선택·우선순위는 사용자와 별도 논의. 무단 UI 변경 없음.
- **상태:** `DOC_DELTA=PREPARED_FOR_GITHUB`; `SKILL_CODE/TESTS=NOT_RUN`; `VIEWER_UI_CHANGE=NOT_RUN`; `LINUX_INSTALL/START/NETWORK_SHARE=NOT_RUN_BY_THIS_WORK`; `GROUP_KNOWLEDGE_WRITE=NOT_RUN`; `NEW_REQUEST_READY/PAID_REVIEW=NOT_RUN`.
- **승인:** 기존 유효 위임 내 READ_ONLY 실사와 설계만 진행. 신규 유료 호출·호스트 설치/설정·그룹 게시/원본 쓰기·네트워크 공개는 실제 권한·유효 승인 없으면 개별 `BLOCKED/NOT_RUN`.

## 5. 업무 GPT 인계 및 다음 한 동작

업무 GPT는 L1Work의 **기존 상세 인계서 13절(웹 실행) + 14절(개인 Knowledge)**을 유지하되, **15절 최신 사용자 역할 변경·UX 보류**를 우선 적용한다. 현장에 존재하는 자료만을 사용해 Knowledge Updater와 Workflow/Kernel/그룹 Knowledge의 읽기 전용 계약을 대조하고, 필요한 메타정보 매핑·REUSE/CONNECT/최소 EXTEND·권한/시험 Gate를 보고할 것. Viewer는 실 화면의 가독성 문제를 별도 OPEN으로만 관리하고, 사용자 UX 논의 전에는 화면을 고치지 말 것.

**다음 한 동작:** 업무 GPT의 현장 READ_ONLY 스킬·그룹 Knowledge 비교 결과를 받아 Updater 최소 설계 범위를 확정하되, 웹 뷰어 UI 변경 결정은 사용자와의 별도 UX 논의 이후로 미룬다.
