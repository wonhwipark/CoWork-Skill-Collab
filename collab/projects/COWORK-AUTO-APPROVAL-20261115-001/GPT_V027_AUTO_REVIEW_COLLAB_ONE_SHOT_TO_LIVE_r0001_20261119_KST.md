# CoWork 자동 리뷰 정상화 — Windows Claude Code 1회 실행 통합 인계 r0001
- 날짜: 2026-11-19 KST
- **정본**: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch **`main`**
- **기존 Work**: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- 같은 목적의 기존 문서 `GPT_V027_INDEPENDENT_REVIEW_GATE_AND_HANDOFF_r0001_20261119_KST.md`에 있던 **“사전검증만 하고 멈춤”을 이 문서로 대체**. 새 Work, REVIEW 원장, 사용자 중간 확인 턴, 임의 유료 재리뷰를 만들지 않는다.
- **사용자 최신 지시**: “한번에 진행하자. 너업무방식이 지치게 만들어”. GPT가 설명한 남은 네 단계(정식 독립 리뷰→판정/필요한 보완→Windows 운영 설치/보호 위임 $3→자동 리뷰 E2E)를 한 번의 Windows 실행에 조건부로 묶어 처리하라는 실행 지시. 일반/설계 공통 최대 USD 3/리뷰·일/월 상한 없음은 이전에 승인됨. 단 **GitHub 문서·채팅 내용만으로 보호된 로컬 signer/Ed25519/ACL 권한이 생기지는 않음**. 유효한 기존 로컬 승인 자격과 설정 변경 권한을 실제 검증한다.
- **강제 비용 제한**: 이번 실행에서 새로운 **유료 독립 리뷰 1건, 1회, 최대 USD 3.00**을 넘지 않음. 수정 후 2차 유료 리뷰·유료 smoke·subagent 자동 호출 금지. 실 비용이 추정 cap을 넘어갈 수 있다는 점은 영수증에 명시.
- **기존 LIVE**: Windows watcher v0.2.25 / `POLICY-STATIC-V1=$1.50`, `-LARGE=$3`, `-DESIGN=$3`, 보호 위임 `max_request_usd=$1.00`. 새 watcher v0.2.27 후보는 아직 미설치. 활성 provider는 GitHub 한 개뿐. 기존 notifier/Telegram을 재설치·중복 실행하지 않는다.

## 0. 실행 방식: 중간 응답 대기 없이 이어서
- 새 창이라면 `collab/CONTEXT_BRIEF.md`, 이 Work의 `CURRENT.md` **상단 최신 1개 요약**, 현재 host 실제 config/코드, `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, 이 문서를 조회. 이전 결과와 최신 정본을 대조. 이미 결과/REQUEST/영수증이 있으면 **중복 생성하지 않고 해당 단계에서 재개**.
- 아래 1~6은 **단일 사용자 실행 지시**. 가능한 단계는 자동으로 연속 진행한다. 승인/접근/보안 blocker면 그 단계만 `BLOCKED`, 다른 **무비용·비변경** 작업은 계속해 결과를 한 번에 게시. 질문을 연쇄적으로 되묻지 말고 사전에 승인된 범위·보호된 호스트 자격을 먼저 검증.
- 개발 Windows Claude Code 세션의 자체시험과 별도 watcher 프로세스가 수행하는 **독립 Claude 리뷰는 구분**. 개발 중 사용자 대화형 코멘트를 독립 리뷰 PASS로 사용하지 않음. 리뷰가 막히면 `REVIEW=BLOCKED/PENDING`, LIVE를 임의 승격하지 않음.

## 1. 리뷰 대상 최종 고정·21 실패 정리
- 출발점: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_27/skill-collab-watcher_v0_2_27_1119_DEV_NOT_FOR_DEPLOYMENT.zip` (309187 B, SHA-256 `baf5a856fbe1e34d0c3b235a5ccd5a7895ad342a18cf448360b53773ac8669e0`), `CANDIDATE_MANIFEST.json`, `diff_v0_2_26_to_v0_2_27.patch`. 실제 remote bytes/SHA/CRC/paths 재확인. 독립 리뷰·운영 설치 0인 상태에서 이전 후보 직접 덮어쓰기 금지.
- Windows 전체회귀 `1010 passed / 21 failed / 12 skipped` 중 6개는 **과거 일/월 제한 기대**, 15개는 **Windows CRLF fixture**라는 보고를 실제 실패 ID와 스택으로 대조. 기존 회귀 의도를 보존하며 test fixture/구식 assertion만 최소 갱신. `collab/ops/tests/test_review_request_gate.py`의 이미 원격 검증된 LF-bytes 수정 재사용. 코드가 실제 잘못된 경우 FAIL로 처리, 테스트를 삭제·skip하여 녹색으로 만들지 않음. 수정으로 후보 bytes가 바뀐다면 **새 패치 버전(v0.2.28 또는 최신 충돌 없는 버전)으로 재패키징**, 최종 정식 ZIP 명명 `skill-collab-watcher_v0_2_28_1119.zip` (실제 버전에 따라 조정); **기존 ZIP 보존**, 최종 package/manifest/diff SHA·크기·CRC·113개 항목/변경분 검증.
- 독립 reviewer가 볼 대상 **정확한 최종 ZIP 바이트**를 이 단계에서 확정. 이후 README·코드·테스트 등 패키지 내용 **단 한 바이트라도 변경되면 해당 리뷰 PASS로 설치 불가**. 승인 입력 컨텍스트는 실제 리뷰 스냅샷에 포함되는 ZIP/FILE_INDEX와 pin된 diff·manifest 링크로 제한. v0.2.25 LARGE R2의 M1(외부 preflight 스크립트 리뷰 입력 누락) 재발 방지.
- 합성 검증: 과거 `REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117`의 실제 ID, rev1, 정책 DESIGN, SHA `26d63c8a03290499b13b2ceb8ff0b70c06eb1b1bcc1a25fe3d8f65fcc213d228`에서 **가상 $3 위임에도 signer/READY/모델 0**; 옛 LARGE R2 완료/Guard UNCERTAIN/활성 전 대기 3건 중복 0; 신규 STATIC/$3 합성 allow; old STATIC 요청 새 금액 소급 실행 0; pin 타입/READY WAIT/만료/범위/중복/송신 불확실 반례. Windows 전체 회귀와 isolated E2E 재실행·개별 PASS/FAIL/SKIP 보고. 배포 게이트는 **미해결 실제 동작 실패 0**이 원칙.

## 2. 정식 유료 독립 리뷰 **1회** — 기존 호스트로 부트스트랩
- **신규 default는 STATIC/USD3**이지만 현재 LIVE STATIC=$1.5/위임=$1이라 바로 신규 통합 자동 리뷰 REQUEST를 게시하면 안 됨. watcher **v0.2.25에 실제 설치된 $3 `POLICY-STATIC-V1-DESIGN` 또는 `-LARGE`**를 *이번 부트스트랩 리뷰 1건의 공식 수동 승인 transport 예외*로만 고려한다. 사용자 승인 $3 한 건과 **로컬 승인자의 실제 유효 보호 자격**을 분리해 확인. 임의 서명/정책 증액/위임 $3 선적용 금지.
- `collab/ops/review_request_gate.py select/check`를 **실제 설치된 local reviewer.config.json + 최종 ZIP 바이트 + 신규 REQUEST 초안**으로 먼저 실행. `select --intent design`가 선택한 등록 ref와 REQUEST ref를 정확히 맞춘다(DESIGN 등록이면 통상 DESIGN 우선). `POLICY_COMPATIBLE_NOT_APPROVED`와 `PASS_PREPUBLICATION_ONLY`는 권한 승인 아님. 기존 `approve_request.py check`와 실제 유효 수동 서명/금액 권한 확인 전에는 게시·READY 금지. $3 수동 경로 불가면 `REVIEW=BLOCKED`로 남기고 3~5의 운영 변경은 하지 말 것.
- 가능하다면 **기존 ID와 구별되는 신규 1개 REQUEST**로 Commit A: 최종 ZIP을 정확히 PRIVATE `collab/packages/`에 새 이름/원본 bytes로 게시하고 `collab/requests/<new-id>/REQUEST.md` 고정; remote bytes/SHA/ZIP size/FILE_INDEX를 읽어 확인하고 해당 원격 commit A로 `SOURCE_PIN.json`(repo_id JSON **string** `"1451933830"`) 생성/검증. 임의 파일 수정/새 정책명/리뷰 중 ZIP 변경 금지.
- 실제 공식 수동 승인 절차의 유효 서명으로 `APPROVAL_SIG.json` 생성, `READY.md` **마지막** 게시. 기존 watcher가 이 **한 ID**만 자동 dispatch해 별도의 **독립 Claude reviewer** 1회 사용(상한 $3, 하위 Agent/재호출 금지). 결과 `REVIEW_RESULT_1.md`, `RECEIPT_1.md`·processing_key/사용량/실제 비용·중복 0 확인. watcher가 갑자기 멈추거나 결과 게시 실패/불확실한 호출이 발생하면 **모델 재호출하지 말고** 복구 가능한 publish-only 정산 또는 UNCERTAIN 보존. **기존 DESIGN R1/완료 LARGE R2는 재서명·재실행 0**.
- v0.2.27을 자체 검토한 개발 세션의 진술만으로 독립 리뷰 완료 표시 금지. 독립 결과 실파일과 실제 receipt가 있어야 `INDEPENDENT_REVIEW=PASS/FAIL` 판정 가능.
- 리뷰가 주요 수정·새 빌드를 요구하면 동일 Work의 허용된 개발/시험은 계속하고 **리뷰 대상과 변경된 ZIP의 SHA 불일치 시 설치 STOP**. 두 번째 유료 리뷰를 자동 생성하지 않음.

## 3. 독립 리뷰 판정·최종 릴리스 게이트
- GPT의 기존 **사전 조건부 실행 판정**: REVIEW_RESULT 실제 완료 + 인증된 고정 입력/영수증 일치 + **BLOCKING=0, MAJOR=0 또는 해결되어 동일 입력 재검증 가능**, 부분 검토·미확인 위험 없음 + Windows release full suite에 **미해결 실제 동작 실패 0**, 전체 E2E/소급/중복/SHADOW/롤백 준비 PASS + **리뷰 ZIP=설치할 ZIP 바이트 SHA 동일**일 때만 다음 호스트 단계를 기술적으로 진행. 비차단 MINOR는 기록하고 배포 차단 여부를 명시. 다르게 해석하지 말 것.
- **이 조건부 객관 게이트는 미래 REVIEW_RESULT에 대한 GPT의 실제 최종 판정이 아님.** Windows는 위 PASS를 근거로 기술적 `RELEASE_GATE=PASS_CONDITIONAL`만 기록. GPT 최종 결과 판정/정본 정리는 결과 게시 후 직접 확인해야 하며, 다른 입력/새 위험/주요 결함을 자동 승인으로 간주하지 않는다.
- 실제 고정 ZIP을 `development_not_for_deployment`에서 승인된 배포 후보로 분류하는 것은 **별도 리뷰·시험 결과를 확인한 경우만** 가능. 사용자 이번 '한번에' 실행 지시의 **기존 범위** 안에서 조건부 설치 수행 가능성은 호스트의 유효 실제 설치/설정 승인 자격과 이 Work의 현재 배포 게이트에 따름. 근거가 없으면 `HOST_DEPLOY=BLOCKED_AUTHORIZATION`, 나머지 결과 게시까지 계속.

## 4. Windows LIVE v0.2.25 → 최종 승인 ZIP 조건부 설치 / USD3 보호 위임
- 위 2~3 완전 PASS와 **실제 유효 보호된 설치/서명 권한**이 있을 때만 Windows watcher/Task/DB main·WAL·SHM/설정/키 상태를 백업, SHA/ACL/rollback 보존; 단일 provider lease·Task 1개 확인 후 **정지→원자적 설치→SHADOW→재시작**. 원본과 DB 이력 손실 금지. 기존 v0.2.25 롤백 가능하게 보존. 새 watcher/Notifier 두 개 동시 LIVE 금지.
- **필수 순서**: 설치된 새 STATIC-only 정책 경로가 정상 작동하는지(특히 옛 DESIGN R1) **USD3 위임 상향 전에** 합성 + 실제 DB/원격 읽기 전용 재평가. 모든 미해결·기완료·UNCERTAIN 요청, old STATIC policy 요청을 새 금액 가정으로 재점검. 과거 요구 승인 상태만으로 재실행을 유발하지 않는지 증명.
- Windows의 유효한 보호된 갱신/서명 도구를 사용해 **동일 project/skill allowlist·동일 또는 단축된 만료/정확 신뢰 루트** 조건에서만 현재 `POLICY-STATIC-V1`을 $3로 등록하고 요청당 보호 `max_request_usd=3` 정합화. `enabled_at`·`earliest_request_at` 또는 동등한 **활성화 시점 새 epoch**를 신뢰되는 **이번 적용 시각**으로 조정해 구 STATIC의 소급 통과 방지, 유효한 signer 권한/재서명 및 load 검증. 보존된 일·월 값은 코드상 무효임이 이미 확인돼 있으므로 무리하게 삭제/임의 수정 금지. 보호 JSON 직접 덮어쓰기/서명 위조/비승인 키 생성/allowlist 확대 금지. **epoch 변경이 기존 신규 정상 요청을 오판하거나 보호 위임 인증을 무효화한다면 BLOCKED**.
- 재가동 전후 동일 ZIP SHA·정책 로드·DB 처리키/claim/영수증·전송 0/중복 0, SHADOW/rollback, watcher 2주기+재시작 검증. 과거 DESIGN R1은 `REVIEW_POLICY` 등 영구 거부, 완료 LARGE R2/Guard UNCERTAIN/위임전 3건 signer/READY/model 0. Task/Notifier 기존 가동 정상. 불확실하면 **현재 상태 보존하고 기존 v0.2.25 및 보호 위임 $1로 안전 롤백**, 정확한 중복/불확실 영수증 보존.

## 5. 자동 리뷰 E2E 증명 (신규 유료 리뷰를 또 실행하지 않음)
- 실제 live에서 별도 **두 번째 유료 리뷰**로 smoke하지 말 것. 가능한 경우 2단계에서 생성된 **실제 정식 REQUEST→APPROVAL_SIG→READY→독립 리뷰→영수증**의 운용 기록(기존 LIVE v0.2.25)을 증거로 재사용하고, 새 LIVE v0.2.28의 자동서명/READY/엔진 경로는 **완전한 SHADOW(fake signer/transport/runner; 유료 모델=0)**로 확인. 실제 v0.2.28에서 신규 자동 모델 실행을 아직 관측하지 못했다면 **`AUTO_SIGNING_HOST=PASS_SHADOW`, `NEW_LIVE_PAID_END_TO_END=NOT_RUN`**으로 정직하게 구분. 한 번 검증을 위해 모델을 두 번 부르지 않음.
- LIVE 새 유료 요청에 대한 실제 자동 서명·독립 리뷰는 **다음 정상적인 사용자 리뷰 요청**을 통해 자연 검증한다. 그 전까지 전체 운영을 `E2E_PAID_VERIFIED`라 과장하지 않는다.
- 기존 Telegram 완료 Notifier는 읽기 전용 현황 확인만(기존 사용자가 연결 완료로 보고함), 신규 중복 sender/bridge 추가 금지.

## 6. 결과 일괄 게시 / 종료
- 모든 중간 단계의 사실·증빙은 같은 Work에 누적하고 최종적으로 **한 결과 문서** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_AUTO_REVIEW_COLLAB_ONE_SHOT_RESULT_FOR_GPT_20261119.md`에 통합 보고. 필요하면 리뷰 REQUEST/READY/RESULT/RECEIPT는 기존 정식 경로의 본문을 링크. CURRENT 상단 현행 요약 + TRACKER 파생 필드만 갱신.
- 출력 필드: `FINAL_ZIP_NAME/SHA256/SIZE`, `WINDOWS_FULL_TESTS=PASS/FAIL/SKIP`, `E2E_SHADOW`, `INDEPENDENT_REVIEW=PASS/FAIL/BLOCKED/NOT_RUN`, `REVIEW_REQUEST_ID`, `MODEL_CALLS`, `MODEL_COST_HOST_AND_RECEIPT`, `REVIEW_INPUT_SHA_BINDING`, `GPT_DISPOSITION=PENDING/ACTUAL`, `RELEASE_GATE`, `BACKUP_ROLLBACK`, `LIVE_VERSION`, `AUTO_SIGNING_USD3`, `RETROACTIVE_MODEL_CALLS`, `PAID_LIVE_E2E`, `NOTIFIER`, `OPEN_BLOCKERS`와 각각 실제 근거.
- PRIVATE main에만 게시하고 파일·ZIP/manifest/diff의 commit, 원격 본문/바이트 SHA-256/CRC를 대조. PUBLIC/업무 호스트 배포 없음. 잘못된 승인 범위/원격 게시 실패가 발생해도 유료 모델·Job 재실행 금지.
- **끝낼 때 사용자가 다시 선택하게 하지 말고, 마지막 결과에 운영 상태와 남은 진짜 blocker 한 가지(있다면)만 제시.** 한 번의 Windows 실행에서 전체 진행을 목표로 하되 권한 없는 실운영 변경/유료 재호출을 성공으로 만들지 않는다.

**NEXT_ONE_ACTION**: Windows Claude Code가 **이 파일 하나의 0~6을 한 번에** 수행해 PRIVATE main에 최종 통합 결과 게시. 이 인계는 자체로 REQUEST/READY/LIVE 실행 트리거가 아니며, 실행은 실제 Windows 호스트에서 수행해야 한다.
