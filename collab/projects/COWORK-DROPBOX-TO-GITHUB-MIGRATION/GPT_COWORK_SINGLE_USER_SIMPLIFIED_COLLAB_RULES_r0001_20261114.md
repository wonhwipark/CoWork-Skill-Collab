# CoWork 단일 사용자 협업·자동 리뷰 간소화 원칙
r0001 · 2026-11-14 KST
Repository: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
Exact path: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_COWORK_SINGLE_USER_SIMPLIFIED_COLLAB_RULES_r0001_20261114.md`
Status: **USER_DIRECTED_SIMPLIFICATION / DESIGN_BASELINE / NOT_OPERATIONAL_CUTOVER**
Current state: `ACTIVE_PROVIDER=NONE`; `MIGRATION_NOT_CUTOVER`.

## 1. 명확한 사용자 환경
- CoWork는 **사용자 1명이 운영**. Windows PC의 Claude Code와 Python watcher는 모바일에서 원격으로 조작됨. 모바일은 독립 승인자 장치가 아님.
- **Windows Claude Code·Watcher PC는 회사 업무 L1 소스코드에 접근 자체가 불가능**. 회사 L1 분석은 별도의 업무 PC/호스트에서 진행하며 본 CoWork 리뷰어와 혼동하지 않는다.
- 저장소 역할: `CoWork-Skill-Collab` PRIVATE = 협업·검토 이력; `L1Work` PUBLIC = 별도 승인된 최종 ZIP은 main **루트**, 업무 PC/Agent용 handoff prompt MD는 main **`handoffs/`**. PUB ZIP 게시·handoff 게시·업무 호스트 설치/실행은 서로 다른 완료 조건.
- 외부 코드 전송 가능 여부는 **CoWork 작업물과 회사 제한 원본을 분류해서 판단**. 과거 D=2(로컬 전용)는 당시 코드 분류 확인 전의 보수적 경계로 유지되어 온 것이므로 자동으로 해제하지 않는다. 회사 원본·고객 자료·비밀·권한 없는 파생 자료는 여전히 게시·전송 금지. **CoWork watcher 자체 소스/ZIP을 기존 Claude 리뷰 경로로 전송할 수 있는지는 사용자의 명시적 허용 범위를 확인한 뒤 판단**. Windows가 회사 코드에 접근 불가하다는 사실만으로 모든 Windows 파일의 반출 허용을 추정하지 않는다.

## 2. 과도한 기본 필수요건 제거 (SU-SIMPLE)
| 항목 | 단일 사용자 기본 설계 |
|---|---|
| 별도 서명자 PC | **기본 필수 아님**. 개인 운영 CoWork 리뷰를 위해 PC 추가 구입·키트 6파일 이동·독립 개인키 발급을 요구하지 않음. 유료/다중 사용자 신뢰 경계로 확장할 때는 별도 검토 가능 |
| 로컬 LLM·온프레미스 독립 리뷰어 | **기본 필수 아님**. 허용된 CoWork 코드에 대해서는 기존 Claude 독립 리뷰 절차 사용 가능하도록 복귀 검토. 개발 세션 자기시험과 독립 리뷰는 구분 |
| 광범위한 보안 입증 | ETW 4축 매트릭스·네트워크 무연결 검사·복잡한 로컬-only 프로토콜·매 단계 조직 정책 확인을 **일반 CoWork 리뷰의 필수 게이트로 삼지 않음**. 실제 결함에 연관된 최소 시험만 |
| 전용 서명·비밀 원장 | 단일 사용자 일반 모드에 새 Ed25519 루트, 2번째 서명자, 정교한 솔트 커밋먼트를 **당연한 선행조건으로 강제하지 않음**. 기존 watcher 잠금·영수증/상태 기록 재사용 |
| 별도 Windows 서비스 계정 | 기본 강제하지 않음. 기존 권한으로 허용된 요청만 실행하도록 단순 설계; 특정 자격/운영 데이터 위험이 입증될 때 최소 범위로 변경 |
| GitHub PAT | 과권한 자격 재사용을 권장하지 않으나, 단일 저장소 최소권한 read credential 1회 구성처럼 **실제 필요한 작업만** 남김. 기존 로그인 수단 사용 가능성을 READ/WRITE 요구사항과 함께 확인 |

**참고:** 제거되는 것은 중복·과잉 설계상의 '조건'이지, 현재 운영 모듈에 이미 구현된 검사 코드를 무심코 삭제하거나 검증을 우회하라는 뜻이 아님. 기존 정식 서명 계약/권한 정책을 설계 문서만으로 임의 무력화하지 않는다. 이전 LOCAL_ONLY v2/ETW 작업의 증거와 이력은 보존하되 원래 목적에 맞는 별도 선택 경로로 보관.

## 3. 기본 자동 리뷰 안정성 — 최소한의 운영 규칙만 유지
1. **정확한 유효 요청만 실행**: 저장소/작업 ID/REQUEST-READY 유효성, 사용자 승인 모드와 이미 합의된 리뷰 비용 한도를 검사. GitHub의 임의 ZIP/메모/커밋만으로 유료 리뷰 자동 호출 금지.
2. **중복 실행 방지**: 동일 논리 요청 1회, 재시작·결과 게시 실패 시 동일 모델 리뷰를 재호출하지 않음. 기존 watcher 잠금과 영속 영수증/이력 기능 우선 재사용. 검증된 중복 방지에 실제 결함이 있을 때만 delta 수정.
3. **자격 노출 방지**: GitHub 토큰/비밀키를 프롬프트·로그·ZIP·PUBLIC에 넣지 않음. 단일 저장소 최소 권한 권장. 테스트 중 모의 자격은 실제 토큰과 구분.
4. **기존 버전·업무 호스트 보호**: 운영 DB/예약 작업·Notifier/Bridge는 최종 운영 승인 없이 변경하지 않음. 최종 후보는 ZIP CRC/경로 이탈/파일 목록/실제 self-test 검증.
5. **실제 독립 리뷰는 별도 작업**: 동일 개발 세션의 자체 테스트/자기 검토를 독립 리뷰 PASS로 기록하지 않음. Claude Code 자동 리뷰 사용 가능 조건(코드 전송 허용/비용/요청 절차)을 만족하면 기존 Claude 리뷰 재개가 우선.
6. **단일 LIVE**: 이전 요청·영수증 보존, 중복 알림·리뷰 방지, 실패 시 복원. `ACTIVE_PROVIDER=NONE`은 실측 가동 이후에만 변경.

이 외 별도 PC, 로컬 LLM 런타임 설치, ETW·network-isolation probe, 새 서명/nonce/commitment 아키텍처는 일반 CoWork 자동 리뷰의 기본 요구가 아님.

## 4. 협업과 최종 배포 흐름 — 핑퐁 최소화
1. GPT: 요구/변경범위·목표 버전·필요 시험·실 리뷰 기준 **한 번에 정리**.
2. Windows Claude Code: 접근 가능한 CoWork 코드의 허용 개발·수정·관련 자체시험을 원샷으로 수행하고 결과/영수증을 PRIVATE main에 게시·readback. 개발과 독립 리뷰 세션은 별도 실행.
3. 유효한 비용·모드 승인 + 코드 전송 허용 시: 기존 Python watcher/Claude 독립 리뷰 경로를 우선 복구. 새 로컬 LLM 설치를 그 선행조건으로 잡지 않음.
4. GPT: 독립 리뷰 결과를 `수용/수정 수용/보류/거절` 판정. 수정·재시험·재리뷰는 필요한 변경만 묶어 진행하고 재리뷰는 새로운 명시 요청.
5. 최종 승인 시: 회사/고객 민감정보 미포함, 배포 게이트 PASS한 **최종 ZIP**을 `wonhwipark/L1Work/main` 루트로, **업무 PC용 Handoff 프롬프트 MD**는 같은 repo의 `handoffs/`로 게시. 양쪽 다 원격 bytes/commit readback. 업무 PC Skill-Updater 실설치/Job 실행은 실제 호스트 영수증으로만 PASS.
6. 결과: GPT가 통합 종료 보고(현재/변경/실 시험/미완료/ZIP & MD 위치/다음 한 동작). 새 질문은 실행을 정말 막는 현실 조건으로 제한.

## 5. 당장 할 일과 변경 승인 경계
- GPT는 기존 '별도 signer PC, 로컬 reviewer 미확보, C 4축'이 단독 사용자 자동 리뷰의 필수조건처럼 반복 요구된 부분을 **설계 차단 사유에서 재분류**하고, 실사용에 필요한 `REVIEW_TRANSPORT`/기존 watcher 재사용 가능성을 검토.
- Windows Claude Code 다음 1회 통합 인계는 **(a) 현재 watcher/Review 계약과 승인된 자동 호출 경로 실측, (b) CoWork 코드 분류 및 외부 Claude 전송 허용 확인, (c) 실제 유효 요청·중복·비용·토큰 최소 수정, (d) LIVE 전환에 필요한 운영 승인을 한꺼번에 보고**에 집중. 이미 구현/검증한 500+ 시험·키트·v2 local-only 장부·ETW 반복하지 않음.
- 실제 토큰 생성/교체·유료 모델 호출/READY 게시·코드/ZIP 반출·운영 상태/Task 변경·PUBLIC 배포·LIVE 전환은 해당 범위 명시 승인 이후에만 실행. *이 MD 작성 자체가 승인/실행 요청은 아님*.
- 기존 `GPT_SINGLE_USER_LOCAL_ONLY_LIVE_FASTTRACK_MASTER_r0001_20261114.md`의 **SU-L1 LOCAL_ONLY/서명대체/온프레미스 reviewer 필수/4축 ACL**은 과도한 가정으로 간주. 새로운 세션에서 현재 목적이 일반 CoWork 자동 리뷰라면 **이 문서의 SU-SIMPLE을 설계 우선순위로 적용**, 과거 계약 실행 권한은 그대로 보존. 상세 충돌은 GPT 판정에서 먼저 해소하고 Windows에 모순된 두 지시를 동시에 전달하지 않음.

## 6. 판정 상태
`ARCHITECTURE=SU-SIMPLE_DESIGN_SELECTED`
`REVIEW_TRANSPORT=REASSESS_LEGACY_CLAUDE_PATH`
`CODE_EXPORT=USER_SCOPE_CONFIRMATION_REQUIRED`
`INDEPENDENT_REVIEW=NOT_RUN`
`ACTIVE_PROVIDER=NONE`
`MIGRATION_NOT_CUTOVER`
