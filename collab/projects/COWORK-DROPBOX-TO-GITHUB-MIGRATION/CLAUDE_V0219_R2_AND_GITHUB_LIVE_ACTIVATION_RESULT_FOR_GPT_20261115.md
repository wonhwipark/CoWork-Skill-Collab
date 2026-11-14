# CLAUDE v0.2.19 독립 R2 + GitHub LIVE 활성화 결과 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-15 KST). **Claude 자체 보고**, GPT 판정 전 canonical 아님.
- 근거: `GPT_V0219_R2_AND_GITHUB_LIVE_ACTIVATION_APPROVAL_AND_ONE_SHOT_r0001_20261115.md`. 승인(A·B·LIVE)은 재질문하지 않았다.
- **결론: 독립 R2 리뷰가 BLOCKING 1건을 보고했고 재현되어, 인계서 §2.5에 따라 B1·B2·B3(운영 변경)과 LIVE 전환은 실행하지 않았다.** `ACTIVE_PROVIDER=NONE`, `CUTOVER=NOT_CUTOVER`(BLOCKED). 운영 호스트는 변경 0.

## 1. 필수 표

| 항목 | 결과 | 증거 / 원인 |
|---|---|---|
| PAID_REVIEW_APPROVED | **YES** | 인계서 기록 |
| REVIEW_ID | `REV-COWORK-V0219-20261114` / 요청 `REQ-COWORK-V0219-R2-20261114` rev 1 | `POLICY-STATIC-V1-LARGE`, effort medium |
| REVIEW_TARGET_SHA | `6e7fee3340cc6d0282d1c18fe3db42a90360259dd73fa6d7c0a7698af7afe5c0` (239143 B) | 로컬·원격 원시 바이트 크기·SHA·CRC 일치 후 진행(§2) |
| REVIEW_MODEL_CALLS | **1** | 감시기 감사 훅: 하위 프로세스 2(인증 확인 1 + 리뷰 1), 디스패치 이벤트 1, 재시도 0 |
| ACTUAL_COST_USD | **$0.9007163** (상한 $3의 30%) | 27 turns, 출력 20,963 토큰, 캐시 생성 72,770 / 읽기 489,461. R2 목표(5 turns·40k/6k)는 초과(강제 수단 없음, `--max-turns` 미지원) |
| INDEPENDENT_REVIEW | **COMPLETED — BLOCKING 1건 → 게이트 FAIL** | §3. 개발 세션과 분리된 독립 프로세스(Read/Grep/Glob, MCP 0, 세션 비저장). 구현자 자체 시험을 독립 리뷰로 계산하지 않음 |
| HOST_DEPENDENCY (B1) | **BLOCKED (A 게이트 FAIL)** | 운영 인터프리터는 `cryptography` 없음 그대로. 격리 임시 venv 리허설은 PASS(§5) |
| NOTIFIER_WATERMARK_MIGRATION (B2) | **BLOCKED (A 게이트 FAIL)** | 운영 Notifier·워터마크 변경 0. 격리 후보 리허설은 이전 단계에서 PASS |
| PENDING_PRESERVED | **PASS** | 운영 DB main/WAL 해시 불변(`4e8bc33a…`/`59de7507…`), pending `L1-KNOWLEDGE-ROADMAP-DESIGN-20261109-001`·COMPLETED 60·CONFLICT 1 보존, 이관·재리뷰 0 |
| ROLLBACK_REHEARSAL | **PASS (격리)** | 운영 변경이 없어 호스트 롤백 불필요. 원본 바이트 복사→격리 복원 리허설은 이전 단계에서 통과, 이번에도 원본 불변 재확인 |
| GITHUB_WATCHER_TASK (B3) | **NOT_RUN** | 게이트 FAIL. Task 등록·시작 0 |
| ACTIVE_PROVIDER | **NONE** | |
| CUTOVER | **NOT_CUTOVER (BLOCKED)** | `LIVE`·`HOST_APPLIED` 기록 안 함 |
| ACTUAL_MODEL_CALLS | **1** (승인된 R2 1회) | 그 외 0 |
| TELEGRAM_DUPLICATES | **0** | 운영 Notifier 무변경, 운영 DB 무쓰기 → 신규 알림 대상 이벤트 0, 테스트 발송 0 |
| FILES_SHA_READBACK | **PASS** | §4 |
| BLOCKED / errors | §6 | |

## 2. 리뷰 전 검증과 실행

- 원격 ZIP 원시 바이트 재조회: 크기 239143, sha256 일치, 로컬 원본과 바이트 동일, ZIP CRC OK, 93개 파일, 경로 이탈 0, 필수 파일·버전 `0.2.19`, 비밀 스캔 0. 원격 manifest·patch 존재 확인. 전부 일치한 뒤에만 요청 게시.
- 정식 계약: commit A(패키지 `3bc24e9421d7`, REQUEST `240680f8912b`, 원격 바이트 동일) → 승인 서명 2시간 유효·SOURCE_PIN(=commit A)·오프라인 검사 OK → commit B(APPROVAL_SIG `b59928d0cb4b`, SOURCE_PIN `ae41c99ebfe6`, **READY 마지막** `8d149b7335cf`). 서명키는 기존 단일 PC Ed25519 키(개인키·토큰 비게시).
- 드라이런(모델 0): GET 27, `VALIDATED`. 이전 `REQ-COWORK-V0217-R2`는 승인 만료로 `APPROVAL_EXPIRED`, `REQ-COWORK-V0214-R1`은 정책 미등록으로 거부 — **재호출 0**.
- 실제 1회: 리뷰어 감시기는 **리뷰 대상 v0.2.19 자신**(고정 바이트에서 추출, 격리 상태 폴더, Classic 쓰기 토큰). 첫 실전 경로가 **완전 자동**으로 동작: 원격 예약 기록 → 모델 → 결과 → 영수증 PUT 3회, 작업 `COMPLETED`(attempt 1). 소요 261초.
- 리뷰와 SHADOW 분리 유지(리뷰는 LIVE 모드 격리 폴더, SHADOW 쓰기 없음). 라이브 운영 폴더 파일 열기 0·SQLite 연결 0.

## 3. 독립 리뷰 결과와 내 검증 (최종 판정은 GPT)

| ID | 리뷰 분류 | 내 검증 | 처리 |
|---|---|---|---|
| Q6 / B1 | **BLOCKING**: `GitHubTransport.repository_id()`가 transport 수명 동안 값을 캐시. 장시간 watch 중 `owner/name`이 다른 저장소(새 숫자 ID)로 바뀌면 N2가 계속 통과 | **재현**(합성): 한 transport를 재사용한 두 번째 승인 확인에서 저장소가 바뀐 뒤에도 2차 리뷰가 실행됨(`calls 2`) | 후보 v0.2.20에서 수정(캐시 제거, 승인 확인마다 서버 조회) + 회귀 시험 |
| N1 | 비차단: 생성 전용의 원자성·읽기 직후 가시성은 GitHub 서버 동작에 의존, 정적 리뷰로 미검증 | **실서버 보강 검증**: 임시 브랜치에서 6개 동시 쓰기 × 4회 → 매회 승자 정확히 1, 나머지 409/422, 승자 내용 즉시 읽힘, 브랜치 삭제 | 해소(추가 증거) |
| N2 | 비차단: S2 `taskkill` 로그는 적절 | — | 조치 없음 |
| Q1~Q5, Q7, Q8 | 이상 없음(원자성·키 결합·분류·크래시/복원·원격 오류·비용 게이트·SHADOW·잠금 상호작용) | 리뷰어가 코드 추적으로 확인한 범위 | — |

- 리뷰어가 검증하지 못했다고 밝힌 것: 실제 GitHub 동시 쓰기(위에서 보강), 저자 시험 재현, 저장소 탈취의 현실성. 지식 정정 제안(N2 캐시 수명을 알려진 갭에 기재)은 v0.2.20에서 코드로 해소.

## 4. 원격 게시물 (PRIVATE main, 바이트 readback 확인)

- 감시기가 **스스로** 올림: 예약 `dispatch/REQ-COWORK-V0219-R2-20261114/DISPATCH_1.md` `19b6e54ba5af`(식별 필드만, 비밀 없음), `reviews/…/REVIEW_RESULT_1.md` `9a151a4233d7`(15,477 B, 엔진 생성 바이트와 동일, sha256 `065831ccb951…`), `receipts/…/RECEIPT_1.md` `d4c42710e385`(식별 필드 일치).
- 개발자 `gh`로 추가: `receipts/…/USAGE_RECEIPT_1.json` `6247c0c034bc`(원격 바이트 동일).
- 의미: **감시기 자동 게시 E2E가 실제 리뷰에서 처음으로 완전 성공**(읽기전용 토큰 시절의 `UPLOAD_PENDING`·수동 게시 없이).

## 5. 후보 v0.2.20 (격리, `development_not_for_deployment`, 독립 리뷰 NOT_RUN)

- 변경: `github_transport.py` 캐시 제거 1곳 + 버전·런북 제목 + 회귀 시험 1개. 시험 venv **674 passed / 12 skipped**, 운영 인터프리터 **607 passed / 17 skipped**, FAIL 0. 새 회귀 시험은 v0.2.19에서 실패하고 v0.2.20에서 통과.
- `skill-collab-watcher_v0_2_20_1115_DEV_NOT_FOR_DEPLOYMENT.zip` **239,432 B**, sha256 `6a8626375e5e711535abdd261ff48781114802bb345cabe2ed5940b75968f386`, 93개 파일, CRC OK, 비밀 스캔 0, 재빌드 바이트 동일. **로컬 보관, 미게시, 새 리뷰 없음**. v0.2.19 리뷰 결과를 소급 적용하지 않으며 이번 1회 승인을 재사용하지 않는다.
- B1 격리 리허설(운영 변경 아님): 운영 인터프리터와 같은 기본 Python 3.11.9로 만든 **임시 venv**에 해시 고정 잠금(`cryptography 50.0.2`, `cffi`, `pycparser`)을 `--require-hashes`로 설치 성공, Ed25519 서명·검증·변조 거부 확인 후 임시 venv 삭제. 운영 인터프리터는 여전히 `cryptography` 없음.

## 6. 차단과 다음 결정

- **BLOCKED 사유**: 독립 리뷰 BLOCKING 1건(인계서 §2.5의 STOP 조건). 운영 설치·Notifier·Task·LIVE는 하나도 실행하지 않았다.
- 재개 경로(GPT 판정): v0.2.20에 대한 **새 독립 리뷰**가 필요하다(이번 승인은 사용·소진). 변경이 한 함수의 캐시 제거라 v0.2.19→v0.2.20 diff 중심의 소규모 리뷰(예: `POLICY-STATIC-V1`, $1, 1회)로 충분한지 GPT가 판단. 사용자가 B 승인(운영 변경 3종)을 새 리뷰 PASS 후에도 유효하다고 명시하면 B1→B2→B3를 같은 인계 하나로 이어서 실행 가능.
- 운영 안전 상태: 운영 DB main/WAL 해시 불변, Task 4개 상태 불변(Notifier Running, 나머지 Disabled), 새 원격 임시 브랜치 정리 완료(이번에 만든 브랜치 모두 삭제).

## 7. 한계

- v0.2.20과 N2 수정은 **자체 시험** 결과이며 독립 리뷰가 아니다. 리뷰는 정적이며 Windows 전용.
- 실제 Claude 사용량 한도 메시지는 계속 미관측(NOT_VERIFIED). 별도 계정 enforce SHADOW·장기 SHADOW는 이번에 실행하지 않았다(운영 변경 전 필수 증거는 B 단계 재개 시 재확인).
- 비밀값·토큰·경로·계정명은 이 문서에 없다.
