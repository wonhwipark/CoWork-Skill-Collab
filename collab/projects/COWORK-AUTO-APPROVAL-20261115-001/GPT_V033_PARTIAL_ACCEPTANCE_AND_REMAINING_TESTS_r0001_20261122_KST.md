# v0.2.33 후보 — GPT 부분 수용 및 남은 시험 판정

- 날짜: 2026-11-22 KST
- 저장소/브랜치: wonhwipark/CoWork-Skill-Collab/main
- Work: COWORK-AUTO-APPROVAL-20261115-001
- 근거 HEAD: 9051f9593a93fe7198465ee8be892cb98e575857
- 원본: [Windows 후속 결과 §9](CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md), Git blob `4cc2e30a1b10c0ca96645e14679ec52164e321c9`
- **GPT_DISPOSITION=ACCEPT_DEVELOPMENT_WITH_CONDITIONS / STEP3=PARTIAL / LIVE_READY=NO**

## 인정하는 결과

GPT가 원격 main의 결과 §9, CURRENT, TRACKER를 조회하여 사용자 보고와 대조했다. 아래 호스트 PASS는 Windows 개발자 자체 수행 보고이며, GPT의 ZIP 실물 검사·코드 검토·독립 리뷰 PASS가 아니다. Windows 원본과 실행 연결은 이 GPT 세션에 제공되지 않아 신규 호스트 시험은 NOT_RUN이다.

| 항목 | 판정 | 범위 |
|---|---|---|
| 1-A 후보 복사 | PASS (HOST_REPORTED) | v0.2.33 폴더, 소스 26/시험 58 |
| 1-B v0.2.29 설치 트리 백업 | PASS (HOST_REPORTED) | diff -rq IDENTICAL, 143개, 파일별 SHA 매니페스트. 기존 복사 권한 차단 해소 |
| 2 SCOPE 연결 | PASS (격리 구현 보고 수용) | commit A REVIEW_INTENT 바인딩, 검증 후 exact skill 1개, 영속 nonce INSERT, 운영 위임 목록 불변 |
| 3 nonce 저장소 경합·재시작 | PASS (HOST_REPORTED) | 서로 다른 OS PID의 nonce 소비자 1명, 저장소 재시작 후 중복 거부 |
| 3 회귀·ZIP | PASS (HOST_REPORTED) | 1007 PASS/0 FAIL/12 SKIP, ZIP 297249 B/109항목 및 검사 |
| 3 프로세스 간 디스패치 경합 | NOT_RUN | 스레드 경합만 존재. nonce 경합 시험으로 대체 불가 |
| 3 승인·디스패치 통합 경로 재시작 | NOT_COVERED | nonce 저장소 시험만 존재 |
| 독립 리뷰 | NOT_RUN / BLOCKED_AUTH | 기존 아키텍처 R1은 이 후보의 독립 리뷰 근거가 아님 |
| 운영 DB 이행·LIVE·호스트 SHADOW 설치 | NOT_RUN | 현재 수행 범위 밖 |

**1~3 전체 완료로 승격하지 않는다.** 기존 지시서가 요구한 프로세스 간 디스패치 경합과 전체 경로 재시작 검증이 미충족이다. 실제 GitHub 경쟁 시험은 기존 쓰기 금지에 따라 계속 NOT_RUN으로 분리한다.

## 기존 승인 범위에서 먼저 끝낼 시험

1. **디스패치 경합:** 기존 watcher/orchestrator 시험을 재사용하여 별도 OS 프로세스 두 개·서로 다른 temp DB·동일 ID/revision/PIN/ZIP으로 모두 디스패치 선점 직전 barrier에 도달시킨다. 프로세스 간 공유되는 원자적 fake claim 저장소를 사용한다. 한 프로세스의 nonce 거부 때문에 다른 한쪽만 claim에 도달한 경우는 이 시험의 PASS가 아니다. 서로 다른 PID·두 도달 이벤트·승자/패자 상태·공유 fake runner 총 호출 1 이하·패자 재스캔 호출 0을 기록한다.
2. **전체 경로 재시작:** 실제 후보의 의도 검증→nonce 소비→후보 상태 보존→재검증→보호 서명/READY→claim 경로를 fake signer/transport/runner로 실행한다. nonce 소비 후와 claim 후 중단·새 프로세스 재기동을 주입하고, 같은 요청 replay·다른 revision/SHA·실행 시작 불명 상태에서 권한 확대/추가 디스패치 0을 검증한다. nonce 저장소 단독 재오픈으로 대체하지 않는다.
3. **재검증 경계 추가 확인:** 보고상 `_revalidate`가 request ID에 대한 nonce 소비 기록으로 scope를 복구한다. 원본 코드를 읽지 못했으므로 결함으로 확정하지 않는다. 다만 소비 기록은 사용자 권한·유효 서명·현재 시각/해지·정확한 revision/commit/입력 바인딩을 대신하는 무기한 허가가 되어서는 안 된다. 최초 검증 이후 만료/키 해지/입력 변경 시 기존 재검증이 fail-closed인지 코드 경로와 관련 시험으로 확인한다. 이미 충족한 시험이 있으면 연결만 한다.

이 보완은 사용자가 요청한 1~3단계 범위에 포함된다. 추가 독립 리뷰 승인이나 LIVE 승인을 요구하며 시험을 건너뛰지 않는다. 이미 PASS인 복사·백업·nonce 단독 시험은 새 근거 없이 반복하지 않는다.

## 패키지·시험 보존

- ZIP: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33_intent_wired_candidate.zip`
- SHA-256 (Windows 보고): `4dc3c701a83c22b2615e244a9dfeca8bd07ef89e9456c1b182a7ec3c01293cda`
- 크기/항목: 297249 B / 109
- 트리 SHA-256 (Windows 보고): `ab80c9f7d9c163a5d130076e7c0d502891cabb4e6248d958073b83ef7da8103c`
- 기존 ZIP·기존 리뷰/영수증 불변. 고정 ZIP 그대로 외부 시험하는 경우 그 입력 SHA를 기록한다. 코드/시험을 ZIP에 반영하여 bytes가 달라지면 기존 ZIP을 보존하고 새 후보 revision·SHA로 고정한다.
- 변경 관련 시험 후 최종 변경이 있으면 그 최종 후보에서 전체 회귀 1회. 실패/변경/미해결 우려가 없는 기존 전체 회귀를 단순 보고 재게시 때문에 반복하지 않는다. 기존 12 SKIP 사유와 실제 명령·로그·빌드/입력 SHA·PID·시점을 연결한다.

## CURRENT·TRACKER 보완

기존 TRACKER는 phase만 v0.2.33으로 바뀌고 self_test/next_action은 v0.2.32 또는 실행 전 상태였다. 이번 판정에서 self_test를 v0.2.33 보고에 맞추고 next_action을 위 남은 시험으로 정렬한다. 기존 아키텍처 리뷰 이력은 보존한다. CURRENT의 “다음은 사용자 운영 승인” 항목보다 이 최신 판정을 우선한다.

## 운영·승인 경계

- 새 테이블 `review_intent_nonces`는 후보/temp DB만 검증됨. 운영 적용 시 생기는 DB 이행은 별도 운영 승인 대상이며 아직 수행하지 않는다.
- 과거 DB 복원 금지 및 최신 처리/청구/UNCERTAIN/claim/알림 이력 보존 유지. v0.2.29 트리 백업 생성은 사본에서의 무손실 복원과 호스트 SHADOW 완료를 자동 의미하지 않는다.
- 독립 리뷰용 보호 승인·정확한 코드 입력 전달 허용, 운영 DB/필요 보호 설정 변경, 실제 호스트 SHADOW 준비, 10단계 비용 위험 수용·LIVE 최종 확인은 개발 시험 완료와 별도다.
- 이번 GPT의 reviewer 모델 호출·REQUEST/READY·서명·운영 DB/키/정책/Task/Notifier/LIVE 변경은 0. 이 판정 게시는 Windows 자동 실행이나 보호 승인이 아니다.

**NEXT_ONE_ACTION:** Windows 기존 Work에서 고정 v0.2.33 후보를 재사용하여 위 두 필수 시험 및 재검증 경계 확인을 끝내고 같은 결과 문서에 근거를 추가한다. 결과·CURRENT·TRACKER main 원격 검증 후 GPT가 3단계 완료 여부를 재판정한다.
