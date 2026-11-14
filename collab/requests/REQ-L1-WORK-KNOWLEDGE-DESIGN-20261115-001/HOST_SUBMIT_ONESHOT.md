# 정식 Work → Knowledge 리뷰 접수 원샷

- PRIVATE 저장소: wonhwipark/CoWork-Skill-Collab
- branch: main
- REQUEST: collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REQUEST.md
- 입력 manifest: collab/projects/L1-WORKSPACE-RAG-20261111-001/review-inputs/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REVIEW_MANIFEST.md
- 현재 상태: REQUEST 작성, 원격 게시 후 재조회 필요. 유효 승인 서명/READY/호스트 validator/모델 실행은 별도이며 이 문서로 완료 처리하지 않는다.

1. 최신 collab/START_HERE.md와 이관 CURRENT를 확인. 본 요청 때문에 watcher 운영 버전·설정/Task/DB·LIVE 상태를 변경하지 않는다. 기존 승인된 독립 리뷰 단발 경로를 재사용할 수 있으면 사용하고, 불가하면 정확한 blocker를 SUBMISSION_STATUS.json에 기록한다.
2. 이전 리뷰 ID L1-WORK-KNOWLEDGE-DESIGN-20261114-001 및 REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001의 디스패치/실행/결과를 확인. 실행 중·이미 완료·불확실하면 신규 모델 호출 0. 기존 결과만 정산한다.
3. REQUEST/ZIP/manifest를 같은 commit A에서 고정. ZIP raw bytes 28805 B / sha256 4ccede070d03e497a8d821fcabc8092c0d46045b245b64dabf023abc83daa417, CRC/경로/일반파일/기밀 검사. 논리 package_path를 GitHub collab/packages/로 기존 transport 매핑. 설계 전용 ZIP이 기존 검사에서 허용되는지 dry-run으로 확인. 미지원이면 우회·가짜 SKILL.md·운영 검사 완화 없이 BLOCKED_UNSUPPORTED_DESIGN_BUNDLE로 보고한다.
4. 이번 ID의 사용자 리뷰 요청은 확인되었음. POLICY-STATIC-V1 / USD 1 이하 / 1회에 대해 현재 호스트 승인 절차에서 유효한 비용 권한과 기존 신뢰 서명자를 확인. 다른 작업의 승인을 전용하지 않는다. 비용 권한/서명 접근 불가면 해당 사유로만 BLOCKED, 유료 호출 0. 새 키/토큰 생성·전송 금지.
5. 기존 공식 도구로 SOURCE_PIN.json(schema SKILL_COLLAB_SOURCE_PIN_V1, commit A, 실제 repo_id) 및 이번 요청/정책/ZIP/만료/모드/실행한도에 묶인 APPROVAL_SIG.json을 작성·검증. repo ID 1451933830은 과거 관측값일 뿐 새 서버 조회·현재 신뢰 루트 검증을 대신하지 않는다.
6. 원격 readback 후 기존 READY schema로 READY.md를 **마지막에** 게시. request_path=/SKILL-COLLAB/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REQUEST.md, 실제 REQUEST sha256 및 package sha256, 현재 호스트 active_baseline_id 사용. 승인/기준값을 추정하지 않는다.
7. 최신 실제 watcher validator dry-run, 승인·입력·한도·중복 모두 통과한 경우 기존 승인된 격리 단발 경로에서 독립 리뷰 1회. 상시 watcher/자동 백그라운드 작업 활성화 금지. 운영 DB/스케줄/Telegram 설정 변경 금지. 단발 경로를 실제로 사용할 수 없으면 READY/실행 상태를 정직하게 보고.
8. 엔진 결과/영수증/디스패치를 PRIVATE main에 게시, 원격 재조회·실제 바이트/해시 확인. 사용량·호스트 실행 ID는 실제 관측값만 기록. 결과/업로드 장애로 모델 재호출 금지.
9. collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/SUBMISSION_STATUS.json, 해당 프로젝트 CURRENT/TRACKER의 이번 리뷰 요약만 갱신. CL/PR 패치/회귀·배포와 다른 리뷰 상태는 보존. 결과 후 설계·코드·지식·운영에 추가 반영하지 않고 GPT 판정을 기다린다.

실행 문구:
PRIVATE wonhwipark/CoWork-Skill-Collab의 main에서 collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/HOST_SUBMIT_ONESHOT.md를 읽고, 기존 정식 승인·REQUEST/READY 계약으로 이 설계 리뷰 1회를 접수·실행하고 결과/영수증 원격 readback까지 진행해줘. 이미 실행 중/완료/불확실이면 재호출하지 마. 서명·비용 권한 또는 실행 경로가 없으면 정확한 blocker만 기록해줘.
