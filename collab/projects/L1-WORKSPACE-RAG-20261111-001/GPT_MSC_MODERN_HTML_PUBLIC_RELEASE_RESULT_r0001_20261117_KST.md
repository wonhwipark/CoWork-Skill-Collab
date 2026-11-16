# MSC 모던 HTML — doc-converter v0.2.26 공개 패키지 결과

- 기준: 2026-11-17 KST / 기존 Work `L1-WORKSPACE-RAG-20261111-001`.
- 판정: **MSC_TEMPLATE_PATCH=PASS / PUBLIC_DELIVERY=PASS / REMOTE_EXACT_BYTES=PASS**.
- 사용자 요청: 최신 스킬을 기준으로 예시와 같은 모던 HTML 양식으로 변경하고 패키지 게시. 이번 범위는 doc-converter의 MSC 표현과 관련 회귀 보완. Knowledge Guard 3종의 개발 후보·차단 상태를 이 릴리스로 해제하지 않음.

## 1. 변경 내용과 역할

- 최신 공개 `doc-converter v0.2.25` ZIP을 기준으로 변경. 입력 SHA-256 `97cbdf6747b2632035a56fd0ecb792115cdd35e0a202caa3555991422544f181`, 162642 bytes. 기존 source-parent Participant 규칙·한글/대소문자 충돌 방지·SVG 내장·단계 검증을 유지.
- `scripts/msc_b_viewer.py::build_html()`: 예시 계열의 네이비 상단바·출처 카드·설명 영역·툴바·모바일 배치. 확대/축소·배율·폭 맞춤·100% 초기화·단계 선택/강조 카드·선택 단계명 유지. 기존 3인자 호출 호환.
- `msc_tool.py`: 기존 spec을 viewer에 전달. 종류/source revision·참여자·표시 메시지·설명만 사용하고 미제공 정보를 만들어 넣지 않음. type 생략/대소문자·visible=false 집계는 기존 renderer 의미와 일치.
- 확인되지 않거나 중복된 단계 위치는 이동 비활성화 및 사유 표시. 외부 자산/네트워크 의존 없이 SVG·CSS·해시 검증 스크립트를 단일 HTML에 포함.
- 기존 `msc-package` 라우트에 MSC HTML/뷰어 및 action 이름의 구체적 키워드 추가. HTML 생성은 여전히 **`--view-mode PROCEDURE_FEATURE` 명시 + 실제 SVG 렌더 성공** 조건. 기본 ISSUE 모드를 임의 전환하지 않음.
- 실제 renderer가 설치된 환경에서도 기존 '렌더러 없음' 회귀가 결정적으로 해당 분기를 시험하도록 test fixture의 PATH/renderer 환경을 격리. PARTIAL 기대를 느슨하게 바꾸지 않음.
- HTML 디자인·생성은 doc-converter. Work 산출물 export는 기존 Kernel, 개인 knowledge 문서의 링크/게시 조정은 기존 Updater·허용 writer. Kernel/Workflow/Git/Updater 코드나 Knowledge 구조는 이번에 수정하지 않음.
- 분석 문서 복귀 URL·원본 텍스트는 기존 입력에 없으므로 예시의 고정 링크/자료를 복사하지 않음. 실제 게시 경로 연결은 업무 G0/E3 대상.

## 2. 실제 시험과 근거 수준

최종 [격리 CI run 43912772886](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43912772886) **SUCCESS**.
입력 commit `bfd55efcd63b55f5eefd76be350a47d0c67c1ddd` / 후보 ZIP SHA-256 `47321d7d1c43d79d8b309d1d78a96b4bbdbbf90fbe8e613d958c7c9b73a9fe78`.

| 검증 | 실제 결과 |
|---|---|
| Python 3.10.22 전체 packaged pytest | **96 PASS**, 11.84초 |
| Python 3.11.18 전체 packaged pytest | **96 PASS**, 15.60초 |
| 실제 direct gateway → PlantUML + Graphviz → SVG → HTML | 두 Python 버전 **PASS**, 가상 6참여자/36메시지/3단계 |
| Chromium 1440×1000, 390×844, 320×800 | **PASS**: 이미지 표시, body 가로 넘침 없음, 확대·축소·폭 맞춤·초기화·단계 이동/상태 유지 |
| 실제 브라우저 JS/CSP 오류·외부 HTTP 요청 | 각 화면 **0 / 0** |
| 별도 로컬 Agent forward test | 이전 snapshot **28 PASS** + 최종 변경 표적 **13 PASS**, [원문](GPT_MSC_MODERN_HTML_FORWARD_EVALUATION_r0001_20261117_KST.md). 합성 DOM/렌더 경계이며 Windows Claude 독립 리뷰와 다름 |
| ZIP 안전·무결성 | CRC·모든 파일 SHA 원장·경로 이탈/심링크/대소문자 충돌·중첩 압축·비밀 패턴·실행 모드 **PASS** |
| 후보 → 최종 ZIP 동일성 | 파일 집합 동일. 차이는 승인 후 release 채널 메타와 이를 반영한 SHA 원장뿐. runtime/test 소스는 CI에서 검증한 bytes와 동일 |
| PUBLIC 원격 readback | main 파일의 실제 bytes가 최종 ZIP과 일치, size/SHA-256/Git blob **PASS** |

[데스크톱 실제 캡처](artifacts/msc-modern-20261117/modern_1440.png) · [모바일 실제 캡처](artifacts/msc-modern-20261117/modern_390.png) · [기계 판독 QA 결과](artifacts/msc-modern-20261117/QA_RESULT.json).
표적/전체 시험 코드: [validate_msc_modern_html_20261117.py](tests/validate_msc_modern_html_20261117.py), 버전 고정 입력은 위 CI branch의 `dev/msc-modern-viewer-20261117/`.

시험 이력도 보존: run 43911989396은 기존 fallback test의 renderer 미설치 가정으로 95 PASS/1 FAIL → fixture 보완. run 43912491792는 Python 3.10/실제 renderer PASS, Ubuntu 최신 OS와 고정 Playwright의 지원 불일치로 browser 설치 FAIL → 격리 CI를 Ubuntu 22.04로 고정. 실패를 소급 PASS로 변경하지 않음. 최종 run의 전체 경로 성공으로 판정.

## 3. 최종 산출물·게시 위치

- **PUBLIC** `wonhwipark/L1Work`, branch `main`, 루트 [doc-converter_v0_2_26_1117.zip](https://github.com/wonhwipark/L1Work/blob/main/doc-converter_v0_2_26_1117.zip).
- 실제 크기 **169204 bytes**.
- **SHA-256 `b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c`**.
- Git blob `dcdb89205ec16ab07f04866bfc514954a02f8bc4`; PUBLIC 게시 commit `8f31fab49d88751bf0c65165f5384d2d241408b3`.
- 동일 최종 ZIP의 PRIVATE 보존본: [candidates/doc-converter_v0_2_26_1117.zip](candidates/doc-converter_v0_2_26_1117.zip).
- 구버전 ZIP·고정 리뷰 입력·영수증·기존 guard 후보 삭제/덮어쓰기 없음. PUBLIC에는 최종 ZIP 한 개만 추가하며 새 HTML 샘플/회사 자료/협업 원문을 게시하지 않음.

## 4. 미실행 경계·GPT 판정

- `WINDOWS_CLAUDE_INDEPENDENT_CODE_REVIEW_THIS_PATCH=NOT_RUN`. 기존 MSC 리뷰 1회 종료 이력 유지; 새 REQUEST/READY·Windows Claude 유료 호출 없음. 로컬 forward 평가와 개발/CI 시험을 정식 Windows 리뷰로 승격하지 않음.
- 업무 OpenCode/Skill-Updater 설치·실제 업무 MSC·Workspace/그룹 writer 게시·HTML 호스팅/CSP/독자 권한·문서→HTML→MSC 실환경 E3는 **NOT_RUN/NOT_VERIFIED**.
- Knowledge Guard 패키지의 별도 QA/차단·단일 writer/권한 G0는 기존 CURRENT를 그대로 따름.
- **GPT_DISPOSITION=ACCEPT_FOR_SCOPED_PUBLIC_DELIVERY**. 이번 사용자 패키지 게시 요청과 실제 보안·호환성·전체 회귀·실제 renderer/browser 결과로 MSC 템플릿 최종 ZIP을 게시. 원격 파일 존재를 호스트 적용/Knowledge 게시 완료로 보고하지 않음.
- **다음 한 행동:** 다음 허용된 업무 실행에서 설치본 버전·SHA와 기존 writer/HTML 렌더 URL을 확인하여 실제 Workspace 문서 링크 열람 G0/E3를 이어감. 기존 분석·Job을 열람 확인 목적으로 재실행하지 않음.
