# 사용자 승인 기록 — 기존 Dropbox 리뷰 감시기 안전 비활성화
작성일: 2026-11-12 KST | r0001
REPO: PRIVATE `wonhwipark/CoWork-Skill-Collab` | BRANCH: `main`
WORK: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
AUTHORIZATION: **APPROVED_FOR_WINDOWS_HOST_CONDITIONAL_EXECUTION**
EXECUTION: **NOT_YET_OBSERVED** (문서 게시 자체는 Windows 작업 실행 아님)

## 명시 승인 근거·범위
사용자는 Dropbox 협업을 더 이상 사용하지 않는다고 명시하고, GPT의 다음 질문 — “기존 Dropbox 리뷰 감시기를 안전하게 중지하고 예약 작업을 Disable하되 기존 DB·요청·리뷰·영수증을 보존하는 방향으로 진행할까요?” — 에 **“그래”**라고 답했다.

**승인**:
- Windows 호스트 **기존 Dropbox 리뷰 감시기 1개**의 실제 예약 작업 이름·실행 파일 경로·유관 PID를 먼저 실측한다.
- 새/불확실 작업의 소실 또는 중복 reviewer 호출 위험이 없고 rollback/백업·종료 증거 준비가 된 경우에만, 해당 기존 예약 작업 **Disable + 기존 감시기 프로세스 안전 중지**.
- 기존 요청/결과/영수증/DB main·WAL·SHM/로그/버전·작업 정의를 **삭제·덮어쓰기 없이 로컬 보호된 별도 저장소에 보존**하고 복구 가능성 검증.
- 프로세스 종료, 트리거 재시작 차단, 신규 reviewer 모델 호출 0을 확인. 결과 MD 및 `CURRENT.md`, `TRACKER.json`을 PRIVATE main에 PR 없이 게시 및 readback.

**미승인**:
- 대시보드 갱신기, notifier, Bridge, Windows Dispatcher, 그 외 예약 작업·서비스 종료/Disable/설정 변경.
- Dropbox 원본 요청/READY/review/영수증/ZIP/운영 DB 삭제·정리·데이터 변경, 미정산 작업 자동 REJECT/HOLD/재실행, 모델 리뷰 새 호출, 텔레그램 임의 발송.
- 실 운영 key/PAT/신뢰 루트, 운영 스키마/메시지, watcher 새 버전 설치, `pythonw.exe` 전환, GitHub LIVE 활성화, PUBLIC 게시.
- GitHub LIVE 승인이나 C/ETW 안전성 PASS 소급. 
- 원본 사내 코드·로그·토큰/DB의 GitHub PRIVATE 업로드(금지).

## 안전 조건 및 상태 표현
- 실행 직전 리뷰 인플라이트/미정산·불확실 작업/잔여 유효 승인 READY/기본 정책·비용/서명/중복 방지 확인. **불분명하면 중지하지 않고 BLOCKED**, 정보와 필요한 다음 허가만 보고.
- 단일 실제 인스턴스 확인(런처+자식 PID 포함), 자동복구 트리거 확인. 정상 종료 수단이 없으면 종료 안전성 확인 후 기존 작업 Stop만 허용, 운영 DB/WAL/SHM 직접 편집/임의 프로세스 강제 종료 금지.
- 백업의 **실제 일관성**과 원격 반출 분류를 구분. VSS/운영 DB 잠금 위험이 있어 안전 보존 증명 불가하면 `BLOCKED_BACKUP_CONSISTENCY`로 처리하고 다음 단계로 넘어가지 않는다.
- 성공 시 `DROPBOX_WATCHER=DISABLED_ARCHIVED`, `ACTIVE_PROVIDER=NONE`, `CUTOVER=MIGRATION_NOT_CUTOVER` (자동 리뷰 없음, 새 GitHub LIVE 아님). 실패/부분 실행은 관측한 개별 상태만 적고 성공으로 보고하지 않는다.
- 운영 복구/재활성화는 이 승인에 포함되지 않는다. 실패한 Disable을 임의 재시작하여 reviewer 호출 위험을 만들지 않는다.

## 실행 인계서
`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/WINDOWS_DROPBOX_WATCHER_SAFE_DISABLE_ONE_SHOT_r0001_20261112.md` 참조. 해당 경로는 별도 문서이며 게시만으로 자동 실행하지 않는다.
