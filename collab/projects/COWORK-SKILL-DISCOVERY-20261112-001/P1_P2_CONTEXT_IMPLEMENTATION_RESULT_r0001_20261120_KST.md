# CoWork P1·P2 적용 결과 — 질문 중심 맥락·관계·변경분·B안 빠른 화면 r0001

- 작성: 2026-11-20 KST / Work `COWORK-SKILL-DISCOVERY-20261112-001`
- **요청 승인:** “리뷰없이 진행후 적용해줘. 이후 p2 도 동일하게 진행해줘” — 이번 **P1/P2 맥락 조회·화면 변경에만** 독립 리뷰 명시적 생략. 다른 Work나 Watcher/Knowledge Guard 코드 리뷰 생략 승인 아님.
- **결론:** `P1_IMPLEMENTATION=PASS_SCOPED`, `P2_IMPLEMENTATION=PASS_SCOPED`, `PUBLIC_PAGES_SOURCE=POSTED`, `PAGES_ACTION=SUCCESS`, `PRIVATE_READONLY_QUERY_TEST=PASS`, `INDEPENDENT_REVIEW=SKIP_BY_USER`, `HOST_E2E=NOT_RUN`, `30_QUESTION_BENCHMARK=NOT_RUN`, `MODEL_CALLS=0`.
- 소유: 맥락/Work 관계는 기존 스킬 관리 Work; 대시보드 화면은 기존 `COWORK-GITHUB-DASHBOARD-20261111-001`.

## 1. 실제 적용 변경

| 항목 | 범위 | 결과 |
|---|---|---|
| P1 PRIVATE 선택 조회 | `collab/dashboard/context_query.py` | 질문→기존 5개 영역 Work의 CURRENT 최상단만 조회. 없는 자료는 `CURRENT_NOT_VERIFIED`. 항상 현장 실행 여부는 미확인 표시 |
| P2 PRIVATE 관계 탐색 | 동일 파일 | 해당 Work `work_id`를 가진 REQUEST를 찾아 PACKAGE/SOURCE_PIN/서명/READY/독립 결과/RECEIPT **존재만** 관계화. 미검증을 완료로 승격하지 않음 |
| P2 PRIVATE 비교 | 동일 파일 `--baseline-commit` | 지정된 40-hex Git commit의 CURRENT 최상단과 현재 LOCAL 내용을 텍스트 diff; 기준 없으면 `NO_BASELINE`. 파일/호스트 상태 수정 없음 |
| P1 PUBLIC 요약 | `docs/cowork-dashboard/index.html`, 신규 `context-view.js` | 기존 B안의 공개 상태 기반 네 카드: 협업/스킬/업무 실행/L1 지식. '공개 자료 마지막 변경'은 호스트 실측 시각이 아님 |
| P2 PUBLIC 관계·변경 | 기존 B안 내 접힘 상세 | 공개 허용된 업무 범주 간 **개념적** 책임 흐름 + 화면 열람 중 이전 승인된 JSON과 변화분만 표시. 이전 스냅샷 없으면 `NO_BASELINE` 의미로 안내 |
| 브리프·운용 | `CONTEXT_BRIEF.md`, [적용 가이드](P1_P2_CONTEXT_APPLICATION_GUIDE_r0001_20261120_KST.md) | 새 창 시작 시 P1/P2 기존 조회 경로 포인터. CURRENT와 상세 근거가 계속 정본 |

**변경하지 않음:** 기존 PRIVATE watcher/approval/READY/DB/비용 정책, 공개 `status.json` 스키마·exporter/allowlist·hand-off 3건·board.js/status.js, Windows Claude Code, 업무 GPT·Linux MCP/LLM, 스킬 ZIP, 개인/그룹 Knowledge, 다른 운영 서비스.

## 2. 실제 게시본 및 정확한 bytes

**PUBLIC** `wonhwipark/L1Work`, `main`
- `docs/cowork-dashboard/context-view.js`: **6539 B**, SHA-256 `dce69693255e96a69dde9b879de2044de89c96fcba740a1bf94d4b949ee1b164`, Git blob `fa9f64e11da72de6ef10944330a9e5f39cf1cce5`. Commit `b70686e6859a042471c2da6a0bdcec4963ed4fec`.
- `docs/cowork-dashboard/index.html`: **23397 B**, SHA-256 `4cce5b380c6348a6036d5ef5ff07ba5c3a2382421fe6d00a3b7d1783566251e1`, Git blob `dc81827c3140aafc37269cdfeeca0d9b15304d6f`. Commit `56c042fb3283a8a223a7b3a391e63f27cdebfb61`.
- 실제 Pages [Action #44579614254](https://github.com/wonhwipark/L1Work/actions/runs/44579614254) `completed/success` (HTML commit 기준).
- 기존 공개 URL: https://wonhwipark.github.io/L1Work/cowork-dashboard/ (기존 서브화면 3개, PUBLIC 허용목록 불변).

**PRIVATE** `wonhwipark/CoWork-Skill-Collab`, `main`
- `collab/dashboard/context_query.py`: **8582 B**, SHA-256 `20af157f2903434b57a7d1603cf1ef08dcf6e086aff4907f6cfd6a6110d34174`, Git blob `a6a1f99849bf524646c1e9264c42acefbf215714`.
- `collab/dashboard/tests/test_context_query.py`: **5153 B**, SHA-256 `55a9cb9e3eaa1d69ce8e65b4c15819fd1b08a7bf035b0b17d8a099b36b11bbbc`, Git blob `89d433b976383a02653fcabb4085fbd42a313a34`.
- [적용 사용법](P1_P2_CONTEXT_APPLICATION_GUIDE_r0001_20261120_KST.md) 및 새 브리프 포인터 게시.
- 기존 [CoWork PRIVATE Dashboard Action #44580631352](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44580631352) `completed/success`, Python `unittest discover -s collab/dashboard/tests` 포함 기존 계약 시험 성공.
- 이후 PUBLIC allowlisted sync [#44580676608](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44580676608) `completed/success`; 이것은 공개 상태 exporter에 Private 링크를 추가했다는 뜻이 아님.

## 3. 검증 실적과 한계

**PASS — 직접 확인**
- GitHub `main`의 공개 HTML+JS와 PRIVATE Python/시험 파일 **원격 blob 및 UTF-8 실제 바이트 SHA-256 계산**.
- PUBLIC JS V8 문법 파싱 PASS, 기존 `board.js`/세 서브화면·CSP·HTML 새 요소 각 1개 존재 정적 PASS.
- 격리 합성 DOM으로 **P1 4카드/개념 관계/기준 없음** 렌더 PASS, 공개 상태 한 항목 변경 시 **P2 변경 관측** PASS, 무효 provider·허용 외 업무 범주 입력 시 **요약/관계/변경분 모두 FAIL-CLOSED** PASS.
- PUBLIC JS `textContent`만 사용, `innerHTML/document.write` 없음, same-origin `status.json` GET 이외 외부 fetch/저장 없음.
- PRIVATE Python 격리 단위시험 9개 시나리오 추가: 질문 라우팅, 과거 절 미선택, 미존재 Work, 관계 미추정, 다른 Work 누락, symlink/path traversal, 이전 commit 부재, host 미검증, scan 상한. 기존 Dashboard Action `success`.
- 신규 PUBLIC Pages build/deploy Action `success`, 기존 자동 exporter/Pages 흐름 변경 0.

**NOT_RUN / 별도 확인**
- 사용자의 모바일/PC 실제 화면 상호작용·키보드·접근성·이해 시간 및 실제 HTTPS 화면 렌더, 30문항 골든셋 정확도/토큰/조회 시간 A/B 측정. 합성 DOM은 실화면 검증이 아님.
- PRIVATE `context_query.py` 실호스트(Windows/Linux) 실제 호출·git baseline diff 실제 업무 시나리오, GitHub 원격 최신 HEAD/CURRENT와 자동 동기화 시험. 이 조회기는 **로컬 사본**이므로 실제 LIVE·원격 최신 상태를 확인했다고 주장하지 않음.
- Claude 독립 리뷰는 이번 사용자 요청의 범위에서 **SKIPPED**이며 PASS가 아님.

## 4. 안전한 후속

기존 리뷰 후보 `REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120`은 Windows `HOST_PREFLIGHT_BLOCKED`로 정식 REQUEST/READY가 없음. 새 사용자 리뷰 생략 지시에 따라 **그 요청을 재생성하거나 signer/READY/유료 리뷰 호출하지 않음**. 과거 P1 요청 기록을 삭제/수정하지 않고 '새 P1/P2 구현은 사용자 리뷰 생략'으로 분리.

**NEXT_ONE_ACTION:** 사용자 PC·모바일에서 기존 [PUBLIC B안 대시보드](https://wonhwipark.github.io/L1Work/cowork-dashboard/)의 첫 화면 네 카드와 P2 펼침/관계/변경 안내를 실제로 확인. 표시 문제가 발견되면 기존 대시보드 Work에서 최소 보완. 이후 정확성·속도 정량 검증은 30문항 표본을 고정한 별도 평가로 실행.
