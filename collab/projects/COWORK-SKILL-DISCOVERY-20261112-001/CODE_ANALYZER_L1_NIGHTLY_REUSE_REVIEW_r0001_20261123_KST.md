# code-analyzer × L1 야간 지식 분석 — 수정 필요성 검토 결과 r0001

- 2026-11-23 KST
- Work: `COWORK-SKILL-DISCOVERY-20261112-001`; 관련 지식 Work: `L1-WORKSPACE-RAG-20261111-001`
- 요청: `l1-knowledge-updater` 업무 GPT 인계 MD 배포, `code-analyzer`의 실제 기능 검토 후 입증된 결손에 한해 수정·배포. 불필요한 코드 변경 금지.
- 판정: **CODE_ANALYZER=REUSE / NO_CHANGE**, `NEW_SKILL_ZIP=NOT_BUILT`, `NEW_SKILL_RELEASE=NOT_NEEDED`.

## 1. 현재 공개 원본

- 저장소: `wonhwipark/L1Work` branch `main`
- 파일: [code-analyzer_v0_15_4_1119.zip](https://github.com/wonhwipark/L1Work/blob/main/code-analyzer_v0_15_4_1119.zip)
- 원격 Git blob: `1c43503a2a4695400727fb3fb1cd0cb3c49f826b`
- 바이트 크기: **515,581 B**, ZIP 중앙 디렉터리 **217 entries**
- 기존 배포 검증 기록의 SHA-256: `11e1da15ee12e750c3652190c348a7fc8e31aa1741876e3c06bc0af3413b16af`
- 근거: 공개 L1Work README와 CoWork 스킬 관리 CURRENT, 실제 원격 ZIP의 base64 바이트·중앙 디렉터리·주요 compressed source 내용 정적 조회. 공개 ZIP이 업무 Linux 설치본과 동일하다고 가정하지 않음.

## 2. 구현 직접 검토

| L1 요구 | 기존 확인 지점 | 판정 |
|---|---|---|
| 범위 고정, 타깃별 사실/호출 추적 | `scripts/ca_core/probe_engine.py`, `references/scope_and_shared_store.md`, `references/scan_methods.md` | REUSE |
| Dispatch/Callback/Compile-condition·State/IPC 근거 추출 | `probe_engine.py`, `feature_analysis.py`; Probe 모듈과 범위 selector 존재 | REUSE, 정확도 실증 필요 |
| Feature ON/OFF, build, State/Event/Message, bounded context | `feature_analysis.py`, `references/feature_behavior_analysis.md` | REUSE |
| Procedure별 IPC REQ/CNF, ambiguity 보존, 자동 반복/재개 | `references/next_procedure.md`, `scripts/flow_composer.py` | REUSE |
| AS-IS MSC·근거 상태·의미 표현 | `references/code_analyzer_msc_contract.md`, `scripts/flow_msc_render.py` 및 기존 PlantUML 정책 | REUSE; B형 HTML 호환은 Converter G0 |
| Source revision·발췌 무결성 | `scripts/ca_core/pec_hop_excerpt_readonly.py`, 기존 provenance/validator | REUSE; 호스트 source 권한은 별도 |
| 기존 Work/Knowledge 보존·발행 | Updater + Workflow/Kernel/기존 writer 책임 | Analyzer 수정 대상 아님 |

**정적 코드에서 확인한 한계:** probe는 일부 정규식 및 bounded source 탐색을 활용하고, 완전한 C++ AST/동적 실행 엔진은 아님. 현재 근거만으로 실제 NR/LTE의 특정 비동기·매크로·템플릿 경로를 잘못 분석했다고 단정할 수 없음. 기능 부족이라는 증거 없이 새 AST/GraphDB나 기존 인터페이스 변경을 추가하면 중복 비용·회귀 위험만 증가. 따라서 이번에는 소스 변경을 하지 않음.

## 3. 1번 인계 실행 결과

- 공개 업무 GPT 인계 MD: [L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md)
- 게시 위치: `wonhwipark/L1Work`/`main`/`handoffs/`
- 인계 범위: 설치본 G0 → 기존 코드 사실 및 지식 재사용 → NR L1 Tx UL Tx Switching 대표 1건 → 신뢰 근거·MSC 검증 → 개인 `l1-workspace` Work 저장/readback → 야간 실행 준비 판정. 기존 215행은 검토 후보이며 일괄 실행 금지.
- GitHub 신규 문서·README 색인 게시/readback과 업무 GPT 수신·Linux 실행을 구분한다.

## 4. 시험·권한·결론

| 구분 | 결과 |
|---|---|
| 공개 ZIP 217개 멤버·주요 파일 정적 내용 검토 | PASS (정적 조회) |
| 새 코드 변경·신규 패키징 | NOT_NEEDED / NOT_RUN |
| 신규 코드 자체/회귀시험 | NOT_RUN (수정 없음) |
| Windows 독립 리뷰 | NOT_RUN (신규 변경 없음) |
| 실제 Linux 설치 버전/G0 | NOT_VERIFIED |
| 실제 L1 Tx 코드 정확도/MSC/Writer E2E | NOT_RUN |
| 야간 Job·cron/systemd 예약/그룹 Knowledge 게시 | NOT_RUN |
| 신규 PUBLIC code-analyzer ZIP 게시 | NOT_NEEDED |

**다음 한 동작:** 업무 GPT가 위 인계서대로 기존 설치본의 NR L1 Tx UL Tx Switching 1건을 먼저 검증하고, 실패 분기/근거·입출력 계약을 기존 업무 Work에 보존. 이후 재현 가능한 분석 누락/오탐이 있으면 해당 함수와 최소 반례만 기준으로 `code-analyzer` 변경을 재평가. 형식적인 버전 올림 또는 강제 신기능 구현 금지.
