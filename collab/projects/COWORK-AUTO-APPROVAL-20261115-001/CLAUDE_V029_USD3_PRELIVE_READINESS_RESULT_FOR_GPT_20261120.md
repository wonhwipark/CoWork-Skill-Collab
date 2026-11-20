# CLAUDE v0.2.29 USD3 정책 정합화 · LIVE 사전검증 결과 (GPT 판정용)

- 작성: Windows Claude Code 세션, 2026-11-20 KST(호스트 측정 19:4x). 근거: `GPT_V029_REVIEW_ACCEPT_AND_USD3_PRELIVE_STAGING_ONESHOT_r0001_20261120_KST.md` §2~5, 사용자의 이 원샷 실행 지시.
- **결론:** 실측으로 확인할 수 있는 사전 게이트는 모두 통과했다(`HOST_PRELIVE_GATE=PASS`, 기준은 읽기 전용 실측 + 운영과 분리된 격리 시험·리허설). 따라서 §5.2에 따라 비실행 LIVE 실행 요청서를 게시했다(`LIVE_EXECUTION_REQUEST=POSTED_CONDITIONAL`). **LIVE 설치·정책 적용·위임 변경·재가동은 하나도 하지 않았고 `LIVE_ENABLE=NOT_RUN`이다.** 실제 정책 적용과 운영자 승인은 컷오버 시점의 별도 단계이다.
- ZIP: `artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip`, 310753 B, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`. 바이트 불변.

## 상태표 (근거 종류: 실측=운영 호스트 읽기 전용 / 격리=운영과 분리한 실제 코드 시험·리허설 / 재사용=이전 증거 / 설계=컷오버 시점)

```
GPT_DISPOSITION=ACCEPT_WITH_CONDITIONS (GPT 판정서·CURRENT 확인), INDEPENDENT_REVIEW=COMPLETE (R1 BLOCKING 0 / MAJOR 0 / MINOR 3), 호스트 비용 USD 0.5387501 이미 정산, 신규 비용 0
STAGED_STATIC3_SELECT_CHECK=PASS [격리] 임시 설정(STATIC 3.00)에서 `--intent unified` select/check 통과, 음성 8건 fail-closed(실제 운영 설정이 막히는 경우 1건 포함), 실제 설정 해시 불변
LEGACY_EXCLUSION=PASS [실측+격리] 실제 요청 18건 분류에서 "STATIC·이력 없음·활성 중 관측" 0건, 합성 소급 분류 5종 모두 자동 승인 0
PROTECTED_POLICY_CAP_ALIGNMENT=PASS_STAGED [격리] 등록 3.0 + 위임 3.0 정합 시 신규 요청 READY, 불일치 시 영구 제외(§3). 실제 운영 값은 STATIC 1.50 / 위임 1.00 그대로
NEW_ENABLED_AT_PLAN=DEFINED [설계] 컷오버 쓰기 시각으로 신규 고정(이전 값보다 낮추지 않음), 이유는 §2에서 시험으로 입증
SU_L1_OFF=PASS [실측] LIVE 런타임 참조 0, 설정 플래그 없음, 패키지 README "NOT wired"
BACKUP_READY=PASS_REHEARSAL [실측+격리] 일관 스냅샷 방법·번들 생성·검증 통과(§4). 내구 저장 위치 지정과 책임자 확인은 컷오버 시점 항목
ROLLBACK_READY=PASS_REHEARSAL [격리] 번들 복원 트리가 운영 트리와 동일, 복원 v0.2.25가 운영용 인터프리터로 복원 DB를 읽음. 운영 위에 덮어쓰는 복원은 하지 않음
SINGLE_PROVIDER=PASS [실측] provider_lease=github, GitHub watcher 작업 1개 Running, Dropbox 시대 작업 3개 Disabled
SHADOW_5WINDOW=PASS [격리+재사용] staged USD3 5창 READY 각 1회·재처리 PUT 0·구 DESIGN 거절, 이전 실제 ZIP 5회 5/5 증거 재사용
CLI_2CYCLE_RESTART_REHEARSAL=PASS [격리] 실제 watcher CLI, 컷오버 후 2주기 구 요청 모델 호출 0, 신규 1건 리뷰 스텁 1회, 재시작 후 추가 0
SOURCE_ZIP_SHA=PASS, SIGNER_ACL_AND_SCOPE=PASS [실측] (참고 §5의 설정 파일 ACL 관찰)
HOST_PRELIVE_GATE=PASS (실측·격리·리허설 기준)
LIVE_REQUEST_GATE=PASS, LIVE_EXECUTION_REQUEST=POSTED_CONDITIONAL, LIVE_EXECUTION=NOT_RUN (AWAITING_OPERATING_APPROVAL), LIVE_ENABLE=NOT_RUN
INDEPENDENT_REVIEW_NEW=0, MODEL_CALLS_NEW=0 (시험의 모델 호출은 호출 카운터 스텁뿐), 신규 REQUEST/READY/서명 0
HOST_PROTECTED_CHANGE_BEFORE_AFTER=변경 없음 (설치 트리 SHA·설정 SHA·위임 SHA·작업 상태·DB job/claim 분포가 측정 전후 동일)
```

## 1. 실측: 운영 호스트(읽기 전용)

- **설치 SHA:** 설치 트리 108개 파일, 트리 SHA `f691bcf8…`, `__version__ = "0.2.25"`. v0.2.25 패키지(`skill-collab-watcher_v0_2_25_1117.zip`, 283930 B, SHA `26d63c8a…`)의 파일 104개와 **모두 바이트 동일**. 추가 4개는 운영 설정 1개와 보관된 이전 패키지 3개.
- **실효 설정:** `POLICY-STATIC-V1` 1.50, `-LARGE` 3.00, `-DESIGN` 3.00, 일/월 한도 null. **보호 위임:** `enabled=true`, `max_request_usd=1.0`, `enabled_at` 2026-11-16T19:47:50+09:00, 만료 2026-12-16T19:47:50+09:00, 계열 `COWORK-`·`L1-WORKSPACE-`, skill 3종, repo_id `"1451933830"`. 로더(Windows ACL 검사 포함)로 사용 가능 확인.
- **작업:** `SKILL-COLLAB-GitHub-Watcher` Running, `SKILL-COLLAB-Notifier` Running, `...Claude-Review-Watcher`·`...Dashboard-Deploy-Bridge`·`...Dashboard-Updater` Disabled. watcher 프로세스는 venv 런처와 자식 인터프리터 한 쌍.
- **DB(일관 스냅샷, 온라인 백업 API):** `integrity_check=ok`, jobs 9건 전부 `COMPLETED`, auto_claims `READY_POSTED` 2 / `UNCERTAIN` 1, auto_seen 11, pending_requests 9, provider_lease 1(github).
- **보호 변경 도구:** 이 설치 트리의 위임·설정을 갱신하는 자동화 도구는 **없다.** 기존 `ops/deploy.ps1`은 옛 Dropbox 시대 설치(`skill-collab-watcher`, 작업 `SKILL-COLLAB-Claude-Review-Watcher`)용이고 GitHub 트리용으로 검증되지 않았다. `README_OPS`가 설정 파일 수정은 항상 직접 승인한다고 명시. 따라서 컷오버는 **운영자 승인 수동 절차**이다.

## 2. 소급 차단 (GPT §2-2, §2-4)

**실제 요청 18건 분류 (원격 목록 + 일관 스냅샷):** 이력 있음(job·READY·영수증) 13, 비활성 중 첫 관측 3(STATIC, 이력 없음), UNCERTAIN claim 1(Guard 코드), 이력 없는 DESIGN 1(`REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117`). **STATIC 등급이면서 이력 없이 활성 중 관측된 요청은 0건**이다.

**격리 시험(합성 구 요청 5종, 컷오버 전후):**

| 구 요청 분류 | 신규 `enabled_at` 적용 후 | `enabled_at` 갱신 없이 상한만 올린 경우 |
| --- | --- | --- |
| A. STATIC, 활성 중 관측, 이력 없음 | `RETROACTIVE_OR_FUTURE_REQUEST` (차단) | **`READY_POSTED` (자동 승인됨)** |
| B. DESIGN, 이력 없음 | `RETROACTIVE_OR_FUTURE_REQUEST` | `REVIEW_POLICY` (v0.2.29가 DESIGN을 자동 승인하지 않음) |
| C. 비활성 중 첫 관측 | `PRE_EXISTING_REQUEST` | `PRE_EXISTING_REQUEST` |
| D. 완료됨 | `READY_POSTED` 반환(멱등), 서명·PUT 증가 0 | 동일 |
| E. UNCERTAIN | `UNCERTAIN` (종결) | 동일 |

- 컷오버 후 신규 요청은 `READY_POSTED`, 구 요청에 대한 서명 호출 증가 0·PUT 증가 0·모델 호출 0.
- **핵심 결론:** `enabled_at` 갱신은 선택이 아니라 필수다. 갱신 없이 상한만 올리면 분류 A가 실제로 자동 승인된다. 현재 운영 DB에는 분류 A가 0건이어서 오늘 기준 노출은 없지만, 컷오버 직전에 같은 분류를 다시 돌려 0건임을 확인해야 한다(`classify_legacy.py`).
- 다른 fail-closed(전부 서명 0): 만료 위임 `DELEGATION_EXPIRED`, 다른 repo 위임 `PIN_MISMATCH`, 허용되지 않은 skill `SCOPE`, 허용되지 않은 프로젝트 `PROJECT_NOT_IN_SCOPE`, 비활성 위임 `DISABLED`, DESIGN·LARGE 라벨 `REVIEW_POLICY`, 숫자형 repo_id `PIN_MISMATCH`, SHA·크기 불일치 `PACKAGE_INVALID`, SOURCE_PIN 없음 `PIN_MISSING`, signer 없음 `INPUT_OR_TRUST`.

## 3. 정책 정합 (GPT §2-3, MINOR 2 조건)

- **함께 적용한 경우(등록 3.0 + 위임 3.0):** 신규 요청 `READY_POSTED`, 예약 300센트, 서명 1회.
- **등록만 먼저 올린 경우(위임 1.0):** 요청이 `PER_REQUEST_COST`로 거절되고 `POLICY_STOPPED`로 영구 제외, 이후 위임을 3.0으로 올려도 `POLICY_STOPPED` 유지(서명 0). 이것이 MINOR 2의 운영 함정이며 **watcher를 멈춘 상태에서 등록 비용·위임 상한·`enabled_at`을 한 번에 적용**해야 하는 이유다.
- **게이트 도구(`--intent unified`, 격리 설정 STATIC 3.00):** select `POLICY_COMPATIBLE_NOT_APPROVED`, check `PASS_PREPUBLICATION_ONLY`. 음성: 가격 2.00 `POLICY_COST_MISMATCH`, 요청이 DESIGN·LARGE 이름 `RUN_POLICY_NOT_LIVE_MATCH`, SHA·크기 변조 불일치, 예산 1.50 `UNIFIED_REVIEW_BUDGET_MISMATCH`, 숫자형 repo_id 거부. 실제 운영 설정에서는 여전히 `POLICY_COST_MISMATCH`.

## 4. 백업·롤백 리허설 (운영과 분리, 쓰기는 임시 폴더에만)

- 번들 114개 파일: 설치 트리 108개 + 보호 파일 사본(위임, 신뢰 루트 2개; **개인키·암호문 사본 0**) + DB 스냅샷 + 작업 XML 2개 + 매니페스트. DB 스냅샷의 행 수는 운영 DB와 일치, `integrity_check=ok`.
- 복원: 복원 트리의 SHA가 운영 트리와 동일, 복원된 `v0.2.25`의 `cli recover`가 **운영용 인터프리터**로 복원 DB를 읽고 "no uncertain/in-flight/failed jobs"를 출력. 리허설 후 운영 설치·위임 SHA 불변.
- **롤백 판정 규칙(설계):** 컷오버 후 이상 시 watcher 정지 → 트리·설정·위임을 번들로 복원. DB는 컷오버 후 **유료 job이 처리되지 않았을 때만** 스냅샷으로 되돌린다(처리됐다면 이력 보존을 위해 DB는 그대로 두고 트리·설정·위임만 되돌림). v0.2.29가 DB에 쓰는 것은 `POLICY_STOPPED` 0센트 행뿐이며 스키마 변경은 없다.
- 실측 의존성: 운영 작업의 인터프리터는 옛 설치의 `D:\User\whpark\skill-collab-watcher\.venv\Scripts\pythonw.exe`, 작업 폴더는 GitHub 설치 폴더이다. **그 옛 폴더를 이동·삭제하면 롤백과 컷오버 모두 깨진다.** Notifier도 같은 venv와 `skill-collab-watcher-dist\notifier`를 쓴다.

## 5. 관찰·한계 (게이트 비차단, 판정 입력)

- **ZIP이 운영 설정을 덮어쓰지 않음:** ZIP의 `config/`에는 `reviewer.config.example.json`만 있다. v0.2.29는 새 감사 이벤트 이름을 추가하지 않아(`AUTO_EXCLUDE`는 읽기 전용 저장소의 섀도 로그 라벨) Notifier 이벤트 목록 변경은 필요 없다.
- **ACL:** 위임 파일은 SYSTEM과 운영자 계정만(F), 승인 키는 운영자 계정만. 반면 `reviewer.config.json`과 설치 폴더에는 `Authenticated Users:(I)(M)`가 상속돼 있어 이 PC의 아무 로컬 계정이 수정할 수 있다. 단일 사용자 PC이므로 비차단으로 두지만 컷오버 시 강화 여부를 운영자가 판단할 사항이다(이번에 변경하지 않음).
- **실제 정책 적용·실제 서비스 정지/교체/재가동·운영 위의 복원은 설계상 NOT_RUN**이다. 이 PASS는 격리 시험과 리허설에 근거하며 LIVE 검증 PASS가 아니다.
- **`su_l1`:** 활성화·연결 금지 유지, 관측된 실패의 원인은 여전히 UNRESOLVED.
- **리뷰 한계(GPT 조건):** R1은 변경분과 호출 지점 중심의 정적 리뷰였다. 운영 게이트의 SHADOW·롤백·legacy 제외는 이 문서의 시험이 보완하며, 실제 LIVE 동작은 컷오버 후 별도 확인 대상이다.
- **ZIP 밖 정오표(GPT 문서 고정):** `docs/AUTO_APPROVAL.md` 29·74행의 일/월 상한 서술은 현 코드와 불일치. 일·월 한도는 텔레메트리일 뿐 거절 게이트가 아니다.
- **개발 라벨:** `CUTOVER_RUNBOOK`의 `development_not_for_deployment`는 이 문서로 해제되지 않는다. 컷오버 시 설치 SHA·시각·이전 SHA·승인자·결과를 별도 운영 결정서로 기록해야 한다.
- 3건의 비활성 중 첫 관측 STATIC 요청과 이력 없는 구 DESIGN R1은 영구 제외된다. 필요하면 수동 승인만 가능.

## 6. LIVE 실행 요청서와 다음 한 동작

- `LIVE_ENABLE_EXECUTION_REQUEST_V029_20261120_KST.md`를 같은 Work에 비실행 문서로 게시했다(`collab/requests/` 아래 아님, READY·APPROVAL_SIG 없음). 컷오버 순서, 신규 `enabled_at` 규칙, 롤백 판정, **실행 시점에 다시 확인할 체크리스트**가 담겨 있다.
- **다음 한 동작(사용자):** 위 실행 요청서를 보고 실제 LIVE 운영 변경을 승인할지 결정. 승인하면 같은 요청서의 체크리스트를 실행 시점에 다시 확인한 뒤 컷오버를 진행한다. 승인 정보가 없으면 `LIVE_EXECUTION=AWAITING_OPERATING_APPROVAL`로 유지된다.

## 7. 하지 않은 것

LIVE 정지·교체·재가동, 설정·위임·`enabled_at`·가격 변경, 서명키·DB·Task·Notifier 변경, 보호 파일 쓰기, 신규 REQUEST/READY/서명, 유료 리뷰·모델 호출, 기존 요청 재큐잉, 패키지 바이트 변경.
