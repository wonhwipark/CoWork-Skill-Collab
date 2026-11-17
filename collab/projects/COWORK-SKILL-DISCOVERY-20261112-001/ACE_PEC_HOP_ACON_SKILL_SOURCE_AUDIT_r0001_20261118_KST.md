# ACE × PEC-HOP × ACON — 개별 스킬 원본 확인 및 설계 영향 감사 r0001

- 작성: GPT / 2026-11-18 KST
- 기존 Work: COWORK-SKILL-DISCOVERY-20261112-001, 연계 L1-WORKSPACE-RAG-20261111-001
- 정본: PRIVATE wonhwipark/CoWork-Skill-Collab, branch main
- 목표: 범위 내 개별 스킬 실제 최신 접근 가능 ZIP의 SKILL.md를 읽고 설계 책임 및 변경 금지 경계를 결정
- 성격: 원본 정적 검토. 운영 설치·실제 업무 실행·별도 독립 리뷰·그룹 Knowledge 쓰기 검증 아님.

## 1. 원본 선정과 최신성

PUBLIC wonhwipark/L1Work/main: 비교 기준 commit 33d959f3376a495875eed59b79b292c0f8f9cfe0에서 최신 확인 commit 670e743e85e148661e4c4e2caf2929eb309a8af5까지 비교 결과 새 스킬 ZIP은 doc-converter_v0_2_26_1117.zip 1개. 각 항목의 실제 GitHub ZIP 바이트를 가져와 ZIP 중앙 디렉터리를 확인하고 SKILL.md를 DEFLATE로 풀어 확인했다.

| 스킬 | 이번에 읽은 ZIP / 저장소·ref | 실제 바이트 | Git blob | 판정 |
|---|---|---:|---|---|
| l1-fix-workflow | PRIVATE dev/l1-knowledge-guards-20261117, v1_6_70_1117 | 758119 | 12ada6bd080498edfe74809e55d76bee381ef1c0 | 개발 후보, PUBLIC 아님 |
| l1-github | PRIVATE dev/l1-knowledge-guards-20261117, v0_3_59_1117 | 567266 | cbbf5bf4df637e5e534928fc874abfee9419d361 | 개발 후보, PUBLIC 아님 |
| work-ledger-kernel | PRIVATE dev/l1-knowledge-guards-20261117, v0_7_43_1117 | 319792 | 778d505d0d9ebeb4c9a68c8bcd2f70432f79a048 | 개발 후보, PUBLIC 아님 |
| code-analyzer | PUBLIC L1Work/main, v0_15_2_1107 | 513811 | 6017f81f51e9747286825648599fc13770cb8903 | 접근 가능한 공개 원본 |
| issue-analyzer | PUBLIC L1Work/main, v0_11_50_1102 | 440609 | f830b6bb561c0c3c1ac11ffd63625ccbf2fdfc13 | 접근 가능한 공개 원본 |
| doc-converter | PUBLIC L1Work/main, v0_2_26_1117 | 169204 | dcdb89205ec16ab07f04866bfc514954a02f8bc4 | 접근 가능한 공개 원본 |
| p4-code-owner | PUBLIC L1Work/main, v0_6_7_1012 | 106017 | ee5801e2d8021a54d224f18d321002a3f1742716 | 접근 가능한 공개 원본 |
| hld-composer | PUBLIC L1Work/main, v0_4_32_1008 | 267227 | da0d969c0ce83b0244e87274d700a4fa136773d3 | 접근 가능한 공개 원본 |

PUBLIC 기준 비교 commit 이후 새로운 코드분석 후보가 있다는 과거 보고만으로 실제 설치/게시된 최신 버전이라고 확정하지 않는다. 기존 카탈로그에 언급된 PRIVATE code-analyzer 0.15.3은 이번에 설치 원본/정확한 ZIP을 확보하지 못해 이번 표의 직접 읽은 원본에 포함하지 않았다.

- 개발 후보 자체 릴리스 메타데이터의 channel=development_not_for_deployment 확인.
- 기존 검증 보고에 기록된 SHA-256: Workflow v1.6.70 c9187ee6f8d0cdba8fe3fdae0f072f6c16d83323083b798d30937d7692999017, GitHub v0.3.59 6351b96bcb984f6388fd195cc579a60fa809fac6e14caab0c0c860e2d30b7cf6, Kernel v0.7.43 0efb8a83b5bb219ffe1f53c04fe6a179b9359cb5ce0c96fe302b56ffc78146e3. 보고서 값이며 이번 독립 SHA256 재계산과 구분.
- 공개 doc-converter 0.2.26의 기존 실측 SHA-256: b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c.
- 관련 정본: [L1 Knowledge CURRENT](../L1-WORKSPACE-RAG-20261111-001/CURRENT.md), [기존 3종 후보 릴리스 게이트](../L1-WORKSPACE-RAG-20261111-001/GPT_KNOWLEDGE_GUARDS_CANDIDATE_QA_PUBLIC_GATE_r0001_20261117_KST.md), [품질 시험](../L1-WORKSPACE-RAG-20261111-001/GPT_SKILL_RELEASE_QUALITY_AND_MSC_CONTRACT_FIX_RESULT_r0001_20261117_KST.md).

## 2. SKILL.md 직접 검토 결과와 연결 설계

| 스킬 | 이미 존재하는 기능·계약 | 이번 설계에서의 판정 | 변경 금지 또는 미확인 |
|---|---|---|---|
| l1-fix-workflow 1.6.70 | 기존 Work 재개, read-only plan/resume, 결정/Checkpoint, 그룹 조회·동일 분석 재사용, knowledge/ changed-path 거부 | ACE용 요청 범위 선택·Work 연속성 = REUSE. 기존 Work 문맥에 연결할 검증 교훈 선택은 CONNECT 후보 | MCP read-only와 인증된 writer 구분, knowledge/ 직접 write 금지. 이미 커밋된 보호 diff 우회 미검증 |
| work-ledger-kernel 0.7.43 | Work ID, append-only 결정 및 Evidence, source/revision guard, exporter, 개인 knowledge/ 파일 보존 | ACE의 원본/결정 SSOT = REUSE. 새 memory/profile/record 필요 없음 | 기존 schema·profile·인증/승인·Evidence 수정 금지, exporter가 Knowledge 최종 writer가 되지 않음 |
| l1-github 0.3.59 | repo role, push/commit single-write, branch·PR 분석 근거, command journal, Work Docs 보호 | source commit/ref pin 및 authorized writer 검증 = REUSE/CONNECT | 상태의 staged/unstaged/untracked 검사만으로 이미 commit된 diff나 raw git 우회 차단 보증 금지 |
| code-analyzer 0.15.2 | source scoped CODE FACT, expected flow, Git 증분 분석, procedure provenance, local shared Fact 경로 | PEC-HOP 근거 추출 = REUSE. 자료 묶음 view만 CONNECT 고려 | 설치원본 및 추가 후보 미확인. HLD/MSC를 CODE FACT로 승격 금지, source revision 다르면 stale |
| issue-analyzer 0.11.50 | 역사 사례 검색·기본 도메인 지식 선조회·증상/원인 분리·실제 로그근거·Code Analyzer 보강 | PEC-HOP의 증상→원인→해결 근거 연결 재사용 | 과거 사례/도메인 기대 흐름 자체는 이번 이슈 root cause 증거 아님. 직접 Git push 금지 |
| doc-converter 0.2.26 | SOURCE_PARENT_DIR_V1, stack_group, scenario_trace, MSC B HTML+SVG, 검증/manifest | 근거 계보·표현 = REUSE, 근거 발췌 패킷에서 읽기만. HTML은 시각화 | CODE FACT 승인/Knowledge 쓰기/호스트 설치/HTML URL 제공 추론 금지 |
| p4-code-owner 0.6.7 | Mango MCP만 이용하는 P4 read-only CL·실제 modifier와 integration 구별 | P4 출처 고정, CL 계보 증거 = REUSE | P4 CLI 직접 접근 금지, CL 후보=확정 원인/모듈 Owner 아님 |
| hld-composer 0.4.32 | HLD 결정 ledger, bounded packet, provenance, source map, 단계별 재개 | HLD 관련 PEC-HOP 패킷 생성에 기존 trace·상태 재사용 | context-only Issue와 Code Fact 혼합 금지; 디자인 수락=구현/시험 PASS 아님 |
| l1-knowledge-updater | 업무 GPT 관리 스킬, 공개 원본 없음 | 설계 적용 제안서만 작성; G0 설치본/그룹 writer API 대조 요청 | 실제 코드 변경·설치·그룹 write 제안서로 시작 금지 |
| CoWork reviewer watcher | v0.2.26 개발 후보와 v0.2.25 조건부 설치 작업이 별개 | 리뷰 운송/승인 정책은 현행 그대로 REUSE | 새 REQUEST/READY를 사전 정책검증 없이 게시 금지, 기존 UNCERTAIN 자동 재실행 금지 |

## 3. 독립적 한계와 확인 수준

- 직접 확인: 위 8개 ZIP의 실제 GitHub blob, ZIP 목록, SKILL.md 압축 해제·기능/안전 계약 읽기.
- 별도 실제 기능 실행/호스트 설치/업무 Knowledge G0/E3: NOT_RUN.
- 공개 source와 개발 후보 혼동 금지. 이 감사가 PUBLIC release gate, Windows 보호 승인, 그룹 writer 권한 증빙을 대체하지 않음.
- 본문은 비민감 역할/인터페이스만 보존. 회사 코드·로그·상세 MSC·개인키·토큰 및 미승인 파생 정보는 포함하지 않음.

## 4. 설계 전 판정

1. ACE는 기존 CONTEXT_BRIEF→CURRENT→결정/Work/Evidence에 연결. 별도 지식 메모리 스킬 및 저장 스키마 신설 불필요.
2. PEC-HOP은 기존 CODE FACT/CL·PR/원문 해시·위치의 검증된 서브셋만 전달하는 파생 view로 제안. 원본 문서 변경 불필요.
3. ACON은 실제 실패를 재현하고 보존된 원본과 대조하는 시험 지침으로 한정. 자동 훈련·원격 호출·상시 압축 엔진 신설 금지.
4. Updater는 업무 환경의 실제 설치 원문·기존 reader/writer/Preview/승인 경계를 대조한 뒤 REUSE/CONNECT/검증된 GAP만 판정.

NEXT_ONE_ACTION: 본 근거에 근거한 통합 설계안과 Updater 설계 적용 제안서를 비민감 정본으로 게시하고, 독립 설계 리뷰는 Windows LIVE 정책 select/check 사전 PASS가 확인된 범위에서만 정식 요청으로 승격.
