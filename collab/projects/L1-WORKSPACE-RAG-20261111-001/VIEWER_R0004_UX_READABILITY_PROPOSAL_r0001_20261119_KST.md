# L1 Workspace Viewer 가독성 개선 제안 r0001 — GPT 잠정안
- 작성: 2026-11-19 KST / 기존 Work: L1-WORKSPACE-RAG-20261111-001 / 저장소: PRIVATE wonhwipark/CoWork-Skill-Collab main.
- 기준: Viewer r0002, 개인 Knowledge r0003, Updater 책임 r0004, 기존 정식 Claude r0002 리뷰 ACCEPT_WITH_CHANGE(BLOCKING B1~B3), 사용자 제공 가독성 저하 피드백.
- 본 문서는 **실제 운영 화면 미확인 상태의 UX 잠정 제안**. 신규 r0004/UX 독립 리뷰·Linux 구현/서비스·업무망 접근 완료를 뜻하지 않음.

## 예상 문제 (합성 시안을 통한 가설, 실운영 결함 확정 아님)
1. works/knowledge/index의 원시 파일 트리만 보면 사용자가 Work 진행과 Knowledge 재사용의 구분을 직관적으로 알기 어려움.
2. 고정 3영역 Explorer/본문/File details는 긴 Markdown·표·MSC 화면 공간을 줄이고, 모바일에서 트리가 본문을 위로 밀어냄.
3. 파일명/경로와 문서 제목·요약·근거/검증 상태의 시각적 위계가 부족할 가능성.
4. 개인 후보 PREVIEW와 승인된 그룹 revision의 상태를 혼동할 가능성.
5. Markdown→MSC HTML 이동 시 현재 Work/시나리오 맥락 및 뒤로 가기 안내가 약할 가능성.

## 선택안 비교
| 안 | 설명 | 재사용 / 예상 부담 | 제안 |
|---|---|---|---|
| A | 기존 3영역/폴더 트리 유지, 글꼴·간격·표·코드 스타일만 변경 | 최대 / 최소 | 신속한 fallback |
| **B** | **업무 중심 홈 → 문서 독서 화면**. Work / 개인 Knowledge / 전체 파일 진입을 분리, 트리·정보는 접이식, 본문/MSC 공간 우선 | 기존 URL·renderer·source 재사용 / 중간 | **우선 권장** |
| C | 새 Knowledge 포털/검색 DB/인덱스 구축 | 낮음 / 높음 | 입증된 gap 전 보류 |

## B안의 구체 요구
- **초기 진입:** 상단 Work / Knowledge / 전체 파일. Work는 최근 Work와 문서, Knowledge는 Module→Feature→Scenario와 Procedure 교차 진입. 메타정보 필드/API를 미리 확정하지 않음.
- **읽기 모드:** 실제 문서 제목을 크게, 원본 경로는 보조 정보로. 제목 아래 한 줄 요약·출처/Revision/검증 상태; 본문 너비 약 880~960px, 줄간격 1.65~1.75, 목차/헤딩 링크, 표·코드 개별 가로 스크롤.
- **패널:** 좌측 전체 트리는 토글로 열기, 우측 File details는 필요할 때 문서 정보/목차로 전환. 현재 위치 breadcrumb와 파일 선택 상태 유지.
- **MSC:** 기존 doc-converter B형 HTML 그대로 큰 화면(독립 viewer)에서 열고 확대·폭맞춤·phase 탐색 재사용. Viewer가 MSC를 중복 생성하지 않음. 6명/12명 participant, 장문 phase를 시험.
- **모바일:** 390/320 폭에서 콘텐츠 먼저, 탐색은 펼치기, 페이지 전체 가로 overflow 0(표·MSC 내부 스크롤은 허용).
- **검색:** 기존 검색/renderer 먼저 REUSE, 제목·경로·문서 유형 분리. 미확인 본문 색인·새 RAG/검색 DB는 선제 구현하지 않음.
- **상태 표시:** 개인 초안/미검증과 그룹 승인 게시를 혼동하지 않도록, 확인된 경우에 한해 하나의 핵심 상태와 고정 revision 표시. 확인 불가=미확인.
- **안전:** 기존 정식 Claude 리뷰의 B1 path containment(TOCTOU), B2 내부 비밀 탐지 fail-closed, B3 MSC HTML origin/cookie 격리 **필수**. UI 개선이 이 선행 게이트를 우회하지 않음.

## 수락 시험 (현재 모두 NOT_RUN)
- UX01 초기 화면에서 Work / Knowledge / 전체파일 의미를 5초 내 구분하는 사용자 관찰.
- UX02 대표 Work→Problem/Cause/Solution→MSC HTML까지 3회 이하 주요 클릭 이동.
- UX03 1440/390/320 반응형, 제목·목차·표/코드·경로 잘림/겹침 없음.
- UX04 B형 MSC 6/12 participant 단계이동·확대·복귀 및 deep link 회귀.
- UX05 현재 Markdown/MSC/원본 링크·문서 다운로드 정책·read only/원본 SHA 불변.
- UX06 PREVIEW와 그룹 승인 revision 오표기 0; 검색의 제한자료 누출 0.
- UX07 B1~B3 및 부정 보안시험 PASS 전 동료 공유/실서비스 판정 금지.

## 수행 게이트
1. 실제 업무 Linux 웹 UI/설치 Revision·현재 URL·허용된 비민감 화면을 G0에서 확인해 합성 샘플과 구분.
2. 사용자가 불편한 항목 2~3개를 우선 확정.
3. r0004 책임·UX 신규 델타는 기존 완료된 r0002 리뷰와 별개로 정식 입력 고정/유효 승인/서명/READY가 충족될 때만 독립 리뷰 1회. 기존 리뷰 재큐잉/추가 유료 호출 금지.
4. 승인된 기존 renderer·UI에서 최소 변경을 적용해 합성 브라우저 및 실제 Linux E3를 단계적으로 검증. 공개 및 그룹 Knowledge writer는 별도 승인.

**잠정 추천: B안(독서 중심) + 기존 renderer의 최소 변경. 새 포털·DB·스키마는 보류.**