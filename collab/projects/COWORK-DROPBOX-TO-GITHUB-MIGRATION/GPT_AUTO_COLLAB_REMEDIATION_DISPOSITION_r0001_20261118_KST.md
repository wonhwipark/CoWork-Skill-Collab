# CoWork 자동 협업 운영진단 후 조치·게이트 판정
- 날짜: 2026-11-18 KST / 작성: GPT
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 기존 Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`, `COWORK-AUTO-APPROVAL-20261115-001` (새 Work/원장 생성 없음)
- 실행 지시: 자동 협업체계 진단 후 사용자 “처리”. 접근 가능한 안전한 수정·조회·게시를 수행하고 운영 권한과 호스트 실행을 별도 판정.

## 1. 판정: PARTIAL_OPERATIONAL (안전한 단일 LIVE, 승인 일부 제한)
- GitHub 단일 LIVE, Windows watcher v0.2.25 설치·Task Running·별도 Notifier 존재는 Windows Claude Code의 2026-11-18 호스트 보고이며 GPT의 Windows 직접 접속 아님. 운영 v0.2.25 ZIP SHA-256 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`; 원격 결과는 `COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V025_WINDOWS_LIVE_CONDITIONAL_DEPLOY_RESULT_FOR_GPT_20261118.md`.
- 운영 정책맵: `POLICY-STATIC-V1=$1.50`, `-LARGE=$3.00`, `-DESIGN=$3.00`. 보호 위임 자체 `max_request_usd=$1.00`은 불변, LARGE/DESIGN 자동 서명 허용은 미확인·제한. **등록된 예산 ≠ 자동 승인 권한**. 로컬 보호 위임/키/정책/Task/DB 변경 권한을 새로 해석하지 않음.
- 완료 리뷰 검출기는 PRIVATE Actions 요약, 기존 Windows Notifier/Telegram 알림은 별도 기존 운영. GPT가 요청받아 PRIVATE 결과·영수증을 직접 조회 가능하지만 GPT 무인 자동 기동/판정 미구현·미검증.
- 추적 9행(Windows 보고): 완료 잔존 4, 미해결 5. `pending_requests` 원시 수 = 실제 실행 가능한 리뷰 수가 아님. Guard `AUTO_SIGNING_UNCERTAIN` 보존·재큐잉 금지. 기존 MSC 두 진입 독립 R1은 결과/영수증·GPT 판정 확인으로 **CLOSED**, 다시 리뷰하지 않음.
- 2026-11-18 이번 조회에서 `CLAUDE_PENDING_GUARD_RECONCILIATION_RESULT_FOR_GPT_20261118.md`와 `artifacts/pending_guard_audit_20261118.json`은 PRIVATE main에 아직 없음. Windows 실운영 DB/표시 정산 완료 주장 금지.

## 2. 이번 세션의 실제 변경
- `collab/ops/tests/test_review_request_gate.py` 두 군데 Windows CRLF 민감 `REQUEST.md` fixture 쓰기를 **UTF-8 bytes/LF 고정**으로 변경하고 fixture LF 검증 회귀 1개 추가. 승인기·게이트 본체 `review_request_gate.py`·운영 런타임·기존 REQUEST/READY/서명/ZIP 바이트 변경 없음.
- Commit `9b9141bc015a5930a2e57de26b6ab2f73be8223a`, 원격 readback Git blob `72e7f3df9523d3755ad790d600fbfd3a67b294ad`, 읽어온 파일 텍스트 UTF-8 bytes SHA-256 `409c956d0220e87d20d490fdfe38786044eb586e63e1c549d8e500818ee8e3ed`.
- **TEST_STATUS**: 원격 내용·변경 위치 확인 PASS; Windows 전체 단위시험/Actions 실행 결과·Windows 회귀는 NOT_VERIFIED/NOT_RUN. 이미 패키징된 v0.2.26 ZIP은 수정되지 않았으므로 그 안의 Windows CRLF 하우징 결함 15개는 그대로. 해당 ZIP을 수정·덮어쓰기 금지.
- **MODEL_CALLS=0 / NEW_REQUEST_READY=0 / PROTECTED_CONFIG_CHANGES=0 / WINDOWS_DB_WRITES=0 / V026_INSTALL=NOT_RUN**.

## 3. GPT 조치 판정 (기존 구현 재사용)
1. **P0 Guard/pending**: [기존 Windows 원샷](GPT_PENDING_GUARD_WINDOWS_ONE_SHOT_r0001_20261118_KST.md)을 그대로 재사용. 최신 운영 버전 v0.2.25·단일 provider 먼저 확인 → 기존 `pending_requests_audit.py` 읽기 전용 → Guard audit/claim/결과/비용 대조 → 유효한 공식 처리만 조건부 사용 → 완료 잔존의 UI 표현 최소 정리 → 결과·영수증 회수. 과거 UNCERTAIN 해제·재예약·다른 리뷰 입력 대체·비용 재호출 금지.
2. **P0 위임 예산**: 등록 정책을 수정하지 않음. 현재 보호 위임 USD 1.00/request를 안전 기준으로 유지. USD 1.50 확대, LARGE/DESIGN 자동 허용, 비용 상한 제거 등 **보호 위임 수치·범위의 새 유효 승인/호스트 권한을 확인하기 전에는 변경 금지**. 신규 리뷰는 실제 허용 정책·비용·source pin·승인·READY fail-closed. 일반적 '처리' 표현만으로 새로운 유료/보호 위임 승인을 생성하지 않음.
3. **P1 CRLF**: 외부 정본 독립 회귀 fixture 최소 수정 수용. 실제 Windows에서 이 파일의 수정 후 테스트를 실행하고 CI PASS를 회수. v0.2.26 패키지 시험의 15건과 동일 수정이 필요하면 **다음 신규 버전 개발 후보에서만** 반영, 새 ZIP SHA/CRC/재현·전체회귀 검증. 기존 v0.2.26 ZIP의 hash 불변.
4. **P1 Notifier**: 설치된 기존 Windows Notifier를 유일 발송 경로로 유지. `notify_events` 신규 모듈은 v0.2.26 후보 내부에 있지만 실제 호출 지점 없음(`NOTIFIER_ADAPTER_CONNECTED=NO`). 호출 지점·기존 워터마크·중복 의미를 먼저 읽기/합성 비발송 검증하고 **기존 경로의 입증된 gap만** 다음 후보에서 연결. 운영 Notifier/Task/Telegram 비밀·키 변경 및 시험 발송 금지. 이중 발송 구조 신설 금지.
5. **P1 v0.2.26**: Windows 격리 회귀 `1010 PASS/21 FAIL/12 SKIP`(21건 알려진 비회귀 원인)과 신규 61 PASS는 호스트 보고. 후보 `development_not_for_deployment`; 자체시험은 독립 리뷰가 아님. 추가 수정 통합 후 안전한 신규 후보·정식 독립 리뷰 1회·GPT 판정·별도 운영 승인 게이트 순서. **새 유료 REQUEST/READY·v0.2.26 LIVE 설치 현재 미승인/미실행**.
6. **P2 GPT 판정**: 완료 감지 Actions·기존 Telegram 통지 유지. 사용자가 GPT에 확인을 요청하면 바로 PRIVATE에서 리뷰 결과/영수증 조회·판정. 유휴 GPT 자동 실행용 새 Bridge/알림/유료 호출은 만들지 않음.

## 4. 실제 확인·한계·다음 한 행동
- GitHub 원격 직접 확인: 최신 이관·자동 승인 CURRENT, Windows v0.2.25/v0.2.26 결과, 기존 Guard 원샷, CRLF 수정 파일 readback, Guard 호스트 결과 2개 미존재. v0.2.26 운영 수정·인증·비용·신규 독립 리뷰는 수행 안 함.
- 현재 세션 연결은 GitHub 파일 접근 가능하지만 **Windows Claude Code 실행/Windows Task·운영 DB 직접 접속 수단은 없음**. PRIVATE 인계 게시만으로 Windows 실행을 시작했다고 주장할 수 없음.
- **NEXT_ONE_ACTION**: Windows Claude Code 기존 실행 세션에서 PRIVATE `wonhwipark/CoWork-Skill-Collab`/`main`의 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_PENDING_GUARD_WINDOWS_ONE_SHOT_r0001_20261118_KST.md`를 실행하고, Windows 시험 fixture 수정 커밋 `9b9141bc015a5930a2e57de26b6ab2f73be8223a` 반영 여부를 격리 검증한 다음 같은 Work에 결과/영수증/원격 바이트 해시를 게시. Guard가 BLOCKED이면 근거만 보고, 다른 유료 리뷰나 보호 위임 수치 변경으로 우회하지 않음.
