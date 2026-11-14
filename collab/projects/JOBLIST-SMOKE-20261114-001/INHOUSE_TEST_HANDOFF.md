# 사내 GPT / Linux MCP — 신규 Job-list 격리 시험 인계
Target repo: `wonhwipark/CoWork-Skill-Collab`
Branch: `main`
Paths:
- `collab/projects/JOBLIST-SMOKE-20261114-001/CURRENT.md`
- `collab/projects/JOBLIST-SMOKE-20261114-001/requests/candidate-one-shot-jobs.json`
- `collab/projects/JOBLIST-SMOKE-20261114-001/scripts/joblist_e2e_smoke.py`
- `collab/projects/JOBLIST-SMOKE-20261114-001/tests/test_smoke_candidate.py`

위 CURRENT와 코드를 먼저 읽고, 사내 GPT/MCP에서 이미 디버깅한 수정분이 실제 호스트에 적용됐는지 **수정 파일/버전/격리시험 증거**로 확인해줘. 접근 불가 항목은 NOT_VERIFIED로 표시.

기존 소비된 `JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01`은 절대 재실행/재큐잉하지 말 것. 신규 Job ID는 `JOB-20261114-JOBLIST-E2E-SMOKE-01`. 먼저 로컬 격리 복사본에서 기존 v0.4.36 기준으로 profile/worker, active requests 1건, manifest/identity를 일치시켜 신규 `job-list_v0_4_37_1114.zip` 후보를 빌드하고 정적검증·합성 회귀시험을 진행해줘. **기존 운영 설치본/DB/Queue/Registry/예약작업 불변**, 원본 소스·Knowledge 수정 금지.

PUBLIC ZIP 게시, 기존 skill-updater를 통한 운영 설치, activate/Runner 실제 실행은 이 문서만으로 승인되지 않았음. 배포 및 실제 실행 게이트 전에는 새 ZIP을 PUBLIC root에 올리거나 운영 파일을 바꾸지 말 것. 본 시험은 LLM 호출 없는 파이프라인 Smoke이며, 기능 분석/MSC 완료로 보고하지 말 것.

보고: `DEVELOPMENT / SELF_TEST / INDEPENDENT_REVIEW / PUBLIC_RELEASE / HOST_E2E`, 기존 디버깅 수정분 적용 상태, ZIP SHA-256/bytes, 신규 ID의 Catalog→Registry→Queue→Run ID→Worker→Receipt→MCP readback 정합성, 최초 실패 단계, 미검증과 다음 한 동작. 호스트 로그/사내 코드/토큰·개인키는 외부 게시하지 말 것.
