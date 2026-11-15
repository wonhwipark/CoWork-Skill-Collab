# PUBLIC Workspace MSC 열람 샘플 — 게시·실브라우저 검증 결과 r0001

- 확인: 2026-11-15 KST / 기존 Work `L1-WORKSPACE-RAG-20261111-001`
- 사용자 명시 요청: 실제 `wonhwipark/L1Work` GitHub의 `sample/` 폴더에 분석 문서 → HTML → MSC 열람 샘플 게시.
- 상태: **PUBLIC_SAMPLE=POSTED_REMOTE_READBACK_PASS / PAGES_DEPLOY=PASS / SAMPLE_UI_REAL_BROWSER=PASS**.
- 실제 업무용 Workspace tree/API·converter 자동 생성·스킬 저장 연동·그룹 게시의 검증 결과는 아님.

## 샘플과 게시 위치

- GitHub 폴더: https://github.com/wonhwipark/L1Work/tree/main/sample
- 브라우저 분석 문서(직접 확인 URL): https://wonhwipark.github.io/L1Work/sample/msc-workspace/index.html
- GitHub 분석 문서: https://github.com/wonhwipark/L1Work/blob/main/sample/msc-workspace/works/DEMO-MSC-001/CODE_FACTS.md
- HTML 뷰어(직접 확인 URL): https://wonhwipark.github.io/L1Work/sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/viewer.html
- PUBLIC commit `bf87f6052683cbc389a4f2349af00f0231b5bf4e`.
- Pages [#43720102625](https://github.com/wonhwipark/L1Work/actions/runs/43720102625), `completed/success`.

기존 `docs/msc-samples/index.html`의 공개 B 가상 시안에서 동일한 6 participant·36 message·3단계 SVG와 텍스트를 재사용. `DEMO-MSC-001`과 `DEMO-r0001`은 예시 식별자이며 실제 Work·source commit이 아님. 단계 2·3의 반복은 화면 비교용이며 실제 변경·해제 프로토콜을 나타내지 않음.

`sample/msc-workspace/`에 Work README·문서안내·CODE_FACTS·MSC_VIEW와 `artifacts/analysis/msc/r0001/`의 viewer.html·msc.svg·msc-preview.svg·msc.txt 배치. 첫 단계 미리보기는 같은 SVG의 viewBox로 생성. HTML 뷰어는 SVG·CSS·스크립트를 내장. 루트 README에 샘플 바로가기 추가.

기존 Pages `docs/` 게시 위치에 맞춰 `docs/sample/`에 동일 바이트의 복사본 생성. source 11개와 게시 복사본 11개, 루트 README 총 23개. 같은 입력/같은 commit으로 게시했으며 새 자동 감시·예약·동기화 작업은 만들지 않음. 기존 대시보드·과거 B 비교 시안은 보존.

## 실제 시험

| 항목 | 판정 | 근거 |
|---|---|---|
| SVG XML·participant/message/stage | PASS | 6명·36개 메시지·3단계, 원본 텍스트와 번호 대조 |
| HTML 상대 링크·이미지·뒤로가기 | PASS | 생성 폴더 전체 상대 경로 존재·경로 이탈 없음 |
| viewer JavaScript 구문·CSP hash | PASS | node --check, inline script SHA-256과 CSP 일치 |
| HTML의 내장 SVG | PASS | 독립 SVG 파일과 동일 그림 내장 |
| Pages 복사본 | PASS | source 11개와 게시 11개 바이트 동일 |
| PUBLIC 원격 readback | PASS | 23개 원격 본문·로컬 바이트 일치, Git blob SHA-1 재계산·아래 SHA-256 |
| GitHub Markdown → 미리보기 | PASS | 실제 익명 브라우저의 GitHub CODE_FACTS에서 이미지 complete=true/naturalWidth=1200 확인 |
| GitHub Markdown → HTML → MSC | PASS | 문서의 ‘MSC 확대 보기 · HTML 뷰어’ 클릭, 실제 Pages HTML에서 SVG 표시 확인 |
| 확대·축소 | PASS | 실제 클릭 100% → 120% → 100% |
| 단계 이동 | PASS | 2단계 scrollTop=665 / 3단계=1253, 표시 단계와 설명 갱신 |
| 폭 맞춤 | PASS | 실제 SVG width=1195 / viewport=1195 |
| 분석 문서 복귀·미리보기 | PASS | 실제 돌아가기 클릭 후 index.html, previewLoaded=true |
| 데스크톱 표시 | PASS | 1363×936, 분석·뷰어 양쪽 문서 가로 overflow 없음 |
| 실제 모바일 viewport·다른 브라우저·오프라인 브라우저 | NOT_RUN | responsive CSS·자원 내장은 정적 점검; 실제 기기/오프라인 시험으로 확대하지 않음 |
| 실제 업무 호스트 tree/API·converter·저장·그룹 게시 | NOT_VERIFIED / NOT_RUN | 이번 샘플은 가상 자료의 UI·열람 확인 |
| 새 독립 리뷰·스킬 설치·Job·유료 호출 | NOT_RUN | 사용자 승인한 PUBLIC 샘플·기존 Pages 게시만 수행 |

## 실제 바이트·위치

저장소 `wonhwipark/L1Work`, branch `main`, 위 PUBLIC commit의 UTF-8 파일:

| 경로 | bytes | SHA-256 |
|---|---:|---|
| `README.md` | 3316 | `4d1a334ddcd89babd99c1ab72bf483b97a515fff9dd8b8cc3d51864f07431e85` |
| `docs/sample/msc-workspace/index.html` | 10561 | `c857e81b585c82a36573822f66a61023437802be62d6ab3792b392cec7f4af68` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/README.md` | 645 | `ecdf0f55e7ea9304d564adf43d78301561aa01158f35acc924cd000286815e28` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.txt` | 1445 | `e8c27c7c27ed7ec17dad09c3336de9317f0bb66a7cac0782dde0cca9f75ebc02` |
| `sample/README.md` | 398 | `4c0f46bd2a4cfc93bce1a04adaa14d27f01712996aea2c288ff4db7b012137aa` |
| `sample/msc-workspace/works/DEMO-MSC-001/CODE_FACTS.md` | 2236 | `5453690a7bec9e23211a48eac71cdee644e72420f23999e0b2d84538c21f0c35` |
| `sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc-preview.svg` | 8764 | `138f24f7c0187321c28d7373c6e69acac038ad6b051a7bf77f80b0db7c416ccf` |
| `sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/viewer.html` | 21115 | `5812b6deaa1cbeb0f9c51b89d04e3d8a0935fea929ae6a2163ca67a0d31c432a` |
| `docs/sample/README.md` | 398 | `4c0f46bd2a4cfc93bce1a04adaa14d27f01712996aea2c288ff4db7b012137aa` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/CODE_FACTS.md` | 2236 | `5453690a7bec9e23211a48eac71cdee644e72420f23999e0b2d84538c21f0c35` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc-preview.svg` | 8764 | `138f24f7c0187321c28d7373c6e69acac038ad6b051a7bf77f80b0db7c416ccf` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/viewer.html` | 21115 | `5812b6deaa1cbeb0f9c51b89d04e3d8a0935fea929ae6a2163ca67a0d31c432a` |
| `sample/msc-workspace/README.md` | 2342 | `3be2a39c0796a9d76d7c94982f0b9bd3a6d0614e7fcf8d90823c94041b962844` |
| `sample/msc-workspace/works/DEMO-MSC-001/MSC_VIEW.md` | 442 | `935d306dc8d86527f830a2d079fd46e4269d173b286efa7b887c6851b8e01175` |
| `sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.svg` | 8766 | `37d2330ab41416913b2eccac2b2783029ed1ca4199ced24d1f4685ba30c7c1b8` |
| `sample/msc-workspace/works/DEMO-MSC-001/문서안내.md` | 645 | `c964cb69b6b78e6e74706fcb7aec4ad29c341fd2480a0c9b32aefaa1e0de1864` |
| `docs/sample/msc-workspace/README.md` | 2342 | `3be2a39c0796a9d76d7c94982f0b9bd3a6d0614e7fcf8d90823c94041b962844` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/MSC_VIEW.md` | 442 | `935d306dc8d86527f830a2d079fd46e4269d173b286efa7b887c6851b8e01175` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.svg` | 8766 | `37d2330ab41416913b2eccac2b2783029ed1ca4199ced24d1f4685ba30c7c1b8` |
| `docs/sample/msc-workspace/works/DEMO-MSC-001/문서안내.md` | 645 | `c964cb69b6b78e6e74706fcb7aec4ad29c341fd2480a0c9b32aefaa1e0de1864` |
| `sample/msc-workspace/index.html` | 10561 | `c857e81b585c82a36573822f66a61023437802be62d6ab3792b392cec7f4af68` |
| `sample/msc-workspace/works/DEMO-MSC-001/README.md` | 645 | `ecdf0f55e7ea9304d564adf43d78301561aa01158f35acc924cd000286815e28` |
| `sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.txt` | 1445 | `e8c27c7c27ed7ec17dad09c3336de9317f0bb66a7cac0782dde0cca9f75ebc02` |

## 다음 한 동작

사용자가 공개 샘플의 문서·미리보기·확대 뷰어를 확인. 실제 적용은 기존 업무 Work 하나의 폴더·converter 출력·권한 있는 HTML 열람 URL에 같은 경로를 매핑하며, 새 분석·Job 재실행이나 호스팅 변경을 이 게시로 시작하지 않음.
