# Agent/MCP 확인 기능·Viewer 변경서 PUBLIC 전달 결과

- Work: L1-WORKSPACE-RAG-20261111-001 / 2026-11-20 KST
- 사용자 지시: 업무 GPT 직접 동작 확인이 불가능하므로 Agent/MCP가 답할 읽기 진단 확장 요청 HO와 Viewer 변경서 업로드
- 범위: 비민감 설계·인계·합성 HTML PUBLIC 배송. 실제 MCP/Viewer 호스트 구현·설치·활성·운영 시험은 NOT_RUN
- 저장소: wonhwipark/L1Work / branch main / MD·HTML 모두 handoffs/

| 파일 | bytes | SHA-256 | 생성 commit |
|---|---:|---|---|
| [L1_Workspace_Wiki_Usability_Preview_20261120_KST.html](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_Workspace_Wiki_Usability_Preview_20261120_KST.html) | 69919 | 7c9ab930bedf0f2cf59834c66d3598a920a95d9215993788b9ca80f125de237c | be6481e1261a83c78e4ab43784b4fa58357bcfe2 |
| [L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md) | 10473 | 9193df9bdf2f9eeb19766fe88171c9000e232a8ab6b10c1629d14d8cd08b7908 | 5146e3b56d8b0cfa61d4a8e42c1efdb5465246d4 |
| [L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md) | 9878 | 8f978f0828f9d3a8871caec0f1b3242541156a6a521664cbe9a51367335645c6 | 924857ec6c10e2e56bde68f109c24bedc06a65b0 |

검증: 각 원격 UTF-8 본문이 전달 원본과 일치. 원격 문자열의 실제 UTF-8 바이트로 SHA-256/크기/Git blob을 계산하여 원격 blob 일치 PASS. PUBLIC ZIP 기존 버전은 교체하지 않음.

연결: L1Work handoffs/README.md 최상단에 새 묶음을 추가하고 기존 11/19 UI 인계서 상단에 새 변경서/MCP 요청서와 UX 완료 상태를 표시. 이전 문서 본문과 이력 보존.

MCP 요청 내용: 실제 대상 호스트 식별, 설치 vs 로드 구분, Viewer API/기존 문서·MSC·Work/Knowledge 연결의 읽기 진단, stale/부분 실패/미실행 구분, 모바일 기본 요약과 숫자 판정, 최소 노출/기존 승인 응답 범위, 실제 MCP→Agent 연결 시험. 임의 shell/경로/URL·Job 재실행·분석/변환/게시·새 외부 수신 파이프라인 제외.

Viewer 요청 내용: 기존 v0.1.0 ZIP과 별도 개선 HTML 구분, P1 두 건·읽기 맥락 유지·I-01~I-07 실제 연결 변경·원본 불변·B1~B3/E3~E4·rollback. UI 정식 소스/패키지·리뷰 입력은 불변.

기존 MCP 피드백 SPEC_ONLY 문서의 외부 전송 도구를 설치된 진단 기능으로 간주하지 않음. 업무용 인계에 CoWork PRIVATE 서비스·경로·인증 의존성을 주입하지 않음.

다음 한 행동: 사용자가 업무 GPT에 새 두 인계서를 전달. 업무 GPT는 허용된 현장 Agent로 실제 대상/기존 기능을 대조하고 최소 진단 확장의 개발·시험·패키징 및 MCP→Agent 응답을 진행. 설치·활성은 실제 유효 권한 범위에서 별도 판정. 현장 원문/상세 로그/코드/MSC의 반출을 요구하지 않음.
