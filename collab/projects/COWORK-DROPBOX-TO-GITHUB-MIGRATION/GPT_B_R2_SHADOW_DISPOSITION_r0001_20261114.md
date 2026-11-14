# GPT 종합 판정 — CoWork v0.2.17 R2 + 실호스트 SHADOW/DB 백업·복구 (2026-11-14 KST)

- Repo/branch: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` / `main`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- Source: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_B_R2_SHADOW_PREFLIGHT_RESULT_FOR_GPT_20261114.md`
- **GPT_DISPOSITION: ACCEPT_WITH_CHANGE** (독립 정적 리뷰 R2 **PASS_WITH_FINDINGS**, **LIVE_NOT_READY**)
- `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`
- 허용된 운영 변경/모델 재리뷰를 이 문서 자체로 시작하지 않음.

## 1. GitHub 원격에서 GPT가 실제 읽은 근거

- Windows Claude 결과 MD blob `7cc46f421cfaf5cdaa9eca3bec366bdd897a2e95`; commit `7968e14a3aed3363fd0fa0e5850d20655cb92a4c`은 호스트 보고.
- 독립 리뷰 `collab/reviews/REQ-COWORK-V0217-R2-20261114/REVIEW_RESULT_1.md` blob `57b630c6897af5c60df388d58d1870893dc3b062`: BLOCKING 0, N1·N2·N3 및 S1·S2. 별도 프로세스 정적 리뷰이며 실제 pytest/실호스트 검증은 수행하지 않았다고 기록.
- 영수증 `collab/receipts/REQ-COWORK-V0217-R2-20261114/RECEIPT_1.md` blob `f1f360f428ec7889db65c33203e2eccec975ac21`, 사용량 `USAGE_RECEIPT_1.json` blob `d12150c9fba36d8a830110040e445fb7c9a10f03`: 모델 호출 1회, **$0.9945836 ≤ $3**, **23 turns**, 출력 **18,029 tokens**, `--max-turns` 미지원. 비용은 승인 범위 이내, R2 5 turns/출력 6000 토큰 목표는 미충족.
- `review-inputs/REV-COWORK-V0217-R2-20261114/REVIEW_MANIFEST.md` blob `4f9eb1e3dfa1c69d753a73ca1c17df0526de446b`: 리뷰 대상 ZIP `skill-collab-watcher_v0_2_17_1114.zip`, 보고 SHA-256 `824f26c4e28fcc804ed1dd3942a34408c54b9091be34ecb1693cc4cb9d46df03`, 크기 232575 B. 원격 매니페스트·리뷰 문서의 대상 해시 일치. **실제 ZIP 바이너리의 GPT 독립 byte/CRC 확인은 NOT_RUN**(Claude 호스트는 원격 raw SHA/CRC 확인을 보고).
- GitHub API `get_repo`에서 실제 ID `1451933830` 확인: 호스트의 trust_root `repo_id` 라벨 **현재 값과 일치**. 그러나 검증기가 GitHub 원격 repository ID와 **실행 시 교차 확인하는 기능은 없다**. 값 일치와 런타임 보안 결합은 구분.

## 2. GPT 지적별 판정

| ID | 판정 | 후속 조건 |
|---|---|---|
| R1 F1~F5 | **수정 수용 / 정적 독립 리뷰 범위 PASS** | reviewer가 코드 추적 및 시험의 주장 확인. 실호스트 복합 시나리오·실 CLI usage-limit 문자열은 미재현, 추가 증거 요구 |
| N1 (nonce 재사용·상태 DB 소실) | **수용 — LIVE 안정성 게이트** | 완료 이력/서명 사용 이력을 보존하고 DB 소실·복원·옛 READY 재노출 시 재디스패치 0을 입증. 코드 재사용 방지 테이블 추가 또는 **동등하게 검증된** 운영 복구/외부 상태 보호 수단을 마련. 단순 문서화만으로 중복 모델 호출 0을 PASS라 하지 않음 |
| N2 (repo_id 문자열만 비교) | **수용 — LIVE 신뢰 게이트** | 실제 GitHub 저장소 ID가 1451933830임은 확인. 실행 시 원격 ID·고정 trust repo/pin이 일치함을 검사하거나, 다른 repo 재사용을 막는 동등한 fail-closed 검증을 입증. 일치하는 값만으로는 런타임 결합이 완료됐다고 주장하지 않음 |
| N3 (토큰 파일 repo 표기 advisory) | **수용 — 문서·검증 보완** | token 파일의 문자열은 인증 근거가 아님. GitHub 실 fine-grained scope와 Contents R/W 부정시험을 통과해야 PASS |
| S1 (미사용 find_logical_job) | **보류 — 비차단** | 코드 정리 후보. 단독 수정·재리뷰 비용을 만들지 말 것 |
| S2 (taskkill 실패 미기록) | **수정 수용 — 비차단** | 다음 수정 묶음에 returncode·손자 생존 경고/시험 추가. SHADOW 또는 운영에서 권한 차이 노출 시 중요도 재평가 |
| Q8 전체 복합 시나리오 | **추가 정보 필요** | usage-limit+재시작+policy revision+cursor 유실+락의 결합 동시 시나리오는 정적 논리만 확인. 격리 host E2E 추가 |
| 실제 CLI usage-limit 문자열 | **추가 정보 필요** | 공식/실측 메시지 수집 가능할 때 정규식 검증. 실제 한도 강제 유발 목적 추가 유료 호출 금지 |

## 3. 실호스트 운영 게이트 판정

| 게이트 | 상태 | 근거/미완료 |
|---|---|---|
| 후보 패키지·시험 | `SELF_TEST_REPORTED` | 호스트: 644 PASS/12 SKIP(venv), 578 PASS/17 SKIP(운영). 운영에서 cryptography 5 SKIP |
| 독립 R2 | `COMPLETED_PASS_WITH_FINDINGS` | static only, blocking 0 / code review; 독립 pytest나 실 제품 실행 증거 아님 |
| GitHub 자동 결과 게시 | `BLOCKED_TOKEN` | 엔진 Contents 쓰기 403·UPLOAD_PENDING, gh 개발자 계정 수동 게시만 성공 |
| 최소권한 PAT | `ACTION_REQUIRED` | 사용자 GitHub UI에서 PRIVATE 단일 저장소 Contents R/W만, 만료 90일 이하로 발급 필요. 기존 classic 40자/무기한 토큰 재사용 금지 |
| 운영 cryptography | `BLOCKED_RUNTIME` | Python 3.11.9 운영 환경에 미설치 → Ed25519 확인 `APPROVAL_UNVERIFIABLE`, fail-closed 0 호출. 설치·작동 실측은 별도 운영 변경 승인 필요 |
| SHADOW GitHub 읽기 전용 | `PARTIAL_PASS` | GET only, 모델 0/remote write 0/Telegram 0, live main/WAL 변동 0(호스트 자체 보고). **별도 Windows 계정 enforce, 네이티브 파일 I/O 추적, 장기 운영 미검증** |
| 운영 DB 격리 백업·복구 | `HOST_REPORTED_PASS` | SQLite로 원본 열지 않음; main/WAL 바이트 복사·해시/stat 불변, 복사본 integrity_check ok, 61 jobs/1 pending_request 등 건수 일치. 호스트 실측 미독립 재연 |
| Notifier | `BLOCKED_INTEGRATION` | `notify_reviews.py --watch` **2개 프로세스** 동작 보고(중복 발송 위험). GitHub 상태 DB·수신 연결/중복 방지/워터마크·실 알림 미검증 |
| 전환·롤백 | `NOT_RUN` | 요청 pending 1건의 무손실 보존/정산 필요, 단일 provider·알림 중복0·실호스트 종료/복원 절차·최종 승인 미완료 |

## 4. 승인 경계와 다음 원샷 준비

### 지금 사용자 조치가 필요한 한 가지
GitHub 웹 UI에서 **fine-grained PAT(만료 90일 이하)**를 발급한다. Resource owner 본인, **Only select repositories = wonhwipark/CoWork-Skill-Collab**, **Repository permissions: Contents Read and write**, Metadata Read 자동, 그 외 권한 불필요. 값은 채팅/문서/GitHub에 붙이지 말고 Windows 로컬 보안 설치 도구로 주입한다. PAT를 만드는 것만으로 LIVE가 활성화되지는 않는다.

### Windows Claude Code가 다음 한 번의 묶음으로 준비할 항목
1. 새 PAT 설치·만료·actual repo Contents read/write 검증(격리 테스트 경로만), 엔진의 `UPLOAD_PENDING` 결과 게시 재시도 **publish-only** 및 원격 영수증 readback; 리뷰 모델 재호출 0.
2. `cryptography` 운영 인터프리터 배치/설치 **변경 승인을 별도로 확인한 뒤** 실서명·비인가/만료/다른 repo 부정시험. 사용자가 승인하지 않은 호스트 설치/Task 변경은 금지.
3. 기존 2개 Notifier 프로세스의 부모/Task/실제 전송 경계만 먼저 읽기 전용 실측. 병합·종료·알림 경로 변경 및 실제 Telegram 발송은 **사용자 운영 승인 전 금지**.
4. N1/N2 보안 위험의 **최소 수정 vs 동등하게 증명되는 운영 차단**을 평가하고, F1~F5 및 복합 Q8 synthetic E2E; 뒤따르는 변경이 필요하면 **새 v0.2.18 로컬 격리 후보**로 준비, 자체 회귀시험 가능. **추가 유료 Claude 재리뷰는 미승인**.
5. 별도 계정 SHADOW/장기 시험과 원본 DB read-only 무영향을 단계적으로 입증. 필요한 계정 생성·권한 변경·운영 Task 변경은 별도 승인 전 불변.
6. 비민감 결과를 PRIVATE `main`의 `CURRENT.md`·`TRACKER.json`에 기록·readback. 이전 승인·결과·원본 ZIP은 보존.

### 최종 LIVE 승인 전 필수 확인
최종 후보와 독립 검증 범위 정합, 엔진 token·서명·이력 보존, SHADOW 격리, Notifier 1개 활성 및 알림 중복0, 미정산 요청 처리, 롤백·복구 리허설을 검증. 이후 **별도 사용자 LIVE 전환 승인**. `R0~R3` 상시 유료 리뷰 자동화·추가 리뷰·PUBLIC 릴리스는 이번 결과를 근거로 승인하지 않음.

## 5. NEXT_ONE_ACTION
GPT 종합 판정 게시 이후 사용자가 새 fine-grained PAT를 GitHub 웹 UI에서 생성·Windows 보호 폴더에 설치하는 것이 우선. 그 전에도 Windows Claude Code는 승인된 범위의 비민감 검토·synthetic 테스트를 계속할 수 있지만 **실운영 변경/추가 유료 재리뷰/LIVE는 금지**.
