# CoWork GitHub 이전 — GPT PHASE1 판정 및 PHASE2 통합 게이트 r0001
날짜: 2026-11-10 KST | GPT_AUTHORITATIVE_DISPOSITION | PR_FREE
근거: `CLAUDE_PHASE1_IMPLEMENTATION_RESULT_FOR_GPT_20261110.md` (Windows Claude Code 보고, PRIVATE main; Claude 보고 SHA-256 17e88579… / 9694 bytes / commit a3f30d85), 설계 r0002 및 기존 정적 리뷰.
**증거 구분:** GPT는 게시된 MD 원문을 GitHub에서 직접 읽어 판정했다. 개발 후보 ZIP은 로컬 Windows dist에만 있어 GPT가 raw bytes/소스 및 시험을 독립 검증하지 못했다. Claude가 직접 구현하고 실행한 합성시험은 독립 Claude 정식 리뷰가 아니다.

## 1. 현재 판정
PHASE1 = **ACCEPT_WITH_CHANGE / PARTIAL**, PRODUCTION_INSTALL=NOT_APPROVED, GITHUB_LIVE=NOT_APPROVED, INDEPENDENT_FORMAL_REVIEW=NOT_RUN.
- Windows 격리 복사본: GitHubTransport, 승인 fail-closed gate, B-2~B-6 수정 구현 보고.
- pytest: 전체 272 PASS / 0 FAIL / 12 SKIP; 기존 Dropbox 232 PASS/12 SKIP (이전 기준 236 PASS/8 SKIP과 차이 원인 아직 불명확), 신규 합성 40 PASS.
- 전체 48 인수시험: 21 SYNTH_PASS (T20은 부분; S01~S10은 테스트 더블), 27 NOT_RUN. **실 Ed25519 S01~S10 NOT_RUN**.
- ZIP: skill-collab-watcher_v0_2_0_1110.zip, 보고된 108936 bytes, SHA-256 1003c1aba21b8e6ac4db0ca599cadb9ba83950097e8eb82d97c9849a24b7ba52. Windows 로컬만, development_not_for_deployment. GPT 직접 byte 검증/보유 NOT_RUN.
- 실 GitHub API/Windows SHADOW/Telegram/운영 SQLite/정식 Claude 독립 리뷰/배포 NOT_RUN.

## 2. 항목별 GPT 판정 — 구현 완료를 운영 안전성 승인과 구분
| 항목 | GPT 판정 | 구현 보완 및 수락 조건 |
|---|---|---|
| B-2 | ACCEPT_WITH_CHANGE | 정확한 basename 분류는 안전 방향이지만 **기존 Dropbox에서 READY로 분류되던 과거 사이드카를 새로 활성화할 수 있음**. 과거 요청 재검출 시 모델 0 회귀 및 V1 파일명 규칙 호환을 입증. 신규 승인 파일은 APPROVAL_SIG.json / SOURCE_PIN.json 고정. |
| B-3 | ACCEPT_WITH_CHANGE / OPERATING_GATE | 모든 CLAIMED/REVIEW_RUNNING을 시작 시 일괄 봉인하면 살아있는 작업이나 운영 이력을 변형할 수 있음. **운영 DB는 사전 read-only 인벤토리+백업**, 이전 프로세스 생존/lease 확인, 대상 범위와 알림 1회 보장, 재호출 0 검증 후 승인. 자동 recover --requeue 경로 차단 필요. |
| B-4 | ACCEPT_WITH_CHANGE / PARTIAL | provider_lease 및 SHADOW read-only 구조는 유효. epoch=1 고정, 전환 이력·lease 만료·시뮬레이션 동시기동 검증 필요. SHADOW가 기존 Dropbox DB를 수정하지 않을 것. |
| B-5 | ACCEPT_WITH_CHANGE | 정책 변경만으로 같은 logical request 재실행하지 않도록 차단한 수정 수용. 같은 request_id/revision/package와 명시적 신규 승인 구분, 과거 처리 이력·provider별 일관성 실증 필요. |
| B-6 | ACCEPT_WITH_CHANGE / LEGACY_COMPAT_GATE | 원본 바이트 SHA는 GitHub adapter에 적합하지만 **기존 Dropbox READY 생성기/validator의 기대 해시와 어긋날 수 있음**. 실 기존 REQUEST/READY 샘플에서 byte/text hash 일치 여부 확인. 필요하면 provider-별 호환 검증기를 택하되 서명 검증에는 항상 원본 bytes를 사용. BOM 허용/거부를 schema로 고정. 기존 요청 호환성 PASS 전 운영 적용 금지. |
| T08 충돌 | ACCEPT_WITH_CHANGE | 동일 ID+revision에 다른 ZIP이면 CONFLICT로 차단하고 기존 결과 보존. 명시적 변경은 신규 revision/승인으로 처리. 이전 완료 기록과 충돌해 재호출하지 않을 것. |
| B-1 | DEFER_REAL_CRYPTO_APPROVAL | 인터페이스/fail-closed는 수용. 실제 Ed25519 백엔드는 **격리된 개발용 venv에서만** 버전/해시 pin 후 별도 사용자 승인을 받아 시험. 운영 venv 변경 금지. |
| B-7 | DEFER_TRUST_BOOTSTRAP_APPROVAL | TrustRoot 로더 interface 수용. **임시 합성 시험키와 실제 운영 신뢰키 발급은 별개의 승인·수명주기**. 운영 키/개인키/토큰을 GitHub에 두지 않는다. 회전/폐기/만료/clock skew/권한 분리 정책 먼저 확정. |
| N-2 | REQUIRED_BEFORE_LIVE | Telegram의 Dropbox 전용 링크/표기 교체, provider별 단일 완료·불확실 알림, 중복 0 검증. 합성 T20 Telegram 0 관찰도 보완. |
| 테스트 기준 차이 | NEED_INFO | 기존 pytest 236/8 → 232/12 변화의 정확한 SKIP 원인/목록/환경 증명; 실패 0만으로 회귀 PASS 승인하지 않음. |

## 3. PHASE2는 하나의 검증·보완 작업으로 통합
1. 실제 Windows v0.2.0 **격리 복사본**에서 위 B-2/B-3/B-4/B-5/B-6/T08/N-2 변경 및 호환성 보완, 이전 Dropbox 요청/READY에서 원본 바이트 해시와 파서 의미 비교.
2. 전체 번호별 48개 T/S 시험의 누락 사항을 **합성 시험 가능한 범위까지 연속 확대**. SHADOW/실 서명/실 GitHub/Public/운영이 필요한 항목은 NOT_RUN 유지. 12 SKIP 사유를 추적하고 재발 방지.
3. 기존 운영 DB·설치/예약작업은 READ_ONLY, **운영 상태를 임의로 봉인하지 않음**. 작은 재검토/프롬프트 왕복 없이 격리 코드 수정→회귀→ZIP→보고 연속 수행.
4. B-1/B-7은 별도 승인 전 기존 venv/실 token/key에 손대지 않는다. 승인 시 개발 격리 venv에서 pin된 cryptography·폐기 가능한 시험키만 써서 실제 S01~S10, 서명 재생·만료·키 폐기 시험. 운영 신뢰키 발급/실 API 최소권한 토큰/SHADOW/LIVE는 계속 별도 승인.
5. 새로운 후보 ZIP은 기존 버전을 보존한 새 버전으로 발행. source/ZIP bytes, SHA-256, test command·pass/skip/evidence, remaining NOT_RUN와 실 모델 호출 0, 운영 무변경을 보고. 소스 반출/비밀 검사를 통과하고 사용자 승인 전에는 사외 공개/PRIVATE 게시도 주의.
6. **분리 검증:** 실제 독립 Claude 리뷰는 개발 Claude 세션의 자체 pytest 결과와 다르다. 리뷰 단계에서 승인된 신규 REQUEST/READY 절차와 영수증이 있을 때만 정식 독립 리뷰로 판정.

## 4. 승인/비승인 경계
**지금 승인되지 않은 사항:** 운영 Windows venv 라이브러리 설치, 운영 신뢰키/서명 개인키 발급, GitHub 최소권한 PAT/토큰 생성, watcher 설치/SHADOW 가동/LIVE 컷오버, 실제 유료 Claude 리뷰 호출, PUBLIC ZIP 게시.
**권고할 다음 사용자 단일 승인 질문:** "운영 환경을 건드리지 않는 별도 격리 개발용 venv에서 cryptography의 버전/해시를 pin해 설치하고, 폐기 가능한 테스트 전용 Ed25519 키만 만들어 S01~S10을 시험하도록 승인합니까?" 이것은 운영 trust root 배포 및 token 생성 승인과 명확히 다르다.

## 5. 다음 한 동작
승인 범위가 정해지면 **PHASE2 통합 검증·보완 원샷**을 Windows Claude Code에 1회 전달. 결과 MD·새 ZIP 해시를 GPT가 판정한다. 사용자 승인 전에도 운영 불변의 설계/합성 회귀 보완은 가능하다.
