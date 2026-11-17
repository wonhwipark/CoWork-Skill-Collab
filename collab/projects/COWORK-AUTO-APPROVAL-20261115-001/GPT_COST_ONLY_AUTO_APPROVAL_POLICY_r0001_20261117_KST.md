# GPT 결정 — 자동 리뷰의 일·월 횟수 상한 제거 / 비용 기준 유지

- 날짜: 2026-11-17 KST
- 정본: PRIVATE `wonhwipark/CoWork-Skill-Collab/main`
- Work: `COWORK-AUTO-APPROVAL-20261115-001`
- 사용자 최신 지시: **“횟수한도를 제약하는 컨셉은 삭제해줘.”**
- 판정: **COUNT_QUOTA_REMOVED_BY_DESIGN / COST_AND_EXACTLY_ONCE_RETAINED**.
- 시행 경계: 본 문서는 운영 위임/서명/READY/Watcher 실행 조건을 자동 변경하지 않음. PRIVATE 개발 후보 생성·시험과 Windows LIVE 설치·승인은 별도.

## 변경 후 유효한 정책

| 항목 | 결론 |
|---|---|
| 일일 호출 횟수 상한 `max_day_calls` | 사용하지 않음. 신규 정책·UI에서 제거, 이전 위임 JSON의 필드는 호환성 입력으로만 수용·무시 |
| 월간 호출 횟수 상한 `max_reviews_per_month` 등 | 도입·사용하지 않음 |
| 호출 수·예약 수의 일·월 집계 | 디버깅/관측 지표로 유지 가능. 승인 적격성 판단에는 사용 금지 |
| 요청당 `max_calls=1`, `attempt=1`, 기존 N1 / one-shot | **유지**. 일일 횟수 제한이 아니라 동일 REQUEST 중복 실행 방지·비용 안전 경계 |
| 요청별 비용 | 기존 위임 USD 1, `POLICY-STATIC-V1` 및 허용 스킬/프로젝트 목록 유지 |
| 일별 비용 | 기존 USD 3, **KST 자정** 기준 유지 |
| 월별 비용 | 기존 USD 10, **KST 달력 월** 기준 유지 |
| 위임 만료·서명·SOURCE_PIN·READY 마지막·기존 승인 범위 | 불변 |
| `UNCERTAIN`/`POLICY_STOPPED` 비용 점유 | **상태명만으로 일괄 제외 금지**. 실제 모델 미호출·READY/N1 부재·호스트 이력이 확정된 경우에만 별도 검증된 정산 후보; 불명확한 경우 예약 비용 그대로 보수 집계 |
| 기존 요청 `AUTO_SIGNING_UNCERTAIN` | 기존 request_id 재시도 금지, 예약/실행 이력 무손실 보존. 새 리뷰를 임의 재큐잉하지 않음 |

## 코드 변경 범위 / 차단 기준

v0.2.23 SHA `f941be8a6b53d00baa10a9b097f234b159470e2aa1242ecc33bcf0bdee080ea7`에서 새 v0.2.24 개발 후보:
1. `auto_policy.py`: 허용 정책의 일일 call-count 판단과 `max_day_calls <= 2` 조건 제거. 일/월 비용·요청당 정확히 한 번·서명 검증 유지.
2. `state_store.py::auto_claim`: `DAY_CALL_LIMIT` 원자 예약 차단 삭제. `BEGIN IMMEDIATE`, `(request_id,revision)` 유니크, `DAY_COST_LIMIT`, `MONTH_COST_LIMIT` 유지. 기존 `max_day_calls` 파라미터는 호출 호환성상 받아도 무시.
3. `auto_approval.py`: 위임 파일의 `max_day_calls`를 무시, 표시 문구에서 횟수 제외. 기존 보호된 JSON·Windows DB·ACL·서명 키를 마이그레이션/변조하지 않음.
4. 실 시험: KST 같은 날 다수 REQUEST 중 비용 내 요청 통과/비용 초과 차단, N1 디스패치 비용 합산, 중복 요청 정확히 한 번, 사전 위임 범위/변조/만료, 원자 경합, UNCERTAIN 재실행 차단. Windows 전용 잠금·SHADOW 테스트는 Windows 운영 인터프리터에서 별도 완료 필수.
5. CI PASS라고 하더라도 **독립 코드 리뷰, 원본 ZIP SHA/CRC, Windows SHADOW, 백업·롤백, 신규 운영 설치 승인**을 생략하지 않음.

## 사용자 제안에서의 변경 이유

초기 `하루 2회 + USD 3` 이중 제한은 서명 검증 실패 1건으로 당일 횟수 한도가 소진되는 서비스 품질 문제를 일으킴. 횟수 상한을 전부 제거하면 호출 횟수 회수 로직은 필요 없어짐. 비용은 보수적인 예약 모델이므로 미정산 예약이 비용에 영향을 줄 수 있다는 별개 문제는 남으며, 비용 정산 최적화로 무조건 확대 해석하지 않음.

과거의 `하루 2회` 활성화 기록과 해당 시점 시험 결과는 역사로 보존. 새 정책이 LIVE에 적용됐다는 표기는 실제 Windows 설치/정본 승인/시험 완료 전에 금지.

## 현재 실행 근거

- 개발 브랜치: `dev/auto-quota-cost-only-20261117`
- 수정·빌더: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/dev/build_v024_cost_only.py`
- 회귀시험 재정의: `collab/projects/COWORK-AUTO-APPROVAL-20261115-001/dev/patch_v024_tests.py`
- 검증 CI: `.github/workflows/cowork-auto-quota-v024-build.yml` (개발 후보, PRIVATE 전용).
- **최종 실행 상태는 관련 CURRENT 및 CI 결과를 우선 조회**. 본 판정 작성만으로 코드 QA/리뷰/LIVE 완료가 아님.

다음 한 동작: 위 브랜치에서 full test 및 Windows 전용 미실행 범위를 판정하고 신규 후보 ZIP·SHA를 PRIVATE에 고정한 뒤, 독립 코드 리뷰·호스트 적용 게이트를 진행. 운영 LIVE의 현행 횟수 제한은 실제 패치가 검증·설치될 때까지 남아 있을 수 있음.
