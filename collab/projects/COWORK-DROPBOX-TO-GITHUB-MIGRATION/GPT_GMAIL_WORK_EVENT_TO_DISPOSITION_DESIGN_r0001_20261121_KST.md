# CoWork Issue #2 — Gmail 이벤트 → ChatGPT Work 자동 GPT 판정 1차 후보 설계
- 문서: r0001 / 2026-11-21 KST
- 범위: 설계·수용 게이트만. 메일 송신·Gmail 연결·Work 이벤트 작업 등록·운영 설정·새 유료 모델 호출·GPT 자동 판정 게시 모두 NOT_RUN.
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` branch `main`, 기존 Work `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/`, 기존 [Issue #2](https://github.com/wonhwipark/CoWork-Skill-Collab/issues/2).
- 사용자 목표: Telegram 기존 알림 유지, Claude 리뷰 완료 후 **모바일 ChatGPT의 자동 판정 전용 Work 대화**에서 **원본 검증 경과·판정 근거·최종 판정·다음 조치** 확인 및 후속 질문. 기존 설계 대화창에 자동 메시지 삽입은 지원 확인 전 약속하지 않음.

## 1. G0 관측과 의존성
| 항목 | 구분 | 근거·경계 |
| --- | --- | --- |
| GitHub LIVE 자동 Claude 리뷰 | HOST_REPORTED_LIVE + 원격 개별 E2E | watcher v0.2.29/STATIC USD3 운영 보고; 신규 Viewer R1 `REQUEST/READY/RESULT/RECEIPT/DISPATCH` 원격 일치 확인. 실제 호스트 키·DB는 GPT 직접 검증 아님 |
| 완료 감지 | CODE_PRESENT_NOT_EVENT_DELIVERED | `collab/dashboard/review_completion.py`는 GitHub Actions summary만 생성, Work를 깨우거나 Telegram/Gmail을 전송하지 않음 |
| 기존 Telegram | USER_CONFIRMED | Windows 별도 Notifier 운영·기존 텔레그램 알림. 해당 호스트 Notifier 내부 발송 hook/source 및 로그는 이 설계 단계에서 직접 열람하지 못함 |
| Gmail 신규 메일 → Work | PRODUCT_CAPABILITY_DOCUMENTED | OpenAI 공식 도움말에서 지원, sender/subject 필터 가능. 실제 사용자 계정에 Gmail 연결·이벤트 트리거 생성권·실행 한도가 있는지는 별도 G0 |
| Gmail 연결 | NOT_CONNECTED_AT_DESIGN_CHECK | 해당 대화의 플러그인 검색에서 Gmail 설치/연결 `installed=false`. 실제 계정 상태와 Work UI에서 재확인 필요 |
| Work 이벤트 소스 조회 | UNVERIFIED | 이 세션의 이벤트 소스 조회 도구 `404 Action not found`. 기능 부재로 단정하지 않으며 Work UI 수동 확인 게이트 |
| GitHub PRIVATE 독립 조회 | GPT_CHAT_PASS / WORK_NOT_TESTED | 현 GPT GitHub 연결은 PRIVATE 조회 가능. Work 이벤트 작업의 동일 계정·repo read/write 권한 및 승인 중단 여부는 미확인 |
| Work 결과 모바일 조회 | PRODUCT_CAPABILITY_DOCUMENTED / EVENT_FLOW_NOT_TESTED | Work cloud 결과는 모바일·웹에서 대화로 볼 수 있음. 새 이벤트들이 같은 전용 대화에 연속 기록되는지 파일럿 확인 |

공식 근거:
- https://help.openai.com/en/articles/10408842-google-app-data-controls-faq
- https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- https://help.openai.com/ko-kr/articles/10291617-scheduled-tasks-in-chatgpt
기존 근거: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_CLAUDE_REVIEW_RECEIVE_VALIDATION_r0001_20261117_KST.md`.

## 2. 제안 아키텍처 (기존 기능 REUSE + 최소 연결)
`Windows watcher`가 보호 정책·SOURCE_PIN·중복을 확인하고 Claude 독립 리뷰 1회 실행 → `REVIEW_RESULT_1.md` 및 `RECEIPT_1.md` 원격 게시·readback 완료 → **기존 완료 이벤트 생산자**에서 분기:
- A: 현재 `Telegram Notifier` 사용자 완료 알림 유지(재설치·변경 없음).
- B: 검증된 동일 완료 건에 한해 **최소 메타데이터 Gmail 1통** 전송하는 *선택적 새 어댑터 후보*. 실제 Notifier 호출 위치/중복 방지 구현을 G0에서 확인하기 전 코딩·배포하지 않음. watcher 안에 새 중복 reviewer/DB/감시 루프를 만들지 않음.
- C: **Gmail new-message event → ChatGPT Work 전용 작업**: sender/subject 필터 후 이메일은 단지 참조 포인터로만 사용. Work는 GitHub PRIVATE main에서 `REQUEST, SOURCE_PIN, APPROVAL_SIG, READY, DISPATCH, REVIEW_RESULT, RECEIPT, 기존 GPT_DISPOSITION`을 다시 읽어 검증하고, 해당 Work `CURRENT` 및 고정 설계/검토 근거까지 조회.
- D: Work 대화에서 검증 과정과 근거별 수용/수정 수용/거절/보류/추가정보필요 의견 및 최종 판정 초안을 보고. **1차 파일럿은 읽기 전용**.
- E: 별도 사용자 승인과 GitHub 쓰기 권한·안전 게이트 이후에만 기존 `collab/reviews/<request_id>/GPT_DISPOSITION.json` 형식으로 신규 판정 1회 CREATE_ONLY 게시·readback, 같은 Work CURRENT/기존 TRACKER 현행 필드 갱신. 새 `collab/decisions` 원장·새 스키마는 기본으로 만들지 않음.
- F: 모바일 ChatGPT Work 알림/전용 대화에서 최종 판정과 다음 한 동작 확인. 판정 요약을 기존 Telegram에 추가 전송하는 기능은 선택 후속이며 파일럿 필수 요건 아님.

구조를 지키는 이유: Gmail/Telegram은 신뢰 루트가 아님. 모델이 메일의 텍스트 명령을 따라 승인·서명·READY/재실행하지 않도록 제한. 기존 `review_chain.inspect`의 필드 대조는 참고 검증이지 암호학적 서명 검증 아님.

## 3. 알림 이벤트 최소 계약(설계용, 실제 구현 스키마 확정 아님)
- **Envelope/메일 발신:** 실제 발신자 주소는 현재 미정(새 계정·토큰 생성 지시 없음). 전용 수신 Gmail은 사용자가 연결/승인한 계정만. Gmail Work 트리거는 발신자 allowlist와 제목 고정 접두사 `COWORK_REVIEW_COMPLETE_V1`로 필터. 주소·subject만 신뢰하지 않음.
- **제목 예시:** `COWORK_REVIEW_COMPLETE_V1 REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120`.
- **본문 허용 필드:** `event_version, request_id, request_revision, package_sha256, processing_key, review_path, receipt_path, completed_utc`, 선택적 `source_commit`. 저장소는 정확히 PRIVATE `wonhwipark/CoWork-Skill-Collab/main` 고정.
- **금지:** 리뷰 본문·업무 코드·고객정보·토큰·운영 로그·개인키·승인 시그니처·원시 DB/업무 L1 지식·파일 첨부·메일 자체의 실행 명령.
- **한 건당 한 이벤트:** 완료 원격 검증·중복 방지 키 매핑이 있는 기존 Notifier를 우선 재사용. 동일 메일 재수신·전송 실패·재시작은 같은 처리키로 인식; 본문에 URL을 넣더라도 이메일 URL을 그대로 열지 말고 미리 허용된 repository/path 규칙으로 재구성·검증.

## 4. ChatGPT Work 판정 검증 게이트
1. **메일 입구:** 계정/발신자/제목/크기/정규식 ID·revision·sha 필드 검증; 조건 불일치면 결과 `HOLD_INVALID_EVENT` (GitHub 게시 0, Windows 모델 호출 0). Work 작업 *자체*는 이미 기동됐을 수 있음.
2. **GitHub 강제 재조회:** 현재 PRIVATE main에서 해당 REQUEST·원본 PACKAGE·SOURCE_PIN/commit·APPROVAL_SIG·READY·DISPATCH·REVIEW_RESULT·RECEIPT를 실파일로 확인. 메일 본문 데이터는 필터/조회 힌트 이외 신뢰 금지.
3. **결속:** `request_id/revision/package_sha256`와 `READY.request_sha256`(원시 REQUEST SHA256)·`processing_key`, result execution_status COMPLETED, receipt ok=true, review_id, dispatch 참조, 고정 원본/commit 정보 일치. 서명 검증을 Work가 직접 할 수 없다면 `SIGNATURE_CRYPTO_NOT_VERIFIED`로 별도 표시; GitHub 파일 존재만으로 실행 자격을 소급 PASS하지 않음.
4. **기존 판정 확인:** `GPT_DISPOSITION.json` 또는 해당 Work 판정 정본이 이미 있으면 재판정·재게시 금지. 동일 처리키 다중 메일은 `ALREADY_DECIDED`로만 기록. revision/sha 변화는 같은 요청의 완료로 자동 승격 금지.
5. **근거 독립 검토:** Claude 결론을 자동 수용하지 않고 지적별 설계 위치·반례·수정안·적용 범위·잔여 위험을 원본과 대조. 미검증 실행/API·업무 Linux 동작은 `NOT_VERIFIED`. 판정은 `ACCEPT/ACCEPT_WITH_CHANGE/REJECT/DEFER/NEED_INFO` 기존 어휘를 재사용(정확한 JSON 필드 계약은 실파일 확인).
6. **게시 단계는 별도 승인:** 기존 `GPT_DISPOSITION.json`을 CAS/Create-only로 정확히 1회 게시. 존재·충돌·권한/승인 중단·readback 실패 시 `WRITE_PENDING_AUTH`/`POST_CONFLICT_PENDING`/`UNVERIFIED`로 보존하고 판정이 게시됐다고 주장하지 않음. 판정 본문 외에 reviewer 요청·READY·운영 설정 등은 변경 금지.
7. **표시:** 모바일 Work 전용 작업 결과에는 `검증 상태 → 지적별 GPT 독립 판단 → 최종 판정 → 게시 여부와 링크 → 후속 한 동작`을 빠짐없이 담고, 근거 파일/시점과 모델 자체 판단을 구별. 이벤트 처리 중간 스트리밍·기존 별도 대화창에 자동 삽입을 필수로 가정하지 않음.

## 5. 비기능 요구·위협 모델
- **중복·비용:** 같은 처리키에 대한 원격 GPT 판정 1개. 파일 게시 후 메일만 재전송했을 때 Claude 재리뷰 0, Windows 승인·서명·READY 재실행 0. 그러나 Gmail 이벤트가 Work를 *시작한 뒤* 형식을 검사하므로 **가짜/중복 이벤트에도 Work 모델 사용량이 발생할 가능성**이 있음. 이를 `NO_MODEL_CALL_ON_INVALID_EMAIL`로 약속하지 않고 실제 사용량·트리거 조건·quota를 별도 실측. 완전한 모델 호출 0 게이트가 필요하면 Gmail→Work 외부 prefilter 서비스를 따로 검토.
- **메일 스푸핑/인젝션:** 발신자 필터 외에 Gmail 본문을 신뢰하지 않음. 메일·리뷰 문서의 명령/링크/프롬프트는 비신뢰 데이터; 승인·키·외부 POST·운영 변경 요구는 무시. GitHub repo·경로와 bytes/readback 중심.
- **권한·노출:** Gmail은 최소 메타데이터만, ChatGPT Work GitHub 접근도 승인된 CoWork PRIVATE 범위만. 미승인 회사 자료·운영 자격증명·원본 로그는 가져오지 않음. Gmail OAuth scope, 연결 만료, 쓰기 승인 정지를 표기.
- **장애:** Gmail 지연·누락, Notifier 오류, Work 일시 중지, GitHub 403/404/429, CAS 충돌 → 원본 기록 보존, 새 Claude 호출·불확실 리뷰 재큐잉 0. 재전송 시 source_evidence 재검증 후 진행하되 추가 판정 중복 0. Telegram은 독립적으로 계속 동작.
- **용량·대화:** 이벤트 1건당 읽는 최대 파일·토큰 예산과 회당 Work 사용량을 파일럿 실측해 한도 도입 여부 판정. 원본 전체 맥락은 해당 Work CURRENT·핀된 참조부터 필요한 문서만 선택 조회. 일회성 전체 소스 감사 금지.
- **수명:** Gmail Work 연결·승인 범위·대상 계정·종료/일시중지 경로 명시. 기존 보호 위임 USD3/12월 만료는 Claude 리뷰용이며 **Work 모델 사용량/권한의 승인으로 재해석 금지**.

## 6. 파일럿 단계와 수용 기준
| 단계 | 대상 | PASS 기준 | 안전 경계 |
| --- | --- | --- | --- |
| G0-1 | Windows Notifier·review_completion·review_chain 원문 실측 | 실제 **원격 완료 검증 후** 이벤트 생산 위치·Telegram 발송·중복키·로그 경로 식별 | 읽기 전용, 운영 변경 0 |
| G0-2 | 실제 계정 Gmail/Work 앱·GitHub 권한/트리거 UI | Gmail new message(sender/subject 조건) 이벤트 생성 가능함을 계정 UI 또는 실제 연결된 자동화 인터페이스로 확인; Work PRIVATE GitHub read 확인 | 메일 전송/작업 활성화·쓰기 0 |
| G1 | 과거 완료 Viewer R1(`REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120`) 입력을 사용한 **로컬 합성 이벤트** | 검증 매핑·불일치 차단·중복/no duplicate write 테스트; 과거 GPT 판정 있으면 새 판정 금지 | 기존 리뷰 재호출/승인/READY 0 |
| G2 | 별도 승인 후 민감정보 없는 **실제 테스트 메일 1통** + Work 읽기 전용 이벤트 | 모바일 Work 대화로 기동·PRIVATE 원문 실제 재조회·근거가 남는 결과 확인; 송신자 필터·오류 경로와 Work usage 확인 | Claude 새 REQUEST/유료 리뷰 0, GitHub 쓰기 0 |
| G3 | 자연 발생하는 신규 완료 리뷰 1건 | 기존 Telegram 동일 작동 + Work 판정 초안 + 처리키 중복 차단 + 사용자 모바일 후속 질문 | 자동 GPT_DISPOSITION 게시 0 |
| G4 | 별도 사용자 승인 후 운영 쓰기 | 기존 `GPT_DISPOSITION.json` create-only remote bytes readback, CURRENT/TRACKER 현행 필드 정합, 충돌·권한 실패 시 안전 보류 | 사용자가 승인하지 않은 코드/설치·재리뷰 0 |

사전 STOP: G0-2가 미확인/불가하면 Gmail 송신/Work 이벤트 등록에 착수하지 않음. G2가 PASS해도 G4(무인 GitHub 쓰기)로 자동 승격하지 않음.

## 7. 모바일 ChatGPT 사용자 화면 수용 예시
**작업 이름:** `CoWork · GPT 독립 판정` (별도 Work 클라우드 대화, 기존 설계 채팅과 분리).
- `[수신]` 리뷰 ID / Work ID / 완료 시각 / 기존 Telegram 링크
- `[원본 검증]` REQUEST·READY·결과·영수증/처리키 일치 PASS 또는 HOLD, 이력이 확인되지 않은 부분은 NOT_VERIFIED
- `[검토 과정]` Claude 지적별 독립 판단과 수정/보류 이유, 리뷰에서 실제 읽지 않은 파일 범위
- `[결과]` 판정 결론 / 판정 게시 여부(POSTED vs DRAFT_ONLY) / GitHub 정확한 링크
- `[다음 한 행동]` 사용자 승인이나 설계 수정이 필요한 단 한 항목; 같은 Work 대화에서 후속 질문
**수용 조건:** 모바일 ChatGPT에서 작업 완료 푸시/예약 작업 진입·전체 판단근거 열람·질문 응답이 되는지 실제 Android에서 확인. 기존 다른 대화에 원격 새 메시지가 자동 등장한다는 주장은 배제.

## 8. 현재 판정·다음 한 동작
- `DESIGN=PREPARED`, `GMAIL_EVENT_PRODUCT_SUPPORT=DOCUMENTED`.
- `ACCOUNT_GMAIL_CONNECTED=NO_IN_CURRENT_PLUGIN_LOOKUP`, `EVENT_TRIGGER_ACCOUNT_G0=NOT_VERIFIED`, `WINDOWS_NOTIFIER_HOOK_G0=NOT_RUN`, `WORK_GITHUB_E2E=NOT_RUN`.
- `AUTOMATION_CREATE=NOT_RUN`, `EMAIL_SEND=NOT_RUN`, `GPT_AUTO_DISPOSITION=NOT_RUN`, `PRIVATE_WRITE=DESIGN_ONLY`, `CLAUDE_PAID_CALLS=0`.
- **NEXT_ONE_ACTION:** 사용자에게 기존 승인 반복 요구 없이 연결된 ChatGPT 계정의 **Gmail/Work 이벤트 트리거 생성 지원과 PRIVATE GitHub 읽기 권한**을 G0 읽기 전용으로 실제 확인한 뒤, 가능하면 *기존 Windows Notifier 완료 이벤트 호출 위치*만 G0로 대조. 이 둘이 확인되기 전에는 Gmail 송신 어댑터·자동 작업 등록·시범 메일 전송을 하지 않음.
