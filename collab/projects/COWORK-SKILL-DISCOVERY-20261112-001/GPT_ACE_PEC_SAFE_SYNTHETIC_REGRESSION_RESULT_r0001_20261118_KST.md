# ACE·PEC-HOP·SAFE 비민감 합성 격리 회귀시험 결과 r0001

- 일자: 2026-11-18 KST
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main`
- Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 사용자 요청: “진행해줘” — R1 종료 후 설계 r0002의 **ACE-02 / PEC-01·03 / SAFE-01** 비민감 합성·읽기 전용 시험
- 설계 고정: [r0002](ACE_PEC_HOP_ACON_INTEGRATED_SKILL_DESIGN_r0002_20261118_KST.md), **24,705 UTF-8 B**, SHA-256 `8959c5785da37d0a7f48687fbbe17576c4f0f517be93ffcd9befc029a1c6def1`
- 리뷰 고정 r0001: SHA-256 `aa69b2e6bba529d09609d8c6c7b1ead0d4b3d744208361ce447c87ad57b41303` — **불변**.
- 시험 코드: [test_ace_pec_safe_synthetic_r0001.js](test_ace_pec_safe_synthetic_r0001.js), commit `d6d0348b09866147a80815a6dce4dc51640b6eef`, **8,815 B**, SHA-256 `407e8f2fcccd341444c912fde09f79d97f7dc650b2f03d9e98f52db51a87a330`, Git blob `e582b3beb4d4f5bbea68e23c60a1f120cca787d6`; 게시 뒤 원격 본문 SHA 계산 확인.

## 1. 범위·실제 실행 방법

- **실제 실행:** JavaScript V8 코드 실행 도구에서 **순수 함수 `runSuite(r0002원문,r0001원문)`를 직접 실행**. 입력은 GitHub PRIVATE `main`에서 실제로 재조회한 r0001/r0002 Markdown 원문. 별도 GitHub 네트워크/호스트/LLM 요청을 호출하는 시험이 아니며, 모든 합성 데이터·결정 기록·Evidence raw bytes는 메모리 내에서만 생성·변조·대조.
- 검증 oracle(시험 전용 함수)은 설계 §3.1.1의 최신 결정 선택, §4.1의 raw byte 발췌 무결성, SAFE-01/03의 부수효과 0·중복 방지 조건을 모사. **실제 l1-fix-workflow/Kernel/code-analyzer/Updater 소스의 구현 기능을 호출한 시험은 아님.** 기존 스킬에 새로운 API/field/schema가 존재한다는 결론을 내리지 않는다.
- SHA256 표준 `abc` 테스트 벡터 검증 후 실제 Markdown UTF-8 raw bytes의 digest를 계산하여 r0001/r0002 고정 입력을 확인. `PASS`는 각 합성 시나리오에서 **예상 PASS/HOLD/FAIL 응답을 정확히 반환**했다는 뜻. 고의 오염 사례에서 FAIL/HOLD를 반환하는 것이 정상.
- **재현 가능 코드 제공:** PRIVATE repo checkout에서 `node collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/test_ace_pec_safe_synthetic_r0001.js` 명령. 로컬 Node CLI 및 Windows/Linux에서 재실행은 이번 작업에서 **NOT_RUN**. Node 실행은 r0001/r0002 로컬 원문만 읽음; GitHub push/Watcher/모델 호출 코드 없음.
- 기존 `collab/ops/tests/test_source_pin.py` 등 정책/핀 회귀 코드는 **변경·중복 구현하지 않음**. CI workflow/triggers·watcher·LIVE/DB·업무 Knowledge writer 변경 없음.

## 2. 결과 요약

| 구분 | 개별 시나리오 | 결과 | 포함된 반례 |
|---|---:|---|---|
| STATIC 원문·수용 기준 | 5 | **5 PASS** | SHA256 표준 벡터, r0001 불변, r0002 정확한 digest, 기존 수용시험 12 ID 1회씩, 종료 리뷰·유료 호출 금지 상태 |
| ACE-02 결정 이력 | 6 | **6 PASS** | append 최신 선택, CURRENT mtime 무시, 타 scope 불개입, 중복 순서 HOLD, 미검증 승인 HOLD, 명시 철회 |
| PEC-01/03 Evidence | 9 | **9 PASS** | 원본 raw byte 정확 복사, 1-byte 변조 FAIL, source revision 차이 HOLD, 식별자 보존, offset 누락/경계 초과, 원본 변조, 권한 없음, 재인코딩 차이 |
| SAFE-01/03 실행경계 | 6 | **6 PASS** | 부수효과 0, 서브에이전트·유료 모델·READY 쓰기·새 Job 시뮬레이션 차단, 완료 리뷰 재큐잉 HOLD |
| **합계** | **26** | **26 PASS / 0 FAIL** | 합성 계약 oracle 한정 |

- 시험 프로세스 내부 신규 모델/외부 Agent/READY/Job/watcher 실행 호출 **0**. 본 결과 문서·시험 파일의 PRIVATE GitHub 게시 자체는 범위 내 승인된 **문서·개발 시험 산출물 게시**로, watcher의 RESERVED/READY 트리거가 아님.
- 테스트가 반환한 `HOLD` / `FAIL`은 고의 오염 또는 미확인 입력을 **성공 처리하지 않았다는 기대 결과**. 생산 환경에서 이 판별 로직이 설치·동작한다는 의미는 아님.

## 3. 실제 관측 vs 미검증 구분

| 검증 층위 | 판정 |
|---|---|
| r0002 계약·r0001 원문 해시 / 12개 기존 수용 시험 ID 정합성 | **PASS**, 실제 GitHub 원문을 입력으로 실행 |
| 순수 함수 ACE/PEC/SAFE 비민감 합성 반례 26건 | **PASS (ISOLATED CONTRACT ORACLE)** |
| 실제 업무/CoWork 기존 스킬 reader·writer·Evidence 기능 연계 | **NOT_RUN** — 로컬/실제 설치 API 호출 없음 |
| Windows/Linux Node CLI에서 동일 파일 단독 실행 | **NOT_RUN** — 원격 재현 명령만 제공 |
| Windows watcher/승인 signer/READY 실제 차단 경로 | **NOT_RUN** — 이번 테스트는 SAFE 계약 함수 모사에 한정 |
| ACON-01 baseline/compressed 각 ≥3회 모델 반복 | **NOT_RUN** — 실제 호출 승인·예산/환경 보류 |
| 업무 GPT Updater G0/Knowledge writer, L1 실제 코드·MSC | **NOT_RUN / NOT_VERIFIED** |
| 신규 독립 유료 리뷰/모델 호출·운영 변경·PUBLIC ZIP 배포 | **0** |

**과대 해석 방지:** 이 결과는 사전 설계에 정의한 합성 검증 oracle이 요구된 실패 유형을 구분하는지 보여준다. 실제 설치된 Workflow·Kernel·analyzer·Updater가 같은 상태를 내는지, 입력 source snapshot/CAS/권한이 존재하는지, 업무 호스트에서 재현되는지는 별도 G0 및 통합 시험이 필요하다. R1의 `ACCEPT_WITH_CHANGE`와 `REVIEW_CYCLE=CLOSED_NO_AUTOMATIC_REREVIEW`은 그대로 유지한다.

## 4. 결과·판정 및 다음 한 행동

- `SYNTHETIC_CONTRACT_REGRESSION=PASS_26_OF_26`, `ACTUAL_SKILL_INTEGRATION=NOT_RUN`, `ACON_MODEL_REPETITION=NOT_RUN`, `EXISTING_R1_REVIEW_CYCLE=CLOSED`, `DEPLOYMENT_READY=NO`.
- 사용자의 요청 범위인 **비민감 합성 테스트 코드 실행·결과 게시 완료**. 다음 단계는 기존 L1 Work/CoWork 설치 기능의 **읽기 전용 G0(실제 reader/Evidence/승인 경로)** 대조. G0를 통과한 함수·데이터 형태가 확인되어야만 기존 스킬에 최소 연결하는 실제 통합 회귀를 확정. 업무 민감 원문은 CoWork PRIVATE/PUBLIC에도 올리지 않음.
- 현재 사용자 요청에 없는 신규 유료 ACON 3+3 재현·추가 독립 리뷰·자동 감시/예약·호스트 설정 변경은 시작하지 않음.
