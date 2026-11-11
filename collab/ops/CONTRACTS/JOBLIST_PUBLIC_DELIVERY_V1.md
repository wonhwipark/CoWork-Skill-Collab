# Job-list / Skill-Updater PUBLIC 전달 운영 계약 — V1

- 제정: 2026-11-12 KST
- 적용: 사외 GPT → GitHub ZIP 게시 → 사내 Linux Skill-Updater → Job-list One-shot / 그 외 스킬 ZIP 배포
- 상태: 현재 사용자 지시로 **전달 저장소 역할 및 실행 상태 분리 규칙 적용**. 이 문서가 기존 배포·설치·실행을 승인하거나 자동 시작하지 않음.
- 상위 안전 규칙: `collab/START_HERE.md`, `collab/ops/CONTRACTS/PUBLIC_RELEASE_GATE.md`, 최신 해당 작업 `CURRENT.md`. 충돌 시 더 엄격한 무단 배포 방지 규칙 적용.

## 1. 저장소 역할 — 앞으로 혼동 금지

| 목적 | 유일한 기준 경로 | 할 수 있는 일 | 하면 안 되는 일 |
|---|---|---|---|
| **사내 Skill-Updater 전달 ZIP** | GitHub **PUBLIC** `wonhwipark/L1Work`, branch `main`, **repository root**, 신규 고유 버전 파일 `<skill>_v<major>_<minor>_<patch>_<MMDD>.zip` | 검증 및 승인된 **최종** 스킬 ZIP 게시, 같은 경로 remote readback | PRIVATE ZIP 게시를 '전달 완료'라고 보고, 비배포 후보를 최종본처럼 올리기, 구 ZIP 덮어쓰기 |
| 개발·리뷰·판정·영수증·후속 메모 | GitHub **PRIVATE** `wonhwipark/CoWork-Skill-Collab` | 비민감 설계, 요청서, 변경분, 시험 요약, 상태/영수증, 검증 보조 스크립트 | Job-list 운영 **전달 위치로 대체**, 민감 사내 코드/로그/MSC 저장 |
| 미검증 후보 ZIP·임시 빌드 | 격리 개발 공간 또는 기한 있는 GitHub Actions artifact | 패키징·시험·검토·재생성 | PRIVATE 저장소에 ZIP만 올리고 사용자에게 배포 완료라고 설명 |

**자동 전달용 ZIP은 PRIVATE가 아니라 PUBLIC 루트에만.** 작업자가 PUBLIC 경로를 명시했다면 우선 해당 유효 배포 경로를 사용한다. 접근 제한·검증 미완료로 PUBLIC 게시가 불가능할 때 PRIVATE에 대신 게시하지 말고 **PUBLIC_RELEASE=BLOCKED/NOT_POSTED** 및 원인을 보고한다. PRIVATE 이력 관리 자체는 배송을 의미하지 않는다.

## 2. Job-list 버전 수명주기 (서로 다른 상태)

1. **REQUEST_DESIGNED**: 사용자 조사 범위/대상 환경·스킬/완료 기준 정의.
2. **CANDIDATE_BUILT / SELF_TESTED**: 이전 ZIP 원본 그대로 보존, 신규 버전으로 제작, CRC·SHA·경로이탈·필수파일·민감정보·회귀시험 검증. 이 단계는 배송도 실행도 아니다.
3. **INDEPENDENT_REVIEW / HOST_G0 / RELEASE_APPROVAL**: 독립 리뷰·사내 설치/호출 계약·보안/실행/이전·롤백 요건은 개별 판정. 미검증이면 `development_not_for_deployment`; PUBLIC 게시 보류.
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
- 호스트 계약이 아직 미검증인 후보를 단지 사용자가 'PUBLIC에 올려줘'라고 요청했다고 최종 배포 ZIP으로 승격하지 않는다. **PUBLIC 경로 사용 승인과 기술적 배포 가능 판정은 다름.**
- 작업 목적이 '퇴근 후 사내 LLM 무인 실행'이면 **PUBLIC 신규 ZIP + 활성 One-shot 실제 실행 게이트**가 준비되어야 요청 완료. PRIVATE 설계/후보 게시나 PUBLIC 비활성 후보 게시만으로 완료라고 하지 않는다.

## 4. 배포 완료 보고 형식 (필수)

`현재 상태 → 변경 내용 → 실제 시험 결과 → 미검증·차단/승인 필요 → PUBLIC ZIP 정확 경로·SHA-256·크기·커밋·원격 재조회 → SKILL_UPDATER 설치/Job 활성화/실제 실행 상태 → 다음 한 동작`.

각 상태는 별도로 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED` 기록. PRIVATE 개발 산출물은 필요할 때 '참고자료'로만 명명. ZIP은 별도 명시적 사용자 승인 없는 자동 PUBLIC 게시/사내 운영 설치/실행을 수행하지 않는다.

## 5. 본 작업 정정 기록 (JOBLIST-NRTX-20261112-001)

- 2026-11-12 사용자가 PUBLIC `wonhwipark/L1Work` root가 **유일한 Job-list 전달 목적지**임을 재확인.
- 기존 개발자가 `job-list v0.4.35` 비활성 후보를 PRIVATE에 게시하고 전달과 혼동한 것은 작업 경로 선정 오류. PRIVATE에는 결과·검토 기록만 보존하고, 이후에는 후보 ZIP을 PRIVATE 배송본으로 올리지 않는다.
- v0.4.35 상태: 후보 ZIP 제작, 33 PASS 자기 시험, **활성 Job 0 / 사내 L1 Knowledge Updater 실제 호출·독립 리뷰·호스트 G0 미검증**. PUBLIC 자동설치·분석은 `NOT_RUN`. 올바른 목적지에 게시할 최종 활성 배포본을 추가 검증·승인 후 제공해야 함.
- 본 정책 변경은 Dropbox LIVE watcher, 운영 DB/WAL, 예약 작업, Bridge/Telegram, 사내 설치본, 기존 PUBLIC ZIP을 변경하지 않음. CoWork `MIGRATION_NOT_CUTOVER / DROPBOX_LIVE` 유지.
