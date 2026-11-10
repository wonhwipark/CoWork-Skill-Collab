# CoWork GitHub 이전 — GPT C-4 판정 및 남은 게이트 통합 인계
작성일: 2026-11-10 KST | 작업: COWORK-DROPBOX-TO-GITHUB-MIGRATION | 방식: NO_PR
STATUS: C4_ACCEPTED_SCOPE_LIMITED / CUTOVER_PARTIAL / CURRENT_LIVE=DROPBOX

## 1. 증거 및 GPT 판정
근거:
- `CLAUDE_CUTOVER_READINESS_ADDENDUM_C4_FOR_GPT_20261110.md`: PRIVATE main, 이전 결과의 C-4 NOT_RUN을 대체하는 보충 문서. Windows Claude Code 읽기 전용 실측 결과이며 본 문서의 GPT 판단은 원문 재조회에 기초.
- `CLAUDE_CUTOVER_READINESS_RESULT_FOR_GPT_20261110.md`: v0.2.3 전체 합성 및 실서명 시험 결과, 운영 적용 전 단계.

**GPT 판정: C-4 ACCEPT (기존 Dropbox V1 정상 요청의 해시 호환성 실샘플 확인)**
- Dropbox 요청 폴더 65개 중 REQUEST 1개와 READY 1개인 63쌍을 검증.
- 63/63에서 REQUEST raw SHA-256 = UTF-8 decode/re-encode SHA-256 = READY request_sha256; 불일치 0.
- REQUEST/READY 유사 이름의 사이드카가 있는 폴더 0. 관측한 표본에서 B-2 basename 변경에 따른 재활성화 징후 없음.
- BOM/CRLF가 있는 실표본 0; 이 경로는 합성시험으로만 확인되었고 실제 현장 호환 PASS로 승격하지 않는다.
- 나머지 2개 폴더(쌍 불성립)는 이유 미확인. 그중 미정산 pending 1건이 포함될 가능성은 **확인되지 않았으며 추론으로만 취급**.
- 원문상 전송 계층 목록/다운로드만 사용, 비밀·식별자 게시 없음, 모델 호출 0. GPT는 개별 원격 요청 bytes 자체를 소유하거나 직접 재해시한 것은 아니므로 `READONLY_REAL_REPORTED` 증거 수준을 유지.

**따라서:** B-6의 정상 기존 요청 호환 확인 게이트 C-4를 해소 처리하되, 2개 불완전 폴더/미정산 pending·B-7 운영 신뢰키·실제 SHADOW·정식 독립 리뷰/영수증·운영 DB 이행·최종 전환 승인은 별도의 게이트로 유지한다.

## 2. 다음 통합 작업 — 추가 승인 없는 준비 전체를 한 번에
Windows Claude Code는 사용자가 별도 긴 피드백을 제공하지 못하는 점을 고려하여 **허용된 읽기 전용 조사와 설계·격리 시험·보고 게시까지 중간 질문 없이 연속 수행**한다.

1. **미정산 pending 1건 정산 준비:** 운영 Dropbox LIVE, 원본 요청·SQLite DB·작업스케줄러는 변경하지 않는다. 기존 전송 계층과 read-only DB 조회로 (i) 쌍이 아닌 2개 폴더의 상태 분류(개인/업무 식별자·내용은 외부 미반출), (ii) pending 1건과 연관 여부 TRUE/FALSE/UNKNOWN, (iii) 유효 READY와 기존 처리키/완료/리뷰 UNCERTAIN 중 어떤 상태인지, (iv) 누락/중복 재호출 0인 정산·hold 방법을 검토한다. 실제 처리/hold/requeue/삭제/READY 발행은 하지 않는다. 조회 권한 실패 시 우회하지 말고 NOT_RUN과 blocker 기록.
2. **운영 B-7 신뢰 루트 준비:** Ed25519 test-key 실험 성공과 운영 키 발급을 구분. 승인권자·서명 권한과 검증자 분리, 신뢰 공개키/repo ID의 Windows 외부 고정 위치·ACL, version/hash pin, 회전/폐기·시계 편차·키 분실/오염 시 fail-closed·롤백 계획을 비밀 없이 설계·격리 합성시험. 운영 키/개인키/PAT 생성이나 운영 파일 설치 없음.
3. **SHADOW 준비:** 기존 v0.1.5 Dropbox LIVE 및 v0.2.3 후보 read-only 계획 정합성 검토. T20: 모델·GitHub write·SQLite 운영 jobs write·Telegram 0, provider 단일 LIVE, cursor rollback 0 손실, notifier 기존 last_id 기반 bootstrap, WAL main/WAL/SHM 불변성 등 **격리 사본 시험 추가**. 호스트에 새로운 운영 watcher를 설치하거나 실행하지 않는다.
4. **독립 리뷰 입력 준비:** 공개 가능한 후보 코드 ZIP bytes가 GPT에게 없어 GPT 독립 코드 검증 미실행이며, Claude 개발 자기검토는 정식 리뷰가 아니다. 비밀/반출 정책을 준수하여 diff·시험 증거 및 소스 전달 가능 여부를 점검. 정식 REQUEST/READY 독립 reviewer·영수증 발행은 사용자 명시 승인과 유효 서명/비용 게이트 이후. 현 단계에서 실행하지 않는다.
5. 추가 코드 보완이 **실제 필요한 경우에만** 새 버전 ZIP 발행, 전체 pytest 및 48건 인수시험 회귀, SHA-256/바이트/실사용 적합성 재확인. 코드 변경이 없으면 v0.2.3 원본 그대로 두고 쓸데없는 ZIP 버전 생성 금지.

## 3. 사용자 핑퐁 최소화 및 종료 형태
- 사용자는 명시적 실행 지시 1회만 제공. Claude Code는 조사→필요 수정→격리시험→결과 MD GitHub PRIVATE main 게시→원격 readback까지 한 번에 수행한다.
- 결과 위치: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_FINAL_PRE_CUTOVER_GATE_RESULT_FOR_GPT_20261110.md` (신규 파일, PR 없음).
- 결과에 필수: 2개 폴더 상태별 집계/pending 연결 판단/운영 데이터 접근 여부, B-7 신뢰키 정책, SHADOW 실행 준비·차단요건, 테스트 pass/fail/skip, v0.2.3 유지 또는 신규 ZIP 명칭·full SHA/size, 운영 및 실제 모델 호출=0, 남은 사용자 승인 1회분.
- PRIVATE라도 식별 가능한 운영 요청, 자격증명·토큰·개인키·회사 반출금지 자료 게시 금지. 요약 카운트·판정·정책만 게시.
- 게시 성공 시 CURRENT 최신 단락을 **append** 후 remote readback. 권한 실패 시 로컬에 보존하고 NOT_POSTED를 기록한다.
- 실제 운영 DB 변경/hold/requeue, 새 GitHub watcher 호스트 SHADOW 설치/기동, 인증 발급, 공식 독립 reviewer 호출/과금, LIVE cutover, PUBLIC 게시 및 Dropbox 운영 종료 **미승인**.
- 작업 종료 후 사용자는 GPT에 `GitHub 최종 전환 준비 결과 판정해줘`라고 한 번만 말하면 된다.

## 4. 현재 완료와 미완료 구분
DONE_REPORTED: C-1 대기 보존 로직 합성/DB 사본 리허설, C-2 notifier 중복 방지 시험, C-3 시험 키 실제 Ed25519 S01~S10, C-4 63 정상 요청 실샘플 SHA 비교, C-5 운영 DB 사본 이행/롤백 리허설, v0.2.3 348 PASS/0 FAIL/12 SKIP.
NOT_RUN: 운영 신뢰키 발급/검증 및 배포, 미정산 Dropbox pending 원인 확인과 실제 정산, 운영 호스트 SHADOW, 정식 독립 리뷰+영수증, 운영 DB 실제 이행 및 LIVE cutover.
후보 `skill-collab-watcher_v0_2_3_1110.zip`은 보고상 131400 bytes, SHA-256 `9a4201295156ea93b572f4a7d0f8bc6b566130c31c1cae72c55d6c8c8489cf41`; Windows 로컬 전용 development_not_for_deployment. GPT가 raw ZIP을 직접 독립 검증한 것은 아니다.
