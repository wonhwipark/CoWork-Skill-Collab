# PEC-HOP·ACE 두 스킬 — 사용자 독립 리뷰 생략·L1Work PUBLIC 최종 ZIP 배송 결과 r0001

- 일시: 2026-11-19 KST
- Work: `COWORK-SKILL-DISCOVERY-20261112-001`, CoWork PRIVATE `wonhwipark/CoWork-Skill-Collab/main`
- 사용자 최신 실행 지시: **“리뷰스킵하고 스킬 업데이트후패키지 l1work 에 올려줘”**
- **종합:** `PUBLIC_RELEASE=POSTED_AND_REMOTE_SHA256_VERIFIED` 두 종 / `INDEPENDENT_CODE_REVIEW=SKIPPED_BY_EXPLICIT_USER_REQUEST` / `NON_REVIEW_RELEASE_GATES=PASS` / `BUSINESS_HOST_INSTALLED=NOT_RUN_BY_GPT` / `BUSINESS_HOST_E2E=NOT_EXTERNALLY_OBSERVABLE`.
- 유효한 기존 검증·사용자 배송 권한과 구분: 구 Windows 정식 독립 코드 리뷰 REQUEST는 `POLICY_COST_MISMATCH`로 **미실행**·모델 호출 0, 이번 사용자 지시로 **이번 두 최종 ZIP의 독립 코드 리뷰만** 명시적으로 생략. 기존 리뷰 결과/영수증을 PASS로 위장하지 않음. 예외 범위: [스코프 기록](PEC_ACE_USER_REVIEW_WAIVER_PUBLIC_DELIVERY_SCOPE_r0001_20261119_KST.md). **기타 스킬·향후 정식 릴리스에 대한 일반 생략 권한 아님**.

## 1. 실제 게시된 최종 바이너리

| 스킬/기능 | PUBLIC `wonhwipark/L1Work/main` 루트 정확한 파일 | bytes | 원격에서 직접 계산한 SHA-256 | GitHub Git blob SHA |
|---|---|---:|---|---|
| Code Analyzer / PEC-HOP | [`code-analyzer_v0_15_4_1119.zip`](https://github.com/wonhwipark/L1Work/blob/main/code-analyzer_v0_15_4_1119.zip) | **515,581** | `11e1da15ee12e750c3652190c348a7fc8e31aa1741876e3c06bc0af3413b16af` | `1c43503a2a4695400727fb3fb1cd0cb3c49f826b` |
| Workflow / ACE | [`l1-fix-workflow_v1_6_74_1119.zip`](https://github.com/wonhwipark/L1Work/blob/main/l1-fix-workflow_v1_6_74_1119.zip) | **760,324** | `b810ce0cf072609431737c58b0ef2b7a0a8ec0701a0746e6a94283c374224989` | `5b05e6e16c8be7902793c62a50fb3c105fd35b6e` |

- **PUBLIC commit:** `b27d7ccaf7d3d827e493e0b61db9ff083817daaf`, parent `41b57a7e8218da3a1f78691f1484eb3c26440cba`, tree `a0aab8420529f72115964fc611949ebcfb985181`. 기존 PUBLIC ZIP 덮어쓰기 0, 신규 파일 2개만 추가.
- **원격 직접 검증:** PRIVATE staging의 원본 ZIP 두 개를 `fetch_file(encoding=base64)`로 읽어 L1Work Git blob(`encoding=base64`) 생성, 두 소스 Git SHA-1과 생성된 목적 blob SHA가 각각 동일한지 비교 → PASS. `create_tree` + `create_commit` + branch `main` optimistic `expected_sha` 업데이트 → PASS. **배포 후 실제 L1Work/main ZIP 두 개를 다시 조회해 base64 전체 바이트 비교 + raw bytes SHA-256 직접 재계산** → 각각 PASS. 중간의 Base64 본문/크기만 보고 완료 판정하지 않음.

## 2. 비리뷰 릴리스 시험·바이트 고정

- [PRIVATE GH Actions 릴리스 빌드/스테이징 run 44512854513](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44512854513), conclusion **SUCCESS**. 고정 빌더 `dev/prepare_pec_ace_review_waived_release_r0001.py`, 실제 PRIVATE staged `release-staging/` 두 파일·검증 JSON 바이트 고정; 이 stage 자체는 공개 배송이 아님.
- `code-analyzer`: 실제 ZIP 내 검증 **12 PASS / 0 FAIL**, 원본 source preservation PASS(기존 216개 중 210 바이트 동일, 의도적 변경 6, 새 PEC 모듈 1), 전체 ZIP CRC/버전/파일 217/manifest 216 PASS, 비밀정보·부적절 아카이브/경로 검사 **217파일** PASS.
- `l1-fix-workflow`: 실제 ZIP 내 검증 **10 PASS / 0 FAIL**, 원본 source preservation PASS(기존 310개 중 303 바이트 동일, 의도적 변경 7, 새 ACE 모듈 1), 전체 ZIP CRC/버전/파일 311/manifest 310 PASS, 비밀정보·부적절 아카이브/경로 검사 **311파일** PASS.
- **2회 독립 빌드 결과 ZIP 바이트 일치 PASS** (각각 `cmp`). PRIVATE Stage raw SHA와 L1Work public remote SHA PASS. `.skill-release.json`은 최종 `channel=public_release`, `release_kind=user_explicit_delivery_with_independent_review_waived`, `independent_code_review=SKIPPED_BY_USER_REQUEST`; 관련 SKILL.md에 실제 생략과 업무 수락 경계 기재. 종전 `development_not_for_deployment` 후보를 그대로 게시하지 않음.
- **제한:** 검사된 비밀 패턴/파일 규칙과 고정 합성시험 범위의 PASS. 독립 코드 리뷰·실업무 보안·Linux 설치 시험/효용 측정의 PASS로 확대하지 않음. 특히 PEC/ACE는 기존 진입 경로의 명시적 opt-in 함수이며, 업무 GPT·Linux Agent가 실제 Evidence/Work 원문·권한을 연결할 수 있는지는 내부 전용 G0/E2E로 판단. 업무 자료·설치본·비민감 요약조차 외부로 반출 요구하지 않음.

## 3. 명확한 완료·미완료 및 후속

| 범위 | 판정 |
|---|---|
| CoWork 코드·개발 후보·최종 ZIP 빌드 | PASS |
| 소스·SHA/CRC/보안 패턴 검사/기능·패키징 합성시험 | PASS(위 한정 범위) |
| 새 Windows Claude Code 독립 리뷰 | **SKIPPED_BY_EXPLICIT_USER_REQUEST, NOT_RUN** |
| L1Work/public/main 루트 신규 ZIP 2개 게시 | **POSTED / REMOTE_SHA256_VERIFIED** |
| 업로드 후 자동 설치/실행 여부 | **NOT_VERIFIED** |
| 업무 Linux 수락·실제 PEC/ACE 효과 | **NOT_EXTERNALLY_OBSERVABLE** |
| ACON, Kernel, Knowledge Updater, skill-updater 수정 | **0** |
| REQUEST/READY/모델 호출/운영 변경/업무 데이터 반출 | **0** |

**NEXT_ONE_ACTION:** 업무 GPT/허용된 Linux Agent가 **업무 환경 내부에서만** `skill-updater`로 실제 설치본 리비전/원본 무결성·opt-in reader 사용성을 확인하고, 기존 [L1Work handoff §13–14](https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)의 1건 파일럿 시험 기준으로 업무 효과 비교. 이 결과/원문은 외부로 회신하지 않음. CoWork는 PUBLIC DELIVERY=완료, HOST E2E=미관측으로 유지.
