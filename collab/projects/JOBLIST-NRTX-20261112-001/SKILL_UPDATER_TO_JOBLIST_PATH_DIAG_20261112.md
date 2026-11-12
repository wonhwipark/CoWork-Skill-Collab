# Skill-Updater → Job-list 실행 경로 진단 — 2026-11-12

- Work: `JOBLIST-NRTX-20261112-001`
- Branch: `wonhwipark/CoWork-Skill-Collab/main`
- 대상 호스트: Linux; 프로젝트 루트 `/home/whpark/Project/smp1900`; 기존 OpenCode Web은 사용자 보고상 복구됨
- 상태: `SOURCE_STATIC_REVIEW=PARTIAL`, `HOST_RUNTIME_DIAG=NOT_RUN`, `HOST_MODIFICATION=NOT_RUN`
- 이 문서 게시 자체로 Skill-Updater/Job-list/OpenCode를 실행하지 않는다.

## 1. 과거 실측(2026-11-12 07:44, 사용자 제공 Agent MCP 화면)

- Skill-Updater `job-list 0.4.36 installed=remote`, `CURRENT / SKIPPED(NO_ACTION)`.
- Catalog `source=active`, Job `JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01`.
- Registry 대상 Job 없음. Queue `DONE / SUCCESS / attempts=1`이지만 `enqueued_at=null`, `worker_started_at=null`, `run_id=null`.
- 07:10 `activate --launch` `PARTIAL_SUCCESS` — 어느 Job의 실패인지는 해당 기록만으로 미확정.
- MCP result `RESULT_UNSUPPORTED`; `bridge_result_allowlist`에 대상 ID 없음.
- 이 증거는 실행 진입 전/결과 추적 경계 문제를 보여주며 **smp1900 코드 분석 실행/변경의 근거가 아님**.

## 2. 배포 당시 코드에서 확인한 경로 계약

PUBLIC `wonhwipark/L1Work/main` v0.4.36 생성 이력에서:
- Commit `a5ee212b6`: 활성 요청 `requests/one-shot-jobs.json`의 Job ID가 `...-EXEC-01`; Profile `nr-l1tx-knowledge-research-linux`; `scripts/job_core.py`의 `BUILTIN_SAFE_PROFILES`에서 `entrypoint=scripts/nr_tx_knowledge_linux_job.py`, `retry=0`, `semantic_result_path=output/nr_tx_knowledge_research/latest_result.json`.
- Commit `d33d8fe78`: Worker `JOB_ID=...-EXEC-01`; `preflight(root, Path.home().resolve())`가 canonical `$HOME/l1sw-private-skills/job-list`와 환경변수 `JOB_LIST_JOB_ID`, `JOB_LIST_PROFILE`, `JOB_LIST_RUN_ID`를 검증.
- Worker가 소스 루트를 `home / "Project" / "smp1900"`로 계산하여 Git HEAD/branch/status를 조회하고, `opencode run --dir <source> --agent build <prompt>`를 **새 subprocess**로 실행하도록 설계.
- `OPENCODE_CONFIG_CONTENT`, `OPENCODE_DISABLE_AUTOUPDATE` 등 제한은 해당 OpenCode 자식 프로세스에 전달하도록 구현. 지속 중인 별도 OpenCode Web 환경의 영구 변경을 주장할 근거는 없음.
- 생성/게시 후 ZIP CRC·해시·33 pytest는 PASS였으나 **호스트 Skill-Updater → activate → Registry → Runner 종단 시험은 없었음**.
- 위 정적 소스와 **호스트에 설치된 실제 파일 내용/바이트 동일성은 별도 readback 필요**. PRIVATE v0.4.35 후보의 Job ID(`...-MSC-01`)를 현재 v0.4.36 Job ID(`...-MSC-EXEC-01`)와 혼동 금지.

## 3. 과거 Skill-Updater 설치 계약 참고

2026-10-28 직접 분석한 `skill-updater_v0_5_44_1027.zip` 기록에 의하면:
- 일반 update 스크립트 `scripts/skill_updater.py`와 외부 Bootstrap `~/l1sw-bootstrap/l1sw_bootstrap.py`의 호출 계약은 별개.
- Skill-Updater의 **자기 업데이트**는 `STAGED_NOT_INSTALLED` 가능, `self_update_policy=manual_canary`나 `automatic_after_exit`와 외부 `cycle --apply-after-exit` 여부에 좌우.
- 현재 설치 버전·호출하는 실제 진입점·Bootstrap 설정은 호스트에서 미검증. 자기 업데이트 계약과 **Job-list post-install activation은 서로 다른 단계**이며 혼동 금지.
- 참고 이력 `R017_skill_updater_self_install_20261028`, `R018_skill_updater_staged_cycle_gap_20261028`. 이력 위치는 분석 컨텍스트로만 사용하며 저장소 운영 변경 없음.

## 4. 호스트 진단 순서 (실제 read-only)

1. Skill-Updater의 **설치된 버전, MCP/OS 예약 호출 스크립트 실경로, 실행 사용자/UID, `HOME`, CWD, `PATH`, CLI 인자**를 관측. 비밀값/환경변수 전체 출력 금지.
2. **Job-list 0.4.36 설치 전후** journal/receipt/activation hook 기록: ZIP 검증과 교체 완료 vs `activate --launch` 호출 여부를 분리. updater 자기 STAGED/Bootstrap 상태는 관련된 경우만 확인.
3. 실제 호출 루트 `$HOME/l1sw-private-skills/job-list` 존재, 심링크/권한, `VERSION`, `requests/one-shot-jobs.json`, `scripts/job_core.py`, Worker 내부 Job ID, `BUILTIN_SAFE_PROFILES` 비교. 과거 ZIP이 아니라 **현재 로드한 파일**을 확인.
4. 07:10 `auto_20261112_071000_6b537804`의 **개별 Job별** activate 결과/첫 실패 단계 확인. `PARTIAL_SUCCESS`를 이 Job의 FAIL로 가정 금지.
5. Catalog → Registry → Queue/Receipt까지 `...-EXEC-01`의 일관성/중복 소모 여부 확인. Registry 미등록 원인이 설치 병합/정책/검증/activation hook/상태 조회 범위 중 어디인지 구분.
6. Runner가 실제 실행됐을 때만 `JOB_LIST_JOB_ID/PROFILE/RUN_ID` 전달, `HOME` 해석, `$HOME/Project/smp1900`, installed skills, OpenCode CLI 발견/인자, Worker preflight의 차단 코드를 조사. Run ID가 없으면 Worker 실행 실패로 오진하지 말 것.
7. MCP `bridge_result_allowlist`·`job_result_read` 결과 조회는 실제 실행과 별개로 조회 등록 경로를 진단.

## 5. 원인 확정 기준

- `A: updater launch not invoked`: 해당 Job의 설치 완료 이후 활성화 트리거가 존재하지 않거나 호출되지 않았다는 원본 기록.
- `B: activation/registry rejected`: 실제 활성화 함수의 Job별 reason code/검증 분기 및 Registry 상태 불일치.
- `C: dispatch/runner failed`: Registry 등록은 됐으나 Queue/Runner 생성 경계에서 실패 근거.
- `D: worker preflight failed`: Run ID/worker started 확인 및 Worker의 구체 reason code.
- `E: MCP result read unsupported`: 조회 제한/allowlist 문제만 확인되면 독립적으로 추적, 실행 원인으로 섣불리 지정하지 않음.

## 6. 안전조건과 결과

- **기존 Job 재등록, `activate --launch` 재호출, Queue/DB/Registry/운영 설정 변경, OpenCode Web 재설정/프로세스 종료, 소스 수정 금지**.
- 읽기 전용 비교/로그 분석만 수행; 회사 원문 소스·원문 로그·비밀값은 호스트 밖에 복제/게시 금지.
- 결과는 8자리 숫자 및 비민감 `reason_code`는 로컬에서 보존. 숫자 계약은 다음과 같다.

**숫자 응답(8자리)**: 1~6은 `1=정상 확인, 2=오류 확인, 3=미확인, 4=도구 미지원`.
1) Updater 실제 진입점/버전 확인
2) Job-list 0.4.36 설치 및 로드 파일 일치
3) 해당 Job post-install 활성화 호출
4) 활성화/Registry ID 등록
5) Runner Run ID 생성 및 Worker 시작
6) MCP Result 조회 허용/조회 가능
7) 최초 실패 단계: `1=Updater 트리거, 2=Job-list 활성화/Registry, 3=Queue/Runner, 4=Worker preflight, 5=복합, 6=미확정`
8) 우선 수정 대상: `1=Skill-Updater, 2=Job-list, 3=MCP Wrapper, 4=Skill-Updater+Job-list, 5=복합, 6=미확정`

숫자 자체는 원인과 증거를 대체하지 않는다. 호스트에 정확한 진단 근거가 없는 항목은 `3`으로 보고하고, 실제 원인 판정을 위해 비민감 reason code/검증 근거를 현장에 보존한다.
