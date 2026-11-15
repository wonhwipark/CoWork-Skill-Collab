# TD-002 — 현 세션 읽기 경로·Work 재개 선택 점검

- 일자: 2026-11-15 KST
- Work: `COWORK-SKILL-DISCOVERY-20261112-001` / 공통 투두 `TD-002` / 상세 V06·V07
- 입력: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`의 `main`; 공통 맥락 브리프의 목적별 CURRENT 링크와 각 CURRENT 최상단을 읽음.
- 점검 범위: **현 대화 세션 내 읽기 경로 검증(V06)**. 새로운 ChatGPT 대화창 생성이나 실제 새 창에서의 재개 시험(V07)을 대신하지 않음.

| 요청 의도 | 선택한 기존 Work | 최신 사실·다음 한 행동 |
|---|---|---|
| NR L1 Tx 실제 코드 분석·Init RACH 결과 | `NR-L1TX-CODE-ANALYSIS-20261115-001` | PUBLIC v0.4.38 게시·원격 검증은 PASS; Linux 설치·MCP 결과 readback NOT_VERIFIED, 실제 코드 분석 NOT_RUN. 다음: 기존 허용된 Linux Agent 경로에서 동일 Job ID/설치 SHA·Receipt 확인 |
| Job-list 신규 무모델 Smoke 실행 준비 | `JOBLIST-SMOKE-20261114-001` | 격리 Worker 자체시험 3 PASS, 전체 후보 ZIP/배포/호스트 E2E 미실행. 다음: 로컬 debug 근거 확인 후 격리 패키징. 기존 소비 Job 재실행 금지 |
| 자동 서명·READY 개선 작업 재개 | `COWORK-AUTO-APPROVAL-20261115-001` | v0.2.21 후보 GPT 정적 판정 BLOCKING 2, 자동 서명 OFF. 다음: Windows Claude Code의 B1/B2 보완 및 시험. 유료 리뷰와 설치는 별도 승인 경계 |
| 기존 협업 provider의 LIVE 운영 상태 | `COWORK-DROPBOX-TO-GITHUB-MIGRATION` | 최신 정본에서 GITHUB 단일 LIVE, v0.2.20 호스트 보고·리뷰 근거 수용. 다음: 정식 신규 유효 REQUEST+READY 첫 실전 관찰. 자동 승인 개선 완료와 동일시 금지 |

- 판정: `SESSION_ROUTING_CHECK=PASS` (4개 목적의 동일·분리 Work 선택 및 최상단 현재 요약 읽기).
- `V07_ACTUAL_NEW_CHAT=NOT_RUN`. 동일 대화의 검증으로 실제 새 창 자동 선조회·맥락 연속성을 입증하지 않음.
- 운영 안전: 기존 Work 재사용, 다른 Work 합치기 금지, 승인 없는 모델 호출/REQUEST/READY/Job 재실행/호스트 변경 0.
- 다음 한 행동: 실제 새 대화창에서 공통 지도 → 해당 CURRENT → 범위·승인·NEXT_ONE_ACTION 선택 여부를 확인하고 V07을 PASS/FAIL로 판정. 그때까지 TD-002는 `작업 연결` 상태 유지.
