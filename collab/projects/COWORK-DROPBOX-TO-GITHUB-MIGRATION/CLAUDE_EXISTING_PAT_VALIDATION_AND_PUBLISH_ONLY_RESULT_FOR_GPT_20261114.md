# CLAUDE 기존 PAT 검증 + publish-only 결과 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-14 KST). **Claude 자체 보고**, GPT 판정 전 canonical 아님.
- 근거 인계서: `GPT_EXISTING_PAT_VERIFY_AND_PUBLISH_ONLY_ONE_SHOT_r0001_20261114.md`
- 금지 항목(운영 DB·Task·Notifier 변경, 추가 유료 리뷰, 모델 재호출, cryptography 운영 설치, LIVE, 새 PAT 임의 발급): **실행 0건**. 사용자에게 토큰 붙여넣기를 요청하지 않았다.

## 1. 구분별 결과

| 항목 | 결과 |
|---|---|
| PAT_CANDIDATES_CHECKED | **2** (이 PC의 감시기 전용 자격 폴더의 JSON 2개; 환경변수 후보 0; PUBLIC 저장소용 토큰은 범위 밖이라 검사 안 함; 개발자 `gh` 로그인은 감시기 PAT로 인정하지 않는 규칙에 따라 제외) |
| PAT_ELIGIBILITY | **FAIL → ACTION_REQUIRED_TOKEN_SCOPE_OR_EXPIRY** (적격 후보 0) |
| INSTALL | **NOT_RUN** (적격 토큰 없음 — 부적격 토큰을 감시기용으로 설치하지 않음) |
| WRITE_PROBE (임시 브랜치) | **NOT_RUN** (같은 이유). 실패 사례는 R2 실행에서 이미 실측: 읽기전용 토큰의 `PUT` → HTTP 403(`UPLOAD_FAILED`) |
| PUBLISH_ONLY (R2 결과) | **PASS** (아래 §3) |
| MODEL_CALL_DELTA | **0** (`new_paid_review_count=0`, `notification_sent=0`) |
| CLEANUP | **해당 없음** (임시 브랜치 만들지 않음 → `CLEANUP_PENDING` 없음) |
| 서버 repo ID 대조 | **PASS** — GitHub 서버가 반환한 숫자 ID가 신뢰 루트 라벨 `1451933830`과 일치, 비공개 저장소 확인. **제품의 runtime repo_id 결합이 구현됐다는 뜻이 아님**(N2 LIVE 게이트 유지) |

## 2. 기존 PAT 검증 (비밀 비노출, 서버 응답 기준)

- 방법: 로컬 JSON을 메모리에서만 읽어 실제 GitHub 서버에 인증. JSON의 `repo`/`scope` 필드는 **판정에 쓰지 않음**. 토큰 종류는 서버의 `x-oauth-scopes` 헤더 유무, 만료는 서버의 `github-authentication-token-expiration` 헤더, 범위는 `/user/repos?visibility=private` 결과로 확인. 값·접두·길이·해시·경로·계정 식별정보는 출력/게시하지 않음.
- 판정 기준(인계서): fine-grained, 승인된 비공개 저장소 1개만, 서버 만료가 1~90일, 쓰기 부정 대조 통과.
- `permissions.push/admin`은 **토큰이 아니라 계정 역할**을 반영하고(서버 응답으로 확인), fine-grained 토큰도 `/user/repos`에 공개 저장소를 포함하므로 이 두 값은 판정에서 제외(처음 버전 프로브가 이 때문에 오판정해 수정·재실행함). 실제 쓰기 권한은 임시 브랜치 쓰기 프로브로만 확정할 수 있는데 적격 토큰이 없어 NOT_RUN.

| 후보 | fine-grained | 서버 만료(1~90일) | 비공개 저장소 1개만 | 결과 |
|---|---|---|---|---|
| 1 (감시기 읽기 전용 파일) | PASS | **FAIL(만료 없음)** | PASS | 부적격 — 읽기 전용(R2 업로드 403 실측)이며 만료 없음 |
| 2 (감시기 쓰기 파일) | **FAIL(classic)** | **FAIL(만료 없음)** | **FAIL(광역)** | 부적격 — classic 광역 토큰 |

- 안전장치: `POST`형 부정 대조(이슈 생성 시도)는 앞선 검사를 **모두 통과한 토큰에만** 실행하도록 설계 — classic 광역 토큰에 쓰기 호출이 가지 않게 함(쓰기 호출 0건).
- 확인 불가 범위: 사용자가 "이미 가지고 있다"고 한 PAT가 **이 PC에 파일/환경변수로 없다**는 것까지만 확인했다. Windows 자격 증명 관리자·다른 계정·다른 PC·브라우저의 토큰은 열람하지 않았다.
- 참고(정정): 앞선 단계에서 토큰 종류와 길이를 로컬 콘솔에 한 번 출력했다(비게시, 값·접두 문자열 자체는 아님). 이후 프로브는 종류/길이를 출력하지 않는다.

### ACTION_REQUIRED_TOKEN_SCOPE_OR_EXPIRY (이 분기에서만 사용자 조치)
- 실패 조건: ① 쓰기 토큰 파일이 classic·광역·무기한, ② 읽기 전용 토큰은 무기한이며 쓰기 권한 없음.
- 사용자 선택지: (a) 이미 갖고 계신 PAT가 위 조건(fine-grained, `CoWork-Skill-Collab` 단일, Contents Read and write, 만료 90일 이하)이면 **`Install-EngineWriteToken.ps1`로 숨김 입력 설치**(채팅에 붙여넣기 금지), (b) 아니면 해당 조건으로 신규 발급. 설치 후 "쓰기 토큰 설치 완료"라고 알려주시면 `verify_engine_write_token.py --live`(임시 브랜치)만 실행한다. 검증기의 만료 판정은 파일 필드가 아니라 서버 헤더를 쓰도록 보강할 예정(현재 `probe_existing_pats.py`가 서버 기준 판정 제공).

## 3. R2 결과 publish-only / 재확인 (모델 호출 0)

- 대상: `REQ-COWORK-V0217-R2-20261114` rev 1, ZIP sha256 `824f26c4e28fcc804ed1dd3942a34408c54b9091be34ecb1693cc4cb9d46df03`, `POLICY-STATIC-V1-LARGE`.
- **원격 vs 로컬 보관본 바이트 비교**(`main`의 현재 파일): `REVIEW_RESULT_1.md`(20255 B, sha256 `a740ba59363d…`), `RECEIPT_1.md`(317 B, `ef936df320ba…`), `USAGE_RECEIPT_1.json`(2151 B, `bccb9e72bf5a…`) 모두 **동일** → `ALREADY_PUBLISHED`(덮어쓰기 0, 신규 게시 0).
- **격리 원장 사본에서 정상 publish-only 경로 실행**(원본 원장·운영 DB 미사용): 사본의 작업 상태 `UPLOAD_PENDING`(시도 1) → **`COMPLETED`**, 이벤트 `UPLOAD_RETRY_COMPLETED` 1. 엔진은 원격 파일이 이미 있으면 업로드 없이 GET으로 결과/영수증 정체성을 readback 확인 후 완료 처리(코드 경로와 일치).
- 증거: HTTP는 `GET api.github.com` 14회뿐(쓰기 0), 하위 프로세스 시작 0, `claude` 경로는 **존재하지 않게** 설정(모델 시작 구조적으로 불가), 디스패치 0, 라이브 폴더 파일 열기 0·SQLite 연결 0, 원본 격리 원장 해시 불변. 신규 서명·APPROVAL·READY 생성 0. SHADOW 모드로는 쓰기 동작 수행 안 함.
- 의미: 쓰기 토큰 없이도 **이미 게시된 결과의 완료 정리는 읽기 전용으로 가능**함을 실측(읽기 전용 GET으로 readback). 단 **결과를 처음 게시하는 자동 업로드 E2E는 여전히 NOT_RUN**(적격 쓰기 토큰 필요).

## 4. 남은 LIVE 게이트 (REMAINING_LIVE_GATES)

1. 감시기 전용 적격 쓰기 PAT 설치 + 임시 브랜치 쓰기·readback 실측 (**ACTION_REQUIRED**), 그 후 엔진 자동 업로드 E2E.
2. 운영 인터프리터 `cryptography` 설치/반입 및 실호스트 서명 검증 E2E (운영 변경 승인 필요).
3. repo_id 원격 신원 결합(N2), nonce 재사용 방지·상태 소실 절차(N1), 데드코드·taskkill 로그(S1/S2) → 수정 시 새 후보 + 재리뷰 승인.
4. 별도 계정 enforce SHADOW + 네이티브 I/O 추적(관리자), 장기 SHADOW.
5. Notifier 2개 동시 실행 원인 확인 및 GitHub 연동 비발송 리허설.
6. 컷오버·롤백 리허설, 단일 ACTIVE_PROVIDER 확인 후 사용자 **별도 최종 승인**. 현재 `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.

## 5. 한계

- 서버가 토큰의 세부 권한(예: Contents write)을 직접 노출하지 않아, 쓰기 권한은 **쓰기 프로브로만 확정**된다. 이번에는 적격 후보가 없어 그 단계가 실행되지 않았고, 따라서 쓰기 권한 자체는 판정하지 않았다(만료·종류·범위 조건에서 이미 탈락).
- 비밀값·토큰·경로·계정명은 이 문서에 없다.
