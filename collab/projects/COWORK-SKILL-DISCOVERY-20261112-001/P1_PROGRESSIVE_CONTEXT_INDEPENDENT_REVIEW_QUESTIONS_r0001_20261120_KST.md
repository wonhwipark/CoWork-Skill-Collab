# CoWork P1 독립 설계 리뷰 — 질문·판정 계약 r0001

- 작성: 2026-11-20 KST / 입력 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 리뷰 종류: **독립 R1 설계·정보 구조·상태 정합성·사용성** / `STATIC_ONLY` / 최대 모델 호출 1회·단일 요청 USD3 이하
- 리뷰어: Windows Claude Code watcher의 **독립 reviewer** (같은 개발 세션 자체검토는 제외)
- 고정 입력: `P1_PROGRESSIVE_CONTEXT_EVIDENCE_DASHBOARD_DESIGN_r0001_20261120_KST.md` + 이 문서 + 입력 manifest; ZIP bytes/hash는 정식 요청 단계에서 재고정.
- 기존 PRIVATE 운영 코드, 업무 Linux 코드/로그, 회사 자료, 현재 host 파일·DB는 **접근 또는 실행하지 않음**.

## 요청 요약
사용자는 'CoWork 전체 구성과 최신 상황을 새 창에서도 빠르고 안정적으로 이해하는 방법'을 요청. 신규 플랫폼/스킬/DB/지식 엔진 없이 기존 `CONTEXT_BRIEF → CURRENT → 근거`, 단계별 검증, 기존 B안 UI를 재사용하는 P1 설계를 검토해 달라는 정식 **한 번의 독립 설계 리뷰**임.

## 독립 리뷰 질문 (10개)
- **Q01 범위 적절성:** 기존 통합 탑뷰 TD-001, 새 창 TD-002, CURRENT·카탈로그·기존 B안 UI와 중복 구현하지 않으면서 P1 목적을 달성할 수 있나? 불필요한 신규 엔진·원장·스키마/대시보드 중복 요구가 있는가?
- **Q02 라우팅:** L0/L1/L2 라우팅에서 '전체', '원인', '최신 버전', 'Knowledge', '리뷰 완료' 등 질문이 잘못된 Work로 연결되거나 필수 근거를 건너뛸 반례는 무엇인가? 종료·확장 규칙은 실행 가능하게 명료한가?
- **Q03 시간·근거:** 개발 후보/배포·LIVE·승인/READY/REVIEW/receipt/호스트 분석을 섞지 않는가? 최신 파일이 오히려 오래된 사실을 기술할 때 판정 방식이 모호하지 않은가?
- **Q04 위험 경계:** 과거 `GUARD UNCERTAIN`, 정책 STATIC/보호 위임 불일치, Queue `DONE`/NULL `run_id`, GitHub readback 대 호스트 실측 같은 사례에서 **거짓 PASS 0**이 가능한가?
- **Q05 PRIVACY:** CoWork PRIVATE 상세와 PUBLIC `L1Work` 허용목록을 구분했는가? PUBLIC 4개 카드가 기존 5개 카테고리/인계 3개 제한·비밀 차단 정책과 양립 가능한가? 새 데이터 필드 없이 표현 가능한가?
- **Q06 UX:** 휴대폰 390/320px, PC 1440/1366px의 1화면 요약이 실사용자의 '현재 / 차단 / 다음 조치' 파악에 도움 되는가? 30초 과제, 상호작용과 접근성 측정이 현실적인가?
- **Q07 정확성/성능:** 30문항 A/B에서 실제 정답 주관성을 줄이려면 어떤 최소 골든셋·고정 시간/sha·실측 로깅이 필요한가? 현재 ≥29/30, zero false PASS, tokens 35% 목표는 목표로서 적절한가?
- **Q08 기존 시스템 재사용:** 현재 B안 대시보드 exporter/Actions, Work tracker, GitHub source pin, 연결된 GitHub 조회로 가능한 범위와 **G0 미검증** 영역을 정확히 나눴는가? 새로운 기능 부재를 단정하는 대목이 있는가?
- **Q09 실패 안전성:** GitHub 조회 실패/정보 부재/동시 업데이트·서로 모순된 호스트 보고 시 fail-closed와 마지막 확인 시각 표시가 충분한가? 사용자 조치를 막는 과도한 경고가 예상되는가?
- **Q10 최소 실행 계획:** 구현 순서가 REUSE→CONNECT→근거 있는 최소 EXTEND에 부합하는가? P1만으로 시작해도 되는 부분과 미룰 P2/P3, 필수 승인·독립 리뷰·운영 검증을 명확히 구분했는가?

## 독립 리뷰 결과 형식
1. `REQUEST_ID`, `REVISION=1`, `PACKAGE_SHA256`, `REVIEWER`, `REVIEW_KIND=INDEPENDENT_DESIGN`, `INPUT_READ=PASS/PARTIAL/NOT_RUN`.
2. 판정 `ACCEPT / ACCEPT_WITH_CHANGE / REVISE / PARTIAL_SCOPE`; 결함 severity `BLOCKING/MAJOR/MINOR/RECOMMENDATION`과 각각 구체적인 근거 위치·사용자 영향·최소 수정·검증 방법.
3. **P1 필수 수정**과 선택 P2/P3를 구분. 결함 수를 강제하지 말고 문제없으면 없다고 보고.
4. **기존 재사용 가능/불가능 또는 미검증** 경계를 증거 중심으로 판단하고 코드 구현·실제 Windows 정책/호스트 검증을 수행했다고 주장하지 말 것.
5. 30문항 평가의 최소 수정 권고와 성공 여부를 판별할 핵심 지표(실제 실험치가 아니면 목표라고 표기).
6. 결론 1문장, 우선순위 3개 이내, GPT 판정에 필요한 미확인 항목.

## 안전·중복·승인
- **새 요청만** 1회. 이미 완료된 디자인·위키 UI·Knowledge Guard·Watcher review 재호출/소급 서명 금지.
- 실제 Windows LIVE config 기준 `review_request_gate.py select/check --intent unified --required-budget-usd 3.00` **출력 PASS 확인 전 REQUEST/READY 게시 금지**. 현재 구 LIVE STATIC=$1.50/보호 위임=$1인 경우 `POLICY_COST_MISMATCH`면 모델 호출 0.
- 과거의 수동 DESIGN $3 예외는 다른 특정 리뷰 ID 전용. 이를 이번 P1으로 자동 확대하지 않음.
- 유효한 보호된 서명·READY 마지막, SHA/크기/ZIP CRC/source pin repo_id JSON 문자열·중복 검증이 없으면 실행하지 않음.
- 모델/결과 게시 불확실 시 재호출 금지. GitHub PRIVATE 문서 게시나 Claude Code 로컬 자체검토는 독립 reviewer 실행이 아님.
