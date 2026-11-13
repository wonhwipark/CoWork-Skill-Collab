# GitHub LIVE 준비 — B1/C1/D2/Token2 단일 결정·로컬 전용 delta 실행
Date: 2026-11-14 KST | r0001
Repo: GitHub PRIVATE **`wonhwipark/CoWork-Skill-Collab`** | Branch: **`main`**
Exact path: **`collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B1_C1_D2_TOKEN2_LOCAL_ONLY_DELTA_ONE_SHOT_r0001_20261114.md`**
Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
Status when posted: **USER_CHOICES_RECORDED / WINDOWS_DELTA_NOT_RUN / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER**
Nature: 설계·격리 시험·보안 점검 인계. **운영 전환·개인키 생성·토큰 설치·코드 반출·유료 reviewer 호출 승인 아님**.

## 0. 사용자 선택의 정확한 의미
사용자는 GPT 질문(네 선택)에서 **B=1, C=1, D=2, 토큰=2**로 응답했다.
- **B=1**: Windows watcher PC **외부의 신뢰된 별도 승인자 기기 지정 가능**. 아직 기기·승인자 identity, key material, root 설치 승인은 확정되지 않았다. 운영키 발급=NOT_RUN.
- **C=1**: **4축 대체 증거 계약 검토 방향**을 선택. ETW/파일격리 엄격 수락 기준을 무조건 완화한 승인이나 C PASS가 아니다. 기본 `C=PARTIAL` 유지.
- **D=2**: **회사 원본/파생 코드 및 후보 ZIP을 외부로 반출하지 않는 로컬 전용 경로**를 택했다. GitHub PRIVATE를 포함한 외부 저장소로 유래 46개 + NEW 24개를 승인 없이 게시하지 않는다. 독립 검토는 **허가된 내부 네트워크·로컬 사람 또는 실제 로컬 모델**로만 설계. 외부 API Claude를 쓰면 코드가 외부로 전송될 수 있으므로 이 선택의 승인 범위 밖.
- **토큰=2**: **기존 토큰 권한 우선 확인**, 신규 발급·설치 승인 아님. 기존 `gho_` OAuth 성격 또는 과권한 자격을 최소권한으로 간주하지 않는다.

## 1. 최신 기준 및 재실행 차단
먼저 PRIVATE `collab/START_HERE.md`, 이 프로젝트 `CURRENT.md` 맨 위, `TRACKER.json`, 최신 `CLAUDE_BCD_TOKEN_APPROVAL_PRECHECK_RESULT_FOR_GPT_20261113.md` F1~F6, `GPT_BCD_TOKEN_PRECHECK_DISPOSITION_AND_DELTA_r0001_20261113.md` §9, `GPT_B7_TRUST_ROOT_AND_APPROVAL_POLICY_DRAFT_r0001_20261110.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`를 읽고 기존 결과 재사용.
확인된 직전 결과: v0.2.11 로컬 ZIP 175714B/SHA256 `174b9fd83361cc85ce3fb1b4b503335dc701bff9e38415ae23a11256ef8b6350` (Claude 자기시험 536 PASS/12 SKIP, 운영 501 PASS/14 SKIP), token verifier r0002 23 모의 PASS×2 및 원본 r0001 합계 34, installer 격리 사본 18 synthetic PASS, 실제 token/permission 검증은 NOT_RUN. Bridge, Dropbox watcher/updater Disabled, Notifier Running. 모델 호출 0, GitHub LIVE 아님.
다시 전체 제품 500+ 시험, 기존 ETW 31, GitHub mock credential 34, installer 18을 단순 반복하지 않는다. **변경분 관련 시험만**.

## 2. C — 4축 대체 수락 계약/증거 매트릭스 (계획·합성까지만)
원래 '운영 DB main/WAL/SHM/watch.lock 실제 I/O 0' 증거는 ETW 측정의 timestamp/프로세스 attribution 오류로 NOT_PROVEN. 동일 결론을 문서로 대체하거나 이전 오류를 무시하지 않는다.
**제안 C_ALT 계약**(승인 전 PROPOSED_ONLY):
1. **계정 강제 분리**: 실제 새 GitHub SHADOW 시험계정의 SID, access token/권한, privilege elevation·RUNAS·자식 프로세스 범위 증명. 운영 DB/main/WAL/SHM/lock, 기존 secret/운영 작업 폴더에 effective ACL deny 및 실제 접근 실패 양성/음성 대조(운영 데이터 내용을 열지 않는 안전한 방식). SYSTEM/관리자 token 또는 다른 계정으로 실행 시 FAIL. 정상 운영 LIVE 계정에 같은 제약을 적용할 수 없다면 `C_ALT_NOT_APPLICABLE_TO_LIVE`.
2. **경로·파일 격리**: SHADOW 전용 state_dir과 보호 폴더가 다른 Volume/File ID/8.3·UNC·junction·hardlink 별칭으로 겹치지 않음. protected_file_ids 포함, 파일 identity 확인 실패·중간 링크·폴더 접근 불명 시 `NOT_PROVEN`. snapshot/격리 복사본과 실제 운영 원본을 혼동 금지.
3. **실제 코드 도달 경로**: `watch/scan/status/config-check/auth-check/auth-init/reconcile/recover` 등의 provider별 분기 전수 확인 및 민감 경로 미진입 증거. 직전 v0.2.11의 config-check/auth-check/auth-init 결함 수정 regression 재사용. 서브프로세스/cron/후킹 플러그인 등 다른 코드 호출로 우회되는지 정적·런타임 증거 구분.
4. **변이/음성·양성 대조**: 권한을 약화하거나 디렉터리를 겹치게 하거나 라이브 secret 접근을 새로 넣은 **격리 변이**가 결정적으로 FAIL; 정상 SHADOW는 자기 state에만 쓰고 reviewer dispatch/model/Telegram/remote write 0. 보존된 원본 운영 DB 직접 SQLite 연결하지 않음.
5. 증거 원장 필수: Host OS/계정 종류/실제 PID·자식, 코드 ZIP SHA, test commands, expected/observed, signed reviewer/검증자 provenance, 파일 identity·권한·task 설정 요약, PASS/FAIL/NOT_PROVEN. private 경로·고객 코드/로그/DB/키는 GitHub 게시하지 않는다.
**C 수락 판정**: 4축 증거가 모든 **운영 예정 실행 모드와 계정**에 적용되며 독립 검토된 경우에만 GPT/사용자와 합의된 새 안전 계약으로 C_ALT 승인 검토. SHADOW 시험 계정 증거만으로 LIVE 다른 계정에 대한 C PASS 금지. ETW_NOT_PROVEN 기록은 보존. 지금은 `C_ALT=EVIDENCE_PREPARATION`, `C=PARTIAL`.

## 3. B — 별도 서명자 기기 준비 (운영 key 0)
- 실제 장치명·소유/운영자·보호 매체 상태는 비민감 분류만 확인(식별정보·PIN/암호 비수집). 키트 6개 파일의 source/provenance를 로컬에서 확인하고 **신뢰 장치로 이동이 조직의 내부 반출 정책에 허용되는지** 확인. NEW 파일/모듈이라는 사실만으로 조직 보안 허가 아님.
- 현 signer kit는 개인키를 **평문 Base64 파일**로 기록한다. BitLocker 등 전체 디스크 암호화, 파일 ACL, 오프라인 보관, 분실 시 폐기/rotation, 서명자 PC 분리 조건을 먼저 설계. 평문 private key를 채팅/PRIVATE 저장소/Windows watcher에 복사하거나 만들어 게시 금지.
- 테스트키/합성 서명 시험은 재사용. 운영키 생성·root pin 설치·실기기 sign은 **신규 명시 승인과 별도 기기 확인 후**. 운영 공개키만 watcher 호스트로 전달, source_commit/ZIP_SHA/repo ID/nonce/expiry/policy/cost 서명 계약 유지.
- 코드/ZIP이 D2 로컬 전용이면 외부 GitHub 원본 ZIP pin을 전제로 한 B 서명 계약 역시 변경 필요. 로컬 artifact SHA/manifest와 **GitHub에 게시 가능한 비밀 없는 commitment**를 분리하는 새로운 버전 계약 초안만 제안. 기존 `Commit A ZIP+REQUEST → signed READY`를 그대로 실행하지 말 것.

## 4. D2 — 코드 반출 없는 검토·증거 게시 경계
**보안 요구**: `v0.2.11 ZIP`, v0.1.5 소스·파생 46개, NEW 24개, 로컬 코드/시험/기밀 파일·원시 diff/로그/절대경로를 **GitHub PRIVATE/PUBLIC, Dropbox, 외부 LLM/API로 보내지 않는다**. 출처 분류에서 신규라고 자동 허용하지 않음. 키트 이동도 회사 정책 확인 전 실행 금지.
로컬 리뷰 제안(설계만):
- **LOCAL_ARTIFACT**: 승인된 내부 호스트에 원본 ZIP 봉인 보존, 실제 바이트 SHA/크기/CRC/zip slip/secret check **로컬에서만 실행**.
- **LOCAL_INDEPENDENT_REVIEW**: 개발과 다른 독립 리뷰어 또는 별도 session + **조직 승인된 온프레미스 모델**이 전체 원본을 점검. 외부 API 전송 OFF/네트워크 격리 검증, 자체시험/동일 개발 세션 리뷰는 `INDEPENDENT_REVIEW=NOT_RUN` 유지. 리뷰 결과 원문이 사외 반출 금지면 로컬에서 보존, GitHub에는 승인된 최소 비민감 요약만 허용.
- **GITHUB_CONTROL_PLANE**: 공개 금지 ZIP 대신 **비식별 opaque artifact ID, 정확한 SHA-256, 크기, 심사상태, 증거 종류, signing payload version, receipt digest** 등 검토·정책이 허용한 필드만 PRIVATE로. **SHA 자체가 내부 물건 식별자라 반출 제한될 수 있으므로 허용 여부 재점검**. local-only 원본 ZIP은 원격에서 원본 bytes readback 불가; remote README/receipt 일치로 소스 전체 무결성 증명했다고 주장 금지.
- **운영 프로토콜 차이**: 기존 GitHub signed READY 계약은 GitHub에 **ZIP raw bytes/Commit A**가 있을 것을 요구하므로 D2에서는 성립하지 않음. `GITHUB_LIVE_LOCAL_ONLY_TRANSPORT=DESIGN_REQUIRED`, local artifact verification, signed source binding, reviewer input locality, result source attestations, replay/cost controls, notification watermark, no-two-LIVE 등 **별도 계약 변경 + 독립 보안 리뷰 + 사용자 운영 승인** 필요.
- 독립 실제 리뷰가 불가능하면 `E=BLOCKED_LOCAL_REVIEWER`로 명확히 보고. '외부 Claude'를 단지 Windows PC에서 실행했다는 이유로 온프레미스/반출 무해로 간주하지 않는다.
- 향후 사용자가 정책상 허용한다고 확인된 최소 메타데이터만 GitHub로 게시. 새 docs가 기존 signed READY / 고정 Commit A 없이는 자동 리뷰를 트리거하지 않게 한다.

## 5. Token2 — 기존 자격 최소 권한 확인 (비밀 취급, 운영 변경 0)
- **기존 자격을 우선 조회**, 토큰 값·일부 문자·prefix·env path·password/hash를 stdout/MD/로그에 출력하지 말 것. GitHub CLI/OAuth 일반 토큰, Windows Credential Manager 등 존재 여부만 로컬 보안 경계에서 확인; 원문 추출/복사/새 token 생성은 이번 선택 밖.
- **우선 비네트워크/비밀 없는 설정 근거**: GitHub 웹 UI의 토큰 유형 fine-grained, 소유자, Only select repositories 정확한 `CoWork-Skill-Collab` 1개, Contents Read-only, Metadata Read-only, 다른 repo/account grant 없음, 만료 90일 이하, watcher 시험 계정에만 관리자가 보호된 전달 방식. 체크리스트 8항목 O/X는 **사람 진술 증거**이며 API만으로 전체 grant 확정 불가.
- 기존 OAuth/과권한 자격이 발견되면 해당 값을 쓰거나 다른 계정으로 복사하지 않고 `BLOCKED_OVERPRIVILEGED_EXISTING_CREDENTIAL`. 기존 최소 권한 fine-grained PAT 존재가 명백해도 시험 계정으로 허가된 secret store에서 읽어 GET-only `github_token_check_r0002.py` 실행하는 것은 별도 사용자 승인 후 단계. 이번에는 **credential 원문/운영 저장소를 열지 말고** metadata/설정 유형만 안전 확인.
- r0002는 **쓰기 probe 완전 금지**, r0001 불안전 probe를 사용하지 않음. exit 1=FAIL, exit 2=NOT_PROVEN, exit 0·기타=NOT_PROVEN. mock 테스트 23·34 및 설치스크립트 18을 중복 실행하지 않고 증거 재사용. r0002의 GET PASS는 실제 PAT 권한 전체의 증명 아님.
- Windows 기존 token scan이 다른 사용자/서비스의 비밀 파일을 읽을 위험이면 일체 탐색 중단하고 `BLOCKED_NEEDS_USER_UI_CONFIRMATION`. 사용자에게 일회에 한해 GitHub Settings에서 8항목 O/X만 확인 요청.

## 6. 이 세션에서 허용된 일·금지
**허용**:
1. PRIVATE GitHub 최신 원문·과거 결과 재사용, 비밀 없는 안전 계약·검증 매트릭스 작성.
2. 호스트 허용된 원본 코드 범위 내 **로컬 격리 복사본에서만** 수정·합성 시험, 새로운 결함의 영향 시험, candidate ZIP 생성/해시/로컬 보존 가능(반출 금지).
3. B 장치 가용성·C 안전 증거 요약·D2 local-only reviewer/transport 설계·기존 token metadata/설정의 **비밀 없는** 정적 점검.
4. 결과 MD와 CURRENT/TRACKER를 비민감 요약만 PRIVATE main PR 없이 직접 게시하고 commit/SHA/remote readback.

**금지**:
- 실개인키 생성/서명/root 설치, 실제 PAT 값 조회·재사용·install, 저장소 권한·secret 변경, 미승인 코드/ZIP/설계상 사외 제한 자료 게시.
- 기존 Dropbox 작업·운영 DB(main/WAL/SHM read 포함)·기존 watcher/Notifier/Bridge/Task Scheduler/Dispatcher 변경.
- signed READY/REQUEST 발행, 유료 reviewer 호출, Telegram 발송, 새로운 자동 감시/cron, GitHub LIVE 활성화·퍼블릭 ZIP 게시. 운영 설정 변경하려면 별도 승인 필요.
- 동일 mock/ETW 시험 반복, 새로운 관리자 측정 작업. 새로운 결함 발견 시 그 delta에만 시험.

## 7. 원샷 Windows 실행 및 결과
- Windows Claude Code는 본 문서 **하나**를 입력 기준으로 Lane B/C/D2/Token2를 가능한 항목부터 동시 준비한다. 막힌 항목만 `BLOCKED/NOT_RUN`으로 격리하고 나머지를 계속한다.
- 신규 결과 (비민감 요약만): `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_B1_C1_D2_TOKEN2_LOCAL_ONLY_RESULT_FOR_GPT_20261114.md`.
- `CURRENT.md` 맨 위와 `TRACKER.json` 유효 enum 업데이트; 기존 결과/이력 덮어쓰기 금지. 원격 bytes/hash/commit readback 확인, 미검증이면 `NOT_POSTED/UNVERIFIED`.
- 최종 표시: `B_DEVICE=AVAILABLE_UNDESIGNATED|DESIGNATED|BLOCKED`, `B_KEY=NOT_RUN`; `C_ALT=PROPOSED|EVIDENCE_COMPLETE|BLOCKED`, `C_OVERALL=PARTIAL`; `D_EXPORT=LOCAL_ONLY`, `LOCAL_REVIEW_E=DESIGN_READY|BLOCKED`; `TOKEN=EXISTING_READ_ONLY_VERIFIED|OVERPRIVILEGED|NOT_PROVEN|BLOCKED`; `E_INDEPENDENT_REVIEW=NOT_RUN`; `ACTIVE_PROVIDER=NONE`, `GITHUB_LIVE=NOT_APPROVED`.
- 이후 사용자에게 필요한 **남은 최소 1회 승인/입력 묶음**만 보고: 서명자 실제 기기(관리 기기 종류), 토큰 GitHub UI O/X, 로컬 독립 검토자 또는 모델 사용 가능성, 로컬-only 프로토콜 변경 승인 여부. 단, 현장에서 본인이 직접 승인할 정책을 대리 확정하지 말 것.

## 8. Windows Claude Code에 전달할 한 줄
`GitHub PRIVATE wonhwipark/CoWork-Skill-Collab main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_B1_C1_D2_TOKEN2_LOCAL_ONLY_DELTA_ONE_SHOT_r0001_20261114.md 하나만 읽고, 사용자 결정 B=1 C=1 D=2 토큰=2에 맞춰 기존 PASS 재사용·로컬 격리 delta 검증·C 대체 증거 매트릭스·B 서명자 장치 계획·D 로컬 리뷰/새 운송 계약안·기존 자격의 비밀 없는 권한 확인만 수행해줘. 운영 키/토큰/DB/task/유료 reviewer/READY/LIVE는 변경하지 말고, 결과 MD+CURRENT+TRACKER를 PRIVATE main에 게시하고 원격 검증해줘.`
