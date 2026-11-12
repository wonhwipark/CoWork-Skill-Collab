# CLAUDE Stage 1 승인 범위 호스트 보안 결과 (GPT용) 2026-11-11

STAGE1_APPROVED_HOST_RESULT: **PARTIAL** — A, B(시험키 범위), C(합성 GitHub 응답 범위) 호스트 실측 PASS. 실키·실GitHub SHADOW·ZIP 게시·정식 독립 리뷰는 BLOCKED/NOT_RUN.
최종 운영 상태: **Dropbox LIVE v0.1.5 유지 / GitHub CUTOVER=NOT_RUN**. DEVELOPMENT=SELF_TEST_REPORTED, INDEPENDENT_REVIEW=NOT_RUN.

## 0. 요약 판정표

| 단계 | 판정 | 증거 종류 | 범위 |
|---|---|---|---|
| A 비관리자 계정·ACL | PASS | HOST_REAL | 시험 계정 1개(비활성 보존), 관리자 전용 trust 폴더, 실제 파일 조작 + 유효권한 API |
| B 승인자 키·trust root | 시험키 PASS / 실운영 BLOCKED_SIGNER_DEVICE | HOST_REAL(시험 공개키) | 실개인키 미생성, 실 root 미설치 |
| C 호스트 SHADOW | PARTIAL (HOST_REAL I/O 계측 PASS, 실GitHub BLOCKED_CREDENTIAL) | HOST_REAL + SYNTHETIC(GitHub 응답) | 3주기, 비관리자 계정, ETW 커널 파일 추적 |
| D ZIP 반출 분류·게시 | BLOCKED_EXPORT_CLASSIFICATION | 정적 분류 | ZIP 로컬 보존, PRIVATE 게시 없음 |
| E 정식 독립 리뷰 | BLOCKED / NOT_RUN | - | 모델 호출 0, 비용 0 |
| 자체시험 보강 | PASS (SELF_TEST_REPORTED) | SYNTHETIC | 결함 3건 수정 → v0.2.10 |
| 33건 수집 차이 | 원인 확인 | HOST_REAL(pytest --collect-only) | 아래 §6 |

## 1. 중복 작업 확인
CURRENT.md, 승인 기록, v0.2.8 최종 처분, 이전 게이트 결과를 읽고 시작했다. 같은 계정/키/토큰/모델 호출을 이전에 만든 적이 없어 새로 만들었고, 기존 작업 결과 재사용은 없다.

## 2. 이번에 호스트에서 발견해 고친 결함 (소스 ZIP 원본 v0.2.8은 보존, 신규 버전에만 반영)
1. **SHADOW 경로 가드 크래시**: 운영 폴더를 열 권한이 없는 계정(의도된 구성)에서 `assert_isolated`가 PermissionError로 비정상 종료. 접근 불가를 "확인 불가"로 취급하도록 수정.
2. **파일 identity 0 크래시**: 이름은 나열되지만 열 수 없는 상위 폴더가 file index 0을 돌려줘 `IDENTITY_UNAVAILABLE`로 거부됨(호스트 재현). 상위 경로는 identity 없음으로 처리하되, SHADOW 폴더 자체가 존재하는데 identity가 없으면 여전히 거부.
3. **독립성 점검 크래시**: 접근 불가 항목에 `Path.exists()`가 PermissionError → "permissions could not be read" finding으로 변환.
회귀 시험 5개 추가(접근불가 라이브 폴더에서 OVERLAP는 여전히 거부, 런타임 기동, identity 0, 독립성 finding). 이 결함들은 단위 시험(합성)으로는 안 보였고 비관리자 계정 실측에서만 드러났다.

## 3. 패키지 (로컬 보존)
| 버전 | 바이트 | SHA-256 | 상태 |
|---|---|---|---|
| v0.2.8 | 173615 | c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa | 원본 보존(변경 없음) |
| v0.2.9 | 174525 | 957272662a978d21499f66fa62e6082bf84f9e8d8206f52da8570811a6c4e15f | 중간본, 대체됨 |
| **v0.2.10** | **174745** | **67ea7fc63ccc1de77a28025b7c4f1b701ee6f4fa387311bca3f3d2bc7432b108** | 현재 후보(로컬만, 70항목) |

v0.2.10 검증(추출본 기준): 시험 venv(cryptography 포함) 527 passed 12 skipped; 운영 인터프리터 3회 492 passed 14 skipped; 개인정보 식별자 스캔 0건; 실GitHub read-only 어댑터 점검 PASS; G1/G4 합성·스냅샷 리허설 PASS; 이전 버전 DB 열기 호환 유지. 변경: v0.1.5 대비 NEW 24 / CHANGED 12 / UNCHANGED 34.

## 4. A — 분리된 비관리자 실행 계정·ACL: PASS (HOST_REAL)
- 로컬 시험 계정 1개 신규 생성: Users 그룹만, **Administrators 아님**, 원격 관리 권한 없음, 평소 **비활성**. 실행 때마다 새 무작위 암호를 메모리에서만 사용하고 종료 시 다시 비활성(암호 출력·저장·전송 없음).
- 시험 폴더는 상속 제거 + 관리자만 쓰기: trust 폴더/파일은 시험 계정이 **읽기만** 가능. 실제 프로세스를 그 계정으로 띄워 쓰기·이름변경·삭제 시도가 거부됨을 확인하고, 유효권한 API(`GetEffectiveRightsFromAclW`)로도 쓰기 비트 0 확인.
- 계정은 운영 상태 폴더 안에 들어갈 수 없음(C의 추적에서 폴더 경로 열기 시도가 거부로만 관찰됨).
- 기존 LIVE 작업 계정·예약 작업·운영 ACL은 변경하지 않았다(전후 비교 §9).

## 5. B — 승인자 키·trust root
- **실운영**: 이 호스트가 감시기 실행 호스트이므로 별도 승인자 기기 요건 불충족 → 실개인키 생성·실 root 설치·서명 **NOT_RUN (BLOCKED_SIGNER_DEVICE)**. 개인키/시드는 어디에도 만들지 않았다.
- **시험키 독립 보안시험(HOST_REAL, 공개키뿐인 시험 root)**: 같은 비관리자 계정으로 LIVE 모드 런타임을 열었을 때
  - trust·pin·config가 관리자 전용 폴더 → `TRUST_ROOT_LOADED` (S-2 충족)
  - 같은 파일을 계정이 쓸 수 있는 폴더에 복사한 대조군 → `TRUST_ROOT_REFUSED: TRUST_ROOT_NOT_INDEPENDENT` (파일·폴더·pin 보관 config 모두 지적)
- 시험 root는 운영 root와 무관하며 실운영 PASS 근거로 쓰지 않는다. BLOCKED_TRUST는 "시험 계정 범위에서 ACL 검사 동작 실측"까지만 해소, 실 root 설치로는 해소되지 않았다.

## 6. 33건 pytest 수집 차이 원인 (확인됨)
- 시험 venv 527+12=539 수집, 운영 인터프리터 492+14=506 수집 → 차이 33.
- `pytest --collect-only`를 두 인터프리터로 비교한 결과 모듈별 차이는 **두 파일뿐**: `test_phase2_ed25519.py` 19개, `test_phase5_signer.py` 16개 = **35개가 운영 인터프리터에서 수집되지 않음**. 원인은 모듈 최상단 `pytest.importorskip("cryptography")` (운영 venv에는 cryptography 없음).
- 수집되지 않은 모듈은 모듈당 SKIP 1건으로 집계되므로 skip이 12→14로 +2. 35 − 2 = **33**.
- 시험 추가/삭제 때문이 아니라 venv 의존 파일 때문이다. 앞서 "35 skipped"라고 쓴 표현은 부정확했고 정확히는 "35 NOT_COLLECTED"이다. 운영 인터프리터에는 Ed25519 서명 시험이 실행되지 않으므로 서명 검증 PASS는 cryptography가 있는 환경에서만 의미가 있다.

## 7. C — 호스트 SHADOW (비관리자 계정, 실 프로세스 I/O 계측)
- 방식: 시험 계정으로 후보 v0.2.10의 실제 `watch` CLI 경로를 3주기 실행. `provider_mode=SHADOW`, 자체 `shadow.state_dir`, read-only 전송 객체, `ShadowRunner`. `local_state_dir`는 **실제 운영 상태 폴더 경로**로 설정(열 권한 없는 계정).
- GitHub 응답은 **프로세스 내부 합성 대역(FakeGitHub)**. 호스트에서 쓸 수 있는 GitHub 토큰은 이 저장소 contents-read-only가 아니라 과권한이어서 실GitHub SHADOW는 **BLOCKED_CREDENTIAL**(시험 계정에 넘기지 않음). 따라서 C는 "실 파일 I/O는 HOST_REAL, GitHub 응답은 SYNTHETIC".
- 결과: 종료코드 0, 주기 3/3 OK, HTTP는 GET만 11회, WATCH_START/SCAN_START×3/WATCH_END 감사 기록, 디스패치 0, 모델 호출 0, Telegram 0, GitHub/Dropbox 쓰기 0.
- **ETW(Microsoft-Windows-Kernel-File) 추적, 해당 PID만 집계**: 이벤트 약 1.4만 건.
  - 양성 대조(미끼 파일 열기 시도) 관찰됨 → 계측이 실제로 작동.
  - 자기 shadow 폴더 안 I/O 97건 관찰.
  - state.sqlite3 / -wal / -shm / watch.lock을 **자기 shadow 폴더 밖에서** 언급한 이벤트 **0건**; 운영 폴더 **안의** 항목 이벤트 **0건**.
  - 주의(정직한 한계): 운영 폴더 **경로 자체**에 대한 열기/조회 이벤트는 42건 있다(경로 가드의 존재·재해석점 검사, OS가 접근 거부). DB 파일은 열린 적 없다. 즉 "운영 폴더를 이름으로 조회" 수준의 메타데이터 접근은 있으며 완전한 무접촉이 아니다. S-1의 목표(운영 DB main/WAL/SHM I/O 0)는 충족.
- 전후 비교: 운영 상태 폴더 이름·크기·수정시각 전후 동일(§9). ETW 추적 파일은 실행 후 삭제.
- 한계: 계측 대상은 단일 실행 3주기. 실GitHub 응답 경로와 장시간 운영은 미검증. PID 기준이므로 자식 프로세스는 파이썬 런타임 사본을 써서 단일 PID로 제한.

## 8. D — ZIP 반출 분류: BLOCKED_EXPORT_CLASSIFICATION
- 70개 항목은 모두 이 협업 작업장에서 AI 세션이 작성한 소스/시험/문서이며, 시험 데이터는 합성이다. 자동 secret 스캔 0건·식별자 스캔 0건이지만 이는 반출 허가가 아니다.
- 그러나 **UNCHANGED 34개는 사내 운영 중인 v0.1.5 감시기에서 온 코드**이고, 소유자·외부 반출 정책에 대한 사용자 확인이 없다. 규칙상 1건이라도 불명확하면 ZIP 통째로 BLOCKED. **PRIVATE 게시 0건, 로컬 보존.** (v0.2.8 원본 173615B도 게시하지 않음.)
- 이후 사용자가 "외부 보관 허용"을 명시하면 v0.2.10 ZIP(위 SHA)을 신규 파일명으로 게시하면 된다.

항목별 분류(출처=AI 세션 작성, 반출 정책=확인 불가, 비밀/PII=스캔 0건; 구분은 신규/변경/기존 v0.1.5 유래로 한 번 더 나뉜다):

| 파일 | 바이트 | 종류 |
|---|---|---|
| config/reviewer.config.example.json | 826 | packaging/other |
| docs/CUTOVER_RUNBOOK.md | 13765 | documentation |
| prompts/review_instructions.md | 3551 | packaging/other |
| requirements-crypto-test.lock | 1998 | packaging/other |
| requirements.txt | 47 | packaging/other |
| skill_collab_watcher/__init__.py | 23 | package source |
| skill_collab_watcher/approval.py | 19679 | package source |
| skill_collab_watcher/auth_flow.py | 4420 | package source |
| skill_collab_watcher/cli.py | 28305 | package source |
| skill_collab_watcher/config.py | 12383 | package source |
| skill_collab_watcher/dropbox_transport.py | 13159 | package source |
| skill_collab_watcher/fake_runner.py | 1335 | package source |
| skill_collab_watcher/github_transport.py | 12828 | package source |
| skill_collab_watcher/lock.py | 1746 | package source |
| skill_collab_watcher/mock_transport.py | 6687 | package source |
| skill_collab_watcher/models.py | 1597 | package source |
| skill_collab_watcher/notify_events.py | 8724 | package source |
| skill_collab_watcher/orchestrator.py | 41846 | package source |
| skill_collab_watcher/review_runner.py | 10862 | package source |
| skill_collab_watcher/secret_prompt.py | 3466 | package source |
| skill_collab_watcher/secrets_store.py | 2257 | package source |
| skill_collab_watcher/shadow_guard.py | 6016 | package source |
| skill_collab_watcher/signature_backend.py | 1228 | package source |
| skill_collab_watcher/state_store.py | 23161 | package source |
| skill_collab_watcher/transport_base.py | 3430 | package source |
| skill_collab_watcher/validator.py | 9715 | package source |
| skill_collab_watcher/watch_loop.py | 4671 | package source |
| skill_collab_watcher/zip_safety.py | 2779 | package source |
| tests/bundle.py | 4939 | test source (synthetic data) |
| tests/conftest.py | 4195 | test source (synthetic data) |
| tests/fake_github.py | 6028 | test source (synthetic data) |
| tests/test_auth_flow.py | 13994 | test source (synthetic data) |
| tests/test_config.py | 4921 | test source (synthetic data) |
| tests/test_cursor_and_pending.py | 9838 | test source (synthetic data) |
| tests/test_dropbox_transport_errors.py | 14188 | test source (synthetic data) |
| tests/test_model_call_boundary.py | 1930 | test source (synthetic data) |
| tests/test_no_model_calls.py | 11582 | test source (synthetic data) |
| tests/test_phase1_approval.py | 7318 | test source (synthetic data) |
| tests/test_phase1_blocking_fixes.py | 12982 | test source (synthetic data) |
| tests/test_phase1_github.py | 11002 | test source (synthetic data) |
| tests/test_phase2_acceptance.py | 9649 | test source (synthetic data) |
| tests/test_phase2_cutover.py | 6315 | test source (synthetic data) |
| tests/test_phase2_ed25519.py | 11964 | test source (synthetic data) |
| tests/test_phase2_notify.py | 8537 | test source (synthetic data) |
| tests/test_phase3_gates.py | 14402 | test source (synthetic data) |
| tests/test_phase3_trust_tool.py | 3186 | test source (synthetic data) |
| tests/test_phase4_unattended.py | 16665 | test source (synthetic data) |
| tests/test_phase5_independence.py | 9402 | test source (synthetic data) |
| tests/test_phase5_shadow.py | 18160 | test source (synthetic data) |
| tests/test_phase5_signer.py | 9290 | test source (synthetic data) |
| tests/test_release_packaging.py | 4651 | test source (synthetic data) |
| tests/test_review_runner_argv.py | 1241 | test source (synthetic data) |
| tests/test_secret_prompt.py | 8153 | test source (synthetic data) |
| tests/test_state_store.py | 1806 | test source (synthetic data) |
| tests/test_v013_hardening.py | 11163 | test source (synthetic data) |
| tests/test_v014_budget_tiers.py | 8220 | test source (synthetic data) |
| tests/test_v015_token_savings.py | 13422 | test source (synthetic data) |
| tests/test_validator.py | 2084 | test source (synthetic data) |
| tests/test_watch_loop.py | 4955 | test source (synthetic data) |
| tests/test_windows_scripts.py | 1469 | test source (synthetic data) |
| tests/test_zip_safety.py | 887 | test source (synthetic data) |
| tools/__init__.py | 0 | operator tool source |
| tools/approval_signer.py | 9277 | operator tool source |
| tools/build_release.py | 7411 | operator tool source |
| tools/trust_root_tool.py | 4197 | operator tool source |
| windows/auth_init.cmd | 211 | packaging/other |
| windows/recover.cmd | 209 | packaging/other |
| windows/run_scan.cmd | 206 | packaging/other |
| windows/run_watch.cmd | 386 | packaging/other |
| windows/status.cmd | 205 | packaging/other |

## 9. 운영 상태 전후 비교 (변경 없음 확인)
- 예약 작업 정의 해시(XML)·상태: 변경 없음. 대시보드 작업 상태가 Running→Ready로 오간 것은 정상 주기.
- 운영 DB 파일 3종: 우리는 **열지 않았고** 메타데이터(이름/크기/시각)만 읽음. 운영 감시기가 계속 가동 중이라 DB/WAL 크기·시각 변화는 운영 자체 활동이며 시험 때문이 아님. C 중 운영 폴더 메타데이터 비교는 실행 전후 동일.
- 운영 v0.1.5 폴더, Telegram 설정, 토큰, 운영 키: 변경 없음. 추가된 호스트 변경은 시험 계정 1개와 시험 샌드박스 폴더뿐(추가만, 아래 §11 회수 계획).

## 10. E — 정식 독립 리뷰: BLOCKED / NOT_RUN
- 실제 공개 trust root + 정상 signer 서명(B 실운영 BLOCKED), 반출 승인(D BLOCKED), 개발과 분리된 reviewer 실행 경로·기록 부재 → 서명된 READY를 만들지 않음.
- 모델 호출 **0**, 비용 **USD 0**. STATIC $1 상한 충족 여부는 미평가가 아니라 "경로가 없어 호출 자체를 하지 않음". 개발 세션 자체 시험은 독립 리뷰가 아니다. 임의 `claude -p` 호출 없음.
- F1 실제 처분, 운영 DB 이행, GitHub LIVE 전환: 실행하지 않음.

## 11. 회수·보존 현황 (삭제하지 않고 상태만 보고)
- 시험 계정: **비활성 상태로 보존**(활성 여부 확인: 비활성). 필요 시 사용자가 제거 또는 후속 시험에 재사용.
- 샌드박스 폴더(후보 코드 v0.2.10, 복사된 파이썬 런타임, 시험 trust 폴더, shadow 상태): 로컬 보존. ETW 추적 파일은 삭제됨.
- 로컬 ZIP: v0.2.0~v0.2.10 보존.

## 12. 사용자 승인이 남은 묶음 (한 번에)
1. **별도 승인자 기기**에서 실 Ed25519 키쌍 생성 및 공개키만 host 관리자 폴더 설치 승인 (B 실운영).
2. 이 저장소 **contents-read-only 전용(fine-grained) 토큰**을 시험 계정이 쓰도록 준비 → 실GitHub SHADOW 재실행.
3. ZIP **외부 보관(PRIVATE 게시) 허용** 여부 — v0.1.5 유래 34개 파일의 소유·반출 정책 확인.
4. 정식 독립 리뷰 실행 경로(별도 세션/기기)와 STATIC $1 승인.
5. 위가 충족된 뒤에만: 운영 DB 이행, F1 처분, GitHub LIVE 전환(각각 별도 승인).
