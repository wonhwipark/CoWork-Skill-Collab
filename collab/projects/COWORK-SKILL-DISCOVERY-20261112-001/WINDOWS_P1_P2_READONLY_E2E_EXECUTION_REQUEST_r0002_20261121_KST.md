# Windows Claude Code P1/P2 실사용 E2E — 실행 경계·비용·전달 보완 r0002

- 작성: 2026-11-21 KST
- Work: `COWORK-SKILL-DISCOVERY-20261112-001` (기존 Work 재사용, 신규 Work/REQUEST 아님)
- 대상: GitHub **PUBLIC** `wonhwipark/CoWork-Skill-Collab`, `main`
- 교체 대상: [r0001 검증 인계](WINDOWS_P1_P2_READONLY_E2E_EXECUTION_REQUEST_r0001_20261121_KST.md) — 원문 보존, 이후 실행은 **이 r0002** 우선
- 기존 검증 기준: [P1/P2 5문항 검증 r0001](P1_P2_AUTO_USE_READONLY_E2E_CHECK_r0001_20261120_KST.md)
- 입력 구현 경로: `collab/dashboard/context_query.py` (확인된 Git blob `a6a1f99849bf524646c1e9264c42acefbf215714`), `collab/dashboard/tests/test_context_query.py` (Git blob `89d433b976383a02653fcabb4085fbd42a313a34`); Windows 실행 시 최신 `main`과 재대조
- 요청 승인 범위: 사용자의 P1/P2 실사용 검증 및 **무과금 로컬 시험/비민감 결과 게시** 지시. 신규 유료 모델 호출·정식 독립 리뷰·LIVE 변경 승인은 아님.

## 0. 전달·실행 계약 — 트리거가 아님

이 MD는 **GitHub에 게시된 호스트 작업 인계**이고, 다음 조건 없이는 실행되지 않는다.

1. GPT: 최신 Work와 요청 내용을 확정해 `main`에 게시하고 GitHub readback 확인. **`HANDOFF_POSTED`까지만 판정**.
2. **실제 Windows Claude Code 사용 세션의 운영자/사용자:** Windows의 CoWork checkout에서 세션을 시작하고, 이 문서를 명시적으로 열어 실행을 지시한다. 기존에 승인·설치된 운영용 명령 전달 수단이 확인된 경우에만 그 수단을 사용할 수 있다. **현재 이 세션에서 자동 감시/원격 Windows CLI 전달 경로는 확인되지 않았다.** MD·CURRENT 게시만으로 실행·수신·ACK를 만들지 않는다.
3. Windows Claude Code: 먼저 원격 정본·기존 결과(있을 경우)·실제 사용권한을 확인하고 **로컬 무과금 시험**을 수행. 자연어 질의는 아래 §2의 모델 사용 게이트를 통과하는 경우에만 수행.
4. Windows Claude Code: 실제 실행된 항목만 결과/증거를 기존 Work에 게시 후 commit·원격 본문/bytes readback 확인. GPT는 결과가 존재하면 판정하며, 결과 게시 실패를 이유로 로컬 시험/모델 호출을 다시 실행하지 않는다.

현재 인계만 게시된 경우: `HANDOFF_POSTED=PASS`, `HOST_RECEIPT=NOT_VERIFIED`, `WINDOWS_E2E=NOT_RUN`.

**사용자/Windows Claude Code 세션에 전달할 한 번 복사 지시문:**

> GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab` branch `main`의 `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/WINDOWS_P1_P2_READONLY_E2E_EXECUTION_REQUEST_r0002_20261121_KST.md`를 읽고, 기존 Work에서 §1 무과금 로컬 검증부터 1회 실행해줘. §2 자연어 Q1~Q5는 이미 허용된 Claude Code 세션/이용 한도 내에서만 진행하고, 새 유료 비용이 필요하거나 권한이 불분명하면 `BLOCKED_MODEL_AUTH`로 남겨줘. 유료 리뷰·REQUEST/READY·LIVE 변경은 금지. 실제 결과만 기존 Work에 게시하고 원격 readback 후 보고해줘.

## 1. Windows 무과금 로컬 검사 (모델/API 호출 없는 명령 범위)

- **기준 체크:** CoWork checkout에서 실행. `git remote -v` 출력에서 자격증명/토큰은 절대 보고하지 않고 신뢰된 `wonhwipark/CoWork-Skill-Collab` 원격인지 확인. `git rev-parse HEAD`, `git ls-remote origin refs/heads/main`을 **읽기 전용**으로 실행해 로컬/원격 SHA 기록. GitHub 접근 장애 시 `REMOTE_HEAD=NOT_VERIFIED`. 일치하지 않으면 자동 `pull/reset/checkout` 금지, 로컬 조회 결과를 최신으로 판정 금지.
- **세션 로딩:** 실제 Claude Code 세션에서 `/context all`의 Memory files에 `CLAUDE.md`, `AGENTS.md`, `collab/CONTEXT_BRIEF.md`가 보이는지 확인. 실제 도구에서 `/context all`이 없거나 해당 항목이 확인되지 않으면 그 사유와 `CONTEXT_LOAD=NOT_VERIFIED` 기록. GitHub 파일 존재나 정적 import만으로 PASS 금지.
- **Python 기존 단위시험:** 설치된 Python을 사용해 `python -m unittest discover -s collab/dashboard/tests -p test_context_query.py -v` 실행. 결과의 개수 및 PASS/FAIL/ERROR/SKIP를 사실대로 기록. 파일 생성은 로컬 임시 시험 데이터에 한정. Windows symlink 권한 등으로 실패했으면 FAIL/ERROR로 기록하고 성공인 척하지 않음.
- **조회기 안전 분기:** 신뢰된 로컬 `main` 정합성이 확인된 경우에만 `python collab/dashboard/context_query.py --root . --question "P1/P2 적용됐어?" --topic skill` 실행. `LOCAL_CURRENT_READ_ONLY`와 `host_execution=NOT_VERIFIED_BY_LOCAL_FILES`, `NO_BASELINE` 등의 실제 출력 확인. HEAD 불일치면 이 명령은 과거 데이터 검사용으로만 허용하고 실행 판정은 `STALE_LOCAL`.
- P2 관계의 `PRESENT_LOCAL_UNVALIDATED`는 파일 존재만 뜻하며 승인·비용·실제 Claude 리뷰 증거가 아니다. 고정 baseline commit이 없다면 변경분 `NO_BASELINE`; 존재하지 않는 40-hex commit은 `BASELINE_NOT_VERIFIED`. 원격 오류나 미검증 입력에서 추정 금지.
- 이 절은 **로컬 코드 검증**이고 Claude Code 자연어 맥락 선택 E2E까지 PASS를 의미하지 않는다.

## 2. Claude Code 자연어 Q1~Q5 — 모델 사용 게이트

- 새로 지급/과금되는 Claude API·독립 리뷰 runner·GitHub Actions GPT API 호출은 금지. **실제 기존 사용자가 이미 허용한 Claude Code 세션 및 요금/잔여 한도 내의 자연어 검증만** 이 요청의 범위에 포함한다. 세션 이용권·모델 요금·권한·비용이 불명확하거나 신규 별도 유료 호출이 필요하면 자연어 시험 **중지**하고 `MODEL_AUTH=NOT_VERIFIED`, `Q1..Q5=BLOCKED_MODEL_AUTH`로 기록. 사용자에게 비용이 발생하지 않았다고 추정하지 않는다.
- 유효한 세션에 한해 아래 질문을 각 1회 입력한다. 같은 질문의 자동 재질의/유료 재리뷰·대량 실험 금지. 사전 입력·출력에 민감정보 노출 금지.
- 질문별 `topic / Work ID / 실제 원격 CURRENT·결과 경로 / 자료 시점 / 답 / 미확인 / 최상단 외 관련 하위절 확장 여부 / 조회기 실제 호출 여부 / 판정`을 기록한다.

| Q | 자연어 입력 그대로 | 기대 자료 확인 |
|---|---|---|
| Q1 | `Watcher LIVE 지금?` | `COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` — GitHub 보고와 Windows 직접 관측 분리 |
| Q2 | `USD3 보호 위임?` | `COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md` — USD3 운영 보고와 실제 첫 유료 E2E 분리 |
| Q3 | `P1/P2 적용됐어?` | 본 Work `CURRENT.md` — 구현 적용과 독립 리뷰 SKIP/Windows E2E 구분 |
| Q4 | `대시보드 현재 형식?` | `COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md` + PUBLIC HTML — D안 타임라인과 P1/P2 카드의 다른 작업 흐름 연결 |
| Q5 | `L1 지식 E2E?` | `L1-WORKSPACE-RAG-20261111-001/CURRENT.md` 관련 하위절 및 증거 — Viewer와 실제 그룹 지식 게시·업무 E2E 구분 |

`CURRENT` 최상단이 직접 답하지 않는 Q4/Q5는 관련 하위 최신 결과·영수증으로만 확장. 지침 전체를 매번 재로딩하지 않는다. Q1/Q2도 Windows 설정 직접 관측 없이 GitHub 기록을 운영 실측으로 승격하지 않는다.

## 3. 변경 가능한 대상·결과·종료 기준

**읽기 전용 범위:** 모든 소스/설정/위임/DB/watcher/Actions/리뷰 이력 및 공개 L1Work. 신규 `collab/requests/`, SOURCE_PIN, 서명, READY, 정식 리뷰, 모델 작업 생성 0. 자동 알림·예약/감시 추가 0.

**게시 허용 범위 (실제 시험 결과가 생긴 뒤):**
- `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CLAUDE_P1_P2_READONLY_AUTO_USE_E2E_RESULT_FOR_GPT_20261120.md` (기존 결과 경로 유지, 없는 경우 최초 생성)
- 같은 폴더 `CURRENT.md`의 **최신 상태·근거·NEXT_ONE_ACTION만** 안전 갱신
- 필요한 기존 `TRACKER.json`의 현행 파생 필드만 CURRENT와 정합화 (새 원장 생성 금지)
- 그 외 파일 변경 금지. 게시 전 비밀/업무 제한 원문 제거, HEAD 경쟁이면 실제 최신 원본 재조회 후 무손실 갱신. 게시 실패로 모델·분석 재실행 금지.

**결과 필수 필드:** `LOCAL_HEAD`, `REMOTE_HEAD`, `CONTEXT_LOAD`, `PYTHON_TEST`, `P2_RELATIONS`, `CONTEXT_QUERY_INVOKED`, `MODEL_AUTH`, `Q1..Q5`, `HOST_ACCESS`, `UNRESOLVED`, `NEXT_ONE_ACTION`, `WINDOWS_CLAUDE_E2E`, 실제 게시 commit/readback. 결과별 `PASS/FAIL/SKIP/NOT_RUN` 정확히 구분.

**완료 판정:** `WINDOWS_CLAUDE_E2E=PASS`는 실제 Windows 세션에서 로딩·원격 정합성·Python 시험·허용된 자연어 5문항/확장·P2 fail-closed가 **모두 확인**됐을 때만. 일부는 `PARTIAL/NOT_RUN/BLOCKED`로 분리. 검증 실패 시 기존 P1/P2 운영 적용·과거 사용자 리뷰 생략 기록을 임의 변경하지 않는다.

## 4. 현재 전송 상태

2026-11-21 이 문서의 GitHub 게시/원격 확인만 가능. Windows 세션에 대한 직접 명령 전달·실행 ACK 경로는 이 GPT 세션에 연결되지 않았으므로 `HOST_RECEIPT=NOT_VERIFIED` 및 `WINDOWS_E2E=NOT_RUN` 유지. Windows Claude Code를 실제 구동하거나 자동 서명/READY/모델 호출을 하지 않았다.
