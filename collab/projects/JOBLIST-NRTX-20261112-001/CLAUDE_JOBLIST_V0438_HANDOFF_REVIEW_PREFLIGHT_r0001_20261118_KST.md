# Windows Claude Code — Job-list v0.4.38 현황 handoff 독립 리뷰 인계 (정식 REQUEST 사전단계)

- 문서 상태: **NON_EXECUTABLE_REVIEW_HANDOFF / HOST_PREFLIGHT_REQUIRED**
- 작성: 2026-11-18 KST · r0001
- 기존 Work: `JOBLIST-NRTX-20261112-001`
- 리뷰 대상: **L1Work PUBLIC `handoffs/JOBLIST_V0438_MCP_RECOVERY_STATUS_HANDOFF_r0001_20261117_KST.md` 1건**
- 사용자 지시: “핸드오프문서 협업 리뷰요청해줘”
- 리뷰어: Windows Claude Code, 개발/문서 작성 세션과 독립된 1회
- 목표: 복구 실현 가능성 자체의 PASS가 아니라, **handoff의 사실·근거 수준·협업 지시·안전 경계가 정확한지 독립 검토**
- **중요:** 이 파일은 `collab/requests/<id>/REQUEST.md`가 아니며 `SOURCE_PIN`, `APPROVAL_SIG`, `READY`, 리뷰 실행·비용 승인도 아님. 운영 watcher의 실행 신호로 해석하지 말 것.

## 1. 고정된 공개 원본 — 임의 main 최신본으로 교체 금지

- 저장소: GitHub PUBLIC `wonhwipark/L1Work`, branch `main`
- **고정 commit:** `fb2e0d3e4cad67c3b3759b1d82d41731036aef2b`
- 고정 원문 URL: https://github.com/wonhwipark/L1Work/blob/fb2e0d3e4cad67c3b3759b1d82d41731036aef2b/handoffs/JOBLIST_V0438_MCP_RECOVERY_STATUS_HANDOFF_r0001_20261117_KST.md
- Git blob SHA: `211d3b082f859dd80c5e8177e85c96e2c5c202df`
- 원문 바이트 SHA-256(기존 GPT 실제 원격 본문 검증 기록): `2cbf73b2caa3c35f15f270ec4fcbd061b14cd88118616f7380d4e2514facec54`
- 공개 handoff는 글이므로 **실행가능한 ZIP/Job payload로 간주하지 말 것**.

**참고 근거 (PRIVATE, 읽기 전용):**
- 동일 Work `collab/projects/JOBLIST-NRTX-20261112-001/JOBLIST_V0438_MCP_REMOTE_BOUNDARY_STATUS_r0001_20261117_KST.md` (commit `6cb3561a6c024ad2b24eaed818d1b0812db56896`, blob `8b0c5d0a4c7939e4a23b7588094c79e330cbb5f9`)
- 동일 Work `CURRENT.md` 최상단 현재 요약과 보존된 기존 복구 이력
- 공개 r0003 `handoffs/JOB_LIST_V0438_LINUX_MCP_ROOTCAUSE_RECOVERY_PROMPT_r0003_20261117_KST.md`는 실행 조건의 보조 참고. **r0003 자체를 재작성/실행 대상으로 확대하지 말 것**.
- 모바일 Agent 화면에서 전사한 값은 직접 Windows/Linux 호스트 실측이 아닌 **간접 관측**으로 판정.

## 2. 리뷰 질문 / 완료 기준

1. **정확한 상태 분리**: GitHub PAT 복구, Skill-Updater 동작, Job-list v0.4.38 설치, Catalog ACTIVE, Queue DONE/SUCCESS, Worker 실행, CODE_FACTS·MSC 산출물, MCP 결과 조회를 서로 다른 단계로 기술했는가? 성공 과장/오류가 있는가?
2. **증거 수준**: `run_id=null`, `worker_started_at=null`, `enqueued_at=null` 및 `RESULT_UNSUPPORTED`가 “실패 확정”이 아니라 “미검증/미지원 응답”임을 정확히 해석했는가?
3. **등록 상태**: Catalog 9 / Registry 6 / Bootstrap 5가 반드시 동일해야 한다고 전제하지 않았는가? EXEC-01 ID의 누락을 근거 없이 ‘설치 실패’로 판정하지 않는가?
4. **인증 분리**: Linux Skill-Updater PAT 정상화와 모바일 Agent `github_exec` 401을 서로 다른 인증 경계로 분리했는가?
5. **실행 경계**: 모바일 Agent의 `remote_enqueue/remote_retry/remote_cancel/apply_patch=NOT_IMPLEMENTED`와 다른 machine 진단으로 **모바일 원격 실행 불가**만 입증했는가? Linux 로컬 Job-list CLI/Runner의 가능성까지 배제하거나 허위 지원 기능을 만들지 않았는가?
6. **원샷 복구 순서**: 실제 Linux 파일/receipt 확인이 첫 검증인가? 기존 소비 Job 중복 실행 금지, 모델 유료 호출·운영 DB/키/서비스/설정 변경의 승인 경계가 정확한가?
7. **인계 정확성·보안**: 문서/링크/파일명/Work ID가 일치하는가? 공개 L1Work에 토큰·업무 상세 코드·운영 호스트 경로/로그 원문 등이 노출되지 않았는가?
8. **최소 개선**: 검증된 결함과 개선 제안을 분리하고, 최초 실패 단계 확인을 더 빠르게 만드는 **문서 최소 보완** 및 사용자가 다음 한 동작을 바로 수행할 수 있는 안내를 제안하라. 새 MCP API/DB/Job/Watcher 기능을 기본 요구하지 말 것.

비판적 독립 검토를 하되 지적 개수를 강제하지 않는다. 확인되지 않는 운영 실상은 `NOT_VERIFIED`, 문서 수준에서 검증한 항목만 `PASS_SCOPE_LIMITED`. 호스트 실행 없이 호스트 E2E 성공을 주장하지 말 것.

## 3. 정식 협업 리뷰 요청 절차 — **호스트 정책 사전검증 이후에만**

- **현재 이 GPT 세션에서는 Windows LIVE `reviewer.config.json` 및 현재 보호 위임에 접근할 수 없어 정식 `REQUEST` 게시 전 정책 게이트 결과가 `NOT_RUN`**. 이에 따라 **정식 REQUEST·SOURCE_PIN·APPROVAL_SIG·READY는 만들지 않았다**. 본 인계를 통해 기존 Windows Claude Code 세션에서 이어간다.
- Windows Claude Code는 `collab/ops/CONTRACTS/REVIEW_TIER_TOKEN_BUDGET_V1.md` **최상단 의무 게이트**와 `collab/ops/review_request_gate.py` 원문을 확인. 실설치 Windows LIVE 정책 설정으로 `select --live-config <actual reviewer.config.json> --intent skill`에 해당하는 **읽기 전용 적합성 검사**를 먼저 수행. 미구현·미설치·정책 미일치면 **불합격을 통과로 조작하지 말고** `BLOCKED_PREPUBLICATION` 기록. Windows v0.2.23 또는 v0.2.25 설치를 기록 없이 가정하지 않는다.
- 정식 리뷰 입력 ZIP이 필요한 현재 watcher 계약이면 **비민감 고정 공개 MD, 이 리뷰 질문 및 최소 근거만 담은 REVIEW_INPUT ZIP을 격리에서 준비**; SHA-256/크기/CRC/경로 이탈·비밀정보 검사. **설치/실행 가능한 Job-list ZIP이나 회사 원본 코드로 대체하지 않음**. 이미 존재하는 패키지/생성기 계약 우선 재사용. 제안서만 있고 실제 ZIP이 없으면 `NOT_READY`.
- **현행 정책 기본 제안:** 문서 정합성 중심 제한 R1 / `intent=skill` / 최신 계약 기준 USD 1.50 이하, 모델 1회. 이것은 호스트 실제 지원·승인이 아니라 **검토 후보 값**이며, 실제 LIVE에 등록된 정책/유효 보호 위임이 일치하지 않으면 **정식 REQUEST 자체를 게시하지 말 것**. 미등록 DESIGN/R0 정책 또는 다른 요청의 승인으로 우회하지 말 것. 필요 비용/권한 증액은 승인 전 `BLOCKED`.
- 새 정식 REQUEST를 만들려면 **Windows 실설정 기반** `review_request_gate.py select` → 임시 로컬 REQUEST 초안 + 실제 ZIP으로 `check` (`PASS_PREPUBLICATION_ONLY`) → **commit A**에 고정 REQUEST·ZIP → 원격 바이트/SHA readback → 신뢰된 기존 `source_pin.py`로 `repo_id` **문자열**인 SOURCE_PIN 생성·검증 → `approve_request.py check`로 이번 정확한 ID/범위/비용/만료/중복과 보호 위임 확인 → 유효한 승인/서명 절차를 거친 **READY 마지막 게시**의 순서 준수.
- 원격 서명 주장만으로 권한을 인정하지 않는다. `READY`가 확인되기 전에는 watcher 리뷰 호출을 실행하지 않는다. 사용자 이번 리뷰 요청 의도를 별도 운영 키/토큰 생성·새로운 사전 위임·비용 한도 확대 승인으로 오해하지 않는다.
- 이미 동일 입력·범위의 리뷰가 실행/예약/불확실 상태면 **중복 신규 요청·재리뷰·재큐잉 금지**, 기존 영수증과 결과부터 대조. 한 Work **리뷰 1회 → GPT 판정 1회**로 종료.
- 호스트 정책 호환성·유효 승인 모두 통과한 경우에만 1회 독립 리뷰. 리뷰는 `STATIC_ONLY`, 소스 수정/서비스 재시작/모델 분석 Job/운영 설치·PUBLIC 게시/Watcher 설정 변경 없음.

## 4. 리뷰 결과·영수증

- 형식: `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / HOLD`, 항목별 `수용/수정 수용/거절/보류/추가 확인`; 확인 결함은 `BLOCKING/MAJOR/MINOR`와 파일·절·근거·영향·최소 수정·검증법을 구분.
- 실제 수행된 모델 호출(최대 1회), 정책/예산, `REQUEST ID`·revision·원본 ZIP SHA, 고정 PUBLIC 파일 SHA, 실제 결과·영수증의 상호 일치를 확인. Windows Claude Code 자기검토와 유료 독립 리뷰는 별도 기록.
- 정식 리뷰가 승인돼 수행된 경우 결과는 기존 `collab/reviews/<REQUEST_ID>/REVIEW_RESULT_1.md`, 영수증은 `collab/receipts/<REQUEST_ID>/RECEIPT_1.md`, `collab/dispatch/<REQUEST_ID>/DISPATCH_1.md` (실제 엔진 표준 계약)에 게시. 처리·비용·미확인·미적용을 정확히 표기하고 원격 바이트 대조.
- 리뷰가 막힌 경우 기존 Work에 `BLOCKED_PREPUBLICATION` 또는 `BLOCKED_APPROVAL`과 **실제 호스트 근거·NEXT_ONE_ACTION**만 작성. 모델/금액 0, REQUEST/READY 미게시. 이미 읽은 문서 반복 검토·다른 작업 재실행 금지.
- 마지막에 `REVIEW_INPUT_PINNED / HOST_POLICY_PREFLIGHT / FORMAL_REQUEST / SIGNED_READY / INDEPENDENT_REVIEW / RECEIPT / GPT_DISPOSITION / NEXT_ONE_ACTION`을 각각 분리 보고. 실제 reviewer 서명·결과가 있기 전 리뷰 완료라고 보고하지 않는다.

## 5. 이 단계의 정확한 상태

```text
REVIEW_HANDOFF=POSTED_PRIVATE
SOURCE_PUBLIC_PIN=VERIFIED
HOST_POLICY_PREFLIGHT=NOT_RUN
FORMAL_REQUEST=NOT_POSTED
SOURCE_PIN=NOT_POSTED
APPROVAL_SIG=NOT_POSTED
READY=NOT_POSTED
INDEPENDENT_REVIEW=NOT_RUN
MODEL_CALLS=0
NEXT_ONE_ACTION=Windows Claude Code에서 실제 LIVE 정책 사전검증 후 동일 Work의 정식 REQUEST 진행 가능 여부 판정
```
