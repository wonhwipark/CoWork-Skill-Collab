# GPT 최초 판정 입력 축소 결정 및 코드 보완 — 2026-11-24 KST

## 상태·판정
- **DECISION=ACCEPT_WITH_CHANGE**: 기존 v0.2.35 완료 Claude 독립 리뷰의 최초 GPT 판정에 한해, 938,634바이트 패키지 텍스트 전체를 프롬프트에 합치는 설계를 폐기하고 검증된 패키지 전체 파일 목록·개별 SHA-256·요청서·완료 리뷰·영수증·릴리스 매니페스트 근거를 사용.
- **SOURCE_CHANGE=POSTED_READBACK_VERIFIED**; `HOST_PREFLIGHT=NOT_RUN_AFTER_CHANGE`, `ACTIONS_OFFLINE_TEST=NOT_VERIFIED`, `GPT_API_CALL=NOT_RUN`, `CLAUDE_REREVIEW=NOT_RUN`, `WINDOWS_LIVE=UNCHANGED`. 코드와 시험 작성·게시만 완료, 실행·호출/판정 완료 아님.
- 기존 승인/서명/READY/REQUEST·보호 키/변수·실운영 DB·Windows watcher·Notifier는 변경하지 않음. 기존 유료 요청 재실행·자동 재시도·신규 claim 발행 없음.

## 결정 이유
- Windows 호스트의 2026-11-24 원본 보고: `v0_2_35_intent_scope_candidate.zip` 114항목, 109개 텍스트, 원문 합계 938,634바이트; `MAX_SOURCE=110,000`을 828,634바이트 초과.
- 실제 ZIP 바이너리의 중앙 디렉터리 별도 확인: 307,418바이트 / 114항목 / 텍스트 109개 938,634바이트, `v0_2_35/docs/RELEASE_MANIFEST.json` 19,476바이트. 이 중앙 디렉터리 조회만으로 서명·ZIP 내부 SHA·CRC를 재검증했다는 뜻은 아님.
- GPT의 역할은 이미 수행된 **Claude 독립 리뷰의 증거 기반 판정**이지 938KB 전체 소스를 처음부터 다시 독립 리뷰하는 것이 아님. 입력 상한을 증설하지 않고, 전체 원본 무결성 검증을 유지한 채 모델 전달 자료만 축소.
- 패키지 파일별 SHA 인벤토리는 소스 의미나 코드 correctness를 검증하는 증거가 아님. baseline diff는 제공되지 않으므로 **미검증으로 명시**. 새 판정 모델에게 코드 자체 검증·diff 확인을 주장하지 않도록 지시.
- 별도 패키지로 리뷰 대상 변경 금지. 동일 `REQ-COWORK-V035-WATCHER-REVIEW-20261123` 1회만 대상으로 유지.

## 실제 수정
1. `collab/tools/gpt_disposition_actions.py`: 전체 ZIP의 크기·SHA·경로/심볼릭 링크·member 수/압축 해제 상한·CRC 검사 유지. 모든 비디렉터리 항목을 읽어 크기·SHA-256 인벤토리화하고 모든 텍스트에서 잠재 Secret 문자열을 검사. 소스 본문 전체 모델 전달을 제거. 릴리스 매니페스트 원문 포함, 매니페스트 32KB·직렬화 증거 110KB·총 입력 140KB 상한 유지. 길이 초과 시 자동 절단하지 않고 HOLD. 코드 리뷰 재검증 범위 제한을 모델 지침에 추가.
2. `collab/tools/tests/test_gpt_disposition_actions.py`: 원본 예시 시험 수정, 텍스트 950KB ZIP 검증·전체 파일 인벤토리, 포함하지 않는 텍스트의 Secret 탐지, 매니페스트 초과 차단, **v0.2.35 실제 원격 ZIP** 회귀 fixture 추가. 시험 자체는 Actions/호스트 결과 필요.
3. 다른 GPT 비용 게이트, 워크플로 스위치/호출, 승인 검증, Telegram 코드 변경 없음.

## 게시·readback 근거
- 코드 게시: `a98e3d7527e71964b8fbb872f885afee0c044359` → 지침/정리 `486ac057c93fd686b14401c6f00b5b64725d381e` → 근거 한계 보강 `f32680b57993fb7ea7d1e9f7f5a4338f87a4b822`.
- 시험 게시: `afef6adba47f7fd0e64528d09405e551cda4b6f3` → 실제 ZIP 회귀 fixture `6c99b6c0046828713891abd2f06774caa3efd7f9`.
- 최종 코드 Git blob: `246af9e910c7498ba98492c30a9865e60ea97402`; 시험 Git blob: `4c45afab2507034811a240850afca5374da9e588`. **Git blob SHA-1은 파일 SHA-256이 아님**.
- 두 수정 파일 각각 GitHub main 원격 본문 바이트 readback 일치. 온라인 워크플로 Run ID/실제 PASS는 이 단계에서 확인하지 못했으므로 미검증으로 유지.

## 운영 안전 재개
1. 먼저 Windows Claude Code 또는 GitHub 무과금 오프라인 시험으로 수정된 소스·시험을 실제 실행. `test_real_v035_package_inventory_preflight_without_network` 포함 PASS 확인; 완료 서명/REQUEST/READY/pin과 원본 패키지의 **실제 preflight 재실행**이 PASS여야 함. Windows git clone은 `core.autocrlf=false`; 공개키 변수는 이전에 검증된 원본 사용.
2. `COWORK_GPT_MODEL=BLOCKED_MODEL`은 **별도 해결 필요**. 사용자 지정 모델을 프로젝트 권한·Responses API JSON Schema 호환으로 확인하거나, 사용자 승인 후 기존 `OPENAI_API_KEY` GitHub Secret을 GitHub Actions 내에서만 사용해 `GET /v1/models` 모델 목록 읽기 전용 조회·민감값 비출력. 조회만으로 모델 실제 응답·구조화 출력 호환이 보장되는 것은 아님.
3. preflight PASS, 모델 확인, 기존 4개 결과·claim 여전히 404이면 보호 스위치/모델 경로 확인 후 **이전 승인 범위에서 완료 리뷰에 대한 GPT 최초 판정 1회만** 실행. 정확한 기존 인계 `GPT_API_TELEGRAM_ACTIVATION_ONE_SHOT_r0001_20261123_KST.md` 단계 5~10 준수. 불확실 호출시 재실행 금지. 판정 readback 후 Telegram 1회 영수증 검증.
4. 공개 저장소 과거 파일의 로컬 경로 언급은 별도 **노출 범위 분류** 대상으로 유지. 즉시 히스토리 재작성·리뷰 원본 수정·승인/서명 원본 변경을 하지 않음.

## 다음 한 행동
수정 코드의 **무과금 실제 오프라인 시험 + v0.2.35 서명 포함 preflight 재실행** 후 결과를 같은 Work에 게시. 모델 확인은 별도의 사용자 지정 또는 한 번의 read-only 조회 승인 후 진행. API/Telegram 스위치는 모두 미변경 유지.
