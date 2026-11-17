# MSC 두 진입 후속 검증 · Kernel 링크 수정 · 재현 가능한 후보 — r0001
- 작성: 2026-11-18 KST / 기존 Work: `L1-WORKSPACE-RAG-20261111-001`
- 사용자 후속 승인: “그래” — 기존 R1 설계 이후 허용된 개발·합성 검증·배포 준비. 기존 완료된 설계 리뷰 재요청/재호출 금지.
- 판정: **DEVELOPMENT_AND_SYNTHETIC_TEST=PASS; PUBLIC_RELEASE/HOST_INSTALL=BLOCKED** (미확인 writer G0, 업무 E3, 신규 코드 독립 리뷰 및 상세 원본 링크 재매핑).
- 전 단계 원문: [기존 구현 결과 r0001](GPT_MSC_DUAL_ENTRY_FOLLOWUP_IMPLEMENTATION_RESULT_r0001_20261118_KST.md), [설계 GPT ACCEPT_WITH_CHANGE](GPT_MSC_DUAL_ENTRY_R1_DISPOSITION_r0001_20261118_KST.md). 두 문서·리뷰 요청·원본 고정 이력 보존.

## 1. 재현한 결함과 최소 수정
1. **검증 전 Kernel 0.7.43 실함수 재현:** Synthetic Work에 doc-converter HTML과 MSC_VIEW.md를 모두 `render_output/utility` Evidence로 등록하면 기존 Kernel exporter가 각각 SHA/파일 경로를 보존해 `works/<work_id>/artifacts/analysis/분석_...__<evidence_id>.<ext>`로 저장. 그러나 원래 Converter 상세 MD의 상대 링크 `01_AS_IS.html`은 원본 파일명에 고정되어 게시 후 **BROKEN**. 단순 ZIP/static 검증으로 발견할 수 없는 기존 링크 불일치. 첫 probe에서 MD를 `asis_msc/utility`로 등록했을 때는 registry가 거부했고, 실제 허용 `render_output/utility`로 바꿔 재현.
2. **Kernel v0.7.45 최소 변경:** 기존 `work_ux.py`의 `artifact_entries`/SHA 확인이 끝난 doc-converter HTML Evidence의 `published_path`만 수집. 기존 생성된 Work-root `MSC_VIEW.md`에 `MSC HTML 다운로드` 링크를 추가하고 Converter의 상세 MD 링크는 `MSC 상세 원본`으로 명확히 표시. 기존 `write_communication`을 그대로 사용하므로 자동 생성물 해시·수동 수정 충돌 방어 계승. 원 Ledger Evidence·원본 상세 MD bytes·개인 `knowledge/`·그룹 writer·schema/FSM은 미변경.
3. **수정 후 실함수 합성 검증:** Work-root `MSC_VIEW.md`의 percent-encoded HTML 링크는 실파일과 일치 `root_link_ok=true`, SHA 게시맵 PASS, 반복 export 멱등 PASS, 사람이 안내 MD를 수정한 다음 재export해도 수동 편집 내용 보존 PASS. **원본 상세 Evidence MD 자체의 `01_AS_IS.html` 상대 링크는 의도대로 bytes 미수정이므로 여전히 BROKEN**. 사용자가 기본 열람하는 Work-root 안내에서 직접 HTML을 선택하는 연결은 복구했지만, 모든 상세 MD 내부 링크 정정·업무용 writer 링크 재매핑을 완료했다고 보고하지 않는다.

## 2. 스킬 개발 후보 (구버전 그대로 보존)
고정 원본:
- Converter PUBLIC `doc-converter_v0_2_26_1117.zip` SHA-256 `b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c`.
- Workflow PRIVATE `l1-fix-workflow_v1_6_70_1117.zip` SHA-256 `1e08302b6a533d2894101427f5a7bb94b43102e00a98f2c6e0b19f534a885ceb`.
- Kernel PRIVATE `work-ledger-kernel_v0_7_43_1117.zip` SHA-256 `80c955790aaa65f695c061f7ec2664bd1c7c5ba7e0a7534045960eea7fe2d5f6`.

| 후보 | bytes | SHA-256 | 개발 변경 |
|---|---:|---|---|
| `doc-converter_v0_2_28_1118.zip` | 169567 | `3fcd89d02aab9be4f29c8a49a9146de6561ce4d956f7397d1dc397bb8ebe6729` | ISSUE `--html-viewer` opt-in 유지, managed parser/policy 포함 |
| `l1-fix-workflow_v1_6_72_1118.zip` | 758427 | `0eb190e704d7e06d8bddf642bff858319fceb399814c83282a480502d377af02` | 기존 MSC handoff에 ISSUE HTML opt-in 계획 전달, 실행 권한 없음 |
| `work-ledger-kernel_v0_7_45_1118.zip` | 320195 | `1bccbbffeaafcefda27b75ca8f430e502bc8c2b475b63bd76425ca7ee1c5d7f8` | 실제 Work-root MSC 안내에서 게시된 HTML 경로 재매핑 |

세 ZIP 모두 `development_not_for_deployment`. 변경 없는 0.2.27/1.6.71 및 0.7.44 이전 후보와 코드 목적은 같지만 **재빌드 ZIP 타임스탬프가 비결정적**인 문제가 확인돼, 새 버전으로 분리하고 [고정 ZIP metadata writer](dev/reproducible_zip.py)를 적용했다. 기존 후보는 삭제·덮어쓰지 않음.

## 3. 시험 근거·재현성
- [PRIVATE main quality CI run 44129301281](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44129301281) **SUCCESS**, head `7c654243514de1b4005bc68daf51694bf87d5153`. Kernel/Converter+Workflow 각각 동일 입력을 연속 2회 빌드하고 3개 ZIP 모두 `cmp` byte equality **PASS**. SHA-256/ZIP CRC/경로 이탈·중복·manifest 전집합·버전 게이트 **PASS**.
- 실제 Kernel `record_evidence` → `work_docs_export` → 최종 artifact publish map/Work-root 안내 링크 경로 확인 **PASS**, `manual_edit_preserved=true`, `export_idempotent=true`. 원본 상세 MD 상대 링크의 `BROKEN`은 정직하게 보존.
- 개발 후보 직접 격리 pytest: doc-converter 주요 5개 MSC 테스트 파일 **28 PASS**. Workflow 두 scenario 모듈+MSC View 전체 **15 PASS**(Kernel 후보를 임시 동일 모듈 경로에 연결). 초기 Kernel dependency 누락 실행은 시험 수집 실패였고 의존성이 제공되자 모두 PASS. 전체 Converter 시험 명령은 환경 렌더러 관련 초과 시간으로 종료돼 `FULL_CONVERTER_TESTS=NOT_VERIFIED`; 위 28건을 전체 PASS로 확대하지 않음.
- 기존 R1 정적 설계 리뷰 `CLOSED`; **이 후속 코드의 새로운 Windows 독립 리뷰는 NOT_RUN**.
- Actions artifact: `msc-dual-entry-development-1118` (run 44129301281, artifact 14348323312, 2026-11-24 UTC 만료 예정). 영구 재생성 정본은 PRIVATE main의 pinned builders [Converter/Workflow](dev/msc_dual_entry_candidate.py) · [Kernel](dev/build_msc_kernel_html_links_r0001_20261118.py)와 [deterministic ZIP writer](dev/reproducible_zip.py). GitHub Actions artifact가 영구 PRIVATE ZIP 또는 PUBLIC 릴리스인 것은 아님.

## 4. 후속 검증 / 배포 차단
- `UPDATER_INSTALLED_SOURCE_G0=NOT_VERIFIED`: 업무 호스트 `l1-knowledge-updater` 최신 원문/실제 group/Workspace writer API·마커·승인·CAS를 조회할 권한/연결이 없음. PRIVATE의 접근 가능한 패키지만으로 대체하지 않음.
- `KERNEL_SYNTHETIC_WRITER=PASS`, `WORK_ROOT_VIEW_HTML_LINK=PASS`, `CONVERTER_DETAIL_MD_RELATIVE_LINK=BROKEN_BY_ORIGINAL_BYTES`. 기존 증거 원본 무변조 정책을 유지하며 본문 내부 상대 링크를 자동 수정하지 않음.
- `REAL_WORKFLOW_PROVIDER_RUNNER=NOT_RUN`, `BUSINESS_HTML_BROWSER_ACCESS=NOT_VERIFIED`, `UPDATER_PERSONAL_KNOWLEDGE_WRITE=NOT_RUN`, `GROUP_WRITER_G0_E3=NOT_RUN`, `INDEPENDENT_CODE_REVIEW=NOT_RUN`, `PUBLIC_RELEASE=NOT_POSTED`, `HOST_INSTALL=NOT_RUN`.
- 원본 재분석·모델/Job 재호출 없음. 기존 Guard `AUTO_SIGNING_UNCERTAIN` 이력과 LIVE 운영 계약 무변경.

**NEXT_ONE_ACTION:** 업무 GPT/호스트에서 기존 Updater·실 writer의 G0를 읽기 전용으로 대조하고, 별도의 비민감 합성 Work에서 승인된 writer로 HTML·설명 MD 게시 경로/Preview-HOLD·부분 실패를 확인. 불일치 상세 링크·호스트 E3가 해소되고 코드 독립 리뷰/배포 승인이 충족되기 전 PUBLIC 승격 금지.

## 5. 후속 CI fail-closed 확인
- 새 검사 코드 [test_msc_dual_entry_kernel_writer_probe.py](dev/test_msc_dual_entry_kernel_writer_probe.py)는 root HTML link·SHA mapping·멱등·수동편집 보존 조건이 FAIL이면 **CI exit 1**로 차단하도록 수정. 일시 진단용 원본 source dump 제거.
- [최신 PRIVATE main CI 44130067446](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44130067446) **SUCCESS**. 변경된 fail-closed gate에서도 전체 빌드 재현성/Kernel 합성 E2E/root link 검증 PASS. 세 ZIP의 내용·SHA-256은 위 표와 동일(동일 고정 입력). 기존 44129301281도 보존.
- 이는 설치·업무 G0/E3·독립 코드 리뷰의 대체 근거가 아니다.
