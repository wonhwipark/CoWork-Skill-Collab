# Viewer v0.5.2 MSC HTML 연계/Updater 직접 분석 HO 보강 결과 — 2026-11-24 KST

- Work: `L1-WORKSPACE-RAG-20261111-001`; 새 Work 없음.
- 사용자 관찰: 업무 Viewer에서 PlantUML 원문은 보이나 HTML 시퀀스 다이어그램 링크가 표시되지 않음.
- 핵심 불확실성: `l1-knowledge-updater`가 실제 `doc-converter`를 호출했는지, HTML/SVG 생성·Workspace 등록·Viewer 표시가 되었는지 미확인. PlantUML만으로 호출 성공/실패 단정 금지.
- 판정: `l1-fix-workflow` 강제 경유 없이 Updater 직접 분석 결과도 공통 writer/Kernel을 사용하여 같은 Work에 저장하고 Viewer에서 열람하도록 설계. 생성·저장·표시 중 실제 결손 단계 확인 후 해당 스킬/adapter만 최소 변경.
- **공개 통합 인계 r0002**: [`L1_WORKSPACE_VIEWER_V052_MSC_UPDATER_CONVERTER_COMPLETE_HANDOFF_r0002_20261124_KST.md`](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_V052_MSC_UPDATER_CONVERTER_COMPLETE_HANDOFF_r0002_20261124_KST.md), Git blob `7f5128b34e5afa14949867af74850fd246a69191`, commit `1d158956a05eff3f450af6cb4bfb5e1d268a057c`.
- **기존 Viewer ZIP 그대로 재사용**: [`l1-workspace-viewer-wiki-integrated_v0_5_2_1124.zip`](https://github.com/wonhwipark/L1Work/blob/main/l1-workspace-viewer-wiki-integrated_v0_5_2_1124.zip), 374,930 bytes, SHA-256 `15e83f136fa10ef680619602b55d74c4cd4c0c86a6cc470c1bec9cac250239ba`; 재패키징·버전업 0.
- 기존 `r0001` 완결 HO 본문 전체를 신규 r0002 뒤에 보존. 전체 계약 A01~A10/H01~H05와 Write/ACL·Read Only 게이트 승계.
- 신규 HO의 실사용 조사 순서: 실제 Updater/Converter 호출 영수증 → HTML/SVG 생성·manifest → Workspace artifact/Evidence/revision readback → Viewer read adapter/HTML 링크 → 업무 브라우저 E2E. 원인별 소유자와 최소 수정 조건 구분.
- 검증 `PASS`: 공개 HO create_file, 원격 fetch_file readback, 입력 ZIP 참조, 기존 전체 문서 포함 여부·핵심 진단 항목 확인.
- `NOT_RUN/UNKNOWN`: 업무 Linux G0, Updater 실제 Converter 호출 증거, MSC HTML/SVG 생성, 업무 Work writer/reader, Viewer 업무 브라우저 E2E, 독립 리뷰, 운영 설치. 게시 자체는 호스트 실행 트리거가 아님.
- 경계: 신규 스킬/Viewer 코드 변경·독립 리뷰 요청·모델 실행·Job/예약·LIVE·운영 설치/Write ON·그룹 Knowledge 게시 없음. 상세 제품 코드/로그/MSC를 공개 문서에 포함하지 않음.
- **NEXT_ONE_ACTION**: 업무 GPT가 공개 HO r0002와 기존 Viewer ZIP의 정확한 입력만 사용해 실제 기존 Work 1건의 Updater→Converter 호출/HTML 생성/Workspace readback/Viewer 표시를 단계별 증빙하고, 입증된 결손에 한해 허용된 최소 연결·회귀시험 수행.
