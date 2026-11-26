# GPT Source Map 독립 설계 리뷰 R1 판정 r0001 — 2026-11-27 KST

## 판정
Claude REVISE / GPT REVISE. 방향성 수용, 구현/배포/그룹 게시 승인 아님. 기존 Work 유지. 정식 리뷰 1회 완료, 재호출 없음.
- [REQUEST](../../requests/REQ-L1-SOURCE-MAP-DESIGN-R1-20261127/REQUEST.md) · [PIN](../../requests/REQ-L1-SOURCE-MAP-DESIGN-R1-20261127/SOURCE_PIN.json) · [READY](../../requests/REQ-L1-SOURCE-MAP-DESIGN-R1-20261127/READY.md) · [결과](../../reviews/REQ-L1-SOURCE-MAP-DESIGN-R1-20261127/REVIEW_RESULT_1.md) · [영수증](../../receipts/REQ-L1-SOURCE-MAP-DESIGN-R1-20261127/RECEIPT_1.md).
- ID/rev/package hash/processing key 일치, execution_status COMPLETED, receipt ok=true, watcher 0.2.35. A/main REQUEST 및 ZIP bytes 일치; 원래 ZIP 3205B SHA256 ec953eb4a92512a3e8d8d74b4f56e72fd8e91b7fddca5ef748cc30744c025eeb 및 CRC 확인. APPROVAL_SIG/READY 존재; 독립 암호학적 서명 검증 NOT_RUN. 비용 $0.29는 사용자 수신 알림 기준, receipt 자체에는 금액 없음. 리뷰어는 1개 설계 문서 전문을 읽었으며 제품 코드/실제 설치본 시험 없음.

## 지적별 판정 및 수정 요구
| ID | GPT | 반영 |
|---|---|---|
| B1 | ACCEPT_WITH_CHANGE | 생성 방법(provenance: parser/tool/LLM/manual/unknown)과 검증 상태(extracted/inferred/unknown 및 실제 원문 검증 여부)를 분리. extracted도 자동 CONFIRMED 아님. 현재 Analyzer/Updater 실제 추출 방식 G0 확인, AST 지원 가정 금지. C++ qualified name/signature/qualifiers/TU/linkage/build variant/definition anchor 구분; 충돌/간접 호출 UNKNOWN. 원본 검증 없이 격상 금지; Updater만 갱신. |
| M1 | ACCEPT_WITH_CHANGE | 동일 source/build/model/budget 고정 D0 baseline/D1 map-only/D2 procedure-only/D3 both. 독립 골드셋 최소 30개 양성 관계+10개 검증된 음성/유사 이름/빌드 변형 반례(범위 부족 시 확대/보류). pilot 목표 recall>=90%(최소 27/30), 허위 CONFIRMED 0, stale/variant 불일치 감지 100% 및 미탐색/누락 명시. 측정치는 제안 수락 기준이지 성능 보장 아님. 허위 CONFIRMED 1건이면 해당 결과 그룹 게시·확대 즉시 HOLD; 수정 후 회귀. 관계 정확도와 Recovery V2/V3 결과 별도 평가. |
| M2 | ACCEPT | 정확 심볼/메시지/module 조회 및 제한 이웃 확장 우선. Aider식 랭킹/그래프 전역 인덱스는 실제 실패와 비용/소유권/승인 입증 후 별도 결정. 특정 ctags 의존 여부는 이번 결정의 전제가 아님. |
| M3 | ACCEPT_WITH_CHANGE | 현장 실제 모델 ID/컨텍스트/출력/도구 한도 확인. 초기 실험 상한은 조회 번들 4096 tokens, 50 records, 직접 코드 탐색 20 files/step 제안(기존 더 낮은 상한 우선). 전체 작업 상한도 사전 고정, 모델 설정 확인 후 조정, 비교 중 고정; truncated/unknown 명시. |
| M4 | ACCEPT | V2/V3의 map 후보에 confidence/provenance 및 source pin 전파. map 부재는 결함/경로 부재 아님. V2 원인 규칙/V3 후보는 최신 코드 원문/정상 반례로 검증, map 밖 탐색 허용. |
| M5 | ACCEPT | 기존 7개 discovery 산출물·manifest·G6 범위·revision 대조 후 동일 snapshot 후보에 편입. 불일치 HOLD, 원문 우선 대조, 이력 보존, 단일 승인된 활성 map. 기존 writer/CAS/group preview 별도 승인. |
| M6 | ACCEPT_WITH_CHANGE | 업무 G0 병행→설계 GPT 계약/합성 fixture·UI 목업→업무 GPT 샘플 한 모듈 실측→판정·필요 개발/독립 리뷰→점진 확대→그룹 별도 승인. 설치/Job/배포 자동 승인 없음. |
| m1 | ACCEPT_WITH_CHANGE | 공개 명명 불일치 주장 자체를 확정하지 않음. 실제 업무 모델 ID/설정 확인만 수용. |
| m2 | ACCEPT_WITH_CHANGE | 단일 구조화 snapshot에서 MD/기존 HTML 표시 파생, 동일 revision/hash, 지원되는 기존 atomic publish/CAS 우선. 불가 시 staging+검증+지원된 활성 전환 또는 HOLD; 혼합 revision 표시 금지. |
| m3 | ACCEPT | Writer ACL/path, Kernel export 보존, 검색/조회/MCP/Viewer adapter 실계약 G0 미검증. 기능 부재 단정·새 엔진 선개발 금지. |

## 책임과 다음 작업
- 설계 GPT: 위 판정 반영 상세 데이터/조회 계약 및 비교 평가 설계. 관리 중인 Analyzer/Viewer/Kernel/Workflow는 실제 입증 gap만 변경. Viewer 독립 Source Map 메뉴, 초기 Markdown+검색 우선.
- 업무 GPT: 활성 Updater/Analyzer/Writer/MCP 계약, 7개 기존 산출물의 데이터·신뢰도·승인 범위 및 실제 모델 설정 확인. Updater가 생성/검증/갱신/저장/그룹 게시 전담; Recovery/Analyzer 등 소비자는 읽기 전용. 제품 소스/경로/로그 반출 금지.
- P0: B1/M1/M3 및 G6/저장 권한 확인. 기존 discovery 재실행 강제 금지. 실제 제품 시험/신규 리뷰/코드/설치/Job/업무 인계/그룹 게시 NOT_RUN. 다음 한 행동: 위 판정을 반영한 통합 설계 r0002와 업무 G0 확인 요구 작성, 별도 요청 시 R2 접수.
