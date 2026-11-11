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
