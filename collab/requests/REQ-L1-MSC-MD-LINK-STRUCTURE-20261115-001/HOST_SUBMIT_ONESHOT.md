# Claude Code 호스트 접수·실행 원샷

- 저장소: PRIVATE `wonhwipark/CoWork-Skill-Collab`
- 브랜치: `main`
- 요청서: `collab/requests/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/REQUEST.md`
- 입력 pin: `collab/requests/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/SOURCE_PIN.json`
- 입력 manifest: `collab/projects/L1-WORKSPACE-RAG-20261111-001/review-inputs/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/REVIEW_MANIFEST.md`
- 같은 Work: `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`

## 전달할 한 문장

> PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`의 `collab/requests/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/REQUEST.md`와 SOURCE_PIN/REVIEW_MANIFEST를 읽고, 이번 MSC·Procedure/Feature MD 링크 구조의 독립 리뷰를 현재 협업 계약으로 접수해주세요. 유효 권한·중복·고정 바이트를 확인한 뒤 가능한 범위만 한 번 실행하고 실제 결과/receipt 또는 차단 이유를 같은 Work에 게시·readback해주세요.

## 호스트가 순서대로 확인할 내용

1. 최신 migration CURRENT의 실제 GitHub LIVE와 auto-approval CURRENT의 실제 설치/활성화 상태를 확인해요. 보호 위임 승인 문구만으로 자동 승인 ON을 가정하지 않아요. 이 요청을 나중에 켜진 위임으로 소급 자동 실행하지 않아요.
2. SOURCE_PIN의 repo ID·Commit A에서 REQUEST·ZIP을 가져와 raw ZIP **38132 B / SHA-256 `90bb61a0e7c3b429942c620480ad9a079980d2a3432b72cea8ba80a4b915907d`**, CRC·일반파일·경로·manifest 및 실제 설치 validator를 확인해요. 텍스트 8개 전용 ZIP이며 SKILL.md나 새 설치가 필요하지 않아요. 실패는 fail-closed/모델 0이에요.
3. 이번 ID/revision/ZIP 및 동일 목적 실행의 dispatch·review·receipt·불확실 기록을 확인해요. 이미 시작/완료/불확실이면 새 모델 호출을 하지 않고 기존 결과 회수/게시만 해요. 이전 Work→Knowledge 요청은 별개 동결 이력으로 보존해요.
4. 이번 요청에 실제 적용되는 기존 유효 승인·보호 위임·예산·만료를 확인해요. 현재 등록만으로 새로운 $1 비용 승인이나 서명을 만들어내지 않아요. 권한이 없으면 `PAID_REVIEW_AUTHORIZATION=NOT_CONFIRMED`, `INDEPENDENT_REVIEW=NOT_RUN`으로 차단 이유를 게시해요. 이미 유효한 권한이 확인되면 같은 승인을 반복 요청하지 않아요.
5. 승인 경로가 충족되면 기존 호스트 절차로 request/revision·source commit·repo ID·raw SHA·정책/최대 $1·1회에 결속한 승인을 검증하고 APPROVAL_SIG readback 후 READY를 **마지막**에 게시해요. 기존 GitHub 단일 LIVE watcher의 자동 처리를 관찰하고 별도 watcher/직접 추가 모델 호출을 시작하지 않아요.
6. R01~R10 구조 리뷰 1회의 결과·receipt·usage·dispatch를 실제 경로에서 readback해요. 개발 세션 자기 검토를 독립 리뷰로 대신하지 않아요. 결과 게시 장애는 게시만 복구하고 재호출하지 않아요.
7. `collab/requests/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/SUBMISSION_STATUS.json` 및 같은 Work CURRENT/TRACKER에 실제 접수·권한·실행·결과 경로·미검증을 기록해요. 이 요청을 수행했다고 운영 설치·업무 코드 분석·Workspace/그룹 게시·RAG를 PASS로 올리지 않아요.

이 GPT 환경에는 Windows Claude Code 프로세스/보호 키/예약 작업을 시작할 수단이 없어요. 이 문서 게시 자체는 호스트 실행 신호가 아니에요. 결과를 실제 수신하기 전 현재 상태는 요청 등록·입력 고정 완료, 독립 리뷰 `NOT_RUN`이에요.
