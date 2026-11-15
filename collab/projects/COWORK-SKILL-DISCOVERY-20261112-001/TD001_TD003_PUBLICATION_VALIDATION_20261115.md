# TD-001~003 — PRIVATE 게시·원격 readback 검증 기록

- 일자: 2026-11-15 KST
- Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 저장소: PRIVATE `wonhwipark/CoWork-Skill-Collab` / branch `main`
- **원격 고정 조회 commit:** `513fdd9eeedbaecedc75e9c3977aed77bc2670df` (이 영수증 게시 **직전** 기준; 아래 9개 blob을 동일 commit에서 읽음)
- 검증 방법: GitHub 연결로 각 경로의 원격 **UTF-8 전체 본문**을 고정 commit에서 재조회 → UTF-8 byte 수·SHA-256 재계산 및 Git blob 확인. SHA-256 계산기 표준 test vector 2종 PASS. 이전 create/update 때 모든 대상 원문과 재조회 본문의 정확한 일치도 개별 확인.
- 검증 대상: 기존 원본/정본 중 **이번 TD-001~003에서 변경·추가한 9개 문서**. 역사의 다른 문서는 전수 재검증하지 않음.

## 1. 대상 파일 9개

| 경로 (저장소 상대 경로) | UTF-8 bytes | SHA-256 | Git blob |
|---|---:|---|---|
| `collab/CONTEXT_BRIEF.md` | 9907 | `b6fca17926725eeea69780e5b06e5195a1bc1bbfdc30199d4163dca3dada2aef` | `4b58e8de56435a80c0617a0c29bc49836a25b7fb` |
| `collab/START_HERE.md` | 17877 | `ac2dfe47432b5c3c93e8339c7238492b3159f9a4ec341f9e03a289a884a9db60` | `e53addc220c74665fa58fd152c3fc4569c9f27e2` |
| `collab/GPT_TODO.md` | 8514 | `6836d6c5c7cdfb6f92463b1d6b1e56a5baa6b3d1283297a062ee7231f53d5ba2` | `f10300adcbce867bb35791c6399d871eda1cf84f` |
| `collab/knowledge/L1_WORKSPACE_RAG_COMMON_r0001_20261111.md` | 26488 | `73dd41f4c946f12c145f74f498b40f2ac1cbe3d1c76c6214570c0e1d29b576b8` | `0450128a070f786ad179b163872036be2100d22c` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/COWORK_L1_INTEGRATED_TOPVIEW_r0001_20261115_KST.md` | 12642 | `1747ae60d283fd15dacb42f13339ebff47ff4193afdea631f20ea2dc1157fe4a` | `8533d42bf77f6bc09db3a16a015d0dda59fbb33f` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/TD002_V07_ACTUAL_NEW_CHAT_VALIDATION_20261115.md` | 5252 | `101e1c4548d7e40905d5052347802221c8a5b567ad4085c237b732fc7478f7dd` | `04c7e6d0ac55be9b4ac3f72e3e97f14008dd75b5` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/TD003_MULTI_SKILL_HANDOFF_FEEDBACK_TRACE_20261115.md` | 8588 | `58b0b5fa4a15de41b15c12d5b58c4af3b68f03ad74066eba82e6d4d7403170fe` | `b1287e9fdece1e599227012b5ca78f3abb40f449` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md` | 20797 | `70edf27b1ac8842fc700b29346eb78052aa2e93100cbc14dc33695599c3d0698` | `85615eff14d819b68b1248e6a1205d646b3cf2e2` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/TRACKER.json` | 506 | `92ade31c773933f7470a209367ed8f4e8203569c92ac12413114178e55e5cb3c` | `ddbeb0cbe44b97539c09b637645d6b1fa7ece281` |

- **원격 readback: 9/9 PASS** (위 고정 commit에 대한 실제 조회).
- 새 문서 3개의 Markdown 상대 링크 **28개/28개**, 이번 세션에서 원문을 실제 읽어 확인한 기존 정본 경로와 일치(PASS). 원격 링크를 자동 실행 API로 해석하지 않음.
- 새 지도 **통합 Mermaid 코드 1개**, 상세 탑뷰의 그림 중복 0개. Mermaid의 실제 GitHub 브라우저 렌더·접근성 E2E는 NOT_RUN.
- `GPT_TODO.md` 상태 TD-001=완료(문서), TD-002=완료(V07), TD-003=작업 연결(문서 추적 PASS, 호스트 E2E NOT_RUN), TD-004=완료. 기존 Work CURRENT 상단과 TRACKER 다음 행동 정합.
- 기존 상세 설계 TODO·L1 r0001/r0002·REQUEST/ZIP/기존 리뷰·영수증·호스트 운영 데이터 수정 없음. 변경된 L1 공통 참고 r0001은 **작성 당시 이관 상태와 현재 상태 조회 위치를 구분하는 포인터 최소 보완**만 적용.

## 2. V01~V10 판정 (증거 범위 한정)

| 기준 | 이번 판정 | 실제 근거·한계 |
|---|---|---|
| V01 전체 통합도/진입 | PASS_DOC | 브리프 단일 흐름도·탑뷰 링크 |
| V02 정본 소유권·갱신 규칙 | PASS_DOC | 탑뷰 SSOT 표/브리프·계약 |
| V03 현행 상태와 과거 r0001/r0002 구분 | PASS_DOC | 공통 참고 현행 포인터/과거 보존 |
| V04 CoWork와 업무 Work/요청 ID 구분 | PASS_DOC | 탑뷰 최소 인계 책임표 |
| V05 피드백 분기·중복 방지 | PASS_DOC | 문서 분기·TD-003 8개 정적 시나리오 |
| V06 현 세션 라우팅 | PASS_SESSION | 기존 TD-002 V06 기록 |
| V07 실제 새 창 수동 재개 | PASS_NEW_CHAT | 이번 TD-002 V07 실조회 문서 |
| V08 링크·원격 본문·UTF-8 bytes/해시 | PASS_REMOTE | 위 9개 + 새 문서 상대 링크 28개 |
| V09 실행/리뷰·Knowledge·RAG 상태 분리 | PASS_DOC | 탑뷰 및 TD-003 한계/승인 구분 |
| V10 첫 실제 Work→Knowledge·RAG | NOT_RUN | Linux MCP/업무 Work·Knowledge 실증 미확인 |

`PASS_DOC/PASS_SESSION/PASS_REMOTE`는 각각 문서/세션/원격 검증의 **세부 범위**이며 코드 설치·호스트 실행 PASS가 아님. `INDEPENDENT_REVIEW=NOT_RUN`.

## 3. 사용자 승인·안전 경계와 다음 한 행동

이번 기록 및 문서 보완은 PRIVATE 비민감 자료로만 진행. 새 유료 Claude 호출·REQUEST/READY·PUBLIC ZIP·운영 Windows/Linux Task/DB/키/토큰·provider/LIVE·업무 그룹 Knowledge write **0건**. 기존 사용자 승인·비용·레거시/소비 Job 보존.

**NEXT_ONE_ACTION:** 기존 [NR 실제 분석 CURRENT](../NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md)에 따라 이미 허용된 Linux Agent 경로에서 v0.4.38 설치 SHA·신규 Job/Run/Receipt·MCP result readback의 동일 ID 확인. 코드 분석/지식 후보 전파는 실제 권한/증거 조건에 맞추어 해당 기존 업무 Work로 회수; TD-003을 E2E PASS로 소급하지 않음.

**검증 문서 자체:** 이 문서를 게시한 뒤 다시 원격 본문·blob을 확인. 위 9개 해시는 **영수증 게시 직전 고정 commit의 target bytes**이며 영수증 자신의 SHA나 향후 추가 커밋의 자동 확인을 뜻하지 않음.
