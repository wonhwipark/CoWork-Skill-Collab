# CoWork GitHub Dashboard — SHADOW (PRIVATE)

**상태:** `DASHBOARD_ACTION_IMPLEMENTED / CUTOVER=MIGRATION_NOT_CUTOVER`

- **개발·판정 주체:** GPT
- **대시보드 생성:** GitHub Actions `.github/workflows/cowork-dashboard.yml`
- **입력:** 같은 PRIVATE 저장소 `collab/projects/*/CURRENT.md`, `collab/requests/`, `collab/reviews/`, `collab/receipts/`
- **출력:** `collab/dashboard/VIEW.md` (즉시 렌더링), `index.html`, `SUMMARY.md`, `state.json` (생성기 `generate.py`)
- **업데이트:** `main`에 관련 입력/생성기 변경 시 push 이벤트, 또는 Actions 화면의 `Run workflow` 수동 실행
- **이 Actions의 출력 영역:** GitHub PRIVATE만. L1Work 공개 샘플은 별도 게시된 정적 HTML이고, Windows 감시기·기존 LIVE 경로에는 쓰지 않음

## 최신 HTML 업로드 파일 (PRIVATE 스냅샷)

**[2026-11-12 협업 흐름·STATUS HTML 스냅샷](snapshots/CoWork_협업흐름_STATUS_20261112.html)** — GPT가 별도로 디자인하여 제공한 파일을 PRIVATE GitHub에 그대로 업로드했습니다. 파일 원본과 원격 본문이 정확히 일치함을 재검증했습니다.

- **저장 위치:** `collab/dashboard/snapshots/CoWork_협업흐름_STATUS_20261112.html`
- **무결성:** SHA-256 `e2530c1062540e93191ca62bcf9dd0ece1d8cdac35e0903d8e6079c047f5d9e1`, Git blob `df233dd31404735f2d41bdc0a6b0059a97d49494`.
- **주의:** 이 HTML은 고정 스냅샷입니다. **실제 자동 갱신 HTML은** `collab/dashboard/index.html`이며 GitHub Actions가 업데이트합니다. 두 HTML을 혼동하지 않습니다.
- GitHub PRIVATE는 HTML 파일을 웹페이지로 직접 호스팅하지 않으므로 다운로드 후 브라우저에서 열어야 합니다. 공개 `L1Work` Pages는 샘플 전용입니다.

## HTML 기본 확인 방식 (2026-11-12)

- **기본 산출물은 HTML:** [협업 흐름·현재 STATUS HTML](index.html) — PRIVATE GitHub의 HTML 원본. GitHub 코드 화면은 HTML을 렌더링하지 않으므로 **파일을 다운로드한 뒤 브라우저에서 열어** 실제 화면을 확인한다.
- **HTML 자동 갱신:** `.github/workflows/cowork-dashboard.yml`이 `CURRENT.md`와 GitHub 리뷰 파일 변경을 감지하면 PRIVATE `index.html`을 재생성한다.
- **보조 산출물:** [VIEW.md](VIEW.md)는 GitHub 자체 표시용이며, HTML을 다운로드하기 어려운 경우에만 사용한다.
- **공개용 L1Work Pages는 합성 샘플 전용:** PRIVATE 실제 협업 현황을 PUBLIC으로 게시하거나 자동 동기화하지 않는다. 로컬 다운로드 HTML은 생성 당시 스냅샷이므로 새로고침만으로 갱신되지 않는다.

## 현재 협업 흐름 및 검증 상태 (2026-11-12)

**[현재 협업 흐름 도식·상태표 바로 보기](VIEW.md)** — GitHub PRIVATE의 Markdown/Mermaid 렌더링을 이용하므로 HTML 다운로드 없이 확인할 수 있습니다.

- **협업 관리 환경:** GPT(범위 정의·최종 판정) + GitHub PRIVATE(REQUEST/READY·결과·영수증) + GitHub Actions(상태 읽기·화면 갱신).
- **업무 실행 환경:** Windows Python watcher(승인·신뢰·비용·중복 가드) + Claude Code(독립 리뷰). 호스트 설치와 독립 검토는 별도 증거 및 승인 게이트.
- 화면은 **현재 기존 LIVE 경로**와 **향후 GitHub 목표 경로**를 구분하며, `CURRENT.md` 최신 섹션의 `WINDOWS_STAGE1_EXECUTION`, `INDEPENDENT_REVIEW`, `CUTOVER`, `GITHUB_PAGES_DEPLOY` 기록을 읽습니다. 오래된 PASS 구간을 최신으로 승격하지 않습니다.
- 신규 `flow_view.py`가 반응형 7단계 HTML 흐름, Mermaid 도식, 운영 STATUS 표를 생성합니다. GitHub 관측 파일 수는 운영 리뷰 완료 수가 아닙니다.
- **공개 [L1Work 샘플 HTML](https://wonhwipark.github.io/L1Work/cowork-dashboard/)**은 실제 진행 상태를 포함하지 않는 별도 페이지입니다. PRIVATE 현황을 PUBLIC에 동기화하지 않습니다.

## 클릭 한 번으로 보기 (PRIVATE)

**[대시보드 바로 보기 — GitHub 화면에서 즉시 표시](VIEW.md)**

이 링크는 GitHub가 직접 렌더링하는 Markdown 대시보드입니다. PRIVATE 저장소 권한이 있는 로그인 사용자만 확인할 수 있습니다. 기존 HTML 파일의 코드 화면을 여는 방식과 다릅니다. GitHub Pages나 PUBLIC 게시 없이 GitHub Actions가 `VIEW.md`를 함께 자동 갱신합니다.

## 별도 공개 샘플 HTML (실제 현황과 분리)

**[공개용 후보 HTML 소스 — PRIVATE에서만 접근](public_preview/index.html)** · [생성기와 보안 기준](public_preview/README.md) · [PUBLIC 배포 승인 게이트](public_preview/PUBLIC_RELEASE_GATE.md)

- 공개용 HTML을 별도로 구현하고 PRIVATE Actions에서 생성·보안 시험합니다.
- 이 후보는 **정적 예시 화면**으로 실제 Work, REQUEST, REVIEW, RECEIPT, GPT 판정, 링크, 수치, 운영 현황을 읽거나 포함하지 않습니다.
- PRIVATE 원본 후보는 이 저장소에 남아 있습니다. 승인된 샘플 치환본만 L1Work PUBLIC Pages에 별도로 게시했습니다.
- **실제 협업 상태·새 후보의 추가 PUBLIC 게시**는 별도 명시적 승인 전 금지입니다.

## 사용자 확인 방법

1. [클릭 한 번에 열리는 대시보드](VIEW.md) — GitHub 모바일/웹에서 바로 표시. [GitHub에서 읽는 요약](SUMMARY.md) — GitHub 모바일/웹에서 바로 확인할 Markdown.
2. [HTML 대시보드](index.html) — 파일 다운로드 후 브라우저에서 표시할 수 있는 정적 HTML. GitHub 코드 화면에서는 HTML 렌더링이 제한될 수 있음.
3. [자동 갱신 워크플로](../../.github/workflows/cowork-dashboard.yml) — Actions의 해당 run 결과/로그로 갱신 성공 확인.

## 실행 권한·보안

- GitHub Actions는 **이미 PRIVATE 저장소에 들어온 자료만** 수집하며, 외부 API·Dropbox·Claude Code·토큰/운영 DB를 읽지 않는다.
- GitHub 파일 존재는 리뷰 승인/실행 완료가 아니다. REQUEST·리뷰·영수증은 **관측된 파일 수만 표시**하며, 미이관은 미확인으로 처리한다.
- 출력은 HTML escape + 소스 링크 도메인 제한; 생성 시 임의 코드/Markdown HTML을 실행하지 않음.
- Action의 `contents: write`는 PRIVATE `main`의 위 세 출력 파일을 갱신하는 데 사용한다. `git push`는 비강제이며 경쟁 커밋이 있으면 실패 후 수동 재실행.
- Dashboard 갱신은 reviewer REQUEST/READY를 만들지 않고, Claude 모델을 호출하지 않으며, 자동 배포를 승인하지 않는다.
- 기존 Dropbox LIVE 및 Windows watcher/Bridge/예약 작업은 **별도 명시적 전환 승인 전 그대로** 유지한다.
- PRIVATE 저장소 Pages는 활성화하지 않습니다. L1Work PUBLIC Pages는 별도의 승인된 **합성 샘플**만 게시하며 PRIVATE 운영 현황은 공개하지 않습니다.

## 시험과 현재 한계

- `python3 -m unittest discover -s collab/dashboard/tests -v` (표준 라이브러리 테스트).
- `python3 collab/dashboard/generate.py` (로컬 수동 생성, 실제 운영 입력은 본 PRIVATE 저장소의 파일에 한정).
- 실제 GitHub Action run 및 자동 push 성공은 **워크플로 실행 이력으로 별도 확인**해야 한다.
- GitHub 리뷰 워처 LIVE 전환·서명/영수증 검증·Windows 설치·재로그인/장기 운영과 본 SHADOW UI를 혼동하지 않는다.


## 2차 — GitHub 리뷰 연결 및 항목별 피드백 (2026-11-11)

- 개발 주체 GPT. 생성기는 collab/dashboard/review_chain.py의 읽기 전용 GitHub 문서 연결 검사를 호출한다.
- 입력: collab/requests/ID/REQUEST.md 및 READY.md, collab/reviews/ID/REVIEW_RESULT_1.md, collab/receipts/ID/RECEIPT_1.md, collab/reviews/ID/GPT_DISPOSITION.json.
- 출력: state.json의 review_chains, SUMMARY.md의 요청별 진행 단계·판정·피드백, index.html의 5단계 카드 및 다음 담당자.
- REQUEST의 request_id·request_revision·package_sha256이 폴더 및 다음 문서와 일치해야 한다.
- READY의 request_sha256은 REQUEST.md 원본 UTF-8 SHA-256과 일치해야 한다. READY 자체는 실행 승인 아님.
- REVIEW_RESULT의 responds_to_request_id/revision, package_sha256, execution_status=COMPLETED가 일치해야 한다.
- RECEIPT의 request_id/revision/package_sha256, ok=true, processing_key=id|revision|sha|positive_revision을 대조한다. 결과의 review_id가 있으면 processing_key와도 일치해야 한다.
- GPT_DISPOSITION.json은 request_id, request_revision, package_sha256, verdict, findings 배열을 갖는다. verdict/decision 허용값: ACCEPT, ACCEPT_WITH_CHANGE, REJECT, DEFER, NEED_INFO. findings의 각 항목은 id(B-1/N-1 등), decision, summary로 구성한다.
- 리뷰 파일에서 발견한 피드백은 GPT_DISPOSITION.json이 없으면 NOT_ADJUDICATED로 표시한다. 서명·신뢰루트·GitHub repo/commit pin 검증은 별도 Windows watcher 책임이므로 문서 연결을 운영 완료로 해석하지 않는다.
- REVIEW/RECEIPT/판정 파일 중 하나라도 불일치하면 뒤 단계는 PASS로 표시하지 않는다. 승인·추가 과금·자동 재리뷰를 발생시키지 않는다.
- 파일명/경로 검증, symlink 제외, 크기 제한, HTML escape, PRIVATE GitHub 원문 링크만 지원. GitHub Pages, PUBLIC, 외부 API, Windows 감시기·운영 DB 접근 없음.
- 기존 7개 + 리뷰 연결 합성 시험 9개로 총 16개 unittest. 실제 GitHub review E2E는 아직 NOT_RUN. 샘플 요청·영수증을 LIVE main에 허위 게시하지 않는다.
- CUTOVER=MIGRATION_NOT_CUTOVER. Dropbox LIVE 유지. 이 화면의 GitHub 리뷰 0건은 이전 Dropbox 리뷰 완료 0건을 뜻하지 않는다.
