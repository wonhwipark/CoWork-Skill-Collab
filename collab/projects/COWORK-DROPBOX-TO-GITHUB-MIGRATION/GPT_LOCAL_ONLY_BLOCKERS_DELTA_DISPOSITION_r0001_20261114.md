# GPT 판정 — LOCAL_ONLY 차단 항목 delta / 실제 자동 리뷰 재개 게이트
작성: 2026-11-14 KST | r0001
Repository: PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
Source: `CLAUDE_LOCAL_ONLY_BLOCKERS_DELTA_RESULT_FOR_GPT_20261114.md` (commit `596b6732c29149fedd2176879c17c2df88e3c043`), `CURRENT.md` and `TRACKER.json`.
Decision: **ACCEPT_WITH_CHANGE / SELF_TEST_REPORTED**, `ACTIVE_PROVIDER=NONE`, `MIGRATION_NOT_CUTOVER`, `INDEPENDENT_REVIEW=NOT_RUN`.

## 1. 수용 결과 및 범위
- 로컬 독립 리뷰어: 기존 Windows PC의 egress probe `NOT_ISOLATED`; 5개 외부 도메인에 TCP 연결 가능. 로컬 모델 런타임 미발견. **외부 API Claude를 PC에서 실행하는 것은 D2 LOCAL_ONLY로 인정하지 않음**. 다른 승인 온프레미스 호스트·사람 리뷰어 존재는 아직 확인되지 않음.
- 진단 `reviewer_isolation_probe_r0001.py` 12 PASS(개발자 자체시험), 루프백 양성·음성 대조, DNS/TCP reachability 판정과 digest. 이 검사는 **외부 전송 차단의 필요조건 일부**이지 조직의 네트워크 격리/실제 실행위치 증명은 아님. DNS 질의/TCP handshake 자체는 네트워크 활동이므로 `no bytes sent`는 **애플리케이션 콘텐츠 페이로드 미전송**으로 한정해 읽음.
- 로컬 전용 `local_only_contract_r0002.py`: nonce·영수증 상태 저장, TTL, 비용 0.00, signer 분리, locality attestation digest, 필드 minimization 등 개선 보고; 26 PASS×8, 10개 mutation PASS(전부 개발 세션 `SELF_TEST_REPORTED`). 이전 r0001의 작은 숫자를 random hex 부분 문자열로 비교한 비결정적 시험은 수정 수용. r0001은 이력으로 보존하고 후속 검토는 r0002 기준.
- LIVE 서비스 계정 분리: 관리자 계정 그대로는 운영 archive DB ACL deny 증명을 적용할 수 없음. **전용 비관리자·GitHub 전용 state dir·old archive 권한 0/제한 로그온** 제안을 수용하되 설치·Task/ACL/DB 이행은 별도 운영 승인 전 NOT_RUN.
- 기존 식별자: SHA·크기·파일명 이력 범위 정량화는 **호스트 자체 보고**로 수용. 비밀 유출 여부의 법적/조직적 판정은 NOT_VERIFIED. `RESTRICTED_PENDING_CLASSIFICATION`, add-only 신규 제한정보 게시 중단. history rewrite/force push/삭제는 하지 않음.

## 2. GPT 정적 코드 리뷰에서 확인한 추가 운영 차단 위험 (r0002 소스 기준)
`tools/local_only_contract_r0002.py`를 GPT가 PRIVATE main에서 직접 읽어 확인한 **정적 코드 사실**:
1. **동시 호출 직렬화 부재**: `State.__init__`이 파일을 읽어 `nonces/accepted` 집합을 메모리에 저장하고, `check_request()`와 `ReceiptLedger.accept()`가 집합 변경 후 `State.save()`에 맡긴다. `save()`는 고정 `.tmp` 이름에 덤프 + `os.replace()`를 사용하지만 **프로세스 간 잠금/SQLite 원자 CAS/lease 검증은 구현돼 있지 않다**. 따라서 두 reviewer/watcher가 동일한 이전 상태를 읽고 동시에 nonce를 허용하거나 영수증을 수락할 위험이 있다. 동일 `.tmp` 경합은 기록 실패/덮어쓰기 위험도 있음. 별도의 OS 단일실행 락이 외부에 있을 수는 있으나 이 프로토타입만으로 재시작·경합 보장을 주장할 수 없다. **운영 전 필수 보완 또는 검증된 기존 단일실행/원장 계약과 결합하고 멀티프로세스 재현시험**.
2. **상태 파일 삭제와 최초 생성 미구분**: `State.__init__`은 `path`가 없으면 `nonces/accepted`를 빈 집합으로 시작한다. 이미 사용한 장부가 삭제/이전/경로 변경된 상태도 초기 기동처럼 취급되어 **이전 승인 replay를 거부할 근거가 사라진다**. 손상된 *존재하는* JSON은 fail closed지만 **사라진 파일은 아니다**. 첫 초기화 시 고정 genesis/checkpoint와 기존 작업·원장 복원 확인, 손실 시 FAIL_CLOSED를 구분하는 상태 머신 또는 운영 DB 내 durable transaction 필요.
3. **실제 reviewer 위치**: 리뷰어 영수증의 `reviewer_locality=ON_PREM`과 `runtime_attestation_sha256`는 형식·서명만 확인하며 격리 호스트의 외부 전송 경로 전체나 증거 digest 원본까지 독립적으로 확인하지 않는다. 이전 보고처럼 **ATTESTED_NOT_VERIFIED** 유지하고 사용자/조직 검증 없이는 E PASS 불가.

### 최소 delta 수락 시험
- 같은 request/nonce를 **두 프로세스 동시에** 검증: reviewer 호출/승인 정확히 1회, race/파일 손상/덮어쓰기 0.
- 이미 정산된 파일을 저장한 뒤 **state 파일 삭제·재시작**: 신규 bootstrap 허가 없이 기존 nonce·영수증 재승인 0; `STATE_MISSING_AFTER_INITIALIZATION` 등 FAIL_CLOSED.
- `.tmp` 경합·강제 종료·os.replace 오류/전원중단/복구: 원장 무손실, 성공을 보장할 수 없는 리뷰는 REVIEW_UNCERTAIN 봉인·자동 재호출 0.
- reviewer 위치 주장 vs 승인된 외부 전송 차단 정책과 attestation 검증; 서명된 주장을 host-real 검증으로 승격하지 않음.
- 기존 제품 500+ 시험/토큰 mock·ETW/26 PASS 통째 재실행 금지; 영향받은 delta만 실행. 개발자 자체 시험은 공식 E 독립 리뷰로 소급하지 않음.

## 3. 자동 리뷰 재개 임계 조건과 순서
1. **최우선 사실 두 개**: (A) 조직 관리 별도 서명자 PC와 공개 도구 6개 내부 이동 가능 여부, (B) 조직 승인한 실제 로컬 독립 리뷰어(온프레미스 모델 host 또는 사람)의 존재/접근. 현재 둘 다 미확인; 추가 코딩만으로 해소 불가.
2. 승인 범위 내에서 §2 세 결함 위험을 통합 수정·회귀시험하고, v2 제어면 계약과 로컬 원장/리뷰어 실행을 **별도 독립 보안 리뷰** 준비. 자동 리뷰로 가려면 사람 reviewer만 있는 경우에는 별도의 자동 호출 주체/절차가 추가 필요.
3. 서비스 계정 및 ACL 실제 설치, 최소 권한 PAT **신규 사용자 발급**(기존 OAuth 사용 금지), 승인된 공개 검증키 root, local-only artifact vault/토큰/로그 노출 차단 및 runtime egress 검증, 서명된 receipt 실제 저장/원격 readback(허용 필드만), 중복 0·reboot/rollback 검증.
4. 단계별 승인: 실제 키 생성/설치, 신규 PAT 발급/설치, 운영 계정·DB/예약작업 변경, 독립 리뷰, GitHub LIVE 활성화 **각각 명시 승인**. 기존 GitHub 원문 ZIP+READY 계약은 D2에서 무효이며 `LOCAL_ONLY_V2=PROTOTYPE_ONLY` 유지.
5. 기존 Dropbox watcher/Bridge/updater Disabled, Telegram notifier Running, `ACTIVE_PROVIDER=NONE` 유지. GitHub 문서 게시로 Windows 작업이 자동 실행되지는 않음.

## 4. 다음 단일 동작
사용자에게 다음 **두 사실만 한 번에 질문**한다.
- 별도 조직 관리 signer Windows PC가 실제 사용 가능하고, 6개 서명 키트 파일을 **조직 내부에서** 그 PC로 이동하는 것이 정책상 가능한가?
- 조직이 승인한 별도 온프레미스 모델 호스트나 독립 사람 reviewer가 실제 있는가? 있다면 종류(모델 호스트 / 사람), 코드 외부 전송을 차단할 수 있는가?
이 답이 없으면 `B=AVAILABLE_UNDESIGNATED, E=BLOCKED_LOCAL_REVIEWER`로 기록하고 임의 운영 변경 없이 종료. 내부 개발자에게 후속 delta 요청이 가능해지면 §2 소스 확인된 2가지 구현 위험과 위치 검증 한계만 **단일 통합 작업**으로 처리한다.
