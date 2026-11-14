# CL/PR 개발 후보 확대 회귀시험 및 미완료 게이트 — 2026-11-15 r0001

- Parent Work: L1-WORKSPACE-RAG-20261111-001.
- Source: [기존 Work 참조 연결 E2 결과](GPT_CLPR_WORK_EVIDENCE_E2_DEVELOPMENT_RESULT_r0001_20261115.md), [기준선 비교](GPT_CLPR_ISOLATED_PY310_PY311_VALIDATION_RESULT_r0001_20261114.md).
- Runner: [GitHub Actions run 43610383804](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43610383804). 검증 브랜치 clpr-e2-work-evidence-20261115; commit 8bc97d5a0bb1b2038ea1ddf31081900b9849ee50.
- Verdict: E2_REFERENCE_LINK=PASS / EXPANDED_REGRESSION=9_OF_11_SUITES_PASS_PER_PYTHON / 2_KNOWN_BASELINE_FAILURES / FULL_REGRESSION=NOT_COMPLETE / PUBLIC_RELEASE=BLOCKED.

## 실제 Python 3.10.22 / 3.11.18 결과

| 항목 | 3.10 | 3.11 |
|---|---|---|
| 5종 PRIVATE ZIP SHA-256/CRC/경로/심링크 검사 | PASS | PASS |
| 신규 ZIP 포함 Python 파일 417개 구문검사 | PASS | PASS |
| P4 CL·scope, GitHub PR·Merged PR, Analyzer share | 5/5 PASS | 5/5 PASS |
| Kernel multi-work, Kernel core | 2/2 PASS | 2/2 PASS |
| 신규 CLPR 기존 WorkReference 통합시험 | PASS | PASS |
| 기존 Workflow Resume pytest suite | 5 tests PASS | 5 tests PASS |
| 기존 Workflow issue-brief | FAIL | FAIL |
| 기존 Workflow core | FAIL | FAIL |
| **합계** | **9 suite PASS / 2 FAIL** | **9 suite PASS / 2 FAIL** |

실패 2개는 test_provider_output_distinguishes_current_execution의 출력 문구 불일치와 test_gs10_resume_uses_ledger의 WORK_NOT_FOUND vs RESUME. 2026-11-14 기준선에서 PUBLIC 원본 v1.6.67과 CLPR 후보 v1.6.68 모두 동일하게 재현된 기존 실패. 신규 후보 v1.6.69에서도 동일. 이번 신규 수정 유발 회귀 근거는 없으나 전체 PASS 아님. CI conclusion=failure 그대로 보존.

CI 설정의 두 차례 보정: (1) 격리 브랜치에서 신규 ZIP을 찾지 못해 PRIVATE main 읽기 전용 checkout 및 고정 SHA 검사 추가. (2) 테스트 러너의 pytest 패키지 부재로 추가 suite import 실패. 격리 runner에 pytest 8.4.2를 설치하고 pytest-native로 실행해 해당 suite 5건 정상 PASS 확인. 환경 문제를 코드 결함으로 소급하지 않음.

## 이번까지 완료한 WorkReference 연결

Workflow에서 Kernel.work_reference_find를 호출하나 기존 Kernel 공개 진입점이 없어 AttributeError 재현. 기존 Kernel WorkReferences.find에 읽기 전용 facade를 추가한 Kernel v0.7.39 개발 후보와 Workflow v1.6.69 개발 후보 구현. 임시 합성 원장의 기존 Work 유일 매칭, P4/PR source ref 기록·재조회, 중복 기록 0, 다중 Work 충돌·부분 검색·입력 오류 차단, Preview 기본·명시 Commit 분리 시험 Python 3.10/3.11 모두 PASS. 새 Work 생성·분석 Evidence 자동 등록·Knowledge 쓰기는 없음.

- [Workflow v1.6.69 PRIVATE 개발 후보](candidates/l1-fix-workflow_v1_6_69_1115.zip): 866671 bytes, SHA-256 d4ba119298cd5763fd18ace2d54223fff010a8d2a1703ebab80eb4fa1b35846b.
- [Kernel v0.7.39 PRIVATE 개발 후보](candidates/work-ledger-kernel_v0_7_39_1115.zip): 409355 bytes, SHA-256 24184fe760c058a6fbc4f79c8d2d3e580978c05bde4597155e81fa3d6f23885a.
- 두 후보 모두 development_not_for_deployment. 원격 readback과 바이트 SHA-256 PASS 기록: [PRIVATE persistence run 43609821708](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43609821708).

## 차단 및 남은 실행

- 실제 Analyzer의 허가된 Evidence kind/stage/provider, 코드 anchor, 실제 Work artifact/write/readback/export 확인: NOT_RUN. 후보 그룹 자체는 확정 원인 Evidence가 아님.
- P4 historical per-file describe/files/integration rev/from_rev 및 과거 소스 조회: 사내 Mango MCP 호스트·허가된 데이터 접근 부재로 BLOCKED. 무인가 P4 CLI/sync 실행 없음.
- 실제 업무 호스트 E3, PR target landing, Cross-Work 동시성, 실Work write/readback, 전체 C01~C12, 보안·롤백, 패치 후 독립 리뷰: NOT_RUN/NOT_COMPLETE.
- 원본 Workflow 2 FAIL을 기존 기능 요구와 시험 기대값으로 구별한 뒤 필요한 최소 범위만 수정·재시험. 전체 릴리스 게이트 PASS 이전에는 PRIVATE 후보 보존만 허용하고 PUBLIC L1Work 신규 ZIP 배포 금지.
- 이번 작업에서 운영 설치·원장·DB/Watcher/Job/Skill-Updater/Knowledge/LIVE 변경 0. 추가 유료 Claude 리뷰, REQUEST/READY 0. 이 문서 게시만으로 외부 Windows Claude Code 실행되지 않음.

**NEXT_ONE_ACTION:** 인가된 개발 호스트에서 Mango MCP historical revision과 Kernel Evidence 슬롯 read-only preflight → 승인된 격리 Work 실통합 E3 → 잔여 회귀·보안·롤백·배포 게이트 확인. 접근 불가하면 해당 단계만 BLOCKED로 관리.
