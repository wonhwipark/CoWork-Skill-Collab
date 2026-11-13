# CoWork 운영 기준 — 마이그레이션 최소 정본 안내
상태: POINTER_ONLY / RAW_SOURCE_NOT_COPIED | 2026-11-10 KST

현재 운영 규칙 원본은 기존 Dropbox:
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
- 리뷰 결과, ZIP 검증, 배포 승인, 호스트 적용, 사내 E2E는 서로 다른 상태.

## 프로젝트 공통 참고 정보 (운영 규칙과 분리)

- [L1 Workspace RAG · Work 유형 · 브랜치별 AS-IS MSC 공통 컨텍스트](L1_WORKSPACE_RAG_COMMON_r0001_20261111.md) — 새 GPT 대화/리뷰/인계에서 재사용하는 **비민감 설계·검증 상태·정본 포인터**. 프로젝트별 최신 상태는 `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`의 마지막 섹션을 우선한다.
- 공통 문서 기록은 Dropbox LIVE 운영 규칙을 복제·수정하거나 REQUEST/READY, 독립 리뷰, 사내 배포·실행을 승인하지 않는다.

- [L1_CHANNEL 담당 모듈·분석 범위 공통 컨텍스트](L1_CHANNEL_MODULE_SCOPE_COMMON_r0001_20261113.md) — NR BCH/LTE ChCfg, NR/LTE L1 Tx의 담당 분야(사용자 확인) 및 분류표 후보; 이슈 분석·지식 갱신 요청 시 우선 조회.
- [담당자 검토용 NR/LTE 분류표 v0.7](references/L1_NR_LTE_OWNER_REVIEW_CLASSIFICATION_v0_7_20261113.md) — 181개 A/B 검토 후보. 확정 코드 사실 아님.

## 새 작업의 보유 스킬 발견

- [공통 스킬 기능 목록](SKILL_CAPABILITY_CATALOG.md)에서 요청 기능과 기존 스킬의 연결 후보를 먼저 확인한다.
- [스킬 발견·재사용 절차](../ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md)에 따라 프로젝트 CURRENT·열린 메모와 관련 원문을 확인한 뒤 REUSE/CONNECT/EXTEND/DEFER를 판단한다.
- 기존 Dropbox LIVE 규칙·스킬 설치·승인 경계는 바꾸지 않는다. 목록과 시작 절차 연결만 수행했으며 18개 전체 재감사는 별도 대기다.
