# MSC 현대화 로컬 forward 평가

## 현재 상태

- 로컬 생성·함수·JavaScript·package 통합 확인: **PASS 28 / FAIL 0**.
- 실제 PlantUML 렌더러 E2E: **NOT_RUN**. 로컬 gateway는 `RENDERER_MISSING`, exit 7, package `BLOCKED`를 명시적으로 반환했다.
- 실제 브라우저·모바일 배치·스크린샷·다운로드 실행: **NOT_RUN**. Chromium이 시작 전에 `socket() failed: Operation not permitted`로 종료됐다.
- 기존 pytest 회귀군: **NOT_RUN**. 런타임에 pytest가 없어, 별도의 직접 함수·생성물 확인만 실행했다.
- Windows Claude 독립 리뷰를 대신하지 않는 로컬 forward test다. 원격 게시·호스트 설치·새 모델 호출을 수행하지 않았다.

## 입력과 범위

- 평가 소스: `/workspace/projects/msc-modern-20261117/doc-converter`.
- 참고 파일: `/workspace/scratch/0f50b4a8562e/msc_html_check/sample_viewer.html`.
- 참고 예시의 가상 SVG를 별도 fixture로 추출하고, 동일한 6개 참여자·36개 메시지·3개 단계를 semantic JSON으로 구성했다. 실제 제품 코드·분석 근거가 아니다.
- source 소스는 수정하지 않았다. 개발 작업자가 반영한 변경은 최신 바이트 해시로 구분했다.

## 실제 확인

| 구분 | 결과 | 근거 |
|---|---|---|
| semantic JSON validation | PASS, 참여자 6·표시 메시지 36 | `forward_results.json` |
| 기존 `build_html(svg,title,phases)` 3인자 호출 | PASS | `legacy_3arg.html`, `static_results.json` |
| context의 revision·종류·개수·흐름 설명 | PASS | `modern.html` |
| 단계 좌표 | PASS, 요청 3·활성 3·비활성 0 | `forward_results.json` |
| 단계명 누락·중복 | PASS, disabled와 사유 표시 | `static_results.json` |
| 임의 제목·설명·revision escape | PASS | `static_results.json` |
| 내장 SVG 원본 bytes 보존 | PASS | `static_results.json` |
| image/download의 동일 data URL | PASS, 실제 다운로드 실행은 NOT_RUN | `static_results.json` |
| 내장 JS와 CSP 해시 일치 | PASS | `static_results.json` |
| 키보드 포커스·ARIA region·반응형 CSS·reduced motion 선언 | PASS, 실제 배치는 NOT_RUN | `static_results.json` |
| 확대·스크롤 비율·폭 맞춤·단계 선택·20–300% 제한 | 합성 DOM에서 PASS 9, 실제 브라우저는 NOT_RUN | `js_event_results.json` |
| `PROCEDURE_FEATURE` payload → HTML/manifest/MSC_VIEW 연결 | 합성 렌더 경계에서 PASS | `integration_results.json` |
| 기존 view_mode 생략 → ISSUE 유지·HTML 미생성 | 합성 렌더 경계에서 PASS | `integration_results.json` |
| CLI view_mode override → HTML 생성 | 합성 렌더 경계에서 PASS | `integration_results.json` |
| 실제 gateway + 렌더러 미설치 | exit 7 BLOCKED/RENDERER_MISSING | `current_procedure_feature.stdout.json` |
| 기존 gateway + `--allow-unrendered` | exit 0 PARTIAL/ISSUE | `legacy_default_issue.stdout.json` |

`integration_*` 폴더의 `READY`는 렌더 경계에 **SYNTHETIC_SVG_FIXTURE**를 주입한 통합 시험 결과다. 실제 PlantUML 렌더·배포 준비 판정으로 사용하면 안 된다.

## 발견 사항과 현재 판정

1. 최초 route에서 `msc-package`/`PROCEDURE_FEATURE HTML` 표현이 `convert`로 연결됐다. 개발 작업자가 route 키워드를 보완한 뒤 동일 입력으로 `msc-package` ROUTED를 확인했다. 현재 해결 확인.
2. 초기 viewer는 메시지 type 생략·대문자·`visible:false` 처리에서 validator와 개수가 달랐다. 개발 작업자가 수정한 viewer에서 표시 메시지 2개가 validator와 일치했다. 현재 해결 확인.
3. 공개 예시의 텍스트 원본 보기·내려받기, 분석 문서 복귀 링크는 새 HTML에 없다. 독립 파일에 원본 SVG를 담고 내려받는 기본 용도는 충족하지만, 이 두 기능까지 같은 경험을 기대한다면 후속 범위로 명시해야 한다. 현재 소스 계약상 필수 gate로 단정하지 않았다.
4. 단계 이동 직후 상태줄에는 단계명과 배율이 표시되지만, 배율을 바꾸면 `배율 120%`처럼 단계명이 사라진다. 선택 dropdown과 카드 강조는 유지된다. 공개 예시에서는 상태줄의 단계명도 유지되므로 경미한 사용성 차이다(`msc_b_viewer.py`의 `applyZoom`).
5. 단계 카드는 단계별 실제 설명 대신 이동 방법을 반복한다. source explanation은 별도 흐름 설명 영역에 보존된다. 의미를 추정하거나 새로운 단계 설명을 만들지 않는 현재 동작은 안전하나, 공개 예시의 메시지 범위 설명과는 차이가 있다.

화면 색상·카드·툴바·단계 영역·모바일 CSS는 공개 예시와 같은 계열로 구성되어 있다. 최종 화면 품질·작은 화면 overflow·실제 scroll/download 동작은 격리 CI의 브라우저 실행 결과로 판정해야 한다.

## 산출물과 해시

| 파일 | SHA-256 |
|---|---|
| `modern.html` 및 `integration_procedure_feature_payload/01_AS_IS.html` | `55eb9553f3570825bbe9b5f28504828a64a5e7f6736870521b28ac7536aa5b8f` |
| `synthetic_package.json` | `c04d405c69bb51c5777118cab0b18dbb4b2cd27b6079e98e657186c11a6bd696` |
| `synthetic_sample.svg` | `95f6e469dcfb8030ae2a96ffde70a1b5e95e9a7dc144ed88326e73427414fffb` |
| 평가 시 `scripts/msc_b_viewer.py` | `ee83ba507681152fbfb691e69d8142264f1decd03340797e2d217b532f22c607` |
| 평가 시 `scripts/msc_tool.py` | `b6986d08e2b83e4800e233125df11f3601247e17cd0e5457e0a715f1a1c8504c` |

모든 평가 파일의 위치는 `/workspace/projects/msc-viewer-forward-eval/`이다. `forward_eval.py`, `static_eval.py`, `js_event_eval.js`, `integration_eval.py`로 로컬 확인을 재현할 수 있고 `browser_eval.js`는 브라우저가 허용된 환경에서 실행할 검사다.

## 다음 한 동작

격리 CI에서 실제 PlantUML을 사용해 package를 생성한 뒤 데스크톱·모바일 브라우저의 확대·단계 이동·폭 맞춤·SVG 다운로드와 화면 overflow를 검증한다. 그 결과와 별도의 Windows Claude 독립 리뷰 판정을 합쳐 전달 gate를 확정한다.

## 최종 후보 추가 확인

최종 후보 갱신 후 요청 범위인 확대·축소/선택 단계 표시와 기존 ISSUE의 렌더러 미설치 분기만 다시 확인했다. **추가 13 PASS / FAIL 0**이며, 실제 브라우저·PlantUML은 재시도하지 않았다. 앞의 28 PASS는 이전 소스 snapshot의 결과로 보존한다.

- 최종 HTML의 실제 내장 JavaScript를 합성 DOM에서 실행: **11 PASS**. 확대 120%·축소 100% 이후에도 선택 dropdown·강조 카드와 상태줄 단계명이 유지됐다. `폭에 맞춤`, 스크롤 비율, 20–300% 제한도 유지됐다.
- 기존 ISSUE 입력, 렌더 생략 미허용: **PASS**. exit 7, `BLOCKED`, `RENDERER_MISSING`, `msc_ready=false`, `render_ready=false`, HTML 미생성.
- 기존 ISSUE 입력, `--allow-unrendered`: **PASS**. exit 0, `PARTIAL`, `PUML_READY_RENDER_SKIPPED`, `msc_ready=false`, `render_ready=false`, HTML 미생성.
- 위 「발견 사항」 4번의 확대 후 상태줄 단계명 소실은 **최종 소스에서 해결 확인**했다. 확대 후 상태 예: `3 · 단계 3 · 해제 후 재설정 · 배율 120%`.

| 최종 확인 파일 | SHA-256 |
|---|---|
| `scripts/msc_b_viewer.py` | `63f24685006541e50e95cf9e7b159397554134df6d4fd6c4b9fe14e16a152cf8` |
| `scripts/msc_tool.py` | `b6986d08e2b83e4800e233125df11f3601247e17cd0e5457e0a715f1a1c8504c` |
| 최종 합성 열람본 `modern_final.html` | `813fa5e9f044bb2565f1d5a79b76cc0b027d6cc5e46e0f62b1625a3b3e3564fa` |

추가 근거는 같은 평가 폴더의 `final_recheck_results.json`, `final_js_event_results.json`, `final_issue_strict.stdout.json`, `final_issue_allow_unrendered.stdout.json`에 보존했다. `final_recheck.py`로 생성·분기를 확인하고, `js_event_eval.js modern_final.html final_js_event_results.json`에 각 파일의 절대 경로를 지정해 최종 JS 확인을 재현한다. 원본 구현 수정·원격 게시·호스트 설치는 수행하지 않았다.
