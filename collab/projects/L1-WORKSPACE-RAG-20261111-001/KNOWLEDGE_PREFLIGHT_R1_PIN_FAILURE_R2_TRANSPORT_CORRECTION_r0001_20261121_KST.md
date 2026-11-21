# knowledge_analysis_preflight v0.2.0 — R1 SOURCE_PIN 장애와 R2 신규 전송 정정

- 날짜: 2026-11-21 KST
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 대상: Windows Claude Code 독립 코드 리뷰 요청 (실행·결과·비용 없음, 요청 정정만)
- 계보: `REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121` (무효 핀, 보존) → `REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121` (CREATE-ONLY 새 요청)
- **실제 사용자 제공 Windows 감시기 진단:** 2026-11-20T23:33:32Z, R1 `AUTO_NOT_ELIGIBLE` + `WAIT_INPUT`, `COMMIT_UNREADABLE`; R1 SOURCE_PIN `84abde50d7c960ca5ec065b392f8aece84bde85d`에는 고정 ZIP만 있고 REQUEST는 이후 `1a49b3cf61e4863a209b202f41531b14d8ab8031`에 게시됨. 감시기는 정상 스캔하며 서명·READY·job·receipt·review 없음(사용자 제공 실측, GPT 직접 Windows 호스트 검증은 아님).
- **두 번째 차단 원인:** `knowledge_analysis_preflight`는 현재 보호 위임 자동 허용 `cowork-review-watcher`, `cowork-dashboard`, `l1-knowledge-updater`에 **포함되지 않음**. 이 문제를 해결하기 위해 요청의 `skill_id`를 위장하거나 자동 서명 위임 범위를 임의 변경하지 않음.

## 정정 실행·원격 확인

| 항목 | 확인 값 | 판정 |
|---|---|---|
| R1 원문·PIN 이력 보존 | 기존 경로 불변, 요청 재큐잉/수정/삭제 없음 | PASS |
| R2 요청 경로 | `collab/requests/REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R2-20261121/REQUEST.md` | PASS |
| Commit A — R2 REQUEST 최초 게시 | `50a8b5d9e832b1fbf9095c729c813e83134b1fd8` | PASS |
| Commit A에서 REQUEST 실존 | blob `1067a502abdacf7ed314efd986b1b2f4aff6864f`, 실제 본문 동일 | PASS |
| Commit A에서 패키지 실존 | `collab/packages/knowledge_analysis_preflight_v0_2_0_1121_REVIEW_INPUT.zip` blob `bbacdcfd33860060552ef5928be0f37b6b436cdb` | PASS |
| 고정 ZIP 바이트 | 16138 B, SHA-256 `90a0d55842138d4c813f0dbc3a5c8e4625e84a110afe68035348297ffedad1f3`, R1과 동일, 이전 원격 base64 바이트 검증 재사용 | PASS |
| Commit B — SOURCE_PIN 게시 | `5493470341c5a6ffd1dad31f34c33269317c81f9` | PASS |
| SOURCE_PIN 내용 | `commit=50a8b5d9e832b1fbf9095c729c813e83134b1fd8`, `repo_id="1451933830"` 문자열, 원격 readback 일치 | PASS |
| 정식 자동 서명 | `skill_id` 미허용 | NOT_ELIGIBLE |
| 승인·서명 / READY / reviewer / receipt / job | 호스트 최신 재판정·실제 신규 실행 미관측 | NOT_RUN/NOT_OBSERVED |
| 최종 PUBLIC ZIP 배포 | 독립 리뷰와 GPT 판정 전 | HOLD |
| 업무 GPT Updater 구현 인계 r0002 | PUBLIC ZIP 확정 후 | HOLD |

## 안전 계약

- 기존 R1은 `WAIT_INPUT`/실행 안 됨으로 보존. 새 R2를 제출했으나 동일 패키지를 재빌드하거나 동일 모델을 재실행한 것은 아님.
- SOURCE_PIN은 자신이 게시된 커밋을 가리키지 않아도 됨. **REQUEST 및 ZIP이 함께 있는 Commit A**를 가리켜야 하며 R2는 이를 충족함.
- `skill_id=knowledge_analysis_preflight` 그대로 유지, 자동 위임에 등록되지 않으므로 정상적인 AUTO_NOT_ELIGIBLE 예상. **별도 유효 수동 1회 승인** 없이는 signer/READY 생성 금지. 위임·정책·비용/만료·키/DB/LIVE 변경 금지.
- 수동 승인·서명 적격성 검토 시 기존 R1/R2 호출·청구 이력 0/중복을 재확인, 감시기 정책 `POLICY-STATIC-V1` 한도 USD 3.00을 넘기지 않아야 함.
- GPT는 APPROVAL_SIG.json·READY.md를 생성하거나 보호 signer 역할을 가장하지 않음. 현 시점 `HOST_MANUAL_REVIEW=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`.
- **재발 방지:** 새 리뷰마다 (1) 고정 ZIP commit/readback (2) REQUEST commit **당시** 같은 commit에서 REQUEST·ZIP 검증 (3) REQUEST·ZIP이 모두 존재하는 commit으로 PIN (4) 올바른 skill_id/scope 확인 (5) 유효 승인·서명 확인 후 READY 마지막 순으로 고정.

## 다음 한 동작

Windows Claude Code/보호 signer가 **R2에 대한 공식 수동 단일 리뷰 승인의 권한·비용·중복**을 실제 호스트에서 검사하고, 유효한 별도 수동 승인이 있을 때만 보호 signer로 승인·READY 마지막 게시·리뷰 한 번 실행. 불가할 경우 HOLD/BLOCKED reason만 보고. 리뷰 결과·영수증 readback을 GPT가 확인한 뒤 배포 여부를 판정.
