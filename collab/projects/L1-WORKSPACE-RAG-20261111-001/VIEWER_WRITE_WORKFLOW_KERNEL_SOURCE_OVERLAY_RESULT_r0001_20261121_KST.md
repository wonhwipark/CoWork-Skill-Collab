# Viewer Write × Workflow/Kernel 코드 보완 — 개발 소스 Overlay 결과 r0001

- 일자: 2026-11-21 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 성격: **실제 개발 소스·합성 시험 완료 / SOURCE_OVERLAY_ONLY / DEVELOPMENT_NOT_FOR_DEPLOYMENT**. 실제 업무 Linux Viewer·Workflow·Kernel 설치/통합·운영 Write 활성화 검증 아님.
- 사용자 요청: "위에서 이야기한 두 스킬 수정 필요한 부분 수정해줘." 기존 원장/Writer 기능 중복 구현을 피하고 Viewer 연결에서 확인된 계약 격차를 좁게 보완.

## 1. 기존 최신 공개본 확인

| 스킬 | L1Work/main 정확한 원본 | 패키지 SHA-256 | 원격 byte 확인 |
|---|---|---|---|
| `l1-fix-workflow` | `l1-fix-workflow_v1_6_74_1119.zip` | `b810ce0cf072609431737c58b0ef2b7a0a8ec0701a0746e6a94283c374224989` | GitHub connector 원본 ZIP base64·entry/DEFLATE 내용 확인 |
| `work-ledger-kernel` | `work-ledger-kernel_v0_7_42_1116.zip` | `ece2bce143ef35a1c8cc3bc12ddf6a73e27e0f218fc69fec87844759d9dfc164` | GitHub connector 원본 ZIP base64·entry/DEFLATE 내용 확인 |

**확인된 재사용 기능:** Workflow의 `discussion-draft`·`discussion-capture`와 기존 Work 재개, Kernel의 Work/Evidence·논의 초안·SHA/읽기 및 기존 export. 기존 Kernel export·MSC_VIEW 읽기를 canonical 문서 편집 writer 지원으로 오인하지 않음. 두 공개 ZIP을 업무 Linux 설치본이라고 간주하지 않음.

## 2. 개발한 최소 코드

| 영역 | 실제 개발 파일(overlay 상대 경로) | 동작·경계 |
|---|---|---|
| Workflow | `overlay/l1-fix-workflow/l1_fix_workflow/viewer_write_route.py` | Viewer 요청을 서버에서 확인된 Work/document ID·revision·SHA에 매칭하고 Knowledge owner·잘못된 경로·추정 ID 거부. 승인·저장은 수행하지 않음 |
| Kernel | `overlay/work-ledger-kernel/work_ledger_kernel/viewer_write_guard.py` | PREVIEW/DRAFT/COMMIT 서버 ACL·source revision 검사, **검증된 외부 CAS writer** 1회 위임 및 영수증+readback hash 검증, 불확실 write 재시도 0. 인증/실제 원본 수정·새 원장/DB 구현 아님 |
| 연결/전달 | `tools/apply_to_verified_originals.py` | 정확한 공개 원본 ZIP SHA·CRC·경로/symlink/중복/버전·overlay 충돌 검사 후 **격리 소스 스테이징**. 기존 VERSION·manifest·ZIP/운영 설치 불변 |

- **새로운 Worker/API/Writer 자동 등록 0**. Host의 검증된 세션/ACL/CSRF/lock·CAS·writer/readback을 요구하며 실제 Linux G0에 따라 CONNECT만 수행.
- 개발 후보 ZIP: **`viewer-write-workflow-kernel-code-overlay_v0_1_0_1121.zip`**, 14,379 B, SHA-256 **`61c47515e7ddea8b35e2f1934ee51c8845c69ff42069046cb2fda30ab9b45669`**, 9 entries/CRC PASS. **현 GPT 대화 첨부로 제공**, L1Work/CoWork GitHub 바이너리 게시 **NOT_POSTED**. 정식 스킬 버전 `v1.6.75`/`v0.7.43` 발행이라고 주장하지 않음.
- 실제 전체 스킬 ZIP은 두 최신 원본이 현 GPT 컨테이너에 없고 GitHub 텍스트 커넥터가 바이너리 직접 로컬 전달을 지원하지 않아 **ASSEMBLED_FULL_ZIP=NOT_RUN**. 전체 regression은 업무 Linux의 정확한 원본과 결합 후 실행 필요.

## 3. 직접 실행 시험·판정

- `test_viewer_write_route_v1675.py`: 8/8 PASS.
- `test_viewer_write_guard_v0743.py`: 13/13 PASS.
- `tests/test_cross_bridge.py`: Work route→CAS callback/ACL denial/stale/request mismatch **4/4 PASS** (합성 callback, 실제 Kernel writer 아님).
- `tools/test_stage.py`: synthetic original ZIP 통과·SHA pin 불일치·path traversal·root mismatch·overlay 충돌 **5/5 PASS**.
- `compileall`: PASS; Overlay ZIP CRC 9/9 PASS; **합계 신규 단위·합성 시험 30/30 PASS**.
- `EXISTING_SKILL_SUITE/LINUX_G0/CAS_REAL_WRITE/B1_B2_B3/E3_E4/INSTALLED_SKILL_INTEGRATION/INDEPENDENT_REVIEW/HOST_DEPLOY=NOT_RUN`.
- 기술 결론: 두 스킬 **Write 연결 코드의 최소 후보 개발 PASS**, 기존 스킬 메인 코드/CLI 설치용 통합/새 전체 ZIP은 아직 NOT_RUN. 운영 Write ON 불허.

## 4. 업무 GPT 전달과 다음 한 동작

기존 <https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_WORKFLOW_KERNEL_E2E_ONESHOT_HANDOFF_r0002_20261121_KST.md>에 따라 업무 GPT가 허용된 업무 Linux Agent/실행 LLM으로:
1. 현장 설치본과 실제 writer/canonical Work/edit ACL 계약 G0 및 정확한 공개 SHA PIN 원본을 확인.
2. 본 개발 Overlay ZIP 소스의 두 신설 모듈을 **기존 스킬 파일을 덮어쓰지 않는 격리 staging**에 연결하고 신규 시험+기존 전체 시험.
3. 기존 native 스킬 packaging·manifest/SHA/CRC/권한/릴리스 게이트, 실제 Linux Writer·B1~B3/E3/E4·롤백 검증 후 승인 범위에서만 적용.
4. 실제 저장/Evidence/hash/readback 결과를 동일 업무 Work에 보존, 비민감 판정만 공유.

**다음 한 행동:** 업무 GPT/Linux Agent가 실제 설치본의 `l1-fix-workflow`/Kernel writer·Work 개정 API를 G0 확인하여 재사용 가능한 API에 이 신설 모듈을 연결하고 본래 스킬 회귀/E2E 수행. 전체 스킬 변경본·운영 설치/Write 활성화는 별도 판단.
