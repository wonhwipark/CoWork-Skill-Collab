# Job-list / Skill-Updater PUBLIC 전달 운영 계약 — V1

- 제정: 2026-11-12 KST
- 적용: 사외 GPT → GitHub ZIP 게시 → 사내 Linux Skill-Updater → Job-list One-shot / 그 외 스킬 ZIP 배포
- 상태: 현재 사용자 지시로 **전달 저장소 역할 및 실행 상태 분리 규칙 적용**. 이 문서가 기존 배포·설치·실행을 승인하거나 자동 시작하지 않음.
- 상위 안전 규칙: `collab/START_HERE.md`, `collab/ops/CONTRACTS/PUBLIC_RELEASE_GATE.md`, 최신 해당 작업 `CURRENT.md`. 충돌 시 더 엄격한 무단 배포 방지 규칙 적용.

## 2026-11-17 사용자 기본 지시 — 검증된 최종 스킬 ZIP의 L1Work 자동 게시

- **최신 사용자 지시:** "올려줘. 앞으로 자동으로 올려." 이에 따라 GPT가 스킬 개발·수정 작업을 맡아 **최종 릴리스 게이트를 모두 충족한 경우**, 같은 작업 흐름에서 사용자에게 매번 별도의 "L1Work에 올릴까요?" 질문을 하지 않고 `wonhwipark/L1Work` / `main` / **루트**에 신규 고유 버전 ZIP을 게시하고 원격 bytes/SHA-256을 대조한다.
- **적용 범위:** 사용자가 GPT에 맡긴 관리 스킬의 허용된 비민감 최종 공개 ZIP. 사용자의 최신 실행 지시와 승인 범위 및 PUBLIC 허용 여부를 확인한다. 기존 ZIP 덮어쓰기·인증정보/업무 제한 원문·미검증 후보 업로드 금지.
- **필수 선행조건 그대로 유지:** 신뢰 원본 pin/ZIP CRC/경로·심링크·민감정보·manifest/회귀시험, 요구되는 독립 코드 리뷰와 실환경 권한/호환 게이트, release channel의 정식 릴리스 일치, readback. `development_not_for_deployment`, `review-candidate`, gate FAIL/NOT_RUN은 PUBLIC에 게시하지 않고 `BLOCKED_NOT_POSTED`를 정확히 기록. 이 지시는 QA/보호 정책 면제 지시가 아니다.
- **자동의 의미:** GPT가 **각 스킬 작업을 수행할 때의 기본 게시 후속 동작**이며, 현재 무인 GitHub Action/신규 PAT·운영 watcher·스케줄러가 설치·활성화됐다는 뜻이 아니다. 별도 운영 자동 게시 서비스·키 생성/설치/지속 감시/운영 권한 변경은 해당 계약에 따른 별도 실제 활성화와 검증 필요.
- 게시 후 `PUBLIC_POSTED`, `SKILL_UPDATER_INSTALLED`, `JOB_EXECUTED`, `GROUP_KNOWLEDGE_WRITE`는 각각 독립 판정한다. 게시 실패로 이미 실행된 빌드·유료 모델·운영 Job을 임의 재실행하지 않는다.
- 2026-11-17 `L1-WORKSPACE-RAG-20261111-001` 3종 후보는 `development_not_for_deployment`; G0/하드 가드/코드 리뷰 미충족으로 현재 `PUBLIC_RELEASE=BLOCKED_NOT_POSTED`를 유지한다. 사용자의 기본 게시 지시 자체는 유효하다.

---

## 1. 저장소 역할 — 앞으로 혼동 금지

| 목적 | 유일한 기준 경로 | 할 수 있는 일 | 하면 안 되는 일 |
|---|---|---|---|
| **사내 Skill-Updater 전달 ZIP** | GitHub **PUBLIC** `wonhwipark/L1Work`, branch `main`, **repository root**, 신규 고유 버전 파일 `<skill>_v<major>_<minor>_<patch>_<MMDD>.zip` | 검증 및 승인된 **최종** 스킬 ZIP 게시, 같은 경로 remote readback | PRIVATE ZIP 게시를 '전달 완료'라고 보고, 비배포 후보를 최종본처럼 올리기, 구 ZIP 덮어쓰기 |
| 개발·리뷰·판정·영수증·후속 메모 | GitHub **PRIVATE** `wonhwipark/CoWork-Skill-Collab` | 비민감 설계, 요청서, 변경분, 시험 요약, 상태/영수증, 검증 보조 스크립트 | Job-list 운영 **전달 위치로 대체**, 민감 사내 코드/로그/MSC 저장 |
| 미검증 후보 ZIP·임시 빌드 | 격리 개발 공간 또는 기한 있는 GitHub Actions artifact | 패키징·시험·검토·재생성 | PRIVATE 저장소에 ZIP만 올리고 사용자에게 배포 완료라고 설명 |

**자동 전달용 ZIP은 PRIVATE가 아니라 PUBLIC 루트에만.** 작업자가 PUBLIC 경로를 명시했다면 우선 해당 유효 배포 경로를 사용한다. 접근 제한·검증 미완료로 PUBLIC 게시가 불가능할 때 PRIVATE에 대신 게시하지 말고 **PUBLIC_RELEASE=BLOCKED/NOT_POSTED** 및 원인을 보고한다. PRIVATE 이력 관리 자체는 배송을 의미하지 않는다.

## 실행용 프롬프트 용어 기본 규칙

- [환경 중립 표현 계약](EXECUTION_PROMPT_TERMINOLOGY_V1.md)을 Job-list 요청·Job Worker용 프롬프트·Agent MCP 조회 프롬프트에 적용한다. 망 위치를 드러내는 구분 표현을 기본적으로 배제하고, 역할/호스트/승인된 스킬 경로를 기준으로 작성한다. 반복 요청 없이 신규 산출물에 자동 적용.

## 2. Job-list 버전 수명주기 (서로 다른 상태)

1. **REQUEST_DESIGNED**: 사용자 조사 범위/대상 환경·스킬/완료 기준 정의.
2. **CANDIDATE_BUILT / SELF_TESTED**: 이전 ZIP 원본 그대로 보존, 신규 버전으로 제작, CRC·SHA·경로이탈·필수파일·민감정보·회귀시험 검증. 이 단계는 배송도 실행도 아니다.
3. **RELEASE_GATE / REVIEW / HOST_G0**: 일반 정식 배포는 원래의 필수 게이트로 판정하되, **사용자가 명시 승인한 읽기 전용 디버깅 ZIP은 8절의 사전 안전검증을 먼저 수행하고 Claude 독립 리뷰·Linux G0/종단 검증은 PUBLIC 배송 후에 수행**한다. 사후 검증 미실행을 PASS로 선언하지 않는다.
4. **PUBLIC_RELEASE_POSTED**: 사용자 승인과 배포 게이트를 통과한 최종 ZIP만 `L1Work/main` 루트 신규 파일명으로 게시. 게시된 bytes/SHA-256·size/commit 및 remote 재다운로드 검증.
5. **SKILL_UPDATER_INSTALLED**: 사내 Skill-Updater가 root-zips 최신 버전을 발견/다운로드/설치한 실제 호스트 영수증이 있어야 PASS. PUBLIC 게시만으로 설치 완료라고 주장 금지.
6. **JOB_ACTIVATED**: 기존 OS 예약 Skill-Updater의 정해진 활성화 hook과 호스트별 승인·중복·만료·Profile·권한 게이트 통과. 일반 업데이트만으로 실행 트리거 생성 금지.
7. **JOB_EXECUTED / RECEIPT_RECONCILED**: 해당 one-shot의 Job ID와 실제 Runner/Worker Run ID·Result·Receipt·Run Catalog readback 및 대상 스킬/산출물 검증. 비어 있는 `jobs: []`는 **활성 작업 0건**이므로 Job 전달 성공으로 보고할 수 없다.
8. **KNOWLEDGE_PUBLISHED**: 별도 소유자 승인 및 source/Evidence 검증·writer/remote readback 확인한 뒤에만 완료. 분석 산출물 생성과 그룹 지식 게시를 구분.

Job-list **한 버전에 활성 One-shot Job 최대 1건**. 이미 소비된 Job 재큐잉 금지, 과거 receipts/history·persistent `data/**`, `output/**` 보존, 동일 이름 ZIP 덮어쓰기 금지. `staged` 목록과 활성 `requests/one-shot-jobs.json` 혼동 금지. 실행 차단은 우회하거나 임의 Job ID/승인/성공 영수증으로 대체 금지.

## 3. 사내 Knowledge Updater 연계 작업

- 사내 Linux 소스·도구의 실제 action/entrypoint/owner 승인 사실은 **사내 호스트**에서 확인. GitHub PUBLIC/PRIVATE의 설계·텍스트가 설치된 `l1-knowledge-updater` 실행 계약의 근거가 아님.
- `l1-knowledge-updater` 조율 하에 `code-analyzer`는 CODE FACTS, `doc-converter`는 검증된 AS-IS 시나리오 MSC 표현을 담당. 임의 shell/명령·임의 도구 action 생성 금지.
- 원본 코드·고객정보·사내 로그·상세 MSC의 GitHub PUBLIC/PRIVATE 외부 반출 금지. 사내 원본 읽기·분석 결과 생성과 지식 정본 쓰기를 분리.
- 일반 후보는 호스트 계약 미검증 시 정식 릴리스로 승격하지 않는다. **단, 사용자가 한정 승인한 읽기 전용 디버깅 Job-list는 8절에 따라 사전 정적 안전검사를 충족하면 배송 후 호스트 검증을 수행한다.** PUBLIC 경로 지시만으로 무검증 패키지를 올리는 것은 허용하지 않는다.
- 작업 목적이 '퇴근 후 사내 LLM 무인 실행'이면 **PUBLIC 신규 ZIP + 활성 One-shot 실제 실행 게이트**가 준비되어야 요청 완료. PRIVATE 설계/후보 게시나 PUBLIC 비활성 후보 게시만으로 완료라고 하지 않는다.

## 4. 배포 완료 보고 형식 (필수)

`현재 상태 → 변경 내용 → 실제 시험 결과 → 미검증·차단/승인 필요 → PUBLIC ZIP 정확 경로·SHA-256·크기·커밋·원격 재조회 → SKILL_UPDATER 설치/Job 활성화/실제 실행 상태 → 다음 한 동작`.

각 상태는 별도로 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED` 기록. PRIVATE 개발 산출물은 필요할 때 '참고자료'로만 명명. ZIP은 별도 명시적 사용자 승인 없는 자동 PUBLIC 게시/사내 운영 설치/실행을 수행하지 않는다.

## 5. 본 작업 정정 기록 (JOBLIST-NRTX-20261112-001)

- 2026-11-12 사용자가 PUBLIC `wonhwipark/L1Work` root가 **유일한 Job-list 전달 목적지**임을 재확인.
- 기존 개발자가 `job-list v0.4.35` 비활성 후보를 PRIVATE에 게시하고 전달과 혼동한 것은 작업 경로 선정 오류. PRIVATE에는 결과·검토 기록만 보존하고, 이후에는 후보 ZIP을 PRIVATE 배송본으로 올리지 않는다.
- v0.4.35 상태: 후보 ZIP 제작, 33 PASS 자기 시험, **활성 Job 0 / 사내 L1 Knowledge Updater 실제 호출·독립 리뷰·호스트 G0 미검증**. PUBLIC 자동설치·분석은 `NOT_RUN`. 올바른 목적지에 게시할 최종 활성 배포본을 추가 검증·승인 후 제공해야 함.
- 본 정책 변경은 Dropbox LIVE watcher, 운영 DB/WAL, 예약 작업, Bridge/Telegram, 사내 설치본, 기존 PUBLIC ZIP을 변경하지 않음. CoWork `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE` 유지.

## 6. 사용자 승인된 사내 G0 선행 조사 Job — 제한적 PUBLIC 전달 모드 (2026-11-12)

- 적용 목적: **실제 `l1-knowledge-updater` 설치 action/호출 계약 및 독립 리뷰는 사내에서만 확인 가능**하므로, 이를 확인하기 위한 무인 **READ_ONLY_BOOTSTRAP_ONE_SHOT**을 사용자 명시 승인 후 PUBLIC `L1Work/main` 루트에 먼저 배송할 수 있다. 일반 개발 후보 ZIP에 대한 무조건 예외가 아님.
- 사전 충족: 고정된 한 개의 활성 Linux Job ID, 비밀/사내 소스 미포함, 승인된 공개 패키지 메타데이터, 신뢰된 기존 ZIP byte pin, CRC·SHA·경로/심링크 검사, 기존 Job 보존, Profile 스키마 검증 및 실패-차단 테스트, 원격 ZIP 재다운로드 해시 검증.
- 허용: 사내 **read-only 탐색/분석/등록된 비파괴 SkillSilent action**, 코드 facts/AS-IS MSC 생성, 기존 그룹 Knowledge의 읽기 전용 비교, **사내 새 출력 파일·영수증** 작성, 설치 계약/실행·리뷰 가능성 사실 조사.
- 금지: 기존 코드·Knowledge 정본·운영 설정·Kernel Work/Evidence·DB 수정, source reset/stash/commit/push, CLI 임의 action/권한 우회, 자료 사외 반출, 독립 리뷰 완료/그룹 게시 PASS 사전 선언.
- 런타임 G0 미통과·허용 action 미확인 시 **BLOCKED/ANALYSIS_PARTIAL** 증거를 남기고 STOP; 스킬 업데이트·인증 발급·사내 데이터 변경으로 우회하지 않는다. 무인 실행이므로 사용자 질의로 멈추지 않고 허용 범위 내 결과를 최대한 취합.
- 배포 성공과 사내 `SKILL_UPDATER_INSTALLED`·`JOB_ACTIVATED`·`KNOWLEDGE_UPDATER_CALL`·`MSC_READY`·`INDEPENDENT_REVIEW`는 서로 독립. 미수신 호스트 결과를 `NOT_VERIFIED` 또는 `NOT_RUN`으로 유지.
- **특수 사례:** 사용자는 `JOBLIST-NRTX-20261112-001`의 조사/호출계약 검증을 PUBLIC 배송 후 사내에서 실행하라고 승인. `job-list_v0_4_36_1112.zip`을 활성 Job 1건의 read-only 조사 전달본으로 PUBLIC 게시. 정식 지식 정본 쓰기/무인 수정/독립 리뷰 PASS 승인은 **아님**.

## 7. Issue Analyzer 1차 배포 경로 확정 (2026-11-14)

- 사용자 명시 지시: `issue-analyzer`의 **1차 ZIP 배포도** GitHub PUBLIC `wonhwipark/L1Work` / `main` / **루트**를 사용한다. PRIVATE `wonhwipark/CoWork-Skill-Collab`은 비민감 협업 문서·상태·독립 리뷰 기록용이지 ZIP 전달 경로가 아니다.
- 이전에 '우선 PRIVATE 후보 ZIP에 게시'하던 단계는 이 작업의 배포 절차에서 제거한다. 개발 작업공간의 임시 후보 ZIP은 배포가 아니며, 사용자에게 PRIVATE 다운로드로 공개 배송을 대체했다고 보고하지 않는다.
- 첫 배포 위치 확정은 **독립 리뷰 PASS, 설치/실행 PASS, 자동 활성화 승인**을 뜻하지 않는다. 단계별 진위·금지된 정보 반출 검사·파일 바이트와 SHA-256 원격 재조회 등 기존 안전 게이트는 유지한다. 미충족이면 정확히 `PUBLIC_RELEASE=BLOCKED/NOT_POSTED`로 기록하며 임의 우회하지 않는다.
- 이 결정의 근거·현황: [issue-analyzer Work CURRENT](../../projects/ISSUE-ANALYZER-20261114-001/CURRENT.md). 최초 후보 목표 파일 `issue-analyzer_v0_11_50_1114.zip`. GitHub 실제 게시/Skill-Updater 설치는 별도 확인 전까지 NOT_POSTED/NOT_RUN.


## 8. 사용자 지정 Job-list READ-ONLY DEBUG 릴리스: 사후 독립 리뷰 / 호스트 검증 — 2026-11-15

**본 절은 2026-11-15 사용자가 승인한 `job-list_v0_4_38_1115.zip` NR L1 Tx Init RACH 분석/디버깅 목적에 직접 적용되는 한정된 예외다.** 이후 다른 공개 스킬 ZIP이나 운영 상태 변경에 자동 확대하지 않는다. 공통 배포 게이트와 충돌하는 경우 **이 요청의 읽기 전용 디버깅 전후 검증 순서에 대해서만 본 절을 우선 적용**한다.

1. **배포 전 필수:** 사용자 PUBLIC 배송 승인, 신뢰된 원본 ZIP의 byte/SHA pin, 전체 ZIP CRC 및 경로/중복/심링크/민감정보 검사, 실제 버전·메타데이터·manifest 일치, 회귀시험 PASS, 신규 유일 Job ID 1건, 기존 소비 Job·DB·Registry·Queue·Receipt 보존, source/Knowledge 정본 쓰기 금지, 진입점·권한·실패-차단 정적 검증. 하나라도 FAIL이면 PUBLIC 배포 금지. `CANDIDATE_TEST_PASS`와 `PUBLIC_RELEASE`는 구분한다.
2. **Claude Code 독립 리뷰는 배포 후 점검:** 본 읽기 전용 디버깅 릴리스는 `INDEPENDENT_REVIEW=POST_RELEASE_PENDING`으로 PUBLIC 배송 가능. 단, 미실행 리뷰를 PASS로 기록하지 않으며, 유료 리뷰 REQUEST/READY나 모델 호출은 기존 승인·서명·비용 게이트에 따라 별도로만 실행한다. 사후 리뷰에 결함이 발견되면 GPT가 지적별 판단 후 **새로운 버전명·새 ZIP**을 발행하고, 같은 이름/바이트를 덮어쓰거나 소비된 One-shot Job을 재실행하지 않는다.
3. **실 Linux 호스트 G0, 기존 장애 복구, OpenCode CLI 및 MCP 결과 조회는 배포 후 검증:** 이 항목들이 미확인이라는 이유만으로 본 승인된 read-only debug ZIP의 PUBLIC 배송을 보류하지 않는다. 호스트 런타임 검사 미통과 시 `HOST_G0=BLOCKED`, `ANALYSIS=NOT_RUN/PARTIAL`로 영수증을 남기고 fail closed. 호스트 설치/활성화/실제 분석/결과 readback은 모두 배송과 다른 상태.
4. **배송 순서:** 승인된 ZIP을 `wonhwipark/L1Work/main` **루트**에 신규 파일로 게시 → 원격 다운로드 실제 ZIP byte SHA-256/크기/commit 검증 → 배송만 `PUBLIC_POSTED` 보고. 호스트 Skill-Updater 자동감지/설치/Job 분석 성공으로 소급 주장하지 않는다.
5. **실행 보호:** NR Tx 코드 루트는 Linux에서 검증된 `/home/whpark/Project/smp1900`이나 공개 ZIP·프롬프트에는 개인 절대 경로/비밀을 포함하지 않는다. 기존 등록 도구의 읽기 전용 동작만 허용하고, Git/업무 코드/지식 정본/운영 데이터·예약 작업 변경·외부 반출 및 추가 유료 호출 금지.
6. **재발방지:** 사용자가 Job-list 배포·분석 시도를 명시 승인했고 사전 안전 검사가 PASS라면, 리뷰/호스트 E2E가 사후라는 사실을 배포 불가 원인으로 삼지 않는다. 권한·무결성·보안·회귀시험 문제로 실제 게시가 실패할 때만 정확한 `BLOCKED` 사유를 즉시 보고한다. `PUBLIC_POSTED`와 `JOB_EXECUTED`는 반드시 별도 열로 관리한다.

**이 절은 Zip PUBLIC 게시 승인이지 Windows watcher LIVE, Linux 운영 설정/DB 수동 변경, 이미 소비된 Job 재활성화, 유료 리뷰 자동 호출 승인이 아니다.**
