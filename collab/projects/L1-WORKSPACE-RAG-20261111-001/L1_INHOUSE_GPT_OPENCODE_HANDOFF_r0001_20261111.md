# 사내 GPT / OpenCode — L1 지식 설계·스킬 연계 원샷 인계 r0001

- 기준일: 2026-11-11
- 문서 성격: **사내 실행용 설계 인계**; 외부 서비스·저장소 접근이나 외부 업로드를 요구하지 않음
- 실행 수준: `READ_ONLY_G0 + LOCAL_DESIGN / NO_PRODUCTION_WRITE`
- 기존 설치본/소스/지식 정본/운영 Work/DB/예약작업/자동화/LIVE는 별도 승인 전 변경 금지

## 1. 목표

기존 사내 `L1 Knowledge Updater`를 재사용한다. 사용자의 자연어 지식 업데이트를 담당 블록·코드 범위로 해석하고, 분석 결과를 그룹 `L1 Software Dev Knowledge`의 공통 개요와 개인 `L1 Workspace`의 상세 코드 분석/MSC/리뷰 이력으로 **중복 없이 라우팅**한다. 사내 GPT는 정책·설계 조정, OpenCode는 접근 가능한 실제 코드·스킬 분석과 격리 시험을 수행한다. `Workflow + Kernel`의 Work·Evidence 정본 책임을 유지한다.

## 2. 역할

- **사내 GPT**: 이 문서를 기준으로 실제 스킬과 기능을 대조, 기존 구현 우선, 인터페이스 차이·개선 우선순위·시험 계약 정리. 로컬 코드에 접근할 수 없다면 코드를 본 척하지 않는다.
- **OpenCode/사내 Agent**: 인가된 소스/스킬/SCM 도구 실제 상태를 읽기 전용으로 실측, 데이터 범위/근거를 고정, 변경이 허용된 격리 사본에서만 시험.
- **L1 Knowledge Updater**: 지식 업데이트 자연어 요청의 진입점, 질문·범위 확정, 코드/지식 분석 조정, 그룹/개인 저장 후보 분류, 스터디 생성(현재 구현 범위는 확인 필요).
- **l1-github + p4-code-owner + code-analyzer**: Git/P4 대상 고정과 이력/의미 분석 근거. 자동 호출 가능성은 실제 설치·도구 계약으로 확인.
- **Workflow + Kernel**: Work ID·SourceSnapshot·Evidence·Finding 이력 연결의 단일 소유자. 새 리뷰 provider/kind를 운영 레지스트리에 무단 추가하지 않는다.

## 3. 한 번에 진행할 작업 (읽기 전용 중심)

1. 실제 설치본의 `L1 Knowledge Updater`, `L1 Software Dev Knowledge`, `L1 Workspace`, Workflow, Kernel, `code-analyzer`, `l1-github`, `p4-code-owner` 존재/버전/출력 계약, 읽기/쓰기 권한을 **실측**한다. 없는 기능은 `NOT_FOUND/UNKNOWN`으로 표기.
2. Updater 입력 질문(블록/폴더/기능/브랜치), 코드분석 요청, 지식 분류, 스터디 생성, 실제 그룹/개인 저장 방식의 producer→consumer 관계와 side effect를 도식화한다. 사용자 설명과 실제 소스/시험 확인을 구분.
3. 기존 G0 H01–H04 범위의 Kernel Evidence registry, PR review/comment, Analyzer CODE_FACTS/MSC, Jira/P4 API tool 계약을 읽기 전용으로 확인한다. 호출이 데이터를 변경하거나 비용을 발생시킬 수 있으면 `NOT_RUN`.
4. 다음 세 가지 사용 사례를 **문서/합성 시뮬레이션**으로 추적한다. (A) 일반 블록 지식 업데이트, (B) 특정 브랜치 코드 분석 및 AS-IS MSC, (C) 과거 Jira/P4 이슈 원인·수정 검토. 실 데이터 반출·운영 지식 Write 없이 실행 흐름과 누락된 연결만 표기.
5. **저장 경계 결정**: 그룹 공통 HLD/개요는 Knowledge Owner 검토·승인·Git readback이 필요. 개인 상세 분석은 Work/Evidence·SourceSnapshot과 연결. 승인 없이 자동 지식 승격/교차 브랜치 합성/정본 덮어쓰기 금지.
6. MCP 피드백 수신·전송은 **우선 현행 MCP 도구 목록, 통신 가능 방향, 인증·네트워크 정책, 내부 보안 승인/반출 범위**만 확인한다. 없으면 신규 구현 계획으로 기록. 외부 endpoint, 데이터 업로드, 임의 권한 증설 금지.
7. Gap 분석에서 이미 있는 기능은 REUSE, 필요한 연결만 CONNECT, 기존 Kernel 등록 변경·RAG Provider 입력 구현 등은 검증과 승인 전 DEFER/BLOCKED로 분류한다.
8. 변경 설계는 인하우스 요약 MD로 기록하되 실제 코드 수정·운영 설치·배포는 하지 않는다. 추가 개발을 수행할 경우 별도 허용된 격리 개발 범위만 다루고 SELF_TEST / INDEPENDENT_REVIEW를 반드시 구분한다.

## 4. 필수 판정 조건

- 동일 코드 사실: Git full commit/P4 개별 revision 고정. DIRTY/UNKNOWN은 VERIFIED 금지. 타 브랜치 증거 재사용 차단.
- Evidence: 등록된 provider/kind/stage/profile만 기록. 미등록 `code_review`, `issue_review`, `p4-code-owner` 직접 Evidence 슬롯을 있는 것처럼 취급하지 않는다.
- Kernel: `record.json` SSOT와 Work Export 파생 문서 소유권 존중; 임의 리뷰 속성 삽입/새 인덱스 생성 금지.
- RAG: 검색 링크만으로 Provider 본문 소비 PASS 금지. 실제 payload/digest와 권한/소스 매칭 실증 전 `M1=BLOCKED`.
- 지식 업데이트: 기존 그룹 지식과의 중복·충돌 Preview, 권한, 승인, commit/readback 없이 정본 업데이트 금지.
- 데이터 보안: 원본·로그·구체 내부 경로·실 MSC·인증정보·제품 세부 설계는 내부 승인된 저장 위치에만 남긴다.

## 5. 결과 문서 2종 — 사내 원본과 비민감 피드백 분리

**A. 내부 원본 (사내만):** `L1_INHOUSE_INTEGRATION_AUDIT_INTERNAL.md`
- 설치본 provenance, 실제 도구/권한/스키마, Updater input/output, 기존 Knowledge 쓰기 경로, Work/Kernel 등록 슬롯, 증거 ID, 차단 사례 및 회귀시험 계획을 상세히 기록.
- 실제 운영 데이터/내부 경로/CL/commit/원본 코드가 포함될 수 있으므로 외부 전송 금지.

**B. 반출 사전 후보 (승인 전 로컬):** `L1_APPROVED_ABSTRACT_FEEDBACK_CANDIDATE.json`
- 별도 `l1/mcp-feedback/0.1` 계약에 따라 **허용 enum, 상태, 비식별 change ID, 계약 버전만** 채운다.
- `release_decision=NOT_APPROVED`를 기본으로 한다. 내부 보안정책상 허용 여부와 사람의 명시적 승인 전 전송 금지.
- 계약 파일의 예시는 합성 데이터이며 내부 실제 데이터를 임의로 복사하지 않는다.

## 6. 필수 보고 순서

`CURRENT_STATUS` → `REUSED_CAPABILITIES` → `GAPS_AND_OWNERSHIP` → `SELF_TEST_PASS_FAIL_SKIP_NOT_RUN` → `INDEPENDENT_REVIEW` → `EXPORT_POLICY_STATUS` → `NEXT_SINGLE_ACTION`.

이 인계서는 회사 외부 서버·서비스의 실행 지시가 아니다. MCP 구현이 필요해도 내부 보안·운영 책임자 승인 전까지 설계/권한 검토만 수행한다.
