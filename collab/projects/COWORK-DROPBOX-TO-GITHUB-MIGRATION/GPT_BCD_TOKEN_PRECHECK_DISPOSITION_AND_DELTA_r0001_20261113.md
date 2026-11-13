# B·C·D·토큰 사전 점검 GPT 판정 및 다음 협업 delta
기준: 2026-11-13 KST / r0001
정본: PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`

## 1. 현재 상태와 판정
- 사용자 지시: “협업위한 다음단계 확인후 진행해줘”. 허용된 개발·격리 자체시험·PRIVATE 결과 게시 범위의 후속 작업을 진행.
- `GPT_DISPOSITION=ACCEPT_WITH_CHANGE`, `ACTIVE_PROVIDER=NONE`, `CUTOVER=MIGRATION_NOT_CUTOVER`.
- Claude 결과 `CLAUDE_BCD_TOKEN_APPROVAL_PRECHECK_RESULT_FOR_GPT_20261113.md`: GPT가 원격 UTF-8 내용을 읽어 14,244 B / SHA-256 `7b4f87dd54bdb160778c66d6d16fb93d547f1b13eb184c9398bc77e041666eaf` 일치 확인(이전 턴). 최신 CURRENT/TRACKER도 다시 확인.
- v0.2.11 후보는 Windows 로컬 175,714 B / SHA-256 `174b9fd83361cc85ce3fb1b4b503335dc701bff9e38415ae23a11256ef8b6350`. GPT는 원본 ZIP/수정 제품 코드를 받지 않았으므로 해당 바이트·536 PASS는 `SELF_TEST_REPORTED`로 수용. GPT 직접 재현 또는 독립 리뷰 PASS로 승격하지 않음.
- 다음 협업은 아래 §6의 **토큰 도구 delta만** 수행. 기존 마스터 `GPT_GITHUB_LIVE_MINIMUM_REWORK_MASTER_r0001_20261113.md`를 새로 전부 실행하지 않음.

## 2. 지적별 판정
| 항목 | 판정 | 근거/영향 |
|---|---|---|
| config-check/auth-check/auth-init의 운영 폴더·비밀 접근 수정 | 수정 수용(자체보고 한정) | 재현→수정 및 회귀시험 보고 수용. 원본 코드/ZIP 독립 검증은 NOT_RUN |
| 간헐 시험 실패의 프로세스 트리 종료 수정 | 수용(자체보고 한정) | 런처/자식 잠금 잔존 원인과 16/16 재시험 보고. GPT Windows 재현 NOT_RUN |
| B 서명 키트 준비 | 준비 결과 수용 | 기기 지정·운영키 생성/설치 미실행. NEW 파일이라는 사실만으로 소유·이동 정책 허가를 확정하지 않음 |
| C 4축 대체 증거 | 조건부 검토 권고 / C=PARTIAL | 별도 비관리자 SHADOW 계정에 한정. ETW NOT_PROVEN 보존; 사용자 본인 계정 LIVE까지 확대하지 않음 |
| D 출처 분류 | 수용 / 게시 차단 유지 | 46개 유래+24개 신규는 출처 분류. 소유권·반출 허가와 별개이며 키트도 필요한 이동/이용 허가를 확인 |
| 토큰 r0001 전체 PASS | 수정 수용 필요 | 기본 실행의 SKIPPED=True 때문에 쓰기 가능 자격도 GET 응답만 같으면 전체 PASS. GPT 모의 응답으로 재현 |
| HTTP 403→쓰기 불가 추론 | 거절 | 403은 rate limit 등에서도 발생. 권한·검증 순서/상태코드만으로 읽기 전용 확정 금지 |
| E 독립 리뷰 | NOT_RUN 유지 | GPT 개발시험·Claude 동일 개발 세션 자체시험은 E를 충족하지 않음 |

## 3. GPT가 직접 변경한 것
기존 `tools/github_token_check_r0001.py`와 해당 시험 원본은 보존. 별도 `r0002` 파일 2개 추가.
- **GET-only**: PUT/POST/DELETE가 없고 `--probe-write`는 파일 읽기·네트워크 전 거부.
- **상태 분리**: GET/만료/관측 저장소 시험은 PASS/FAIL. 실제 설정된 저장소 선택·전체 권한은 항상 `NOT_PROVEN`. CLI 종료 1=실패, 2=미입증/부분 확인. 이 진단 도구는 설치 준비 완료를 뜻하는 종료 0을 내지 않음.
- `/user/repos?visibility=private` 관측을 사용. 공개 저장소는 PAT의 기본 읽기 범위가 있으므로 “GitHub 전체에서 정확히 하나만 접근 가능”이라고 주장하지 않음. 비공개 관측 한 저장소도 설정 권한 전체의 증거가 아님.
- 90일을 날짜 내림 없이 timestamp로 비교. 90일+1초/만료/헤더 부재 거부. 응답 shape·페이지네이션 불확실성 거부.
- 인증 헤더가 리다이렉트로 전달되지 않도록 redirect 차단. 통신 예외/응답 본문/자격 값/자격 파일 경로를 출력하지 않음. 네트워크 오류는 자동 재시도 없음.

## 4. 실제 시험
환경: GPT Linux Python 3.12.14. HTTP는 전부 모의 응답, 실제 PAT·네트워크 요청 0.
명령(도구 폴더):
```text
python -m unittest -v test_github_token_check_r0001.py test_github_token_check_r0002.py
```
| 범위 | 결과 |
|---|---|
| 보존 r0001 기존 시험 | 11 PASS (기존 의미 검증만; 안전성 승인 아님) |
| 신규 r0002 회귀·경계·오류·비밀 비출력·GET-only | 23 PASS |
| 합계 | 34 PASS / 0 FAIL / 0 SKIP |
| 실제 Windows/실 PAT/운영 설치 | NOT_RUN |
| v0.2.11 제품 전체 시험 | 536 PASS/12 SKIP 및 운영 인터프리터 501 PASS/14 SKIP×3은 Claude 보고 재사용 |
- 기존 r0001에 파일 미종료 ResourceWarning이 나타남. 원본 보존; r0002는 with 문으로 종료.
- 대시보드 TRACKER는 저장소의 실제 `collab/dashboard/work_tracker.py` 검증기로 로컬 후보를 확인하고, 원격 게시 후 readback으로 내용·SHA-256을 재확인. 게시 검증 완료 여부/커밋은 CURRENT 최상단 및 실제 readback 결과를 기준으로 함.

## 5. 산출물 바이트
| 파일(프로젝트 tools/ 기준) | 크기 | SHA-256 |
|---|---:|---|
| github_token_check_r0002.py | 7312 B | `2ab292aa63b23f010620548c91f43cb02a9b182fad10dc5122f63dc0e79fccc4` |
| test_github_token_check_r0002.py | 8469 B | `36b14ff5c2676df44542e66cacdd165e9ec399f936dc1a7e79a5bf69d50452bf` |
후보 watcher ZIP/운영 배포 패키지 변경 없음. 이 보완은 운영 설치 대상이 아니라 협업용 개발 진단 도구.

## 6. Windows Claude Code 다음 한 동작 — delta 자체시험/통합 준비
**이 섹션을 사용자가 Windows Claude Code에 전달하면 허용 범위만 1회 실행. GitHub 게시 자체로 자동 실행되지 않음.**

정확한 입력:
- repository `wonhwipark/CoWork-Skill-Collab`
- branch `main`
- handoff `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_BCD_TOKEN_PRECHECK_DISPOSITION_AND_DELTA_r0001_20261113.md`
- CURRENT `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md`
- 도구 2개 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/tools/*github_token_check_r0002.py` (실제 파일명은 §5)

실행:
1. 최신 CURRENT 최상단이 이 문서를 대체했으면 중단하고 최신 지시 확인. 두 도구의 바이트·SHA-256을 §5와 대조. 격리 개발 폴더로 복사.
2. 개발 환경에서 `python -m unittest -v test_github_token_check_r0002.py` 수행(기대 23 PASS). 운영 인터프리터를 사용해도 새 패키지 설치 없이 동일 모의 시험만 가능. 실제 자격 파일/운영 설정을 읽지 않음.
3. 로컬 `cowork-phase1/token/Install-ReadToken.ps1`을 **실행하지 않고** 원문만 검토. 자격 값/사용자 절대경로를 결과에 복사하지 않음. 설치 스크립트의 **격리 사본**만 r0002 연결에 맞게 보완: 종료 1 실패, 종료 2는 미입증이며 설치/LIVE 허용 근거가 아님. 기존 운영/사용자 설치 스크립트 원본은 보존.
4. GitHub 설정 확인용 비민감 체크리스트 준비: 실제 Resource owner, Only select repositories 대상 1개, Contents:Read-only, Metadata:Read-only, 그 외 repository/account 권한 없음, 만료 ≤90일. 이 확인도 사용자/담당자 진술 증거로 구분하고 API 증명/서명 검증으로 부르지 않음. 값·스크린샷 속 토큰·파일 해시·토큰 일부를 수집하지 않음.
5. r0001의 전체 PASS를 더 이상 설치 준비 증거로 쓰지 않도록 로컬 개발 인계 참조를 보완. 스크립트가 r0002 종료2를 성공으로 우회하지 않는 합성시험 수행. 기존 대규모 제품 시험은 변경/새 실패 근거가 없는 한 재실행하지 않음.
6. 결과는 기존 `CLAUDE_BCD_TOKEN_APPROVAL_PRECHECK_RESULT_FOR_GPT_20261113.md`에 **별도 후속 섹션**으로 추가(이전 원문/해시 이력 보존). `SELF_TEST_REPORTED`, 도구 해시·시험 명령·PASS/FAIL/SKIP/NOT_RUN, 격리 스크립트 상태, 남은 결정과 다음 한 동작만 기록. CURRENT/TRACKER와 함께 PRIVATE main PR 없이 게시, 원격 바이트/SHA-256 재조회. 사용자 경로를 제거할 수 없는 스크립트는 로컬 보존.
7. 사용자 B/C/D/토큰 결정이 없으면 해당 항목은 BLOCKED/PARTIAL 유지. 관리자 셸/시험계정 활성화/실 PAT 검증·발급·설치/운영키·root/ZIP 반출/유료 리뷰/READY/운영 DB·예약 작업·알림·LIVE 변경 금지. 임시 실제 키도 이번 delta에 불필요.
8. 이것은 개발자 자체시험 인계이며 정식 E 독립 리뷰 요청/실행이 아님. 새 모델 리뷰 호출 0.

## 7. 남은 승인 — 재질문 대신 한 묶음으로 유지
B(별도 승인자 기기), C(별도 계정 SHADOW 대체 기준 검토 또는 ETL), D(소유·반출 허가), 토큰(최소 자격 발급·설치 가능 여부)의 **사용자 응답은 아직 없음**. 기존 승인 패킷 §대화 형식을 유지. “다음단계 진행”을 이 네 가지 사실이나 운영 실행 승인으로 치환하지 않음.
- B/C/D/토큰을 선택해도 실키·설치·외부 전송·E 비용·운영 전환의 실제 승인 범위는 별도 확인.
- 유래 파일/신규 파일이라는 분류만으로 회사 소유/개인 소유를 추정하지 않음.
- E 정식 독립 리뷰와 LIVE 최종 승인은 선행 증거 확인 후 별도.

## 8. 참고 근거
- GitHub [PAT 관리](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens): 선택 저장소·권한 설정 및 공개 저장소 기본 읽기 범위.
- GitHub [REST 오류 진단](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api): 403/429 rate limit 및 인증 오류. HTTP 403 단독은 쓰기 권한 부재의 충분조건이 아님.
- GitHub [저장소 API](https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user): private visibility·페이지네이션.
- 운영 계약은 최신 CURRENT 실측을 우선. 예전 계약의 Dropbox LIVE 유지 문구를 현재 provider로 소급하지 않음.
