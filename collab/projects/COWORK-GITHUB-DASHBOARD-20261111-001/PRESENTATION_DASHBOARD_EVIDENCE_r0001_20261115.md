# 발표용 대시보드 개선 — 근거 snapshot
2026-11-15 KST. 아래 Git blob은 각각 조회한 원문 식별자이며 전체 파일이 같은 commit에서 조회됐다고 주장하지 않음. 리뷰 입력 ZIP 안 source 파일 바이트가 최종 고정 입력이다.

| 파일 | Git blob |
|---|---|
| collab/dashboard/public_sync.py | 04c370025f048c18a0c02adc323b3fe7a3bb59ab |
| collab/dashboard/work_tracker.py | 7c200e1e0d4489e0d7effeb8b5bc95518c43a01e |
| L1 Work TRACKER.json | 529a11c2fca2fe800f4b13aa6bff378c1df59a45 |
| 이관 CURRENT.md | 400a58c29ed29bace8b627275da2cd2c8598c4b1 |
| PUBLIC docs/cowork-dashboard/status.json | 23538934ab6a9af55c337a0893fe803041e811ff |
| 기존 요청 v0.2.20 preflight 보고 | 0d5a54f15174577559fa5028f9c7545821432833 |
| PUBLIC_PAGES_DEFAULT_POLICY.md | 3fe5765a55d9319b844a76f3782c5737b133d3f1 |

직접 브라우저: https://wonhwipark.github.io/L1Work/cowork-dashboard/ 와 업무 상세 선택. 이번 발표 적합성 검토를 위해 실제 개요/상세 확인. 회사 원문/이미지/스크린샷은 ZIP에 포함하지 않음.

직접 진단: source/work_tracker.py의 _registered()에 현재 source/L1_TRACKER.json을 넣으면 None. 두 enum을 FAIL/NOT_RUN으로 바꾼 메모리 합성 비교는 수용. 실제 소스/Tracker 무변경. 정상값 선택은 실제 상태의 정본 갱신이 아닌 비교 조건이다.

source/public_sync.py의 _read_active_provider, build_payload의 cutover/provider guard와 PUBLIC_WORKS 고정 매핑을 필요한 범위만 확인.
정적 소스와 실제 실패 Actions 로그는 구분: SOURCE_CONFIRMED_REJECTS_GITHUB, ACTUAL_FAILED_ACTION_LOG=NOT_VERIFIED.
