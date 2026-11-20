# GPT 판정 — Viewer 인증 기반 편집 독립 설계 R1 (2026-11-20 KST)

- Work: `L1-WORKSPACE-RAG-20261111-001`
- Review: `REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120` / revision 1
- **GPT_DISPOSITION=ACCEPT_WITH_CHANGE / R1_REVIEW_CYCLE=CLOSED**
- 정적 독립 설계 리뷰 완료. 설계 보완본 r0002 작성·게시. **추가 유료 리뷰/R2=0, 구현·Linux 호스트 테스트·배포=NOT_RUN.**

## 1. 검증된 협업 근거
| 대상 | 원격 확인 |
|---|---|
| REQUEST | `collab/requests/REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120/REQUEST.md` · revision=1 |
| SOURCE_PIN | `commit=0b741ce6ed9455d7606850321830cc359d83e227`, `repo_id` 문자열 `1451933830` |
| 고정 입력 ZIP | `collab/packages/l1-workspace-viewer-edit-design_r0001_1120_REVIEW_INPUT.zip` · 19,482 B · SHA-256 `764477880d6b6b6b4bb468f4bb9ccaf6802e5561944ec89569030d69c7080975` · CRC 2개 PASS |
| 승인·READY | `APPROVAL_SIG.json` 존재 및 `READY.md`의 요청 ID·revision·REQUEST SHA·ZIP SHA 일치. 개인키/호스트 신뢰 루트 실제 검증은 GPT의 직접 검증 범위 아님 |
| Dispatch | `collab/dispatch/REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120/DISPATCH_1.md` · v0.2.29 / 처리키 고정 |
| 독립 결과 | `collab/reviews/REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120/REVIEW_RESULT_1.md` · `execution_status=COMPLETED` · `ACCEPT_WITH_CHANGE` |
| 영수증 | `collab/receipts/REQ-L1-WORKSPACE-VIEWER-EDIT-DESIGN-R1-20261120/RECEIPT_1.md` · `ok=true`, 요청 ID·revision·ZIP SHA·처리키 일치, watcher v0.2.29 |
| 비용 | 사용자 제공 완료 알림 **USD 0.29**. 원격 영수증에 실제 비용값 없음 → 비용 독립 검증 `NOT_VERIFIED` (호스트 DB/usage 확인 아님) |

독립 리뷰어는 `01_VIEWER_EDIT_DESIGN.md`·`02_REVIEW_README.md` 두 정적 문서를 검토했으며 실제 코드 실행/Windows-Linux 업무 Viewer 원본 열람/업무 LLM-MCP 시험은 없음. `review_scope: CODE_REVIEW` 메타는 운영 분류일 뿐 실제 코드 리뷰가 아님. 이 R1 완료를 기존 Linux B1/B2/B3·E3/E4 PASS로 승격 금지.

## 2. 리뷰 지적·GPT 판정
| 리뷰 ID | 심각도 | GPT 판정 | 정확한 수용 범위 |
|---|---|---|---|
| B-1 | BLOCKING | **수용** | 별도-origin MSC iframe의 화살표를 부모가 직접 선택한다고 가정한 모순 제거. **부모 Viewer 소유 DOM**에 기존 서버가 ACL 검증해 반환한 canonical message/participant anchor 목록을 표시하고, 서버에서 원본 revision/anchor/권한 재검증. 기존 지원·앵커 부재 시 구조적 쓰기 차단. 임의 `postMessage` bridge 금지 |
| M-1 | MAJOR | **수용** | G0에서 CSRF·속도 제한/계정 보호·세션 고정 방어·문서별 권한이 미확인/부재라면 `EDIT_AUTHORIZED` 활성화/코드 병합을 HARD_STOP. 서버 정책·보호를 우선 확인/최소 보완 |
| M-2 | MAJOR | **수용** | 초안 저장·Diff/Preview·최종 Commit 각각 세션/CSRF/edit ACL 재검사, writer 진입 직전 재검증 |
| N-1 | MINOR | **수정 수용** | 초안 TTL/정리 기존 계약 우선 재사용, 미지원이면 G0 GAP 및 초안 영속화 보류 |
| N-2 | MINOR | **수용** | 편집 인증 성공 시 세션 ID 재발급/회전 등 session fixation 방지 |
| N-3 | MINOR | **수정 수용** | Agent 검증 기본 후보는 사용자 요청 1건당 최대 1회·자동 재시도 0. 실제 정책/비용/승인 한도 현장 확인 전 자동 호출 활성화 금지 |
| N-4 | MINOR | **수용** | 기존 Viewer P1·U01/U02 범위별 회귀를 선행 검토하고 편집 기능 합성 UI와 실호스트 활성화를 구분 |

**리뷰 제안의 첫 구현 범위 축소는 수정 수용**: 사용자 확정대로 첫 증분에 MSC **메시지·Participant 수정 요청 UI**는 포함한다. 단, 실제 canonical 구조 변경 저장·Agent 자동 호출·doc-converter 재생성은 canonical anchor/provider·writer/CAS·근거·호스트 ACL 검증 이후 다음 활성화 게이트로 분리한다. 이렇게 하면 첫 구현 요구를 폐기하지 않으면서 미검증 쓰기를 막을 수 있다.

## 3. 수용 반영 문서 및 상태
- 기존 입력 r0001과 R1 결과/영수증 **불변**.
- GPT 후속 보완: [`L1_WORKSPACE_VIEWER_AUTH_EDIT_DETAILED_DESIGN_r0002_20261120_KST.md`](L1_WORKSPACE_VIEWER_AUTH_EDIT_DETAILED_DESIGN_r0002_20261120_KST.md). 직접 수정 UI·메시지/participant 요청·안전 선택·인증/권한 하드스톱·충돌/복구·T17~T19 부정시험 반영.
- **수정 설계 r0002는 GPT 보완본이며 Claude가 r0002를 독립 재검토한 결과가 아님.** 기존 R1 `ACCEPT_WITH_CHANGE` 판정 유지. 추가 REQUEST/READY/유료 R2 만들지 않음.
- `REVIEW_COMPLETED=PASS_REMOTE_EVIDENCE`, `GPT_DISPOSITION=ACCEPT_WITH_CHANGE`, `DESIGN_R0002=POSTED`, `HOST_G0_AUTH/API/ANCHOR/WRITER=NOT_VERIFIED`, `VIEWER_EDIT_IMPLEMENTATION=NOT_RUN`, `HOST_INSTALL/WORK_WRITE/KNOWLEDGE_WRITE/PUBLIC=NOT_RUN`.

## 4. 미검증 및 안전한 다음 행동
- 업무 Linux 별도 Viewer 실제 repository/branch/commit, 현재 인증(세션·CSRF·ACL·rate-limit/계정 보호), Viewer API/read handler, canonical 메시지/participant anchor 제공 여부, 개인 draft writer, Kernel/Updater 저장 CAS·멱등키·readback, 실제 doc-converter B형 렌더 실패 반환을 **기존 접근 가능한 업무 GPT/Linux Agent에서 READ_ONLY G0** 확인.
- B1 경로 이탈/B2 비밀·제한자료/B3 HTML origin 격리, E3 Linux localhost/E4 동료 2계정, 실편집 인증/권한 보안시험은 아직 미실행. 사용자에게 내부 소스·설치 파일 반출을 재요구하지 않음.
- **NEXT_ONE_ACTION:** 동일 Work의 업무 GPT가 상세 설계 r0002를 기준으로 기존 Linux Viewer/Updater의 설치 계약을 G0로 한 번 대조해 **REUSE / CONNECT / 확인된 GAP / BLOCKED** 및 D2 합성 UI와 실제 쓰기 활성화의 분리 수락 기준을 정리. 이 G0는 구현·설치·실쓰기·Job 실행 승인 아님.
