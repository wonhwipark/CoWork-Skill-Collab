# 자연어 정식 리뷰 제출기 — 리뷰 생략·Windows 원샷 적용 인계 r0001

- 대상 정본: GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab` / `main`
- Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- 대상: `collab/ops/submit_review_request.py` + `review_request_gate.py`, `review_pin_preflight.py`, `source_pin.py`
- 사용자의 최신 지시: 독립 리뷰 여부 확인 후, 미완료라면 별도 GPT 리뷰 판정·재요청 없이 가능한 배포를 원샷 진행
- 범위: **기존 코드의 Windows CoWork 체크아웃 반영·실제 정책/회귀 검증**. 유료 리뷰 요청·APPROVAL/READY·기존 R1/R2 재실행·watcher LIVE/DB/Task/키 변경은 범위 밖

## 1. 최신 결과와 중복 방지

2026-11-21 `main` 확인 기준, 표준 제출기 소스와 합성 8건 시험·자연어 진입 지침은 게시 완료. **이 변경을 입력으로 한 별도 Claude 독립 리뷰 결과/영수증 또는 Windows 운영 적용 증거는 확인되지 않음**. 사용자 지시에 따라 `INDEPENDENT_REVIEW=SKIPPED_BY_USER` (독립 리뷰를 완료로 표기하지 않음), `GPT_DISPOSITION=SKIPPED_BY_USER`. 신규 정식 REQUEST/서명/READY를 만들지 않는다. 기존 다른 R1/R2와 섞지 않는다.

## 2. Windows Claude Code 실행: 한 번에 확인·적용

**담당:** 이미 승인된 Windows Claude Code 작업 세션. **실행 대상:** Windows의 CoWork 로컬 체크아웃, NOT GitHub Actions Runner, NOT Linux MCP.

A. 작업 시작 전 대상 컴퓨터의 실제 CoWork 저장소 경로와 실제 LIVE `reviewer.config.json` 위치를 **로컬에서 식별**. 두 값/키/토큰은 공개 기록에 게시하지 않음. 현재 checkout이 `wonhwipark/CoWork-Skill-Collab`의 `main`인지, 변경 중인 파일·중복 실행·진행 중 요청이 있는지 확인. 변경 중이거나 신뢰 origin이 아니면 BLOCKED, 강제 reset/삭제/덮어쓰기 금지.

B. 실제 `main` fast-forward 갱신. PowerShell에서 경로는 **조회로 검증한 로컬 실경로**로 치환:

```powershell
$repo = '<VERIFIED_WINDOWS_COWORK_CHECKOUT>'
$live = '<VERIFIED_WINDOWS_LIVE_REVIEWER_CONFIG>'
git -C $repo status --porcelain
git -C $repo pull --ff-only origin main
powershell -NoProfile -File (Join-Path $repo 'collab/ops/windows_formal_review_submitter_rollout.ps1') -RepoRoot $repo -LiveConfig $live -Apply
```

**주의:** `git pull`은 저장소 변경이므로 B의 작업/정책 검증 후에만. 구 checkout의 스크립트 부재를 해소하기 위한 첫 fast-forward이며, 중복 배포나 요청 재전송이 아님. 원샷 helper는 origin/branch/clean/latest 확인 후 fast-forward만 허용, 기존 실제 모듈을 사용하는 제출기·PIN 회귀시험 및 `POLICY-STATIC-V1=USD3` 읽기 전용 정책 호환성 검증을 수행. **새 리뷰 요청을 만들거나 `--publish`를 호출하지 않음.**

C. 새 Windows Claude Code 세션에서 `CLAUDE.md`/imports 로딩을 `/context all`로 확인. 실제 자연어 명령 `정식 리뷰 요청`의 후속 흐름이 표준 제출기 사용으로 연결되는지, **유효한 사용자의 신규 입력 없이 요청 파일·서명·READY가 만들어지지 않는지** 확인. 실입력 ZIP/REQUEST가 없으면 `submit_review_request.py`의 실제 LIVE 드라이런은 `NOT_RUN`; 합성 시험을 실제 정책+실입력 E2E로 대체 표기하지 않음.

D. 실제 설치된 watcher signer 전 경로에 강제 검사 hook이 존재하는지 **읽기 전용 확인**. 단일 제출기 코드/프로젝트 지침 배포는 GitHub API 직접 게시를 시스템적으로 차단하지 않는다. 없는 경우 `HOST_HARD_ENFORCEMENT=NOT_APPLIED`로 남기고 운영 watcher·키·DB·Task·GitHub ruleset을 임의 변경하지 않음.

## 3. 성공·실패 판정 경계 (결과만 보고, 별도 GPT 리뷰 판정 생략)

| 항목 | 보고 값 |
|---|---|
| GitHub `main` 원격 코드 | `PUBLISHED`, 원격 blob/commit |
| Windows 실제 체크아웃 변경 | `APPLIED` / `BLOCKED` / `NOT_RUN` 및 git HEAD |
| 기존 모듈 통합 unittest | `PASS` / `FAIL` / `NOT_RUN` (실제 개수 기록) |
| Windows 실제 LIVE 정책 select | `PASS` / `FAIL` / `NOT_RUN` (설정 원문 제외) |
| Windows Claude 세션 로딩 | `PASS` / `NOT_VERIFIED` |
| 강제 signer/branch 경로 | `APPLIED` / `NOT_APPLIED` / `NOT_VERIFIED` |
| 독립 리뷰·GPT 판정 | `SKIPPED_BY_USER` |
| 새로운 리뷰 요청·유료 모델·READY | `0` |

기존 Work의 `CURRENT.md` 맨 위에 실제 호스트 결과만 보완. 시험/호스트/원격 증거는 비민감 요약·커밋으로 남기고 게시 후 원격 readback. 이 단계에서 실패하면 재큐잉·승인 재발급·과거 요청 수정 없이 해당 부분 `BLOCKED`, 나머지 허용된 검증은 계속. **Windows 실행 증거가 없으면 최종 운영 배포 완료로 선언하지 않음.**

## 4. 현재 인계 상태

- `SOURCE_CODE_GITHUB_PUBLISHED=PASS`
- `REVIEW=SKIPPED_BY_USER`
- `WINDOWS_APPLY=NOT_RUN` (이 GPT 세션은 Windows 명령/로컬 LIVE 설정 접근 수단 없음)
- `WINDOWS_REGRESSION=NOT_RUN`
- `HOST_HARD_ENFORCEMENT=NOT_APPLIED_OR_UNVERIFIED`
- `NEW_PAID_CALLS=0`, `NEW_REQUESTS=0`, `LIVE_CHANGE=0`

원샷 실행용 스크립트: [`collab/ops/windows_formal_review_submitter_rollout.ps1`](../../ops/windows_formal_review_submitter_rollout.ps1).
