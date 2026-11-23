# Windows Claude Code — v0.2.35 독립 리뷰 → LIVE 원샷 실행 인계 (사용자 최종 승인 반영)
작성: 2026-11-23 KST
정본: wonhwipark/CoWork-Skill-Collab / main
기존 Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
최신 근거: CURRENT.md 최상단, CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md §13
이 문서는 호스트 실행 트리거가 아니며 실제 Claude Code 세션에서 명시적으로 실행해야 한다.

## 사용자 최종 승인 (이 대화 2026-11-23 KST)
1. **공개 리뷰 입력 1건 승인:** Windows 후보 `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_35_intent_scope_candidate.zip`, 정확 SHA-256 `658a6f3da8bd018b96b64453892aec77d96868e19bc5788745c1591b1729a740`, 307418 B, 114 ZIP 항목. 이 정확한 바이트의 ZIP만 공개 저장소에 리뷰 입력으로 게시 허용. 다른 SHA/파일·민감자료·임의 공개 확대 불가.
2. **조건부 LIVE 변경 승인:** 해당 후보의 독립 리뷰 통과 및 필수 게이트 검증 후, Windows 운영 watcher 안전 정지 → 설치 트리 v0.2.29→v0.2.35 교체 → 운영 DB `review_intent_nonces` 추가 전용 생성 → watcher 재시작. 설정·위임·키·trust root·Task 정의·Notifier·Bridge는 변경 금지.
3. **단일 모델 실행 금액 상한 없음 위험 수용:** 기존 시간 제한·외부 디스패치 최대 1회·서명·scope·만료·nonce·중복·원본 고정 검증 유지. 사후 비용/영수증 보존. 이 수용은 무제한 재호출/무권한 모델 실행 승인이 아님.
이 세 승인 항목은 다시 질문하지 말 것. 사용자 대화의 승인은 Windows 보호 signer의 암호학적 승인/위임/서명을 대체하지 않는다. 유효한 보호 실행권한이 확인되지 않으면 AUTH_BLOCKED/모델 0.

## 원샷 실행 순서
0. `collab/CONTEXT_BRIEF.md`, 이 Work CURRENT 상단, §13, 기존 리뷰/영수증, 실제 운영 상태를 최신 main과 Windows 호스트에서 확인. 이미 수행한 F1/F2/F3·QA28 28/28·Windows 스크립트 4/4·전체 회귀 1075 PASS/0 FAIL/8 GUI SKIP, v0.2.35 ZIP 결과는 원본 SHA가 일치하고 변경 영향이 없으면 증거 재사용. 기존 r2 리뷰 재실행 금지.
1. 로컬 ZIP SHA/크기/CRC/매니페스트/민감정보를 다시 확인. 정확한 ZIP 한 건만 기존 승인된 공개 CoWork 리뷰 입력 경로에 게시하고 원격 실제 bytes/SHA를 확인. 저장소 visibility를 실제 재조회(브리프에 따르면 현재 PUBLIC), 반출 금지 자료 없는지 확인. 다른 패키지 게시 금지.
2. 기존 `collab/ops/submit_review_request.py` 및 `collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md` 계약에 따라 동일 Work의 기존 요청/영수증과 중복 대조 후 신규 v0.2.35 독립 리뷰 REQUEST+ZIP Commit A → SOURCE_PIN Commit B 게시 및 원격 readback. 정확한 repo_id 문자열, ZIP SHA/크기/REQUEST revision 고정. 유효한 보호 위임·서명·만료/nonce/원본 검증이 되면 APPROVAL → READY LAST → watcher DISPATCH → RESULT/RECEIPT 확인. 모델 실행이 이미 시작됐거나 불확실하면 재큐잉 금지. 유료 리뷰라는 별도 유형/금액 상한 차단 재도입 금지.
3. 독립 리뷰 결과 BLOCKING=0 및 보호 검증 통과를 확인. BLOCKING이 있으면 LIVE 중단, 기존 Work에서 보완·시험·새 후보 패키징. 새 SHA는 이 승인된 공개 ZIP 및 LIVE 설치 대상과 다르므로 새 공개/설치 승인 범위 확인 전 전환 금지. 리뷰 완료가 불확실하면 모델 재실행 금지.
4. 운영 전환 전 게이트: 실제 GitHub 전송 경합/원자성 및 Windows 호스트 설치 SHADOW를 안전한 격리/승인된 시험 경로에서 검증; GitHub 원격 쓰기·모델 호출은 유효 권한 범위만. 실행 불가한 필수 검증은 NOT_RUN/BLOCKED로 두고 LIVE 강행 금지. 컷오버 직전 DB/WAL/SHM 일관된 새 백업과 복구 무결성, 설치 트리 백업 재검증, 기존 실행/중복/UNCERTAIN·provider=github 단일성·설정/위임/키/Task/Notifier 불변 확인. v0.2.29 rollback 절차와 nonce 테이블의 구 코드 호환성 확인.
5. **모든 필수 게이트 통과 시에만** 승인 범위의 watcher 정지→설치 교체→추가 전용 테이블 생성→watcher 시작. 단일 provider와 기존 이력/nonce/DB 보존. 설정·위임·키·Task 정의·Notifier·Bridge 변경 금지. 실패 시 안전 정지/기존 설치 트리 복원/현재 DB 유지/해시 대조/재기동; 임의 재호출·DB 교체·DROP 금지.
6. 운영 검증: 버전 0.2.35/프로세스/Task/Notifier 상태, WATCH_START, DB integrity, provider 단일성, 비용 차단 제거·보호 fail-closed·중복 방지. 승인된 유효 실제 요청이 존재할 때만 승인→READY→DISPATCH→RESULT→RECEIPT E2E 검증. 테스트를 위해 무권한 유료 요청 생성하지 말 것. 실모델 검증이 불가능하면 해당 항목 NOT_RUN 및 LIVE 검증 한계를 명시.
7. 기존 결과 문서 §14(후속 절), CURRENT 최상단, 필요한 TRACKER 필드만 업데이트하고 `main`에 PR 없이 게시, commit/원격 바이트 readback 확인. 증거/영수증/해시·시험/승인 범위·설치 버전·백업·복구·미실행·LIVE 상태·다음 한 행동을 기록. 민감 키·운영 DB·제한 코드 게시 금지.

## 완료 기준과 차단 규칙
- REVIEW=PASS, 필수 운영 검증 PASS, 실제 설치/기동 확인 후에만 LIVE=ON. LIVE_READY는 별도 판정.
- 게시 완료는 호스트 실행/독립 리뷰 완료/LIVE 활성화의 증거가 아님.
- 유효한 사용자 승인 범위 안에서는 중간 확인 반복 없이 계속. 보호 권한 실패, 원본 SHA 불일치, 차단 리뷰, 필수 SHADOW/경합 실패는 해당 경계에서 fail-closed; 가능한 결과 게시까지 진행.
- Windows Claude 개발 세션 자체 시험과 독립 리뷰 분리. 완료된 리뷰/Job/모델 호출 재실행 금지.
