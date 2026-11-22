# CoWork P1·P2 빠른 상황 파악 — 적용·운용 안내 r0001

- 2026-11-20 KST / 기존 Work `COWORK-SKILL-DISCOVERY-20261112-001`
- 사용자 최신 지시: **P1·P2 독립 리뷰 생략 후 적용**. 해당 두 범위에 한정 `INDEPENDENT_REVIEW=SKIP_BY_EXPLICIT_USER_REQUEST`; 기존 완료 리뷰·불확실 요청 및 독립 리뷰 의무가 있는 다른 변경에는 적용하지 않음.
- 담당: P1/P2 맥락 절차·PRIVATE 조회 기능은 맥락 Work, B안 UI는 기존 `COWORK-GITHUB-DASHBOARD-20261111-001`.
- 설치/호출: 모델·Windows watcher/LIVE·서명/READY/DB·업무 Linux/Knowledge 변경 **없음**.

## 1. 현재 적용된 기능과 사용법

### P1: 주제 선택·3단계 조회 + PUBLIC 4카드
- 질문에서 주제만 분류 → `collab/CONTEXT_BRIEF.md` 목적별 진입 Work 선택 → **CURRENT 최상단** → 그 주장에 필요한 결과/리뷰/영수증만 추가 조회. 기존 브리프와 각 CURRENT가 유일한 구조/상태 정본. 전체 스킬을 매번 감사하지 않음.
- PRIVATE 로컬 조회기 `collab/dashboard/context_query.py`를 기존 PRIVATE checkout에서 **읽기 전용**으로 호출할 수 있음.
- PUBLIC `https://wonhwipark.github.io/L1Work/cowork-dashboard/`: 기존 B안 상단에 **협업·리뷰 / 스킬·배포 / 업무 실행 / L1 지식** 4카드. 데이터는 기존 PUBLIC `status.json`의 승인된 5개 범주에서만. `LIVE/리뷰/호스트` 근거를 독립 검증하지 않으므로 상태는 **'신고/별도 확인'**으로 표시.

### P2: PRIVATE 리뷰 관계/텍스트 변경 비교 + PUBLIC 제한된 관계 보기
- PRIVATE 조회기는 지정 Work와 같은 `work_id`가 있는 `REQUEST.md`만 찾고, `SOURCE_PIN/APPROVAL_SIG/READY/REVIEW_RESULT/RECEIPT/패키지` 경로의 **로컬 파일 존재 여부**만 연결. **존재=실행/PASS가 아님**. 후보 패키지 바이트·SHA에 대한 실검증도 별도.
- `--baseline-commit <40-hex>`를 전달한 경우에만 **이전 Git commit의 같은 CURRENT 최상단**과 현재 로컬 최신 요약을 텍스트 diff로 비교. `git show` 읽기 전용, shell/네트워크·상태 저장 없음. baseline 없거나 없어진 파일이면 `NO_BASELINE/BASELINE_NOT_VERIFIED`, 과거 변경을 만들어내지 않음.
- PUBLIC은 승인된 업무 범주에 한한 **개념적 책임 흐름**만 보여주며, 이전 120초 polling 상태와 비교하는 변경분은 **현재 화면이 열린 동안만** 표시. 새로 접속하면 '이전 스냅샷 없음'. PRIVATE Work/REQUEST ID, 패키지 SHA/경로, 비용/영수증 원문은 PUBLIC로 보내지 않음.

## 2. PRIVATE 조회 명령 (추가 서비스·설치 불필요)

CoWork PRIVATE `main` 로컬 체크아웃 최상위에서:

```bash
python collab/dashboard/context_query.py --root . --question "Claude 리뷰가 왜 중단됐어?"
python collab/dashboard/context_query.py --root . --question "스킬 ZIP 배포 여부" --topic skill
python collab/dashboard/context_query.py --root . --question "현재 스킬 변경점" --topic skill --baseline-commit <검증된-40자리-Git-commit>
```

출력은 JSON이며 `LOCAL_CURRENT_READ_ONLY / CURRENT_NOT_VERIFIED`, 관련 REQUEST의 **로컬 파일 존재**와 `LOCAL_TEXT_DIFF_ONLY`만 표시. **실제 LIVE Windows·GitHub 원격 HEAD·Linux 설치·LLM 호출·Knowledge 게시 확인은 별도 운영 근거**가 필요함. 이 출력은 PRIVATE이며 업무 원본에 대한 외부 전송/반출 허가가 아님.

## 3. 기존 시스템 호환·보안

| 구성 | 변경 |
|---|---|
| PRIVATE | `collab/dashboard/context_query.py` + `collab/dashboard/tests/test_context_query.py`; 새 Work/DB/원장/워처/액션 생성 없음 |
| PRIVATE 기존 자동화 | `cowork-dashboard.yml`의 기존 `unittest discover`가 새 격리 테스트를 함께 실행. 실행/결과 경로 변경 없음 |
| PUBLIC | 기존 `L1Work/main/docs/cowork-dashboard/index.html`에 한 화면 섹션과 CSS, `context-view.js` 정적 소스 추가. 기존 `board.js`, `status.js`, `status.json` 스키마/허용목록·기존 3개 서브화면 불변 |
| PUBLIC 조회 | same-origin `status.json`만 GET. DOM 출력 `textContent`; 외부 fetch, iframe, 사용자 입력 전송, localStorage, 외부 JS/CDN, PUBLIC 비승인 링크 없음 |
| 기존 리뷰 | 신규 P1 후보 `REQ-COWORK-P1-CONTEXT-RETRIEVAL-DESIGN-R1-20261120`의 정식 REQUEST/READY 부재 및 Windows `POLICY_COST_MISMATCH` 이력 보존. 이번 사용자 **리뷰 생략**으로 신규 유료 요청·서명을 다시 만들지 않음 |
| 호스트 | 업무 GPT·Linux MCP/LLM/Knowledge writer 동작 변경·결과 미관측 |

## 4. 시험·계속 검증할 항목

- **코드**: Python topic 라우팅/최상단 요약/파일 경로 이탈·symlink 차단/요청-리뷰 연계/영수증 미추정/경계 및 baseline 비교 합성 단위시험.
- **PUBLIC**: 기존 B안 주요 메뉴·board.js 유지, 외부 script 차단 CSP 유지, 새 스크립트 문법/승인 JSON 처리/4카드·관계·baseline 없음 렌더, GitHub Pages 배포 Action 확인.
- **미검증**: 실제 Android/PC 브라우저 화면 pixel·키보드/스크린리더, 사용자의 30초 파악 시험, 골든셋 30개 A/B 정확도/토큰 절감 실측, 실제 Windows/GitHub LIVE·Linux 호스트까지의 E2E. 실측 수치 예측 또는 완료 판정 금지.
- 기능 확장은 없고, 기존 테스트와 직접 브라우저 확인에서 오류가 나오면 해당 소유 Work에서 최소 수정.

## 5. 기대 활용

새 창에서 "전체 상황"을 물으면 첫 문장은 **현재 상태·차단·다음 동작**으로, 필요할 때만 근거 파일로 내려가도록 운용. 기존 문서에 기록된 현재 상태가 바뀌면 GitHub 최신 HEAD·해당 Work의 CURRENT를 재조회하고, PRIVATE 조회기 결과만으로 실호스트가 최신이라고 주장하지 않음.

다른 영역 데이터·레코드 스키마/자동 승인/WINDOWS 리뷰 transport/업무 GPT 스킬 변경은 이번 P1/P2 범위 밖.


## 6. 2026-11-22 R1 F1~F3 후속 보완 — E2E 이전 운용 주의

- 이 절은 2026-11-20 원문 이력을 보존한 후속 보완이다. 자세한 수정·시험·30질문 출력: [F1~F3 보완 결과](P1_P2_R1_F1_F3_PRE_E2E_REMEDIATION_RESULT_r0001_20261122_KST.md).
- **F1 (조회 상한)**: 요청 폴더가 200개를 넘으면 `snapshot()`은 CURRENT 요약을 계속 반환하되, `relations=[]`와 `relations_state=RELATIONS_SCAN_LIMIT_EXCEEDED`를 함께 반환한다. 이는 '관계 없음'이 아니라 **관계 조회 미완료/NOT_VERIFIED**다. `related()` 직접 호출은 `RequestScanLimitExceeded(ValueError)`를 발생시키는 기존 상한 의미 유지. 요청 상한을 풀거나 조회를 무제한 확대하지 않는다.
- **F2 (경로 안전)**: `safe_file()`은 Windows 드라이브 경로(`C:/...`, `C:foo`)와 UNC·POSIX 절대경로를 파일 접근 **전에** 거부하도록 보완. Windows 자체 시험은 별도.
- **F3 (질문 분류)**: `choose()`는 문자 부분 일치로 점수를 매긴다. **키워드 미매칭은 무조건 `skill`**로 라우팅하며 '분류 불가'를 의미하지 않는다. `그룹웨어`는 `그룹` 부분문자열 때문에 `knowledge`로 오분류될 수 있고, 복수 주제는 점수·우선순위로 한 Work만 선택한다. 이 결과를 의미 정답이나 최신 실행 상태로 승격하지 않는다. 담당자가 명확한 질문에는 `--topic` 명시를 우선하며, 정보가 불충분하면 관련 Work의 최신 하위 증거를 추가 조회한다.
- **시험 구분**: 격리 Linux/Python 단위 13/13 PASS 및 모델 없는 30질문 분류 출력 기록. 이는 실제 Windows·모바일·PC 및 A4 정량 정확도/토큰/E2E 검증을 대체하지 않는다. 추가 유료 독립 리뷰·운영 LIVE 변경·L1Work 공개 UI 변경 없음.


## 7. 2026-11-22 후속 적용 — F1 부분 결과 유지·오류 격리 / F2 유지

이 절은 §6의 F1 상한 초과 처리와 Windows 전체 E2E 우선 계획을 보완하는 현행 기준이다. §6과 이전 시험·리뷰 기록은 당시 이력으로 보존한다.

- **조회 순서:** 선택 Work의 CURRENT에 나타난 REQUEST ID와 같은 Work 안의 직접 연결된 Markdown 최대 4개에서 발견한 ID를 우선 검사한다. 링크는 탐색 힌트이며, 실제 REQUEST의 `work_id`가 일치해야 관계로 포함한다. 중복 ID는 한 번만 검사한다. 재귀 탐색·네트워크 조회·새 인덱스는 없다.
- **상한과 부분 결과:** 우선 조회와 디렉터리 후속 조회는 REQUEST 검사 예산 200건을 공유한다. 디렉터리 이름 후보는 최대 201개만 수집한다. 상한을 넘겨도 이미 확인한 관계를 유지하며 `relations_state=RELATIONS_SCAN_LIMIT_EXCEEDED`, `relations_scan.complete=false`를 반환한다. 전체 디렉터리를 정렬하거나 전수 조회한 결과가 아니며, 읽지 못한 나머지 관계의 부재를 증명하지 않는다.
- **개별 오류 격리:** REQUEST의 UTF-8 오류·읽기 권한·읽기 중 파일 소실·메타데이터 미확인은 해당 ID의 `relations_scan.issues`에 기록하고 다음 항목을 계속 확인한다. 상한이 아닌 오류는 `RELATIONS_SCAN_INCOMPLETE`다. 이미 읽은 REQUEST의 증거 파일 접근 오류는 해당 필드를 `NOT_VERIFIED_LOCAL`로 남기고 관계 행을 유지한다.
- **빈 결과 해석:** `complete=false`일 때 빈 `relations`는 ‘관련 요청 없음’이 아니다. REQUEST 디렉터리가 없거나 접근이 불가능한 경우도 미완료다. `complete=true`는 로컬 탐색 범위의 완료일 뿐, 승인·서명·SHA·독립 리뷰·운영 실행을 검증한 결과가 아니다.
- **호환:** 기존 CLI 옵션·관계 행·`execution_verdict=NOT_INFERRED_FROM_FILES`·호스트 미검증 표시는 유지한다. 진단용 `relations_scan`만 추가한다. 목록만 반환하는 `related()`는 상한 초과 시 기존 `RequestScanLimitExceeded(ValueError)`, 그 외 미완료 시 `RequestScanIncomplete(ValueError)`를 발생시키며 불완전 목록을 정상 목록으로 숨기지 않는다. 부분 결과는 `snapshot()`/CLI에서 확인한다.
- **F2/F3:** `safe_file()`의 Windows 드라이브·UNC·절대경로·경로 이탈·symlink 보호와 `choose()` 분류 정책은 변경하지 않는다. 새 문서 힌트도 F2 가드를 통과한 같은 Work 상대경로만 읽는다.
- **검증 경계:** Linux Python 3.12.14 회귀시험 28/28 PASS, 합성 CLI PASS, F2/F3 함수 AST 불변 확인. 수정 후 독립 리뷰·실제 Windows·Claude 세션 로딩·A3 UI·A4 30문항 A/B는 NOT_RUN. Windows 조회기 사용 시 경로 호환·세션 활용은 각각 별도 검증하며 Watcher 전체 E2E를 이번 코드 적용의 필수조건으로 묶지 않는다.
- **상세 근거:** [F1 부분 조회·오류 격리 적용 결과](P1_PARTIAL_RELATIONS_ERROR_ISOLATION_RESULT_r0001_20261122_KST.md). 기존 R1 재실행·새 REQUEST/READY·Watcher/LIVE·서명·DB·L1Work UI 변경은 없다.


## 8. 2026-11-22 전체 설계 평가·F3 진단/P2 패키지 관계 안전 개선

- 최신 종합 판정 및 고정 소스: [P1/P2 전체 설계 평가·최소 개선 결과](P1_P2_ARCHITECTURE_EVALUATION_AND_SAFETY_HARDENING_r0001_20261122_KST.md).
- 기존 `choose()` 6개 ROUTES·미매칭 `skill` 폴백·복수 질문 우선순위는 **변경하지 않았다**. 대신 선택 근거를 `routing.state / selected_topic / candidate_topics / requires_review`로 표시. `FALLBACK_UNVERIFIED`, `MULTI_TOPIC_REVIEW`, `SUBSTRING_MATCH_REVIEW`에서는 선택 Work를 의미 정답으로 확정하지 말고 사용자 의도/관련 CURRENT를 추가 확인한다. `SINGLE_TOPIC_MATCH` 역시 정답 검증이 아니다.
- 기존 `summary`는 3,600자 상한을 유지하되 `summary_truncated=true`면 상단 절을 전부 읽지 않은 것임을 표시한다. Q4/Q5처럼 같은 Work의 여러 흐름은 필요한 최신 결과를 별도 증거로 좁혀 읽는다.
- P2 `package_path`는 정확한 평면 ZIP 경로만 로컬 파일 존재 연결. 비표준 하위 경로의 basename을 같은 파일명으로 추정하지 않는다. `PRESENT_LOCAL_UNVALIDATED`는 기존처럼 해시/승인/실행 근거가 아니다.
- 추가 회귀시험 7개는 원격 게시됐으나 이 세션에서 전체 실제 Python 시험·Windows Claude E2E·A4 30문항 A/B는 **NOT_RUN**. 축소 로직 재현 10/10 PASS를 전체 회귀 PASS로 승격하지 않는다.
- 운영 WATCHER/LIVE·DB/서명/READY·GitHub Actions·L1Work UI는 변경하지 않았다. 새 창 자동 로딩도 이 코드 게시만으로 실현되지 않는다.
