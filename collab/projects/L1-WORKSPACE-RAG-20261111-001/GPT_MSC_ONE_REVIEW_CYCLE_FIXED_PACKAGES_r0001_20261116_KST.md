# MSC 스킬 리뷰 1회 종료 — 수정·패키징·자체시험 결과 (r0001 / 2026-11-16 KST)

- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`.
- 사용자 최신 지시: **Claude Code 리뷰 사이클은 1회로 종료. 추가 독립 리뷰 REQUEST/READY·유료 모델 호출 없이** 지난 리뷰의 6개 결함에 대한 개발·시험·최종 신규 패키지 전달.
- 원본 리뷰 및 GPT 판정 보존: `CLAUDE_MSC_SKILL_PATCH_INDEPENDENT_REVIEW_RESULT_FOR_GPT_r0001_20261116.md`, `GPT_MSC_PATCH_CLAUDE_REVIEW_DISPOSITION_r0001_20261116_KST.md`. 재리뷰/승인 요청 생성 없음.
- 산출물은 GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / branch `main`의 **같은 Work** `candidates/`에 새 버전으로 게시(커밋 `395dafd4c2aa2378444b78e897829ab010198ca4`, 이전 후보 변경·삭제 없음).

## 패키지 실제 결과

| 스킬 | 신규 ZIP (위 Work 상대 경로) | 바이트 | SHA-256 | 원격 Git blob |
|---|---|---:|---|---|
| `doc-converter` | `candidates/doc-converter_v0_2_24_1116.zip` | **215092** | `2ef0929bc0a80a1c0aca67bf3c8fc02f967bddba223b45c27807c363e96229f7` | `f740c1f2578403e80faa239694fe8c419468d320` |
| `work-ledger-kernel` | `candidates/work-ledger-kernel_v0_7_41_1116.zip` | **413709** | `48d1bf5e24c613e7e0ba04df9946c427c5d1ee39d8d16204966afff07e93497b` | `c62d0783200b4786097a98cff2d874a971f1a364` |

원격 main에서 후보 ZIP을 다시 읽고 Git blob·실제 파일 크기 **PASS**. SHA-256은 격리 CI 생성·무결성 검사 원본 바이트 기준이며 ZIP을 바이트 그대로 Git blob으로 업로드했음.

## 독립 리뷰 지적 → 수정 결과

| 지적 | 실제 변경 |
|---|---|
| B1 Kernel `.svg` 허용 후 `name_for()` 미지원으로 전체 `export_docs` 실패 | `artifact_names.name_for()`의 `.svg` 및 기존 정본 이름 탐색 확장. `work_ux.export_docs()`는 명시적 MSC 역할/경로 SVG만 기존 evidence export로 재사용하고 무관한 SVG는 이전처럼 skip. MSC 대용량 SVG는 예외 처리, 직접 열릴 수 있는 SVG의 script/외부 href/이벤트 속성 차단 |
| M1 `--view-mode` 관리 정책 미연결 | `skillsilent/policy.json`의 `msc-package`·`msc-scenario-build` 액션에 값 플래그 등록(없던 scenario-build 액션은 package 정책 기반 최소 연결). `cmd_scenario_build()`에서 IR에 명시된 `view_mode` 전달, CLI 지정 우선. default ISSUE 유지 |
| M2 Windows `Init/init` 중복 파일 덮어쓰기 | 파일명 `casefold()` 기준 중복 차단 유지, collision `DIAGRAM_NAME_DUPLICATE` 실패 |
| m1 내부 버전·패키지 해시 목록 불일치 | VERSION, SKILL.md, VERSION.md(doc), skillsilent/manifest.json(doc), .skill-release.json, doc `PACKAGE_CONTENTS.sha256` 전 회원, Kernel `MANIFEST_SHA256.json` 갱신 |
| m2 한글 NFC/NFD 비멱등 | 시나리오 이름 정제 후 NFC 정규화, SHA 접미사 계산·중복 확인 전에 적용 |
| m3 Phase 버튼 누락 비가시 | HTML 뷰의 기존 manifest에 `html_phase_buttons` 보고(요청/활성/누락 이유), 중복·없는 SVG 단계는 점프 버튼 비활성 상태 표시 |

`l1-fix-workflow v1.6.69`, `code-analyzer v0.15.3`: 기존 역할 재사용, 신규 수정·버전 발행 없음. `l1-knowledge-updater`와 업무 writer G0 검토는 별도 범위이며 이번 후보에 의존성 주입하지 않음.

## 실제 자체시험

- [GitHub Actions 격리 빌드·검증 Run 43799762374](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43799762374), Python 3.11, 상태 **SUCCESS**. 이 실행은 사용자 지시를 따른 **개발자 자체시험**이며 두 번째 독립 리뷰 아님.
- 입력 ZIP SHA pin·원본 CRC **PASS**. 출력 ZIP 전체 CRC, 원격 업로드 동일 blob·크기, 중앙 디렉터리 멤버 중복·모든 Python 구문 컴파일 **PASS**.
- 새 ZIP 내부 무결성 원장 **전 회원 일치 PASS**(doc converter 90 archive members, Kernel 166 archive members).
- 수정 코드 **실행 표적 테스트 7/7 PASS** (doc converter 4, kernel 3). Converter 대소문자 충돌 hard-fail, NFC/NFD 안정성, 정책 JSON 등록, Phase 미발견·중복 보고; Kernel SVG 게시 이름 수용 및 SVG 안전 필터 실행.
- **미검증/보류:** 실제 등록 Evidence가 있는 Work의 `export_docs` 소형 SVG 게시·대용량·무관 SVG 실행 경계 통합시험, **실제 skillsilent runner** end-to-end, Python3.10 대상 수정본 전용 실행시험, 기존 전체 pytest, 실제 PlantUML 렌더·브라우저 host CSP/링크, 그룹 writer의 `published_path`/원격 readback 및 업무 호스트 E3. 이전 리뷰에서 확인된 실패→수정 PASS의 **전체 통합 증거는 아님**.
- 두 새 ZIP은 `development_not_for_deployment`; **PUBLIC `wonhwipark/L1Work` 루트 배포·Skill-Updater/업무 호스트 설치·Knowledge 게시/운영 LIVE 미실행**. 이 지침 범위를 넘는 전파·운영 활성화 승인이 아님.

## 리뷰 횟수·완료 경계

- `INDEPENDENT_REVIEW_CYCLES=1`, `ADDITIONAL_REVIEW_REQUESTS=0`; 별도 Claude Code 후속 리뷰 수행·요청 없음.
- `SOURCE_PATCHED=PASS`, `CANDIDATE_PACKAGED=PASS`, `NEW_TARGETED_SELF_TEST=PASS`, `NEW_INDEPENDENT_REVIEW=NOT_RUN_BY_USER_DIRECTION`, `PUBLIC_RELEASE=BLOCKED_PENDING_HOST_E3`.
- **NEXT_ONE_ACTION:** 사용 가능 업무 환경에서 실제 기존 Evidence/skillsilent/HTML 게시 계약을 설치 전에 read-only G0로 대조하고, 새 ZIP의 실제 Work 통합시험·링크 readback 결과를 기록. 사용자가 제한한 리뷰 1회는 재개하지 않음.
