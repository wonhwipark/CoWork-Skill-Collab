# K5.8/K6 r0005 — 범위 명확화·문서 게시 검증 기록

- Date: 2026-11-11 KST
- Kind: DOCUMENT_SCOPE_CLARIFICATION / PUBLICATION_READBACK. 독립 리뷰·호스트 시험 영수증이 아님.
- Authorization: 기존 PRIVATE 갱신·PUBLIC handoff 게시 지시를 이어 최신 범위 제한을 문서에 반영. 사내 knowledge/metadata에는 쓰지 않으며 이번 원격 쓰기는 설계·인계·상태 MD만.
- Source: PRIVATE main `8d9f87ed21205dba892d4c332e9468d790d3cde9`의 r0004/CURRENT, PUBLIC main `cf13392bbf02a1d178f1cd3b83348a7321447c07`의 r0004/README 직접 확인. 실제 설치 사실 미확인.

## 원격 검증한 내용

| Repository | Path | UTF-8 bytes | SHA-256 | Git blob SHA | Content commit | Readback |
|---|---|---:|---|---|---|---|
| wonhwipark/L1Work | `handoffs/L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md` | 41825 | `cec3b699b0c6b0e825016007965a512d8d766f14c1eef8977d651fbc0fc22be8` | `bc8f7d3d72fd8275b6ec3d81dee240a9a18c5edf` | `a205efc2d24b93ad6c484273ac57db8af290425d` | PASS |
| wonhwipark/L1Work | `handoffs/README.md` | 1445 | `9b6733774873accab8d5805ad9fa5ee988607b17ff0a63e9d74e7eaa3b27ba8b` | `a57ec793c7c489d4b359e3c6d5caecd2b5fd1161` | `a205efc2d24b93ad6c484273ac57db8af290425d` | PASS |
| wonhwipark/CoWork-Skill-Collab | `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0005_20261111.md` | 38154 | `0c71c8825a0dd662705e4f14f0e58e0b0ff2acf98fa414b7459e4bdae480734f` | `9a8339abd493afa4119445228a843e95ad1f8f8f` | `75153a2975aa7bbce15add4b8683bd8f122a14ea` | PASS |

검증 방법: 실제 작성 UTF-8 bytes로 SHA-256·Git blob SHA 계산 후 main 원문 전체 및 반환 blob과 일치함을 확인. 표는 이미 검증한 content commit을 가리킨다. 이 기록/CURRENT의 metadata commit은 별도 게시 후 readback하며 자기 hash를 미리 확정하지 않는다.

## 범위·보존·검사

- G0 직접 설치 사실/미확인과 G1 가정은 별도 표. 현재 G0=NOT_RUN, 설치 사실=NONE_CONFIRMED. K5.8 재분류는 Markdown 설계표이며 기존 knowledge/tier/metadata/record/schema/index·Work/Evidence·경로 변경 없음.
- SourceSnapshot/CAS/N:M/복구는 기존 Kernel/Updater/Git 제공자를 먼저 조사·재사용. 미확인 API/record는 ADDITIONAL_CHECK_REQUIRED 또는 BLOCKED, 구현 대상 확정 금지. 실제 gap과 재사용 불가 근거가 있는 최소 범위만 후속 설계 후보.
- PUBLIC 변경은 r0005 handoff 추가·handoffs/README 갱신, 기존 r0004/r0002·ZIP 보존. PRIVATE content 변경은 r0005 계약 추가이며 기존 계약/리뷰·collab/knowledge 보존.
- DOCUMENT_STATIC_QA=PASS: UTF-8/LF/newline/fence, G0/G1 분리·무쓰기·기존 기능 우선·확인 gap 제한·미확인 API/record 처리, G01~G14/T01~T24·NOT_RUN 게이트, PUBLIC 경로/서비스/credential marker와 내용 검토. 소프트웨어 시험 아님.
- Branch 갱신은 expected head + non-force, PR/REQUEST/READY/모델 호출 없음.
- G0_INSTALL_FACTS=NONE_CONFIRMED / G1_ASSUMPTIONS=PROVISIONAL / INHOUSE_E3=NOT_RUN / TEST_T01_T24=NOT_RUN / EXISTING_KNOWLEDGE_WRITE=NOT_RUN / EXISTING_METADATA_WRITE=NOT_RUN / RAG_M1=BLOCKED / INDEPENDENT_REVIEW=NOT_RUN / SOURCE_PATCH=NOT_RUN / NEW_ENGINE_OR_SCHEMA=DEFER_UNTIL_CONFIRMED_GAP / SKILL_RELEASE=NOT_RUN / LIVE_CUTOVER=NOT_RUN.
- 기존 KR-05/06·G0/M1 블로커는 유지. 사내 다운로드·실제 조사·통합 실행 NOT_RUN. 내부 원문/코드/MSC/로그·상세 결과 사내 보관. MIGRATION_NOT_CUTOVER / DROPBOX_LIVE 유지.

다음 한 동작: 사내 GPT에 PUBLIC r0005를 첨부해 읽기 전용 G0 사실/미확인과 G1 가정·기존 기능 매핑·K5.8 설계표만 작성한다.
