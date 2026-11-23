# code-analyzer 분석 시작 시 l1sw-dev-knowledge 연결 원본 검토 및 무수정 판정 r0001

- 작성·판정: GPT / 2026-11-23 KST
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001`, 연관 `L1-WORKSPACE-RAG-20261111-001`
- 사용자 요청: 코드 분석 시작 시 `l1sw-dev-knowledge` 실행/조회 지점을 원본으로 확인하고, 수정 필요 시 최소 수정·시험·L1Work 배포까지 수행. 강제 수정 금지.
- 원본: [L1Work/main/code-analyzer_v0_15_4_1119.zip](https://github.com/wonhwipark/L1Work/blob/main/code-analyzer_v0_15_4_1119.zip)
- 원격 Git blob 및 실제 내려받은 ZIP 바이트 SHA-1 일치: `1c43503a2a4695400727fb3fb1cd0cb3c49f826b` (**PASS**); ZIP 515581 B / 217 entries.
- 기존 L1Work 릴리스 기록 SHA-256: `11e1da15ee12e750c3652190c348a7fc8e31aa1741876e3c06bc0af3413b16af`. 이번 SHA-1 원본 바이트 검증과 기존 기록의 SHA-256을 구분한다.

## 1. 실제 원본 구현 근거

| 실제 원본 | 관측 결과 | 경계 |
|---|---|---|
| `SKILL.md` 18~47행 | Knowledge는 선택적 보조 도메인 문맥; 최초 분석 전 `knowledge-link-show -- --prompt-once` 1회; 등록 이후 재사용; 실제 노출된 승인 도구로만 필요할 때 조회 | Knowledge 내용으로 CODE FACT/빌드 옵션 확정 불가 |
| `scripts/request_router.py` import 및 292~296행 | `inspect_knowledge_link(prompt_once=not args.plan_only)`를 `route-request` 초기 경로에서 호출하고, `knowledge_link` 상태를 반환 | 자동 링크 상태 점검이지 provider 실행이 아님 |
| `scripts/knowledge_link.py` | 로컬 `data/config/knowledge_provider_link.json` 등록/조회/clear, 최초 1회 질문 및 재등록 보호 | 링크 자체는 설치·접근 권한 증명이 아니며 fetch/CLI 추측·자동 설치 없음 |
| `references/knowledge_link.md` | 등록/미등록/접근 실패 처리. provider 미가용이면 `KNOWLEDGE_CONTEXT_UNAVAILABLE`로 표기 후 분석 계속 | Knowledge 부재는 BLOCKER 아님 |
| `scripts/knowledge_inventory_export.py` | 기존 CODE FACT의 후단 지식 번들 export | 시작 시 무조건 지식 게시하는 경로 아님 |
| `tests/test_knowledge_link_v0151.py` | 최초 1회 질문, 영구 링크/중복/clear 및 라우터 앵커 검증 계약이 이미 존재 | 이번 turn에서 Python 테스트 직접 실행은 하지 않음 |

## 2. REUSE / CONNECT / MODIFY 판정

- **REUSE:** 분석 시작 시 등록상태 점검·등록 링크 재사용·실제 승인된 tool 노출에서만 지원 지식 참조·접근 실패 비차단·source-evidence 우선 정책.
- **CONNECT:** Module/Feature/Scenario 및 Procedure·MSC의 기존 지식 검색/후보 선정/중복 방지는 `l1-knowledge-updater`가 담당하고, 확인된 source 범위를 `code-analyzer`에 전달. 기존 [업무 GPT 야간 분석 인계 r0001](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md)을 재사용.
- **MODIFY:** **NOT_NEEDED.** 매 코드 분석마다 그룹 Knowledge 전체 조회를 강제하거나 신규 provider CLI/API·RAG engine을 넣을 근거 없음. 기존 안전 경계, 저사양 실행 및 소스 사실 우선순위를 훼손할 위험이 더 큼.
- **남은 검증:** 실제 Linux 설치본이 PUBLIC ZIP과 같은 버전인지, 승인된 Agent가 `l1sw-dev-knowledge` 조회 tool을 제공하는지, 해당 질의가 실제 NR UL Tx Switching 분석 정확도·중복 절감에 도움 되는지는 G0/첫 시나리오 E2E 확인 전 UNKNOWN. 야간 batch에서 미등록 링크 시 출력되는 질문의 무인 처리도 현장 검증 대상(질문 출력 자체가 분석 중단이라는 증거 없음).

## 3. 수행·시험·배포

- 원격 Git ZIP exact bytes ↔ Git blob SHA-1: **PASS**.
- 기존 ZIP 내부 `SKILL.md`/`knowledge_link.py`/`request_router.py`/참고문서/기존 테스트의 정적 원문 검토: **PASS**.
- 코드 변경/신규 regression/Windows 독립 리뷰: **NOT_RUN (변경 없음)**.
- 신규 버전 ZIP 및 L1Work 재배포: **NOT_NEEDED / NOT_POSTED**. 이미 공개된 v0.15.4 원본 불변.
- 업무 Linux G0, 실제 provider invocation, 제품 C++/MSC 및 Workspace E2E: **NOT_RUN**. 문서만으로 자동 호출 PASS를 주장하지 않음.
- 사용자 요청의 조건부 릴리스는 수정 필요성이 입증되지 않아 실행하지 않음. 유료 호출/예약/설치/운영 변경 없음.

**NEXT_ONE_ACTION:** 업무 GPT가 기존 야간 분석 인계의 첫 대표 사례에서 Updater의 Knowledge 조회 → Analyzer의 source fact → MSC/개인 Work 저장·readback을 실제 검증. 정확한 재현 가능한 누락·오탐이 발생하면 **해당 결손을 소유한 스킬만** 최소 수정 후 재시험·릴리스 판정.
