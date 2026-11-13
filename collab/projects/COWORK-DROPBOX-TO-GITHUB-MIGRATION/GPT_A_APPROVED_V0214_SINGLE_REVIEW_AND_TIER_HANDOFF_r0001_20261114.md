# v0.2.14 A안 승인 실행 인계 — 독립 리뷰 1회와 등급형 예산
작성 2026-11-14 KST · r0001
Repo: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
Exact relative path: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_A_APPROVED_V0214_SINGLE_REVIEW_AND_TIER_HANDOFF_r0001_20261114.md`
Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
**A안 승인 완료 / B안 미승인 / LIVE 미승인 / 실제 Windows 리뷰 미실행**

## 사용자 승인 반영
- 사용자는 **A안을 승인**: CoWork watcher `v0.2.14` 고정 리뷰 대상 `REV-COWORK-V0214-20261114`에 **정식 Claude 독립 리뷰 정확히 1회**, 정책 `POLICY-STATIC-V1`, effort `medium`, **최대 USD 1.00**.
- 운영자 Windows PC에서 **Ed25519 서명키·신뢰 루트 1개 생성/암호화 보관**, 단일 사용자용 `trust_root_independence=warn` 운용까지 A안 범위로 명시 승인됨. 서명 검증 자체는 끄지 않고 기존 signed APPROVAL/READY 계약을 따라야 함. 별도 서명자 PC 불필요.
- **추가 비용 승인 질문 반복 금지**: 본 리뷰 1회는 이미 승인됐음. 다만 B안 토큰 신규 발급/교체, 운영 감시기·DB·작업·Notifier/Bridge 수정, 유료 추가 리뷰·재리뷰, 신규 L1Work PUBLIC 게시, LIVE 전환은 승인되지 않았음.
- GitHub에 CoWork 자체 소스/ZIP을 게시해 리뷰 링크로 전달하는 것은 이미 사용자 승인됨. 회사 L1 원본 코드·고객자료·토큰/비밀은 전송/게시 불가.

## 실행 전에 참조할 정본
- `collab/START_HERE.md`, 본 작업 `CURRENT.md` 최상단, `TRACKER.json`
- `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`, `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md`, `GPT_V0214_PREFLIGHT_DISPOSITION_AND_APPROVAL_GATE_r0001_20261114.md`
- 리뷰 Manifest: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/REV-COWORK-V0214-20261114/REVIEW_MANIFEST.md`
- ZIP: `skill-collab-watcher_v0_2_14_1114.zip`, 원격 ZIP 고정 commit `dc429c05039b42e0af343a07ea2a9fb6d783feda`, SHA-256 `3a221dcdb22ba75208a60ca555b0ee75866313a591148b1f482b7cbb6aa0b367`, 219663 bytes. 실제 GitHub 원격 다운로드·SHA 재확인 후에만 실행. 관련 diff/소스의 고정 URL은 Manifest를 따를 것.

## Claude Code Windows 실행 1회: 중간 핑퐁 금지
1. A안 범위에서 단일 Windows PC 보호된 위치에 운영키·신뢰 루트를 생성/보호하고, PIN/키 일치/암호화 보관·실서명 검증을 격리 시험. 비밀·개인키·token 내용을 GitHub나 로그에 게시하지 않음. **실제 운영 watcher 설정·Task/DB 변경은 금지**.
2. 기존 `v0.2.14` ZIP/manifest를 고정한 채 입력 범위를 diff+관련 `state_store/orchestrator` 호출부+핵심 E2E 증거로 제한. 실제 리뷰 유형은 **R1 변경 결함 리뷰**(입력 약 16k/출력 약 3k 토큰 *목표*; 실제 hard cap이라고 주장 금지), 기존 정책 `POLICY-STATIC-V1`, `--max-budget-usd 1`, 가능한 `--max-turns 3`를 CLI 실지원 확인 뒤 사용. 기존 runner가 turn 옵션 미지원이면 실제 미지원 상태를 보고하고 임의로 제품 코드/ZIP을 수정하지 않음.
3. 유효한 단일 서명 APPROVAL/REQUEST/READY 게시 절차가 실제 사용 가능하고, 기존 인증으로 요청 생성/검증·결과 게시가 허용된다면 **별도 독립 Claude 리뷰 한 번만 수행**. 이 사용자 승인이 실 리뷰 비용 1회 권한임. 기존 감시기는 `ACTIVE_PROVIDER=NONE`이므로 GitHub LIVE가 활성화된 것처럼 주장 금지. 승인 서명·상태·요청/영수증 경로가 정상 동작하지 않거나 B안 토큰 설치가 반드시 요구된다면 비용 있는 호출 0으로 해당 항목만 `BLOCKED_CREDENTIAL_OR_TRANSPORT` 처리하고 완료된 A키·실서명·입력 준비/차단 근거를 한 번에 보고. **정식 서명/READY를 우회해 임의 CLI 실행 후 독립 리뷰 PASS로 기록하지 않음**.
4. 독립 리뷰 결과 발생 시, 개발 세션 자체시험과 구별되는 별도 실행·입력·비용 영수증·결과를 GitHub PRIVATE에 게시, remote readback 후 GPT 판정 요청. `try_claim` 동일 키 CAS 외 다른 policy revision 키와의 논리 중복, `scan/watch` 경합, `_check_ceilings` 선행 비원자 비용 한도, 결과 게시 실패 재호출 0, Windows `claude.cmd` 적합성에 집중.
5. 리뷰 지적에 대해서는 재현·기술적 심각도와 제한된 수정 범위를 정리; 수정 가능하다면 허용 범위에서 같은 작업 안에 필요한 격리 패치를 준비하고 회귀시험. **ZIP 변경 시 해당 새 ZIP은 기존 리뷰 PASS와 별개이며, 추가 유료 재리뷰는 새 승인 없이 자동 시작하지 않음**.
6. 새로운 **리뷰 4등급 정책 R0/R1/R2/R3는 설계만 등록**된 상태. 기존 v0.2.14 리뷰를 위해 실행 정책/패키지 전체를 수정하지 않음. 추후 상시 예산 정책을 **사용자가 한 번 승인**하면 해당 한도에서 *매 리뷰 건별 반복 승인 없이* 자동 실행하도록 준비. 현재 상시 정책 승인은 없는 상태. 이번 1회 A안 리뷰는 이미 승인된 것이므로 재승인 질문 금지.
7. 최종 결과 하나 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_A_APPROVED_V0214_SINGLE_REVIEW_RESULT_FOR_GPT_20261114.md`와 해당 `CURRENT.md`/`TRACKER.json`을 GitHub PRIVATE `main`에 PR 없이 게시하고 원격 readback. 결과: 키/승인서 준비 여부, 실제 모델 호출 횟수(0 또는 1), 실제 비용/입출력 토큰(알 수 없으면 NOT_AVAILABLE), 독립 리뷰 PASS/FAIL/NOT_RUN, 지적별 disposition, 남은 B 토큰/LIVE 준비 조건을 모아 보고. 조건이 막혀도 같은 작업에서 가능한 나머지 활동 계속.

## 향후 리뷰 등급 자동화: 매번 승인하지 않는 설계
자세한 4개 등급은 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md` 참조.
- 사용자 **사전 상시 예산 정책 1회 명시 승인**을 받으면 요청된 신규 Work에 대해 등급·상한·일간 호출·총비용 제한 안에서 자동 리뷰 가능하도록 개발. 새 요청은 Work ID·고정 ZIP·review ID와 결합해 재사용/무한 호출 금지. GitHub README·ZIP 게시만으로 모델 호출 시작 금지.
- 상한 초과/새 등급/고비용 심층/재리뷰/허용 범위 밖 Work는 별도 명시 승인. 이번 A안은 **특정 v0.2.14 R1 리뷰 한 건**의 승인일 뿐 추후 모든 리뷰의 포괄승인은 아님.

## Windows Claude Code에 붙여넣을 한 문장
```text
GitHub PRIVATE wonhwipark/CoWork-Skill-Collab, main의 collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_A_APPROVED_V0214_SINGLE_REVIEW_AND_TIER_HANDOFF_r0001_20261114.md를 원샷 인계서로 읽고 승인된 A안(동일 Windows PC 서명키+trust warn, REV-COWORK-V0214-20261114의 POLICY-STATIC-V1 최대 $1 독립 리뷰 1회)을 추가 승인 질문 없이 가능한 범위에서 끝까지 진행해줘. 리뷰는 R1 기준 diff 중심으로 압축하고 실제 usage를 기록해줘. B 토큰 신규 발급·설치, LIVE, 운영 DB·Task, 추가 유료 리뷰/재리뷰는 승인하지 않았어. A안의 실행/서명·리뷰가 인증·계약상 막히면 그 부분만 BLOCKED로 남기고 결과 MD 하나와 CURRENT/TRACKER를 PRIVATE main에 올려 원격 재확인해줘. 리뷰 4등급은 별도 계약의 향후 상시 예산 정책 설계로만 보존하고 이번 v0.2.14를 임의 수정하지 마.
```
