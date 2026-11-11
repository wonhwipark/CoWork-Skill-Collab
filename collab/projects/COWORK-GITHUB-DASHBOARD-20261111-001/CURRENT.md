# COWORK-GITHUB-DASHBOARD-20261111-001 — CURRENT

## GitHub Actions SHADOW 대시보드 1차 구현 (2026-11-11 KST)

- **현재 상태:** `DEVELOPMENT=IMPLEMENTED`, `SELF_TEST=PASS`, `ACTION_RUN=SUCCESS_OBSERVED`, `INDEPENDENT_REVIEW=NOT_RUN`, `LIVE_CUTOVER=MIGRATION_NOT_CUTOVER`.
- **담당:** GPT 개발·시험·최종 판정 / GitHub Actions 대시보드 빌드·PRIVATE 게시 / Windows Claude Code 독립 리뷰는 별도 유효 요청 시 진행.
- **대상 저장소/브랜치:** `wonhwipark/CoWork-Skill-Collab` PRIVATE `main`.
- **소스:** `collab/dashboard/generate.py`.
- **워크플로:** `.github/workflows/cowork-dashboard.yml` (push: 관련 CURRENT/requests/reviews/receipts/생성기/워크플로 변경; 수동 workflow_dispatch).
- **실제 생성물:** `collab/dashboard/index.html`, `SUMMARY.md`, `state.json`.
- **테스트:** `collab/dashboard/tests/test_generate.py` 7개 로컬 PASS; GitHub Actions 42954499889의 Build/Test 및 PRIVATE Publish 단계가 모두 SUCCESS.
- **원격 관측:** HTML 2개 CURRENT 프로젝트 및 GitHub 파일 관측 수(REQUEST 0/REVIEW 0/RECEIPT 0), 상태 `MIGRATION_NOT_CUTOVER`. Dropbox에서 미이관된 데이터는 완결 0건이 아니라 UNKNOWN.
- **비용·권한:** Actions는 GitHub 자체 런타임 사용; Claude 리뷰 모델 호출 없음. `GITHUB_TOKEN`의 `contents:write`는 PRIVATE 대시보드 산출물 자동 갱신에만 사용, 외부 API/Pages/PUBLIC 발행 없음. 실행 권한은 소스·기본 브랜치 접근 통제에 종속.
- **보안:** 검증되지 않은 리뷰 파일을 승인 증거로 승격하지 않음. 템플릿 HTML 이스케이프/프로젝트 경로 검증/대상 파일 크기 상한; 내용의 원본 전체 복제 금지. push는 비강제/동시성 제한, 결과가 동일하면 no-op.
- **한계:** GitHub에 REQUEST/REVIEW/RECEIPT 원본은 아직 이관되지 않았으며, GitHub watcher LIVE·Windows 호스트 SHADOW·독립 Claude 정적 리뷰·Private Pages 노출 검토·모바일 브라우저 E2E = NOT_RUN. 이전 Dropbox LIVE 및 Windows 운영 감시기/DB/Bridge/Telegram에 변화 없음.
- **표시 방식:** PRIVATE GitHub `SUMMARY.md`는 모바일/웹에서 즉시 읽기 가능. `index.html`은 GitHub 소스 미리보기에서 실행되지 않으므로 브라우저로 다운로드해 열어야 함. GitHub Pages는 게시하지 않음.
- **다음 한 동작:** 이후 GitHub 협업 자료가 실제로 PRIVATE에 이관되면 상태별 파일 집계를 확대하고, 검증된 영수증/승인 레이어를 별도 구현한다. 기존 LIVE cutover 승인과는 분리.
