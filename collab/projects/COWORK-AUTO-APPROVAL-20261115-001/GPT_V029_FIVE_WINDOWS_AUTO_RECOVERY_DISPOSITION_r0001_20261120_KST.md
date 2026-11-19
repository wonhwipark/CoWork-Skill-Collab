# v0.2.29 — 5개 창 연속 요청 자동 복구 원칙 및 격리 모델 시험

- 2026-11-20 KST · PRIVATE wonhwipark/CoWork-Skill-Collab/main · 기존 Work COWORK-AUTO-APPROVAL-20261115-001
- 기준 ZIP: artifacts/v0_2_29/skill-collab-watcher_v0_2_29_1120.zip / SHA-256 c67bc342fe77547b000fc42e1b886396cbef035c0d265dbcd124947e267ed83f
- 기존 결과: GPT_V029_FIVE_CHAT_WINDOWS_SEQUENTIAL_REQUEST_SIMULATION_r0001_20261120_KST.md
- 결정: 차단만 하는 것이 아니라, 기존 Work/Git writer/Watcher 역할 안에서 자동 복구할 수 있는 것은 복구하고 보호 승인·유료 결과 불확실성만 선택적으로 멈춘다.

## 1. 오류별 복구안

| 상황 | 해결 계약 | 중단 조건 |
| --- | --- | --- |
| 스킬 수정 3건이 같은 이전 source SHA 사용 | 같은 skill의 최종 패키징·리뷰를 직렬화. 리뷰 REQUEST 확정 전에 최신 원본 HEAD/SHA 재조회 → 이전 변경 반영한 새 후보로 rebase → 관련 시험 → 정확한 ZIP·SHA 고정. 새 SHA를 독립 검토한 뒤 그 바이트만 게시 | 동일 의미 영역의 비자동 병합 충돌은 해당 Work만 NEEDS_DECISION |
| 공유 CURRENT.md/TRACKER.json 갱신 충돌 | GitHub 기존 blob-SHA CAS 사용. 충돌 시 최신 원격 재읽기 → 다른 Work의 변경 무손실 병합 → 새 SHA로 최대 3회 유한 재시도 → 원격 readback. 마지막 쓰기로 이전 값 덮어쓰기 금지 | 게시 readback 불일치 또는 충돌 반복 시 해당 게시만 보류; 모델/분석 재호출 금지 |
| REQUEST ID 중복 | GitHub 고정 REQUEST 게시 이전에만 새 고유 ID 할당·원본 hash/pin 재생성. 게시·서명·READY 이후 ID는 불변 | 이미 게시된 ID는 rename/overwrite 금지; 새 공식 REQUEST·승인 범위 필요 |
| 결과·영수증 송신 불확실 | 기존 watcher DB + remote result/receipt/dispatch 정확한 processing_key 및 SHA를 대조. 결과가 존재하면 결과 게시만 회복. 동일 결과 재실행 금지 | 실제 실행 여부 불확실하고 근거 미발견 시 UNCERTAIN 유지, 유료 재시도 0 |
| 앞선 동일 스킬 수정이 UNCERTAIN | 다른 skill/Work는 진행. 해당 skill의 후속 수정은 후보 보존하되 확정·유료 리뷰는 WAIT_DEPENDENCY | 불확실 결과를 증거 없이 자동 완료 처리 금지 |
| 레거시 DESIGN/보호 scope/비용 불일치 | REQUEST 게시 전 실제 설치 정책과 유효한 scope/상한을 확인. 허용된 신규 리뷰만 통합 STATIC/USD3 경로로 준비 | 구 REQUEST 수정·cap 자동 증액·권한 자동 확장 금지. AUTH_REQUIRED/WAIT_HOST_CONFIG |
| v0.2.29 POLICY_STOPPED | 비용 상한 때문에 영구 제외된 과거 요청을 새 cap으로 자동 소급 복구하지 않음 | 재실행 필요 시 별도 정상 수동 승인 경로 |

책임 분리: 코드 변경 재기준화/병합/공통 CURRENT·TRACKER 갱신은 기존 Work writer/Git 인터페이스. watcher는 고정 REQUEST/보호 서명/READY/중복·비용·영수증·UNCERTAIN 담당. watcher가 코드 내용을 임의 병합하거나 유료 재호출하지 않음. 구현됐다고 가정하지 않고 기존 인터페이스를 먼저 조회한 후 입증된 gap만 최소 수정.

## 2. GPT 격리 SQLite 모형 5회 결과

- Linux Python 표준 SQLite + 가짜 remote·runner·source HEAD·shared CAS. 실제 v0.2.29 ZIP Python import 및 Windows watcher 실행은 NOT_RUN.
- 스크립트: cowork_5windows_auto_recovery_model_20261120.py / SHA-256 87490f5a38a987aafedb5dd51c0ec0ed5de30f72073c0b3b11800587e74e19d4 (ChatGPT 세션 sandbox 보존)
- 결과: cowork_5windows_auto_recovery_model_20261120.json / SHA-256 706c453da723ded8f2507adce2cddfaccce231c77d88cb6c59ed7c7c60d01bdd (ChatGPT 세션 sandbox 보존)
- 모의 패키지 고정 SHA는 리뷰 실행 전에 계산하고 결과 SHA와 일치한 후보만 실제 source에 반영하도록 시험.

| Run | 주입 조건 | 결과 | CAS 복구 / 재기준화 |
| --- | --- | --- | --- |
| 1 | 5개 창 순차, 같은 스킬 기준 원본 및 상태 SHA 중복 | 5/5 완료 | 4건 / 2건 |
| 2 | Run1 + 게시 전 REQUEST ID 충돌 | 5/5 완료, ID 재발급 1 | 4건 / 2건 |
| 3 | Run1 + 3번 창 UNCERTAIN, 정확한 원격 결과 존재 | 5/5 완료, 호출 반복 0 | 4건 / 2건 |
| 4 | 3번 창 UNCERTAIN, 원격 결과 미확인 | 독립 설계 2건 완료, 3번 불확실, 같은 스킬 4~5번 의존 대기 | 1건 / 0건 |
| 5 | ID 충돌 + UNCERTAIN 원격 결과 회수 | 5/5 완료, 호출 반복 0 | 4건 / 2건 |

추가 반례: 위임 scope에 없는 설계 2건은 AUTH_REQUIRED, 허용 스킬 3건만 처리. 동일 코드 필드 의미 충돌은 NEEDS_DECISION, 원래 변경 보존. 실제 모델 호출·호스트 서명·READY 게시·LIVE 설정 변경은 0.

판정: MODEL_RECOVERY_TEST=PASS_5_ROUNDS (4회 전원 완료, 1회 의도된 안전 대기). V029_ACTUAL_ZIP_5_WINDOWS_E2E=NOT_RUN. SIMULATION_PASS를 운영 PASS로 승격 금지.

## 3. 다음 하나의 수행

Windows Claude Code가 기존 스킬 writer·Git CAS·watcher recover/reconcile를 먼저 확인하고, 기존 v0.2.29 정확한 ZIP의 격리 Windows 가짜 signer/runner·DB에서 위 교차창 복구 시나리오를 기존 5회 사전검증 안에 넣어 재현한다. 실제 미지원 부분만 기존 Work에서 최소 보완·자체시험·후보 고정. 실패 전후 source/REQUEST/ready/receipt 원격 바이트, Work별 상태, mock caller 횟수, 비과금 증거를 남긴다.

실제 ZIP 5회 검증 전 정식 유료 리뷰·추가 REQUEST/READY/실제 모델 호출 0. LIVE v0.2.25 / 보호 위임 USD1 불변. 검증 후에도 별도 유효 승인·독립 리뷰·호스트 배포 게이트가 필요.

NEXT_ONE_ACTION: 기존 Work의 Windows Claude Code가 실제 v0.2.29 ZIP과 현재 Git writer의 복구 가능 기능을 대조하고 5창 복구 E2E를 무료 격리로 검증하여 결과·남은 GAP·원격 readback을 게시.
