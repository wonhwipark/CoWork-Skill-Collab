# CLAUDE L1 Workspace 로컬 뷰어 r0002 독립 리뷰 결과 (GPT 판정용)

- 작성: Windows Claude Code, 2026-11-18 KST. 근거: `HOST_SUBMIT_ONESHOT_150USD_AND_LIMIT_CLEANUP_20261118.md`. 사용자 명시 승인(USD 1.50, 1회)에 따라 끝까지 수행했다.

## 결론

**독립 설계 리뷰 1회 완료. 판정 `ACCEPT_WITH_CHANGE`. BLOCKING 3건(G2/G3 진행 전 해결 필요), 비차단 제안 4건.** 모델 1회, 비용 USD 0.6055119, 중복 0.

## 1. Prepublication gate (모델·쓰기 0)

- `select --intent skill --required-budget-usd 1.50` → `POLICY_COMPATIBLE_NOT_APPROVED / POLICY-STATIC-V1 / 1.50`.
- r0002 ZIP 재검증: 91,324 B, SHA-256 `6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f`(일치), CRC 정상.
- 고정 초안(`REQUEST_PREFLIGHT_DRAFT_LOCAL_VIEWER_R0002_150USD_20261118.md`) 원시 바이트로 `check` → **`PASS_PREPUBLICATION_ONLY`**, `request_sha256=cd488efff623cccb5c7c96982f823f1697606ff59a8ea744d9fe3a1699c22e46`.
- 중복 확인: 신규 ID는 원격에 REQUEST/PIN/SIG/READY 미존재, 로컬 `jobs` 테이블 0건.

## 2. 게시 체인

- Commit A: 사전검증한 바이트 그대로 `REQUEST.md` 게시(commit `0c3fce16ea4b`), 원격 재조회로 바이트 동일 확인(request_sha256 동일).
- `source_pin.py create --repo-id 1451933830 --commit 0c3fce16ea4b6c74d18519581526162beb49e915` → `check --expected-repo-id 1451933830` **PASS**. `SOURCE_PIN.json` 게시(commit `e8b91ab8e5cf`), 원격 바이트 동일.
- `approve_request.py check` 16/16 PASS(cap USD 1.5) → `approve --max-usd 1.5 --execute`: 서명(만료 2시간) → `APPROVAL_SIG.json`(commit `0000bd0a0aad`) → `READY.md`(마지막, commit `8d409d8eb181`). 둘 다 원격 바이트 동일.

## 3. 실행과 결과

- 감시기(v0.2.25) 1회: `CLAIMED → REVIEW_DISPATCHED(POLICY-STATIC-V1, max $1.5) → REVIEW_COST(USD 0.6055119, 11턴) → COMPLETED`.
- 원격 확인: `DISPATCH_1.md`(440 B), `RECEIPT_1.md`(357 B, `ok=true`), `REVIEW_RESULT_1.md`(13,189 B).

### 리뷰 핵심

- **판정 `ACCEPT_WITH_CHANGE`.** 전체 Workspace 기본 열람 + 사후 렌더링(전량 HTML 사전 변환 금지) 방향과 P0~P6/G0~G6 게이트 구조는 타당. 범위는 `PARTIAL_SCOPE`가 아니라 문서 전체 커버.
- **BLOCKING 3건 (G2/G3 진행 전 해결 필요):**
  1. **B1** Path containment 알고리즘이 구체화되지 않음 — "`../`·심링크 거부"만 서술, 정확한 canonicalize 시점·함수(`realpath`+`commonpath`) 미지정.
  2. **B2** 전체 기본공개 전환에 따른 콘텐츠 내부 비밀 탐지가 한 줄 서술뿐 — r0001의 사람 승인 allowlist를 없애면서 유일한 안전망이 약화됨. 스캔 실패/미실행 파일은 기본 403(fail-closed) 필요.
  3. **B3** MSC HTML sandbox의 "별도 origin"이 구현 수준에서 미정의 — 같은 도메인 다른 path로는 쿠키 scope 공유로 "별도 origin" 요건이 깨짐. 서브도메인 또는 iframe sandbox+쿠키 제한 중 하나를 G0에서 확정 필요.
- **비차단 4건:** 캐시 무효화/회수 정책 누락, PREVIEW/UNVERIFIED 배지가 전체공개 UI에 미반영, r0002 신규 파일 provenance pin 부재, ZIP 크기(91,324B)와 멤버 바이트 합(90,120B) 불일치(1,204B 차이, 확인 필요).
- 리뷰어 직접 명시: 이 리뷰는 **문서 정적 검토**이며 `review_request_gate.py`/`approve_request.py`/실제 Linux G0는 실행하지 않았다.

## 4. 요청 후 한도 설정 정리 (사용자 후속 지시)

- **이번 요청 전용 임시 override는 생성된 적이 없다.** `POLICY-STATIC-V1`이 USD 1.00→1.50으로 바뀐 것은 2026-11-18 앞선 **별도 승인 작업**(v0.2.25 운영 정책 맵 변경)에서 영구적으로 이뤄졌고, 이번 리뷰를 위해 임시로 만든 값이 아니다. 따라서 **원복할 임시 설정이 없다** — `TEMP_LIMIT_CLEANUP=NOT_APPLICABLE(사전에 생성된 임시 override 없음)`.
- 보호 경계는 지시대로 **전혀 건드리지 않았다**: `auto_delegation.json`의 `max_request_usd=1.0`(건당 보호 한도) 불변, `known_run_policy_refs`(비용 맵) 불변, 서명·SOURCE_PIN·READY·중복·만료 검증 로직 불변. 일·월 누적 상한은 이미 2026-11-17에 `null`(정책상 폐기)이라 추가로 지울 대상이 없음.
- 사용자의 "한도 관련 설정 삭제"는 **전역 보호 위임/서명 검증을 삭제하는 것으로 해석하지 않았다.** 이번 USD 1.50 승인은 이 요청 1건에만 적용됐고, 장래 호출에 대한 무제한 위임 확대로 쓰지 않았다.

## 5. 상태값

```
REQUEST_SHA=cd488efff623cccb5c7c96982f823f1697606ff59a8ea744d9fe3a1699c22e46
COMMIT_A=0c3fce16ea4b6c74d18519581526162beb49e915
SOURCE_PIN=PASS (repo_id string, commit match)
APPROVAL_SIG=PASS (commit 0000bd0a0aad)
READY=PASS (commit 8d409d8eb181, last)
REVIEW_RESULT=COMPLETED (commit 확인됨)
USAGE=total_cost_usd 0.6055119, num_turns 11, max_budget_usd 1.5
MODEL_CALLS=1
ACTUAL_COST=USD 0.6055119
TEMP_LIMIT_CLEANUP=NOT_APPLICABLE (해당 임시 override 없음)
PROTECTED_DELEGATION_CHANGED=False
```

## 다음 한 동작

GPT가 BLOCKING 3건의 수용 여부를 판정한다. 수용되면 B1~B3를 G2/G3 수용 기준에 반영한 r0003 설계로 이어가거나, 업무 GPT용 PUBLIC 작업지시서 게시 전에 이 세 가지를 먼저 구체화해야 한다.
