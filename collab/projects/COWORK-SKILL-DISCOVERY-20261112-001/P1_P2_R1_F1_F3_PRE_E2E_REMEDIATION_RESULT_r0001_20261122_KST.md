# P1/P2 R1 F1~F3 후속 수정 · E2E 이전 검증 결과 r0001

- 작성: 2026-11-22 KST
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 근거: 독립 리뷰 `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122` rev 1, GPT 판정 `ACCEPT_WITH_CHANGE`(BLOCKING 0 / MAJOR 1 / MINOR 2)
- 범위: F1·F2 최소 Python 수정·회귀, F3 현행 분류 위험 문서/정적 30질문 점검, Work 정본 반영. Windows 실사용 E2E와 추가 유료 독립 리뷰는 제외.
- 정본: GitHub `wonhwipark/CoWork-Skill-Collab`, `main`. 이 저장소는 2026-11-22 조회 기준 PUBLIC이므로 회사 제한 코드·운영 비밀을 추가하지 않음.

## 1. 변경 및 결과

| ID | 변경 | 직접 확인 |
|---|---|---|
| F1 MAJOR | `related()`에서 `max_requests+1`개까지만 수집하고 전용 `RequestScanLimitExceeded(ValueError)` 발생. `snapshot()`은 해당 예외를 잡아 `relations=[]`, `relations_state=RELATIONS_SCAN_LIMIT_EXCEEDED`, `warning` 내 불완전·NOT_VERIFIED를 반환하며 CURRENT 및 baseline 요약은 유지 | 201개(모두 다른 Work)에서 crash 0 및 구조화된 degraded 출력 확인. 199+동일 Work 1개, 합계 200건에서 관계 누락 없음 |
| F2 MINOR | `safe_file()`의 첫 가드에 `Path(rel).is_absolute()` 및 `PureWindowsPath(rel).drive` 추가. Windows `C:/...`, `C:relative`, UNC 형식은 실파일 접근 전 거부 | `is_symlink/is_file/stat`를 예외 Mock으로 막고 유해 입력의 접근 호출 0 확인 |
| F3 MINOR | 기존 `choose()` 정책은 변경하지 않음. 미매칭 `skill` fallback 및 짧은 부분문자열·복수 주제 오분류 가능성을 운용 안내에 명시 | 30개 모델 비사용 deterministic routing probe 실행, 아래 입력/출력 보존 |

- 변경 코드: `collab/dashboard/context_query.py` / **9,472 bytes**, SHA-256 `a38465c3de7439e2594c9f42cc3f434b4c5ae7e19a5b597db0643a3a5848b59c`, Git blob `8086c2b91f67c6c99528a7fcd83fe7df34d71559`.
- 시험: `collab/dashboard/tests/test_context_query.py` / **7,746 bytes**, SHA-256 `d520dd11b3e62a0daa54e7a32c99bfd5809c43c83ea8b1ef62630444c531b9b1`, Git blob `6ff548b5cd4278218024c2738f940c11ac63dc49`.
- 실행 명령: `python -m unittest discover -s collab/dashboard/tests -p test_context_query.py -v` (격리 Linux Python 3.13.5). **13/13 PASS, ERROR 0, FAIL 0**; `py_compile` PASS. 기존 9개 시험+추가 4개 시험. 실제 Windows 환경 시험은 NOT_RUN.
- 별도 합성 CLI 확인: 201개 REQUEST 폴더 상태에서 `snapshot()`가 `LOCAL_CURRENT_READ_ONLY`와 `RELATIONS_SCAN_LIMIT_EXCEEDED`, `host_execution=NOT_VERIFIED_BY_LOCAL_FILES`, `delta=NO_BASELINE`을 반환.

## 2. F3 고정 30질문 — 모델 없는 분류기 출력 기록

현재 라우터의 **기존 출력**을 기록한 것이며, 이 30행이 자연어 의미 정답/성공률을 입증하거나 본래 A4 30문항 실사용 벤치마크를 대체하지는 않음. 1~24는 정상 키워드, 25~27은 미매칭 fallback, 28~30은 의미 충돌/오분류 관찰용.

| # | 검증 유형 | 질문 | `choose()` 출력 |
|---:|---|---|---|
| 1 | 협업 | Windows watcher 상태? | `collab` |
| 2 | 협업 | Claude 리뷰 실행? | `collab` |
| 3 | 협업 | 협업 LIVE 확인? | `collab` |
| 4 | 협업 | provider 이관 기록? | `collab` |
| 5 | 자동승인 | 보호 위임 범위? | `auto` |
| 6 | 자동승인 | 자동 승인 상태? | `auto` |
| 7 | 자동승인 | 서명 실패 원인? | `auto` |
| 8 | 자동승인 | USD 비용 계획? | `auto` |
| 9 | 스킬 | 스킬 ZIP 버전? | `skill` |
| 10 | 스킬 | 맥락 조회 방법? | `skill` |
| 11 | 스킬 | skill 설치 위치? | `skill` |
| 12 | 스킬 | 배포 후보? | `skill` |
| 13 | 대시보드 | 대시보드 화면 구성? | `dashboard` |
| 14 | 대시보드 | UI 가독성? | `dashboard` |
| 15 | 대시보드 | dashboard 화면 문제? | `dashboard` |
| 16 | 대시보드 | 화면 변경? | `dashboard` |
| 17 | 실행 | Linux MCP 실행? | `execution` |
| 18 | 실행 | Job list 상태? | `execution` |
| 19 | 실행 | opencode llm 동작? | `execution` |
| 20 | 실행 | 실행 분석 결과? | `execution` |
| 21 | 지식 | 그룹 지식 충돌? | `knowledge` |
| 22 | 지식 | knowledge RAG 이슈? | `knowledge` |
| 23 | 지식 | updater 동작? | `knowledge` |
| 24 | 지식 | L1 지식 최신? | `knowledge` |
| 25 | 폴백 | 메뉴 추천? | `skill` |
| 26 | 폴백 | 회의 일정? | `skill` |
| 27 | 폴백 | 전혀 관계없는 질문 | `skill` |
| 28 | 애매/오분류 | 그룹웨어 설치 문의 | `knowledge` |
| 29 | 애매/오분류 | 협업 정책 계약? | `auto` |
| 30 | 애매/오분류 | 대시보드 스킬 ZIP 현황? | `skill` |

- **알려진 한계:** 25~27은 질문 내용과 무관하게 `skill`로 분류됨. 28의 ‘그룹웨어’는 substring ‘그룹’ 탓에 `knowledge`로 분류됨. 29는 ‘협업/정책’ 혼합 입력에서 `auto`, 30은 ‘대시보드/스킬 ZIP’ 혼합 입력에서 `skill`로 분류됨. 세 항목은 정책 변경·정확도 검증 없이 자동 정답으로 취급 금지.
- 후속 A4: 의도 라벨을 별도로 확정한 30문항 골든셋에서 topic/Work 정합·필요 근거 확장·미확인 표시·조회 시간·토큰·질문 충돌을 측정. 본 30회 probe에서 실제 GPT/Claude 호출, host 최신 동기화, 답변 정확도/성능 A/B 측정 **없음**.

## 3. 상태/운영 경계

- `F1_CODE_FIX=POSTED`, `F2_CODE_FIX=POSTED`, `F3_DOC=POSTED`; `LOCAL_UNIT_TEST=PASS_13_OF_13`, `ROUTER_PROBE=30_EXECUTED_OUTPUT_RECORDED`.
- `WINDOWS_CODE_REGRESSION=NOT_RUN`, `WINDOWS_NATURAL_LANGUAGE_E2E=NOT_RUN`, `MOBILE_PC_RENDER_E2E=NOT_RUN`, `A4_ACCURACY_BENCHMARK=NOT_RUN`, `LIVE_LONG_RUN=NOT_VERIFIED`.
- 기존 R1 REQUEST/ZIP/SOURCE_PIN/APPROVAL_SIG/READY/review/receipt 무변경·재호출 금지. Windows watcher/서명/비용·위임/DB/예약·GitHub Actions 설정/L1Work 공개 UI 변경 없음.
- **다음 한 행동:** 기존 `WINDOWS_P1_P2_READONLY_E2E_EXECUTION_REQUEST_r0002_20261121_KST.md`에 따라 Windows에서 최신 HEAD 및 두 코드 파일 SHA 재확인 → Python 13건 회귀 → 로컬 맥락 자동 로딩 및 Q1~Q5 실제 사용 검증. 비용/실제 권한 불명 시 모델 호출 중지. 호스트 시험을 원격 코드 게시로 PASS 승격 금지.
