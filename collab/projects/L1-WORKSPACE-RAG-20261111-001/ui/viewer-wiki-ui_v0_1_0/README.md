# L1 Workspace · 팀 위키형 UI v0.1.0

2026-11-19 KST · **독립 합성 데모 완성 / development_not_for_deployment**

여러 담당자가 함께 읽는 문서를 위해 본문 16px, 선명한 제목과 상태, 밝은 회색 탐색 영역과 보라색 선택 강조를 적용한 HTML/CSS/JavaScript UI예요. 빌드·CDN·프레임워크·DB가 필요하지 않아요.

## 바로 확인

- `index.html`: 브라우저로 열어 탐색하는 다중 파일 버전. 합성 데이터만 포함.
- `L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html`: 같은 코드를 묶은 단일 파일 버전. 다운로드 후 브라우저에서 바로 열 수 있어요.
- `DESIGN.md`: 화면·상태·렌더·보안 경계.
- `INTEGRATION.md`: 업무 GPT의 기존 Linux Viewer 연동 지시와 매핑표.
- `TEST_REPORT.md`, `tests/results.json`: 실제 합성 Chromium 시험.
- `screenshots/`: PC·모바일·MSC 화면 증거.
- `manifest.sha256`: 패키지 구성 파일별 해시. 이 파일 자체는 목록에서 제외.

Work / Knowledge / 전체 파일 탭, 계층 탐색, fixture 검색, Markdown·원문 보기, 목차·직접 링크·뒤로가기, 메타 패널, 모바일 드로어, 합성 MSC 6/12명 확대·폭 맞춤·접기를 지원해요. 검색은 fixture 13개 문서에 한정돼요.

`tests/harness.html`은 합성 데모 전용 브라우저 시험 도구예요. `index.html`과 함께 동일 origin의 기존 정적 미리보기에서 열고 **전체 시험 실행**을 누르면 56개 검사를 재현할 수 있어요. 실제 업무 데이터를 연결한 서비스에 tests/·fixtures/를 노출하지 마세요.

## 현재 판정

| 항목 | 상태 |
|---|---|
| UI 구현·합성 브라우저 시험 | PASS |
| 원본 Work·Evidence·Knowledge 쓰기 | 구현 없음 |
| 실제 API·인증·Linux 통합 | NOT_VERIFIED / NOT_RUN |
| 실제 doc-converter MSC 원본 연동 | NOT_RUN, placeholder만 제공 |
| B1 containment / B2 비밀 검사 / B3 HTML origin 격리 | 실제 호스트에서 미해결 BLOCKING 유지 |
| 신규 독립 코드 리뷰 | NOT_RUN |
| 호스트 설치·서비스 재시작·동료 공유 | NOT_RUN |

다음 한 동작: 업무 GPT가 `INTEGRATION.md`로 실제 서비스의 읽기 계약을 확인한 후, adapter 매핑과 기존 renderer 이식만 좁게 수행해요.
