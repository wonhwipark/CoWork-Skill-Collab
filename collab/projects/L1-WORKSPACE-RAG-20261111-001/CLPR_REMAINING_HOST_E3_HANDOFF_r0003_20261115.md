# CL/PR 이슈 분석 — 남은 P4 historical / Analyzer Evidence / E3 구현·검증 인계 r0003

- Work ID: L1-WORKSPACE-RAG-20261111-001.
- 기준 저장소: GitHub **PRIVATE** wonhwipark/CoWork-Skill-Collab
- 브랜치: **main**
- 상대 경로: **collab/projects/L1-WORKSPACE-RAG-20261111-001/CLPR_REMAINING_HOST_E3_HANDOFF_r0003_20261115.md**
- 작성일: 2026-11-15 KST
- 목적: 기존 실행 결과를 보존하고 남은 P4 per-file before/after, 실제 Analyzer Evidence, 호스트 E3, 배포 게이트만 최소 범위에서 이어감.
- **문서 게시 자체는 어떤 Windows Claude Code 세션·Job·Watcher·MCP도 자동 실행하지 않음.** 호스트 개발·격리시험 실행은 해당 실행 호스트의 허용된 호출·권한 범위에서만.

## 기준 결과 — 중복 작업 금지

- [최신 CURRENT](CURRENT.md)
- [후보 개발·E2 결과](GPT_CLPR_WORK_EVIDENCE_E2_DEVELOPMENT_RESULT_r0001_20261115.md)
- [확대 회귀 3.10/3.11 결과](GPT_CLPR_EXPANDED_REGRESSION_AND_REMAINING_GATES_r0001_20261115.md)
- [원래 r0002 인계](CLPR_REMAINING_IMPLEMENTATION_HOST_HANDOFF_r0002_20261114.md)
- PRIVATE main 후보 5종: p4-code-owner v0.6.9 SHA 51363124aad349dd01f7e21f471bff4ae4d41d33d221ed9e4fb84e4217aab5ba; l1-github v0.3.57 SHA f1b8fb43d3af427f2c5d52864051c65894f3cb45969ab35ca502f344735611ce; l1-fix-workflow v1.6.69 SHA d4ba119298cd5763fd18ace2d54223fff010a8d2a1703ebab80eb4fa1b35846b; code-analyzer v0.15.3 SHA dbbd0f9fd4d5173b8f445aa2fabd9f7417593ecd996ac0e2f0ad10278f3626c2; work-ledger-kernel v0.7.39 SHA 24184fe760c058a6fbc4f79c8d2d3e580978c05bde4597155e81fa3d6f23885a.
- E2는 Python 3.10/3.11 각각 WorkReference 6/6 PASS, 확대 11 suite 중 9 PASS/2 기존 PUBLIC baseline FAIL, Python 417 구문 PASS. 기존 Workflow failure 2건은 **완전 회귀 PASS 아님**, 기존 원본의 동일 실패 근거를 우선 보존.
- Workflow v1.6.69·Kernel v0.7.39는 개발 후보. PUBLIC ZIP 및 설치본 아님. 기존 후보/운영본 덮어쓰기 금지.

## 단계 B0 — 실제 호스트 READ-ONLY preflight

1. 사내 승인된 소스/원장 호스트인지, 설치된 스킬/Kernel 버전·MCP 진입점과 사용자 승인된 임시 Work 영역이 무엇인지 실측. 불명확하면 STOP/BLOCKED. 운영 Work/DB/WAL/SHM에 read-only 주장만으로 side-effect 발생하지 않는지도 점검.
2. Mango MCP의 실제 허용된 describe/files/integration 조회·필드 구조·권한을 **읽기 전용** 확인. 과거 CL 파일별 rev/from_rev 및 실제 revision 범위, integration lineage의 유무/불일치와 Code Analyzer input 계약을 기록. 임의 p4 CLI/sync·토큰 공유·회사 소스 외부 반출 금지.
3. GitHub merged PR 메타의 base/head/merge SHA, target branch·적용 상태, branch drift·dirty/untracked·object missing을 각각 구별. 동일 repo PR 처리 직렬화.
4. 기존 Kernel 등록 provider/kind/stage Evidence 슬롯·work_reference_add/find·record_evidence API, Work artifact/export, 직렬 writer와 충돌/재시작 복구 경계를 실제 설치 소스 기준으로 검증. Schema/record.json/README/index/registry 임의 확장 금지.

## 단계 B1 — 호스트 격리 구현 및 시험

1. P4 before/after 원문과 정확한 file revision이 확보된 경우만 CODE_CONFIRMED 근거 후보. 미확보면 INFERENCE 또는 UNKNOWN 유지, 환각 root cause·PASS 금지.
2. 기존 Work를 조회하고 유일 매칭에서만 P4/GitHub PR ref 추가; idempotency 0 duplicate, 다중 Work 충돌·부분 검색·동시 두 Writer를 fail-closed. 반드시 시리얼 직렬 실행과 rollback 지원.
3. **실제 분석 결과 및 source anchor를 확보한 뒤에만** 등록된 Kernel Evidence kind/stage/provider 조합으로 실제 파일/해시·code revision 기록. CLPR 그룹핑 후보는 Evidence가 아님. Problem/RootCause/Fix/Verification/CurrentApplicability 각각 근거수준 독립 표기.
4. 격리된 승인 Work/Evidence write→readback→export, 재실행 동일 hash·중복 Work 0, Work source scope 변경 시 drift 차단, registry invalid·missing source·cross-work 경쟁·rollback negative tests. Work ID, 실제 원장 바이트 해시, 명령, 성공/실패/미실행을 보고.
5. 이전 Workflow baseline 두 실패의 현업 요구·테스트 기대를 소스 사실로 판정하고, 실제 기능 영향이 확인된 범위만 최소 패치·회귀시험. 기존 사용 기능 손상 없이 진단; 무조건 기대값 변경으로 PASS 위장 금지.

## 단계 C — 확대 회귀 및 공개 배포 분리 게이트

- Python 3.10/3.11에서 각 후보 정확한 ZIP 바이트·SHA/CRC/ZipSlip/심링크, VERSION·manifest·skillsilent 및 모든 관련 회귀/C01~C12.
- 실제 사내 호스트 E3, 회사 내 반출 금지 자료 격리, 보안·개인정보·rollback, 새 패치 독립 리뷰 필요성을 각 분리 상태로 기록. 동일 개발 세션 자체 시험은 SELF_TEST_REPORTED, 독립 리뷰 PASS로 소급 금지.
- 기존 사용자 지시에 따라 추가 유료 Claude 독립 리뷰/REQUEST/READY 자동 실행하지 않음. 필요한 별도 승인 게이트는 BLOCKED로 기록.
- 모든 공개 배포 조건이 실제 PASS되고 유효한 게시 권한·승인이 확보된 **최종 ZIP**만 GitHub PUBLIC wonhwipark/L1Work, branch main, root에 신규 버전명으로 게시·원격 바이트 SHA 재검증. 그 전 개발 ZIP은 PRIVATE 유지.
- 운영 설치본/실Work/운영 DB·Job·Watcher/LIVE·Knowledge 정본은 별도 운영 승인 없이는 불변.

## 결과 제출 계약

PR 없이 PRIVATE main 다음 경로에 비민감 결과 MD 하나로 통합하여 게시하고 원격 readback·commit/SHA/bytes 확인:
collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_CLPR_REMAINING_HOST_E3_EXECUTION_RESULT_FOR_GPT_r0001_20261115.md

기록 순서: 실제 host preflight → 단계별 DEVELOPMENT/SELF_TEST/E3/INDEPENDENT_REVIEW 상태 → 수정 파일/diff 및 신규 ZIP 무결성 → 차단 원인 → GitHub 원격 readback → 공개 게시 게이트. 소스·회사 로그·보안자료·토큰은 PRIVATE에도 넣지 않음. CURRENT.md/TRACKER.json은 기존 이력 보존 후 갱신. GPT가 결과를 직접 확인해 배포 또는 BLOCKED 판정.

**다음 한 동작:** 허가된 업무 호스트의 개발 실행 세션에서 B0 read-only preflight부터 시작. 기존 합성 E2 및 5종 SHA 검증 성공을 재실행 완료 요구로 오해하지 않음.
