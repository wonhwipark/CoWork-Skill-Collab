# GPT 판정 — 잔여 Dropbox 의존성 감사 및 Bridge·갱신기 정리 준비
기준일: 2026-11-13 KST | rev: r0001
저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` | 브랜치: `main`
work_id: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
상태: **AUDIT_ACCEPTED / STOP_DISABLE_APPROVAL_REQUIRED / WINDOWS_CHANGES=0**
이 문서는 새 Windows 작업의 실행 승인이나 LIVE 전환 승인이 아니다.

## 1. 근거
- GPT가 `CLAUDE_POST_DROPBOX_DISABLE_DEPENDENCY_AUDIT_RESULT_FOR_GPT_20261113.md` 및 최신 `CURRENT.md`를 원격에서 직접 확인. 결과 Git blob SHA: `2ee1e803022e9cff6ff606343b738a00c43e886b`.
- 감사 결과(Claude `SELF_TEST_REPORTED`): `DEPENDENCY_AUDIT=PASS; DASHBOARD=RETIRE_CANDIDATE; NOTIFIER=KEEP; BRIDGE=RETIRE_CANDIDATE; ACTIVE_PROVIDER=NONE; HOST_CHANGES=0`. GPT는 Windows 호스트/현장 로그를 직접 검사하지 않았고 소스 검색은 사용자·자동화 폴더 범위로 한정되므로 전 디스크 불참조는 입증되지 않음.
- 사용자는 **Dropbox 대시보드를 더 이상 열어보지 않는다고 안내**했으며, 별도 Claude 응답에서도 이 사실을 정리 승인으로 받아들이지 않았다. 본 GPT도 **관심 없음/미사용과 Stop+Disable의 실행 승인은 분리**한다.

## 2. 항목별 판정
| 대상 | GPT_DISPOSITION | 근거·영향 |
|---|---|---|
| Bridge | **ACCEPT_RETIRE_CANDIDATE_FIRST** | 갱신기 v0.1.9에 대한 1회 설치 수신기, `HOST_APPLIED` 완료. 현재 5분 주기로 `ALREADY_COMPLETED` 반환하며 제어 대상은 갱신기 작업 하나. 다른 기능 참조 없음은 조사 범위에서만 확인. 설치 승인 만료 2026-11-14 00:00 KST는 다른 안전 게이트를 대신하지 않음 |
| Dropbox Dashboard updater | **ACCEPT_RETIRE_CANDIDATE_SECOND** | Dropbox requests/reviews/receipts에서 Dropbox `dashboard/index.html`만 업데이트. GitHub PRIVATE Action/Pages와 별개. 요청 65·결과 60 고정, 원격 HTML 마지막 갱신 11-09. 중지 후 과거 화면이 남아 구형 정보가 최신처럼 보일 위험 |
| Telegram notifier process | **KEEP_PENDING_LATER_DECISION** | 감시기 DB 이벤트 전용 폴링이나 Telegram 라이브러리/비밀은 독립 `notify_note` 경로가 공유. notifier process는 후속 독립 승인 대상; 모듈·비밀·워터마크 및 공용 venv 삭제 금지 |
| GitHub dashboard/Actions/Pages | **KEEP_UNCHANGED** | Windows Dropbox 갱신기와 코드·배포 경로가 별개. PUBLIC 상태 자동 동기화 및 민감정보 허용목록 게이트는 별도 운영 계약에 따름 |

## 3. 실행 전 준비 및 안전 게이트 (후속 승인 시)
- **실행 주체**: 허가받은 Windows Claude Code는 Task Scheduler 액션·정확한 작업명/작업경로·RunAs/실 PID·자동 재시작 경로를 다시 확인. Disable에는 관리자 권한 필요; 우회 불가. 사용자 관리자 셸 명령은 가능한 **검증된 한 묶음**으로 제공.
- 2개 작업의 설정 XML·해시·연결 구성·설치 상태·로그/워터마크·오류 정보를 **LOCAL_ONLY**로 보존. 이전 watcher 아카이브/운영 DB·WAL·SHM 및 Dropbox 요청·영수증은 변경·삭제하지 않음.
- Bridge `ops/disable_bridge.ps1` 기존 파일 존재 여부와 실제 내용을 검토하되, 검증 전 실행 금지. 정확한 작업 하나만 중지하는지, 예기치 않은 태스크·서비스·토큰 변경은 없는지 검사.
- ***Bridge 먼저*** 안전한 `Disable`+실행 중 인스턴스 확인/Stop. 5분 트리거를 포함한 재시작 차단을 확인. 작업의 현재 상태가 실행 중이거나 설치/승인 진행 중이면 무손실 완료 경계 전 중지 금지.
- ***갱신기 다음*** 작업 `Disabled` 설정 + 실행 중 Python 런처/자식 정상 종료 여부. 로그온 trigger 및 restart 3회/5분이 있으므로 작업 상태만 보고 성공 처리 금지. 프로세스 재기동 0과 정지 후 Dropbox 쓰기 0을 실측.
- 이미 감시기 task Disabled/PID0 유지, Notifier 및 다른 Task/Bridge 밖의 구성요소 정의 SHA/프로세스 불변, `ACTIVE_PROVIDER=NONE`, `MODEL_NEW_CALLS=0`, `C_OVERALL=PARTIAL`, `MIGRATION_NOT_CUTOVER` 유지.
- 2개 종료 후 별도 시간 지점에서 실제 PID/Task Enabled=False/신규 트리거 여부 재확인. 일부 실패 시 `PARTIAL/BLOCKED` 명시, 임의 타 작업 Disable 또는 스크립트 재시도 루프 금지.
- Dropbox HTML의 오래된 값은 '더 이상 갱신되지 않는 화면'이다. 사용자 미사용으로 현재 게시물 변경 필요성 낮음. **Dropbox 원격 HTML을 수정해 공지 삽입하는 행위는 별도 승인 대상**, 기존 파일을 임의 삭제하거나 덮어쓰지 않음.
- 롤백은 보존한 정확한 Task 정의와 관리자 Enable/Start를 이용. **작업 복원 E2E 미시험**이면 `ROLLBACK_READY=PARTIAL`로 명시.

## 4. 무엇을 하지 않는가
- **사용자 별도 승인 전** Bridge/갱신기/Notifier에 대한 실제 Stop·Disable·Enable·재설치·삭제를 실행하지 않는다.
- DB main/WAL/SHM에 SQLite `mode=ro`로도 접속하지 않음. SHM 수정 시각이 30초 주기로 notifier 폴링과 일치하는 것은 **CORRELATED_NOTIFIER**, 핸들 기반 인과 증명 아님.
- 공용 venv, 감시기 설치 코드/설정/인증/Telegram 전송 모듈·비밀·note publisher, 계정/토큰, 자동화·Dispatcher, Dropbox 이력/ZIP/영수증을 변경하거나 PRIVATE에 업로드하지 않는다.
- 운영 signer·개인키 생성/배포, 실제 과금 reviewer, GitHub LIVE 설치/전환, 새로운 READY 발행은 모두 권한 밖.
- 이 문서 게시로 Windows Claude Code나 예약 작업이 자동 실행되지는 않는다.

## 5. 승인 문구 및 이후 원샷 결과 계약
- 사용자에게 필요한 명시 승인: **“Bridge와 Dropbox 전용 대시보드 갱신기만, 무손실 보존·롤백 준비 후 그 순서로 Stop+Disable하는 것을 승인한다. Notifier와 공용 파일은 유지한다.”**
- 그 승인 후 Windows Claude Code가 현장 검증→보존→Bridge 중지/Disable→갱신기 중지/Disable→모델/타 프로세스 영향 검증→결과 MD와 CURRENT/TRACKER PRIVATE main 직접 게시/remote readback을 **한 번의 작업**으로 끝낸다. 실행 중 승인 범위 밖 게이트가 있으면 해당 항목만 `BLOCKED`.
- 예상 결과 명: `CLAUDE_DROPBOX_BRIDGE_AND_UPDATER_DISABLE_RESULT_FOR_GPT_20261113.md`. 실측 전 `HOST_CHANGES=0 / STOP_DISABLE_NOT_RUN`.
- `ACTIVE_PROVIDER=NONE`, `GITHUB_LIVE=NOT_RUN`, `CUTOVER=MIGRATION_NOT_CUTOVER`는 실제 LIVE 별도 승인 전 불변.

결론: `GPT_AUDIT_DISPOSITION=ACCEPT`, `BRIDGE=RETIRE_CANDIDATE`, `DASHBOARD=RETIRE_CANDIDATE`, `NOTIFIER=KEEP`, `OPERATIONAL_DISABLE=AWAITING_EXPLICIT_APPROVAL`.
