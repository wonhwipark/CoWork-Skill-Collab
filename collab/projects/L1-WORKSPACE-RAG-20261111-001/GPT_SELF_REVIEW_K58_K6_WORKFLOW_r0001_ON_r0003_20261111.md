# GPT 자체 델타 리뷰 — K5.8/K6 × Workflow r0003

- 작성: 2026-11-11 KST / REVIEW_KIND=GPT_SELF_REVIEW / DESIGN_DELTA_REVIEW
- 원본 판정: REVISE. BLOCKING 2 / MAJOR 11 / MINOR 1.
- SOURCE_ACCESS=VERIFIED. 실제 사내 원문/설치본은 AS_IS_NOT_VERIFIED.
- 원본 source snapshot: PRIVATE wonhwipark/CoWork-Skill-Collab main `7212df7b4adabb4f0fca5e7f316128cc7519ffda`. CURRENT.md와 r0003을 마지막 재조회했을 때 동일함을 확인.
- r0003 blob: `789f06c3bb199565a049daf30bdbf1330fa17c2c`.
- 범위: 그룹 지식 범위 변경과 K5.8/K6/Workflow 계약의 diff 중심 설계 검토. 기존 전체 RAG 리뷰 재실행 아님.
- 최초 결과는 현재 대화에 보고했으며 당시 원격 쓰기 없음. 이후 사용자 지시에 따라 본 결과와 보완 계약·인계서를 게시한다.

## 1. 직접 읽은 원문과 증거 경계

저장소 PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`; 프로젝트 디렉터리 `collab/projects/L1-WORKSPACE-RAG-20261111-001/`.

| 별칭 | 문서 | 조회 결과 |
|---|---|---|
| CURRENT | CURRENT.md | 최신 r0003 절까지 원격 확인 |
| K | L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0003_20261111.md | 전체 원문 확인 |
| A | L1_E2E_INHOUSE_OFFSITE_ARCHITECTURE_r0002_20261111.md | 역할·정본·게이트 비교 |
| H | L1_INHOUSE_GPT_OPENCODE_HANDOFF_r0002_20261111.md | S01~S09 및 호출 계약 비교 |
| G | L1_REVIEW_ACCUMULATION_G0_PARTIAL_AUDIT_r0001_20261111.md | 기존 공개 Kernel 정적·격리시험 보고 확인 |
| R | GPT_SELF_REVIEW_STRUCTURAL_r0001_ON_RAG_r0002_20261111.md | 기존 지적의 신규 영향만 평가 |
| START | collab/START_HERE.md (저장소 상대 경로) | 운영 경계 확인 |

E0=사용자 전달 전제/미확인, E1=원격 문서·계약·시험 보고, E2=실제 소스/격리시험, E3=사내 설치본/실환경 해당 항목 실측. 이번 리뷰의 신규 직접 근거는 E1이며 기존 E2 결과는 보고서를 읽은 것일 뿐 재실행하지 않았다. 설치 확인과 실제 API/통합 E3 성공도 구분한다.

## 2. 종합 판정

그룹 HLD·상세 설계·AS-IS MSC·기술 이슈 히스토리 정본과 개인 Work/Evidence 정본 분리는 수용한다. Workflow/Updater/Kernel 책임 분리도 타당하다. 구현 기준으로는 승인에 묶이는 source/근거/권한, 영속 publication 복구, 독립 검증 상태축, N:M·변경 단위와 검색 자격 계약이 부족하므로 REVISE이다. G0 읽기 전용 조사는 가능하며 기존 tier/K6 호환성은 AS_IS_NOT_VERIFIED이다.

| 영역 | 수용할 변경 | 필요한 보완 |
|---|---|---|
| K5.8 | 상세도 routing 폐기·기존 tier 보존 | 독립 상태·구 reader/writer·이행/롤백 |
| K6 | 검증 AS-IS 그룹 후보 | 주장별 근거·런타임 구분·별도 설계 승격 |
| Issue history | 수정 전 검증 원인 후보 | 증명 조건·variant·반증/정정 |
| Workflow/Kernel | 동일 Work·허용 Evidence 재사용 | 원자적 선택·N:M·영속 멱등성 |
| RAG/보안 | 게시와 M1 독립 | scope/주장 종류/권한·현재성 필터 |

## 3. 고유 지적과 판정

실패 시나리오는 문서 기반 설계 반례이며 실제 사내 장애 관측이 아니다. BLOCKING은 해당 게시 기능 구현/운영을 차단하며 G0 조사를 차단하지 않는다.

| ID | Severity | 원문 근거 | 실패 시나리오 | 제안 수정 | GPT 판정 | 수용 기준 | 증거 수준 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KR-01 | MAJOR | K §2.1 “필요한 경우 … 별도 필드”의 선택적 상태 분리 | 시험 상태 갱신이 원인·설계 승인 상태를 대체하거나 STALE이 과거 검증 사실까지 소실 | 독립 상태축과 증거 기반 판정을 필수화; 게시와 링크 상태 분리 | 수정 수용 | 원인 검증·수정 미반영·시험 미실행 동시 표현 | E1 |
| KR-02 | MAJOR | K §2.2 CAUSE_VERIFIED/FIX_PENDING 및 §4 root_cause | 정적 추론·CL 관련성만으로 원인과 회피책 유효성까지 확정 | 주장·검증 방법·조건·반례·검증자 명시; 회피책 별도 검증 | 수정 수용 | 수정 전 원인 게시의 근거·한계 명확화 | E1 |
| KR-03 | MAJOR | K §2.2 원인 게시 후보 허용; H §7 S01 그룹 확정 게시 0 | 진행 중이지만 원인이 검증된 이슈의 처리에서 문서별 해석 충돌 | r0003/r0004가 대체하는 S01 해석을 명시 | 수정 수용 | 미검증 메모와 검증된 원인 구분, 동일 입력 동일 판정 | E1 |
| KR-04 | MAJOR | K §2.1~2.2 기존 tier 유지·점진 도입 | 구 reader가 상태를 무시하거나 구 writer가 새 메타데이터 제거 | 실제 tier 매핑·reader/writer 호환·단계 이행·롤백 명세 | 추가 정보 필요 | 사내 원문 확인과 구버전 왕복·롤백 검증 | E1 / 현행 E0 |
| KR-05 | BLOCKING | K §5.2 단계 6~7 후보/target revision/preview digest 승인 | 대상 지식 revision은 같지만 승인 후 source·Evidence·권한이 변경되어 게시 | 승인을 전체 후보 manifest·소스·근거·목적지·정책에 바인딩; writer 재검증 | 수정 수용 | 승인 조건 변경·만료·철회·현재 scope drift 시 쓰기 0 | E1 |
| KR-06 | BLOCKING | K §5.3 publication dedupe; §5.2 uncertain 중복 게시 금지 | 원격 commit 직후 종료·응답 유실·로컬 영수증 유실로 중복 게시 또는 영구 미정산 | 영속 operation ID·게시 의도·원격 식별자·정산 규칙 | 수정 수용 | 동일 게시 복구, 확정 불가 HOLD, 중복 게시 0 | E1 |
| KR-07 | MAJOR | K §5.2 단계 0 및 §5.3 request_id dedupe | 두 진입점이 서로 다른 request ID로 동시에 Work·분석 생성 | 공통 요청 상관키·원자적 Work 선택·분석 재사용 키 | 수정 수용 | 동시 진입·재시도·재시작에서 Work/동일 분석 중복 0 | E1 |
| KR-08 | MAJOR | K §4 origin Work ID(s); §5.1 단일 work_id/source_snapshot_ref | 여러 Work·before/after source 계보 축약, Evidence ID namespace 충돌 | namespace Work/Evidence Ref, 복수 origin, 역할별 SourceSnapshot | 수정 수용 | N:M 및 변경 전후 근거 무손실 추적 | E1 |
| KR-09 | MAJOR | K §4 관련 지식 ID; §5.1 content_delta_digest | Issue history만 개정되고 HLD/MSC는 이전 내용을 현재 사실로 유지 | section/scenario write set·영향 관계·variant·일관 게시 | 수정 수용 | 원자 반영 또는 명시적 부분 상태, 불완전 조합 현재화 0 | E1 |
| KR-10 | MAJOR | K §3.1 Git SHA/dirty/scope; P4 file#rev/haveRev | 동일 SHA의 다른 build/의존성 또는 P4 로컬 변경을 같은 입력으로 오인 | 실제 분석 바이트·설정·의존성을 묶은 typed SourceSnapshot | 수정 수용 | SCM revision과 실제 입력·적용 scope 일치 확인 | E1; 기존 E2 보고 참조 |
| KR-11 | MAJOR | K §3.1 중요한 메시지; §3.2 공통 MSC 게이트 | 추론 메시지를 포함한 전체 MSC 검증 배지 또는 TO-BE kind만 변경해 AS-IS 승격 | 주장별 근거·방법·coverage, AS-IS/설계 게이트 분리 | 수정 수용 | 필수 근거 누락·타이밍 추론 은폐 0, 자동 승격 0 | E1 |
| KR-12 | MINOR | K §3.1 participant alias와 ID 분리 | 경로 변경/동명 alias/변환에서 ID와 근거 소실 | 논리 stable ID·alias map 버전·명시적 병합·왕복 계약 | 수정 수용 | 가독 표시 규칙과 ID·상태·근거 보존 | E1 / converter 현행 E0 |
| KR-13 | MAJOR | K §3.1 HISTORICAL/SUPERSEDED 및 §4 변경 상태 | 원인 반증·수정 revert 후 게시/연관 지식/캐시에 현재 유효 상태 잔존 | 정정·철회·revert 계보, 의존 재평가, 현재 포인터/캐시 무효화 | 수정 수용 | 원장 보존과 잘못된 현재 주장 회수 병행 | E1 |
| KR-14 | MAJOR | K §5.2 단계 9 scope/게시 revision/payload | 게시된 TO-BE·미해결 원인·과거 브랜치 지식이 현재 코드 설명에 혼합 | 권한→scope→주장 종류/상태→현재성 순 검색 자격 판정 | 수정 수용 | GROUP_PUBLISHED만으로 현재 AS-IS 자격 부여 0 | E1 |

우선순위: KR-05/06 → KR-01/03/07/08/10/11/14 → 나머지. 현행 원문이 필요한 KR-04 매핑은 추정 확정하지 않는다. 기존 RAG source-root/Job/owner/반출/M1 블로커는 별도로 OPEN이며 신규 지적 수에 다시 합산하지 않는다.

## 4. 최소 수정 계약 및 G0/시험 계획

본 대화에서 제안한 필수 의미를 [L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0004_20261111.md](L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_CONTRACT_r0004_20261111.md) r0004에 반영한다. 상태축·원인 조건·typed SourceSnapshot·메시지별 MSC 근거·participant/변환 계약·Work/Evidence namespace·N:M/write set·승인 바인딩·영속 operation 복구·Work별 링크·정정/회수·RAG 검색 자격·legacy 이행을 포함한다. 실제 스킬/Kernel schema 변경은 수행하지 않는다.

사내 전달은 PUBLIC `wonhwipark/L1Work`, branch `main`, `handoffs/L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md`를 사용한다. 이 파일은 민감 근거와 사외 협업 경로·인증 의존성을 제외한 독립형 G0 인계다. PUBLIC 게시 승인은 본 대화의 사용자 지시로 해당 설계 문서에 한정하며 스킬 ZIP 또는 운영 배포로 확대하지 않는다.

## 5. G0 읽기 전용 확인표

아래 항목은 조사 전 모두 AS_IS_NOT_VERIFIED이다. 실제 설치본과 원문을 근거로 항목별 CONFIRMED/GAP/AS_IS_NOT_VERIFIED/BLOCKED를 판정한다. 설치본을 읽은 사실과 API/통합 실행 성공을 구분한다.

| ID | 실제 확인할 내용 | 해소 대상 |
| --- | --- | --- |
| G01 | 실제 설치 버전·release 상태·entrypoint 및 읽기 명령의 쓰기 부작용 | 설치본 기준·조사 범위 |
| G02 | K5.8 전체 tier 원문·우선순위·예외·routing·reader/viewer | KR-01·04 |
| G03 | K6 AS-IS/TO-BE/승인 설계/런타임 확인 규칙과 예외 | KR-11 |
| G04 | 두 진입점의 Work 탐색·재개·동시 생성 차단·상관키 | KR-07 |
| G05 | 설치 Kernel registry·schema/validator parity·exporter 소유권 | KR-08 및 임의 필드 금지 |
| G06 | analyzer 출력 snapshot/anchor·영구 ArtifactRef·Run 보존 정책 | KR-08·10·11 |
| G07 | TO-BE 작성/승인 책임자, converter의 ID·상태·근거 왕복 | KR-11·12 |
| G08 | Git/P4 실제 입력 바이트·build 조건·의존성 고정 방식 | KR-10 |
| G09 | 그룹 stable ID·variant·section·N:M·영향 관계의 현행 저장 계약 | KR-09·13 |
| G10 | 기존 writer CAS·CREATE 충돌·operation 조회·원격 readback 보장 | KR-05·06 |
| G11 | 승인 철회·만료·권한 변경을 writer 경계에서 검증하는 방식 | KR-05 |
| G12 | 구 reader/writer·tier 매핑·메타데이터 보존·점진 이행·롤백 | KR-04 |
| G13 | 정정·철회·revert의 현재 포인터·연관 지식·캐시 처리 | KR-13·14 |
| G14 | 실제 RAG source/owner/root/Job·body/driver/payload 검증 경로 | 기존 M1 차단 유지 |

K5.8/K6 전체 원문·설치 경로·상세 I/O 증거는 사내에만 보관한다. ‘재분류’는 재분류 설계표 작성이며 파일/데이터 이동이 아니다. 자연어 진입점을 호출하면 Work 생성·DB 갱신이 일어날 수 있으므로 G0는 원문·소스·기존 계약의 읽기 전용 확인을 우선한다. 읽기 부작용을 보장할 수 없는 명령은 실행하지 않고 한계를 남긴다. 운영 DB의 WAL/SHM을 포함해 쓰기 영향이 없어야 한다. Work 생성·Evidence 등록·그룹 writer·Job/Provider 호출은 G0에서 실행하지 않는다.

## 6. 부정·회귀시험 계획 T01~T24

다음은 시험 계획이다. 이번 문서 작성·게시 과정에서 상태 전이/스킬/실 API/호스트 시험은 수행하지 않았다. 모든 항목의 현재 상태는 NOT_RUN이다. 기존 문서의 시험 PASS를 이 표로 승계하지 않는다. G0 뒤 명세 확정 → 승인된 격리 구현·시험 → 별도 운영 판정 순서다.

| ID | 시험 | 수용 기준 | 현재 상태 |
| --- | --- | --- | --- |
| T01 | 상세 HLD/MSC와 기존 tier | 상세도만으로 개인-only 강제 0, 기존 tier 보존 | NOT_RUN |
| T02 | 원인만 검증되고 수정 미완료 | 원인/수정/시험/회피책 독립, 미확인·반례 명시 | NOT_RUN |
| T03 | 설계 승인·코드 미반영 | 승인과 구현·시험 별도, AS-IS 승격 0 | NOT_RUN |
| T04 | 새 코드 수정 없는 정적 AS-IS MSC | 고정 근거로 후보 가능, 런타임 추론 메시지 별도 | NOT_RUN |
| T05 | 미구현 TO-BE 및 승인 설계 | 설계 게시와 현행 AS-IS 구분, 자동 승격 0 | NOT_RUN |
| T06 | Branch A/B 상이·동일 SHA 및 build 조건 | 다른 적용 scope 거부, 검증된 동등 scope 재사용 허용 | NOT_RUN |
| T07 | 동시 두 진입점·서로 다른 호출 ID·재시작 | Work/후보/동일 분석 중복 0 | NOT_RUN |
| T08 | CAS 변경·승인 철회/만료·source/Evidence 변경 | 쓰기 0, 조건 재검증·재승인 | NOT_RUN |
| T09 | 게시 성공 후 복수 Work 일부 링크 실패 | 영수증 보존, 링크별 복구, 재게시 0 | NOT_RUN |
| T10 | 구 tier·구 viewer/exporter 왕복 | 원장·tier·새 메타데이터 무손실 또는 안전한 격리 | NOT_RUN |
| T11 | 미등록 slot·schema/runtime 차이·producer 위장 | 등록 계약 준수, 허용 필드 가장/임의 삽입 0 | NOT_RUN |
| T12 | 링크만 전달·다른 본문·payload 변조·권한 변경 | 검색과 M1 분리, 미검증 M1 PASS 0 | NOT_RUN |
| T13 | N:M·variant·section 동시 개정 | 출처 보존, CAS, 관련 문서의 일관된 게시 | NOT_RUN |
| T14 | 승인 후 drift·P4 로컬 변경·anchor 유실 | 현재 VERIFIED 게시 차단, 상태 표시 유지 | NOT_RUN |
| T15 | 게시 원인의 후속 반증 | 정정 계보·현재 주장 회수·의존 재평가 | NOT_RUN |
| T16 | Branch A만 수정·다른 snapshot 시험 | Branch B 수정 완료 및 해당 수정 시험 PASS 오인 0 | NOT_RUN |
| T17 | 원격 commit 후 응답·로컬 영수증 유실 | 동일 operation 게시 복구, 불명확 HOLD, 중복 0 | NOT_RUN |
| T18 | 동일 멱등키·다른 후보/본문/대상 | 요청 거부, 이전 영수증 오재사용 0 | NOT_RUN |
| T19 | 철회·권한 변경 후 검색 캐시 | 최종 Provider 입력에서 자격·접근 차단 | NOT_RUN |
| T20 | participant 충돌·rename·converter 왕복 | stable ID·표시·상태·근거 보존 | NOT_RUN |
| T21 | Run 정리로 artifact/anchor 유실 | 근거 보존 또는 검증 불가 명시, 무근거 재승격 0 | NOT_RUN |
| T22 | HLD/detail/MSC write set 일부 게시 | 원자 적용 또는 명시적 부분 상태, 불완전 현재화 0 | NOT_RUN |
| T23 | 그룹 reader에 개인 Evidence 권한 없음 | 승인된 설명만 제공, 개인 본문·경로 누출 0 | NOT_RUN |
| T24 | legacy mapping 후 구 writer 실행·롤백 | Work 원장·tier·출처·게시 계보 무손실 | NOT_RUN |

각 시험 기록은 종류(정적/합성/격리 통합/실호스트), 명령·입력 revision·환경·수정 파일·실제 PASS/FAIL/SKIP/NOT_RUN·Evidence를 구분한다. 위 시험을 G0 요청에 포함했다고 실제 실행 승인이 된 것은 아니다.

## 7. 실제 수행·미수행과 인계 준비도

| 실제 수행 | 결과 | 한계 |
|---|---|---|
| 지정 원격 MD 조회 | PASS | 문서 접근 확인 |
| main 고정 커밋·CURRENT/r0003 원문 대조·마지막 재조회 | PASS | 검토 중 변경 없음 |
| 상태축/registry 경계/복구 상태/T01~T14 문구 존재 점검 | 확인 | 동작 시험 아님 |
| 신규 스키마/상태전이/스킬 통합/실 API | NOT_RUN | 설계 검토 범위 |
| 사내 설치본/운영 호스트 | NOT_RUN | 접근·실행 없음 |

기존 G0 보고서의 6 PASS와 기존 RAG 리뷰의 11 PASS/1 FAIL은 이전 결과이며 이번 회차 시험 또는 사내 설치본 PASS로 합산하지 않는다. 문서 게시 무결성 검사는 별도 원격 publication receipt로 기록하며 스킬 시험과 구별한다.

| 대상 | 준비도 |
|---|---|
| r0003 원문을 그대로 구현 명세로 사용 | REQUIRES_REVISION |
| 보완된 r0004 독립 인계로 읽기 전용 매핑 | READY_FOR_INHOUSE_G0 |
| 실제 구현·그룹 write·M1 해제 | BLOCKED_AT_G0_AND_RELEVANT_VALIDATION |

G0_K58_K6_SOURCE=NOT_VERIFIED / INHOUSE_E3=NOT_RUN / RAG_M1=BLOCKED / INDEPENDENT_REVIEW=NOT_RUN / GROUP_WRITE=NOT_RUN / SKILL_RELEASE=NOT_RUN / LIVE=MIGRATION_NOT_CUTOVER/DROPBOX_LIVE.

다음 한 동작: 새 handoff를 사내 GPT에 전달해 기존 K5.8/K6·설치 I/O·writer 보장만 읽기 전용 확인한다. 모든 내부 근거는 사내 보관하며 외부 회신을 자동 요구하지 않는다.
