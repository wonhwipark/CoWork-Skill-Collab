# CoWork 공개 샘플 GitHub Pages 배포 게이트 — 최신 판정
기준: 2026-11-11 23:49 KST

## 승인 및 실제 상태
- `CONTENT_APPROVAL=GRANTED_FOR_FIXED_SYNTHETIC_SAMPLE_ONLY`: 사용자에게서 기존 합성 샘플의 공개 업로드 지시를 받음.
- `HOSTING_APPROVAL=GRANTED_FOR_GITHUB_PAGES_SAMPLE_ONLY`: 실제 데이터를 제외한 샘플 페이지 1개를 GitHub Pages에 게시하는 범위.
- `PUBLICATION=BLOCKED_NOT_PUBLISHED`: Pages 설정 미활성/사이트 조회 404로 실제 배포 실패.
- `PAGES_ARTIFACT_UPLOAD=SKIPPED`, `PAGES_DEPLOY=SKIPPED`, `PUBLIC_HOST_E2E=NOT_RUN`.
- `CUTOVER=MIGRATION_NOT_CUTOVER`: Dropbox LIVE를 유지하며 Windows watcher·운영 DB를 변경하지 않음.

## 정확한 고정 콘텐츠
- PRIVATE `main` 후보: `collab/dashboard/public_preview/index.html`, 4,754 bytes, SHA-256 `6acf4bc151dc292e32d97a03479784b26f0384c61aef59f99120867c1d239786`.
- 승인 후 Pages Actions는 **원본 바이트가 정확히 일치할 때만** 공개용 아티팩트로 변환. 출력 `index.html`은 안내 문구 4곳만 수정한 정적 합성 샘플(이번 실행 4,765 bytes / SHA-256 `40a33950e4fc37ed643522ed06b73ea89afdd9b4c0447417d67bc19501c82779`).
- 생성기 자체의 원본 `data-release=NOT_APPROVED` 표기는 개발 후보의 고정 과거 상태이며, 외부 배포 출력에는 `PUBLIC_SAMPLE_APPROVED`를 기입한다.
- PRIVATE의 `CURRENT.md`, 요청/리뷰/영수증·실제 통계·계정·경로·하이퍼링크는 **공개 아티팩트에 포함하지 않는다**.

## 실행 증거 및 차단
- Pages workflow: `.github/workflows/cowork-public-preview-pages.yml` (PRIVATE `main`), commit `7b251a336ed1184e90682495e5d79652260d22a2`.
- [Actions run #43042181335](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43042181335): 승인 후보 해시 검증·1개 파일 스테이징 PASS; Pages 구성 FAIL (404 Not Found); 실제 업로드·배포 SKIPPED.
- 블로커 해소는 GitHub 저장소 `Settings → Pages → Build and deployment → Source = GitHub Actions` 설정. PRIVATE 저장소 Pages 사용 가능 요금제인지 확인해야 한다.
- PUBLIC `wonhwipark/L1Work`에는 HTML을 올리지 않는다. PRIVATE 전체 내용이 Pages로 복제되지 않도록 1개 파일만 허용한다.
- Pages 활성화 후 같은 workflow 수동 1회 실행, **실제 URL 응답·웹페이지 SHA 검증 후에만** `PUBLICATION=PASS` 기록.

## 승인되지 않은 별도 작업
- 실제 REQUEST/READY/REVIEW/RECEIPT, Work ID·담당자·결함 원문·운영 실시간 수치의 공개 연동.
- 향후 변경된 후보의 자동 무조건 공개, PRIVATE 협업 문서/비밀/사내 반출 금지 자료의 공개, 운영 키/토큰, Windows watcher/DB 변경, Dropbox LIVE 종료.
- 이 항목들은 각각 별도 보안·허용 필드 심사와 명시 승인 전까지 차단한다.

## 최신 상세 보고
`collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/PUBLIC_PAGES_ATTEMPT_AND_FINAL_STATUS_20261111.md`
