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


## 2026-11-10 과도기 정확성 보충 (GPT / DRAFT ONLY)
- 상단 §4의 `request_id|revision|package_sha256|review_attempt`는 **구형 오프라인 프로토타입의 예**이며 실제 Windows watcher 처리키가 아니다. Windows v0.1.5 실측 처리키는 `request_id|revision|package_sha256|local_policy_revision`였다고 Claude가 보고했다. 최신 v0.2.3은 별도 불변 `logical_request_id=request_id|revision|package_sha256`로 provider/정책 개정에 의한 중복을 막는 방향. 운영키를 승인 전 임의 이행하지 않는다.
- GitHub 승인 서명은 외부 고정 신뢰 루트에서 검증할 것. GitHub READY 존재·GitHub 쓰기권한·브랜치/작성자 명의는 실행 승인 근거가 아님. 상세 B-7 초안 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md`와 설계 r0002를 대조한다.
- Commit B의 원자성은 API에 따라 달라진다. Contents API로 여러 파일을 쓰면 READY만 마지막에 게시해야 하며, 원자적 다중파일 보장을 주장하지 않는다. READY의 commit B SHA를 서명 자기 참조에 넣지 않는다.
- 최신 단계·시험 결과는 이 정적 계약의 과거 상태 문구보다 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`가 우선. 현재 LIVE는 여전히 Dropbox이고 GitHub 실제 정식 리뷰는 NOT_RUN.
