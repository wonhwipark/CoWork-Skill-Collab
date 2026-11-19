# PEC-HOP 우선 · ACE 최소 보강 — 단방향 운영·현장 실증 판정 r0001

- 작성: 2026-11-19 KST / 소유: 기존 `COWORK-SKILL-DISCOVERY-20261112-001`
- 사용자 최신 결정: **PEC-HOP 우선 / ACE 기존 기능 최소 연결 / ACON 보류**. 범위 축소와 현장 검증 기준 수립 승인. 신규 ZIP 배포·업무 Linux 설치·실제 지식 원본 외부 전송 승인이 아님.
- **방화벽 가정:** 업무 Linux의 코드·분석·Evidence·Knowledge·운영 기록·실행 판정은 외부 GitHub PRIVATE/PUBLIC 및 개발 GPT로 **전달할 수 없음**. 별도 적법한 반출 승인이 실제로 확인된 자료에만 예외 가능; 현재 기본은 `NO_EXPORT`. *“비민감 요약”도 반출 승인 없이 기본 회신하지 않음*.
- 이 문서는 스킬 구성과 검증 기준(공개 가능한 일반 인터페이스·합성 예시)을 정리할 뿐, 현장 호스트 자체의 영수증을 대체하지 않음.

## 1. 한 방향 구획과 인수 주체

```text
[개발·검증 영역]                               [업무 실행 영역]
GPT + Windows Claude Code
  공개 가능한 공통 스킬 코드
  합성 source/Evidence로 자체시험·독립 리뷰
      |
      v
CoWork PRIVATE: 설계·코드·리뷰·게이트
      |
      v
L1Work PUBLIC/main 루트: 승인된 최종 ZIP
      |
      v  (입력 전용, 승인된 skill-updater 경로)
[업무 GPT + 허용된 Linux Agent/MCP]
  실제 설치본·버전·read-only 접점 자체 대조 (G0)
  기존 Workflow + Kernel: Work·결정·Evidence
  기존 Code Analyzer: CODE FACT·근거·source rev
  PEC-HOP: 원본·발췌·revision/byte-range 검증
  ACE: 최신 유효 결정 선택과 HOLD·중단 Work 재개
  Knowledge Updater(업무 전용): 기존 Work 지식 후보·승인/게시 경계 유지
  내부 전용 비교·판정·시험 영수증 보존
      X
  코드/실행 결과/비민감 요약의 외부 기본 회신 경로 없음
```

- **개발영역의 완료 책임:** 스킬 원본 pin·비민감 코드·합성 회귀·독립 코드 리뷰/릴리스 게이트 후 PUBLIC 배송 및 공개 ZIP SHA 검증까지만.
- **업무 실행영역의 완료 책임:** 설치 실제 revision·호환성·원본 권한·실제 코드/Work Evidence 읽기·관련 내부 비교·로그/영수증 **업무 환경 내 보존**. 개발영역은 내부 `HOST_VERIFIED`를 읽지 못하므로 `NOT_EXTERNALLY_VERIFIED` 표기.
- 사용자 모바일은 수정 요구를 **새로운 비민감 일반 계약 또는 외부에 작성 가능한 합성 재현**으로 전달할 수 있을 때만 전달; 실제 로그·Code FACT·함수/IPC/고객 식별·경로/내부 source hash·업무 평가표는 전달 금지. 문제가 외부에서 재현 불가능하면 **업무 GPT/Agent 현장 수정·현장 테스트** 담당으로 끝내고, 원본 코드 외부 송신을 요구하지 않음.
- `L1Work POSTED` ≠ `skill-updater installed` ≠ `업무 적용 PASS`; 외부가 모른다는 것은 현장 테스트가 불가능하다는 뜻이 아님.

## 2. 최신 우선순위·스킬 책임(중복 엔진 금지)

| 범위 | 우선순위 / 소유자 | 최소 CONNECT; 실측 미확인은 유지 |
|---|---|---|
| PEC-HOP: 근거 왜곡·누락 방지 | **P1 / Code Analyzer(Evidence 생성) + Workflow/Kernel(읽기 전용 소비)** | 기존 source pin·Evidence가 제공하는 원본 byte offset/length와 digest를 먼저 재사용; raw range가 없으면 원문 구간을 기존 권한으로 재조회해 로컬 비교하거나 `HOLD/NOT_VERIFIED`. IPC/상태/함수·branch/조건·MSC source-map 링크는 현장 내부에만 보존 |
| ACE: 중단 Work 재개 정확성 | **P2 / Workflow·Kernel 기존 reader** | 동일 Work·동일 scope의 최신 **유효 권한/출처/append 순서**를 확인하고 재개 요약에 선택 결정·미해결·다음 작업 연결. 모호하거나 권한 결여 시 `HOLD`; timestamp/LLM 추측만으로 판단 금지 |
| ACON: 압축 실험·학습 | **DEFER** | 새 모델 실행, baseline/압축본 3+3, 자동 지침/메모리 갱신, 독립 엔진 신규 개발·운영 없음. 기존 v1.6.73 후보의 ACON 순수 코드/20 PASS는 **과거 개발 사실로 보존하되 현재 적용·릴리스 범위에서 제외** |
| Knowledge Updater | **변경 대상 아님 / 업무 GPT·허용 Agent** | 현재 업무 전용 원본을 외부로 제공하지 않음. ACE/PEC 적용 때문에 기존 그룹 Knowledge writer와 개인 knowledge writer의 소유권·승인 경계를 변경하지 않음 |

**합리화:** 코드가 있는 v1.6.73 후보 전체를 출하하는 것이 아니라, 실제 기존 API 접점을 현장 G0로 확인한 뒤 **P1→P2만 최소 연결**. 최종 재패키징 시 소스 계보·변경분 보존, 새로운 고유 버전과 정확한 byte pin/CRC·정보등급·회귀·필요 코드 독립 리뷰/릴리스 게이트를 적용. 유효 배포 승인은 기존 사용자 승인 범위 안에서 재사용, 현재 미충족 gate 우회 금지.

## 3. 현장 소규모 실증 — 모든 업무 원본·결과 로컬 보존

### 3.1 시험 방법

1. **업무 GPT가 업무 환경 안에서만** 실제 설치된 Workflow/Kernel/Analyzer/Updater의 역할과 호출 가능한 기존 reader, Evidence format/원본 권한, G0 부작용(읽기만 하는데 mkdir/쓰기 발생하는지)을 확인. 이전 설치본을 추정하지 않음.
2. 현재 우선순위의 실사례 **1개**(예: NR L1 Tx recovery와 동일 유형의 업무 Work; 실제 Work ID/코드/IPC 이름은 외부로 내보내지 않음)를 현장에서만 선택. 먼저 기존 기능 baseline의 처리 결과·누락·시간을 보존.
3. 기존 코드와 원본 revision을 pin하고, PEC 검증을 기존 Evidence reader에서 적용. ACE는 진행 중 중단/재개 또는 상충 결정을 가진 같은 Work에서 제한적으로 적용. 실제 운영 Work를 원본 대신 수정하지 않도록 테스트 사본·권한을 구분.
4. 동일 입력·동일 설정·동일 담당 평가기준으로 이전/개선 경로를 비교. 필요하면 **3~5개 서로 다른 유효 사례**로 확대하되, 샘플 수와 실패 상태를 속이지 않음. 반복 실험을 요구할 근거가 아직 없는 ACON은 시험하지 않음.
5. 시험 기록·비교표·실패·Evidence 원문은 모두 업무 환경의 기존 Work/Evidence·승인된 QA 경로에 보존. 외부 CoWork는 `HOST_TEST_NOT_OBSERVABLE`로 유지(반출 없는 구조).

### 3.2 수용 시험과 등급(실제 수행 전 전부 NOT_RUN)

| ID | 대상 | 최소 관측 시험/합격 기준 |
|---|---|---|
| PEC-P1 | 원본 연결 | 현장 권한 검증 후 pinned source revision·근거 구간 raw bytes·필요시 offset/length/digest 일치만 `PASS`; 없거나 읽지 못한 경우 `HOLD` |
| PEC-P2 | 변조·stale 부정시험 | 별도 **합성** 원문 1 byte 변조·stale branch/source rev·발췌 위치 누락을 각각 `FAIL/HOLD` 처리. 통과 판정 0 |
| PEC-P3 | CODE FACT→MSC 인계 | 선택 사례의 핵심 IPC/상태/예외 조건/소스 근거 누락·변형 **0건**, 근거 없는 Cause 확정 **0건**. 실제 원문·변환본은 현장에만 보관 |
| ACE-P1 | 최신 결정 | 동일 Work·동일 scope의 유효 순서/철회·상충 결정 사례를 비교. 유효 최신 결정을 선택하고 모호함은 `HOLD`, 잘못된 승인 적용 **0건** |
| ACE-P2 | 중단/재개 | 기존 Work ID, 마지막 승인된 결정, 미해결 항목 및 다음 액션을 유지. 불필요한 새 Work 생성·이미 끝난 Job 재실행 **0건**, 재개 과정 source/revision 혼합 **0건** |
| SAFE-P1 | 무영향 | 실험 도중 무단 그룹 Knowledge 게시, Git/P4 write, Job/READY·운영 변경·유료 호출 **0건**. 데이터가 외부로 전송된 횟수 **0건** |
| VALUE-P1 | 업무 효과 비교 | 기존 baseline vs 변경판에서 **근거 오류/작업 재개 누락/수동 확인 횟수/경과 시간**을 같은 기준으로 기록. 개선된 지표가 실측되지 않으면 `BENEFIT_NOT_DEMONSTRATED`, 정확성 퇴행 또는 핵심 게이트 실패 시 `FAIL` |

- 정확성·보안 항목은 **0건 위반**이 합격 조건. 속도·수동 작업 감소는 미리 임의 목표 퍼센트를 적용하지 않고 실측 비교로 판단.
- 소수 샘플에서의 PASS는 `LOCAL_PILOT_PASS_SCOPE_LIMITED`이며 전체 모듈·실서비스 품질 PASS가 아님.
- 실제 업무 데이터에 대한 허가·안전 정책 미확인이면 **업무 환경 합성 fixture만 테스트**하고 실사례는 `NOT_RUN` 유지.

## 4. 스킬·배포 및 기존 결과와의 양립

- 현재 `l1-fix-workflow_v1_6_73_1119.zip` 개발 후보 CI는 **20 PASS**(ACE 7/PEC 7/ACON 6), 760,970 B, SHA256 `4e435a165a692f9c77c816067d6dd7d11f920def4c808d4ecb06b44b613a5c77`, `development_not_for_deployment`. 과거 코드/CI·독립 설계 R1은 보존, **최신 승인된 PEC+ACE 파일럿 설계로 자동 승격하지 않음**.
- 공개 배포를 위한 기존 보호 조건(신규 코드 독립 리뷰, 패키지 계보/호환·통합 시험, raw Git/인증/동시성 writer 안전·권한, channel, 공개 정보등급·byte SHA) 유지. 현재 `PUBLIC_ZIP=BLOCKED_NOT_POSTED`.
- **중요한 수정:** 기존 CoWork `CURRENT`·L1Work 인계서 §§9~12의 “업무 GPT의 비민감 설치/시험 요약을 외부로 회수” 문구는 **사용자 최신 반출 불가 조건에서 실행 요구로 사용하지 않음**. 최소 G0와 수용 시험은 업무 환경 내부에서 완료·보존; **외부 정본은 이를 PASS로 소급하지 않음**.
- 재검토: 실제 P1·P2 효과가 업무 환경에서 확인된 뒤에만 ACON 재개 여부/외부 공개 코드 최소 수정 필요성을 별도 판단. 작업 범위를 다시 넓히는 자동화 금지.

## 5. 오늘 판정 및 다음 한 행동

- `SCOPE_DECISION=PEC_P1_ACE_P2_ACON_DEFER`
- `NO_EXPORT_BOUNDARY=ENFORCED_AS_DESIGN` (정책 문서 판정; 실제 네트워크 차단 시스템 설치/시험 아님)
- `DEVELOPMENT_PREVIOUS=WORKFLOW_V1.6.73_DEV_CI_20_PASS`
- `LOCAL_PILOT_ALL=NOT_RUN`; `BUSINESS_GPT_G0=NOT_RUN`; `HOST_VERIFIED_EXTERNAL=NOT_OBSERVABLE`
- `PUBLIC_NEW_FINAL_ZIP=BLOCKED_NOT_POSTED`; `NO_NEW_REQUEST/READY/MODEL/INSTALL/KNOWLEDGE_WRITE=YES`
- **NEXT_ONE_ACTION:** 업무 GPT가 PUBLIC 인계서 최신 보완절에서 **현장 전용** G0와 `PEC-P1~3/ACE-P1~2/SAFE-P1/VALUE-P1` 시험 계약을 읽고 1개 현장 사례에 적용 가능성을 자체 판정. 결과·근거·평가표는 업무 환경에만 기록. 외부 GPT는 PUBLIC 배포 품질만 따로 담당; 현장 PASS는 확인했다고 주장하지 않음.
