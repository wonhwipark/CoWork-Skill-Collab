# Job-list v0.4.38 / Linux MCP 복구 현황 — 원격 실행 경계 확인

- 기준: 2026-11-17 KST / r0001
- 기존 Work: `JOBLIST-NRTX-20261112-001` (Job-list/MCP 진단). NR 코드 분석의 실제 완료 판정은 `NR-L1TX-CODE-ANALYSIS-20261115-001`에서 별도 관리
- 증거 수준: 사용자 제공 모바일 Agent 화면의 **읽기 전용 조회 결과** 및 앞서 게시한 r0003 인계 문서. Linux 호스트 원본 파일·실행 로그를 GPT가 직접 읽은 것은 아님
- 이 문서 게시 자체는 Linux MCP·Job-list 운영 실행, 패치, 재큐잉, 승인, 유료 호출의 트리거가 아님

## 현재 요약 / 분리 판정

| 항목 | 최신 관측·판정 |
|---|---|
| GitHub 인증 / Skill-Updater | 사용자 측 PAT 복구 후 Skill-Updater 수행 보고. Linux 인증 장애 해소 관측; **모바일 Agent의 `github_exec` 401과는 인증 주체가 다름** |
| Job-list 설치 | 모바일 Agent `job_capabilities_read`에서 설치 `0.4.38` 확인. 실제 설치 ZIP 바이트/실행 코드 연계는 별도 검증 필요 |
| Skill-Updater | 모바일 Agent 당시 설치본 `0.5.43`; 목표 `0.5.44` 미적용. 이번 장애를 이유로 업데이트 강제하지 않음 |
| RACH Catalog | `source=active`, profile `nr-l1tx-init-rach-analysis-linux` 보고. **ACTIVE는 Worker 실행 증명이 아님** |
| RACH Job ID | `JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01` |
| Queue | `state=DONE`, `receipt_state=SUCCESS`, `attempts=1`, `pending_count=0` 보고. 어떤 단계의 성공인지 원본 계약 미검증 |
| Worker/Run | `enqueued_at=null`, `worker_started_at=null`, `run_id=null`: **실제 분석 실행 UNKNOWN** |
| 결과 조회 | `job_result_read: RESULT_UNSUPPORTED`. `bridge_result_allowlist` 9건에 해당 ID 미포함 보고. API 경계/정의 누락 원인 미확정 |
| Catalog/Registry/Bootstrap | 각각 9/6/5건, RACH는 Catalog에만 관측. 목록이 동등 집합이어야 하는지 **설계 계약 확인 필요** |
| 분석 산출물 | `CODE_FACTS`, MSC, `artifact_path` 실제 존재 미검증; `semantic_state=UNKNOWN` |
| MCP 수정·배포 | 모바일 Agent 읽기 전용 재조회에서 MCP 소스/설정 실제 변경·배포 영수증 없음. `NOT_APPLIED`로 보고 |
| 독립 리뷰 / 호스트 회귀시험 | `NOT_RUN` / `NOT_RUN` (이번 원격 진단 기준) |
| 전체 복구 | **NOT_VERIFIED / NOT_APPLIED**. 기존 `DONE/SUCCESS`를 NR 분석 완료로 승격하지 않음 |

## 최신 모바일 Agent 실행 요청의 실제 결과

1. 공개 r0003 인계 본문 **10,233자 읽기 PASS**. 문서 확보는 복구 실행 성공이 아님.
2. `job_capabilities_read.runner_boundary`는 `remote_enqueue`, `remote_retry`, `remote_cancel`, `apply_patch` 모두 `NOT_IMPLEMENTED`로 보고. **모바일 Agent에 노출된 MCP는 READ/PLAN 기능만 확인됨.**
3. 모바일 Agent 실행 컨테이너와 Linux MCP 운영 호스트는 서로 다른 machine. Agent 컨테이너에서는 `[MCP_ROOT]`, `[JOB_LIST_ROOT]` 실제 운영 파일을 읽거나 수정·재시작할 수 없음.
4. Agent 측 `github_exec`가 HTTP 401을 반환했고 공개 GitHub API 경로로 r0003을 읽음. **이 401은 Linux Skill-Updater의 PAT 복구 실패를 의미하지 않음.**
5. 실제 수정 파일 **0건**, 새 Run ID **없음**, Job 재실행 **없음**, 새 산출물 검증 **없음**. `HOST_VERIFIED=FAIL`, `OPERATIONAL_APPLY=NOT_APPLIED`, `JOB_EXECUTION=UNKNOWN`, `ANALYSIS_RESULT=UNKNOWN`, `INDEPENDENT_REVIEW=NOT_RUN`으로 보고.
6. 모바일 Agent가 표시한 `DUPLICATE_JOB_EXECUTIONS=0`은 **이번 요청에서 중복 실행하지 않았다는 뜻으로만 사용**. 호스트 전체 이력의 중복 부재가 검증된 것은 아님.

## 근본 원인 후보와 검증할 계약

- **실제 Worker 도달 미확인**: `DONE/SUCCESS` 기록을 만드는 원본 함수를 확인해 요청/등록 성공과 Worker 성공을 분리.
- **등록/활성 계약 미확인**: `Catalog(9) ↔ Registry(6) ↔ Bootstrap(5)`의 목적·집합 관계, 단일 RACH ID의 실행 경로 확인. 수를 무조건 맞추거나 이미 소비된 Job을 재큐잉하지 않음.
- **결과 조회 계약 미확인**: `RESULT_UNSUPPORTED`가 allowlist 누락, 지원하지 않는 결과 타입 또는 단순 대체 경로인지 판단. 결과 파일이 없다면 allowlist만 고쳐도 분석 성공은 아님.
- **산출물 미확인**: 운영 호스트에서 기존 RACH Job의 원래 출력 위치에 `CODE_FACTS`·MSC·영수증 존재 여부를 먼저 확인.
- **배포 추적**: 이전 `DEPLOYMENT_NOT_TRACKED`는 MCP 배포 추적과 Job 결과 실패의 관계부터 확인; 근거 없이 파일을 조작하거나 PASS 처리 금지.

## 작업 경로 / 승인 경계 / 다음 한 행동

- **이번 한계는 Job-list 자체의 실행 불가능 확정이 아님**: 모바일 Agent에서 원격 apply/launch 도구가 없는 것이 확인되었고, Linux 호스트 내부의 기존 CLI/Runner 경로 가능성은 **미검증**.
- Job-list 형태로 별도 복구 Job을 설계·배송하는 방안은 가능성 검토 대상이나, 현재 장애 경로에 자기복구를 의존하는 위험이 있음. 이 시점에서 **새 Job/READY/ZIP/운영 변경을 생성하지 않음**.
- 기존 r0003 인계는 [PUBLIC handoff](https://github.com/wonhwipark/L1Work/blob/main/handoffs/JOB_LIST_V0438_LINUX_MCP_ROOTCAUSE_RECOVERY_PROMPT_r0003_20261117_KST.md). 사용자 요청에 따라 Linux 운영 호스트에 접근하는 **업무 LLM 세션에서 직접 실행**하는 방향이 우선.
- **NEXT_ONE_ACTION:** 업무 LLM이 Linux 운영 호스트의 **기존 RACH Job 결과 디렉터리 및 실제 Runner/Worker 영수증을 읽어**, `CODE_FACTS/MSC`의 실재와 `DONE/SUCCESS`가 생성된 정확한 단계를 **한 번의 점검으로** 판정. 그 결과에 따라 확인된 최소 결함만 허용 범위에서 보완·시험.
- 운영 MCP/DB/서비스/설정 변경, 소비된 Job 재실행·재큐잉, 신규 유료 모델 호출은 **기존 유효 승인·사전 위임 확인 전 수행 금지**. 미확인은 `BLOCKED`/`NOT_RUN`으로 유지.
- 민감 코드·운영 로그 원문·토큰·키·상세 MSC를 PRIVATE/PUBLIC에 게시하지 않으며, 실행 근거 원본은 허용된 업무 로컬 저장소에 보존.

## 관련 정본

- [Job-list 진단 CURRENT](CURRENT.md)
- [NR L1 Tx 코드 분석 CURRENT](../NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md)
- [r0003 업무 LLM 직접 복구 인계 (PUBLIC)](https://github.com/wonhwipark/L1Work/blob/main/handoffs/JOB_LIST_V0438_LINUX_MCP_ROOTCAUSE_RECOVERY_PROMPT_r0003_20261117_KST.md)
- [최신 비민감 모바일 Agent 후속 인계 (PUBLIC)](https://github.com/wonhwipark/L1Work/blob/main/handoffs/JOBLIST_V0438_MCP_RECOVERY_STATUS_HANDOFF_r0001_20261117_KST.md)
- 과거 v0.4.36 진단 원문은 `MCP_JOBLIST_RECOVERY_HISTORY_20261113.md` 보존 (이번 관측으로 과거 이력 덮어쓰기 금지).
