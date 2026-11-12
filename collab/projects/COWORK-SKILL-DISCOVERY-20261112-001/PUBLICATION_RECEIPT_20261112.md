# 공통 스킬 발견·시작 절차 게시 검증 기록

- Date: 2026-11-12 KST
- Repository: PRIVATE `wonhwipark/CoWork-Skill-Collab` / branch `main`
- CONTENT_COMMIT: `af8ea93ae0e31dc21b7c96311e45135307a3b1da`
- METHOD: 고정 commit의 전체 UTF-8 원격 본문을 작성 내용과 비교. 실제 로컬 bytes의 SHA-256과 Git blob을 계산했고 원격 blob·본문 일치를 확인.
- DOCUMENT_STATIC_QA: 7개 MD의 UTF-8/LF/최종 newline·fence 확인, 내부 링크 29개 대상 존재 확인 PASS.
- COMMIT_SCOPE: 원격 commit diff의 변경 7개가 승인된 문서 목록과 일치 PASS.
- RUNTIME / HOST / ACTUAL_SKILL_CALL / INDEPENDENT_REVIEW: NOT_RUN.
- SKILL_18_DETAIL_RECHECK: PENDING_CHECK / 별도 작업. 기존 요약 재사용을 전체 검증으로 보고하지 않음.

| 문서 | Bytes | SHA-256 | Git blob | Readback |
|---|---:|---|---|---|
| `AGENTS.md` | 1318 | `f89a1e83af913a1fea09e89d16cb2968babffd1b18a225aa3c6df15ea29247b1` | `34a81c03701ccc5aed872ebf4bf8a3d23f7c6c48` | PASS |
| `README.md` | 3185 | `613c28231c704d2272323934c5b51d59dea93af76f3708e1c596f9b3fb12f4a4` | `ac8a4d564bd0af795406b83784eb4d4b92ec6672` | PASS |
| `collab/START_HERE.md` | 7293 | `2227d953180f70699066355efc0bc90ebe0520adecf576f3d20064a5a4f6ccaa` | `01e81c7d810745cdde3df744007b938661812546` | PASS |
| `collab/knowledge/OPERATING_BASELINE.md` | 2509 | `a544dc295a31c3c01ee5767b70b1b038384895f5b1345dfcbf5aa510c50cf7db` | `95221518fa09111c6c97c8416bde612280ba53f1` | PASS |
| `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` | 8723 | `c749892cfec548e1b8c65f31e521493a4491304f328611422ec5f84026cb745c` | `25b3e6eb0dc1cfca0793be51fd3534f09c048f71` | PASS |
| `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md` | 5266 | `5f3ffad629ba4be22bedc17255e28ed8f91b2006f82fc6144bde672b19912961` | `99859ae9f76c890f857ad5ce7aecfa698af28461` | PASS |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md` | 3292 | `3f26c7a040e3cd3e86a2b38d2b499d7c57c093f5590a90d37ad86191bb16918a` | `762e211bd59c713307a2def9f99b78b7f1f2055d` | PASS |

위 CURRENT는 content commit의 최초 게시본이다. 본 영수증과 CURRENT의 최종 상태 추가는 다음 metadata commit에서 게시하며, 자기 commit/자기 hash를 미리 PASS로 기록하지 않는다. 최종 metadata 게시 후 별도 원격 본문을 다시 확인한다.

기존 L1 r0005 인계·수행 요청·Knowledge/metadata·스킬 코드·운영 설치본·Job/예약·REQUEST/READY·PUBLIC·LIVE는 변경하지 않았다. ChatGPT 프로젝트 설정 변경 또는 다른 창의 자동 로드를 완료했다고 주장하지 않는다.
