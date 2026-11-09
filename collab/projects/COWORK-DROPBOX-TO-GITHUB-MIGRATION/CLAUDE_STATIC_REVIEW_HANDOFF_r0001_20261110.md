# Windows Claude Code 인계 — GitHub adapter 독립 정적 설계 검토 r0001
2026-11-10 KST | 상태: `HANDOFF_POSTED`, `CLAUDE_REVIEW=NOT_RUN`, `NO_LIVE_CHANGE`

## 목표
Dropbox `/SKILL-COLLAB/`에서 작동하던 **GPT→REQUEST/READY→Python watcher→Claude Code 리뷰→REVIEW_RESULT/RECEIPT→GPT 판정·재수정** 계약을, 동작과 운영 통제를 유지한 채 GitHub PRIVATE repo 운송 계층으로 바꾸는 설계를 독립적으로 검토한다.

## 참조
- GitHub PRIVATE: `wonhwipark/CoWork-Skill-Collab`
- 검토 브랜치: `review/github-adapter-design-20261110`
- 필독 설계: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GITHUB_ADAPTER_AND_REVIEW_FLOW_DESIGN_r0001_20261110.md`
- 공통 계약(main): `collab/ops/CONTRACTS/REVIEW_TRANSPORT_V1.md`
- 최신 main 상태: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`
- 기존 Windows 실행 호스트: 실제 watcher 설치 소스/설정(로컬 읽기 전용); 버전 추정 금지
- 기존 운영 규칙: 현재 Dropbox `knowledge/OPERATING_RULES_r0010.md` 및 `REQUEST_PUBLICATION_GUARD_20261106.md` (접근 가능할 경우 비교, 파일 경로/사내 반출 여부는 확인)

## 우선 점검 질문
1. 동일 협업 semantics: 사용자 요청부터 GPT 판정까지 Dropbox와 비교해 누락된 필드·상태·인수인계/Telegram/SEMI_AUTO 단계가 없는가?
2. 현재 watcher의 실제 source/module names에서, 검증·비용·SQLite·Claude runner를 그대로 재사용하고 GitHub API만 교체할 수 있는 경계는 무엇인가?
3. 브랜치 보호 없는 PRIVATE repo에서 READY 파일 위조/서명 위조/commit pin TOCTOU/재생 공격/키 탈취 시 모델 실행을 어떻게 차단할 것인가?
4. YAML V1 REQUEST/READY와 신규 source pin/approval sidecar의 backward compatibility를 보장하려면 어떤 exact parser tests가 필요한가?
5. Dropbox LIVE와 GitHub SHADOW에서 동시 리뷰 0, 승인된 단일 LIVE로 전환 후 restart/429/crash 시 추가 Claude 호출 0을 어떻게 증명할 것인가?
6. GitHub 결과/영수증 CAS readback, Telegram 1회, GPT finding별 판정, 사용자가 모바일에서 재개하는 UX를 보존하는가?
7. PUBLIC `wonhwipark/L1Work`에는 승인 최종 ZIP만 전송, reviewer/watchers에는 Public write 0이 유지되는가?

## 실행 범위
- **허용:** 개인 Windows PC의 사전 승인된 기존 watcher/코드를 읽기 전용으로 점검; PRIVATE 설계 문서 비교; 테스트 갭·반례·최소 수정안 작성. 필요 시 별도 격리 작업 디렉터리에서 합성 fixture를 생성해 로컬 정적 테스트를 돌릴 수 있으나 운영 watcher 코드나 예약 작업을 변경하지 않는다.
- **금지:** 기존 Dropbox watcher 중단/재시작, GitHub 신규 LIVE, 실제 REQUEST/READY 게시, Claude 리뷰 실행을 위한 자동 감시기 호출, 실제 모델 리뷰 완료를 허위 기록, 토큰/개인키/사내 반출 금지 코드·로그를 GitHub에 업로드, PUBLIC ZIP 게시, SSH/인증 설정 무단 변경, `/AI-CONTINUITY/` 변경.
- 이 안내를 읽는 **대화형 Claude Code 세션의 정적 설계 검토**와 자동 watcher를 통한 **정식 비용/영수증 있는 독립 리뷰**를 구분한다. 현재 후자는 `NOT_RUN`.

## 기대 산출물
- `CLAUDE_STATIC_REVIEW_RESULT_FOR_GPT_20261110.md` (비밀 제거): 검토 자료/실측 여부, `ACCEPT / ACCEPT_WITH_CHANGE / BLOCK / NEED_INFO`, blocking findings 무제한, nonblocking 3~5개, 각 항목 ID/심각도/반례/영향/최소 수정/필수 시험.
- `WATCHER_REUSE_MATRIX_20261110.md`: 실측 파일/모듈명 기반 `REUSE / WRAP / REPLACE / UNKNOWN` 및 근거. 회사 자료이거나 비밀인 원문은 **로컬 보존**, 원격 보고에는 구조적·비민감 요약만.
- 테스트 매트릭스: 인계서 T01~T38 + 서명 보강 S01~S10의 `PASS/FAIL/NOT_RUN` 분리. 실제 실행 명령/환경/증거 없는 설계 가설은 PASS 금지.
- 다음 한 동작: 최소 수정 설계 반영 / 호스트 인증 차단 / 기존 Dropbox 정식 리뷰 준비 등 정확히 하나 제시.
- 결과는 우선 사용자 대화에 요약 보고하고, 회사 정책상 가능한 비민감 정적 결과만 PRIVATE repo의 검토 브랜치에 저장할 수 있다. 저장소 접근 또는 승인 문제가 생기면 `BLOCKED`로 표기한다.

## 공식 연동 실행의 다음 게이트
정식 GitHub REVIEW_REQUEST/READY는 watcher GitHub provider가 독립 테스트·권한·승인 서명을 통과한 뒤 승인된 단일 파일럿에만 적용한다. 그전 정식 독립 리뷰는 기존 검증된 Dropbox REQUEST/READY 경로를 사용한다. 일방적인 ZIP push 또는 PR 생성만으로 리뷰가 시작되어서는 안 된다.
