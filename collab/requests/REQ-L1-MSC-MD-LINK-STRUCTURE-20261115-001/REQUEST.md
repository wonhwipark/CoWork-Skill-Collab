---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: REQUESTED
request_id: REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: l1-knowledge-updater
package_path: /SKILL-COLLAB/packages/msc-md-link-structure_r0001_1115_REVIEW_INPUT.zip
package_file_id: github:REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001
package_rev: structure-r0001
package_sha256: 90bb61a0e7c3b429942c620480ad9a079980d2a3432b72cea8ba80a4b915907d
package_size_bytes: 38132
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [msc-md-link-structure]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent structural review of two analysis entry points, converter MSC viewer, destination MD links, publication paths and recovery
---

# MSC · Procedure/Feature MD 링크 — Claude Code 독립 구조 리뷰 요청

- 사용자 지시: “클로드코드로 구조리뷰요청해줘”.
- 이번 대상: `collab/projects/L1-WORKSPACE-RAG-20261111-001/MSC_MD_LINK_SKILL_SUPPORT_REVIEW_AND_PROPOSAL_r0001_20261115_KST.md`, 고정 원문 commit `b3f207728867ad9fad5d06d0ad8d3ff244106b06`, SHA-256 `b4f64584c0edf48921f77c0930b520e438b14d6299dd8aa49da5f9ef86ee290a`.
- 새 Work를 만들지 않고 기존 `L1-WORKSPACE-RAG-20261111-001`에 연결해요. 이전 Work→Knowledge 동결 요청 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001`의 입력·승인·서명·실행 이력은 보존하며 이번 요청에 전용하지 않아요.

## 리뷰 범위

1. `l1-fix-workflow` 또는 `l1-knowledge-updater` → code-analyzer → doc-converter의 기존 기능과 책임을 재사용해요. 두 진입 모두 같은 Work에 분석·초안·MSC를 저장/갱신할 수 있어야 해요.
2. Workspace 또는 그룹 지식의 해당 Procedure/Feature MD에서 MSC 미리보기와 실제 HTML 뷰어를 열 수 있는 구조를 검토해요. converter는 표현 자료를 만들고 기존 대상 writer가 최종 경로의 링크를 연결하는 분리가 타당한지 판단해주세요.
3. F1~F5를 독립적으로 검증해주세요. Kernel SVG/PUML 복사와 파일 이름 변경, 미렌더 fallback, Evidence/provider 계약, 그룹 독자 권한, MD 마커·수동 본문 보호, source revision, 게시 일부 실패·Work 역링크 복구를 우선 확인해요.
4. 코드 발췌는 4개 고정 PUBLIC baseline이에요. Updater·그룹 설치 원문/실제 업무 저장소·writer·호스팅은 미접근이에요. 미확인을 기능 부재로 단정하거나 새 원장·schema·호스팅을 기본 요구로 추가하지 마세요.
5. 합성 샘플의 브라우저 PASS와 converter 자동 생성·실제 업무 게시 E2E를 구분해주세요. 코드 분석·Job·설치·그룹 지식 쓰기·PUBLIC 게시를 실행하지 않아요.

`00_README.md` → `01_REVIEW_QUESTIONS.md`의 R01~R10 → `02_PROPOSAL.md` → `03_SOURCE_EVIDENCE.md` 순으로 읽어요. 나머지는 기존 수용 설계·공개 샘플·바이트 출처예요. 8개 입력은 ZIP에 고정했으며 별도 knowledge_refs는 없어요. 설계/정적 검토 입력 ZIP으로, 설치용 SKILL.md를 요구하거나 코드 실행을 시도하지 마세요. `/SKILL-COLLAB/...`는 기존 GitHub transport의 논리 경로이고 실제 파일은 PRIVATE `wonhwipark/CoWork-Skill-Collab/main`의 `collab/`에 있어요. Dropbox 재활성화 지시가 아니에요.

## 승인·실행 경계

독립 Claude 리뷰 **최대 1회, POLICY-STATIC-V1, 최대 USD 1.00**예요. 이 값은 정책 상한이며 이 요청 본문 자체가 신규 유료 실행 권한·보호 위임·유효 서명을 대신하지 않아요. 사용자 구조 리뷰 요청은 확인했지만 이번 새 ID의 별도 비용 권한은 아직 확인되지 않았어요. Windows 호스트가 실제 현재 승인/신뢰 정책과 비용·만료·중복을 확인하고, 적용 가능한 유효 권한이 있을 때만 기존 절차를 이어가요. 없으면 해당 게이트만 BLOCKED·모델 0으로 기록해요. 다른 요청의 $1/$3 승인이나 활성화 전 자동 승인 설계를 소급 적용하지 않아요.

기존 GitHub 단일 LIVE watcher를 사용하고 APPROVAL_SIG 검증 후 READY를 마지막에 게시해요. GPT가 READY/서명/receipt를 꾸미거나 Windows 호스트에 접근한 것으로 보고하지 않아요. 추가 모델·하위 Agent·재리뷰·자동 재큐잉을 시작하지 않아요. 실행 불확실은 REVIEW_UNCERTAIN으로 보존하고, 결과 게시 장애는 저장된 결과 게시만 복구해요. 운영 watcher·DB·키·설정·provider는 변경하지 않아요.

## 결과·영수증

R01~R10별 `수용 / 수정 수용 / 거절 / 보류 / 추가 확인`과 최종 `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`를 작성해주세요. BLOCKING/MAJOR/MINOR 지적은 최대 6개, 각각 정확한 파일/절·함수/조건, 영향, 최소 수정, 담당 기존 스킬과 검증 기준을 제시해요. 직접 확인·GPT 사전 정적 검토·호스트 보고·미실행을 구분해주세요.

- 결과: `collab/reviews/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/REVIEW_RESULT_1.md`
- 영수증: `collab/receipts/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/RECEIPT_1.md`
- 디스패치: `collab/dispatch/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/DISPATCH_1.md`
- 사용량: 같은 receipts 폴더에 기존 엔진 계약의 실제 사용량 영수증을 보존해요.

결과와 receipt의 request/revision/ZIP SHA를 확인한 후 같은 Work CURRENT/TRACKER에 연결하고 GPT가 지적별 판정해요. 파일 게시 성공을 독립 리뷰 실행·업무 E2E PASS로 승격하지 않아요.
