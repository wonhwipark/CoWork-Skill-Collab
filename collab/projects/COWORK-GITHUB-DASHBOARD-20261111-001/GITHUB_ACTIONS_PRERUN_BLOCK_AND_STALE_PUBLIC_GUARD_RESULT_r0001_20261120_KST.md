# CoWork PRIVATE Actions 실행 전 실패·PUBLIC 지연 안전표시 — 점검 및 적용 결과 r0001

- 2026-11-20 KST / 기존 Work: `COWORK-GITHUB-DASHBOARD-20261111-001` / PRIVATE `wonhwipark/CoWork-Skill-Collab/main`
- 사용자 승인: Actions 오류 원인 조사 → 가능한 최소 복구 → PUBLIC 최신 상태 정합성 및 P1/P2 검증. **유료 모델 호출/Windows LIVE 변경·서명·READY·비용/Actions 예산 변경/임의 재실행 없음**.
- **최종 판정:** `ACTIONS_PRERUN_FAILURE=CONFIRMED`, `ERROR_ANNOTATION_TEXT=NOT_ACCESSIBLE`, `ROOT_CAUSE=NOT_VERIFIED`, `PRIVATE_GENERATE=BLOCKED`, `PUBLIC_ALLOWLISTED_SYNC=BLOCKED`; `PUBLIC_STALE_GUARD=POSTED`, `SYNTHETIC_JS_REGRESSION=PASS`, `PUBLIC_PAGES_BUILD=PASS`, `ACTUAL_BROWSER=NOT_RUN`.

## 1. 실패 근거와 코드 문제 여부 분리

| 비교 | 직전 성공 | 최신 실패 대표 |
|---|---|---|
| Workflow run | [#44720614237](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44720614237) | [#44756245749](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44756245749) |
| GitHub 결과 | success | failure |
| 시작 시각 UTC | 2026-11-20 10:36 | 2026-11-20 14:43 |
| Runner | ID 1000002806 | ID **0**, 이름 없음 |
| 실제 workflow steps | **7** | **0** |
| Actions run timing | 시작·정상 실행 | billable total_ms **0**, run_duration_ms 3000 |
| Check run annotation | 별도 확인 불요 | **1개 존재** (내용 연결 API 접근 제한) |
| Workflow 파일 Git blob | `806576617650fb601acfaaea859a6d12aa8a989d` | **동일** `806576617650fb601acfaaea859a6d12aa8a989d` |

- 해당 실패는 Python 단위시험·대시보드 생성에 **도달하기 이전**임이 확정. 동일한 workflow YAML이 성공 당시와 실패 당시 같으므로, 단순 Python 코드 수정·workflow 재작성으로 복구될 근거는 없음.
- GitHub check-runs API에서 `generate` annotation_count=1은 확인했으나 `/check-runs/{id}/annotations` GET이 현재 GitHub 연결에서 허용되지 않음. workflow_job_logs 재조회도 BlobNotFound를 반환했으므로 **오류 문구 원문 미확보**.
- **원인 가설만**: 계정 Actions 사용량/예산·결제 잠금, 저장소 Actions 허용 정책, Runner 배정 제한, 플랫폼 문제. **원인 확정/과금액 확정 아님**. GitHub 공식 안내 https://docs.github.com/en/actions/how-tos/troubleshoot-workflows , https://docs.github.com/en/actions/concepts/billing-and-usage .
- 실패할 때 후속 PUBLIC sync가 `skipped`인 것은 workflow 조건 `upstream.conclusion=='success'`을 충족하지 못하기 때문이며, 정상 fail-closed. **PUBLIC JSON 직접 덮어쓰기·조건 해제·다른 runner로 우회 실행 금지**.

## 2. PRIVATE 운영 상태 원본의 최소 정합성 보강

- 2026-11-20 [v0.2.29 LIVE 호스트 보고·GPT 판정](../COWORK-AUTO-APPROVAL-20261115-001/GPT_V029_LIVE_CUTOVER_FINAL_DISPOSITION_r0001_20261120_KST.md)은 단일 GitHub Watcher LIVE, STATIC USD3, 보호 위임 USD3, 첫 유료 E2E `NOT_RUN`.
- 기존 이관 `CURRENT.md` 최상단이 11/18의 Guard 과거 상태여서 `flow_view.snapshot()` 및 `public_sync._read_active_provider()`가 `ACTIVE_PROVIDER=GITHUB`/`CUTOVER=LIVE`를 찾지 못했음. 사용자 이전 지시 범위 내에서 이관 Work 최상단에 **이미 수용된 실제 호스트 보고**를 링크하고 정형 값만 보강, PRIVATE commit `75c4a99178a5de3ea2f57c0a8d47b6b8760c8f22`. 새 호스트 실측과 별개.
- PUBLIC `L1Work/main/docs/cowork-dashboard/status.json`는 원격 `generated_at=2026-11-20T09:23:06Z`, `cutover=정식 전환 전`, `checks.active_provider=기록 미확인` 그대로. **PUBLIC 상태 동기화는 BLOCKED**이고 이것을 실제 LIVE=OFF로 해석해서는 안 됨.

## 3. PUBLIC의 30분 지연 안전표시 최소 수정·배포

기존 PUBLIC 상태 `status.json`의 공개 허용 필드와 기존 네 카드·P2 관계·변경분·3개 탭을 그대로 유지.

- `L1Work/main/docs/cowork-dashboard/context-view.js`: snapshot `generated_at`가 브라우저 기준 30분보다 오래되면 **'최신 상태 미확인 · 공개 자료 갱신 지연'** 및 '**마지막 공개 기록(현재 상태 아님)**'으로 구분, P2 변경분 비교를 보류·기준 초기화. 최신 검증 JSON 도착하면 정상 렌더 복귀. SHA-256 `f1c5aaad1f28e20882a89e892931e04801d8b283fc7861ffa13b4d5fa9b5759a`, **7278 bytes**, Git blob `c67b769693fe9e8ea78f91dced82944629084607`, source commit `fe0f47ba4e3a88e7177dee8f3faa66eb322a4bf5`.
- `L1Work/main/docs/cowork-dashboard/index.html`: JS 캐시 버전 `context-view.js?v=p1p2-20261120-stale1`만 갱신. SHA-256 `f2a8f4c19b780b3c57eb9a1577d91f5e439d5949af656f20ab113490a75d8ee0`, **26422 bytes**, Git blob `e64601363aadbdeedafd3dd83f492346d10e55b9`, commit `f0b45aa69bafafced6bc9680166dbd9707517634`.
- GitHub Pages [#44757131366](https://github.com/wonhwipark/L1Work/actions/runs/44757131366) `completed/success`; 새 `main` HTML+JS 파일 원격 본문 및 blob 확인 PASS. **서비스 HTTP 수신/실제 PC·Android 렌더는 NOT_VERIFIED/NOT_RUN**.
- 실제 공개 UI: https://wonhwipark.github.io/L1Work/cowork-dashboard/

### 합성 DOM 시험
1. 기존 오래된 공개 JSON → 스탬프 30분 지연 표시, 4카드 최신 미확인, 각 카드 과거 공개 상태만 유지, 변경분 보류 **PASS**.
2. `generated_at=now` 신규 유효 JSON → 기존 카드 상태 복구/변경분 baseline 없음 **PASS**.
3. 동일 브라우저의 이후 공개 phase 변경 → P2 변경 감지 **PASS**.
4. 비허용 provider/변조 카드 → 상태·관계·변경분 fail-closed **PASS**.
5. 변경 소스 V8 문법 검사·same-origin `status.json`·`textContent` 사용 유지 **PASS**.

## 4. 계정/Runner 진단 — 사용자 확인이 필요한 단 한 가지

1. 브라우저에서 [PRIVATE 실패 실행 #44756245749](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44756245749) 열기 → 실패한 `generate` 검사/상단 빨간 오류 메시지(체크 주석)를 확인.
2. **표시된 오류 메시지의 비민감 문구만** GPT에 전달. 화면에 토큰/비밀키/전체 로그가 있으면 복사하지 않음.
3. 오류가 billing·budget·account lock 유형일 때만 GitHub 사용자 **Settings → Billing and licensing → Usage/Budgets → Actions**를 확인. 실제 과금·예산 상향·결제 수단·정책 설정은 **새 비용 승인 필요**, 이번 변경으로 진행하지 않음.
4. 오류가 Actions permissions/runner 유형이면 repo **Settings → Actions → General** 및 GitHub 장애 상태 확인. 실제 권한 변경 전 현재 제한 원문 확인. **단순 반복 rerun/자가 호스팅 전환으로 우회하지 않음.**
5. 외부 차단이 해결된 이후에만 기존 PRIVATE 대시보드 자동화 1회 정상 성공 여부와 allowlisted PUBLIC sync 성공, 최종 remote `status.json` readback, 공개 첫 화면 동작을 순서대로 검증. 과거 실패 run의 일괄 rerun 불필요.

## 5. GPT·Windows Claude P1/P2 맥락 검증 경계

- GPT 측 실제 Q1~Q5 선택 조회 결과/Windows 호스트 동일 질문 검증 절차는 [기존 검증 문서](../COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_AUTO_USE_READONLY_E2E_CHECK_r0001_20261120_KST.md)로 재사용. GPT `PASS_WITH_LIMITATION`.
- Windows Claude Code의 로컬 CoWork checkout 최신성, `/context all` 3파일 자동 로딩, `context_query.py` 실제 실행, Q1~Q5 호스트 반복은 **NOT_RUN**. GitHub에 `CLAUDE.md`와 검증 안내를 게시했으나 로컬 Agent 실행 트리거가 아님.
- LIVE v0.2.29/위임/DB/Task/Watcher 변경 0; 신규 REQUEST/READY/모델 호출 0; PUBLIC schema/allowlist 변경 0; 신규 Work/원장/자동 감시 0.

**NEXT_ONE_ACTION:** 사용자에게 GitHub 실패 `generate` 검사의 빨간 오류/annotation 메시지의 비민감 한 줄을 확인받아 Actions 계정 제한 또는 인프라 원인을 확정한다. 그 후 이미 승인된 범위에서 자동 생성·allowlisted 동기화의 정상화만 검증. Windows P1/P2 호스트 E2E는 별도 host 접근 시 실제 실행 근거로 정산.
