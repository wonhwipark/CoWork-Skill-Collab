# CLAUDE B·C·D·토큰 승인 사전 점검 결과 (GPT용) 2026-11-13

기준 문서: `GPT_BCD_TOKEN_SINGLE_APPROVAL_PACKET_r0001_20261113.md`. 성격: Windows Claude Code **자체 시험·실측 보고(SELF_TEST_REPORTED)**, 독립 리뷰 아님. 관리자 셸 실행 0, 새 ETW 추적 0, 운영 DB 열기 0(권한 검사는 보안 설명자만 읽음), 모델 호출 0, 비용 $0. 운영 개인키 생성·root 설치·ZIP 업로드·READY 게시·LIVE 활성화 0.

## 0. 요약

| 항목 | 값 |
|---|---|
| ACTIVE_PROVIDER | NONE (이번 세션에서 호스트 운영 설정 변경 작업 0) |
| B | **BLOCKED_SIGNER_DEVICE** — 단, 승인자 기기에 옮길 **서명 키트 6개 파일**(두 `__init__` 포함)을 구성·시험 완료(§2). 사용자 지정만 남음 |
| C | **PARTIAL** — 대체안 4축 증거 수집 완료, 결함 1건 발견·수정(§3). 수락 기준 승인 전 C PASS 아님 |
| D | **BLOCKED_EXPORT_CLASSIFICATION** — 유래 46개 확정·정량화, 대안 3종 정리(§4) |
| 토큰 | **BLOCKED_CREDENTIAL** — 검증기·설치 스크립트 준비·시험 완료, 토큰 발급은 사용자 몫(§5) |
| E | NOT_RUN |
| 후보 | **v0.2.11** 로컬 ZIP 175714 B / 70항목 / SHA-256 `174b9fd83361cc85ce3fb1b4b503335dc701bff9e38415ae23a11256ef8b6350` (미게시). v0.2.10(174745 B, `67ea7fc6…b432b108`)은 **바이트 그대로 보존**, 대체하지 않음 |
| MODEL_NEW_CALLS / USD_SPEND | 0 / 0 |
| CUTOVER | MIGRATION_NOT_CUTOVER |

## 1. 재사용한 증거와 이번 delta
재사용(재실행 안 함): A 비관리자 ACL, 시험키 보안시험, 실GitHub GET-only 3주기, Dropbox 감시기·Bridge·갱신기 Disabled, ETW r0002 합성 시험 20개, v0.2.10 시험 결과.
이번 delta: 후보 코드 결함 1건 수정(v0.2.11), 시험 취약점 1건 수정, 키트·토큰 도구 신규, 시험계정 SID 유효 권한 재계산, 변이 시험(§3).

### v0.2.11 검증 (추출본 기준)
- 시험 venv(cryptography 포함) **536 passed, 12 skipped**; 운영 인터프리터 3회 모두 **501 passed, 14 skipped**. 수집 차이 (536+12)−(501+14)=33, 원인은 이전 보고와 같다(cryptography 필요한 두 모듈 35개 미수집 − 모듈 SKIP 2).
- ZIP 검증 ALL PASS, secret 스캔 0, 개인식별자 스캔 0, 롤백·이행 리허설과 실GitHub read-only 점검 변화 없음(재실행 결과 동일), v0.1.5가 이행본·복원본을 여전히 연다.
- **간헐 실패 원인 규명**: `test_T19_second_watcher_process_cannot_take_the_lock`이 운영 인터프리터에서 8회 중 2회 실패. 원인은 제품 코드가 아니라 시험: 운영 venv의 `python.exe`는 실제 인터프리터를 자식으로 띄우는 런처라서 `kill()`이 런처만 죽이고 잠금을 쥔 자식이 남는다(호스트에서 부모-자식 구조 직접 확인). 프로세스 트리 전체를 종료하도록 수정, 수정 후 운영 인터프리터 16/16·시험 venv 4/4 PASS.

## 2. B — 운영 서명키: 별도 기기 방식과 절차 (키 생성 0)
**방식**: 승인자 기기에서만 Ed25519 키를 만들고, 감시기 PC에는 공개키·지문·pin과 관리자 보호 root만 둔다.

**서명 키트(승인자 기기에 복사할 파일 6개)**: `skill_collab_watcher/__init__.py`(버전 한 줄, 23 B), `approval.py`, `signature_backend.py`, `tools/__init__.py`(0 B), `approval_signer.py`, `trust_root_tool.py`. 이 중 `approval.py`·`signature_backend.py`·`approval_signer.py`·`trust_root_tool.py`는 **v0.1.5에 없던 신규 파일**이고 두 `__init__`는 버전 한 줄과 빈 파일이다. 즉 **v0.1.5 유래 코드를 승인자 기기로 옮길 필요가 없다**(D와 독립). 필요한 외부 패키지는 `cryptography`, `PyYAML`(공개 오픈소스).
- **시험 결과(HOST_REAL, 임시 시험 키, 종료 후 삭제)**: 키트만 경로에 둔 상태에서 keygen 성공(개인키가 표준 출력에 없음, 기존 개인키 파일 덮어쓰기 거부) → trust root 작성 → sign 성공(출력 2개 파일에 개인키 흔적 없음) → check 통과("감시기가 지금 이 승인을 받아들인다") → **패키지를 1바이트 바꾸면 `REFUSED: 패키지가 REQUEST에 선언된 크기·SHA-256과 다름`**. 첫 시도에서 `signature_backend.py` 누락을 발견해 키트에 포함시켰고, 그 시도의 "변조 거부"는 예외 때문이라 가짜 통과였음을 확인한 뒤 원인 파일을 포함해 재시험한 결과만 채택했다.

**사용자 절차(요약)**
1. 감시기 PC와 **다른 신뢰된 기기**(회사 관리 PC 권장) 지정. 개인키 파일은 BitLocker로 암호화된 디스크 또는 오프라인 매체에만 둔다. **한계**: 도구는 개인키를 암호문으로 저장하지 않고 평문(base64) 파일로 쓴다. 저장 매체 암호화가 유일한 보호이며 필요하면 비밀번호 보호 옵션을 후속 개발 항목으로 둘 수 있다.
2. 승인자 기기에서 `keygen` 실행. 출력의 **공개키·지문만** 감시기 PC로 옮긴다(USB·메신저 모두 가능, 공개정보). 개인키는 채팅·GitHub·Dropbox·감시기 PC에 두지 않는다.
3. 감시기 PC에서 `trust_root_tool build`로 root(버전 1)와 pin을 만들고, 관리자만 쓸 수 있는 폴더에 배치(상속 제거, 시험 계정은 읽기만). 시험 계정으로 `inspect`·LIVE 열기를 실행해 `TRUST_ROOT_LOADED`를 확인(대조: 쓰기 가능한 폴더에서는 `NOT_INDEPENDENT`로 거부, Stage 1 HOST_REAL 확인됨).
4. 서명은 승인마다 승인자 기기에서 `sign`: 요청 ID·ZIP SHA·고정 커밋·정책 revision·비용 상한·nonce·만료를 모두 서명하며, 문장 텍스트는 신뢰하지 않는다. 최대 유효 168시간.
5. 폐기·교체: root 버전을 올려 키 상태를 REVOKED/RETIRED로 바꾼다(버전 래칫으로 롤백 거부, 시험 PASS).
- 이번 점검에서 **키 생성·root 설치·pin 기록 0**. 사용자가 기기를 지정하고 각 행위를 별도로 승인해야 한다.

## 3. C — 운영 격리 대체안 4축 분석 (ETW 재측정 안 함)
**축 1. Windows ACL (HOST_REAL, 이번 세션 신규 계산)**: 시험 계정 SID의 유효 권한을 보안 설명자에서만 계산(파일 데이터는 열지 않음, `GetEffectiveRightsFromAclW`). 운영 상태 폴더, `state.sqlite3`, `-wal`, `-shm`, `runs` 폴더 **모두 마스크 0x0(권한 없음)**. 대조군: 자기 shadow 폴더 읽기·쓰기(0x1301BF), trust 폴더·후보 코드 읽기 전용(0x1200A9), 임의 시스템 파일 읽기. 앞서 Stage 1의 실제 접근 시도에서도 폴더가 보이지 않음(거부)이 HOST_REAL로 확인되어 있다.
**축 2. 독립 상태 경로 + 파일 identity (SYNTHETIC + HOST_REAL)**: 경로 가드는 UNC·상대경로·드라이브 루트·junction·8.3 이름·겹침·identity 별칭을 거부하고, 열 수 없는 운영 폴더에서도 비정상 종료하지 않는다(호스트 결함 2건 수정, v0.2.10 이상). SHADOW 3주기 실측에서 운영 폴더 목록 불변·자체 폴더에만 DB/lock/runs 생성(Stage 1, HOST_REAL).
**축 3. 실행 경로 (정적 + 동작, 이번 세션 신규)**: 라이브 폴더(`state_dir`/`local_state_dir`)를 참조하는 함수를 코드 전체에서 전수 조사해 **6개**(`_work_dir`의 LIVE 분기, `_build_transport`의 Dropbox 분기, `config-check`, `auth-check`, `auth-init`, 설정 속성 하나)로 확정, 정적 회귀 가드 시험으로 고정. 이 조사에서 **실제 결함 발견**: `config-check`·`auth-check`·`auth-init`이 SHADOW·GitHub 설정에서도 라이브 폴더를 만들고 Dropbox 비밀을 읽거나 쓸 수 있었다(`watch`/`scan`/`status`/`reconcile`/`recover`는 해당 없음). 재현 시험 → 수정(Dropbox 전용 명령은 GitHub 설정에서 거부, `config-check`는 GitHub에서 비밀을 읽지 않음) → v0.2.11. 이 결함은 DB가 아니라 비밀 파일 영역이다. `watch`를 계측하는 ETW는 이 명령들을 실행하지 않으므로 볼 수 없는 경로이고, 코드 전수 조사로만 발견할 수 있었다.
**축 4. 양성·음성 대조 (SELF_TEST + HOST_REAL)**: 변이 시험 4종(SHADOW가 라이브 폴더를 사용 / 경로 가드 무력화 / 라이브 폴더를 읽는 새 함수 추가 / 수정 되돌림) **전부 시험이 실패로 검출**. 양성 대조는 ACL 대조군과 Stage 1의 미끼 파일 열기 관찰.

**판정**: `C_ALT_EVIDENCE = 조건부 충족 (별도 계정 SHADOW 구성 한정)`. `C = PARTIAL` 유지 — 수락 기준 변경은 GPT·사용자 승인 사항이며 이 문서는 PASS 선언이 아니다. 기존 ETW `FAIL_UNTRUSTED_MEASUREMENT` 이력은 그대로 보존한다.
**한계(숨기지 않음)**: ①축 1은 **시험 계정을 쓰는 구성**에서만 보호한다. LIVE 감시기가 사용자 본인 계정으로 돌면 ACL은 보호가 아니며 축 2·3과 코드 시험에만 의존한다. ②DACL 계산은 관리자·SYSTEM·백업 권한 같은 우회 경로를 다루지 않는다. ③실 프로세스 파일 I/O 증거(ETW)는 여전히 NOT_PROVEN. ④운영 DB는 현재 아무도 쓰지 않는 보관본(감시기 Disabled)이라 위험은 손상 방지에 한정된다.

## 4. D — 소스 반출 분류
v0.2.11 ZIP 70항목을 v0.1.5와 해시·줄 단위로 비교: **UNCHANGED 34 + CHANGED 12 = 유래 46 / NEW 24** (v0.2.10과 동일 분류).
- UNCHANGED 34 (3957줄): 패키지 8, 시험 17, windows 스크립트 5, config 예시 1, 프롬프트 1, 빈 `__init__` 1, requirements 1.
- CHANGED 12 (3375줄): 신규 추가 약 890줄, **v0.1.5 줄 약 74%(2485줄) 유지**. 파일별 유지율 — validator 94, review_runner 90, conftest 88, fake_runner 85, cli 81, config 79, transport_base 72, orchestrator 70, zip_safety 61, state_store 40, `__init__` 0(버전 한 줄), build_release 99.
- NEW 24 (5014줄): 시험 15, 패키지 5, 도구 2, 문서 1, 루트 1. 이 협업에서 작성했으나 소유·정책 확인은 사용자 몫.
- **유래 비율**: 전체 약 12,346줄 중 v0.1.5 유래 약 6,442줄(약 52%).
- 비밀 스캔 PASS는 반출 허가가 아니다. 유래 46개의 소유권과 사외 반출 허가가 확인되지 않아 **ZIP 전량 PRIVATE 업로드 금지**, 로컬 보존.

**대안 3종**
- (a) **전량 게시**: 조직이 유래 46개 반출을 승인하면 v0.2.11을 신규 파일명으로 게시. 가장 간단하지만 승인 필요.
- (b) **신규 24개만**: 게시 가능 여부는 소유 확인에 달렸다. 한계: 신규 시험 15개는 미게시 유래 모듈을 임포트해 실행 불가, 따라서 **정적 검토만 가능**하고 전량 ZIP 독립 리뷰가 아니다(부분 검토로 명시).
- (c) **사내 로컬 리뷰**: GitHub 없이 사내에서 검토. 두 갈래를 구분해야 한다 — ①사람 검토자 또는 **사내 LLM**(OpenCode·Roo Code 등)은 코드가 외부로 나가지 않는다. ②**Claude 계열 모델에 코드를 읽히는 것도 모델 제공사로의 전송**이므로 조직 정책상 반출과 같은 승인 대상일 수 있다(이 개발 세션이 이미 이 코드를 처리했다는 사실도 같은 정책 질문이다). 어느 쪽이든 서명된 READY·영수증 절차와는 별개 경로이므로 설계가 필요하다.
- 서명 키트(§2)는 유래 코드가 없어 D 결정과 무관하게 이동 가능.

## 5. GitHub Contents 읽기 전용 토큰
**준비 완료(시험 PASS)**
- 검증기 `github_token_check_r0001.py`(+시험 11 PASS, PRIVATE `tools/`에 게시): 토큰을 파일에서만 읽고 출력하지 않으며, ①fine-grained PAT 종류 ②GitHub 수락 ③OAuth 스코프 헤더 없음 ④만료 90일 이내 ⑤`/user/repos`가 **정확히 이 저장소 1개** ⑥Contents 읽기 성공 ⑦(옵션 `--probe-write`) 잘못된 PUT 1회가 403이면 쓰기 불가(422면 쓰기 가능으로 FAIL; 본문이 무효라 아무것도 쓰이지 않음). 현재 호스트의 gh 토큰(`gho_` OAuth, repo·workflow 스코프)은 ①③⑤에서 FAIL할 것이다.
- 설치 스크립트(로컬 보존, 경로 포함이라 미게시): 관리자 셸에서 1회 실행, 토큰은 입력이 **표시되지 않는 프롬프트**로만 받아 시험 계정 전용 폴더의 파일 1개에 기록, 폴더 상속 제거·Administrators/SYSTEM 전체 권한·시험 계정 **읽기 전용(0x120089)**. 기존 토큰 파일은 덮어쓰지 않는다. `-SelfTest`(더미 값, 네트워크 없음)로 ACL 레이아웃을 호스트에서 확인했고 자체 폴더는 삭제됐다. `-RunCheck`는 시험 계정으로 검증기를 실행한다.

**사용자 UI 절차**: GitHub 설정 → Developer settings → Fine-grained tokens → 새 토큰: Resource owner=본인, **Only select repositories → `CoWork-Skill-Collab` 하나**, Repository permissions → **Contents: Read-only**(Metadata는 자동 필수), 만료 ≤90일. 값은 채팅·문서에 붙이지 말고 설치 스크립트의 숨김 입력에만 입력.
- 설치 전 `BLOCKED_CREDENTIAL`. 단기 GET 성공과 시험 계정 영구 설치는 별개로 표시한다. 이번 점검에서 토큰 생성·설치·네트워크 호출 0.

## 6. 사용자 결정 (B → C → D → 토큰 순, 숫자로 답)
- **B**: 1=별도 승인자 기기 지정 가능(서명 키트 사용 가능), 2=추후, 3=불가(대안 검토)
- **C**: 1=4축 대체증거를 수락 기준으로 검토·승인(**추천**, 단 한계 ①을 이해한 상태에서 별도 계정 SHADOW 구성 전제), 2=보존 ETL 재분석 선호, 3=보류
- **D**: 1=조직 반출 허가 확인 진행(전량 게시 가능성), 2=허가 불가/로컬-only(사내 LLM·사람 검토 대안 설계로 진행), 3=이미 정식 허가 확보(증빙 범위 확인 필요)
- **토큰**: 1=발급·설치 가능(UI 절차와 설치 스크립트 사용), 2=기존 최소 권한 자격 확인 필요, 3=현재 불가
각 "가능"은 실제 실행 승인과 다르며, E 비용·독립성과 LIVE 전환은 선행 요건 검증 후 별도 승인이다.

## 7. 보호 범위
운영 watcher·DB·작업·Bridge·알림기·인증·토큰·Dropbox history 변경 0. 추가물은 로컬 시험 도구·임시 시험 키(삭제)·이 결과·`tools/` 도구뿐. 시험 계정 비활성·샌드박스 보존 유지.
