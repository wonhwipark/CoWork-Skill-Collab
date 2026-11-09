# Windows Claude Code — P1/P2 사전 확인 (READ_ONLY, NO REVIEW CALL)
2026-11-10 | work_id=COWORK-DROPBOX-TO-GITHUB-MIGRATION

## 목적
기존 Windows Dropbox watcher는 그대로 둔 채 현재 운영 버전·예약 작업·단일 실행 상태·PRIVATE GitHub 접근 가능 여부를 알아내는 **호스트 사전점검**. 이 문서 게시만으로 실행이 시작되지는 않는다.

## 작업 순서
1. 현재 PC와 기존 설치 디렉터리의 실제 경로를 확인. 과거 인계 경로를 확정값으로 가정하지 말 것.
2. `collab/ops/WINDOWS_READONLY_AUDIT.ps1`을 **내용 확인 후** 로컬 격리 폴더에서 실행. watcher 홈은 실측 경로를 인자로 전달하고 결과 JSON은 로컬에만 저장.
3. 설치 버전은 패키지 metadata/코드의 진짜 버전 문자열을 **읽기만** 해서 확인. 구성파일의 내용, 인증정보, 토큰, 환경변수, 프로세스 명령행 전체, SQLite 내용은 수집/업로드 금지.
4. GitHub CLI 또는 기존 승인된 도구가 있는지와 **PRIVATE repo에 대한 읽기 권한만** 확인. 새 토큰 생성·노출·재설정/설치 금지. 403/404는 그대로 보고.
5. 기존 watcher의 활성 인스턴스 개수, 마지막 정상 동작/실패 근거, SQLite DB 존재 여부(경로와 내용은 공유하지 않음), Claude reviewer 엔트리포인트·현재 리뷰 mode를 민감 데이터 없이 요약.
6. 공유 전에 host_inventory JSON을 비식별화(필요하면 경로, 사용자명, 프로세스 ID 등 제거). 조직 반출 금지 요소가 있으면 GitHub에 게시하지 말고 `REDACTION_REQUIRED`로 보고.

## 명시적 금지
- 기존 watcher/Bridge/Dashboard/Telegram 중지·설치·설정 수정 금지.
- 모델/Claude 리뷰를 직접 호출하지 않음. 신규 REQUEST/READY 생성·게시 금지.
- GitHub clone/push 또는 원격 업로드는 별도 쓰기 승인 전 수행하지 않음. 이 문서 자체는 실행 권한이 아님.
- PRIVATE GitHub도 사내 반출 금지 자료를 받아서는 안 됨.

## 기대 결과 형식
`HOST_AUDIT_STATUS: PASS|PARTIAL|BLOCKED` / watcher_version / scheduled_task_count / watcher_process_count / github_private_read: PASS|DENIED|NOT_TESTED / sqlite_state: PRESENT|ABSENT|NOT_TESTED / gaps / next_one_action. 비밀자료와 로컬 전체 경로·로그/소스 원문을 포함하지 말 것.

## 다음 게이트
GPT가 결과를 판정한 뒤에만 GitHub adapter 소스 수정/시험 대상 확정. GitHub LIVE cutover, PUBLIC ZIP 배포, 실제 Claude 모델 리뷰는 여전히 NOT_APPROVED/NOT_RUN.
