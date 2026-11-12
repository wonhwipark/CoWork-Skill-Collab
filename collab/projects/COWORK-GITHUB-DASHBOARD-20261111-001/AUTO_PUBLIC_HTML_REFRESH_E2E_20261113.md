# CoWork Executive HTML 대시보드 지속 자동 갱신 검증 결과

- 기준: 2026-11-13 KST
- 요청: 새로운 CoWork 협업 갱신 발생 시 PUBLIC HTML 대시보드를 자동 갱신하고 열린 탭에도 상태를 반영
- 대상 URL: https://wonhwipark.github.io/L1Work/cowork-dashboard/
- 운영 구분: **대시보드 공개 상태 자동화**만 적용, 실제 협업 LIVE 운송은 `MIGRATION_NOT_CUTOVER`

## 1. 최종 판정

| 항목 | 상태 | 근거 |
|---|---|---|
| 프로젝트·작업 변경 감지 범위 확장 | PASS | PRIVATE `.github/workflows/cowork-dashboard.yml`에서 `collab/projects/**` 전체 감지 |
| PRIVATE HTML/JSON 갱신 | PASS | `CURRENT.md`/`TRACKER.json` 기반 생성·회귀시험 |
| 공개 허용 필드 검증 및 전송 | PASS | PRIVATE `public_sync.py` + 공개 허용목록 |
| 연속 갱신 시 낡은 상태 캐시 충돌 보완 | PASS | PUBLIC sync에서 최신 PRIVATE `main` 스냅샷 상태를 로컬 재생성 후 공개 필터 실행 |
| 실제 작업 변경 → PUBLIC 자동 JSON 갱신 | **PASS** | PRIVATE `TRACKER.json` 작업 단계 2→4 변경, 아래 E2E 증거 |
| GitHub Pages 최신 배포 | **PASS** | L1Work Pages run [#43251906090](https://github.com/wonhwipark/L1Work/actions/runs/43251906090) SUCCESS |
| 이미 열린 HTML 탭 상태 재확인 | CODE_APPLIED · 브라우저 E2E NOT_RUN | PUBLIC `status.js`에서 120초 간격 갱신 + 탭 재활성/포커스 시 재조회, JS 구문검사 PASS |
| Windows/Claude 독립 리뷰/LIVE 전환 | NOT_RUN · MIGRATION_NOT_CUTOVER | 관련 운영 기능 변경 없음 |

## 2. 구체적으로 보완한 내용

- **변경 감지:** `collab/projects/**/CURRENT.md`, `TRACKER.json`뿐 아니라 프로젝트에 추가되는 비민감 피드백·인계 MD 등 **모든 프로젝트 파일 변경**에 PRIVATE dashboard Action이 실행되도록 `.github/workflows/cowork-dashboard.yml`을 수정. 기존 `collab/requests/**`, `collab/reviews/**`, `collab/receipts/**` 감지는 유지. 단 변경 파일의 내용이 실제 상태 집계에 사용되지 않는 경우 또는 공개 승인 범위 밖인 경우 공개 HTML 값은 변경되지 않을 수 있음.
- **소스 정합성 경합 수정:** 과거 PUBLIC sync 실패 [#43251033752](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43251033752)에서 `stale PRIVATE dashboard state`가 실제 관측됨. 공개 sync Action 내부에서 `python3 collab/dashboard/generate.py`를 로컬 실행해 신뢰된 최신 체크아웃의 `CURRENT/TRACKER` 기준 상태를 다시 만든 다음 `public_sync.py prepare` 실행. PRIVATE repo에는 이 작업 중 추가 쓰기하지 않음; 공개 필터/고정 경로 검증 그대로 유지.
- **이미 열린 브라우저:** `L1Work/docs/cowork-dashboard/status.js`가 PUBLIC `status.json`을 **120초 간격**으로 재확인. 탭 숨김 상태에서는 polling 생략, 다시 표시하거나 포커스되면 최신 데이터 요청. 중복 요청 방지, 이전 데이터와 동일하면 불필요한 DOM 재구성 방지, 오류 시 최근 수신한 표시 유지. PRIVATE 직접 접근·토큰 노출 없음.
- **시각적 상태 불일치 방지:** STATUS 표의 Windows/독립 리뷰 상태를 공개 JSON의 제한된 enum 값으로 갱신. HTML에 박혀 있던 과거 고정 날짜를 상태 JSON 기준일 출력으로 변경. 사용자가 브라우저를 새로 고칠 필요 없이 상태 변화 반영 가능(브라우저 E2E 자동시험은 NOT_RUN).

## 3. 실제 갱신 E2E

1. PRIVATE `collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/TRACKER.json`의 `cowork-dashboard` Work `phase=DEVELOPMENT` → `DISPOSITION`으로 변경 (개발자 자체시험 PASS·독립 리뷰 NOT_RUN 그대로, 완료 승격 아님). 입력 commit `88135a754efa8af2970127013aae879c82ae1431`.
2. PRIVATE dashboard GitHub Actions [#43251843321](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43251843321): `completed/success`.
3. 별도 PUBLIC sync Actions [#43251880632](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43251880632): `completed/success`, 코드 검증 47 + 공개 보안 8 = **55 PASS / 0 FAIL**. 로그에서 `ALLOWLIST_BUILD=PASS`, `PUBLIC_SYNC=POSTED_READBACK_PASS` 실측.
4. PUBLIC `L1Work/main/docs/cowork-dashboard/status.json` 원격 재조회: `dashboard` 카드의 `phase_index`가 **2에서 4**로, `phase_label`이 **개발·시험 신고에서 판정·보완 신고로** 자동 변경, 새 blob `b1226dfa91d0420bb1b98373274d5755191ac7b6`. 내부 Work ID/PRIVATE 문서 원문 미포함.
5. GitHub Pages [#43251906090](https://github.com/wonhwipark/L1Work/actions/runs/43251906090): `completed/success`; 새 PUBLIC 상태가 배포 대상에 반영됨. 별도 실제 브라우저 시각적/HTTP 응답 검증은 `NOT_RUN`.

## 4. 안전성과 제한

- PUBLIC 자동 반영은 **공개 허용목록에 있는 작업 범주·정형 단계·합계 수치만**. PRIVATE 원문, 고객자료, 사내 반출 금지 소스, Work ID, 요청·리뷰·영수증 원문, 비밀키·토큰 등을 공개하지 않음.
- 신규 미승인 스킬명이나 상세 피드백을 PUBLIC에 직접 표시하지 않음. 새로운 프로젝트는 허용된 범위의 전체 건수로만 변화가 드러날 수 있음.
- PUBLIC status 파일 변경이 없으면 GitHub REST 동일 바이트 검증 후 `UNCHANGED`이며 불필요한 Pages 재배포를 하지 않음. 즉 변경 이벤트마다 **검증은 자동**, 사용자 화면의 공개 데이터가 바뀔 때만 **PUBLIC 데이터/Pages 게시** 발생.
- 수시 다중 변경 시 GitHub Actions concurrency 제한으로 중간 대기 실행 일부가 취소될 수 있으나, 성공한 이후 실행이 최신 `main` 소스를 재생성하는 방식. 모든 중간 이벤트의 처리 로그를 1:1 보장하는 시스템은 아님. 최종 상태 기준 eventual consistency 운영.
- Windows watcher, 기존 Dropbox LIVE, 운영 DB/WAL, 예약 작업, Bridge, Telegram, 모델 리뷰 실행, 운영 토큰·서명 변경 없음.
- 공개용 별도 토큰은 기존 `COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN`을 사용. 추가 토큰 발급 필요 없음.

## 5. 산출물/다음 한 동작

- PRIVATE 흐름 정의: `.github/workflows/cowork-dashboard.yml`, `.github/workflows/cowork-public-status-sync.yml`
- PRIVATE 필터: `collab/dashboard/public_sync.py`
- PUBLIC 브라우저: `wonhwipark/L1Work/docs/cowork-dashboard/index.html`, `status.js`, `status.json`
- **기본 URL:** https://wonhwipark.github.io/L1Work/cowork-dashboard/
- 다음 한 동작: 사용자가 브라우저에서 대시보드를 열고 카드 `CoWork 대시보드`의 `판정·보완 신고` 표시를 확인. 향후 PRIVATE 상태가 바뀌면 같은 경로로 자동 업데이트되며, 미승인 PUBLIC 필드 확대나 LIVE 전환은 별도 승인 필요.
