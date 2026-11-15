# GPT 최종 정적 판정 — v0.2.23 접두사 호환성 수정

- 판정: **PASS_FOR_INDEPENDENT_R2_CANDIDATE_ONLY** / 2026-11-15 KST / r0001
- PRIVATE: `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 이 문서: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_V0223_PREFIX_COMPAT_FINAL_DISPOSITION_r0001_20261115.md`
- Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 소스: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V0222_APPROVED_PREFIX_COMPAT_FIX_RESULT_FOR_GPT_20261115.md`
- 동결 후보: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/artifacts/v0_2_23/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip`

## 1. 판정 사유 (확인된 것과 미검증 구분)

**8자→7자 하한 변경은 현재 명시된 사용자 승인 범위에서 수용한다.**

- 기존 보호된 위임의 승인 대상 `COWORK-`는 정확히 7문자, `L1-WORKSPACE-`는 8자 이상. 종전 최소 8자 검사 때문에 두 항목을 한 파일에 둔 위임 전체가 `POLICY_UNREADABLE`가 됐다.
- v0.2.23의 `skill_collab_watcher/auto_approval.py::_families` 정규식 `[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*-`는 `fullmatch`로 적용되고 `len(x)>=7`을 추가로 강제. ASCII 영문·숫자·단일 하이픈 구분, 하이픈으로 끝나는 유효한 접두사만 허용. 단어/구분자 없는 문자열, 공백, Unicode 유사문자, `*` 와일드카드, 선행 하이픈·연속 하이픈은 거부.
- `project_scope`의 기존 검사에는 **보호된 로컬 `project_families`에 사용자 등록한 정확한 접두사** 및 `len(project)>len(prefix)`가 필요하며 skill exact allowlist·비용/회수/만료/READY/signature 게이트는 변경 없음. GitHub에 임의 `project_families: [*]` 문구를 추가하는 것으로 범위를 넓힐 수 없다.
- 7자는 일반적인 모든 문자열의 안전 기준은 아니지만, 이 구현에서는 사용자 보호된 **명시 목록이 권한의 원천**이고 최소 길이는 오입력 방어. 이번 고정 범위 `COWORK-`, `L1-WORKSPACE-`를 손상 없이 표현하기 위한 7자 하한은 적절. 단독 `ABCDEF-` 같은 새로운 7자 family는 사용자가 보호 로컬 정책을 별도로 바꾸어 등록하지 않으면 자동 허용되지 않음.
- **GPT 직접 실물 확인:** v0.2.23 GitHub 원격 ZIP base64 디코딩 후 원시 bytes SHA-256 직접 계산: **282340 B**, **SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`**, **ZIP directory entries 102**, Git blob `0d7001798d402e5545833e6aaf8c5f4b9d2b8fbf`. 실제 원격 ZIP 보고치와 정확 일치.
- **GPT 직접 patch 확인:** `artifacts/v0_2_23/diff_v0_2_22_to_v0_2_23.patch`의 5개 변경파일(규칙·테스트·버전·런북), `tests/test_v023_prefix_compat.py`의 승인 범위 긍정/부정 시험. v0.2.22 핵심 B1/B2/M1/M2 알고리즘은 변경된 patch에 포함되지 않음.
- **Windows Claude Code 자체시험 보고:** 기존 v0.2.22 후보에 신규 시험 추가 시 **5 FAIL/19 PASS**; 수정 v0.2.23에서는 전부 PASS; 최종 ZIP의 Windows Python venv와 운영 Python 3.11.9 각각 **890 PASS / 12 SKIP**, 격리 CLI SHADOW **8/8 PASS**, 격리 install/rollback PASS, CRC/zip-slip/symlink/secrets scan PASS 보고. 이는 **SELF_TEST_REPORTED**, GPT가 Windows 회귀·CRC를 직접 수행했거나 독립 리뷰한 뜻은 아님.
- **변이 시험**: v0.2.23 전체 변이 시험은 NOT_RUN(이전 v0.2.21 16/17). R2 독립 reviewer가 B1/B2/M1 및 접두사/예산/회복의 악의적 반례를 별도 확인해야 함.

## 2. 독립 R2/승인·운영 경계

- `DEVELOPMENT=PASS`, `GPT_STATIC_DISPOSITION=PASS_FOR_R2_CANDIDATE`, `INDEPENDENT_REVIEW=NOT_RUN`, `OPERATING_LIVE=v0.2.20_UNCHANGED`, `AUTO_SIGNING=OFF`, `NEW_PAID_CLAUDE_CALLS=0`.
- **기존 사용자 통합 승인**: `GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md`에 승인된 R2 `POLICY-STATIC-V1-LARGE` 최대 **$3, 모델 호출 단 1회**와 보호 로컬 위임 가족 `COWORK-`/`L1-WORKSPACE-`, 정확 3개 skill, 요청당 $1/1회, 일 2회/$3, 월 $10, 30일, R2 독립 PASS 및 GPT 최종 판정 조건부 Windows 설치·LIVE 활성화는 **그대로 보존**.
- 다만 기존 R2 비용 승인은 **고정 v0.2.22 입력**에 결속되어 있음. v0.2.23은 바이트가 바뀌었으므로 기존 승인 기록을 임의로 수정해서 다른 ZIP에 적용하거나 두 차례 유료 리뷰로 확대할 수 없다.
- 필요한 확인은 오직 **독립 R2 대상의 변경: v0.2.22 → v0.2.23, 고정 SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`, 동일 `POLICY-STATIC-V1-LARGE` 최대 $3/모델 1회**. 새 비용·누적 위임 범위·기간·설치 승인 반복 요구 금지. 비용은 지금까지 미사용.
- **확인 후** Windows signer의 기존 절차로 새 유효 R2 `REQUEST/ZIP` 원본 핀, Commit A·SOURCE_PIN·해시/중복/남은 예산·유효기간 검사 → `APPROVAL_SIG.json` 검증/게시 → `READY.md` 마지막 게시 → 기존 단일 GitHub LIVE watcher 독립 리뷰 1회 및 결과/영수증 원격 재조회 → GPT 최종 결함 판정.
- R2 BLOCKING이 있거나 실행 불확실하면 운영 설치·자동 서명 enable 금지, 모델 임의 재호출 금지. **R2 PASS + GPT 최종 판정**을 확인한 경우에만 앞서 승인된 위임 범위로 Windows `v0.2.23` 백업/설치 OFF→첫 1주기 대기 REQUEST 선등록→자동 서명 ON→2주기/재시작/Notifier/rollback 검증. 기존 `v0.2.20` LIVE provider 보존.
- 본 파일은 **정적 판정·변경 입력 확인 대기**이며 정식 R2 REQUEST/READY, 운영 적용, 유료 리뷰 호출을 생성하거나 승인한 문서가 아님.

## 3. 다음 한 동작

사용자에게 **딱 한 번** 다음 변경만 확인: `v0.2.23 SHA-256 f941be8a…80ea7`에 대하여 기존 $3/1회 R2 승인을 적용해도 되는지. 확인되면 추가 범위 승인 없이 앞서 정의된 기존 Windows signer 기반 R2 및 조건부 운영 적용을 계속. 현재 `INDEPENDENT_REVIEW=NOT_RUN`, `AUTO_SIGNING=OFF`.
