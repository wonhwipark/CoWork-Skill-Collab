---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122
request_revision: 1
project_id: COWORK-SKILL-DISCOVERY-20261112-001
work_id: COWORK-SKILL-DISCOVERY-20261112-001
skill_id: cowork-context-design
package_path: /SKILL-COLLAB/packages/cowork_p1p2_context_review_input_r0001_1122.zip
package_file_id: github:REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122
package_rev: cowork-p1p2-context-review-r0001-1122
package_sha256: 35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3
package_size_bytes: 94843
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [cowork-p1p2-context-code-design-and-e2e-plan-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent review of CoWork P1 P2 context retrieval implementation and Windows E2E verification plan
---

# CoWork P1/P2 구현 및 Windows 검증 설계 — 정식 독립 리뷰 REQUEST 초안 (아직 미게시)

이 문서는 `collab/projects/`에만 게시된 **Windows 사전검사용 REQUEST 초안**이다. YAML의 `state: SUBMITTED`는 필수 파서 형식이며 정식 `collab/requests/REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122/REQUEST.md`로 게시됐다는 뜻이 아니다. 이 파일은 **실행 트리거가 아님**.

## 최신 사용자 요청 및 과거 이력

- 2026-11-22 KST: "협업 다시확인후 정식 리뷰요청해줘" — 현재 대화창의 가장 최근 P1/P2 구현 및 Windows E2E 인계 r0002를 기준으로 **독립 리뷰 1회 요청**.
- 2026-11-20의 P1 설계 R1 `REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120`은 `HOST_PREFLIGHT_BLOCKED`, 실제 REQUEST 미게시/모델 0. 과거 입력 ZIP·오류 기록 보존; 이번 R1을 과거 R1의 재큐잉 또는 패키지 변조로 처리하지 않음.
- 2026-11-20 P1/P2 구현은 당시 사용자 지시로 독립 리뷰 생략 후 적용. **이번 새로운 명시 리뷰 요청은 별도의 한정 리뷰**이며 기존 SKIP 이력을 소급 PASS로 변경하지 않음.

## 입력 고정 및 리뷰 범위

- ZIP 후보 bytes: 94843 B; SHA-256 `35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3`; 안전 경로 10 members(8개 실제 소스/문서 + MANIFEST/README), CRC10/10 PASS.
- 현재 검증용 **비트리거 base64 staging**: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_REVIEW_CANDIDATE_r0001_1122.zip.base64`. Windows에서 반드시 원본 ZIP으로 정확히 decode한 다음 SHA/CRC 재검증. 제출 시 ZIP 이름은 정확히 `cowork_p1p2_context_review_input_r0001_1122.zip`여야 함.
- 대상 원본: CoWork `collab/dashboard/context_query.py`·`tests/test_context_query.py`·P1 설계·P1/P2 적용 결과·실사용 검증 계획 r0001·Windows 실행 인계 r0002. L1Work `docs/cowork-dashboard/context-view.js`·`index.html`의 **조회 시점 최신 원본**. `MANIFEST.json`의 각 repo/path/Git blob SHA/bytes/sha256으로 실제 고정. 다른 시점의 CURRENT/운영 LIVE를 이 ZIP만으로 최신 실측 판정 금지.
- 리뷰 목표: (Q1) 질문별 Work 라우팅의 누락·오분류/다중 Work, (Q2) 최신 CURRENT·과거 기록·호스트 실제 실행 정합성/거짓 PASS, (Q3) P2 REQUEST·ZIP·PIN·서명·READY·영수증 관계의 안전한 미검증 판정, (Q4) Python path traversal/symlink/파일 상한·Git baseline 안전, (Q5) PUBLIC 상태 allowlist·비밀정보 유출·JS DOM 안전, (Q6) B안 4카드·D안 타임라인·6시간 공개 상태를 혼동하지 않는 UX, (Q7) 9개 기존 단위시험과 실제 Windows/PC·모바일/30문항 미검증 범위, (Q8) Windows r0002의 비용·권한·문서 게시/실제 세션 자동 로딩·결과 게시 구분, (Q9) 사용자 실사용을 위한 최소 필요 수정, (Q10) 더 이상 확장할 필요 없는 기능 경계.
- 리뷰 방법: **독립 STATIC_ONLY 코드/설계 리뷰 1회**. 소스·문서를 읽고 취약점·개선 필요/선택 사항을 심각도 BLOCKING/MAJOR/MINOR/RECOMMENDATION으로 구분. 변경 제안은 근거 파일/행·재현·최소 수정·시험 기준 제시. 실제 Windows 세션·LIVE·브라우저·Linux E2E를 수행한 것으로 과장하지 않음.
- 리뷰 출력: `collab/reviews/REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122/REVIEW_RESULT_1.md` + `collab/receipts/REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122/RECEIPT_1.md`, 실제 게시 후만 완료 판정. 독립 리뷰 진행은 기존 개발자 자체시험과 분리.

## 정책 및 실행 게이트 (항상 사전 검증)

- 정책: 최신 사용자 공통 건당 최대 USD3·`POLICY-STATIC-V1` / 모델 최대 1회 / 기존 유료 승인 범위만 사용. 이 대화에서 GitHub 원격 문서로 확인된 Windows 마지막 LIVE 보고는 `v0.2.29 / STATIC USD3 / 보호 위임 USD3`; 새 Windows 실제 조회는 별도.
- **AUTO 금지 기본:** 대상 `skill_id=cowork-context-design`은 지난 보호 allowlist에 없었음. 다른 `skill_id`로 위장하여 자동 위임 우회 금지. Windows 실제 허용 목록이 갱신되었음을 확인하지 못하면 `--approval-route manual`로 사전검사. 이는 서명 승인과 다름. 공식 보호 signer의 **유효한 단발성 수동 승인/권한 검사**가 불가하면 서명·READY·모델 호출 0.
- 정식 제출 전 Windows LIVE `review_request_gate.py select/check --intent unified --required-budget-usd 3.00` 및 실제 ZIP+이 초안의 바이트 고정·중복/레거시 검사 필수. `PASS_PREPUBLICATION_ONLY`가 나오지 않으면 `collab/requests`에는 아무것도 게시하지 않음.
- PASS 후에도 **표준 `collab/ops/submit_review_request.py`만 사용**해 Commit A에 REQUEST+ZIP 동시 게시, Commit B에 A를 가리키는 SOURCE_PIN(repo_id 문자열 `1451933830`) 게시·readback, 실제 signer 서명·중복/비용 검증 뒤 READY 마지막, Claude 리뷰 1회, 영수증/비용/중복 0 확인. 기 승인 범위를 넘어선 새 운영/서명 정책·설치 변경 금지.
- `UNVERIFIED`, `POST_CONFLICT`, `UNCERTAIN`이면 자동 재요청·재서명·재큐잉·재모델 호출 금지. 입력 SHA/크기/원본이 달라지면 이번 초안을 조용히 변경해서 제출하지 말고 새 revision/필요 승인 확인.
- GitHub 문서·base64 후보 게시만으로 `REQUEST_POSTED`, `READY`, `INDEPENDENT_REVIEW`를 PASS로 보고하지 않음.

**현재:** `REVIEW_INPUT_CANDIDATE=POSTED_READBACK`, `FORMAL_REQUEST=NOT_POSTED`, `SOURCE_PIN=NOT_POSTED`, `SIGNER=NOT_RUN`, `READY=NOT_POSTED`, `INDEPENDENT_REVIEW=NOT_RUN`.
