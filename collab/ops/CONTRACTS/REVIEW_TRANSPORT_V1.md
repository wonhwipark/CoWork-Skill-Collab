# GitHub Review Transport Contract — DRAFT / NOT_ACTIVE
2026-11-10 | 기존 Dropbox 리뷰 운영과 분리

1. PRIVATE `main`의 검증된 신규 READY만 GitHub watcher 탐색 후보. PR, issue, fork, ZIP, 문서 변경은 실행 신호가 아니다.
2. Commit A: ZIP·REQUEST·mode·지식 근거를 게시한 뒤 **원본 바이트·크기·SHA-256 및 Git commit pin** 확인.
3. Commit B: 원격 검증 성공 시 READY를 마지막에 신규 게시. REQUEST/READY ID·revision·SHA 정확히 연결.
4. `request_id|revision|package_sha256|review_attempt` 등 정책상 승인된 처리키로 로컬 SQLite 영속 상태 및 단일 실행 잠금 구현. 이전 Dropbox 처리 기록과 충돌/중복 검사.
5. 중단/실패 시 `REVIEW_UNCERTAIN`을 기본으로 모델 재호출 금지. 결과/영수증 게시만 재시도할 수 있다.
6. `SHADOW_READ_ONLY`는 모델/쓰기/알림 0회. `ACTIVE_PROVIDER`는 운영 중 정확히 하나만.
7. 실제 Claude 리뷰, 리뷰 결과와 영수증 원격 readback, Telegram 알림, GPT 판정은 별도 관찰·상태로 기록.
8. 실행 모드 기본 SEMI_AUTO. AUTO_PENDING_SETUP에서 Work 자동 진행 금지.
9. Windows GitHub 인증·권한은 GPT 권한과 다르다. 토큰은 저장소나 로그에 게시 금지.
10. 정책 상한 STATIC $1 / LARGE $3 / XLARGE $6. 사용자의 별도 승인 없이 상향 금지.

**상태:** 설계안만 기록. GitHub watcher 구현/테스트/설치/실 리뷰 NOT_RUN. 이 문서는 REQUEST/READY가 아니며 Claude 호출을 유발하지 않는다.
