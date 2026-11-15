# PRIVATE → PUBLIC 최종 ZIP 배포 게이트 — DRAFT / NOT_ACTIVE

## Job-list / Skill-Updater 전달 정본 (2026-11-12 보완)

- 운영 세부 계약: [`JOBLIST_PUBLIC_DELIVERY_V1.md`](JOBLIST_PUBLIC_DELIVERY_V1.md). 사내 Skill-Updater가 내려받는 전달 ZIP의 목적지는 **`wonhwipark/L1Work/main` 루트**. PRIVATE 개발 후보 ZIP은 설치·실행 전달 경로가 **아님**.
- Job-list에서 신규 ZIP은 사내 업데이트 감지 신호가 될 수 있으므로 **활성 One-shot Job·실제 Profile·승인·검증·원격 재조회**가 준비된 최종 ZIP만 PUBLIC 게시. `jobs: []` 비활성 후보를 무인 Job 전달 성공으로 오인하지 않는다.
- 사용자가 PUBLIC 배송을 지시했더라도 **필수 배포 게이트 실패는 `PUBLIC_RELEASE=BLOCKED/NOT_POSTED`**로 보고하고 PRIVATE 배송으로 대체하지 않는다. 개발/시험과 승인·배송, 설치, 활성화, 실행, 결과 조회는 각각 별도 상태.

## 2026-11-15 승인된 읽기 전용 디버깅 ZIP — 사후 리뷰·호스트 검증

- [상세 계약 8절](JOBLIST_PUBLIC_DELIVERY_V1.md)에서 사용자 승인된 `job-list_v0_4_38_1115.zip` NR L1 Tx Init RACH 읽기 전용 디버깅 릴리스는 **배포 전 원본 무결성·보안·호환성·회귀시험 PASS 및 명시적 PUBLIC 승인**을 충족한 경우, **Claude Code 독립 리뷰 / Linux 호스트 G0·기존 장애 복구·MCP E2E는 게시 후 확인**한다. 이 미완료 항목만으로 PUBLIC 게시를 차단하지 않는다.
- 배포 시 `INDEPENDENT_REVIEW=POST_RELEASE_PENDING`, `HOST_G0=POST_RELEASE_PENDING`, `PUBLIC_RELEASE=POSTED`를 독립 기록한다. 검증 실패·리뷰 지적은 신규 버전의 새 ZIP으로 보완하며 기존 이름의 ZIP/소비된 Job을 덮어쓰거나 재실행하지 않는다.
- **예외 범위는 현재 사용자 지정 Job-list 디버깅 배포만**이다. 쓰기·LIVE·운영 변경, 민감정보·계약 미확인 무제한 실행, 타 스킬에 대한 일반 배포 게이트 해제는 승인되지 않았다. 공개 전 ZIP CRC·manifest·path/symlink·비밀 스캔, 한 개 신규 Job/비수정 권한 및 fail-closed 검증이 실패하면 배포 금지.

## 사내 계약 조사용 제한적 READ_ONLY_BOOTSTRAP_ONE_SHOT (2026-11-12)

- `JOBLIST_PUBLIC_DELIVERY_V1.md` 6절 조건에 한해, 사내에서만 가능한 설치 계약·독립 리뷰의 **사전 G0 탐색을 위해** 사용자 명시 승인된 읽기 전용 활성 One-shot ZIP을 PUBLIC 루트에 먼저 게시할 수 있다.
- 이때 외부에서 요구되는 것은 바이트·보안·정적/회귀시험·한 건의 고정 활성 Job·무인 FAIL-CLOSED 동작·원격 재다운로드 검증. 실호스트 설치/Skill 호출·MSC 완성/독립 리뷰는 **사내에서 수행할 후속 항목**이므로 PASS로 표기하지 않는다.
- `READ_ONLY_BOOTSTRAP_ONE_SHOT`은 **운영 쓰기/배포 승인 일반화가 아님**. 기존 소스·그룹 Knowledge·운영 DB/설정 수정, 사내 민감 자료 반출, 무승인 외부 게시, 임의 CLI 실행 및 미완료 리뷰의 소급 PASS 금지.
- `job-list_v0_4_36_1112.zip`: 사용자 승인된 최초 적용 사례. 공개 배송 POSTED, 호스트 결과 NOT_VERIFIED. v0.4.35 비활성 후보와 구분.

2026-11-10

- PRIVATE: 개발 후보·설계·리뷰·영수증·판정·대시보드.
- PUBLIC: `wonhwipark/L1Work` 저장소 **기존 루트 ZIP 경로**에 사내 무인증으로 내려받을 수 있는 **승인된 최종 ZIP만**.
- 공개 게시 필수: ZIP 원본 SHA-256·크기·CRC·경로/심링크·중첩 아카이브·민감정보/사내 자료 검사, 릴리스 채널/테스트/독립 리뷰 결과/GPT 판정, 해당 ZIP 공개 승인 확인.
- 일반 정식 릴리스의 `development_not_for_deployment`, `review-candidate`, `NOT_APPROVED` ZIP은 PUBLIC 게시 차단. **사용자가 승인한 Job-list v0.4.38 디버깅 ZIP은 공개 전에 메타데이터/문구를 디버깅 배송본으로 정리하고 사전 안전시험 PASS 후, 리뷰 및 Linux G0는 공개 후 검증** (상세 계약 8절). 미검증 개발 후보 바이트를 그대로 최종본이라고 주장하지 않는다.
- 기존 경로에 같은 이름이 있을 때 SHA 동일 = ALREADY_PUBLISHED(새 commit 0), SHA 다름 = RELEASE_PATH_COLLISION(덮어쓰기 0).
- 공개 게시 후 실제 ZIP 재다운로드 SHA 대조, 사내 Skill-Updater의 무인증 다운로드 별도 확인.
- PUBLIC에는 REQUEST/READY/원본 리뷰/영수증/내부 경로·토큰·Private 운영 자료를 게시하지 않는다.
- Windows watcher는 PUBLIC write 권한이 없어야 한다. 별도 Publisher와 사용자 배포 승인 필요.
- GitHub commit/blob SHA는 ZIP SHA-256과 다르다. 소급 삭제는 Git 역사/clone을 지우지 못한다.

**상태:** 게이트 설계. 자동 Publisher, 공개 ZIP 게시, 사내 E2E = NOT_RUN.
