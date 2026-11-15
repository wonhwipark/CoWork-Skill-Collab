# GPT 공통 투두 — 개선 후보 목록

- 관리: GPT / 작성·갱신 기준: 2026-11-15 KST.
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/GPT_TODO.md`.
- 목적: 전체 운용·협업·L1 지식·맥락 관리의 개선 후보와 GPT 검토 의견을 한곳에서 조회.
- 진입: [공통 맥락 브리프](CONTEXT_BRIEF.md) · [협업 진입점](START_HERE.md).
- 이번 범위: 공통 목록 구성·네 가지 후보 등록·기존 상세 문서 연결. 후보의 실제 수정·시험·Claude Code 리뷰는 시작하지 않음.

## 개선 후보

우선순위는 GPT의 검토 의견이며 실행 승인이 아님. 아래 네 항목은 기존 상세 설계의 조회 묶음이며 별도 실행 작업을 중복 등록한 것이 아님.

| ID | 우선 | 상태 | 개선 후보 | GPT 검토 의견 | 기존 상세 근거 |
|---|---|---|---|---|---|
| TD-001 | 1 | 후보 | 협업 체계·L1 지식 통합 탑뷰 정리 | 기존 r0001/r0002와 최신 정본을 대조해 전체 순환과 공통 지도 진입 링크를 보완 | [통합 설계 D01~D06](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md#3-통합-설계-todo) |
| TD-002 | 1 | 후보 | 새 창 재개 실제 검증 | 문서 적용 완료와 실제 재개 성공을 구분. 같은 Work·작업 흐름·승인 범위·다음 행동 선택 확인 | [D07·D09 / V07](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md#7-수용검증-체크리스트) |
| TD-003 | 2 | 후보 | 여러 스킬 간 인계·피드백 순환 검증 | 첫 승인 사례에서 기존 Work/Evidence와 인계표를 재사용하고 맥락 누락·중복 Work·불필요한 재분석 확인 | [D05·D06·D10](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md#3-통합-설계-todo) |
| TD-004 | 2 | 후보 | CURRENT의 과거·현재 표시 정리 검토 | 이미 적용된 상단 현재/과거 구분을 유지하고, 과거 LATEST·PENDING 표현의 추가 정리 필요성을 실사용에서 확인 | [D07](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md#3-통합-설계-todo) |

상세 문서의 D01~D10·수용 기준·이력은 그대로 재사용. 위 네 묶음으로 다른 기존 항목을 취소하거나 신규 실행을 시작하지 않음.

## GPT 검토 메모

- 기준 근거: 원격 commit `8d991be90e803af8e0baef0ac2489320be6babf7`의 [상세 설계 TODO](projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_CONTEXT_DESIGN_TODO_r0001_20261115_KST.md)와 [맥락 운용 CURRENT](projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md). 이 기준은 등록 당시 관찰이며 실행 시 최신 정본을 재조회.
- TD-001: [아키텍처 r0002](projects/L1-WORKSPACE-RAG-20261111-001/L1_E2E_INHOUSE_OFFSITE_ARCHITECTURE_r0002_20261111.md)는 그룹 기술 정본·개인 Work 역할을 이미 보완한 설계. r0001만 보고 같은 보완을 새 결함으로 단정하지 않음. provider·버전·승인·시험 상태는 탑뷰에 복사하지 않고 해당 CURRENT로 연결.
- TD-002·003: 기존 맥락 운용 규칙·문서 연결 적용 완료는 유지. 실제 새 창·여러 스킬 인계·첫 분석 사례의 실행 검증은 각각 별도 근거가 필요하며 이번 목록 등록을 PASS로 대체하지 않음.
- TD-004: 최신 CURRENT의 상단 요약과 과거 구분 개선은 이미 존재. 남은 표현의 오독 가능성을 확인할 후보이며 실제 실패가 입증된 결함으로 취급하지 않음.
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
- 다음 한 동작: 필요할 때 공통 목록을 조회하거나 실행할 항목 ID를 지정.
