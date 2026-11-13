# CoWork 운영 기준 — 마이그레이션 최소 정본 안내
상태: POINTER_ONLY / RAW_SOURCE_NOT_COPIED | 현재 포인터 정정: 2026-11-14 KST

## 현재 기준과 과거 원본 구분

- 현재 협업 방식·승인 범위는 [START_HERE](../START_HERE.md)와 [이관 CURRENT 최상단](../projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md)을 먼저 확인. 과거 원본의 LIVE/미검증 문구를 현재 상태로 복사하지 않음.
- 단일 사용자 최신 설계와 실제 실행·유료 독립 리뷰·LIVE 전환은 구분. 설치된 운영 보호 장치를 이 포인터 정정으로 해제하지 않음.
- L1 현재 정책·후속 시점은 [2026-11-14 판정](../projects/L1-WORKSPACE-RAG-20261111-001/L1_KNOWLEDGE_FEEDBACK_DISPOSITION_r0001_20261114.md) 우선.

## 보존된 과거 규칙 원본 (현재 provider 증거 아님)

기존 Dropbox 원본:
- `/SKILL-COLLAB/knowledge/OPERATING_RULES_r0010.md` — GPT 판정 후 연속 실행 및 권한 게이트.
- `/SKILL-COLLAB/knowledge/OPERATING_RULES_r0009.md` — SEMI_AUTO 기본, AUTO_PENDING_SETUP 분리.
- `/SKILL-COLLAB/knowledge/OPERATING_RULES_r0008.md` — 기본 역할/권한, Claude 노트·리뷰·증거 계약.
- `/SKILL-COLLAB/knowledge/REQUEST_PUBLICATION_GUARD_20261106.md` — 실제 바이트 SHA 및 READY 마지막 게시.
- `/SKILL-COLLAB/RESUME_LATEST_r0005.md` — 기존 Dropbox 운영 진입점.

이 파일은 위 원본을 대체하지 않는다. 원문 복제는 실제 바이트 대조/민감 분류 후 개별 승인한다.
- GPT: 오케스트레이션·코드 변경·시험·최종 판정.
- Windows Claude Code: 독립 리뷰어(정식 유효 요청일 때만 모델 리뷰).
- Python watcher: 감지/검증/실행/영수증 게시. 무요청 호출 0건.
- 비용 정책: STATIC $1 / LARGE $3 / XLARGE $6; 예산 자동 증액 금지.
- 리뷰 불가 시 GPT 독자 개발 가능, `CLAUDE_REVIEW=NOT_RUN/PENDING`; 리뷰 성공 오인 금지.
- 리뷰 결과, ZIP 검증, 배포 승인, 호스트 적용, 실행 호스트 E2E는 서로 다른 상태.

## 프로젝트 공통 참고 정보 (운영 규칙과 분리)

- [L1 Workspace RAG · Work 유형 · 브랜치별 AS-IS MSC 공통 컨텍스트](L1_WORKSPACE_RAG_COMMON_r0001_20261111.md) — 새 GPT 대화/리뷰/인계에서 재사용하는 **비민감 설계·검증 상태·정본 포인터**. 프로젝트별 최신 상태는 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`의 마지막 섹션을 우선한다.
- 공통 문서 기록은 Dropbox LIVE 운영 규칙을 복제·수정하거나 REQUEST/READY, 독립 리뷰, 작업 PC 배포·실행을 승인하지 않는다.

- [L1_CHANNEL 담당 모듈·분석 범위 공통 컨텍스트](L1_CHANNEL_MODULE_SCOPE_COMMON_r0001_20261113.md) — NR BCH/LTE ChCfg, NR/LTE L1 Tx의 담당 분야(사용자 확인) 및 분류표 후보; 이슈 분석·지식 갱신 요청 시 우선 조회.
- [최신 NR/LTE 분류표 v0.9](references/L1_NR_LTE_Confluence_Module_Procedure_Feature_Table_v0_9_20261113_KST.md) — 215개 P/F 검토행. 실제 코드/ID/담당자 승인 아님. [v0.7 181행](references/L1_NR_LTE_OWNER_REVIEW_CLASSIFICATION_v0_7_20261113.md)은 계보 보존.

## 새 작업의 보유 스킬 발견

- [공통 스킬 기능 목록](SKILL_CAPABILITY_CATALOG.md)에서 요청 기능과 기존 스킬의 연결 후보를 먼저 확인한다.
- [스킬 발견·재사용 절차](../ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md)에 따라 프로젝트 CURRENT·열린 메모와 관련 원문을 확인한 뒤 REUSE/CONNECT/EXTEND/DEFER를 판단한다.
- 실제 provider·승인 범위는 이관 CURRENT 우선. 관리 18개 중 17 ZIP 정적 확인·skillsilent 추가 확인 상태이며, 설치/API·실호출 검증과 구분. 불필요한 전체 재감사 대신 관련 원문·변경분만 확인.

## 공통 용어 표기 기준

- [용어·저장소·실행 환경 표기 원칙](../ops/CONTRACTS/TERMINOLOGY_AND_ACCESS_SCOPE_V1.md) — 신규 설명/인계/답변에서는 실제 저장소·접근 권한·작업 PC/실행 호스트로 구분한다. 이전 문서의 원문·파일명·해시·기록은 보존한다.

[새 창 공통 맥락 개선 검토](../projects/COWORK-SKILL-DISCOVERY-20261112-001/NEW_CHAT_CONTEXT_BOOTSTRAP_REVIEW_r0001_20261114.md)는 단일 브리프+관련 CURRENT 읽기를 제안한다. 자동 로더·프로젝트 설정 변경은 수행하지 않음.
