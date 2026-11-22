# 독립 리뷰 비용 검사 제거 — 격리 후보 결과 (Windows Claude Code)

- 작성: Windows Claude Code, 2026-11-22 KST. Work: `COWORK-AUTO-APPROVAL-20261115-001`. 기준: GPT 게시기 `a21bab69dcf1`, 보완 `ea3a4811e520`.
- **결론: 격리 후보 v0.2.30을 작성하고 시험했다(952 PASS / 0 FAIL / 12 SKIP). 신규 독립 리뷰의 실행 허가가 금액으로 결정되던 경로 2개를 제거했다. LIVE 적용 NO. 유료 호출·신규 리뷰·기존 REQUEST 재디스패치 0.**

## 1. 추적 결과

- 실제 운영 기준: 설치본 `D:\User\whpark\skill-collab-watcher-github` = v0.2.29(트리 SHA `b0134258…`, 읽기만 함).
- 개발 원본 `D:\User\whpark\skill-collab-watcher`는 v0.1.5 구버전이며 venv만 보유. 이 후보의 출발점으로 쓰지 않았다.
- 금액 기반 실행 허가 경로:
  1. `auto_policy.assess` — `PER_REQUEST_COST`(추정 센트 > 위임 `max_request_usd`). **제거**.
  2. `auto_approval` — `PER_REQUEST_COST` 발생 시 영구 제외(`auto_exclude`) 분기. 1번 제거로 도달 불가하므로 **제거**.
  3. 수동 승인 도구 `approve_request.py` — `--max-usd`가 정책 cap과 같아야 통과하는 금액 일치 검사, `--max-usd` 필수. **제거**(플래그는 받되 검사 없음).

## 2. 제거·수정 파일 (후보 폴더만)

| 파일 | 변경 |
|---|---|
| `skill_collab_watcher/auto_policy.py` | `PER_REQUEST_COST` 차단 2줄 삭제, 주석 갱신 |
| `skill_collab_watcher/auto_approval.py` | 도달 불가 `PER_REQUEST_COST` 분기 삭제 |
| `skill_collab_watcher/__init__.py` | 버전 0.2.30 |
| `approve/approve_request.py` | `--max-usd` 일치 검사·필수 제거, `SKILL_COLLAB_DEPLOY` 환경변수 오버라이드 추가(기본값은 기존 경로) |
| `tests/test_auto_policy_gpt_proto.py` | 큰 추정 금액이 차단되지 않음을 검증하도록 교체 |
| `tests/test_v022_findings.py` | B2 중 `max_request_usd` 축소 케이스 제거, "축소해도 대기 요청을 멈추지 않음" 대조 시험 추가 |
| `tests/test_v029_cost_refused_exclusion.py` | 삭제(상한 상향 후 재진입 금지 시험은 대상 동작이 없어짐) |
| `docs/CUTOVER_RUNBOOK.md` | 제목 버전만 v0.2.30 (내용 불변) |

## 3. 남아 있는 비용 관련 조건 (의도적으로 유지)

| 조건 | 위치 | 판단 |
|---|---|---|
| CLI `--max-budget-usd` 실행 상한 | `review_runner.py` 185 / `orchestrator.py` 750–768 | **사용자 결정 필요.** 제공자 측 하드 정지로 금액 판단이 아니지만, 제거하면 상한 없는 유료 실행이 된다. 유지함 |
| `UNSUPPORTED_DELEGATION_LIMIT` (1~10000 센트) | `auto_policy.py` 79 | 위임 설정 범위 검증. 실행 허가 판단 아님. 유지 |
| `INVALID_COST` (cents ≤ 0) | `state_store.py` 393 | 정책 금액이 등록되지 않은 경우에만 발생. 유지 |
| 위임 파일의 `max_request_usd` 값 | 보호 파일 | 값은 이제 무효. 보호 파일이므로 **변경하지 않았다** |
| `REVIEW_POLICY` (리터럴 `POLICY-STATIC-V1`) | `auto_policy.py` 73 | 정책 이름 검사. 금액 검사 아님. 유지 |
| 게시기 `POLICY_COST_MISMATCH` | `tools/review_request_gate.py` 98–100 | GitHub 게시기는 GPT가 이미 바꿨으나 **Windows 복사본에 잔존**. 사용처 확인 후 정리 필요 — 잔여 |
| `notify_events.py` 117 `PER_REQUEST_COST` 문구 | 알림 매핑 | 죽은 문자열, 무해. 잔여 |
| `CUTOVER_RUNBOOK.md` 142 일일 비용 상한 행 | docs | 코드상 legacy inert인데 문서는 차단이라 서술 — **문서 정정 필요**, 미수정 — 잔여 |

## 4. 보호 장치 유지 확인

- 위조·변조·중복·만료·재실행·무모델호출 관련 시험 부분집합 100 PASS (서명 위조, 변조 번들, 중복/UNCERTAIN 봉인, 만료 위임, 재실행, 모델 미호출).
- 서명 전 재검증, Ed25519 서명, READY 마지막 게시, 원자적 1회 클레임, `max_calls=1`, PIN·ZIP 무결성 검사는 코드 미변경.
- 위임 허용 목록 미확대. `cowork-context-design`은 여전히 `SCOPE`로 자동 대기(별도 승인 사항).

## 5. 시험 결과

| 항목 | 결과 | 근거 |
|---|---|---|
| 전체 단위·회귀 시험 | PASS | 후보 `pytest tests` = 952 PASS, 0 FAIL, 12 SKIP |
| 변경 전 기준선 재측정 | NOT_RUN | 기준선은 docs 누락 상태에서 956 PASS / 1 FAIL(docs 누락)만 측정. docs 보완 후 재측정 생략 |
| 격리 E2E (stub 실행기) | PASS | 스위트 내 가짜 Claude 실행기 사용. 실제 유료 모델 호출 0 |
| Windows 호스트 실제 `claude` CLI 실행 | NOT_RUN | 이번 범위 밖, 유료 호출 금지 |
| 승인 도구 후보 `check`/`approve` 실행 | NOT_RUN | 후보 폴더에 설정 파일 없음. 서명·READY 금지 |
| 모델 호출 수 | 0 | 시험 전부 stub/fake runner |

## 6. 패키지

- 후보 폴더: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_30_cost_gate_removal\`
- zip: `D:\User\whpark\skill-collab-watcher-dist\candidates\v0_2_30_cost_gate_removal_candidate.zip`
- zip SHA-256 `541cd3f1a973fd2869ca3759a2987105a682189ecd81f78752c6e4c32dcbf121`, 288,594 B, 102 파일(`__pycache__` 제외)
- 트리 SHA-256(파일별 해시 연결) `c6bd39a40c4cd92ae50108ecfe716143bf10e70b82f6e1ff2261c4a83e6c5c7b`
- 코드 zip은 공개 저장소에 올리지 않았다. 결과 문서와 CURRENT만 게시한다.

## 7. LIVE 적용과 롤백

- LIVE 적용: **NO**. 라이브 v0.2.29 설치본, 설정 SHA `2ead4007…`, 위임 SHA `6d826672…`, Task·DB·Notifier 모두 불변.
- 롤백: 후보는 설치되지 않았으므로 롤백할 것이 없다. 적용 시에는 현행 설치본을 새 백업 번들로 먼저 보존한 뒤 교체하고, 실패 시 백업으로 복귀한다.

## 8. 잔여 SCOPE 문제

- `cowork-context-design`은 보호 위임 skills 목록에 없어 자동 경로에서 계속 `SCOPE`로 대기한다. 이번 작업은 이를 해결하지 않았다. 해결하려면 위임 허용 목록 변경에 대한 별도 명시 승인이 필요하다.

## 9. 추가 승인 또는 조치 필요

1. CLI `--max-budget-usd` 실행 상한을 유지할지 제거할지 사용자 결정. 권장: 유지(하드 정지 안전장치).
2. LIVE 적용 승인. 적용 시 백업 번들 선행, 기존 Task 중지·교체 절차 필요.
3. Windows 게시기 복사본의 `POLICY_COST_MISMATCH`와 문서 일일 비용 행 정리(후속 Work).
4. 위임 허용 목록에 `cowork-context-design` 추가 여부 — 별도 판단.
