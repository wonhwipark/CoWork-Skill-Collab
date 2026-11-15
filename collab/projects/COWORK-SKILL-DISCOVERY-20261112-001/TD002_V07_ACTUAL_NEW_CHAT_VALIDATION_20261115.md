# TD-002 / V07 — 실제 새 대화 재개 검증

- 일자: 2026-11-15 KST
- 대상: GPT 공통 투두 TD-002 / 기존 Work `COWORK-SKILL-DISCOVERY-20261112-001`
- 읽기 대상: PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main` (검증 시작 시 branch head `a1c8dd9198c52ec4458793449e35dddd8e15bdee`)
- 검증 종류: **실제 별도 ChatGPT 대화에서의 수동 정본 조회·Work 재개**. 새 대화의 자동 선조회/프로젝트 설정 동작 확인이 아님.
- 이전 증거: [TD002_SESSION_ROUTING_CHECK_20261115.md](TD002_SESSION_ROUTING_CHECK_20261115.md)의 `V06_SESSION_ROUTE=PASS`, `V07_ACTUAL_NEW_CHAT=NOT_RUN`.

## 1. 실제 수행과 결과

이번 별도 대화에서 사용자가 TD-002를 지정하여 재개를 요청한 뒤, GitHub 연결을 이용해 아래 순서로 `main`의 원문을 직접 읽음. 이전 대화의 답변·기억에만 의존하지 않음.

| 확인 | 실제 조회한 정본 | 관측 / 판정 |
|---|---|---|
| 공통 진입 | [CONTEXT_BRIEF](../../CONTEXT_BRIEF.md), blob `b51f76f44d6fea7764a3883c77be636897bf81b3` | 목적별 Work 경로·정본 소유권·재개 순서 확인 / PASS |
| 공통 목록 | [GPT_TODO](../../GPT_TODO.md), blob `b3c8a096d3e52badb45ca9ed0f99d6a0e6cd8364` | TD-002 연결, TD-001/003 후속 순서 확인 / PASS |
| 기존 Work | [CURRENT](CURRENT.md), blob `128246265ce59f439b97e1dcc10496c0d395351a` | 상단 현재 요약·승인 범위·NEXT 확인 / PASS |
| 범위·기준 | [상세 통합 설계 TODO](COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md), [SKILL_DISCOVERY_AND_REUSE_V1](../../ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md) | V07과 V06 구분, 보존·게시 계약 확인 / PASS |

### 목적별 기존 Work / 실제 CURRENT 읽기

| 요청 의도 | Work / 실제 blob | 마지막 유효 상태와 다음 한 행동 |
|---|---|---|
| NR L1 Tx Init RACH 실제 분석 | [NR-L1TX-CODE-ANALYSIS-20261115-001](../NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md), `3e56afee01775b2d0e091f46a95301f4cfb664d7` | PUBLIC v0.4.38 ZIP 배송·시험 확인. 설치/MCP 결과 미확인, 실제 분석 NOT_RUN. 기존 신규 Job ID의 설치 SHA·Receipt·MCP 연계 확인; 과거 소비 Job 재실행 금지 |
| 무모델 Job Smoke | [JOBLIST-SMOKE-20261114-001](../JOBLIST-SMOKE-20261114-001/CURRENT.md), `4a6a5f1134d6053670e901945ec758627c1a5f20` | 합성 Worker 3 PASS, 전체 ZIP/운영 E2E NOT_RUN. 실제 debug 근거 확인 후 격리 패키징·시험; PUBLIC/활성화는 별도 승인 |
| 자동 승인·서명 개선 | [COWORK-AUTO-APPROVAL-20261115-001](../COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md), `15b888d52cb313981c739abdea1df88f51cdbd81` | v0.2.21 개발 후보 GPT BLOCKING 2·MAJOR 2, `AUTO_SIGNING=OFF`. Windows Claude Code B1/B2 최소 보완·회귀/격리 SHADOW 보고 후 GPT 재판정; R2 유료/운영 위임 별도 |
| 기존 협업 단일 LIVE | [COWORK-DROPBOX-TO-GITHUB-MIGRATION](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md), `400a58c29ed29bace8b627275da2cd2c8598c4b1` | `ACTIVE_PROVIDER=GITHUB / CUTOVER=LIVE`(Windows 호스트 보고 및 리뷰/영수증 원격 판정). 신규 정식 요청 첫 실전/Notifier 실제 수신 등은 미검증; 임의 요청·재호출 금지 |

위 네 경로를 **서로 다른 기존 Work로 선택**했고, 자동 승인 개선의 OFF 상태와 기존 provider의 LIVE를 혼동하지 않음. 오래된 `CURRENT` 하위 절의 NONE/미게시 상태를 현재 상태로 선택하지 않음.

## 2. 수용 기준 판정

- `V07_ACTUAL_NEW_CHAT=PASS`: 실제 새 대화에서 공통 지도→관련 CURRENT→최신 근거/승인/다음 한 행동을 재현.
- `V06_SESSION_ROUTE=PASS`는 기존 결과 그대로 보존. V07의 이번 직접 재현을 V06 문서 점검만으로 소급 판정한 것이 아님.
- `AUTO_BOOTSTRAP/PROACTIVE_LOAD=NOT_VERIFIED`: 사용자의 명시적 요청을 받은 뒤 수동 GitHub 조회. 향후 아무 지시 없이 새 대화를 여는 경우 자동 선조회된다는 의미가 아님.
- `HOST_E2E / SKILL_INSTALL / RAG / INDEPENDENT_REVIEW=NOT_RUN`: 문서·라우팅 검증 결과로 해당 실행 상태를 변경하지 않음.
- `APPROVAL_SCOPE=READ_AND_PRIVATE_NON_SENSITIVE_DOCS`: 이번 작업은 PRIVATE 원문 읽기·문서 판정/기록으로 한정. 신규 유료 모델 호출·REQUEST/READY·호스트 실행·공개 배포·LIVE 변경 없음.

## 3. TD-002 후속과 다음 순서

- TD-002의 명시적 완료 기준인 V07 실제 새 창 수동 재개는 충족. 본 결과·GPT_TODO·CURRENT 갱신 및 원격 readback 뒤 `완료`로 확정.
- 다음은 사용자의 지정 순서 **TD-001 → TD-003**. 같은 맥락 Work 재사용, 중복 Work 생성 금지.
- 필요한 실제 업무 호스트/여러 스킬 간 인계 검증은 TD-003 또는 첫 승인된 분석 Work의 별도 E2E로 남김.

## 4. 검증 한계

이번 시험은 별도 대화의 GitHub 정본 읽기와 논리적 Work 선택을 확인. 테스트 전후 GitHub main이 다른 작업에 의해 바뀔 수 있으므로 실행·운영 상태를 고정 승인값으로 취급하지 않음. 실제 새 대화가 문서를 읽도록 **사용자가 명시 요청**한 경우에 대한 PASS이며 무지시 자동 로더 기능 PASS가 아님.
