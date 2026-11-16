# MSC 개발 후보 2종 격리 회귀시험 결과 — r0001 / 2026-11-16 KST

- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 시험 범위: PRIVATE 후보 `doc-converter_v0_2_23_1116.zip`, `work-ledger-kernel_v0_7_40_1116.zip`. 기존 분석/호스트/업무 그룹 지식은 실행·수정하지 않음.
- 실행: PRIVATE의 임시 격리 브랜치 `msc-skill-validation-20261116`; 읽기 전용 CI(permissions `contents: read`), `actions/checkout` 인증 지속 없음, 사용자 데이터·Secrets·모델 호출 사용 없음.
- 실제 검증 실행 [Run 43786218200](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43786218200), commit `3611c44ce11cac52c48b2458299c2bbf3c947867`, conclusion=**success**. 선행 Run 43785991527도 Python 3.10·3.11 모두 success였으나 최신 Run을 최종 근거로 사용.
- 스킬 후보는 CI 브랜치에서 변경하지 않았으며 아래 원본 hash를 검증한 뒤 임시 경로로 추출·시험. 실제 PRIVATE main의 두 후보와 동일한 바이트.

## 실제 측정

| 구분 | Python 3.10.22 | Python 3.11.18 |
|---|---|---|
| SHA-256·전체 ZIP CRC·경로·심링크·중복 검사, 구문 컴파일 | PASS | PASS |
| 표적 검증 합계 | **19/19 PASS** | **19/19 PASS** |
| doc-converter 파일 | 88 ZIP members / 33 `.py` py_compile PASS | 동일 |
| kernel 파일 | 164 ZIP members / 68 `.py` py_compile PASS | 동일 |
| 신규 표적 테스트 | doc-converter 5개 + kernel 1개 = **6/6 PASS** | **6/6 PASS** |
| Chromium 단일 B HTML 생성·실제 스크린샷 | 해당 job에서 SKIP | **PASS** (PNG 18,649 B) |

실제 로그의 `MSC_QA_TOTAL=19 PASS=19 FAIL=0`를 Python별로 확인했으며, Python 3.11 브라우저 단계는 `BROWSER_CHROMIUM_SMOKE_PASS` 확인. screenshot은 격리 runner 내 임시 파일로 생성했으며 별도 외부 호스팅·업무 URL·PUBLIC 게시 없음. Run 상세 job IDs: Python 3.10 `133034325330`, Python 3.11 `133034324937`.

- doc-converter ZIP: 210426 B / SHA-256 `43805ae0ce1b08205125441f383f6bdfc6f114ef53bb2609295827f10b1ce23e`.
- kernel ZIP: 410922 B / SHA-256 `b8077fd717f326fb7bc556407b8e8b8a7f32a580e143ec3a6d646d3b1e9df7ce`.

## 평가 한계

- 테스트 **19/19**는 ZIP 무결성·컴파일·6개 신규 표적 단위시험 등을 포함한 **표적 검사**. 기존 모든 pytest suite, 코드/Work 통합, 커버리지 전체를 뜻하지 않음.
- kernel 신규 테스트는 현재 SVG guard 소스 계약 정적 확인이고, 실제 `WorkUX.export_docs` 내부의 등록 Evidence/게시/사이즈 초과 `KernelError` 런타임 반례는 **NOT_RUN**.
- B HTML Chromium 화면 렌더와 PNG 저장은 확인, 실제 Phase 버튼 클릭·위치 정확도, CSP 격리·호스팅 정책, 위험 SVG/크기 초과/유효하지 않은 SVG에 대한 동작은 **NOT_RUN**.
- 실제 업무용 `l1-workspace` 원장·marker·Knowledge writer/승인·`published_path`/원격 readback·역링크/E2E는 **NOT_VERIFIED**.
- Python 3.10/3.11 표적 시험은 개발자 자체시험 범주. Windows Claude Code **독립 코드 리뷰 미수행**, 리뷰 결과·영수증 미수신.
- 두 ZIP `development_not_for_deployment`. PUBLIC L1Work 최종 ZIP/Skill-Updater/운영 설치/DB/Watcher/Job/LIVE/Knowledge write 변경 없음.

## 후속 독립 리뷰의 필수 검토

1. Python 표적 PASS의 오탐 가능성: 누락된 부정·통합 사례, CLI 모드 호환, 실제 오류 전파, `MANIFEST_SHA256.json`·release metadata/버전 계약.
2. B HTML: 임의 SVG 데이터/Title·Phase XSS, XML/외부 참조, embedded image CSP, 스크롤 좌표·유일 라벨, 파일 크기 제한, 렌더 실패 폴백, 실제 URL을 열람 링크로 과장하지 않기.
3. Kernel: 등록된 Evidence `.svg`만 복사·상한 초과 실패 경계, 기존 `published_path` 및 파일명 변경 매핑, 링크 고아 처리/중복/충돌/부분 실패.
4. Workflow/Analyzer 기존 후보는 신규 수정하지 않았으므로 실제 구간 책임 이탈·재분석 없는 연결만 확인. Updater/그룹 writer 미접근은 명시.

**NEXT_ONE_ACTION:** 위 실제 시험 근거와 PIN한 두 수정 ZIP으로 Windows Claude Code에게 **개발 세션과 별도인 독립 소스·패치 비판 리뷰** 요청; 확인된 결함이 있으면 GPT가 동일 Work에서 수정·재시험. 이 문서 자체로 reviewer 실행·승인/READY·유료 호출 시작하지 않음.
