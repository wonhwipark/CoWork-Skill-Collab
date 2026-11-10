# GPT 판정 — Windows 로그온 없는 시작 호환성 r0001
판정일: 2026-11-11 KST | work_id: COWORK-DROPBOX-TO-GITHUB-MIGRATION
상태: **ACCEPT_WITH_CHANGE / COMPAT_STATUS=PARTIAL / HOST_LOGONLESS_E2E=NOT_RUN**
운영 상태: **MIGRATION_NOT_CUTOVER / Dropbox LIVE 유지**
근거: `main`의 `CLAUDE_NO_LOGON_START_COMPAT_RESULT_FOR_GPT_20261111.md` (GitHub blob `ab14b84699adc5e9e2efee91d3385dc2e321d0fa`) 및 `CURRENT.md`. 독립적으로 Windows 호스트에 접근해 시험하거나 실제 ZIP/로그를 재현한 것은 아님.

## 1. 근거별 판정
| 구분 | Claude 보고 | GPT 판정 | 한계 |
| --- | --- | --- | --- |
| R01 현 예약 작업 4개 조회 | PASS / REAL_READ_ONLY | **ACCEPT** | 4개 모두 InteractiveToken; 기존 서비스/부팅 실행 없음. 문서상 자체 관측 |
| R02 실행 계정·Claude 인증 | PARTIAL | **ACCEPT_WITH_CHANGE** | 로그인 프로필 저장 방식, S4U에서 보호 자격 사용 여부, Windows 계정 암호 존재 여부 UNKNOWN |
| R03 작업 XML·런처 합성 | PASS / SYNTHETIC | **ACCEPT_SYNTHETIC_ONLY** | 파서 수락은 실제 작업 등록·부팅·배치 로그온 권한·Claude 인증 성공의 증거가 아님 |
| R04 방식별 보안 분석 | ANALYSIS | **ACCEPT_AS_DESIGN** | 저장 암호 방식은 관리자 노출 및 자격 관리 위험; 비관리자 실행 우선 |
| R05 운영 변경 없음 | PASS / REAL_READ_ONLY | **ACCEPT_REPORTED_WITH_CAVEAT** | 운영 task/프로세스/설정 등 스냅샷 동일 자체 보고. SQLite `mode=ro`는 SHM에 부수 쓰기 가능하므로 DB main/WAL/SHM 실제 바이트 불변을 R05만으로 확정 금지 |
| R06 호스트 시험 계획 | PLAN / NOT_RUN | **ACCEPT_PLAN_ONLY** | 실제 등록/재부팅/무로그온 유지·롤백·Notifier 연동 전부 미실행 |

## 2. 기술적 판정
- **Windows 자동 로그인 비권장**. 사용자 데스크톱 자동 개방·관리자 및 물리 접근 위험에 비해 불필요한 노출.
- 우선 검토: **시스템 시작 트리거 + 로그온 여부 무관 실행 + S4U**. 암호를 예약 작업에 저장하지 않는 장점이 있으나, Claude Code의 보호된 로그인 정보 접근 및 네트워크 자격 사용 가능 여부가 미검증. **적합 확정 아님**.
- S4U가 불가능하면 **Password 계정 방식**을 별도 검토하되, 기존 관리자 계정의 암호를 저장하는 구성은 권장하지 않음. 가능하면 전용 비관리자 계정·최소 ACL·정책 확인 후 별도 승인. 암호·토큰을 GitHub/로그/프롬프트에 기록하지 말 것.
- `claude_executable` 절대 경로와 `WorkingDirectory` 지정 필요. 현재 CLI는 사용자 PATH에만 있음. GUI·프로필 자격·콘솔 의존성과 세션 속성은 진짜 비대화형 시험 전까지 UNKNOWN.
- 감시기만 무로그온 시작으로 바꿔도 Notifier·Dashboard Updater·Bridge는 InteractiveToken이므로 운영 전반의 무인 가용성은 보장되지 않음. 알림·복구·장애 통지는 별도 운영 게이트.
- 합성 XML에서 `LogonType=S4U`가 수락되었어도 실제 스케줄러 권한·계정 자격·시스템 부팅 트리거 등록이 성공했다고 볼 수 없음.
- **S-1 충돌 방지:** 다른 최신 GPT 판정에 따르면 SQLite `mode=ro` SHADOW 사본에서 SHM 변화가 관찰됨. 이후 SHADOW는 운영 DB/상태 폴더와 물리적으로 분리된 복사본만 사용하고, 실 운영 호스트 DB를 시험으로 직접 열지 않는 것이 우선.

## 3. 추가 확인이 반드시 필요한 조건
1. 비밀 추출 없이 Windows 계정 비밀번호 설정 상태 및 `Log on as a batch job` 권한의 실행 적합성 확인. 암호 상태는 사용자 측에서만 점검하고 공유 불필요.
2. **모델 호출 없는 Claude 인증 전용 preflight**를 격리된 조건에서 확인. 현재 v0.2.5에 preflight 전용 명령은 구현되지 않았다는 Claude 보고가 있으므로 실제 무로그온 인증 PASS로 보고 불가.
3. S4U가 실패해도 B(암호 저장)로 **자동 전환하거나 자격 증명을 생성·저장하지 않음**. 원인과 보안 영향에 대해 사용자에게 별도 결정 요청.
4. 실제 새 예약 작업 등록, 시작 방식 전환, 로그오프·재부팅, 후보 설치, 알림 변경은 각각 운영 변경이므로 **사전 명시 승인 필요**.
5. 보안 시험에서 기존 watcher 1개·단일 ACTIVE_PROVIDER·REQUEST/READY 검증·모델 호출 0을 지킬 것. 운영 DB main/WAL/SHM 및 예약 작업·Telegram에는 쓰기 0.

## 4. 최종 판정 및 다음 행동
- `DEVELOPMENT=SELF_TEST_REPORTED`; `INDEPENDENT_REVIEW=NOT_RUN`; `HOST_LOGONLESS_E2E=NOT_RUN`; `PRODUCTION_CHANGED=false`.
- 지금 단계에서 **Windows 무로그온 시작 적용/재부팅/기존 watcher 중단/모델 호출/LIVE 전환은 승인하지 않음**.
- 다음은 현재 다른 작업에서 준비된 **1차 SHADOW 안전 검증과 충돌하지 않도록 통합**해, 운영과 완전 분리된 테스트 설계 및 최소 권한·프로필 의존성 확인을 먼저 묶어 판정.
- 추후 사용자 명시 승인으로만 시험용 작업 등록과 모델 미호출 부팅 E2E를 진행. S4U 불가라면 Password 방식은 자동 fallback 금지.
- 이전 요청과 결과·영수증, 후보 ZIP 원본을 보존. Dropbox LIVE 유지.
