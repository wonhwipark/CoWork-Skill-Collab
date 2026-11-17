# MSC 두 진입 설계 리뷰 요청 — 절차·규칙 감사 r0001

- 검토일: 2026-11-17 KST
- 대상: `REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117`, revision 1
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 초기 요청 게시: commit A `939b5b9f4c59534d908bc48ced59cfd25a4e8f64`, 2026-11-17 **08:09:07 KST**(실제 Git commit 시간).
- 최신 관찰 snapshot: `2c1e2ee3187c1c0548c56d353fd4388f8e3a1d24`, 2026-11-17 **23:43:09 KST**의 main commit. 아래 NOT_OBSERVED는 이 snapshot의 완전한 재귀 트리 기준.
- 이번 작업: GPT 직접 원문·바이트·관리 스킬 소스·당시/현행 계약 대조 및 격리 비유료 재현. **Windows Claude의 설계 독립 리뷰를 수행하거나 대체한 작업이 아님.**

## 1. 판정

**처음부터 규칙을 모두 충족한 요청은 아니었다.** GPT가 처음 만든 SOURCE_PIN의 `repo_id` JSON 타입이 숫자였고, 당시 운영 v0.2.23 승인 검사는 문자열과 직접 비교해 `REPO_ID_MISMATCH`로 거부한다. 원격 bytes readback만으로 이 계약 적합성까지 검증한 것은 아니었으며, 최초 게시 전 검증 누락은 GPT 요청 작성 측 문제다.

현재 pin은 기존 승인된 수정 작업에서 문자열로 보정됐다. 이번 감사에서도 수정본의 타입/ID/commit 검사는 통과했다. 하지만 **입력 보정 PASS와 Windows 서명·READY·독립 리뷰 완료는 다르다.** 이번 요청의 로컬 보류·예약·불확실 상태와 실제 호출 여부는 GPT 직접 확인 불가다.

| 검사 항목 | 판정 | 확인 근거·한계 |
|---|---|---|
| 사용자 리뷰 의도·기존 Work 재사용 | PASS | 설계안 작성·Claude 리뷰·관계/상황 전달 지시, 같은 L1 Work 사용 |
| 설계·관계·상황·근거·수락 조건 | PASS_INPUT_SCOPE | 6파일 ZIP에 설계, 스킬 역할, 세 사용 경로, 소스 발췌, 검토 질문/13개 수락 시나리오 포함. 설계 자체의 타당성 PASS는 아님 |
| REQUEST 필수 형식 | PASS | 운영 보고와 바이트가 같은 v0.2.23 parser로 필수 11필드/ID/경로 검사 통과 |
| 고정 REQUEST·ZIP·크기·해시 | PASS | REQUEST·ZIP의 현재 bytes가 commit A와 동일. ZIP CRC/경로/실제 secret scanner·manifest 5개 항목 검증 |
| 최초 SOURCE_PIN repo_id 타입 | **FAIL_CONFIRMED** | 숫자 `1451933830`은 문자열 신뢰 루트와 불일치 |
| 현재 SOURCE_PIN 보정 | PASS_SCOPE_LIMITED | 문자열 `"1451933830"`, 원래 commit A 유지. 전체 서명/권한 PASS를 뜻하지 않음 |
| 당시 정책·리뷰 범위 | LIMITED_R1 | 기존 `POLICY-STATIC-V1`, USD 1/1회 한정. 전체 구조 R2/R3와 구분해야 함 |
| 보호 로컬 위임·잔여 한도·호스트 사전 점검 | NOT_VERIFIED_BY_GPT | 기존 호스트 위임 보고와 요청 project/skill/policy는 맞지만 현재 로컬 ACL·한도·상태는 미접근 |
| GPT가 서명/READY를 만들지 않음 | 규칙 준수 | 보호된 signer/watcher 책임을 지킨 것. READY 부재 자체를 GPT의 서명 누락으로 해석하지 않음 |
| 실제 독립 리뷰·영수증 | PENDING / NOT_OBSERVED | APPROVAL_SIG/READY/DISPATCH/REVIEW_RESULT/실행 RECEIPT 모두 snapshot에 없음 |
| 무단 실행·자동 재큐잉·기존 입력 변경 | 이번 감사 0 | REQUEST·ZIP·pin·로컬 DB·정책·설치본 변경 없이 감사 문서/현재 상태만 게시 |

## 2. 확인된 최초 결함과 재현

### 원본과 현재 pin

원본 commit B `a5422ae840855cab2027d7c649f77541a082644e`:

```json
{"schema":"SKILL_COLLAB_SOURCE_PIN_V1","commit":"939b5b9f4c59534d908bc48ced59cfd25a4e8f64","repo_id":1451933830}
```

현재 동일 요청:

```json
{"schema":"SKILL_COLLAB_SOURCE_PIN_V1","commit":"939b5b9f4c59534d908bc48ced59cfd25a4e8f64","repo_id":"1451933830"}
```

- 원본 Git blob: `2ebb6f9d8264b6420a46c03de59eb8cb0a6c0d06`; SHA-256 `b6a3762a3cd8e112fc9d3d07befe5c2b436d17a37e81056d3683e392bb043535`.
- 현재 Git blob: `30db8caa9083b9c8bf78af3a4afe5469d28c8e05`; SHA-256 `d1f9c614b3dfd3a98c5804d69f81877fc598c4dea1dae6ffe583edf6e6080bcf`.
- 당시 정상 완료 요청 `REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116`도 `repo_id` 문자열을 사용했다. 기존 예시/실제 소비자 비교까지 확인했어야 했다.
- [기존 타입 보정 결과](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/SOURCE_PIN_REPO_ID_STRING_REPAIR_RESULT_r0001_20261117_KST.md)에 사용자 수정 지시·원본 보존·타입만 보정·불확실 상태 유지가 기록돼 있다. 이번 감사는 이를 다시 변경하지 않음.

당시 호스트 설치본과 동일한 SHA의 [watcher v0.2.23 ZIP](../COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip)을 내려 받아 확인:

- 282340 bytes; SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`.
- `skill_collab_watcher/approval.py:407`: `pin.get("repo_id") != trust.repo_id`이면 `REPO_ID_MISMATCH`. 숫자와 문자열을 같다고 처리하지 않는다.
- 실제 코드의 이 비교식을 AST에서 추출해 **키/서명 없이 비교식만** 실행: 원본 mismatch=true, 수정본 mismatch=false.
- 기존 [source_pin.py](../../ops/source_pin.py) `check`: 원본 exit 2/숫자형 거부, 현재 pin exit 0/PASS.
- 이 검사는 암호학적 서명 검증·실제 Windows 승인 시험이 아니다. GPT가 실제 또는 가짜 READY/서명 파일을 작성하지 않았음.

### 왜 파일 수정만으로 자동 완료를 보장할 수 없는가

v0.2.23 `auto_approval.py` 초기 pin 비교는 `str(pin.get("repo_id"))`로 값 비교를 수행하지만, 최종 승인 검사는 위와 같이 JSON 타입을 보존해 비교한다. 따라서 최초 pin은 초기 검사와 최종 검사 사이에서 다르게 처리될 수 있다. 이는 실제 소스에서 확인한 **검사 차이**다.

동 소스는 예약 뒤 오류를 `UNCERTAIN`으로 보존하며, `_resume`은 `UNCERTAIN` 상태를 자동 재실행하지 않는다. 그러므로 pin 수정이 로컬 상태 정산을 대신하지 않는다.

기존 보정 보고의 Windows 사용자 전달 `AUTO_SIGNING_UNCERTAIN`은 **Guard 코드 요청**의 관측이다. MSC 요청에도 같은 pin 결함이 존재했음은 직접 확인했지만, **MSC의 정확한 로컬 상태·오류 이벤트·예약 여부까지 같다고 단정하지 않는다.** 지출 0/호출 0도 현재 원격 파일 부재만으로 확정하지 않는다.

## 3. 설계 관점·리뷰 등급의 범위

초기 요청은 관계/책임/HTML/실패 복구를 검토하도록 지시했고, 비판적 검토·반례·최소 수정/구조 대안·근거·PARTIAL_SCOPE를 포함했다. 사용자 추가 요청의 상황 정보는 전달됐다.

그러나 당시 예산 계약은 모듈/설계의 기본 추천을 R2로, R1은 변경 영향과 인접 구조 위험의 한정 검토로 구분했다. 이 요청은 기존 자동 위임의 USD 1 범위를 유지하기 위해 **R1 한정 설계 검토**로 명시했고, R2/R3 자동 승급·추가 호출을 금지했다.

따라서 다음처럼 판정한다.

- 기존 정책명을 창작하거나 USD 1을 초과하도록 요청한 사실은 없음. 당시 v0.2.23 보호 위임 보고의 프로젝트 가족 `L1-WORKSPACE-`, skill `l1-knowledge-updater`, 정책 `POLICY-STATIC-V1`, 기간과 명목상 일치.
- R1이 설계 관련 질문을 전혀 할 수 없다는 규칙은 아님. **전체 구조 리뷰와 같은 깊이를 확보했다는 주장은 할 수 없음.**
- 당시 호스트의 실제 잔여 한도·보호 정책·승인 가능성은 실행 전 Windows가 별도로 검증해야 함. 설치 보고/REQUEST 문구가 승인 증거를 대체하지 않음.
- 현행 설계 USD 3 정책으로 기존 요청을 무단 변환하거나 같은 목적을 신규 요청으로 자동 재큐잉하지 않음.

## 4. 당시 규칙과 이후 추가된 규칙

초기 commit A에 존재했던 [예산 계약](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/939b5b9f4c59534d908bc48ced59cfd25a4e8f64/collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md)과 [현재 계약](../../ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md)을 각각 조회했다.

현재의 모든 **신규** REQUEST는 Windows LIVE `reviewer.config.json`에 대해 기존 `review_request_gate.py select/check`를 실행하고, 호환 목적/정책/금액·초안 bytes·ZIP 검증을 통과한 후 commit A로 게시해야 한다. 현행 설계 기본 USD 3·등록 정책 호환 확인과 보호 위임은 별도다. 개발 후보에만 있는 정책을 실제 LIVE로 추정하면 안 된다.

이 PREPUBLICATION 절차는 초기 08:09 요청의 commit A에는 없었다. **후에 도입된 게이트의 미실행을 과거 요청의 소급 위반으로 추가하지 않는다.** 최초 pin 타입 오류와 당시 실제 소비자 검증 누락은 그와 무관하게 확인된 결함이다. 현행 게이트/예산 정책 변경이 기존 로컬 불확실 이력·기존 요청의 승인 범위를 자동 변경하지도 않는다.

## 5. 이번 직접 확인과 시험

| 검증 | 결과·범위 |
|---|---|
| REQUEST 현재/commit A 실제 UTF-8 bytes 일치 | PASS, 3609 bytes, SHA-256 `16f375c166104161f0e0bdc836bdd5bb1db89568faf1edb5f99b776695ef82b5` |
| ZIP 현재/commit A 실제 bytes 일치 | PASS, 29111 bytes, SHA-256 `e5c2da38fda253781b2cf0179c46d3cd6dbefdc5f5efb3f0603ddaaf7d03b91c` |
| ZIP CRC/경로·링크 안전성/manifest 항목 5개 | PASS, ZIP 6멤버, manifest 자체는 외부 ZIP SHA로 고정 |
| 실제 v0.2.23 REQUEST parser·11필수 필드·ID/경로 | PASS |
| 실제 `AutoApprover._package_clean` | PASS, 기존 secret scanner/safe_extract 호출; 실제 업무 자료 공개 승인 판정과는 별개 |
| 실제 validator + READY 없음 | WAIT_INPUT: REQUEST present but no matching READY yet. 격리 가상 정책의 parser 검사이며 LIVE 정책 점검 아님 |
| 실제 승인 코드 ID 비교식 | 원본 FAIL / 현재 PASS, 비교식 범위만 |
| 공통 pin validator | 원본 exit 2 / 현재 exit 0 |
| Windows 보호 signer·로컬 SQLite/audit·예약·현재 한도 | NOT_RUN / NOT_VERIFIED |
| 실제 Claude 독립 설계 리뷰 | NOT_OBSERVED, 실행 결과·실행 영수증 없음 |

검증 과정 signer 호출 0, 키 생성 0, READY 생성 0, 모델 호출 0. 기존 운영 DB/설치/정책/위임·REQUEST/ZIP/pin 변경 0. 입력 자료로 내려 받은 소스의 관련 순수 검사만 격리 실행. 전체 watcher 회귀나 Windows 운영 시험을 재실행했다고 보고하지 않음.

## 6. 다음 한 행동

Windows Claude Code가 **같은 기존 request_id/revision**의 `auto_seen`·예약/서명 시도·dispatched/결과·비용 이력을 먼저 읽기 전용 정산하고 비민감 결과를 같은 Work에 게시한다. 기존 유효 승인과 로컬 상태로 정상 처리 가능함이 입증된 경우만 기존 signer/watcher 계약에 따라 기존 1사이클을 처리한다. 불확실·중복·한도·승인 불충족이면 보류 근거만 기록하며 임의 재큐잉/호출/위임 수정 금지.

기존 [Windows 완료 인계](GPT_MSC_DUAL_ENTRY_EXISTING_REVIEW_CLOSEOUT_HANDOFF_r0001_20261117_KST.md)를 재사용한다. 이 감사 문서 게시 자체는 Windows 실행/새 리뷰/새 비용/새 승인 요청이 아니다. 실제 REVIEW_RESULT/RECEIPT가 게시된 뒤 GPT가 지적별 판정·정리한다.
