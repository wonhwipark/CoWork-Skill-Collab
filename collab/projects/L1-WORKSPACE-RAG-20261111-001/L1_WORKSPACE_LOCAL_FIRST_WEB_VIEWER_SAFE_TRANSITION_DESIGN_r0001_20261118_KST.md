# L1 Workspace — Linux 로컬 정본·읽기 전용 웹 뷰어·그룹 Knowledge 안전 전환 설계 r0001

- 날짜: 2026-11-18 KST
- 기존 CoWork Work: `L1-WORKSPACE-RAG-20261111-001` (새 Work 생성 안 함)
- 정본 저장 위치: `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/projects/L1-WORKSPACE-RAG-20261111-001/`
- 범위: 개인 업무 `l1-workspace`의 **로컬 원본 및 읽기 전용 열람 구조**, 그룹 `l1sw-dev-knowledge`의 기존 승인 게시 유지, GitHub 필수 게시 의존성을 **검증 후 조건부 축소**
- 설계 판정: `DIRECTION=ACCEPT_WITH_CHANGE`, `KERNEL_LOCAL_EXPORT_SYNTHETIC=PASS`, `WORKFLOW_REMOTE_DEPENDENCY=CONFIRMED_IN_CANDIDATE`, `LINUX_HOST_G0=NOT_VERIFIED`, `INDEPENDENT_REVIEW=NOT_RUN`, `HOST_CUTOVER=NOT_RUN`, `TEAM_VIEWER_LIVE=NOT_RUN`
- 절대 변경 금지(이번 작업): 실제 업무 Linux 원본/기존 Git 원격·Writer/OS 권한, 그룹 Knowledge·업무 코드, Job/스케줄, PUBLIC 스킬 ZIP, Windows watcher, 토큰/키/DB, 기존 불확실 승인/READY. 문서·격리 합성 시험만 허용.

## 0. 의사결정 요약

**권장: 2단계 분리.** (1) **SHADOW_WEB_VIEW**: 기존 `l1-workspace` Git/Kernel writer를 그대로 둔 채, 로컬 파일을 *읽기 전용으로 별도 격리 export/preview*하고 실제 동일 Work의 MD/MSC HTML 탐색·인증·보안·링크를 시험. (2) **LOCAL_AUTHORITY_CUTOVER**: 아래 모든 게이트가 충족된 뒤에만 Workspace Work 정본/이력과 그룹 게시 근거를 **Linux 로컬 Git 또는 검증된 로컬 revision 저장 + 오프호스트 백업**으로 전환하고 Work 문서 작성 경로에서 GitHub push 의무를 제거. 두 단계는 **동일한 변경/승인이 아니며** 중간에 `LOCAL_AUTHORITY_CUTOVER`를 자동 시작하지 않는다.

- 우선 목적: 개발·검토 중 문서의 가독성, 문서→MSC B형 HTML 이동, 본인 검색, 필요 시 권한 있는 동료의 읽기 전용 열람.
- 유지 목적: Work ID/원 Ledger·Evidence·source pin·변경/결정/시험/리뷰 히스토리, approved group writer의 Preview·CAS/승인·readback·역링크, 그룹 동시 변경 시 충돌 보존, 출처 추적.
- **중요한 구분**: 로컬 Linux 저장 = 다른 동료의 브라우저에서 `file://`로 바로 열림이 아니다. 승인된 웹 서비스가 허용 문서만 HTTP(S)로 제공해야 한다. 인터넷 PUBLIC Pages·L1Work/CoWork에 업무 본문/상세 MSC 업로드 금지.
- 새로운 동기화 엔진/벡터 DB/Work schema/`l1-workspace` 전용 Skill을 먼저 만들지 않는다. 기존 Kernel exporter, 기존 Git writer/백업, 기존 웹 뷰어/OpenCode Web/정적 파일 제공자를 우선 조사.

## 1. 확인한 근거와 전제의 구분

| 유형 | 원본·시험 | 정확한 확인 내용 | 아직 미확인 |
|---|---|---|---|
| 실제 코드/격리 시험 | `work-ledger-kernel_v0_7_45_1118.zip` SHA-256 `1bccbbffeaafcefda27b75ca8f430e502bc8c2b475b63bd76425ca7ee1c5d7f8`; `work_ledger_kernel/work_ux.py::export_docs`; `kernel.WorkLedgerKernel.work_docs_export` | `.git` 미존재 새 폴더에 synthetic Work `README.md`, `works/<id>/`, `index/` 등 12파일 생성, 연속 export byte equality PASS. 관련 기존 pytest `test_github_docs_layout_v077.py`, `test_feature_stage4_export.py` **5 PASS**. `TL_REVIEW` legacy가 있으면 공유 export 자체 차단 테스트 포함 | 실제 업무 설치본과 G0, 운영 파일 수/용량/상태, 웹 URL·접속 |
| 실제 코드/정적 검토 | `l1-fix-workflow_v1_6_72_1118.zip` SHA-256 `0eb190e704d7e06d8bddf642bff858319fceb399814c83282a480502d377af02`; `l1_fix_workflow/github_docs.py` | `docs_sync()`는 `l1-github repo-config`의 `work_docs` 역할 등록·원격 Git origin identity·clean tree 검사를 통과해야 Kernel export 호출. `docs_push()`는 Git commit/push 및 원격 SHA/readback까지 요구. **현 코드를 설정만 바꿔 GitHub 없는 mode로 성공한다고 추정 금지** | 현 Linux의 실제 Workflow 버전/호출 계약, 기존 로컬 단독 인계·읽기 API |
| 기존 협업 설계 | `L1_WORK_TO_KNOWLEDGE_FLOW_r0002_20261115_KST.md`; `L1_WORKSPACE_KNOWLEDGE_34_SKILL_CHANGE_REVIEW_r0001_20261116_KST.md` | Updater 직접 요청/Workflow 기존 분석 모두 Workspace Work에 보존, 개인 `knowledge/` 콘텐츠는 Updater 단독 writer, Kernel Work/Evidence는 기존 관리. 그룹 Knowledge는 별도 승인·revision/readback 후 역링크 | 실제 업무 Updater/group writer의 설치 계약/G0-E3 |
| 기존 MSC 검증 | `GPT_MSC_DUAL_ENTRY_G0_LINK_AND_REPRO_VALIDATION_RESULT_r0001_20261118_KST.md` | Kernel 합성 Work-root `MSC_VIEW.md` → 게시된 HTML 직접 링크 PASS. Converter **상세 원본 MD 내부**의 옛 상대 HTML 링크는 BROKEN; 두 링크를 별도 시험해야 함 | 전체 마크다운/브라우저 실제 동작, HTML 호스팅 보안 |
| 외부 기술 참고 | 공식 MkDocs 설정/배포 문서, Caddy `file_server`, Python `http.server` 보안 문서 | 일반적인 정적 Markdown 사이트/파일 웹 제공 가능. 원문 Work 폴더 직접 문서루트 사용 금지. Python `http.server`는 운영 서버로 권장되지 않음 | 조직 내 승인된 Web/SSO/TLS/네트워크 서비스 및 허용 정책 |

**모든 개발 ZIP은 `development_not_for_deployment`**이며, 위 코드 시험을 업무 설치·그룹 게시·PUBLIC 릴리스 PASS로 승격하지 않는다. 관리 스킬 3종의 기존 Knowledge 보호 미검증/코드 독립 리뷰 게이트는 그대로 유지한다.

## 2. 목표 구조 / 정본·권한 경계

```text
모바일 Agent/업무 GPT/로컬 Agent → 기존 Linux MCP/실행 LLM (현재 허용 경로만)
    │
    ├─ A: Updater 직접 Procedure/Feature 분석
    └─ B: Workflow ISSUE/FEATURE/REFACTOR/설계 Work 분석
             │  동일 Work ID, revision, Code Evidence, MSC 원본/해시, source pin
             ▼
    [업무 Linux 로컬 Work 정본: 기존 Kernel Ledger + 기존 l1-workspace works/]
      (원래 Work 원본·결정·수정·시험·리뷰·업데이트 히스토리)
             ├─ 기존 Local Writer / Work ID 원장 (단일 writer·충돌 보호)
             ├─ 기존 Personal knowledge/ (Updater 전용 WRITE; Workflow READ_ONLY)
             ├─ 승인된 viewer-export (읽기/필터/승인/해시·링크 검사)
             │        ├─ 개인 viewer (본인만, 기존 서비스 우선)
             │        └─ shared viewer (선택된 Work만; 별도 웹 루트+권한)
             └─ 기존 Updater 후보 → Group baseline 비교/Preview → 승인·CAS
                      → 기존 l1sw-dev-knowledge writer → readback/revision
                      → 원 Work 그룹 게시 역링크 (실패 시 그룹 재게시 금지)

CoWork PRIVATE: 비민감 설계/결정/시험·승인/리뷰 영수증만
L1Work PUBLIC: 승인된 최종 스킬 ZIP/비민감 handoff/허용 상태만
```

정본 3개를 혼동하지 않는다: **Ledger/Work 업무 기록 정본**, **그룹 Knowledge 기술 정본**, **웹 게시물(재생성 가능한 파생 복제본)**. 웹 사이트 편집은 정본 기록이 아니며 그룹 Knowledge의 게시 revision과 페이지 URL은 다른 개념이다.

### 저장 위치·권한 설계 (표시 경로는 개념적 식별자, 호스트 실경로 아님)

| 구역 | 소유/권한 | 목적/전송 |
|---|---|---|
| `WORKSPACE_ROOT/works/`, `WORKSPACE_ROOT/index/`, `WORKSPACE_ROOT/knowledge/` | 기존 Workflow/Kernel/Updater의 검증된 writer만 WRITE. 개인 ACL. | 원본 개인 Work · 인덱스 · 후보; **그대로 웹 document root 지정 금지** |
| `LEDGER_ROOT` | 기존 Kernel writer와 백업 주체 | 원장과 근거. 웹 서버에서 절대 직접 접근 불가 |
| `VIEWER_STAGING` | 검증된 publisher만 WRITE, 네트워크 서빙 없음 | export·허용목록·민감성 검토·임시 검사; 사고 시 폐기 가능 |
| `VIEWER_PRIVATE_ROOT` | 발행 writer WRITE, 사용자 viewer READ | 본인 전용 Markdown/MSC 가독성 열람. localhost 또는 승인된 인증 통로만 |
| `VIEWER_SHARED_ROOT` | 발행 writer WRITE, 팀 viewer READ, 절대 GROUP WRITE 아님 | **명시적 allowlist Work/파일만** 웹 제공, 동료는 읽기 전용 |
| `BACKUP_ROOT` | 독립 보호·스냅샷·복구 정책, 일반 viewer NO_ACCESS | 원본/이력 오프호스트 보존과 복원 검증 |

실제 경로·도메인·서비스/ACL/사용자 그룹은 업무 Linux G0 실측 후 매핑. 숨김 디렉터리/토큰/코드/로그/ZIP/DB/README 밖 파일을 폴더 전체 나열로 웹에 노출하지 않는다. 기본 `DENY`; allowlist가 없으면 shared 출력 **0개**.

## 3. 후보 방식 비교와 최종 선택 규칙

| 후보 | 장점 | 위험/실제 전제 | 권장 |
|---|---|---|---|
| A. 기존 Git writer 유지 + 로컬 **개인** VIEWER 미러(읽기 전용) | 사용자 즉시 가독성, authority 미변경, 롤백 쉬움 | 기존 OpenCode Web·기존 웹 서버가 안전한 read-only 문서 루트를 지원하는지 확인 | **첫 시범** |
| B. A + 승인받은 내부 HTTPS **팀** VIEWER (선택 Work만) | 검색/MSC/Work ID 팀 공유 | 조직 인증·ACL·접속 경계·CSP·개인 PC 가동 가용성/백업 검증 필수 | G0 및 팀 보안 게이트 후 |
| C. 기존 Git push 제거, **로컬 Git/Kernel 정본 + 검증된 오프호스트 백업**, viewer는 파생 | GitHub 필수 게시 부담 완화, 업무 코드·상세 근거 로컬 보존 | 현재 `docs_sync/docs_push`의 원격 identity/commit/push/readback 계약 변환 필요, 크래시/이중 writer/다른 호스트 재개·복원 리스크 | **별도 authority cutover** |
| D. 공유 NFS/SMB를 단일 Work writable 루트로 변경 | 폴더 직접 공유 | 동시 쓰기, 권한·파일 잠금, Git/Kernel writer 불변성 위험 | 비권장. 별도 승인 없는 직접 변경 금지 |
| E. 새 동적 웹 앱/DB/RAG 엔진 | 기능 확장 가능 | 구현·권한·검색 색인 보안 부담 큼; 이미 있는 viewer와 중복 | 미검증 gap 입증 전 보류 |

우선 **A→B를 검토하고 C의 별도 평가**. 동료들이 항시 볼 필요가 있으면 사용자 개인 Linux PC 단독 호스팅보다 승인된 상시 가동 읽기전용 서버에 *허용 문서만 복제*하는 방식을 고려. 웹 주소가 `file://`나 GitHub PUBLIC URL이면 안 되며 실제 HTTPS 권한·접속 시험 후 확정한다.

## 4. 웹 뷰어 UX / 파일 형식 / 안전 요구

- 첫 화면: Work ID·Module·Procedure/Feature·source revision·진행 상태·마지막 업데이트·다음 한 동작 검색/필터. `works/<work_id>/` 디렉터리 링크를 안정 키로 사용. 제목 변경으로 경로 바꾸지 않음.
- Work 상세: Overview/결정·코드 근거/설계·HLD·문서/MSC B형 HTML/시험·리뷰/Evidence/지식 후보·그룹 게시 revision. 원본 MD와 HTML 렌더링을 구분하고 **원본 해시·source pin·확인 상태**를 표시.
- MSC: Viewer B형 HTML+SVG를 **별도 복제 파일**로 열람. Work-root `MSC_VIEW.md`의 확인된 `published_path`만 사용. 상세 Converter MD 안의 원본 상대 HTML 링크는 별도 검증하고 깨진 경우 공유 사이트 404를 허용하지 말고 **해당 카드/링크 HOLD**. 원본 Evidence의 본문·해시 무단 덮어쓰기 금지.
- 검색: 권한 필터 후 승인된 사용자/Work 범위에서만 색인 생성; search index JSON 자체도 민감한 본문을 담을 수 있으므로 같은 인증·ACL 보호. 개인 검색과 동료 검색은 색인을 분리. 임시가설/제한코드·로그·토큰은 색인·프리뷰·브라우저 캐시에 반출하지 않음.
- 웹 도구 우선순위: **기존 승인된 OpenCode Web/내부 static service** 재사용 G0 → 적합하지 않으면 MkDocs의 정적 빌드(기존 렌더러와 링크 변환 호환 검증 필요) + 조직 승인된 HTTPS reverse proxy/SSO → 동적 앱 마지막 선택. 서버 설치/오픈 포트/서비스 등록은 별도 호스트 승인.
- 보안: 별도 vhost/origin, 인증/최소권한/접근 로그, 암호화, 콘텐츠 분류·승인; 파일 확장자 허용 MD/HTML/SVG/소형 이미지(정책 허용 시) + MIME 검증. HTML/SVG 내 script/iframe/external URL/네트워크 요청은 제거·제한 또는 사용자 접근 자체 HOLD. 대화형 MSC의 JS 허용 필요 시 격리 origin·iframe sandbox·CSP 호환 및 실제 브라우저 검증. JS 파일 검토 없이 CSP를 임의 완화 금지.
- Path 보안: 상대 `..`, 절대경로, UNC, URL-encoded traversal, unicode/casefold 경로 충돌, 숨김·symlink/hardlink 외부지점, file://·data:·javascript:·외부 origin link, HTML base href·redirect를 탐지하고 거부/격리. 원본 Work 전체를 웹 루트로 가리키지 않음.
- 운영 서버로 `python -m http.server`를 사용하지 않음(공식 Python 문서가 운영 용도 비권장). 정적 사이트는 호스팅 서비스가 별도.

## 5. 스킬별 재사용 / 변경 영향 (G0 전제)

| 스킬/서비스 | 현재 확인 | 우선 대응 | 실제 EXTEND 확정 조건 |
|---|---|---|---|
| `work-ledger-kernel` | 개발 v0.7.45 `work_docs_export`가 비Git 임시 폴더에 동작 PASS. `TL_REVIEW` legacy auto 공유 차단 내재. | **REUSE** exporter의 원본/인덱스. 안전한 VIEWER_STAGING 복사/링크 맵·원본 비변조 시험 | Markdown/HTML asset mapping 또는 기존 export가 게이트 요구 미충족 입증 시 최소 패치 |
| `l1-fix-workflow` | 개발 v1.6.72 `docs_sync()` Git origin identity·clean tree, `docs_push()` Git remote readback 강제. | 현행 WORK 저장/push 변경하지 않고 **viewer만 독립** 연결. 나중에 로컬 authority를 별도 `mode`/role 계약으로 설계 | 실제 LOCAL_ONLY 전환 결정과 기존 provider로 분리 불가능 입증 뒤. 임의로 remote 체크만 삭제 금지 |
| `l1-github` | 기존 `repo-config work_docs`·workspace-state·commit/push/remote-readback 역할; 개인 `knowledge/` 경로 보호 미검증 이력 | 현재 role/원격·권한/변경 파일·push guard/백업을 G0. Git을 로컬 revision로 유지할지 평가 | 완전 local source of truth에서 기존 remote_readback의 대체 계약·writer ACL·CAS 확인 필요 |
| `doc-converter` | MSC B형 HTML 및 신규 ISSUE opt-in은 일부 PRIVATE 개발 후보; 최신 현장 미확인 | **REUSE** HTML/MD/manifest, linked asset 보정은 경로별 E3 별도 검증 | 기존 버전이 승인된 B형 HTML 생성 실패한 경우만 기능 확장 |
| `l1-knowledge-updater` | 설치 원문·개인·그룹 writer G0 미확인 | 두 진입 동일 Work/Evidence로 후보/Preview/그룹 반영; 로컬 파생 Viewer URL은 사실 출처가 아니라 부가 링크 | 실제 Installed API 확인 후 고정 revision/그룹 writer CAS 연결 미지원 gap만 확장 제안 |
| `l1sw-dev-knowledge` | 그룹 검증 지식 정본, 실제 별도 writer·Repo 위치 G0 미확인 | **불변:** 승인/Preview/group HEAD/CAS/readback, Work 역링크 | 실제 지원 공백과 별도 권한 승인 확인 전 변경 금지 |
| 웹 호스팅 | 실제 OpenCode Web/Apache/Nginx/Caddy/SSO·포트 G0 미확인 | 기존 인가 서비스 재사용 여부 우선, 신규 도입 결정 보류 | 기존 서비스가 문서 read-only/auth·HTML 정책 미충족인 경우 |

## 6. 안전 전환 워크플로 / Stop 조건

### P0. 선언·원본 동결 및 G0 (읽기 전용, NOW)
- 같은 Work ID, 기존 Git 원격·branch·미커밋·untracked·lock·stale 상태, 실제 Kernel/Workflow/Updater·Git provider/웹 서비스의 설치 버전, 현재 Ledger와 workspace 루트, 읽기용 local source root registry를 **읽기 전용** 확인.
- 파일 수/총 바이트·큰 파일·정리 대상·Work ID 개수·분류별 비공개 상태·원본 MSC 상대 링크 패턴·이미지/JS 의존성·Work 1,000개 이상 여부는 **수량만** 회신; 이름/원문/절대 경로 외부 반출 금지.
- 기존 백업 위치/복구 완료 이력·RPO/RTO, 동료 네트워크 접근 가능성·웹 인증 방식/조직 허용 정책, 상세 HTML/로그/코드 공유 제한 확인. 미확인 → **C/B 보류**, P1 합성 검토만 진행.

### P1. 비민감 합성·오프라인 회귀 (NOW, 검증 가능)
- Kernel의 로컬 non-Git export와 idempotence/기존 `work_docs_navigation`과 snapshot 구조를 직접 시험. **이미 5 PASS + 별도 synthetic nonGit 12파일 export PASS**.
- Viewer 구현을 확정하기 전 최소 자료형·권한/링크 반례를 시험 계획으로 고정. 미접근 source를 위해 가짜 구현 API 생성 금지.
- PRIVATE에는 비민감 설계/시험 결과·G0 인계만. 실제 개인 Work·회사 코드·로그·MSC를 업로드하지 않음.

### P2. 개인 SHADOW 뷰어 실측 (G0 뒤, 별도 Linux 승인)
- 운영 Work 원본은 손대지 않고 기존 도구가 만든 export의 **복사본**을 격리된 staging에 생성. exporter는 legacy rename/migrate 가능한 코드이므로 **실제 루트에 처음 호출 금지**. 안전한 preflight→적합한 작업본에서만 실행; 원본 Work 0변경 확인.
- 파일 허용목록·원본 SHA/source_revision·생성 목록·업로드 금지 항목 검사, `WORK_ROOT`→HTML·원본 상세 MD 링크 등 전부 검사. 실패하면 VIEWER_ROOT 교체/반영 0.
- 검증 후 개인 viewer의 local-only(네트워크 외부 차단) 열람; 기존 데이터 writer/push 완전 유지. 개인 UI는 전용 `VIEWER_PRIVATE_ROOT`만 읽음. 캡처된 G0 및 승인 없는 포트/프로세스 실행 금지.

### P3. 선택 Work 동료 READ_ONLY 시범 (별도 공유·서버 승인)
- 동료용 Work별 explicit reviewer-approved allowlist(범위·만료·사유), 링크/이름/본문·첨부의 등급 및 사람 검토, 기존 서버/SSO/VPN/HTTPS/방화벽 승인 확인.
- 별도 `VIEWER_SHARED_ROOT`에는 선택된 Work만, 파일 모드 읽기 전용, server 계정은 `WORKSPACE_ROOT`/Ledger/개인 candidate에 접근 금지. 웹 검색 색인도 동일 whitelist/ACL.
- 타 Work URL·비승인 링크·symlink·path traversal·direct blob/API·cache로 누출 불가 확인. 허용되지 않은 경우 공유 0건, 개인 사이트만 유지. 공유 승인만으로 그룹 지식 게시 권한 생기지 않음.

### P4. 로컬 AUTHORITY 전환 준비 (동료 뷰어 성공과 별개)
- 기존 Git remote 보존/변경 전 full snapshot·원본 SHA/tree/HEAD/dirty/migration history/인증 권한/복원 완료 영수증. 미커밋·conflict가 있으면 fail-closed, 자동 stash/reset/rebase/cherry-pick 금지.
- **로컬 Git 또는 기존 provenance 지원**으로 Work ID·원장 revision·업무 증거·동시 writer 충돌·이력 추적·2번째 Linux 호스트 복구 기능을 보존. 단일 PC 장애 대비 오프호스트, 접근 제어된 백업 및 복원 시험 필수. GitHub를 유지한 mirror가 승인되면 remote mirror도 출처/보존 정책에 포함.
- Workflow `docs_sync/docs_push`의 `git_plan.commit/push/remote_readback` 의존을 별도 `LOCAL_EXPORT/LOCAL_VERIFY`(제안 개념)와 원격 게시로 분리하는 최소 diff 설계. 이름/CLI/API 확정은 실제 현장 G0와 독립 코드 리뷰 후. 단순 코드 분기 삭제·remote 제거는 안 됨.
- 사전 backward compatibility: 기존 Github mode 동일 동작, 미검증 local mode default OFF, 구버전 소비자/manifest schema 불변, rollback 시 이전 role/remote 복원 가능.

### P5. 통제된 cutover (별도 명시적 운영 승인)
- 준비 완료, 승인 시점 freeze: writer 1개·진행 중 Job 0·host backup verified. 승인된 일정 동안 모든 새 Work WRITE 중단, ledger/workspace snapshot 1회, output/원본 각 SHA 비교.
- local authority writer 및 개인 viewer만 ON; GitHub mode는 보존하되 명시적 선택 없이는 push되지 않도록 검증. 이중 쓰기/양방향 sync 자동 시작 금지. 기존 원격 main/history는 삭제·force push 금지.
- 1개 비민감 테스트 Work → 기존 Work 재개·요약·Evidence 추가·문서화·재실행 멱등·그룹 후보/Preview→승인된 경우에만 그룹 게시 E3. 로그/영수증 기록. 문서 뷰어 실패는 파생물만 재생성, group 게시 재실행 금지.

### P6. 운영 수락/확산·복구
- 정해진 관찰 기간에 host 재시작·동료 2계정 권한·검색 색인 격리·직접 링크/HTML 연결·backup restore·문서 수정 충돌·업무 Agent 조회·그룹 승인/게시 역링크를 검증. 기간/횟수는 업무 환경 SLA 및 사용자 승인으로 확정.
- 실패시 web first OFF(더 이상 노출 안 됨) → 해당 site 복제본 폐기/이전 버전 복귀 → 원본 Workspace 복원 검증 → 기존 Git/Workflow provider 경로 사용 가능성 점검. **데이터를 덮어쓸 수 있는 역방향 자동 merge/push는 롤백으로 간주 금지**. 어느 writer가 authoritative인지 모르면 STOP/격리/증거 보존.

### 전환 Gate 요약

| Gate | PASS를 위한 실행 근거 | FAIL/HOLD 시 |
|---|---|---|
| G0 인벤토리·권한 | 실제 설치/Work ID·원격/sync/backup·웹/ACL·writer 인터페이스 read-only 근거 | `G0=NOT_VERIFIED`, P1 외 운영 불가 |
| G1 Kernel 합성 | 비Git 로컬 export, SHA, idempotence, manual edit/legacy/1000 boundary | exporter 소규모 보완·반례 재시험 |
| G2 링크/보안 | 모든 MD/HTML asset `published_path`·원본 SHA, traversal·secret·JS/CSP 거부, shared 기본 0 | 해당 Work shared HOLD, 원본 미변경 |
| G3 개인 웹 | 격리 개인 viewer real browser, 백업 영향 0, 사용자 auth/local-only 확인 | browser/서비스 보류, 이전 Git 경로 유지 |
| G4 동료 웹 | 사용자/회사 승인, 선택 Work ACL, TLS/네트워크/로그, 타 Work 403/404 | 동료 공유 금지, 개인 viewer 유지 |
| G5 authority | 이력/백업 복원·writer 충돌·기존 Git 호환·코드 리뷰·승인·상세 G0 | GitHub push 필수경로 유지 |
| G6 Knowledge E3 | Updater 두 진입·Preview/CAS/승인·group readback·같은 Work 링크, 충돌/부분 실패 | 그룹 미반영·보류, 기존 원본 보존 |

## 7. 주요 사고·반례 / 합격 테스트 매트릭스

**표의 예상은 설계 수락 기준이며 실제 호스트 시험 PASS가 아님.**

| 테스트 | 입력/반례 | 필수 결과 |
|---|---|---|
| T01 | `.git` 없는 새 폴더에 synthetic Work export | 생성된 문서·index 보존; **격리 PASS** |
| T02 | 같은 Work 반복 export | 파일 hash 변경 0; **격리 PASS** |
| T03 | Legacy `TL_REVIEW` 기록 | 공유용 export 차단; **Kernel 기존 pytest 범위 PASS** |
| T04 | Work의 수동 `문서안내.md` 변경 | 덮어쓰기 금지/충돌 보존 |
| T05 | 두 Worker 같은 Work 동시 기록 | 단일 writer/lock·stale revision 차단 |
| T06 | Source SHA 변경 또는 dirty tree | 구버전 분석을 최신 사실로 승인 금지 |
| T07 | Work-root MSC_VIEW → HTML | 실제 원격/로컬 파일 링크·SHA 일치 |
| T08 | Converter 상세 원본 MD → `01_AS_IS.html` | 기존 BROKEN 해소 또는 해당 링크 HOLD, 원본 MD 무단 수정 금지 |
| T09 | 상대 링크 `../..`, 절대·인코딩 traversal | 해당 viewer 링크/파일 차단 |
| T10 | symlink·hardlink·hidden/`knowledge/` alias | 원본 외부 접근·공개 0 |
| T11 | 비승인 Work/비허용 확장자 | shared 문서 0/HTTP 403·404 |
| T12 | 비밀 문자열/제한 로그/고객자료 | 최소 보안 검사+사람 검토 불합격 시 shared 0 |
| T13 | HTML/SVG 내 JS·iframe·외부 fetch | 격리·CSP/ACL 검증 또는 공유 HOLD |
| T14 | 사용자 A 허용 Work, 사용자 B 불허용 Work | 사용자 B direct URL/search/assets 접근 차단 |
| T15 | 검색 색인·브라우저 cache·ETag | 서로 다른 권한 범위로 데이터 누출 0, 갱신 반영 |
| T16 | Unicode NFC/NFD·대소문자·경로 중복 | 동일 실파일 충돌 fail-closed |
| T17 | 매우 긴 파일명/HTML asset·복수 participant | MSC B 보기/확대·스크롤·상대경로·가독성 검증 |
| T18 | index 1000+ Work 또는 5MB+ Evidence | Kernel 기본 limits와 누락 탐지/크기 정책, 잘린 상태 PASS 금지 |
| T19 | staging 중 전원/빌드 실패 | 마지막 승인된 viewer root 유지, 부분 파일 노출 0 |
| T20 | Web server 중지/호스트 재부팅 | Work/Group 원본 영향 0, viewer 재생성 가능 |
| T21 | 원본 Work Git 충돌/diverged/untracked | auto reset/rebase 금지, HOLD·복구 가능 |
| T22 | 오프호스트 백업 유실/복원 실패 | authority cutover 금지 |
| T23 | 그룹 게시 CAS 충돌/다른 동료 갱신 | Preview 재대조·수동 승인; 덮어쓰기 금지 |
| T24 | 그룹 게시 성공 + Work 역링크 실패 | group write 재시도 금지, 링크만 복구 |
| T25 | 그룹 write 응답 불명확/중복 요청 | remote receipt/readback 우선, 임의 재게시 금지 |
| T26 | rollback 시 로컬에만 신규 이벤트 있음 | 원본 snapshot/양 writer 증거 보존·대조 전 과거 remote로 덮어쓰기 금지 |

## 8. 실제 운영·보안 승인 경계

- `DESIGN_DOCS_AND_SYNTHETIC_TEST=ALLOWED`. CoWork PRIVATE main의 비민감 설계·검증 증거 기록만 수행. 업무 Linux의 설치본·Work/코드/고객/운영 로그·키·토큰은 PRIVATE/PUBLIC에 복사하지 않음.
- `READ_ONLY_LINUX_G0`: 업무 GPT/로컬 Agent가 사용자의 승인된 도구 내에서 기존 설치본의 계약/상태를 읽을 수 있는지 확인. 이를 자동으로 실제 Linux 접근 PASS로 취급 금지. 호스트에서 유료 모델/Job/외부 전송·설치·토큰 생성 금지.
- `P2_PERSONAL_LOCAL_SERVER`: localhost 여부와 설치/서비스 실행·OS 권한 변경은 별도 승인 확인. G0 확인되지 않으면 설정 제안만 하고 실행 금지.
- `P3_SHARED_SERVER`, `P5_AUTHORITY_CUTOVER`, `GROUP_WRITE`: 신규 네트워크 공개·인증/ACL·서버 설치, 원본 이동·기존 writer/remote 변경, Knowledge 쓰기는 각각 별도 명시 승인·사전 보호검증. 완료로 보고 금지.
- **Windows Claude** 독립 설계 리뷰는 이 작업의 별도 독립 검토자가 수행. 결과/영수증 없으면 `INDEPENDENT_REVIEW=NOT_RUN`; 기존 완료 MSC R1의 결과를 이 전환 설계로 소급 승인 금지. REQUEST/READY는 보호 signer/policy/budget 유효성 실확인 후만 게시. 대화/MD만으로 모델 호출·호스트 작업 트리거 없음.

## 9. 업무 GPT Linux G0 회신 계약 (별도 L1Work handoff 게시)

코드 1=원문/호스트 근거로 확인, 2=근거로 미지원 확정, 3=미확인·접근 불가, 4=일부 지원·조건 있음. 다음 A~P 항목에 대해 **16개 숫자**로 응답. 외부 출력에는 실제 root/host/branch/사용자/토큰/개인 문서/접속 URL/Work 제목·내용을 포함하지 않는다.

| 항목 | 물을 질문 |
|---|---|
| A | Kernel 실제 설치본은 로컬 non-Git docs export를 지원하는가? |
| B | Workflow 실제 docs_sync는 git origin identity/clean tree가 필수인가? |
| C | Workflow 실제 docs_push가 remote commit/push/readback을 요구하는가? |
| D | `work_docs` role·실제 root/host 설정을 안전하게 조회 가능한가? |
| E | 기존 local Git 이력/단일 writer 및 approved backup/restore 근거가 있는가? |
| F | 개인 `knowledge/` Updater 단독 writer/다른 Skill READ_ONLY가 강제되는가? |
| G | Updater 두 진입 모두 기존 Work/Evidence를 기록·재사용 가능한가? |
| H | 그룹 writer Preview·승인·CAS/readback과 Work 역링크를 제공하는가? |
| I | Kernel Work-root MSC_VIEW→HTML 링크가 실제 설치본에서 유효한가? |
| J | Converter 상세 원본 MD 상대 HTML 링크도 유효한가? |
| K | 승인된 기존 웹 서비스가 정적 MD/HTML을 읽기 전용으로 제공하는가? |
| L | 개인 localhost 시범이 기존 권한/인증·보안 경계를 만족하는가? |
| M | 동료의 로그인·그룹 ACL·HTTPS·감사·네트워크 공유 수단이 승인되어 있는가? |
| N | 개인/동료 승인 파일만 별도 web docroot로 출판하는 경로가 존재하는가? |
| O | 업무 원본의 민감 등급/동료 공유 허용목록 분리가 가능한가? |
| P | 별도 writer 변경 없이 G0 다음에 비민감 synthetic host E3가 가능한가? |

G0 완료 전에는 구체 설치·변경 명령, 기동 포트·신규 호스트 경로, 파괴/지우기/원격 변경 지시 금지. 숫자 중 3·4가 존재하면 해당 항목을 HOLD; **16개의 1**이 아니더라도 개인 VIEWER를 어떻게 테스트할 수 있는지 독립 판단 가능.

## 10. 품질·유지보수·동료 UX 완료 기준

- 본인: 최신 Work를 열 때 코드 diff가 아니라 `Overview → Evidence/MSC → Decision → 다음 조치`가 2단계 이내; Work ID/기간/Source Revision/AS-IS·TO-BE/지식 반영 상태를 혼동하지 않음.
- 동료: 승인된 Work만 열람, 변경하거나 잘못된 그룹 최신 사실로 오인하지 않음; 공유 URL 복사 후 인증된 계정만 열람; 승인 만료 시 접근 차단·검색 색인 반영.
- Team Knowledge: module→feature→scenario 탐색 유지, Procedure는 교차 축; 이슈는 증상/원인/해결, Feature는 신규/개선. 개인 임시 분석·그룹 검증 지식의 source pin/revision을 구분.
- 운영: 사용자 PC 다운·GitHub 원격 장애·Linux viewer 장애에서도 기존 원본/승인 지식이 손상되지 않음. 실제 복원 시험과 권한 부정시험이 완료돼야 `CUTOVER_READY`.

## 11. 이번 실행 결과·다음 한 동작

- `SOURCE_REVIEW=PASS_SCOPE_LIMITED`: 기존 CoWork 최신 Work·카탈로그·Workflow/Kernel 원문 및 과거 Knowledge Guard/MSC 판정 확인.
- `SYNTHETIC_KERNEL_LOCAL_EXPORT=PASS`: 실제 개발 후보 v0.7.45를 격리해 Git 없는 폴더에 12파일 export 및 동일보존·멱등성 직접 확인.
- `TARGETED_KERNEL_PYTEST=PASS`: 기존 2개 테스트 파일 합계 5 PASS (0.49s). Linux 호스트가 아닌 이 세션 로컬 합성 시험.
- `G0_LINUX_INSTALLED=NOT_RUN`; `P2~P6_HOST_APPLIED=NOT_RUN`; `GROUP_WRITE=NOT_RUN`; `INDEPENDENT_REVIEW=NOT_RUN`.
- `NEXT_ONE_ACTION`: 업무 Linux의 G0를 공개 허용된 숫자 답변으로 수신→실제 호스트에서 이미 있는 웹 서비스/백업/권한·writer 계약과 대조→개인 SHADOW 뷰어의 승인 가능한 최소 diff/인계/테스트를 같은 Work에서 확정. 미확인 공급자를 이유로 새 DB/서비스를 자동 설치하지 않는다.