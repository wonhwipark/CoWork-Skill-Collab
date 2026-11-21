# Viewer Write × Workflow/Kernel — 전체 스킬 개발 패키지 생성·L1Work 배송 검증

- 작성: 2026-11-21 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 승인 범위: 기존 두 스킬 실제 코드 수정·전체 ZIP 패키징·L1Work PUBLIC 업로드 및 정본 인계. Linux 운영 설치·계정/키/DB/서비스 변경·실쓰기 활성화·새 유료 독립 리뷰 승인 아님.
- **최종 판정:** `PUBLIC_DEVELOPMENT_FULL_ZIPS_DELIVERY=PASS_REMOTE_VERIFIED`, `DEVELOPMENT_NOT_FOR_DEPLOYMENT`, `LINUX_HOST_E2E=NOT_RUN`, `INDEPENDENT_CODE_REVIEW=NOT_RUN`.

## 1. 실제 정본 ZIP 전달

| 스킬 | 기준 원본 → 신규 후보 | size | SHA-256 | GitHub blob |
|---|---|---:|---|---|
| `l1-fix-workflow` | `l1-fix-workflow_v1_6_74_1119.zip` → **`l1-fix-workflow_v1_6_75_1121.zip`** | **832,039 B** | `fd337ee31e09c9f694146c9d159799ca7182af052c93121e73888a9ee367a0a1` | `2a75b0ad3108a02e0374706b739b1b7973f17568` |
| `work-ledger-kernel` | `work-ledger-kernel_v0_7_42_1116.zip` → **`work-ledger-kernel_v0_7_43_1121.zip`** | **379,642 B** | `9866ff7164884b0fb346bd31d37dbdf2013b5e5910e5857f8e35075624cf92f1` | `a8554d559b46d7292a4add98552c6821d55ac8af` |

- **업로드 저장소/브랜치:** GitHub PUBLIC `wonhwipark/L1Work` / `main` / 위 파일 두 개 모두 **루트**.
- **동일 commit:** `fe869519e588a56e2282fbbd854cfed83bf8ad64`.
- Github 원격 bytes GET Base64 전체 SHA-256/크기/Git blob readback **2/2 PASS**. 원본 전체 311/163 항목 검증 후 새 전체 ZIP **315/166 entries**, 314/165 manifest-covered items CRC/SHA 검사 **PASS**. 기존 ZIP 바이트/상대경로/기존 Work 원본 보존.
- 패키지 내 `VERSION`, `pyproject.toml`, `SKILL.md`, `README.md`, `.skill-release.json`, `MANIFEST_SHA256.json` 및 Workflow release note, Kernel CHANGELOG에 신규 버전·기능/게이트를 반영. **release_kind=development_not_for_deployment**, `independent_code_review=NOT_RUN`.
- 배포 안내: [L1Work 업무 GPT 최종 HO r0003](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_WRITE_WORKFLOW_KERNEL_FULL_SKILLS_HANDOFF_r0003_20261121_KST.md) / L1Work `handoffs/README.md` 최신 색인, 두 문서 POSTED/READBACK PASS. 기존 r0001/r0002 HO 불변.

## 2. 실제 코드 추가

| 스킬 | 새 코드·테스트 | 신규 책임·제약 |
|---|---|---|
| Workflow | `l1_fix_workflow/viewer_write_route.py`, `tests/test_viewer_write_route_v1675.py` | 서버 canonical Work/document/source revision/SHA와 Viewer 요청을 read-only로 확인하고 Knowledge owner·불일치·비편집 대상 거부. 저장/인증/Work 생성 아님 |
| Kernel | `work_ledger_kernel/viewer_write_guard.py`, `tests/test_viewer_write_guard_v0743.py` | 서버 ACL/source 재검사, 검증된 **기존 CAS writer callback**에 1회 위임, receipt+readback 확인, WRITE_UNCERTAIN 재시도 0. 실 writer/보안 인증 시스템을 새로 구현하거나 자동 등록하지 않음 |
| 양쪽 | `docs/VIEWER_WRITE_SAFE_CONNECT_V1.md`, SKILL·README 관련 설명 | 기존 Viewer Read Only, 기존 원장·Workflow CLI 유지, 실제 G0/B1·B2·B3/EAuth/E3/E4/롤백 이후에만 host 연결 |

업무 Viewer's `L1ViewerWriteHostAdapter`는 합성 프런트 계약이고 실제 서버 API로 입증되지 않음. 두 스킬의 추가 helper는 **설치 즉시 동작하는 완성된 Write backend가 아님**. 이 제한을 개발 릴리스 메타와 문서에 명시.

## 3. 실제 시험·미검증

| 범위 | 결과 |
|---|---|
| 신규 Workflow 단위시험 | **8/8 PASS** (로컬 신규 overlay 원본 Python) |
| 신규 Kernel 단위시험 | **13/13 PASS** |
| Workflow→Kernel 연계 합성시험 | **4/4 PASS** |
| Overlay 격리 staging 안전시험 | **5/5 PASS** |
| ZIP 빌더 자체 재구성 ZIP Python `zipfile.testzip()` 및 해시/CRC 일치 검증 | **PASS** (격리 synthetic archive) |
| 신규 실제 전체 ZIP GitHub Base64 원격 readback 및 전 멤버 SHA/CRC/manifest 검증 | **PASS** |
| 실제 전체 기존 Workflow/Kernel 테스트 suite | **NOT_RUN** (업무 Linux 설치·기존 원본 로컬 복원/테스트 환경 미확인) |
| Linux Viewer Write→실 writer/CAS/Evidence→readback E2E | **NOT_RUN** |
| B1/B2/B3/EAuth/E3/E4/운영 설치 | **NOT_RUN** |
| 새로운 코드 독립 리뷰 | **NOT_RUN** (기존 설계 리뷰 결과로 대체하지 않음) |

**역할 분리:** 새 전체 패키지 원격 게시/무결성 PASS ≠ 운영 배포 게이트 PASS ≠ 업무 GPT 수신/실행 확인.

## 4. 미해결·다음 한 동작

- 실 Linux에 설치된 `l1-fix-workflow`/`work-ledger-kernel` 버전·활성 runner, Viewer writer/인증·CAS·canonical anchor G0 미확인. 실제 설치본이 새 공개본보다 변경됐거나 정책 제한이 있으면 덮어쓰기 금지.
- `work-ledger-kernel` 기존 Work/Evidence 보존과 새로운 수정 요청 승인 경로를 실제 writer에 CONNECT하고, source revision/actor/session/CSRF/ACL/중복보호·충돌/복구·readback을 호스트에서 확인해야 Write 활성화 후보가 됨.
- **NEXT_ONE_ACTION:** 업무 GPT가 [최신 HO r0003](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_WRITE_WORKFLOW_KERNEL_FULL_SKILLS_HANDOFF_r0003_20261121_KST.md)와 2개 고정 SHA 전체 개발 ZIP을 입력으로 실제 설치본 G0→전체 회귀→범위 내 최소 연결/E2E→게이트 판정을 진행. 게시만으로 Linux Job을 자동 실행하지 않음.
