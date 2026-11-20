# 저사양 LLM 지식 추출·라이선스·MSC 호환 검토 및 개발 후보 QA — r0001

- 2026-11-21 KST / 기존 Work `L1-WORKSPACE-RAG-20261111-001` / GPT 직접 정적 검토·합성 시험
- **범위**: `NR L1 Tx → UL Tx Switching` 대표 사례의 Module·Feature·Scenario 분류 신뢰성, Code Analyzer→Knowledge Updater→doc-converter 연계. Viewer·MCP 구현·그룹 Knowledge 게시·운영 설치 제외.

## 판정

| 게이트 | 상태 | 근거와 주의 |
|---|---|---|
| 저사양 LLM 적합성 | CONDITIONAL_DESIGN_PASS | LLM은 단일 Feature/Scenario 분류·설명, 탐색·근거 추출/길이 제한은 결정형 Python·기존 Code Analyzer. **호스트 모델 호출·메모리 실측 NOT_RUN** |
| OSS·논문 방법 차용 | LICENSE_IDEA_REUSE_LOW_RISK | Agentless MIT, LocAgent/RepoAgent/RepoGraph/Aider Apache-2.0, GraphRAG MIT, tree-sitter MIT, scip-clang Apache-2.0 원 LICENSE 확인. 제3자 소스/바이너리/가중치 복사 0. 실제 코드 복사·배포하면 각 고지와 dependency 별도 확인 |
| CodeQL | EXCLUDE_RUNTIME | 공식 README상 비공개 코드 분석 CLI에 별도 commercial license 필요; 제어/데이터 흐름 **개념**만 참고 |
| RepoAgent C++ 직접 적용 | NOT_SUPPORTED_AS_ASSUMED | 공개 README는 Python 중심; C++ 확장 예고 상태. 도구를 그대로 쓰지 않음 |
| Code-based MSC | CONDITIONAL_DESIGN_PASS | 기존 Analyzer가 source fact, Converter가 canonical Scenario IR→PUML/SVG/B형 HTML 담당. 입력 필드·branch reachability·호출 순서·source revision G0/E2E 미검증 |
| 신규 독립 결정형 후보 | SELF_TEST_PASS | 합성 12개 Python unittest, ZIP CRC/manifest·원본 해시, 두 번 빌드 byte-identical |
| 실제 Updater 스킬 수정 | NOT_RUN_BLOCKED_G0 | 설치 원본·writer/skill 계약 직접 접근 불가. 새 helper는 실제 Updater/Analyzer/Converter 수정 아님 |
| independent review / host E2E | NOT_RUN / NOT_RUN | 결론을 운영 PASS로 승격하지 않음 |

## 이번 범위에서 만든 개발 후보

- 산출물: `knowledge_analysis_preflight_v0_1_0_1121.zip` (Python 3.10+ 목표, 표준 라이브러리 기반; **developer helper, development_not_for_deployment**).
- **고정 최종 ZIP**: 15,379 bytes, SHA-256 `e307358cb9b6b9bfe0a8c3a1306ceca743ec09549e5ef53de5a879cc4e9ba865`, Git blob expected `f77cc18b7373af12e2b0ec9e68af9b7c7aa0c02d`, ZIP entries 10 / manifest-indexed 9 / CRC PASS, reproducible second build identical.
- 내용: `preflight.py` (규모 제한 evidence context + scenario anchor/revision preflight), README, 독립 작성 원칙/라이선스 검토·저사양 2단계 프롬프트, **합성** 예시/12개 unittest, manifest, 결과 보고.
- **중요**: `preflight.py`의 입력은 독립 synthetic normalization schema, 출력은 **doc-converter canonical Scenario IR 아님**. 검증 통과는 `EVIDENCE_LINKED_NOT_EXECUTION_VERIFIED`로만 보고, `may_invoke_doc_converter=false`, `may_publish_knowledge=false`. 실행 가능한 실제 call order, branch feasible path, IPC 메시지 완성도를 증명하지 않음.
- ZIP은 본 GPT 대화의 sandbox artifact로 생성·검증. **이 문서 게시 자체는 ZIP을 GitHub PRIVATE/PUBLIC에 업로드하는 행위가 아님**. 별도 이진 바이트 게시/원격 SHA 검증 전 `ZIP_REMOTE_POSTED=NO`.
- 실제 데이터·고객자료·토큰·회사 코드 반출 0.

## 최소 구현 방향

1. 기존 `code-analyzer`의 실제 설치 반환 CODE FACT·call tree / source pin 및 updater 기존 지식 분류·Workspace writer와 실제 입력/출력 형식 확인.
2. 파일→함수→조건/상태/IPC 경로 계층 검색을 **기존 분석기를 재사용**. LLM 1회에 단일 Feature·Scenario 근거 묶음만, context truncation은 누락으로 표시·requery.
3. Module/Feature의 Procedure 관계와 scenario 입력 이벤트·조건·상태·실제 적용/해제 경로를 **fact anchor/commit**로 검증. LLM의 자기 설명만으로 Knowledge 반영하지 않음.
4. **Converter native IR, SOURCE_PARENT_DIR_V1, stack_group, participant 별칭, PROCEDURE_FEATURE/ISSUE mode, SVG 성공 및 B형 HTML 조건을 실제 설치본과 대조**. 시나리오 JSON→Converter의 임의 가상 API 생성 금지.
5. 같은 소스 revision·기준 시나리오에서 classification 정밀도/근거 오류/MSC 재현성·토큰/시간을 before-after 검증. 실제 `l1-workspace` writer·readback과 그룹 게시 승인·CAS는 별도 게이트.

## 배포 판정

- PRIVATE 비민감 **검토 결과 기록**: 게시 가능.
- 독립 후보 ZIP: 로컬 생성·검증 PASS. 실 Updater 연결되지 않았고 독립 코드 리뷰와 호스트 계약이 미확인 → **PUBLIC 최종 스킬 ZIP 배포 차단**, 기존 스킬 삭제·교체 없음.
- Windows Claude Code 독립 리뷰(명시적 사용자 승인/기존 규칙 필요 시)·G0 실증 후 기존 스킬에 필수 변경만 최소 통합. 이미 검증된 기존 근거와 동일 Work 재사용.
- NEXT_ONE_ACTION: 업무 GPT/허용 Linux Agent가 `NR L1 Tx UL Tx Switching` 1건에 대해 설치 Updater/Analyzer/Converter 인터페이스를 G0 READ_ONLY 확인해 REUSE/CONNECT/증명된 GAP과 기존 MSC 증빙 1개를 반환.

## 외부 출처(코드 사용 아님)

- [Agentless MIT](https://github.com/OpenAutoCoder/Agentless/blob/main/LICENSE)
- [LocAgent Apache-2.0](https://github.com/gersteinlab/LocAgent/blob/master/LICENSE)
- [RepoAgent Apache-2.0](https://github.com/OpenBMB/RepoAgent/blob/main/LICENSE)
- [RepoGraph Apache-2.0](https://github.com/ozyyshr/RepoGraph/blob/main/LICENSE)
- [Aider Apache-2.0](https://github.com/Aider-AI/aider/blob/main/LICENSE.txt)
- [GraphRAG MIT](https://github.com/microsoft/graphrag/blob/main/LICENSE)
- [Tree-sitter MIT](https://github.com/tree-sitter/tree-sitter/blob/master/LICENSE)
- [CodeQL 비공개 코드 상용 라이선스 경고](https://github.com/github/codeql/blob/main/README.md)
