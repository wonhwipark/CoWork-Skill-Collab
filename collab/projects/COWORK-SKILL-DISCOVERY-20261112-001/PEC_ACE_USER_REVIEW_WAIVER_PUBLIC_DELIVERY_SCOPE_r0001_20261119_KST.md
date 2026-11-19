# PEC·ACE 두 스킬 — 사용자 독립 리뷰 생략 및 PUBLIC 전달 한정 판정 r0001

- 기준: 2026-11-19 KST, 기존 Work `COWORK-SKILL-DISCOVERY-20261112-001`
- 최신 사용자 명시: **“리뷰스킵하고 스킬 업데이트후패키지 l1work 에 올려줘”**.
- **범위 내 사용자 직접 지시로 확인한 생략:** 이번 한 번, `code-analyzer` PEC-HOP v0.15.4 및 `l1-fix-workflow` ACE v1.6.74 두 신규 ZIP의 **Windows Claude Code 독립 코드 리뷰만** 생략. `INDEPENDENT_CODE_REVIEW=SKIPPED_BY_USER_REQUEST`. 완료/PASS/영수증/모델 호출을 가장하지 않음. 이전 설계 리뷰 R1 CLOSED 및 Windows 요청 `POLICY_COST_MISMATCH` BLOCKED 역사 무손실 보존.
- **명시적으로 생략하지 않은 것:** 최신 source pin·시큐리티/민감정보·full ZIP CRC/경로/심링크·hash manifest/버전/기능 회귀·기존 소스 보존·실제 패키지 byte 재현성·공개 저장소 경로 충돌·원격 raw bytes SHA 검증. 본문만으로 이런 조건을 PASS로 판정하지 않음. 본문 자체는 최종 릴리스가 아님.
- **기존 정책과의 관계:** 기존 `collab/ops/CONTRACTS/PUBLIC_RELEASE_GATE.md`의 Job-list v0.4.38 사후 리뷰 허용을 PEC·ACE에 일반화하지 않음. 이 파일은 사용자 **새로운 명시적 예외 지시를 이 Work/두 ZIP의 1회 배송 의사로만** 기록하며 일반 릴리스 정책·운영 승인·서명·READY/유료 모델 권한을 전혀 바꾸지 않음. 필수 비리뷰 QA 미충족 시 `PUBLIC=BLOCKED_NOT_POSTED` 유지.
- **범위상 제한:** 두 스킬에는 기존 선택적 읽기 전용 PEC/ACE 경로만 추가. ACON, Kernel, Knowledge Updater, skill-updater·Git/P4 writer·업무 원본/Knowledge 내용·Windows watcher/LIVE 설치 변경 0. 업무 Linux 원본·로그·호스트 시험·비민감 요약이라도 외부 반출 금지(NO_EXPORT). PUBLIC ZIP 존재가 업무 설치/호스트 검증 PASS가 아님.
- **개발 기준:** Private CI run `44453442652`, `code-analyzer_v0_15_4_1119.zip` SHA256 `ca1e4cd2d89afd5bf35ce49cab4d2034e93650ffb50a3e713db28eb65b758d21` / 515271 B / 12 PASS; `l1-fix-workflow_v1_6_74_1119.zip` SHA256 `546936c3856ef19e212ecea3076446d7c75d89db6fcb5ff34df77981024edcd6` / 760040 B / 10 PASS. **이 바이트는 development_not_for_deployment이므로 그대로 L1Work에 게시 불가.** 새 USER-REVIEW-WAIVED 최종 릴리스 ZIP은 metadata 변경 및 전체 매니페스트 재해싱 후 새 SHA 기록 필수.
- **정본 배포 위치:** `wonhwipark/L1Work`, branch `main`, **루트** 신규 ZIP 2개만. 기존 공개 ZIP 덮어쓰기 0. PRIVATE CI staging은 PUBLIC 릴리스와 구별. 사용자가 공개 배송을 지시했더라도 원격 SHA 확인 실패는 `UNVERIFIED` 처리.
- **완료 보고:** 각 ZIP `PRE_RELEASE_NON_REVIEW_GATES=PASS/FAIL`, `REVIEW=USER_SKIPPED`, `PRIVATE_STAGED=PASS/NOT_POSTED`, `L1WORK_PUBLIC_POSTED=PASS/NOT_POSTED`, `HOST_INSTALL=NOT_EXTERNALLY_OBSERVABLE`로 구분.
