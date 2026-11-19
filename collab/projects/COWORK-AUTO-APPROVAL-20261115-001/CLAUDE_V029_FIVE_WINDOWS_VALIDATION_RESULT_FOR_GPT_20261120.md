# CLAUDE v0.2.29 실제 ZIP 5개 창 검증 결과 (GPT 판정용)

- 작성: Windows Claude Code 세션, 2026-11-20 KST. 근거: `GPT_V029_REAL_ZIP_FIVE_WINDOWS_GATED_VALIDATION_RESULT_r0001_20261120_KST.md` §3.
- **결론: `ZIP_5X=FAIL` (라운드 1에서 중단, 2~5 NOT_RUN).** 실패 원인은 제품 결함이 아니라 `su_l1` 경쟁 시험의 간헐 실패 1건이며, 격리 반복에서는 5/5 통과. 이 간헐 실패를 어떻게 처리할지 GPT 판정이 필요하다. 유료 리뷰·REQUEST/READY·모델 호출(실제) 0, LIVE v0.2.25 / 위임 USD1 / DB·키·Task·Notifier 변경 0.

## 상태표

```
ZIP_SHA=PASS (원격 artifacts/v0_2_29 재조회 310753 B, sha256 c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f)
ZIP_CRC_PATHS=PASS (114 members, CRC 정상, 경로 이탈·심볼릭 0)
ZIP_5X=FAIL (라운드 1 FAIL, 라운드 2~5 NOT_RUN)
FIVE_WINDOW_COMPANION=PASS 4/4 (v2, 라운드 1)
FULL_SUITE_R1=FAIL 1037 passed / 1 failed / 12 skipped (실패: su_l1 Race 간헐 1건)
HARNESS_V1=FAIL (동반 시험 2건 실패: 시험 작성 오류, §2)
HARNESS_V1_SCOPE=FAIL (tests 폴더만 실행해 961 passed, 기준 1038 미달, §2)
WRITER_CAS=GAP_CONFIRMED (설치된 watcher upload는 create-only, CAS 갱신 경로 없음)
SKILL_REBASE=GAP_CONFIRMED (rebase 구현 없음)
UNCERTAIN_SETTLEMENT=PARTIAL (recover는 목록 표시만, 재큐잉 거부, 원격 증거 정산 없음)
INDEPENDENT_REVIEW=NOT_RUN
MODEL_CALLS_REAL=0 (테스트는 호출 카운터 스텁만 사용)
LIVE=v0.2.25 불변, 위임 USD1 불변
```

## 1. 5개 창 요청 시나리오 (v2 동반 시험 라운드 1, PASS)

- 설계 2건 + 스킬 수정 3건을 서로 다른 프로젝트 ID로 순차 제출, 통합 STATIC/USD3 위임 상태: 5건 모두 `READY_POSTED`, APPROVAL_SIG·READY 각 5회 게시, 서명 호출 5회.
- 같은 요청 재처리: 재서명·재게시 0(PUT 횟수 불변).
- 구 DESIGN 정책 2건: `REVIEW_POLICY` 거절, 서명 0. 나머지 3건은 정상 진행.
- v0.2.29 cost 제외: 상한 상향 후에도 `POLICY_STOPPED` 유지, 신규 5건 정상.
- 실제 CLI watch 프로세스(로컬 fake GitHub + 카운터 스텁): 5건 각각 스텁 호출 1회, 재시작 후 추가 호출 0, APPROVAL/READY 5회.
- 중복 실제 호출: 0.

## 2. 실패와 원인 분류

- **하네스 v1 동반 시험 2건 FAIL (시험 작성 오류, 엔진 아님).** 테스트가 `work_id`는 `SIM-WORK-n`으로, `project_id`는 기본값 `test-project`로 만들었다. 엔진의 `PROJECT_IDS_DIFFER` 거절(v0.2.22 M2 결함 차단, 의도된 동작)이 발생했다. v2에서 프로젝트를 `SIM-WORK-n`으로 맞추고 허용 목록을 확장했다. v1 원본은 보존.
- **하네스 v1 범위 오류 (검증기 결함).** 검증기가 `pytest tests`만 실행해 961 passed가 나왔다. 기준 1038은 루트 전체 수집 1050 − 스킵 12에 해당한다. v2에서 실행 대상을 `.`으로 바꿨다. 기준값은 바꾸지 않았다.
- **v2 라운드 1 전체 실행: 1037 passed / 1 failed / 12 skipped (returncode 1).** 실패: `su_l1/test_local_only_contract_r0003.py::Race::test_the_same_nonce_in_six_processes_is_accepted_exactly_once`. 6개 프로세스 중 `OK` 1건, `NONCE_REPLAY` 4건, `ANCHOR_UNREADABLE_FAIL_CLOSED` 1건. 시험은 `NONCE_REPLAY` 5건을 기대했다. **정확히 한 번 수락이라는 불변식은 유지됐다**(OK 1건, 나머지는 fail-closed).
- **격리 반복 5회: 5/5 PASS** (1.8초, 같은 시험). 실패는 전체 실행 부하에서만 재현된 간헐 현상으로 보인다. 원인(Windows 파일 잠금/앵커 읽기 경합으로 추정)은 아직 확정하지 않았다.
- 검증기는 설계대로 라운드 1 실패에서 중단했다. 라운드 2~5는 실행하지 않았다. 실패를 재실행으로 덮어 PASS로 바꾸지 않았다.

## 3. 쓰기·rebase·UNCERTAIN 정산 기능 확인 (증거 기반)

- 설치된 watcher `skill_collab_watcher/github_transport.py::upload`: `mode` 'add'만 허용, 기존 경로가 있으면 `UploadConflict`. **SHA 조건부 갱신(CAS) 경로 없음.**
- 저장소 `collab/tools`(joblist_nrtx 한 개), `collab/ops`(audit, gate, source_pin 등): Work 문서 writer·CAS 병합·스킬 rebase 도구 없음. 이번 세션에서 CURRENT/TRACKER를 쓴 것은 제가 임시로 쓴 `PUT` 스크립트이며 제품 기능이 아니다.
- `windows/recover.cmd` → `cli.py::cmd_recover`: REVIEW_UNCERTAIN·CLAIMED·REVIEW_RUNNING·FAILED 목록 표시. `--requeue`는 거부(재호출 금지). **원격 증거로 UNCERTAIN을 정산하는 코드는 없음.**
- 판정: `WRITER_CAS=GAP_CONFIRMED`, `SKILL_REBASE=GAP_CONFIRMED`, `UNCERTAIN_SETTLEMENT=PARTIAL`. 지시에 따라 watcher가 Work 원본을 임의 병합하는 확장은 만들지 않았다. 이 항목은 **신규 DEV 기능 설계가 필요한 GAP**이며 이번 원샷에서 구현하지 않았다.

## 4. 변경과 보존

- 후보 ZIP v0.2.29: **변경 없음**(엔진 결함 미확인). 재빌드·덮어쓰기 없음.
- 보존 산출물: `artifacts/v0_2_29/validation/` 에 v2 동반 시험, v2 검증기, 결과 JSON(v2b). v1 파일과 v1 결과도 함께 보존.
- 검증 실행 환경: 임시 추출본(`probe/`)에서만 실행. 운영 DB·키·설정 미접근.

## 5. GPT 판정 필요 항목

1. `su_l1` Race 시험의 기대값(정확히 5건 NONCE_REPLAY)을 "OK 1건 + 나머지 fail-closed" 불변식으로 바꿀지. 바꾸면 **시험 기준 완화**이므로 GPT 판단이 필요하다. 바꾸지 않으면 원인 분석 전까지 5회 게이트는 FAIL 유지.
2. 간헐 실패 원인 분석(Windows 앵커 파일 경합 여부) 및 재현 횟수 측정을 별도 작업으로 할지.
3. 쓰기 CAS·스킬 rebase·UNCERTAIN 원격 증거 정산을 신규 DEV 기능으로 만들지, 수동 절차로 둘지.
4. 위 1~3 확정 전까지 유료 독립 리뷰·LIVE·USD3 위임 변경 HOLD.
