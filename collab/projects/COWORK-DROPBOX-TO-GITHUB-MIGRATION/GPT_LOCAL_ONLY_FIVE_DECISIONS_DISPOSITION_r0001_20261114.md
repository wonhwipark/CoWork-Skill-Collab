# GPT 판정·선택 권고 — LOCAL_ONLY GitHub LIVE 잔여 5개 결정
날짜: 2026-11-14 KST | r0001
저장소: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` | branch `main`
work_id: `COWORK-DROPBOX-TO-GITHUB-MIGRATION`
상태: **GPT_RECOMMENDATION / USER_OR_ORG_CONFIRMATION_REQUIRED / NO_OPERATIONAL_APPROVAL**
최신 결과: `CLAUDE_B1_C1_D2_TOKEN2_LOCAL_ONLY_RESULT_FOR_GPT_20261114.md` (host SELF_TEST_REPORTED, GitHub commit `615da26d0257cbb864689c1c3a52210f66f34265`).
LIVE: `ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`; 독립 리뷰 `NOT_RUN`.

## 1. 현재 상황 판단
- D=2 LOCAL_ONLY: 개발 코드·후보 ZIP·원본 diff·고객/사내 제한 데이터의 PRIVATE GitHub 포함 외부 업로드 금지. GitHub는 최소 승인된 메타데이터·정책/영수증 중심의 control plane만. 단 기존 외부 ZIP 원문을 요구하는 GitHub `Commit A/READY` 계약은 **D2에 그대로 사용 불가**.
- Windows Claude의 로컬 v0.2.12(71항목) 자체시험: 시험 venv 566 PASS/12 SKIP, 운영 518 PASS/15 SKIP ×3, 비관리자 SHADOW 계정검사 17 PASS·변이 5, 암호화 서명 키 13 PASS, 로컬 제어면 프로토타입 19 PASS·변이 5 모두 **SELF_TEST_REPORTED**, 독립 리뷰/E2E LIVE PASS 아님. 사용자가 확인하지 않은 기기/리뷰어 정책을 추정 승인으로 승격 금지.
- 현재 Windows에서는 로컬 LLM 런타임이 관측되지 않았으며, 다른 조직 승인 온프레미스 호스트·사람 리뷰어의 존재/접근권은 확인되지 않았다.
- 현 자격은 classic OAuth 범위가 넓고 fine-grained 단일 저장소 읽기 전용으로 검증되지 않음.
- LIVE 운영자 계정은 보호된 오래된 운영 DB/WAL/SHM에 전체 권한 있음. 이전 별도 시험 SHADOW 계정 ACL deny 근거를 운영자 계정 LIVE에 소급할 수 없음.

## 2. 사용자 질문 5개에 대한 GPT 권장·확인 경계
| # | 선택 | GPT 권고 | 사용자/조직 확인 필요 | 승인 전 판정 |
|---|---|---|---|---|
| 1 | 별도 운영 서명자 기기 | 감시기와 분리된 **조직이 관리하는 Windows PC** 권장; 암호화 키 저장+BitLocker/접근 제한, 개인키 PC 외부 반출 금지 | 그런 기기 실제 보유·승인자 지정 및 6개 signer kit 파일을 **조직 내부에서 이동해도 되는지 정책 승인** | B_DEVICE=AVAILABLE_UNDESIGNATED; B_KEY=NOT_RUN |
| 2 | GitHub 읽기 전용 자격 | 기존 과권한 OAuth **사용 금지**; 별도 fine-grained PAT(정확히 이 PRIVATE 저장소 1개, Contents read, Metadata read, 다른 권한 없음, 만료 ≤90일) 사용자 직접 발급 **권장** | 발급자의 명시적 동의, GitHub UI에서 8항목 확인, 안전한 설치에 대한 별도 권한·관리자 절차 | TOKEN=BLOCKED_OVERPRIVILEGED; NEW_TOKEN=NOT_ISSUED |
| 3 | 로컬 독립 리뷰 및 v2 계약 | **로컬 소스 보존 + 독립 사람 또는 조직 승인 온프레미스 모델**. 로컬 v2 control plane/solt commitment/영수증 **설계·독립 보안 리뷰 진행 권장** | 실제 reviewer/모델 제공 가능 여부, 외부 API·Telemetry·원격 전송 차단 입증; 실제 프로토콜 변경/운영 적용 별도 명시 승인 | E=BLOCKED_LOCAL_REVIEWER; PROTOCOL_V2=PROTOTYPE_ONLY |
| 4 | GitHub LIVE 계정 | **전용 비관리자 서비스 계정** 권장. GitHub 전용 state와 최소 권한 ACL만 허용, 이전 Dropbox 아카이브 DB/main/WAL/SHM·secret 접근 거부. root 공개 검증만 읽기 | 계정 생성·Task/run-as 변경·운영 ACL 변경은 운영 변경으로 사용자 별도 승인, rollback 및 권한격리 실측 필요 | LIVE_ACCOUNT=PROPOSED_ONLY; C=PARTIAL |
| 5 | 기게시 다이제스트·크기·파일명 | **제한정보로 잠정 분류**, 추가 게시 중단; 기존 PRIVATE 문서·git history 노출 범위 비파괴 점검 후 조직 정책에 따라 처리 | 데이터 분류 소유자 승인. 승인 없이 Git history rewrite/force push/삭제 금지. 이미 게시된 값은 git 삭제로 완전 소거 안 됨 | PRIOR_IDENTIFIERS=RESTRICTED_PENDING_CLASSIFICATION |

**중요:** GPT 권고를 사용자의 실제 정책 승인, 운영키 생성 허가, PAT 발급 허가, 로컬 프로토콜 운영 승인, 서비스 계정/ACL 변경 실행 승인으로 해석하지 않는다. 사용자가 단순히 이 내용을 Claude Code에 전달해도 위 미승인 작업은 수행하지 않는다.

## 3. 자동 리뷰를 가장 빨리 복구할 경로
경로 A — **실제 로컬 독립 reviewer 확보가 최우선**:
1. 조직 승인 모델/사람을 개발 세션과 분리해 승인된 내부 환경에서 사용 가능한지 판정. Claude Code가 Windows PC에서 실행된다는 사실만으로 코드가 로컬에 머문다고 간주 금지.
2. 내부 전용 전체 ZIP은 내부 artifact vault에 보존·해시/CRC 검증. 실제 리뷰자 접근 통제/모델 네트워크 차단/서명 영수증 검증/1회성 nonce·상태·중복 차단 시험을 격리 환경에서 구현.
3. GitHub control plane은 **비민감·승인된 필드만** 허용. 서명자 실제 운영키는 별도 기기, 검증 공개 root는 승인된 최소 권한 보호폴더. v2 서명 계약에 artifact binding/receipt/report provenance/nonce/replay/expiry/cost/idempotency를 정식 명세화하고 독립 보안 리뷰. 결함 수정 후 관련 delta test만.
4. 신규 자격은 least privilege로 분리하고, LIVE 전용 계정·state dir·old DB deny를 host-real 시험. 실제 준비된 다른 호스트가 있으면 이 PC에 무리하게 새로운 runtime을 설치하지 말고 허용된 워크플로를 연계.
5. B+C+local-reviewer+v2 contract+credential + recovery/alert gates가 통과해야만 E 정식 독립 리뷰와 최종 LIVE 설치·전환 **각각 별도 사용자 명시 승인**. 그 전 자동 리뷰 provider `NONE`.

경로 B — 승인된 로컬 독립 리뷰어가 없다면 `E=BLOCKED_LOCAL_REVIEWER` 유지. 추가 서명 코드·ETW 반복보다 실제 reviewer 확보가 우선. 원본 코드 없이 외부에서 메타데이터만 평가한 결과는 전체 코드 독립 리뷰 PASS가 아니다.

## 4. Windows Claude Code 다음 한 번의 delta (미운영·미승인 실행)
- 동일 기존 시험 500+, 토큰 mock 34, installer 18, v2 synthetic 19를 목적 없이 재실행 금지. 정확한 현재 `CURRENT.md`·본 결과를 읽고 후속 개발에 필요한 **재현 가능한 delta만** 다룰 것.
- **허용**: 내부 리뷰 후보 탐색은 사용자/조직의 허용 범위에서 민감정보를 읽지 않는 런타임·호스트 메타데이터만, 서비스 계정 최소 권한 설계, v2 정식 계약 위협 모델/계약 문서·보안 시험안, 과거 식별자 비파괴 인벤토리·노출 범위 확인(추가 해시/파일명/경로 재게시 금지), GitHub 읽기 토큰 발급 UI 안내/안전 설치 체크리스트.
- **금지**: 운영키 발급/ROOT 설치, 사용자 PAT 발급·복사·테스트 계정 설치, 기존 계정/Task/DB/ACL 변경, 회사 코드/ZIP/로그/실 해시 외부 반출, READY/REQUEST·유료 reviewer·외부 LLM 호출, GitHub LIVE 활성화, history rewrite/데이터 삭제.
- 정책 확인 불가능하면 승인된 사실 대신 `USER_OR_ORG_CONFIRMATION_REQUIRED`로 남겨 다른 허용된 작업은 계속.
- 비민감 결과만 기존 `CURRENT.md`와 `TRACKER.json`에 보완; 새 Windows 결과가 필요하면 단일 결과 MD 작성·PRIVATE main direct publish 후 remote UTF-8 readback.

## 5. 다음 한 동작 — 확인할 최소 현실 제약
- 사용자에게 한 번에 확인할 **필수 사실 두 갈래**: (i) 별도 회사 관리 승인자 PC와 6개 키트 내부 이동 허용 여부, (ii) 조직 승인 온프레미스 모델·사람 리뷰어의 실제 존재·접근 가능 여부.
- 나머지 토큰 신규 발급, 운영 서비스 계정 변경, v2 운영 계약 승인, 기게시 식별자 처분은 각 범위의 명시 승인을 받아서 실행하되 **미승인 동안 개발 가능한 계획/격리 검증은 중단하지 않는다**.

결론: `GPT_DISPOSITION=ACCEPT_AS_DESIGN_CANDIDATE_WITH_BLOCKERS / B=DEVICE_UNDESIGNATED / C=PARTIAL / D=LOCAL_ONLY / TOKEN=BLOCKED / E=BLOCKED_LOCAL_REVIEWER / ACTIVE_PROVIDER=NONE / MIGRATION_NOT_CUTOVER`.
