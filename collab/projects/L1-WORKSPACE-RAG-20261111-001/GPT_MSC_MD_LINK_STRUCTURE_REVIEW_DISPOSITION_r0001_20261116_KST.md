# GPT 판정 — MSC·Procedure/Feature MD 링크 구조 (r0001 / 2026-11-16 KST)

- **Work:** `L1-WORKSPACE-RAG-20261111-001`
- **정적 리뷰 원문:** [Windows Claude Code 대화형 검토](CLAUDE_MSC_MD_LINK_STRUCTURE_INTERACTIVE_REVIEW_FOR_GPT_20261115.md)
- **고정 요청:** `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001` rev 1 / package `structure-r0001`, ZIP 38,132 B, SHA-256 `90bb61a0e7c3b429942c620480ad9a079980d2a3432b72cea8ba80a4b915907d`, SOURCE_PIN `013b9f26fde91c3bcc87374952f64a61111c5a69`.
- **판정:** `GPT_DESIGN_DISPOSITION=ACCEPT_WITH_CHANGE`. 기존 두 진입·같은 Work 보존·converter 표현·대상 writer 게시 책임은 유지. 설계 보완을 반영하되 구현·실사용 검증 PASS 아님.
- **근거 등급:** Claude가 고정 발췌를 직접 대조한 사실과 아직 확인되지 않은 설치/호스트 동작을 구분. GPT가 실제 개발 호스트 코드를 직접 실행하거나 독립 코드 리뷰를 재수행한 것은 아님.
- **리뷰 경계:** 이 결과는 Windows Claude Code의 **대화형 정적 구조 검토**. 정식 `POLICY-STATIC-V1` 감시기 독립 리뷰의 `REVIEW_RESULT_1.md`/receipt/READY와 별개. 이 요청의 정식 `INDEPENDENT_REVIEW=NOT_RUN`, `PAID_MODEL_CALL=0` (확인 가능한 문서 기준). 기존 요청의 입력·승인·상태를 소급 변경하지 않음.

## 1. 지적별 GPT 판정

| ID | 등급 | 판정 | 최소 반영·근거 경계 |
|---|---|---|---|
| I-01 / R02,R10 | MAJOR | **수정 수용** | 검증된 시나리오 IR / code-analyzer semantic spec / 기존 PUML→msc-export의 **입력 클래스·지원 경로·출력 열** 구분. semantic spec의 IR 변환 지원은 미확인; Procedure/Feature 기본은 **기존 검증된 MSC 산출물 재사용 우선**. Phase·source revision은 실제 제공된 메타만. |
| I-02 / R04,R07 | MAJOR | **수정 수용** | 고정 Kernel 발췌상 `.svg/.puml` 소형 Evidence 복사 제외, 이름 변경에 따른 **상대 링크 불일치**는 정적 결함. 다른 writer가 모두 같은 결함인지 단정 금지. 게시 경로 map 기반 **파생 MD 링크**와 기대/실제 게시 목록·해시 readback 대조. `.html`은 단일 SVG 내장 뷰어 우선, 필요 시 **미리보기 `.svg`만** Kernel 허용 범위 검토. 상한 초과 무음 누락을 완료 실패로 표기. |
| I-03 / R09 | MAJOR | **수정 수용** | HTML 렌더링 URL·권한을 확인한 경우에만 “MSC 확대 보기”. 미확인/차단 시 SVG 직접 링크 및 HTML **다운로드** 안내, SVG도 없으면 PUML/원본+“그림 미완료”, 둘 다 없으면 MSC 절 미생성. 파일 URL과 렌더 URL을 혼동하지 않음. |
| I-04 / R03,R06 | MAJOR(조건부) | **수정 수용** | 고정 converter 발췌의 한글 이름 정제·중복 무검증 위험. 고유 ASCII 시나리오 ID 우선, 최종 산출 파일명 충돌 검사·fail-closed 또는 결정적 고유명 매핑. 입력이 항상 고유 ID인지 설치/호출 계약 확인 전 일반화 금지. |
| I-05 / R06 | MAJOR | **수정 수용** | MSC 절 갱신 **소유자 하나**: Workspace는 해당 진입 스킬이 연결한 기존 writer, 그룹은 그룹 writer. writer의 정해진 마커·revision/Preview/diff를 검증하고 수동 본문 보호. 마커 계약 미확인이면 자동 덮어쓰기 금지. code-analyzer 재생성 후 마커 보존은 설치 I/O 확인. |
| I-06 / R03 | MINOR | **수정 수용** | B 뷰어는 범용 MD→HTML 변환 자체가 아니라 **SVG 내장 HTML 템플릿/생성기**. 단계 좌표는 SVG 렌더 결과에서 일치 라벨을 추적, 0개/복수면 단계 이동 비활성화. Procedure/Feature의 AS-IS 문맥과 이슈 전용 문구·존재하지 않는 `MSC_DELTA.md` 링크 분리. CSP 확인. |

`R01=수용`, `R02=수정 수용`, `R03=수정 수용`, `R04=수정 수용`, `R05=수용`, `R06=수정 수용 + 설치 확인`, `R07=수정 수용`, `R08=수용(샘플 PASS 비일반화)`, `R09=수정 수용`, `R10=수정 수용`.

### Claude 제안의 조건부 보정

- “두 진입 × 두 목적지에서 링크 3개가 모두 열림”은 **정상 렌더 가능 경로**에 한정. URL 없음/차단/미렌더 폴백에서는 **존재하지 않는 3종 링크를 만들지 않는 것**이 합격 기준. `naturalWidth > 0`은 브라우저 SVG 미리보기 단계의 조건이며, Git/로컬 다운로드 경로의 보편 조건이 아님.
- “같은 입력이면 SVG 해시 동일”은 동일 renderer·설정·환경·출력 정상화 기준이 검증된 경우의 목표. 환경이 다르면 동일 manifest provenance와 의미적 일치를 우선 검증하며 SHA 동일을 근거 없이 강제하지 않음.
- 그룹 게시를 포함한 네 조합의 선행 단계인 **개인 Workspace 저장**은 두 진입 각각에서 유지; 그룹 미반영을 개인 Work 실패로 전염하지 않음.

## 2. 보완 설계 정본과 실행 게이트

- 변경분 정본: [MSC MD 링크 지원 제안 r0002](MSC_MD_LINK_SKILL_SUPPORT_REVIEW_AND_PROPOSAL_r0002_20261116_KST.md); 고정 입력인 r0001·ZIP·REQUEST/SOURCE_PIN은 **변경하지 않음**.
- 스킬/소유자: `code-analyzer` 사실·revision → `doc-converter` 기존 MSC 정규화·표현·HTML → `l1-fix-workflow` 또는 `l1-knowledge-updater` 가 해당 Work 결과 저장 연결 → Kernel/허용 Workspace writer → 유효 승인 시 Updater/그룹 writer. 절/링크는 최종 **대상 writer**가 소유.
- 먼저 **읽기 전용 설치 I/O 계약 대조**: Updater/그룹 writer, Kernel export·registry, converter 입력/파일명/HTML, 게시 경로/size limit, 실제 열람/CSP. G0 가정과 사용 경로를 분리. 이후 필요성이 입증된 최소 패치·합성 회귀·업무 호스트 검증을 순차 수행.
- 이번 판정으로 유료 모델 리뷰/서명/READY, 실제 코드 수정·패키지·설치·운영, 업무 Workspace/그룹 지식 게시, PUBLIC 배포를 **시작하지 않음**.
- **소스 경계 정정(2026-11-16 KST):** `code-analyzer`, `doc-converter`, `l1-fix-workflow`, `work-ledger-kernel` 4종은 [PUBLIC L1Work/main](https://github.com/wonhwipark/L1Work)의 기존 고정 ZIP 경로에서 GPT가 직접 확인 가능(루트 파일 존재·size·Git blob 메타 확인). **`l1-knowledge-updater`만 별도 실제 스킬 원문 확인**. 그룹 `l1sw-dev-knowledge` writer·업무 호스트 설치 차이·접근권은 여전히 별도 확인. PUBLIC 소스 검토와 업무 설치 E2E를 혼동하지 않음.
- **NEXT_ONE_ACTION:** 위 4종 공개 정적 분석은 GPT의 기존 확인을 재사용하고, 업무 GPT/허용 로컬 Agent는 **Updater 실제 I/O, 그룹 writer, 업무 설치본과 공개본 차이·호스팅 접근**만 읽기 전용으로 대조해 같은 Work에 회신. 다른 Work/재분석/새 호스팅 추가 없음.

## 3. 검증 상태

| 대상 | 상태 |
|---|---|
| 대화형 정적 리뷰 원문 회수·GPT 항목별 판정 | PASS (정적 문서 범위) |
| 설계 수정 방향 정리 | PASS (제안 r0002) |
| 정식 감시기 독립 리뷰/영수증 | NOT_RUN / NOT_RECEIVED |
| 변경 스킬 구현·회귀·패키징 | NOT_RUN |
| 업무 호스트 Updater·그룹 writer·viewer 지원 | NOT_VERIFIED |
| Work→그룹 게시·HTML 브라우저 E2E | NOT_RUN |
| 비용·운영 변경 | 새 모델 호출 0 (문서 근거), 운영 변경 없음 |

소스·리뷰 및 위 판정은 **설계 증거**이며, 실제 기능 가용성·지식 반영·RAG 재사용 성공 판정으로 승격하지 않는다.
