# Windows 원샷 — Guard 정산·pending 표시 분리

## 최신 실행 보충 (2026-11-18 KST / GPT 운영 판정)
- Windows 호스트의 최근 실측 보고: **GitHub 단일 LIVE / watcher v0.2.25 이미 설치·검증**. 이 원샷에서는 v0.2.25를 **재설치하지 말고** 시작 시 Task·프로세스·DB·배포 결과만 읽기 전용 대조. 호스트 최신 상태가 다르면 원인부터 기록.
- GPT 새 판정: [자동 협업 최소 조치 결과](GPT_AUTO_COLLAB_REMEDIATION_DISPOSITION_r0001_20261118_KST.md). 운영 정책맵 예산과 별개로 보호 위임 요청당 USD 1.00은 미변경. 위임 숫자·허용 리터럴을 **신규 승인 없이 변경하지 않음**.
- CRLF 시험 fixture 저장소 정본 수정 커밋 `9b9141bc015a5930a2e57de26b6ab2f73be8223a`를 격리 Windows에서 1회 시험할 수 있음. `python -m unittest discover -s collab/ops/tests -p test_review_request_gate.py -v` (모델 호출·키·원격쓰기 0). 이 시험은 **PRIVATE 저장소의 독립 도구**이며 기존 v0.2.26 ZIP 내부 15개 CRLF 실패가 해결됐다는 의미가 아님.
- 최신 조회 시 이 원샷의 Windows 결과 MD/감사 JSON은 원격 미게시. **실행·결과 확인 전에는 완료라고 보고 금지**. 기존 9행·Guard UNCERTAIN은 READ_ONLY 우선, 완료 4행 데이터 삭제·재호출 금지.
- Windows 기존 세션이 작업 수행 후 결과를 게시할 때 `HOST_GUARD_AUDIT`, `DISPLAY_APPLIED`, `GATE_TEST_WINDOWS`, `MODEL_CALLS`를 구분하여 기입. 새로운 유료 리뷰·REQUEST/READY·설치/Notifier 변경 금지.

- 정확한 저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`.
- 이 인계의 상대경로: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_PENDING_GUARD_WINDOWS_ONE_SHOT_r0001_20261118_KST.md`.
- 사용자 최신 실행 지시: “이제 조치해줘”. 기존 Work `COWORK-DROPBOX-TO-GITHUB-MIGRATION` 및 Guard의 `L1-WORKSPACE-RAG-20261111-001`을 이어감.
- 목적: 기존 실행/서명 이력 정산 → 완료 잔존을 실행 대기와 구분 → Guard의 기존 1사이클을 공식 보호 경로로 완료할 수 있는지 판정하고 가능한 부분만 수행 → 결과 게시까지 한 세션. 문서 게시가 호스트 기동이나 새 유료 호출 승인은 아님.

## 1. 실제 입력과 변경 경계
1. 먼저 기존 Windows 실행 명령/Task에서 실제 Python·watcher 설치 루트·설정·활성 provider·DB 경로를 확인. 경로/설치 버전을 추측하지 말고 기존 Config/CLI의 DB 경로 계산을 재사용. 토큰/키/설정 원문은 출력·게시하지 않음.
2. v0.2.25 조건부 배포가 별도 세션에서 진행 중이면 그 작업의 최신 결과와 단일 LIVE 상태를 먼저 확인. 중복 설치/재기동/운영 변경 없음. 현재 개발된 v0.2.26은 [별도 Work CURRENT](../COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md)의 후보이며 이 정산 때문에 설치하거나 고정 v0.2.25 ZIP을 교체하지 않음.
3. PRIVATE main 최신 내용을 깨끗한 별도 로컬 체크아웃에서 취득하고 원격 HEAD/로컬 source commit을 기록. REQUEST 사본의 최신성을 확인하기 전 “완료 제외 4/미해결 5”를 실측으로 단정하지 않음. 구 설치본을 덮어쓰지 않음.
4. 아래 정산 도구는 기존 설치본의 StateStore(read_only=True)와 parser만 사용. 별도 watcher·DB schema·예약·새 원장 생성 없음. 실제 보호 키/토큰·DB/WAL/SHM·auto_claims·기존 요청을 직접 수정/삭제하지 않음.

## 2. 한 번에 실행할 읽기 전용 정산
- 도구: `collab/ops/pending_requests_audit.py`, SHA-256 `b21cdbe571b0da0090ab303d0d91ae786f86f3c51bbb47b4cb0756c44ebb4911`.
- 시험: `collab/ops/tests/test_pending_requests_audit.py`, SHA-256 `7aa7674eaa2ffd9f854a4c46312f7cdde7e4c587cb9e81e8caa11304d4229196`.
- 기존 설치본이 v0.2.23/v0.2.25일 때 해당 소스와 실제 SQLite API를 사용한 Linux 회귀 각각 17 PASS. 다른 설치본이면 API·스키마·파이썬 호환부터 격리 확인. 시험 PASS를 Windows 운영 PASS로 바꾸지 않음.
- 먼저 기존 `reconcile`을 기존 config로 실행해 provider별 pending/jobs/lease를 확인. 이 명령도 StateStore read-only 모드임.
- 아래 PowerShell 변수는 **실제 확인한 값**으로 설정. 사용자에게 경로를 다시 묻기 전에 Task/설정/기존 명령을 조사. 결과 파일은 로컬 임시 경로이며 원본 DB가 아님.

```powershell
# $privateRepo, $python, $watcherRoot, $stateDb, $auditOut은 위 조사에서 확정
& $python (Join-Path $privateRepo 'collab/ops/pending_requests_audit.py') --watcher-root $watcherRoot --db $stateDb --requests-root (Join-Path $privateRepo 'collab/requests') --scope github > $auditOut
if ($LASTEXITCODE -ne 0) { throw 'READ_ONLY_AUDIT_BLOCKED; do not change state or approval' }
```

출력에서 `tracked_total`(원시 추적), `completed`(현재 id/revision/ZIP과 일치하는 로컬 완료), `held`(UNCERTAIN/실행·게시 중/충돌), `waiting`, `unverified`, `unresolved_total`을 구분. source 최신성·서명 유효성·실행 권한은 별도. 이 결과의 WAITING은 리뷰 실행 가능 판정이 아니며 이벤트 기록 부재도 과거 호출 0의 단독 증거가 아님.

## 3. Guard의 기존 요청만 정산·조건부 공식 처리
- 정확한 요청: `REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117`, revision 1.
- 고정 입력: `collab/requests/REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117/REQUEST.md`, 원래 Commit A `b2edf8b090b292163864cfbf670c77d1ad09c058`.
- 리뷰 ZIP: `collab/packages/l1-knowledge-guards-three-skill-code_r0001_1117_REVIEW_INPUT.zip`, 25569 B, SHA-256 `a67311473e63e7750ba9aa435f10311767d957b82e059bff0256a5e305c84849`.
- SOURCE_PIN repo_id는 보정된 JSON 문자열 `"1451933830"`. pin/REQUEST/ZIP이 현재 원본과 일치하는지 공식 검사로 확인하며 새 입력으로 바꾸지 않음.
- 먼저 local signing audit·auto_claims·jobs·기존 리뷰 프로세스/실행 로그·dispatch·결과·receipt·비용 이력을 함께 대조. 보호 위임·만료·기존 요청의 유효 USD 1/모델 1회 범위는 공식 signer/admission 도구가 판단. 개발된 일반 $1.5 정책으로 이 요청을 재편집하지 않음.
- 이미 결과/영수증이 있으면 완료 근거만 회수하고 모델 0회. 실행 가능성 불명, 기존 dispatch/유료 실행, in-flight·uncertain이 있으면 **재큐잉/임의 초기화/추가 호출 0**, 정확한 HOLD 근거만 기록.
- 서명 단계에서만 실패했고 미실행이 충분한 근거로 입증되며 **기존 공식 수동 도구가 이 UNCERTAIN 상태를 정상적으로 처리하도록 지원**하는 경우에만 기존 유효 승인 범위로 check → 승인 서명/원격 readback → READY 마지막 게시 → 기존 watcher가 원래 리뷰 1회 → 결과/receipt/비용 정산. 기존 auto_claims를 수동 SQL로 해제하거나 직접 primitive signer로 공식 도구를 우회하지 않음.
- 공식 도구에 해당 지원이 없거나 승인/비용/만료 미충족이면 그 부분만 BLOCKED로 종료. 새 REQUEST/revision/새 리뷰나 새 유료 승인 요청을 자동 생성하지 않음. 이미 승인된 같은 범위 재승인을 반복 요구하지 않음.

## 4. 완료 잔존·구요청·표시 처리
- 기존 완료 4건: `REQ-COWORK-V0214-R1-20261114`, `REQ-COWORK-V0217-R2-20261114`, `REQ-COWORK-V0219-R2-20261114`, `REQ-COWORK-V0220-R1-20261115`. 현재 입력 식별값과 jobs/결과/receipt가 일치하면 실행 대기 집계에서 제외. pending 행·jobs·audit/서명/영수증은 보존.
- “대기 9건”을 만드는 **실제 상태 표시/Notifier 소스**를 찾아, 원시 행 수는 “추적”, 검증된 완료 제외 값은 “미해결”, held는 “보류”로 분리하는 최소 표시 변경만 기존 승인 범위에서 적용. source snapshot 미확인/다른 revision/다른 ZIP은 완료 제외 금지. 관련 합성 입력으로 표시·빈 값/오류/보류 회귀 및 백업·원격 결과를 남김.
- 이 도구만 게시/실행한 것을 기존 Telegram/Windows 상태 표시 수정 완료로 보고하지 않음. 표시 소스 접근·안전한 적용 범위가 없으면 DISPLAY_APPLIED=NOT_RUN/BLOCKED로 구분. 새 watcher ZIP/실행 게이트를 바꿔야 한다면 별도 후보로 남기며 기존 v0.2.25 고정 승인본을 덮어쓰지 않음.
- 구 Budget DESIGN은 같은 ZIP의 LARGE R2 완료로 추가 리뷰 불필요한 미시작 대체 이력. READY/리뷰를 새로 만들지 말고 기존 지원되는 정산/무시 경로가 있으면 적용·이력 보존; 없으면 표시만 분리하고 로컬 종결 미적용으로 기록.
- 구 MSC 구조는 대화형 리뷰/GPT 판정 완료와 watcher NOT_RUN을 구분. 구 Knowledge 설계는 후속 FIXED R1과 남은 범위를 대조하며 중복 유료 호출 없음. Dashboard는 기존 승인 범위 미확인 대기 유지.

## 5. 같은 세션에서 게시·정산까지
PRIVATE `wonhwipark/CoWork-Skill-Collab/main`에 다음을 게시하고 commit·원격 본문·SHA-256을 확인:
1. 결과: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_PENDING_GUARD_RECONCILIATION_RESULT_FOR_GPT_20261118.md`.
2. 비민감 감사 JSON: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/artifacts/pending_guard_audit_20261118.json`. utility 출력은 원문/서명/키/오류 원문을 포함하지 않지만 게시 전에 다시 민감정보 점검.
3. 실제 표시 패치/시험 근거가 있으면 같은 Work의 기존 artifacts/에 보존. raw DB/WAL/SHM·로컬 로그·보호 설정은 게시 금지.
4. migration CURRENT 및 Guard의 L1 CURRENT/TRACKER 현행 필드를 맞추되 transport 완료·기존 MSC 판정/후속 v0.2.26 후보를 덮어쓰지 않음.
5. 결과에 HOST_AUDIT, GUARD_ADMISSION, GUARD_REVIEW, DISPLAY_APPLIED, 모델 실제 호출·비용·미확인, 원본 이력 보존을 각각 PASS/FAIL/NOT_RUN/BLOCKED로 기록. 실행 불가 부분만 차단하고 가능한 정산·표시·게시를 끝까지 수행.

**완료 기준:** 구체적 실측과 필요한 최소 표시 변경이 검증되어 게시되거나, 불확실/권한/실행 경로의 정확한 차단 근거가 보존되어 게시됨. 무근거 재실행이나 단순히 “승인 대기”로 다시 넘기는 것으로 끝내지 않음. 이 문서는 GitHub 등록만으로 Windows에서 자동 실행되지 않음.
