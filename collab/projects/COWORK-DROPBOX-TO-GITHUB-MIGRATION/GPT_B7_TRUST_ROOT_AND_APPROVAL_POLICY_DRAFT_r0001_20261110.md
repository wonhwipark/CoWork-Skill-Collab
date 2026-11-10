# CoWork GitHub watcher — B-7 운영 신뢰 루트·서명 승인 정책 초안
작성 2026-11-10 KST | GPT 단독 설계 | STATUS=DESIGN_READY_NOT_OPERATIONALLY_APPROVED | CURRENT_LIVE=DROPBOX

## 1. 범위/판정
- 목적: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`에 쓰기 권한이 있거나 READY를 위조해도 **별도의 승인 서명 없이는 유료 Claude reviewer를 호출할 수 없게 하는 것**.
- 기존 v0.2.3(Windows Claude 자기시험) 보고: 시험용 Ed25519 backend S01~S10 실제 검증 PASS, 실 운영 신뢰 루트/키 배치·호스트 독립 리뷰는 NOT_RUN. 후보 ZIP이 GPT에 없으므로 아래는 **아키텍처/정책 제안**이며 운영 코드 구현 검증이 아니다.
- 인계 지침은 설계 승인과 운영 활성화를 분리. 이 문서의 GitHub 게시 자체는 REQUEST/READY가 아니며 모델 호출 0, LIVE 변경 0.

## 2. 보안 경계
| 주체 | 권한/자료 | 금지 |
|---|---|---|
| GPT·일반 협업 작성자 | GitHub PRIVATE 문서/REQUEST/후보 생성 | 승인 개인키 접근, READY 존재만으로 리뷰 호출 |
| 별도 승인권자/서명 프로세스 | 조직/사용자가 통제하는 **Ed25519 개인 서명키** | 개인키의 GitHub/Dropbox/프롬프트/로그/ZIP 게시 |
| Windows 검증 watcher | PRIVATE 읽기 + 별도 최소 쓰기 경로, **외부 고정 공개키 allowlist** | 승인키 교체를 GitHub 파일로 신뢰, 서명 전 모델 호출 |
| Claude reviewer | 서명·정책 확인된 승인 1회 | 개발자의 자체 시험을 독립 리뷰로 표시 |
| PUBLIC 배포자 | 최종 승인 ZIP 전용 | PRIVATE 리뷰/영수증/개인키 공개, 미승인 ZIP 배포 |

공격 가정: GitHub main이 브랜치 보호되지 않아 원격 콘텐츠/READY 변조 가능. GitHub commit author·write permission·repository metadata는 충분한 승인 근거 아님. 개인 서명키 또는 Windows 호스트 침해는 본 계약만으로 방어하지 못함.

## 3. 운영 trust root 데이터·위치
1. 신뢰 루트는 **GitHub/Dropbox 밖**, 권한 보호된 Windows 운영 파일/OS 저장소에 둔다. 사용자·운영 절차가 설치 승인. watcher process에는 공개 검증 자료 읽기 권한만. private key는 다른 보안 경계에서 보관하고 watcher 호스트에 저장하지 않는다.
2. 최초 설정에 숫자 `repo_id`, 정확한 `repo_full_name`, `branch=main`, 허용 signer `key_id → Ed25519 public key + SHA-256 fingerprint`, 각 키의 `not_before/expires/revoked`, policy hash/version, 최대 비용, 허용 host 및 `epoch`를 고정한다. **키/정책의 원격 저장소 수정으로 변경되지 않음**.
3. 운영 루트 부재·포맷 불명·repo ID 충돌·키 미등록/폐기·fingerprint 불일치·시계 동기성 실패는 **FAIL_CLOSED, 모델 호출 0**. 이전 신뢰 루트를 임의 원격 자동 갱신 금지.
4. 신규 키 발급은 별도 명시 승인으로만 수행. 정기 회전 시 새 공개키를 승인된 로컬 루트에 먼저 배치한 뒤 서명자에 새 키를 적용하고, 구 키로 발행한 **미정산 요청**을 보존·정산한 다음 폐기한다. 키 유출은 즉시 폐기 및 REVIEW_UNCERTAIN 봉인. 폐기 키는 과거 성공 이력만 보존하고 새 호출 권한 없음.
5. 루트 및 revocation 변경은 별도 운영 변경 영수증(누가, 어떤 fingerprint, 언제, rollback)을 남기되 개인키/원본 비밀은 게시 금지. 백업/복구와 동시 키 회전 중 다중 LIVE provider 금지.
6. 유효 시계: UTC epoch seconds, 최대 시간 편차는 기존 후보 테스트와 부합하도록 **300초 잠정안**. 만료는 현재 시간 기준 엄격하게 차단하고 미래 발행, 시계 역행, last trusted time 불명/과도한 NTP 오차를 별도 차단. 이전 관측 시간/서버 시간 검증의 신뢰성은 Windows SHADOW/운영 승인 때 확인.

## 4. 서명 대상과 PR 없는 READY 마지막 게시
A. `Commit A`에서 원본 REQUEST V1, ZIP, 실행 모드/지식 참조/정책 스냅샷을 게시 → **원격 raw bytes** SHA-256·크기·CRC 및 40자리 원본 commit ID를 직접 readback. Git blob SHA1/Dropbox content_hash를 SHA256으로 혼동하지 않음.
B. 서명자는 변경 불가능한 canonical payload에 `repo numeric ID/full name`, `source_commit_A`, `request_id/revision`, `request_raw_sha256`, `zip_raw_sha256/size/path`, `mode/policy hash/version`, `knowledge refs digest`, `max_cost`, `reviewer host`, `not_before/expires`, `nonce`, `schema_version`, `READY payload digest`(계약에 포함 시 정규화 규칙)을 정확히 결합해 별도 개인키로 Ed25519 서명.
C. 서명 대상은 **Commit B의 SHA 또는 자기 자신을 포함하지 않는다.** READY marker와 승인 sidecar를 분리하는 경우: `SOURCE_PIN.json`, `APPROVAL_SIG.json`을 먼저 게시하고 **`READY.md`를 마지막에** 작성하거나 Git Trees API로 하나의 atomic commit을 수행. GitHub Contents API 개별 호출은 원자적 다중 파일 commit이 아니므로 '한 커밋으로 원자적'이라고 주장하지 않는다.
D. `READY.md` 관측은 발견 후보일 뿐. watcher는 repo ID·branch·소스 commit A 고정 원본·서명·nonce/만료·정책·ZIP/REQUEST·예산·로컬 allowlist·LogicalRequestId·실행 횟수 모두 통과해야만 리뷰 1회 요청.
E. canonical JSON은 **현재 Windows v0.2.3 실제 verifier와 golden byte fixtures로 계약을 확정해야 한다.** UTF-8·중복 키 거부·비정규/부동소수·BOM/CRLF·field order·서명 필드 자체 참조를 시험. 기존 REQUEST는 V1 YAML/frontmatter이며 GPT의 구형 offline gate(JSON 전용)와 다르므로 과거 gate 코드를 그대로 운영에 끼워 넣지 않는다.
F. 서명 본문에 권한·가격·실행 모드·policy SHA·고정 커밋이 누락되면 fail-closed. GitHub에서 서명과 payload를 동시에 바꿔도 운영 공개키와 일치하지 않으면 호출 0.

## 5. 중복 실행·상태·알림
- `logical_request_id`는 `request_id + revision + package_sha256`에 기반하고, Dropbox/GitHub provider와 local policy revision 변경만으로 신규 승인으로 간주하지 않는다. 같은 ID+revision/다른 ZIP은 CONFLICT.
- 승인 nonce는 일회용·durable 처리. SQLite 원자 예약 직후 crash 시 `REVIEW_UNCERTAIN`, 자동 재호출 0. 게시 실패 시 기존 RESULT/RECEIPT **재게시만**, reviewer 재실행 금지.
- READY 무효/키 폐기/기존 완료/비용 초과/SHADOW/두 provider LIVE 요청 → 모델 0. notifier는 provider+epoch durable watermark와 기존 last_id에 맞춰 중복/누락 0 설계.
- GitHub 전환 전에 Dropbox pending 요청 보존 또는 개별 정산, 단일 ACTIVE_PROVIDER + rollback cursor 일치, 운영 DB WAL 안전 백업·마이그레이션 실측이 필수.

## 6. B-7 시험·승인 게이트
| 확인 | 합성시험 목표 | 운영 실측 상태 |
|---|---|---|
| 유효 TEST 키 S01~S10 | 테스트용 Ed25519 서명 실제 검증, 0 무단 호출 | Windows Claude 보고 PASS(TEST_KEY) |
| 미등록·폐기·다른 repo 키 | fail-closed / 모델 0 | Windows 운영 루트 NOT_RUN |
| clock rollback/미동기화 | fail-closed, replay 불허 | 운영 호스트 NOT_RUN |
| 교차 provider replay/동일 logical key | 원장 재호출 0 | 운영 호스트 NOT_RUN |
| READY 선공개·부분 sidecar | 전체 원본/승인 전 모델 0 | 합성 범위 보고, 실제 운영 NOT_RUN |
| root rotation/revocation & restart | 승인된 변경만, 과거 요청 보존 | 운영 신뢰키 미승인 |
| 사용자 승인+서명자 권한 분리 | 비밀 외부 노출 없이 운영 설치 증명 | NOT_APPROVED |
| 비용정책+유효 REQUEST/READY | 정책 상한/nonce/receipt 검증 | 실제 유료 독립 리뷰 NOT_RUN |

## 7. GPT 판정 및 남은 한 승인 묶음
- **B-7 설계: READY_FOR_INDEPENDENT_REVIEW**, NOT_READY_FOR_INSTALL. 키·토큰 생성/운영 venv/Windows trust root 설치/모델 유료 호출은 미승인.
- Claude Code를 사용할 수 없을 동안 GPT가 정책·재현 가능한 합성 보안검증·문서화를 계속할 수 있지만, 개발 Claude 자체 시험을 정식 독립 리뷰 PASS로 승격할 수 없음.
- 사용자가 향후 함께 검토할 승인 묶음: 운영 키 및 승인 주체 확정, 최소 권한 GitHub 인증, pending 1건 무손실 정산, 운영 호스트 SHADOW, 정식 Claude 독립 리뷰/영수증, 운영 DB 이행/롤백, 실제 단일 LIVE cutover.
