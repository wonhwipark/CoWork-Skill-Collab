# TD-003 — 다중 스킬 인계·피드백 순환 검증 (정본 추적)

- 날짜: 2026-11-15 KST
- Work: `COWORK-SKILL-DISCOVERY-20261112-001` (별도 Work 생성 없음)
- 목적: 사용자 실행 요청에 따라 D05/D06/D10의 **인계 의미, 기존 Work 재사용, 오류/피드백의 귀속**을 최신 증거로 검토.
- 범위: PRIVATE 정본과 실제 보고가 남은 단계의 **문서·원격 증거 추적**. Linux MCP/업무 L1 Work·Knowledge 실제 호출, Windows 신규 Claude 유료 리뷰는 이번 세션에서 실행하지 않음.
- 기준: [통합 탑뷰](COWORK_L1_INTEGRATED_TOPVIEW_r0001_20261115_KST.md), [Work→Knowledge 흐름](../L1-WORKSPACE-RAG-20261111-001/L1_WORK_TO_KNOWLEDGE_FLOW_r0001_20261114_KST.md), [Updater/Workflow r0005 계약](../L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0005_20261111.md).

## 1. 재사용한 기존 실제 사례 — NR L1 Tx Init RACH

| 순서 | 담당·기존 컴포넌트 | 실제 근거와 현재 확인 상태 | 후속 확인 |
|---|---|---|---|
| 1. 사용자 요청/CoWork 추적 | `NR-L1TX-CODE-ANALYSIS-20261115-001` | [EXECUTION_REQUEST](../NR-L1TX-CODE-ANALYSIS-20261115-001/EXECUTION_REQUEST.md)와 [CURRENT](../NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md) 실존. `L2_L1_TX_REQ`부터 PHY IPC까지 최소 범위 | 문서 추적 ID를 업무 Kernel Work ID나 Job ID로 동일시 금지 |
| 2. 배포·인계 | Job-list v0.4.38 → PUBLIC `L1Work/main` | 최신 CURRENT: `job-list_v0_4_38_1115.zip` 배포 해시 `0cdda16fe214f86811d4df25cc04f3453ec93789ddc9bc2b0769e730bb9c16e0`, 정적/회귀 38 PASS, 게시·원격 재다운로드 PASS | ZIP 배송 ≠ Linux Skill-Updater 설치·Job activation |
| 3. 실제 호스트 접수 | 모바일 Agent → Linux MCP → Skill-Updater / Job-list | `SKILL_UPDATER_INSTALLED=NOT_VERIFIED`, `JOB_ACTIVATED=NOT_VERIFIED`, 결과 readback `NOT_VERIFIED` | 신규 Job ID `JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01`의 Catalog·Registry·Queue/Run/Receipt 일치 확인 |
| 4. 실제 코드 분석 | `code-analyzer` 우선, 필요 시 검증된 Workflow 분석 전용 action | `CODE_ANALYSIS=NOT_RUN`. `l1-knowledge-updater`를 코드 분석의 대체 도구로 오인하지 않음 | 허용된 read-only 호출과 source revision·scope, CODE FACTS·영수증 확인 |
| 5. 업무 Work/Evidence | Workflow / work-ledger-kernel | 업무 Work의 새 결과 저장·기존 Work 재개 및 Evidence 대응 `NOT_VERIFIED` | 동일 업무 Work ID, source/Artifact/Evidence 참조, 저장 후 재조회 |
| 6. 후보/Preview/보완 | Knowledge Updater | 설계상 `REUSE/CONNECT` 계약은 존재. 실제 입력 매핑·후보·비교·보완 반환 `NOT_RUN` | 기존 Work를 유지, 부족한 사실만 재확인; 분류 검토행 ≠ 실제 지식 ID |
| 7. 게시/역링크/재사용 | 기존 지식 writer / Kernel / RAG Provider | `GROUP_KNOWLEDGE_WRITE=NOT_RUN`, 실제 게시 revision·역링크·검색 본문/Provider 소비 `NOT_RUN` | 유효한 게시 승인과 실제 원격 readback; 역링크·RAG 각각 별도 증거 |

**중요:** 첫 실제 승인 NR 분석은 L1 지식 게시와 범위가 다름. 분석 권한을 자동으로 그룹 write/게시 승인까지 확대하지 않음. `JOBLIST-SMOKE-20261114-001`은 별도 무모델 Worker 목표의 기존 Work; 본 분석 Job과 합치지 않음. 과거 소비 Job `JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01`은 재큐잉 금지.

## 2. 비교: 이미 실제로 완료된 협업 리뷰 운송

- [GitHub LIVE 이관 CURRENT](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md)의 독립 R1 `REQ-COWORK-V0220-R1-20261115` 리뷰 원문·receipt·usage·dispatch와 GPT 판정은 원격 조회 완료, 독립 `BLOCKING=0`, 단일 모델 호출로 보고됨.
- 이는 **CoWork 개발→정식 리뷰→영수증→GPT 판정** 경로에 관한 실증이며 **업무용 Workflow↔Kernel↔Updater↔팀 지식의 실행 검증 근거는 아님**.
- 별도 [자동 승인 CURRENT](../COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md)는 `AUTO_SIGNING=OFF`, v0.2.21 정적 BLOCKING 2. 기존 LIVE 완료와 자동 승인 개선 완료를 합치지 않음.
- [L1 지식 CURRENT](../L1-WORKSPACE-RAG-20261111-001/CURRENT.md)의 Work→Knowledge 설계 독립 리뷰 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`은 사용자 **최대 $1/1회 승인**이 있으나 서명·READY·실 리뷰 아직 미완료. 승인된 다른 요청을 재사용하거나 새 유료 호출을 발행하지 않음.

## 3. 인계·오류 주입 시나리오 — 정적 계약 대조 (D05/D06)

| 시나리오 | 기대 동작·현재 문서 대조 | 판정 |
|---|---|---|
| CoWork Work/요청 ID와 업무 Kernel Work ID가 다름 | 서로 다른 SSOT로 보존, 새 업무 Work 자동 생성·ID 겹침 가정 금지 | DOC_TRACE_PASS / HOST_NOT_RUN |
| Work/Evidence는 있으나 후보에 source revision이 빠짐 | Updater는 부족 근거를 원래 Work에 반환; 미확정 주장 그룹 게시 금지 | DOC_TRACE_PASS / HOST_NOT_RUN |
| 동일 Work·동일 입력에서 재분석 요청 | 기존 결과 유효성 먼저 확인·재사용. scope/revision 변경 때만 근거 재검토 | DOC_TRACE_PASS / HOST_NOT_RUN |
| Updater 후보 Preview의 기존 지식과 충돌 | 변경분 비교·승인 기준 revision 재검증, 기존 reader/writer 기능 우선 | DOC_TRACE_PASS / HOST_NOT_RUN |
| 게시 성공 후 업무 Work 역링크만 실패 | 그룹 본문 **재게시 금지**, 원본 Work 연결만 복구 | DOC_TRACE_PASS / HOST_NOT_RUN |
| 게시 응답이 유실되어 성공 여부 불분명 | receipt/commit/history로 정산. 불확실 실행을 임의 재실행·재큐잉 금지 | DOC_TRACE_PASS / HOST_NOT_RUN |
| 문서 설명 오류 vs 스킬 결함 vs 호스트 운영 요청 | 문서는 소유 Work, 스킬은 기존 개발 Work, 운영·비용은 현행 승인 계약으로 분기 | DOC_TRACE_PASS / HOST_NOT_RUN |
| 코드 분석 결과가 있으나 실제 RAG Provider 본문 검증 없음 | 분석·지식 게시·RAG 활용 각각 별도 상태. 링크 검색/Preview만으로 RAG PASS 금지 | DOC_TRACE_PASS / HOST_NOT_RUN |

**정적 결과:** 8개 계약 시나리오에서 각 담당·정본·차단 조건의 문서 연결을 확인. 그러나 실제 API/중복 방지/장애 복구의 **실행 결과는 하나도 시험하지 않았으므로 E2E PASS가 아님**.

## 4. 간극·위험 및 피드백 판정

| 항목 | 판정 | 이유/귀속 |
|---|---|---|
| 기존 Work 재개와 인계 표 연결 | 수용 / REUSE | Workflow·Kernel·Updater 기존 계약에서 동일 Work, Evidence·source pin·후보 입력 책임 명시 |
| 정적 역할 분리와 중복 실행 차단 | 수용 / DOC_TRACE_PASS | 신규 스키마·동기화 엔진 없이 기존 원문 계약으로 추적 가능 |
| 설치된 실제 Workflow↔Updater 호출 API·업무 기록 | 추가 확인 / NOT_VERIFIED | 최신 G0 일부 호스트 보고와 실제 함수/API 호출·readback을 구분. 업무 L1 Work에서 확인 필요 |
| NR 분석 최초 Job/Receipt·code-analyzer 호출 | 추가 확인 / NOT_RUN | 배포 완료·호스트 실행 미확인. [NR 분석 CURRENT](../NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md)에서 처리 |
| 그룹 지식 게시·역링크·Provider 본문 활용 | 보류 / E2E_NOT_RUN | 첫 실제 분석 근거와 별도 유효 승인 후 업무 L1 Knowledge에서 검증, CoWork 문서에 민감 결과 저장 금지 |
| 새 CoWork 전용 원장/API/모든 스킬 재감사 | 거절 / NO_NEW_ENGINE | 입증된 gap 없음. 다른 Work의 설치·코드·독립 리뷰를 소급 PASS하지 않음 |

## 5. 결론·다음 한 행동

- `TD003_DOCUMENT_TRACE=PASS` (기존 Work/스킬 역할·인계·피드백 8개 시나리오 정합성)
- `TD003_REAL_MULTI_SKILL_E2E=NOT_RUN` (호스트 결과·업무 Knowledge readback 없음)
- `TD003_STATUS=작업 연결`, **완료 아님**. D10/V10도 `NOT_RUN` 유지.
- `INDEPENDENT_REVIEW=NOT_RUN`. TD-003 후보 검토나 PRIVATE 문서 게시 자체는 서명·READY·모델 호출을 유발하지 않음.
- **NEXT_ONE_ACTION:** [NR 분석 CURRENT](../NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md)의 기존 허용된 Linux Agent 경로에서 v0.4.38 설치 SHA·신규 Job ID/Run ID/Worker/Receipt·MCP readback의 실제 상태를 회수. 분석 CODE FACTS·Evidence가 확인되는 경우에만 원래 업무 Work에서 Updater 후보 인계의 최소 실제 시험을 별도로 검토하고 필요한 게시 승인 범위를 확인. 이 문서로 호스트를 직접 실행·재큐잉하지 않음.
