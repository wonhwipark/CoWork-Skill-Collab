# GPT 판정 — MSC 링크 스킬 4종 / Knowledge Updater 필수 G0 / PUBLIC 인계 r0001

- 기준: 2026-11-16 KST / Work `L1-WORKSPACE-RAG-20261111-001`.
- 목적: 기존 r0002 설계와 Claude Code 정적 검토 의견에 맞춰 PUBLIC ZIP 4종의 변경 필요성을 좁게 판정하고, 업무 GPT 설치본 확인 요청은 PUBLIC `L1Work/main/handoffs`로 전달.
- PUBLIC 인계: [MSC 링크 G0 READ_ONLY 인계](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_MSC_LINK_SKILL_G0_REVIEW_HANDOFF_r0001_20261116_KST.md); 원격 원문 SHA-256 `2de8f2d5a69f8691d7aad03e8e0e7b7bb5a863d4b3e43b1a4b87aea1c059bead`, 6708 bytes; 게시·원격 재조회 PASS.
- 과거 r0001 동결 설계/REQUEST/SOURCE_PIN·review ZIP, 구 r0005/MSC B 인계 및 기존 비용/승인/영수증은 변경하지 않음.

## 판정 근거와 실행 한계

- 선행 `MSC_MD_LINK_SKILL_SUPPORT_REVIEW_AND_PROPOSAL_r0001_20261115_KST.md`의 PUBLIC ZIP 4종 bytes/CRC 및 관련 함수 정적 검토, `MSC_MD_LINK_SKILL_SUPPORT_REVIEW_AND_PROPOSAL_r0002_20261116_KST.md`, `CLAUDE_MSC_MD_LINK_STRUCTURE_INTERACTIVE_REVIEW_FOR_GPT_20261115.md`의 MAJOR 5/MINOR 1을 재대조.
- 이번 턴 PUBLIC 저장소와 기존 문서·승인 경계를 다시 읽었다. 작업 컨테이너의 `raw.githubusercontent.com` DNS 조회가 실패해 4개 ZIP을 다시 다운로드/압축 해제·코드 변경하지 못했다. 선행 정적 검토를 **이번 신규 시험 PASS로 승격하지 않음**.
- 실제 업무 설치 버전, 대상 저장소 writer·호스팅·업데이트 승인, Markdown 마커 소유권, 그룹 reader 접근은 여전히 G0 미확인.

## 스킬별 최소 범위 판정

| 스킬 | 근거 공개 baseline | 판정 | 최소 범위 / 보류 조건 |
|---|---|---|---|
| `doc-converter` | v0.2.21 | **EXTEND 후보 / 지금 코드 변경 NOT_RUN** | 기존 PUML/SVG·MSC_VIEW/manifest는 재사용. 자동 SVG 내장 B HTML·안전 파일명 충돌 검사·없으면 DELTA 링크 미생성·AS-IS 문구·SVG 라벨 기준 단계 이동은 구체적 후보. 설치본 계약/합성 회귀 필요 |
| `work-ledger-kernel` | v0.7.37 | **CONNECT 우선, 조건부 최소 EXTEND** | 정적 발췌의 소형 Evidence export는 `.md/.html/.json/.txt` 위주, SVG/PUML 제외. 기존 파일 등록/실게시 경로 매핑·rename/readback 사용 가능 여부 우선 확인. 실제 미지원 시에만 SVG 제한 허용·size/누락 검증 후보 |
| `l1-fix-workflow` | v1.6.67 | **REUSE/CONNECT** | 기존 scenario handoff/Work 선택·원본 조회 사용; 추가 renderer·별도 그룹 writer 금지. 같은 Work 저장·호환성은 업무 환경에서 별도 확인 |
| `code-analyzer` | v0.15.2 | **REUSE/추가 수정 보류** | 기존 Code Facts·MSC·source revision 우선. Semantic spec을 verified scenario IR로 단정하지 않음. Procedure/Feature 문서 재생성에서 대상 MSC 절 보존 여부 확인 |
| **`l1-knowledge-updater`** | 공개 ZIP 미확인 | **반드시 G0 검토** | 직접/Workflow 두 진입에서 같은 개인 Work 보존, 후보·Preview·승인된 그룹 writer·리비전과 링크 갱신 계약 확인. 실제 Updater 소스 미접근 상태에서 수정 불필요로 제외하지 않음 |
| `l1sw-dev-knowledge` / 호스팅 | 실제 설치본·권한 미확인 | **ADDITIONAL_CHECK_REQUIRED** | 그룹 MSC 절 최종 writer, 자산 게시·readback, 실제 독자 URL 접근 및 CSP/폴백 확인 |

필요한 시험(아직 NOT_RUN): 3가지 입력 클래스, 한글 파일명 충돌, 렌더 실패, SVG 중복/미존재 Phase, 조건부 `MSC_DELTA.md`, HTML size gate, 게시 rename/hash/readback, 수동 문단 보호·중복 append 0·stale source, 두 진입의 동일 Work 저장, 승인된 그룹 게시와 폴백 브라우저 열람. 샘플 B UI PASS는 converter 자동 생성 PASS가 아님.

## 실제 결과·판정

| 항목 | 상태 |
|---|---|
| 기존 4종 정적 근거·Claude 의견 재대조 | PASS (기존 문서 범위) |
| PUBLIC 업무 GPT G0 인계 MD 게시 및 원격 확인 | PASS |
| PUBLIC handoffs/README.md 목록 추가 | PASS |
| PRIVATE 변경 필요성/분리 판정 | PASS (문서 범위) |
| 이번 ZIP 원본 새 다운로드 및 패치/회귀 | NOT_RUN (컨테이너 네트워크 DNS 제약) |
| 업무 GPT/로컬 Agent 설치 G0 질문 Q1~Q8 | REQUEST DOCUMENT POSTED / 실제 검토·응답 NOT_RECEIVED |
| 유료 watcher 독립 리뷰/영수증 | 이번 요청 NOT_RUN / NOT_RECEIVED (기존 CURRENT 상태 유지) |
| 업무 Workspace/그룹 지식/브라우저 전체 E2E·RAG | NOT_RUN |

업무 GPT용 공개 문서는 회사 코드·상세 MSC·고객자료·운영 로그·PRIVATE 결과/REQUEST/영수증을 포함하지 않는다. PUBLIC Handoff 게시와 PRIVATE 판정/실제 검토 호출·설치·PUBLIC 최종 스킬 ZIP은 별도 상태. 문서 작성·게시만으로 유료 호출·host 실행·지식 write·운영 변경 승인이 발생하지 않음.

**NEXT_ONE_ACTION:** 업무 GPT/허용 로컬 Agent가 공개 인계 Q1~Q8을 실제 설치본 및 기존 G0 근거로 READ_ONLY 대조하고, 비민감 REUSE/CONNECT/입증된 EXTEND·미확인 결과를 회신. GPT는 해당 결과로 좁은 개발·합성 시험 후보를 결정하되 기존 Work 재사용.
