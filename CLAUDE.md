# CoWork — Windows Claude Code 세션 시작 지침

@AGENTS.md
@collab/CONTEXT_BRIEF.md

## 자연어 정식 리뷰 요청 접수 시 필수 경로

진행 중인 설계·개발 세션에서 “리뷰요청해줘” 또는 “리뷰 요청해줘”만 지시하더라도 **지금까지 확정한 동일 Work의 최신 설계·구현물**을 대상으로 삼는다. 별도 긴 프롬프트·Work ID·파일 경로를 다시 요구하지 않는다. 새 세션에서 “정식 리뷰 요청/협업 리뷰/재리뷰”라고 하면 `@AGENTS.md`의 자연어 리뷰 요청 규칙을 먼저 적용한다. 기존 Work/REQUEST/READY/영수증/현재 LIVE 정책을 재조회하고, 신규 요청은 `collab/ops/submit_review_request.py`의 읽기 전용 사전검사 → 유효 시 명시적 `--publish` 경로를 사용한다. 기존 요청을 자동으로 재발행하지 않는다. `SUBMITTED_AWAITING_PROTECTED_SIGNER`는 정식 제출·PIN 확인까지만 의미하며 서명·READY·모델/영수증과 다르다. 승인·비용·위임·중복은 현재 보호 signer에서 별도로 검증한다.

**주요 검증:** Commit A에 `REQUEST.md`와 ZIP이 모두 있는지, Commit B PIN이 정확히 A를 가리키는지, ZIP SHA/크기 및 `repo_id` 문자열이 맞는지. 오류는 게시/후속 단계 `BLOCKED`로 중단한다. 저장소에 문서를 올린 것만으로 Windows PC가 이 절차를 실행한다고 간주하지 않는다.

## 세션 시작 시 자동 인식 범위

- 이 파일과 위 두 상대경로 import는 **CoWork 저장소를 현재 작업 디렉터리 또는 상위 디렉터리로 두고 실행한 Claude Code 세션**의 프로젝트 맥락이다. GitHub에 게시하는 것만으로 Windows PC의 클론 동기화나 실행 중인 세션 로딩이 완료되는 것은 아니다.
- 로딩된 브리프는 로컬 체크아웃의 **시작 지도**이고, 최신 실행 상태의 정본은 아니다. 첫 사용자 요청이 협업 현황·스킬·릴리스·지식 설계·리뷰·승인을 다루면, 답변 전에 GitHub PUBLIC `wonhwipark/CoWork-Skill-Collab` **main**의 `collab/CONTEXT_BRIEF.md`와 요청 목적별 `CURRENT.md` **최상단 현재 요약**을 읽기 전용으로 조회하고 필요한 최신 결과·리뷰·영수증만 추가 확인한다.
- 특히 **L1Work 스킬 현황** 요청은 `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md` → `L1WORK_PUBLIC_SKILL_RELEASE_ANALYSIS_r0001_20261117_KST.md` → 실제 PUBLIC `wonhwipark/L1Work/main` HEAD 순으로 대조한다. **개발 후보 / PUBLIC 최종 ZIP / 호스트 설치 / 실제 실행**을 각각 구분한다. 해당 분석 파일은 고정 시점 스냅샷이다.
- 리뷰·승인·운송 상태는 각각 **해당 목적의 CURRENT** 및 실제 REQUEST/READY/REVIEW_RESULT/RECEIPT에서 확인한다. 파일이 있다는 이유만으로 승인이나 watcher 트리거·모델 호출·작업 완료로 간주하지 않는다.
- GitHub 최신 조회나 실행 호스트 확인이 불가능하면 마지막 확인 시점과 `NOT_VERIFIED`를 명시하고 과거 정보로 실행 가능 여부를 확정하지 않는다. 읽기만을 위해 신규 Job·리뷰 요청·READY·예약·유료 호출·PUBLIC 쓰기·운영 설정 변경을 만들지 않는다.
- 동일 내용을 새 상태 원장으로 복제하지 않는다. 사용자가 실행을 지시한 경우 기존 Work와 유효 승인 범위에서만 진행하고 결과·최신 상태는 기존 CURRENT/결과 문서에 보존한다.

## 실행 확인

- Windows Claude Code에서 이 저장소의 실제 최신 `main` 체크아웃으로 시작하고 `/context all`의 **Memory files**에서 `CLAUDE.md`와 두 import 로딩 여부를 확인한다. `AGENTS.md`는 중복 정본을 새로 만들지 않고 import만 한다.
- 본 파일의 GitHub readback 및 상대경로 정적 확인은 **호스트 자동 로딩 E2E PASS가 아니다**. Windows 로컬 실행 경로·클론 최신화·Claude Code 버전·설정·`/context all` 결과는 호스트에서 별도 확인한다.


## P1/P2 단계별 맥락 조회 — 질문이 들어온 경우에만

- CoWork 전체/스킬/운영/Knowledge 현황 질문이 들어오면, 먼저 `collab/CONTEXT_BRIEF.md`로 기존 Work를 찾고 해당 `CURRENT.md` **최신 요약과 필요한 하위 작업 흐름**을 확인한다. 질문이 최신 최상단 단락과 다른 흐름을 묻는 경우, 이 Work의 기존 하위 제목/최신 결과를 **추가 조회**해 문맥 누락을 막는다. 여러 Work가 관련된 질문이면 해당 목적 CURRENT만 추가한다.
- PUBLIC 최신 `main` 로컬 checkout을 검증했고 Python 실행이 허용된 경우에 한해 기존 읽기 전용 조회기 `python collab/dashboard/context_query.py --root . --question "사용자 질문"`을 **보조 힌트**로 사용할 수 있다. 매번 CLI를 호출할 의무는 없으며, 조회 실패나 오래된 로컬 checkout이면 직접 GitHub main을 읽어 확인한다. 조회기 결과 `LOCAL_CURRENT_READ_ONLY`는 원격 최신성·호스트 LIVE·완료 판정이 아니다.
- 연결된 요청·패키지·리뷰·영수증의 파일 존재만으로 독립 리뷰/승인/비용 지급/READY·호스트 실행이 확인됐다고 말하지 않는다. 비교 기준 commit이 고정되지 않았다면 변경분 추정 금지. PUBLIC에는 기존 allowlist만 사용.
- 구체적인 목적별 경로·예시는 [P1/P2 적용 가이드](collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_CONTEXT_APPLICATION_GUIDE_r0001_20261120_KST.md), [실사용 검증 체크](collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/P1_P2_AUTO_USE_READONLY_E2E_CHECK_r0001_20261120_KST.md)에 기록. **이 문서 게시는 로컬 세션 로딩/실행을 증명하지 않음**. 사용자가 명시적으로 요구하지 않은 유료 리뷰·LIVE 변경·이전 REQUEST 재실행 금지.

## 신규 REQUEST의 정책 사전 호환성

GPT가 신규 리뷰 요청을 준비할 때 Windows Claude Code는 LIVE 운영 설정을 **읽기 전용** 조회하고, `collab/ops/review_request_gate.py select/check`를 기존 승인 범위 내에서 실행해 정책명·건당 예산·고정 ZIP SHA/CRC가 호환되는지만 보고한다. 로컬 설정 파일의 내용·토큰·개인키는 GitHub/대화/로그에 복사하지 않는다. `POLICY_COMPATIBLE_NOT_APPROVED` 및 `PASS_PREPUBLICATION_ONLY`는 승인/서명/READY/모델 실행의 증거가 아니다. 실제 승인·서명 전에는 별도 `approve_request.py check`의 보호 범위·만료·권한 검사를 수행한다. 설계 후보에만 있는 미등록 정책으로 기존 LIVE 리뷰를 요청하지 않는다. 조회·시험 실패 시 BLOCKED, 직접 정책 설정/위임을 우회 변경하지 않는다.

