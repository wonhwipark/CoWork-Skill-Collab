# LIVE 실행 요청서 (비실행) — watcher v0.2.29 컷오버 / USD3 통합 정책

- 작성: Windows Claude Code, 2026-11-20 KST. 근거: `GPT_V029_REVIEW_ACCEPT_AND_USD3_PRELIVE_STAGING_ONESHOT_r0001_20261120_KST.md` §5.2, 결과 `CLAUDE_V029_USD3_PRELIVE_READINESS_RESULT_FOR_GPT_20261120.md`.
- **이 문서는 실행 트리거도, 설치·정지·설정·위임·키 변경의 승인도 아니다.** `collab/requests/` 아래에 두지 않았고 APPROVAL_SIG·READY·SOURCE_PIN이 없어 watcher가 소비하지 않는다.
- **상태:** `LIVE_REQUEST_GATE=PASS`, `LIVE_EXECUTION_REQUEST=POSTED_CONDITIONAL`, **`LIVE_EXECUTION=NOT_RUN`(AWAITING_OPERATING_APPROVAL)**, `LIVE_ENABLE=NOT_RUN`.

## 1. 대상

- 저장소/브랜치/Work: PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main` / `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`.
- **설치할 바이트(검토된 바이트 그대로):** `artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip`, 310753 B, SHA-256 `c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f`. 독립 리뷰 `REQ-COWORK-V029-ONEOFF-R1-20261120`(BLOCKING 0 / MAJOR 0 / MINOR 3), GPT `ACCEPT_WITH_CONDITIONS`.
- **현재 LIVE(2026-11-20 19:4x KST 실측):** 설치 트리 SHA `f691bcf808cbf81e9c2c2a9be65335e527c2df99ea4d54a427665e4c90045c9f`(108개 파일), v0.2.25 패키지 `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`와 패키지 파일 104개 동일. 설정 SHA `fbce30a97c06f8d04e2e0029c731c41d2ccd87963196afe80279f10cf7509c27`, 위임 SHA `ddead4e497759ac30db9e8d90974cfe4f68114d99ef99cdf85a083e9bf54fd4c`.
- **목표 정책 상태(한 번에 함께 적용):** `POLICY-STATIC-V1` 등록 비용 **USD 3.00** + 보호 위임 `max_request_usd` **3.0** + **신규 `enabled_at`**. `POLICY-STATIC-V1-LARGE`·`-DESIGN` 등록은 이력·수동 승인 호환용으로 유지(v0.2.29는 자동 승인하지 않음). `expires_at`은 기존 2026-12-16T19:47:50+09:00을 **연장하지 않음**(연장은 별도 결정).

## 2. 신규 `enabled_at` 규칙 (필수)

1. 값은 **watcher가 정지된 상태에서 위임 파일을 쓰는 시각**(ISO-8601, +09:00)으로 새로 정한다.
2. 이전 값(2026-11-16T19:47:50+09:00)보다 **낮추거나 같게 하지 않는다**, `expires_at`보다 앞이어야 한다.
3. 적용 직전에 `classify_legacy.py`를 다시 돌려 "STATIC·이력 없음·활성 중 관측" 요청이 **0건**임을 확인한다. 그리고 쓰기 시각이 원격 `collab/requests/*`의 모든 REQUEST 최초 커밋 시각보다 늦음을 확인한다.
4. **이유(격리 시험으로 입증):** 상한만 올리고 `enabled_at`을 갱신하지 않으면 이력 없는 STATIC 구 요청이 자동 승인된다. 신규 `enabled_at`을 같이 적용하면 구 요청은 `RETROACTIVE_OR_FUTURE_REQUEST` 등으로 모두 차단된다.

## 3. 컷오버 순서 (운영자 승인 수동 절차)

1. **사전 재확인(실행 시점):** §5 체크리스트. 하나라도 미충족이면 중단하고 `AWAITING_OPERATING_APPROVAL` 유지.
2. watcher 작업 `SKILL-COLLAB-GitHub-Watcher` **정지**(진행 중 리뷰·in-flight job 0 확인). Notifier는 건드리지 않는다. Dropbox 시대 작업은 Disabled 유지(단일 provider).
3. **백업:** 설치 트리, `reviewer.config.json`, `auto_delegation.json`·신뢰 루트 사본(개인키·암호문 제외), DB 일관 스냅샷(온라인 백업 API; main/WAL/SHM 직접 복사 금지), 작업 XML, SHA 매니페스트. 리허설에서 쓴 `rehearsal.py` 방식. 저장 위치는 **운영자가 이 시점에 지정**(Dropbox 동기화 폴더 밖, 예: 기존 관례의 `D:\User\whpark\skill-collab-watcher-dist` 아래 또는 설치 폴더의 형제 폴더).
4. **설치:** 고정 ZIP의 SHA·CRC 확인 후 설치 트리의 코드·도구·문서를 교체. **운영 `config/reviewer.config.json`과 `package/`는 덮어쓰지 않는다**(ZIP에는 `reviewer.config.example.json`만 있음). 교체 후 트리 SHA와 `__version__ = "0.2.29"` 확인.
5. **보호 설정 적용(한 번에):** 등록 STATIC 3.00 + 위임 `max_request_usd` 3.0 + 신규 `enabled_at`. 파일은 직접 승인으로만 수정.
6. **재가동 전 검증(모델 호출 0):** 격리 DB 사본으로 `cli config-check`/`recover`, 신규 정책에서 `review_request_gate select/check --intent unified --required-budget-usd 3.00` 통과, 위임 로더(Windows ACL 포함) 사용 가능, 구 요청 분류 재실행.
7. **재가동은 별도 LIVE 승인 후에만.** 작업 시작 → **2주기 관찰 + 재시작 1회**: 구 요청 서명·READY·모델 호출 0, 중복 provider 0, 오류 이벤트 없음.
8. 첫 실제 신규 요청에서 자동 서명·READY·리뷰 1회·영수증 일치를 확인하기 전에는 `LIVE 유료 E2E`를 검증된 것으로 표기하지 않는다(`NEW_LIVE_PAID_E2E=NOT_RUN` 유지).

## 4. 롤백 (이상 발견 즉시)

- 트리거: 설치 SHA 불일치, 위임·설정 로드 실패, 구 요청 서명·READY 발생, 중복 provider, 재시작 후 비정상, 임의의 예외.
- 순서: watcher 정지 → 설치 트리·설정·위임을 백업 번들로 복원 → SHA 대조 → 인터프리터·작업 폴더 확인 → (별도 승인 후) 재가동. **DB는 컷오버 후 유료 job이 처리되지 않았을 때만 스냅샷으로 복원**한다. 처리됐다면 DB는 그대로 두고 트리·설정·위임만 되돌린다.
- 보존: 실패·UNCERTAIN 원시 기록, 이전 완료·불확실 요청은 모델 재실행 0.
- **금지:** 옛 인터프리터 폴더 `D:\User\whpark\skill-collab-watcher`(실제 운영 작업이 `.venv`를 사용)의 이동·삭제·이름 변경.

## 5. 실행 시점에 다시 확인할 체크리스트 (사전검증은 격리·리허설 기준이며 아래는 실행 시점 확인 사항)

- [ ] **LIVE 운영 변경에 대한 사용자의 명시적 승인** 또는 유효한 기존 사전 위임의 정확한 범위·한도·만료. (없으면 `LIVE_EXECUTION=AWAITING_OPERATING_APPROVAL`)
- [ ] 보호 파일 쓰기 권한: 위임·설정 편집 권한(운영자 직접 승인)과 작업 정지·시작 권한.
- [ ] **백업 저장 위치 지정**과 번들 매니페스트 검증, 롤백 책임자 확인.
- [ ] in-flight job 0, 진행 중 리뷰 0, `jobs` 미완료 0.
- [ ] 설치할 ZIP SHA `c67bc342…`와 직전 LIVE 트리 SHA `f691bcf8…`가 위와 같다(다르면 그 사이 다른 변경이 있었으므로 중단하고 재측정).
- [ ] 분류 재실행 결과: STATIC·이력 없음·활성 중 관측 0건, UNCERTAIN은 Guard 1건 그대로.
- [ ] `development_not_for_deployment` 라벨 해제 여부를 **별도 운영 결정서**로 기록(설치 SHA·시각·이전 SHA·승인자·결과·롤백 결과 포함).
- [ ] (선택) `reviewer.config.json`·설치 폴더의 `Authenticated Users:(M)` 상속 권한 강화 여부.

## 6. 근거 링크

결과 문서 `CLAUDE_V029_USD3_PRELIVE_READINESS_RESULT_FOR_GPT_20261120.md`, 리뷰 `collab/reviews/REQ-COWORK-V029-ONEOFF-R1-20261120/REVIEW_RESULT_1.md`, 영수증 `collab/receipts/REQ-COWORK-V029-ONEOFF-R1-20261120/RECEIPT_1.md`, 검증 산출물 `artifacts/v0_2_29/validation/usd3_prelive/`.
