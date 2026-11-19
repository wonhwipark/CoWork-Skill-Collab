# 업무 GPT 인계 — Recovery Workspace 연결의 구현 계약

r0001 / 2026-11-20 KST / 개발 후보 연결 설계용

## 목적과 전제

이미 전달한 l1-channel-recovery 분석 컨셉에, 같은 Work의 결과 저장과 Recovery별 탐색을 연결해 주세요. 현재 MCP는 설치본 확인 자료의 조회·제공을 지원하지 않는다는 사용자 확정 제약을 유지해요. 사용자에게 자료를 다시 요구하거나 MCP 확장 완료를 기다릴 필요 없이, 업무 GPT가 접근 가능한 실제 원문으로 최소 연결 설계를 진행해 주세요.

이 문서는 접근 가능한 관리 스킬에서 구현·합성 확인한 인터페이스를 전달해요. 업무 스킬·운영 호스트에 설치·활성화됐다는 의미가 아니에요. 아래 후보의 정식 전달/설치와 실제 권한은 기존 승인 범위에서 구분해 주세요. CoWork 서비스·경로·인증을 업무 스킬의 의존성으로 넣지 않아요.

## 구현된 후보

| 대상 | 후보 | SHA-256 |
|---|---|---|
| work-ledger-kernel | 0.7.46 | dabd412847354c77ca105da3ed686924f676f5f3c67428a2b984e68f2998076e |
| l1-fix-workflow | 1.6.75 | d13259cd0c9359dee2cddcb1c622fce5d98b663f9bc6eaea48c8a1c3b46b9ce4 |

두 후보는 development_not_for_deployment예요. 신규 23건 PASS, 관련 합계 100건 중 97 PASS·2 FAIL·1 ERROR이며 실패 3건은 수정 전 원본에서도 같았어요. 신규 독립 코드 리뷰·업무 호스트 통합 시험은 아직 수행하지 않았어요.

## 생산자가 연결할 인터페이스

기존 Work ID에 UTF-8 Markdown 또는 JSON object 결과를 연결해요. 제한은 5 MiB이며 본문을 새 schema에 강제 변환하지 않아요. 실제 생산자 버전·고정 source revision·보고서 요약을 선언해요. JSON에 provider/provider_version/code_rev를 담는 경우 선언과 일치해야 해요.

- 제공자: l1-channel-recovery.
- Evidence kind: recovery_analysis.
- stage: 기존 utility. 부가 보고서 보존이며 lifecycle의 기술 분석 완료 조건이 아니에요.
- Kernel preview: recovery_report_preview(work_id, source_path, provider_version, code_rev, summary).
- Kernel 등록: record_recovery_report(work_id, source_path, provider_version, code_rev, summary, expected_sha256, expected_revision).
- preview 반환의 source_sha256·evidence_revision을 다음 등록에 사용해요.
- 기존 Workflow attach-evidence에서도 같은 preview/apply 흐름을 제공해요.

```text
<기존 Workflow launcher> attach-evidence --work-id <기존 ID> --file <결과 MD/JSON> --kind recovery_analysis --provider l1-channel-recovery --provider-version <실제 선언 버전> --code-rev <고정 대상 revision> --summary <요약>
```

기존 허용된 로컬 writer가 preview를 확인한 뒤 같은 명령에 --apply --expected-sha256 <source_sha256> --expected-revision <evidence_revision> --actor <기존 identity> --session-id <기존 session>을 전달해요. 이 문서는 writer 환경 플래그를 새로 켜는 설치 지시가 아니에요. MCP read-only 모드에서는 이 로컬 첨부 경로를 거부해요.

현재 설치 Kernel에 해당 API가 없으면 RECOVERY_KERNEL_UNSUPPORTED로 답해요. 기존 스킬에서 동등 계약이 있으면 재사용/매핑하고, 후보가 필요하면 기존 개발·검증·설치 절차에서 적용 범위를 정해 주세요. 사용자가 설치본 자료를 다시 제공해야만 설계를 진행할 수 있다는 조건은 두지 않아요.

## 원본·재시도·조회

Work/본문 hash/생산자 버전/source revision이 같으면 기존 Evidence를 재사용해요. source revision이나 내용이 다르면 이전 원본과 별도 보존해요. 같은 identity에서 summary·원본이 다르거나 preview가 stale이면 충돌로 거부해요. 저장되는 confidence는 AUTO_CANDIDATE이며 기술 검증이나 제품 시험 PASS를 부여하지 않아요.

등록 결과의 evidence_id·source_sha256·created·saved를 대조해요. 원격 게시 실패 때문에 분석이나 등록을 다시 실행하지 않고, 기존 등록/원격 이력을 확인한 뒤 필요한 단계만 복구해요.

Kernel work_recovery_reports(work_id) 또는 recovery-list --work-id <ID>는 원본 경로·SHA 무결성과 저장 메타정보를 읽어요. 보고서 본문을 자동 전송하거나 분석기를 실행하지 않아요. 기존 docs export가 다음 파생 보기를 만들어요.

- Work RECOVERY.md와 state/recovery_reports.json.
- 루트 RECOVERY.md와 index/recovery.json.
- 등록 Evidence의 실제 artifact publish mapping을 이용한 원본 보고서 링크.

위 목록은 재생성 가능한 읽기 projection이에요. 새 Work 원장·RECOVERY profile을 도입하지 않아요. Viewer는 허용된 실제 문서/읽기 계약에 이 파생 정보를 연결해 주세요. 개인 Knowledge의 Recovery 목록·재사용 지식은 Updater가 원래 Work를 참조하도록 설계해요.

## 보존할 분석과 경계

수정 CL Seed와 현재 대상 revision, 원인 패턴, 후보의 미커버·보호됨·기각·보류·미분석, caller/callee/상위 보호 근거, 검출 신호·상태/자원 소유자·안전 복귀 조건, 선택 조치·실제 시험/NOT_RUN을 원본에 유지해요. REQ→CNF 미수신 timeout의 이미 구현된 recovery 커버 범위는 제외해요.

업무용 l1-workspace의 실제 저장소·브랜치·root는 업무 환경 기존 매핑에서 정확히 확인해요. 동명 GitHub.com 저장소를 대입하지 않아요. 분석 원본과 제한 자료는 허용된 업무 Work에 보존하며 원문 반출을 요구하지 않아요. Git 게시·Knowledge 승격·원격 조회·제품 코드 변경은 각각 기존 책임과 유효 승인 범위로 판단해요.

## 업무 GPT가 작성할 결과

실제 생산자 출력→위 저장 계약→기존 Work 선택→허용 writer→읽기 projection/Viewer·선택적 Updater 연결 매핑을 설계해 주세요. 기존 동등 기능은 재사용하고 실제 결손만 최소 보완해요. 설치된 원문/버전과 이 후보의 차이·변경 파일·실제 시험 및 미실행·운영 적용 여부는 업무 환경 Work에 남겨 주세요.

한 건의 수락 기준은 원본 ID/SHA 재조회, Recovery 보기→Work/보고서 연결, 기존 기술 탐색 유지, 동일 결과 재처리·부분 실패에서 중복 방지, 이전 revision/기각·보류 보존, 저장과 기술/제품 검증 상태 분리예요.

