# 비용 제한 제거 — 코드 수정·시험·호스트 적용 경계
기준: 2026-11-23 KST / wonhwipark/CoWork-Skill-Collab / main
Work: COWORK-AUTO-APPROVAL-20261115-001

**사용자 지시 “비용제한 삭제해줘 이거로인해 리뷰안되는거 무의미해” 및 “진행해줘”를 수용. COST_LIMIT_REMOVAL=USER_AUTHORIZED, COST_RECONSENT=NOT_REQUIRED.**
가격·건당/일/월 금액·고정 USD3 일치 여부가 신규 독립 리뷰의 접수·서명·READY·디스패치 자격을 결정하지 않는 방향으로 수정했다. 과거 “비용 무상한 위험 수용 별도 승인 대기”는 이 비용 제한 제거 지시와 관련해 해소하며 동일 동의를 다시 묻지 않는다. 청구·실제 사용량은 사후 기록으로 유지한다.
**소스 수정·직접 시험은 완료. Windows 운영 비용 게이트 적용은 BLOCKED_HOST_ACCESS/NOT_RUN. LIVE_READY=NO.** 새 후보 전체 설치·DB 이행·최종 LIVE 컷오버 승인으로 확대하지 않는다.

## 1. 변경 코드

| 경로 | 제거한 차단 | 유지 |
|---|---|---|
| collab/ops/review_request_gate.py | independent 가격 인수 자체 거부, legacy unified USD3 일치, legacy 정책 가격 비교, CLI 가격 파싱/필수 금액 | REQUEST/ZIP SHA·크기·CRC·안전 경로, 등록 policy identity, SOURCE_PIN 형식, 승인/READY를 생성하지 않는 경계 |
| 후보 config.py | max_budget_usd 필수 양수, tier별 금액 양수 파싱 거부 | 정책 이름·effort·enabled/dry_run·설정 구조 검증 |
| 후보 auto_approval.py / auto_policy.py | max_request_usd 파싱 거부, 가격 파싱 오류, 재검증의 저장 cents 파싱 의존, 승인 경로의 집계 회계 조회 의존, 오해를 주는 가격 제한 출력·기본값 | 보호 위임 enabled/기간/repo/project/skill, 실제 서명·원본 바인딩·nonce·중복/UNCERTAIN |
| 후보 state_store.py | INVALID_COST 예약 거부 | BEGIN IMMEDIATE·기존 identity/행·유일키, 과거 이력 유지. 잘못된 회계 값만 새 행에서0으로 정규화 |
| 후보 cli.py / tools/review_request_gate.py | 가격 상한으로 보이는 현황 출력·구 도구 금액 차단 | cost_gate=OFF, 선택적 회계 참조, 정책 ID와 정식 승인 분리 |

- 올바른 옛 금액 값은 회계 참고로 읽을 수 있으나 실행 상한으로 쓰지 않는다. 없거나 null/0/음수/문자열/비정상 수치여도 **금액 때문에** 거부하지 않는다. 인가·필수 설정 구조 오류는 별개로 계속 거부.
- 독립 리뷰는 단일 유형. legacy unified/skill/design 표기는 고정 이력·도구 호출 호환만 유지하며 가격 등급 선택으로 사용하지 않는다. 기존 REQUEST의 policy·금액·서명 bytes는 수정하지 않음.
- r2에서 이미 제거된 CLI --max-budget-usd 전달·집계 금액 비교는 되살리지 않음. 관련 기존 시험으로 무예산 argv와 사후 비용 기록을 확인.
- max_model_calls=1/단일 요청 디스패치 보호, 영수증 우선·게시 실패 시 모델 재호출 금지 유지. 계정 제공자의 사용량 응답·실행 timeout/중단 처리는 별개로 보존.
- 개발 후보 원본은 동결 r2 SHA23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206. 구 ZIP·요청·승인·READY·리뷰 결과·영수증·운영 DB는 변경하지 않음. 독립 리뷰 재실행/새 요청/실제 모델 호출0.

## 2. 실제 시험 — GPT Linux / 가짜 전송·시험 Ed25519 키

| 시험 | 결과 | 한계 |
|---|---|---|
| main 접수기 unittest | **55 PASS / 0 FAIL** | 정식 A/B를 시험용 로컬 Git 저장소에서 확인. GitHub 실행·실제 서명/READY 아님 |
| 금액 제거 집중 회귀 | **237 PASS / 0 FAIL / 1 SKIP** | 설정·위임 가격 누락/변조 수치, 실제 시험키 서명1/중복 추가0, disabled 위임 서명0, 회계 조회 불의존, 저장 cents 변조 재검증, 원본·policy 검사. SKIP=Win32 ACL |
| 전체 트리 1차 실행 | **1009 PASS / 28 FAIL / 34 SKIP** | Linux에서 Windows msvcrt/프로세스 잠금·cmd·SHADOW OS 전제 시험 등이 실패. 28 FAIL을 PASS/SKIP으로 바꾸어 보고하지 않음. Windows 재검증 필요 |
| 최종 휴대 가능한 회귀 | **1011 PASS / 0 FAIL / 34 SKIP / 28 DESELECTED** | 위 실패 node28만 명시 제외 후 실행. 최종 추가 시험2 포함. 전체 Windows 회귀 PASS와 같지 않음 |
| 패치 재적용·실물 bytes | **PASS** | 깨끗한 r2 사본에 git apply --check/apply, 변경12파일 모두 목표 SHA와 정확 일치 |
| Windows 설치·운영 비용 적용 | **NOT_RUN / BLOCKED_HOST_ACCESS** | 이 세션에 실제 Windows 명령/파일 연결 없음. 소스 게시를 호스트 적용으로 주장하지 않음 |
| 독립 리뷰·LIVE·운영 DB 변경 | **NOT_RUN** | 기존 r2 독립 리뷰는 완료 상태 보존; 이 변경으로 자동 추가 리뷰하지 않음 |

시험 통계 JSON의 junit tests에는 pytest subtests15가 별도 포함될 수 있음. 위 PASS/FAIL/SKIP는 콘솔 집계 기준. 전체 실패 목록은 [시험 근거](artifacts/cost_gate_tests_r0001.json)에 보존. 초기 집중 시험은 새 시험의 캐시 상태 반환값 가정과 구 금액 거부 기대를 바로잡은 후 최종237/0/1로 재검증했다. 테스트 기대 수정은 비용 제거로 의도적으로 바뀐 행동에만 한정하며 권한/원본 거부 시험은 유지함.

## 3. 전달 가능한 개발 패치

- [cost_gate_removal_r2_r0001.patch](artifacts/cost_gate_removal_r2_r0001.patch)
- **SHA-256: 28d6b6db55a130fbba7e55863426d62749ed0f1047756a9e884f30ced1431366**
- 크기39061 B, 변경12파일. [원본·목표 파일 SHA 매니페스트](artifacts/cost_gate_removal_r2_r0001.json).
- 적용 대상은 **격리 r2 소스 루트만**. `git -C <isolated_r2_root> apply --check <absolute_patch_path>` 후 원본/목표 SHA 대조. clean r2 사본 재적용 검증 완료. 실제 v0.2.29 설치 트리에 이 패치를 직접 적용하지 않음.
- 새 릴리스 ZIP은 만들거나 PUBLIC 배송하지 않았음. 이는 **development_not_for_deployment 패치**이며 F1(원본 의도 만료 재검증), F2(구 release manifest), F3(Commit A 자기 참조)는 이 비용 변경의 해결 범위가 아니므로 그대로 열린 상태. 동결 r2 리뷰가 이 패치/새 SHA를 검토한 것으로 승격하지 않음.
- GitHub main에는 접수기 소스·시험을 직접 갱신하고 위 후보 패치·근거·CURRENT/기존 지시서를 같이 게시한다. 기존 패키지/영수증의 bytes는 보존.

## 4. 다음 한 동작·운영 경계

기존 Windows 지시서의 F1/F2/F3 보완 한 묶음에 이 **시험된 비용 제거 패치**를 통합하고 실제 Windows 회귀·새 패키지까지 마무리한다. 비용 제거 의사나 금액별 허용을 다시 질문하지 않는다. 현재 막힌 이유는 **Windows 실행 접근 및 아직 열린 소스/호스트 검증**이며 비용 동의 부족이 아니다.

사용자가 비용 제한 제거를 지시했으므로 비용 정책 수용은 승인 대기 항목에서 제외. 보호 키/신뢰 루트·scope·DB 이력은 건드리지 않고, 새로운 후보의 설치·운영 DB 이행·최종 LIVE 컷오버는 기존 별도 최종 확인 경계를 유지한다. 기존 v0.2.29 운영 게이트가 실제로 사라졌다는 보고는 호스트 적용/재조회 증거가 생긴 뒤에만 한다. 이 문서 게시 자체는 Windows 실행 트리거가 아니다.
