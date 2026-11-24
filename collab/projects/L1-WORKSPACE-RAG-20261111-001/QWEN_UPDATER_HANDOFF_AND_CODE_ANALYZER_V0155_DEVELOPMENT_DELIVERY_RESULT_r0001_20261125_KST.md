# Qwen 분석 품질 개선 — Updater 인계 및 Code Analyzer v0.15.5 개발 전달 결과

- 2026-11-25 KST. 기존 Work L1-WORKSPACE-RAG-20261111-001 유지. 사용자 요청: Updater 업무 GPT 인계, Code Analyzer 수정·L1Work ZIP 전달.
- 기존 [R1 GPT 판정](GPT_QWEN36_DESIGN_R1_REVIEW_DISPOSITION_r0001_20261125_KST.md) 이후 실제 원본 점검에서 구체적 code gap 확인; 정적 설계 리뷰를 신규 코드 리뷰로 승격하지 않음.

## 결과와 원본

- [완결 업무 GPT 인계](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0001_20261125_KST.md): 요청 템플릿, 설치 G0, 명시적 Analyzer/Converter 호출, 품질 게이트, 문서/MSC/Work/Viewer 연결, baseline 비교, 회신 및 v0.15.5 개발 후보의 적용 경계. 원격 본문 일치 PASS, blob 1f72560e44ee82c29b4e09f3c7a07cc18c808881.
- [신규 ZIP](https://github.com/wonhwipark/L1Work/blob/main/code-analyzer_v0_15_5_1125.zip) root, 594930 bytes / SHA-256 61099248ab0a4b2597ca8316e613f5987caaee671d735337eea1e0f70a6c2877 / Git blob 81cf9a4acc94da8f6c63c1c7bb043d66bbcaea7d. L1Work main commit 891b05ccb794d67ea7ea168d2f96e2d8444a0ec8, index blob 7f24b42291179fb3304e3ac5e696e293153f7785. 원격 base64 decode 실제 bytes/SHA-256 및 인계/색인 본문 일치 PASS.
- 원본 v0.15.4: fixed L1Work commit 9eeda1cc674b4453f6637da2a60bb12a61f8c445, ZIP blob 1c43503a2a4695400727fb3fb1cd0cb3c49f826b, 515581 B, SHA-256 11e1da15ee12e750c3652190c348a7fc8e31aa1741876e3c06bc0af3413b16af. 원본 CRC 217/217, manifest 216/216 PASS. 원본 무변경.

## 입증된 결손 및 변경

- scripts/ca_core/probe_engine.py: 기존 run_probe는 load_scope_files의 max_files 선택 목록을 callers/callees의 call_edge_probe에 전달하지 않음. 구조 파일 전수 탐색으로 budget/RN/files_analyzed와 실제 facts 불일치. 또한 line 부재/불량/endpoint 누락을 CONFIRMED로 반환하여 기존 patch_writer의 CONFIRMED 승격 경로에 들어갈 수 있음.
- v0.15.5: 선택 목록 전달·필터, source/structure 유효성 및 line 양의 정수/실제 파일 행 범위·endpoint 확인. 누락·불량은 UNCERTAIN, 탐색 제한은 partial RN/aggregate UNCERTAIN 또는 NOT_ANALYZED. probe_meta 선택 필드 추가, 기존 schema/CLI/structured evidence 유지. 구조 anchor 존재만으로 source revision 일치·실행 reachability·비동기 인과를 확인했다고 주장하지 않음. 기존 provenance/merge 게이트 유지.
- 수정 7개 기존 파일: probe_engine.py, VERSION, skillsilent/manifest.json, .skill-release.json, SKILL.md, references/live_probe.md, PACKAGE_CONTENTS.sha256. 추가 3개: tests/test_call_edge_coverage_v0155.py, RELEASE_NOTES_v0_15_5.md, VALIDATION_v0_15_5.md. 나머지 210개 payload 원본 보존.
- 신규 probe_engine SHA-256 cb5771768d33e6ba8fddae7337306e0d46e3e33461547bdcee7ce5265ed25187. 변경 함수 및 테스트 소스 SHA를 로컬 시험 코드와 대조.

## 시험·경계

| 항목 | 판정 |
|---|---|
| 실제 공개 ZIP 원본 SHA/CRC/manifest | PASS |
| Python 격리 call-edge harness | 9 PASS (양방향 budget, 기존 정상 evidence, invalid/missing/out-of-range anchor, endpoint, source/structure 부재, empty/malformed edges) |
| 신규 ZIP CRC/manifest/경로 안전/roundtrip | 220/220, 219/219 PASS |
| 원격 ZIP 실제 bytes/SHA 및 인계/색인 readback | PASS |
| 전체 원본 package 내 Python 회귀 및 실제 설치본 | NOT_RUN |
| 신규 코드 독립 리뷰 / 실제 Qwen 성능·MSC·Workspace E2E | NOT_RUN |

로컬 네트워크에서 GitHub DNS 접근 불가. connector로 실제 ZIP bytes를 확보하고 압축 해제/manifest/CRC/패키징·원격 게시 수행. Python 시험은 변경 함수 및 호환 dependency stub을 사용한 격리 harness로, 전체 패키지 실행이 아님. 기존 공개 파일의 무변경 payload와 비민감 새 변경만 게시. **개발용 공개 전달, development_not_for_deployment**, 운영 설치/배포 PASS 아님. 업무 GPT 실제 수신/실행 및 신규 Analyzer 코드의 업무 환경 효과 미확인. R1/자동 GPT claim/READY 원본 무변경, 신규 리뷰/API/Job/설치/그룹 Knowledge 변경 0.

NEXT_ONE_ACTION: 업무 GPT가 완결 HO 기준으로 실제 Updater의 G0 및 기존 호출·품질 gap만 보완하고, 신규 Analyzer는 격리 전체 회귀/호환 검증 후 유효 승인 범위에서만 설치 후보로 사용. 기존 운영본 자동 덮어쓰기 금지.
