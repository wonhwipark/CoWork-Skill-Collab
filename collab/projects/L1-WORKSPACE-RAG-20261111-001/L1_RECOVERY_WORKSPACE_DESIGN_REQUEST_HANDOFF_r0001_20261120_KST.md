# 업무 GPT 설계 요청 — Recovery 분석 결과의 Workspace 저장·분류 연결

- 개정: r0001 / 2026-11-20 KST
- 문서 성격: 기존 기능을 대조해 최소 연결안을 확정하기 위한 설계 요청 HO
- 대상: 업무 스킬 l1-channel-recovery, 기존 l1-workspace/Work·Evidence writer, 필요한 읽기·분류 연결
- 범위: 이미 전달한 수정 CL 기반 유사 결함·Recovery 분석 기능에 **결과 보존과 Recovery별 탐색**을 연결
- 현재 상태: 설계 요청 준비. 설치본 확인·코드 수정·실제 저장·운영 적용 완료 보고가 아님

## 1. 확정된 배경과 진행 방식

사용자 확인상 **현재 MCP는 이 확인 자료의 조회·제공을 지원하지 않아요.** 따라서 사용자에게 설치본·manifest·진단 숫자·호스트 회신을 먼저 제공하도록 요구하거나, 해당 자료가 올 때까지 설계 요청 작성을 멈추지 않아요.

설계 GPT는 접근 가능한 비민감 계약과 기존 검토로 요구·배경·재사용 원칙·완료 기준을 이 HO에 정리해요. **업무 GPT가 업무 환경에서 접근 가능한 실제 스킬 원문과 저장 계약을 대조하고 구체 설계와 입증된 최소 보완을 결정**해 주세요. 현장 상세 근거는 업무 환경에 보존하며 원문을 이 대화로 반출하는 절차를 전제하지 않아요.

MCP 진단 기능 추가는 별도 작업이에요. 그 구현·설치나 사용자 자료 제공을 이번 Recovery 저장 연결 설계의 선행 조건으로 만들지 않아요. 현장에서도 접근할 수 없는 항목은 미확인으로 남기되 독립적으로 가능한 설계는 계속 진행해요.

## 2. 기존 분석 기능과 이번 추가 목적

이미 전달한 분석 컨셉은 **수정 CL을 Seed로 원인 패턴을 추출하고, 현재 코드에서 아직 보호되지 않은 유사 경로를 찾아 조치를 판단**하는 방식이에요.

- Seed의 수정 전후와 현재 분석 대상 revision을 구분.
- 후보 생성 후 caller/callee/wrapper·상위 계층의 동등 보호와 도달 가능성·반례를 대조.
- 직접 fix 누락, 미커버 변형, 이미 보호됨, 전제 불성립, 보류·미분석을 구분.
- 정적 결함 가능성, runtime 검출 가능성, 안전한 복귀 가능성을 각각 판정.
- 원인 수정·예방·관측·국소 recovery·상위 이관 중 조치를 선택.
- REQ에 대한 CNF 미수신 timeout과 기존 recovery가 이미 커버하는 해당 범위는 제외. 같은 커버 범위를 다른 이름으로 다시 후보화하지 않음.

사용자가 기존 r0002 분석 인계를 전달 완료했고 업무 GPT가 l1-channel-recovery에 적용할 예정이라고 확인했어요. 이 문서는 기존 분석 알고리즘을 중복 구현하라는 요청이 아니라 **그 결과를 축적·재조회하는 연결 설계**예요.

관련 기존 전달 자료의 정확한 위치:

- 저장소: wonhwipark/L1Work / branch: main
- 상대 경로: handoffs/L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0002_20261119_KST.md

위 링크 접근을 업무 실행의 필수 의존성으로 만들지 말고 이미 전달받은 본문을 재사용해 주세요. 업무용 l1-workspace의 실제 저장소·브랜치·root는 현장 기존 매핑에서 확인하며 동명 GitHub.com 저장소를 대입하지 않아요.

## 3. 설계 목표

**분석 원본은 기존 Work/Evidence에 한 번의 정본으로 보존하고, Recovery는 해당 원본으로 연결되는 목적별 탐색으로 제공**해요. 기존 Module→Feature→Scenario 기술 탐색과 Jira·CL·PR 연결을 함께 유지해요.

긍정 후보뿐 아니라 이미 보호됨·기각·보류·미분석 범위도 보존해야 같은 검토를 반복하지 않아요. 새 분석 revision은 이전 원본과 판정 이력을 보존해요.

저장 완료, 원격 게시 완료, 후보의 기술 검증, 제품 recovery 구현·시험 성공은 각각 구분해요. Recovery 목록에 보인다는 이유로 검증 상태를 올리지 않아요.

## 4. 기존 스킬의 책임과 대조할 지점

| 구성요소 | 재사용할 책임 | 이번 연결 설계 |
|---|---|---|
| l1-channel-recovery | 기존 Seed·현재 후보 분석과 조치 판단 | 실제 결과 형식·생산자 버전·run·revision을 반환하고 허용된 Work 저장 경로에 연결 |
| work-ledger-kernel / 기존 허용 writer | Work ID·참조·Evidence·context·revision 충돌 검사·export | 보고서를 실제 생산자 정보로 등록·보존하고 ID/SHA/readback 반환. 일반 첨부 계약이 있으면 우선 재사용 |
| l1-fix-workflow | 기존 Work 검색·선택·재개·결과 연결·docs 게시 | 동일 Work 연결. 직접 호출 라우팅이 필요한 부분만 보완하고 저장 때문에 전체 Workflow를 강제하지 않음 |
| l1-github | work_docs 목적지·remote·host path 확인과 Git 게시 | 기존 승인된 writer와 동시성·게시 readback 재사용 |
| Workspace 읽기/Viewer | 기존 문서·Work·Evidence 조회 | Recovery 모음에서 원본 보고서·Work로 연결. 조회가 분석·게시를 실행하지 않음 |
| l1-knowledge-updater | 개인 Knowledge 관리·분류·그룹 후보/Preview 연결 | 개인 Knowledge의 Recovery 모음이 필요할 때 원래 Work 참조. Work 원본을 옮기거나 덮어쓰지 않음 |
| code-analyzer / P4·Git·Jira / 조건부 issue-analyzer | 코드 사실·수정 이력·실제 로그 분석 | 기존 근거 참조를 재사용. 저장 기능 때문에 분석 전체를 다시 실행하지 않음 |
| doc-converter | 기존 문서·MSC 표현 | 그림/HTML이 필요할 때 사용. Markdown 보고서 저장의 필수 선행 작업은 아님 |

개인 Knowledge 분류의 콘텐츠 writer는 Updater, Work/Evidence writer는 Kernel이라는 기존 책임을 유지해요.

## 5. 공개본 검토에서 얻은 설계 입력

다음은 공개 고정 입력에 대한 정적 검토와 격리 확인이에요. **업무 설치본의 현재 기능 부재나 결함으로 단정하지 않아요.**

| 공개본 근거 | 확인 결과 | 업무 GPT가 대조할 내용 |
|---|---|---|
| Kernel v0.7.42 registry·record_evidence | l1-channel-recovery 제공자 조합이 없고 미등록 보고서는 REGISTRY_MISMATCH | 설치본의 실제 provider/artifact·일반 첨부 지원과 의미가 맞는 저장 경로 |
| 기존 context event | 후보 요약은 WORK_DISCUSSION으로 보존되지만 별도 보고서 Evidence 등록은 아님 | 요약 저장과 원본 보고서 등록을 구분할 실제 반환·readback |
| Kernel snapshot/active index | Recovery 목적 분류 필드가 없음 | 기존 tag/category 또는 Evidence 출처를 읽어 파생할 수 있는 탐색 |
| 기존 Evidence/export | ID·SHA·경로·크기·게시 매핑 검사 존재 | 등록 원본을 안전하게 재사용하는 producer→writer→읽기 연결 |
| 공개 Workflow v1.6.74 | knowledge/ 경로 쓰기 방어와 dirty checkout 차단 존재 | 실제 writer의 허용 경로·공유 checkout 동시성·게시 실패 처리 |

당시 공개 입력 tree는 72ec441616f6ad0cdbb7f737b26c26e470e5b778이에요. 기존 Kernel 회귀 8건 PASS와 격리 계약 확인은 저장 기반의 제한된 검증이며 실제 Recovery 연동 PASS가 아니에요.

## 6. 최소 설계 원칙

1. **기존 Work 우선:** 명시 Work ID와 Jira/CL/PR를 기존 검색으로 대조해 같은 목적의 Work를 재사용. 모호한 매칭을 임의 신규 Work로 치환하지 않음. 후보마다 새 Work를 만들 필요 없음.
2. **실제 출처 유지:** Recovery 판단을 code-analyzer/issue-analyzer가 생성한 것처럼 provider를 바꾸지 않음. 기존 합법적 첨부·등록 경로가 없을 때에만 Recovery 보고서 수용을 위한 최소 adapter/계약 확장을 제안.
3. **분류와 lifecycle 분리:** 새 RECOVERY profile·Work 원장·Knowledge DB를 선제 도입하지 않음. 기존 분류가 있으면 재사용하고, 없다면 기존 제공자·Evidence 참조에서 읽기 보기를 파생하는 안부터 비교.
4. **표현 계층 대조:** active index에 없는 정보가 Viewer에 자동 노출된다고 가정하지 않음. 실제 읽기 계약을 확인하고 필요한 좁은 projection만 검토. 임의 API 이름이나 필드를 이미 지원되는 기능으로 문서화하지 않음.
5. **원본 보존:** 임시 run 경로만 적어 장기 저장 완료로 보고하지 않음. 기존 writer의 원본 등록과 ID/SHA readback을 사용. 등록 후 본문을 수정해 SHA를 바꾸지 않고 새 revision으로 보존.
6. **재시도:** 동일 결과 재처리 시 Work·분석 식별·content hash·revision을 기존 등록/반환과 대조. 원격 게시 실패로 분석을 재실행하지 않고 실패한 단계만 복구. 중복 Evidence·게시·분석 방지에 기존 기능을 우선 사용.
7. **Knowledge 연결:** 개인 Knowledge의 Recovery 목록은 Updater가 원래 Work를 참조하도록 설계. 그룹 지식은 기존 후보·Preview·유효 승인·게시 revision/readback·역링크 절차로 별도 처리.
8. **기존 보호 유지:** 생성 README/index·knowledge/를 생산자가 독자 수정하는 방식을 피하고 기존 허용 writer 사용. 실제 writer의 경로·동시성·권한 검증 범위를 명시.
9. **저사양 모델:** 기존 분석을 재사용하며 한 Seed/범위씩 순차 처리. 설계 요청을 이유로 다중 Agent·새 분석 엔진·전체 저장소 재분석을 추가하지 않음.

위 항목은 필요한 의미와 판단 기준이에요. 신규 영속 schema/enum/API 명세를 미리 확정한 것이 아니에요.

## 7. 보고서 보존 내용

| 항목 | 원본에 필요한 근거 |
|---|---|
| 식별·출처 | 기존 Work, 실제 생산자/version/run, 등록 결과의 Evidence 참조와 hash |
| Seed와 현재 대상 | Jira/CL/PR, 수정 전후 및 현재 source revision, product/branch/build·범위 |
| 원인 패턴 | 설명 주장·코드 사실·추론 구분, Seed 전후 보정 근거 |
| 후보 전체 | 미커버·보호됨·반례·보류·미분석, caller/callee/상위 보호 대조 |
| 검출·복귀 | 손상 상태·검출 신호·상태/자원 소유자·cleanup·재진입·복귀 조건 |
| 조치·검증 | 조치 선택 근거, 실제 시험과 NOT_RUN, 분석/보호/시험 coverage, 잔여 위험 |

모든 내용을 Kernel root metadata에 새 필드로 넣으라는 뜻이 아니에요. 실제 지원되는 메타정보와 보고서 본문으로 나눠 매핑해 주세요.

## 8. 업무 GPT가 작성할 구체 설계와 수락 기준

설계 산출물에는 실제 설치 소스/branch/revision, 사용 가능한 기존 함수·입출력, REUSE/CONNECT/입증된 GAP/미확인, 최소 변경 파일, 실패·재시도·롤백·호환 및 시험 계획을 포함해 주세요. 외부 확인 자료를 받아야만 이 설계를 작성할 수 있다는 조건을 두지 않아요.

| 수락 항목 | 완료 근거 |
|---|---|
| 같은 Work 저장 | 기존 Work에 원본 보고서가 등록되고 Work/Evidence ID·SHA 재조회 일치 |
| Recovery 탐색 | Recovery 모음→Work→원본 연결과 Module→Feature→Scenario 탐색 동시 유지 |
| 이력 보존 | 보호됨·기각·보류·미분석과 이전 source revision/판정 유지 |
| 반복·부분 실패 | 같은 결과/응답 유실·게시 실패에서 기존 등록을 대조하고 중복 분석·등록·게시 방지 |
| 잘못된 입력 | 미등록/의미 불일치 provider, 모호한 Work, SHA 불일치·revision 변경을 정확하게 거부/보류 |
| 상태 분리 | 원본 저장/export/게시/분류 조회와 기술 검증·제품 구현/시험을 별도 보고 |
| Knowledge 선택 연결 | 범위에 포함될 때만 Updater 후보·승인·그룹 게시/readback·Work 역링크 확인 |

위 시험은 **계획**이에요. 실제 실행 결과는 PASS/FAIL/SKIP/NOT_RUN으로 구분해요. 현장 설계 결과와 상세 시험 근거는 업무용 Work에 보존하고, 필요하면 허용된 비민감 진행 요약만 회수해요.

이 HO는 설계 요청이며 코드 변경·호스트 설치·서비스 시작·Job·유료 호출·그룹 게시를 자동 승인하지 않아요. 기존 유효 권한 범위에서 가능한 작업은 계속하고, 범위 밖 단계만 구분해 주세요.

## 9. 다음 한 동작

**업무 GPT가 이 문서로 같은 업무를 재개해 실제 스킬·저장/읽기 계약을 대조하고 최소 연결 설계를 작성**해 주세요. 사용자에게 MCP 설치본 자료나 진단 결과를 다시 요구하는 흐름으로 되돌아가지 않아요.
