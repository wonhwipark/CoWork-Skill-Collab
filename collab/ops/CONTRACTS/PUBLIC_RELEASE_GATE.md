# PRIVATE → PUBLIC 최종 ZIP 배포 게이트 — DRAFT / NOT_ACTIVE
2026-11-10

- PRIVATE: 개발 후보·설계·리뷰·영수증·판정·대시보드.
- PUBLIC: `wonhwipark/L1Work` 저장소 **기존 루트 ZIP 경로**에 사내 무인증으로 내려받을 수 있는 **승인된 최종 ZIP만**.
- 공개 게시 필수: ZIP 원본 SHA-256·크기·CRC·경로/심링크·중첩 아카이브·민감정보/사내 자료 검사, 릴리스 채널/테스트/독립 리뷰 결과/GPT 판정, 해당 ZIP 공개 승인 확인.
- `development_not_for_deployment`, `review-candidate`, `NOT_APPROVED` ZIP은 PUBLIC 게시 차단.
- 기존 경로에 같은 이름이 있을 때 SHA 동일 = ALREADY_PUBLISHED(새 commit 0), SHA 다름 = RELEASE_PATH_COLLISION(덮어쓰기 0).
- 공개 게시 후 실제 ZIP 재다운로드 SHA 대조, 사내 Skill-Updater의 무인증 다운로드 별도 확인.
- PUBLIC에는 REQUEST/READY/원본 리뷰/영수증/내부 경로·토큰·Private 운영 자료를 게시하지 않는다.
- Windows watcher는 PUBLIC write 권한이 없어야 한다. 별도 Publisher와 사용자 배포 승인 필요.
- GitHub commit/blob SHA는 ZIP SHA-256과 다르다. 소급 삭제는 Git 역사/clone을 지우지 못한다.

**상태:** 게이트 설계. 자동 Publisher, 공개 ZIP 게시, 사내 E2E = NOT_RUN.
