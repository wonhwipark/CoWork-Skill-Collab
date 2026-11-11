# 공개 배포 게이트 — Fail Closed

- `CANDIDATE_STATUS=DEVELOPMENT_PREVIEW`
- `DATA_SOURCE=STATIC_SYNTHETIC_ONLY`
- `CONTENT_APPROVAL=NOT_GRANTED`
- `HOSTING_APPROVAL=NOT_GRANTED`
- `PUBLICATION=NOT_RUN`
- `CUTOVER=MIGRATION_NOT_CUTOVER` (기존 Dropbox LIVE 유지)

## 현재 허용
PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`에 공개용 HTML 후보·소스·시험·보고서 기록. 기존 PRIVATE GitHub Actions로 후보만 생성하고 검증. 로컬 다운로드 HTML 미리보기.

## 추가 명시적 승인 없이는 금지
PUBLIC `wonhwipark/L1Work`, GitHub Pages, 외부 호스팅, 공개 Artifact/CDN 게시. PRIVATE 협업 데이터·계정·프로젝트 ID·이슈·리뷰·영수증·토큰·경로·메타데이터 노출. 운영 키/토큰 발급, Windows watcher/운영 DB 변경, LIVE 전환.

## 최종 공개 판정 조건
공개 대상 파일 SHA-256/크기, 허용 필드, 민감정보 검사, 공개 위치, 사용자 승인 및 롤백이 모두 명시되어야 합니다. 승인되지 않은 향후 개정본 자동 게시 금지.
