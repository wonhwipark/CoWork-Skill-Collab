# L1 Workspace — 전체 폴더 URL 탐색·파일별 웹 렌더링 설계 변경 r0002

- 작성: 2026-11-18 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 기준: [안전 전환 r0001](L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_SAFE_TRANSITION_DESIGN_r0001_20261118_KST.md), [업무 GPT 제안 초안 r0001](L1_WORKSPACE_LOCAL_VIEWER_LINUX_PROPOSAL_AND_WORK_ORDER_DRAFT_r0001_20261118_KST.md)
- 변경 근거: 사용자 후속 요구 “업무 네트워크 내 `l1-workspace` 전체를 URL로 열람할 수 있도록, Work별 선택 공개를 기본으로 하지 말 것”; 모든 Markdown 등 문서를 HTML 파일로 사전 변환해야 하는지 질의.
- 단계: `DESIGN_DELTA / HOST_G0_NOT_VERIFIED / INDEPENDENT_REVIEW_NOT_RUN / NOT_APPROVED_FOR_OPERATION`.
- 우선순위: **이 r0002는 r0001의 Work별 선택 공개를 수정하는 최신 요구사항**. 이전 r0001 원본/테스트/리뷰 인계/ZIP은 훼손하지 않고 이력으로 보존. 상충하는 범위·시험은 본 문서가 우선.
- “전체 공개”는 업무 네트워크에서 적절한 사용자에게 **업무 Work 문서/파일 전체를 탐색**하는 UX 요구. **인터넷 익명 공개·호스트 OS root 공유·인증정보/키/토큰/세션/비밀 환경파일 노출·GitHub PUBLIC 업로드 허용을 뜻하지 않음**. 개인·고객정보/회사 관리 정책상 별도 제한 항목은 실제 Linux G0에서 확인, 최소한 시스템 비밀은 제외.

## 1. 핵심 판정 — 전체 HTML 사전 변환 불필요

**파일 저장 원본과 화면 렌더링을 분리**한다.

| 파일/범주 | 원본 보존 | URL 열람 시 처리 | 사전 정적 HTML 전량 생성 |
|---|---|---|---|
| Markdown(`.md`) | 원본 그대로 | 승인된 Markdown renderer가 HTML 화면으로 실시간 또는 캐시 렌더, XSS sanitization, 원본 보기 선택 | **NO** |
| 기존 MSC/가이드 HTML(`.html`) | 원본 그대로 | 기존 인터랙티브 HTML을 별도 격리 origin/sandbox + 엄격한 CSP로 제공, 외부 리소스 정책/상대 asset 확인 | **NO** |
| SVG(`.svg`) | 원본 그대로 | 정적 표시 또는 sandbox SVG 전용 handler, active script/외부 로드 제한 | **NO** |
| JSON/TXT/YAML/CSV/로그 | 원본 그대로 | 텍스트·코드·구조/테이블 뷰어; 크기 제한/라인 분할/다운로드 정책 | **NO** |
| 이미지/PDF | 원본 그대로 | 브라우저 native viewer 또는 검증된 이미지/PDF handler | **NO** |
| 기타 바이너리/대용량 | 원본 그대로 | 검증된 MIME/type에 따라 다운로드·미리보기 미지원 표시; 보호 파일은 403/404 | **NO** |

정적 웹 호스팅만 제공되는 기존 서비스가 G0로 확인되면 **선별 Markdown을 빌드 시 HTML로 변환하는 정적 캐시 방식**은 대안으로 허용. 이는 “원본 문서 전량을 각기 별도 HTML 정본으로 작성”하는 요구와 다르며, 원본 변경/새 지식 정본 생성이 아님. Markdown→HTML render 기능을 무조건 새로 만들지 않고 설치된 서비스의 기존 renderer를 우선 REUSE한다. 전체 사이트 생성기를 기본 필수 설치 대상으로 확정하지 않음.

## 2. 전체 트리 탐색 UX / 원본과 URL 경계

- 단일 진입 URL(설계 예시): `https://<업무망에서 승인된 호스트>/workspace/`. 실제 DNS/포트/HTTPS/접속 경로는 Linux G0 후 확정; 현재 URL 할당/서비스 실행 **NOT_RUN**.
- `/workspace/`에서 최상단 폴더 트리·Work 목록·개인 Knowledge·최근 수정/검색·원본 revision을 확인하고 하위 `works/<work_id>/...`, `knowledge/...`, `index/...`로 이동. Work ID/경로는 실제 업무 설치 루트와 일치해야 하며 `l1sw-workspace`라는 구어/동명 GitHub 저장소를 곧바로 실체로 간주하지 않음.
- 클릭하는 파일 확장자/검증 MIME에 따라 Markdown/MSC HTML/SVG/텍스트/JSON/PDF/이미지 뷰어를 자동 선택. 동일 URL에서 원본 Download/Raw/Preview 권한 구분 필요성은 G0에서 확인.
- 개별 Work의 `MSC_VIEW.md`→`published_path`와 Converter 상세 MD→HTML/AS-IS/TO-BE 링크를 **각각 검증**. 원본 MD 링크는 변경하지 않는 것을 우선; 웹 라우팅이 다르면 **뷰어 계층의 매핑만** 최소 변경. 일부 파일 렌더 실패가 Work 전체 열람 실패/원본 변경으로 확대되지 않아야 함.
- 원본 Workspace/Kernel Ledger/Work·Evidence의 바이트·SHA/원본 revision/쓰기 owner는 그대로. 뷰어는 화면 projection이며 지식 writer가 아님.
- 두 도입 방식을 실제 G0로 비교: (A) 기존 승인된 OpenCode Web/웹 서비스에 **읽기 전용 디렉터리 mount + 파일 핸들러**(가능한 경우), (B) 원본 → 격리된 READ_ONLY snapshot → 승인된 서비스로 조회. **원본 루트 자체를 미검증 정적 HTTP 파일 서버에 그대로 걸지 말 것**. 디렉터리 traversal, symlink, HTML active content, 숨김 파일·환경파일 유출을 막는 필터를 반드시 통과해야 함.

## 3. 전체 업무 자료 공유 vs 호스트 비밀 보호

- 사용자 요구에 맞게 **Work별 공개 목록·동료별 승인 워크플로·개별 문서 분류·별도 개인/동료 색인 중복 생성은 기본 필수 사항에서 제거**. 업무 네트워크에서 허용된 계정은 기본적으로 Workspace 업무 콘텐츠 전체 검색/열람.
- 단, `.git/`, `.ssh/`, 인증키, 토큰, `.env`, 앱 DB의 자격정보/임시 세션, 브라우저 쿠키, credential cache, 실제 호스트 OS 디렉터리, symlink로 Workspace 밖을 가리키는 파일은 뷰어의 **하드 제외**. 콘텐츠 내부에 embedded token 등 비밀이 있는 경우 검사/차단 우선. 운영 보안 정책상 제한 자료는 G0에서 보호 영역으로 분리 가능해야 함.
- 업무 네트워크 내 공유라는 사실만으로 외부 인터넷 무인증 노출을 허용하지 않음. 승인된 VLAN/VPN/방화벽/기존 인증 수단과 읽기 전용 service identity 사용, 인증 적용 가능성 및 감사 요구는 G0로 확인. HTTPS 가능한지 확인; 허용된 기존 프록시를 우선 REUSE.
- 다수 동료 접근이 요구되면 Linux PC 전원/슬립/주소/방화벽/프로세스 재시작 시 URL이 끊길 수 있음을 명시. 상시 가용성이 요구되면 별도 조직 승인된 상시 호스트로 snapshot만 제공하는 C안 검토(자동 배포/업무 원본 반출 근거 아님).
- HTML/SVG의 active content는 원본 서버·업무 토큰과 같은 origin에서 실행 금지. MSC 확대/단계별 동작을 살리면서 sandbox/CSP를 실제 브라우저에서 확인. 외부 CDN 요청/iframe/path traversal/원격 asset loading 부정시험 필수.
- 원본 Linux Workspace 안의 회사 업무 콘텐츠는 사용자 요구에 따라 업무망에서 전부 대상으로 삼되, 정책·권한 검증 전 자동 네트워크 공유·대외 GitHub 업로드 0. CoWork PRIVATE에도 업무 상세 코드/MSC/로그를 게시하지 않음.

## 4. 안전 워크플로 — r0001 P0~P6/G0~G6에서 변경되는 부분

| 단계/Gate | r0001 | r0002 변경 | 실패/중단 |
|---|---|---|---|
| P0/G0 | 전체 Work/서비스/writer/백업/ACL 조사 | **최소 3개 추가 사실**: 업무 root 전체 콘텐츠 유형/파일수·성능, 기존 Markdown/JSON/PDF 핸들러·디렉터리 browse 지원, 전체 사용자 업무망 접근/비밀 제외 정책 | 증거 없이 viewer 종류/상시 서비스 확정 금지 |
| P1/G1 | 격리 synthetic export | 같은 합성 export 유지 + **파일형식별 렌더링·수정불가·새 파일 자동 발견·원본 무변조 테스트** | 전체 HTML 강제 변환/원본 format 변경 금지 |
| P2/G2 | 선택 파일/asset 링크·security allowlist | Work별 allowlist 대신 **Root containment + secret denylist + MIME/size safety + HTML isolation** | 비밀·root 탈출·script 실행은 fail-closed |
| P2~P3/G3~G4 | 개인 SHADOW→선택 Work 동료 Pilot | G3 전체 업무 트리의 localhost 탐색, G4 **업무망 동료 전체 업무 트리 read-only**. 별도 per-Work ACL 정책은 기본에서 제거; 2개 동료 계정으로 동일 범위/읽기만 확인 | 호스트 보안 정책·네트워크 승인 불확실 시 공유 HOLD |
| P4~P5/G5 | GitHub→local authority | **변경 없음**. Viewer 성공이 Git writer 제거·이중 write·local cutover 승인 근거 아님 | 복구/단일 writer/독립 코드 리뷰/원본 고정 필수 |
| P6/G6 | Updater→그룹 writer | **변경 없음**. Viewer URL=열람 편의, group Knowledge 정본/승인/CAS/readback 독립 | URL 실패 시 그룹 재게시 금지 |

### 업무 GPT G0 요청 수정 사항
기존 A~P 숫자 확인은 유지하되:
- **K:** 기존 웹서비스가 업무 root 디렉터리 browse + Markdown 동적 렌더 + HTML·SVG·JSON·PDF를 읽기 전용 표시할 수 있는지 별도 근거.
- **L/M:** 개인/업무망 URL의 접근·기존 서비스/네트워크 정책. 문서별 ACL/Work별 승인 기본 요구는 삭제. 인증 방식은 조직 정책 G0.
- **N:** 전체 원본의 read-only mount와 격리 snapshot 두 방식 중 어떤 것이 안전하게 지원되는지.
- **O:** 기존 per-Work allowlist 여부 조사 대신 **보호 파일/Workspace root 이탈/비밀 denylist**, 숨김 파일과 symlink 처리·서버 identity 통제 확인.
- 추가 Q=파일별 Markdown 렌더·HTML 인터랙티브 MSC·JSON/PDF/이미지 기존 핸들러; R=새 파일/변경 파일의 화면 최신화 방식; S=업무망 동료 동시 접속/PC 꺼짐 시 동작·가용성 요구. 답변 1/2/3/4 코드 동일. 기존 A~P 응답을 강제로 재진행하지 말고 미확인 부분만 확인.

## 5. 새로운 수락 테스트(기존 T01~T26에 추가)

| Test | 범위/기대 결과 |
|---|---|
| T27 | 모든 Work/Knowledge 폴더 탐색이 업무 root 기준 유지되고 새 문서 자동 발견·검색 갱신; 원본 0변경 |
| T28 | `.md` 클릭 즉석 렌더와 원문 보기, XSS/HTML injection 무해화, UTF-8 한글/표/상대 링크 정상 |
| T29 | 기존 B형 MSC HTML/JS/SVG 별도 origin·sandbox·CSP에서 단계 이동·확대 정상, 인증 쿠키/토큰 접근 불가 |
| T30 | JSON/TXT/이미지/PDF/기타 형식별 preview/downloader, 대용량·바이너리/지원 불가 graceful fail |
| T31 | root 탈출: `../`, encoded path, symlink/hardlink·absolute·casefold/NFC·hidden/secrets 403/404; 시스템 비밀 노출 0 |
| T32 | 동료 업무망 2계정에서 전체 Work 목록/검색/상세 URL 동일하게 읽고 API/브라우저에서 쓰기·삭제·rename 불가 |
| T33 | 업무 PC offline/재시작/기본 URL 변경 시 실패 메시지·안정 복구, 기존 Work/Group Knowledge 동작 불변 |
| T34 | 전량 HTML 변환·전량 snapshot 없이 가능 여부, on-demand vs incremental cache 성능/메모리/접근 지연·갱신 부하 비교. 미측정은 NOT_RUN |

## 6. Claude 독립 설계 리뷰 추가 질문 (기존 R01~R22 보존)

- R23: **전량 HTML 생성 불필요** 판단이 설치 서비스의 renderer/정적 대안과 양립하고, 원본 `.md`를 HTML 정본으로 중복 관리하지 않는가?
- R24: 업무망 Workspace **전체 콘텐츠 기본 열람** 시 Work별 ACL을 없애면서도 `.git`/토큰/secret/root 탈출과 JS 공격 격리를 보장하는가?
- R25: 기존 OpenCode Web/Kernel export/Converter를 재사용하고 새 custom server/정적 site generator/인덱스를 선제 구현하지 않는가?
- R26: 파일별 뷰어·Directory browse·검색 최신화·처리 불가 파일 안내와 신규 Work 증가 시 성능을 검증하는가?
- R27: Host local authority 전환을 단순 viewer 전환과 계속 분리하고, Group Knowledge writer의 승인/재게시 안전성을 유지하는가?

## 7. Windows 리뷰 상태·비용 불일치 확인 및 새로운 입력 고정 원칙

- 2026-11-18 실제 Windows [사전검증 결과](CLAUDE_L1_WORKSPACE_LOCAL_VIEWER_DESIGN_REVIEW_PREFLIGHT_BLOCKED_FOR_GPT_20261118.md): `select --intent skill --required-budget-usd 1.00`에서 `POLICY_COST_MISMATCH`. 운영 정책의 최소 USD 1.50 vs 보호 위임 USD 1.00. **기존 요청은 REQUEST/SOURCE_PIN/APPROVAL_SIG/READY/모델 호출 0**, `PREFLIGHT_BLOCKED`.
- 기존 `collab/packages/l1-workspace-local-viewer-design_r0001_1118_REVIEW_INPUT.zip`의 바이트·SHA와 기존 인계서 원본은 **수정하지 않고 보존**. 새로운 요구를 리뷰에 포함하려면 이 r0002를 포함한 **새 고정 입력 r0002 ZIP**으로 패키징하고 해당 manifest·원샷 링크만 새로운 입력을 가리키도록 변경한다. r0001 고정 패키지에 소급 덮어쓰기 금지.
- 새로운 유료 리뷰 정책/위임 1.50/3.00 USD 중 무엇을 적용할지는 **사용자의 명시적 비용 승인**이 있어야 하며, 이를 통한 기존 `auto_delegation.json` 일괄 변경/임의 서명/READY를 하지 않는다. 제안한 새 입력 패키지 등록만으로 Claude가 실행된 것은 아님.

## 8. 후속 전달 기준

- Claude 독립 리뷰 1회 결과/영수증 실제 수신 → GPT 지적별 판정 → r0002 반영 업무 GPT **최종 작업지시서**를 비민감 내용만 `wonhwipark/L1Work/main/handoffs/` 게시·원격 검증.
- 그 전에는 이 설계 변경안을 PRIVATE main에만 기록하고 업무 Linux 원본/동료 웹 서비스/Knowledge group writer/운영 Windows 자동 승인 설정을 변경하지 않음.
- 상태 표시는 `REQUIREMENT_DELTA_POSTED`, `HOST_G0_NOT_VERIFIED`, `WINDOWS_PREFLIGHT_BLOCKED_COST_MISMATCH`, `CLAUDE_REVIEW_NOT_RUN`, `FINAL_BUSINESS_HANDOFF_NOT_POSTED`로 구분.

**NEXT_ONE_ACTION:** r0002 Delta를 포함한 새 고정 리뷰 입력을 PRIVATE에 게시·검증한 뒤, Windows의 비용 승인 조건이 충족될 때에만 정식 REQUEST/SOURCE_PIN/서명/READY/Claude R1 1회 실행. 실제 비용 승인 전 0 유료 호출.
