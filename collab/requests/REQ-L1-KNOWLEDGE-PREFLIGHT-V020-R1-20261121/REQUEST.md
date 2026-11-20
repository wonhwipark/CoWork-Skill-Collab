---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: knowledge_analysis_preflight
package_path: /SKILL-COLLAB/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip
package_file_id: github:REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121
package_rev: knowledge-analysis-preflight-v0.2.0-r1
package_sha256: 90a0d55842138d4c813f0dbc3a5c8e4625e84a110afe68035348297ffedad1f3
package_size_bytes: 16138
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [l1-knowledge-updater-offline-evidence-bridge]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent code review for bounded low-resource Module Feature Scenario evidence checker and fail-closed MSC boundary
---

# Knowledge Analysis Preflight v0.2.0 — 독립 코드 리뷰 R1

- **사용자 의도/실행 순서:** 설계 GPT가 기존 Updater에 필요한 저사양 Code Evidence 분류 보조를 독립 구현·시험 → 독립 리뷰·GPT 판정 → 승인된 최종 ZIP을 L1Work PUBLIC 루트에 배포 → **그 후에** Updater 통합 구현 요구서를 업무 GPT에 전달. 이전 업무 GPT 우선 수정 인계는 현재 HOLD.
- **고정 입력:** GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` `main` **commit `84abde50d7c960ca5ec065b392f8aece84bde85d`**에 `collab/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip`, 16138 bytes SHA-256 `90a0d55842138d4c813f0dbc3a5c8e4625e84a110afe68035348297ffedad1f3`, blob SHA `bbacdcfd33860060552ef5928be0f37b6b436cdb`. 실제 원격 base64 payload와 로컬 binary가 일치함을 확인.
- **내용:** 기존 사전검증기 `preflight.py` + 신규 `hierarchy.py`, `SKILL.md`, README, 학습 프롬프트, synthetic examples, `tests`, manifest. Python 3.10+ stdlib. **독립 Helper이지 기존 Updater·Code Analyzer·Converter에 연결/설치된 기능이 아님.**
- **개발자 자체시험:** synthetic regression 38/38 PASS, Python compile PASS, ZIP CRC/manifest SHA/path traversal/bytes PASS, deterministic rebuild PASS. 실업무 C++·저사양 LLM 실행/MSC IR·개인 Workspace writer E2E 모두 NOT_RUN.

## 독립 리뷰 질문

1. `preflight.py`의 schema/path/source revision/size/step/malformed input 검증이 fail-closed인지, `hierarchy.py`의 Module→Feature→Scenario 연결·Procedure 교차 참조에 타입 예외·잘못된 ID 연결·중복·누락 우회가 있는지 코드와 반례를 확인. 특별히 unhashable types, UTF-8/메모리 상한, prompt injection 방어 검토.
2. `bounded_context`가 truncated/omitted 사실을 숨겨 '모든 근거를 읽었다'로 오인하게 하는지; 저사양 LLM에 유효한 상한·부분 증거·재탐색을 보장하는지 확인. 실제 host token/latency 숫자 PASS를 요구하지 말 것.
3. `EVIDENCE_LINKED_NOT_EXECUTION_VERIFIED`와 `may_invoke_doc_converter=false`, `may_publish_knowledge=false`를 전 경로에서 준수하는가? 하나의 anchor가 실제 control/data flow·branch reachability·RF/PHY IPC·MSC 순서를 증명한다고 오판할 경로가 있는가?
4. 기존 CoWork 분류/지식 계약을 침범하지 않는가? `doc-converter v0.2.26` native Scenario IR나 Knowledge Updater/Writer API를 추측·구현·호출했다고 주장하지 않는가? 설계 경계 및 문서가 정확한가?
5. 외부 소스/라이브러리·코드복사 없이 구현된 것이 확인되는가? README/THIRD_PARTY_NOTICES/manifest·ZIP 경로·version·payload SHA, supply-chain 위험, 회귀시험의 누락을 평가해 최소 수정안을 제안.
6. 공개 단독 개발 컴포넌트의 **문서화된 비운영 배포**와 **설치 가능한 최종 스킬 배포**의 게이트 차이를 분명히 평가하고, 현재 버전의 판정을 `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`로 제시.

## 출력 및 비용 계약

- 한국어. 지적별 `BLOCKING / MAJOR / MINOR`, 파일·함수/라인·반례·최소 수정·회귀시험. `INDEPENDENT_REVIEW=PASS/FAIL/PARTIAL/NOT_RUN`, 최종 `ACCEPT/ACCEPT_WITH_CHANGE/REVISE/HOLD`.
- 외부 제품 코드·업무 MSC/로그·고객자료·토큰 0; 리뷰어는 본 비민감 synthetic ZIP과 CoWork 비민감 요약만 접근. 업무 C++/호스트 시험은 범위 밖.
- 신규 리뷰 **정확히 1회**, `POLICY-STATIC-V1`, 최대 USD 3.00/건. Windows watcher의 **실제 정책·보호 위임·만료·repo_id/source pin·SHA·중복·승인 scope**가 검증된 경우에만 signer가 보호 서명하고 **READY를 마지막에 게시**. 미충족 시 BLOCKED, 모델 호출 0. GPT는 `APPROVAL_SIG.json` 또는 `READY.md`를 생성하지 않음.
- 리뷰 결과: `collab/reviews/REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121/REVIEW_RESULT_1.md`; 영수증: `collab/receipts/REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121/RECEIPT_1.md`. 결과·비용·input SHA/readback 확인 전 리뷰 완료, GPT PASS, PUBLIC 최종 ZIP 게시를 주장하지 않음.
