# Windows Claude Code — CoWork P1/P2 정식 독립 리뷰 제출·검증 원샷 r0001

- 날짜: 2026-11-22 KST; 기존 Work `COWORK-SKILL-DISCOVERY-20261112-001`
- 정본: GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab`, branch `main`; 실제 제출 스킬/서비스는 **이 저장소의 기존 CoWork GitHub reviewer watcher**
- 사용자 최신 명시 지시: **“협업 다시확인후 정식 리뷰요청해줘”**. 2026-11-20의 구현 단계 리뷰 SKIP과 구 P1 DESIGN R1 BLOCKED는 이력으로 보존. 이번에는 **새 대상 P1/P2 코드+검증 계획** 독립 리뷰 **1건**, 모델 최대 1회, 신규 요청 한 건 USD 3 상한.
- 기존 prepublication 계약: `collab/ops/CONTRACTS/PRE_READY_SOURCE_PIN_PREFLIGHT_V1.md` r0003 및 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`
- 사전 정책·원본 검증기: `collab/ops/review_request_gate.py`
- 표준 게시기: `collab/ops/submit_review_request.py` (기본 드라이런, `--publish`만 Commit A/B 전송)
- 임의 GitHub 직접 쓰기로 `collab/requests/` 게시하거나 YAML의 `state: SUBMITTED`만으로 공식 요청 접수라고 보고하는 행위 금지

## 0. 고정 입력 및 기존 이력 확인

이번 **정확히 한 개**의 새 ID: `REQ-COWORK-P1P2-CONTEXT-CODE-R1-20261122` / rev 1.

- REQUEST 원본(비실행 초안): `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_FORMAL_REVIEW_REQUEST_UNPOSTED_DRAFT_r0001_20261122_KST.md`
- Base64 ZIP 원본(비트리거 후보): `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_REVIEW_CANDIDATE_r0001_1122.zip.base64`
- 복원 ZIP 파일명: `cowork_p1p2_context_review_input_r0001_1122.zip`
- ZIP 크기 **94,843 bytes**, SHA-256 **`35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3`**.
- 10개 member (기존 source/문서 8 + MANIFEST/README), ZIP stored+CRC/상대경로 검증. 소스별 Git blob SHA는 ZIP 안 `MANIFEST.json`. 실제 Windows에서 decode 후 SHA·CRC를 반드시 독립 검증.
- 요청 및 리뷰/영수증 기존 ID 3곳, 보호 signer DB/claim/UNCERTAIN 상태까지 중복 확인. **기존 P1 설계 R1을 재서명/재큐잉하지 않음**.

## 1. Windows 입력 복원 (정본 read-only, 임시 폴더만 허용)

1. 기존 CoWork repo checkout에서 원격이 `wonhwipark/CoWork-Skill-Collab` / `main`이고 안전한 origin인지 확인. 로컬 `git status --porcelain`이 비어 있는지, `git rev-parse HEAD`와 `git ls-remote origin refs/heads/main`이 일치하는지 확인. 다르면 **제출 중단**, 리포지토리 충돌·기존 변경을 자동 reset/force하지 않음. 최신 GET 후 운영자가 정상 동기화를 별도 처리.
2. 체크아웃 밖 임시 위치에 위 candidate base64와 REQUEST 원문을 **Git의 원본 bytes 그대로** 복원. PowerShell 환경의 UTF-8 BOM/자동 줄바꿈 변조를 피하기 위해 다음 Python 코드 예시 사용 (임시 폴더 경로는 호스트에서 설정).

```powershell
$env:COWORK_REVIEW_TEMP = '<OUTSIDE_REPO_TEMP_DIR>'
python -c "import os,base64,pathlib,subprocess,hashlib,zipfile; p=pathlib.Path(os.environ['COWORK_REVIEW_TEMP']); p.mkdir(parents=True,exist_ok=True); b=subprocess.check_output(['git','show','HEAD:collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_REVIEW_CANDIDATE_r0001_1122.zip.base64']); z=base64.b64decode(b.strip(),validate=True); f=p/'cowork_p1p2_context_review_input_r0001_1122.zip'; f.write_bytes(z); assert len(z)==94843 and hashlib.sha256(z).hexdigest()=='35de54934944807518e0141daaedde1888a42c08c1d264584e9b341f65dcd5f3'; a=zipfile.ZipFile(f); assert a.testzip() is None and len(a.infolist())==10; d=subprocess.check_output(['git','show','HEAD:collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_FORMAL_REVIEW_REQUEST_UNPOSTED_DRAFT_r0001_20261122_KST.md']); (p/'REQUEST.md').write_bytes(d); print('PREPARED_CANDIDATE_BYTES_ONLY')"
```

3. 위 출력만으로 승인/요청/모델 실행은 확인되지 않음. 원본 ZIP과 초안의 완전 동일 바이트를 정식 입력으로 사용. 임의 수정·다른 버전 ZIP 교체 금지.

## 2. Windows 정책 선검사 — FAIL CLOSED

1. 실제 운영 설치 `reviewer.config.json` 위치·현재 v0.2.29 여부·단일 `POLICY-STATIC-V1` USD3를 **Windows에서 read-only** 확인. 과거 GitHub 보고만으로 판단하지 않음.
2. `skill_id=cowork-context-design`의 실제 보호 위임 allowlist를 읽기 전용 확인. 과거 보고상 허용 목록 밖이므로 `--approval-route manual` 기본 사용. **자동 승인 수용을 위해 `skill_id` 바꾸거나 위임/키/설정을 수정하지 말 것.** 이번 단일 REQUEST에 대한 실제 Windows **공식 수동 signer 승인·서명 자격**이 검증되지 않으면 서명/READY/모델 호출 0. 유효한 기존 승인 범위 밖의 추가 비용/변경은 진행하지 않음.
3. `python collab/ops/review_request_gate.py select --live-config <ACTUAL_WINDOWS_LIVE_CONFIG> --intent unified --required-budget-usd 3.00`; 반드시 실제 `POLICY_COMPATIBLE_NOT_APPROVED`.
4. `python collab/ops/review_request_gate.py check --live-config <ACTUAL_WINDOWS_LIVE_CONFIG> --intent unified --required-budget-usd 3.00 --request <OUTSIDE_REPO_TEMP_DIR>/REQUEST.md --package <OUTSIDE_REPO_TEMP_DIR>/cowork_p1p2_context_review_input_r0001_1122.zip`; 반드시 `PASS_PREPUBLICATION_ONLY`.
5. `collab/requests/<ID>/REQUEST.md`, `SOURCE_PIN.json`, `APPROVAL_SIG.json`, `READY.md`, 기존 reviews/receipts와 Windows DB/영수증 중복·불확실/만료 상태를 확인. 스킬 범위/예산/원본이 하나라도 불일치하면 `BLOCKED`로 종료. **Commit A 이전** 아무 정식 REQUEST도 쓰지 않음.

## 3. 정확한 입력으로 정식 제출 (조건부 자동 연속)

- 모든 선행 검사 PASS 및 Windows 공식 보호 승인 범위가 유효한 경우에만 아래 단일 표준 도구를 사용:

```powershell
python collab/ops/submit_review_request.py --repo-root . --request-draft "<OUTSIDE_REPO_TEMP_DIR>/REQUEST.md" --package "<OUTSIDE_REPO_TEMP_DIR>/cowork_p1p2_context_review_input_r0001_1122.zip" --live-config "<ACTUAL_WINDOWS_LIVE_CONFIG>" --approval-route manual
# status=PREPUBLICATION_PASS_NOT_SUBMITTED일 때만 동일 인자에 --publish 추가
python collab/ops/submit_review_request.py --repo-root . --request-draft "<OUTSIDE_REPO_TEMP_DIR>/REQUEST.md" --package "<OUTSIDE_REPO_TEMP_DIR>/cowork_p1p2_context_review_input_r0001_1122.zip" --live-config "<ACTUAL_WINDOWS_LIVE_CONFIG>" --approval-route manual --publish
```

- `SUBMITTED_AWAITING_PROTECTED_SIGNER` = **정식 REQUEST+ZIP Commit A 및 PIN Commit B 원격 게시/검증까지만**. `SOURCE_PIN.repo_id`는 반드시 문자열 `"1451933830"`. 실제 signer의 별도 승인, 승인 범위/비용·중복·만료 검증을 통과한 경우에만 유효한 서명을 생성하고 `READY.md`를 **마지막** 게시.
- watcher가 이 **한 건만** 독립 STATIC_ONLY Claude 리뷰 최대 1회 실행. 결과+영수증의 요청 ID/rev/ZIP SHA/실비용/처리키/중복 0/모델 호출을 대조. UNCERTAIN 또는 게시 실패는 **모델 재실행/재큐잉하지 않고** 근거/영수증 정산.
- 이전 UI/스킬 리뷰나 구 P1 요청의 모델 호출을 재사용하거나 과거 READY를 수정하지 않음. **새로운 운영 정책·위임 scope 변경·새 비용 상한 승인·Watcher/Actions 설치/운영 변경 불가**.
- 작업 결과·실제 판정은 원본 `collab/reviews/<ID>/REVIEW_RESULT_1.md`, `collab/receipts/<ID>/RECEIPT_1.md`와 기존 Work `CURRENT.md`에 게시, commit·remote 본문 SHA/bytes readback. 모델/Host 결과 미관측은 `NOT_RUN` 유지. 독립 리뷰 없는 개발자 자체시험을 `PASS`로 승격하지 않음.
- 기존 자동화에 의한 후속 GPT API 유료 자동 판정은 이번 요청에 포함되지 않음. 별도 비용 정책·운영 플래그 유지.

## 4. 호스트 전달 경계

**이 인계 파일 게시 자체는 watcher/Windows가 처리하는 REQUEST가 아니다.** GitHub public `main`의 문서가 Windows에 도착했다는 자동 ACK/트리거는 아직 검증되지 않음. 이 GPT 채팅에서 Windows 실행 명령을 직접 보낼 도구가 없으므로 실제 Windows Claude Code 세션/이미 허용된 로컬 Agent에게 아래 단일 자연어 요청으로 호출해야 함.

> `wonhwipark/CoWork-Skill-Collab` `main`의 `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_FORMAL_REVIEW_WINDOWS_ONE_SHOT_r0001_20261122_KST.md`를 읽고, 기존 Work의 P1/P2 독립 리뷰 REQUEST를 정책에 맞게 원샷으로 진행해줘. 먼저 ZIP/REQUEST 원본 복원·Windows LIVE 정책/보호 signer·중복 검사를 실측한 뒤, 허용될 때만 표준 제출기 Commit A/B → 유효 서명/READY 마지막 → Claude 리뷰 1회 및 영수증까지. 차단 시 변경·유료 호출 없이 원인만 해당 Work에 게시해줘.

**현 시점 판정:** `REVIEW_CANDIDATE=POSTED`, `FORMAL_REQUEST=NOT_POSTED`, `HOST_PREFLIGHT=NOT_RUN`, `HOST_RECEIPT=NOT_VERIFIED`, `MODEL_CALLS_BY_THIS_GPT=0`. Windows 실제 수행 증거 이전에 `REQUEST/READY/REVIEW=PASS`라는 메시지를 전송하지 않음.
