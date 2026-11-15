# GPT 공통 투두 — 개선 후보 목록

- 관리: GPT / 작성·갱신 기준: 2026-11-15 KST.
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/GPT_TODO.md`.
- 목적: 전체 운용·협업·L1 지식·맥락 관리의 개선 후보와 GPT 검토 의견을 한곳에서 조회.
- 진입: [공통 맥락 브리프](CONTEXT_BRIEF.md) · [협업 진입점](START_HERE.md).
- 최초 등록 범위: 공통 목록 구성·네 가지 후보 등록·기존 상세 문서 연결. 최초 등록 당시 후보의 실제 수정·시험·Claude Code 리뷰는 시작하지 않았음. 후속 실행·판정은 아래 목록과 해당 Work의 CURRENT를 따른다.

## 2026-11-15 최신 실행 판정

- **TD-002 완료:** 실제 새 창 V07 수동 조회·기존 Work 재개 PASS. 무지시 자동 로더·호스트 기능 시험과 구분.
- **TD-001 완료(문서 범위):** 협업→업무·지식→피드백 단일 탑뷰/정본·인계·승인/검증 경계의 D01~D09 설계 반영. 실 운영·코드·RAG PASS 주장 없음.
- **TD-003 작업 연결:** 기존 NR 분석 Work를 추적한 8개 계약 시나리오 DOC_TRACE_PASS. 실제 업무 스킬 다중 호출·Knowledge 게시/역링크·RAG E2E는 NOT_RUN.
- 최신 결과/승인·다음 행동은 [맥락 Work CURRENT](projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md)와 해당 실행 Work CURRENT에서 조회. 신규 독립 리뷰/모델 호출/REQUEST/READY 없음.

## 개선 후보

우선순위는 GPT의 검토 의견이며 실행 승인이 아님. 아래 네 항목은 기존 상세 설계의 조회 묶음이며 별도 실행 작업을 중복 등록한 것이 아님.

| ID | 우선 | 상태 | 개선 후보 | GPT 검토 의견 | 기존 상세 근거 |
|---|---|---|---|---|---|
| TD-001 | 1 | 완료 | 협업 체계·L1 지식 통합 탑뷰 정리 | D01~D09의 비민감 설계·정본 책임·통합 흐름도·현행 포인터 적용, 원격 본문 대조. 실제 호스트·유료 리뷰와 구분 | [통합 탑뷰](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_TOPVIEW_r0001_20261115_KST.md) · [원래 설계 D01~D09](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md) |
| TD-002 | 1 | 완료 | 새 창 재개 실제 검증 | 실제 별도 대화에서 PRIVATE 최신 지도·목록·기존 Work와 목적별 CURRENT 4건을 재조회. V07 수동 새 창 PASS, 자동 선조회는 별도 미검증 | [V07 실제 새 창 결과](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD002_V07_ACTUAL_NEW_CHAT_VALIDATION_20261115.md) · [기존 V06 점검](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD002_SESSION_ROUTING_CHECK_20261115.md) |
| TD-003 | 2 | 작업 연결 | 여러 스킬 간 인계·피드백 순환 검증 | 8개 인계/오류 분기 문서·증거 추적 PASS, 실제 Linux MCP→업무 Work→Updater→Knowledge E2E는 NOT_RUN. 기존 NR 분석 Work 첫 사례에 연결 | [TD-003 인계 추적](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD003_MULTI_SKILL_HANDOFF_FEEDBACK_TRACE_20261115.md) · [D05·D06·D10](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md#3-통합-설계-todo) |
| TD-004 | 2 | 완료 | CURRENT의 과거·현재 표시 정리 검토 | 기존 맥락 Work의 CURRENT 과거 절 2곳 `(LATEST)` 오독 위험 정정. 역사적 내용·근거 보존, PRIVATE 원격 본문 재조회 완료. 다른 Work의 전수감사는 이번 범위 밖 | [D07](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md#3-통합-설계-todo) · [TD-004 결과](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD004_CURRENT_HISTORY_LABEL_REVIEW_20261115.md) |

상세 문서의 D01~D10·수용 기준·이력은 그대로 재사용. 위 네 묶음으로 다른 기존 항목을 취소하거나 신규 실행을 시작하지 않음.

## GPT 검토 메모

- 기준 근거: 원격 commit `8d991be90e803af8e0baef0ac2489320be6babf7`의 [상세 설계 TODO](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md)와 [맥락 운용 CURRENT](projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md). 이 기준은 등록 당시 관찰이며 실행 시 최신 정본을 재조회.
- TD-001: [아키텍처 r0002](projects/L1-WORKSPACE-RAG-20261111-001/L1_E2E_INHOUSE_OFFSITE_ARCHITECTURE_r0002_20261111.md)는 그룹 기술 정본·개인 Work 역할을 이미 보완한 설계. r0001만 보고 같은 보완을 새 결함으로 단정하지 않음. provider·버전·승인·시험 상태는 탑뷰에 복사하지 않고 해당 CURRENT로 연결.
- TD-002·003 등록 당시에는 현 세션의 Work 탐색만 확인했고 V07·다중 스킬 E2E가 미실행이었다. 2026-11-15 후속 재개에서 **V07 실제 새 대화 수동 조회는 PASS**, TD-003의 **계약 추적은 PASS/실제 호스트 E2E는 NOT_RUN**으로 별도 기록.
- TD-004: 기존 상단 요약 구조를 유지하고 2026-11-12 과거 절의 잘못된 최신 표기 두 곳을 최소 정정했음. 문서 표기 정리의 완료이며 새 창 실제 재개·호스트 기능 시험 PASS로 확대하지 않음.
- 피드백: 같은 목적의 실행 보완은 원래 Work로 회수. 전체 운용의 새 아이디어는 이 목록에 후보로 추가. 결과·판정 원문은 해당 Work의 결과/결정/notes에 보존.

## 조회·작업 연결

1. 사용자는 “공통 투두 보여줘”, “TD-001에 의견 추가해줘”로 조회·정리 요청. GPT가 세션에서 중복·우선순위·검토 의견·근거를 관리하고 게시 후 원격 확인.
2. “TD-001 진행해줘”처럼 항목 실행 요청이 오면 관련 CURRENT·최신 근거·기존 승인 범위를 확인해 같은 목적의 기존 Work에 연결. 새 Work는 기존 Work로 처리할 수 없을 때만 생성.
3. Claude Code 협업은 사용자가 해당 협업을 요청한 경우 실제 계약에 따라 연결. 후보 등록·우선순위 지정만으로 REQUEST/READY·모델 호출·자동 감시를 만들지 않음.

| 상태 | 의미 |
|---|---|
| 후보 | 아이디어·GPT 의견·근거를 보관 |
| 보류 | 보류 이유·재검토 조건을 기록 |
| 작업 연결 | 사용자 실행 지시·범위·실제 Work/요청 경로를 기록. 진행·결과는 해당 CURRENT에서 조회 |
| 완료 | 연결 Work의 완료 근거·결과 링크를 확인한 뒤 기록 |

후보 상태·우선순위·GPT 의견의 정본은 이 목록. 상세 문서는 수정 방향·근거·완료 기준, CURRENT는 실제 작업 진행·결과를 관리. 브리프·진입점에는 고정 링크만 두며 후보별 상태를 복사하지 않음.

## 등록 이력

- 2026-11-15: 사용자 승인으로 GPT 공통 목록과 TD-001~004 구성. 기존 상세 설계 TODO를 재사용하고 공통 브리프·협업 진입점에 연결. 기존 Work·진행 중 요청·실행 승인 상태는 유지.
- 2026-11-15: 사용자 순차 검토·실행 요청에 따라 TD-004를 기존 맥락 Work에서 먼저 처리. [점검 결과](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD004_CURRENT_HISTORY_LABEL_REVIEW_20261115.md)와 [CURRENT](projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md)에 연결. PRIVATE 문서 수준 점검이며 독립 리뷰·실제 새 창 검증 미실행.
- 2026-11-15: TD-002 기존 Work에서 [현 세션 라우팅 4건](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD002_SESSION_ROUTING_CHECK_20261115.md) 점검, V06 세션 내 PASS / V07 실제 새 창 NOT_RUN. `작업 연결`로 기록.
- 2026-11-15: 새 대화의 PRIVATE 직접 조회로 [TD-002 V07](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD002_V07_ACTUAL_NEW_CHAT_VALIDATION_20261115.md) PASS, 목록을 `완료`로 전환.
- 2026-11-15: [TD-001 통합 탑뷰](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_TOPVIEW_r0001_20261115_KST.md) 작성, 브리프 통합도 및 START_HERE/공통 L1 포인터 보강. 비민감 문서 범위 `완료`.
- 2026-11-15: [TD-003 실제 증거 추적](projects/COWORK-SKILL-DISCOVERY-20261112-001/TD003_MULTI_SKILL_HANDOFF_FEEDBACK_TRACE_20261115.md) 8개 문서 분기 PASS, 호스트 E2E NOT_RUN으로 `작업 연결`.
- 다음 한 동작: TD-003 실제 E2E는 NR 분석 기존 Work에서 Linux Agent의 v0.4.38 설치 SHA·신규 Job ID/Run ID·Receipt/MCP readback 확인부터 재개. 승인 없는 Job 재실행/그룹 게시 금지.
