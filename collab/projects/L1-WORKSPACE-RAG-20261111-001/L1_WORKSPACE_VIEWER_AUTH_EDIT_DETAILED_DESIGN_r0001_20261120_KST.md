# L1 Workspace Viewer — 인증 기반 편집 상세 설계 r0001
- 일자: 2026-11-20 KST
- Work: L1-WORKSPACE-RAG-20261111-001
- 성격: DESIGN_PROPOSAL / INDEPENDENT_DESIGN_REVIEW_INPUT
- 범위: 기존 별도 Linux Read Only Viewer의 인증 후 편집 확장. 구현·배포·호스트 실행 지시 아님.
- 출처: 기존 CURRENT, 11/19 Viewer UI v0.1.0 개발 결과, 11/20 UI 연동 검토·PUBLIC Viewer 변경서 r0002, 사용자 대화 결정.
- 사용자 확정: 기본 Read Only / [수정] 노출 / 클릭 때 ID·비밀번호 입력 / 권한 확인 후 편집 화면 / 직접 편집·수정 요청 / Diff·Preview 후 저장 / MSC 메시지·participant 요청까지 1차 포함.

## 1. 목적과 비목표
목적은 현재 열람 중인 이슈 분석/MSC를 안전하게 보완하되, 원본 Evidence·기존 조회 권한·코드 사실과 기술 지식의 정본 분리를 보존하는 것.
포함: 분석 본문, 코멘트, MSC 설명, MSC 메시지, participant의 수정 또는 추가 요청; 개인 초안/개정본; 버전 비교·충돌·복구·readback.
제외: 새 RAG/검색/DB/원장 엔진, 사용자 계정 저장소 자체 구현을 기본 전제로 삼기, Viewer가 Knowledge 직접 게시, 그룹 무승인 게시, 임의 Job 실행, 제품 코드 수정, 기존 Work 자동 재분석, 운영 설치·접속 범위 변경.
기존 viewer-wiki-ui_v0_1_0은 합성 데모(브라우저 56 PASS·정적 19 PASS)이고 11/20 UX 개선 HTML은 별도 시안. 실제 Linux Viewer의 repository/branch/commit/auth API는 G0 미확인. 설계에 적은 인터페이스 이름은 논리 계약이며 설치 API 명칭이 아님.

## 2. 기존 책임과 설계 판단
| 구성 요소 | 현행 확인/설계 | 편집 확장의 소유 범위 | 결론 |
|---|---|---|---|
| Linux Viewer | UI·읽기 handler, 실제 구현 미확인 | Read Only 유지, 수정 진입·권한 UI·편집 패널·비교 화면·검증된 서비스 요청 | CONNECT / G0 확인 |
| l1-fix-workflow | 기존 Work 진입/연속성·MSC_VIEW 원본 텍스트 읽기 | 기존 Work 선택·개정 처리 조정 | REUSE |
| work-ledger-kernel | Work/Evidence 원장·SHA·기존 export/writer | 원본을 보존한 Work 개정본·Evidence·revision/readback | REUSE / 실제 writer G0 확인 |
| l1-knowledge-updater | 개인 Knowledge 후보·그룹 Preview/승인·readback 책임 | 개인 Knowledge 대상 저장/검토, 이후 그룹 반영은 별도 | REUSE / 실제 설치 계약 G0 확인 |
| doc-converter | canonical MSC 입력→B형 HTML/SVG | 검증된 원본 변경 후 렌더 재생성, HTML은 편집 정본이 아님 | REUSE |
| code-analyzer / Agent | 기술 사실 분석 근거 | 기술 의미가 바뀌는 메시지·participant 요청 검증에만 선택적 호출 | CONDITIONAL_CONNECT |
| l1-github/실제 Git writer | 허용된 게시와 충돌 관리 | 기존 인증·commit/readback·복구를 재사용 | REUSE / G0 |

기존 Viewer는 서비스 UI이지 스킬 실행 허브가 아님. Agent/MCP 기존 스킬 접근 경로는 별도. 편집 요청이 필요할 때만 허용된 업무 실행 경로를 사용하며 Viewer 조회만으로 분석/Job/게시를 실행하지 않음.
Knowledge 직접 작성은 Updater 진입, 이슈 Work 개정은 Workflow/Kernel 진입으로 유지. 순수 Knowledge 작업에 새 Work ID 발급을 강제하지 않음. 동일 원본을 두 저장소에 자동 fan-out하지 않음.

## 3. UX 상태·권한·인증 시퀀스
상태: READ_ONLY → AUTH_DIALOG → AUTH_PENDING → (EDIT_AUTHORIZED | AUTH_DENIED) → EDIT_DIRTY → DIFF_PREVIEW → (DRAFT_SAVED | COMMIT_PENDING | CONFLICT | SAVE_ERROR) → READ_ONLY.
초기 화면은 현재와 동일한 좌측 탐색·중앙 본문·우측 목차, [수정] 버튼만 추가. 편집 아이콘/버튼이 노출돼도 서버 권한을 뜻하지 않으며 모든 내용/다운로드/검색은 현재 조회 ACL 유지.
사용자 [수정] 클릭 → 같은 화면 위의 모달에 ID/PW 입력 → 기존 호스트 인증 서비스 재인증 + 해당 문서/Work/Knowledge edit ACL 확인 → 성공 시 현재 문서·스크롤·검색/MSC 선택을 유지하고 우측 편집 패널 활성. 실패 시 입력 초기화, 상세 계정 정보 비노출, Read Only로 복귀. 비밀번호의 JS 상태 최소화·디스크/localStorage/URL·로그·본문·Agent 프롬프트 저장 금지. Viewer 자체 계정 DB 신규 개발 금지.
로그인 후 자격 증명과 편집 세션은 서버 관리. 인증 만료·로그아웃·권한 회수는 새 API 호출/저장 시 서버 측 재검사; 화면 표시만으로 권한 허용 금지. 재인증 세션 사용 범위·TTL·rate limit·계정 잠금·CSRF·SameSite/HttpOnly/Secure cookie·TLS·클릭재킹 방어는 기존 서비스 정책을 G0 대조 후 최소 보완. 인증 불가/세션 만료 때 원본 쓰기 0. 사용자 편의성: 편집 종료 시 읽던 위치 복귀, 미저장 변경 경고, 키보드·모바일 초점 복원.
동료 읽기만 계정은 인증 성공해도 EDIT_DENIED. 인증된 편집자도 해당 소스별 write 권한과 그룹 게시 권한을 별도로 확인. 편집 로그인 = 그룹 게시 승인 아님.
표현: Read Only / 편집 중(초안) / 미저장 / 검증 필요 / 충돌 / 저장 확인됨 / 게시 확인됨을 구분. 미확인 필드는 UNKNOWN, 상상 속 PUBLISHED 표시 금지.

## 4. 편집 UI·항목별 기능
데스크톱: 기존 위키 3영역 유지, 우측 목차를 필요 시 접고 편집 패널로 대체. 중앙 본문/MSC 배율 및 좌측 탐색 유지. 모바일: 편집 패널을 독립 드로어로, 본문/MSC와 왕복 시 초점·읽던 위치 유지. 기존 P1 두 건(실제 MSC 넘침 방향 안내·CSS 중복 정리)과 U01/U02(문서 위치·탭별 마지막 문서) 작업은 편집 UI 변경과 충돌하지 않도록 같은 회귀 계획에 포함하되 완료로 소급 금지.
- 이슈 분석 본문: 문단·절 선택 → 내용 수정/추가 → 최소 Markdown 편집 + 원문 비교. 문제/원인/해결, 증거·검증 상태를 임의 승격하지 않음.
- 코멘트: 문단 또는 MSC 단계에 연결되는 주석 추가. 기술 사실 수정과 표시용 주석을 구분. 원본 Evidence의 무단 본문 덮어쓰기 금지.
- MSC 설명: phase/message 설명 편집. 출력 표현·상세 설명 변경과 순서·발신/수신 의미 변경을 구별.
- 메시지: MSC 화살표 선택 → stable source anchor와 실제 원본 일부 확인 → 표시 문구 수정 또는 방향/순서/추가/삭제 의도 지정 → 기술적 의미 변경이면 Agent 검증 요청과 결과를 표시. 설명만 바꾼 경우는 실제 코드 분석 자동 재실행 금지.
- participant: lane 선택 → 표시 이름/통합 alias(예: TxCfgMngr·TxCmdMngr→TxMngr)와 실제 canonical participant 존재/통신 대상을 별도 편집 의도로 분리. 마지막 폴더명 표시 정책은 기존 doc-converter에 맞춤. 실제 participant 추가/삭제는 근거 검증 없으면 확정 금지.
복수 편집은 한 문서의 대기 변경 목록에 모으되 하나의 항목 실패로 다른 독립 초안까지 자동 폐기 금지. UI에서 원본이 아닌 rendered HTML/SVG DOM을 canonical로 간주하지 않음.

## 5. 메시지·participant 수정 식별 및 근거 계약
Viewer에서 선택 가능한 원본 메시지/participant 목록은 서버가 허용한 canonical source와 연결돼야 함. 3번째 화살표 같은 화면 위치, arbitrary DOM text, SVG 좌표, 사용자 입력 경로만으로 write 대상 확정 금지. 기존 저장 포맷에서 지원되는 immutable ID/anchor/source revision/hash를 먼저 확인. 식별자가 없으면 read-only 설명/수정 요청을 유지하고 즉시 구조적 확정 저장은 HOLD. 신규 영속 ID/manifest/schema는 G0 gap 입증 후에만 최소 설계.
수정 제안은 최소 논리 필드: 대상 소속(Work 또는 개인 Knowledge), source anchor/revision/hash, 편집 의도(TEXT / DESCRIPTION / STRUCTURAL), 후보 변경, 원본 근거·근거 상태(FACT/INFERENCE/UNVERIFIED), 검증 주체, 승인 선택. 이 필드는 교환 의미 목록이며 새 DB schema 제안이 아님.
Agent 호출 조건: 메시지 순서·발신/수신·시점·조건·participant 실제 개체 등 기술적 의미 변경. 기존 코드 근거가 명확하면 재사용, 필요한 범위만 code-analyzer/도구 조회. Agent가 source revision·검토 범위·정확성·미확인을 반환. 분석 결과 자체를 승인/PASS로 취급하지 않음. 미확인·모델 실패 시 변경 요청은 초안으로 보존 가능하되 확정/Knowledge 승격은 HOLD.

## 6. 저장 플로우·원본 보존
1. GET/read: 현재 허용 범위 안의 canonical revision/hash, 소속 owner, 원래 Work/Evidence 링크 또는 Knowledge ID를 서버에서 조회.
2. EDIT: 사용자 편집 초안은 원본과 분리. 세션 내 임시 수정은 UI 상태, 서버 초안 저장은 기존 개인 writer/허용 경로가 있는지 G0 대조. 초안 저장 성공에 readback 필수, Knowledge 게시 성공을 뜻하지 않음.
3. DIFF: base→candidate 줄/필드/메시지/participant 단위 비교 및 근거 설명. Preview는 허용된 source에서 격리 렌더, 실제 저장본과 구분.
4. COMMIT: 권한·대상·base revision/hash의 stale 검사(CAS/3-way 제공자가 있으면 재사용), canonical source 변형 허용 여부와 구조 변경의 기술 검증을 대조. 양호한 경우에만 기존 Workflow/Kernel 또는 Updater writer에 정확히 한 번 개정 요청.
5. RENDER: canonical MSC 성공 후 기존 doc-converter의 B HTML/SVG를 재생성. canonical 변경과 파생 HTML 생성의 성공/실패 상태 분리. 변환 실패로 저장 완료를 거짓 표시하거나 모델/분석을 자동 재호출하지 않음.
6. VERIFY: write receipt 및 실제 원격/로컬 허용 readback으로 revision/hash·target link 확인. Work 원본과 Evidence 변경 이력 보존; 그룹 지식 반영은 Updater 후보/Preview/승인/기존 writer/고정 revision/readback 별도.
7. EXIT: 사용자 저장 확인 뒤 Read Only 복귀. 재인증 편집 세션은 종료/만료 처리. 부분 실패·미확인 상태를 사용자에게 분명히 노출.
권장 오류 분류: AUTH_DENIED, PERMISSION_CHANGED, INVALID_TARGET, SOURCE_STALE, SEMANTIC_CONFLICT, ANALYSIS_UNVERIFIED, WRITE_FAILED, WRITE_UNCERTAIN, RENDER_FAILED, READBACK_FAILED. 저장 성공·렌더 실패면 원본 재저장 금지; 출력만 수동 복구.

## 7. 충돌·복구·감사
base/theirs/ours의 3-way 비교를 원칙으로 하며 revision/hash 불일치 시 강제 덮어쓰기 금지. 독립된 코멘트의 병합은 기존 writer가 확실히 지원하는 경우에만; 메시지 순서·참여자 alias 충돌·출처 참조 변경은 NEEDS_USER_DECISION.
동시 편집: 서로 다른 세션도 동일 revision 재확인, 서버에서 권한 검증. 실행 불확실·중복 요청은 멱등키 등 기존 writer 보장을 확인하고 UNCERTAIN 유지. 임의 재실행·삭제·원장 재작성 금지.
복구: 이전 확정 revision을 새 복원 후보로 제안, 사용자 Diff·확정 및 readback. 원본 Evidence/감사 기록 삭제·파일 직접 overwrite 금지. 초안 폐기와 확정 이력 rollback을 분리. source SHA/size/버전/작성자/타임스탬프/변경 근거를 기존 기록 계약에 연결하되 새 메타 원장을 기본 요구하지 않음.
원본 출처가 Work인지 Knowledge인지에 따라 단일 소유 writer 적용. 개인 초안 보존 위치·그룹 동시 편집 보호, readback/역링크의 실제 API는 G0에서 확정.

## 8. 보안 경계와 실패 차단
기존 B1: canonical root/path containment, ../·encoded traversal·symlink/TOCTOU·hardlink·허용 외 경로·변경 대상 파일 권한을 읽기/쓰기 모두 부정 시험.
기존 B2: 제한자료·비밀 패턴을 HTML뿐 아니라 raw/search/related/cache/download/preview/diff/comment/Agent 입력/오류 로그에도 동일 적용.
기존 B3: MSC B HTML은 별도 origin/sandbox/CSP로 격리. 읽기 렌더 iframe에 인증 쿠키·편집 권한·임의 JS bridge를 열지 않음. 편집 요청은 부모 Viewer가 인증된 canonical 선택을 서버에 전달하고 서버가 별도 검증; iframe DOM 직접 수정 금지.
신규 EAuth: 편집 버튼 노출·URL 직접 호출·CSRF·권한 없음·세션 만료·계정 잠금·브루트포스·이중 제출·편집자→관리자 권한 상승 부정 시험. 비밀번호·세션 비밀을 GitHub/Agent prompt/브라우저 persistent storage에 두지 않음.
추가 검토: XSS/Markdown sanitizer, stored comment injection, prompt injection을 통한 Agent 도구 오남용, 임의 경로·명령·네트워크 전송 차단, 요청 비용/호출 횟수 제한. Windows Claude 리뷰어는 회사 L1 소스에 접근 불가하므로 설계/공개 합성 아티팩트만으로 리뷰. 실제 보안 검증 PASS 아님.

## 9. 구현·검증 단계(후속 범위, 이번 실행 안 함)
G0 읽기 대조: 실제 Linux Viewer 저장소/브랜치/revision, 인증/ACL, handler/MSC, 개인 초안 writer/업무 Work writer, Updater와 Converter의 실제 API·버전. 이미 받은 G0 일부 보고 재사용, 사용자에게 원문 반출/수동 진단 재요구 금지.
D1 설계 리뷰: 이번 r0001 독립 구조/보안/사용성 정적 R1 1회 → GPT 판정, 설계 보완.
D2 구현 기반: v0.1.0 최신 UI 및 P1·필요한 U01/U02와 인증 모달·편집 패널의 좁은 추가. 기존 readonly 경로·쓰기 차단 회귀.
D3 기능: 이슈·코멘트·설명 직접 편집 + 메시지/participant 정밀 선택/수정 요청; 우선 합성 fixtures, 실제 renderer와 분리.
D4 연결: 기존 writer·업무 Agent 검증·Converter. 확정 저장/초안/그룹 게시 권한·실제 API 확인 후 필요한 부분만.
D5 시험: 인증·편집·충돌·복구·원본 SHA·B1~B3·EAuth, Linux localhost E3, 별도 승인 공유 E4, 1440/720/390/320 및 MSC 6/12명·긴 phase/스크롤.
D6 배포: 격리 시험과 독립 코드 리뷰·권한/운영 승인·백업/rollback을 각각 판정. 이번 설계 리뷰가 운영 변경 승인 아님.

## 10. 첫 구현 수락 시나리오(예시/시험 계획, 수행 NOT_RUN)
T01 Read Only 미인증 사용자는 조회·검색만 가능, 직접 쓰기 API 거부.
T02 수정 클릭→ID/PW 입력·편집자 승인→원래 문서 위치에서 EDIT 진입.
T03 잘못된 자격증명·읽기 전용 동료·권한 회수·세션 만료는 fail-closed/원본 불변.
T04 이슈 본문·코멘트·MSC 설명 수정→Diff/Preview→개인 초안 저장/readback; 원본 SHA 불변.
T05 Agent 없이 단순 설명/오탈자 수정; 분석 자동 호출 0.
T06 메시지 화살표 선택→원본 anchor 식별→순서 변경 요청→근거 불확실 HOLD.
T07 메시지 방향/순서/추가/삭제 제안→source 확인된 경우에만 canonical 수정·Converter 재생성.
T08 participant 표시 alias 변경과 실제 참가자 구조 변경을 구분, 임의 raw label만으로 수정 금지.
T09 base stale·권한 변경·동시 수정 충돌에서 원본 overwrite 0, 3-way 비교 및 사용자 선택.
T10 저장 성공·렌더 실패는 부분 성공 표시, 원본 write 재실행 0.
T11 저장 이후 readback SHA 불일치/불확실은 완료 표시 금지, 복구/중복키 감사.
T12 이전 revision 복원 후보→Diff→기존 writer 새 revision으로 적용, Evidence 이력 보존.
T13 Work 분석 개정이 Knowledge에 자동 게시되지 않음; 그룹 반영에는 별도 승인.
T14 raw/search/download/cache/preview/diff/Agent 모두 제한자료 권한 유지, 경로 우회·HTML/XSS 격리 시험.
T15 1440/390/320 PC·모바일 편집/복귀·키보드·화면 6/12 participant; 읽던 위치·가로 넘침 안내 유지.
T16 비밀번호·인증/서명비밀 미로그·미게시·저장 없음, 재인증 세션 관리 확인.

## 11. 독립 설계 리뷰 요청 질문(비판적 검토)
R01 로그인 뒤 편집 진입만으로 서버의 write ACL 우회를 막을 수 있는가? 권한 회수·세션/CSRF·브루트포스에 대한 필수 선행 조건은?
R02 기존 별도 origin MSC와 우측 편집 패널의 데이터·선택 동기화에서 B3가 무너지는가? 안전한 대안은?
R03 canonical MSC selection ID가 없을 때 첫 구현 메시지/participant 요청을 어디까지 허용할 수 있는가?
R04 source code 검증과 표시 alias 수정, 설명 문구 변경을 구분하는 기준은 현실적인가?
R05 Work/Evidence와 개인 Knowledge 두 writer 경로의 저장 책임이 충돌하거나 원본/파생 HTML 상태가 섞이지 않는가?
R06 초안 저장/확정 저장/그룹 게시의 실제 권한·source revision·CAS 실패/부분 실패 설계에 누락은?
R07 기존 UI P1/U01/U02 개선과 편집 추가의 개발 순서·회귀 전략에 과도한 의존 또는 UX 회귀는?
R08 B1~B3 외에 필수 보안 위협(XSS, prompt injection, credentials, raw/download/diff leakage, replay)이 누락됐는가?
R09 G0 미확인 사실을 새 API/DB/schema로 과도하게 확정한 부분과 REUSE 대안은?
R10 제한된 저사양 LLM·업무 Agent 상황에서 안전하면서 더 단순한 첫 구현의 최소 범위는?
각 이슈는 severity BLOCKING/MAJOR/MINOR, 근거 설계 절·사용자 영향·반례·최소 수정 제안·검증법으로 제출. 비차단 개선은 근거가 있는 경우에만. 기능 부재 단정/설계 PASS=호스트 PASS 금지.

## 12. 관련 고정 참고
- PRIVATE main: collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md
- PRIVATE main: collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_WIKI_UI_IMPLEMENTATION_RESULT_r0001_20261119_KST.md
- PRIVATE main: collab/projects/L1-WORKSPACE-RAG-20261111-001/WIKI_UI_SKILL_INTEGRATION_COMPATIBILITY_REVIEW_r0001_20261120_KST.md
- PRIVATE main: collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_WIKI_UI_UX_R1_DISPOSITION_r0001_20261119_KST.md
- PRIVATE main: collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_MSC_DUAL_ENTRY_DOCUMENT_DESIGN_r0001_20261117_KST.md
- PUBLIC wonhwipark/L1Work/main/handoffs/L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md
본 문서는 비민감 설계만 포함하며 회사 제한 코드·상세 MSC·로그·계정·비밀·호스트 절대 경로를 포함하지 않음.
