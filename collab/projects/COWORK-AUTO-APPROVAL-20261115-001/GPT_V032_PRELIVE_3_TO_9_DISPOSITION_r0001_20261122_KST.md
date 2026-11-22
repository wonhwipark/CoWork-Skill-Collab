# v0.2.32 LIVE 직전 3~9단계 — GPT 판정

- 판정일: 2026-11-22 KST
- 저장소/브랜치: `wonhwipark/CoWork-Skill-Collab/main`
- Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 기준 HEAD: `d080d1c4c5bacad01c6627af9203323e1878e800`
- 실행 지시: [3~9단계 원샷 인계](WINDOWS_V031_TO_LIVE_PRECHECK_ONE_SHOT_HANDOFF_r0001_20261122_KST.md)
- 원본 결과: [Windows v0.2.32 결과](CLAUDE_V032_PRELIVE_3_TO_9_RESULT_FOR_GPT_20261122.md), Git blob `a67514698aa42a34de4b48154714b838127565e0`
- **GPT_DISPOSITION=ACCEPT_DEVELOPMENT_WITH_CORRECTIONS**
- **LIVE_READY=NO / LIVE_CUTOVER=HOLD / development_not_for_deployment**

## 1. 확인 범위

GPT가 CURRENT, 실행 지시서, Windows 결과 본문과 원본 Git blob, v0.2.31 판정, START_HERE 및 자료 전달 계약을 직접 조회했다. Windows 개발·시험은 기존 수행 결과를 재사용했으며 재실행하지 않았다. v0.2.32 ZIP·소스·전체 시험 로그는 이번 환경에 없고 Windows 호스트 실행 수단도 노출되지 않았다. 따라서 아래 PASS는 Windows 자체시험 보고 범위이며 GPT 직접 시험 또는 독립 리뷰 PASS가 아니다.

저장소 실제 visibility는 PUBLIC이다. 신규 게시물은 비민감 판정·상태 문서뿐이며 코드 ZIP, 자격정보, 운영 백업을 게시하지 않는다. 기존 요청·READY·리뷰 결과·영수증은 변경하지 않는다.

## 2. 단계별 판정

| 단계 | 결과 | 인정 범위와 남은 조건 |
|---|---|---|
| G3 동시 경합 | PASS (HOST_REPORTED, 모의 전송) | 서로 다른 DB/barrier, runner 합계 1, 5회 반복 보고 수용. 원격 create-only는 잠금으로 모사했으므로 실제 GitHub 경쟁 E2E PASS로 확대하지 않음. 서로 다른 OS 프로세스 사용 여부는 게시된 요약만으로 확인 불가 |
| G4 종료·재시작·복구 | PASS (HOST_REPORTED) | crash 봉인, timeout/신호/exit 1, 게시만 재시도, 구 필드 호환 보고 수용. 원시 명령·로그·전체 빌드 SHA·12 SKIP 사유는 이번 결과에 없음 |
| G5 SCOPE 설계 | PASS (조건부 설계 수용) | 정확한 입력·skill·만료·nonce·서명 목적 바인딩, GitHub 승인 주장 불인정 방향 수용. 실제 신뢰 주체·nonce 소비와 재시작 시 보존은 코드/통합 시험으로 확인 필요 |
| G6 SCOPE 격리 검증기 | PASS (HOST_REPORTED, 격리 함수만) | review_intent.py 및 25건 시험 보고 수용 |
| G6 승인 경로 통합·활성화 | NOT_RUN / BLOCKED | assess 미연결. 새 키 생성 승인만으로 구현 완료가 되지 않음. 운영 연결·키·trust root 변경은 현재 금지 범위 |
| G7 회귀·패키지 | PASS (HOST_REPORTED) | 994 PASS / 0 FAIL / 12 SKIP, ZIP 검사 보고 수용. GPT ZIP 실물 SHA/CRC 및 독립 바이트 검증 NOT_RUN |
| G8 독립 리뷰 | NOT_RUN / BLOCKED_AUTH | 이 후보에 대한 유효 보호 승인·고정 입력·결과·영수증 미확인. 기존 R1을 신규 34개 시험/변경의 독립 리뷰로 승격하지 않음 |
| G9 DB 사본 SHADOW | PASS (HOST_REPORTED, 사본 한정) | dispatch 0, 모델 0, 라이브 감사 최대 id 22803→22803 보고 수용 |
| G9 호스트 실운영 SHADOW | NOT_RUN | 설치·Task 추가 미승인. 사본 결과로 대체 PASS 금지 |
| 백업·복원 | PASS (HOST_REPORTED, DB·설정·위임 한정) | integrity ok/작업 12 보고 수용. 설치 트리 백업 NOT_RUN(호스트 보고 NOT_DONE, 권한 거부) |
| 결과·CURRENT 게시 | PASS (GPT 직접 원격 조회) | 기존 결과·CURRENT 실재 및 내용 확인. 본 판정·CURRENT·TRACKER 게시와 원격 바이트 검증은 게시 후 실행 기록으로 확인 |

## 3. 수정 수용 및 보완 조건

1. **G3 증거를 정확히 한정:** 모의 경쟁 검증은 개발 후보 근거로 수용한다. 단 실제 GitHub 원자성과 서로 다른 OS 프로세스 경합은 현재 원문으로 입증되지 않는다. 이미 있는 명령·로그·PID 증거를 우선 연결하고, 존재하지 않는 항목만 NOT_RUN으로 남긴다. 증거 보완만을 위해 전체 회귀나 기존 리뷰를 반복하지 않는다.
2. **응답 유실 후 재진입:** 같은 DB에서 ALREADY_OURS가 나온 사실만으로 재디스패치를 일반 허용해서는 안 된다. 첫 시도가 모델 시작 전에 끝났다는 지속 상태 증거가 있어야 한다. 시작 여부 불명/재시작/다른 DB는 봉인한다. 현재 보고의 생애주기 1회 결과를 해당 시험 범위로 수용하며 실제 코드 경계는 독립 리뷰 대상이다.
3. **SCOPE는 키 승인과 구현을 분리:** 현 후보는 검증 함수만 존재하고 승인 경로는 미연결이다. 같은 후보를 키만 설치해 SCOPE 완료로 보고하지 않는다. 기존 signer/trust root 재사용 가능성부터 확인하며 새 키를 모든 대안의 필수 조건으로 고정하지 않는다. 격리 통합 개발은 기존 사용자 범위지만 원본 접근 불가로 이번 GPT 실행은 BLOCKED_SOURCE_ACCESS. 코드 수정 시 기존 ZIP을 보존하고 새 후보 revision·관련 시험·새 SHA로 고정한다.
4. **PUBLIC 게시 차단 사유 정밀화:** START_HERE는 허용된 CoWork 자체 소스/후보 게시를 인정하는 문구와 과거 PRIVATE 제한을 함께 보존한다. 따라서 PUBLIC이라는 이유만으로 모든 CoWork 코드 게시가 영구 금지라고 일반화하지 않는다. 이번 정확한 후보의 내용·반출 허용 범위 및 실제 bytes는 검증되지 않았으므로 업로드하지 않는다. 자료 게시 허용과 보호 리뷰 실행 승인은 별개이며 후자는 여전히 미충족이다.
5. **백업은 승인과 권한을 구분:** 사용자 지시에는 읽기 전용 백업/롤백 준비 검증이 포함되어 있다. 설치 트리 사본 미생성의 직접 원인은 Windows가 보고한 권한 거부다. 문구상의 재승인만으로 해결됐다고 보지 않는다. 기존 거부 동작을 우회하지 않으며 허용 경로·실제 거부 사유를 호스트에서 확인해야 한다. Task 중지·설정/DB 변경은 현재 금지다.
6. **롤백 이력 보존 보완:** 원문의 옛 DB 번들 교체 초안만으로 무손실 복원을 승인하지 않는다. 백업 이후 처리/청구/UNCERTAIN/원격 claim/알림 watermark가 생겼다면 과거 DB로 되돌려 이력을 잃을 수 있다. 컷오버 시점의 일관된 DB/WAL/SHM 보존과 스키마 호환을 먼저 판단하고, 코드 복원 시 현재 원장 유지 가능성 또는 승인된 무손실 복구 방법을 명시해야 한다. 이번에는 DB 교체/이행/Task 조작 0.
7. **시험 증거 보완:** 기존 로그에서 TEST_ID/ENV/BUILD_SHA/INPUT_SHA/COMMAND/OBSERVED/RESULT/EVIDENCE/EXECUTOR/UTC 및 12 SKIP 사유를 연결한다. 보고 누락은 시험 실패 확정이 아니지만 LIVE 검증 완료 근거로도 쓰지 않는다.
8. **LIVE 카운터:** Windows가 보고한 v0.2.29 Running 및 R1에 따른 dispatch 2→3, model_calls_new 4→6 설명은 호스트 보고로 보존한다. 원시 영수증/감사 대조 없이 GPT 독립 검증으로 승격하지 않는다. 이번 GPT 세션의 reviewer 모델 호출·디스패치·Telegram·운영 변경은 모두 0이다.

## 4. 고정 패키지

- Windows 경로: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_32_live_precheck_candidate.zip`
- SHA-256 (Windows 보고): `cbf95d1141cbed6973d6cace2950065b4ed5eb36e988ecf522a9fc3ab087fa94`
- 크기/항목: 295,885 B / 106
- 트리 SHA-256 (Windows 보고): `644eaf61e33c1430fa7d90b18df9d5cc28eacf24f955c5acb916a2e9d253e9cd`
- 새 후보 생성/기존 ZIP 수정: 이번 GPT 세션 0
- 이전 v0.2.30/v0.2.31 ZIP 및 모든 기존 영수증 보존

## 5. 남은 실행 조건과 승인

| 구분 | 필요한 것 |
|---|---|
| 기존 범위 내 후속 개발·증거 | 정확한 v0.2.32 원본 접근, 기존 로그·SKIP 사유 연결, 격리 SCOPE 통합, 설치 트리 백업 권한 원인 확인, 무손실 롤백 보완. 자동 전체 재시험·기존 리뷰 재실행 금지 |
| 독립 리뷰 1회 | 최종 고정 후보 실제 bytes 검증/전달 허용 및 유효한 보호 승인 확인. REQUEST/ZIP Commit A→PIN B→보호 서명/READY 마지막→1회 디스패치. 부재 시 모델 0 |
| 운영 변경이 필요한 경우 | 최종 채택된 SCOPE 보호 설정/키 변경과 호스트 SHADOW 설치·Task 변경의 구체적 범위 승인. 이번에는 미실행 |
| 10단계 | 선행 보완·독립 리뷰·SHADOW/복원 검증 후 GPT 재판정, 비용 무상한 위험 수용 및 사용자 LIVE 최종 확인. 현재 승인 요청으로 합격 게이트를 대체하지 않음 |

**NEXT_ONE_ACTION:** Windows 기존 Work에서 같은 v0.2.32 원본·기존 로그를 재사용해 §3의 증거/격리 통합/무손실 복구 보완을 진행하고, 유효 보호 승인 없이는 독립 리뷰·READY·LIVE를 실행하지 않는다. 이번 GPT는 호스트에 명령·메시지를 전송하지 않았고 문서 게시를 자동 실행으로 보고하지 않는다.
