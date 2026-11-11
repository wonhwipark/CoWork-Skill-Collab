# CoWork GitHub Dashboard — SHADOW (PRIVATE)

**상태:** `DASHBOARD_ACTION_IMPLEMENTED / CUTOVER=MIGRATION_NOT_CUTOVER`

- **개발·판정 주체:** GPT
- **대시보드 생성:** GitHub Actions `.github/workflows/cowork-dashboard.yml`
- **입력:** 같은 PRIVATE 저장소 `collab/projects/*/CURRENT.md`, `collab/requests/`, `collab/reviews/`, `collab/receipts/`
- **출력:** `collab/dashboard/index.html`, `SUMMARY.md`, `state.json` (생성기 `generate.py`)
- **업데이트:** `main`에 관련 입력/생성기 변경 시 push 이벤트, 또는 Actions 화면의 `Run workflow` 수동 실행
- **영역:** GitHub PRIVATE만. 공개 Pages, PUBLIC `L1Work`, Windows 및 Dropbox LIVE에는 게시하지 않음

## 사용자 확인 방법

1. [GitHub에서 읽는 요약](SUMMARY.md) — GitHub 모바일/웹에서 바로 확인할 Markdown.
2. [HTML 대시보드](index.html) — 파일 다운로드 후 브라우저에서 표시할 수 있는 정적 HTML. GitHub 코드 화면에서는 HTML 렌더링이 제한될 수 있음.
3. [자동 갱신 워크플로](../../.github/workflows/cowork-dashboard.yml) — Actions의 해당 run 결과/로그로 갱신 성공 확인.

## 실행 권한·보안

- GitHub Actions는 **이미 PRIVATE 저장소에 들어온 자료만** 수집하며, 외부 API·Dropbox·Claude Code·토큰/운영 DB를 읽지 않는다.
- GitHub 파일 존재는 리뷰 승인/실행 완료가 아니다. REQUEST·리뷰·영수증은 **관측된 파일 수만 표시**하며, 미이관은 미확인으로 처리한다.
- 출력은 HTML escape + 소스 링크 도메인 제한; 생성 시 임의 코드/Markdown HTML을 실행하지 않음.
- Action의 `contents: write`는 PRIVATE `main`의 위 세 출력 파일을 갱신하는 데 사용한다. `git push`는 비강제이며 경쟁 커밋이 있으면 실패 후 수동 재실행.
- Dashboard 갱신은 reviewer REQUEST/READY를 만들지 않고, Claude 모델을 호출하지 않으며, 자동 배포를 승인하지 않는다.
- 기존 Dropbox LIVE 및 Windows watcher/Bridge/예약 작업은 **별도 명시적 전환 승인 전 그대로** 유지한다.
- GitHub Pages는 PRIVATE 저장소와 관계없이 외부 노출 위험이 있을 수 있어 **활성화하지 않는다**.

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
