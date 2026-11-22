# v0.2.31 독립 리뷰 단일 실행·비용 상한 제거 — GPT 후보 판정

- 판정일: 2026-11-22 KST
- Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 기준: `CLAUDE_INDEPENDENT_REVIEW_IDEMPOTENT_CANDIDATE_RESULT_FOR_GPT_20261122.md`, 최신 `CURRENT.md`
- **GPT_DISPOSITION: ACCEPT_DEVELOPMENT_WITH_CONDITIONS**
- **LIVE_CUTOVER: HOLD_NOT_AUTHORIZED**
- **COST_UNBOUNDED_LIVE_RISK: USER_ACCEPTANCE_REQUIRED**
- **SCOPE_MANIFEST: CONDITIONAL_DESIGN_ACCEPTANCE; IMPLEMENTATION_AND_DELEGATION_NOT_AUTHORIZED**

## 근거와 확인 범위

Windows Claude Code 보고와 GitHub main 원격 결과 문서/CURRENT의 내용 일치 확인. 자체 회귀: 960 PASS / 0 FAIL / 12 SKIP, 신규 8건, FakeReviewRunner·in-memory transport 기반 모델 호출 0. 실제 Claude CLI 실행, 두 watcher가 **동시**에 처리하는 경쟁 시험, 기타 터미널 실패 및 부팅 시 CLAIMED/RUNNING 봉인의 별도 시험은 NOT_RUN. Windows 운영 PC, 설치본, DB, 키 및 ZIP 실물은 GPT가 직접 검사한 것이 아니며 독립 리뷰도 NOT_RUN.

후보: Windows 로컬 `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_31_independent_idempotent_candidate.zip`, 291,484 bytes, 103 entries, reported SHA-256 `1df85457ec01eaaa1a63022777f40b658732355e9d4f016a92b07076da950ea3`. GitHub PUBLIC에는 결과 메타데이터만 존재하고 후보 ZIP 없음. SHA는 Windows 호스트 보고값으로서 이 GPT의 독립 바이트 해시 검증을 의미하지 않음. v0.2.30 기존 ZIP 보존.

## 판단

1. **비용 게이트 제거의 기술적 방향 수용:** 신규 독립 리뷰 단일 경로에서 `--max-budget-usd`, 금액 기반 입장 차단 및 금액 0 클레임 거부 제거. `accounting_reference_usd`는 회계 참고값이지 실제 모델 청구액이나 실행 상한이 아님. 기존 요청/결과/영수증 보존. **단일 Claude CLI 작업 내부의 모델 턴 수·청구 금액은 무상한**이므로 이는 비용 통제 대체가 아니라 명시적 재정 위험. 사용자가 LIVE 위험을 수용하지 않은 현 단계에서 LIVE 배포 승인으로 해석 금지.
2. **요청 ID 중복 방지 후보 수용:** 반복 스캔·동일 DB 재시작·새 DB 순차 두 번째 watcher·다른 ZIP 충돌·timeout UNCERTAIN·게시 재시도 시험은 자체시험 PASS. 그러나 두 watcher의 동시 경합/원격 create-only 경쟁을 직접 실증하지 않았으므로 global exactly-once는 운영 E2E PASS가 아님.
3. **LIVE 전 선행 보호 검증:** 격리된 두 독립 watcher/DB의 동시 경합 테스트(Barrier, 동일 ID·PIN·ZIP)와 디스패치 1회/청구 모델 호출 최대 1회 입증, 충돌·크래시·결과 게시 실패 시 재모델 호출 0, terminal FAILED/부팅 시 잔여 CLAIMED/RUNNING 봉인·새 모델 호출 0, ZIP 실물 SHA/CRC 및 백업·롤백·실제 LIVE 보호 설정 확인. 개발자 자체시험과 별도 독립 리뷰/실제 운영 승인 분리. 모든 시험은 fake runner/stub로 무과금 수행 가능; 실제 유료 모델 호출은 추가 사전 승인 없이는 수행하지 않음.
4. **SCOPE 설계 조건부 수용:** 유효한 사용자 의도·권한에 **독립적으로 인증된 보호 서명**을 바인딩한 명시적 매니페스트만 검토. 이 매니페스트가 (a) watcher 자신이 임의로 발급·서명해 권한을 확대하거나 (b) GitHub 본문에 적힌 서명 주장만으로 승인됨을 뜻하지 않아야 함. 신뢰 주체·별도 보호 키의 소유/활성화, 대상 repo/project family·exact skill ID·요청 시점 이후 적용·만료/nonce·재사용 차단·서명 검증, 기존 `SOURCE_PIN`과 `READY`의 경계를 명시하고, 보호 정책의 확장에는 실제 유효한 사용자 위임/운영 승인이 필요. 와일드카드·구 REQUEST 소급 승인·`cowork-context-design` 무단 추가 금지. **설계 후속 검토는 허용, 운영 위임 변경/구현 설치/신규 유료 리뷰는 미승인**.
5. LIVE 설치에는 **별도 사용자 승인**과 단일 provider, 설정·DB/WAL/SHM·작업/Notifier·키·위임의 보존/복원, 동일 ZIP SHA 검증, fail-closed 및 롤백 검증 필요. 현행 Windows v0.2.29 운영 설치본 불변(마지막 Windows 보고 기준).

## 현재 결과

| 구분 | 판정 |
|---|---|
| Windows 개발자 자체시험 | 960 PASS / 0 FAIL / 12 SKIP (HOST_REPORTED) |
| GitHub 결과/CURRENT readback | PASS |
| ZIP 본문 GPT 직접 검증 | NOT_RUN (Windows 로컬에만 존재) |
| 동시 두 watcher 경합 실증 | NOT_RUN |
| v0.2.31 독립 리뷰 | NOT_RUN |
| 비용 무상한 LIVE 수용 | NOT_AUTHORIZED |
| LIVE 컷오버 | HOLD |
| SCOPE 사용자 위임 확대 | NOT_AUTHORIZED |
| 기존 REQUEST 재디스패치 / 신규 모델 호출 | 0 (보고 범위) |

**NEXT_ONE_ACTION:** Windows Claude Code가 *동일 Work/기존 v0.2.31 후보*에서 **실제 과금 0의 동시 두-watcher 경합 + 미시험 terminal/재시작 분기**만 추가 격리 검증하고 결과·CURRENT를 GitHub main에 게시해 원격 바이트 확인. 별도 새로운 요청 ID/유료 리뷰·기존 요청 재큐잉·LIVE 설치/위임 변경은 수행하지 않음. 그 결과와 사용자의 비용 위험 수용/운영 승인 여부로 LIVE 컷오버를 다시 판정.
