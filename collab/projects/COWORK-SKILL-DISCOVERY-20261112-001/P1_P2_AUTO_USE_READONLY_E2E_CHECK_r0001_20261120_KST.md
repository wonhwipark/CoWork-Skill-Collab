# P1/P2 실사용 자동 조회 검증 — GPT 5문항 결과 + Windows Claude Code 읽기 전용 체크 r0001

- 작성: 2026-11-20 KST / CoWork PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 소유 Work: `COWORK-SKILL-DISCOVERY-20261112-001`; B안/PUBLIC 상태 차단 확인은 `COWORK-GITHUB-DASHBOARD-20261111-001`.
- 사용자 최신 지시: 자동 맥락 조회 검증·안전한 상태 정합성 복구. **실제 Windows 호스트 실행 승인/유료 리뷰/운영 config 변경은 이번에 포함하지 않음.**
- 게이트: READ_ONLY, GitHub main에서 실제 CURRENT 조회; `REQUEST/READY/APPROVAL_SIG`/정기·유료 모델 호출/운영 변경 0. 외부 테스트 자동 게시·자동 감시·새 장기 상태 원장 만들지 않음.

## 1. GPT 측 실측: 맥락 목적별 최신 정본 5문항

실행: 이 GPT 세션에서 연결된 GitHub PRIVATE main의 실제 파일들을 개별 readback. 재사용된 브리프→Work CURRENT→필요한 결과 접근, `context_query.py`를 GPT 호스트에서 실행했다고 주장하지 않음.

| 질문 | P1 Work 경로 | 이번 조회 결과 | 판정 |
|---|---|---|---|
| Q1 'Watcher LIVE 지금?' | 이관 CURRENT, 필요 시 자동 승인 CURRENT | 최상단 `ACTIVE_PROVIDER=GITHUB/CUTOVER=LIVE`, 호스트 보고 v0.2.29 링크, 유료 E2E 미검증을 분리 | GPT 조회 PASS |
| Q2 'USD3 보호 위임?' | 자동 승인 CURRENT | v0.2.29, STATIC USD3, 위임 USD3, `LIVE_PAID_E2E=NOT_RUN` 확인 | GPT 조회 PASS |
| Q3 'P1/P2 적용됐어?' | 스킬 관리 CURRENT | P1/P2 적용, 이번 범위 독립 리뷰 SKIP, PUBLIC 4카드 안내 확인 | GPT 조회 PASS |
| Q4 '대시보드 현재 형식?' | 대시보드 CURRENT + PUBLIC HTML | CURRENT 첫 절은 D안 타임라인, P1/P2는 다음 절·PUBLIC HTML에서 확인 | **추가 조회 후 확인**, L0만으로는 불충분 |
| Q5 'L1 지식 E2E?' | L1 Knowledge CURRENT | 최상단은 Viewer 편집 R1 리뷰·설계 r0002 관련, 전체 지식 Updater 실행/그룹 게시 성공은 상단에 없음 | **L0 불충분**, 관련 하위 흐름 추가 조회·업무 호스트 확인 필요 |

**판정:** 5개 질문의 선택 Work 경로 조회는 성공했지만, 단일 CURRENT 맨 위만 읽는 원칙은 다중 작업 Work에서 2/5 질문의 충분한 답을 보장하지 못함. 이것을 모델 정확도 60%나 성능 벤치마크 수치로 과장하지 않음. 30문항 골든셋·조회시간·토큰은 여전히 NOT_RUN.

### 사용 규칙 최소 보완
- CURRENT 첫 절이 질문 주제에 직접 답하지 않으면 그 Work의 **관련 최신 하위 제목·결과/영수증**을 추가 조회 (반복 전체 문서 상시 로딩 금지).
- 실행 완료 질문이면 정본의 직접 증거(호스트 결과/영수증/원격 readback)가 필수. 못 확인하면 `CURRENT_NOT_VERIFIED` 또는 `HOST_NOT_VERIFIED`.
- P2 관계 출력은 각 REQUEST의 파일 존재/메타데이터일 뿐 완료 판정이 아니다. baseline 없으면 변경분을 추정하지 않음.

## 2. Windows Claude Code — 실제 로컬 E2E 체크 (미실행)

### 필수 조건
- Windows Claude Code에서 CoWork PRIVATE `main` 최신 checkout 작업 디렉터리로 시작.
- 해당 호스트의 `/context all` **Memory files**에서 `CLAUDE.md`, `AGENTS.md`, `collab/CONTEXT_BRIEF.md` 실제 로드 여부 확인. 활성 세션에 GitHub 파일 게시만으로 자동 import됐다고 추정하지 않음.
- GitHub 원격 main commit과 로컬 HEAD를 읽기 전용 대조. SHA 불일치 시 로컬 CLI 조회는 캐시된 정보로만 취급하고, 승인이 없는 로컬 강제 pull/reset·파일 변경은 하지 않는다.
- Python 3.11 등 기존 허용된 로컬 런타임이 있으면 `python collab/dashboard/context_query.py --root . --question "Windows watcher LIVE 지금?" --topic collab`을 읽기 전용으로 실행할 수 있음. 설치된 도구 옵션부터 대조. 수동 또는 세션 내 첫 호출 여부를 명확히 기재.
- Q1~Q5를 **같은 문구**로 순차 입력하고 각 질문마다 `route / CURRENT main SHA / 실제 읽은 증거 파일 / 답변 / 미확인 / 조회기 호출 여부` 기록. Q4/Q5에서는 CURRENT 아래 다른 흐름을 찾아 확장되는지 검증. 실호스트 상태는 별도 직접 관측되지 않으면 완료로 쓰지 않음.

### 검증용 기대
| 테스트 | 성공 조건 |
|---|---|
| 호스트 시작 로딩 | /context all에 3개 파일 실제 노출 또는 `HOST_AUTOLOAD=NOT_VERIFIED` |
| Q1 | migration LIVE와 v0.2.29 운영 보고는 별도 호스트 근거로, 신규 유료 E2E는 NOT_RUN |
| Q2 | 승인 USD3 정책·위임의 적용과 첫 유료 E2E를 분리 |
| Q3 | P1/P2 사용자 리뷰 생략을 독립 리뷰 PASS로 표현하지 않음 |
| Q4 | D안 공개 타임라인 + P1/P2 4카드 모두 확인. PUBLIC JSON의 최신성 별도 표시 |
| Q5 | 상단 Viewer 작업만으로 전체 지식 게시 E2E PASS 주장 금지. 관련 Work 흐름을 좁혀 필요 근거 확인 |
| P2 관계 | REQUEST/REVIEW/RECEIPT가 없는 상태와 존재만 하는 상태를 구별, SHA/호스트 실행 자동 주장 금지 |
| 실패 안전 | GitHub 조회 실패 시 마지막 확인 시점과 미확인 표시; 모델 호출/WRITE 없이 종료 |

### 결과 위치 (실행 시에만)
- Windows Claude Code는 시험이 **실제로 진행된 뒤에만** 기존 Work `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CLAUDE_P1_P2_READONLY_AUTO_USE_E2E_RESULT_FOR_GPT_20261120.md`에 비민감 결과를 작성하고 원격 본문 확인. 실제로 기록할 항목: `LOCAL_HEAD`, `REMOTE_HEAD`, `CONTEXT_LOAD`, `Q1..Q5`, `CONTEXT_QUERY_INVOKED`, `HOST_ACCESS`, `UNRESOLVED`, `NEXT_ONE_ACTION`.
- 이 문서 자체는 실행 신호가 아니라 실행 지침. 유효한 별도 host 세션이 없으면 `WINDOWS_CLAUDE_E2E=NOT_RUN`. 예약/감시/REQUEST/READY 생성 없이 대기.

## 3. 공개 대시보드 상태 정합성·CI 진단

- 2026-11-20 21:08 KST Windows host 결과: Watcher v0.2.29/GitHub LIVE, STATIC/보호 위임 USD3, first paid E2E NOT_RUN. CoWork PRIVATE 자동 승인 Work 최신 결과에서 재확인.
- 기존 migration CURRENT 최상단에는 11-18 Guard 단락만 있어 `flow_view.snapshot`와 `public_sync._read_active_provider`가 `ACTIVE_PROVIDER`/`CUTOVER`를 찾지 못함. PRIVATE main `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`를 **11-20 LIVE 근거 최상단 절**로 최소 갱신 (commit `75c4a99178a5de3ea2f57c0a8d47b6b8760c8f22`).
- 2026-11-20 13:22 UTC PRIVATE `cowork-dashboard.yml` Action `44743762139` = `failure`; job의 `runner_id=0`, steps=[], 시작~종료 1초. 후속 PUBLIC sync `44743774215` = `skipped`. 로그 다운로드 요청은 `BlobNotFound`여서 정확한 계정/Actions/Runner 실패 이유 확인 **BLOCKED**. Python 생성 코드가 실패했다고 단정하지 않음.
- PUBLIC `L1Work/main/docs/cowork-dashboard/status.json`의 관측 상태는 2026-11-20 09:23:06Z 생성, `cutover=정식 전환 전`, `active_provider=기록 미확인`. **PUBLIC_CURRENT_STATUS=STALE/NOT_VERIFIED**, Windows LIVE 자체가 전환 전이라는 의미가 아님.
- 허용목록 동기화 작업은 CI 검증 후에만 `status.json`에 게시. GitHub API로 수동 덮어쓰거나 공개 허용목록을 확대해 우회하지 않음.
- 마지막 성공 PRIVATE Actions와 현재 failure는 구별, 먼저 GitHub Actions Runner 사용량/실행 권한/계정 요금 한도/실행 경고 등 **실제 run UI의 비밀 없는 메시지**를 확인해야 함. Runner 0/step 0은 실행 코드 전 단계에서 종료됐다는 증거지만 구체적 원인은 아직 확인되지 않음.
- 액션 실행이 정상화되면 **기존** PRIVATE generator → allowlist PUBLIC sync → L1Work Pages 실서비스 JSON readback을 순서대로 검증. 불확실/실패 중에는 재실행 반복·수동 공개 덮어쓰기 금지.

## 4. 이번 범위 판정

- `GPT_SCOPED_SOURCE_LOOKUP=PASS_WITH_LIMITATION` / 실제 5문항과 원격 현재상태 조회 근거 있음.
- `WINDOWS_CLAUDE_CONTEXT_AUTOLOAD=NOT_RUN`; `WINDOWS_P1_P2_SCRIPT_EXECUTION=NOT_RUN`; E2E 결과 보고서 아직 없음.
- `PRIVATE_MIGRATION_CURRENT_STATUS=UPDATED_AND_POSTED`; `PUBLIC_STATUS_SYNC=BLOCKED_BY_ACTIONS_RUNNER`; `PUBLIC_SERVING_LIVE_LABEL=NOT_VERIFIED`.
- `WATCHER_LIVE_CONFIG_CHANGED=NO`, `PAID_MODEL_CALLS=0`, `NEW_REVIEW_REQUESTS=0`, `NEW_AUTOMATIONS=0`.
- **NEXT_ONE_ACTION:** Actions failure 상세 원인(브라우저 경고 및 계정 Actions billing/runner 가능 상태)을 확인하고 기존 자동 파이프라인이 정상 복구될 때 공개 JSON readback 검증. Windows Claude Code는 별도 기존 허용 read-only 세션에서 Q1~Q5 검증 후 결과 게시.
