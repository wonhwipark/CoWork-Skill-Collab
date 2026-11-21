# CoWork REVIEW REQUEST/PIN/ZIP 게시 전 필수 정합성 검증 V1

- 제정: 2026-11-21 KST
- 직접 원인: `REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121`의 SOURCE_PIN이 **ZIP만 있는 커밋**을 참조했고, 해당 커밋에 REQUEST가 없어서 Windows watcher가 `COMMIT_UNREADABLE / WAIT_INPUT`으로 정지.
- 추가 원인: `skill_id=knowledge_analysis_preflight`가 실제 자동 위임 허용 집합에 없음. 자동 signer가 허용되지 않는 요청을 수동 승인 없이 실행할 수 없음.
- 효력: **신규 리뷰 요청을 게시·서명·READY 처리하는 GPT/Windows Claude Code의 절차 계약**. 이 MD와 Python helper의 게시만으로 Windows 운영 watcher의 실제 preflight 로더/호출 경로가 변경되는 것은 아님. 운영 자동 연동 여부는 별도 G0 검증.

## 자연어 정식 리뷰의 표준 제출 명령 (r0002 / 2026-11-21)

**신규 요청 기본 경로:** 실제 Windows LIVE 정책을 검증할 수 있는 환경에서 `collab/ops/submit_review_request.py`를 사용한다. 이 제출기는 기존 `review_request_gate.check_request`, `source_pin.dumps_source_pin`, `review_pin_preflight.inspect`를 **연속 호출**하고, 요청 생성에 필요한 Commit A/B를 안전하게 `git push`한다. `--publish`가 없으면 원격/로컬에 쓰지 않는 드라이런이다. 안전성 위해 클린 `main`·신뢰 `origin`·원격 최신 SHA·새 REQUEST ID를 강제한다. 인증 토큰·보호 서명·READY는 절대 생성하지 않는다.

예시(Windows, 실제 설치 LIVE 설정 경로는 호스트 확인 후 지정):

```powershell
python collab/ops/submit_review_request.py --repo-root . --request-draft <OUTSIDE_REPO>\\REQUEST.md --package <OUTSIDE_REPO>\\skill.zip --live-config <WINDOWS_LIVE_CONFIG_PATH>
# 모든 게이트 검증 성공한 경우에만, 동일 인자로 --publish 추가
python collab/ops/submit_review_request.py --repo-root . --request-draft <OUTSIDE_REPO>\\REQUEST.md --package <OUTSIDE_REPO>\\skill.zip --live-config <WINDOWS_LIVE_CONFIG_PATH> --publish
```

**성공 판정 경계:** `PREPUBLICATION_PASS_NOT_SUBMITTED` = 미게시, `SUBMITTED_AWAITING_PROTECTED_SIGNER` = REQUEST+ZIP·PIN 원격 게시/검증까지, 정식 실행/서명 아님. 프로그램이 `FORMAL_REVIEW_SUBMISSION_BLOCKED`를 출력하면 명시적으로 실패, **자동 재시도 금지**, 원격 Commit·보호 signer·DB·중복/UNCERTAIN 판정 후 새 revision을 선택. 자동 위임 허용 여부는 게시기의 `approval_mode=manual` 형식 무결성 검사로 입증되는 것이 아니며 **Windows 공식 보호 signer가 별도 확인**한다.

**중요 제한:** 신규 보조 코드는 GitHub 저장소에 게시됐지만 Windows PC에서 실행/설치 확인 전이다. 단일 명령을 우회한 GitHub API 직접 게시·다른 GPT/Agent에 대해 저장소 수준 강제 브랜치 보호를 활성화한 것은 아니다. 실제 운영 signer 연결/강제 status check는 운영 변경 승인과 실측 후에만 PASS로 판정한다. 기존 R1/R2의 서명·READY·실행 상태는 그대로 보존한다.

## 예방 조치와 담당

| 항목 | 필수 행위 | PASS 기준 | FAIL/불확실 |
|---|---|---|---|
| 0. 시작 전 승인 분류 | 대상 skill_id, 실제 로드된 delegation scope, 비용 정책·만료 확인 | AUTO 허용 여부 또는 MANUAL 한정 분류 | 자동 전환/스킬 명의 우회 금지 |
| 1. 고정 패키지 | 안전한 ZIP의 CRC/경로/파일 SHA·크기 검증 | exact package sha256, bytes, Git blob | 게시 중지 |
| 2. Commit A | **같은 commit tree**에 정확한 REQUEST.md와 패키지 ZIP이 존재하도록 게시 | A에서 REQUEST/ZIP 둘 다 READBACK, REQUEST 실제 바이트 고정 | PIN 만들지 말 것 |
| 3. SOURCE_PIN | **A를 commit으로 지정**하고 repo_id를 **문자열**로 직렬화 | `source_pin.py check` / main readback | READY·서명 금지 |
| 4. Commit B와 READBACK | PIN은 뒤 커밋 B에 게시. 확인된 최신 main과 **PIN이 가리킨 A**를 비교 | A의 REQUEST와 B/current REQUEST 동일 바이트, ZIP SHA/크기 일치 | `COMMIT_UNREADABLE` / `REQUEST_BYTES_CHANGED` 등 BLOCK |
| 5. 승인 | AUTO=실제 로드 scope 적합 여부 / MANUAL=정식 보호 signer 자격·예산·사용자 범위 | signer의 실제 APPROVAL 검증 | 사용자 발화/MD만으로 서명 PASS 불가 |
| 6. READY | 유효 서명·중복/UNCERTAIN·정책 검사 후 **맨 마지막 새 파일로** 게시 | watcher가 1회 처리/결과+영수증 | fail-closed, 모델 0 |
| 7. 사후 | 결과·영수증·비용·모델 호출·중복 원격 대조 | GPT 판정 후 승인된 배포 | 미검증은 NOT_RUN |

## 읽기 전용 개발/현장 검증 도구

- 코드: `collab/ops/review_pin_preflight.py`
- 회귀: `collab/ops/tests/test_review_pin_preflight.py` (합성 git 저장소 15건 직접 PASS; R1 잘못된 commit/REQUEST 변조/ZIP 변경/숫자 repo_id/미허용 자동 skill/READY 재큐잉 등 포함)
- Python 표준 라이브러리 + Git + 기존 `collab/ops/source_pin.py`; **네트워크/쓰기/승인/서명/READY/LLM 호출 없음**.
- **실행 전:** 로컬 Git 체크아웃에 최신 원격 main commit과 참조하는 A commit을 `git fetch`하여 확보. `--main-commit`에 **실제 원격 main에서 별도 조회·검증한 전체 SHA**를 입력. helper는 오프라인 검증이므로 로컬 HEAD가 원격 최신인지 스스로 입증하지 못함.

예시 (R2, 한정 MANUAL 승인 분류 — 명령은 읽기 전용):

```bash
python collab/ops/review_pin_preflight.py \
  --repo-root . \
  --main-commit <LIVE_REMOTE_MAIN_40HEX_SHA> \
  --request-id REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121 \
  --package-repo-path collab/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip \
  --expected-repo-id 1451933830 \
  --approval-mode manual
```

- `status=PASS_PINNED_INPUTS_ONLY`은 **커밋·REQUEST·ZIP 바이트 정합성만 PASS**를 뜻함. `signer_authority=NOT_VERIFIED`, `ready_or_model_calls=0`은 의도된 보호 결과.
- 자동 승인은 반드시 **현장 보호 위임의 실 로드 allowlist**를 `--delegated-skill`로 전달하여 `--approval-mode auto`로 검사. 공백 allowlist나 skill 미허용은 BLOCK. 임의 allowlist 전달은 정식 signer 검증을 대체할 수 없음.
- EXIT 2/`REVIEW_PIN_PREFLIGHT_BLOCKED`이면 서명/READY/모델 호출 0. 기존 R1 또는 이미 서명·READY·결과가 있는 요청은 **새로 처리하지 말고 처리키·DB·영수증 상태를 재조회**. 실제 실패시 재실행하지 않음.
- 저장소 병합·branch SHA·원격 readback과 **Windows 운영 보호 signer, 실제 승인·정책·비용·중복 검증은 별도**다.

## 운영 반영 방법

- GPT/Claude 요청 게시자: **신규 요청마다 Commit A 검증·Commit B preflight를 필수**로 한다. 계열 작업의 기존 R1 실패 재발 방지.
- Windows signer/watcher: 다음 승인된 운영 변경 시 **실제 signer 직전의 필수 호출 게이트**로 연결하고, 원격/DB 상태와 일치하는지 SHADOW·실제 테스트로 검증. 현재 LIVE 설치·예약 작업·키·위임·DB·정책은 변경하지 않음.
- 이전 잘못된 요청을 조용히 고쳐 READY 처리하는 대신 새 ID/revision을 만들고 구 이력은 보존.

## 관련 Work

- `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`
- `collab/projects/L1-WORKSPACE-RAG-20261111-001/KNOWLEDGE_PREFLIGHT_R1_PIN_FAILURE_R2_TRANSPORT_CORRECTION_r0001_20261121_KST.md`
- R2: `collab/requests/REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121/REQUEST.md` 및 `SOURCE_PIN.json`
