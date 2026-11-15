# 지속 갱신형 맥락 운용 — PRIVATE 적용 기록 r0001

- 기준일: 2026-11-15 KST.
- Work: COWORK-SKILL-DISCOVERY-20261112-001 / 작업 흐름: 문서 운용 개정.
- 승인: 사용자가 PRIVATE의 공통 지침·브리프·갱신 규칙 적용을 요청한 범위.
- REUSE: 기존 브리프·CURRENT·결과/notes·계약·카탈로그·TRACKER와 Git commit/readback. 새 엔진·schema·자동화 없음.
- 입력: PRIVATE main 고정 commit `7eea02387513abe25b556ae3365f1e882d64f042`. [이전 브리프 r0006 원문](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/7eea02387513abe25b556ae3365f1e882d64f042/collab/CONTEXT_BRIEF.md)은 source blob·상태 요약·날짜별 메모를 포함한 당시 기록으로 Git 이력에 보존.

## 변경과 피드백 판정

| 항목 | 판정·적용 |
|---|---|
| CURRENT가 바뀔 때마다 브리프 요약·source blob 동시 수정 | 수정 수용: 일반 상태를 브리프에 복사하지 않고 해당 CURRENT와 근거에서 조회 |
| 결과·피드백을 CURRENT에만 전부 누적 | 구체화: 원문은 기존 결과/결정/notes, CURRENT는 짧은 현재 요약·근거 링크·다음 행동 |
| 피드백마다 새 Work 생성 | 같은 목적의 기존 Work·작업 흐름에서 보완. 독립 목적만 기존 등록 계약 적용 |
| Job 관련 진입 경로 혼재 | NR 실제 분석·기존 진단·Smoke를 별도 경로로 안내. 자동 승인 개선도 별도 경로 |
| 지도·카탈로그 유지보수 | 구조/역할/경로 및 스킬 책임/I/O/연결 변경 때만 갱신 |
| 최신 조회 실패 | 마지막 확인 시점·미확인을 표시하고 과거 정보로 실행 가능 여부를 확정하지 않음 |
| 다음 창 자동 주입 | 문서 조회 규칙 적용과 자동 선조회·프로젝트 설정을 구분 |

## 실제 확인 범위

- SELF_TEST: 문서상 갱신 기준, 브리프의 상태/source blob 복사 제거, 요청별 목적 라우팅, 상대 링크, TRACKER JSON·허용 상태·Work ID 보존을 게시 전에 점검.
- SELF_TEST=PASS (문서 정적 점검, 35개 점검·상대 링크 100개). 실제 로컬 검증 출력에 근거하며 실행 호스트·스킬 호출·새 창 인계 시험을 뜻하지 않는다.
- REMOTE_READBACK=PASS: content commit `0c15299de0b22e5c28a4b21dda5ad9c8f9c0c515`의 11개 파일 원격 본문·Git blob·바이트 SHA-256 일치. main `04f680f9dc8e11201b72cb8276a5757459303ec6` target blob 일치도 확인. [파일별 원격 검증 기록](CONTINUOUS_CONTEXT_READBACK_r0001_20261115_KST.md). 이 확인 뒤 CURRENT·본 기록·검증 기록의 메타데이터를 게시한다.
- INDEPENDENT_REVIEW=NOT_RUN. NEW_CHAT_RESUME_E2E=NOT_RUN. MULTI_SKILL_HANDOFF_E2E=NOT_RUN.
- PUBLIC 신규 게시·Windows 설치·운영 DB/Task·LIVE·유료 모델·Job 실행은 이번 작업에서 수행하지 않음.

## 다음 한 동작

실제 새 창에서 공통 지도를 읽고 목적에 맞는 CURRENT와 기존 Work/작업 흐름을 선택해 완료 근거·미확인·기존 승인 범위·다음 행동을 복기하는지 확인한다. 일반 결과 발생 시 그 Work 결과/CURRENT를 갱신하고, 이번 공통 지도에 상태를 다시 복사하지 않는다.
