# GitHub CoWork 수락시험 매트릭스 r0001
2026-11-10 KST | 전체 48건 = T01~T38 + S01~S10
근거: 사용자 제공 COWORK_DROPBOX_TO_GITHUB_MIGRATION_HANDOFF_r0002_20261110.md의 T01~T38, Claude 정적 리뷰 원문 B-1~B-7, 신규 서명 시나리오 S01~S10.

## 시험 상태 해석
- 아래의 NOT_RUN은 **해당 완성형 GitHub watcher 구현에 대한 번호별 E2E를 실행하지 않았다**는 뜻이다.
- Claude Code의 Windows watcher v0.1.5 격리 합성시험 P1~P5/Q1~Q4: 기존 부분 동작 및 결함 재현 근거. T01/T02/T10~T13 계열에 일부 대응할 수 있으나 번호별 완성형 테스트 PASS가 아니다.
- 이전 GPT 보안 게이트 오프라인 합성 시험 41 PASS는 별도 후보에 대한 보고. 이 Windows 환경에서 검증되지 않아 아래 T/S 개별 PASS로 승격하지 않는다.
- 모든 S01~S10은 실제 서명 라이브러리·신뢰키/승인 봉투 E2E NOT_RUN.

## 번호별 명세
| ID | 입력/상황 | 기대 관찰 | 현재 상태 |
|---|---|---|---|
| T01 | ZIP만 있고 READY 없음 | 모델 호출 0 | NOT_RUN |
| T02 | REQUEST만 있고 READY 없음 | 모델 호출 0 | NOT_RUN |
| T03 | READY가 먼저 보임 / commit A 검증 전 | FAILED_PRECHECK, 모델 0 | NOT_RUN |
| T04 | READY.request_sha256 불일치 | 거부, 모델 0 | NOT_RUN |
| T05 | ZIP SHA/size/CRC 불일치 | 거부, 모델 0 | NOT_RUN |
| T06 | knowledge_refs hash/revision 누락 | 거부, 모델 0 | NOT_RUN |
| T07 | 동일 ZIP·다른 request_id 반복 요청 | 승인 정책 준수, 무단 재리뷰 0 | NOT_RUN |
| T08 | 같은 request_id에 다른 ZIP overwrite | CONFLICT, 원본 보존 | NOT_RUN |
| T09 | PR/포크/Issue/태그에 READY 게시 | 모델 0 | NOT_RUN |
| T10 | main에 유효 READY 최초 게시 | Claude 1회, durable claim | NOT_RUN |
| T11 | 동일 READY 중복 poll/재시작 | 추가 Claude 0 | NOT_RUN |
| T12 | Claude 실행 도중 호스트 중단·재시작 | REVIEW_UNCERTAIN 봉인, 재호출 0, 불확실 알림 1 | NOT_RUN |
| T13 | 모델 완료 후 결과 게시 실패/429 | 기존 결과 재게시만, 재호출 0 | NOT_RUN |
| T14 | REVIEW_RESULT는 있으나 RECEIPT 없음 | PUBLISH_PENDING, 완료 알림 0 | NOT_RUN |
| T15 | Receipt ok=false / ID·revision·SHA 불일치 | COMPLETED 승격 금지 | NOT_RUN |
| T16 | source commit A와 이후 HEAD 다름 | 고정 A 바이트 읽기/변조 탐지 | NOT_RUN |
| T17 | 동시 CURRENT/결과 게시 CAS 경합 | 충돌 검출, force push 0 | NOT_RUN |
| T18 | 403/404/인증 만료·네트워크 오류 | fail-closed, 민감 로그 0 | NOT_RUN |
| T19 | Windows watcher 두 프로세스 동시 실행 | 단일 runner, 리뷰 1회 이하 | NOT_RUN |
| T20 | Dropbox LIVE + GitHub SHADOW | GitHub 모델 0, DB jobs write 0, remote write 0, Telegram 0 | NOT_RUN |
| T21 | cutover 후 과거 완료 요청 재검출 | logical_request_id/원장 reconcile로 재호출 0 | NOT_RUN |
| T22 | SEMI_AUTO 완료 Telegram | 1회 완료 알림, 사용자 GPT 재개 후 결과·영수증 확인 | NOT_RUN |
| T23 | AUTO_PENDING_SETUP / mode 생략 | GPT Work 자동 실행 없음 | NOT_RUN |
| T24 | STATIC 비용 상한 초과 | 정책상 차단, 예산 자동증액 없음 | NOT_RUN |
| T25 | 악성 ZIP 경로 이탈·symlink·숨김 비밀 | 패키지 거부, 임의 실행 0 | NOT_RUN |
| T26 | Private 자료를 Public/fork로 유도 | 게시 차단 | NOT_RUN |
| T27 | Dashboard JSON 불량/깨진 work item | 항목 격리, 이전 유효 HTML 유지 | NOT_RUN |
| T28 | Public Pages 무단 게시 | 미승인 외부 게시 0 | NOT_RUN |
| T29 | 파일럿 성공 후 Dropbox rollback | 중복 없이 1 ACTIVE, 이력 보존 | NOT_RUN |
| T30 | GitHub 삭제 후 Git history 복구 가능 | 완전 삭제로 오판하지 않음 | NOT_RUN |
| T31 | PRIVATE REQUEST/RECEIPT 공개 업로드 시도 | PUBLICATION_BLOCKED, Public 신규 파일 0 | NOT_RUN |
| T32 | development-only ZIP PUBLIC 배포 시도 | NOT_DEPLOYABLE, Public write 0 | NOT_RUN |
| T33 | 기존 Public ZIP 동일 이름·동일 SHA | ALREADY_PUBLISHED, 새 commit 0 | NOT_RUN |
| T34 | 기존 Public ZIP 동일 이름·다른 SHA | RELEASE_PATH_COLLISION, 원본 보존 | NOT_RUN |
| T35 | 승인 ZIP과 공개 업로드 bytes 다름 | SHA_MISMATCH, 배포 미완료 | NOT_RUN |
| T36 | 사내 무인증 PUBLIC ZIP 다운로드 | 동일 SHA, Private credential 불필요 | NOT_RUN |
| T37 | reviewer가 PUBLIC 저장소 write 시도 | 권한 거부, reviewer 영향 없음 | NOT_RUN |
| T38 | PUBLIC ZIP 민감정보 혼입 | 사전 검사 차단; 한계 기록 | NOT_RUN |
| S01 | 서명 없음 | 거부, 모델 0 | NOT_RUN |
| S02 | 서명 위조·canonical payload 불일치 | 거부, 모델 0 | NOT_RUN |
| S03 | 다른 저장소 ID | 거부, 모델 0 | NOT_RUN |
| S04 | 만료된 서명/시계 경계 | 거부, 모델 0 | NOT_RUN |
| S05 | 변조된 source commit A | 거부, 모델 0 | NOT_RUN |
| S06 | 변조된 REQUEST 원본 bytes | 거부, 모델 0 | NOT_RUN |
| S07 | 변조된 ZIP bytes | 거부, 모델 0 | NOT_RUN |
| S08 | 키 폐기/회전 후 구 키 사용 | 거부, 모델 0 | NOT_RUN |
| S09 | 동일 승인 replay / 정책 버전 변경 | 재호출 0 | NOT_RUN |
| S10 | READY/승인 sidecar 부분 관찰 | 완전한 묶음 승인 전 모델 0 | NOT_RUN |

## Claude Code 기존 합성시험 → 기대 시나리오 연결 (정식 PASS 아님)
- P1: 정책 개정으로 처리키 변경(B-5) → T21, S09 추가 반례 **결함 재현**.
- P2: LF/CRLF/BOM 변경으로 해시 충돌(B-6) → T04, S06 지원 반례 **결함 재현**.
- P3: unknown 확장 필드 통과 → REQUEST V1 하위 호환 부분 근거, 서명 보안 증거 아님.
- P4/Q2: READY_APPROVAL.json 중복 분류 → T03/S10 관련 **결함 재현**.
- Q1/Q3: 합성 정상 흐름, mode 사이드카 영향 없음 → T10·T11 관련 일부.
- Q4: 호출 중 중단/재시작시 재호출 0이나 REVIEW_RUNNING 잔존 → T12의 **현행 구현 FAIL 근거**. r0002에서 보완 목표.
- ETag/304 실측: GitHub 읽기 최적화 관찰, 실제 watcher GitHub poll E2E 아님.
- B-4에서 공유 DB의 이미 있는 처리키 INSERT OR IGNORE는 관찰, 두 provider 동시 실행 거부는 미실측.

## 구현 후 시험 결과 작성 계약
각 시험은 TEST_ID / ENV / BUILD_SHA / INPUT_BYTES_SHA256 / DRIVER_OR_COMMAND / EXPECTED / OBSERVED / PASS|FAIL|NOT_RUN / EVIDENCE / EXECUTOR / TIMESTAMP_UTC를 기록한다.
기존 watcher/Dropbox 호환 17개 테스트 파일 회귀(실제 파일과 범위 확인), 추가 B-2 파일명, B-3 복구, B-4 provider, B-5 정책 변경, B-6 바이트/해시, B-1/B-7 서명을 별도로 포함한다.
SHADOW_READ_ONLY에서는 reviewer model 0·remote write 0·Telegram 0을 실증하고 LIVE 파일럿 이전 별도 승인받는다.
