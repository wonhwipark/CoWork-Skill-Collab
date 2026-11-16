# MSC 스킬 2종 L1Work PUBLIC 최종 ZIP 게시 결과 — r0001 / 2026-11-16 KST

## 1. 현재 상태

- **PUBLIC_DELIVERY=PASS / REMOTE_SHA256_READBACK=PASS**.
- 사용자 요청: 실제 실행자는 **OpenCode**이므로 `skillsilent` 런타임 시험을 필수 릴리스 게이트에서 **SKIP**하고, 핵심 코드·실제 Work/CLI 회귀·배포 패키지 안전성을 확인한 뒤 `wonhwipark/L1Work/main` 루트에 최신 스킬 ZIP 게시.
- 독립 Claude Code 리뷰 사이클은 사용자 지시에 따라 **1회로 종료**. 이후 추가 Claude 리뷰·REQUEST/READY·유료 호출 0. 본 릴리스는 개발자 자체시험을 통과했으며 별도의 패치 후 독립 코드 리뷰 완료라고 주장하지 않음.
- 최종 공개 커밋: `32a9c3f2d03a654c3cfc7c832067e35f6c83d8c9`, 저장소 `wonhwipark/L1Work`, branch `main`. 기존 ZIP 삭제/덮어쓰기 0.

## 2. 실제 변경 및 PUBLIC 산출물

| 패키지 / PUBLIC main 루트 | 실제 바이트 | SHA-256 (GitHub 원격 실제 bytes 검증) | Git blob |
|---|---:|---|---|
| [doc-converter_v0_2_25_1116.zip](https://github.com/wonhwipark/L1Work/blob/main/doc-converter_v0_2_25_1116.zip) | 162642 | `97cbdf6747b2632035a56fd0ecb792115cdd35e0a202caa3555991422544f181` | `be847e46b8e47885e02b869391c3c9975574fd0c` |
| [work-ledger-kernel_v0_7_42_1116.zip](https://github.com/wonhwipark/L1Work/blob/main/work-ledger-kernel_v0_7_42_1116.zip) | 320083 | `ece2bce143ef35a1c8cc3bc12ddf6a73e27e0f218fc69fec87844759d9dfc164` | `7799e03fbfa5c95851c430a20f8df0da253cbf07` |

- 사용한 정확한 입력 고정: PRIVATE `candidates/doc-converter_v0_2_24_1116.zip` SHA `2ef0929bc0a80a1c0aca67bf3c8fc02f967bddba223b45c27807c363e96229f7` / `candidates/work-ledger-kernel_v0_7_41_1116.zip` SHA `48d1bf5e24c613e7e0ba04df9946c427c5d1ee39d8d16204966afff07e93497b`. 이전 PRIVATE 후보 보존.
- 최종 ZIP은 별도 신규 버전, 개발 후보 `development_not_for_deployment` 메타를 덮어쓰지 않고 릴리스 전용 `channel=public`, `release_kind=approved_final_zip` 메타로 신규 재빌드. `SKILL.md`, `VERSION`, `skillsilent/manifest.json`, `skillsilent/contract.json`(존재 시), `references/low_spec_routes.json`(doc), Kernel CLI 런타임 버전 정합화.
- `doc-converter`: 기존 한글 NFC/대소문자 충돌 차단, opt-in Procedure/Feature B형 HTML+SVG 및 Phase 누락 상태 기록 유지. 보유 기능의 직접 CLI 동작을 시험. `work-ledger-kernel`: 실제 Evidence 등록→MSC SVG/MD export, 게시 경로·SHA/멱등성, 무관 SVG skip, 크기 초과/악성 SVG fail-closed 유지. Linux launcher와 기존 Claude hook shell wrapper의 실행 비트 복구.
- 출시 메타/테스트 계약의 구버전 불일치, 예전 TL_REVIEW 차단·Work README 라벨·날짜 고정 테스트를 **현재 보호 정책·UI·시간 의미에 맞추어 갱신**. 무관한 운영 코드 기능 확장 없음. 구버전 테스트/개발 과정의 근거는 기존 PRIVATE Work 이력에 보존.

## 3. 실제 시험과 보안 게이트

- [GitHub Actions Run 43806773258](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43806773258): isolated test branch `msc-skill-validation-20261116`, Python 3.10·3.11 각각 **conclusion=success**; 마지막 export job도 success.
- **각 Python 버전별 full packaged pytest:** doc-converter **83 PASS**, work-ledger-kernel **244 PASS + 39 subtests PASS**, kernel warnings 1 (기능 FAIL 아님).
- 실제 인터페이스 테스트: `WorkLedgerKernel.new` + 실제 Registry `code-analyzer/asis_msc` → `record_evidence` → `work_docs_export`. 소형 SVG·MD 게시 / 비MSC SVG 제외 / published_path와 바이트 SHA / 재실행 동일 / 대형·active SVG 차단 **PASS**. `doc-converter`는 Python 직접 CLI (`package --view-mode PROCEDURE_FEATURE --allow-unrendered`) 호출 및 결과 manifest/MD 생성 **PASS**. 위 테스트는 격리 합성 입력이며 업무 소스/호스트 실행 아님.
- ZIP 전체 CRC, 전 회원 내부 SHA 인덱스, 파일 경로·중복·심링크·실행 모드, 민감정보 패턴 및 중첩 압축파일 점검 **PASS**. 최종 PUBLIC main에서 파일을 재조회해 SHA-256을 자체 계산했으며 공개 Git blob·바이트 수·해시 모두 **PASS**.
- `skillsilent` 런타임 검증은 실제 사용자 지정 OpenCode 경로가 아니므로 **SKIP_BY_USER_SCOPE**. 버전·정적 계약 메타는 릴리스와 일치시킴. 이 Skip은 직접 OpenCode CLI 확인의 대체/누락이 아니라 실행자 분기.
- 실제 업무 `l1-workspace` / `l1sw-dev-knowledge` writer, HTML 호스팅 CSP/클릭 URL·원격 published_path end-to-end, 운영 호스트 설치, Skill-Updater Job 실행, 승인된 Knowledge 게시, LIVE 변경: **NOT_RUN/NOT_VERIFIED**. PUBLIC 게시만으로 이들 성공을 주장하지 않음.

## 4. 안전 경계·다음 한 동작

- PUBLIC 업로드는 사용자가 본 턴에서 명시 요청한 범위 내 **2개 최종 ZIP 루트 게시**에 한정.PRIVATE 운영 설계·리뷰 이력/민감 원본/업무 자료는 PUBLIC에 업로드하지 않음.
- 추가 독립 리뷰 REQUEST/READY·별도 유료 모델 실행 **0**. PRIVATE 프로젝트 CURRENT/TRACKER와 이 결과 문서만 기록 대상으로 유지. 자동 Skill-Updater/호스트 설치·설정·DB·LIVE 건드리지 않음.
- **NEXT_ONE_ACTION:** 다음 승인된 업무 OpenCode/Skill-Updater 실행에서 PUBLIC ZIP 실제 SHA-256을 핀으로 사용하여 설치본과 비교하고, 업무 writer의 URL·published_path 및 group Knowledge 후보 연결 G0/E3를 별도로 확인. PUBLIC 배송 완료와 호스트 적용을 구분.
