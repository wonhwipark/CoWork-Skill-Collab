# 설계 리뷰 질문과 후속 수락 조건
## 리뷰 목적·출력
리뷰 유형은 SCOPED_INDEPENDENT_DESIGN. 전체 RAG/LIVE/권한 제품을 재감사하지 않고 01/02의 두 진입·MD·HTML 연결을 비판적으로 검토.
기존 POLICY-STATIC-V1의 1회·최대 USD 1·R1 입력 목표 16,000/출력 목표 3,000 tokens 범위. 설계 관점은 유지하되 전체 R2 심층 검증으로 승격하거나 새 모델/서브에이전트·도구 재귀 호출하지 말 것. 예산 내 확정할 수 없으면 PARTIAL_SCOPE.
출력: ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD. (1) 설계 이해·타당한 결정 (2) 확인된 결함과 근거/반례·심각도·최소 수정 (3) 비차단 개선·필요 시 구조 대안과 비용/회귀 (4) G0·미검증·다음 구현 순서.
결함 수 강제 없음. 확인된 결함 없으면 없다고 보고. 문서 가정을 설치 기능으로 승격하거나 개발 자체시험을 독립 통합 PASS로 재진술하지 말 것.

## 집중 질문
- Q1: A/B가 실제로 독립 진입인가? Updater가 Work 저장/출처를 위해 전체 Workflow를 호출해야 하는 숨은 의존이 남는가?
- Q2: 분석의 기술 내용, Converter 상세 MSC, Kernel Work 문서, Updater 지식 MD의 owner가 중복/누락되지 않는가? 같은 MSC_VIEW 이름의 두 역할은 충분히 구분되는가?
- Q3: 순수 지식 작성의 Work ID optional을 유지하면서 출처·revision·재사용을 기존 계약으로 보장할 수 있는가? 미확인을 새 원장으로 해결하는 과잉이 있는가?
- Q4: ISSUE 설명과 HTML 출력을 분리하는 선택 인자 제안이 가장 작은 보완인가? 기존 action/manifest로 더 단순하게 가능한가? 직접/관리 gateway·양쪽 caller의 호환성은?
- Q5: Kernel artifact 이름/경로 매핑 이후 링크의 최종 owner는 어디인가? 원본 Evidence hash를 유지하며 작은 공통 formatter 또는 기존 writer만으로 해결 가능한가?
- Q6: AS-IS와 TO-BE·코드/설계/시험 상태, 여러 source revision·variant가 혼동될 수 있는 지점은?
- Q7: 부분 게시·수동 본문 변경·응답 유실·개인/그룹 독자 접근 차이에 대한 안전 동작이 충분한가?
- Q8: 구현 순서에서 Updater/그룹 G0 미확인이 독립적인 Workflow 이슈 HTML 보완까지 불필요하게 막는가? 각 경로의 완료 게이트를 따로 제시할 것.
- Q9: 재사용보다 신규 조정기·스키마·프로필·공통 문서 엔진을 과도하게 도입하는 부분이 있는가?

## 후속 수락 시나리오 — 모두 계획, 이번에 실행하지 않음
| ID | 상황 | 기대 조건 |
|---|---|---|
| T01 | Updater 직접 UL CA 조사·Work 없음 | Workflow 실행 0, Work 강제 생성 0, 기존 형식으로 출처 보존 또는 해당 G0 미확인만 표시 |
| T02 | Updater의 기존 분석/Work 근거 재사용 | 동일 scope/revision/hash면 중복 분석 0, 원본 무손실 |
| T03 | Workflow 이슈 AS-IS/TO-BE | Updater 필수 호출 0, knowledge WRITE 0, 기존 Work에 근거 등록·문서 연결 |
| T04 | TO-BE 제안/수락/적용 구분 | 설계 수락이 코드 반영/시험 PASS로 보이지 않음 |
| T05 | ISSUE 기존 호출 / ISSUE+HTML / 기존 PROCEDURE_FEATURE | 기존 기본 출력 유지 / 이슈 문구+HTML / 기존 HTML 호환 |
| T06 | renderer 미설치·구문/Phase 실패 | 원본 보존·진실한 부분/차단 상태, 없는 HTML·단계 링크 0 |
| T07 | exporter 이름 변경·작은 파일 제한·부분 복사 | published_path/hash 대조, 원본 무변조, 유효한 출력만 링크 |
| T08 | 사람 수정 MD·마커 누락/충돌 | 본문·타 절차 무손실, Preview/HOLD, 중복 append 0 |
| T09 | 원격 HTML URL 없음·CSP 차단 | SVG/다운로드 폴백, 웹 클릭 열람 PASS로 오인 0 |
| T10 | source branch/revision·dirty 조건 변경 | stale 표시/보류, 다른 코드 사실로 자동 재사용 0 |
| T11 | 같은 repo의 Work/Knowledge writer 동시 동작 | 경로/actor·잠금·HEAD 검증은 기존 계약 우선, 혼합 stage/손실 0 또는 G0 보류 |
| T12 | 그룹 게시 성공·개인 링크/응답 실패 | 원격 정산 후 미완료 연결만 복구, 그룹·분석·Job 재실행 0 |
| T13 | 한 경로의 G0 차단 | 다른 경로의 허용 개발/표현 시험은 계속, 전체 통합 PASS로 승격하지 않음 |

구현 후 시험은 PASS/FAIL/SKIP/NOT_RUN, source/G0/합성/호스트 E3를 구별. 설계 리뷰 PASS 자체는 이 표의 실행 PASS가 아님.
