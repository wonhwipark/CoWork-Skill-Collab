# 발표용 대시보드 설계 리뷰 — LIVE 접수
2026-11-15 KST. PRIVATE wonhwipark/CoWork-Skill-Collab / main.
정식 요청: collab/requests/REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001/REQUEST.md
설계 정본: collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/PRESENTATION_DASHBOARD_DESIGN_r0001_20261115_KST.md

1. 최신 START_HERE/이관 CURRENT로 기존 GitHub LIVE 가동 상태를 확인. 이 요청 때문에 watcher/Task/DB/키/권한/LIVE를 변경하지 않는다. 새 단발 reviewer를 병행하지 않는다.
2. 이번 ID의 dispatch/review/receipt 및 운영 이력을 기존 공식 도구로 확인. 실행 중/완료/REVIEW_UNCERTAIN이면 추가 모델 호출 0, 기존 결과 정산만 진행.
3. Commit A의 REQUEST·ZIP·manifest를 고정. ZIP 24687 B / cbb72c90f77e969fc9f3241ba83b4a203b74d4e60ae34969e67a6fda933f3343, CRC/경로/심링크/비밀검사와 현재 운영 v0.2.20 validator를 dry-run. 설계 전용 ZIP 검사는 유지. 과거 다른 설계 ZIP의 호스트 PASS를 이번 ZIP PASS로 승계하지 않음.
4. 이번 요청은 사용자 설계 리뷰 지시를 기록한 것이며, POLICY-STATIC-V1 / USD 1 / 1회에 대한 비용 권한은 기존 호스트 승인 절차로 확인. 이 ID의 유효 비용 권한을 확인할 수 없으면 BLOCKED_COST_AUTHORIZATION으로 기록하고 서명/READY/모델 호출 금지. 다른 승인 전용 금지.
5. 같은 요청의 고정 repo ID/commit/REQUEST·ZIP/정책·모드·유효기간·한도에 기존 호스트 서명자로 APPROVAL_SIG.json 생성·검증. 기존 SOURCE_PIN.json이 있으면 값 검증 후 재사용하고 바이트 순서 차이로 덮어쓰지 않음. 새 키/토큰 발급·개인키 전송 금지.
6. 입력·서명 원격 readback 후 현재 baseline으로 READY.md를 **마지막에** 게시. 유효 READY 게시 시 기존 LIVE watcher가 자동 디스패치할 수 있으므로 비용 승인/중복 확인은 게시 전에 완료. 이 GPT가 미서명 READY를 만들었다고 가정하지 않음.
7. 기존 LIVE watcher의 결과/receipt/실제 호출 수·비용을 확인하고 원격 readback. 추가 reviewer 실행·자동 재리뷰 금지; 게시 실패는 저장 결과만 복구. 기존 장기감시를 재설정하거나 새 자동화를 만들지 않음.
8. 이 폴더 SUBMISSION_STATUS.json 및 대시보드 Work CURRENT/TRACKER의 이번 요청 관련 요약만 실제 상태로 갱신. PUBLIC은 기존 승인 allowlist만, PRIVATE 요청/코드/정책/ID 공개 금지.
9. 결과 후 GPT 판정을 기다림. 이번 요청으로 실제 대시보드/정책/UI/운영/지식/배포를 변경하지 않는다.

실행 문구:
PRIVATE wonhwipark/CoWork-Skill-Collab의 main에서 collab/requests/REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001/HOST_SUBMIT_ONESHOT.md를 읽고, 기존 GitHub LIVE 계약으로 이 설계 독립 리뷰 1회를 접수해줘. 입력·비용 권한·기존 서명을 검증하고 READY를 마지막에 게시한 뒤 결과·영수증 readback까지 진행해줘. 실행 중/완료/불확실이면 재호출하지 말고, 비용 권한이나 서명 접근이 없으면 정확한 차단 사유만 기록해줘.
