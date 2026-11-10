# Windows Claude Code 다음 단계 — GitHub adapter 최소 변경 구현 준비
2026-11-10 KST | MODE: ISOLATED_DEVELOPMENT / NO_PR / NO_LIVE / NO_REVIEW_REQUEST

## 목적
기존 Dropbox CoWork watcher(v0.1.5로 Claude가 소스 조사 보고)를 가능한 한 재사용하고 GitHub PRIVATE transport를 격리 작업 복사본에서 구현·회귀시험한다. GitHub를 변경된 협업 정본으로 쓰되 정식 REQUEST/READY 자동 리뷰 시스템은 아직 검증되지 않았다. 이 문서는 실행 요청(READY)이 아니며 자동 리뷰를 트리거하지 않는다.

## 필수 입력(main에서 직접 읽기)
1. collab/START_HERE.md
2. collab/ops/CONTRACTS/NO_PR_COLLABORATION_V1.md
3. collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0002_20261110.md
4. collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/ACCEPTANCE_TEST_MATRIX_r0001_20261110.md
5. collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md
6. collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md
PR #1은 폐쇄된 과거 설계 증거일 뿐 사용하지 않는다.

## 실행 계획 — 격리 복사본 한정
1. LIVE watcher 원본/설치 버전/현재 task/DB 백업 필요 사항을 읽기 전용으로 확인. 운영 경로에 새 코드 쓰기 금지. 별도 작업 폴더를 만들고 허용된 watcher 소스의 **복사본**에서만 작업.
2. 실제 transport_base.Transport 메서드·orchestrator·state_store·validator·cli·watch_loop·notify_reviews의 정확한 연결을 확인. 기존 Dropbox 회귀 17개 시험 파일이 실제 존재하는지 확인.
3. GitHub transport(API raw blob bytes, main ETag 304/conditional poll, commit pin fetch, CAS add-only publisher) 최소 변경 후보 구현. 기존 DropboxTransport, 정책·Claude runner는 보존.
4. B-2는 APPROVAL_SIG.json/SOURCE_PIN.json 이름을 사용하고 sidecar 매칭 회귀. B-5는 local_policy_revision 처리키/정책 변경 시 logical duplicate 재호출 0. B-3는 중단된 REVIEW_RUNNING/CLAIMED를 재호출 없이 REVIEW_UNCERTAIN 봉인. B-4 단일 provider lease와 SHADOW DB write 0. B-6 GitHub API 원본바이트로 LF/CRLF/BOM 점검.
5. B-1/B-7 서명 계층은 승인 전 암호 라이브러리 설치·신뢰키 생성 없이 **인터페이스와 실패시 모델 0**까지만 구현·시험. 실제 Ed25519 인증 완료로 표시 금지.
6. 합성 실행과 기존 Dropbox 회귀시험. T01~T38 및 S01~S10은 시험한 범위별 증거와 NOT_RUN을 구분. 정상 호출 Q1은 반드시 FakeRunner, 실제 Claude 모델 호출 0.
7. 결과는 코드 변경 목록·diff/현재 설치판과의 경계·회귀 실측·미시험/차단·후보 ZIP 정보(SHA-256/bytes)·다음 한 동작으로 정리. 비밀과 회사 반출금지 원문은 PRIVATE GitHub에도 업로드하지 않음.

## 금지
- 운영 watcher 파일/SQLite/예약작업 수정·중지·재시작·추가 설치
- PRIVATE 저장소에 실제 REQUEST/READY 발행 또는 GitHub watcher LIVE 실행
- 신규 토큰 발급/암호 라이브러리 운영 venv 설치/서명키 발급(별도 사용자 승인 선행)
- 실제 Claude Code 독립 리뷰 자동 호출, PUBLIC L1Work write, PR 생성/병합
- 자격증명·사내 반출 금지 소스/로그/개인키를 저장소/모델 프롬프트에 노출
- /AI-CONTINUITY/ 수정

## 보고
IMPLEMENTATION_STATUS = PASS|PARTIAL|BLOCKED, 파일별 REUSE/WRAP/NEW, 실제 테스트 명령·환경/통과·실패, model_calls=0, sha256, 남은 승인 필요 항목을 구분. 실제 설치가 없으면 HOST_APPLIED=NOT_RUN.
초기 작업은 로컬 격리 복사본에서만 실시. 결과를 PRIVATE에 게시하려면 비밀/반출 검사 후 직접 파일 게시·원격 readback을 하되, watcher가 감시하는 REQUEST/READY 폴더에는 쓰지 않는다.
