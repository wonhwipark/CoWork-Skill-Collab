# CoWork GitHub LIVE 직전 원샷 — 리뷰 입력 게시·독립 리뷰·감시기 연동·전환 사전검증
r0001 · 2026-11-14 KST | **ONE_SHOT_EXECUTION_HANDOFF / LIVE_CUTOVER_NOT_AUTHORIZED**
Repo: `wonhwipark/CoWork-Skill-Collab` **PRIVATE** | branch `main`
Exact relative path: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_ONE_SHOT_REVIEW_INTEGRATION_PREFLIGHT_r0001_20261114.md`
Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
이 문서의 실행은 **Windows Claude Code에게 사용자 1회 전달**하는 것만으로 시작한다. GitHub 문서 게시 자체로 Windows Claude Code·Python watcher가 자동 실행되는 것은 아니다.

## 0. 단일 목표와 중요한 환경 사실
**1회 Windows Claude Code 작업에서 (1) GitHub PRIVATE 리뷰 자료의 실제 바이트 게시와 고정 링크, (2) 이미 승인된 실제 독립 Claude 리뷰 절차가 있다면 그 범위의 1회 리뷰/영수증 또는 독립 리뷰 실행 준비까지, (3) 격리된 Windows CoWork 감시기 전체 연동·전환 사전시험, (4) 개발 결함 수정·최소 관련 재시험·최종 후보 보존 및 (5) LIVE 직전 통합 보고까지 끝낸다.**
- 사용자 1명이 Windows Claude Code PC를 모바일로 원격 조작. 이 PC는 **회사 L1 SW 소스에 접근 불가**. CoWork 자체 소스/ZIP을 **GitHub PRIVATE에 게시하여 Claude 독립 리뷰에 전달하는 것을 2026-11-14 사용자가 명시 승인**했다. `wonhwipark/L1Work`의 기게시 스킬 ZIP 및 `handoffs/` MD도 GitHub 링크 리뷰 허용.
- **과거 과도한 선행 요구를 복원하지 말 것**: 2번째 signer PC, 로컬/온프레미스 LLM, ETW 4축 입증, 3종 토큰 일괄 교체, 별도 Windows 서비스 계정 설치, 별도 LOCAL_ONLY v2/v3 정책 엔진 도입을 일반 CoWork LIVE 준비의 필수 조건으로 삼지 않는다.
- **최소 유지 사항**: 실제 리뷰와 자체시험 구분, 한 요청당 모델 리뷰 중복 0, 비용/승인범위 준수, 토큰·회사 원본 비밀 미노출, 운영 DB/Task와 이력 보존, GitHub review input 진짜 원격 검증, 단일 활성 LIVE, 롤백 가능성.
- **LIVE 전환은 이번 작업에 포함되지 않는다**. 실제 운영 Task·활성 provider·기존 DB/WAL/SHM·Notifier/Bridge/운영 인증 변경, 신뢰키 생성·이관, LIVE cutover, `L1Work` PUBLIC 신규 ZIP 배포는 별도 최종 승인 후에만.
- **유료 리뷰와 READY는 자동 승인 아님**: 사용자의 자료 전달 승인은 모델의 추가 비용 지출 승인이 아님. 이번 작업에 대해 유효한 명시적인 리뷰 실행·비용/모드 승인이 이미 존재하며 계약이 충족된 경우에 한해 정확히 1회 실행 가능. 그런 승인이 없다면 **준비까지만 하고 `INDEPENDENT_REVIEW=PENDING_APPROVAL` / `MODEL_CALLS=0`**. 사용자 추가 지시를 기다리느라 나머지 작업을 중단하지 않는다.
- 프로젝트 기준: `collab/START_HERE.md`, 해당 `CURRENT.md` 최신 상단, `TRACKER.json`, `GPT_COWORK_SINGLE_USER_SIMPLIFIED_COLLAB_RULES_r0001_20261114.md`, `GPT_GITHUB_LINK_REVIEW_TRANSPORT_APPROVAL_AND_ONE_SHOT_r0001_20261114.md`, `CLAUDE_SINGLE_USER_LIVE_FASTTRACK_RESULT_FOR_GPT_20261114.md`, `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, `collab/ops/CONTRACTS/PUBLIC_RELEASE_GATE.md`.
- 직전 Windows 보고: `v0.2.13` 후보 로컬 `D:\User\whpark\cowork-phase1\dist_phase2\`, 코드 `D:\User\whpark\cowork-phase1\contract\`. 실제 디렉터리/후보 ZIP·버전·원본 SHA는 반드시 **호스트에서 검증**. 직전 제품 자체시험 보고 `642 PASS/13 SKIP`, r0003 28 PASS×3 및 14 변이 검출. 모두 `SELF_TEST_REPORTED`. 지난 후보 `CONTRACT_INTEGRATION=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `ACTIVE_PROVIDER=NONE`. SU-L1 r0003 독립 프로토타입은 **제품에 미연결**; 이 상태를 독립 리뷰나 LIVE 통과라고 추정 금지.

## 1. 순서와 범위: 핑퐁을 줄이는 실제 수행 계획
**A. 정확한 정본·호스트 확인 — 반복 조사 금지**
1. 최신 원격 `CURRENT.md`, 별도 진행 중인 작업/미정산 요청과 기존 watcher 기존 설치·백업·정책/데이터 처리키를 읽기 전용으로 확인. 로컬 **운영 DB 파일을 읽더라도 WAL/SHM 쓰기 여부를 검증해야 하며 안전하지 않으면 접근하지 말 것**. 사용 중단 상태도 실측과 문서 주장을 구분.
2. 위 폴더의 `v0.2.13` 원본 ZIP·코드, 버전 manifest, local-only r0003과 원 watcher의 기존 중복 처리 구현을 비교. **r0003/SU-L1을 반드시 제품에 통합하라는 뜻 아님**. 기존 watcher 내 중복 방지가 제품 경로에서 정상 입증되면 재사용한다. 빠진 필수 기능만 수정.
3. 이전 성공 642/13, r0003/ETW/토큰 합성 시험은 **변경하지 않은 모듈에 대해 반복하지 말 것**. 고친 부분과 제품 진입점의 delta 시험 중심.

**B. 격리된 실제 제품 진입점 연동 시험 — 리뷰 전 결함 수정**
1. 운영 감시기가 아닌 **격리 복사본·별도 임시 디렉터리·모의 DB·모의 reviewer·모의 notifier**로 진입점부터 시험: `GitHub 요청 획득 → 계약/승인 검증 → logical key/중복 예약 → reviewer dispatch(모의) → 결과/영수증 → 원격 검증 → 완료/중복알림 방지`. 실제 외부 모델/기존 알림 호출 금지. 이 흐름에 필요한 최소 통합 코드는 허용된 개발 사본에서 직접 수정.
2. **최소 E2E 필수 시험**: (a) 정상 신규 유효 요청 1회 결과 1건, (b) 동일 요청 재스캔·2프로세스 경합 중 모델 호출 모의 카운터=1, (c) 재기동 후 replay=0, (d) 잘못된/승인 없는 READY는 호출=0, (e) 결과 원격 쓰기 실패 시 리뷰 재호출=0 (`REVIEW_UNCERTAIN`+게시만 재시도), (f) 오래된/미정산 Dropbox 이력 보존·활성 provider 하나, (g) backup·rollback 이행 계획/재기동 시 이력 무손실, (h) 중복 Telegram/notify 0, (i) 사용 중단 작업·기존 DB/Task 변경 0. 신규 GITHUB transport가 이전에 요구한 실제 서명 검증과 충돌하면 기존 필수 구현을 조용히 우회하지 말고 `BLOCKED_CONTRACT_GAP`로 설명하고 보완 설계/시험 준비.
3. GitHub 실제 read-only SHADOW 연결은 허용된 범위에서만. review-inputs 업로드 및 원격 readback을 운영 watcher의 실제 REQUEST/READY 관찰과 혼동하지 말 것. SHADOW에서는 모델 호출, 상태 DB 쓰기, Telegram 0.
4. 합성 E2E 실패는 같은 개발 작업 내 수정·재시험. 불필요한 대형 신규 인증/로컬 LLM 개발로 확장 금지. 통합 테스트는 스텁에서만 돌렸다면 `INTEGRATION=SYNTHETIC_PASS`, 실제 설치된 후보 실행 진입점/호스트에서 돌렸다면 `HOST_ISOLATED_PASS`, 아예 못 돌렸으면 `NOT_RUN`. **운영 LIVE E2E PASS라고 표현 금지**.

**C. GitHub PRIVATE 실제 코드·ZIP·리뷰 명세 게시**
1. 유출 금지 대상(회사 L1 소스·고객자료·개인키/토큰·운영 비밀)이 없음을 확인. CoWork 자체 제품 코드·최종 시험 대상 버전의 소스·ZIP·변경 diff, 짧은 `REVIEW_MANIFEST.md`를 NEW `review_id` 아래 PRIVATE review-inputs에 게시 가능. 기존 후보를 덮어쓰지 말 것.
2. 실제 바이트 ZIP을 이용할 수 있는 `gh`/GitHub API 등 승인된 **binary upload** 경로로 새 이름 업로드하고 원격 **raw bytes** 다운로드 SHA-256/크기·commit pin·ZIP CRC/필수 경로를 확인. GitHub blob SHA/commit SHA는 ZIP SHA-256이 아님. 코드를 비트 손실 있는 text API 경로로 억지 변환하지 말 것.
3. `REVIEW_MANIFEST.md`: work ID, revision, candidate version, 변경 파일·기존 결함·시험 PASS/FAIL/SKIP, 원격 확인된 파일별 **GitHub 고정 커밋 URL**, raw ZIP SHA/bytes, 자체시험 표기, 독립 리뷰자에게 요청하는 구체 결함/위험(중복·replay·복구·GitHub link transport·Windows 호환성) 및 승인된 모델/비용/모드가 있으면 값. **검증한 URL만** 넣기.
4. 미승인 CoWork 후보 ZIP을 `wonhwipark/L1Work` PUBLIC root로 올리지 말 것. PUBLIC `handoffs/` 리뷰는 필요시 **기존 게시 문서 링크**를 별도 work ID로 참조만 하고 본 watcher LIVE 작업의 scope를 확장하지 말 것.
5. 업로드 불가능한 항목이 생겨도 다른 작업을 진행하고 `UPLOAD=BLOCKED`(원인·도구 권한 포함)로 격리.

**D. 실제 독립 Claude 리뷰 — 권한 있으면 1회만**
1. **다른 실행·다른 요청·다른 평가 컨텍스트**의 Claude 독립 reviewer를 사용. 개발자가 동일 세션에서 자체검토했다는 사실만으로 독립 리뷰라고 하지 않는다.
2. 기존 watcher Dropbox/GitHub valid REQUEST/READY와 승인된 리뷰 정책을 검증. GitHub `REVIEW_TRANSPORT_V1`은 DRAFT/NOT_ACTIVE이며 **문서 또는 단순 ZIP 게시만으로 리뷰를 시작하지 않음**. 비용/모드/승인/소유권 중 하나라도 명확하지 않으면 리뷰 및 READY `NOT_RUN/PENDING_APPROVAL`.
3. 정확한 review ZIP commit+SHA/URL을 reviewer에게 주고 **실제 결과 MD + 비용 영수증(또는 비용 0 증거) + 독립 session identity + 변경/중복 ID**를 PRIVATE에 게시·원격 readback. 게시 실패 때문에 모델을 두 번 호출하지 않으며 불확실 시 `REVIEW_UNCERTAIN`.
4. **독립 리뷰 결과가 실제 나온 경우에만** 지적을 반영하여 허용된 결함을 같은 개발 묶음에서 고치고 관련 delta 회귀시험; **수정 후 artifact가 달라졌다면 원래 ZIP 리뷰 PASS를 새 ZIP의 PASS로 승계하지 말 것**. 재리뷰는 새 명시 승인으로만, 그렇지 않으면 `PENDING_REREVIEW`로 보존. 비용 제한/호출 건수 강행 우회 금지.

**E. LIVE 직전 최종 검증 패킷**
1. 승인 전 접근 가능한 설정/데이터/작업 등록 실측, 새 후보를 설치할 정확 경로, 기존 Dropbox 이력·미정산 ID 보존 방법, backup/restore, rollback, 단일 active provider, notifier watermark 및 중복발송, 대상 호스트/실제 privilege/API 경로를 짧게 정리. **실운영 적용 아닌 격리 리허설**까지만.
2. 실제 인증 연결이 없는 경우 토큰 발급/광역 교체를 요구하기 전 `기존 gh login / watcher token 요구/권한 / 필요한 최소 변경`을 근거로 판정. 오래된 6개 승인 목록을 그대로 반복하지 말 것.
3. 최종 LIVE 조건표: `REVIEW_INPUT_UPLOAD`, `INDEPENDENT_REVIEW`, `HOST_ISOLATED_INTEGRATION`, `STATE_RECOVERY`, `NOTIFIER_DEDUP`, `CREDENTIAL_MINIMUM`, `CUTOVER_PLAN`, `FINAL_APPROVAL`을 각 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED`로 구분; 시뮬레이션이 실운영 검증을 대체하지 못한다고 기록.
4. `ACTIVE_PROVIDER=NONE` / `MIGRATION_NOT_CUTOVER`를 유지. 실제 운영 Task enable/disable, 설치·기존 DB migration, GitHub LIVE activation, REQUEST/READY 게시, 유료 모델 호출, PUBLIC 발행은 각각 기존 승인 조건 충족 시에만 진행. **이번 원샷 실행 문서 자체는 그런 승인 아님**.

## 2. 최종 산출물 — GitHub PRIVATE 파일 하나로 통합
**결과 파일**: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT_FOR_GPT_20261114.md`.
- 첫 페이지에 **현재 상태 → 변경 내용 → 실제 시험 결과 → 미검증/차단/승인 필요 → 산출물(로컬 후보 ZIP 및 실제 GitHub source/ZIP/manifest URLs·commit·원격 SHA) → 다음 사용자 한 동작** 순서로 작성.
- 개발 세션 자체시험은 `SELF_TEST_REPORTED`; 독립 리뷰의 실제 별도 요청/실행/영수증이 없으면 `INDEPENDENT_REVIEW=NOT_RUN`; 계획만 있으면 `PENDING_APPROVAL`. 명시 비용 승인 없을 때 `MODEL_CALLS=0 / PAID_REVIEW=NOT_RUN`.
- `CURRENT.md` 맨 위와 `TRACKER.json` 업데이트. 기존 이력 보존, PR 없이 PRIVATE main 직접 게시 후 **원격 내용/commit/ZIP 원본 bytes SHA readback**. readback 실패하면 `NOT_POSTED/UNVERIFIED`로 보고.
- **사용자에게 요청할 것은 실제 남은 승인만 1번에 묶기**: 예를 들어 독립 모델 리뷰 1회 비용/모드(미승인 시), 최종 운영 LIVE/실 Windows Task·DB 전환(사전 검증 통과 이후). 추가 PC·로컬 LLM·ETW 시험/토큰 3종 교체 등을 다시 기본 조건으로 묻지 않음.
- 실행 프롬프트는 이 문서 하나만 가리킨다. 구현 중 새 결함이 발견되면 같은 작업 안에서 수정/시험/반영 후 통합 보고. **실제 작업이 도구/권한으로 차단되면 막힌 행위만 NOT_RUN**, 완료인 척 하지 않음.

## 3. Windows Claude Code에 보내는 단일 메시지
```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main에서
collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LIVE_ONE_SHOT_REVIEW_INTEGRATION_PREFLIGHT_r0001_20261114.md
하나를 원샷 실행 인계서로 읽고 §1 A~E를 중간 확인 질문 없이 수행해줘.

Windows 로컬 v0.2.13 후보/기존 642 PASS 자체시험을 재사용해, 감시기 요청→모의 reviewer→결과·영수증·중복 방지의 실제 제품 진입점 격리 연동 시험을 우선 수행하고 결함은 같은 작업에서 수정·delta 회귀시험해줘. 최종 리뷰용 CoWork 소스/ZIP을 GitHub PRIVATE review-inputs/<review_id>/에 실제 업로드하고 원격 ZIP raw bytes/SHA·파일별 고정 commit URL을 검증해줘. 이미 유효한 명시 리뷰 비용/모드/요청 승인이 존재하면 별도 Claude 독립 리뷰 1회와 결과·영수증 게시까지 진행하고, 없으면 리뷰 준비만 완료한 뒤 PENDING_APPROVAL로 남겨줘. 그 때문에 다른 작업을 멈추지 마.

별도 signer PC/로컬 LLM/4축 ETW/3종 PAT 교체를 기본 요구하지 말고, 실운영 DB·Task·Notifier·Bridge/기존 요청 이력·운영 LIVE는 수정하지 마. 유료 모델/READY·새 PUBLIC ZIP 게시·LIVE cutover도 명시 승인 없이 하지 마.

최종 CLAUDE_GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT_FOR_GPT_20261114.md 하나와 CURRENT.md/TRACKER.json을 PRIVATE main에 게시하고 원격 readback 검증 후, 실제 남은 사용자 승인만 하나의 묶음으로 보고해줘.
```

## 4. 현재 완료 상태(이 문서는 인계 준비일 뿐)
`HANDOFF=PREPARED_AND_POSTED_PENDING_WINDOWS_EXECUTION`
`USER_REVIEW_SOURCE_TRANSFER=AUTHORIZED`
`WINDOWS_EXECUTION=NOT_RUN`
`SOURCE_ZIP_UPLOAD=NOT_RUN`
`INTEGRATION_E2E=NOT_RUN`
`INDEPENDENT_REVIEW=NOT_RUN`
`LIVE=NOT_APPROVED`
`ACTIVE_PROVIDER=NONE`
`MIGRATION_NOT_CUTOVER`
