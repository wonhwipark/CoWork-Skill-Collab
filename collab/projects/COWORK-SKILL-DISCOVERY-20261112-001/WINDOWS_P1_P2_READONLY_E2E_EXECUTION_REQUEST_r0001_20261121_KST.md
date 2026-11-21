# Windows Claude Code — P1/P2 실제 읽기 전용 E2E 검증 실행 요청 r0001

- 요청일: 2026-11-21 KST
- 사용자의 현재 지시: “Windows Claude Code에서 P1/P2 실제 동작 검증” 진행 승인
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 정본 저장소: GitHub **PUBLIC** `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 세부 계약: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_AUTO_USE_READONLY_E2E_CHECK_r0001_20261120_KST.md`
- **이 문서는 호스트 실행을 시작하는 트리거가 아님. 게시 여부와 실제 Windows 실행을 분리한다.** 이 문서를 읽은 승인된 Windows Claude Code 세션만 아래 단계를 수행한다.

## 1. 범위·금지

기존 P1/P2 구현 및 2026-11-20 실사용 점검 지침을 **REUSE**, 새로운 Work·엔진·스키마·요청 생성 없음. Windows 실제 로딩/조회/라우팅/안전 분기만 **읽기 전용**으로 확인. 로컬 테스트용 임시 폴더 생성은 허용하지만 CoWork 파일/운영 상태 변경 금지.

- 신규 유료 리뷰, REQUEST/SOURCE_PIN/APPROVAL_SIG/READY, 모델 유료 실행, watcher/서명키/위임/DB/Task/Notifier 변경 **금지**.
- 자동 감시·GitHub Actions 실행·운영 설치/재시작·PUBLIC L1Work 재배포·로컬 강제 pull/reset **금지**.
- 계정 비밀·권한 파일 원문·업무 코드/로그는 화면·GitHub 결과에 게시하지 않음.
- 이미 사용자 승인으로 독립 리뷰를 생략한 P1/P2 구현을 독립 리뷰 PASS로 재표기하지 않음.

## 2. Windows 호스트 검사 순서

1. **실제 Claude Code 환경:** CoWork `main` 체크아웃 폴더에서 새 Claude Code 세션을 시작. `/context all`의 Memory files에서 `CLAUDE.md`, `AGENTS.md`, `collab/CONTEXT_BRIEF.md`의 실제 로딩 여부를 확인. 표시되지 않거나 새 세션을 열지 못하면 `CONTEXT_LOAD=NOT_VERIFIED/NOT_RUN`으로 남기고 정적 파일 존재만으로 PASS 금지.
2. **원격 정합성:** 원격 주소가 정확히 `wonhwipark/CoWork-Skill-Collab`인지 민감정보 노출 없이 확인. `git rev-parse HEAD`와 `git ls-remote origin refs/heads/main`의 SHA를 비교하고 기록. 불일치 시 로컬 조회기는 **오래된 로컬 스냅샷**으로 취급하고 원격 `main`의 최신 CURRENT를 읽기 전용 조회. 자동 pull/reset 금지.
3. **기존 Python 자체 회귀:** 기존 Python이 있으면 저장소 루트에서 `python -m unittest discover -s collab/dashboard/tests -p test_context_query.py -v` 실행. Windows symlink 권한 등으로 실패하면 원시 오류의 비민감 요약·기대/실측을 기록하고 테스트를 임의 SKIP/PASS 변환 금지. 실행하지 못하면 `NOT_RUN`.
4. **동일 Q1~Q5 실사용:** 각 질문에 대해 *자연어로 Claude Code에게 질문*한 경로와 실제 읽은 GitHub `main` CURRENT·필요한 하위 근거를 기록. 로컬 `context_query.py`를 호출했다면 별도로 CLI 여부와 출력의 `LOCAL_CURRENT_READ_ONLY`/호스트 `NOT_VERIFIED`를 구분. 질문/기대 근거는 아래 표 준수.
5. **P2 안전 분기:** 연결 파일이 있더라도 `PRESENT_LOCAL_UNVALIDATED`는 승인/리뷰 실행 증거가 아님을 확인. baseline commit이 없으면 `NO_BASELINE`, 존재하지 않는 정확한 commit이면 `BASELINE_NOT_VERIFIED`. GitHub 접근 실패/로컬 SHA 불일치 시 원격 최신성·실호스트 상태 추정 금지.
6. **결과 보고:** 실제 시험 종료 후에만 기존 결과 경로에 결과·증거·미검증을 게시하고 `CURRENT.md` 최신 요약 갱신. 결과를 원격 readback. 다른 자동화·모델 실행은 없음.

| 질문 | 기대 경로/핵심 검증 |
|---|---|
| Q1 `Watcher LIVE 지금?` | `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md` 및 필요 시 정책 Work; 문서상 LIVE와 직접 호스트 관측 분리 |
| Q2 `USD3 보호 위임?` | `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md`; USD3 설정 보고와 첫 유료 E2E 구분 |
| Q3 `P1/P2 적용됐어?` | 본 Work `CURRENT.md`; 구현 PASS, 독립 리뷰 SKIP, Windows E2E 여부 분리 |
| Q4 `대시보드 현재 형식?` | `collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md`의 관련 절+PUBLIC HTML; D안/P1/P2 화면을 최상단만으로 추정 금지 |
| Q5 `L1 지식 E2E?` | `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`와 관련 하위 흐름; Viewer와 그룹 지식 반영/실행 검증 분리 |

참고 가능한 로컬 조회 (각 실행은 선택적 보조자료이며 자연어 자동 로딩을 대신하지 않음):

```powershell
python collab/dashboard/context_query.py --root . --question "Watcher LIVE 지금?" --topic collab
python collab/dashboard/context_query.py --root . --question "USD3 보호 위임?" --topic auto
python collab/dashboard/context_query.py --root . --question "P1/P2 적용됐어?" --topic skill
python collab/dashboard/context_query.py --root . --question "대시보드 현재 형식?" --topic dashboard
python collab/dashboard/context_query.py --root . --question "L1 지식 E2E?" --topic knowledge
```

## 3. 완료 기준 및 결과 위치

- `CONTEXT_LOAD`: 실제 `/context all` 결과 근거
- `LOCAL_HEAD / REMOTE_HEAD`: 실제 SHA·일치 여부
- `UNIT_TESTS`: 실행 수·PASS/FAIL/SKIP/NOT_RUN
- `Q1..Q5`: 각각 라우팅 Work, 실제 읽은 증거 파일, 주요 답변, 하위 절 확장 여부, `PASS/FAIL/PARTIAL/NOT_RUN`
- `P2_RELATIONS / NO_BASELINE`: 실제 출력 및 완료 오인 방지
- `CONTEXT_QUERY_INVOKED`: 실제 CLI 호출/미호출
- `HOST_ACCESS`, `UNRESOLVED`, `NEXT_ONE_ACTION`, `WINDOWS_CLAUDE_E2E`: 근거에 맞게 판정
- 결과 파일: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CLAUDE_P1_P2_READONLY_AUTO_USE_E2E_RESULT_FOR_GPT_20261120.md` (기존 계약의 파일명 유지)
- 원격 게시: 같은 저장소 `main`, commit + 원격 본문 readback; 기존 `CURRENT.md` 갱신. `WINDOWS_CLAUDE_E2E=PASS`는 실제 Windows 실행 근거가 모두 존재할 때만 사용.
- 독립 리뷰/운영/비용: 이 실행에선 `NOT_REQUESTED / NO_CHANGE / MODEL_CALLS=0` (실제 증거에 한함).

## 4. 게시 시점의 구분

이 요청서 자체는 **GPT가 정본 코드를 조회해 마련한 실행 인계**이며 `WINDOWS_CLAUDE_E2E=NOT_RUN`. 본문만으로 Windows 세션을 시작하거나 Windows 호스트가 GitHub의 신규 문서를 자동 인식하지 않는다. 실제 실행 가능 도구가 없는 환경에서는 이 상태를 유지한다.
