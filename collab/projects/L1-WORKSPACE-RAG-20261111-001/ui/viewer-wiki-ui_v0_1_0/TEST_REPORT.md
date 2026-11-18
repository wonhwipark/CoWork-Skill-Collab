# UI 구현·시험 결과 · v0.1.0

2026-11-19 KST · 개발 세션 자체시험 · **INDEPENDENT_REVIEW=NOT_RUN**

## 최종 판정

| 범위 | 결과 | 실제 근거 |
|---|---|---|
| 합성 Chromium 브라우저 검사 | **PASS 56 / FAIL 0** | `tests/results.json`, Chrome 156 Linux |
| JS 문법·금지 sink·외부 요청/저장 API·핵심 대비 | **PASS 19 / FAIL 0** | `tests/static-results.json` |
| 단일 HTML 렌더·검색·Esc 1회 닫기 | PASS | 실제 브라우저 AX와 키보드 입력 확인 |
| 모바일 드로어 Shift+Tab 순환·Esc 초점 복귀 | PASS | 실제 브라우저 키보드 입력, Evidence→메뉴 버튼 초점 |
| ZIP CRC·경로·파일별 SHA-256 | PASS | 재현 빌더·별도 패키지 검사, `manifest.sha256` |
| 실제 Linux 통합·API·인증·원본 파일 보호 | NOT_RUN / NOT_VERIFIED | 호스트 접근 없음 |
| 실제 doc-converter B형 HTML·6/12 participant | NOT_RUN | 화면의 MSC는 합성 placeholder |
| 동료 2계정·실사용자 5초 인지·3회 이내 탐색 관찰 | NOT_RUN | 합성 자동 시험과 구분 |
| B1 containment / B2 비밀 검사 / B3 origin 격리 | NOT_VERIFIED / BLOCKING | 기존 독립 설계 리뷰 지적 보존 |
| Firefox/Safari·실기기·스크린리더·고대비 | NOT_RUN | Chromium 프런트엔드만 시험 |

## 브라우저 시험 범위

동일 origin에 띄운 합성 앱 iframe의 CSS viewport를 1920/1440/1024/720/390/320px로 바꾸어 레이아웃을 검사했어요. 실기기 에뮬레이션이나 실제 운영 서비스의 E3/E4 시험은 아니에요. 200%는 1440px 화면의 720 CSS px 상당 reflow 시험이며 브라우저 UI 확대·OS 확대의 전체 검증이 아니에요.

Work→이슈 개요, Module→Feature→Scenario/Procedure, 전체 파일, JSON, 미지원 형식, 오류·복구, 원문/본문, H2/H3·표·코드·TOC, deep link 재열람·뒤로가기, 검색 결과/빈 상태/초점/Esc, 개인 초안/합성 게시/미확인, HTML·script·javascript/data URL·메타 악성 입력, 긴 코드·표, 모바일 패널, MSC 6/12명 확대·폭 맞춤·phase 설명 접기·복귀를 실제 브라우저에서 실행했어요.

핵심 본문·메뉴·상태 텍스트의 지정 색상 조합은 4.5:1 이상이에요. 7조합 대비 계산은 정적 값 검사이며 모든 화면·disabled·focus·OS 모드를 포함한 WCAG 인증은 아니에요.

## 발견과 보완

- 초기 시험 도구에서 `SCell` 검색이 1개라고 가정했으나 본문 교차 링크까지 검색되어 2개가 맞았어요. 유일한 제목 쿼리로 시험을 수정했어요. 그 실패 뒤 열린 dialog 때문에 초점 시험 2개가 연쇄 실패했으며, 재실행 54개 PASS로 확인했어요.
- 실제 모바일 AX에서 검색 아이콘의 이름이 사라지는 문제를 확인해 버튼에 명시적 `aria-label`을 추가했어요.
- 실제 키보드 시험에서 검색어가 있는 search input의 첫 Esc가 단어만 지우는 동작을 확인했어요. 명시적 dialog Esc 처리를 추가하고 **검색어가 있어도 Esc 1회 닫기**를 회귀 항목으로 추가했어요. 최종 56개 PASS 및 실제 키보드 재확인 완료.
- 최초 직접 Chromium 프로세스 실행은 환경의 Unix socket 제한으로 시작되지 않았어요. 해당 시도를 PASS로 계산하지 않고, 지원되는 브라우저 미리보기에서 실제 시험을 완료했어요.
- 브라우저 확장의 metadata 전달 오류 로그는 관찰됐어요. 앱 origin의 script/CSP 오류는 관찰되지 않았으며, 확장 오류를 앱 오류와 구분했어요.

## 재현과 증거

합성 코드만 동일 origin 정적 미리보기로 제공한 뒤 `tests/harness.html`에서 **전체 시험 실행**을 눌러요. 결과 JSON은 페이지 하단에 표시돼요. 일반 Python/Node가 있는 환경에서는 `python3 tests/static_check.py`로 정적 검사를 재현할 수 있어요.

| 스크린샷 | 실제 관찰 |
|---|---|
| `screenshots/wiki-1440.jpg` | 1440 CSS px PC 문서·트리·목차·메타 |
| `screenshots/wiki-390.jpg` | 390 CSS px, 본문 16px·드로어 진입 버튼 |
| `screenshots/wiki-320.jpg` | 320 CSS px 제목 줄바꿈·본문·표 내부 스크롤 |
| `screenshots/msc-12.jpg` | 넓은 MSC 화면·확대·설명 접기·원본 구분 |

스크린샷은 실제 브라우저 캡처이며 전부 합성 예시예요. 기존 Linux 업무 화면과 동일하다는 뜻은 아니에요. 시험 페이지의 외부 iframe은 QA 도구이며 앱 내부 MSC iframe은 0개예요.
