# Windows Claude Code 독립 코드 리뷰 요청 — MSC 4종 재사용·2종 개발 패치 r0001

- **Review ID:** `L1-MSC-SKILL-PATCH-20261116-001` / 기존 Work `L1-WORKSPACE-RAG-20261111-001`
- **정본:** GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- **본 요청 경로:** `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_MSC_SKILL_PATCH_INDEPENDENT_REVIEW_REQUEST_r0001_20261116.md`
- **고정 입력 commit:** `29aadbaeb5245f7a811c3050160c10cddce46954`. **리뷰 입력은 이 commit에서만 읽고**, 이후 main 변동을 코드 입력 변경으로 자동 반영하지 않음
- **형식:** 사용자 요청에 따른 **Windows Claude Code의 개발 세션과 구분된 독립 소스·패치 리뷰**. 이 문서는 대화형 리뷰 원샷 인계이며 watcher용 `REQUEST/APPROVAL_SIG/READY`가 아님. 문서 게시만으로 Windows 프로세스·유료 모델 호출을 실행하지 않음.
- **초기 상태:** `REQUEST_DOCUMENT=POSTED`, `WINDOWS_DELIVERY=NOT_VERIFIED`, `INDEPENDENT_REVIEW=NOT_RUN`, `RESULT/RECEIPT=NOT_RECEIVED`.
- **업무 원본·로그·MSC 금지:** 공개/허용된 스킬 ZIP의 합성 데이터만. 실제 업무 l1-workspace/그룹 writer/코드/고객자료/비밀·인증정보에는 접근권이 있다고 가정하지 않음.

## 1. 리뷰 입력 — 변경분 중심

| 역할 | commit에 고정한 파일 경로 | Git blob / 바이트 SHA-256 |
|---|---|---|
| **doc-converter 변경 후보** | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/doc-converter_v0_2_23_1116.zip` | blob `ba32a057a2590fdf51aac6aad30f831404ed0222` / 210426 B / SHA-256 `43805ae0ce1b08205125441f383f6bdfc6f114ef53bb2609295827f10b1ce23e` |
| **Kernel 변경 후보** | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/work-ledger-kernel_v0_7_40_1116.zip` | blob `3e9346ad5d13645d86bcfdce6aa20f7e17f4699d` / 410922 B / SHA-256 `b8077fd717f326fb7bc556407b8e8b8a7f32a580e143ec3a6d646d3b1e9df7ce` |
| **Kernel diff 기준** | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/work-ledger-kernel_v0_7_39_1115.zip` | blob `418d11db6a2d5071d37bcdd8bf1cc9e94f23346c` |
| **Workflow 재사용 확인** | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_69_1115.zip` | blob `e18b8d7740acff0f04efb0b11906d63198b23389` / **이번 MSC 목적 신규 패치 없음** |
| **Analyzer 재사용 확인** | `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/code-analyzer_v0_15_3_1114.zip` | blob `a661219a0c6c909bd2cb71fa849a81d795b93547` / **이번 MSC 목적 신규 패치 없음** |

Converter 원래 baseline은 PUBLIC `wonhwipark/L1Work/main/doc-converter_v0_2_21_1106.zip`. PRIVATE 중간 후보 `candidates/doc-converter_v0_2_22_1116.zip`도 diff 확인용으로 보존. PUBLIC 루트 ZIP과 업무 설치본의 동일성은 미확인. **금번 검토는 위에 고정된 2개 개발 후보의 실제 코드/diff를 우선**하며, 전체 18개 스킬 재감사는 요구하지 않음.

읽을 설계·개발 근거:
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/MSC_MD_LINK_SKILL_SUPPORT_REVIEW_AND_PROPOSAL_r0002_20261116_KST.md`
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_MSC_MD_LINK_STRUCTURE_REVIEW_DISPOSITION_r0001_20261116_KST.md`
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_MSC_FOUR_SKILL_DEV_PATCH_RESULT_r0001_20261116_KST.md`
- **실제 자체시험** `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_MSC_SKILL_CANDIDATE_QA_RESULT_r0001_20261116_KST.md`.

## 2. 확인된 시험 — 독립 리뷰 PASS와 구분

- PRIVATE GitHub Actions Python 3.10.22 / 3.11.18 [Run 43786218200](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43786218200), 시험 브랜치 commit `3611c44ce11cac52c48b2458299c2bbf3c947867`.
- 각 **표적 검사 19/19 PASS**(full ZIP CRC, 경로·심링크·중복, 전체 `.py` compile, 신규 테스트 **6/6**). Python3.11 Chromium synthetic B HTML 이미지 screenshot 생성 **PASS**.
- **아직 미검증:** 기존 전체 pytest, Kernel 실제 Evidence·SVG 오류 경로, Phase click 실제 이동·CSP/script 정책·unsafe SVG, 실제 원격 `published_path`/Markdown writer/업무 host E3. 테스트 파일에 의존한 **자체시험**이므로 독립 검증으로 승격 금지.

## 3. 독립 리뷰 질문 (비판적·반례 중심, 결함 개수 강제하지 않음)

1. **기존 동작 보존/패치 최소성:** v0.2.21→v0.2.23의 default ISSUE 동작, v0.7.39→v0.7.40 CL/PR WorkReference 및 Evidence 등록 규칙이 깨지지 않았는지. 필요한 API가 이미 있으면 신규 구현보다 REUSE/CONNECT 우선. 간단한 대안을 비용·회귀 위험과 함께 비교.
2. **doc-converter 이름 충돌/경로:** 한글·혼합 이름이 파일명 하나로 합쳐지거나 같은 정규화 결과로 덮어쓰지 않는지, 고유 SHA 접미사·동일 이름 hard-fail·중복 정상/음성 경로·manifest reference 일치, 특수문자/경로 이탈/재실행 idempotency를 실제 코드로 확인.
3. **B HTML 보안/정확성:** 소스 SVG/Title·Phase를 신뢰해도 되는가(XSS, SVG XML 외부 리소스, CSP, `data:image/svg+xml;base64`)? 위치 계산이 실제 SVG divider 1개와 고정 좌표/중복 라벨을 구분하는가? 클릭·줌·장문·6 participant를 실제 브라우저로 확인하고, 호스트에 HTML 실행 URL이 없으면 SVG/다운로드/원본 순서로 fallback해야 하는지 판정.
4. **doc-converter AS-IS·모드/manifest:** Procedure/Feature 전용 문구, 없는 `MSC_DELTA.md` 링크 억제, scenario-build/package의 `--view-mode` API, `MSC_PUBLIC_MANIFEST` HTML 값과 실제 파일·SHA가 일치하는가? 렌더 실패/부분 파일/2 MiB 초과가 성공 처리되지는 않는가?
5. **Kernel Evidence SVG:** `.svg`만 기존 승인 Evidence에서 복사하는지, 크기 초과를 예측 가능하게 거부하고 기존 `.html/.md`의 큰 파일 처리까지 바꾸지 않는지. `published_path`·변경 파일명/hash/manifest·충돌 및 원격 readback과 원본 링크 orphan을 분리할 수 있는가?
6. **두 진입×두 목적지:** Workflow/Updater 직접 진입이 같은 Workspace Work를 유지하도록 기존 writer와 연결할 수 있는가? MD owner·마커/수동 문단/source revision·그룹 게시/역링크는 실제 writer G0 미접근이므로 입증되지 않은 구현을 요구하지 않고 필요한 계약과 보류 게이트를 명확히 구분할 것.
7. **시험의 반증:** 기존 자체시험 19 PASS가 놓친 반례를 독립적으로 최소 1개 이상 설계·실행할 수 있는가(실행할 수 없으면 NOT_RUN)? 패키지 메타 `VERSION`, `.skill-release.json`, `MANIFEST_SHA256.json`, `SKILL.md`와 ZIP 출시 이름의 실제 일관성 및 Python3.10/3.11 호환을 직접 점검. 결함 수를 만들기 위해 억지 지적은 금지.

## 4. 결과·판정·실행 경계

리뷰어가 **개발자와 분리된 별도 세션**에서 입력 원본 SHA를 확인하고, 직접 확인·선행 GPT 주장·테스트 로그·추론·미확인을 나눌 것. 발견 사항마다 `severity(BLOCKING/MAJOR/MINOR)`, `file/function/line or ZIP member`, 재현 가능한 근거, 영향, 최소 수정안, 담당 스킬, 검증법·더 단순한 대안, `수용/수정 수용/거절/보류/추가 확인` 제안을 포함. 최종 `ACCEPT/ACCEPT_WITH_CHANGE/REVISE/HOLD`. 결함 0도 허용.

- **독립 리뷰 결과 게시 요청:** `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_MSC_SKILL_PATCH_INDEPENDENT_REVIEW_RESULT_FOR_GPT_r0001_20261116.md`.
- **수행 증거 (개발자 자체시험과 구분):** `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_MSC_SKILL_PATCH_REVIEW_EXECUTION_EVIDENCE_r0001_20261116.json` (review ID, reviewer environment/time, read SHA, 실제 독립 테스트/상태, 비용/모델을 호출했으면 그 실제 근거, 공개 허용 요약만).
- 기존 Work `CURRENT.md`·`TRACKER.json`은 리뷰어가 실제 결과·증거를 게시한 후에만 해당 리뷰 실행 상태를 갱신. **PRIVATE main에 PR 없이 게시하고 원격 본문·SHA-256/커밋 readback** 확인. 불가 시 결과만 `NOT_POSTED` 보고.
- **금지:** 원본/리뷰 고정 ZIP 임의 변경, 이전 유료 REQUEST/READY 재활성화·모델 재호출, watcher/LIVE/DB/운영 키/설정·업무 호스트/Knowledge 수정, PUBLIC L1Work 새 ZIP 배포, 회사 원본/민감정보 게시. formal reviewer 호출은 현재 유효한 별도 승인/보호 서명이 확인된 경로에서만 가능하며 이번 문서 자체로 실행되지 않음.
- 새로 발견한 결함이 있으면 **GPT 판정 뒤 동일 Work에서 변경 코드·회귀를 보완**. 본 리뷰 세션에서 자신이 수정한 코드를 스스로 독립 PASS로 판정하지 말 것.

## 5. Windows Claude Code에 1회 전달할 문구

> GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CLAUDE_MSC_SKILL_PATCH_INDEPENDENT_REVIEW_REQUEST_r0001_20261116.md`를 읽어주세요. 문서의 입력 commit `29aadbaeb5245f7a811c3050160c10cddce46954`와 두 ZIP SHA-256을 고정하고, 개발과 분리된 독립 코드·패치 리뷰를 실제로 수행해주세요. Python 표적 시험 19/19와 브라우저 smoke PASS는 자체시험이므로 검증 범위와 누락 반례를 비판적으로 확인하세요. 비민감 결과 MD와 실제 실행 근거 JSON을 문서 지정 경로의 PRIVATE main에 게시·readback하고, 변경·유료 호출·PUBLIC 배포·운영 설정은 하지 마세요.
