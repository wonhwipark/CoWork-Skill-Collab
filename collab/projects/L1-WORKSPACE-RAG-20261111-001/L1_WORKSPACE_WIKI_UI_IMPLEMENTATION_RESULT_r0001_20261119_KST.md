# 2안 팀 위키형 UI 구현·시험·패키징 결과 r0001

- 작성: 2026-11-19 KST
- Work: L1-WORKSPACE-RAG-20261111-001
- 판정: **FRONTEND_DEMO=COMPLETE / SELF_TEST=PASS / development_not_for_deployment**
- 입력: [최신 구현 핸드오프](L1_WORKSPACE_WIKI_UI_GPT_IMPLEMENTATION_TO_BUSINESS_GPT_HANDOFF_r0001_20261119_KST.md), blob `5244482aee0a2e5b5ef019354f08d016608fa2af`. Viewer r0002/개인 Knowledge r0003/Updater 책임 r0004 추가 확인.

## 변경과 현재 상태

사용자가 확정한 2안 팀 위키형을 독자적인 HTML/CSS/JS로 구현. 모던한 밝은 독서 영역·보라색 선택 강조·본문 16px·줄간격 1.75·명확한 제목/상태·PC 3영역·모바일 본문 우선 드로어 적용. Work/Knowledge/전체 파일, Module→Feature→Scenario/Procedure, Markdown/원문/JSON, 목차/deep link/뒤로가기, 검색·빈/오류 상태·메타 패널, 합성 MSC 6/12명 확대·폭 맞춤·phase 설명 접기·복귀 지원.

13문서·인물·경로·Work ID·revision·MSC는 전부 합성. 실제 스키마/API를 확정하지 않으며 adapter는 읽기 전용 presentation DTO. 원문·제목·메타는 DOM/textContent로 처리. 일반 URL/HTML 실행 차단. 실제 MSC iframe·URL 활성화 없이 placeholder만 구현하며 기존 doc-converter 변환기를 대체하지 않음. 현장에서는 기존 renderer/링크 mapper/handler 우선 재사용.

## 실제 시험

| 범위 | 결과 | 증거 |
|---|---|---|
| Chromium 합성 브라우저 | PASS 56 / FAIL 0 | [results.json](ui/viewer-wiki-ui_v0_1_0/tests/results.json) |
| JS 문법·금지 sink·저장/외부 호출·핵심 대비 | PASS 19 / FAIL 0 | [static-results.json](ui/viewer-wiki-ui_v0_1_0/tests/static-results.json) |
| 1920/1440/1024/720/390/320 CSS px | PASS, 페이지 가로 overflow 0 | 동일 origin iframe viewport 실제 변화 |
| 단일 HTML·검색·키보드/모바일 초점 | PASS, 실제 AX·키 입력 | [TEST_REPORT.md](ui/viewer-wiki-ui_v0_1_0/TEST_REPORT.md) |
| ZIP CRC·경로·manifest·비밀 패턴 검사 | PASS | 23개 파일, manifest 22개(자기 자신 제외) |

실제 키보드에서 첫 Esc가 검색어만 지우는 동작을 발견해 dialog Esc 1회 닫기로 보완·회귀 검증. 모바일 검색 accessible name 보완. 초기 검색 결과 수 가정 오류와 열린 dialog에 따른 연쇄 초점 실패는 시험 도구 수정 후 해소. 직접 Chromium 시작의 Unix socket 환경 제한은 PASS로 계산하지 않고 지원되는 브라우저 미리보기에서 실제 시험. 200%는 720 CSS px 상당 reflow로, 브라우저 UI 확대·실기기·스크린리더 전수 검증 아님.

## 산출물·정확한 위치

정본: **GitHub PRIVATE wonhwipark/CoWork-Skill-Collab / main**

- 소스/설계/연동/시험/화면: `collab/projects/L1-WORKSPACE-RAG-20261111-001/ui/viewer-wiki-ui_v0_1_0/`
- ZIP: `collab/packages/l1-workspace-wiki-ui_v0_1_0_1119.zip` ([다운로드](../../packages/l1-workspace-wiki-ui_v0_1_0_1119.zip))
- [실행 단일 HTML](ui/viewer-wiki-ui_v0_1_0/L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html)
- [DESIGN.md](ui/viewer-wiki-ui_v0_1_0/DESIGN.md) · [업무 GPT INTEGRATION.md](ui/viewer-wiki-ui_v0_1_0/INTEGRATION.md)
- [PC](ui/viewer-wiki-ui_v0_1_0/screenshots/wiki-1440.jpg) · [390px](ui/viewer-wiki-ui_v0_1_0/screenshots/wiki-390.jpg) · [320px](ui/viewer-wiki-ui_v0_1_0/screenshots/wiki-320.jpg) · [MSC](ui/viewer-wiki-ui_v0_1_0/screenshots/msc-12.jpg)

| 파일 | bytes | SHA-256 |
|---|---:|---|
| ZIP | 267140 | `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9` |
| L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html | 65344 | `119be5e0104fbcc22d0daa89b42c418eefd8f00cdb94534a6f3518c79de4ed9d` |
| INTEGRATION.md | 7899 | `a2e2c4ecd4a8bf954a3f04238d13952141495d12794e891ef5b962d3ec48dfa3` |

원격 commit·본문·실제 bytes 검증은 후속 게시 영수증에 기록. ZIP은 개발 후보이며 PUBLIC 정식 배포·업무 호스트 배송·설치 완료가 아님.

## 미검증·보존·다음 한 행동

`LINUX_HOST_API/REVISION=NOT_VERIFIED`, `HOST_INTEGRATION/INSTALL/SHARING=NOT_RUN`, `ACTUAL_CONVERTER_MSC=NOT_RUN`, `INDEPENDENT_CODE_REVIEW=NOT_RUN`. 기존 r0002 정식 Claude 독립 설계 리뷰 ACCEPT_WITH_CHANGE 및 B1 containment/B2 파일내용 비밀 검사/B3 MSC origin 격리 BLOCKING 3건 유지. 새 REQUEST/서명/READY·유료 호출·기존 완료 리뷰 재실행 0.

기존 Work/Evidence·그룹 Knowledge·스킬·실제 Linux/Windows 서비스·운영 설정 불변. 과거 CURRENT·설계·리뷰·요청·영수증 무손실 보존. 구조·책임 변경 없으므로 공통 브리프/카탈로그 수정 불필요.

**NEXT_ONE_ACTION:** 업무 GPT가 받은 ZIP의 `viewer-wiki-ui/INTEGRATION.md`로 실제 Linux 별도 Viewer의 저장소·브랜치·revision·읽기 API·권한·renderer를 G0 대조하고 adapter/기존 UI만 최소 연결. 실제 API·writer·새 서비스는 임의 정의하지 않으며 B1~B3·E3/E4를 현장에서 검증.
