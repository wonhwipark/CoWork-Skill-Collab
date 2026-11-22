# v0.2.33 — 기존 1~3단계의 남은 시험만 원샷 재개

저장소: wonhwipark/CoWork-Skill-Collab
브랜치: main
Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
범위: 사용자 “3단계까지 원샷으로 진행해줘”의 미완료 보완. 같은 범위 승인 반복 질문 없음.
최신 판정: GPT_V033_PARTIAL_ACCEPTANCE_AND_REMAINING_TESTS_r0001_20261122_KST.md
근거: CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md §9.
1-A/B 복사·v0.2.29 트리 백업은 PASS 보고됨. 이 작업을 처음부터 다시 하지 않는다.

## 고정 입력
후보 폴더: D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33
ZIP: D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33_intent_wired_candidate.zip
SHA-256: 4dc3c701a83c22b2615e244a9dfeca8bd07ef89e9456c1b182a7ec3c01293cda
297249 B/109항목. 실물·폴더 대응 확인 후 재사용. 기존 ZIP·리뷰·영수증 보존.
기존 전체 회귀는 1007 PASS/0 FAIL/12 SKIP의 자체시험 보고. 새 시험 PASS로 재사용하지 않는다.

## 이번에 끝낼 것
1. 별도 OS 프로세스 watcher 두 개·서로 다른 temp DB·동일 ID/revision/PIN/ZIP으로 모두 실제 디스패치 claim 직전 barrier에 도달시킨다. 프로세스 간 공유되는 원자적 fake claim 저장소, 서로 다른 PID와 두 도달 이벤트를 기록한다. fake runner 합계 1 이하, 패자/재스캔 추가 호출 0. nonce 소비만 경쟁하거나 두 스레드만 사용하는 것으로 대체하지 않는다. 실제 GitHub 쓰기 경쟁은 NOT_RUN 유지.
2. 의도 검증→nonce 소비→상태 보존→재검증→서명/READY→claim의 통합 경로를 실제 후보 코드와 fake signer/transport/runner로 실행한다. nonce 소비 후·claim 후 프로세스 중단과 새 프로세스 재기동을 주입한다. 같은 요청 replay, 다른 revision/SHA, 모델 시작 여부 불명에서 권한 확대/추가 디스패치 0을 확인한다. nonce 저장소 단독 재시작으로 대체하지 않는다.
3. _revalidate의 nonce 소비 기록이 현재 권한·만료/키 해지·정확한 revision/commit/입력 바인딩을 대체하지 않는지 코드 경로·관련 시험을 확인한다. 최초 검증 후 만료/해지/입력 변경도 fail-closed. 기존 시험이 있으면 연결만 한다. source 미접근 단계는 결함 확정 없이 NOT_RUN으로 기록한다.
기존 스킬·API·시험을 재사용해 관련 실패만 최소 수정한다. test key/temp DB/모의 전송만 사용한다. 운영 DB의 테이블 생성·이행은 수행하지 않는다.

## 후보·회귀
기존 ZIP 그대로 검증하는 경우 입력 SHA 고정. 코드/시험을 ZIP에 반영하여 bytes가 바뀌면 구 ZIP 보존·새 후보 revision 발행·관련 시험·최종 전체 회귀 1회·새 SHA/크기/트리 SHA/CRC/중복/경로/링크/민감정보 검사. 최종 변경/실패/미해결 우려가 없으면 기존 전체 회귀를 게시만을 위해 반복하지 않는다. 12 SKIP 사유·명령/로그/빌드·입력 SHA/PID/시점을 연결한다.
코드 ZIP과 운영 백업은 공개 게시하지 않는다.

## 기록·종료
같은 CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md에 새 절로 추가하고 과거 §9를 보존한다. CURRENT·TRACKER self_test/next_action을 실제 결과와 맞춰 main 직접 게시·commit/원격 bytes SHA 확인.
독립 리뷰/REQUEST/READY/실제 모델 호출/Telegram/LIVE 설치·정책·키·운영 DB·Task/Notifier 변경 0. 호스트 SHADOW 설치도 이번 범위 밖. LIVE_READY=NO 유지.
도구 차단 시 원문과 정확한 필요 범위 기록·우회 금지. 새 승인 요청 때문에 이미 허용된 시험을 중단하지 말고 가능한 범위 끝까지 수행한다.
