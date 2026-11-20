---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: SUBMITTED
request_id: REQ-L1-WORKSPACE-VIEWER-STYLE-DESIGN-R1-20261121
request_revision: 1
project_id: L1-WORKSPACE-RAG-20261111-001
work_id: L1-WORKSPACE-RAG-20261111-001
skill_id: l1-knowledge-updater
package_path: /SKILL-COLLAB/packages/l1-workspace-viewer-style-design_v0_1_0_1121_REVIEW_INPUT.zip
package_file_id: github:REQ-L1-WORKSPACE-VIEWER-STYLE-DESIGN-R1-20261121
package_rev: l1-workspace-viewer-style-design-v0.1.0-r1
package_sha256: 4cefbc4d97372365b6046beb4591afc04d97136723c76d91aa10bc1345926576
package_size_bytes: 15497
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [l1-workspace-wiki-ui-visual-ux-review]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: independent static visual design R1 on bluegray professional Viewer UI and issue-first Work labels
---

# L1 Workspace Viewer — 동료용 시각 스타일 A안 정식 독립 설계 R1 요청

- 사용자 최신 요청: 위 블루그레이 A안과 기존 Viewer 비교 설계를 **협업 리뷰에 정식 요청하고 결과를 판정한 후에만 구현을 재개**.
- 대상: 기존 Work `L1-WORKSPACE-RAG-20261111-001`의 1차 Read Only Viewer 개선; 2차 인증/편집 및 Linux 실제 배포는 리뷰 대상이 아님.
- PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`. 고정 입력 commit **`fbd577ca29fd3aea6e76ea6353f842a543859397`**에 ZIP·설계 MD·합성 HTML·리뷰 안내가 실존함.
- ZIP: `collab/packages/l1-workspace-viewer-style-design_v0_1_0_1121_REVIEW_INPUT.zip`; size **15497 bytes**, SHA-256 **`4cefbc4d97372365b6046beb4591afc04d97136723c76d91aa10bc1345926576`**, 3개 파일 원격 base64 readback 대조 PASS.
- 정확한 3개 입력: `01_VIEWER_VISUAL_REFRESH_DESIGN.md`(상세 설계), `02_VIEWER_STYLE_A_B_COMPARISON.html`(구 스타일 vs A안 합성 목업), `03_REVIEW_README.md`(평가 범위).
- 참고 v0.1.0 원본: `collab/projects/L1-WORKSPACE-RAG-20261111-001/ui/viewer-wiki-ui_v0_1_0/`, CSS blob `5d3e1e88b5ff3553ea94f745cd52c431457ca2e3`, 스크린샷 `screenshots/wiki-1440.jpg`·`wiki-390.jpg`. 이들은 **고정 ZIP 외의 별도 참고**이며 실제 신규 리뷰가 기존 UX R1 재실행이 되어서는 안 됨.
- 기존 후기: 위키 UI UX R1 `REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119` ACCEPT_WITH_CHANGE, 편집 설계 R1 `REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120` ACCEPT_WITH_CHANGE. 이번 요청만 별도 R1, 과거 결과/영수증/ZIP 불변.

## 독립 리뷰 질문
1. 기존 보라색(#5145CD) 대비 A안 블루그레이(#1E40AF)의 동료용 기술문서 적합성·과잉 장식 제거의 효과 및 **유지해야 할 기존 UI 강점**은?
2. 1440/390/320px, Work/Knowledge 선택·focus·링크·상태 배지·메타 텍스트의 가독성/색 대비(WCAG AA), P1 CSS override/MSC overflow 안내와 충돌 여부는?
3. **SOC 등의 검증된 대표 이슈번호를 제목 맨 앞에 표시**하고 Work ID는 보조로 두는 UX가 실사용에 유용한가? 길이·동명이름·대표 이슈 불명확·번호 중복 반례는?
4. 읽기 무로그인 유지·원본 Work ID/폴더/Evidence SHA 불변·B1/B2/B3 경계·기존 Viewer adapter/CSP/renderer에 대한 최소 영향으로 제한 가능한가? 실제 Linux G0 미확인/합성 프리뷰의 경계는?
5. 최종 1차 범위는 **색상·미세 문구·Work title 표시·UX P1**로 제한하고 후속 2차 [수정] 전용 ID/PW/Writer·스킬 기능 변경과 섞이지 않게 하는 최소 구현/시험·검증 순서를 판정해 달라.

## 결과 계약
- 한국어, `INDEPENDENT_DESIGN_REVIEW`, `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`.
- 지적별 severity `BLOCKING/MAJOR/MINOR`, 정확한 입력 파일/절·사용자 영향·반례·최소 수정·재현/시험법. 문제 수 강제 금지.
- `VISUAL_INSPECTION=PASS/PARTIAL/NOT_RUN`과 직접 연 preview/이미지, 실제 브라우저 실행 여부를 표시. **정적 목업을 실제 Linux Viewer E3/E4·B1~B3 PASS로 보고 금지**.
- 이 기존 Work의 다음 한 행동 및 간단한 1차 개발 최소 범위·원본 Work/Knowledge 미변경 확인을 보고.

## 비용·보호·실행 안전
- 요청 1회 / 모델 호출 최대 1 / 정책 **`POLICY-STATIC-V1` USD3.00/건 이내**. Windows watcher v0.2.29 LIVE+보호 위임 USD3는 2026-11-20 호스트 보고 기준이며 **신규 요청 첫 유료 E2E는 당시 NOT_RUN**. 실제 호스트에서 최신 정책·위임 scope·만료·repo_id/source pin·SHA·중복·승인을 검증한 적격 경우에만 reviewer 호출.
- **이 REQUEST 및 SOURCE_PIN은 signer 권한이 아님. GPT는 APPROVAL_SIG.json/READY.md를 직접 만들거나 승인·서명을 가장하지 않음.** 유효한 보호 signer가 승인·서명하고 마지막에 READY를 게시해야 실제 정식 실행 후보. 불가하면 PENDING/BLOCKED + 모델 호출 0.
- 별도 운영 설치/설정·DB·키·인증 계정·PUBLIC 게시·워크플로/업무 Work·Knowledge 수정·원본 회사 코드/실제 MSC/로그/토큰 반출 0. 독립 리뷰 자동 재실행·재과금 0.
- 예상 결과 위치: `collab/reviews/REQ-L1-WORKSPACE-VIEWER-STYLE-DESIGN-R1-20261121/REVIEW_RESULT_1.md`, `collab/receipts/REQ-L1-WORKSPACE-VIEWER-STYLE-DESIGN-R1-20261121/RECEIPT_1.md`; 결과와 영수증을 원격 확인하기 전 REVIEW=COMPLETED 주장 금지.
