# 정식 Work → Knowledge 리뷰 접수 원샷

- PRIVATE 저장소: wonhwipark/CoWork-Skill-Collab
- branch: main
- REQUEST: collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REQUEST.md
- 입력 manifest: collab/projects/L1-WORKSPACE-RAG-20261111-001/review-inputs/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REVIEW_MANIFEST.md
- 현재 상태(2026-11-15 사전 검증 후): REQUEST·ZIP·manifest·SOURCE_PIN 게시/readback PASS, 운영 v0.2.20 Validator 격리 시험 PASS(설계 ZIP/REQUESTED 수용). APPROVAL_SIG·READY는 미게시, 모델 호출 0. GitHub LIVE watcher는 운영 중이며 READY 없음으로 WAIT_INPUT을 기록. 판정 근거는 프로젝트 GPT_REQUEST_VALIDATOR_PREFLIGHT_DISPOSITION_r0001_20261115.md.

1. 최신 collab/START_HERE.md와 이관 CURRENT를 확인. 현재 ACTIVE_PROVIDER=GITHUB 단일 LIVE(호스트 보고)이며 이번 요청 때문에 watcher 운영 버전·설정/Task/DB·LIVE 상태를 변경하지 않는다. 리뷰의 실행자는 기존 LIVE watcher이며, 새 격리 단발 reviewer 실행이나 중복 watcher 시작은 하지 않는다.
2. 이전 리뷰 ID L1-WORK-KNOWLEDGE-DESIGN-20261114-001 및 REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001의 디스패치/실행/결과를 확인. 실행 중·이미 완료·불확실하면 신규 모델 호출 0. 기존 결과만 정산한다.
3. 이미 고정된 Commit A `0a46fea5f7f63c68c5cb12cfa35bfaed00c2c1a3`의 REQUEST/ZIP/manifest 및 GitHub main readback 결과를 재확인(원본 수정/재게시 불필요). ZIP raw bytes 28805 B / SHA-256 4ccede070d03e497a8d821fcabc8092c0d46045b245b64dabf023abc83daa417, CRC·경로·비밀 검사 및 설계 문서 5개 수용은 운영 v0.2.20의 실제 Validator 격리 시험 PASS. SKILL.md 추가·Validator 완화 금지.
4. 이번 ID의 사용자 리뷰 요청은 확인되었음. POLICY-STATIC-V1 / USD 1 이하 / 1회에 대해 현재 호스트 승인 절차에서 유효한 비용 권한과 기존 신뢰 서명자를 확인. 다른 작업의 승인을 전용하지 않는다. 비용 권한/서명 접근 불가면 해당 사유로만 BLOCKED, 유료 호출 0. 새 키/토큰 생성·전송 금지.
5. 기존 SOURCE_PIN.json(schema SKILL_COLLAB_SOURCE_PIN_V1, commit A, repo_id=1451933830)은 실제 Validator에서 정상 수용됐으므로 덮어쓰지 않는다. Windows에서 실제 GitHub repo ID와 신뢰 루트를 재조회하고 이번 요청/정책/ZIP/만료/모드/1회 한도에 묶인 APPROVAL_SIG.json만 **해당 요청의 별도 유료 비용 승인(최대 $1)이 실제로 확인된 후** 기존 공식 서명 도구로 작성·검증한다. 다른 작업의 서명을 재사용하지 않는다.
6. 원격 readback 후 기존 READY schema로 READY.md를 **마지막에** 게시. request_path=/SKILL-COLLAB/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REQUEST.md, 실제 REQUEST sha256 및 package sha256, 현재 호스트 active_baseline_id 사용. 승인/기준값을 추정하지 않는다.
7. **READY가 게시되면 이미 운영 중인 GitHub 단일 LIVE watcher가 다음 30초 주기에 자동으로 검증·디스패치한다.** 별도 격리 단발 reviewer/Watcher를 시작하거나 운영 Task·DB/스케줄/Telegram을 변경하지 않는다. 모델 호출 1회·비용 상한 $1·중복/서명/비용/만료 게이트를 적용한다. 허용된 정식 서명이 없으면 READY 게시하지 않고 WAIT_INPUT 유지·모델 호출 0. 유효한 상태에서 중복/불확실 발생 시 fail-closed 재실행 0.
8. 엔진 결과/영수증/디스패치를 PRIVATE main에 게시, 원격 재조회·실제 바이트/해시 확인. 사용량·호스트 실행 ID는 실제 관측값만 기록. 결과/업로드 장애로 모델 재호출 금지.
9. collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/SUBMISSION_STATUS.json, 해당 프로젝트 CURRENT/TRACKER의 이번 리뷰 요약만 갱신. CL/PR 패치/회귀·배포와 다른 리뷰 상태는 보존. 결과 후 설계·코드·지식·운영에 추가 반영하지 않고 GPT 판정을 기다린다.

실행 문구:
PRIVATE wonhwipark/CoWork-Skill-Collab main의 collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/HOST_SUBMIT_ONESHOT.md를 읽어줘. Validator 결과는 PASS이고 REQUEST/ZIP/SOURCE_PIN은 원본 그대로 유지해. 이번 리뷰 ID의 유료 비용 승인(최대 $1 1회)이 명시적으로 확인된 경우에만 기존 서명자로 APPROVAL_SIG.json을 생성·원격 readback 후 READY.md를 마지막에 게시해줘. 이미 실행 중/완료/불확실하면 재호출하지 말고 정산만 해줘. READY 후 기존 LIVE watcher가 자동 디스패치하므로 별도 watcher나 모델 리뷰 세션을 중복 기동하지 말아줘. 결과/영수증 원격 readback 및 SUBMISSION_STATUS/CURRENT/TRACKER 갱신까지. 비용 권한/서명 검증 불가면 READY 없이 BLOCKED로 기록해줘.
