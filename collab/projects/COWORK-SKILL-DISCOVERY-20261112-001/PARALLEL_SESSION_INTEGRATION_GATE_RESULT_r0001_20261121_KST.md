# CoWork 병렬 대화창 통합 게이트 구현 결과 r0001

- 기준: 2026-11-21 KST
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001` (새 창/공통 협업 운용)
- 재현 사례: `L1-WORKSPACE-RAG-20261111-001`의 Wiki UI/Write/Preferences 분리 개발
- 원인: 개별 코드/시험은 있었지만 동일 배포 산출물의 병렬 변경을 최종 단일 ZIP에서 증명하는 필수 공통 검사가 없었음.
- 변경 코드: `collab/ops/integration_gate.py`, `collab/ops/tests/test_integration_gate.py`
- 계약: `collab/ops/CONTRACTS/PARALLEL_CHANGE_INTEGRATION_GATE_V1.md`
- 연결: `collab/CONTEXT_BRIEF.md`, `collab/START_HERE.md`, 이 Work의 CURRENT, Viewer Work의 CURRENT
- 테스트: Python 3 stdlib unittest, 임시 bare Git remote + UI/Write 가상 ZIP, **19/19 PASS** (정상 포함, stream 누락·덮어쓰기·겹침 충돌/해결, SHA 변경, local/remote 기준 변경, 필수 cross-stream 누락, 개발/배포 구분, dirty tree, 중복·경로 이탈 ZIP, 시험 근거 누락 등).
- **독립 리뷰:** NOT_RUN. **두 개 실제 ChatGPT 창 간 작업 동기화/동시 게시:** NOT_RUN.
- **기존 Viewer v0.4.0 실제 입력으로 검사:** NOT_RUN (실제 소스 ZIP과 브라우저/Linux E2E 게이트 증거를 추가해야 함).
- **자동 배포 차단:** 기존 모든 게이트/게시 주체를 스크립트 호출로 연결한 사실은 미검증. 사용자 요청에 따라 자동 GitHub Actions 재가동 없음.
- **CoWork GitHub 게시:** 코드·시험·문서 등은 본 결과 기록이 포함된 commit 및 원격 readback으로 별도 확인. 미확인 시 NOT_POSTED/UNVERIFIED.
- **금지/불변:** Windows watcher/DB/신뢰 키·서명, REQUEST/READY, 실제 Linux 호스트, L1Work 패키지, 유료 리뷰/자동화 전부 변경 없음.
- **다음 한 동작:** Viewer Work에 현재 실제 UI·Write·Preferences 3개 stream을 등록하고 동일 ZIP에 대한 교차 브라우저 + Linux G0 시험 후 통합 게이트 재검증. 새로운 대화창 두 개에서 등록/경합과 게시 CAS까지 실증.
