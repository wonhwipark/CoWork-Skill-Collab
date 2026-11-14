# CL/PR 이슈 분석 → Workspace 축적: 독립 설계 리뷰 결과 (GPT용)

```text
REVIEW_STATUS: COMPLETED
REVIEW_KIND: INDEPENDENT_DESIGN
INPUT_REPO / INPUT_BRANCH: wonhwipark/CoWork-Skill-Collab (PRIVATE) / main
PINNED_INPUT_COMMIT: 74cf1417ad41b2c3bbe6519c3cb87424d21e1a51 (읽은 시점의 main 최신)
INPUT_BLOB_SHA: 요청서 da8ea1bbea59f2a81c8ce7d8df0fabe1d0817183 / 기준안 b7838b5e86e3c88d322c5111ffccee0a4e835456
                계약 감사 203e09ae1ab7dba1377689fe9470d1c3440b6dd5 / G0 부분 감사 c6bba605782f8478a6bf8944b40024988b7a9385
                피드백 판정 16b522a61be3c8c4257d42491ad0f22679de053b
EVIDENCE_LEVEL: E2 (게시된 스킬 6종의 실제 코드를 읽고 합성 입력으로 일부 실행) / E3 NOT_VERIFIED
DESIGN_DISPOSITION: ACCEPT_WITH_CHANGE
CODE_PATCH / HOST_EXECUTION / GROUP_WRITE / PUBLIC_RELEASE: NOT_RUN
```

## 0. 한 줄 결론과 범위

기준안의 **방향(REUSE 우선, 새 분석 스킬·원장·RAG 선제 개발 금지)은 코드로도 타당**하다. 그러나 기준안이 "미확인"으로 둔 접점 중 **다섯 개가 실제 코드에서 결함 또는 공백으로 확정**됐고(R01, R02, R03, R04의 P4 과거 변경, R07), 기준안 질문 밖의 **새 결함 세 건**(N1~N3)이 나왔다. 최소 수정은 모두 기존 스킬 안의 소규모 CONNECT/EXTEND이며 새 엔진은 필요 없다.

- **증거 범위**: PUBLIC `L1Work`의 기게시 스킬 ZIP 6종(`code-analyzer`, `p4-code-owner`, `l1-github`, `work-ledger-kernel`, `issue-analyzer`, `l1-fix-workflow`)의 실제 소스를 읽었다. 이 중 세 ZIP의 Git blob SHA는 계약 감사가 고정한 값과 일치했다. **회사 L1 소스·내부 MCP·로그·실제 CL/PR 번호는 접근하지 않았고 이 문서에도 없다.** 사내 설치본과의 드리프트(C01)는 `NOT_VERIFIED`다.
- **실행한 것**: 임시 폴더·임시 HOME·합성 입력에서만. 실제 원장·네트워크·모델 호출 0. 원장 시험은 Python 3.11에서 구문 오류가 나는 파일(N1) 때문에 **한 줄의 따옴표 모양만 바꾼 임시 복사본**으로 수행했다(게시된 패키지는 수정하지 않음).
- **읽은 범위의 한계**: 기준안, 요청서, 계약 감사, G0 부분 감사, 피드백 판정은 전체를 읽었다. K5.8/K6 워크플로 계약(약 38KB)과 `CURRENT.md`(약 51KB)는 구조와 관련 줄만 확인했다. R09는 그래서 E1 수준이다.
- **독립성**: 별도 세션·별도 입력으로 수행했다. 이 설계의 작성 주체는 아니나, 같은 협업 저장소에서 다른 작업(CoWork 감시기)을 해온 Claude Code 세션이다.

## 1. 질문별 판정

| ID | 판단 | 심각도 | 근거 | 요지 |
|---|---|---|---|---|
| R01 | REVISE | BLOCKING(확정) | E2 실행 | CL 번호만으로 시작하는 공식 경로 **없음** |
| R02 | REVISE | BLOCKING(확정) | E2 코드 | `merged`·`merge_commit_sha`를 읽지 않아 병합과 단순 종료가 구분되지 않음 |
| R03 | ACCEPT_WITH_CHANGE | BLOCKING | E2 코드 | 그룹핑의 재사용 가능한 부분은 Jira 연결 CL뿐, 나머지는 신규 규칙 필요 |
| R04 | ACCEPT_WITH_CHANGE | BLOCKING(P4 과거) / MAJOR | E2 코드 | 파일별 판정 집계는 좋음, 과거 CL의 이전·이후 내용을 읽는 경로 없음 |
| R05 | ACCEPT_WITH_CHANGE | MAJOR | E2 스키마 | 주장 상태(확인/추론/불명)는 메타데이터에 자리가 없어 파일 안에 있어야 함 |
| R06 | ACCEPT | MINOR | E2 코드 | `issue-analyzer`는 로그·SDM·TXT 입력 전용, CL/PR만으로는 호출하지 않는 것이 맞음 |
| R07 | REVISE | BLOCKING(확정) | E2 실행 | 미등록 조합은 거부됨, 단 `delivery` 슬롯 우회는 **수락**되어 위험 |
| R08 | ACCEPT_WITH_CHANGE | MAJOR | E2 실행 | CL/PR로 Work를 찾는 기능은 이미 있음, 참조 정규화가 없어 중복 위험 |
| R09 | ACCEPT_WITH_CHANGE | MAJOR | E1 | 게시·역링크 독립 상태는 타당, 코드 근거는 미확보 |
| R10 | ACCEPT | MAJOR | E1/E2 | 반출 경계는 충분, 아래 N3과 하나의 정책 충돌 정리 필요 |
| R11 | ACCEPT_WITH_CHANGE | MAJOR | 실행 포함 | 파일럿 우선순위 재배열(§5) |
| R12 | — | MAJOR | — | 스킬별 최소 변경 매트릭스(§4) |

## 2. 확인된 문제와 최소 수정안 (FINDINGS)

### F-R01 (BLOCKING) CL 목록만으로 시작하는 공식 경로 없음
- **증거(E2)**: `jira_fix_cl_scan.py`의 `prepare`는 입력 Markdown에서 Jira 키를 정규식으로 뽑고 없으면 `ValueError("No Jira Issue Keys in MD input")`로 끝난다(합성 CL 3개 목록으로 실행, 종료코드 2, 산출물 0). CL 후보 자체가 Jira 설명·댓글 텍스트에서만 추출된다(`cl_candidates`). 유일한 CL 입력 액션인 `cl-coverage`는 "이 CL이 여러 로컬 브랜치에 반영됐는가"가 목적이며 로컬 매핑된 브랜치 폴더가 필요하고, P4 접근은 Mango MCP 필수(단독 실행은 계약상 `MANGO_MCP_REQUIRED`로 실패)다.
- **영향**: 사용자가 CL 번호만 주면 기존 스킬로는 시작할 수 없다. Jira를 임의로 만들어 채우는 우회는 금지(올바른 판단).
- **최소 수정**: `p4-code-owner`에 **Jira 비의존 단계 하나** 추가(예: `cl-evidence`). Agent가 Mango 읽기 도구(`describe`, `filelog`, `integrated`, `fstat`)로 모은 CL별 레코드를 받아 **기존 `validated_change()`를 그대로 재사용**해 L1 범위·통합 원본 미확인(`INTEGRATION_ORIGIN_UNRESOLVED`)을 판정한다. 역할은 기본 `UNKNOWN_ROLE`, 가짜 Jira 키 대신 `UNLINKED` 그룹. 예상 규모는 스크립트 한 단계와 선택 필드 추가.
- **부정시험**: CL만 있는 목록 → `UNLINKED`로 수집, Jira 키 생성 0, L1 범위 설정 없음 → `SCOPE_NOT_CONFIGURED`, 통합 CL 원본 미확인 → `PENDING`.
- **소유**: `p4-code-owner`.

### F-R02 (BLOCKING) 병합 여부와 실제 반영 SHA를 분리하지 않음
- **증거(E2)**: `pr_code_analysis.py::_token_metadata`는 `state`, `base.sha`, `head.sha`, 브랜치 이름만 읽는다. **`merged`, `merged_at`, `merge_commit_sha`는 어디에서도 읽지 않는다.** GitHub의 병합된 PR과 병합 없이 닫힌 PR은 모두 `state=closed`이므로 둘이 같은 `CLOSED`로 기록된다. 분석 범위는 `merge-base(base, head)..head`(PR 자체의 변경)로 올바르게 계산하지만, "대상 브랜치에 실제로 무엇이 들어갔는가"를 나타내는 필드가 핸드오프에 없다. 스쿼시·리베이스 병합이면 PR head 커밋이 대상 이력의 조상이 아니어서, `semantic_workspace_ready`(HEAD가 PR head와 같을 때만 참)로 분석한 코드는 **병합 전 트리**다.
- **영향**: "머지됨" 하나로 대상 브랜치 반영·현행 코드 확인을 주장하게 되는 오류(기준안 R02가 금지한 것)를 현재 코드는 막지 못한다.
- **최소 수정**: 같은 `pulls/{n}` 응답에 이미 들어 있는 `merged`, `merged_at`, `merge_commit_sha`를 핸드오프에 추가하고(`base.ref`는 이미 수집 중) `landing` 블록(`MERGED / CLOSED_UNMERGED / OPEN`, 병합 방식 추정, `head_reachable_from_target`)을 둔다. 추가 API 호출 불필요.
- **부정시험**: 닫힌 미병합 PR → `CLOSED_UNMERGED`, 스쿼시 병합 → head 조상 아님 표시 + 반영 커밋 별도 diff, 리베이스 병합 → 동일.
- **소유**: `l1-github`.

### F-R03 (BLOCKING) 그룹핑 신뢰 기준은 Jira 연결 부분만 재사용 가능
- **증거(E2)**: CL의 역할 분류(`FIX/INTEGRATION/REVERT/REFERENCE/UNKNOWN_ROLE`)와 한 이슈 키 아래 여러 CL을 묶는 것은 `score_issues`가 이미 한다(한 CL이 여러 이슈에 속하는 N:M도 후보로 허용). 반면 **Jira가 없는 변경끼리 같은 이슈로 묶는 로직은 어떤 스킬에도 없다.**
- **영향**: 그룹핑이 곧 신규 개발 범위다. 같은 모듈·같은 수정자로 묶는 단순 휴리스틱은 기준안이 금지한 것이라 선택지가 아니다.
- **최소 수정**: 파일럿에서는 **자동 병합 없이 "근거 목록이 붙은 후보 그룹"만 생성**(공통 Jira 키, 공통 통합 계보, 명시적 상호 참조만 근거로 허용). 근거가 하나도 없으면 `UNLINKED` 단독 케이스. 병합은 사용자 확인 후에만. 신규 엔진은 만들지 않는다.
- **부정시험**: T04(같은 모듈의 별개 이슈 2개)에서 병합 0, 근거 없는 후보 그룹 0.
- **소유**: 연결 규칙은 Workflow 쪽 connector, 데이터는 위 두 스킬.

### F-R04 (BLOCKING: P4 과거 변경 / MAJOR: 그 외) code-analyzer 입력
- **증거(E2)**: 좋은 점: `provenance_resolver`는 단일 기준 CL에 대해 파일별 `VERIFIED/MISMATCH/UNKNOWN`을 내고 **하나라도 MISMATCH면 전체 MISMATCH, UNKNOWN이면 전체 UNKNOWN**으로 집계한다. 따라서 파일마다 리비전이 섞인 상태에서 `CODE_CONFIRMED`가 나오지 않는다(`allow_assumed_head` 기본 거짓, 기준 CL을 추론하지 않음). 한계: 이 검증은 **현재 작업 복사본이 한 기준 CL의 상태와 같은가**만 본다. 과거 CL의 이전·이후 내용을 읽기 전용으로 되살리는 기능은 없고(`p4 sync`는 `p4-code-owner`가 금지), `p4_evidence.json`의 `files[]`에는 `path`와 `action`뿐이라 **파일별 리비전 필드가 없다**.
- **영향**: P4 과거 CL은 현재 작업 복사본이 우연히 같지 않은 한 코드 확정(`CODE_CONFIRMED`)에 도달할 수 없다. 이슈 그룹이 여러 CL에 걸치면 기준 CL이 하나뿐인 스코프 모델과 맞지 않는다.
- **최소 수정(파일럿)**: ①P4 과거 변경은 **`INFERENCE`(diff 텍스트 기반)로 명시 고정**, 현행 코드 확정 주장 차단. ②`p4_evidence`의 `files[]`에 **선택 필드** `rev`, `from_rev` 추가(Mango `describe`가 제공). ③그룹이 여러 CL이면 스코프를 CL별로 나눈다. ④읽기 전용 스냅샷 생성기(`print`로 임시 트리 구성)는 **DEFER**, 파일럿에서 실제로 필요하다고 판명될 때만.
- **부정시험**: T07(리비전 혼합, dirty, 객체 누락) → 전체 비확정, Knowledge 게시 차단.
- **소유**: `p4-code-owner`(필드), connector(명시 고정).

### F-R05 (MAJOR) 주장 상태는 메타데이터에 자리가 없다
- **증거(E2)**: Evidence 스키마의 `confidence_state`는 `AUTO_CANDIDATE | HUMAN_CONFIRMED | REJECTED | SUPERSEDED`뿐이고 `additionalProperties:false`, `code_rev`는 문자열 하나다. 코드 분석기의 증거 상태(`CODE_CONFIRMED`, `RN`)는 코드 사실에 대한 것이고, "문제·원인·수정" 같은 이슈 주장의 상태는 정의되어 있지 않다.
- **영향**: Kernel은 `INFERENCE`와 `확인`을 구분해 강제할 수 없다. 기준안 §4의 `claim state`가 **어디에서도 집행되지 않으면** 무심코 확정처럼 읽힌다.
- **최소 수정**: 주장 상태·근거 앵커·미확인을 **Evidence 파일(`path`, sha256 결합) 안의 정형 필드**로 두고, 요약(`summary`)에는 상태 약어를 필수로 넣는다. 메타데이터 필드 추가 금지(G0-M01: 스키마는 추가 필드를 금지하는데 런타임 검증기는 통과시키는 불일치가 이미 보고되어 있으므로 그 빈틈에 기대지 말 것). 수정 반영·시험·현행성은 `verification_result`를 쓰지 않고(검증 단계 Evidence 전용) 파일 안 별도 상태로 둔다.
- **부정시험**: T12(원인 확인 + 시험 `NOT_RUN`) → `VERIFIED_CLOSED` 표기 불가.
- **소유**: connector 문서화.

### F-R06 (MINOR) issue-analyzer
- `issue-analyzer`의 입력은 `.sdm`, `.log`, `.txt` 또는 붙여넣은 로그와 증상이며, Kernel 슬롯도 `BUG`, `BUG-NR` 프로필의 `analyze-issue`뿐이다. 로그·증상이 없는 CL/PR 시작에서는 **호출하지 않는다**는 기준안이 맞다. 증상 로그가 후에 제공될 때만 선택 연계.

### F-R07 (BLOCKING) Kernel Evidence 등록부와 `delivery` 우회 위험
- **증거(E2, 실행)**: 임시 원장에서 `p4-code-owner/p4_cl_provenance/analyze`, `l1-github/pr_analysis/analyze`, `code-analyzer/code_review/analyze` 기록 시도가 **모두 `REGISTRY_MISMATCH`**로 거부됐다(G0의 6건 합성 시험 결과와 일치). 등록부에서 `l1-github`는 `deliver` 단계의 `delivery` 종류로만, `p4-code-owner`는 어디에도 없다.
- **새로 확인한 위험(E2, 실행)**: `l1-github/delivery/deliver` 기록은 **수락**된다. `delivery` 증거는 상태 전이 `DELIVERED`의 가드(`delivery_evidence_present`)이고 `DELIVERED` 상태에서는 무효화(stale) 판정의 대상이다. 과거 PR을 이 슬롯에 넣으면 **"이 Work가 전달한 변경"의 증거로 읽힌다.** 자동으로 `DELIVERED`가 되지는 않는다(`VERIFIED` 상태와 사용자 `approve-delivery`가 추가로 필요).
- **영향**: 등록부가 막아주는 경로 옆에 "수락되지만 의미가 틀린" 경로가 열려 있다. 한쪽 provider를 다른 용도로 쓰는 것은 기준안이 금지한 가장(masquerade)이다.
- **최소 수정**: **P4/PR 출처를 `delivery`나 `change_provenance`에 넣지 않는다**고 connector 계약에 명시한다. `change_provenance`는 이름이 같아도 정규 `code_rev`(64자리 작업트리 다이제스트)와 `spec_digest` 결합 규칙이 붙어 있어(`record_evidence`) 쓰면 안 된다. 코드 사실은 기존 `code-analyzer`의 `analyze-code` 슬롯(`asis_callflow`, `impact`)을 그대로 쓴다. 이슈 서술과 출처는 **Evidence가 아니라 Work 문서(exporter)**를 먼저 시도하고, 그것이 불가능하다고 파일럿에서 증명될 때만 Kernel 쪽에 **새 provider·종류 쌍**(예: `observed_change_set`, 기존 이름과 충돌 없게)을 등록부 변경으로 요청한다.
- **부정시험**: T10 재확인 + "과거 PR을 `delivery`로 기록하려는 connector"를 거부하는 시험(connector 쪽).
- **소유**: Kernel 변경은 DEFER, connector 규칙은 Workflow.

### F-R08 (MAJOR) Work 재개·중복 방지
- **증거(E2, 실행)**: Kernel은 이미 `work_reference_add`/`work_find`로 **P4 CL과 GitHub PR로 Work를 찾는 기능**과 한 Work에 여러 참조를 붙이는 N:M을 제공하고, 같은 값 재추가는 `already_present`로 무해하다. `set_work_name`은 이름 중복을 `WORK_NAME_CONFLICT`로 거부해 **결정적 키로 쓸 수 있다**. 그러나 **정규화가 없다**: 같은 CL이 `5322160`, `CL 5322160`, `perforce:server-a:5322160` 세 값으로 모두 수락되어 별개 값으로 저장되고, 검색은 대소문자 무시 **완전 일치**라 `CL5322160`은 찾지 못한다. GitHub PR URL도 끝의 `/` 유무가 서로 다른 값이다(`#files`, `http`는 거부). 또한 CL 번호에는 **P4 서버 식별이 없다**.
- **영향**: 같은 목록을 다른 표기로 재입력하면 기존 Work를 못 찾고 **중복 Work가 생길 수 있다**(이 부분은 코드와 위 실행으로 추론, 두 번째 Work 생성까지는 시연하지 않음).
- **최소 수정**: 새 원장 없이 **connector의 정규화 규칙**만: CL은 `p4:<서버 별칭>:<번호>`, PR은 호스트 소문자·끝 `/`·조각 제거. 정규 참조 집합의 해시로 `work_name`(`CLPR-<10자>`)을 정하고 `work-find` 선행 후 있으면 재사용, 서로 다른 Work에 걸치면 병합하지 않고 사용자 확인. `purpose=TRACKING_ONLY`는 이미 있는 값이다. 프로필은 임시로 `MAINT`가 기본이라(`profile or "MAINT"`) **이슈 서술 슬롯 `analyze-issue`(BUG, BUG-NR 전용)를 쓸 일이 없는지** 먼저 정하고, 필요하면 확인된 프로필로 시작한다.
- **부정시험**: T09(표기·순서만 다른 동일 목록) → 새 Work 0, 참조 중복 0.
- **소유**: connector(Workflow 연계).

### F-R09 (MAJOR) 지식 승격 연결 — E1
기준안의 독립 상태(원인 확인·수정 반영·시험·현행성)와 "게시와 역링크는 독립", "v0.9 검토행은 실제 ID가 아님"은 최신 피드백 판정·K5.8/K6 계약과 일치한다. 코드 근거는 확보하지 못했다(`NOT_VERIFIED`). 요구: 승격 후보에는 위 F-R05의 상태 필드를 **그대로 전달**하고, 현행성·수정·시험 미확인 항목이 있으면 그 사실을 후보에 표시.

### F-R10 (ACCEPT) 반출·승인 경계
요청서의 경계(PRIVATE에 제한 자료 0, 회사 코드 없는 E1/E2와 업무 호스트 E3 분리)는 충분하다. 이 리뷰 자체가 그 경계로 수행됐다(공개 스킬 소스만 사용). 단 **N3**을 정리해야 E3에서 흔들리지 않는다.

## 3. 새 결함 (기준안 질문 밖)

- **N1 (MAJOR, 호스트 Python이 3.12 미만이면 BLOCKING)**: 두 파일이 **Python 3.12 이상의 문법**을 쓴다. `work_ux.py:1290`(f-string 안에서 같은 종류 따옴표 중첩)과 code-analyzer `share_export.py:178`(f-string 표현식 안의 역슬래시). 505개 파일 중 이 2개만 3.11에서 구문 분석 실패이고 나머지 4개 패키지는 0개다. 그런데 Kernel `pyproject.toml`은 `requires-python = ">=3.10"`이며 개발 시험은 Python 3.13에서만 수행됐다. **`work_ux.py`를 임포트하는 모든 `work-*` 명령이 3.10/3.11에서 시작도 못 한다**(이 호스트 3.11에서 `work-create` 실패 재현). 사내 호스트 Python 버전은 `NOT_VERIFIED`. **최소 수정**: 두 줄을 호환 문법으로 고치거나 요구 버전을 `>=3.12`로 정정하고 CI에서 선언한 최소 버전으로 구문 검사. **소유**: Kernel, code-analyzer.
- **N2 (MAJOR)**: `l1-github`의 PR 분석 체크아웃은 **저장소당 하나만 유지하고 다른 PR이 같은 작업 트리를 교체**한다(`_workspace_path` 정책). PR 목록을 연속 분석하면 앞 PR의 `semantic_workspace_ready`가 뒤 PR에 의해 깨질 수 있다. **최소 수정**: 한 PR의 code-analyzer 결과(와 핸드오프)를 확보한 뒤에만 다음 PR로 진행하도록 connector에서 **직렬화**하고, 분석 직전에 준비 상태를 재확인. **소유**: connector.
- **N3 (MAJOR)**: **P4 접근 정책이 두 스킬에서 충돌**한다. `p4-code-owner`는 로컬 `p4` CLI·서브프로세스를 금지하고 Mango MCP만 허용하지만, code-analyzer의 `provenance_resolver`는 로컬 `p4` 실행 파일을 호출한다(`p4_executable`, 기준 다이제스트 조회, CRLF 판별용 `p4 diff`). **최소 수정**: CL/PR 흐름의 P4 제공자를 **Mango MCP 단일**로 정하고, 기준 증거는 `EVIDENCE_FILE` 경로(`depot_path`, `revision`, `digest` 행)로 주입한다. 로컬 `p4` 사용 가능 여부는 E3에서 확인(`NOT_VERIFIED`). **소유**: connector + 호스트 정책.

## 4. SKILL_MATRIX

| 스킬 | 판정 | 확인한 계약 / 공백 |
|---|---|---|
| `l1-fix-workflow` | REUSE + CONNECT | Work 선택·재개(`resume --work-id` 정확한 ID). 같은 Jira에 Work가 여러 개일 수 있다는 점을 코드가 인정. 이 연결의 **connector 규칙**(정규화·직렬화·상태 필드)을 둘 곳 |
| `l1-github` | REUSE + EXTEND(소) | PR 범위·SHA 검증·분리 작업트리 우수. 공백: `merged`·`merge_commit_sha` 미사용(F-R02), 체크아웃 단일(N2). 리뷰 댓글 수집기는 확인한 코드에 없음(G0-M02와 같은 결론, `NOT_VERIFIED`) |
| `p4-code-owner` | REUSE + EXTEND(소) | Jira 연결 CL 판정·통합 계보 규칙 우수(`validated_change`). 공백: CL 단독 시작(F-R01), 파일별 리비전 필드(F-R04) |
| `code-analyzer` | REUSE | Git PR 범위·증분·기준 CL 검증·MSC. 공백: P4 과거 변경의 스냅샷(DEFER), `share_export.py` 3.12 문법(N1), 로컬 `p4` 호출(N3) |
| `issue-analyzer` | DEFER(조건부) | 로그·증상 있을 때만 |
| `work-ledger-kernel` | REUSE, 변경 DEFER | 등록부·참조·이름 유일성 활용. `work_ux.py` 3.12 문법(N1). 등록부 확장은 파일럿이 필요를 증명할 때만, `delivery` 우회는 금지 |
| `l1-knowledge-updater` | DEFER | 게시·승격은 후속, 입력 상태 필드만 맞춰 둠 |

## 5. 테스트 T01~T14 (실근거)

| ID | 결과 | 근거 |
|---|---|---|
| T01 PR 단독 | NOT_RUN | git·gh 필요, 설계는 타당(범위 계산 정확) |
| T02 CL만, Jira 없음 | **PASS(경로 부재를 확인)** | 실행: `prepare` 종료 2 `No Jira Issue Keys`, 산출물 0 → `ADDITIONAL_CHECK_REQUIRED`가 맞고 Jira 생성은 없음 |
| T03 2 CL + PR 1 한 이슈 | NOT_RUN | F-R01·F-R03 수정 선행 |
| T04 같은 모듈 별개 이슈 | NOT_RUN | 병합 금지 규칙은 F-R03에서 설계 |
| T05 병합했지만 스쿼시·백포트 미연결 | **FAIL_STATIC** | 현재 `l1-github` 코드는 반영 SHA 필드가 없어 분리 판정 불가(F-R02) |
| T06 통합 CL, 원본 불명 | **PASS_STATIC** | `validated_change`: 통합 + 원본 미확인 → `INTEGRATION_ORIGIN_UNRESOLVED`(코드 읽기, 미실행) |
| T07 dirty·객체 누락·리비전 혼합 | **PARTIAL** | P4 혼합은 집계로 차단(정적 PASS), Git 객체 누락·dirty는 문서·코드상 보호, 실행 미확인 |
| T08 댓글 일부 누락 | **PARTIAL** | Jira는 `comments_complete`로 처리(정적), PR 리뷰 댓글 수집기는 확인되지 않음 |
| T09 동일 목록 재입력 | **PARTIAL(실행)** | 정확히 같은 값은 무해하게 재사용, 표기 차이는 별개 값으로 저장·검색 불가(F-R08). 정규화가 있으면 PASS 기대 |
| T10 미등록 provider·종류 | **PASS(실행)** | 3건 `REGISTRY_MISMATCH`. 단 `delivery` 우회 수락(F-R07) |
| T11 Run 정리 후 재열람 | NOT_RUN | 실제 호스트 필요(G0 H03) |
| T12 원인 확인·시험 NOT_RUN | NOT_RUN | 상태 필드 설계(F-R05) 후 확인 |
| T13 PRIVATE에 회사 자료 | NOT_RUN | 이 리뷰는 공개 소스만 사용했으나 차단 장치 시험은 아님 |
| T14 Workspace만 성공 | NOT_RUN | 후속 |
**파일럿 우선순위(제안)**: ①T02, T09, T10(이미 실행 가능, 수정 후 재실행) ②T05, T06, T07(F-R02, F-R04 수정 후) ③T03, T04(그룹핑) ④나머지는 첫 승인된 실제 분석 후.

## 6. 기준안에 대한 필수 변경 (설계 문서 수정 요청)

1. §2 표의 `p4-code-owner` 미확인 항목을 **확인됨(공식 CL 단독 경로 없음, `cl-coverage`는 목적이 다름)**으로 갱신하고 F-R01의 CONNECT를 명시.
2. §3 S1에 **`merged`·`merge_commit_sha`·반영 커밋** 수집을 필수로 추가하고, 현재 코드에 없음을 명기(F-R02).
3. §3 S3에 **P4 과거 변경은 `INFERENCE`로 고정**한다는 규칙과 파일별 리비전 필드(F-R04).
4. §3 S6에 **금지 목록**을 추가: `delivery`, `change_provenance`, 가짜 provider 사용 금지(F-R07). 참조 정규화와 `work_name` 키(F-R08).
5. 새 §에 **실행 환경 전제**: Python 최소 버전(N1), P4 제공자 단일화(N3), PR 직렬화(N2).

## 7. 미확인·차단 (UNVERIFIED_OR_BLOCKED)

- E3 전부(사내 설치본 버전·해시·드리프트, 실제 MCP 도구 이름·권한, 실제 반환 JSON): `NOT_VERIFIED`. 미확인을 미지원으로 단정하지 않는다.
- GitHub PR 리뷰 댓글·승인 수집, 페이지 누락 처리: 확인한 코드에 수집기 없음(`NOT_VERIFIED`).
- Work 문서(exporter)로 이슈 서술을 보관할 수 있는지, Run 정리 후 링크 무결성: 호스트 시험 필요(G0 C09, C10).
- Evidence 스키마와 런타임 검증의 불일치(G0-M01): 이번에 재시험하지 않고 G0 결과를 재사용.
- 한 호스트에서 `work-find`가 두 Work에 걸친 참조를 반환할 때의 실제 동작·병합 정책: 설계 필요.

## 8. 실행·게시 경계 확인
코드 수정, 설치, 운영 변경, 스킬 ZIP·Kernel 등록부 변경, 회사 Git/P4 쓰기, Job·MCP 실행, 모델 자동 호출, 감시기·DB·Task 변경, PUBLIC 게시, 그룹 지식 쓰기: 모두 **NOT_RUN**. 시험은 임시 폴더에서 합성 입력으로만 수행했고 끝난 뒤 삭제했다. 이 문서에는 회사 코드·경로·로그·MCP ID·실제 CL/PR 번호·토큰이 없다(예시 번호는 모두 합성값).

## 9. NEXT_ONE_ACTION
GPT가 §6의 다섯 가지 변경을 기준안에 반영하고, 그 뒤 사용자가 사내 호스트에서 **읽기 전용 확인 세 가지**(Python 버전, P4 접근 제공자(Mango MCP 단일 여부), `l1-github pr-code-analysis` 실제 반환 JSON의 `merged` 계열 필드)만 보고한다. 코드 변경(F-R01, F-R02, N1)은 그 확인과 소유자 승인 뒤 별도 작업으로 진행하고, 파일럿은 합성 CL 3개·PR 2개로 T02, T09, T10부터 시작한다.

```text
RESULT_POST / COMMIT / SHA256 / READBACK: (게시 후 실제 값은 최종 보고와 원격 조회로 확인)
```
