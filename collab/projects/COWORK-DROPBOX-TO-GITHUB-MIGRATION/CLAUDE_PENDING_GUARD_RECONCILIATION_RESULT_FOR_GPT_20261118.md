# CLAUDE Pending·Guard 정산 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-18 KST. 근거: `GPT_PENDING_GUARD_WINDOWS_ONE_SHOT_r0001_20261118_KST.md`, `GPT_AUTO_COLLAB_REMEDIATION_DISPOSITION_r0001_20261118_KST.md`.
- v0.2.25 **재설치하지 않음**. 모델 호출 0, 신규 REQUEST/READY 0, 보호 위임 변경 0, v0.2.26 설치 0.

## 상태값

```
HOST_AUDIT=PASS
GUARD_ADMISSION=HOLD (정확한 근거: 아래)
GUARD_REVIEW=NOT_RUN (admission이 HOLD이므로)
DISPLAY_APPLIED=PARTIAL (breakdown 산출·게시, 설치된 코드의 "pending: N" 텍스트 자체는 미패치)
GATE_TEST_WINDOWS=PASS (24/24, 아래)
MODEL_CALLS=0
```

## 1. 호스트 상태 재확인 (재설치 없음)

- 운영 트리 `D:\User\whpark\skill-collab-watcher-github`: `__version__ = "0.2.25"`(변경 없음). Task `SKILL-COLLAB-GitHub-Watcher` Running, 프로세스 2개. 단일 provider(`github`) 유지.
- Python 3.11.9(운영 venv, 변경 없음).

## 2. HOST_AUDIT — `pending_requests_audit.py` 실행

- 도구/시험 SHA-256 사전 확인: `pending_requests_audit.py` `b21cdbe571b0da0090ab303d0d91ae786f86f3c51bbb47b4cb0756c44ebb4911`(일치), `test_pending_requests_audit.py` `7aa7674eaa2ffd9f854a4c46312f7cdde7e4c587cb9e81e8caa11304d4229196`(일치).
- 시험(`WATCHER_SOURCE_ROOT=실제 설치 트리`): **16 passed, 1 failed**. 실패 1건(`test_cli_runs_against_real_existing_store`)은 테스트 자신의 `subprocess.run(..., text=True)`가 이 Windows 호스트의 로캘(cp949)로 UTF-8 자식 프로세스 출력을 디코드하다 깨지는 **Windows 로캘 전용 테스트 하우징 결함**이다(도구 로직 결함 아님). 실제 CLI를 직접 `encoding="utf-8"`로 호출해 재현·확인: 정상 동작.
- 실제 운영 DB 바이트 복사본(main+WAL+SHM, 복사 전후 해시 동일) + `collab/requests/` 15개 폴더의 REQUEST.md 미러(원격에서 그대로 받음) 대상으로 `--scope github` 1회 실행, 운영 DB·설치본·요청 파일 수정 0:

```
tracked_total=9, completed(로컬 jobs 테이블 기준)=0, held=1, waiting=8, unverified=0, unresolved_total=9
```

- **로컬 `jobs` 테이블에는 4건의 오래된 완료 요청(`REQ-COWORK-V0214-R1-20261114`, `-V0217-R2-20261114`, `-V0219-R2-20261114`, `-V0220-R1-20261115`) 행이 없다**(jobs=[] 반환). 도구가 "실행 이벤트 부재만으로 과거 호출 0을 증명하지 않음" 원칙을 지켜 **완료로 단정하지 않은 것**이지, 결함이 아니다. 이 4건은 **원격에서 직접 재확인**: 각각 `REVIEW_RESULT_1.md` 1개·receipts 2개(RECEIPT_1.md+USAGE_RECEIPT_1.json 또는 동급) 존재 — **4건 모두 독립적으로 완료 확인됨.**
- 따라서 실제 미해결은 **5건**: `REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117`(WAITING, 이전에 PREFLIGHT_BLOCKED로 보고됨), `REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001`(WAITING), `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001`(WAITING, 대화형 리뷰는 별도 완료), `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`(WAITING), `REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117`(HELD/UNCERTAIN).
- 비민감 전체 JSON: `artifacts/pending_guard_audit_20261118.json`(원문 토큰/키/서명 미포함, 게시 전 재점검 완료).

## 3. GUARD_ADMISSION — HOLD (정확한 근거)

- 고정 입력 그대로 확인: `REQUEST.md`(원 Commit A `b2edf8b090b292163864cfbf670c77d1ad09c058`), ZIP 25,569 B SHA-256 `a67311473e63e7750ba9aa435f10311767d957b82e059bff0256a5e305c84849`, `SOURCE_PIN.json` `repo_id` 문자열 `"1451933830"`(보정 확인됨) — **모두 변경하지 않음**.
- `auto_claims`: `stage=UNCERTAIN, attempts=1` 그대로 보존. 자동 재큐잉 없음(`requeue_allowed=false`).
- 공식 수동 승인 도구 점검(`approve_request.py check`, 16/16 PASS) 결과: **`APPROVABLE (cap USD 1.5, 1 call)`.**
- **서명하지 않았다.** 이 요청의 `run_policy_ref=POLICY-STATIC-V1`은 2026-11-16 최초 시도 당시 **USD 1.00** 범위였다. 그 사이(2026-11-18) 같은 정책명의 등록 상한이 **USD 1.50**으로 바뀌었다. 지금 서명하면 이 특정 요청이 원래 승인받지 않은 더 넓은 예산으로 조용히 편입된다 — 두 인계서 모두 "개발된 일반 $1.5 정책으로 이 요청을 재편집하지 않음" / "USD 1.50 확대… 새 유효 승인 전 변경 금지"를 명시했다.
- **판정: GUARD_ADMISSION=HOLD.** 필요한 승인: 이 특정 요청(REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117)에 USD 1.50 적용을 명시적으로 승인, 또는 원래 USD 1.00 범위를 보존할 별도 조치(현재 등록에는 $1.00 등급이 없음). 승인 없이는 `GUARD_REVIEW=NOT_RUN`.

## 4. DISPLAY_APPLIED — 부분

- "대기 9건"의 소스를 찾았다: 감시기 `orchestrator.py`의 `SCAN_END` 로그(`{"dispatched":N,"pending":len(store.list_pending())}`)가 raw 추적 수를 그대로 출력한다. 이 코드는 **보호된 설치 패키지의 일부**라 이번 읽기 전용 원샷에서 패치하지 않았다(별도 후보·독립 리뷰가 필요한 변경).
- 대신 **최소 표시 분리**를 산출·게시했다: `artifacts/pending_guard_audit_20261118.json`의 `display_breakdown_for_the_user_facing_pending_count` = `{tracked:9, remote_verified_completed:4, held:1, unresolved_display:5}`. 이 결과 문서와 artifact가 "추적 9"와 "미해결 5"를 분리해 보여주는 실제 산출물이다.
- **정확히 말해:** 설치된 Notifier나 watcher의 `pending: N` 텍스트 자체는 바꾸지 않았다(`DISPLAY_APPLIED` 전체 PASS 아님). 이 도구 실행·게시만으로 운영 표시 수정 완료를 주장하지 않는다.

## 5. GATE_TEST_WINDOWS — CRLF 수정 커밋 격리 시험

- 커밋 `9b9141bc015a5930a2e57de26b6ab2f73be8223a`의 `collab/ops/tests/test_review_request_gate.py` 원격 readback, SHA-256 `409c956d0220e87d20d490fdfe38786044eb586e63e1c549d8e500818ee8e3ed`(**일치**). 수정은 `self.request.write_bytes(...)`로 바뀐 한 줄(그 외 `write_text`는 JSON 파일이라 CRLF 영향 없음) — 범위가 정확히 최소다.
- 이 파일을 **변경 없는** `review_request_gate.py`와 함께 격리 폴더에 두고 `python -m unittest discover -s tests -p test_review_request_gate.py -v` 실행: **24 passed (기존 23 + 신규 LF 고정 시험 1), 0 failed.** 이전(2026-11-17) 같은 시험은 8 PASS/15 FAIL이었다 — Windows CRLF 하우징 결함이 이 수정으로 해소됨을 직접 확인.
- **범위 한계(정확히):** 이 수정은 `collab/ops/tests/`의 독립 정본 파일에만 적용됐다. **이미 패키징된 v0.2.26 ZIP(SHA `f08adb60…`)은 건드리지 않았고, 그 내부의 동일한 15건 CRLF 실패는 그대로 남아 있다.** 다음 v0.2.26류 후보에서 같은 수정을 반영하려면 새 ZIP SHA·전체 회귀가 필요하다.

## 6. 변경하지 않은 것 / 보존

- 보호 위임(`auto_delegation.json`): 바이트 미변경.
- 운영 DB(main/WAL/SHM), Task, 설정, 키/토큰: 읽기만 함(복사본에서 작업).
- 기존 완료 MSC 두 진입 R1, v0.2.26 ZIP, Dashboard 대기: 변경·재호출 0.
- `REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117`의 `auto_claims`/UNCERTAIN: 그대로 보존.

## 다음 한 동작

GPT가 Guard에 USD 1.50(또는 별도 $1.00 등급 복원) 적용을 승인할지 판정한다. 승인되면 같은 공식 도구(`approve_request.py`)로 check→approve→READY→리뷰 1회→결과 게시를 이어간다. Notifier/watcher의 raw "pending" 텍스트를 실제로 바꾸려면 별도 코드 후보·독립 리뷰 게이트가 필요하다.
