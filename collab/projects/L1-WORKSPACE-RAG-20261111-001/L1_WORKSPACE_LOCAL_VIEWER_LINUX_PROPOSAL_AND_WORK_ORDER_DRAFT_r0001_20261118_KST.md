# 업무 GPT 제안 및 작업 지시서 — Linux 로컬 L1 Workspace + 읽기 전용 웹 뷰어 (리뷰 반영 전 초안)

- 문서: r0001 / 2026-11-18 KST
- **상태: DRAFT / CLAUDE_INDEPENDENT_REVIEW=PENDING / HOST_G0=NOT_VERIFIED / NOT_APPROVED_FOR_OPERATION**
- 목적: 업무 Work의 분석·Evidence·결정 이력을 Linux 로컬에서 안전하게 보존하고, 허용된 문서만 읽기 전용 웹으로 열람하며, 검증한 기술 지식을 **기존 그룹 Knowledge**에 승인·게시하는 단계적 전환. 개인 작업 원본과 그룹 Knowledge 정본을 혼합하지 않음.
- 실행 역할: 업무 GPT(요청/판정) → 허용된 Linux Agent / MCP(읽기 전용 조사·승인 범위 내 시험) → 기존 Workflow/Kernel/Converter/Updater(각자 책임 유지).
- 모든 식별자와 경로는 **업무 호스트에서 확인**. 동명 GitHub.com 저장소를 l1-workspace 실체로 가정하지 않음. 추측한 API·설치 명령·포트·URL 금지.
- 이 문서는 검토와 G0를 위한 초안. Claude 독립 리뷰 결과/영수증, GPT 최종 판정 후 개정하여 최종 실행서만 사용.

## A. 제안 요약과 선택지

**권장 기본안 A — 기존 Git 원본 유지 + Linux 개인 읽기 전용 SHADOW Viewer부터.** 안전성이 입증된 뒤 승인된 Work의 팀 공유를 선택적으로 제공하고, 최종 local-authority cutover는 별도 Gate로 결정한다. 초기 단계에서 GitHub push 강제 경로를 제거하거나 원본을 이사하지 않는다.

| 구조 | 권장 시점 | 장점 | 이행/운영 위험 |
|---|---|---|---|
| A. 기존 Git/Work writer + 로컬 viewer 파생본 | 1차 시범 | 원본·이력/원격 readback 그대로, 복구 쉬움 | 로컬 viewer 별도 생성·권한 관리 |
| B. local Git authority + offhost 보존·복원 | G0·G5·별도 승인 후 | 원격 게시에 대한 일상 의존 축소 | 단일 writer·충돌·백업 RPO/RTO 대체 필요 |
| C. 승인된 공용 호스트의 읽기 전용 복제 viewer | 동료 상시 접속 필요·G4 후 | 개인 PC 다운과 분리 가능 | 계정/ACL·HTTPS·유출·운영 주체 검증 필요 |

**세 개 영역의 소유권**: ① 업무 로컬 Work Ledger/초안/Evidence(진행 원본), ② 별도 allowlist/격리된 HTML 웹 파생본(정본 아님·READ_ONLY), ③ 팀 `l1sw-dev-knowledge`의 승인된 기술 지식(별개 revision/CAS 정본). 웹 viewer는 자체 Knowledge writer가 아니며, Group 업데이트 성공 여부는 서버 운영 여부와 무관하게 따로 확인한다.

## B. 업무 GPT가 우선 수행할 읽기 전용 G0 조사

**중요**: 이 단계만 읽기 전용으로 실행. 허용 도구에 접근할 수 없으면 가정으로 채우지 말고 3(미확인) 회신. 전송에는 실제 호스트명, 사용자명, 절대 경로, 코드/로그, 토큰, 고객/프로젝트 상세 자료를 포함하지 않는다. 전체 원본을 외부 저장소에 복제하지 않는다.

답변 코드: `1=실제 설치/원문 근거로 확인`, `2=근거로 미지원 확정`, `3=미확인/접근불가`, `4=부분지원/조건 있음`.

| 번호 | 실제 환경에서 확인할 항목 |
|---|---|
| A | 실제 Kernel `work_docs_export`가 비Git 로컬 복제 폴더에 출력 가능한지 |
| B | Workflow `docs_sync`의 registered origin/clean tree 필수 여부 |
| C | Workflow `docs_push`의 commit/push/remote-readback 의존 |
| D | 실제 `work_docs` role/root/host 설정과 Work ID·Ledger 출처 조회 가능성 |
| E | 로컬 Git 이력/동시 writer 보호/오프호스트 백업 및 복원 **실제 근거** |
| F | 개인 `knowledge/`의 Updater 단독 WRITE와 다른 스킬 READ_ONLY 통제 |
| G | Updater 직접 분석/Workflow 분석 두 진입이 동일 기존 Work/Evidence를 지원하는지 |
| H | 그룹 writer의 Preview/승인/CAS/readback/원 Work 역링크 |
| I | Work-root `MSC_VIEW.md`가 실제 HTML 파일을 가리키는지 |
| J | Converter 상세 MD 내부의 HTML 상대 링크도 실제로 동작하는지 |
| K | 승인된 기존 웹 서비스에서 정적 MD/HTML을 읽기 전용 제공하는지 |
| L | 개인 localhost/인증 격리와 최소 공개 요구 충족 여부 |
| M | 동료 인증/그룹 ACL/HTTPS/감사/네트워크 공개에 대한 유효 승인·서비스 |
| N | 원본과 분리된 선택적 web docroot/staging/publish 사용 여부 |
| O | Work별 보안 등급/승인된 공유 allowlist·개인 비공개 분리 |
| P | 기존 원본 writer 변경 없이 합성 Work로 Linux host SHADOW 시험 가능성 |

출력: `A~P: 숫자 16개`와 `EVIDENCE_LEVEL(설치본/원문/보고/미확인)`, `BLOCKERS`, `READ_ONLY_ONLY=YES`를 기록. 민감 내용은 로컬 Evidence에만 저장; 외부로는 증빙 유형·버전 확인 여부·근거 유무만 전달.

## C. 단계별 실제 작업 지시 (승인 조건 엄수)

### P0. 환경 확인/원본 보존 평가 — READ_ONLY, 현재 착수 가능

1. 기존 스킬과 문서의 실제 설치 버전·`l1-workspace` root·Work ID·Ledger·동기화 주체·기존 Git remote·dirty/diverged/untracked 여부를 **읽기 전용** 파악.
2. 기존 승인된 viewer/OpenCode Web/Markdown 렌더/정적 사이트 생성기를 확인, **REUSE → CONNECT → 검증된 gap만 EXTEND**.
3. backup 위치(외부에 경로 공개 금지), 권한/암호화·복원 증거, Git 복구 이력, 단일 writer lock 및 동시 Job 수를 파악.
4. Group updater의 두 진입과 개인 Knowledge 쓰기 소유권, Preview/CAS/그룹 publication authority를 문서·설치본에서 구분.
5. 실제 URL/서비스/사용자 ACL은 비민감 상태와 capability 확인만 보고. 절대 경로·호스트 주소·고객자료를 공개 협업으로 보내지 않음.
6. `G0_REPORT`: A~P 숫자, 현재 유지할 경로·필요한 별도 승인·호스트 G0 blocker/제안 최소 연결만 요약.

**금지**: 신규 install, 포트 listen, firewall/ACL/Git 설정 변경, push/pull, DB/원본 Work update, backup 자동 삭제, 그룹 게시, 새 모델 호출/Job 실행.

### P1. 격리 합성 export·링크/보안 설계 — G0 결과 확인 및 허용된 시험 범위

1. 실제 로컬 Kernel 설치본 또는 검증된 후보를 분리하여 테스트. 기존 원본 Work가 아니라 **synthetic** 입력과 독립 staging/test dir 사용.
2. 동일 Work를 2회 export해 파일명/수량/UTF-8/해시/멱등성·기존 수동 편집 보존을 검증.
3. Work-root `MSC_VIEW.md`→실제 HTML `published_path`와 Converter 상세 원본 MD→AS-IS/TO-BE HTML **두 링크를 각각** 검사. 깨진 내부 링크는 공유 HOLD하거나 승인된 viewer 레이어에서만 정규화; 원본 Evidence byte 변경 금지.
4. 상대·절대·URL 인코딩 traversal, symbolic/hard links, hidden file, 대소문자/NFC, 전자적 파일 서명/자산 누락, HTML inline JS/외부 연결/iframe/CSP·SVG 공격 반례 시험.
5. 개인 viewer와 공유 viewer는 web docroot/search index/cache/asset을 별개로 설계. viewer는 원본 source code·Knowledge root 직접 서빙하지 않음.
6. 실패 시 publish 거부하고 마지막 승인된 viewer snapshot 유지; 작업 원본 불변.

**수락**: 실제 호스트에서 G1(비Git Kernel export), G2(해시/링크/부정시험), 증거/실패 조건이 명확해야 P2 후보.

### P2. 개인 SHADOW 웹 뷰어 — 별도 허용된 실행 승인 후

1. 기본 가정은 `localhost` 개인 접근만. 기존 승인 웹 서버를 우선 재사용; MkDocs/새 서비스 설치를 자동 결정하지 말 것.
2. 원본 → 읽기 전용 export → 검사된 staging → 원자적 publish → 승인된 localhost viewer. 원본 Work/Knowledge 디렉터리를 웹 서버 루트에 직접 연결하지 않음.
3. UX: `Work Overview → 분석·결정 → Evidence/MSC(HTML+SVG) → 그룹 반영 상태`, Work ID·Module/Feature/Scenario/Procedure·AS-IS/TO-BE·source revision 표기.
4. 실제 브라우저에서 Markdown·HTML·MSC 확대/스크롤/모바일 레이아웃·URL 직접 열기·링크 2종·수정 불가·검색 색인 확인.
5. 서버/빌드 실패 시 viewer만 중단·재생성. Git/원본/그룹 게시 기능에 영향 0.

**수락**: G3/권한·열람 시험 PASS, 상세 실패 목록 및 rollback 가능.

### P3. 동료용 선택적 읽기 전용 Viewer — 조직/호스트 승인 후

1. `allowlist`에 없는 Work는 메타데이터·search·asset·직접 URL까지 403/404. 기본 공유 0건.
2. 사용자/그룹 인증(SSO 또는 기존 승인 인증), HTTPS, 감사, 로깅 최소화, 권한별 색인 분리와 만료를 실증.
3. 개인 PC 가용성에 의존하면 공유 상시 서비스로 과장하지 말고 공용 read-only 사본 대안 평가.
4. 승인된 Work 요약/MSC만 게시. 원본 코드·로그·비밀·고객 관련 자료를 전사·PRIVATE GitHub·PUBLIC GitHub로 자동 전송하지 않음.

**수락**: G4, 두 계정 A 허용/B 거부·직접 링크·색인·캐시 부정시험 통과, 별도 서비스 운영 승인 확인.

### P4. local authority 전환의 설계·코드 준비 — 별도 코드 독립 리뷰 필요

1. Local mode를 기본 OFF. 기존 Workflow `docs_sync/docs_push` 기능(registered origin/clean tree/remote readback)은 기본 모드에서 **변경 없음**.
2. 실제 설치본에 없는 계약을 발명하지 말고 `LOCAL_EXPORT/LOCAL_VERIFY`와 git 원격 publish를 분리할 **최소 diff**를 G0 기반 제안. responsibility: Workflow=흐름, Kernel=Work/Evidence/export, Git skill=provenance, Converter=HTML/MD, Knowledge Updater=승인 지식 writer.
3. provenance/work ID/증거 SHA, 단일 writer, lock/revision CAS, partial failure/중복 방지, 오프호스트 백업·restore, 기존 consumer/manifest 호환성을 각각 실측.
4. 원본 Git remote/HEAD/history/dirty/미완료 작업 사전 snapshot, 복원 시험. 백업 없는 정본 cutover 금지.
5. 실제 source revision과 권한/복구 RPO·RTO 미확인은 `BLOCKED`.

### P5. local authority CUTOVER — 사용자 명시적 운영 승인과 전 게이트 PASS 후에만

1. 작업 writer freeze·진행 Job 0 확인, 원본 저장본·SHA/size/revision·백업/복원 receipt 고정. 이중 writer/양방향 자동 sync 금지.
2. 승인 범위 내 1개의 비민감 synthetic/선별 Work로 read/write/export/rollback을 검증. 원본 Git remote 삭제·force push·자동 rebase/reset/stash/cherry-pick 금지.
3. GitHub mode로 복귀 가능하다고 실제 확인하기 전 기존 Git Writer 의존은 유지. Local authority가 모호하면 즉시 STOP, 양측 이력 보존.
4. 그룹 Knowledge E3는 개인 Work 전환과 **별도 승인·게시 revision/readback**으로 검사; 그룹 게시 성공·Work 역링크 실패 시 그룹 재게시하지 않고 link만 복구.

### P6. 수락/복원·확산 — 증거 기반

- Linux 재시작·viewer 장애·네트워크/Git 원격 장애·백업 복원·원본 변경 충돌·동료 권한·유출 부정시험, 그룹 E3 CAS 충돌/불확실 응답/역링크 실패를 재현.
- 위 장애 중 원본·Knowledge 정본 손상 0, viewer 재생성, 원래 Git 경로 복구 가능성·실제 책임자 인수 증거를 확인.
- 일정/관찰 기간은 운영 승인된 SLA 기준으로 별도 설정. 미측정이면 완료 선언 금지.

## D. Gate와 실패 안전 정책

| Gate | PASS 필수 | FAIL/HOLD 시 수행 |
|---|---|---|
| G0 | A~P 실제 읽기 전용 설치·권한 근거, G0 blocker 명시 | P0 외 실행 보류 |
| G1 | 합성 로컬 export, hash·idempotence·manual-edit 보존 | Kernel 최소 보완 검토만 |
| G2 | asset/link·Traversal/SVG/HTML/security negative | 해당 Work web publish HOLD |
| G3 | 개인 localhost 웹 브라우저·권한 실증 | 기존 Git 유지 |
| G4 | 동료 HTTPS/SSO/ACL·allowlist·cache test | 공유하지 않음 |
| G5 | 단일 writer·Git provenance 동등성·오프호스트 복원·독립 코드 리뷰·명시적 승인 | Local cutover 금지 |
| G6 | Group Updater Preview/CAS/승인·readback·Work 역링크 E3 | Group write 보류, Work 원본 보존 |

- `PASS` = 실제 실행·증거, `FAIL` = 확인된 결함, `SKIP` = 조건 불해당, `NOT_RUN` = 실행되지 않음. 소스/문서 추정은 G0·E3 PASS가 아님.
- **원본 / 파생 viewer / 그룹 Knowledge** 3 영역 각각 별도 실패 상태·rollback. 성공 불명확 응답은 이력 조회 우선, 재실행·재게시 금지.
- HTML 링크의 Work 안내 PASS가 Converter 상세 MD 내부 링크 PASS를 뜻하지 않음. 상세 MD 파생본 처리 없이 공유하면 G2 HOLD.

## E. 스킬 변경 최소화 표

| 스킬 / 컴포넌트 | 기본 책임 | 현재 단계 |
|---|---|---|
| `work-ledger-kernel` | Work ID·Ledger/Evidence·export | 합성 export 재사용, 실 설치 G0 대조 |
| `l1-fix-workflow` | Work 재개·분석·Git docs publisher | 기존 Git mode 보존, local 경로 최소 분리 검토 |
| `l1-github` | remote / provenance / repo role | 변경 없이 의존·호환성 G0 확인 |
| `doc-converter` | HTML+SVG/Markdown·MSC 링크 | 두 종류 링크 검증, 원본 무변조 |
| `l1-knowledge-updater` | 두 진입 후보·Preview·그룹 writer 연결 | 실제 설치 G0, writer 승인/CAS/readback 근거 |
| 기존 웹 호스트/MCP | 인증·문서 읽기 전용 서빙 | 기존 서비스 재사용·부족한 기능만 최소 EXTEND |

**불필요한 신규 구현 금지**: 새 DB, 양방향 sync 엔진, 별도 RAG 엔진, 새로운 저장소·인덱스·승인 스키마, 맹목적 plugin/서비스 설치.

## F. 단일 보고 양식 (업무 GPT가 단계별 회수)

```text
WORK: L1 Workspace Local Viewer Transition (same existing Work)
HOST_G0_A_TO_P: <16 numbers or NOT_RUN>
ACTUAL_INSTALLED_SOURCE: VERIFIED / PARTIAL / NOT_VERIFIED
GATES: G0=... G1=... G2=... G3=... G4=... G5=... G6=...
TESTS: PASS n / FAIL n / SKIP n / NOT_RUN n
SOURCE_AND_BACKUP: verified | unverified (redacted; no absolute path)
DOC_LINKS: work_root_html=... ; converter_detail_html=...
SECURITY: allowlist=... ; auth=... ; index_acl=... ; local_only=...
GROUP_WRITER: preview=... ; CAS=... ; readback=... ; reverse_link=...
NO_MUTATION: YES / NO (explain within allowed business environment)
BLOCKED: precise conditions and needed approval
ARTIFACTS: local protected report IDs; version and SHA-256 only if safe to disclose
NEXT_ONE_ACTION: exactly one permitted next step
```

## G. 리뷰 후 최종화해야 하는 항목 (현재 미완료)

1. Windows Claude 독립 R01~R22 실제 `REVIEW_RESULT`/영수증/approval input 결속 확인.
2. GPT 지적별 `수용/수정수용/거절/보류/추가 확인` 판정, 심각도별 차단조건 업데이트.
3. 해당 실제 리뷰 의견에 따른 범위·반례·테스트/단일 writer/백업/보안 수정.
4. 비민감 최종 업무 GPT 인계 MD를 L1Work PUBLIC `main/handoffs/`에 게시·원격 UTF-8 본문/바이트 SHA-256 확인.
5. 업무 G0 결과 수신 이후 **호스트에서만** 실제 수정 명령·설치 여부·URL/권한·롤백 절차를 구체화. 리뷰 자체는 Linux 설치 검증을 대신하지 않는다.

**판정**: 기술 제안·단계별 범위는 준비됨. 리뷰 및 실제 설치본 G0 전에는 `OPERATING_CHANGE=BLOCKED`; 업무 GPT에게 전달되는 것은 **읽기 전용 G0 요청**과 **후속 수행을 위한 설계 초안**이지 운영 승인된 변경 지시가 아님.
