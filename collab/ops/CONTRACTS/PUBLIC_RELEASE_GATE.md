# PRIVATE → PUBLIC 최종 ZIP 배포 게이트 — DRAFT / NOT_ACTIVE

## Job-list / Skill-Updater 전달 정본 (2026-11-12 보완)

- 운영 세부 계약: [`JOBLIST_PUBLIC_DELIVERY_V1.md`](JOBLIST_PUBLIC_DELIVERY_V1.md). 사내 Skill-Updater가 내려받는 전달 ZIP의 목적지는 **`wonhwipark/L1Work/main` 루트**. PRIVATE 개발 후보 ZIP은 설치·실행 전달 경로가 **아님**.
- Job-list에서 신규 ZIP은 사내 업데이트 감지 신호가 될 수 있으므로 **활성 One-shot Job·실제 Profile·승인·검증·원격 재조회**가 준비된 최종 ZIP만 PUBLIC 게시. `jobs: []` 비활성 후보를 무인 Job 전달 성공으로 오인하지 않는다.
- 사용자가 PUBLIC 배송을 지시했더라도 **필수 배포 게이트 실패는 `PUBLIC_RELEASE=BLOCKED/NOT_POSTED`**로 보고하고 PRIVATE 배송으로 대체하지 않는다. 개발/시험과 승인·배송, 설치, 활성화, 실행, 결과 조회는 각각 별도 상태.

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
