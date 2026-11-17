# CoWork GPT→GitHub→Windows 자동 서명·독립 리뷰 최소 설계

## 2026-11-17 최신 결정 r0002 — 일·월 누적 상한 제거, 건별 $1.50/$3.00
- **사용자 최신 요구로 이전 2026-11-17 r0001 ($1/일 $3/월 $10)도 대체됨:** [건당 $1.50 스킬·$3 디자인, 일/월 횟수 및 누적 비용 상한 없음](GPT_AUTO_REVIEW_BUDGET_POLICY_r0002_20261117_KST.md). 과거 위임/설치 이력의 당시 값은 보존. 개발 후보 v0.2.25는 PRIVATE만 게시, Windows LIVE 미적용.


- [최신 정본: COST_ONLY 정책](GPT_COST_ONLY_AUTO_APPROVAL_POLICY_r0001_20261117_KST.md).
- 일/월 리뷰 **호출 횟수 상한은 사용하지 않음**. `max_day_calls` 필드는 기존 보호 위임 파일과 API 호환용으로만 받아들이고 정책 허용/원자 예약/상태 화면의 제한으로 사용하지 않는다.
- 기존 **요청당 1회·중복/UNCERTAIN 자동 재시도 금지**, 프로젝트/스킬/서명/SOURCE_PIN, **USD 1/요청·USD 3/KST 일·USD 10/KST 월 비용 상한**은 유지한다.
- 아래 2026-11-15 설계의 `하루 2회` 표기는 작성 당시 기준 이력이며 **신규 정책으로 적용 금지**. Windows 운영 LIVE에서는 새 ZIP의 독립 리뷰/호스트 시험/승인·설치 완료 전까지 과거 설정이 실제로 적용될 수 있으므로 문서 변경을 호스트 전환이라고 보고하지 않는다.

---

- 버전: r0001 / 2026-11-15 KST
- 저장소/브랜치: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 정확한 상대 경로: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/AUTOMATIC_SIGNING_MINIMAL_DESIGN_r0001_20261115.md`
- Work ID: `COWORK-AUTO-APPROVAL-20261115-001`
- 상태: `DESIGN_CANDIDATE / NOT_OPERATIONAL`
- 근거: [GitHub LIVE 이관 최신 CURRENT](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md), 기존 운영 Watcher v0.2.20, 기존 Windows Ed25519 signer/approval verifier/READY/원격 중복 예약, [단일 사용자 간소화 기준](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_COWORK_SINGLE_USER_SIMPLIFIED_COLLAB_RULES_r0001_20261114.md)
- 이전 Telegram 버튼 설계 [GPT_APPROVAL_BRIDGE_MINIMAL_DESIGN_r0001](../COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_APPROVAL_BRIDGE_MINIMAL_DESIGN_r0001_20261115.md)는 작성 당시 대안으로 보존하되 **이번 자동 승인 기본 구현안으로 채택하지 않음**. 운영 변경은 중단 상태 유지.

## 1. 목적 및 정확한 신뢰 경계

사용자는 CoWork 개인 운영자이며 기본 목표는 **사용자 요청 → GPT의 PRIVATE REQUEST 게시 → Windows 자동 승인 처리 → 기존 LIVE watcher 독립 리뷰 1회 → GPT 결과 판정**이다. 정상 동작 시 Telegram 추가 확인·Windows Claude Code 수동 조작·승인 반복이 0회여야 한다.

**중요:** `GitHub에 REQUEST가 있다`는 사실은 사용자 명시 승인에 대한 암호학적 증명이 아니다. 이번에 확인된 REQUEST는 사용자의 지시로 생성됐지만, GitHub 계정/PAT, CI, GPT의 오인·중복 생성 또는 자격 유출로 다른 REQUEST 파일을 작성할 기술적 가능성은 남아 있다. 반면 실제 무단 REQUEST가 발생했다고 확인된 증거는 없다. 이 위험을 이유로 정상 요청마다 추가 승인 버튼을 요구하지 않고, **사용자가 Windows에 1회 등록한 제한적·영속적 위임 정책**으로 조건에 맞는 GPT/GitHub 요청에 한해서 자동 서명을 허용한다. 이 선택은 'GPT/GitHub 쓰기 주체를 위임 한도 안에서 신뢰'하는 **명시적 위험 수용**이며 GitHub commit 작성자 문자열을 사용자 인증 근거로 꾸미지 않는다.

최초 위임 설정의 실제 사용자 승인과 Windows 보호된 로컬 정책 적용은 별도 1회 게이트. **이번 설계 작성·기존 특정 리뷰 $1 승인을 미래 모든 REQUEST의 자동 실행 권한으로 확대하지 않는다.** 위임은 비밀/키를 GitHub에 게시하는 방식이 아니다.

## 2. 목표 처리 파이프라인 (기존 서비스 재사용)

```text
사용자 → GPT: 개발·독립 리뷰 요청
   ↓
GPT: 범위/후보 ZIP/REQUEST/비용등급을 PRIVATE main에 게시, Commit A·원시 SHA/크기 검증
   ↓
기존 Windows GitHub LIVE Watcher (단일 Task/30초 loop)
   ├── REQUEST-only 후보 스캔 단계 추가 (현재 READY-only 실행 감시와 별개)
   ├── 로컬 전용 AUTO_DELEGATION_V1 정책 확인 (기본 disabled)
   ├── repo ID/commit A/SOURCE_PIN/REQUEST·ZIP hash/CRC/도메인·mode 확인
   ├── 기존 SQLite 처리 원장+새 승인 예약 상태로 중복/예산 원자 선점
   └── 기존 Windows signer: 정확한 READY 원문 미리 구성, ready_sha256에 묶어 서명
           ├── APPROVAL_SIG.json 생성 전용 원격 게시 + 검증 readback
           └── READY.md 생성 전용 **마지막** 게시 + 검증 readback
   ↓
같은 기존 LIVE Watcher의 변경 없는 READY 검증/N1 원격 예약/Claude 독립 리뷰 1회
   ↓
REVIEW_RESULT + RECEIPT + USAGE_RECEIPT → 기존 notifier/Telegram 완료 통지 → GPT 판정
```

- 새로운 Telegram 승인 버튼·봇 update 소비자·새 watcher Task·새 reviewer 프로세스는 **기본 구현에 추가하지 않음**.
- 1순위는 기존 운영 **동일 watcher 루프**에 pre-READY 단계 최소 추가. 단, Windows 실행 계정이 보호된 signer에 실제 접근 가능한지 확인해야 한다. 접근 불가하면 **키 ACL 완화/키 복제 없이**, 이미 승인된 동일 호스트의 별도 인증 가능한 signer 호출 경로가 실제로 있는 경우만 재사용하고 불가하면 `BLOCKED_SIGNER_BOUNDARY`로 후보 보고. 별도 신규 백그라운드 서비스 기본 추가 금지.
- 기존 `APPROVAL_SIG` 검증/Ed25519·SOURCE_PIN·정책/비용/만료·중복 실행·`REVIEW_UNCERTAIN`/publish-only 기능 제거·완화 금지.
- 실제 v0.2.20 `APPROVAL_SIG.json`의 signed payload에는 `ready_sha256`가 있으므로 **READY 본문은 서명 전에 바이트 단위로 확정하되, GitHub 게시만 마지막**에 한다. 서명/READY 파일 형식을 추측하여 재구현하지 말고 기존 검증기/CLI/코드의 정확한 생성·검증 함수를 재사용.
- Commit A의 REQUEST·ZIP·SOURCE_PIN은 보존. 브랜치 head가 변경되어도 pin된 바이트를 확인하고 요청에 묶이지 않은 latest 파일로 대체하지 않음.
- GitHub 문서 작성만으로 Windows Claude Code 또는 모델 리뷰가 직접 실행되지는 않음; 이 기능은 **Windows 실행 코드가 설치된 이후에만** 동작.

## 3. 로컬 위임 정책 초안 (민감값 미포함, 현재 승인 전 DISABLED)

정책은 Windows 관리자 전용 보호 위치에만 저장하고 버전/서명 또는 변경 감사 기록을 유지. 외부 GitHub는 정책의 유효성·내용·비용 한도를 변경할 수 없어야 한다. 다음 값은 **사용자 1회 확정을 위한 추천 범위**이며 실제 승인값 아님.

| 설정 | 추천 초기값 | 설명 |
|---|---|---|
| `enabled` | `false` | 첫 설치/격리 시험은 반드시 OFF |
| `repo_id` | `1451933830` (실서버 재조회) | PRIVATE CoWork 이외 거부 |
| `branch` | `main` | pin된 Commit A 필수 |
| `allowed_projects/skills` | **명시적 허용 목록만** | 빈 목록은 실행 금지, 작업별 범위는 한 번에 확정 |
| `allowed_policy` | `POLICY-STATIC-V1` | LARGE/XLARGE 자동 승인 금지 |
| `max_cost_per_request` | `USD 1.00` | 1 요청/1회 |
| `max_calls_per_request` | `1` | 재리뷰는 새로운 위임 없이 자동 시작 금지 |
| `daily_limit` | **USD 3.00 (횟수 상한 없음)** | 일일 비용만 KST 기준으로 제한; 과거 2회 상한 폐기 |
| `monthly_limit` | **제안 $10.00** | 추가 누적 상한(사용자 확정 전 OFF) |
| `delegation_expiry` | **제안 30일** | 만료 시 자동 서명 차단. 갱신은 명시적 사용자 결정 |
| `revocation` | 보호된 로컬 `enabled=false` 즉시 | 서명 단계 이후 호출 중인 리뷰는 기존 영수증·중복 계약 적용 |

AUTO 요청에서 PROJECT/skill/ZIP 타입뿐 아니라 데이터 분류와 파일 크기를 검사한다. 업무 제한 자료/고객 로그/토큰·개인키는 PRIVATE에도 업로드 금지. 운영 설치·PUBLIC 배포·LIVE provider 전환/원장 이행·지식 정본 게시 권한은 **리뷰 자동 승인과 무관**하고 자동 허용하지 않는다.

## 4. fail-closed / 비용 상한 / 중복

1. pre-READY 요청 스캔에서 `APPROVAL_SIG/READY/REVIEW_RESULT/DISPATCH/RECEIPT` 또는 기존 provider 이력이 이미 존재하거나 모호하면 기존 완료/소진/불확실 상태를 조사해 **재서명·모델 호출 0**(publish-only 정산만 허용). 이전 `REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001` 등의 기존 승인/미정산 요청은 자동 위임 도입 시 retroactive auto-enqueue 금지. 기본 **기능 활성화 시점 이후의 새 요청에만** 적용; 과거 REQUEST는 명시된 1회 마이그레이션/처리 승인 없으면 대상 제외.
2. 새 signer 호출 전 **로컬 영속적 원자 예약** `(repo_id,request_id,revision,package_sha256,logical_attempt)` 및 예산 예약을 동일 transaction으로 확정. 이미 유사 잠금이 있으면 확장 없이 재사용. crash 후 원장 분실·복원 불확실이면 signing 자동 재개 금지.
3. 요청 identity/ZIP/SOURCE_PIN/commit/정책/최신 repo ID/서명 만료/허용 scope·일·월 총액을 **서명 직전과 READY 직전**에 확인. Github 문서 안의 `cost` 또는 `user_approved: true` 필드는 승인 근거 아님.
4. `APPROVAL_SIG` PUT 전 실패/409/timeout: 원격 상태 readback, 정확한 같은 payload면 정산. 승인 키로 재서명할 필요/요청이 불확실하면 자동 재시도 없이 `SIGNING_UNCERTAIN`. 임의 새 서명 생성 금지.
5. `APPROVAL_SIG` 게시 후 READY 전 실패: 서명 payload와 준비된 READY bytes, existing signature 검증 통과 시 **기존 READY만** 게시 가능. HEAD race/원격 충돌 시 종료·보고, 영수증 확보 전 재호출 금지.
6. READY 게시 후 Windows 중단/비용 한도 문제: **기존 Watcher N1 예약/REVIEW_UNCERTAIN**를 그대로 사용하여 모델 리뷰 1회만 실행. 첫 요청을 처리한 뒤 Telegram 알림 실패는 모델 재호출 사유가 아님.
7. 매일/매월 사용량은 실제 청구+이미 예약된 최대 비용으로 보수적으로 계산. UTC/KST 경계 기준 한 가지를 고정하고 재시작/복구 후에도 정합성을 보장(추천 KST). 총액 상한은 **로컬 위임+기존 watcher 중 더 엄격한 비용 제한**을 적용. 일/월 호출 횟수 상한은 두지 않는다.
8. 신규 정책 변경·권한 확대, 위임 부재·만료·변조, allowlist 밖 요청, 모델 변경/프로파일 상승, 한도 초과는 `WAIT_USER_SCOPE` 또는 `BLOCKED`; Telegram 추가 승인 버튼을 자동으로 만들지 않음. 필요할 때 사용자에게 **한 번의 범위 확정**만 요청.

## 5. 구현 범위, 테스트, LIVE 게이트

**최소 예상 변경(실제 코드 확인 후 확정):** `orchestrator.py` pre-READY discovery, 기존 `approval` signer/validator 호출 연결, 설정의 local delegation reader/validator, 기존 DB의 승인 예약 및 비용 원장, config-check/dry-run 진단, 관련 시험·런북. `github_transport.py`는 매 요청 repository_id 재조회와 create-only/readback 보장 등 기존 함수 재사용; 대규모 리팩터링 금지. 실제 파일명/함수는 Windows 소스 확인 후 명시할 것.

필수 합성/회귀:
- 기본 `enabled=false`: REQUEST 신규/변조/READY 없음 전부 signer 0·model 0.
- 허용 scope+유효 바이트+예산: 승인 1, `APPROVAL_SIG`/READY create-only 순서, 현재 verifier PASS, 모델 1회.
- 두 작업 동시, 재시작, 같은 요청 2회 scan/2개 task 경쟁, 원장 복구, 409/422, timeout, 서명 후 READY 전 crash, READY 후 receipt 업로드 실패에서도 `model_calls<=1`.
- 요청/ZIP/Commit A/repo ID 변조, 해시/CRC·정책/모드·신뢰 루트 실패, expired delegation, allowlist 밖, 모델 limit/day/month 경계, 기존 과거 REQUEST retro-trigger 모두 signer/model 0.
- 실제 GitHub LIVE watcher 사용 중 원본 Task/DB main·WAL·SHM/Notifier/Dropbox Disabled·운영 키 불변. `SHADOW` 단계는 **원격 쓰기·Telegram 발송·실서명·유료 리뷰 전부 0** (fake signer/transport).
- 승인 후 시험/패키지: 목표 Python 3.11 Windows 운영 호환, 기존 회귀 전체 + 추가 상위/실서명·READY 형식, ZIP 신규 버전/actual SHA-256, CRC/path traversal/symlink/secrets, isolated rollback, 독립 리뷰/영수증 별도 상태. 기존 승인 v0.2.20 ZIP/Task 덮어쓰기 금지.

**배포 게이트:** `DEVELOPMENT=PASS`, `SELF_TEST=PASS`, `INDEPENDENT_REVIEW=PASS`(미수행이면 `NOT_RUN`), `PACKAGE_VERIFIED=PASS`, `WINDOWS_SHADOW=PASS`, `ROLLBACK=PASS`, `OWNER_DELEGATION_SCOPE_APPROVED=YES`, `HOST_INSTALL_EXPLICITLY_APPROVED=YES` 이후만 auto signing LIVE enable. 현재 요청은 **설계·격리 개발 승인**으로 처리, 추가 유료 리뷰·키/운영 DB·Task 실제 변경 및 자동 서명 LIVE 전환 승인은 별도.

## 6. 역할, 원샷 운영, 산출물

- **GPT 지금:** 설계·정적 계약 판정, 테스트 가능한 순수 policy gate 작성/합성시험, PRIVATE 문서·개발 코드 게시/readback. 실제 Windows 운영 signer/Task/DB·유료 Claude 호출 권한 없음.
- **Windows Claude Code 1회 실행:** 정확한 `WINDOWS_ONE_SHOT_DEVELOP_TEST_CANDIDATE_HANDOFF_r0001_20261115.md`에 따라 최신 설치 source/설정과 diff 확인 → 격리 최소 수정 → 반례/기존 회귀 → SHADOW + 롤백 리허설 → 후보 ZIP/SHA/CRC → PRIVATE 결과/readback까지 중간 질문 없이 처리. 접근/비밀/추가 유료 승인 차단 항목만 `BLOCKED` 기록하며 나머지 무비용 단계 계속.
- **GPT 결과 수신 후:** 항목별 판단 및 필요 결함 수정 묶음, 운영 후보/승인 스코프·배포 게이트 한번에 판정. **독립 리뷰는 개발자 자기시험과 분리**; 비용 승인 없으면 `PENDING`으로 기록. 운영 적용 승인 시 Windows Claude Code 별도 최종 적용/rollback/실운영 시험을 실행.
- **운영 전환 판단:** 기존 GitHub LIVE는 계속 **LIVE**; 바뀌는 것은 `AUTO_SIGNING=DISABLED → ENABLED`이며 기존 provider 변경이 아님. 별도 Dropbox LIVE 재가동/새 LIVE provider 시작 금지.

**다음 한 동작:** Windows Claude Code에서 정확한 PRIVATE/main/handoff를 **한 번** 실행해 개발·시험·후보 보고까지 완료. 새 구조는 승인된 재사용 기본값을 초과하는 scope/cost와 실운영 변경이 필요한 마지막 단계에서만 사용자 판단 요청.
