# LTE/NR L1 Source Map 약 1,500파일 설계 및 R2 리뷰 판정

2026-11-27 KST · L1-WORKSPACE-RAG-20261111-001 · REQ-L1-SOURCE-MAP-DESIGN-R2-20261127

**판정**　R2 Windows Claude Code 정적 독립 리뷰 1회 완료. BLOCKING 0, MAJOR 4, MINOR 2. GPT는 r0002에 보완이 필요하다는 결론을 수용하고, 수정 및 자체 검증을 마친 업무 GPT용 r0003을 설계 전달본으로 확정했어요. 추가 독립 리뷰는 최신 지시에 따라 생략해요. 실제 업무 G0·성능 검증과 운영 적용은 미실행이에요.

| 피드백 | GPT 판정 및 반영 | 확인 |
|---|---|---|
| M1 관계 형식 예시 | 수용. contains/include/declares/defines/calls, send/receive/payload, 등록·dispatch·콜백, read/write·knowledge_ref의 방향·근거·검증 명제를 r0003 §5.1에 명시 | 형식 레코드 15개, 고유 관계 14종. YAML 파싱과 양 끝·evidence·snapshot 참조 확인 |
| M2 변경 반례 | 수용. 합성 등록 키 변경, tombstone·역참조 철회·stale 전이, CAS 실패·응답 유실·reader의 snapshot 고정을 §5.2에 보완 | GCC 헤더 역의존 A/B 비교·이름 변경, 두 빌드 전후 구문, SQLite 충돌/고정 reader 모형 확인. 업무 Writer 동시성은 G03 |
| M3 해시 식별 | 수정 수용. 사용자 첨부 원본(487c4a6c…)·R2에 실린 MD·입력 ZIP을 별도로 명명. r0003 자체 해시는 아래에 외부 기록 | 원본 bytes의 SHA-256을 직접 대조 |
| M4 시험 근거 | 수용. 개발자 Linux 시험, Windows 문서 리뷰, 업무 호스트의 G0 검증을 분리. G0에 실행 명령·환경·허용된 로그와 SHA 회신 칸을 추가 | 개발자 로그·합성 fixture·재현절차·개별 checksum 22항목 묶음을 사용자에게 제공. 실제 G0 증빙은 대기 |
| m1 / m2 | 수용. table/switch는 dispatches의 pattern으로 구분하고 등록은 별도 근거 필요. 외부 자료를 확인한 주체와 정적 리뷰 한계를 표시 | r0003 §2·3·7·10 |

**확정 구성**　허용된 전체 파일을 경량 인덱싱하고 기존 Discovery 7건과 대조해요. 대표 모듈·build별 직접 호출·IPC·guard를 우선 검증하고, 저사양 LLM은 한 질문의 exact + 1-hop만 읽은 뒤 필요한 원문을 확인해요. Aider의 제한 문맥 개념, CodeQL의 사실·관계 질의 개념을 참고해요. 로컬 LLVM 계열은 기존 probe의 식별 결손과 도구 승인 확인 후 선택적으로 비교해요. 신규 엔진·제품 코드 또는 운영 변경은 전달 범위 밖이에요.

**실제 시험**　Analyzer 개발본 85/85, Viewer 8/8 Node 프로그램, GCC 4/4, 합성 1,500파일의 범위 제한 테스트 통과. dispatch가 등록 위치 대신 호출 인자 쌍을 반환하거나 field가 실제 쓰기를 놓친 합성 사례도 확인했어요. 제품 코드 전체 색인·Qwen D3−D2·업무 권한·그룹 반영은 미실행이에요.

**입력·결과 대조**　request rev 1, A e4f82504d509333863c6d6129f28bf2b14b31941, PIN B 5330aa00a4ba453dd0220696d3513ad04be6df19. 공개 원격 A/B의 REQUEST·ZIP 원본 바이트, PIN, repo ID 문자열 및 표준 pre-READY checker PASS. APPROVAL payload/READY의 입력 hash, dispatch·result·receipt의 ID/rev/package SHA/processing key 일치. 결과 execution_status COMPLETED, receipt ok=true, watcher 0.2.35. 독자적인 공개키 서명 검증이나 비용 측정은 수행하지 않았어요.

| 파일 | SHA-256 |
|---|---|
| R2 리뷰 입력 ZIP, 14,106 B | 138af88da296a738d48f86636724f71ec72f3c9c84d2d7fd900a652eb4ed38db |
| R2에서 읽은 업무 GPT 인계서 r0002 | 909447e4ec91cf4d8567e89d66076eb5c9b8dc48e4dcf7844ed7dfd54ac62a55 |
| 최종 L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0003_20261127_KST.md, 45,813 B | 5d85c228426fc9fcfc3d4c67d8cbe3e2750f85e842d0b3644a681a8c07eee968 |
| 개발자 증거 L1_SOURCE_MAP_1500_VALIDATION_EVIDENCE_20261127_KST.zip, 10,721 B | c4f938fe0df840eebf07b6e38770994428f8712bb8881f56e62a0d24a6e0e1a9 |

[REQUEST](../../requests/REQ-L1-SOURCE-MAP-DESIGN-R2-20261127/REQUEST.md) · [PIN](../../requests/REQ-L1-SOURCE-MAP-DESIGN-R2-20261127/SOURCE_PIN.json) · [리뷰 결과](../../reviews/REQ-L1-SOURCE-MAP-DESIGN-R2-20261127/REVIEW_RESULT_1.md) · [영수증](../../receipts/REQ-L1-SOURCE-MAP-DESIGN-R2-20261127/RECEIPT_1.md)

**다음**　업무 GPT가 r0003 §3과 §8로 기존 Discovery 7건의 source/build·근거·재사용/누락을 먼저 회신해요. L1Work/handoffs 게시와 업무 적용 상태는 별도로 관리해요.
