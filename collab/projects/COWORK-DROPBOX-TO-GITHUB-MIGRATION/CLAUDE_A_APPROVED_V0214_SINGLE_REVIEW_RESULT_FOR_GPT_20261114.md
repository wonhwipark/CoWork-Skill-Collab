# CLAUDE A안 승인 범위 결과 — v0.2.14 단일 R1 독립 리뷰 (GPT 판정용)

- 작성: Windows Claude Code (2026-11-14 KST). 이 문서는 **Claude 자체 보고**이며 GPT 판정 전까지 canonical이 아니다.
- 근거 인계서: `GPT_A_APPROVED_V0214_SINGLE_REVIEW_AND_TIER_HANDOFF_r0001_20261114.md`
- 승인 밖 항목(운영 DB·Task 변경, 새 PAT 발급·설치, 추가 유료 리뷰, LIVE 활성화)은 **실행 0건**. 운영 DB는 열지 않았다.

## 1. 한 줄 결론

| 항목 | 상태 |
|---|---|
| 서명키·신뢰 루트 준비 | DONE (암호화 보관, trust_root_independence=warn) |
| REV-COWORK-V0214-20261114 R1 독립 리뷰 1회 | DONE (모델 호출 1회, $0.9695 ≤ $1) |
| 결과 업로드(엔진) | 엔진 쓰기는 읽기전용 토큰이라 403 → `UPLOAD_PENDING`(설계 동작). 개발자 `gh` 로그인으로 동일 바이트를 게시 |
| 리뷰 지적 5건 | 전부 재현(F1은 조건부) → 격리 후보 v0.2.17에 최소 수정 + 회귀 시험 |
| BLOCKED | 없음(계약 우회 0건). 단, 아래 §8 항목은 승인 대기 |

## 2. 서명키 / 신뢰 루트

- 키 ID `cowork-approver-1`, Ed25519 공개키 지문 `9c6f650ce89d7cad177c17520ba3452345bb7e927fbde39780d07d8db141d90c`
- 신뢰 루트 핀(sha256) `591c22fc2938caaa4f90686c761713c2bf66a5440397fbb28cf3e369d457d9c7`, repo_id 라벨 `1451933830`
- 개인키는 scrypt+AES-GCM 암호화 파일, 암호문 비밀번호는 무작위 생성 후 **Windows DPAPI(CurrentUser) 블롭으로만** 보관. 평문 키·평문 비밀번호는 어디에도 없음(자체 시험 15항목 PASS: 왕복·손상·ACL·덮어쓰기 거부·서명/검증/변조 거부).
- 폴더는 사용자 전용 ACL, 동기화(Dropbox) 폴더 밖. 단일 PC 키이므로 신뢰 루트 독립성은 `warn`(승인된 그대로).

## 3. 리뷰 실행 사실

- 요청 `REQ-COWORK-V0214-R1-20261114` rev 1, 패키지 `skill-collab-watcher_v0_2_14_1114.zip` 219663 B, sha256 `3a221dcdb22ba75208a60ca555b0ee75866313a591148b1f482b7cbb6aa0b367` (ZIP 변경 0).
- 게시 순서: commit A(패키지+요청) `aedddc49bfdc…` → commit B(APPROVAL_SIG·SOURCE_PIN(=A)·READY, 마지막) `2ed6dbafe23b…`. 승인 유효 2시간, 정책 `POLICY-STATIC-V1`, effort medium, 최대 $1.
- 사전 리허설(격리·스텁): 읽기전용 토큰이면 모델 1회 호출 후 `UPLOAD_PENDING`, 재호출 없음 확인. 드라이런 후 실제 1회.
- 사용: 모델 호출 1회, 18 turns, 비용 $0.9695. **R1 목표(입력 16k/출력 3k/turn 3)는 초과**(비용 상한만 준수). CLI 2.1.218은 `--max-turns` 미지원이라 turn 상한을 걸 수 없었음 → R1 등급 turn 목표를 강제하려면 다른 수단(프롬프트 지시·예산) 필요.
- 독립성: 별도 프로세스, 빈 작업 폴더, 도구 Read/Grep/Glob, dontAsk, MCP 0, 세션 비저장, 프로젝트 설정 미로드, 개발 세션 문맥 공유 없음.
- 게시(PRIVATE main, 원격 바이트·SHA 일치 확인): 리뷰 결과 `1df4fb8be6a1`, 영수증 `6c3f7f1da0ac`, 사용 영수증 `772ea6607883` (`collab/reviews/REQ-…/REVIEW_RESULT_1.md`, `collab/receipts/REQ-…/`).
- 주의: 리뷰에 쓴 엔진은 v0.2.16이고 리뷰 **대상**은 v0.2.14이다(엔진≠대상, 의도된 구성).

## 4. 지적 5건 검증과 처리 (미패치 v0.2.16 복사본에서 재현 후 수정)

| # | 리뷰 분류 | 재현 | 내 판정 | 최소 수정(후보 v0.2.17) | 회귀 시험 |
|---|---|---|---|---|---|
| F1 | BLOCKING: 미디스패치 job이 정책 개정 변경 시 이중 디스패치 | 조건부 재현 — 재서명(새 nonce)+정책 롤백+커서 유실에서만 | MAJOR, 범위는 롤백/커서 유실로 **좁음** | 논리 요청 조회가 미디스패치 키도 보고, 디스패치된 논리 job이 있으면 거부 | `test_f1_…` |
| F2 | BLOCKING: watch의 seal이 살아있는 scan의 job을 봉인 | 재현(오탐 `REVIEW_UNCERTAIN`) | MAJOR | `scan`도 `watch.lock`을 취득(동시 실행 거부, exit 3) 후 exclusive | `test_f2_…`, `test_a_second_scan_is_refused…` |
| F3 | 비차단: 일일 상한 check-then-act | 재현(공유 패키지에서 calls==2) | MAJOR로 상향 확정(비용 직접 영향) | 클레임을 `BEGIN IMMEDIATE`로 상한 검사+예약 원자화 | `test_f3_…` |
| F4 | 비차단: scan 전용 운영에서 크래시 job이 조용히 CLAIMED로 잔류 | 재현 | 운영 공백 확정 | F2 수정으로 다음 scan이 봉인(`REVIEW_UNCERTAIN`) | `test_f4_…` |
| F5 | 비차단: 타임아웃 시 프로세스 트리 미종료 | 재현(.cmd 래퍼 손자 프로세스 생존) | 확정 | `Popen` + `taskkill /T /F`로 트리 종료 | `test_f5_…` |

- 수정 중 발견한 부수 회귀 1건(내가 넣은 lock 핸들러가 `ShadowIsolationError`를 삼켜 SHADOW 거부 exit 코드가 6→3): 수정하고 scan·watch 양쪽 회귀 시험 추가.
- 격리 시험 결과(후보 v0.2.17): 시험 venv **644 passed / 12 skipped**(기준 v0.2.16: 636/12), 운영 인터프리터 **578 passed / 17 skipped**. 변경 파일은 `state_store`·`orchestrator`·`cli`·`review_runner`와 시험.
- 후보 v0.2.17은 **로컬 격리 산출물이며 미리뷰·미게시**. 자동 재리뷰 없음(승인 밖). v0.2.14 ZIP은 바이트 보존.

## 5. v0.2.16 후보 vs 승인된 리뷰 대상(v0.2.14) 차이

- 코드 변경 파일: `cli`, `config`, `models`, `notify_events`, `orchestrator`, `review_runner`, `state_store`, `validator`, 런북 1건, E2E 스텁·시험 2개(+신규 시험 `test_usage_limit_resume`, `test_token_file_formats`).
- 주 내용: (a) **사용량 한도 대기·재개** 로직 신규(`usage_limit_wait_sec` 1800 / `_max_wait_sec` 86400 / `_max_deferrals` 12, 한도 메시지 정규식, 비재시도 한도 분류) — 가장 큰 증분, (b) GitHub 토큰 파일 형식 지원(JSON token/repo/scope/expires) 시험, (c) 알림 이벤트·검증기 소폭 변경.
- v0.2.14 리뷰는 위 (a)(b)를 **보지 않았다**. 따라서 v0.2.14 리뷰 통과가 v0.2.16(및 v0.2.17)의 통과를 뜻하지 않는다.

## 6. 추가 발견(비차단, GPT 판정 요청)

1. 승인 서명의 `repo_id`는 신뢰 루트의 **라벨**일 뿐 저장소 실체와 대조되지 않는다(payload/pin 간 문자열 비교만).
2. r0002 토큰 검사기는 엔진이 읽는 JSON 토큰 파일 형식을 읽지 못한다(도구 한계). 엔진 판독기 로직으로 별도 확인했고 토큰 값은 출력하지 않음.
3. 읽기전용 fine-grained 토큰에 **만료 없음**, 개발자용 클래식 쓰기 토큰 존재 — 회전·만료 정책 필요(새 PAT 발급은 미승인이므로 미실행).
4. 리뷰 결과 문서는 서술형이라 R1 토큰 목표 초과 시 자동 차단 수단이 없다(`--max-turns` 미지원).

## 7. LIVE 전환에 필요한 미완료 항목

- GitHub 인증: 엔진 쓰기 가능한 B안 쓰기 PAT(승인·발급·설치 미실시) → 그 전까지 결과 업로드는 `UPLOAD_PENDING`.
- SHADOW: 실제 계정 격리 SHADOW 가동 증거 없음(시험은 격리 환경 한정).
- 백업/복구: 운영 DB의 실제 백업·복구 리허설 미실시(운영 DB 접근 미승인).
- 알림: Notifier의 GitHub 연결·실전 알림 미검증.
- 운영 인터프리터에 서명 검증용 암호 라이브러리 런타임 확인 필요(시험 17개 skip 중 일부가 이 사유).
- 컷오버·롤백 리허설, v0.2.17(수정본)의 **재리뷰**(신규 승인 필요), 리뷰 등급 R0~R3 상시 정책 승인.

## 8. 사용자 승인이 필요한 남은 결정

1. B안: 쓰기 PAT 발급·설치(만료 포함).
2. 수정본 v0.2.17(또는 v0.2.16 기반 재작성) 재리뷰 1회 승인(등급·비용).
3. R0~R3 상시 정책 일회 승인 여부.
4. 운영 DB 백업·복구 리허설과 SHADOW 실가동 승인.

## 9. 한계

- 본 결과는 정적 리뷰와 Windows 격리 시험이며 Linux·사내 LLM·MCP 동작은 검증하지 않았다.
- 리뷰 PASS가 아니라 **지적 5건의 목록**이다. 최종 판정과 canonical 갱신은 GPT 몫.
- 비밀값·경로·계정명은 이 문서에 포함하지 않았다.
