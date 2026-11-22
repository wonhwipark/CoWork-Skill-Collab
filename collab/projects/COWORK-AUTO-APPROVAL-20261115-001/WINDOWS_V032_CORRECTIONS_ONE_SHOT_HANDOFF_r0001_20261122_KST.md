# v0.2.32 후속 보완 — Windows 원샷 실행 지시

저장소: wonhwipark/CoWork-Skill-Collab
브랜치: main
기존 Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
사용자 지시: GPT 판정 후 “진행”. 격리 보완·시험·비민감 결과 게시를 계속하며 10단계 LIVE 승인은 제외.

## 시작과 입력 고정
CURRENT.md, GPT_V032_PRELIVE_3_TO_9_DISPOSITION_r0001_20261122_KST.md, CLAUDE_V032_PRELIVE_3_TO_9_RESULT_FOR_GPT_20261122.md 순으로 읽는다.
원본 폴더: D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_32_live_precheck
원본 ZIP: D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_32_live_precheck_candidate.zip
SHA-256: cbf95d1141cbed6973d6cace2950065b4ed5eb36e988ecf522a9fc3ab087fa94
크기 295885 B/106항목. 실물 SHA/CRC·폴더 대응 확인 후 재사용한다. 불일치 시 해당 소스 보완만 BLOCKED, 다른 읽기 전용 준비는 계속한다. v0.2.29 LIVE 및 구 ZIP 불변.

## 하나의 세션에서 수행
1. 기존 시험 로그·명령·빌드/입력 SHA·UTC·12 SKIP 사유를 연결한다. G3의 별도 OS 프로세스/PID 증거와 모의 전송 범위를 확인한다. 이미 유효한 시험·기존 리뷰를 증거 재게시 때문에 재실행하지 않는다. OS 프로세스 증거가 없으면 기존 race 시험을 재사용하여 별도 프로세스/DB 격리 시험만 추가하고 mock 모델 합계 1 이하를 확인한다. 실제 GitHub 경합은 이번에 쓰기 시험을 추가하지 말고 NOT_RUN을 유지한다.
2. 기존 signer·assess·review_intent·DB/nonce API를 읽고 REUSE→CONNECT한다. 운영 자격 없이 격리 사본에서 의도 검증을 승인 경로에 연결한다. 서명 검증→정확한 repo/request/revision/skill/commit/SHA·크기/만료 확인→기존 nonce 소비·재사용 차단→READY 순서→원격 claim 순서를 보존한다. 원자적 nonce 보존 수단이 없으면 격리 개발로 최소 보완하되 운영 DB 이행 0. 기존 정책으로 유효한 요청의 동작은 보존한다. 신뢰 키가 없거나 목적이 맞지 않으면 fail-closed; test key만 임시 격리 공간에서 사용한다.
3. valid exact intent, 위조/만료/변조/replay/동시 nonce/재시작 후 replay/revoked/wrong skill·repo/소급 요청/GitHub 승인 주장, 모델 시작 불명 재시작을 시험한다. 모델 시작 여부를 지속 증거로 확증할 수 없는 ALREADY_OURS는 봉인한다. fake runner·temp DB만 사용한다.
4. 설치 트리 백업 거부의 원문·경로·계정·권한 계층을 비밀 없이 확인한다. 기존 승인된 읽기 전용 복사 수단과 허용 경로로 해결 가능할 때만 수행한다. 동일 거부 동작을 다른 수단으로 우회하거나 권한·Task를 바꾸지 않는다. 거부 시 BLOCKED_PERMISSION과 정확한 필요 권한만 기록한다.
5. 롤백은 기존 LIVE_ENABLE_EXECUTION_REQUEST_V029_20261120_KST.md §4와 CLAUDE_V029_LIVE_BACKUP_BUNDLE_RESULT_FOR_GPT_20261120.md를 재사용한다. 백업 이후 완료/실패/UNCERTAIN/claim/회계/알림 이력이 있거나 유무가 불명하면 과거 DB로 교체하지 않는다. 코드 복원 시 현재 DB·schema 호환을 확인하고 불명/비호환이면 복구 BLOCKED로 보존한다. 사본에서 최신 이력이 유지되고 과거 요청/알림 재실행 0인지 검증한다. 운영 DB 복원·정지·이행은 수행하지 않는다.
6. 코드 변경 시 충돌 없는 차기 후보(예: v0.2.33)를 만들고 변경 관련 시험 후 최종 통합 회귀를 1회 수행한다. 실패한 관련 부분만 보완한다. 구 ZIP 보존, 새 ZIP SHA/크기/CRC/경로·링크·민감정보/트리 SHA를 기록한다.
7. 최종 후보 독립 리뷰는 기존 요청·영수증·UNCERTAIN 중복 및 실제 보호 승인·전달 허용을 확인한 경우에만 1회 수행한다. 없으면 REQUEST/READY/서명·모델 호출 없이 BLOCKED_AUTH. 기존 R1 재실행 금지. 키·trust root·위임·LIVE 설정을 새로 활성화하지 않는다.
8. 가능한 기존 읽기 전용 SHADOW만 수행한다. 설치/Task 변경이 필요하면 NOT_RUN. 운영 DB·GitHub 업무 레코드·Telegram 쓰기 0, LIVE provider 1개 유지. 결과 문서·CURRENT 게시만 별도 허용한다.

## 완료·게시
같은 Work의 CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md에 수행/미수행·실제 명령/근거·단계별 PASS/FAIL/SKIP/NOT_RUN, 원본/최종 ZIP SHA, 리뷰 ID·결과·영수증 또는 차단, 백업/복구·운영 전후 상태를 적는다. CURRENT와 기존 TRACKER 현행 필드만 맞추고 main에 직접 게시하여 commit·원격 bytes SHA를 확인한다.
회사 제한 자료·자격정보·운영 DB/백업은 게시 금지. 정확한 최종 ZIP 공개 허용을 검증하지 못하면 로컬 보존한다.
10단계 비용 위험 수용·LIVE 설치·정책/키/DB/Task/Notifier 변경은 이번 지시에 포함되지 않는다. 중간 질문 없이 가능한 범위를 끝내고 차단 항목만 분리한다.
