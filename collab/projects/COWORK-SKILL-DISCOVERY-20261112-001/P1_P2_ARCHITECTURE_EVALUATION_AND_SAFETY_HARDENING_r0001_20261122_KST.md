# P1/P2 전체 설계 평가·최소 안전 개선 r0001

- 작성: 2026-11-22 KST
- Work: `COWORK-SKILL-DISCOVERY-20261112-001` (신규 Work·별도 원장 없음)
- 정본: GitHub **PUBLIC** `wonhwipark/CoWork-Skill-Collab`, `main`. 비민감 코드/문서 범위에 한함
- 근거: 기존 P1/P2 운용 가이드, 2026-11-22 CURRENT 상단, R1 독립 리뷰의 `ACCEPT_WITH_CHANGE`, F1 부분 검색 보완 결과, 실제 `context_query.py`·`test_context_query.py` 소스
- 기존 R1 고정 입력·REQUEST/PIN/APPROVAL/READY/리뷰/영수증·소스 이력 불변. 신규 유료 호출 0

## 1. 종합 판정

**ARCHITECTURE=RETAIN_WITH_TARGETED_IMPROVEMENT.** 기존 CONTEXT_BRIEF → 관련 CURRENT → 필요한 근거/영수증의 3단계 조회, 독립 리뷰 운송과 근거 조회 분리, 로컬 read-only, 기존 Work 사용 원칙은 유지. 새 DB/RAG 엔진/자율 에이전트/인덱스/Watcher를 도입할 근거가 없음. 구현 성숙도와 새 창의 실사용 입증은 별개.

| 영역 | 판단 | 근거·영향 |
|---|---|---|
| 정본/Work 책임 | KEEP | 브리프는 라우팅 지도, CURRENT는 최신 상태, 세부 결과는 원문. 상태 이중 원장 최소화 |
| P1 정적 라우팅 | IMPROVE | `choose()`의 6개 정적 경로, 부분문자열, 미매칭 `skill` 폴백, 복수 주제 1개 Work 선택은 질문 의미 정답을 보장하지 않음 |
| P1 CURRENT 상단 | IMPROVE | 3,600자 상한과 첫 `##` 절만 읽는 방식은 Q4/Q5처럼 같은 Work 안에 흐름이 공존할 때 답변 불충분. 실측 A/B 필요 |
| P1 최신성/출처 | VERIFY | 조회기는 로컬 checkout을 읽음. 원격 main HEAD·호스트 실상태·자동 로딩 증명이 아니라는 표시 유지 |
| P2 REQUEST 관계 | KEEP+HARDEN | work_id 메타데이터 재확인, 200건/직접 링크 4개 예산, 부분 결과·개별 오류 격리는 긍정적 |
| P2 패키지 링크 | FIX | 임의 하위 경로의 마지막 ZIP basename으로 `collab/packages/<basename>`를 추정하던 혼동 제거 |
| P2 변경 비교 | VERIFY | 선택한 baseline과 CURRENT 상단 텍스트 diff일 뿐 상태 변경·실제 서명/실행 검증이 아님 |
| UI/Windows/효과 | NOT_RUN | 모바일/PC·Windows Claude 자동 로딩·A4 질문 정확도/토큰/속도 실측 없음 |

## 2. 이번 적용: 정책 보존형 최소 패치

**Source**: `collab/dashboard/context_query.py`

1. `route_diagnostics(question, topic)` 추가. `choose()` 자체와 6개 ROUTES/CLI 선택/반환 Work는 변경하지 않고, 결과에 `routing={state, selected_topic, candidate_topics, requires_review}` 추가:
   - `EXPLICIT_TOPIC`: 사용자 명시 `--topic` 우선.
   - `SINGLE_TOPIC_MATCH`: 하나의 분류에서 키워드 일치 (의미 정답 입증은 아님).
   - `FALLBACK_UNVERIFIED`: 아무 키워드 없음. 기존 `skill` 폴백은 유지하되 확정 경로로 취급하지 않음.
   - `MULTI_TOPIC_REVIEW`: 두 개 이상 주제에서 일치. 기존 우선순위 결과 외 후보와 경고 표시.
   - `SUBSTRING_MATCH_REVIEW`: 검증된 `그룹웨어` 류의 `그룹` 부분 일치 위험 경고.
2. `summary_truncated` 및 경고 추가. CURRENT 상단 3,600자 절단을 감추지 않음. 기존 `summary` 내용·길이 상한은 유지.
3. package_path를 정확히 `/SKILL-COLLAB/packages/<flat-filename>.zip` 형식으로 검증한 뒤 로컬 패키지 경로와 연결. `nested/candidate.zip`를 `candidate.zip`로 잘못 매칭하지 않음. 이는 파일 존재 여부 점검이며 실제 ZIP 해시 검증은 아님.
4. 기존 P2 200 REQUEST 예산·부분 결과·오류 격리/안전 경로, baseline 텍스트 diff, 호스트 실행 미검증 분리 불변.

**새 소스 식별자 (원격 main readback):**

| 파일 | UTF-8 bytes | SHA-256 | Git blob |
|---|---:|---|---|
| `collab/dashboard/context_query.py` | 15135 | `6f9f94e98a53133b1466ffc6bcc2dcad28bd84d460ea306b0e7d6a5def2caaab` | `8e9351b96c9af491e344d890d4b63d35372de1e3` |
| `collab/dashboard/tests/test_context_query.py` | 21231 | `ad8f3aae4a12ff68b47182f7fff6d24486306f827d68f5503b1d9d9553c1c7be` | `5e3fdcff55d3f95063ec2a136abaf2c4765db1f9` |

- SOURCE_COMMIT: `5c73e0179a313695ed4b1281f5653e7d2853db9c`
- TEST_COMMIT: `f45ec56b42e778704dcdfe4aa32758eee9d2376e`
- 두 파일 원격 전체 UTF-8 콘텐츠 일치 확인. SHA-256은 표준 UTF-8 byte 처리로 계산한 해시 (SHA-256 알고리즘은 공개 `abc` known-answer와 대조).

## 3. 시험·미검증 구분

| 시험 | 상태 | 근거/한계 |
|---|---|---|
| 변경 전 Linux Python 회귀 28건 | PASS(이전 소스에 한정) | 2026-11-22 기존 F1 보완 결과 |
| 이번 변경 축소 독립 로직 재현 | PASS 10/10 | 새 라우터 진단/패키지 형식 로직을 별도 격리 Python fixture로 재현, 실제 전체 모듈 실행 아님 |
| 새 회귀시험 소스 7개 | POSTED_NOT_RUN | 기존 test_context_query.py에 추가, 예상 전체 35개 |
| 최신 모듈 `py_compile`·전체 35 unittest | NOT_RUN | 이 GPT 세션에서 GitHub connector의 파일을 로컬 Python 실행환경에 동일 bytes로 마운트하지 못함 |
| Windows Python·Claude 자동 로딩·Q1~Q5 | NOT_RUN | 호스트가 별도이고 이 코드 게시로 자동 실행되지 않음 |
| A4 30문항 정답/근거/조회 시간·토큰 A/B | NOT_RUN | 기존 30문항 출력 기록은 정답률 실측이 아님 |
| 추가 독립 리뷰 | NOT_RUN | 기존 R1은 수정 전 입력의 정적 리뷰로 종결, 자동 재실행하지 않음 |

소스 게시/로컬 축소 시험을 새로운 전체 회귀 PASS 또는 실사용 성공으로 바꾸지 않는다. 이 단계에는 신규 모델 호출·자동 승인·READY·Windows LIVE·Actions 실행·L1Work UI 게시 없음.

- 30개 기존 라우터 예문에 대한 **축소 독립 Python 로직 재현**: 24개 기존 선택 결과 24/24 동일, 새 진단의 `SINGLE_TOPIC_MATCH` 23건 / `MULTI_TOPIC_REVIEW` 3건 / `FALLBACK_UNVERIFIED` 3건 / `SUBSTRING_MATCH_REVIEW` 1건. 7건은 확인 필요로 표시. 이는 실제 저장소 모듈 실행, 사용자 골든 정답률, A4 자연어 답변 A/B가 아니다.

## 4. 후속 설계: 우선순위 및 완료 기준

**P0 — 새 소스 회귀·정적 안전성 확인(최우선)**
- 실제 Python 환경에서 `python -m unittest discover -s collab/dashboard/tests -p test_context_query.py -v` (기존 28 + 신규 7)와 `python -m py_compile collab/dashboard/context_query.py collab/dashboard/tests/test_context_query.py` 실행.
- FAIL이면 같은 Work에서 최소 수정 후 회귀. 이전 성공 결과로 PASS 대체 금지.

**P1 — A4 30문항 골든셋과 질문별 근거 확장**
- 사용자 의도 라벨(정답 Work 또는 복수 Work/unknown)과 답변에 필요한 증거 경로·시점·상태를 질문별로 별도 확정. 기존 단순 30문항 `choose()` 출력은 골든셋이 아님.
- 기존 경로/하드코딩 선택의 top-1 및 후보 포함률, unknown 회피, 질문별 관련 최신 하위 근거 찾기, 과거 상태 오판, 잘림/불완전 경고 적합성 확인.
- 조회 파일 수·시간·입력 token 수는 실제 동일 환경 A/B에서 측정. 모형 토큰 절감율·정확도를 추정치로 PASS 선언하지 않음.
- 가장 비용 대비 효과가 높은 후속 구현 후보: CURRENT의 질문 관련 최신 하위 heading/직접 연결 결과를 **제한된 evidence candidate**로 제시하고, 실제 주장에는 원문 근거와 별도 실행증거를 요구. 오래된 heading은 정답으로 자동 승격하지 않음.
- `choose()`의 strict fallback 차단, 다중 Work 선택, 정적 ROUTES를 브리프의 역할 맵과 연결하는 변경은 A4에서 오분류 개선·호환성이 입증된 경우에만 최소 반영.

**P2 — Windows 새 세션 실제 재개**
- 기존 `WINDOWS_P1_P2_READONLY_E2E_EXECUTION_REQUEST_r0002_20261121_KST.md` 재사용. 원격 HEAD/로컬 SHA와 Python 시험을 먼저 검증한 뒤 Claude Code 세션 로딩 및 Q1~Q5 답변/증거를 분리 검증.
- 읽기 전용 실행 이외의 유료 모델 호출·운영 provider/Watcher/DB/키/서명/READY·L1Work 공개 상태 변경은 해당 승인 없이 하지 않음.
- GitHub 문서·Python 코드 게시를 자동 로딩 또는 실제 Windows 호스트 검증으로 보고하지 않음.

## 5. 최종 판단

현재 P1/P2는 **정본 재사용과 fail-closed에 강점**, 의미 분류 정확도·하위 근거 탐색·호스트 최신성에는 아직 실사용 증거가 부족하다. 새로운 RAG/DB나 자동 agent보다 **추가 진단 → 회귀 → A4 골든셋 → 근거 선택 개선 → Windows 실제 E2E** 순서가 최소 위험·최대 실용성의 개선 방향이다.

**NEXT_ONE_ACTION:** 최신 두 Python 파일을 동등 바이트로 확보한 검증 환경에서 35건 회귀+`py_compile`부터 실행해 판정한다. 그 뒤 같은 Work에서 A4를 진행하며 기존 Windows r0002 인계는 중복 생성하지 않는다.
