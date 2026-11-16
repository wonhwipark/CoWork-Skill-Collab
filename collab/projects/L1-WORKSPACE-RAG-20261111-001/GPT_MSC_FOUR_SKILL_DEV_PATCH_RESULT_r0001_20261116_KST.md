# MSC 링크 4종 스킬 개발·검토 결과 — r0001 / 2026-11-16 KST

- Work: `L1-WORKSPACE-RAG-20261111-001`; GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`.
- 사용자 지시: 업무 GPT의 설치본 G0 확인과 **독립적으로** 공개/기존 4종 스킬을 검토해 안전한 범위에서 수정 진행.
- 설계 입력: `MSC_MD_LINK_SKILL_SUPPORT_REVIEW_AND_PROPOSAL_r0002_20261116_KST.md`, `CLAUDE_MSC_MD_LINK_STRUCTURE_INTERACTIVE_REVIEW_FOR_GPT_20261115.md`, 직전 GPT 판정.
- 결론: **2종 실제 소스 수정·개발 ZIP 게시**, 2종 기존 기능 재사용/연결 우선으로 소스 수정 보류. 이번 변경의 업무 설치/G0 확인 또는 정식 독립 패치 리뷰를 수행했다는 뜻 아님.

## 스킬별 실제 결과

| 스킬 | 입력 원본 | 이번 판정/변경 |
|---|---|---|
| `doc-converter` | PUBLIC `L1Work/main/doc-converter_v0_2_21_1106.zip` (blob `bd5192c802fcc28d21f75ead81fb4cffc10d8470`) | **실제 수정**. v0.2.22 중간 후보(루트 candidates 보존) → **v0.2.23**: 한국어 다이어그램명 SHA 기반 고유화·중복 충돌 hard-fail; Procedure/Feature AS-IS 전용 문구/조건부 delta 링크; opt-in `PROCEDURE_FEATURE` mode에서 기존 SVG를 내장한 단일 HTML B viewer와 유일한 SVG divider 라벨에 한정된 Phase 이동. 기존 `ISSUE` 기본 동작 유지. 기존 source 분석 재실행 없음 |
| `work-ledger-kernel` | PRIVATE `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/work-ledger-kernel_v0_7_39_1115.zip` (blob `418d11db6a2d5071d37bcdd8bf1cc9e94f23346c`) | **실제 수정**. **v0.7.40-dev.1**: 기존 export에서 등록된 소형 `.svg` 허용, 승인 크기 초과 `MSC_SVG_TOO_LARGE` 차단. 기존 `published_path`/SHA/중복 매핑 보호 재사용; 클라우드 링크와 MD 자동 rewrite는 임의 도입 안 함. 기존 CL/PR WorkReference v0.7.39 변경 계승 |
| `l1-fix-workflow` | PRIVATE 기존 후보 `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/l1-fix-workflow_v1_6_69_1115.zip` 존재 확인 | **REUSE/CONNECT, 신규 패치 NOT_RUN**. 기존 Work 선택·재개/MSC handoff 사용. 단일 HTML viewer를 Workflow에 중복 구현하거나 그룹 writer 책임 추가하지 않음. 실제 대상 MD writer 연결 계약은 별도 확인 필요 |
| `code-analyzer` | PRIVATE 기존 후보 `collab/projects/L1-WORKSPACE-RAG-20261111-001/candidates/code-analyzer_v0_15_3_1114.zip` 존재 확인 | **REUSE, 신규 패치 NOT_RUN**. CODE_FACTS·semantic spec·MSC source revision 재사용. 시나리오 IR을 자동 검증된 사실로 승격하거나 문서 writer 책임을 추가하지 않음. 원본 인터페이스·설치본과의 차이는 G0 미확인 |

## PRIVATE main 산출물 (별도 신규 버전, PUBLIC 미배포)

| ZIP 상대 경로 (위 Work 기준) | 바이트 | 원격 바이트 SHA-256 | Git blob | 검증 |
|---|---:|---|---|---|
| `candidates/doc-converter_v0_2_23_1116.zip` | 210,426 | `43805ae0ce1b08205125441f383f6bdfc6f114ef53bb2609295827f10b1ce23e` | `ba32a057a2590fdf51aac6aad30f831404ed0222` | 원격 readback 일치, ZIP 중앙 디렉터리·중복/이탈 0·수정 STORED 항목 CRC PASS |
| `candidates/work-ledger-kernel_v0_7_40_1116.zip` | 410,922 | `b8077fd717f326fb7bc556407b8e8b8a7f32a580e143ec3a6d646d3b1e9df7ce` | `3e9346ad5d13645d86bcfdce6aa20f7e17f4699d` | 원격 readback 일치, ZIP 중앙 디렉터리·중복/이탈 0·수정 STORED 항목 CRC PASS, 내부 MANIFEST_SHA256 변경 항목 갱신 |

- doc-converter 생성 commit `f48b80928fbe410cb2c8c0f38f2f4ac7472320ee`; Kernel 생성 commit `1d11177af8155c559a73c85decd12c638d6abdec`; 두 커밋 이후 원격 파일 blob/바이트/hash 읽기 확인.
- doc-converter 중간 산출물 `candidates/doc-converter_v0_2_22_1116.zip`는 PRIVATE 루트의 보존용 단계이며 최종 검토 대상은 위 Work의 v0.2.23. 구버전 삭제 없음.
- ZIP은 실제 코드가 변경된 개발 후보이나, **버전 메타데이터·manifest 및 전 이력의 완전한 스킬 릴리스 검증 PASS가 아님**.

## 시험, 안전, 잔여 차단

| 게이트 | 실제 상태 |
|---|---|
| 소스 patch anchor 및 코드 변경 후보 생성 | PASS (GitHub ZIP 바이트 기반, 변경 후보 범위) |
| 새 ZIP 원격 조회·바이트 SHA-256·경로 안전성·수정 STORED CRC | PASS |
| 모든 DEFLATED 항목 새 독립 CRC·ZIP 전체 퍼포먼스 시험 | NOT_RUN (변경하지 않은 기존 압축 바이트 재사용) |
| Python 3.10/3.11 구문·단위·기존 전체 회귀 | **NOT_RUN**. ZIP에 새 테스트 파일 포함했으나 실행하지 않음 |
| B HTML 실제 PlantUML 렌더/Chromium 단계 이동/CSP/스크립트 차단 | **NOT_RUN** |
| 업무 Work/그룹 writer의 HTML·SVG `published_path`, readback, 상대 MD 링크, 부분 게시 복구 | **NOT_VERIFIED**. G0 및 E3 필요 |
| 설치 `l1-knowledge-updater` 실제 I/O와 두 진입, 승인된 Knowledge 게시 | 별도 기존 G0 인계 유지, 이번 패치 실행 범위 아님 |
| 패치 후 개발자 자체 Python 시험/독립 코드 리뷰·영수증 | NOT_RUN |
| PUBLIC L1Work 루트 최종 ZIP, skill-updater/호스트 설치/LIVE/Job/Knowledge write/유료 리뷰 | **NOT_RUN / RELEASE_BLOCKED** |

현재 `doc-converter`의 `MSC_VIEW.md`에 생성되는 HTML 링크는 **로컬 패키지 상대 경로**다. 실제 Work/Knowledge 게시에서 파일명 변경과 권한/호스팅을 확인한 `published_path` 기반 링크로 교체하는 것은 대상 writer의 후속 책임이며, 로컬 단일 HTML 생성만으로 실제 브라우저 확대 링크 PASS를 주장하지 않음. SVG 미리보기 역시 Kernel export map에서 게시 경로를 대조해야 함.

이 변경은 회사 코드·상세 MSC·로그·인증 자료를 포함하지 않음. 기존 REQUEST/SOURCE_PIN/READY/과거 승인·비용·영수증 및 운영 LIVE 설정은 수정하지 않음. GitHub의 대시보드/Pages 자동 작업 PASS는 스킬 Python 회귀 PASS가 아님.

**NEXT_ONE_ACTION:** 이 2개 개발 후보를 격리 Python 3.10/3.11 환경에서 신규 및 기존 테스트·3종 입력 클래스/한국어 이름 충돌/상한 초과·HTML 브라우저 폴백/manifest 일관성까지 실행해 실제 PASS/FAIL 근거를 회수. FAIL만 같은 Work에서 수정·재시험, 검증 전 PUBLIC 릴리스 금지. 업무 G0와 독립으로 개발 시험 진행 가능.
