# 보유 스킬 18개 패키지 정적 확인

- 작성: 2026-11-12 KST
- 범위: 사용자 확인한 1~18번. 19번은 사내 GPT 협업을 통해 l1sw-dev-knowledge 스킬을 업데이트하는 사내 l1-knowledge-updater로 분리.
- PUBLIC source commit: `8ebd07c654f71cfc48a99c8abd01bdff9e644a8d`; PRIVATE 문서 기준 commit: `8d681d3b4daa37ccec42d0889a34121a031725fd`.
- 실제 확인: 17개 ZIP 원격 bytes 다운로드, Git blob 일치, ZIP CRC, SKILL.md UTF-8/이름/description·역할·관련 제목 및 필요한 MSC/예약 절 확인. 전체 구현·등록 action 지원 여부·실 API 동작을 검증한 것은 아님.
- 결과: PACKAGE_STATIC_REVIEW=COMPLETE_WITH_GAPS; 17 PACKAGE_SKILL_READ / skillsilent PACKAGE_NOT_FOUND. 독립 리뷰·설치·호스트·통합·모델/Job 호출 NOT_RUN.

## 패키지 바이트와 원문 위치

| 스킬 | 고정 원본 ZIP | bytes | SHA-256 | ZIP 내부 SKILL 경로 |
|---|---|---:|---|---|
| issue-analyzer | [issue-analyzer_v0_11_50_1102.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/issue-analyzer_v0_11_50_1102.zip) | 440609 | `76f5a233f050674132a5ed095fabbbe8265d64cab7f74d8149a413119de6ef03` | `issue-analyzer/SKILL.md` |
| code-analyzer | [code-analyzer_v0_15_2_1107.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/code-analyzer_v0_15_2_1107.zip) | 513811 | `9786bb0deb86fe5faed69f7e0c5a343e661af195d745a63e759b577c8b39a669` | `code-analyzer/SKILL.md` |
| code-fix | [code-fix_v0_4_19_20260928.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/code-fix_v0_4_19_20260928.zip) | 170699 | `f170df1e3a538249c9ceb14249d37f00c6a486da81e40f7ac29b84a4ba3e2944` | `code-fix/SKILL.md` |
| l1-fix-workflow | [l1-fix-workflow_v1_6_67_1110.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/l1-fix-workflow_v1_6_67_1110.zip) | 749307 | `a3c5f055845a0711692afea5b09c0e53e93dfba89adc792c0f2e73385899b30a` | `l1-fix-workflow/SKILL.md` |
| work-ledger-kernel | [work-ledger-kernel_v0_7_37_1103.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/work-ledger-kernel_v0_7_37_1103.zip) | 318845 | `8cf53c9ba14aed97b9be7b00db39ca5458ba0127ba00b9a1eef3533aba3a06a5` | `SKILL.md` |
| hld-composer | [hld-composer_v0_4_32_1008.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/hld-composer_v0_4_32_1008.zip) | 267227 | `baf21608d99453696959bacd864991ec010a6c2a276cb2c3f96f9a375f31ead0` | `hld-composer/SKILL.md` |
| doc-converter | [doc-converter_v0_2_21_1106.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/doc-converter_v0_2_21_1106.zip) | 155012 | `ef5d1d9e0b8847d2732d13ae387dc842bb8e90765952bc170345ea0a7b51039a` | `doc-converter/SKILL.md` |
| hld-code-compare | [hld-code-compare_v0_10_15_0825.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/hld-code-compare_v0_10_15_0825.zip) | 160883 | `c02296c33b8eadf77b2febe826f542a6c42572e3fc2b40b6fd621ea6deb501e3` | `hld-code-compare/SKILL.md` |
| hld-code-implement | [hld-code-implement_v0_5_14_0815.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/hld-code-implement_v0_5_14_0815.zip) | 121821 | `26cd3dae17f2359a4e202d9be69d00bbf32fd8f994506cfa2ff248c2a875abf9` | `hld-code-implement/SKILL.md` |
| l1-github | [l1-github_v0_3_56_1110.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/l1-github_v0_3_56_1110.zip) | 572047 | `f608b55978f03895b98f2e26dd31de0f3d1b6c72a5613c62a9b4036417993b84` | `SKILL.md` |
| p4-code-owner | [p4-code-owner_v0_6_7_1012.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/p4-code-owner_v0_6_7_1012.zip) | 106017 | `225490726a60741fcea689a74f956041262a6e1971a2684068daf960d5df0d71` | `p4-code-owner/SKILL.md` |
| l1-cl2git-merge | [l1-cl2git-merge_v0_3_5_1017.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/l1-cl2git-merge_v0_3_5_1017.zip) | 39005 | `7915487c98b1272e50c55931d30ddf79bff1dfacd0becb5862551ccdb351d8d8` | `l1-cl2git-merge/SKILL.md` |
| l1-sam-fixer | [l1-sam-fixer_v0_2_85_0929.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/l1-sam-fixer_v0_2_85_0929.zip) | 648748 | `117a3b5f7288e533eb5b34795bdd29f874b62a055fb271061489e21c08ca26e4` | `l1-sam-fixer/SKILL.md` |
| skill-updater | [skill-updater_v0_5_44_1027.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/skill-updater_v0_5_44_1027.zip) | 210717 | `0185778e44f7cce2d11a5e6b78f6e3f86e4b886ea07861984caa7fc7965b4fcd` | `skill-updater_v0_5_44_1027/SKILL.md` |
| skillsilent | 독립 ZIP 미발견 | — | — | 추가 확인 |
| job-list | [job-list_v0_4_36_1112.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/job-list_v0_4_36_1112.zip) | 1563658 | `cbe17dc15199593e2a9bce6aa2b8857c1f011336ebd2cd3d4c8ee3cce0eee3f6` | `job-list_v0_4_36/SKILL.md` |
| autotask-builder | [autotask-builder_v0_4_24_0918.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/autotask-builder_v0_4_24_0918.zip) | 116458 | `0f2765d6d779dedb42dc5fb1d2c379d3f5587f3b056646a4bd40ab1d547be698` | `autotask-builder/SKILL.md` |
| l1-cleanup | [l1-cleanup_v0_13_6.zip](https://github.com/wonhwipark/L1Work/blob/8ebd07c654f71cfc48a99c8abd01bdff9e644a8d/l1-cleanup_v0_13_6.zip) | 210536 | `b22b48e557064c6a272623333bd3f07e85f23734b5cfad74dd6dd9045e4179d4` | `l1-cleanup_v0_13_6/SKILL.md` |

## 발견·수용 판정

| 항목 | 판정·후속 |
|---|---|
| 기존 목록에서 빠진 6개 | code-fix, hld-code-compare, hld-code-implement, l1-cl2git-merge, l1-sam-fixer, l1-cleanup을 공통 목록에 추가 |
| MSC participant 정책 | doc-converter 0.2.21 원문에 SOURCE_PARENT_DIR_V1·TxMngr 병합·BCH/DRX 이름 정리·stack_group·scenario_trace 존재. 코드 근거 없는 폴더 병합 금지. 기존 표현 기능 우선 재사용 |
| 예약 책임 | autotask-builder는 OS 예약만 소유. Windows Task Scheduler/Linux user timer·공개 child launcher 지원 문서 확인. Job-list queue·child 설정·SkillSilent registry를 소유하지 않음 |
| skillsilent | 독립 ZIP 없음. 다른 ZIP의 policy/manifest 참조는 gateway 설치/정본·호스트 실행 증거가 아님. ADDITIONAL_CHECK_REQUIRED 유지 |
| l1-cl2git-merge | ZIP v0.3.5, SKILL front matter v0.3.4 관측. RELEASE_IDENTITY_UNRESOLVED; 최신/설치 정본으로 확정 금지 |
| l1-sam-fixer | ZIP v0.2.85, 제목 v0.2.82와 일부 신규 절 v0.2.85 공존. description의 옛 knowledge-manager 참조는 현행 지식 provider와 추가 대조 필요. 자동 alias 치환/호출 금지 |
| Workflow/Kernel | Workflow 개발 후보, Kernel SKILL 0.7.37-dev.1 관측. 공개 ZIP 존재를 운영 배포 가능 근거로 승격하지 않음 |
| Job-list | 선택 ZIP 0.4.36의 requests/one-shot-jobs.json에 jobs 1개 확인. SKILL 안에 과거 0.4.34 jobs=[] 설명 공존. 현재 패키지와 과거 설명 구분. 설치·실행 여부는 NOT_VERIFIED |
| 19번 사내 스킬 | USER_REPORTED_INHOUSE_SKILL. 역할·입출력 연동 참고만; 실제 원본·수정·검증은 사내 담당. 이번 18개 패키지 감사와 분리 |
| 18개 외 추가 패키지 | 공개 루트에서 추가 이름도 관측됨. 이번 사용자 확인 목록을 전체 보유 스킬의 완전한 목록으로 주장하지 않으며 자동 범위 확대하지 않음 |

## 다음 작업과 보존

실제 기능이 필요할 때 관련 SKILL의 필요한 reference/policy와 승인된 설치본만 확인한다. skillsilent 원본·위 버전/provider 불일치는 추가 확인 대상으로 남긴다. 새 API·엔진·schema·원장·예약을 만들거나 실행하지 않는다. 기존 r0005 인계/수행·Knowledge/metadata·운영 설치본·PUBLIC ZIP은 수정하지 않았다.

원격 게시의 commit/readback은 게시 후 CURRENT 및 검증 기록에 기록한다. 이 보고서 작성 자체는 독립 리뷰·배포·LIVE 전환의 PASS가 아니다.
