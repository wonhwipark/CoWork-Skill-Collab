# v0.2.32 후속 보완 원샷 결과 (Windows Claude Code)

- 작성: 2026-11-22 KST. Work: `COWORK-AUTO-APPROVAL-20261115-001`. 지시: `WINDOWS_V032_CORRECTIONS_ONE_SHOT_HANDOFF_r0001_20261122_KST.md`. 판정 입력: GPT `GPT_V032_PRELIVE_3_TO_9_DISPOSITION_r0001_20261122_KST.md`.
- **STATUS: 부분 완료. LIVE_READY=NO, LIVE_APPLY=NOT_RUN, 신규 리뷰·모델 호출·REQUEST/READY/서명 0.**
- **차단의 핵심:** 차기 후보 폴더(`v0_2_33`) 생성용 폴더 복사 명령이 권한 계층에서 두 번 거부되었다(§7). 우회하지 않았으므로 승인 경로 연결, 신규 시험 추가, 차기 ZIP 생성은 수행하지 못했다. 코드 변경 0.

## 1. 입력 고정

| 항목 | 값 | 판정 |
|---|---|---|
| v0.2.32 ZIP SHA-256 | `cbf95d1141cbed6973d6cace2950065b4ed5eb36e988ecf522a9fc3ab087fa94` | 실물 재확인 PASS |
| 크기/항목 | 295,885 B / 106 | 이전 결과와 일치 |
| v0.2.30·v0.2.31 구 ZIP | `541cd3f1…`, `1df85457…` | 변경 없음 |
| 라이브 | v0.2.29 Running, 설정·위임 SHA 불변(직전 검증) | 변경 없음 |

## 2. 단계별 결과

| 단계 | 결과 | 근거·한계 |
|---|---|---|
| 1. 시험 증거 연결 | PASS(재사용) / G3 프로세스 증거 NOT_RUN | 이전 Windows 결과의 race 시험은 **같은 OS 프로세스 안의 두 스레드**와 서로 다른 임시 DB를 사용했다. 서로 다른 OS 프로세스를 쓰는 시험은 없다. 모의 전송은 잠금으로 create-only를 흉내 냈다. 실제 GitHub 경합은 NOT_RUN(쓰기 금지) |
| 2. 승인 경로 연결(REUSE→CONNECT) | **BLOCKED_PERMISSION** | 차기 폴더 생성 거부. 코드 변경 없음. 연결에는 `REVIEW_INTENT` nonce 저장소(`review_intent_nonces`)가 필요하며, 설치 시 DB 테이블 추가 이행이 생긴다 |
| 3. 의도 검증 시험(보완) | 기존 범위만 PASS / 일부 **NOT_COVERED** | 기존 `review_intent` 시험 25건이 정확 바인딩, 위조, 변조, 만료, 미래 시점, 수명, 해지 키, 승인용 목적 키, 와일드카드, 본문 승인 주장, 재사용 nonce(동일 프로세스)를 다룬다. **미포함:** 재시작 후 nonce 재사용, 동시 nonce 소비, 소급 요청(통합 경로 없음). 모델 시작 불명 재시작은 기존 `test_lost_reservation…`/`test_crash…`가 봉인을 확인 |
| 4. 설치 트리 백업 | **BLOCKED_PERMISSION** | 필요 작업: `D:\User\whpark\skill-collab-watcher-github`(라이브 v0.2.29 읽기) → `D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_29_precheck_20261122\install_tree_v0_2_29`. 계정 `ME`. Bash 복사 명령 2회 거부(첫 시도 전체 스크립트, 이번 세션 복사 명령). 다른 수단으로 재시도하지 않음. **필요 권한:** 이 복사 작업 허용 또는 허용된 읽기 전용 복사 방식 지정 |
| 4a. DB·설정·위임 백업 | PASS(이전) | `backup_v0_2_29_precheck_20261122\`: state.sqlite3(백업 API, integrity ok, 작업 12, 감사 최대 id 22804), reviewer.config.json SHA `2ead4007…`, auto_delegation.json SHA `6d826672…`, MANIFEST.json |
| 5. 롤백 준비 | **BLOCKED_PRESERVE / 복구 BLOCKED** | 기존 2026-11-20 번들은 **v0.2.25 설치 트리**(SHA `f691bcf8…`)이고 v0.2.29 트리 백업이 아니다. 2026-11-20 이후 완료 작업이 있어 과거 DB(작업 9)로 교체하면 이력이 유실된다. 따라서 DB 교체 금지. 코드 복원은 v0.2.29 트리 백업(단계 4)이 필요하다. 사본 복원 시험은 이전에 integrity ok, 최신 이력 유지 확인 |
| 6. 차기 후보 v0.2.33 | **BLOCKED_PERMISSION** | 단계 2와 동일 원인. ZIP 생성 없음 |
| 7. 독립 리뷰 | **BLOCKED_AUTH** | 이 패키지에 대한 유효 보호 승인·전달 허용 없음. 신규 REQUEST는 코드 ZIP을 PUBLIC 저장소에 올려야 하므로 불가. 기존 R1 재실행 없음. 유료 호출·REQUEST·READY·서명 0 |
| 8. 읽기 전용 SHADOW(사본) | PASS(사본 한정) | 재실행 결과 `dispatched=0`, `pending=8`, 모델 0, 쓰기 차단 래퍼. 라이브 DB는 읽기 전용 URI로만 접근. 라이브 감사 최대 id: 실행 전 22998 → 실행 후 22999. 증가분은 실행 중인 라이브 watcher가 남긴 자체 기록이다(SHADOW는 쓰지 않음). 설치·Task 기반 호스트 SHADOW는 NOT_RUN |

## 3. 시험 기록 (재실행 없음)

- 전체 후보 시험 994 PASS / 0 FAIL / 12 SKIP (v0.2.32, 이전 Windows 결과).
- 관련 신규: race·복구 9건, 의도 검증 25건(이전 수행).
- 이번 단계에서 새 시험을 실행하지 않았다(코드 변경 없음).

## 4. 운영 전후 상태

- 라이브 watcher 2개 Running(pid 30904/31848 기준, 직전 검증), 설치·설정·위임 SHA 불변.
- 운영 DB 쓰기 0, GitHub 업무 레코드 쓰기 0, Telegram 0, 신규 모델 호출 0, 디스패치 0.
- 키·trust root·위임·LIVE 설정 변경 0.

## 5. 공개 게시 판단

- 코드 ZIP은 PUBLIC 저장소에 게시하지 않는다. 이 결과 문서는 비민감 상태·SHA·경로 요약만 포함한다.
- 자격정보, 개인키, 운영 DB 사본, 백업 본문은 게시하지 않았다.

## 6. LIVE 판정

LIVE_READY = **NO**. 막힌 항목:
1. 차기 후보 생성과 승인 경로 연결(단계 2, 6) — 폴더 생성 권한 필요.
2. v0.2.29 설치 트리 백업(단계 4) — 복사 권한 필요. 현재 존재하는 번들은 v0.2.25 기준이다.
3. 독립 리뷰(단계 7) — 보호 승인 필요.
4. 호스트 실운영 SHADOW(단계 8) — 설치·Task 승인 필요.
5. 비용 무상한 위험 수용(10단계) — 사용자 결정.

## 7. 권한 거부 기록

- 대상: 폴더 복사 명령(라이브 설치 트리 읽기 → dist 백업 경로, 또는 candidate 폴더 → v0_2_33).
- 계정: `ME`. 호스트: Windows 11, Git Bash 도구.
- 현상: 도구 권한 계층이 명령을 거부. 우회하지 않음, 다른 복사 도구(PowerShell 포함)로 재시도하지 않음.
- 필요 권한: 위 두 복사 작업을 허용하거나, 허용된 읽기 전용 복사 방식을 지정.

## 8. NEXT_ONE_ACTION

사용자에게 복사 권한(v0_2_33 생성, v0.2.29 트리 백업) 허용 여부를 묻는다. 허용되면 단계 2·3·4·6을 이어서 수행한다. 10단계 비용 위험 수용과 LIVE는 별도 승인 전까지 진행하지 않는다.
