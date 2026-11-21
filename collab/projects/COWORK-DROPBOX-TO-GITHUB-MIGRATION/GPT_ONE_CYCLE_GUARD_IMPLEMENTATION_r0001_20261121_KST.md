# CoWork 1사이클 제한 — GitHub Actions GPT 판정 게이트 구현 결과
2026-11-21 KST · 기존 Issue #2 및 COWORK-DROPBOX-TO-GITHUB-MIGRATION Work

## 사용자 확정 정의
- **1사이클 = GPT의 리뷰 요청 1회 → Windows Claude Code 독립 리뷰 1회 → GPT 판정 1회 → 종료**.
- GPT 판정이 ACCEPT_WITH_CHANGE/REJECT/DEFER/NEED_INFO여도 자동 수정, 신규 REQUEST/READY, Claude 재리뷰, GPT 재호출을 시작하지 않음.
- 같은 Work의 기존 사이클 이후에는 다른 요청 ID를 발행하더라도 자동 사이클로 이어지지 않음. 별도의 사용자 지시와 유효 승인 범위를 가진 후속 작업은 사람이 판정해야 하며, **현재 구현은 자동 예외/초과 허용 경로 없음**.

## 적용된 변경 (PUBLIC main)
- `collab/tools/gpt_disposition_actions.py`:
  - `one_cycle_work_id()`는 REQUEST의 `work_id`/ID 및 `collab/projects/<work_id>/CURRENT.md` 정합성을 검사. 같은 Work ID에 속한 **다른 REQUEST.md가 1개라도 존재하면 차단**. 파일 검사 범위 초과·현재 요청 필드 부재·Work 정본 누락 시 fail-closed.
  - GPT API 비용·승인 게이트 통과 뒤 **모델 호출 이전** `collab/projects/<work_id>/ONE_CYCLE_CLAIM.json`을 GitHub Contents API CREATE_ONLY로 선점. 이미 존재/읽기 실패/충돌이면 GPT 모델 호출 0.
  - 기존 `GPT_API_EXECUTION_CLAIM.json` 및 `GPT_DISPOSITION.json`의 동일 요청 중복 방지·원격 readback·자동 재호출 금지를 보존. 신규 판정 필드에 `work_id`와 Work claim 경로를 연결.
  - `--check-cycle-request <request_id>`는 로컬 체크아웃의 **읽기 전용 사전 검사**만 수행하며, Windows watcher 설치·실행을 의미하지 않음.
- `collab/tools/tests/test_gpt_disposition_actions.py`: 최초 Work 허용·동일 Work 두 번째 요청 차단·서로 다른 Work 허용·Work 식별자/정본 누락 차단·Work claim 우선 생성·claim 실패 시 모델 호출 0의 시험 6건 추가. 종전 9건 유지.
- 기존 `.github/workflows/cowork-gpt-disposition.yml`의 OFF 게이트/단일 동시성 그룹/무과금 오프라인 self-test는 유지. 추가 Telegram 알림 없음.

## 원격 코드 확인 값
- GPT 실행기: `collab/tools/gpt_disposition_actions.py`; Git blob `c6b82b29c519d8f206be43eed43081ebbf3fe949`; SHA-256 `b4f6c90c7bde4e9a708da749787bd0315fa4377820fe431cfed1beba09254e7e`.
- 회귀시험: `collab/tools/tests/test_gpt_disposition_actions.py`; Git blob `f738bef21404e932dc5d8e9eaabe51bb8bde1bc7`; SHA-256 `c6d55a19d8a7cfbd68a54f51608c38384284842f2bab465affad685cf02b7ffb`.
- GitHub 파일 blob 및 내용 재조회 완료. 위 해시는 LIVE 설치본·Actions Runner 실행 증거와 구별.

## 실행 안전 경계와 미적용 부분
1. **Windows watcher v0.2.29 LIVE 미변경**. GPT 실행기 신규 코드가 Windows watcher의 REQUEST→승인/READY 이전 단계에 연결된 것은 아님. 따라서 **Claude 리뷰를 시작하기 전에 Work별 1사이클 제한이 실제 차단되는지 = NOT_APPLIED/NOT_VERIFIED**. 이 구간에 새 유료 요청을 만들어 테스트하지 않음.
2. GitHub Actions GPT API Job은 기존처럼 OFF. 별도 OpenAI 비용/키/모델 지출 승인·설정 0, 실제 호출 0. GitHub Runner의 새 시험 결과·실행 트리거, 실 Ed25519 검증 E2E는 접근 제약으로 NOT_VERIFIED.
3. GitHub checkout에 동일 Work의 과거 REQUEST가 존재하면 **과거 READY가 없어도** 의도적으로 차단. 신규 Work를 명목상 만들어 우회하는 행위는 승인 없음. 기존 이력은 삭제/재작성하지 않음.
4. Work claim은 GPT API 판정기 관점에서 영속적 1회 잠금이며 요청별 claim보다 먼저 게시. 네트워크·게시 불확실은 자동 재호출 금지. **Claude 단계와 GPT 단계를 통합한 엔드투엔드 잠금은 Windows watcher가 같은 Work 단위 거부 게이트를 채택·운영 검증하기 전까지 미완성**.
5. 사용자가 이후 명시적으로 같은 Work의 별도 독립 리뷰를 승인하는 경우는 현재 일괄 자동 차단. 사용자 지시 없이 같은 Work ID의 재리뷰 요청을 다시 제출하지 않음.

## 시험 및 상태
- 신규 단일 Work 판정 알고리즘의 **독립 격리 Python 검증 5건 PASS** (최초/중복/다른 Work/식별자/정본 누락). 이는 원격 실행기 전체 시험과 다른 로컬 시험.
- GitHub 저장소에 추가된 6개 회귀시험은 코드 게시됨. **GitHub Actions Runner를 통한 통합 15건 시험 결과 NOT_VERIFIED**; 로컬 실제 최신 executor와 15건 전체 실행도 NOT_RUN.
- SOURCE_CODE=POSTED / GITHUB_BLOB_READBACK=별도 조회 / WINDOWS_PRE_CLAUDE_GATE=NOT_APPLIED / GPT_AUTO_LIVE=OFF / PAID_MODEL_CALL=0 / WATCHER_HOST_CHANGE=0 / INDEPENDENT_REVIEW=NOT_RUN.
- 통과 기준: 15건 실제 실행 PASS, 무과금 Actions Runner 정상, 이후 Windows watcher 사전 게이트 설계/후보·비용 0 검증 및 명시 운영 승인 후 새 요청 한 건에서 1 Claude + 1 GPT + 0 자동 재리뷰 E2E 확인.

## 다음 한 동작
GitHub Actions의 `offline-selftest`를 읽기 전용 확인하고, Windows watcher 기존 승인/READY 진입점에 **동일 Work 중복 거부**를 최소 변경으로 연결할 후보/시험을 준비. Windows LIVE 설치·유료 리뷰·GPT API 활성화는 해당 권한이 확인되기 전에는 하지 않음.
