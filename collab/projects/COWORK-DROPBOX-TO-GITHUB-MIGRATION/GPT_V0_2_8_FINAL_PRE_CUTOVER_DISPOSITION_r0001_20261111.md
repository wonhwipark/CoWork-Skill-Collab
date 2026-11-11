# GPT 최종 판정 — GitHub 전환 필수 게이트 v0.2.8
판정일: 2026-11-11 KST | 작업: COWORK-DROPBOX-TO-GITHUB-MIGRATION
Repository: PRIVATE `wonhwipark/CoWork-Skill-Collab` | branch: `main`

- **GPT_DISPOSITION: ACCEPT_WITH_CHANGE / PRE_CUTOVER_READINESS=PARTIAL**
- **CURRENT_LIVE: Dropbox v0.1.5** / **CUTOVER=MIGRATION_NOT_CUTOVER**
- **DEVELOPMENT=SELF_TEST_REPORTED** / **INDEPENDENT_REVIEW=NOT_RUN**
- **HOST_SHADOW=NOT_RUN** / **DB_LIVE_MIGRATION=NOT_RUN** / **PRODUCTION_CHANGED=false** (Claude 보고)
- 본 MD는 REQUEST/READY, 개발·운영 실행 지시, 서명키/토큰 발급, 반출 허가, 유료 리뷰 승인, LIVE 전환 승인이 아니다.

## 판정 근거 및 신뢰 수준
- 직접 원격 재조회 원문: `CLAUDE_CUTOVER_ESSENTIAL_GATES_RESULT_FOR_GPT_20261111.md` (GitHub blob `da3eb4b11713e64fa544ff4314f4731134029c3e`), `REVIEW_INPUT_MANIFEST_v0_2_8_FOR_GPT_20261111.md` (blob `f35e48d9fbcf58a30382a239dc08935f0fd23546`), 최신 `CURRENT.md`.
- 보고된 ZIP: `skill-collab-watcher_v0_2_8_1111.zip`, **173615 bytes**, SHA256 `c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa`. Windows 로컬 전용, **development_not_for_deployment**, GPT 원본 ZIP 바이트 직접 검증 `NOT_RUN`, PRIVATE 소스 ZIP `NOT_POSTED`. v0.2.6/v0.2.7은 폐기 보존.
- 개발자 자체 시험 보고: test venv **522 PASS/0 FAIL/12 SKIP**, 후보 ZIP 추출본 동일; Windows 운영 인터프리터 **487 PASS/0 FAIL/14 SKIP**, 실서명 모듈 일부 미실행. T 23 SYNTH/API_RO PASS, 3 PARTIAL, 12 NOT_RUN; S01~S10 시험키 실서명 PASS. **공식 독립 리뷰와 영수증은 없음.**

## 항목별 판정
| 이슈 | GPT 결정 | 근거 / 남은 조건 |
| --- | --- | --- |
| 문서·코드 불일치(런북이 폐기 SHADOW 설명) | **수정 수용** | v0.2.8에서 새 방식으로 수정·런북/코드 일치 회귀 추가했다고 보고. 변경된 ZIP 자체 리뷰는 NOT_RUN. 향후 변경 시 동일 검사 유지 |
| ZIP 헬퍼의 2초 경계 비결정성 | **수정 수용** | 원인 재현 및 고정 타임스탬프 수정, 200회·전체 10회 반복 0 FAIL 보고. 제품 런타임 결함으로 확대 해석 금지 |
| 과거 격리 임시 DB 사본 잔존 | **조치 수용(범위 한정)** | 자기 임시 폴더 삭제 보고. 추가 잔존 파일/민감정보 유출 없는지 확인은 NOT_RUN. 삭제를 기존 운영 데이터 정리 승인으로 확대 금지 |
| S-1 운영 DB 접근 SHADOW | **격리 코드/리허설 수용 / 호스트 PASS 아님** | 별도 `shadow.state_dir`, ShadowRunner, GitHub GET 7회·3사이클, 파일 핸들 tripwire, 원격 쓰기/모델 0. 실제 호스트 I/O 추적·설치 `NOT_RUN`. LIVE DB main/WAL/SHM에 어떤 신규 SHADOW 접근도 금지 |
| S-2 신뢰 루트 앵커 독립성 | **BLOCKED_TRUST (LIVE BLOCKER)** | 현 대화형 관리자 계정/프로필 구성에서는 자체 권한 검사로 LIVE 거부. 비관리자 전용 실행 계정 + 관리자만 쓸 수 있는 신뢰 루트·핀 폴더 + 승인자 기기 개인키 분리 후 실제 ACL/권한 검증 필요 |
| 승인자 서명 도구·시계 역행 보호 | **격리 시험 수용** | `approval_signer.py` 및 고수위 시계 가드 자체 보고. 유효 운영 키·실제 승인자 서명·운영 사용자 권한 분리 미실행 |
| F1 보존 및 DB·알림 리허설 | **사본 리허설 수용 / 운영 적용 보류** | 원격 Dropbox F1은 READY 없는 대기 상태로 보존; 스냅샷 사본 이행·rollback/receipt·watermark 중복 0 보고. 실제 운영 F1 HOLD/DB 이행·복원·전환 NOT_RUN |
| ZIP 보안검사·소스 반출 분류 | **로컬 검사 결과 참고 / 외부 반출 보류** | 항목 70개, manifest, CRC/secret 검사 자체 보고. 파일별 분류표 자체로 사용자의 PRIVATE 반출 승인을 대체하지 않음 |
| 정식 독립 리뷰 | **NOT_RUN** | 개발·자체 시험과 별개인 독립 실행, 적법한 서명 REQUEST/READY, 원문+영수증, 비용 승인 필요 |

## 추가 정확성 검증 요구
- **시험 수집 수 불일치:** 시험 venv는 `522+12=534`건인데 운영 인터프리터는 `487+14=501`건으로 총 수집 수가 33건 적음. 보고서에 '실서명 두 모듈 35건이 건너뜀'이라고 되어 있지만 `SKIP` 증가만으로는 33건이 수집되지 않은 이유가 설명되지 않음. 같은 코드/옵션인지 `pytest --collect-only`와 구체적 import skip/collection/selection 로그를 **격리 조건에서** 확인하고 PASS/SKIP/NOT_COLLECTED를 구분; 이 차이를 운영 호스트 전부 PASS로 오인하지 말 것.
- **현재 LIVE가 관리자 계정에서 동작:** 격리 SHADOW 테스트를 위한 신규 비관리자 계정/권한 분리와 운영 Dropbox watcher 변경을 구분. 1차 작업에서 기존 감시기를 다른 계정으로 무단 재구성하지 말 것.
- **실 SHADOW/전환 판정의 증거:** 합성 tripwire가 실제 Windows 운영 파일 I/O 접근 0을 보장하지 않음. 실제 호스트 프로세스 파일 open/path/file identity·WAL/SHM 접근 및 네트워크 GET-only 실측 완료 전 SHADOW=PASS 금지.
- **재부팅 무로그온 시작:** 별도 UX/가용성 트랙. GitHub LIVE 전환 필수 차단 항목으로 추가하지 않음.

## LIVE 전환 8게이트
| 게이트 | GPT 판정 |
| --- | --- |
| 1 실제 호스트 SHADOW read-only | NOT_RUN |
| 2 신뢰 루트/키/ACL/승인자 서명 실제 검증 | **BLOCKED_TRUST** |
| 3 소스 ZIP 반출 승인 + PRIVATE raw SHA 검증 | NOT_RUN |
| 4 독립 리뷰 실행 + 결과·영수증 | NOT_RUN |
| 5 F1 무손실 보존/최종 정산 | PARTIAL (실처분 미실행) |
| 6 운영 DB 백업/복원/실이행 준비 | PARTIAL (사본 리허설만) |
| 7 단일 provider·재호출/알림 중복 0 | PASS (SYNTHETIC/COPY), REAL HOST NOT_RUN |
| 8 최종 사용자 LIVE 승인 | NOT_APPROVED |

## 1차 승인 묶음(현재 **요청**; GPT가 승인하지 않음; LIVE 전환 제외)
1. **호스트 최소 권한 분리**: 시험용 비관리자 계정과 관리자 전용 trust root·config ACL 구성(기존 Dropbox LIVE 계정/스케줄러/DB 불변 유지).
2. **승인자 키 준비**: 승인자 소유 기기에서 개인키 생성, 공개 trust root와 pin 배치 및 위협 모델/ACL 검증. 운영 비밀 GitHub 게시 금지.
3. **HOST SHADOW 격리 시험**: 별도 폴더/READ-ONLY contents 토큰/기간·중단 조건 설정 후 모델 0·Telegram 0·원격 쓰기 0·운영 DB 접근 0을 실제 파일 I/O로 확인. 새 계정에서 인증이 불가하면 승인 없이 자격 재발급/권한 상향 금지.
4. **PRIVATE 소스 게시 분류 승인**: 파일별 출처·반출 가능 여부를 사용자/내부 권한 기준으로 확인한 뒤 허용된 ZIP에 한하여 신규 파일로 게시하고 원격 바이트 SHA 검증; 불명확한 파일은 로컬 보존.
5. **정식 Claude 독립 리뷰 1회**: 유효 서명/README·고정 커밋·ZIP 해시·정책 검증과 비용 승인 후 `STATIC <=$1` 상한 1회. 변경분·S-1/S-2 중심 검토. 비용 상한 초과 예상·조건 미충족 시 모델 호출 0, 상한 증액은 신규 승인.
- 일부 단계 차단 시 승인 가능한 시험/문서 작업은 계속하되 `BLOCKED/NOT_RUN` 기록. **권한·서명·토큰·유료 리뷰·파일 반출을 사용자 메시지 없이 실행하지 말 것**.
- **2차 별도 승인:** 운영 DB 안전 백업·이행/rollback, F1 실제 hold/처분, 단일 GitHub LIVE 전환과 Dropbox 종료·복구 계획. 1차 승인만으로 2차 수행 불가.

## 다음 한 동작
- 사용자에게 위 1차 승인 묶음을 1회에 제시하고 명시적 승인 여부 확인. 승인 전 현 LIVE/스케줄러/DB/Telegram/키/토큰/모델 불변.
- 승인 뒤 Windows Claude Code 원샷 인계(정확한 repo/branch/path 포함)로 안전 구현·호스트 시험·문서 readback까지 묶어 실행. 독립 리뷰는 개발 세션과 별도의 유효 REQUEST/READY 및 receipt로만 PASS 판정.
