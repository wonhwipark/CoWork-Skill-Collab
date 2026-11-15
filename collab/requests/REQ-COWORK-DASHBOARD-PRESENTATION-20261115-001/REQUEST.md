---
schema: SKILL_COLLAB_REVIEW_REQUEST_V1
state: REQUESTED
request_id: REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001
request_revision: 1
project_id: COWORK-GITHUB-DASHBOARD-20261111-001
work_id: COWORK-GITHUB-DASHBOARD-20261111-001
skill_id: cowork-dashboard
package_path: /SKILL-COLLAB/packages/cowork-dashboard-presentation-design_r0001_1115_REVIEW_INPUT.zip
package_file_id: github:REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001
package_rev: presentation-design-r0001
package_sha256: cbb72c90f77e969fc9f3241ba83b4a203b74d4e60ae34969e67a6fda933f3343
package_size_bytes: 24687
baseline_package_ref: null
knowledge_refs: []
consumer_profiles: [presentation-dashboard-design]
reviewer_os: WINDOWS
test_policy: STATIC_ONLY
run_policy_ref: POLICY-STATIC-V1
output_contract: SKILL_COLLAB_REVIEW_RESULT_V1
goal: focused independent design review of dashboard presentation clarity and source-state correctness
---

# 발표용 대시보드 개선 설계 — 독립 리뷰 요청 1회

사용자 지시: 발표 적합성 검토 결과에 대한 설계 작성 후 협업 리뷰 요청. 이번 요청은 기존 Work→Knowledge 설계 리뷰/Watcher v0.2.20 리뷰와 다른 신규 ID. 타 요청의 승인·서명·결과를 재사용하지 않는다.

## 대상·한도
비민감 설계/공개된 CoWork 도구 근거 snapshot 전용 ZIP. 설치/배포 후보가 아니며 실행하지 않는다.
R1 집중 검토, POLICY-STATIC-V1 / 최대 USD 1 / 1회만 제안. 사용자 리뷰 요청 의도는 확인되었으나 실제 비용 권한과 승인 서명은 호스트에서 이번 ID에 대해 확인할 것. 상한 정의가 서명 승인 자체는 아니다. 미승인·서명 불가·한도 초과는 모델 호출 0으로 보존. 자동 R2 상향·추가 호출·다른 리뷰 재호출 금지.
GitHubTransport의 /SKILL-COLLAB/... 는 기존 논리 경로이며 Dropbox 업로드·재가동 지시가 아니다.

## 입력·질문
DESIGN.md → EVIDENCE.md → REVIEW_QUESTIONS.md. source/public_sync.py는 _read_active_provider/build_payload 및 고정 PUBLIC_WORKS 매핑, source/work_tracker.py는 _registered/collect의 관련 부분만 읽는다.
확인된 문제: 공개 상태가 GITHUB/LIVE를 거부하는 코드 경로, 잘못된 Tracker enum의 UNKNOWN fallback, 구체 성과/대기/다음 역할 부재, 오래된 공개 JSON 재수신과 원본 최신성 혼동.
검토 질문:
Q1. 최신 정본·호스트 보고·직접 격리 재현·가정의 근거 수준이 구분되는가?
Q2. 승인된 GITHUB/LIVE 고정 매핑 추가와 미지 상태 차단을 함께 지키는 최소 정책/코드 개정인가?
Q3. parent Work/하위 활동/각 리뷰 ID의 상태가 섞이지 않는가?
Q4. 요청등록/유효 승인·READY/예약/실행/결과·receipt/GPT판정을 정확히 구별하는가?
Q5. 발표용 완료·현재·다음 담당/행동·결과물이 가독성과 공개 allowlist를 만족하는가?
Q6. 최근 수신/데이터 기준/원본확인/내용불변·sync실패·레이스 처리에 거짓 최신/완료가 있는가?
Q7. 기존 URL·5범주·필터·최근 인계3건·schema와 호환되는 최소 확장인가?
Q8. A01~A15 반례·수용 기준의 핵심 누락과 구현 전 확정할 한 가지는 무엇인가?

## 결과
질문별 판정과 최대 6개 지적(BLOCKING/MAJOR/MINOR), 문서 절·문제/영향·최소 수정·확인 기준 및 ACCEPT/ACCEPT_WITH_CHANGE/REVISE/HOLD.
입력 약16k tokens/출력 약3k tokens/3 turns는 목표이며 실제 하드 토큰 보장은 아님. source 전체/무관한 이력으로 범위를 확대하지 말고 부족하면 PARTIAL_SCOPE 보고. 별도 서브에이전트/추가 모델 호출 없음.
이번 리뷰는 설계 판단. 코드·공개정책·UI·배포·운영 watcher/DB/Task·기존 리뷰/Knowledge 변경 금지.
엔진 표준 결과: collab/reviews/REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001/REVIEW_RESULT_1.md
엔진 표준 영수증: collab/receipts/REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001/RECEIPT_1.md
예약: collab/dispatch/REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001/DISPATCH_1.md
실행 불확실 상태는 REVIEW_UNCERTAIN 보존. 게시 실패는 동일 결과 바이트만 재게시, 모델 재호출 금지.
결과와 receipt readback 뒤 GPT 항목별 판정. 실제 UI 수정/Pages/모바일 검증 PASS로 확대하지 않는다.
