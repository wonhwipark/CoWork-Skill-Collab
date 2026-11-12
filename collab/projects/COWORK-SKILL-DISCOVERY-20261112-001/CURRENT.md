# COWORK-SKILL-DISCOVERY-20261112-001 — CURRENT

- Updated: 2026-11-12 KST
- Scope: 비민감 공통 스킬 목록·발견/재사용 절차·진입 링크·저장소 AGENTS 문서.
- USER_AUTHORIZATION: 공통 기능 목록을 보강하고 새 창 시작 절차에 연결. 18개 PRIVATE/원본 재확인은 다음 별도 작업으로 분리.
- DOCUMENTATION: READY_FOR_PUBLICATION / REMOTE_READBACK=PENDING (이 게시 후보 작성 시점).
- SKILL_18_DETAIL_RECHECK: PENDING_CHECK / NOT_RUN_THIS_TASK.
- INDEPENDENT_REVIEW: NOT_RUN.
- SKILL_CODE_CHANGE / HOST_INSTALL / JOB_RUN / SCHEDULER_CHANGE / REQUEST_READY / PAID_REVIEW / PUBLIC_POST / LIVE_CUTOVER: NOT_RUN.
- 기존 운영 상태는 START_HERE 및 이관 CURRENT를 따른다. 이 작업으로 LIVE를 변경하지 않음.

## 변경 내용과 근거

| 대상 | 내용 |
|---|---|
| `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` | 기존 문서·대화에서 발견한 후보를 이름/별칭·기능·입출력·연결·근거/미확인으로 정리. 전체 18개 또는 최신 설치본 검증 주장 없음 |
| `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md` | 운영지침 → 공통 목록 → 프로젝트 CURRENT/열린 메모 → 관련 원문 → 재사용 판정 |
| `AGENTS.md` | 저장소에서 시작하는 에이전트의 조회·재사용 순서 |
| `collab/START_HERE.md`, `README.md`, `collab/knowledge/OPERATING_BASELINE.md` | 공통 목록·시작 절차로 발견 경로 연결 |

기준 원문 조회 commit: `fb5402fdec4412703670a995f46fc9244170d710`. 근거는 기존 공통 문서·r0005 후속 메모·Job-list 전달 계약과 사용자 대화다. 기존 감사의 요약을 재사용했으며 18개 ZIP/원문을 재검증하지 않았다. 원본/API 미확인은 후보 검색의 후속 확인 사항으로 유지한다.

## 보존·실행 경계

- PUBLIC r0005 handoff 및 진행 중 요청, L1 RAG 프로젝트 CURRENT/후속 메모는 이번 변경 대상이 아니다.
- G0 사실/G1 가정 분리, K5.8 설계표 제한, 기존 Knowledge/metadata 불변, 기존 Kernel/Updater/Git 제공자 우선 재사용을 유지한다.
- 새 스킬·함수·엔진·schema·DB·예약/자동 감시·모델 호출을 만들지 않는다.
- GitHub와 AGENTS의 지침을 읽는 세션에 적용하는 문서 연결이다. ChatGPT 프로젝트 설정·다른 창·설치 스킬의 자동 변경은 수행하지 않았다.

## 실제 확인 상태

- 기존 문서·경로 조회: 수행. 파일 존재·내용을 직접 확인.
- 변경 문서 UTF-8·내부 링크·시작 순서·미확인/승인 경계 점검: PASS (문서 정적 확인; 기능시험 아님).
- 원격 commit/바이트 SHA-256/readback: 게시 후 확인 예정. 검증 후 별도 영수증과 최신 절을 추가.
- 실제 스킬 호출·호스트·통합시험: NOT_RUN. 문서 점검을 기능시험 PASS로 처리하지 않는다.

## 다음 별도 작업

`SKILL_18_DETAIL_RECHECK=PENDING_CHECK`: 기존 18개 감사 자료와 PRIVATE 정본을 대조해 정확한 이름·원본 위치·역할/I/O·연결·근거 수준을 보강한다. 사용자가 정한 순서에 따라 현재 문서 연결 작업 완료 후 별도 진행하며, 이 기록으로 백그라운드 작업이나 유료 리뷰를 시작하지 않는다.
