# CoWork v0.2.22 R2 단일 비용 승인 기록 및 승인 범위 호환성 선행 수정 게이트

- 개정 r0001 / 2026-11-15 KST
- 정본 GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- 정확한 상대 경로: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/GPT_R2_APPROVAL_AND_V0222_SCOPE_FIX_GATE_r0001_20261115.md`
- 기존 Work `COWORK-AUTO-APPROVAL-20261115-001`. 기존 GitHub LIVE는 `v0.2.20`(최종 Windows 호스트 관측), `AUTO_SIGNING=OFF`.
- 사용자 최신 응답: GPT가 `GPT_V0222_DISPOSITION_AND_COMBINED_APPROVAL_GATE_r0001_20261115.md`에서 제안한 R2 1회 비용, 제한적 사전 위임, R2 PASS 조건부 Windows 운영 적용을 묶어 승인할지 질문했고 사용자가 **“그래”**라고 답함. 이 정본은 그 승인된 **정확한 범위**를 기록하며 자체가 Windows 서명/READY/모델 호출/운영 적용 실행 트리거가 아님.

## 1. 이미 받은 통합 승인 범위 (추가 반복 질문 금지)

| 내용 | 사용자 승인 범위 |
|---|---|
| 독립 R2 리뷰 | `v0.2.22` 당시 고정 후보의 신규 Claude 독립 R2 **1회**, `POLICY-STATIC-V1-LARGE`, 모델 호출 최대 **1회 / USD $3**, 재리뷰·다른 후보 자동 전용 금지 |
| 위임 저장소 | PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`; GitHub repo numeric ID `1451933830`을 Windows에서 실제 재조회 |
| 위임 project families | **정확히** `COWORK-`와 `L1-WORKSPACE-`, 다른 계열 거부 |
| 위임 skill exact allowlist | `cowork-review-watcher`, `cowork-dashboard`, `l1-knowledge-updater` |
| 자동 리뷰 정책 | `POLICY-STATIC-V1`만, 요청당 **1회 / 최대 $1**, 자동 R2/LARGE/XLARGE·재리뷰 금지 |
| 총액 제한 | 하루 최대 **2회 / $3**, 월 최대 **$10**. 기존 watcher 및 보호 로컬 위임 중 엄격한 제한 우선 |
| 기간 | 자동 승인 활성화 이후 **30일** 만료(그 후 자동 OFF). 과거 REQUEST 소급 자동 실행 금지 |
| 운영 적용 | **독립 R2에서 차단 결함 0 + GPT 최종 PASS**를 확인한 *같은 정확한 후보*에 한해 Windows 기존 LIVE 백업 → 기능 OFF 설치 → 초기 대기 요청 1주기 선등록 → 보호 정책 enabled=true → 2주기/재시작/Notifier/비인가 호출 0 검증 → 실패 시 비활성·원복. 새로운 Telegram 수동 버튼 불필요 |
| 별도 금지 | 운영 provider 변경, 기존 Dropbox watcher 재기동, 업무 제한 원본/키·토큰 GitHub 게시, PUBLIC 배포, 무단 추가 유료 호출 |

승인 후에도 실제 Windows 서명자가 보호된 정책과 입력 SHA/원격 중복/현재 비용·만료를 검증해야 한다. GitHub 문구만으로 승인 서명을 만들 수 있다는 뜻이 아니다. 기존 Windows 키는 호스트에서만 사용.

## 2. NEW GPT 선행 검토 — R2 시작 전에 확인된 정확한 불일치 (BLOCKED)

**이미 승인된 `COWORK-` 접두사가 v0.2.22 후보 검증 규칙에서 거부됨.**

- GitHub PRIVATE 원본: `artifacts/v0_2_22/diff_v0_2_21_to_v0_2_22.patch`의 `skill_collab_watcher/auto_approval.py::_families`.
- 현재 조건: `x.endswith("-") and len(x) >= 8` 및 와일드카드·공백 거부.
- 실제 `len("COWORK-") == 7` (COWORK 6자 + '-' 1자). 승인된 `L1-WORKSPACE-`는 최소 길이를 만족하지만 `COWORK-`는 불만족.
- 따라서 승인된 두 계열을 보호 정책의 `project_families`에 그대로 쓰면 정책 로드가 `POLICY_UNREADABLE`로 차단되어 정상 무인 실행이 불가능함. 이는 **확인된 호환성 차단**, 악의적 입력에 대한 보안 사고가 아님.
- 기존 M2 시험은 더 긴 접두사(예: `test-project-`)를 사용해 이 실제 승인 범위를 포착하지 못했다. 다른 AUTO 보호 경계를 완화하는 것은 해결책이 아님.

**운영·비용 우선순위:** 현재 v0.2.22 바이트에 R2를 즉시 쓰면 수정본에 별도 리뷰가 필요해질 수 있으므로 **R2 모델 호출 0, REQUEST/READY/서명 0을 유지**한 채 위 호환성 결함을 먼저 수정·동일 회차 재시험하는 것을 결정. 사용자 통합 승인 내용은 유지하되 **R2의 특정 입력 v0.2.22에 대한 승인 범위를 자동으로 다른 바이트/새 버전으로 확대하지 않음**. 새 후보로 리뷰 대상을 변경할 필요가 생기면 **그 변경 항목만 사용자에게 확인**, 누적 위임 범위·비용 한도·조건부 운영 목적의 승인 전체를 다시 요구하지 않음. 새 R2 REQUEST/READY가 없으므로 기존 R2 비용은 미사용.

## 3. Windows Claude Code **1회 무비용 최소 보완 작업**

Windows Claude Code가 이 문서를 읽어 다음을 **중간 질문 없이 하나의 격리 개발·재시험 회차**로 수행:

1. 기존 v0.2.22 ZIP/설치본을 그대로 보존하고 격리 복사본에서 `_families()`의 규칙을 확인. 기본값은 `len>=8` 그대로 유지하면서 사용자 승인된 짧은 **정확한 `COWORK-` 접두사만 예외**로 허용하거나, 동일한 제한을 보장하는 더 단순한 안전 코드를 사용. `*`, 짧은 임의 접두사, 빈/공백·비정상 ID까지 허용하는 무제한 완화 금지.
2. 기존 후보에서 FAIL → 수정본에서 PASS하는 회귀 추가: 보호 정책이 `project_families=["COWORK-","L1-WORKSPACE-"]`를 실제 읽고 ACTIVE 위임 판정을 통과, 유효한 `COWORK-AUTO-APPROVAL-20261115-001` 프로젝트/허용 스킬에서 정상 1회 승인; `COWORK-` 접두사 자체·`COWORKX-`·`COWORK`·외부 프로젝트·스킬·정책 변조에서 signer/READY/모델 0. 기존 `L1-WORKSPACE-`도 PASS. 실제 owner 위임 파일은 아직 활성화하지 말 것.
3. 기존 v0.2.22 핵심 수정 B1(비용 합집합), B2(위임 축소), M1(이중 서명), M2(접두사) 회귀 유지. 전체 Windows 3.11.9 회귀 + fake GitHub/임시 키 격리 SHADOW·crash/rollback(운영 변경 0) 수행. 실패 발견 시 같은 개발 회차에서 최소 수정/재시험.
4. 새 **개발 후보 버전**은 충돌 없으면 `skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip`; 새 버전 ZIP 실제 SHA-256/크기/CRC/경로 이탈/심볼릭 링크/비밀 검사. 기존 v0.2.20/v0.2.21/v0.2.22 원본 보존.
5. 허용된 CoWork 후보 파일·diff·시험 결과를 같은 PRIVATE Work 아래 게시, git commit 및 원격 **raw bytes/SHA** 검증. 결과는 정확히 `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CLAUDE_V0222_APPROVED_PREFIX_COMPAT_FIX_RESULT_FOR_GPT_20261115.md`, `CURRENT.md`·`TRACKER.json` 최신 상태 갱신. GPT 직접 검사와 Windows 자체시험 구분.
6. **절대 실행 금지:** 새 유료 R2 모델 호출, 다른 요청 재리뷰, `APPROVAL_SIG.json`/READY 게시, 실제 키 서명, 운영 DB/Task/Notifier/키·설정 변경·LIVE 자동서명 켜기·PUBLIC 배포. 실제 Windows 코드/키에 접근할 수 없으면 가능한 설계·격리 작업만 계속하고 `BLOCKED/NOT_RUN` 별도 기록.

## 4. 현재 판정 / 다음 한 동작

`OWNER_COMBINED_APPROVAL=RECORDED`, `R2_COST_APPROVED_V0222=$3_MAX_ONE_CALL`, `R2_CALLS=0`, `R2_REQUEST=NOT_POSTED`, `R2_SIGNATURE=NOT_CREATED`, `R2_READY=NOT_POSTED`, `AUTO_SIGNING=OFF`, `V0222_SCOPE_COMPAT=BLOCKED`, `HOST_DEV_DELTA_FIX=NEXT`, `OPERATING_GITHUB_LIVE=v0.2.20_UNCHANGED`.

**NEXT_ONE_ACTION:** Windows Claude Code에 이 파일 경로를 한 번 전달해 안전한 접두사 호환 수정·전체 재시험·새 DEV ZIP 및 PRIVATE 결과 readback. GPT가 새 패키지 실바이트 확인 후 **변경된 리뷰 대상에 대한 좁은 추가 확인만** 받고 R2 서명→READY 마지막→독립 1회→GPT 판정→기존 조건부 운영 적용을 이어감. 이 과정에서 동일 비용 승인을 다시 쓰거나 임의 R2 재호출하지 않음.
