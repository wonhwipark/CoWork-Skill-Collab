# GPT 판정 — CoWork 자동 승인 v0.2.22 후보 / 독립 R2·사전 위임·LIVE 설치 통합 게이트

- 버전 r0001, 2026-11-15 KST
- Repository: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 정확한 상대 경로: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md`
- Work ID: `COWORK-AUTO-APPROVAL-20261115-001`
- 출처: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V0221_GPT_FINDINGS_FIX_RESULT_FOR_GPT_20261115.md`
- 현재 `ACTIVE_PROVIDER=GITHUB / CUTOVER=LIVE / OPERATING_VERSION=v0.2.20` (기존 Windows 호스트 보고 기준). `AUTO_SIGNING=OFF`, 본 새 개발·보완 중 운영 변경 0. 과거 Dropbox pending 보존.
- **GPT 판정** `ACCEPT_V0222_FOR_INDEPENDENT_REVIEW_ONLY`. 독립 리뷰 PASS·운영 적용 완료가 아님. 본 문서 게시만으로 요청·서명·READY·모델 호출·운영 변경이 시작되지 않음.

## 1. GPT 직접 확인 / Windows 자체시험 구분

- **Windows Claude Code 결과 보고**: v0.2.21의 B1(서로 다른 예약/디스패치를 max로 과소 집계), B2(위임 축소 재확인 누락), M1(동일 프로세스 이중 서명 경합), M2(신규 Work 범위) 수정 후 신규 v0.2.22 후보 생성. 추출된 최종 ZIP Windows Python 3.11 venv·운영 3.11.9 각각 **866 passed / 12 skipped**, v0.2.20 기준 **674 passed / 12 skipped**, 격리 CLI SHADOW **8/8 PASS**, 롤백 복사본 PASS. 구 v0.2.21 FAIL → v0.2.22 PASS 반례와 M1 구본 **12회 중 3회 이중서명** 재현 및 신본 **12/12 PASS**. **SELF_TEST_REPORTED**이며 독립 리뷰로 승격 금지.
- **GPT 원격 실제 파일**: `artifacts/v0_2_22/skill-collab-watcher_v0_2_22_1115_DEV_NOT_FOR_DEPLOYMENT.zip`을 GitHub에서 base64로 가져와 직접 원시 바이트 SHA-256 계산: **280313 B, 101 ZIP entries, SHA-256 `1b67de37891cb7fdbae721b9424e312d1cc5b8c68e06e69357555a556d27bd87`**, 보고치 정확 일치. Git blob `caa55e965df2a42693a06cee44e17e2e1cb879e5`, ZIP EOCD 확인. 이 세션의 모든 entry CRC·압축 내부파일 테스트는 별도 미실행(Windows 호스트 보고 기준).
- **GPT 수정 patch 직접 검토**: `artifacts/v0_2_22/diff_v0_2_21_to_v0_2_22.patch`, 987줄. B1 `state_store._auto_usage_locked/auto_claim`의 request ID/revision union·원자 예약·KST 달력; B2 `_revalidate`의 보호된 현재 위임·후보 재판정, 각 서명/approval/READY 직전 호출·`POLICY_STOPPED` terminal; M1 `AutoApprover._in_progress` 중복 진입 차단; M2 `project_scope` exact + 제한된 `project_families` 및 다른 project_id/work_id 거부를 확인.
- **검증 한계**: Windows 운영 실제 signer 호출 0, 실제 신규 REQUEST+READY의 LIVE 1회 실행 NOT_RUN, 최종 v0.2.22 mutation test 미실행, 독립 보안 리뷰 NOT_RUN. 정적 코드 열람은 악의적 입력/경합 경로 완전무결성 보증이 아님.

## 2. 원래 지적 항목 GPT 판단

| ID | 판정 | 검증 수준 |
|---|---|---|
| B1(자동+기존 디스패치 비용 합산) | **수정 수용/독립 리뷰 대상** | patch에 union/transaction 수정 확인 + 구/신 반례 Windows 보고 |
| B2(위임 정책 축소) | **수정 수용/독립 리뷰 대상** | patch에 현행 정책 반복 재검증/terminal STOP 확인 + 33건 Windows 보고 |
| M1(간헐 중복 서명) | **원인·수정 수용/독립 리뷰 대상** | 구후보 3/12 재현, 새 in-progress guard, 신후보 12/12 Windows 보고 |
| M2(새 Work 자동 허용 범위) | **설계 수용/실제 위임 사용자 확정 대기** | 프로젝트 접두사 제약·스킬 exact 필터·negative tests, 운영 정책 OFF |

**재리뷰 핵심:** (a) day/month union audit 로그의 request identity 처리, KST 경계 및 지연 영수증, 실제 최대 비용 누락 반례; (b) 변경된 위임의 재검증 시점, STOP 복구/원자성, signed READY 결속; (c) 멀티 스레드/프로세스/crash 재서명 0; (d) 가족 접두사 인접/Unicode·비정상 project_id/work_id; (e) 실키 signer와 Watcher same process 신뢰 경계·DPAPI/ACL; (f) 변경분 회귀와 기존 단일 LIVE·N1 원격 예약. Windows 자체 테스트를 그대로 믿지 말고 반례/결함 근거를 요구. 새 모델의 라이브 실행 여부와 별도임.

## 3. 다음 독립 리뷰 요청 범위 — *비용 승인 전, 아직 미실행*

- 후보 `v0.2.22`, 단일 R2 독립 Claude 리뷰를 **`POLICY-STATIC-V1-LARGE`, 최대 USD $3, 호출 1회**로 권고. **현재 사용자 비용 승인 없음**.
- 리뷰 대상은 고정된 v0.2.22 ZIP + `CANDIDATE_MANIFEST.md` + `diff_v0_2_21_to_v0_2_22.patch` 및 v0.2.20 기준 핵심 계약(서명/상한/중복/원격 예약). 무관한 스킬·L1 업무 원본·서브에이전트/반복 R2는 제외.
- 비용 허가 후에만 동일 Work에서 **정식 신규 `REQ-COWORK-AUTO-APPROVAL-V0222-R2-20261115` 또는 충돌 없는 새 ID**를 등록하고 원본 ZIP/manifest를 reviewer가 접근 가능한 기존 논리 `/SKILL-COLLAB/packages/` 위치로 원본 바이트 그대로 고정, Commit A + SOURCE_PIN + SHA/CRC/size 검증. Windows 기존 signer가 유효 승인 계약·원격 중복/지출 검사 후 APPROVAL_SIG와 READY 마지막 게시. 새 auto-sign feature는 OFF 유지하며 **기존 서명 경로**로 **유료 R2 1회만** 실행.
- REVIEW_RESULT/RECEIPT/USAGE/DISPATCH의 실제 원격 readback과 비용·BLOCKING/MAJOR/증거를 GPT가 확인해 판정. 리뷰가 BLOCKING이면 자동 설치·유료 재리뷰 금지, 동일 Work에서 개발 보완 후 새 승인 범위만 요청.

## 4. 한 번에 확정할 사용자 사전 위임·운영 범위 제안 (아직 승인받지 않음)

사용자 목적은 GPT가 요청을 게시하면 **추가 Telegram 버튼이나 Windows Claude Code 수동 서명 없이** Windows가 신뢰 가능한 사전 위임 범위 내에서 승인·READY·기존 watcher 독립 리뷰까지 자동 수행하는 것. 처음 한 번의 보호 로컬 정책 승인과 변경 전 백업·롤백은 필요하다.

| 항목 | 기본 권고안(승인 전 제안) |
|---|---|
| 대상 저장소 | `wonhwipark/CoWork-Skill-Collab` PRIVATE main, numeric repo_id `1451933830` 재확인 |
| 자동 허용 Work 가족 | 우선 `COWORK-` / `L1-WORKSPACE-` 두 접두사(각 고정되고 끝 `-`), 기타 Work는 자동 거부 |
| 자동 허용 스킬 exact | `cowork-review-watcher`, `cowork-dashboard`, `l1-knowledge-updater` (**현재 실제 세 REQUEST에서 확인한 값**). 그 외 스킬은 자동 거부; 향후 목록 추가는 보호 로컬 정책 승인 필요 |
| 자동 승인 리뷰 | `POLICY-STATIC-V1`만, 요청당 모델 최대 **1회/US$1**. R2/LARGE/XLARGE와 재리뷰 자동 승인 금지 |
| 누적 제한 | 하루 최대 **2회 / US$3**(기존 watcher 상한 이내), 월 최대 **US$10**, 정책 만료 **30일** 후 자동 OFF. 월/만료는 신규 제안값 |
| 첫 적용 대상 | 활성화 이후 처음 본 새로운 REQUEST만; 현재 대기 중 Work→Knowledge·대시보드 요청 **소급 자동 실행 금지** |
| 변경/운영 권한 | 새 패키지 리뷰 자동 실행에만 한정. 실제 업무 호스트 실행, 키/DB 이행, PUBLIC ZIP 배포, LIVE provider 변경은 자동 허용 금지 |
| 설치 게이트 | **R2 BLOCKING=0 등 GPT 최종 PASS + 사용자 통합 승인 후** 기존 LIVE Task/원본 보존·백업 → v0.2.22 운영 후보 설치(기능 OFF) → 기존 대기 요청 1주기 선등록 → `enabled:true` + `enabled_at` → 2주기·재시작·1회 중복/0비인가 모델·Notifier 확인 → 실제 결과 원격 readback. 문제가 있으면 AUTO_SIGNING OFF→원본 v0.2.20 롤백 |
| 추가 운영 보호 | 새 `AUTO_SIGNING_UNCERTAIN` 이벤트를 운영 Notifier 허용 목록에 추가해 사용자가 사고를 확인할 수 있게 함. 별도 Telegram 승인 버튼 없음 |

이는 **R2 $3/1회 비용 승인 + 본 한정 위임 범위 + R2 PASS 조건부 Windows 운영 설치/auto signing activation**을 하나의 명시적 사용자 응답으로 승인받기 위한 제안. 사용자가 명시 승인하지 않았다면 비용 호출/운영 변경 0.

## 5. 현재 정리와 NEXT_ONE_ACTION

`GPT_DIRECT_ZIP_SHA=PASS`, `B1/B2/M1/M2_PATCH_REVIEW=ACCEPT_FOR_R2`, `SELF_TEST=PASS_HOST_REPORTED`, `INDEPENDENT_REVIEW=NOT_RUN`, `NEW_PAID_CALLS=0`, `AUTO_SIGNING=OFF`, `OPERATING_GITHUB_LIVE=v0.2.20`, `PUBLIC_RELEASE=NOT_RUN`.

**NEXT_ONE_ACTION:** 사용자의 **한 번의 명시 통합 승인** 요청. 그 승인을 확보하면 (1) 새로운 유효 R2 REQUEST/ZIP pin 및 Windows 기존 signer·READY LAST → 기존 LIVE watcher 독립 Claude 1회 리뷰·영수증 → GPT 결과/버그 판정, (2) 독립 리뷰 PASS이면 승인 범위 안에서 Windows 한 회차 백업·install OFF→enabled+검증·rollback/readback. 실제 Windows 시작 수단이 GPT 환경에 없으면 정확한 PRIVATE 원샷 프롬프트로 인계하며 미수행을 완료로 보고하지 않음.
