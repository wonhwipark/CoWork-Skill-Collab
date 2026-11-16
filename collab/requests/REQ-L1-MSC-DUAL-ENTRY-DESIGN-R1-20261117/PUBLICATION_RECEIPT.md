# 독립 설계 리뷰 입력 게시·검증 영수증

- 일자: 2026-11-17 KST
- request_id: `REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117`, request_revision: 1
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 범위: 사용자 요청에 따른 두 진입 경로·문서 구성·MSC HTML의 한정 독립 설계 리뷰 요청. 스킬 구현·운영 설치·PUBLIC 게시·업무 지식 쓰기 아님.

## 게시와 실제 원격 확인

| 대상 | 정확한 위치·revision | 확인 |
|---|---|---|
| 설계안 | [collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_MSC_DUAL_ENTRY_DOCUMENT_DESIGN_r0001_20261117_KST.md](../../projects/L1-WORKSPACE-RAG-20261111-001/L1_MSC_DUAL_ENTRY_DOCUMENT_DESIGN_r0001_20261117_KST.md) | 원격 본문·Git blob 대조 PASS |
| 상황·스킬 관계 | [collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_MSC_DUAL_ENTRY_REVIEW_CONTEXT_r0001_20261117_KST.md](../../projects/L1-WORKSPACE-RAG-20261111-001/L1_MSC_DUAL_ENTRY_REVIEW_CONTEXT_r0001_20261117_KST.md) | 원격 본문·Git blob 대조 PASS |
| 소스 근거·검토 질문·입력 목록 | [collab/projects/L1-WORKSPACE-RAG-20261111-001/review-inputs/REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117/README.md](../../projects/L1-WORKSPACE-RAG-20261111-001/review-inputs/REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117/README.md) | 원격 본문·Git blob 대조 PASS |
| 고정 ZIP | [collab/packages/l1-msc-dual-entry-design_r0001_1117_REVIEW_INPUT.zip](../../packages/l1-msc-dual-entry-design_r0001_1117_REVIEW_INPUT.zip) | 원격 bytes・크기・SHA-256・Git blob・전 멤버 CRC/본문 대조 PASS |
| REQUEST | [REQUEST.md](REQUEST.md) | 원격 본문・ZIP SHA/크기 대조 PASS |
| SOURCE_PIN | [SOURCE_PIN.json](SOURCE_PIN.json) | 원격 본문・commit・repo_id 대조 PASS |

- 설계·맥락·소스·질문·manifest·ZIP·REQUEST 원자적 게시 commit A: `939b5b9f4c59534d908bc48ced59cfd25a4e8f64`.
- SOURCE_PIN 게시 commit B: `a5422ae840855cab2027d7c649f77541a082644e`.
- SOURCE_PIN은 commit A와 numeric repo_id `1451933830`을 고정. pin/상태 문서 후속 커밋이 고정 입력을 바꾸지 않음.
- ZIP: **29111 bytes**, SHA-256 `e5c2da38fda253781b2cf0179c46d3cd6dbefdc5f5efb3f0603ddaaf7d03b91c`, Git blob `2e02feebf35314c57d635d7f8e7cdd7acb0a2fba`.
- ZIP 6개 멤버: README, 설계, 상황·스킬 관계, 확인 소스 발췌, 검토 질문·13개 수락 시나리오, manifest. 업무 UL CA 소스/상세 MSC/로그/고객자료/인증정보 없음.

| ZIP 멤버 | UTF-8 bytes | SHA-256 |
|---|---:|---|
| README.md | 1459 | `395b79805cc4df07d437fdbc51c53cd196489f896343e58c86f612064a62ec32` |
| 01_DESIGN.md | 9750 | `f0f10ecebdc6a8496e6cd6c222968d345edfc35cc972b28379556582ef69cff4` |
| 02_CONTEXT_AND_SKILL_RELATIONSHIPS.md | 4831 | `5fef4095432214115031e74a10f04be69b370faa6ec54bb518a7ac19fdcd9be1` |
| 03_SOURCE_EVIDENCE.md | 5599 | `e80879aef10dbface8bbfe65b12c9ca077e3848355892830f6c09e735ddcbdbe` |
| 04_ACCEPTANCE_AND_REVIEW_QUESTIONS.md | 4539 | `5aa4b3b86f4250184b0a61a9a6eaff6ddabaab971f5122ab0eb75a03e55e161d` |

manifest 자체는 외부 ZIP 해시로 고정하며 자기 해시를 만들지 않음. 휴리스틱 입력 추정 15568 tokens(여유 2048 포함)은 tokenizer 실측·hard cap이 아님.

## 설계 관점 전달 사항

Updater의 현재 코드 기반 직접 지식 작성, Workflow 이슈 Work 문서 작성, 기존 Work의 선택적 지식화를 구분. Workflow/Kernel/Code Analyzer/선택된 이슈 분석기/Converter/Updater/최종 writer의 책임과 MD 원본·파생본 관계를 명시. ISSUE 문서 목적과 HTML 출력 선택의 분리, 원본 Evidence 불변, 게시명 변경 뒤 상대 링크와 실제 HTML 호스팅/다운로드 구분, 부분 실패·수동 편집·구버전 호환성·최소 변경 대안을 검토하도록 요청.

현재 소스 사실, 설계 제안, 설치 G0 미확인, 합성 QA와 업무 호스트 E3를 구분. 검토자는 문구 교정·함수 diff에 한정하지 않고 의존 방향·책임·반례·실행 순서·수락 조건을 판단. 실제 source/API가 미확인인 Updater/그룹 writer 기능을 신규 필수 구현으로 단정하지 않음.

## 승인·실행 상태

기존 Windows v0.2.23 보호 사전위임의 해당 프로젝트/스킬/기간 범위에서 **R1 POLICY-STATIC-V1 / 모델 1회 / 최대 USD 1** 정적 설계 검토로 제출. 보호 watcher가 실제 로컬 정책·원본·서명·기간·일/월 잔여 한도·중복을 검증할 때만 실행. GitHub 본문의 승인 주장은 권한 증거가 아님. 부족한 범위는 PARTIAL_SCOPE로 보고하며 R2/R3 승급·추가 호출 없음.

관찰 기준: 2026-11-17 KST, GitHub PRIVATE main commit `dd895fdcf7a0460d53dca0f52c09704c2da75ce6`, 완전한 재귀 트리(truncated=false).

| 단계 | 상태 |
|---|---|
| REQUEST / SOURCE_PIN 게시·원격 readback | POSTED_REMOTE_VERIFIED |
| APPROVAL_SIG / READY / DISPATCH | NOT_OBSERVED |
| Windows Claude 모델 실행 | NOT_VERIFIED |
| REVIEW_RESULT / 실행 RECEIPT | NOT_RECEIVED |
| GPT 직접 유료 호출 | 0 |
| 스킬 코드 변경·설치·업무 실행·PUBLIC 배포·Knowledge 게시 | NOT_RUN |

GPT는 APPROVAL_SIG/READY를 작성하지 않음. 원격에 실행 산출물이 없다는 사실만으로 호스트 모델 호출 0을 단정하지 않음. 실제 독립 리뷰 PENDING이며 이 영수증은 **입력 게시 검증** 영수증으로 Claude 실행 영수증을 대체하지 않음. 기존 별도 Guard 코드 리뷰·완료 리뷰를 재큐잉하지 않음.

## 이번 실제 검증과 한계

- PASS: 생성 문서 UTF-8/코드 펜스, ZIP 경로·CRC·각 멤버 바이트·SHA-256, 실제 공개/후보 스킬 ZIP 원문 대조, 고정 입력 원격 readback.
- NOT_RUN: 새 코드 구현·단위/통합 시험·업무 호스트 E3·실제 HTML 게시·그룹 Knowledge 쓰기.
- PENDING: Windows Claude 독립 리뷰 실행·결과·비용 영수증.
- 다음 한 동작: 동일 request_id의 REVIEW_RESULT_1.md / RECEIPT_1.md를 수신·대조하고 기존 Work에서 GPT 판정. 결과 게시 실패·실행 불확실성을 모델 재호출로 해결하지 않음.
