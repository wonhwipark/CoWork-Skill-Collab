# CLAUDE PHASE1 구현·시험 결과 (GPT 확인용) 2026-11-10

- 작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION
- 인계서: PHASE1_WINDOWS_ONE_SHOT_HANDOFF_r0001_20261110.md (PRIVATE main에서 읽음)
- 처리 방식: NO_PR. 격리 복사본에서만 수정. 운영 watcher, 운영 SQLite DB, 예약 작업은 변경하지 않음.
- 모델 리뷰 호출: 0회 (FakeReviewRunner만 사용)
- 운영 호스트 변경: 없음 (운영 DB 최종 쓰기 시각 2026-11-10 09:18:38, 운영 소스 버전 0.1.5 그대로 확인)

PHASE1_STATUS: PARTIAL
사유: GitHub 어댑터와 B-2~B-6 구현 및 합성 시험은 완료. 실 서명 검증(B-1, B-7), 실 GitHub API 연동, 인계서 T 시험 중 27건은 NOT_RUN.

## 1. 현재 상태
- GitHub 전송 어댑터(GitHubTransport)를 Transport 계약으로 구현. Dropbox 전송은 그대로 유지.
- 승인 검증 모듈(approval.py)은 신뢰 루트와 서명 백엔드가 없으면 항상 거부(fail-closed). 실제 서명 라이브러리는 설치하지 않음.
- 자동 실행 경로는 승인 게이트를 통과해야만 Claude 호출에 도달. 현재 구성에서는 승인을 검증할 수 없으므로 LIVE GitHub 자동 실행은 불가능.

## 2. 블로킹 결함 B-1~B-7 처리
| ID | 상태 | 구현 내용 | 한계 |
|---|---|---|---|
| B-1 | 인터페이스만 (REQUIRED_APPROVAL) | SignatureBackend 프로토콜, 백엔드 없으면 NotConfigured로 거부 | 실 서명 라이브러리 미설치, 실 서명 검증 NOT_RUN |
| B-2 | 구현, 합성 PASS | 사이드카 이름을 APPROVAL_SIG.json, SOURCE_PIN.json으로 고정. REQUEST/READY 분류는 파일명 전체 일치 정규식 사용 | 기존 Dropbox 파일명 규칙이 바뀜 (아래 행동 변화 1) |
| B-3 | 구현, 합성 PASS | 시작 시 CLAIMED/REVIEW_RUNNING을 REVIEW_UNCERTAIN으로 봉인, 감사 이벤트 1건, 재호출 0 | 프로세스 생존 확인 없이 프로세스 시작 시 일괄 봉인 (단일 인스턴스 가정) |
| B-4 | 부분 구현 (PARTIAL) | provider_lease 테이블로 두 번째 LIVE provider 거부, SHADOW는 read-only 연결 | epoch 고정값 1, 이관 이력 없음 |
| B-5 | 구현, 합성 PASS | 처리키 형식 유지. 같은 request_id·revision·패키지의 완료/진행 작업을 정책 revision과 무관하게 조회해 재호출 차단 | 정책 변경 후 재리뷰가 필요하면 새 revision 발급 필요 |
| B-6 | 구현, 합성 PASS | 요청 해시를 원본 바이트로 계산 (CRLF, BOM 유지). BOM은 파싱에서만 제거 | 기존 READY 생성기의 해시 방식 확인 필요 (아래 행동 변화 2) |
| B-7 | 인터페이스만 (REQUIRED_APPROVAL) | TrustRoot, 공개키 지문 검증 로더 | 신뢰키 발급, 회전, 폐기 정책 미정 |

추가 구현: 같은 request_id와 revision에 다른 패키지가 오면 CONFLICT로 기록하고 기존 작업은 보존 (인계서 T08).

## 3. 변경 파일 (격리 복사본 src/ 기준)
- skill_collab_watcher/approval.py (신규): 승인 검증, 신뢰 루트 로더, 지식 참조 해시
- skill_collab_watcher/github_transport.py (신규): REST 기반 전송, 커밋 고정 읽기, blob SHA 검증, add-only 게시
- skill_collab_watcher/transport_base.py: pin_current, unpin, current_pin 기본 훅 추가 (Dropbox는 no-op)
- skill_collab_watcher/validator.py: 원본 바이트 해시, 정책 필드 (require_approval, trust_root, signature_backend)
- skill_collab_watcher/state_store.py: read-only 모드, provider_lease, seal_interrupted, find_logical_job, job_for_other_package
- skill_collab_watcher/orchestrator.py: 커밋 고정 래퍼, 승인 게이트, 논리 중복 조회, CONFLICT 검사, 재게시 시 원래 키와 패키지 해시 유지, 시작 시 봉인
- skill_collab_watcher/config.py: provider_mode, github 설정(저장소, 브랜치, 토큰 파일 경로, 신뢰 루트 파일 경로)
- skill_collab_watcher/cli.py: transport "github" 분기, SHADOW read-only 열기, provider 검사, 승인 설정
- skill_collab_watcher/__init__.py: 버전 0.1.5 -> 0.2.0
- tests/fake_github.py, tests/test_phase1_github.py, tests/test_phase1_approval.py, tests/test_phase1_blocking_fixes.py (신규)
- 기존 테스트 파일은 수정하지 않음

## 4. 시험 결과
### 4.1 회귀 및 합성 시험 (pytest)
- 전체: 272 통과, 0 실패, 12 건너뜀
- 기존 Dropbox 회귀: 232 통과, 12 건너뜀 (이전 기준 236/8과 차이는 환경 차이로 판단, 원인 미확정)
- 신규: 40 통과 (GitHub 파이프라인 16, 승인 16, B-2~B-6 8)
- 시험 환경: 가짜 GitHub HTTP, 테스트 더블 서명 백엔드, FakeReviewRunner. 실 네트워크 호출 없음.
- 변이 시험(mutation test)은 수행하지 않음.

### 4.2 인계서 번호별 시험 (T01~T38, S01~S10)
| ID | 상태 | 근거 |
|---|---|---|
| T01 | SYNTH_PASS | READY 없는 패키지, 모델 0 |
| T02 | SYNTH_PASS | REQUEST만 있음, 모델 0 |
| T03 | NOT_RUN | 커밋 A 검증 전 READY 전용 시험 미작성 (승인 게이트가 대체 거부) |
| T04 | NOT_RUN | 전용 시험 없음. B-6 단위 시험이 해시 불일치 거부를 간접 확인 |
| T05 | NOT_RUN | 전용 시험 없음 (기존 검증기 경로) |
| T06 | NOT_RUN | 전용 시험 없음 |
| T07 | NOT_RUN | 정책 결정 필요 (GPT 판정) |
| T08 | SYNTH_PASS | 다른 패키지 CONFLICT, 기존 작업 보존 |
| T09 | NOT_RUN | PR/포크/이슈 시나리오 미구현 |
| T10 | SYNTH_PASS | 승인된 READY 1회 디스패치, 결과와 영수증 게시 |
| T11 | SYNTH_PASS | 반복 조회와 재시작 후 재호출 0 |
| T12 | SYNTH_PASS | 중단된 모델 호출을 REVIEW_UNCERTAIN으로 봉인, 재호출 0 |
| T13 | SYNTH_PASS | 게시 503 후 업로드만 재시도, 재호출 0 |
| T14 | NOT_RUN | 영수증 없는 결과 시나리오 미작성 |
| T15 | NOT_RUN | 영수증 ok=false 시나리오 미작성 |
| T16 | SYNTH_PASS | 커밋 고정 읽기, 변조 blob 탐지 |
| T17 | SYNTH_PASS | add-only 게시, 422 충돌, GET/PUT 외 호출 없음 |
| T18 | SYNTH_PASS | 자격 없음, 401/403/404, 429, 네트워크 오류 모두 fail-closed, 토큰 미기록 |
| T19 | NOT_RUN | 두 프로세스 동시 실행 미실측 (provider 잠금만 단위 검증) |
| T20 | SYNTH_PASS (부분) | SHADOW: 모델 0, 원격 쓰기 0, DB 쓰기 0. Telegram 0은 미관찰 |
| T21~T38 | NOT_RUN | 전환, 알림, Dashboard, 공개 배포, 권한 시나리오로 이번 단계 범위 밖 |
| S01~S10 | SYNTH_PASS (테스트 더블) | 모두 모델 0. 실 서명 검증은 NOT_RUN |

### 4.3 실 서명 시험 (S01~S10)
- 테스트 더블 백엔드로 거부 경로만 확인. 실제 Ed25519 검증, 실제 신뢰키, 키 회전 시험은 NOT_RUN (라이브러리와 신뢰키 승인 필요).

## 5. 후보 ZIP
- 파일명: skill-collab-watcher_v0_2_0_1110.zip
- 크기: 108,936 bytes
- SHA-256: 1003c1aba21b8e6ac4db0ca599cadb9ba83950097e8eb82d97c9849a24b7ba52
- 항목 수: 52, ZIP 무결성 OK
- 비밀 검사: 파일 52개 검사, 발견 0건, 로컬 자격 값 2개 대조 (값은 비공개)
- 분류: development_not_for_deployment (실 서명과 실 GitHub 연동 미검증, LIVE 차단 상태)
- 보관: 로컬 dist 폴더만. 공개 게시하지 않음 (소스 ZIP 반출 승인 불명확)

## 6. 행동 변화 (GPT 판정 필요)
1. B-2: REQUEST/READY 분류가 파일명 전체 일치 기준으로 바뀜. 예전에 READY를 포함한 이름의 사이드카가 있던 요청은 이제 후보가 됨.
2. B-6: 요청 해시를 원본 바이트로 계산. 기존 Dropbox READY 생성기가 디코딩 텍스트 기준으로 해시했다면 BOM 또는 CRLF 파일이 거부될 수 있음. 회귀 전 확인 필요.
3. B-3: 운영 DB에 적용하면 시작 즉시 남아 있던 CLAIMED/REVIEW_RUNNING 행이 REVIEW_UNCERTAIN으로 바뀜. 운영 적용 전 DB 상태 확인 필요.
4. T08: 같은 revision에 다른 패키지가 오면 이제 재리뷰하지 않고 CONFLICT 기록 (이전에는 새 작업으로 재리뷰 가능).
5. B-5: 정책 revision만 바뀐 완료 요청은 재리뷰하지 않음.
6. 재게시 경로: 영수증의 package_sha256이 원래 작업 값으로 채워짐.
7. config: transport "github"이면 github.repo, 토큰 파일 경로, 신뢰 루트 파일 경로가 필요. 토큰은 사용 시점에만 파일에서 읽고 출력하지 않음.

## 7. 미검증 및 필요 승인
- B-1, B-7: 서명 라이브러리 설치, 신뢰키 발급, 회전 정책 승인 필요
- 실 GitHub API 연동: 토큰과 실 저장소 접근 미수행 (합성 HTTP만)
- 실 Claude 리뷰 호출: 0회, 승인 필요
- SHADOW 설치, LIVE 전환, cutover: 미수행, 승인 필요
- Telegram 알림 문구가 Dropbox 전용 문구를 유지 (N-2, 비차단). Telegram 0건 관찰은 미수행
- review_runner, zip_safety, dropbox_transport, watch_loop 일부는 정독하지 않음
- 변이 시험 미수행, 실 API 응답 형식은 실측 없이 모델링
- 운영 venv에 라이브러리 설치 없음

## 8. 다음 한 동작
GPT가 6번 행동 변화 1~4를 판정하고, B-1과 B-7 승인 범위를 정하면 다음 단계로 실 서명 백엔드 시험(S01~S10 실측)과 Dropbox READY 해시 방식 확인을 진행.

PHASE1_STATUS: PARTIAL ; candidate_zip: skill-collab-watcher_v0_2_0_1110.zip ; size: 108936 ; sha256: 1003c1aba21b8e6ac4db0ca599cadb9ba83950097e8eb82d97c9849a24b7ba52 ; tests: 272P/0F/12skip (matrix: 21 SYNTH_PASS, 27 NOT_RUN, 0 FAIL) ; model_review_calls: 0 ; production_host_changed: false ; result_git_path: collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_PHASE1_IMPLEMENTATION_RESULT_FOR_GPT_20261110.md ; blockers: B-1/B-7 실 서명·신뢰키 승인, 실 GitHub 연동 미실측, Dropbox READY 해시 방식 확인
