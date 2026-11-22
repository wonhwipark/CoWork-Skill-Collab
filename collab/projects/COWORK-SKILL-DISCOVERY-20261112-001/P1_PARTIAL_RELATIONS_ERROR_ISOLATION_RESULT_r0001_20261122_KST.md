# P1/P2 F1 부분 결과 유지·개별 오류 격리 적용 결과 r0001

- 작성 기준: 2026-11-22 KST
- 정본: GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 기존 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- 사용자 지시: “마지막 제안 방향으로 진행해서 적용해줘. 작업 전에 최신 상황 확인 후 진행해줘.”
- 시작 기준 main: `29c4e5e6ae2dc9a76e2873e23459b66ed6242937`. 공통 브리프 r0017, 해당 CURRENT·열린 결과·TRACKER·루트 AGENTS·시작/재사용·통합 계약을 조회했다. 기존 코드·시험·가이드 blob은 이전 검토본과 동일했다.
- 적용 범위: 선택적 읽기 전용 `context_query.py`의 F1 보완·관련 회귀·운용 안내·동일 Work 상태. F2와 F3 정책 유지. Windows 설치·Watcher 운영 변경은 포함하지 않는다.

## 1. 재사용·변경 판단

| 구분 | 판단과 근거 |
|---|---|
| REUSE | 기존 CURRENT·REQUEST frontmatter·관계 행·CLI·F2 경로 검사·기존 200건 예산·기존 시험을 재사용 |
| CONNECT | CURRENT와 같은 Work의 연결 결과에서 기존 REQUEST ID를 탐색 힌트로 사용. 신규 DB·중앙 인덱스·스키마·Agent·Watcher 없음 |
| 최소 EXTEND | 상한 도달 시 유효 관계 폐기 및 관련 없는 UTF-8 오류의 전체 전파를 직접 재현했으므로, 부분 결과·로컬 탐색 완료 여부·개별 오류 진단을 추가 |
| DEFER | A3 UI·A4 자연어 A/B, 실제 Windows 경로·Claude 자동 로딩·추가 독립 리뷰는 별도 범위 |
| 병렬 변경 | 시작 tree에서 이 Work의 다른 integration stream 등록은 없었다. 동일 ZIP의 다중 stream 통합 작업이 아닌 단일 Python 소스 보완이다. 별도 릴리스 ZIP·호스트 배포 완료를 주장하지 않는다 |

## 2. 실제 동작 변경

1. CURRENT의 REQUEST ID를 우선 수집하고, 같은 Work의 직접 연결 Markdown은 최대 4개만 읽는다. 같은 ID는 중복 검사하지 않는다. Work 일치는 항상 REQUEST 메타데이터로 다시 확인한다.
2. 우선 검사와 후속 디렉터리 검사는 고유 REQUEST 최대 200건 예산을 공유한다. 디렉터리 후보 이름 수집은 최대 201개다. 상한 초과 시 이미 확인한 관계를 유지한다.
3. `relations_state=RELATIONS_SCAN_LIMIT_EXCEEDED`는 유지하면서 `relations_scan.complete=false`·검사 수·상한·우선 검사 수·개별 오류를 반환한다. 상한 외 읽기·메타데이터 오류는 `RELATIONS_SCAN_INCOMPLETE`로 표시한다.
4. REQUEST 읽기/UTF-8/권한 오류를 개별 격리한다. 증거 파일 접근 오류는 `NOT_VERIFIED_LOCAL`로 남기고 해당 REQUEST 행을 유지한다. CURRENT 자체가 읽히지 않으면 `CURRENT_NOT_VERIFIED`를 반환한다.
5. 빈 관계 목록과 탐색 완료를 구별한다. 읽지 못한 범위가 있으면 ‘관련 요청 없음’·실행 완료·승인 유효를 추정하지 않는다.
6. `related()`의 목록 전용 호출은 불완전한 탐색을 성공 목록으로 숨기지 않는 엄격 API다. 기존 상한 예외는 보존하고, 그 외 불완전 탐색에는 `RequestScanIncomplete(ValueError)`를 반환한다.
7. `safe_file()`와 `choose()`는 AST 비교로 변경 없음이 확인됐다. 새 문서 힌트는 같은 Work 상대경로만 허용하며, Windows 경로·UNC·상위 경로·외부 URL·symlink를 따라가지 않는다.

`complete=true`는 로컬 요청 탐색의 완료만 뜻한다. 관계 행은 파일 존재/메타데이터 대조이며 서명·ZIP SHA·실행·호스트 LIVE의 검증이 아니다. 제한된 디렉터리 prefix는 전체 요청을 정렬한 페이지가 아니며, 재호출 시 다음 페이지로 이동하는 cursor도 이번 범위에 추가하지 않았다.

## 3. GPT 직접 시험

| 항목 | 결과와 범위 |
|---|---|
| 회귀시험 | Linux Python 3.12.14 `python -m unittest discover -s collab/dashboard/tests -p test_context_query.py -v`: **28 PASS / 0 FAIL / 0 ERROR / 0 SKIP**. 기존 13개 유지·의미 보완 + 추가 15개 |
| 상한 초과 | 읽은 유효 관계 유지, 200건 경계, 201건 초과 미완료, 검사 예산 200건 이하 확인 |
| 우선 탐색 | CURRENT 링크·연결 결과의 REQUEST가 다른 Work 201개보다 먼저 검사됨. ID 중복 제거·다른 Work 혼입 방지 확인 |
| 개별 오류 | 잘못된 UTF-8·PermissionError·잘못된 frontmatter·누락 REQUEST·디렉터리 오류·증거 파일 오류에서 유효 행/요약 유지 |
| 안전 경계 | 문서 힌트의 드라이브/UNC/경로 이탈/symlink 차단, 직접 문서 최대 4개, 재귀 없음 |
| 합성 CLI | 연결된 유효 REQUEST 1건 + 다른 Work 201건 + 잘못된 UTF-8 1건: exit 0, 유효 행 1개 유지, limit exceeded·complete=false, UnicodeDecodeError 개별 기록, host 미검증·NO_BASELINE 유지 |
| F2/F3 불변 | 변경 전후 `safe_file()`·`choose()` AST 동일. 기존 Windows 경로의 파일 상태 접근 0 모의시험 PASS |
| 구문·차이 | `py_compile` 및 `git diff --check` PASS |
| 독립 리뷰 | 수정 후 추가 리뷰 **NOT_RUN**. 기존 R1은 수정 전 고정 ZIP 대상의 정적 리뷰이며 종결·재실행 금지 |
| 실호스트/효과 | 실제 Windows 회귀·Claude 세션 로딩·A3 UI·A4 자연어/속도/토큰 A/B **NOT_RUN** |

합성 CLI 시험에서 fixture 경로 목록은 실행 전후 동일했다. 이 확인은 임의 운영 디스크·모든 시스템 호출·호스트 설치 상태에 대한 감사가 아니다. 모델 없는 로컬 시험 결과를 자연어 정확도나 운영 E2E PASS로 확대하지 않는다.

## 4. 소스 고정 식별자

| 파일 | bytes | SHA-256 | Git blob |
|---|---:|---|---|
| `collab/dashboard/context_query.py` | 13471 | `9ccba5b635220b152ebbe84d2600a8b27abde9cd38e98f5d8f2b4d54433eb9b1` | `29062b29392a792b0ae206c38e813d2e0d5092ef` |
| `collab/dashboard/tests/test_context_query.py` | 17981 | `06f828d245fa27adde6eebc12ea51dafd0037fb491496fe85dbe4143aa903f77` | `36262dbbac4252d936f78ef2c73078a197a29581` |

함께 갱신한 파일: 기존 적용 가이드 §7, CURRENT의 짧은 최신 요약, 기존 TRACKER의 현행 파생 필드, 이 결과 문서. 과거 결과·R1 REQUEST/입력 ZIP/PIN/승인·READY·리뷰·영수증은 보존한다.

## 5. 적용 및 후속 경계

- 이번 코드 보완은 GitHub main의 선택적 로컬 조회기에 적용한다. PR 없이 기존 게시 경로와 예상 HEAD 검사를 이용하고, 게시 후 원격 본문·실제 UTF-8 bytes/크기·SHA-256·Git blob을 대조한다. 게시 확인은 아래 기록에 추가한다.
- F2는 유지하며, 실제 Windows에서 이 조회기를 사용할 때 해당 경로 호환을 확인한다. Claude 문서 로딩은 별도 클라이언트 활용 검증이다. Watcher 전체 운영 E2E는 이 F1 코드 적용의 필수조건이 아니다.
- 다음 별도 검증은 기존 A4 골든셋에서 질문별 하위 근거 확장·최신 변경·미확인 처리·정확도/조회량을 평가하는 작업이다. 이 변경으로 F3 정확도·자동 로딩·UI·장기 운영을 PASS로 승격하지 않는다.
- 새 REQUEST/READY·추가 독립 리뷰·운영 signer/위임/DB/예약·Watcher/LIVE·L1Work UI·Actions 설정 변경 없음.

## 6. 게시 확인

- **SOURCE_CONTENT_COMMIT:** [`7ead07ce3724d1c593aa75b68024d6a65368016a`](https://github.com/wonhwipark/CoWork-Skill-Collab/commit/7ead07ce3724d1c593aa75b68024d6a65368016a).
- **게시:** 시작 main `29c4e5e6ae2dc9a76e2873e23459b66ed6242937`의 tree 위에 변경 6개 파일을 한 커밋으로 반영하고 예상 HEAD를 검사하는 fast-forward로 main 갱신. commit 메시지에 `[skip ci]`를 사용했다. PR·새 리뷰 REQUEST·READY·Actions 재활성화 없음.
- **REMOTE_READBACK=PASS_6_OF_6:** 위 고정 commit에서 6개 파일을 base64 원문으로 재조회·디코딩하고, 실제 bytes 전체·크기·SHA-256·Git blob을 로컬 게시본과 대조해 모두 일치했다. GitHub main도 위 commit을 가리키는 것을 확인했다.
- 아래 값은 **위 소스 적용 commit의 파일**에 대한 검증이다. 이 게시 확인 절과 CURRENT의 검증 요약은 후속 메타데이터 커밋으로 기록하므로 두 문서의 최신 SHA는 아래 고정 시점 값과 달라질 수 있다. 소스·시험·가이드·TRACKER는 그대로 유지한다.

| 고정 commit 파일 | bytes | SHA-256 | 원격 대조 |
|---|---:|---|---|
| `collab/dashboard/context_query.py` | 13471 | `9ccba5b635220b152ebbe84d2600a8b27abde9cd38e98f5d8f2b4d54433eb9b1` | PASS |
| `collab/dashboard/tests/test_context_query.py` | 17981 | `06f828d245fa27adde6eebc12ea51dafd0037fb491496fe85dbe4143aa903f77` | PASS |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md` | 114898 | `5fec691a49d93d51f5933f70e4ac973899eca299ebee2cfcba70108931339283` | PASS |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_CONTEXT_APPLICATION_GUIDE_r0001_20261120_KST.md` | 11074 | `511b8d4130de1e8f1bb85d493f37ae576e38fcf0ee99940dd239a8bdff471498` | PASS |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/TRACKER.json` | 917 | `77704f4a847cc9a2558a2e3ae05dee828e6c27df912e9407564870f707da94a7` | PASS |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_PARTIAL_RELATIONS_ERROR_ISOLATION_RESULT_r0001_20261122_KST.md` | 7484 | `87aae1e774d3296edeb5c66612896ab39a8b2fc00a808f7978286430e94b8da4` | PASS |

- **적용 판정:** `F1_PARTIAL_RELATIONS=APPLIED_MAIN`, `F2=UNCHANGED`, `LOCAL_REGRESSION=PASS_28_OF_28`, `CLI=PASS`. 이 판정은 실제 Windows·독립 리뷰·A3/A4·Watcher 운영 E2E 완료가 아니다.
