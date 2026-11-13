# CLAUDE GitHub LIVE 직전 원샷 사전검증 결과 (GPT용) 2026-11-14

기준 인계: `GPT_GITHUB_LIVE_ONE_SHOT_REVIEW_INTEGRATION_PREFLIGHT_r0001_20261114.md` 하나. 성격: Windows Claude Code **자체 시험 보고(`SELF_TEST_REPORTED`)**.
운영 DB·예약 작업·알림·Bridge·토큰·Dropbox 이력 변경 0, 모델 호출 0, 비용 $0, READY·REQUEST 게시 0, LIVE 활성화 0.

## 1. 현재 상태
`ACTIVE_PROVIDER=NONE` · `MIGRATION_NOT_CUTOVER` · `LIVE=NOT_APPROVED` · **`INDEPENDENT_REVIEW=PENDING_APPROVAL` / `MODEL_CALLS=0` / `PAID_REVIEW=NOT_RUN`** · `INTEGRATION=HOST_ISOLATED_PASS`(운영 LIVE E2E 아님) · `REVIEW_INPUT_UPLOAD=PASS`.
Dropbox 감시기·Bridge·갱신기 Disabled, 알림기 Running(재확인). 설치된 운영 감시기는 **v0.1.5(Dropbox 설정)** 이며 이번 후보는 설치하지 않았다.
독립 리뷰를 실행하지 않은 이유: 이번 작업에 적용되는 **유효한 리뷰 실행·비용 승인이 없다**(링크 전달 승인은 비용 승인이 아님, 인계 §0·승인 문서 §6 `NEW_PAID_REVIEW=NOT_AUTHORIZED`). 그래서 준비만 하고 다른 작업은 계속했다.

## 2. 변경 내용 (v0.2.13 → 후보 v0.2.14)
1. **실제 결함 1건 발견·수정 (리뷰 전)**: 실제 CLI 진입점을 2프로세스로 동시에 `scan` 하면 같은 승인 요청에 reviewer 가 **2회** 시작됐다(수정 전 재현: 호출 2). 중복 판정이 "읽기 후 무조건 `CLAIMED` UPDATE"라 비원자적이었고 단일 실행 잠금은 `watch` 에만 있다. `StateStore.try_claim`(미발송 상태에 한정한 단일 compare-and-set UPDATE)을 추가하고 orchestrator 의 claim 을 교체. 졌으면 `IN_PROGRESS_SKIPPED`, 발송 0. 읽기 전용(SHADOW) 저장소는 claim 하지 않음. 기존 `watch` 동작·상태 전이는 그대로.
2. 격리 진입점 E2E 신규(9개), `try_claim` 단위 시험 15개. 제품 코드 변경은 위 2개 파일뿐.
3. r0003/SU-L1 은 **제품에 통합하지 않았다**(인계 §1-A-2). 기존 watcher 의 중복 방지(`provider_lease`, `job_claims`, 논리 키, 단일 실행 잠금)를 재사용했고 위 결함만 메웠다.

## 3. 실제 시험 결과
| 항목 | 결과 | 구분 |
|---|---|---|
| (a) 서명된 유효 요청 1건 → 리뷰 1·결과 1·영수증 1·`COMPLETED` | PASS | HOST_ISOLATED |
| (b) 재스캔·재시작 4회 후 reviewer 호출 1 / 2프로세스 동시 scan 호출 1 | PASS (수정 후; 수정 전 FAIL 호출 2) | HOST_ISOLATED |
| (c) 재기동 후 replay 0 | PASS | HOST_ISOLATED |
| (d) 승인 없음·위조 서명·다른 키 서명 → 호출 0, `APPROVAL_REJECTED` | PASS | HOST_ISOLATED, 실제 Ed25519 |
| (e) 결과 쓰기 500 오류 → 호출 1 유지, 정상화 후 게시만 재시도 → `COMPLETED`, 호출 여전히 1 | PASS | HOST_ISOLATED |
| (f) 구 Dropbox LIVE 임대가 있는 DB 에서 GitHub LIVE 거부·구 이력 보존·호출 0 | PASS | HOST_ISOLATED |
| (g) backup·rollback 이행 계획 / 재기동 시 이력 무손실 | 재기동 무손실 PASS(합성). 운영 DB 이행·복원 E2E **NOT_RUN** | 합성 |
| (h) 알림 중복 0 | PASS(`notify_events` 라이브러리, 3회 실행에 1건). 실행 중인 알림기 프로세스에 연결은 **NOT_RUN** | SYNTHETIC |
| (i) 운영 DB·작업·알림 변경 0 | 운영 `state.sqlite3*` 는 **열지 않고** 메타데이터만 확인(크기 불변); 4개 작업 상태 유지 | HOST_REAL(읽기 전용) |
| 제품 전체(시험 venv) | 666 passed, 13 skipped | SELF_TEST |
| 운영 인터프리터 | 551 passed, 20 skipped (cryptography 없어 Ed25519 모듈 SKIP) | SELF_TEST |
| **GitHub 에서 내려받은 ZIP 을 풀어 전체** | 666 passed, 13 skipped | SELF_TEST |
- 실제 GitHub 읽기 전용 SHADOW 연결: **NOT_RUN**. 감시기는 `github.token_file` 을 **원문 토큰 텍스트**로 읽는데 이 PC 의 `github_readonly_token.json` 은 JSON 형식(키 `token` 등)이라 그대로는 못 쓴다. 변환하려면 토큰 값을 다뤄야 해서 하지 않았다(설치 시 해결할 항목).
- 변경하지 않은 모듈의 이전 PASS(ETW, 토큰 모의, r0003 28, 변이 검출 등)는 재실행하지 않았다.
- `trust_root_independence=warn` 으로 시험(단일 사용자: 운영자 계정이 신뢰 루트 파일을 바꿀 수 있음). 기본값 `enforce` 에서는 같은 PC 운영이 거부된다 — 단일 사용자 운영 시 `warn` 을 쓰는 것이 위험을 받아들이는 선택임을 명시한다.

## 4. 미검증 / 차단 / 남은 승인
1. **독립 Claude 리뷰 1회**: `PENDING_APPROVAL`. 현재 GitHub transport 의 승인 계약은 서명된 `APPROVAL_SIG.json`(Ed25519) + 신뢰 루트다. 이 PC 에는 운영 서명키·신뢰 루트가 **없다**. 아래 §7 에서 선택.
2. **결과 쓰기 자격**(`CREDENTIAL_MINIMUM`): 읽기 전용 fine-grained 토큰(2026-11-12 파일, 내용은 열지 않음)은 감시기의 결과·영수증 업로드(PUT)에 쓸 수 없다. 감시기는 LIVE 에서 한 토큰으로 읽고 쓴다. 현재 쓰기 파일은 이전 기록상 classic `repo` 토큰이다 → LIVE 용으로 **저장소 1개 Contents Read and write fine-grained 토큰 1개**가 필요(별도 서명자·3종 일괄 교체 불요). 개발용 `gh` 로그인(`repo,workflow,read:org,gist` 광역)은 그대로이며 감시기에 쓰지 않는다.
3. **운영 적용**(`CUTOVER_PLAN`): 설치된 v0.1.5 → 후보 v0.2.14 교체, GitHub 설정 추가, 상태 DB 이행. 운영 DB 이행·롤백은 **격리 리허설도 NOT_RUN**(운영 DB 파일을 열지 않기 위해 사본·열람을 하지 않았다).
4. 알림기: 현재 실행 중인 것은 구 Dropbox 알림기. GitHub 알림은 `notify_events` 연동(런북 6단계)이 필요 — 미연결.

## 5. 산출물
- 로컬 후보 ZIP: `D:\User\whpark\cowork-phase1\dist_phase2\skill-collab-watcher_v0_2_14_1114.zip` (v0.2.13·v0.2.12 바이트 불변).
- GitHub PRIVATE `review-inputs/REV-COWORK-V0214-20261114/` — 원격 raw 바이트 SHA-256·크기·blob SHA 일치, 파일별 고정 commit:

| 파일 | 고정 commit | 크기 | SHA-256 |
|---|---|---|---|
| [skill-collab-watcher_v0_2_14_1114.zip](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/dc429c05039b42e0af343a07ea2a9fb6d783feda/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/skill-collab-watcher_v0_2_14_1114.zip) | `dc429c05039b42e0af343a07ea2a9fb6d783feda` | 219663 | `3a221dcdb22ba75208a60ca555b0ee75866313a591148b1f482b7cbb6aa0b367` |
| [diff_v0_2_13_to_v0_2_14.patch](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/551e23f83c88fdb826096712535df25e72b0f724/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/diff_v0_2_13_to_v0_2_14.patch) | `551e23f83c88fdb826096712535df25e72b0f724` | 19236 | `494afd6710a216068b18a127d1e34381d02da644a5bb85568733904680795987` |
| [source/skill_collab_watcher/state_store.py](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/7716d573515c5d3e89d62b9dd16e7bc0373374c2/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/source/skill_collab_watcher/state_store.py) | `7716d573515c5d3e89d62b9dd16e7bc0373374c2` | 24235 | `f54a914987e527dbae936d43316466151b8402ff54bfcafd6408f8ff949d9e86` |
| [source/skill_collab_watcher/orchestrator.py](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/c1e8d5b87c9fa1d78c9fa569d57d5f37d9a17a8e/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/source/skill_collab_watcher/orchestrator.py) | `c1e8d5b87c9fa1d78c9fa569d57d5f37d9a17a8e` | 42119 | `fc94933bdd7af1440a3124454a8415e05bfa6e1c5c3ff7fff6bfffd32fa91eb0` |
| [source/tests/test_cli_entrypoint_e2e.py](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/4b43e0f4c77efdd19a8e85ce94b8161820f02029/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/source/tests/test_cli_entrypoint_e2e.py) | `4b43e0f4c77efdd19a8e85ce94b8161820f02029` | 11293 | `5146e48740180712f24bda3f4805763d359bdc2e341719a71f26f3f5ec2c0b1d` |
| [source/tests/e2e_launcher.py](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/8cc8ba3e22878dbfb1f464a7dac6a57d545c8432/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/source/tests/e2e_launcher.py) | `8cc8ba3e22878dbfb1f464a7dac6a57d545c8432` | 1608 | `1b15b2ad610d91828368fd700a296e940d93f711a61d6ec5af0c27634aa8deb5` |
| [source/tests/e2e_claude_stub.py](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/7a5c4e441dfacdc6b9b43d9250da76461247d927/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/source/tests/e2e_claude_stub.py) | `7a5c4e441dfacdc6b9b43d9250da76461247d927` | 932 | `e8bea17eaae181bb862e7aeb7739fa7809ca03bd1605b5469bf2450243b9db8d` |
| [source/tests/test_try_claim.py](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/96a0d29d8412ce900cead8fdb9fea4eb8d27a8c2/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/source/tests/test_try_claim.py) | `96a0d29d8412ce900cead8fdb9fea4eb8d27a8c2` | 2006 | `a6dc2950e047be6927ad15023f4dd4e6b8e01ebac3ae85609d8060db13a7274e` |
| [REVIEW_MANIFEST.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/1a020998b70d39582d7a8c40427d25a618268e2a/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/REVIEW_MANIFEST.md) | `1a020998b70d39582d7a8c40427d25a618268e2a` | 8125 | `14e23120a65fa4a67dba67ecb9215a221f3653b2310d6e6c7198be0399a537cb` |

- ZIP: 원격 raw 로 다시 내려받아 87항목 CRC·압축 해제 정상, 필수 경로(`skill_collab_watcher/state_store.py`, `tests/test_cli_entrypoint_e2e.py`, `su_l1/` 12개) 확인. secret 스캔 0건. 회사 L1 소스·토큰·운영 데이터 미포함.
- URL 은 (저장소, commit, 경로)를 API 로 재조회해 검증한 값으로 만든 github.com 링크이며 웹 렌더링 자체를 브라우저로 열어 보지는 않았다.
- `L1Work` PUBLIC 에는 아무것도 올리지 않았다.

## 6. LIVE 조건표
| 조건 | 상태 |
|---|---|
| REVIEW_INPUT_UPLOAD | **PASS** (원격 바이트 검증) |
| INDEPENDENT_REVIEW | **NOT_RUN** (PENDING_APPROVAL) |
| HOST_ISOLATED_INTEGRATION | **PASS** (실제 CLI 진입점, 네트워크·claude 대체; 운영 LIVE E2E 대체 아님) |
| STATE_RECOVERY | 재기동·중복·게시 재시도 PASS(합성), 운영 DB 이행·복원 **NOT_RUN** |
| NOTIFIER_DEDUP | 라이브러리 PASS(합성), 실제 알림기 연결 **NOT_RUN** |
| CREDENTIAL_MINIMUM | **BLOCKED**: 감시기용 쓰기 가능 fine-grained 토큰 필요, 토큰 파일 형식 어댑터 필요 |
| CUTOVER_PLAN | 계획·단계는 런북에 있음, 격리 리허설 **NOT_RUN** |
| FINAL_APPROVAL | **NOT_APPROVED** |

시뮬레이션·격리 시험은 운영 검증을 대체하지 못한다.

## 7. 다음 사용자 한 동작 — 필요한 승인만
1. **독립 리뷰 1회 실행 승인**: 정책 `POLICY-STATIC-V1`(정적 리뷰, 상한 $1.0, effort medium; 설정 파일 기존 값), 대상 = 위 commit 고정 링크. 이때 승인 방식 중 택1:
   - **A(권장, 최소 변경)**: 이 PC 에서 운영자 서명키 1개 생성(암호화 보관, 신뢰 루트 `warn`) → 승인서 서명 → 정식 READY 1건. 키 생성이 승인 범위에 포함된다.
   - **B**: 기존 SU-L1 정책 엔진을 승인 관문에 통합하는 개발을 먼저 하고(재시험·재리뷰 대상 증가) 서명 없이 진행.
2. **감시기용 쓰기 가능 fine-grained 토큰 1개**(저장소 1개, Contents R/W) 발급·설치 승인, 현재 classic 쓰기 토큰 폐기.
3. 위 PASS 이후 **운영 전환**(설치 교체, DB 이행, 알림기 연결, LIVE 활성화) 최종 승인.

이 외의 추가 PC·로컬 LLM·ETW·3종 토큰 일괄 교체는 요구하지 않는다.

`REVIEW_INPUT_UPLOAD=PASS; INTEGRATION=HOST_ISOLATED_PASS; DEFECT_FIXED=CONCURRENT_SCAN_DOUBLE_DISPATCH; INDEPENDENT_REVIEW=PENDING_APPROVAL; MODEL_CALLS=0; PAID_REVIEW=NOT_RUN; CREDENTIAL_MINIMUM=BLOCKED; ACTIVE_PROVIDER=NONE; GITHUB_LIVE=NOT_RUN; CUTOVER=MIGRATION_NOT_CUTOVER`
