# 독립 설계 리뷰를 위한 상황·스킬 관계
## 사용자 목적
사용자는 모바일에서 작업을 요청하고, 업무 OpenCode/로컬 Agent가 허용된 코드·기존 스킬로 실행. 설명 MD를 읽다가 절차별 MSC를 클릭해 모던 HTML에서 확대/스크롤·단계 이동하고 싶어 함.
두 실제 질문이 출발점: (A) Updater가 현재 코드 기준 UL CA 지식을 knowledge/에 직접 만들면 Workflow가 필요한가? → 필수 아님. (B) Workflow 이슈 분석 중 AS-IS/TO-BE를 만들고 Workspace에 올리면 누가 MD를 구성하는가? → Workflow 조정, Kernel Work 문서, Converter MSC 상세. 두 상황을 하나의 강제 파이프라인으로 섞지 않도록 검토 요청.

## 운영·접근 조건
- 업무용 l1-workspace의 works/는 Work·진행·분석/결정/Evidence 원본. knowledge/는 Updater가 관리할 개인 지식 영역. 그룹 l1sw-dev-knowledge는 검증된 팀 기술 정본.
- Windows Claude reviewer는 업무 L1 소스에 접근할 수 있다고 가정하지 않음. 이 패키지의 비민감 설계·관리 스킬 소스 발췌로 독립 검토. 실제 UL CA 코드/MSC/로그·고객 자료·인증정보는 포함하지 않음.
- 실행자는 업무 OpenCode 경로. skillsilent만을 필수 런타임으로 가정하지 않고 기존 direct policy gateway도 유지. Windows 리뷰가 업무 호스트 시험을 대신하지 않음.
- 같은 목적의 기존 Work L1-WORKSPACE-RAG-20261111-001을 사용. 이 리뷰는 현재 두 진입/MD/HTML 설계의 신규 1회 요청이며 기존 완료 리뷰나 별도 Guard 코드 리뷰의 재실행이 아님.

## 스킬별 책임·공통 재사용
| 스킬 | 제공하는 것 | 맡기지 않을 것 |
|---|---|---|
| Workflow | 이슈 intent/Work 선택·재개, 분석/변환 인계, docs_sync/docs_push 조정 | Updater 직접 경로의 의무 관문, knowledge 콘텐츠 직접 WRITE |
| Kernel | Work/Evidence 정본·기존 등록 API·파생 Work 문서/목차/export | 순수 Knowledge 요청마다 Work 강제 생성, knowledge 본문 재생성 |
| Code Analyzer | 코드 call/IPC·조건·source revision 근거, 기존 MSC/behavior 산출물 | 수정안 승인·그룹 게시, 표현 개선을 위한 무조건 재분석 |
| 기존 이슈 분석기 | 선택된 이슈 분석·RCA; 수정 논의 owner는 해당 기존 계약 | 완료 보고서가 있으면 반복 전체 분석을 기본 실행 |
| Converter | 입력에 근거한 MSC 원본·비교 MD·SVG/HTML 표현·manifest | source fact/승인 추론, 대상 Knowledge/Work 원장 직접 게시 |
| Updater | 직접 조사·기존 Work 지식화, 개인 지식 MD 조립/출처/링크·기존 그룹 게시 조정 | Workflow 필수 종속, Kernel/그룹 writer 우회, 별도 원장/엔진 |
| 그룹 스킬·기존 Git writer | 실제 지식 규칙·허용 writer·승인/HEAD/readback | 개인·그룹 성공 상태를 한 번에 추정 |

## 확인한 사실과 미확인
- 확인한 소스: Workflow 공개 1.6.67 및 개발 후보 1.6.70, Kernel 공개 0.7.42 및 후보 0.7.43, Converter 공개 0.2.26, Code Analyzer 공개 0.15.2, Issue Analyzer 공개 0.11.50. 정확 바이트/발췌는 03_SOURCE_EVIDENCE.md.
- Workflow docs_sync는 kernel.work_docs_export를 호출. MSC handoff는 Code Analyzer/Converter/Kernel 역할을 명시하나 계획(actual_execution=NOT_STARTED)이며 실제 실행 성공의 증거는 아님.
- Kernel은 실제 등록된 canonical MSC_VIEW Evidence를 복사한 경우 Work 루트 MSC 안내를 생성. Converter의 상세 MSC_VIEW와 구분해야 함.
- Converter 0.2.26 모던 양식: 공개 전달 및 Python 3.10/3.11 각 96 PASS·실제 renderer·합성 브라우저 QA를 확보. 이는 업무 이슈 HTML/Knowledge 링크 통합 성공이 아님.
- Updater·그룹 writer 설치 원문/API·실제 지식 폴더·독자 접근·회사 호스트 E3는 미확인. 스킬 이름/함수를 창작해 호출 가능으로 간주하지 말 것.
- 순수 Knowledge의 Work ID optional, Workflow knowledge READ_ONLY, 그룹 구조 미러링·기존 승인/CAS/readback 원칙은 기존 합의. Guard 후보의 hard enforcement·코드 독립 리뷰는 별도 미완료 흐름.

## reviewer에게 필요한 관점
단순 문서 교정/함수 diff 리뷰로 축소하지 말 것. 요청별 시작점·책임·인계 데이터·저장 대상·문서 원본/파생본·실패/복구가 일관되는지 판단.
새 공통 조정기/범용 문서 엔진을 기본 해결책으로 도입하지 말 것. 확인된 작은 연결 gap과 미확인 설치 기능을 구별하고, 필요한 공통 계약만 제안.
필수 출력: 타당한 결정과 근거, 확인된 결함/반례, 비차단 개선, 최소 수정과 필요 시 구조 대안/비용·호환성, G0 질문, 단계별 수락 조건.
