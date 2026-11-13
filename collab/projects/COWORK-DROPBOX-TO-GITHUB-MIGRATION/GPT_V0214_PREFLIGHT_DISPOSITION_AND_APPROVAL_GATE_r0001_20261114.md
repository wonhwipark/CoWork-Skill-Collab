# GPT v0.2.14 LIVE 직전 원샷 사전검증 판정 및 최소 승인 게이트
작성 2026-11-14 KST · r0001
PRIVATE repo `wonhwipark/CoWork-Skill-Collab`, branch `main`
Exact path `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_V0214_PREFLIGHT_DISPOSITION_AND_APPROVAL_GATE_r0001_20261114.md`
WORK `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
**GPT_DISPOSITION=ACCEPT_WITH_CHANGE; INDEPENDENT_REVIEW=PENDING_APPROVAL; ACTIVE_PROVIDER=NONE; MIGRATION_NOT_CUTOVER.**

## 1. 기준 원문과 확인 범위
- `CLAUDE_GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT_FOR_GPT_20261114.md` (GitHub PRIVATE main, 결과서 게시 commit `ad411255ce2a6678aa0f47517a7f0f468439230e`), 최신 `CURRENT.md`/`TRACKER.json`.
- `review-inputs/REV-COWORK-V0214-20261114/REVIEW_MANIFEST.md` 및 `diff_v0_2_13_to_v0_2_14.patch`, `source/skill_collab_watcher/state_store.py`, `source/skill_collab_watcher/orchestrator.py`, `source/tests/test_try_claim.py`를 GPT가 GitHub PRIVATE에서 직접 조회해 정적 점검. ZIP 자체의 raw bytes/ZIP CRC/Windows 실행은 이번 GPT 세션에서 직접 재현하지 않음. 패키지 SHA/크기·원격 raw 검증은 **Windows Claude 자체 보고** 기준.
- 리뷰 ZIP `skill-collab-watcher_v0_2_14_1114.zip`, 파일별 고정 commit 링크는 `CLAUDE_GITHUB_LIVE_ONE_SHOT_PREFLIGHT_RESULT_FOR_GPT_20261114.md` §5와 manifest §1에서 확인. ZIP remote SHA-256 (개발자 보고) `3a221dcdb22ba75208a60ca555b0ee75866313a591148b1f482b7cbb6aa0b367`, 219663 bytes, 87 ZIP entries. 새로운 게시·모델 호출은 이 판정의 결과가 아님.

## 2. 항목별 판정
1. **실제 결함 수정 수용**: `orchestrator.py`의 무조건 `update_job_state(CLAIMED)` 호출이 `store.try_claim(final.processing_key)` CAS로 대체됨. `state_store.py`의 `UPDATE jobs SET state='CLAIMED', attempt_count=attempt_count+1 WHERE processing_key=? AND state IN ('DISCOVERED','WAIT_INPUT','VALIDATED','AUTH_REQUIRED')`는 `isolation_level=None` SQLite 연결에서 단일 autocommit SQL이므로 같은 processing_key에 두 스캔이 동시에 실행해도 오직 한 번만 상태 전이가 가능한 구조. 패배 프로세스 리뷰 발송 0. GPT 직접 확인은 **정적 코드검토**, 테스트 성공 수치는 `SELF_TEST_REPORTED`.
2. **HOST_ISOLATED E2E**: 9개 ×3 PASS, 클로드 스텁/루프백 GitHub 서버 사용, signed approval/CLI/RealReviewRunner/상태처리 실제 경로라는 개발자 보고를 수용. 이는 운영 LIVE E2E가 아님. 제품 전체 666 PASS /13 SKIP(venv), 운영 interpreter 551 PASS/20 SKIP(crypto 의존 시험 SKIP), 원격 ZIP 풀어 666 PASS/13 SKIP도 **개발자 자체 보고**. 실제 운영 Python/venv에 Ed25519/cryptography가 있는지는 전환 전에 간단히 확인해야 함.
3. **리뷰 입력 준비**: PRIVATE의 ZIP·diff·소스 6개·manifest 게시 및 원격 raw byte/크기/CRC 검증 자체 보고; GitHub의 텍스트 파일 직접 조회는 성공. 회사 L1 원본 코드와 결별된 CoWork 자체 리뷰자료는 사용자 승인된 범위. 신규 PUBLIC L1Work 게시 없음.
4. **독립 리뷰**: `NOT_RUN / PENDING_APPROVAL`, 모델 호출 0, 비용 $0. 이 상태에서 독립 리뷰 PASS 또는 LIVE READY 선언 금지.
5. **운영 준비**: 실제 GitHub SHADOW 미실행(원문 텍스트 토큰 요구 vs JSON 파일), 실제 notifier 연결과 운영 DB 안전 백업/복원 리허설 미수행, 감시기용 단일 fine-grained Contents Read/Write 인증 미설치. 후보 v0.2.14 운영 설치 미실행. `ACTIVE_PROVIDER=NONE` 및 기존 Dropbox 이력 보존 유지.

## 3. 독립 리뷰의 집중 점검 항목 (무분별한 추가 개발 금지)
- `try_claim` CAS가 **동일 processing_key**를 보호하는 것은 확인. 그러나 `find_logical_job`/policy revision 변경으로 processing_key가 달라지는 동시 작업, `scan`과 `watch`의 경합, `seal_interrupted(exclusive=True)`와 다른 프로세스 소유권 경계는 별도 리뷰에서 확인.
- `orchestrator._check_ceilings`의 일일 요청·비용 한도 검사는 `try_claim` **전에 별도 SQL 조회**함. 서로 다른 processing_key가 병렬 처리될 때 공동 한도 초과를 막는 원자적 예약/상위 락이 있는지는 현재 조회한 변경분만으로 확인 불충분. 리뷰어가 코드와 실제 호출 경로를 확인하고 필요할 때만 최소 delta 수정을 권고. 본 항목은 **위험 후보 / NOT_CONFIRMED_DEFECT**로 기록하며 검증 없는 심각 결함 확정 금지.
- `POLICY-STATIC-V1` 리뷰에는 위 항목 + GitHub 전송 복구·Windows `claude.cmd`/인코딩·토큰 원문 형식 적합성만 집중. 수정으로 ZIP이 바뀌면 해당 새 아티팩트의 재리뷰 상태는 별도 판단; 기존 PASS를 옮겨 적지 않음.

## 4. 단일 사용자 협업 기준의 최소 승인 제안
**지금 결재할 묶음** (사용자의 명시 승인 답변 필요):
A. 독립 Claude 리뷰 `REV-COWORK-V0214-20261114`의 **1회 유료 실행**, 정책 `POLICY-STATIC-V1`, **최대 $1.00**, effort=medium, 현재 게시/확인된 ZIP 해시·commit을 고정. 기존 watcher의 signed approval이 필요하여 **같은 Windows PC에서 단일 운영자 Ed25519 개인키/신뢰 루트 생성(암호화 보호) + `trust_root_independence=warn` 단일 사용자 운용 위험 수용**을 권고. 별도 승인자 PC·로컬 LLM·SU-L1 신규 연계 강제하지 않음. `warn`을 통한 신뢰 경계 완화는 실제 A안 명시 승인 뒤에만 적용; 무서명 검증 우회 금지.
B. **감시기 전용 저장소 1개** fine-grained PAT **Contents Read and write** 발급·안전 설치와 JSON 형식 불일치 수정(기존 JSON credential을 직접 로그/문서에 노출하지 않고 감시기가 읽는 원문 토큰 형식 또는 검증된 parser). 개발자 `gh` 광역 자격을 무작정 전면 교체하지 않음. 기존 classic 토큰은 새로운 자격 정상 동작과 다른 사용처 영향 확인 후 안전하게 비활성화(독립 승인/권한 범위 안에서). **이번 승인 전 발급/교체 실행 금지**.
- 두 승인 각각 별도 행위임. 직접 사용자 승인 없이 유료 호출/키 발급/PAT 생성 또는 토큰 파일 내용 출력 금지. 같은 PC 단일 승인 방식은 사용자 요구에 따라 보안 복잡도를 줄인 선택이며, 같은 관리자 환경의 독립 보안까지 보장하지 않음.
**다음 최종 승인 묶음** (A/B 확인 및 실제 독립 리뷰 결과 반영 이후):
C. **Windows 운영 교체 및 GitHub LIVE 전환** — v0.1.5 → 후보 v0.2.14(리뷰 후 수정될 수 있음), 운영 DB/이력 backup·restore dry-run, notifier 실제 연결, GitHub SHADOW(비모델·무쓰기) 검사, 최소권한 인증, rollback 리허설, 단일 provider와 비용/중복 확인 후 사용자의 별도 LIVE 승인. 이 결재는 **이번 문서로 선승인하지 않음**.

## 5. 다음 한 동작
사용자에게 `A안(동일 PC 서명키+warn) / POLICY-STATIC-V1 최대 $1 독립 리뷰 1회`와 `B안(저장소 전용 fine-grained PAT 1개 설치·형식 호환)`을 한 질문으로 묶어서 승인 받을 것. 승인되면 Windows Claude Code가 **하나의 작업**에서 해당 권한·실 리뷰 호출·결과/영수증 원격 게시·GPT 판정 입력을 수행. 리뷰 중 결함 발견 시 필요한 최소 수정·시험은 같은 작업 안에서 진행하되 *재리뷰는 새로운 명시 요청*만 가능. 운영 LIVE 실행은 아직 금지.
