# Windows Claude Code 독립 코드 리뷰·Windows 시험 인계 — cost-only 자동 승인 v0.2.24

- 날짜: 2026-11-17 KST
- 협업 저장소: PRIVATE `wonhwipark/CoWork-Skill-Collab`, 정본 branch `main`
- **같은 Work:** `collab/projects/COWORK-AUTO-APPROVAL-20261115-001`
- 현행 결정: `GPT_COST_ONLY_AUTO_APPROVAL_POLICY_r0001_20261117_KST.md`
- 개발 브랜치: `dev/auto-quota-cost-only-20261117`
- 개발 후보: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/candidates/skill-collab-watcher_v0_2_24_1117.zip` (282548 B, SHA-256 `3c78699b734d88202a34ef5fd430f5f278ab1692a437b6affb6b6c64d24ca360`; ZIP 바이트 변동 시 최신 검증 결과 우선)
- 고정 기반: PRIVATE `collab/packages/skill-collab-watcher_v0_2_23_1115_DEV_NOT_FOR_DEPLOYMENT.zip`, SHA-256 `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`.
- 개발 빌더·회귀시험: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/dev/build_v024_cost_only.py`, `dev/patch_v024_tests.py`
- GitHub 개발 CI: `https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44002235785`

## 독립 리뷰 요청 범위

원본 ZIP과 후보 ZIP **실제 바이트 SHA/ZIP CRC**, Python 코드 diff를 독립적으로 읽고 검토. 개발 세션의 같은 코드 자체점검과 독립 리뷰를 구분.

검증 목표: `max_day_calls`/일·월 호출 횟수 기반 거절을 **모든 허용 경로에서 제거**, 표시·정책·원자 예약 일치. 과거 JSON의 `max_day_calls` 입력은 호환 목적으로 무시되며 실제 횟수 승인 한도가 되어서는 안 됨. 다만 `max_calls=1`·`attempt=1`·`auto_claim` 유일 키 및 N1 원격 예약/동시성·중복·REVIEW_UNCERTAIN·READY 마지막 게시·SOURCE_PIN·signature 검증은 동일하게 유지되어야 함.

예산 게이트는 보호된 로컬 위임 USD 1/요청·USD 3/KST 일·USD 10/KST 월을 엄격히 유지. 이전 리뷰 디스패치 비용/최대 예약 비용의 KST 집계, 동일 ID 1회, 타 요청 동시 경합, 비용 한도 초과 전 모델 호출 0을 직접 확인. `UNCERTAIN`/종결 예약의 비용은 확정적 0회 증거 없이 자동 반환하지 않는다. SQL `auto_claims`의 기존 이력·WAL·SHM·감사 추적은 보존.

## 실제 시험과 증거

기존 개발 CI는 Linux 대상 `25 PASS/2 SKIP` 표적 및 `578 PASS/30 SKIP/1 제외` Linux 지원 전수 시험. Windows 전용 Lock·SHADOW 전체와 운영 Python 3.11.9, 실제 Windows 설치본 비교는 별도 **NOT_RUN**.

Windows Claude Code에서 실제 운영 트리 수정 없이 **격리 복사/Windows 임시 디렉터리**로 ZIP을 검증하고 전체 pytest(운영 인터프리터/venv), 신규 비용 기반/3건 이상 호출/중복·실패/경합의 실제 실행시험, SHADOW에서 원격 게시·유료 모델·Telegram 발송 0, 롤백 리허설을 점검해 결과 작성. 독립 코드 리뷰가 개발자 자체시험에 종속되지 않도록 리뷰어·입력·판정·근거 기록 분리.

결과를 PRIVATE main 같은 Work의 `CLAUDE_COST_ONLY_V024_INDEPENDENT_REVIEW_RESULT_FOR_GPT_20261117.md`로 게시하고 SOURCE PIN·테스트 개수·PASS/FAIL/SKIP/NOT_RUN·후보 SHA/바이트·차이점·권고·다음 1동작 및 원격 readback을 보고. 기존 `CURRENT.md` 상단만 최신 결과로 갱신.

**중요:** 이 문서는 REQUEST/READY가 아니며 유료 Claude 모델 호출, 보호 키 서명, Windows watcher 설치·DB 변경·provider 전환을 승인하거나 실행시키는 신호가 아님. 독립 리뷰 실행 비용이 별도로 드는 경로는 유효한 기존 사전 위임·비용·승인 범위와 정확히 연결된 경우에만 처리. 허용 경로가 없으면 `INDEPENDENT_REVIEW=NOT_RUN`로 남기고 단독 시험·리뷰 입력 패키징을 계속. 동일 실패 REQUEST 재큐잉·LIVE 임의 교체 금지.
