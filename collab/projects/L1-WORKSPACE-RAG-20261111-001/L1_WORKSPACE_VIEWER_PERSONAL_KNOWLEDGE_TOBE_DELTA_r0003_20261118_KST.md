# L1 Workspace 로컬 웹 뷰어 × 개인 Knowledge 축적·탐색 TO-BE — 변경 델타 r0003

- 작성: 2026-11-18 KST
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001` (신규 Work 아님)
- 기준 Viewer: [r0002 전체 트리·형식별 렌더](L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md)
- 기준 Workspace 흐름: [L1 분석→Workspace 보존→그룹 반영 r0002](L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md)
- 변경 입력: 사용자가 제공한 **업무 GPT 협의 결과 화면 2장**. 화면의 문구를 근거로 요지를 정리했으며 원본 업무 화면/이미지 자체는 GitHub에 올리지 않음.
- 범위: 설계·업무 GPT 인계 정리. Linux 실설치·코드 변경·Git writer 전환·그룹 게시·유료 리뷰 실행 **없음**.
- 판정: `DESIGN_DELTA_RECORDED / ACCEPT_WITH_GATES / HOST_AND_SKILL_IMPLEMENTATION_NOT_VERIFIED`
- **우선 적용 규칙:** 기존 Viewer r0002의 전체 업무 콘텐츠 읽기 전용 탐색·형식별 렌더·보안 게이트는 유지. 본 r0003은 **개인 Knowledge의 축적/탐색과 Updater의 저장·그룹 게시 연계**만 추가. 두 요구를 하나의 Writer/서비스로 합치지 않음.

## 1. 화면에 명시된 핵심 합의

`l1-knowledge-updater`의 **기존 분석 기능을 유지**하면서 **개인 Knowledge 저장·관리와 그룹 Knowledge 게시 연계**를 추가한다. 기존 v1.8과 TO-BE 비교라는 업무 GPT 자료의 표현을 그대로 보존하되, *현재 Linux 설치본 버전이나 실제 구현 완료를 확인한 결과는 아님*.

| 항목 | 이전 방식(화면 기재) | TO-BE / 처리 구분 | 영향 |
|---|---|---|---|
| 개인 Knowledge | `PERSONAL_DETAILED` 후보만 분류·저장 | **D-1~D-4 DEFER**: 개인 Knowledge 후보 저장·관리 지원, 최소 `EXTEND` | Updater 개인 후보의 지속 보관·수정 관리 |
| 저장 위치 | Updater 세션 디렉터리 + Preview | 기존 업무 Linux `l1-workspace/knowledge/` 연결 `CONNECT` | 실제 절대 경로는 현장 읽기 전용 G0 확인; GitHub에 개인 호스트 경로 게시 금지 |
| 개인 탐색 | 별도 구조 미확정 | **Module → Feature → Scenario** 중심 탐색, 최소 `EXTEND` | 화면 분류 요구. 실물 폴더/파일 스키마는 기존 계약·설치본 확인 전 미확정 |
| 메타정보 | 후보·Evidence 중심 세션 산출물 | Work·Evidence·Revision·Coverage·검증·게시 상태 **연결** `CONNECT` | 기존 Work/Kernel의 참조를 사용; 중복 원장/필드 신설을 기정사실화하지 않음 |
| 그룹 포맷 | 그룹 정본 기준 직접 Preview | 개인 Knowledge를 **기존 그룹 포맷에 선별 변환** `CONNECT` → 입증된 gap만 `EXTEND` | 개인 분석·진행 메타정보 전체를 그룹에 복제하지 않음 |
| 저장 대상 | K5.8 Tier와 K7 Placement 중심 | 개인/그룹 **Target Store·작업 위치 구분** `CONNECT` | 기존 K5.8/K7 판정 논리 변경 아님 |
| Work 연계 | Workflow·Kernel 실제 호출 일부 미확인 | 기존 Work ID 재사용, Updater 검토 이력 연결 `CONNECT` | 두 진입·Work 원장 보존, 실제 API 미확인 |
| 그룹 게시 | K8 read-only GitHub Handoff | **승인 후** 기존 `l1-github` 게시·readback 연결 `CONNECT` | K8 문서만으로 게시·승인 발생하지 않음 |
| 역링크 | 기존 Kernel 계약 확인 필요 | 그룹 **고정 Revision**을 개인 Knowledge·원래 Work에 연결 `CONNECT` | 그룹→개인 역쓰기·자동 동기화와 구분 |
| Workflow 쓰기 권한 | `knowledge/` 접근 제한 미구현 | Workflow Bootstrap에서 `knowledge/` **WRITE 금지** 별도 최소 변경 | **Workflow의 개인 Work 저장까지 금지하는 뜻 아님**. Updater의 인가된 개인 Knowledge 저장과 분리 |
| K5.8 회귀 | 화면에 기존 회귀 **485개**, 통합 여부 미확인 | 기존 러너 통합 여부 확인은 **별도 품질 개선** | 수량은 사용자 제공 화면의 현황 표현, 직접 실행/검증 `NOT_RUN` |

## 2. 변경하지 않을 정본 및 사용자 결정

- 기존 **K0~K8 분석 파이프라인**, K5.5/K5.6/K5.7/K5.8, K6 대표 MSC 정책, **Classification Baseline v0.9.1** 유지.
- 기존 Work/Kernel 원장과 `works/`·Evidence 원문: 이동·삭제·덮어쓰기 금지. 변경 시 source revision·근거·판정·영수증 연결.
- 그룹 `l1sw-dev-knowledge`의 **기존 정본 구조·writer·승인 규칙** 유지. 승인된 HLD·상세설계·AS-IS MSC·기술 이슈 이력은 그룹의 검증된 정본.
- 개인 `knowledge/`는 그룹 폴더 구조를 **물리적으로 복제할 필요 없음**. 개인에서는 더 풍부한 분석·진행·Coverage·검증 상태를 보존하며, 그룹 반영 시 검증된 기술 사실과 필요한 메타정보만 선별·변환.
- 개인 탐색 기준은 **Module → Feature → Scenario**. 기존 Procedure/Feature 분석 입력 분류를 폐지한다는 뜻이 아님. Procedure는 관련 Work/Evidence 또는 검증된 교차 참조로 탐색 가능해야 하나 *구체 UI·물리 레이아웃은 G0에서 판정*.
- 이 변경의 핵심은 **개인 Knowledge를 단순 후보 분류에서 실제 축적·탐색 가능한 공간으로 확장**하는 것.

## 3. Viewer r0002 대비 정확한 영향

| Viewer r0002 요구 | 유지/보완 | 변경 방법 |
|---|---|---|
| `/workspace/` 전체 업무 트리의 읽기 전용 탐색 | 유지 | `knowledge/`가 실제 존재·권한 허용 시 함께 표시. 개인 Module/Feature/Scenario를 탐색할 수 있는 뷰를 **기존 디렉터리 탐색/링크로 우선 REUSE** |
| Markdown 열 때 HTML 렌더, 기존 B형 MSC·SVG·PDF·JSON | 유지 | Updater 저장 후보의 Markdown/MSC도 동일 뷰어 사용. 전량 정적 HTML 신규 생성 금지 |
| A 기존 안전한 Viewer 연계 vs B 격리 snapshot | 유지 | 개인 Knowledge의 갱신·정책상 열람 가능한 범위를 G0에 추가; A/B 선택은 실측 후 |
| 원본 무변조·read-only Viewer | 유지 | **Viewer service identity에는 저장 권한 없음**. Updater만 해당 승인·Writer 계약 아래 개인 Knowledge 저장 가능. 웹 URL·탐색이 WRITE 권한을 만들지 않음 |
| 조직 승인 계정의 전체 업무 콘텐츠 열람 | 보안 게이트 보완 | 개인 분석/진행 메타정보가 동료 열람 정책에 적합한지 G0 확인. 시스템 비밀/제한 정보는 하드 차단; 공유 정책이 불명확하면 E4 HOLD. Work별 개별 공개 목록을 기본 UX에 재도입하지 않음 |
| GitHub Writer/local-authority cutover(G5), 그룹 게시(G6) | 변경 없음 | Updater의 후보 저장, Viewer의 열람, 승인된 그룹 게시·readback을 **서로 다른 실행/승인 결과**로 관리 |

**비결정 사항:** 실제 개인 Knowledge 최상위 루트·물리 디렉터리 네이밍·메타데이터 스키마·저장 API/CLI·K8 publish 계약·동료 접속 정책·기존 회귀 러너의 범위는 화면만으로 확인 불가. 임의 API/DDL/권한을 생성하지 않음.

## 4. 최소 수정 설계·스킬 책임

1. **`l1-knowledge-updater` (주 변경 후보):** 기존 K0~K8 분석·분류 유지. D-1~D-4 후보를 기존 세션 Preview에서 개인 Knowledge 지속 저장으로 `CONNECT`하고, 필요한 gap만 `EXTEND`. 기존 Work ID/Evidence/Revision 상태 참조 및 개인→그룹 포맷 변환·사전 Preview·승인/게시/readback·고정 revision 연결. 개인 쓰기 인터페이스와 실제 설치본은 G0 확인 전 미검증.
2. **`work-ledger-kernel` (우선 REUSE):** 기존 Work/Evidence·source revision·고정 그룹 revision 링크 관리. 새 중복 원장/자동 그룹 writer 도입 금지. 실제 기존 API 호출 계약 확인.
3. **`l1-fix-workflow` (최소 권한 분리 후보):** 기존 `works/`·Evidence 기록 기능 보존. Bootstrap 과정에서 `knowledge/` WRITE 차단이 실제로 필요한지/기존 보호가 있는지 G0 확인 후 최소 보강. Updater 전용 인가된 개인 Knowledge 기록과 충돌 금지.
4. **`l1-github` (우선 REUSE):** 그룹 정본 승인 후 게시·revision/readback. K8 read-only Handoff와 실제 WRITE 실행 분리. 승인 전 자동 publish 금지.
5. **기존 웹 서비스·Markdown 렌더러·`doc-converter` (우선 REUSE):** 개인 `knowledge/` 디렉터리/문서 탐색·렌더·MSC 링크 표시. 신규 독립 Knowledge DB·웹 서비스·writer·sync 엔진 선제 도입 금지.
6. **그룹 `l1sw-dev-knowledge`:** 기존 정본 책임·포맷·승인 및 CAS/충돌/복구 보호 유지. 미승인 폴더 구조 전환 금지.

## 5. G0(읽기 전용) → 후보 수정 → 별도 실행 게이트

**G0에 추가로 확인할 항목** (기존 Viewer A~S·E0~E5는 재실행 없이 재사용):
- PK-G01: 실제 Linux `l1-workspace/knowledge/`의 존재·생성 주체·쓰기 owner/권한. 사용자 제공 업무 호스트 절대 경로는 **현장에서만** 확인.
- PK-G02: 현재 설치된 Updater의 `PERSONAL_DETAILED`, D-1~D-4 DEFER, Preview·candidate 산출 및 기존 저장 기능/제약.
- PK-G03: 개인 후보에서 Work ID·Evidence·Revision·Coverage·검증·그룹 게시 상태까지의 **기존 저장·링크 계약**. 새 필드는 이미 있다고 간주하지 않음.
- PK-G04: Module/Feature/Scenario 기존 분류·탐색·직접 링크와 Procedure 교차 참조의 실지원.
- PK-G05: K5.8 Tier, K7 Placement, K8 Handoff, 그룹 대상 포맷, 기존 `l1-github` 승인 게시·readback·고정 revision 경로.
- PK-G06: Workflow Bootstrap의 `knowledge/` WRITE 가능성·기존 권한 보호. `works/` 쓰기 유지 확인.
- PK-G07: Viewer가 개인 분석 메타정보·비밀·제한 자료를 노출하지 않도록 root/identity/HTML origin/cache·검색 색인 전체 경계 확인.
- PK-G08: 화면에 기재된 '기존 485개 회귀'의 실제 범위·현재 러너 통합 여부. **보고 수치≠현재 호스트 시험 결과**.

**후속 검증 케이스 (신규 계획, 전부 NOT_RUN):**
- PK-T01: 기존 분석 결과·K0~K8 불변, 입력 분류 회귀.
- PK-T02: D-1~D-4 개인 후보 저장→재열람→수정 이력 보존.
- PK-T03: 개인 Module→Feature→Scenario 탐색·직접 링크, Procedure 연결.
- PK-T04: Work/Evidence 원문 SHA 불변, 동일 Work ID·Revision/Coverage 링크.
- PK-T05: 개인 후보→기존 그룹 포맷 Preview·선별 변환, 기존 그룹 폴더 구조 불변.
- PK-T06: 미승인 K8에서 그룹 WRITE=0; 승인된 경로에서만 l1-github 게시·readback·고정 revision 역링크.
- PK-T07: Workflow Bootstrap의 `knowledge/` WRITE 거부와 `works/` 기존 기록 기능 동시 보존.
- PK-T08: 웹 Viewer 원본 무변조·검색/링크 갱신·Markdown/MSC 가독성.
- PK-T09: 개인 정보/비밀·root traversal·HTML active content·캐시·동료 열람 정책의 부정시험.
- PK-T10: 기존 K5.8 회귀 러너 통합 여부·기존 테스트 불변 검증.

**실행 승인 경계:** 설계 게시와 G0 READ_ONLY는 호스트 코드 수정·스킬 설치·원본 파일 저장·유료 Job·서비스 기동·업무망 공개·그룹 Knowledge WRITE·Git writer 전환의 승인이 아님. 기존 유효 위임 확인 후 해당 범위의 시험만 실행. 부족한 승인 단계는 `BLOCKED/NOT_RUN`.

## 6. 업무 GPT에 넘길 변경 지시(비민감 요약)

기존 `L1Work/main/handoffs/L1_WORKSPACE_LOCAL_VIEWER_R0002_BUSINESS_GPT_DETAILED_REVIEW_AND_G0_HANDOFF_r0001_20261118_KST.md`의 **13절 웹 Viewer E0~E5**는 유지한다. 별도 **개인 Knowledge TO-BE**에 대해서는 PK-G01~G08을 현장 읽기 전용으로 검토하여 다음을 구분한다.

- 개인 Knowledge: D-1~D-4 DEFER 해소용 지속 저장·관리/Module→Feature→Scenario 탐색/풍부한 메타정보·Work/Evidence 연결.
- 그룹: 기존 포맷·정본과 K0~K8 분석 경로 보존. 승인 후 선별 변환·기존 l1-github 게시·readback·고정 Revision 역링크만.
- Viewer는 이 개인 Knowledge를 **표시만** 하며 Updater/Workflow/Kernel/Group의 Writer 권한을 상속하지 않는다.
- 실제 지원은 `REUSE / CONNECT / MINIMAL_EXTEND_GAP / NOT_VERIFIED`로 구분하고, 구현 수정 범위·현장 부정시험·롤백·필요 승인만 보고. 코드 변경·서비스 가동/공유·그룹 쓰기·리뷰 재요청은 이번 인계만으로 실행하지 않음.

**다음 한 동작:** 업무 GPT가 설치본의 기존 사실을 활용해 Viewer G0 미확인과 PK-G01~G08을 **한 번에 읽기 전용 대조**하고 개인 Knowledge 저장/탐색과 그룹 게시 연계의 최소 구현 변경·권한/시험 계획을 회신한다.
