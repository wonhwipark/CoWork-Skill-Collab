# 위키 UI × 실제 사용 스킬 연동 적합성 검토

- Work: L1-WORKSPACE-RAG-20261111-001 / 2026-11-20 KST / GPT 정적 검토
- 판정: CONDITIONAL_CONNECT. 책임 분리는 재사용 가능하나 현재 HTML을 실제 서비스에 그대로 연결하는 것은 불가
- 범위: 최신 PRIVATE 계약, 최신 PUBLIC 패키지 3종의 SKILL/관련 구현, v0.1.0 UI 및 개선 시안 대조. 실제 Linux 설치 소스·API·업무 데이터·계정·운영 서비스 미접근
- 실제 결과: ZIP 3종 Git blob/크기·CRC 확인 PASS, 관련 계약/코드 정적 대조 완료. 실제 API 통합·스킬 실행·Linux 브라우저·두 계정 시험 NOT_RUN

## 1. 무엇이 UI를 사용하는가

UI는 스킬을 실행하는 화면이 아니라 별도 Linux Viewer의 읽기 화면이다. Workflow/Kernel/Updater/converter가 생산·관리하는 기존 문서와 Evidence를 Viewer의 읽기 API/형식별 handler가 제공하고, UI가 이를 표시한다. 조회 버튼으로 분석·변환·게시 스킬을 자동 호출하는 구조를 추가하지 않는다.

| 대상 | 실제 원문/설계에서 확인한 책임 | UI와 연결할 부분 | 판정 |
|---|---|---|---|
| 기존 Linux Viewer | 실제 소스·브랜치·revision·API·인증은 미확인 | 화면 asset, 읽기 adapter, 문서/MSC handler, 권한·검색·캐시 | 직접 변경 대상. 설치 계약 G0 필요 |
| l1-knowledge-updater | r0004 계약상 개인 Knowledge 관리·분류·그룹 Preview/승인 게시·readback·역링크의 관리 주체 | 기존 지식 ID·탐색/메타정보를 읽기 매핑 | 계약 재사용. 설치 SKILL/소스 직접 미확인 |
| l1-fix-workflow 1.6.74 PUBLIC | Work 조회·연속성·group-knowledge 읽기 연결. MSC_VIEW는 저장된 원본의 텍스트 흐름 조회 | Work 요약·Evidence 참조·기존 읽기 정보 | REUSE. MSC_VIEW를 HTML API로 간주 금지 |
| work-ledger-kernel 0.7.42 PUBLIC | Work/Evidence 원장·기존 export·published mapping·원본 SHA 대조. HTML/명시적 MSC SVG export 경로 존재 | 기존 Work ID/Evidence ID/배포 상대 경로·SHA | REUSE. UI용 새 원장·writer 불필요 |
| doc-converter 0.2.26 PUBLIC | msc_b_viewer.py에서 실제 SVG를 내장한 B형 HTML 생성, 배율·단계 이동·메타 표시 | 생성된 HTML 원본을 기존 격리 handler로 열기 | REUSE. 합성 SVG를 실제 MSC로 사용 금지 |
| code-analyzer / hld-composer | 기존 기술 사실/HLD 입력 책임, 이번 직접 원문 감사 대상 아님 | 이미 생성된 결과 참조 | UI 도입을 이유로 신규 실행 요구 없음 |

공개 ZIP이 최신 설치본이라는 뜻은 아니다. PRIVATE 11/17 분석표보다 PUBLIC main에 더 최신 Workflow/doc-converter가 있어 이번에 실제 바이트를 읽어 확인했다. 업무용 Updater는 PUBLIC 루트에 없어 구 l1-knowledge-manager로 대체하지 않았다. G0 일부 호스트 보고는 기존 근거로 재사용하되 Viewer 전체 설치/API 확인으로 확대하지 않는다.

## 2. 확인된 연결 변경점

| ID | 확인한 근거 | 그대로 붙일 때 문제 | 필요한 최소 조치 |
|---|---|---|---|
| I-01 | 개선 시안 documentView가 window.WikiFixtures.trees를 직접 참조. adapter도 fixture 기반 | fixture를 제거하고 adapter만 바꾸면 탐색 링크 생성·이동에서 오류 가능. 실제 문서 소속을 찾을 수 없음 | 화면의 fixture 직접 참조 제거. 기존 읽기 목록/분류로 소속과 진입 맥락을 해결. msc- ID 접두사 대신 실제 문서 종류/연결 정보 사용 |
| I-02 | HTML CSP는 connect-src none, frame-src none | 실제 API 요청과 MSC iframe을 허용하지 않는 데모 정책 | 실제 승인된 인증/origin에 맞는 운영 CSP 구성. 제한적인 데모 meta를 유지한 채 헤더만 덧붙이는 방식으로 처리하지 말고 운영 asset·헤더 정책을 함께 대조. 와일드카드/토큰 하드코딩 금지 |
| I-03 | renderMsc는 synthetic-placeholder만 처리. 실제 url은 사용하지 않음 | adapter가 실제 MSC 주소를 반환해도 열리지 않음. 텍스트 MSC_VIEW 출력으로 HTML을 대체할 수 없음 | doc-converter 기존 B형 HTML을 서버 허용 대상에 매핑해 격리 열람. 승인된 별도 origin·sandbox·CSP·asset/다운로드 정책 검증 |
| I-04 | 데모 Markdown/JSON/BINARY 분기와 doc: 링크 사용 | 기존 Markdown 확장·로컬 상대 링크·SVG/PDF/이미지 handler가 자동 호환되지 않음 | 기존 renderer/링크 resolver/형식별 handler 재사용. 본문 일괄 재변환이나 링크 rewrite 금지 |
| I-05 | 검증 표시가 SYNTHETIC_ONLY 외에는 미확인, byline/설명에 합성 문구 존재 | 실제 검증/게시 의미를 표현하지 못하거나 실제 자료에 합성 문구가 남음 | Updater/Kernel 실제 원천과 표시 매핑. 검증/수정/시험/게시 상태를 구분하고 모르는 값은 미확인. fixture-r1/PUBLISHED 예시를 실제 성공으로 사용 금지 |
| I-06 | buildTree가 하위 노드를 재귀 조회. listRoots/listChildren은 pagination 없는 fixture 예시 | 실제 전체 트리의 누락·대량 조회 지연 가능. UI 검색 범위와 호스트 권한도 미검증 | 기존 API의 pagination·재귀/크기 제한 대조. 권한 있는 노드만 조회하고 규모/지연 측정 후 필요한 최소 lazy load 판단 |
| I-07 | 개선 시안의 읽기 위치/배율은 열린 창 메모리와 부모 DOM에 저장 | 새 revision·계정 변경 또는 별도 origin MSC의 내부 상태까지 자동 복원된다고 볼 수 없음 | 부모 문서 위치부터 복원. 권한/문서 현재성 재확인. child MSC 배율/위치 보존은 별도 검증된 계약 없으면 범위 제외. 동일 origin 합치기로 해결 금지 |

위 항목은 데모의 의도된 경계를 포함한다. 현장 스킬에서 실제로 장애가 발생했다는 보고가 아니다. 특히 I-01은 이번 개선 시안에 추가된 구현 의존성으로, 이전 v0.1.0의 독립 리뷰 결과가 이 추가 코드를 검토한 것으로 취급하지 않는다.

## 3. 코드에서 확인한 재사용 근거

- doc-converter/scripts/msc_b_viewer.py: build_html은 SVG를 data:image/svg+xml로 내장하고 source revision·kind·participant/message 수를 기존 context에서만 표시. 자체 CSP는 해시 스크립트·connect-src none을 사용하며 호스팅/게시 기능은 제공하지 않음. PROCEDURE_FEATURE opt-in과 기존 SVG 성공 조건 보존.
- Workflow의 docs/MSC_VIEW_AGENT_READONLY.md와 l1_fix_workflow/msc_view.py: Work evidence_index에 등록된 원본의 SHA를 대조하여 메시지 흐름을 반환. read_only=true, provider_executed=false, saved=false. HTML URL/서비스를 제공하는 경로와 구분 필요.
- Kernel work_ledger_kernel/work_ux.py 856~894행: 기존 Evidence 상대 경로·Work containment, 명시적 MSC SVG 안전 검사, 크기 제한, SHA 불일치/기존 published mapping 충돌을 검사하고 artifacts/category 경로로 복사. 이 export 검사만으로 Viewer의 전체 파일/raw/검색 보안이 충족되는 것은 아님.
- Workflow group_knowledge_bridge.py와 SKILL 원문은 기존 l1-github knowledge 역할의 검증된 checkout/commit 기반 읽기 연결을 설명. 새로운 그룹 writer나 UI 작성 기능을 요구하지 않음.

## 4. 실사용 가능 판정에 남은 필수 확인

| 확인 | 재사용할 근거 / 완료 기준 | 현재 |
|---|---|---|
| 설치 대조 | 실제 Viewer 소스/branch/revision, Updater SKILL/버전·API, 공개 3종과 설치 SHA 비교. 이미 유효한 G0 일부 보고 재사용 | NOT_VERIFIED |
| 문서 한 건 | 기존 Work MD/표/코드/상대 링크/원문을 읽고 Work·Evidence·source revision 매핑. 원본 SHA 불변 | NOT_RUN |
| 실제 MSC 한 건 | 기존 B형 HTML+내장 SVG, 6/12 participant·긴 phase·단계 이동·확대·복귀·다운로드 정책 | NOT_RUN |
| B1 경로 보호 | root canonical containment, 경로 탈출·symlink/TOCTOU 등 기존 부정시험 | BLOCKING / NOT_VERIFIED |
| B2 내용 보호 | 본문뿐 아니라 raw·검색·관련 문서·캐시·download에 같은 권한/제한자료 차단 적용 | BLOCKING / NOT_VERIFIED |
| B3 HTML 격리 | 별도 origin·sandbox/CSP·인증 쿠키/토큰 격리와 허용 asset·외부 요청 정책 | BLOCKING / NOT_VERIFIED |
| E3/E4 | 승인된 Linux localhost 회귀, 동료 2계정·deep link·검색·원본 불변·복구 | NOT_RUN |

단일 HTML 시안의 자체 브라우저 확인은 실사용 E3/E4나 기존 세 가지 BLOCKING의 해소 근거가 아니다. 스킬 ZIP 정적 확인도 실제 설치·호출·게시 성공 근거가 아니다.

## 5. 후속 한 번의 대조 범위

업무 GPT가 기존 동일 Work에서 허용된 Linux Agent/MCP의 READ_ONLY 조사로 실제 설치본과 매핑표를 대조한다. UI 7개 예시 adapter 메서드를 새 호스트 API 명세로 확정하지 않고, 기존 API/handler별 REUSE·CONNECT·입증된 GAP·UNKNOWN만 기재한다. 기존 Work MD 1건과 기존 B형 MSC 1건으로 대상/형식/권한을 먼저 확인하고, 실제 변경·서비스/공유 전환은 해당 유효 승인과 B1~B3/E3~E4에 따라 판단한다.

Viewer asset/adapter/handler의 좁은 연동을 우선하며 Workflow·Kernel·Updater의 데이터 구조를 UI에 맞춰 일괄 수정하지 않는다. 설치 Updater에서 실제 결손이 확인되는 경우에만 해당 책임 범위의 최소 보완을 설계한다. 이번 검토는 새 모델 호출·Job·분석·변환·스킬 설치·PUBLIC 교체 지시가 아니다.

## 6. 고정 입력·검증

PUBLIC main tree: 72ec441616f6ad0cdbb7f737b26c26e470e5b778. 아래 ZIP은 실제 원격 base64 바이트를 읽어 로컬 SHA/크기/Git blob/CRC를 확인. 패키지 실행 시험은 수행하지 않음.

| 파일 | bytes | SHA-256 | Git blob |
|---|---:|---|---|
| l1-fix-workflow_v1_6_74_1119.zip | 760324 | b810ce0cf072609431737c58b0ef2b7a0a8ec0701a0746e6a94283c374224989 | 5b05e6e16c8be7902793c62a50fb3c105fd35b6e |
| work-ledger-kernel_v0_7_42_1116.zip | 320083 | ece2bce143ef35a1c8cc3bc12ddf6a73e27e0f218fc69fec87844759d9dfc164 | 7799e03fbfa5c95851c430a20f8df0da253cbf07 |
| doc-converter_v0_2_26_1117.zip | 169204 | b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c | dcdb89205ec16ab07f04866bfc514954a02f8bc4 |

- 개선 시안: L1_Workspace_Wiki_Usability_Preview_20261120_KST.html, 69919 bytes, SHA-256 7c9ab930bedf0f2cf59834c66d3598a920a95d9215993788b9ca80f125de237c. 실제 스킬 연동 없는 별도 합성 아티팩트. 기존 v0.1.0 ZIP/정식 리뷰 입력 불변.
- [INTEGRATION.md](ui/viewer-wiki-ui_v0_1_0/INTEGRATION.md), blob 924ec349844235dca1ed86e8ba43ce34c96a18ae
- [Updater 책임 r0004](L1_WORKSPACE_KNOWLEDGE_UPDATER_OWNERSHIP_AND_VIEWER_UX_DELTA_r0004_20261118_KST.md), blob 1c35a5fcccdc134d6420226f1fe22267fef55205
- [G0 일부 보고와 첫 사례 후속 구분](L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md), blob 16b522a61be3c8c4257d42491ad0f22679de053b

이번 변경: 이 검토 결과와 CURRENT의 짧은 근거 연결만 게시. UI 정식 소스/ZIP·스킬·운영 설정·Work/Evidence/Knowledge는 변경하지 않음.
