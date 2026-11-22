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
