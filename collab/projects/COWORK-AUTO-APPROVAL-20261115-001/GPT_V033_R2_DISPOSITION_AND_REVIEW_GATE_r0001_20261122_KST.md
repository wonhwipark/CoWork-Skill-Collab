# v0.2.33 r2 — GPT 개발 후보 판정·정정·리뷰 진입

- 판정일: 2026-11-22 KST
- 저장소/브랜치: wonhwipark/CoWork-Skill-Collab/main
- Work: COWORK-AUTO-APPROVAL-20261115-001
- 기준 HEAD: f49c418dfa09e5ad3df1c90da8c5e7698c134d23
- 원본: [Windows 결과 §10](CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md), Git blob `37fa21fda8b87a84951a30d8b74c56773a65c25d`
- 사용자 최신 정정: SHADOW 감사 행 증가를 watcher 기록으로 설명한 문구는 스크립트의 상수 출력이며 실제 귀속 확인이 아님.
- **GPT_DISPOSITION=ACCEPT_DEVELOPMENT_CANDIDATE / INDEPENDENT_REVIEW=NOT_RUN / LIVE_READY=NO**

## 1. 수용 범위

GPT는 원격 결과·CURRENT·TRACKER를 대조했다. Windows ZIP·소스·원시 시험 로그는 GPT가 직접 검사하지 않았다. 아래 PASS는 개발자 자체시험/호스트 보고 수용이며 독립 리뷰·운영 E2E PASS가 아니다.

| 항목 | 판정 | 범위 |
|---|---|---|
| 후보 복사·v0.2.29 트리 백업 | PASS (HOST_REPORTED, 이전 완료) | 복사 거부 해소·143개 백업을 재사용 |
| 두 프로세스 디스패치 경합 | PASS (HOST_REPORTED) | 다른 PID/다른 DB/barrier, 공유 O_EXCL 디스패치 기록, 모델 합계 1·패자 UNCERTAIN |
| 모델 진입 후 강제 종료·새 프로세스 재기동 | PASS (HOST_REPORTED) | 재기동 봉인, 추가 모델 0 |
| nonce 저장소 재시작·프로세스 경쟁 | PASS (HOST_REPORTED) | 재사용 거부, 소비자 1 |
| 재검증 보완 | PASS (보고한 사례 한정) | 신뢰 루트 전달 경로 수정, 키 해지·위임 비활성·미소비 nonce 거부, rev1 의도로 rev2 승인 거부 |
| 회귀·r2 패키지 | PASS (HOST_REPORTED) | 1014 PASS/0 FAIL/12 SKIP; GUI 옵트인 8, Windows .venv 조건 스크립트 4 |
| 사본 SHADOW | PASS (HOST_REPORTED, 사본 동작 한정) | dispatch 0/모델 0/대기 8. 라이브 감사 행 증가 귀속은 미확인 |
| 백업 DB 사본 리허설 | PASS (HOST_REPORTED, 사본 한정) | 백업 불변·integrity ok·작업 12/12/claim 5/감사 22804 유지, nonce 테이블 사본 생성·반복 적용 |
| 실제 GitHub 경쟁 | NOT_RUN | 기존 쓰기 금지 유지 |
| 설치/Task 기반 호스트 SHADOW | NOT_RUN | 별도 설치 미승인 |
| 독립 리뷰 / 운영 DB 이행 / LIVE | NOT_RUN | 아래 게이트 미충족 |

이전 GPT 판정의 프로세스 디스패치 경합 미실증 사유는 §10의 새 개발 증거로 해소한다. 새 프로세스 재기동 결과도 보고한 시점·경로에서 수용한다. 보고되지 않은 중단 지점이나 모든 보안 조건까지 PASS로 확대하지 않는다. 현재 동일 전체 회귀·완료 백업을 반복하도록 지시하지 않으며 다음 진입은 고정 r2 코드에 대한 독립 리뷰다.

## 2. 감사 귀속 정정 — 수정 수용

- §10.4의 감사 최대 id `23349→23350`과 그 증가 원인 설명을 구분한다. 사용자 정정은 **증가 원인을 watcher에 귀속한 설명**에 적용한다.
- 스크립트에 상수로 찍히는 “watcher 기록” 문구는 실제 프로세스·요청·감사 레코드 대조 증거가 아니다. **LIVE_AUDIT_DELTA_CAUSE=UNVERIFIED**로 정정한다.
- 이 문구로 SHADOW의 운영 DB 무쓰기를 입증했다고 주장하지 않는다. 사본의 읽기 전용 URI·쓰기 차단·모델 차단 보고는 해당 사본 시험 범위로만 인정한다.
- 현재 라이브 DB 전체의 변화, 라이브 watcher의 통상 감사 기록, 해당 시험이 발생시킨 기록은 별도다. 원시 대조 없는 귀속은 추가 추정하지 않는다. 기존 원문·과거 보고는 보존하며 이 정정이 최신이다.

## 3. 롤백 계획 보완 — nonce 이력 보존

Windows §10.4의 “롤백은 테이블 삭제 또는 구 코드 복원” 중 **운영 nonce 테이블 삭제를 일반 롤백으로 채택하지 않는다**. 운영 적용 후 소비 이력을 삭제하면 replay 방지 상태·감사 이력을 잃을 수 있다.

기본 계획은 현재 DB와 nonce 소비 이력을 보존한 채 호환되는 구 코드만 복원하는 방식이다. 구 코드의 추가 테이블 무시는 현재 호스트 보고이며 실제 적용 전 사본 호환 근거를 확인한다. 비호환이면 임의 DROP/과거 DB 교체 없이 복구 보류와 별도 승인된 무손실 이행을 따른다. 사본 리허설 결과를 운영 이행·복원 실행으로 보고하지 않는다. 이번에 운영 DB/테이블을 변경한 사실은 없다.

## 4. 고정 리뷰 대상·정확한 게시 확인 범위

- 파일: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33_r2_intent_wired_candidate.zip`
- SHA-256 (Windows 보고): `23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206`
- 크기/항목: 301136 B / 111
- 트리 SHA-256 (Windows 보고): `e4ecdc4c9d141ec76be922410dcd0ea1eb8e3598c6df01a80908ccfadf4cd0e0`
- 제안 게시 위치(아직 NOT_POSTED): `wonhwipark/CoWork-Skill-Collab/main/collab/packages/v0_2_33_r2_intent_wired_candidate.zip`
- 범위: CoWork 감시기 자체 코드·시험의 위 정확한 바이트만. 회사 제한 자료·키·토큰·운영 DB/백업은 제외하며 검사에 실패한 bytes는 게시하지 않는다. L1Work 배포·호스트 설치로 확대하지 않는다.

`collab/START_HERE.md`에는 허용된 CoWork 감시기 소스/후보의 PUBLIC 게시 문구와 미승인 후보 PRIVATE 리뷰 제한 문구가 함께 있고, 연결된 11/14 계약도 PRIVATE를 지정한다. 따라서 이번 정확한 r2 ZIP을 PUBLIC CoWork에 게시해도 되는지 **구체적 자료 전달 범위 확인**을 남긴다. 어느 한 문구만으로 전체 코드 공개 허용 또는 영구 공개 금지를 일반화하지 않는다. 이번 GPT는 자료를 공개 게시하거나 사용자 결정을 대신 발급하지 않는다.

## 5. 독립 리뷰 처리 — 요청 게시와 보호 실행을 분리

- 사용자는 기술 마무리 묶음의 독립 리뷰 1회를 이미 요청했다. 같은 리뷰 의도·비용 승인을 반복 요청하지 않는다. 다만 이 의도가 실제 보호 signer 서명·위임 검증을 대체하지 않는다.
- 현재 후보의 정식 요청/ZIP/PIN은 미게시다. **FORMAL_REQUEST=NOT_POSTED**와 **PROTECTED_AUTH=NOT_VERIFIED_FOR_CANDIDATE**를 분리한다. 기존 아키텍처 R1 완료로 후보 리뷰를 대체하지 않는다.
- 정확한 입력 전달이 허용되면 Windows에서 실물 SHA/CRC·민감정보·기존 요청/결과/UNCERTAIN을 검증하여 기존 `collab/ops/submit_review_request.py` 및 PRE_READY 계약으로 REQUEST+ZIP Commit A→원격 검증→PIN Commit B→원격 검증까지 수행한다. Windows 보호 승인 유무를 REQUEST 출판의 일괄 사전 차단 조건으로 되돌리지 않는다.
- 실제 signer/watcher의 승인·위임·만료·원본·중복 게이트를 통과한 경우에만 보호 서명·READY 마지막·독립 리뷰 1회 실행. 유효 권한이 없으면 해당 경계에서 BLOCKED_AUTH·모델 0. 정책/키/skill 명의를 바꿔 우회하지 않는다.
- 리뷰 범위: 프로세스 claim·불확실 후 무재실행, nonce 원자성·재시작·정확한 원본 바인딩, 재검증 시 만료/해지/권한, 실제 보호 키·운영 설정 호환, additive schema·이력 보존/롤백, 후보 코드와 시험의 일치. 이는 코드 리뷰 초점이며 미검증 결함 확정이 아니다.
- GPT가 실제 고정 입력·결과·영수증을 읽은 뒤에만 독립 리뷰 판정. 모델/분석 재실행으로 게시 실패를 복구하지 않는다.

## 6. 남은 두 묶음

1. 기술 마무리의 남은 독립 리뷰: 정확한 r2 PUBLIC 전달 범위 확인→정식 A/B→실제 보호 승인→1회 리뷰→결과/영수증 확인. 기존 개발·시험·백업 반복 없음.
2. 리뷰 및 실제 준비 근거를 GPT가 판정한 뒤 최종 운영 결정: 필요한 DB 이행/보호 설정·호스트 SHADOW 준비 범위, 비용 무상한 위험 수용, LIVE 컷오버를 한 번에 사용자에게 확인. 이번에는 미실행이며 설치 SHADOW 미수행도 숨기지 않는다.

**NEXT_ONE_ACTION:** 위 r2 ZIP 한 건의 PUBLIC 게시 범위를 확인하고, 허용될 때 기존 Windows 보호 경로로 정식 리뷰 접수·1회 실행까지 이어간다. GPT는 Windows 원본/실행 연결이 없어 직접 ZIP 검사·요청 게시·리뷰 호출을 실행하지 않았음. LIVE_READY=NO.
