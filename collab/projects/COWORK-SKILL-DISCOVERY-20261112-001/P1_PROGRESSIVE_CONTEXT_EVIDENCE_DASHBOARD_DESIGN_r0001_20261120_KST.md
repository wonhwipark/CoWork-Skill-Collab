# CoWork P1 — 질문 중심 단계별 맥락 조회·시점/근거 판정·한 화면 요약 설계 r0001

- 작성: 2026-11-20 KST / **DESIGN_CANDIDATE_FOR_INDEPENDENT_REVIEW** (구현·운영 적용 아님)
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main`
- 소유 Work: `COWORK-SKILL-DISCOVERY-20261112-001`; 기존 대시보드 구현 소유자 `COWORK-GITHUB-DASHBOARD-20261111-001`
- 사용자 요청: 복잡한 스킬·협업·업무 GPT·Linux LLM·L1 Knowledge 전체를 **빨리 이해하고 현재 사실을 안정적으로 판정**하는 P1 설계 및 Windows Claude Code 독립 협업 리뷰
- 결정 경계: 기존 브리프/CURRENT/결과·영수증/Tracker/대시보드 재사용. 새로운 Agent·RAG/그래프 엔진·Watcher·원장·DB·스키마·비용 정책·자동 실행 트리거 **도입하지 않음**.

## 1. 문제 및 성공 조건

### 현행에서 관측된 문제
1. 전체 협업·L1 연결을 한 번에 설명하면 질문과 무관한 스킬/Work/운영 이력이 섞여 찾는 시간이 늘어남.
2. 과거 설계의 `LATEST`, 개발 ZIP과 PUBLIC ZIP, LIVE 설정과 향후 후보, PRIVATE 게시와 호스트 검증을 혼동하기 쉬움.
3. REQUEST 게시가 곧 승인/READY/Claude 리뷰가 아니며, Job `DONE`이 Worker/Run/Evidence 완료를 입증하지 않는 등 **단계별 검증 경계**가 존재.
4. GitHub PRIVATE 상세와 PUBLIC `L1Work` 허용목록 대시보드의 정보 공개 수준이 다름. 잘못된 자동 요약은 업무 정보 반출 또는 상태 오판을 유발할 수 있음.

### 성공 정의
- 사용자 질문 한 개당 첫 응답에는 **판정 1줄 + 현재 상태/차단/다음 한 행동 + 주요 근거/확인 시각**만 노출. 요청받으면 상세 Work와 원본 근거로 내려감.
- GPT 또는 Windows Claude Code가 질문에 맞는 기존 CURRENT를 선택하고, 관련 없는 Work/스킬을 기본 탐색하지 않음.
- 운영 LIVE, 독립 리뷰, PUBLIC 배포, Linux 설치, 실제 업무 분석, Knowledge 게시를 **서로 다른 증거·판정**으로 유지.
- 사용자에게 현재 사실이라고 제시하는 모든 중요한 판정에는 근거·시점·실행 수준을 함께 제공. 충돌·조회 실패는 `NOT_VERIFIED`/보류로 표시.
- 공개 대시보드는 기존 allowlist만 사용하며 PRIVATE ID/경로·업무 데이터·서명·token·비용 세부/영수증 원문을 유출하지 않음.

## 2. REUSE 판단 및 정본 경계

| 구성요소 | 현행 정본/기능 | P1 적용 | 하지 않을 일 |
|---|---|---|---|
| 공통 구조·라우팅 | `collab/CONTEXT_BRIEF.md` | 목적별 기존 Work 선택 | 현재 LIVE/버전/REQUEST 상태 복제 |
| 개별 상태 | 각 Work `CURRENT.md` 최상단 | 최신 짧은 요약·열린 메모·마지막 결과 포인터 | 상세 이력 재복제·모든 Work 자동 읽기 |
| 검증 근거 | 기존 `RESULT`, `REVIEW_RESULT`, `RECEIPT`, GitHub commit, 실제 호스트 결과 | 검증 질문이 요구할 때만 필요한 파일 조회 | 실측 없는 PASS/READY/실행 추정 |
| 스킬 책임 | `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` | '어느 스킬 담당?'일 때만 사용 | 전체 스킬 전수감사 |
| 기존 대시보드 | `COWORK-GITHUB-DASHBOARD-20261111-001`, 기존 exporter/JSON/UI | 단일 화면 핵심 카드와 상세 펼치기 UX 설계 | 새 공개 포털·새 exporter·PUBLIC 허용목록 확대 |
| 업무 실행 | 업무 GPT·Linux MCP·Agent/LLM, 업무 `l1-workspace`, 그룹 `l1sw-dev-knowledge` | 동작 책임/근거 경계 표기 | 업무 원본 조회 권한 가정·호스트 모델 호출 |
| 협업 리뷰 | `REQUEST → 승인/서명 → READY → REVIEW_RESULT/RECEIPT → GPT 판정` | 단계별 상태 별도 표기 | GitHub 문서 게시로 watcher 실행 주장 |

**근거 수준을 섞지 않음:** 문서 설계 < PRIVATE 게시/readback < 격리 자체시험 < 별도 독립 리뷰 < 실제 호스트 설치/호출 < L1 실행 결과/Knowledge readback. 순서가 언제나 자동 우열을 뜻하는 것은 아니며, **주장별 직접 증거**가 우선.

## 3. P1-A: 질문 중심 Progressive Disclosure 라우팅

### L0 / L1 / L2
- **L0 (기본 1화면):** 질문 분류, 확인한 최신 상태·시각, 핵심 차단 1건, 다음 한 동작, 증거 링크 1~3개. 전체 흐름도를 기본 본문으로 출력하지 않음.
- **L1 (관련 영역):** 목적별 CURRENT와 상단 현재 요약, 해당 Work의 최신 결과·열린 메모를 확인. 질문이 '원인'이면 관련 승인/배포/호스트의 경계만 추적.
- **L2 (원문 증거):** 리뷰·영수증·SOURCE_PIN·커밋·원본 시험·호스트 readback 중 **현재 답변에 부족한 것만** 확인. 필요할 때 다수 Work를 횡단하되 근거 연결 경로를 설명.

### 목적별 라우팅 규칙 (기존 브리프의 포인터 재사용)
| 질문 | 우선 Work | 추가 조회 조건 |
|---|---|---|
| 'Claude 리뷰 왜 멈췄어?' | 이관 CURRENT + 자동 승인 CURRENT | 특정 REQUEST의 실제 READY/결과/영수증, 필요 시 호스트 상태 |
| '최신 스킬 PUBLIC 배포됐어?' | 스킬 관리 CURRENT + L1Work `main` 실제 목록 | 정확한 ZIP명/bytes/SHA/원격 commit, 대상 스킬 Work |
| '업무 GPT/LLM 코드 분석했어?' | NR 분석/Job 진단 Work | 실제 Linux Run·Worker·Evidence를 확인할 권한이 있을 때 |
| 'Knowledge 반영됐어?' | L1 Knowledge Work | 개인 Work/Evidence, Preview, 승인, 그룹 commit/readback 등 |
| '화면 잘 보여?' | 기존 대시보드 Work | 기존 PUBLIC JSON/Pages·브라우저 관측/허용목록 |
| '전체 구조?' | CONTEXT_BRIEF의 단일 탑뷰 | 사용자 선택 분야에서만 추가 상세 |

**조회 중단 규칙:** 먼저 브리프의 목적별 경로 + 관련 CURRENT를 활용. 이 둘로 충분하면 종료. 모순·실측 주장·결정/승인·시간 의존성이 있으면 관련 결과/호스트 근거까지 확장. **'조회 2회'를 고정 상한으로 삼아 필수 근거를 생략하지 않음.** 읽을 수 없는 자료는 접근 실패와 마지막 유효 확인 시점을 함께 명시.

### 예시
질문 `"지금 독립 리뷰가 안 된 이유?"`
- L0: `리뷰 미완료 / 운영 정책·위임 불일치(최신 증거 시점 명시) / 다음 행동=실제 Windows 사전검증`.
- L1: 자동 승인/이관 CURRENT 및 이 요청의 상태.
- L2: 승인된 POLICY REF와 protected delegation·원본 입력/READY/RESULT·처리 불확실 DB, 필요한 범위만.
- **하지 않음:** 모든 스킬 ZIP, L1 Knowledge 전체 설계, Job-list 소스 감사.

## 4. P1-B: 시간·근거 기반 상태 검증

### 질문에 보이는 판단 항목
최종 응답의 주요 사실마다 `주장 / 상태 / 시점(KST 또는 source timestamp) / 근거 경로+rev / 직접 확인 수준 / 미확인·충돌`을 유지. 이들은 **답변 생성 시 사용하는 논리 항목**일 뿐 새 JSON/Kernel 필드나 데이터베이스 요구가 아님.

### 충돌 해결 규칙
1. 먼저 **주장의 대상 범주**를 확인: Windows LIVE 운영, GitHub 게시, 독립 리뷰 실행, Linux 설치, L1 지식 게시 중 무엇인가?
2. 동일 주장에 대해 실제 도달 단계의 receipt/호스트 증거가 있으면 그 증거와 해당 시점의 원본을 우선. GitHub 원격 본문은 '게시 사실'을 확인할 뿐 로컬 호스트 실행을 입증하지 않음.
3. 더 최근인 '개발 계획'은 더 오래된 '실제 운영 관측'을 덮지 못함. 반대로 최신 호스트 실측이 있으면 오래된 CURRENT 헤더를 그대로 현행으로 인용하지 않음.
4. 날짜/commit/revision이 다른 기록은 시간을 보존해 분리. 동일 시점·동일 주장에 실제 충돌이 있으면 `CONFLICT_UNRESOLVED`, 판정 보류.
5. GitHub `READY`는 후보 접수 신호일 뿐 승인·정산 아님; `REVIEW_RESULT`와 `RECEIPT`는 고정 ID/revision/SHA/processing key 일치 확인 전 완료 판정 금지.
6. PUBLIC ZIP 존재와 설치본·실제 OpenCode/LLM 호출은 구분. Queue `DONE`/Receipt `SUCCESS`만으로 Code Facts/MSC 존재를 확정하지 않음.
7. **정보가 바뀌지 않았는데 경과 시간이 길다는 이유만으로 '장애/오래됨'으로 판단하지 않음.** 이벤트 발생 시각, 마지막 확인 시각, 마지막 변경 시각의 의미를 분리. 자동 게시 중단 의혹은 검증 기록과 비교.
8. 불확실·권한 실패·원격 조회 실패는 과거 상태를 '현행 VERIFIED'로 승격하지 않고 `LAST_VERIFIED_AT`과 `CURRENT_NOT_VERIFIED`로 표시.
9. PUBLIC 출력에는 기존 허용된 수준의 상태만. PRIVATE 진단 경로·Work ID·민감 이름·company source·로그 내용은 제거. 익명화도 반출 승인으로 간주하지 않음.

### 상태 문장 예시
- **허용:** `"PUBLIC ZIP은 GitHub main에서 확인. Linux 설치는 확인되지 않음."`
- **허용:** `"Watcher LIVE 버전은 11/19 Windows 보고 기준. 이 대화에서 실제 Windows 프로세스는 조회하지 못함."`
- **금지:** `"READY 있으니 Claude 리뷰가 실행 중"`, `"개발 ZIP vX이므로 L1Work 최신 배포"`, `"DONE/SUCCESS이므로 MSC 분석 완료"`.

## 5. P1-C: 한 화면 요약 UI (기존 B안 대시보드에 연결)

### 기본 정보 구조 (사용자 30초 파악 목표)
상단: `CoWork 전체: 부분 가동 / 마지막 실측 시점 / 신뢰도·미확인 수 / 다음 중요한 조치 1개`.
본문: 기존 공개 분류와 충돌하지 않도록 **표현상 4개 진입 카드**:
1. **협업 리뷰·운영**: LIVE/정책/REQUEST/REVIEW 단계 간 차이와 핵심 blocker.
2. **스킬·공개 배포**: 개발 후보/독립 리뷰/PUBLIC ZIP/호스트 설치를 구별.
3. **업무 실행**: 업무 GPT→Agent/MCP→LLM/Job→Run/Evidence 상태를 분리.
4. **L1 지식**: 개인 Work/Preview/승인/그룹 게시/readback·RAG 별도 검증.

카드 필드의 표현: `상태 1문장`, `1차 차단 원인(있을 때)`, `다음 한 동작`, `마지막 확인`, `근거 보기`. 확장/선택 시 해당 Work만 노출. 시각적 상태를 색에만 의존하지 않고 짧은 텍스트와 아이콘으로 병기. 모바일은 1열·본문 우선, 스크롤/긴 제목/접힘 상태를 확인.

### 기존 UI·보안 제한
- 사용자 선호 B안(보드/표/검색, 서브화면 구조)을 유지. 실제 구현 소유는 기존 `COWORK-GITHUB-DASHBOARD-20261111-001` Work.
- **PRIVATE 상세 보기**와 **PUBLIC 허용목록 요약**은 서로 다른 접근 권한. PUBLIC은 현재 승인된 exporter/status.json 필드만 사용. 기존 허용목록 5개 범주, 인계 최근 3건, 120초 폴링, 기존 Pages URL을 설계 변경만으로 바꾸지 않음.
- 미허용 새로운 Work명/요청 ID/원본 evidence를 공개하지 않음. 마스킹에 의존한 무허가 반출 금지.
- 인터랙션은 기존 카드 선택/근거 보기의 UI 방식 재사용. P1 설계 단계에서는 HTML/JS·PUBLIC·status schema 변경 **없음**.

## 6. 최소 구현/시험 로드맵 (이 설계 리뷰 후 별도 실행)

| 단계 | 작업 | 실제 PASS 증거 |
|---|---|---|
| A1 | 질문→기존 Work 매핑 표·기존 L0/L1/L2 응답 규칙 적용(프롬프트/조회 절차만) | 기존 문서 6종 대표 질문 수동 조회 로그, 누락/불필요 조회 기록 |
| A2 | 시간·증거 규칙을 응답 평가 체크리스트로 도입(읽기 전용) | LIVE/후보/REQUEST/호스트 충돌 반례의 정확 판정 |
| A3 | 기존 B안 UI 4카드 **격리 목업** (허용 데이터만) | PC 1440/1366·모바일 390/320 시각/키보드/overflow·상태 레이블 확인 |
| A4 | 30질문 기존 방식 vs P1 A/B 비교 | 아래 평가표 원본·시간·조회·오분류 수 |
| A5 | 성능/정확도 충분하면 기존 대시보드/문서에 최소 패치 | 기존 CI·공개 허용목록 검증, 필요 독립 리뷰, 원격 readback |
| A6 | 승인된 경우만 PUBLIC UI 업데이트 | 별도 PUBLIC 배포 게이트·HTTP/Pages/재방문 실제 시험 |

**A1~A4는 권한 없는 운영 변경·유료 자동 리뷰·새 watcher 설치 없이 진행.** A5~A6은 이번 P1 설계 요청의 승인 범위를 넘으므로 별도 실행 판정. `CONTEXT_BRIEF`와 카탈로그는 구조/역할이 바뀔 때만 갱신.

## 7. 객관적 평가 설계

**벤치마크**: 기존 시스템의 실제 비민감 질문 30개를 고정. 상태/버전 10, 다수 Work 관계/원인 8, 충돌·과거 자료 8, 미접근·불확실 4. 정답은 질문별 시점 고정 GitHub commit/host receipt 범위로 담당자가 수동 검증한 표. 업무 제한 데이터는 CoWork로 이전하지 않고 합성/비민감 결과만 사용.

| 지표 | 측정 방법 | P1 수용 목표(예측이 아닌 목표) |
|---|---|---|
| 현행 상태 정확도 | 30문항 정답과 일치 비율 | ≥95% (30문항 중 ≥29개) |
| 거짓 PASS/LIVE/INSTALL/REVIEW 완료 | 미검증을 완료로 오판한 수 | **0건** |
| 핵심 주장 근거 누락 | 답변에 근거/시점 없는 경우 | **0건** |
| 충돌·미확인 안전 판정 | 고정 반례의 fail-closed 여부 | **전부 PASS** |
| 사용자 이해 속도 | 5명 이상 30초 요약 후 핵심 상태/다음 동작을 설명하는 과제 | 첫 화면 30초 내 정확 파악 목표 |
| 조회 효율 | 동일 30문항의 읽은 문서수·토큰·지연 중앙값 | 입력/조회량 35% 이상 감소 목표; 정확도 희생 금지 |
| PUBLIC 정보 경계 | 기존 allowlist 밖 ID/내용·비민감 가정에 의한 원본 노출 검사 | 0건 |
| 구현 호환 | 기존 대시보드/브리프/Work ID/이력 무손실 | PASS |

비교는 동일한 고정 샘플, 동일 모델 설정, 동일 조회 권한으로 수행. 평가표에는 `expected / actual / source / time / evidence-level / failure`를 계산용으로만 활용하고 새 운영 원장을 신설하지 않음. 비측정 개선율·시간·시인성은 PASS로 보고하지 않음.

## 8. 연구 근거의 채택 범위와 라이선스 안전성

- **Lost in the Middle**: 긴 컨텍스트의 위치 의존 오류 → 전체 문서 일괄 투입을 피하는 동기. https://arxiv.org/abs/2307.03172
- **RAPTOR**: 추상화 층별 탐색에서 아이디어만 차용. https://arxiv.org/abs/2401.18059
- **Microsoft GraphRAG**: 관계 중심 질문 확장의 연구 참고, **라이브러리/코드·그래프 DB를 이번 P1에 포함하지 않음**. https://arxiv.org/abs/2404.16130
- **LongMemEval**: 시간 추론/업데이트·무지 상태 평가의 시험 방향만 참고. https://arxiv.org/abs/2410.10813
- **Anthropic Agent Skills progressive disclosure**: 상단 메타→필요 시 상세 읽기라는 설계 개념만 참고. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

**원문 논문 코드·학습 데이터·라이브러리를 복사하거나 패키지에 포함하지 않음**. 아이디어를 독립적으로 재설계하며 개별 라이선스 적용 여부는 향후 실제 코드 도입 시 재검토.

## 9. 미확인·위험 및 리뷰에서 판정할 사항

- Windows watcher LIVE의 실제 config·보호된 승인 자격, 외부 GPT의 호스트 접근 여부는 이 설계 문서만으로 확인 불가.
- 업무 GPT/LLM 설치본, Linux MCP Tool API, Knowledge writer 실제 호출은 접근 불가·별도 검증.
- PUBLIC 기존 `status.json`가 P1의 모든 구분을 표현할 수 있는지는 **기존 실제 allowlist 필드 대조 후 결정**. 스키마 확장을 확정하지 않음.
- 전체 카드 가독성/30초 실제 이해/토큰 절감/정답률은 미측정. 한글·모바일/스크린리더/키보드 시험을 개발 단계에서 수행.
- 비동기 상태 경쟁·LIVE stale·동일 날짜 여러 갱신·서명 불확실에 대한 책임/우선순위가 모호해질 수 있으므로 **증거 범주별** 판정 원칙을 리뷰 요청.

## 10. P1 단계의 완료 조건과 다음 한 행동

**이번 사용자 요청의 목표**는 설계 r0001 + 실제 승인된 보호 경로의 독립 리뷰 1회. 코드 수정, 새 스킬 ZIP, PUBLIC 배포, 업무 호스트 실행은 이번 범위에서 하지 않음.

정식 검토 실행은 LIVE 설치 정책 `review_request_gate.py select/check`가 승인된 단일 USD 3 정책을 실제 지원하고, 보호된 승인/서명 자격을 확인했을 때만 고정 ZIP + REQUEST/SOURCE_PIN/APPROVAL_SIG/READY 마지막 → 독립 Claude 결과/영수증 → GPT 판정으로 진행. 기존 USD3 수동 부트스트랩 예외는 **명시된 다른 1건 전용**이므로 이번 P1에 임의로 재사용하지 않음.

**NEXT_ONE_ACTION:** Windows Claude Code가 최신 LIVE 정책으로 P1 신규 독립 설계 리뷰를 사전검증하고, 실제 유효 권한 범위에서만 동일 입력의 정식 REQUEST/READY를 게시하여 1회 리뷰·영수증을 회수. 정책이 불일치하면 REVIEW=BLOCKED, 모델 호출 0으로 원인을 기록.
