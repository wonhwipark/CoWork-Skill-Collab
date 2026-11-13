# CLAUDE 단일 사용자 SU-L1 LOCAL_ONLY 패스트트랙 결과 (GPT용) 2026-11-14

기준 인계: `GPT_SINGLE_USER_LOCAL_ONLY_LIVE_FASTTRACK_MASTER_r0001_20261114.md` 하나. 성격: Windows Claude Code **자체 시험·실측 보고(SELF_TEST_REPORTED)**, 독립 리뷰 아님.
이번 작업에서 **하지 않은 것**: 운영키·PAT 발급/설치, 운영 계정·ACL·예약 작업·운영 DB 변경(운영 DB는 열지 않음; 새 시험 원장은 임시 폴더의 별도 파일), 코드·ZIP·원시 해시·크기·경로의 GitHub 게시, 외부 모델 호출 추가, 유료 리뷰, READY/REQUEST 게시, LIVE 활성화. 모델 호출 0, 비용 $0.

## 0. 최종 표시
| 항목 | 값 |
|---|---|
| ACTIVE_PROVIDER / GITHUB_LIVE / CUTOVER | NONE / NOT_RUN / MIGRATION_NOT_CUTOVER |
| LANE_A 원장 결함 2건 | **FIXED_AND_RETESTED** (`local_only_contract_r0003`, SELF_TEST) |
| CONTRACT_INTEGRATION | **NOT_RUN** (감시기 제품 경로에 연결하지 않음) |
| LANE_B SU-L1 정책 엔진 | **PROTOTYPE_SELF_TESTED**, 기능 플래그 기본 OFF, 제품 미연결 |
| LANE_C 로컬 리뷰어 | **E=BLOCKED_LOCAL_REVIEWER**, AUTO_REVIEW=NOT_RUN |
| LANE_D | 문서·초안·시뮬레이션 완료, 실제 적용 NOT_RUN, ROLLBACK_READY=PARTIAL |
| 후보 ZIP | v0.2.13 로컬 보존·검증 완료 (미게시) |
| INDEPENDENT_REVIEW | NOT_RUN |
| 상태 | **DEVELOPMENT_READY_NOT_FOR_DEPLOYMENT** |

## 1. 현재 상태 요약
Dropbox 감시기·Bridge·갱신기 Disabled(프로세스 0), 알림기 Running 유지. 새 예약 작업·계정 없음. 이번 작업은 로컬 개발·시험 폴더와 로컬 후보 ZIP, 이 결과 및 비민감 시험 도구의 게시에 한정.

## 2. 구현 변경 요약
### Lane A — 원장 hardening (`local_only_contract_r0003`, 새 파일; r0001·r0002 이력 보존)
- **결함 재현(r0002)**: 같은 nonce를 6개 프로세스가 동시에 "읽고→판단→저장"하는 r0002 패턴에서 2개가 ACCEPTED(재현 하니스는 판단 지연 50ms를 둔 모델이며 실제 창은 더 짧을 수 있으나 잠금·원자성이 전혀 없다는 점을 확인). 상태 파일 삭제 후 `State()`는 빈 집합으로 시작(replay 허용)함을 확인.
- **수정**: ① 별도 개인 SQLite 원장(PRIMARY KEY로 nonce·영수증·리뷰 예약 유일성) + OS 파일 잠금 + `BEGIN IMMEDIATE`, 실패 시 전체 롤백. 고정 `.tmp` 대신 쓰기마다 고유 임시 이름. ② 첫 생성과 분실 분리: 명시 확인 문구가 있는 **1회 bootstrap**만 생성 가능, 이후 `open`은 파일 없음·앵커 없음·genesis 불일치·**과거 사본 복원(rollback)**·이력 해시 불일치·손상 모두 `FAIL_CLOSED`. 앵커(`genesis+seq+head`)는 DB 밖의 별도 파일이며 커밋 후에 올라가므로(지연은 안전한 방향) 크래시에 안전.
- **리뷰 예약**: 리뷰어 시작 전 원자적 1회 예약, 요청당 최대 1 시도, 동시 활성 상한(트랜잭션 내부 검사). 프로세스가 죽은 RESERVED는 `UNCERTAIN`으로 봉인하고 재예약·재호출 0.
- 개발 중 발견·수정한 결함: `_verify`의 `except ValueError`가 `ContractError`(ValueError 하위)까지 삼켜 구체 사유를 `STATE_UNREADABLE`로 덮음 → 수정; `sqlite3.connect`가 없는 DB를 **조용히 새로 만드는** 문제 → 존재 확인 후 `STATE_MISSING_AFTER_INITIALIZATION`.
### Lane B — SU-L1 정책 엔진 (`su_l1_policy_r0001`, 기능 플래그 기본 OFF)
관리자 보호 로컬 정책(repo ID·branch·work ID 허용목록·승인 artifact 폴더·reviewer runner·허용 OS 주체·`LOCAL_ONLY`·비용 0.00·활성 1·시도 1·만료·kill switch·정책 epoch 단조 증가) + 로컬 OS 사용자 + 로컬 artifact 커밋먼트 결합. **GitHub 요청의 어떤 필드도 승인이 되지 않으며** 추가 필드(`approved` 등)는 거부. 정책 ACL을 읽기 전용(`icacls` 파싱)으로 검사해 비관리자 쓰기 가능이면 `POLICY_NOT_ADMIN_PROTECTED`(검증 불가도 FAIL_CLOSED). 경로 이탈·심볼릭 링크 이탈 거부. Ed25519 운영키는 이 모드의 필수 조건이 아님(별도 서명자 PC 요구 제거).
### Lane D — 개발 문서·시뮬레이션
공개 허용 최소 필드 영수증 게시 **시뮬레이션**(가짜 원격: add-only, 누출 검사, 바이트·blob 해시 readback, 네트워크·토큰 0). 서비스 계정·ACL·작업 적용/롤백 명령 초안, 신규 PAT 발급 UI 8항목, 결과 쓰기 서비스 분리 설계, 이행·재시작·롤백 계획은 **로컬 문서**(실행 안 함).

> 주의: 이 문서가 인용하는 코드(r0003, SU-L1, 시뮬레이션)와 후보 ZIP은 **로컬 전용이며 GPT가 직접 읽을 수 없다**(§6). 아래 수치는 모두 개발 세션 자체 보고다.

## 3. 시험 결과 (HOST_REAL / SYNTHETIC / SELF_TEST 구분)
| 시험 | 결과 | 구분 |
|---|---|---|
| r0003 원장·계약 28개(동일 nonce 6프로세스 정확히 1 수락, 동일 영수증 6프로세스 1 수락, 서로 다른 nonce 8프로세스 갱신 손실 0, 동시 예약 1, 재시작 replay 0, DB 삭제·앵커 삭제·과거 사본·타 원장·이력 변조·손상 → FAIL_CLOSED, 상태 분실 후 리뷰 호출 0, 프로세스 사망 후 UNCERTAIN·재호출 0, 커밋 후 앵커 전 크래시, 트랜잭션 도중 예외 무커밋, `os.replace` 오류, 잠금 보유 프로세스 사망/생존 시 해제/타임아웃, 원장 파일에 다이제스트·솔트·리뷰 텍스트 없음) ×3회 | **28 PASS ×3** | SELF_TEST(실제 다중 OS 프로세스, 합성 키) |
| r0003 변이 14종(중복 허용, 영수증 중복 허용, 재예약 허용, 파일 없음=신규, 앵커 무시, 롤백·genesis·이력 미검사, 봉인 안 함, 사유 가림, 사전검사 전 nonce 소비, 미등록 요청 영수증, 롤백 안 함) | **14/14 검출** | SELF_TEST |
| SU-L1 정책 19개 | 18 PASS, **1 SKIP**(심볼릭 링크 생성 권한 없음; PASS로 세지 않음) ×3회 | SELF_TEST + 1건 HOST_REAL(아래) |
| SU-L1 변이 18종 | **18/18 검출** | SELF_TEST |
| 호스트 실측(읽기 전용): 이 PC의 사용자 소유 임시 파일에 실제 `icacls` 적용 → 비관리자 쓰기 가능으로 판정 → `POLICY_NOT_ADMIN_PROTECTED` | PASS(음성 사례) | **HOST_REAL**(ACL 변경 0) |
| 영수증 게시 시뮬레이션 4개 | 4 PASS(반복 8회) — 작성 중 시험 오류 1건(크기 숫자가 무작위 hex의 부분 문자열) 발견·수정 | SYNTHETIC |
| 후보 v0.2.13 제품 전체 | 시험 venv **642 passed, 13 skipped**; 운영 인터프리터 3회 **536 passed, 19 skipped**(cryptography 필요 모듈 3개는 importorskip로 SKIP) | SELF_TEST (패키징·버전 변경 때문에 1회 전체 실행; 이전 566/12·518/15 대비 신규 77개) |
| 압축 해제본에서 `su_l1`+패키징 시험 | 87 passed, 1 skipped | SELF_TEST |
- **재사용(재실행 안 함)**: ETW r0002 합성 20, 토큰 모의 34, 설치 스크립트 격리 사본 18, 시험 계정 ACL 실측, 롤백 리허설 근거, reviewer probe 12.
- **미수행/한계**: ETW 실 프로세스 I/O 증거 `NOT_PROVEN` 유지(`C_OVERALL=PARTIAL`), 시험 계정 실행·서비스 계정 실제 격리 `NOT_RUN`, 제품 경로 연결 `NOT_RUN`, 동시성 시험은 이 PC의 로컬 NTFS에서만 확인(네트워크 드라이브·동기화 폴더는 미검증이므로 원장·앵커는 **동기화 폴더 밖 로컬 디스크**에 둔다는 조건을 둔다).
- **보안 한계(그대로 고지)**: 원장과 앵커, 정책, 관리자 계정이 같은 PC에 있으므로 **그 관리자 계정이 침해되면 막지 못한다**. 앵커·원장을 둘 다 삭제하고 `bootstrap`을 다시 승인하면 새 시작이 가능하다(자동 복구는 없고 명시 오프라인 조작으로 한정). reviewer 위치는 서명된 주장(`ATTESTED_NOT_VERIFIED`) 그대로.

## 4. 제품 ZIP 후보 (로컬 검증, 원시 해시·크기·경로 비게시)
- v0.2.13 = v0.2.12 + `su_l1/` 12개 파일(모듈·시험·변이 검사·README) 추가, 변경 3개(버전, 런북 첫 줄, 패키징 허용 목록에 `su_l1`). 83항목(71+12), 제거 0. 기본 설정으로는 SU-L1이 어디에도 연결되지 않음.
- 불투명 ID `art-c0c576f15eb39f01`, 솔트 커밋먼트 `a759dd2c6eee54ae321d3a0026e3d6e697c573d6302b520e000e818f7f938b34`(솔트·다이제스트는 로컬 파일만).
- 결정적 재빌드 바이트 동일, ZIP 무결성 OK, secret 스캔 83파일 발견 0, 로컬 자격 값 대조 2건 0, v0.2.12 ZIP 바이트 불변.

## 5. Lane C — 로컬 독립 리뷰어
이번 작업에서 새로 탐색·probing 하지 않았다(인계 지시). 이전 실측 재사용: 이 PC에 로컬 모델 런타임 없음, 외부 접속 가능(`NOT_ISOLATED`), 조직 승인 온프레미스 호스트·사람 reviewer 존재 미확인 → **`E=BLOCKED_LOCAL_REVIEWER`, `AUTO_REVIEW=NOT_RUN`**. 이 개발 세션의 Claude 자체 검토로 대체하지 않았다.
**정책 확인 필요(§2-5)**: Claude Code 백엔드는 외부 서비스이므로 이 개발 세션이 읽은 제품·도구 코드가 외부 모델로 전송된다. 이전 작업도 같은 구조였으며 이번에 새로 만든 개념 증명 코드는 모두 합성 데이터만 담았다. 이 전송이 조직 정책상 허용되는지는 사용자 확인 사항이다(§7-6).

## 6. 게시 범위
GitHub PRIVATE에는 ① 이 결과 MD, ② CURRENT 최상단·TRACKER 필드만 게시한다. **코드는 게시하지 않았다**: `local_only_contract_r0003`·`su_l1_policy_r0001`·`receipt_publish_sim_r0001`과 각 시험·변이 검사·워커(합성 데이터만 포함), 제품 소스·ZIP, `LANE_D` 로컬 초안, 솔트, 실 다이제스트는 모두 이 PC의 로컬에만 있다(마스터 §4 "코드 게시 금지" 준수; 게시 시도는 자동 권한 판정이 거부해 우회하지 않았다). 따라서 GPT가 r0003·SU-L1 소스를 직접 정적 검토하려면 **코드를 PRIVATE에 올리는 것을 사용자가 별도로 승인**하거나 조직이 허용한 다른 경로가 필요하다(§7-6에 포함). 그 전까지 이 문서의 시험 수치는 `SELF_TEST_REPORTED`이며 소스 검토 가능성은 `NOT_AVAILABLE_TO_GPT`이다.
게시에 쓴 GitHub 자격은 개발자 도구(`gh`) 기존 로그인으로 이전 결과 게시와 동일하다. 감시기·SU-L1이 쓰는 토큰이 아니며 교체는 §7-2에 포함.

## 7. 실제 LIVE로 가기 위한 사용자 승인 묶음 (한 번에, 항목별 별도 승인)
1. **리뷰어**: 조직 승인 온프레미스 모델 호스트 또는 독립 사람 reviewer가 있는가(종류·코드 외부 전송 차단 가능 여부)? 없으면 E는 BLOCKED 유지이며 LIVE 불가.
2. **토큰**: 신규 fine-grained **읽기 전용** PAT 직접 발급·설치(UI 8항목은 로컬 초안), 결과 쓰기용 별도 자격(저장소 단위 Contents write + 브랜치 ruleset; 경로 제한 가능 여부는 플랜 의존 `NOT_PROVEN`), 개발자 도구 `gh` 광역 자격 교체.
3. **비관리자 서비스 계정·ACL·예약 작업 적용**과 구 운영 폴더에 대한 명시 거부 ACE(운영 ACL 변경).
4. **SU-L1 정책 활성화**(정책 파일 설치, 원장 bootstrap, 운영 데이터 이행 방식=제자리 보존·비이행, rollback 계획).
5. **실제 독립 검토 실행**(비용 0 로컬 한정)과 **최종 GitHub LIVE 전환**.
6. **조직 정책 확인**: 개발 세션(외부 모델)의 코드 열람 허용 여부, 이미 게시된 SHA·크기·파일명 이력의 분류, 그리고 합성 데이터만 담은 개념 증명 코드(r0003·SU-L1)를 GPT 검토용으로 PRIVATE `tools/`에 올려도 되는지.
수락 기준 현황: 최소권한 인증·호스트 격리 HOST_REAL `NOT_RUN`, 원장 race·loss·crash 회귀 `PASS(SELF_TEST)`, 실 독립 reviewer `BLOCKED`, 영수증 원격 readback 시뮬레이션만, 재실행 0 `PASS(SELF_TEST)`, 알림 dedup 미연결, 미정산 이력 보존 계획, rollback/backup HOST_REAL `NOT_RUN`, ACTIVE_PROVIDER 단일 `NONE`. → **LIVE 불충족, `DEVELOPMENT_READY_NOT_FOR_DEPLOYMENT`**.

`LANE_A=FIXED_AND_RETESTED; CONTRACT_INTEGRATION=NOT_RUN; LANE_B=PROTOTYPE_SELF_TESTED; E=BLOCKED_LOCAL_REVIEWER; AUTO_REVIEW=NOT_RUN; ZIP_CANDIDATE=v0.2.13_LOCAL_ONLY; INDEPENDENT_REVIEW=NOT_RUN; ACTIVE_PROVIDER=NONE; GITHUB_LIVE=NOT_RUN; CUTOVER=MIGRATION_NOT_CUTOVER`
