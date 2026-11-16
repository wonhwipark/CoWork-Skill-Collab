# GPT 판정 — MSC 두 개발 스킬 독립 패치 리뷰 r0001 (2026-11-16 KST)

- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`.
- 기준 독립 리뷰: `CLAUDE_MSC_SKILL_PATCH_INDEPENDENT_REVIEW_RESULT_FOR_GPT_r0001_20261116.md` (Windows Claude Code 별도 대화형 코드 리뷰; commit `5595d5fbee4de16757070841014f44faa190af49`), 수행 증거 `CLAUDE_MSC_SKILL_PATCH_REVIEW_EXECUTION_EVIDENCE_r0001_20261116.json` (commit `a78c8a010915217787a075b30f0c24fbe103d7c3`). GitHub PRIVATE main 원격 파일·commit 경로 조회 완료. 감시기 REQUEST/READY 경로의 공식 유료 리뷰와 구분.
- 고정 입력: commit `29aadbaeb5245f7a811c3050160c10cddce46954`; `doc-converter_v0_2_23_1116.zip` SHA-256 `43805ae0ce1b08205125441f383f6bdfc6f114ef53bb2609295827f10b1ce23e`; `work-ledger-kernel_v0_7_40_1116.zip` SHA-256 `b8077fd717f326fb7bc556407b8e8b8a7f32a580e143ec3a6d646d3b1e9df7ce`.
- **GPT 최종 판정: `REVISE / DEPLOYMENT_BLOCKED`**. BLOCKING 1, MAJOR 2, MINOR 3. 이전 격리 CI Python 3.10/3.11 각 19 PASS 및 Chromium smoke PASS는 실제 사실이나 코드 행위 회귀를 놓쳤으므로 후보 배포 게이트의 근거로 충분하지 않음.

## 지적별 판정·최소 수정

| 리뷰 지적 | GPT 판정 | 필요한 변경과 회귀 증거 |
|---|---|---|
| B1 Kernel SVG export 전체 실패 | **수용, BLOCKING** | `artifact_names.py::name_for`에 승인된 `.svg` 게시 이름 규칙을 최소 추가하고, `work_ux.py`의 copy·크기 초과 거부 적용 Evidence scope를 기존 MSC 미리보기 요구에 맞게 제한. 실제 `export_docs` 동작 시험: 기존 `.md` 무회귀, 작은 SVG 게시·hash/`published_path`, 큰 SVG 예외, 무관 SVG 처리, 동일 입력 재실행. 구 v0.7.39 정상/구 후보 v0.7.40 FAIL → 수정본 PASS 순서로 재현 |
| M1 converter `--view-mode` 정책 미연결 | **수용, MAJOR** | `skillsilent/policy.json`의 두 명시 액션에 최소 허용 플래그를 반영하고 `scenario_ir_adapter.py`의 인자 전달 보완. 직접 CLI와 정책 경유 각각 ISSUE default·PROCEDURE_FEATURE opt-in 시험, 관리 정책 fail-closed 유지 |
| M2 Windows 대소문자 충돌 | **수용, MAJOR** | `name.casefold()` 기준 파일명 중복 검증을 부가해 `Init/init`이 `DIAGRAM_NAME_DUPLICATE`로 거절되도록 수정. Windows 파일 2→1 무음 덮어쓰기 회귀 시험 |
| m1 메타/해시 불일치 | **수용, 출시 게이트** | `PACKAGE_CONTENTS.sha256`, `MANIFEST_SHA256.json`(해당 시), `VERSION`, `VERSION.md`, `SKILL.md`, `skillsilent/manifest.json`, `.skill-release.json`의 기준 값·실제 파일 바이트·필수 멤버를 릴리스 빌드에서 검증. 설치기 소비 여부는 G0 별도 확인, 불일치 방치는 금지 |
| m2 NFC/NFD 비멱등 | **수용** | 파일명 해시·중복 검사 전에 `unicodedata.normalize("NFC", ...)` 적용. NFC/NFD 동일 이름의 stable ID 및 재게시 경로 일치 시험 |
| m3 Phase 버튼 누락 비가시 | **수정 수용** | `html_phase_buttons` 또는 기존 manifest 표현을 사용해 정상/누락 n/m·이유를 기록. 새 상태 엔진·스키마 확대 불필요. 실제 PlantUML divider와 B viewer 브라우저 회귀·fallback 확인 |

### 기타 판단

- `code-analyzer v0.15.3`와 `l1-fix-workflow v1.6.69`: **REUSE/CONNECT 유지**. 이번 리뷰로 새로운 소스 패치 필요성이 확인되지 않음.
- `l1-knowledge-updater`, 그룹 writer, Knowledge 게시 소유자·마커, 브라우저 호스팅 URL 및 `published_path`: **G0 미확인 보류**. 이번 패치로 임의 구현·업무 자료 복제·지식 쓰기를 추가하지 않음.
- Windows reviewer의 Edge CDP 테스트는 사용자 지정 HTML 문구·XSS·Phase click에서 **직접 실행 근거**, 반면 실제 PlantUML 렌더·업무 host E3·전체 pytest는 **NOT_RUN**. 해당 경계를 유지.
- 개발 세션의 코드 수정/자체시험과 수정 이후 **별도 Claude Code 독립 재검토**를 분리. 기존 리뷰 결과를 수정본의 PASS로 재사용하지 않음.

**다음 한 행동:** PRIVATE 기존 Work에서 두 ZIP의 검증된 B1·M1·M2와 출시 메타/Unicode/표시 결함을 동일 변경 묶음으로 최소 패치 → 격리 Python/Windows 실제 export 및 정책 경유 재시험 → 새 `development_not_for_deployment` ZIP 2개/바이트 해시/실패→성공 근거 게시. 이후 수정자가 아닌 Claude Code 재리뷰를 새 유효 요청으로 처리. PUBLIC 최종 ZIP·호스트 설치/Knowledge write 및 LIVE 변경 **NOT_RUN/BLOCKED**.
