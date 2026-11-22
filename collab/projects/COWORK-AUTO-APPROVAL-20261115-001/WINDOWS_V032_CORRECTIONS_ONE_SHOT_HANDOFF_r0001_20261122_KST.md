# v0.2.32 후속 보완 — 최신 실행 범위 1~3

저장소: wonhwipark/CoWork-Skill-Collab
브랜치: main
Work: collab/projects/COWORK-AUTO-APPROVAL-20261115-001/
2026-11-22 KST 사용자 최신 지시: “3단계까지 원샷으로 진행해줘”.
이는 직전 남은 조치 표의 ①복사 차단 해소 ②격리 SCOPE 연결 ③누락 시험·회귀·v0.2.33 패키징을 뜻한다. 기존 본문의 독립 리뷰·호스트 SHADOW·운영 활성화까지 확대하지 않는다.
이전 지시서는 Git commit 0a1d72042779a292ee0f558349961e3eb178e3e6의 같은 경로로 보존한다.

## 0. 재개
CURRENT.md와 CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md를 읽고 이미 한 작업·기존 로그를 재사용한다.
원본 폴더: D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_32_live_precheck
ZIP: 위 candidates 아래 v0_2_32_live_precheck_candidate.zip
기준 SHA-256: cbf95d1141cbed6973d6cace2950065b4ed5eb36e988ecf522a9fc3ab087fa94
295885 B/106항목. 실물 SHA/CRC와 폴더 대응 확인. 구 ZIP 불변.

## 1. 두 복사 작업
사용자는 다음 두 작업의 실행을 이번 요청 범위에 포함했다. 같은 작업 범위 승인을 반복 질문하지 않는다.
A. 원본 후보 폴더 → D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_33
B. D:\User\whpark\skill-collab-watcher-github (현재 v0.2.29 설치 트리 읽기) → D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_29_precheck_20261122\install_tree_v0_2_29
대상이 이미 있으면 출처·완전성을 검증해 재개하고 무조건 덮어쓰지 않는다. B는 원본 읽기·백업 경로 쓰기이며 LIVE 원본 수정/정지/재시작이 아니다.
이 지시가 도구 권한 시스템의 허용 결정을 대신하지 않는다. 최신 사용자 요청으로 기존 정식 권한 경로에서 해당 두 작업을 재평가한다. 거부가 지속되면 실제 명령·비밀 제외한 거부 원문·차단 계층·필요 허용 범위를 기록하고 해당 항목만 BLOCKED_PERMISSION. 다른 셸/도구로 거부를 우회하거나 포괄 권한/ACL/보안 설정을 변경하지 않는다. A/B가 독립적으로 가능하면 가능한 쪽은 계속한다.
백업은 전체 설치 트리 SHA/파일 수/매니페스트와 원본 전후 불변을 확인한다. DB·위임·키 사본은 GitHub에 게시하지 않는다. 옛 v0.2.25 번들을 v0.2.29 백업으로 취급하지 않는다.

## 2. 격리 SCOPE 통합
v0.2.33 후보에서 기존 signer/assess/review_intent/StateStore를 조사하고 REUSE→CONNECT한다. 정확한 repo/request/revision/skill/commit/REQUEST·ZIP SHA·크기/만료/서명 목적을 검증한 의도만 승인 경로에 연결한다.
nonce는 재시작·동시 프로세스에서도 한 번만 소비되도록 기존 저장·트랜잭션 경계를 우선 재사용한다. 새 테이블이 실제로 필요하면 후보 코드와 temp DB에서만 구현·시험하고 운영 이행 요구를 기록한다. 운영 DB 테이블 추가는 이번 범위 밖이다.
위조/해지/만료/입력 불일치/소급·미승인 요청/GitHub 본문 승인 주장은 fail-closed. 기존 유효 요청 호환, 보호 서명→READY→원격 claim 순서 보존. test key는 격리 임시 공간만 사용한다.

## 3. 누락 시험·최종 패키지
- 별도 OS 프로세스·서로 다른 DB·barrier로 같은 요청 경합. 프로세스 간 공유되는 원자적 모의 claim 저장소 사용, PID/명령/증거 기록, fake runner 합계 1 이하. 실제 GitHub 쓰기 경쟁 시험은 NOT_RUN 유지.
- nonce: 같은 저장소의 재시작 후 replay 거부, 동시 소비 성공 1 이하, 소급 요청 거부, 통합 경로에서 위조·변조·만료·해지·wrong skill/repo 거부.
- 모델 시작 여부 불명 CLAIMED/RUNNING/ALREADY_OURS는 봉인, 자동 재디스패치 0. 결과 게시 실패는 게시만 재시도.
기존 로그·12 SKIP 사유를 우선 연결하고 새/변경 관련 시험 후 최종 후보 전체 회귀를 1회 실행한다. 실패 시 관련 수정·재시험. fake runner·temp DB만 사용한다.
v0.2.33 ZIP 새 생성: CRC/중복/경로 이탈/링크/필수 파일·민감정보/크기/전체 SHA-256/트리 SHA 확인. 코드 ZIP은 로컬 보존하고 공개 배포하지 않는다. 실패 후보는 development_not_for_deployment.

## 결과·종료
같은 Work의 CLAUDE_V032_CORRECTIONS_ONE_SHOT_RESULT_FOR_GPT_20261122.md에 후속 실행 시각·명령·원본/최종 SHA·1~3별 PASS/FAIL/SKIP/NOT_RUN·차단 사유를 추가하고 이전 이력을 보존한다. CURRENT와 TRACKER 현행 필드를 맞춰 main에 직접 게시, commit·원격 bytes SHA 확인.
실행 중 프로세스는 watcher/Notifier를 실제 명령·Task로 구별하여 중복 watcher를 추정으로 종결하지 않는다. 변경·종료는 금지.
새 독립 리뷰/REQUEST/READY/모델 호출/Telegram/호스트 SHADOW 설치/운영 DB·키·정책·Task·Notifier 변경 0. 단계 4~6 및 10단계 LIVE는 이번 범위 밖. 결과 게시 후 종료하며 LIVE_READY=NO를 유지한다.
