# GPT 판정 — 기존 PAT 적합성 검증 및 R2 publish-only 정산
2026-11-14 KST / r0001

- Repository: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`
- Branch: `main`
- Work ID: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
- Source: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CLAUDE_EXISTING_PAT_VALIDATION_AND_PUBLISH_ONLY_RESULT_FOR_GPT_20261114.md`
- Source blob read from GitHub: `2742f9b17254e99567f00d3d4e17239f82103e37`
- Source commit: `78a489b6ea39f53b334e1e76cc4c185b8860cc49` (GitHub recent commit list confirmed)
- **GPT_DISPOSITION=ACCEPT_WITH_CHANGE**
- `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`
- 이 판정은 운영 설치·토큰 발급·추가 유료 리뷰·LIVE 전환 실행 승인이 아니다.

## 1. 사실·검증 근거

1. Windows Claude Code 보고: PC의 **감시기 전용 자격 폴더 JSON 2개**만 서버 인증으로 검사. 후보 1: fine-grained·비공개 대상 1개·**읽기 전용/만료 없음**. 후보 2: **classic·광역·만료 없음**. 둘 다 기존 정책 미충족, `PAT_ELIGIBILITY=FAIL`, 설치와 실제 쓰기 PROBE `NOT_RUN`.
2. 사용자는 별도의 PAT 보유 사실을 확인했지만, Windows 자격 증명 관리자·다른 Windows 계정·다른 PC·브라우저의 토큰은 이번 탐색 범위 밖. 따라서 **"사용자가 적격 PAT를 보유하지 않았다"는 결론은 금지**. 현재 PC에서 접근·검증된 적격 토큰은 `0`개라는 범위 한정 사실만 수용.
3. 기존 R2 `REQ-COWORK-V0217-R2-20261114`의 리뷰 결과·영수증·사용영수증 3개는 호스트에서 로컬·GitHub 바이트 동일 판정(`ALREADY_PUBLISHED`). 격리 원장 사본에서 `UPLOAD_PENDING → COMPLETED`, `UPLOAD_RETRY_COMPLETED` 이벤트 1, GET 14, remote write 0, 모델 호출 0, 알림 0 보고.
4. 이 실측은 이미 원격에 있던 결과에 대해 수행된 **읽기 전용/격리 원장 정산 시험 PASS**다. **감시기 토큰으로 새 결과를 처음 자동 업로드하는 E2E**, 또는 운영 원장 `UPLOAD_PENDING` 실정산은 `NOT_RUN`. `REVIEW_V0217=PASS_WITH_FINDINGS` 상태는 불변; 재리뷰 불필요.
5. 실제 GitHub repo ID가 `1451933830`이라는 조회 보고는 기존 GPT 확인과 일치. `repo_id`를 제품 실행 때 원격과 신뢰 루트에 바인딩하는 N2 결함은 아직 미해결. 자격 JSON의 `repo` 필드·account `permissions.push`는 토큰 세부 권한을 증명하지 않음.
6. 로컬 검증 스크립트가 초기에 권한 신호를 오판정한 뒤 수정·재시험됐다고 보고. 그 스크립트 소스·실제 Windows 자격은 GPT가 직접 검증하지 않았으므로 `HOST_SELF_TEST_REPORTED`로 구분.

## 2. GPT 항목별 판정

| 항목 | 판정 | 사유·최소 후속 |
|---|---|---|
| 기존 PC의 두 자격 부적합 | 수용 | classic 광역/무기한·fine-grained read-only/무기한은 watcher Contents R/W 기준 미충족. 재사용 강제 금지 |
| 사용자가 다른 적격 PAT를 보유할 가능성 | 추가 정보 필요 | 사용자에게 토큰 문자열·경로를 요구하지 말고, Windows 보호 로컬 입력/인증 과정에서 기존 토큰을 우선 실측 |
| token 설치·임시 브랜치 쓰기 시험 | 보류 | 적격 자격 식별 후 진행, 독립 테스트 경로·원격 readback·브랜치 정리 |
| R2 이미 게시된 결과의 정산 | 수용(격리시험) | `ALREADY_PUBLISHED`와 격리 원장 `UPLOAD_PENDING→COMPLETED` PASS 보고. 운영 실원장 변경은 확인하지 않았고 승인 없이 실행하면 안 됨 |
| 비용·모델 중복 방지 | 수용(이번 실행 범위) | 리뷰 새 호출·비용 0 보고. N1 nonce replay/DB 소실 후 중복 디스패치는 별도 LIVE 게이트 |
| LIVE 적합성 | 보류/FAIL 게이트 | 엔진 최초 자동 업로드·운영 cryptography·Notifier 중복 및 연결·N1/N2·격리/복구 등 미해결 |

## 3. 다음 한 동작 — 기존 토큰 우선

1. 사용자 보유 PAT가 **이미 fine-grained / CoWork-Skill-Collab 단일 PRIVATE repo / Contents R/W / 유효 기간 ≤90일 / 불필요 권한 없음**이면 Windows의 준비된 `Install-EngineWriteToken.ps1` **숨김 입력**으로 저장한다. *채팅·GitHub·콘솔에 값/접두/길이/경로/해시를 남기지 않는다*. 기존 부적격 토큰을 무단으로 덮어쓰거나 개발자 `gh` 자격으로 대체하지 않는다.
2. 그 토큰을 Windows 로컬 보안 설치한 뒤 `verify_engine_write_token.py --live`가 **실제 해당 토큰만** 사용하여 격리 임시 브랜치에서 create/readback/delete를 실행하고 Contents 쓰기 권한·저장소 제한·만료를 가능한 범위에서 확인. GitHub 서버에서 token scope 정보가 노출되지 않는 부분은 `NOT_VERIFIED`로 명시.
3. **적격 PAT가 실제로 없을 경우에만** 최소권한 fine-grained PAT 신규 발급 조치 필요. 사용자의 이미 보유하신 PAT가 별도 장소에 있는지는 아직 미확정이므로 사용자 발급 반복 요청 금지.
4. 기존 R2 결과의 publish-only readback을 재차 유료 reviewer로 재실행하지 않는다. 자동 업로드 E2E는 **새 시험 요청·안전한 격리 경로**로 검증하되 리뷰 모델 호출 0, 추가 비용 0.
5. 이후 완료 증거와 남은 LIVE 게이트를 `CURRENT.md`·`TRACKER.json`·비민감 결과 MD에 갱신. **운영 DB/Task/Notifier/cryptography 설치, LIVE 전환은 별도 명시 승인이 없는 한 금지**.

## 4. NEXT_ONE_ACTION

Windows에 아직 설치/인증되지 않은, 사용자가 보유했다고 밝힌 별도 PAT를 **Windows 안전 입력 절차로 검증**하는 것이 우선. 기존 PC에 확인된 자격 2개에 대한 재검사는 불필요하다. 이후 적격이면 설치·실 GitHub write/readback 검증, 부적격이면 차이만 ACTION_REQUIRED로 기록. `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER` 유지.
