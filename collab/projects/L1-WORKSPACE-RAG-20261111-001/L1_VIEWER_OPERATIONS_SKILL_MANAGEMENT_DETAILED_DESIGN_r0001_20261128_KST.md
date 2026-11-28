# L1 Workspace Viewer — 운영 관리 / Skill Management 상세 설계 r0001

- 작성: 2026-11-28 KST
- 기존 Work: \`L1-WORKSPACE-RAG-20261111-001\` (별도 신규 Work/엔진 생성 금지)
- 상태: **DESIGN_R0001 / STATIC_REVIEW_INPUT**, 실제 Linux 호스트·활성 Viewer·MCP 전수 G0는 미검증
- 대상: 기존 Viewer v0.5.8 개발 후보(운영 설치본으로 간주 금지), Linux 설치 스킬 현황 및 기존 상태 제공자
- 리뷰 목적: 독립 **설계 리뷰 1회**, 승인/설치/실제 모델·Job 실행/운영 구성 변경과 분리
- 원칙: 기존 개별 스킬 비통합, 기존 Viewer·Kernel·Job-list·Skill Updater·MCP 중복 구현 금지, Read Only 우선, 민감 원본 외부 게시 금지

## 0. 최종 결정 사항과 비목표

사용자의 요구는 기존 L1 Workspace Viewer **운영 관리 영역 내부**에서 업무 Linux LLM 스킬들을 통합 열람하는 것. 최상위 Work/Knowledge/Recovery/Source Map 탐색에 신규 대형 메인 탭을 남발하지 않는다. 화면을 통합하되 스킬 설치, 업데이트, 실행, 스케줄 제어, 정책 변경 기능을 Viewer로 이전하지 않는다.

**포함**: 스킬 목록/책임/설치 버전·활성 버전·공개 패키지 버전 분리, 스킬별 상태 신뢰도/마지막 확인 KST, 관련 마지막 Job/Run/영수증, Handoff·CURRENT, 근거가 허용된 경우 의존 관계, 필터 및 상세 drill-down, 누락·충돌·오류 진단과 모바일 화면.

**제외**: 새로운 스킬 레지스트리 정본, 새로운 Kernel Work/Evidence 스키마, 전역 Job 큐, Reviewer/Signer 기능, 임의 shell/SSH 실행, 현재 운영 스킬 자동 교체, LLM 추정으로 운영 상태 보정, 회사 소스/호스트 경로/토큰 외부 전송, 공개 인터넷에서 Linux 운영 데이터 제공.

## 1. 고정 근거와 검증 수준

| 기준 원본 | 확인된 사실 | 설계에 주는 제약 |
|---|---|---|
| [Viewer v0.5.8 / Analyzer v0.15.7 전달 인계](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_SOURCE_MAP_VIEWER_ANALYZER_DEVELOPMENT_DELIVERY_r0001_20261127_KST.md) | Viewer 패키지 SHA-256 \`5d7935edba33bf062d167c95f3a44c620c683c33accc9c7aadacb69561fa73de\`; \`index.html\`, \`assets/app.js\`, \`adapters/adapter.js\`, \`assets/source-map.js/.css\` 변경, Source Map 전용 route/조회 취소·stale 방지, 실제 어댑터는 미검증 | 같은 navigation/read adapter의 **검증된 실제 인터페이스**만 재사용; 화면 코드·상태 결손을 최소 분리 |
| [Viewer v0.5.7 인계](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_V057_KNOWLEDGE_SECTION_ORDER_COMPLETE_HANDOFF_r0001_20261126_KST.md) | Work/Knowledge/Recovery/MSC, 도우미·오늘의 업무·설정·편집 보호 유지 | 기존 렌더·라우팅/원문/권한/저장 계약 회귀 0 |
| [Job-list v0.4.39 배송 r0004](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_VIEWER_AUTO_UPDATE_JOBLIST_PUBLIC_RELEASE_AND_RECOVERY_HANDOFF_r0004_20261128_KST.md) | ZIP 공개 게시·SHA 확인; Linux 설치, cron 후속 실행/영수증은 **NOT_VERIFIED**. \`output/viewer_autoupdate_g0/latest_result.json\` 등은 관측 후보 | 공개 ZIP 게시를 Linux 실행 완료로 오인 금지; 기존 Job/Run/Receipt readback 우선 |
| [Job-list·MCP·Updater·Recovery 통합 인계](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_JOBLIST_KNOWLEDGE_UPDATER_RECOVERY_MCP_EXECUTION_RESULT_HANDOFF_r0001_20261128_KST.md) | MCP capability/catalog/result, Skill Updater/Job-list 설치·실행 단계 구분; 실제 action 목록은 G0 대상 | 새 실행/조회 API 명칭을 실제로 존재한다고 단언하지 않음 |
| [CoWork 스킬 카탈로그](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/knowledge/SKILL_CAPABILITY_CATALOG.md) | 18개 관리 스킬+업무 Updater 1개 역할 목록. 실제 호스트 설치 전수 아님 | 목록은 *discovery seed*이며 설치 사실의 정본 아님 |
| [통합 아키텍처 HTML](https://github.com/wonhwipark/L1Work/blob/main/handoffs/CoWork_L1_Integrated_Architecture_20261125_KST.html) | 설계 GPT / 업무 GPT / Linux Agent / Viewer 책임 경계 시각화. 11/25 시점 구조 | 참고 맥락. 해당 HTML의 과거 버전을 현재 실행본으로 오인하지 않음 |

**실측 한계:** 공개 패키지 인계의 모듈/파일·시험 결과를 확인했지만 Viewer v0.5.8 ZIP 내부의 모든 함수 시그니처 및 Linux 실제 로딩 코드·권한은 이번 설계 작업에서 직접 추출·실행 검증하지 못했다. 따라서 아래 데이터 구조/함수명은 **TO-BE 논리 계약**이며 즉시 구현 확정된 API가 아니다. G0에서 소스 및 설치본을 대조한 뒤 계약을 정식 매핑한다. 이 한계를 독립 리뷰에 숨기지 않는다.

## 2. 역할·책임·재사용 경계

| 책임 | 기존 소유자 | 이번 변경 | 절대 금지 |
|---|---|---|---|
| 스킬 탐색/메타데이터 | Linux 실제 설치/manifest, 기존 Catalog, 공개 릴리스 목록 | 조회-only aggregation, provenance | Viewer 자체 스킬 registry 정본 만들기 |
| 설치/업데이트/롤백 | \`skill-updater\` 및 승인된 OS 예약/Bootstrap | 설치 영수증·상태 **표시만** | Viewer가 updater action/cron 직접 실행 |
| Job 등록·소비·상태 | \`job-list\` / Runner / Worker / Run Catalog | 기존 Job/Run/Result 읽기 | 임의 재큐잉·retry·new job |
| Work/Evidence·revision | \`l1-fix-workflow\` / \`work-ledger-kernel\` | Work 참조/영수증 링크만 | 동일 기록 이중 writer·스키마 추가 |
| Linux API/접근제어 | 기존 Viewer backend/read adapter 또는 허용된 Linux MCP | 기존 read projection에 최소 연결 | 범용 파일 브라우저/원격 shell/새 공개 API |
| 기술 분석/MSC | Analyzer/Converter/Updater/Recovery | 기존 결과로 이동 | Viewer가 분석 재실행 또는 기술 결과 생성 |
| UI/표시 | Viewer read-only renderer/router | 운영 관리 하위 페이지, 상태/필터/상세 | Write 세션·원문 링크·Source Map route 오염 |

변경 후보 판정: Viewer 메뉴/표시 **EXTEND (UI gap)**; 설치·잡·Work·지식 원본 **REUSE**; 기존 Linux read projection에 충분한 읽기 필드가 없다면 **CONNECT**; Collector 및 신규 API **DEFER UNTIL G0 PROVEN GAP**.

## 3. 화면 IA·UX 상세

### 3.1 메뉴와 기존 UX 보존
- 기존 Viewer의 상위 정보구조(Work, Knowledge, Recovery, Source Map, 오늘의 업무, 기존 설정·업무 도우미)를 유지.
- 기존 **운영 관리** 접힘 그룹이 실제 있으면 그 내부 \`스킬 관리\` 항목 추가. 없으면 G0에서 기존 메뉴 구조·label/token·모바일 네비게이션을 조사한 뒤 **운영 관리 그룹 1개**만 신설하며 기존 메뉴를 재배치하지 않음.
- URL은 기존 Viewer router의 *실제* route naming 규칙 사용. 문서 예시 \`operations/skills\`, \`operations/skills/:id\`는 논리 경로이며 실제 설치 route 아님.
- 탭 진입 시 읽기 로딩만 시작. 다른 메뉴로 이동하거나 필터 변경 시 이전 요청 취소; 오래된 응답 덮어쓰기 금지.
- 초기 진입에는 \`전체 / 확인 필요 / 실패·차단\` 요약(숫자는 실제 증거가 있을 때만), 검색창(스킬명/별칭), 상태·담당·버전 차이 필터, 표/모바일 카드.
- 리스트 기본 열: 스킬명·역할, Linux 설치/활성 버전, 공개 릴리스 버전, 차이/검증, 마지막 상태 관측(KST), 관련 마지막 실행(유형/시간), 상세 링크.
- 상세: **개요 / 설치·버전 / 최근 실행 / 의존·인계 / 검증·근거**의 로컬 섹션. 별도 대형 상위 탭 금지.
- 본문 우측 도우미는 기본 숨김, 원문 접근은 기존 권한 검증/버튼만 사용. 버튼은 \`상태 다시 조회\` (읽기-only) 및 기존 승인된 외부 링크 열기만 제공. \`설치\`, \`재시작\`, \`재실행\`, \`승인\` 버튼 금지.
- 320~1440px, 200% zoom, 키보드 탭/포커스, 스크린리더 라벨, 표 가로 스크롤, 한 행 글자수 제한, 텍스트 상태표시(색상만 사용 금지). 스킬이 100개여도 초기 렌더링·목차 반응을 유지.

### 3.2 화면 로직 상태
\`LOADING\`, \`READY\`, \`EMPTY_VERIFIED\`, \`PARTIAL\`, \`STALE\`, \`CONFLICT\`, \`DENIED\`, \`ERROR\`를 **표시 상태**로 둔다. 개별 스킬의 실행 상태 \`RUNNING/SUCCESS/FAILED/NOT_RUN/UNKNOWN\`과 혼합하지 않는다. \`UNKNOWN\`은 정상이나 실패로 치환하지 않는다.

- 섹션별 부분 실패 시 성공한 스킬은 표시하되 stale/누락 원인을 명확히 표기.
- 현재 실행 중인 Job이 있어도 UI의 자동 refresh가 새 Job을 만들지 않는다.
- 사용자가 확인한 버전과 공개 배포 버전이 달라도 운영 이상 확정 금지(승인 롤백, staging, host 별 설치 차이 가능).

## 4. 데이터 계약 (신규 DB가 아닌 읽기 전용 VIEW MODEL 제안)

다음 스키마는 frontend/adapter 사이의 논리 모델로, Linux 원본 시스템에 해당 필드를 신규 저장하라는 뜻이 아님.

\`\`\`json
{
  "schema": "SkillManagementReadModelV1",
  "snapshot_id": "opaque-observation-id",
  "observed_at": "2026-11-28T07:00:00Z",
  "scope": {"host_alias": "authorized-alias", "viewer_tenant": "opaque"},
  "completeness": "PARTIAL",
  "skills": [{
    "skill_key": "catalog-or-installed-namespace-id",
    "display_name": "code-analyzer",
    "category": "code-analysis",
    "presence": "PRESENT",
    "installed_version": {"value": null, "state": "UNKNOWN", "evidence_ref": null},
    "active_version": {"value": null, "state": "UNKNOWN", "evidence_ref": null},
    "public_release": {"version": "v0.15.7", "channel": "development_not_for_deployment", "source_ref": "L1Work commit"},
    "last_job": null,
    "last_update_receipt": null,
    "dependencies": [],
    "handoff_refs": [],
    "last_observed_at": "2026-11-28T07:00:00Z",
    "provenance": ["inventory-source-ref"],
    "warnings": ["HOST_NOT_VERIFIED"]
  }],
  "errors": [{"source": "job-catalog", "reason": "UNAVAILABLE"}]
}
\`\`\`

**필수 불변식**:
1. 스킬 식별자는 대소문자/하이픈 정규화만으로 서로 합치지 않음. \`host_alias + actual skill namespace + installed skill identity\` 조합의 정본 키를 G0 확인; 이름 별칭은 별도 매핑과 증거 필요. 중복 ID/다중 설치 경로는 **CONFLICT**.
2. \`public_release\`, \`installed_version\`, \`active_version\`은 서로 다른 필드이며 독립 증거. \`installed\`는 디스크 존재, \`active\`는 실제 로딩/Runner 확인, \`public\`은 GitHub 게시만 뜻함.
3. \`null\`, \`UNKNOWN\`, \`NOT_RUN\`, \`DENIED\`는 서로 다른 의미. 버전 미확인 ≠ 최신 버전. 부재 확인은 범위가 완전한 목록의 탐색 증명 필요.
4. 각 상태에 \`source_kind\`, \`source_revision\`, \`observed_at\`, \`receipt_ref\` 또는 \`evidence_ref\` 중 실존하는 원본 추적 정보 연결. source가 검증 안 되면 상위 상태 신뢰도 \`UNVERIFIED\`.
5. \`snapshot_id\`는 묶음 조회 식별이고 기존 Kernel ID를 덮어쓰지 않음. 여러 시스템 관측 시각이 다르면 **mixed snapshot**과 각 원천 시각 명시; 같은 시점의 원자적 스냅샷이라고 선언하지 않음.
6. 시간은 원천의 offset-aware UTC ISO-8601로 보존, Viewer에서 KST \`YYYY-MM-DD HH:mm\` 표시. 시각이 없거나 미래/클럭 오류면 \`UNKNOWN_TIME\`; 사용자 기기 시간만으로 호스트 최신성을 확정하지 않음.
7. 버전 비교는 파싱 가능한 공통 버전 체계와 동일 배포 채널일 때만. \`0.5.8 > 0.5.7\`만으로 승인/호환/설치 권고 금지. build revision/SHA 다르면 같은 라벨이라도 conflict 후보.
8. HTML/MD/URL/에러 문자열은 텍스트 escape. 임의 URI, 로컬 절대경로, 파일 원문, access token, 사용자 계정, 민감 명령어는 출력 필터에서 제외.

### 4.1 수집·합성 우선순위
- **A Linux 실제 관측**: 설치 metadata/manifest, Loader/서비스 활성 revision, 기존 Skill Updater 설치 영수증. 접근 권한과 해당 Host ID를 확인한 경우에만 활용.
- **B 실행 영수증**: Job-list 기존 Catalog/Queue/Result, Runner run_id·job_id 연결, Update receipt는 별개로 표기. 최근 1~N건 페이징.
- **C 참조 정보**: CoWork catalog/CURRENT, 승인된 L1Work 릴리스/인계. **참조일 뿐 Linux 활성 상태 근거가 아님**.
- **D 부재/차단**: 조회 거부·지원 안 함·오래된 증거 시 \`UNKNOWN/PARTIAL\`, 절대 추정 보정하지 않음.
- 같은 속성에 복수 상충 원본이 있으면 오래된 값을 최신으로 교체할 수는 있지만 **상충 기록은 provenance/warnings에 남김**. 실제 active revision은 GitHub 최신본으로 덮지 않음.

## 5. Adapter / 데이터 경로 설계

\`\`\`text
Linux Skill manifest/installed metadata ─┐
Active loader / process receipt ─────────┤
Skill Updater approved install receipt ──┤
Job-list / Runner / Result catalog ──────┼─ [기존 승인된 READ adapter/API]
Kernel Work/Evidence read projection ────┤          │ ACL + allowlist + pagination
CoWork catalog / L1Work release metadata ┘          v
                                          [minimum SkillRead aggregation]
                                                        │ (read-only, scoped)
                                             Viewer Operations / Skills
\`\`\`

- A0: **기존 Viewer read adapter**, Linux MCP 또는 기존 서버 서비스의 실제 접근 방법을 G0 확인. 브라우저에서 Linux 경로를 직접 읽는 코드는 금지. 모바일 Agent용 MCP와 브라우저 Viewer의 경로를 같다고 가정하지 않음.
- A1: 기존 제공자의 읽기-only API로 전부 충족 시 **새 Collector/서버/API 0개**. Viewer에 최소 adapter mapping/UI만 추가.
- A2: 일부 필드 미지원이면 기존 backend의 안전한 allowlisted projection을 **최소 확장 후보**로 제시. 인증된 사용자 scope 및 동일 host identity를 확인; 기존 역할 바깥 접근 금지.
- A3: Linux Collector는 G0에서 현재 provider로 충족 불가능하다는 구체적 결손과 승인된 보안·운영 인터페이스가 확인된 경우에만 별도 상세설계/승인으로 진행. 이번 R1 범위에는 Collector 구현/배포 포함하지 않음.
- A4: 브라우저 폴링은 기존 성능/호출 계약을 준수하고 기본 수동 재조회. 자동 주기·캐시 만료값은 호스트 성능 실측 후 확정; 무한 루프/중복 요청 차단.
- A5: 읽기 실패 시 표시 페이지에서만 정직하게 \`PARTIAL/UNKNOWN\` 안내. 실패를 계기로 Job·Updater·LLM 호출 금지.

### 5.1 권한·오류 인터페이스
\`list\` / \`detail\` / \`receipts\` / \`releases\`라는 이름은 설계상 기능 구분이며 실제 endpoint 명칭 아님. 기존 endpoint가 있으면 이름을 교체해 매핑. 없으면 G0의 source-of-truth와 허용 ACL을 확인하고 추가 설계한다. 스킬 이름이 URL path의 권한 근거가 되면 안 되며, 서버가 요청 identity/tenant/host/scope 검증 후 allowlist 조회한다. 로그인하지 않은 기존 Read Only 사용자에게 민감 운영 데이터 공개 불가: 권한 없는 섹션은 \`DENIED\`로 표시, 마스킹 데이터라도 일괄 노출 금지.

## 6. 상태판정/실행 추적 알고리즘

1. 현재 사용자 권한·호스트 선택 범위를 확인. 데이터 원천별 조회 성공/시점/버전/identity를 기록.
2. 설치 스킬 목록이 완전한지 증빙 확인. 완전하지 않으면 목록 \`PARTIAL\`, 누락 스킬을 \`ABSENT\` 처리 금지.
3. 각 스킬의 실설치/활성/공개 버전 분리, 동일 라벨이더라도 digest·channel·role 비교. 실제 설치본 임의 자동 업데이트 대상에 포함하지 않음.
4. \`latest_run\`은 같은 실제 job_id/run_id/target_skill/host를 가진 영수증만 표시; queue \`DONE\`이나 등록 완료만으로 Worker 성공 승격 금지.
5. 만료된 snapshot, 권한 차단, 혼합 시각, inconsistent result, worker receipt 누락을 각기 다른 reason code로 표시.
6. 클릭 시 실제 기존 Work/Job/Evidence 원본으로 이동; 참조 ACL 재검증. 허용된 상세 증거만 노출. 원본/절대경로/raw log는 페이지에 미표시.
7. 새 공개 릴리스 감지는 참고 정보로만 갱신; 승인된 target revision, 백업/롤백 증거 없이는 "설치 필요"를 단정하지 않음.

**대표 reason_codes(표현 계약 예시):** \`HOST_NOT_VERIFIED\`, \`INVENTORY_PARTIAL\`, \`ACTIVE_UNKNOWN\`, \`MISMATCH_VERSION\`, \`DIGEST_CONFLICT\`, \`RECEIPT_MISSING\`, \`RESULT_UNSUPPORTED\`, \`STALE_OBSERVATION\`, \`ACCESS_DENIED\`, \`SOURCE_UNAVAILABLE\`. 기존 backend reason code가 있으면 매핑하며 중복 enum 도입하지 않는다.

## 7. 예외 및 공격·실패 시나리오

| 시나리오 | 올바른 대응 | 잘못된 판정 |
|---|---|---|
| 공개 ZIP 최신, Linux 활성본 옛 버전 | 두 버전 별도 표시, release channel/승인 확인 | 자동 업데이트 완료/실패 선언 |
| 설치 두 위치 동일 이름 | 충돌·원천 둘 다 노출(권한 범위), 관리자 확인 | 임의 최신 하나 채택 |
| Run Catalog DONE, Worker ID 없음 | RESULT_UNSUPPORTED 또는 UNKNOWN | SUCCESS |
| 조회 시점 상이, UI route 빠른 전환 | 이전 요청 폐기, 일관된 새 조회만 렌더 | 과거 응답이 새 화면 덮기 |
| 활성 원본 digest 변경, 레이블 동일 | SOURCE_REVISION_CONFLICT | VERIFIED |
| API/서버 일시 차단 | 섹션 DENIED/UNKNOWN, 기존 결과 유지하되 stale 표시 | 누락 0개/정상 |
| 지원되지 않는 status tool | capability 미지원 표기, 무분별한 probing 중단 | 새 API 있다고 가정 |
| 공격자가 만들어낸 스킬 이름/상세 링크/HTML | escape, allowlist, ACL 재검사, 외부 요청 안전 차단 | HTML/JS 실행/경로 탐색 |
| 공개 카탈로그에는 있으나 설치 범위 밖 | 참고 스킬 별도 분류 | 설치된 스킬로 표시 |
| 원본 업무 로그·비밀·상세 경로 존재 | 서버에서 최소 데이터만 노출, 공개 업로드 금지 | 마스킹 UI만 믿고 전송 |
| 업데이트 직후 rollback | 롤백 원인·active revision의 실제 증거 연결 | release label 높은 값 기준 정상 |

## 8. 구현 파일/범위 후보 — 실제 API는 G0 결정

| 후보 | 수정 가능 범위 | G0에 반드시 확인 |
|---|---|---|
| \`index.html\` / \`assets/app.js\` | 운영 관리 메뉴·route·view lifecycle | 기존 메뉴/route 방식·Source Map·Recovery conflict |
| 신규 \`assets/skill-management.js/.css\` 또는 기존 동일 모듈 | 상태 목록/상세/필터/시간 KST 표시 | 현재 bundle/build/CSP·표시 토큰·XSS 보안 |
| \`adapters/adapter.js\` | 기존 read provider의 snapshot normalize/ACL-preserving adapter | 실제 read interface·abort/cancel·데이터 shape |
| \`fixtures/demo-data.js\` | 합성 불일치/권한/빈 상태 fixtures | fixture가 실제 데이터와 혼합되지 않는 분기 |
| \`tests/*\` | 운영 메뉴 회귀·상태/권한/동시성 시험 | 기존 전체 테스트 목록/실행법 |
| \`README_INTEGRATED.md\`, \`VERSION\`, \`manifest.sha256\`, \`tools/build_release.py\` | **구현 때만** 버전·배포 검증·CSP | 기존 빌드·패키징 무결성 |
| 기존 Kernel/Job-list/Updater/Workspace | 원칙적 **변경 없음** | 실제 read gap 입증 전 수정 금지 |

인계·원문은 PUBLIC GitHub에 설계만 게시한다. 실제 Linux 호스트에 적용되는 코드/경로/API/스크린샷/로컬 인증 데이터는 별도 제한된 업무 영역에서 확인한다.

## 9. G0→G5 실행·승인 게이트

- **G0 실제 호스트 읽기-only 근거 확보**: Viewer active build hash, menu/router/adapter 구현, 설치 스킬 전체/범위, updater receipt, job catalog/result, MCP capability, auth/ACL. 호스트별 허용 자료만 보존.
- **G1 계약 매핑**: 기존 기능 REUSE/CONNECT/PROVEN_GAP/UNKNOWN, 실제 API명·필드·필수 권한, 대상 파일/변경량 추정. 확인 불가 시 원칙 범위를 설계 확정이 아닌 \`CONDITIONAL\`.
- **G2 설계 자체검증**: 설계 0~10절 요구 ↔ 확인 근거 ↔ 구현 변경 ↔ 수락시험 ↔ 책임자 traceability. 거짓 실행 성공·무단 UI 쓰기·민감 노출 후보를 제거.
- **G3 독립 설계 리뷰 1회**: 정적 설계 본문·테스트 표·원본 인계/카탈로그를 고정된 입력 ZIP으로 제출. 승인 서명과 READY는 보호된 기존 signer가 처리. 설계 리뷰 결과/영수증 이전에 \`COMPLETED\` 금지.
- **G4 리뷰 지적 처리**: BLOCKING/MAJOR/MINOR별 수용/조건부/거절 근거 및 설계 수정, GPT 판정. 신규 독립 리뷰를 자동 반복하지 않음.
- **G5 구현·배포(별도 단계)**: 사용자 지정 범위의 실제 개발/회귀/릴리스 게이트 이후에만 설치·운영 반영. **이번 요청으로 G5 승인된 것 아님**.

## 10. 수락시험 (리뷰가 반례까지 검토할 기준)

| ID | 시험 | 기대 결과 |
|---|---|---|
| SM-01 | 기존 메뉴/route 이동·뒤로가기 | Work/Knowledge/Recovery/Source Map/오늘 업무/도우미/설정 불변 |
| SM-02 | READ_ONLY 권한으로 운영 관리 진입 | 허용된 목록만 노출, 실행/업데이트 버튼 0 |
| SM-03 | 설치 vA, active vB, public vC | 3개 독립 표시, 최신/운영 성공 단정 금지 |
| SM-04 | 이름 중복/다중 호스트/별칭 충돌 | CONFLICT, 잘못된 merge 0 |
| SM-05 | 설치 부분 실패·catalog 404 | PARTIAL/UNKNOWN, "0개 설치" 거짓 표시 0 |
| SM-06 | LAST_RUN DONE+receipt 없음 | SUCCESS 불가, 최초 결손 표시 |
| SM-07 | Result Unsupported, UI 재조회 | unsupported 보존, 재실행/모델 호출 0 |
| SM-08 | stale/부분 응답 경쟁 100회 | 이전 응답에 의한 화면 overwrite 0 |
| SM-09 | 읽기 API cross-tenant/host ACL | 요청 거절 및 원본 경로/비밀 노출 0 |
| SM-10 | 악성 스킬명/링크/HTML | XSS·path traversal·open redirect 0 |
| SM-11 | 데이터 한 원천 지연/오류 | 페이지 일부는 유지, 문제 항목·시각·원인 표시 |
| SM-12 | 시각 UTC→KST, 미래/없음 | \`YYYY-MM-DD HH:mm\` 정확, 불명시 unknown |
| SM-13 | 공개 릴리스 후보 development | 운영 사용 승인으로 표시하지 않음 |
| SM-14 | 링크 원본 접근 DENIED/삭제 | 링크 차단/권한 재검증, 임의 fallback 금지 |
| SM-15 | 모바일 320/390px·데스크톱 1440px | 가로 overflow 제어·키보드·스크린리더 정상 |
| SM-16 | 100~500 스킬·최근 Run paging | 성능 기준 실측 기록, 무한 렌더·빈번한 풀스캔 0 |
| SM-17 | Work/Knowledge/MSC 편집 세션 회귀 | 기존 승인 편집·저장·충돌 가드 불변 |
| SM-18 | Job/Updater/Kernel spy harness | Viewer 페이지 진입/필터/재조회 중 write/execute 0 |
| SM-19 | rollback/동일 버전 다른 digest | 충돌·롤백 근거와 활성 확인 분리 |
| SM-20 | Linux 호스트 실제 스킬 2~3개 검증 | 식별/설치/활성/공개/receipt/링크 각각 실제 원본 일치 |

시험은 **설계상 수락 기준**이며 이번 문서 작성으로 실행하지 않았다. 기존 Viewer 합성 Chromium PASS나 기존 ZIP CRC PASS를 SM-01~20 전체 실측 PASS로 승격하지 않는다. PASS/FAIL/SKIP/UNKNOWN/NOT_RUN 및 증거 URL/버전/환경/실행자 구분 필수.

## 11. 정적 설계 리뷰어의 필수 판정 질문

1. v0.5.8의 실제 router/adapter 변경 내용과 이 설계가 충돌하는가? 실제 API 미확인 상태를 위험하게 확정한 곳은?
2. 운영 관리 내 UX가 기존 Work/Knowledge/Recovery/Source Map을 중복하지 않으면서 상태를 충분히 보여주는가?
3. 실설치/실활성/공개 ZIP/실행 영수증을 별개로 판정하는 데이터 모델에 누락 반례가 있는가?
4. Linux와 브라우저의 인증/ACL/외부 데이터 노출 경계를 최소 비용으로 지키는 방안은?
5. 기존 Kernel·Job-list·Skill Updater·MCP를 재사용하면서 Collector/신규 API 추가가 정말 필요한가? 불필요한 설계 범위는?
6. race/staleness, 중복 스킬, stale receipt, 실패/차단 오인, 여러 호스트/워크스페이스의 주체 혼합 위험은?
7. SM-01~20 수락시험만으로 설계 품질을 판정할 수 있는가? BLOCKING 반례와 최소 보완은?
8. **최소 구현안(A: UI+기존 read adapter 재사용)**과 입증된 결손만 확장하는 안(B)의 비용·복잡도·안전 차이를 비교해 권장안을 선정해 달라.

**리뷰 결과 형식:** ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD. 지적별 \`severity(BLOCKING/MAJOR/MINOR) | 설계 절/근거 | 구체 반례 | 최소 수정 | 소유자 | 수락시험\`을 표로 정리. 인증/실설치/도구 존재 증거가 없을 때는 UNKNOWN으로 명시. 신규 실행·설치·자동 리뷰 재시도 요구 금지.

## 12. 리뷰 후 인계·수정 조건

- 같은 CoWork Work 유지, REQUEST/REVIEW/RECEIPT/review disposition을 연결; 과거 Viewer 편집 UX 리뷰를 재실행하지 않음.
- 리뷰 ACCEPT_WITH_CHANGE 시 실제 지적을 r0002에 반영하고 하나의 구현 handoff를 L1Work/handoffs에 게시하는 것은 리뷰 판정 후 별도 후속 범위다.
- 현 단계에서 **설계 작성/자체 검토는 완료 대상으로 하고, 독립 리뷰 실제 요청은 별도 정식 전송·보호 signer 게이트**를 거친다.
- 이번 설계는 사용자에게 운영 관리 메뉴의 개념만 보여주는 시안이 아니라, 데이터·권한·수집·경합·시험까지 검토하는 정적 설계 기준선이다.
