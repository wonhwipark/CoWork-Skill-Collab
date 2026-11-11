# COWORK-GITHUB-DASHBOARD-20261111-001 — CURRENT

## 2차 GitHub 리뷰 연결·항목별 피드백 및 Actions 검증 (2026-11-11 KST)

- 사용자 실행 지시: GitHub Actions SHADOW 대시보드에 GitHub REQUEST → READY → REVIEW → RECEIPT → GPT 판정 연결, 항목별 피드백·다음 담당을 추가.
- **현재 상태:** DEVELOPMENT=IMPLEMENTED / SELF_TEST=PASS / ACTION_RUN=SUCCESS / INDEPENDENT_REVIEW=NOT_RUN / GITHUB_REAL_REVIEW_E2E=NOT_RUN / CUTOVER=MIGRATION_NOT_CUTOVER.
- **수정 파일:** collab/dashboard/review_chain.py (신규 연결기), generate.py (연결 데이터·HTML·MD에 통합), tests/test_review_chain.py (신규 9개 synthetic regression), .github/workflows/cowork-dashboard.yml (collector *.py 변경 감지), collab/dashboard/README.md (입력·보안 계약).
- **출력:** collab/dashboard/state.json (SHADOW_V2 및 review_chains[]), index.html (요청별 5단계·비차단 피드백·다음 담당), SUMMARY.md (모바일 읽기용 연결 표).
- **실제 Actions 실행:** GitHub run #42998956812 (commit 549ed2b38f31b9974b6490d25e3a36fe4a895bd2) completed=SUCCESS, Checkout/Build and test/Publish 각 단계 SUCCESS. 기존 7개 + 신규 9개 = 16개 unittest (workflow의 build/test step 성공). 이는 **합성시험**이며 실제 GitHub reviewer/영수증 실 API 시험 아님.
- **원격 직접 재조회:** state.json schema COWORK_GITHUB_DASHBOARD_SHADOW_V2, review_chains 길이 0, 3개 CURRENT 프로젝트; SUMMARY.md와 index.html에 새 연결 섹션 표시됨. GitHub 실제 요청/리뷰/영수증 0개는 **미이관**이며 Dropbox에서 완료가 0건이라는 뜻이 아님.
- **검증 안전성:** request ID/revision/ZIP digest + READY request raw SHA + REVIEW COMPLETED + RECEIPT ok/processing key + GPT JSON 결정이 일치할 때만 단계 상승. 실패/불일치 시 완료 처리 금지. GPT_DISPOSITION.json은 동작 승인 파일이 아니라 표시용 후속 판정 기록.
- **미검증:** 운영 신뢰 서명·고정 repo ID/commit pin·권한·중복 방지는 Windows watcher/승인 게이트의 별도 사항. 실제 GitHub REVIEW/RECEIPT 입력 E2E, 정식 독립 Claude 리뷰, 모바일 브라우저 E2E, Pages 운영: NOT_RUN.
- **미변경:** 기존 Dropbox LIVE, Windows watcher v0.1.5/Bridge/Dashboard/운영 SQLite·WAL·SHM, Telegram, PUBLIC L1Work, 클로드 모델 호출 0, LIVE 전환 승인 없음.
- **다음 작업:** 정식 승인된 실제 GitHub 리뷰 데이터가 PRIVATE에 안전하게 게시되면 1건 E2E를 검증한다. 검증 전까지 샘플 REQUEST/READY/RECEIPT를 main에 게시하거나 리뷰 실행으로 승격하지 않는다.

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
