# GPT 최종 전환 준비 판정 — watcher v0.2.4
판정일: 2026-11-11 KST | 프로젝트: COWORK-DROPBOX-TO-GITHUB-MIGRATION
REPO: PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
GPT_DISPOSITION: **ACCEPT_WITH_CHANGE / PARTIAL**
CUTOVER: **MIGRATION_NOT_CUTOVER** | ACTIVE_PROVIDER: **기존 Dropbox LIVE 유지**
DEVELOPMENT: **SELF_TEST_REPORTED** | INDEPENDENT_REVIEW: **NOT_RUN**
본 판정 문서 자체는 REQUEST/READY가 아니며 리뷰/운영/과금/LIVE 승인 신호가 아니다.

## 1. 판정 대상과 증거 수준
- 원문 `CLAUDE_FINAL_PRE_CUTOVER_GATE_RESULT_FOR_GPT_20261110.md` 및 `REVIEW_INPUT_MANIFEST_v0_2_4_FOR_GPT_20261110.md`를 GPT가 PRIVATE main에서 직접 재조회.
- 개발 후보 `skill-collab-watcher_v0_2_4_1110.zip`, **146879 bytes**, 보고 SHA-256 `854d2d324033dac77771ed7145feabf0a659b3450d7b7579c54f487ae3f6ed20`. ZIP은 Windows 로컬에만 있으며 PRIVATE에 게시되지 않음. GPT의 **바이트 해시 검증/소스 독립 리뷰/실행 시험은 NOT_RUN**.
- 개발 세션 자체 시험: **410 PASS / 0 FAIL / 12 SKIP**(GUI 실창 8, 프로젝트 .venv 조건 4). 압축 해제본 재시험도 동일하다고 보고. 지난 348 PASS 대비 +62건은 B-7 보안 게이트 51건 + 신뢰 루트 도구 11건.
- 수락시험 T01–T38: **23 PASS(SYNTH) / 3 PARTIAL / 12 NOT_RUN**. S01–S10: **10 PASS(REAL TEST-KEY)**. Windows 운영 기기 호스트 SHADOW·정식 유료 독립 리뷰는 별도 NOT_RUN. 자체시험 결과를 독립 리뷰 PASS로 소급하지 않음.

## 2. 조건부 수용
| 영역 | GPT 판정 | 근거 및 잔여 조건 |
|---|---|---|
| 미정산 F1 요청 1건 | **설명 수용, 실제 정산은 미완료** | 65 요청 = 작업 있는 정상쌍 60 + REJECTED 쌍 3 + 불완전 2. F1은 READY 없이 정상 WAIT_INPUT, 운영 DB pending 1건과 동일. 현재 대기를 **보존**해야 하며 실제 PENDING_HELD 기록/전환은 실행 안 함. |
| 불완전 F2/거부 G1–G3 | **설명 수용** | F2 완료 이력 1, G1–G3는 검증 거부 3; 과거 재호출 0이라는 정적/사본 증거. 이력/영수증 원문 및 실제 운영 상황은 추후 변화 가능. |
| 실데이터 65개 차이시험 | **조건부 수용** | 구 버전과 후보 판정 64개 동일, 1건은 동일 원인으로 최종 거부하며 검증 시점만 달라졌다는 개발자 보고. 실제 모델 호출 0. |
| B-7 운영 신뢰키 수명주기 | **개발 구현/격리시험 수용** | 키 상태/회전·폐기·frozen/ACL/핀/래칫/시계 오차 시험 보고. 실제 운영 signer·공개 루트·보안 ACL 설정 및 승인 서명 도구는 NOT_RUN. |
| DB 사본 전환·롤백 | **사본 리허설 수용** | 운영 3개 테이블 이행, 구버전/복원, cursor/lease·notifier watermark 증거. 운영 DB 실제 이행·정지 시점·백업/복원은 미승인. |
| SHADOW 3사이클 | **부분 수용 (핵심 주의 있음)** | 운영 폴더 사본 + 실 PRIVATE GitHub GET 9회, 모델/Telegram/remote write 0. **호스트 실제 설치·가동 없음. SHM 바이트 변경 관측**. |
| ZIP·독립 리뷰 | **보류** | 로컬 64항목 ZIP의 SHA·CRC·비밀검사는 Claude 자체 보고; 실제 ZIP 제공/반출 분류/독립 리뷰+영수증 미실행. |

## 3. GPT가 발견한 추가 차단/검증 사항 — 특히 SHM
**S-1: WAL SHM 쓰기 영향 — BLOCKING BEFORE HOST SHADOW**
- Claude 보고: SHADOW의 SQLite `mode=ro`로 DB 메인 파일과 WAL은 동일하나 **SHM 파일은 변경**. 단순히 "SHM은 파생 인덱스"라며 무조건 예외 처리할 수 없음. 프로젝트 운영 규칙은 읽기 전용 관찰에서도 DB main/WAL/SHM에 발생하는 영향을 점검하도록 요구한다.
- SQLite 공식 문서에 따르면 `-shm`은 WAL 인덱스 공유 메모리이며 읽기 연결도 read-mark/잠금을 위해 shm 상호작용이 있을 수 있음: https://www.sqlite.org/wal.html , https://www.sqlite.org/walformat.html .
- **중요한 구분:** 사본 SHM의 바이트 변화가 곧 운영 본체 손상이라는 뜻은 아님. 하지만 **호스트 운영 SHM 불변이 입증됐다는 뜻도 아님**. 기존 WATCHER/Notifier 가동 중 영향이 없어야 하는 경계를 확인할 수 없다면 실 호스트 SHADOW PASS를 선언하지 말 것.
- 우선 격리 사본에서 "운영 DB main/WAL/SHM 파일 3종 모두 절대 무쓰기"를 충족하는 방식 또는 **완전히 독립된 일관성 보장 스냅샷**을 연구·재시험한다. SQLite WAL 경유 조회의 정합성과 checkpoint/복원 가능성을 유지하면서 변경/잠금/권한 0 영향 실측. 단순히 `immutable=1`을 운영 중 WAL DB에 덧붙여 정합성 문제를 만들면 안 됨. SHM 변경이 불가피하면 정식 요구 변경의 안전 근거와 사용자 별도 승인이 선행되어야 한다.
- 준비 시험에서는 snapshot provenance/DB main-WAL-SHM SHA, 작업 수·데이터 식별 무노출, 단일 LIVE·중복 알림 0, 실제 GitHub GET only, 실패 시 fail-closed를 요구.

**S-2: 신뢰 루트 앵커 독립성 — BLOCKING FOR LIVE**
- `trust_root_sha256` 핀과 trust root 본문이 동일 권한 영역에서 동시에 바뀌면 해시 핀만으로 비인가 교체를 막는다는 주장이 충분하지 않음. 운영 루트·핀/ACL·version ratchet의 수정권한이 실제 signer 승인 경계와 분리됐는지 **Windows 실 ACL 및 rollback/restart 실측** 필요.
- GitHub Date와 로컬 시간 5분 비교는 기술적 개선이지만 위조/시간 역행/시간원 불능 시 fail-closed 및 이전 승인 재사용 차단이 지속되는지 독립 리뷰에서 확인. GPT의 과거 *별도 오프라인 프로토타입* 시간 역행 결함을 최신 v0.2.4 결함으로 단정하지 않는다.
- 개발 세션에서 추가한 trust_root_tool.py는 공개키 도구로 보이나 **운영 승인자 서명 도구는 미구현**. 실제 유효 REQUEST/READY reviewer 파일럿 실행 전 합법적인 승인·서명 경로를 준비해야 한다.

**S-3: 미정산 F1 무손실 보존**
- `F1=HOLD`는 현재 실행된 DB 상태가 아니라 **전환 시 제안된 처리 방식**. READY 없는 F1을 조용히 드롭하거나 GitHub에서 자동 재큐잉하지 않음. 실제 hold는 원장 영속화·감사 로그·알림 중복 여부 확인 후 사용자 승인 하에 수행.
- F1이 Dropbox에서 계속 WAIT_INPUT으로 남도록 승인하는 선택과, GitHub에서 신규 승인 요청으로 다시 시작하는 선택을 구분하여 처리. F2와 G1–G3는 임의 재실행 금지.

**S-4: 소스 바이트/실독립 리뷰**
- `REVIEW_INPUT_MANIFEST_v0_2_4_FOR_GPT_20261110.md`에 64개 항목별 SHA/size/diff와 질문 9개 존재. **매니페스트만으로 코드 안전 또는 ZIP byte hash 검증을 대신할 수 없음**.
- ZIP은 반출 허용 분류가 명시적으로 확인된 경우에만 PRIVATE에 신규 파일로 게시. GPT는 실소스 독립 정적 검증·비밀 점검·해시 대조를 다시 할 수 있으며, 정식 Claude 독립 리뷰는 유효 REQUEST/READY와 별도 모델 비용 승인 후 1회. 기존 STATIC $1 상한 초과 예상 시 모델 호출 없이 fail-closed, 사용자 승인 없이 비용 증액 금지.

## 4. 현재 남은 승인 게이트 (원샷으로 묶되 실제 운영 변경은 제외)
**1차 통합 승인 묶음(아직 승인되지 않음)**
1. 승인자 기기에서 키를 생성하고 별도 고정 신뢰 루트/정책핀·최소권한 토큰을 호스트에 설치·시험(승인 로그/롤백 포함; 개인키는 저장소·watcher에 게시하지 않음).
2. 보호된 별도 경로에서 호스트 SHADOW 실측(기간 및 중지 조건 합의), **S-1 해결**과 운영 main/WAL/SHM 영향 검증이 선행. Dropbox LIVE/기존 예약 작업 불변.
3. 출처·반출 허용 확인 뒤 v0.2.4 원본 ZIP과 diff를 허용된 저장소에 게시하고 실제 원격 SHA를 재검증.
4. 유효한 서명·정책·예산 한도 아래 별도 **정식 Claude 독립 리뷰 1회** 실행, 결과+영수증 readback 및 GPT 수용/보완.
**2차 명시적 운영 승인 묶음(후속):** 운영 DB 백업·유효 정산/hold 처리·실제 마이그레이션/rollback 검증, GitHub 단일 LIVE 전환, 이전 Dropbox 상태 보존 및 실패 시 복구. PUBLIC 배포는 별도.

## 5. 결론과 다음 한 동작
- **`GPT_DISPOSITION=ACCEPT_WITH_CHANGE / PRE_CUTOVER_PARTIAL`**: v0.2.4 개발·격리 시험은 진전. 운영 배포 승인, SHADOW 실호스트 PASS, 정식 독립 리뷰 PASS, LIVE cutover PASS가 아님.
- 비용·권한·실운영 변경·사외 반출 승인 없이 할 수 있는 추가 작업은 GPT가 문서 정리·설계 분석·기존 소스 접근 범위에서 수행. Claude 개발자 자체 시험을 독립 리뷰로 승격하지 않음.
- 최종 사용자 요청은 여러 번 나누지 않고 **1차 승인 여부를 묶어 판단한 뒤** 허용된 범위의 호스트 SHADOW/공식 독립 리뷰를 원샷 실행, 결과 확인 후 **2차 LIVE cutover 승인**으로 이어간다. GitHub 문서 게시는 실행 트리거가 아니다.
