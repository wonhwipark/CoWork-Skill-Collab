---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-L1-WORKSPACE-VIEWER-V050-DESIGN-R1-20261122
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: l1-workspace-viewer-wiki-integrated
package_path: /SKILL-COLLAB/packages/l1-workspace-viewer-wiki-integrated_v0_5_0_1122.zip
package_file_id: github:REQ-L1-WORKSPACE-VIEWER-V050-DESIGN-R1-20261122
package_rev: l1-workspace-viewer-wiki-integrated-v0.5.0
package_sha256: a133d8703cc36a7f74cce8de1fd37db757052ed6a44030bc05fea89a05c253fa
package_size_bytes: 117897
baseline_package_ref: L1Work-v0.4.0-and-conversation-v0.4.1
knowledge_refs: []
consumer_profiles: [viewer-v050-today-assistant-independent-design-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent design review of Viewer v0.5.0 today work and right-side assistant usability readability context and status flows
---

# Viewer v0.5.0 — 오늘의 업무·우측 업무 도우미 독립 디자인 리뷰 R1

## 요청·고정 입력

- 사용자 명시 요청: 현재 대화에서 “위 디자인에대해서 독립리뷰요청해줘”.
- 대상 Work: L1-WORKSPACE-RAG-20261111-001. 동일 Work의 현재 확정 v0.5.0만 검토. 과거 Viewer UX/편집/색상 리뷰의 재실행이 아님.
- 리뷰 대상은 별도 Viewer UI이며 Knowledge Updater 스킬 자체 수정이 아님. 실제 대상 ID를 자동 승인 허용 ID로 바꾸지 말 것.
- 입력 정본: wonhwipark/L1Work, main의 고정 commit `599469f9f17aaa8367c39bbb3069c90130f7b9bd`, 루트 `l1-workspace-viewer-wiki-integrated_v0_5_0_1122.zip`.
- Git blob `6f62820eef5dace0950f3cf75ccd3c5d35612b5c`, bytes 117897, SHA-256 `a133d8703cc36a7f74cce8de1fd37db757052ed6a44030bc05fea89a05c253fa`. 동일 ZIP 원본 바이트를 이번 Commit A의 collab/packages/에 재사용.
- 원본 34개 항목·CRC·manifest 확인. 코드/fixture/문서 모두 비민감 합성 개발물. 실제 업무 코드·로그·MSC/계정 자료 없음.
- 개발물 공개 전달은 이미 완료. 독립 리뷰는 이번 신규 요청이며, 운영 승인이나 통합 검증 완료로 소급 승격하지 않음.
- v0.4.1 기반: 긴 제목 2줄/전체 보기, 너비 조절/저장, 본문을 숨기지 않는 종류 필터, 모바일 탐색·목차/본문 가독성. v0.5.0 추가: 우측 목차/업무 도우미 전환, 도우미 크게 보기, 오늘의 업무 탭, Work별 대화·초안·현재 대상·요청 상태·영수증·결과 문서.

## 읽을 입력 — ZIP 내부 경로

1. `viewer-wiki-ui/README_INTEGRATED.md`, `INTEGRATION_ASSISTANT.md`: 기능 범위·사용자 결정·연결 계약·현장 시험 A01~A10.
2. `viewer-wiki-ui/index.html`, `standalone-preview.html`: 같은 source의 정식 다중 파일 화면/단독 합성 미리보기.
3. `assets/assistant.css`, `assets/viewer-integrated.css`, `assets/style.css`, `assets/professional-theme.css`: 실제 cascade·반응형·본문·우측 패널·기존 스타일.
4. `assets/assistant.js`, `assistant-client.js`, `app.js`, `navigation.js`, `preferences.js`: 문서/오늘 탭 이동, 대상 변경, 대화·초안 보존/초기화, 상태·제안·실행·오류·키보드 흐름의 설계 근거.
5. `tests/v050-regression-results.txt`, `tests/v050-assistant-client-results.txt`, `source-pin.json`, `manifest.sha256`: 자체시험·원본 고정 근거. 자체시험을 독립 리뷰 PASS로 취급하지 않음.
6. 기존 Write 파일들은 미변경 참고. 전체 분석기/Kernel/Workflow 코드 감사로 범위를 확대하지 말 것.

## 중점 디자인 질문

1. **업무 목적·발견성:** 처음 연 사용자가 문서 읽기/오늘 할 일/도우미 대화의 차이를 이해할 수 있는가? 상단 도우미·좌측 오늘 탭·우측 목차/도우미의 중복·전환 비용은 적절한가?
2. **공간·가독성:** 중앙 본문/MSC를 읽으며 우측 대화 사용이 가능한가? 넓은 화면 380px 도우미와 1300px 이하 드로어, 좌측 너비 조절의 상호작용·본문 폭·스크롤·간격·선택 강조를 정적 CSS 기준으로 검토.
3. **오늘 업무 화면:** 목록·진행/확인/완료 요약·업무 카드·대화 영역·문서 열기/이 업무로 대화가 자연스러운가? 조회 실패·미지원·0건·미확인 상태를 구분하는가?
4. **대화 맥락:** Work별 대화/초안이 우측↔오늘 탭에서 이어지며, 다른 Work/문서/revision·전역 요청의 대상이 사용자에게 명확한가? 문서 이동 중 대기/기존 proposal 원본 고정·새로고침 소멸·프로필 전환을 검토.
5. **처리 신뢰성:** 질문→제안→명시 실행→요청 상태→영수증/문서 연결을 이해할 수 있는가? 실제 처리 중/불명확/실패/확인 필요를 구분하고 자동 재전송 없는 복구를 안내하는가? 완료 표시를 근거보다 앞세우지 않는가?
6. **접근성·입력:** 1440/1300/1040/760/390/320px 경계, Tab/Shift+Tab/Escape·탭 좌우키·IME·Ctrl/Command+Enter·터치 대상 크기·포커스 복원/트랩·zoom 200%·테마/글자 크기·긴 제목의 설계 반례는?
7. **기존 기능 공존:** 탐색 필터/환경설정/너비 조절/목차/MSC/Write UI가 도우미 추가로 가려지거나 동작이 바뀌는가? body class·hidden·panel-open·CSS cascade와 화면 전환을 대조.
8. **과잉 구현·역할 경계:** 기존 read adapter/LLM·Agent·Workflow/Kernel/Updater를 최소 연결하는 설계인가? 아직 설치 API 미확인인 UI bridge를 서버 구현 사실로 오해하게 만들지 않는가? 새 서버/DB/임의 shell 도입 필요를 근거 없이 확대하지 말 것.
9. **합성/실제 구분:** 기본 데모 답변·예시 완료 수·실제 요청 결과를 구분하는 문구가 충분한가? 실제 API 미연결·장기 대화 저장 미지원·업무 환경 검증 미실행을 사용자 흐름에 맞게 안내하는가?
10. 위 항목의 **사용자 영향이 큰 최소 수정 우선순위**와 유지할 강점을 제시. 지적 수를 강제하지 말고 반례가 있는 항목만 보고.

## 리뷰 범위·출력 계약

- **독립 디자인 리뷰 1회**, 구현 source는 화면·상태 전이 설계 확인용. test_policy STATIC_ONLY. 패키지 실행/설치·개발 수정·업무 Linux 검증·실제 모델/Agent/Job 호출·원본 Work/Knowledge 쓰기·watcher/DB/키/정책 변경 금지.
- 사용자는 실제 검증을 업무 환경에서 진행하기로 함. Windows 독립 리뷰는 정적 HTML/CSS/JS 및 제공 설계·자체시험 근거를 검토. 허용된 시각 자료 검토 가능 범위만 수행하고, 시각 확인·브라우저 실행을 못 하면 NOT_RUN 명시. 리뷰를 위해 UI를 실제 업무 호스트에 설치하지 않음.
- 결과는 한국어. 총평 `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`.
- 지적마다 `BLOCKING / MAJOR / MINOR`, 정확한 ZIP 파일/함수·선택자·설계 절, 사용자 영향, 구체 반례, 최소 수정, 확인 방법을 제시.
- `STATIC_DESIGN_REVIEW`, `VISUAL_INSPECTION`, `BROWSER_EXECUTION`, `BUSINESS_HOST_VALIDATION`을 각각 구분. 정적 코드 추정을 실제 화면·접근성·Linux E2E PASS로 주장하지 말 것.
- 자체시험 25 PASS의 증명 범위는 제한적. 실제 운영/권한/요청 복구/Writer·정식 통합 게이트는 NOT_RUN. 자료 부족은 질문/조건부 판정으로 남기고 실제 확인된 결함과 구분.
- 유지할 강점, 우선 수정 3개 이내 요약(실제 필요 시), 업무 GPT 인계 보완, 기존 Work의 다음 한 행동 포함.

## 요청 실행·보호 경계

- 신규 요청 ID당 독립 디스패치 최대 1회, 불확실 실행·결과 게시 실패를 이유로 자동 재리뷰/재과금/재큐잉 금지. 이전 요청·서명·READY·영수증/waiver 이력 불변.
- `run_policy_ref=POLICY-STATIC-V1`은 현재 포맷 호환용. GPT 게시자는 신규 가격·위임 허용 범위를 결정하지 않음. 실제 Windows 보호 signer가 신뢰되는 사용자 의도·실제 위임/한도·만료·입력 SHA/PIN·중복을 검증한 경우에만 승인/READY 마지막 게시·리뷰 실행.
- **GPT는 APPROVAL_SIG.json/READY.md를 작성하거나 실행 권한을 가장하지 않음.** 이 REQUEST/PIN 게시와 보호 승인/디스패치/Claude 결과는 별개.
- 결과: `collab/reviews/REQ-L1-WORKSPACE-VIEWER-V050-DESIGN-R1-20261122/REVIEW_RESULT_1.md`.
- 영수증: `collab/receipts/REQ-L1-WORKSPACE-VIEWER-V050-DESIGN-R1-20261122/RECEIPT_1.md`. 실제 결과·영수증 확인 전 완료로 보고하지 말 것.
