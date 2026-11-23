# Viewer v0.5.2 가독성 개선·공개 개발물 전달 결과 (r0001)

- 2026-11-24 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`
- 범위: 사용자가 제공한 `L1_WORKSPACE_VIEWER_V051_READABILITY_REVIEW_20261124_0013_KST.md`의 Viewer 1차 수정.
- 저장소: `wonhwipark/L1Work` PUBLIC `main`, commit [`0b602472b2a505a86ebb0fdf0d94535098f5117d`](https://github.com/wonhwipark/L1Work/commit/0b602472b2a505a86ebb0fdf0d94535098f5117d)

## 1. 현재 상태

**PUBLIC_DEV_DELIVERY=PASS_REMOTE_VERIFIED, NODE_RUNTIME=NOT_RUN, BROWSER_E2E=NOT_RUN, INDEPENDENT_REVIEW=NOT_RUN, HOST_DEPLOY=NOT_RUN.**

기존 Viewer v0.5.1은 불변 보존. 신규 ZIP `l1-workspace-viewer-wiki-integrated_v0_5_2_1124.zip`을 `main` 루트에 추가. **374,930 bytes / 36 files / SHA-256 `15e83f136fa10ef680619602b55d74c4cd4c0c86a6cc470c1bec9cac250239ba` / Git blob `6dc79e44dbb209a6cf2b437fcd0672649a772a10`.**

- [ZIP](https://github.com/wonhwipark/L1Work/blob/main/l1-workspace-viewer-wiki-integrated_v0_5_2_1124.zip)
- [업무 GPT 완결 인계서](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_V052_READABILITY_COMPLETE_HANDOFF_r0001_20261124_KST.md)
- [합성 HTML 미리보기](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_Workspace_Viewer_v0_5_2_20261124_KST.html)

원격 readback: ZIP blob/크기, 인계 blob `3976a0b4252c0a7605e7c11936a172f535aa3dc1`, HTML blob `a2417b9316d9015951f0ebc34b4aa9123a94943b` 일치.

## 2. 실제 변경

| 대상 | 처리 | 범위·주의 |
|---|---|---|
| `assets/markdown.js` | 상대 `.md` 링크를 resolver로 전달. `\\|`, `&#124;`, `CFG\\_REQ`, `&lt;` DOM 텍스트 복구. 표 split을 unescaped `|` 기준으로 변경 | HTML 직접 실행·외부 URL 연결 금지 유지 |
| `adapters/adapter.js` | 같은 Work 경로·기존 docId 매핑 예시 및 선택적 issue snapshot/getDocumentMeta 테스트 메타 | **합성 데모 전용**, 업무 실제 read adapter 미접근 |
| `assets/app.js` | Work 진행/코드 수정/시험 결과 분리, PASS/FAIL/NOT_RUN/기록 없음 표기. 선택적 issue snapshot 4칸 요약, 근거 링크, 전체 원문 접기 | 실제 Work 기록이 없으면 원문 fallback. G0에서 실 adapter 매핑 |
| `assets/viewer-integrated.css` | 글자 크기를 표·코드·목차·제목까지 확장; 긴 경로·식별자 및 반응형 카드 | 기존 Write·도우미·원본 스키마 불변 |
| `fixtures/demo-data.js` | 합성 후속 문서·검증 부분결과·원인 가설 예시 | 운영 사실로 취급 금지 |
| 기타 | VERSION/source pin/manifest/standalone/릴리스 스크립트/호스트 인계/새 Node 회귀 코드 | 패키지 재현 및 현장 시험용 |

**스킬 변경 없음:** `l1-fix-workflow v1.6.75`, `work-ledger-kernel v0.7.43`의 기존 출력 우선 재사용. 실제 TL 요약이나 문서 원문에서 근거가 누락된 경우에만 해당 스킬 변경 검토.

## 3. 실제 검증

| 게이트 | 판정 | 근거 |
|---|---|---|
| v0.5.1 source pin | PASS | 원격 349,332 bytes, SHA-256 `0bc0240261e29c863c541e9650e9f99271b2b924ffd52be753598889f66cf290` 일치 |
| 후보 ZIP 구조/CRC | PASS | 저장 방식 ZIP의 36개 로컬 엔트리/중앙 목록·개별 CRC 재검사 |
| manifest / Write 불변 | PASS | 각 원본 해시와 배포 manifest 재계산, Write 3파일 pinned SHA 일치 |
| v0.5.2 L1Work 원격 readback | PASS | 새 ZIP/인계/HTML blob SHA 및 바이트 수 확인 |
| v0.5.2 Node 신규/기존 회귀 | **NOT_RUN** | `tests/regression.cjs`, `assistant-client.cjs`, 신규 `readability.cjs`를 포함. 실제 Node 실행 미수행 |
| 브라우저 키보드·시각/E2E | **NOT_RUN** | 실제 브라우저 렌더 미수행 |
| 현장 Linux source·실제 read adapter/ACL | **NOT_RUN** | 업무 Linux 직접 연결 없음 |
| 독립 리뷰·운영 설치·Write/LLM/Agent | **NOT_RUN** | 별도 요청/호스트 검증 없음 |

이 후보의 ZIP 정적·해시 검사는 Node DOM/JS 런타임 시험 결과가 아니다. 과거 v0.5.1 Node 25 PASS나 별도 후보 시험을 v0.5.2 결과로 승격하지 않는다. **deployment_not_approved**.

## 4. 잔여 위험·필요 게이트

- 실제 Linux Viewer의 adapter 파일 위치/인증/계정·Work ACL·읽기 root·source revision 미확인. 데모 `WikiAdapter`를 운영 구현으로 간주 금지.
- `getIssueSnapshot(docId)`과 `getDocumentMeta`의 테스트 결과·근거는 실제 기존 Workflow/Kernel에 존재하는 값만 매핑하며, 없는 정보는 누락/기록 없음. 과거 데이터를 자동 재작성하거나 LLM으로 새 결론 생성 금지.
- 대표 Work 3건에서 링크 같은 Work 범위·5열 후속 표·원문 토글·검증 구분·폰트/표/목차, 기존 A01~A10/H01~H05와 Write 원본 불변 회귀 필요.
- **호스트/유료 리뷰/Job/LIVE/Write 활성화 수행 0**. 별도 보안·백업·롤백·승인 게이트 유지.

## 5. 다음 한 행동

업무 GPT가 L1Work `main/handoffs/L1_WORKSPACE_VIEWER_V052_READABILITY_COMPLETE_HANDOFF_r0001_20261124_KST.md` 및 루트 v0.5.2 ZIP만 읽고 실제 Linux 기존 Viewer read adapter G0 확인 → 연결 → Node/브라우저/권한 회귀 근거 제출. 업무 제한 소스·상세 MSC/고객 로그·토큰은 공개 저장소로 반출 금지.
