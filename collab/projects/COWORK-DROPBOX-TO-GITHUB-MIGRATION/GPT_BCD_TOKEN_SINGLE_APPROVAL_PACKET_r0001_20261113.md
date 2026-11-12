# GitHub LIVE B·C·D·GitHub 인증 단일 승인/실행 준비 패킷
기준일: 2026-11-13 KST | r0001
PRIVATE: `wonhwipark/CoWork-Skill-Collab` | branch `main`
Work: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
상태: **DECISION_PACKET_READY / USER_DECISIONS_PENDING / HOST_OPERATIONS_NOT_APPROVED**
전제: `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`; E 정식 독립 리뷰 `NOT_RUN`.

## 읽어야 할 정본
- `collab/START_HERE.md`와 현재 작업 `CURRENT.md` 최상단.
- `GPT_GITHUB_LIVE_MINIMUM_REWORK_MASTER_r0001_20261113.md`.
- `CLAUDE_GITHUB_LIVE_FAST_TRACK_READINESS_RESULT_FOR_GPT_20261113.md`.
- `GPT_MINIMUM_REWORK_RESULT_DISPOSITION_r0001_20261113.md`.
이미 완료된 시험과 호스트 보고는 재사용하고 **변경된 delta만** 분석·시험. 기존 watcher/Bridge/updater Disabled 상태 보존.

## 하나의 의사결정 패킷
**B — 승인자 별도 기기 및 신뢰 루트**
- 사용자가 감시기 Windows PC와 **다른 신뢰된 승인자 기기**를 하나 지정하는지 확인.
- 운영 Ed25519 **개인키는 해당 승인자 기기에서만 생성·보관**, PRIVATE GitHub/Dropbox/채팅/Windows watcher에 전달하지 않는다. Windows watcher에는 공개키·fingerprint·pin과 관리자 보호된 root만 설치하도록 구성.
- 이 단계에서는 기기 선택/보안·설치 절차·분리 시험 계획만 정리. **키 생성·root 변경·운영 설치는 별도 명시 승인 전 0**.

**C — 운영 격리 수락 기준 선택**
- 추천: 독립 비관리자 계정 ACL 접근거부 + SHADOW 독립 상태 디렉터리/파일 identity·경로별칭 + 실행 call path/프로세스 권한 + 음성/양성 대조의 **4축 대체 증거**를 검토 대상으로 선택.
- 이 선택은 **검증 방법 변경 제안**이며 C의 즉시 PASS가 아니다. 실제 증거와 적합성을 별도 검증해야 `C_ALT=PASS` 가능. 기존 ETW `FAIL_UNTRUSTED_MEASUREMENT` 이력 보존.
- 대안: 보존 ETL을 해독·사전검증하고 필요하면 신규 관리자 실제 계측 **1회**. 반복 관리자 셸 금지.

**D — 후보 소스 외부 반출**
- Windows 로컬 `v0.2.10` ZIP 70항목: UNCHANGED 34 + CHANGED 12(둘 모두 기존 v0.1.5 유래 총 46), NEW 24. **PRIVATE도 사외**.
- 사용자/조직이 각 유래 소스·신규 소스의 소유권과 사외 반출 허가를 확인한 범위만 게시 가능. 비밀 스캔 PASS는 반출 승인이 아님.
- 전량 허가 불가하면 내부 로컬 독립 리뷰 또는 공개 가능한 신규·요약만으로 부분 리뷰를 수행하는 *별도 대안 설계*를 준비. 부분 리뷰를 전량 ZIP 독립 리뷰로 표시하지 않는다. 반출 여부를 사용자 임의 진술만으로 조직 허가로 소급하지 않는다.

**GitHub 읽기 전용 자격**
- `CoWork-Skill-Collab` 한 저장소만 Contents:Read-only로 읽는 최소 권한 Fine-grained credential을 사용자 측에서 안전하게 발급·설치하도록 **UI 단계와 현장 확인 절차** 제공.
- 채팅·문서·로그·결과 MD에 PAT 값 절대 적지 않으며 과권한 GitHub 인증으로 대체하지 않는다. 단기 실GitHub GET 성공과 시험계정 영구 자격 설치는 별개로 표시.
- 설치 전 `BLOCKED_CREDENTIAL`; 시험계정 비활성·운영 인증 변경 금지.

## 승인 대화 형식 (사용자가 숫자로 답할 수 있게)
- B: 1=별도 승인자 기기 지정 가능, 2=추후, 3=불가(대안 검토).
- C: 1=4축 대체증거 기준 검토 승인(추천), 2=보존 ETL 재분석 선호, 3=보류.
- D: 1=조직 반출 허가 확인 진행, 2=허가 불가/로컬-only, 3=이미 정식 허가 확보(증빙 범위 확인 필요).
- 토큰: 1=발급·설치 가능, 2=기존 최소 권한 자격 확인 필요, 3=현재 불가.
각각의 '가능'은 해당 실제 실행 승인과 다른 사실. 표준 질문은 위 4개만 한 번에 한다.

## 허용 실행과 금지
- Windows Claude Code는 최신 문서·코드·Task 정의의 **읽기 전용 확인**, 실측 가능한 합성시험과 격리 경로 보완, 조건별 작업자 체크리스트, 필요한 입력 정보 **한 번에 통합 보고**까지 수행 가능.
- 이 승인 패킷 작성·GitHub 게시는 사용자/조직의 실제 D 반출 허가, 운영 B 키 설치, 장기 토큰 발급, C 수락기준 변경, 유료 E 독립 리뷰 또는 최종 LIVE 승인 아님.
- 원본 운영 DB(SQLite ro 포함), 예약 작업·Notifier·Bridge·Dropbox history·비밀·키·토큰·LIVE provider/README의 승인 조건을 변경하지 않는다.
- 추가 결과 문서는 필요하면 `CLAUDE_BCD_TOKEN_APPROVAL_PRECHECK_RESULT_FOR_GPT_20261113.md` **하나만**, `CURRENT.md` 최상단/유효 TRACKER와 함께 PRIVATE main PR 없이 직접 게시·remote readback. 다른 과거 인계를 다시 실행하지 않는다.

사용자가 B/C/D/토큰 결정을 한 번에 제공하면 각각 충족한 게이트에 한정한 새 실행 승인만 후속 진행한다. E 비용·독립성과 LIVE 전환은 후속 별도 명시 승인.
