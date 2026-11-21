# CoWork — 병렬 대화창·개발 작업 통합 게이트 V1

- 2026-11-21 KST. 적용 대상: 동일 Work/단일 배포 산출물에 여러 대화창, GPT, Agent가 기여하는 개발.
- 검사 코드: `collab/ops/integration_gate.py`; 시험: `collab/ops/tests/test_integration_gate.py`.
- GitHub 계약·읽기 전용 사전검사 도구임. **호스트 자동 설치, 모든 릴리스 자동 차단, GitHub Actions 자동 재시작을 의미하지 않음**.
- 기존 리뷰 REQUEST/PIN/승인·READY, ZIP 무결성, 보안 및 운영 설치 게이트와 별개임.

## 1. 병렬 개발 계약

1. 새 창은 공통 브리프 → 해당 `CURRENT.md` → 최신 원본·통합 상태·관련 열린 메모를 확인한다.
2. **동일 산출물을 수정하는 모든 창은 기존 Work와 하나의 통합 대상 ID를 재사용**한다. UI, Write, Preferences는 같은 Viewer Work 안에서 별도 stream으로 등록한다. 새 목적만 신규 Work로 구분한다.
3. 각 작업 시작 시 해당 Work에 stream_id, base revision, 변경 예정 파일·산출물 범위를 기록하고, 종료 시 검증 가능한 소스 ZIP, SHA256, 필수 엔트리별 SHA256과 실제 자체시험을 등록한다. 등록 누락 작업은 자동 발견 불가하므로 작업 시작 시 등록을 필수로 한다.
4. 동일 Work의 등록된 모든 stream을 한 번에 조회해 **단일 통합 ZIP**을 만든다. 파일 중복 수정은 단순 덮어쓰기를 허용하지 않는다. 의미적 병합과 별도 교차 기능 시험 근거가 필요하다.
5. 통합 최종 판정 전 원격 main 재조회, 고정 원본 revision, 각 ZIP 내용·해시·중복/경로 이탈, 모든 stream 포함, 회귀 및 교차 시험을 검사한다. 원격 SHA가 달라졌으면 재검토·재시험한다.
6. 게시 주체는 직전 검증된 HEAD를 기준으로 가급적 예상 HEAD CAS(ref compare-and-swap) 게시를 수행한다. 검사와 게시 사이 레이스를 줄이는 수단으로, 정식 게시자에게도 검사를 연결해야 함.
7. 결과가 `INTEGRATION_BLOCKED` 또는 시험 미실행이면 최종 통합 완료·운영 배포 판정 보류. 개발 후보 기록은 가능하며 PASS로 승격하지 않는다.

## 2. 등록 데이터의 위치와 형식

기존 Work의 `integration/streams/<stream_id>.json`을 등록 정본으로 재사용하고, 게시 전 스테이징 폴더에 해당 JSON 전부와 소스 ZIP·통합 ZIP·시험 근거를 둔다. 전체 Work를 중복 등록하거나 새 중앙 원장·DB를 만들지 않는다. 스테이징 경로는 Work 아래여도 되지만, 검사를 실행할 로컬 git checkout은 깨끗해야 한다. 공개 가능한 비민감 자료만 등록한다.

UI stream 예시 (자리 표시자를 실제 고정 SHA로 바꾸어 사용):

```json
{
  "schema": "COWORK_INTEGRATION_STREAM_V1",
  "work_id": "L1-WORKSPACE-RAG-20261111-001",
  "stream_id": "UI",
  "artifact": {"path": "ui.zip", "sha256": "<actual 64-char SHA256>"},
  "required_entries": {"viewer/ui.css": "<actual 64-char entry SHA256>"}
}
```

스테이징 `integration.json`:

```json
{
  "schema": "COWORK_INTEGRATION_GATE_V1",
  "work_id": "L1-WORKSPACE-RAG-20261111-001",
  "branch": "main",
  "source_base_sha": "<actual 40-char original commit>",
  "mode": "development_candidate",
  "candidate": {"path": "viewer-integrated.zip", "sha256": "<actual SHA256>"},
  "included_streams": ["UI", "Write"],
  "merge_resolutions": [],
  "checks": [
    {"type": "regression", "status": "PASS", "covers": ["UI", "Write"], "evidence": {"path": "regression.txt", "sha256": "<actual SHA256>"}},
    {"type": "cross_stream", "status": "PASS", "covers": ["UI", "Write"], "evidence": {"path": "integration.txt", "sha256": "<actual SHA256>"}}
  ]
}
```

같은 ZIP 엔트리를 여러 stream이 다르게 수정했다면 `merge_resolutions`에 아래 기록. 이 근거만으로 의미적 정확성을 보장하지 않는다:

```json
{
  "entry": "viewer/README.txt",
  "streams": ["UI", "Write"],
  "evidence": {"path": "merge-review.txt", "sha256": "<actual SHA256>"}
}
```

통합본의 해당 엔트리 SHA는 각 충돌 소스와 달라야 한다.

## 3. 검사 실행 및 판정

```sh
HEAD=$(git -C /path/to/cowork rev-parse HEAD)
python3 /path/to/cowork/collab/ops/integration_gate.py \
  --repo-root /path/to/cowork \
  --work-dir /path/to/staging \
  --branch main --remote origin --expected-head "$HEAD"
```

`--expected-head`는 현재 원격 main에서 실제 확인한 SHA를 고정한 값. 검사는 로컬/원격 HEAD가 그 값과 모두 같은지 확인한다. 이 SHA를 같은 commit에 포함된 manifest 안에 쓰면 자기 참조 문제가 있으므로 **명령 인자로 전달**한다. base revision은 `source_base_sha`로 전달해 commit ancestry 확인.

- 성공: 종료 0 + `INTEGRATION_PRECHECK_PASS` = 그 시점의 단일 패키지 구성·검사 증거 사전 확인. 실제 기능 동작을 자동 보증하지 않음.
- 차단: 종료 2 + `INTEGRATION_BLOCKED` = 누락/불일치/미확인, 배포 판정 금지.
- development_candidate에도 regression과 모든 stream을 포괄하는 cross_stream PASS 증거를 요구한다.
- deployment 모드는 security 및 host_e2e PASS 증거를 추가로 요구한다. **`deployment_approved=false`는 언제나 유지**하며 리뷰 승인·최종 배포/운영 승인·실제 Linux 적용은 별도.
- 실제 Linux/Windows 접근이 안 되면 해당 검사는 NOT_RUN. synthetic PASS를 대신 제시하지 않는다.

## 4. 적용 범위와 남은 강제화

- 보장 범위: **등록된** 모든 stream, 각 소스 ZIP SHA 및 필수 엔트리, 단일 ZIP, 중복·경로 이탈·zip 손상, 겹치는 파일 미해결, 시험 근거 SHA·커버리지, 깨끗한 checkout, 로컬·원격 HEAD.
- 미보장: 아예 등록하지 않은 다른 창 작업, 서로 다른 Work에 숨은 종속성, UI 의미적 호환성, 직접 GitHub 편집/업로드로 사전검사 우회, 사전검사 이후 게시까지의 시간차, 실호스트 설치·쓰기 기능.
- 이전 사용자 요청에 따라 자동 Actions 검증은 중지 상태를 유지한다. 각 게시 주체가 **발행 직전에** 이 코드를 직접 호출하도록 연결하고 실제 2개 대화창의 교차 등록/배포 시험을 해야 시스템 전역의 기술적 차단이라고 말할 수 있다.
- 기존 Viewer 통합 v0.4.0은 개발 후보. 본 계약 게시 자체는 이미 배포한 ZIP이나 Linux Viewer E2E를 소급 통과시키지 않는다.
