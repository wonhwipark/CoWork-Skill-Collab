# CLAUDE B안 / v0.2.17 R2 / SHADOW·DB 리허설 통합 결과 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-14 KST). **Claude 자체 보고**이며 GPT 판정 전 canonical 아님.
- 근거 인계서: `GPT_B_R2_SHADOW_APPROVAL_AND_ONE_SHOT_r0001_20261114.md`
- 승인 밖 항목(기존 리뷰 재호출, 추가 유료 리뷰, R0~R3 상시 자동화, 운영 DB·Task·Notifier 변경, 알림 발송, GitHub LIVE 전환, PUBLIC 게시, 새 PAT 임의 생성): **실행 0건**. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` 유지.

## 1. 한눈에 보기

| 구분 | 상태 | 요약 |
|---|---|---|
| ① 쓰기 PAT (B안) | **ACTION_REQUIRED** | 현재 쓰기 토큰 파일은 classic(40자, 만료 없음)으로 조건 미충족. fine-grained 발급은 GitHub 웹 UI 사용자 조작 필수. 설치 스크립트·검증기는 준비·시험 완료 |
| ② v0.2.17 R2 독립 리뷰 1회 | **DONE** | 모델 호출 1회, $0.9946(≤$3), BLOCKING 0건·비차단 3건. 엔진 게시는 읽기전용 토큰이라 403 → `UPLOAD_PENDING`, 개발자 `gh`로 동일 바이트 게시 |
| ③ 실호스트 SHADOW(읽기전용) | **PASS(부분)** | 모델 0·GitHub 비-GET 0·Telegram 0·라이브 DB 무변경. 별도 계정 강제(enforce)와 네이티브 파일 I/O 추적은 NOT_RUN(관리자 필요) |
| ③ 운영 DB 안전 백업·격리 복구 | **PASS** | 원본을 SQLite로 열지 않고 바이트 복사. 무결성 ok, 건수 일치, 원본 main/WAL 해시·stat 불변 |
| 17 SKIP 분류·crypto 호환 | **DONE** | §6 |
| Notifier 연동 | **NOT_RUN(비발송 분석만)** | §7 |

## 2. 고정된 v0.2.17 산출물 (리뷰 대상)

- ZIP `skill-collab-watcher_v0_2_17_1114.zip`, **232575 B**, sha256 `824f26c4e28fcc804ed1dd3942a34408c54b9091be34ecb1693cc4cb9d46df03`. 91개 파일, ZIP 무결성 OK, 경로 이탈·절대경로 항목 0, 비밀 스캔 findings 0, **재빌드 시 바이트 동일(결정적)**.
- 리뷰 전 추가 패치 **없음**(고정 후 바이트 불변). v0.2.14/v0.2.16 ZIP 및 이전 리뷰 결과 불변.
- 시험(고정 ZIP을 새로 풀어 실행): 시험 venv(cryptography 포함) **644 PASS / 12 SKIP**, 운영 인터프리터 **578 PASS / 17 SKIP**. FAIL 0.
- v0.2.14 → v0.2.17 diff: 20개 파일, 1111줄(`diff_v0_2_14_to_v0_2_17.patch`).
- 게시 위치(PRIVATE main, 원격 바이트·SHA·ZIP CRC 확인): `review-inputs/REV-COWORK-V0217-R2-20261114/` {ZIP, REVIEW_MANIFEST.md, patch} (commit `154b8e9a602f` / `eada1add78a4` / `bc0141b112ab`).
- 리뷰 범위에서 의도적으로 **패치하지 않은 것**: repo_id 원격 신원 결합(알려진 갭으로 명시해 리뷰에 넘김). 설계 변경이라 후보 바이트를 흔들 수 있어 별도 승인 후 다루는 것이 안전하다고 판단.

## 3. R2 독립 리뷰 실행 사실

- 요청 `REQ-COWORK-V0217-R2-20261114` rev 1, `POLICY-STATIC-V1-LARGE`, effort medium, 최대 $3. commit A(패키지+요청) `af9b0a89cd05` → commit B(APPROVAL_SIG `56b7c8679d0e`, SOURCE_PIN `bdba42a45a64`, READY 마지막 `4c35ca4bf9df`). 승인 유효 2시간, 서명키는 A안에서 준비한 동일 키(지문 `9c6f650ce89d…`), `trust_root_independence=warn`.
- 드라이런(모델 0): GET 16, `VALIDATED`. 이어서 실제 1회: 디스패치 1, 승인 후 **모델 호출 정확히 1회**, 재호출 0.
- 비용·사용: **$0.9946**(상한의 33%), 23 turns, 출력 18,029 토큰, 캐시 생성 89,330 / 캐시 읽기 617,912. **R2 목표(5 turns, 40k/6k)는 초과**(비용 상한만 강제 가능, `--max-turns` 미지원 재시도 안 함). 소요 약 230초.
- 엔진: v0.2.16(리뷰에 쓰인 감시기) / 대상: v0.2.17. 엔진 쓰기는 읽기전용 토큰 때문에 HTTP 403 → `UPLOAD_PENDING`, 모델 재호출 0(설계 동작). 개발자 `gh` 로그인으로 엔진이 올렸을 바이트를 게시:
  `REVIEW_RESULT_1.md` commit `c2aeee1757d0`(20255 B), `RECEIPT_1.md` `7977241953c9`, `USAGE_RECEIPT_1.json` `c1429f10d07d`; 전부 원격 바이트 일치. (경로 `collab/reviews|receipts/REQ-COWORK-V0217-R2-20261114/`)
- 독립성: 별도 프로세스, 빈 작업 폴더, 도구 Read/Grep/Glob, dontAsk, MCP 0, 세션 비저장, 개발 세션 문맥 미공유. 정적 리뷰: 리뷰어는 코드를 실행하지 않았고 모든 시험 PASS는 코드 추적에 의한 판단이다.

## 4. 리뷰 지적과 내 검증 (최종 판정은 GPT)

BLOCKING **0건**. F1~F5 수정과 usage-limit 대기/재개는 코드·시험 기준으로 이상 없다고 판단(실행 재현은 하지 않음).

| ID | 내용 | 내 코드 검증 | 제안 판정 |
|---|---|---|---|
| N1 | 승인 nonce 재사용 방지 저장소 없음. 재사용 방지는 로컬 SQLite의 `jobs` 중복 차단에만 의존 → 상태 DB 소실·재구축 후 같은 승인 번들이 재검증돼 2차 유료 리뷰 가능 | **확인**(nonce는 길이 검사만, 저장 테이블 없음) | MINOR(LIVE 전 문서화 또는 `used_approval_nonces` 추가). |
| N2 | repo_id는 라벨(서명·핀·신뢰 루트 문자열 비교)이며 GitHub 실제 저장소 ID와 결합되지 않음 | 알려진 갭 재확인. 키 없이는 위조 불가, 같은 trust root를 다른 저장소에 쓰면 승인이 통용되는 운영 위험 | LIVE 전 게이트로 유지(수정은 새 후보+재리뷰 필요) |
| N3 | 토큰 파일의 `repo` 검사는 권고용(토큰 실제 범위 미검증) | 확인 | 보안 경계 아님을 문서화 |
| S1 | `find_logical_job` 호출처 없음(데드코드) | **확인**(정의만 존재) | 정리 권고 |
| S2 | `_kill_tree`가 `taskkill` 반환값을 버림 | **확인**(`check=False`, 미기록) | 경고 로그 추가 권고 |
| 리뷰어 미검증 | Q8 복합 시나리오(usage-limit+재시작+정책 개정+커서 손실+락)는 코드 순서 추론만, 실제 한도 메시지 문자열 미관측 | — | 호스트 시험으로 보완 필요(GPT 판단) |

- 위 수정은 **적용하지 않았다**(리뷰 후 후보 변경은 기존 리뷰 승계 불가 + 신규 승인 필요). 필요하면 v0.2.18로 별도 승인.

## 5. 쓰기 PAT (B안) — ACTION_REQUIRED

- 현황(값 미노출 확인): 읽기전용 토큰 = fine-grained, Contents 읽기 전용, 단일 저장소, 만료 없음. 쓰기 토큰 파일 = **classic 40자, 만료 없음** → 인계서의 "만료형 fine-grained·단일 저장소 최소권한" 불충족이라 감시기용으로 **사용하지 않음**. 개발자 `gh` 로그인(광역 `repo` 범위)도 감시기용으로 재사용하지 않음.
- 사용자 필요 조치(웹 UI, 대체 불가): 저장소 `CoWork-Skill-Collab` **한 개만** 선택, 권한 Contents Read and write(Metadata Read 자동)만, 만료 90일 이하로 fine-grained PAT 생성.
- 준비된 도구(로컬 `b_r2/token_write`, 비밀 없음; 실측 범위 = 오프라인 판정 로직 8케이스 불일치 0 + 설치 스크립트 PowerShell 구문 오류 0, **실제 설치·라이브 GitHub 검증은 NOT_RUN**): `Install-EngineWriteToken.ps1`(숨김 프롬프트, 사용자 전용 ACL, 동기화 폴더 거부, 기존 파일 덮어쓰기 거부, `github_pat_` 접두 검사)와 `verify_engine_write_token.py --live`(형식·만료≤120일·단일 저장소 가시성·권한 부정 대조 2종·**임시 브랜치**에서만 쓰기 프로브 후 브랜치 삭제 → main·요청·영수증 무손상). 토큰 설치 후 "쓰기 토큰 설치 완료"라고 알려주시면 검증만 수행한다.
- 현재 결과 영향: 설치 전까지 엔진 자동 업로드 E2E는 **NOT_RUN**(서버 측 쓰기 403 동작만 실측).

## 6. 실호스트 SHADOW + 운영 DB 리허설

### 6.1 SHADOW (고정 v0.2.17 바이트, 실제 PRIVATE 저장소, 분리 상태 폴더)
- 모드·상태 분리: R2 모델 리뷰와 별도 프로세스·별도 상태 DB. 시험 venv와 운영 인터프리터 **둘 다** 실행: `scan` 1회 + `watch` 2 사이클 + `status`.
- 결과(두 인터프리터 동일): 모델 호출/하위 프로세스 시작 **0**(감사 훅), HTTP는 **GET api.github.com만**(scan 14, watch 14), 비-GET 0, Telegram/타 호스트 0, 디스패치 0(`DISPATCH_SKIPPED_NOT_ALLOWED`), 자체 DB에 `VALIDATED` 1건, 종료코드 0.
- 라이브 폴더 접근: 프로세스 내부 감사 훅 기준 라이브 폴더 파일 열기 **0**, 라이브 폴더 SQLite 연결 **0**. 운영 DB main/WAL 해시·stat **불변**.
- **관측(개입 아님)**: 라이브 `-shm` 수정 시각이 유휴 상태에서도 약 30초마다 갱신됨 → 실행 중인 Notifier(`notify_reviews.py --watch`)의 주기 폴링으로 귀속, SHADOW와 무관(SHADOW 중 감사 훅 0, 유휴 관찰에서도 동일 주기).
- **한계(NOT_RUN)**: ① 다른 Windows 계정에서 `account_isolation=enforce`로 실행(관리자·시험 계정 활성화 필요) — 현재는 `warn`, 같은 계정. ② ETW/Procmon 네이티브 파일 I/O 추적(관리자 필요) — 감사 훅은 파이썬 수준 증거이며 네이티브 열기는 못 잡음. ③ 장기간(예: 수 시간) SHADOW. 라이브 폴더 신원 확인(핸들 열기)은 가드가 수행하나 DB 파일은 열지 않음.

### 6.2 운영 DB 안전 백업·격리 복구 (비밀·경로 미게시)
- 방법: **원본을 SQLite로 열지 않음**(`mode=ro`도 `-shm`을 건드림). main·WAL 바이트만 읽어 격리 폴더로 복사, 복사 전후 원본 해시·stat 비교. `-shm`은 복사 안 함.
- 원본: main 1,896,448 B(sha256 `4e8bc33a6f6e…`), WAL 2,331,952 B(sha256 `59de75073464…`); 복사 중·후 main/WAL 해시·stat **불변**, 복사본 바이트 동일.
- 복사본(WAL 복구는 복사본에서만): `integrity_check`=ok, jobs 61(COMPLETED 60, CONFLICT 1), audit_log 22,907, cursors 1, counters 8, pending_requests 1, 진행 중(CLAIMED/REVIEW_RUNNING) 0.
- 백업 파일: 1,908,736 B(sha256 `3913856b85fa…`), 무결성 ok, 건수 일치.
- 격리 복구: 운영 폴더 밖 경로에 복원 → 백업과 바이트 동일, 무결성 ok, 건수 일치. 운영 경로 덮어쓰기 0.
- 호환: 복사본을 v0.2.17 코드로 열기 → 열림, 무결성 ok, 기존 5개 테이블 건수 보존, 신규 테이블 3개(`provider_lease`, `provider_history`, `job_claims`) 생성. (복사본 한정 — 운영 DB 마이그레이션 아님)
- 백업·복사본은 운영 데이터이므로 **로컬 전용**, 게시 안 함.
- 롤백 체크리스트(설계·미실행): ① 감시기·Notifier 정지 확인 → ② 원본 main/WAL/SHM 보존본 확보 → ③ 복원 대상은 항상 새 경로 → ④ 복원본 `integrity_check`·건수 대조 → ⑤ 운영 교체는 별도 승인.

### 6.3 SKIP 분류·crypto
- 시험 venv 12 SKIP = GUI 실창 시험 8(`SKILL_COLLAB_GUI_TESTS=1` 선택) + 프로젝트 `.venv` 필요 4(환경 사유).
- 운영 인터프리터 17 SKIP = 위 12 + **`cryptography` 미설치로 인한 5**(Ed25519 서명·키 보호·E2E·R1 회귀 시험). 운영 인터프리터에는 `cryptography` 없음(Python 3.11.9) → 승인 서명 검증이 **한 번도 실행되지 않음**. 코드는 fail-closed(`default_backend()`=None → `APPROVAL_UNVERIFIABLE`, 재시도, 모델 0)로 리뷰어도 확인. 따라서 **운영 환경에 설치하지 않는 한 LIVE에서 모든 승인이 검증 불가로 대기**한다. 운영 설치는 미승인이라 변경하지 않음.

## 7. Notifier·GitHub 연동 (비발송 분석만)

- 관측: `notify_reviews.py --watch` 프로세스가 **2개** 동시에 실행 중(서로 다른 인터프리터). 중복 알림 위험 가능성 — 원인·영향 미확인, 변경하지 않음.
- Notifier는 운영 DB를 주기적으로 읽는다(`-shm` 갱신). GitHub 이행 시에는 SHADOW 상태 DB·영수증을 보도록 소스 전환이 필요하며 현재 GitHub 연동은 **NOT_RUN**(알림 발송 0, 설정 변경 0, 예약 작업 변경 0).

## 8. 남은 LIVE 차단 항목

1. 쓰기 PAT 사용자 발급(ACTION_REQUIRED) 후 엔진 자동 게시 E2E 실측.
2. 운영 인터프리터에 `cryptography` 설치/잠금 파일 반입(운영 변경 승인 필요) 및 실호스트 서명 검증 E2E.
3. repo_id 원격 신원 결합(N2), nonce 재사용 방지 또는 상태 소실 절차(N1), 데드코드·taskkill 로그(S1/S2) → 수정 시 v0.2.18 + 재리뷰 승인.
4. 별도 계정 enforce SHADOW + 네이티브 I/O 추적(관리자), 장기 SHADOW.
5. Notifier 중복 프로세스 원인 확인 및 GitHub 연동 비발송 리허설.
6. 컷오버·롤백 리허설, 단일 ACTIVE_PROVIDER 확인, 그 후 사용자 **별도 최종 승인**.

## 9. 한계와 정직한 구분

- 자체 시험 PASS와 R2 리뷰는 서로 다른 증거다. 리뷰는 정적이며 코드 실행 없음, Windows 전용(Linux·사내 LLM·MCP 미검증).
- R2 목표(5 turns, 40k/6k 토큰)는 강제 불가였고 초과했다(비용 상한만 준수).
- 비밀값·토큰·경로·계정명은 이 문서에 없다.
