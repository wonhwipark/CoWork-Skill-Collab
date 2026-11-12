# CoWork 대시보드 — HTML Pages 기본 운영 및 공개 허용 목록

**정책 적용:** 2026-11-12 / **기본 URL:** https://wonhwipark.github.io/L1Work/cowork-dashboard/

## 현재 운영 결론

- **PAGES_DEFAULT=ENABLED:** 사용자가 대시보드를 확인할 때 기본으로 열어야 할 화면은 위 GitHub Pages HTML이다. GitHub PRIVATE HTML 소스 링크나 Markdown VIEW를 기본 UI로 제시하지 않는다.
- **PAGES_DEPLOY=PASS:** L1Work PUBLIC `main/docs/cowork-dashboard/index.html` 업데이트 후 GitHub Pages 배포 성공. 실제 PUBLIC 파일 GitHub readback PASS.
- **PUBLIC_DATA_SYNC=MANUAL_ALLOWLIST_ONLY:** PRIVATE 데이터와 공개 상태가 자동 연결된 것으로 보고하지 않는다. GitHub Pages 자동 빌드/배포는 **L1Work PUBLIC 파일이 바뀔 때만** 동작한다.
- **SOURCE_OF_TRUTH=PRIVATE_CURRENT_AND_VERIFIED_EVIDENCE:** 실제 진행 상태는 PRIVATE `CURRENT.md`, 리뷰·영수증 및 Actions 증거를 확인해 반영한다. 이전/미관측 정보는 PASS로 승격 금지.
- **CUTOVER=MIGRATION_NOT_CUTOVER:** 기존 LIVE Windows watcher, DB, 예약 작업, Telegram, Claude 독립 리뷰 운송 및 GitHub 전환에는 변경이나 승인을 부여하지 않는다.

## Executive Work Tracker 공개 적용 (2026-11-12)

- 사용자 선택: 디자인 시안 **01 Executive**. 기본 공개 URL은 `https://wonhwipark.github.io/L1Work/cowork-dashboard/` 그대로 유지하며, 공개 HTML의 상단 KPI → 개별 Work Tracker → 협업 7단계 흐름 → 검증·다음 조치 순서.
- **PUBLIC 승인 정보는 비식별·상위 범주만:** PRIVATE `CURRENT.md`가 존재하는 다섯 개 업무 범주(협업 운송, 대시보드, 스킬 탐색, 업무 자동화 후보, 지식 구조 설계)를 별도 카드로 표현한다. 내부 Work ID, PRIVATE 파일 링크, 상세 사내 환경/개발 소스/리뷰 요청 원문/영수증/토큰/고객 자료 공개 금지.
- `l1-fix-workflow` 및 `l1-github`는 사용자가 예시로 든 공개 스킬명으로서 **미등록·상태 미확인 예시**로만 표시. 실제 진행·리뷰 대기·완료로 추정하거나 활성 Work 수에 합산하지 않는다.
- GitHub PRIVATE `collab/dashboard/work_tracker.py`는 Work ID별 상태를 읽어 PRIVATE HTML/상태 JSON/VIEW를 갱신한다. 여기서 PUBLIC으로 자동 동기화하는 쓰기 권한/토큰/Actions는 추가하지 않는다.
- `phase`, `self_test`, `independent_review`의 문서 기재는 자기 신고 수준이고, REVIEW/RECEIPT 무결성 검증 또는 실제 실행 완료를 뜻하지 않는다. 공개 단계 막대는 완료율이 아닌 등록된 단계 위치다.
- PAGES 배포는 PUBLIC HTML 커밋 시 GitHub Pages가 자동 실행. `PAGES_AUTO_DEPLOY=PASS`와 `PRIVATE_STATUS_AUTO_SYNC=NOT_IMPLEMENTED`는 계속 분리 판정.

## 공개 허용 필드 (2026-11-12 사용자 Pages 게시 승인 범위)

- 업무 흐름의 일반적인 **단계명·주체 역할** (GPT / GitHub 협업 관리 환경 / Windows watcher·Claude Code 업무 실행 환경).
- 전환 여부의 상위 상태 (기존 LIVE 경로 유지 / GitHub 정식 전환 전).
- 독립 리뷰 및 호스트 Stage1 실검증의 상위 상태 (`NOT_RUN`을 미실행으로 표시).
- GitHub PRIVATE 추적 파일의 **비식별 합계 수치** (프로젝트 CURRENT 3 / REQUEST 0 / REVIEW 0 / RECEIPT 0, 2026-11-12 기준). 파일 관측 수는 완료 횟수가 아니다.
- 공개 HTML 제공·배포 성공 여부 및 날짜 기준. 페이지가 스냅샷이며 PRIVATE 자동 동기화가 없다는 고지.
- 개인·조직·업무 원문이 없는 공개 가능한 일반 프로젝트 범주 요약.

## 기본 공개 금지 및 강제 차단

- PRIVATE 내부 문서 원문, 기업 반출금지 코드, 고객정보, 사내 네트워크 주소·로컬 경로, 작업 ID/리뷰 요청 ID, ZIP 원본 및 실제 SHA, GitHub PRIVATE 링크, 토큰/키/서명, 운영 DB·로그 내용, 사람 이름, 상세 피드백, 리뷰 비용·실행 정책 구체 값.
- 공개 허용 목록에 없는 정보는 안전하다고 추정하지 않는다. 새 항목은 별도 반출 판단 및 승인 후 반영.
- PRIVATE Action의 `contents:write` 범위를 PUBLIC 쓰기 권한으로 확대하거나 별도 개인 토큰을 저장하지 않는다.
- 자동 PUBLIC 동기화는 **추가 구현/권한/승인 필요**. '항상 기본 Pages'는 표시 형식의 기본값이지 무인 실무 데이터 유출 승인이 아니다.

## 공개 페이지/인계

- PUBLIC 소스: `wonhwipark/L1Work` `main/docs/cowork-dashboard/index.html`.
- **기본 바로가기:** `https://wonhwipark.github.io/L1Work/cowork-dashboard/`
- PRIVATE 내부 상세: `collab/dashboard/index.html` (GitHub 코드 파일은 브라우저 실행 아님), `collab/dashboard/VIEW.md` (GitHub Markdown).
- 새 작업 시 사용자에게 HTML Pages 링크를 먼저 제공하고 `최종 상태 확인 일자` 및 `배포 성공/미검증`을 함께 알린다.
- PUBLIC 새 게시 후 GitHub 원격 readback, Pages Actions 빌드/배포 PASS, 가능 시 실제 HTTP 200/본문 해시 확인. 실패/검증 불가면 해당 항목만 NOT_VERIFIED로 기록.
