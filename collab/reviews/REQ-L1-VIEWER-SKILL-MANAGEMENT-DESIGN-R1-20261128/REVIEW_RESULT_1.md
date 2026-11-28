---
schema: SKILL_COLLAB_REVIEW_RESULT_V1
review_id: "REQ-L1-VIEWER-SKILL-MANAGEMENT-DESIGN-R1-20261128|1|0d755b787468af4567484805256ff6a3cb3625d80924fa4cc6bdabdfdcc0b509|1"
responds_to_request_id: "REQ-L1-VIEWER-SKILL-MANAGEMENT-DESIGN-R1-20261128"
responds_to_request_revision: "1"
package_sha256: "0d755b787468af4567484805256ff6a3cb3625d80924fa4cc6bdabdfdcc0b509"
skill_id: "l1-knowledge-updater"
run_policy_ref: "POLICY-STATIC-V1"
knowledge_refs: []
consumer_profiles: ["l1-workspace-viewer", "skill-updater", "job-list", "work-ledger-kernel"]
reviewer_os: WINDOWS
review_scope: CODE_REVIEW
test_policy: "STATIC_ONLY"
execution_status: COMPLETED
limitations: ["static review by an automatically started Claude Code process; no package code was executed", "knowledge files were delivered as the REQUEST pinned them; which parts were actually read is reported by the reviewer in the text", "reviewer host is Windows; Linux, in-house LLM and MCP behaviour are not verified by this review"]
---

# 리뷰 결과

# 독립 설계 리뷰 R1 — Viewer 운영 관리 / Skill Management

- request_id: `REQ-L1-VIEWER-SKILL-MANAGEMENT-DESIGN-R1-20261128` (rev 1)
- package_sha256: `0d755b787468af4567484805256ff6a3cb3625d80924fa4cc6bdabdfdcc0b509` (REQUEST 기재값이며 직접 해시하지 않음)
- 방식: Windows에서 정적 읽기만 수행. 실행·설치·시험 없음
- 아래 "설계서"는 `L1_VIEWER_OPERATIONS_SKILL_MANAGEMENT_DETAILED_DESIGN_r0001_20261128_KST.md`, `L숫자`는 그 파일의 줄 번호

## 판정: **REVISE**

방향은 타당합니다. 읽기 전용, 기존 책임 재사용, Collector/신규 API 보류, 미확인 API 비확정 원칙을 유지할 만합니다. 다만 **ACL 집행 위치, 권한 거절 시 잔존 데이터, 데이터 계약의 자기모순**은 구현 인계 전에 고쳐야 합니다. 세 건 모두 Linux 현장 자료 없이 문서만으로 수정할 수 있습니다. 자동 R2는 요청하지 않으며 처분은 GPT 몫입니다.

| 등급 | ID | 요지 |
|---|---|---|
| BLOCKING | B1 | 합성·ACL 집행 위치 미정, fail-closed 기준 없음 |
| BLOCKING | B2 | 거절·사용자/호스트 전환 시 이전 결과 유지 가능 |
| BLOCKING | B3 | view model이 자체 불변식을 표현하지 못함 |
| MAJOR | M1~M7 | 실행 판정, 병합·stale, 출력 보안, 기존 기능 보호, 호환·롤백, 시험, 근거 고정 |
| MINOR | m1~m5 | 문서 렌더링, enum, 범위, 게이트, 예시 |

---

## BLOCKING

### B1. 합성과 접근통제를 어디서 집행하는지 없음
- **절/담당:** §5, §5.1, §8, §9 G0 / GPT(설계), Viewer 담당(G0)
- **근거:** L115-125 그림은 ACL 상자 뒤에 `minimum SkillRead aggregation`을 두지만 실행 위치가 없습니다. L128 A1은 "새 서버/API 0개, adapter mapping/UI만 추가"이고, L171은 `adapters/adapter.js`에 "snapshot normalize/ACL-preserving adapter"를 둡니다. L135는 서버의 identity/host/scope 검증을 요구하지만, 그런 서버가 있다는 근거는 패키지에 없습니다.
- **반례:** 기존 adapter가 브라우저 코드이고 기존 제공자가 사용자별 필터를 하지 않습니다. A1대로 6개 원천을 브라우저에서 합치면 권한 밖 호스트의 경로·영수증이 응답에 실리고 화면에서만 숨겨집니다. L162의 "마스킹 UI만 믿고 전송" 금지를 설계 자신이 위반합니다.
- **최소 수정:**
  - "ACL, host scope, 필드 allowlist, 오류 문자열 정제는 브라우저에 도달하기 전에 신뢰 경계(서버 측)에서 집행한다. 브라우저 adapter는 정규화만 한다"를 불변식으로 추가합니다.
  - G0에서 이를 증명하지 못하면 **실데이터를 연결하지 않고** 합성 fixture와 승인된 비민감 참조 정보만 표시하며 상태는 `HOST_NOT_VERIFIED`로 둡니다.
  - A1의 성립 조건에 "기존 제공자가 서버 측 scope를 집행함"을 넣습니다.
- **수락시험:** 권한이 다른 두 계정과 비로그인 상태에서 **네트워크 응답 원문**을 검사합니다. 권한 밖 host, 절대경로, 계정, 토큰, 명령어가 0건이어야 합니다. 화면 검사만으로는 PASS가 아닙니다.

### B2. 권한 거절을 일시 오류처럼 처리해 이전 데이터가 남음
- **절/담당:** §7 L158, §3.2, §5 A5 / GPT
- **근거:** L158 "API/서버 일시 차단 → 섹션 DENIED/UNKNOWN, **기존 결과 유지**하되 stale 표시". `DENIED`와 일시 장애가 한 행입니다. 캐시 파기 규칙은 어디에도 없습니다.
- **반례:** 사용자 A가 host-1 상세를 조회한 뒤 권한이 회수되거나 같은 브라우저에서 계정이 바뀝니다. 재조회가 403인데 이전 영수증과 버전이 stale 배지만 달고 계속 보입니다. 호스트 전환 뒤 실패하면 host-1 값이 host-2 화면에 남을 수 있습니다.
- **최소 수정:** 행을 둘로 나눕니다.
  - 인증·권한 거절(401/403 상당): 해당 scope의 화면·메모리·저장 캐시를 즉시 파기합니다.
  - 일시 장애: **동일 사용자·동일 host·동일 scope**일 때만 stale로 유지합니다.
  - 로그아웃, 사용자 전환, host 전환 때는 파기합니다. 운영 데이터는 브라우저 영속 저장을 금지합니다.
- **수락시험:** 조회 → 권한 회수 → 재조회 후 DOM, 저장소, 뒤로가기 화면에 이전 값 0건. host 전환 직후 실패를 주입해 교차 표시 0건.

### B3. §4 view model이 §4·§6·§7의 요구를 담지 못함
- **절/담당:** §4 L69-104, §10 SM-04/19 / GPT
- **근거와 반례:**

| 설계가 요구하는 것 | JSON의 실제 | 반례 |
|---|---|---|
| digest·channel·role 비교(L141, L157, L103) | installed/active는 `value/state/evidence_ref`뿐이고 digest 없음 | 같은 `v1.0`, 다른 빌드가 일치로 표시되어 SM-19 구현 불가 |
| 상태별 `source_kind/source_revision/observed_at`(L100) | 필드 없음, `public_release`는 state·시각·digest 없음 | 옛 공개 정보의 신선도를 알 수 없음 |
| 두 설치 위치를 둘 다 노출(L154) | `installed_version` 단일 객체 | adapter가 하나를 골라야 함 |
| key에 `host_alias` 포함(L97) | `scope.host_alias` 하나, skill 행에 host 없음 | 두 host 결과를 합칠 때 주체가 섞임 |
| null/UNKNOWN/NOT_RUN/DENIED 구분(L99) | `last_job: null`, `last_update_receipt: null`, `dependencies: []` | Job 원천 거절이 "실행 없음"으로, 의존 미조회가 "의존 없음"으로 보임 |
| 부재 확인에는 완전성 증명(L99, L140) | `presence` 허용값 미정, 예시는 `PRESENT` + 버전 UNKNOWN + `HOST_NOT_VERIFIED` | catalog에만 있는 스킬이 설치됨으로 표시 |

  추가로 SM-04(L195)는 "다중 호스트"를 `CONFLICT`로 요구합니다. L97의 host 포함 key와 L63의 "host별 설치 차이 가능"에 어긋나며, 정상인 2-host 환경이 전부 충돌로 표시됩니다.
- **최소 수정:**
  - 모든 속성을 공통 envelope `{state, value, source_kind, source_revision, digest, channel, source_event_at, fetched_at, evidence_ref, reasons[]}`로 통일합니다. 원천이 주지 않는 값은 `UNKNOWN`입니다.
  - `installations[]`에 `host_alias`와 namespace를 둡니다.
  - `state`와 `presence`의 닫힌 enum을 정의합니다. 모르는 값은 `UNKNOWN`으로 처리합니다.
  - `PRESENT`는 A급 설치 증거가 있을 때만 허용합니다.
  - SM-04를 "다른 host는 별도 행, **동일 host** 내 중복·별칭 모호만 CONFLICT"로 고칩니다.
- **수락시험:** 위 반례 6개와 정상 2-host를 fixture로 만들어, 각각이 서로 다른 출력이 되고 거짓 병합이 0건인지 확인합니다.

---

## MAJOR

### M1. 실행 성공 판정에 역행·버전 결속 반례가 있음
- **절/담당:** §6.4 L142, §7 L155, SM-06 / GPT, job-list 담당(G0)
- **반례:**
  1. 어제 run은 성공 영수증이 있고 오늘 run은 영수증이 없습니다. "영수증 있는 latest_run"을 고르면 어제 SUCCESS가 최신으로 보입니다.
  2. vA에서 받은 성공 영수증이 active vB 옆에 표시됩니다. L142의 결속 키(job/run/skill/host)에는 버전과 digest가 없습니다.
  3. L24의 `latest_result.json` 같은 덮어쓰기형 파일이 run_id 확인 없이 최신 실행으로 쓰입니다.
- **최소 수정:**
  - 원천의 실행 시각·순서로 **최신 시도를 먼저** 고른 뒤 그 시도의 영수증만 판정합니다. 과거 성공으로 대체하지 않고 "이전 성공"으로 따로 표시합니다.
  - 영수증에 revision/digest가 없으면 "버전 미결속"으로 표시합니다.
  - 판정 주체는 Job-list/Runner입니다. Viewer는 backend 판정을 매핑하며, 근거 부족 시 **낮추기만** 하고 승격하지 않습니다.
  - `target_skill` 등 결속 필드의 실존은 G0 항목이며, 없으면 `UNKNOWN`입니다.
- **수락시험:** 위 3건 fixture에서 현재 SUCCESS 표시 0건.

### M2. 원천 병합, stale, 비교 가능성 규칙이 열려 있음
- **절/담당:** §4.1 L111, §3.1 L52-53, §3.2, §5 A4 / GPT
- **반례:**
  - L111은 "오래된 값을 최신으로 교체할 수 있다"고 하는데 L154는 "임의 최신 채택"을 금지합니다. 시계가 빠른 원천이나 하위 신뢰 원천이 값을 덮을 수 있습니다.
  - `STALE` 상태는 있으나 임계값이 없고 A4는 나중에 정하겠다고 합니다.
  - 방금 가져온 한 달 전 영수증이 "마지막 관측 = 지금"이 됩니다.
  - ACL 필터로 빈 목록이 오면 `EMPTY_VERIFIED`, 즉 "0개 설치"가 됩니다.
  - Job 원천이 실패하면 "실패·차단 0"이 됩니다.
  - 개발 채널 공개본과 운영 설치본이 "버전 차이"로 분류됩니다.
- **최소 수정:**
  - 교체는 동일 원천·동일 identity의 더 새 revision에만 허용합니다. 원천이 다르면 `CONFLICT`입니다.
  - 원천 시각과 조회 시각을 분리합니다.
  - 임계값 확정 전에는 "최신/정상"을 선언하지 않고 경과 시간만 표시합니다.
  - `EMPTY_VERIFIED`는 요청 scope 전체의 완전성 증거가 있을 때만 씁니다.
  - 관련 원천이 부분 실패면 요약 숫자는 "확인된 N건(부분)" 또는 "—"로 표시합니다.
  - 채널·체계가 다르면 `NOT_COMPARABLE`입니다.
  - 표시 상태가 겹칠 때(DENIED > CONFLICT > PARTIAL > STALE 등)의 우선순위 또는 복수 배지를 정의합니다.
- **수락시험:** 시계 왜곡, 원천 간 상충, ACL 필터 빈 결과, Job 원천 실패 fixture. SM-11, SM-12를 확장합니다.

### M3. 출력 보안이 "텍스트 escape"에 의존함
- **절/담당:** §4 L104, §3.1 L55, §7 L160, SM-10/14 / GPT, Viewer 담당
- **반례:**
  - escape된 `href="javascript:…"`, `data:`, `//외부호스트`는 여전히 동작할 수 있습니다.
  - `../`나 `%2F`가 든 skill id가 `:id` route나 backend 조회에 그대로 쓰입니다.
  - 외부 GitHub 링크의 Referer로 내부 URL이 나갑니다.
  - backend 예외 문자열에 경로나 토큰이 섞여 `errors[]`로 노출됩니다.
  - C급 공개 정보를 브라우저가 직접 가져오면 업무망에서 외부 요청이 생기고 신뢰할 수 없는 내용이 유입됩니다. 가져오는 방식이 L109에 없습니다.
- **최소 수정:**
  - DOM은 text API만 사용하고 원천 HTML/MD는 렌더하지 않습니다.
  - 링크는 `https`와 호스트 allowlist로 제한하고 `rel="noopener noreferrer"`, no-referrer를 적용합니다.
  - route id는 서버가 발급한 opaque id를 쓰고 서버에서 allowlist 조회합니다.
  - 오류는 reason code만 전달합니다.
  - 공개 참조 정보는 브라우저 live fetch를 금지하고, pin된 정적 사본이나 기존 승인된 서버 경로만 씁니다. 기존 CSP는 완화하지 않습니다.
- **수락시험:** SM-10에 위 payload를 명시합니다. 페이지 진입·상세 중 허용 외 origin 요청 0건, 응답의 경로·비밀 0건.

### M4. 기존 쓰기 흐름 보호와 변경 범위가 느슨함
- **절/담당:** §8 L167-175, §3.1, SM-17/18 / Viewer 담당
- **반례** (실제 코드를 보지 못한 가정 시나리오):
  - Knowledge 편집 중 스킬 관리로 이동해 미저장 내용이 사라집니다.
  - Source Map의 취소 토큰을 공유해 서로의 요청을 취소합니다.
  - "상태 다시 조회"가 실제로는 영수증을 쓰거나 probe Job을 만드는 updater/MCP action에 매핑됩니다.
- **최소 수정:**
  - L170의 "신규 또는 기존 동일 모듈"을 **신규 모듈**과 별도 read-only adapter namespace로 확정합니다.
  - 공용 `index.html`·`app.js`·`adapter.js`는 메뉴 1개와 route 등록 수준으로 제한합니다.
  - 기존 미저장 이탈 guard를 그대로 통과시키고, 취소 토큰은 분리하며, CSS는 범위를 한정합니다.
  - 호출은 부작용 없음이 G0에서 확인된 method allowlist만 허용하고 나머지는 거부합니다.
- **수락시험:** SM-17에 "편집 중 이동" 사례를 추가합니다. SM-18 spy는 Job/Updater/Kernel 외에 MCP action, LLM, 비읽기 HTTP를 포함하고 allowlist 밖 호출 0건이어야 합니다.

### M5. 기준 버전 호환과 Viewer 자체 롤백이 없음
- **절/담당:** §1, §8, §9 G5, SM-19 / GPT
- **근거/반례:** v0.5.8은 개발 후보이고 설치본이 아닙니다(L6). 실제 active가 v0.5.7 이하라면 Source Map route를 전제로 한 SM-01과 §8 변경 대상이 맞지 않습니다. SM-19는 **스킬** 롤백만 다룹니다.
- **최소 수정:** G0의 active build hash에 따라 기준선을 정하는 분기를 둡니다. 불일치하면 구현을 보류하고 v0.5.8 동시 배포를 암묵적으로 묶지 않습니다. 메뉴 비활성 스위치 또는 직전 패키지 복원 절차를 둡니다. schema의 미지 버전·필드는 `UNKNOWN`으로 처리합니다.
- **수락시험:** 기능을 끄거나 롤백한 뒤 기존 메뉴·저장 흐름이 기준선과 같고 잔여 route·캐시가 오류를 내지 않아야 합니다.

### M6. SM-01~20은 범위가 좋지만 판정 기준으로는 부족함
- **절/담당:** §10 L188-213 / GPT
- **근거:**
  - B1, B2, M1~M5의 반례에 대응하는 시험이 없거나 약합니다.
  - SM-16(L207)은 "실측 기록"뿐이라 실패할 수 없습니다.
  - SM-20만 실호스트이고, 나머지의 시험 단계가 표시되어 있지 않습니다.
  - SM-08의 100회는 취소 외에 host·사용자 전환 경합을 명시하지 않습니다.
- **최소 수정:** 시험마다 `fixture 단위 / 통합 / 실호스트 운영`, 필요한 G0 선결, 통과 임계를 열로 추가합니다. 신규 사례는 거절 후 파기, 응답 원문 검사, 과거 성공 대체 금지, 미조회/없음 구분, ACL 빈 결과, 기능 롤백입니다. SM-16은 임계값 확정 전까지 `NOT_RUN`/`UNKNOWN`입니다.
- **수락시험:** B·M 지적마다 시험 ID가 하나 이상 연결된 추적표가 있어야 합니다.

### M7. "고정 근거"가 고정되지 않았고 리뷰 입력과 어긋남
- **절/담당:** §1 L18-29, §9 G3 L184, 리뷰 가이드 / GPT
- **근거:**
  - §1 링크는 모두 `blob/main`의 가변 참조입니다. SHA-256이 적힌 것은 Viewer 패키지 하나입니다.
  - G3는 "원본 인계/카탈로그를 고정된 입력 ZIP으로 제출"이라 하고 가이드도 이를 "유효 입력"으로 적습니다. 실제 패키지에는 **설계서와 가이드 2개 파일뿐**입니다.
- **영향:** §1의 사실 주장(router 변경, Linux `NOT_VERIFIED`, 18+1 스킬 등)은 이 리뷰에서 **전부 미검증 주장**입니다. main이 바뀌면 설계 근거가 달라집니다.
- **최소 수정:** commit pin과 문서별 digest를 기재합니다. G3 문구와 가이드를 실제 입력에 맞추고, 원문 대조는 G1의 미완 항목으로 남깁니다.
- **수락시험:** 각 근거를 pin으로 열어 digest가 일치해야 합니다.

---

## MINOR (비차단 제안)

| ID | 절/근거 | 문제 | 최소 수정 / 담당 / 확인 |
|---|---|---|---|
| m1 | 설계서 전반(L4, L69, L115 등) | 백틱이 `\``로 escape되어 코드 블록과 그림이 렌더되지 않음 | escape 제거 / GPT / 미리보기에서 JSON·그림 블록 확인 |
| m2 | L147 대 L157, §3.2 | `SOURCE_REVISION_CONFLICT`가 대표 목록에 없고 `DIGEST_CONFLICT`와 중복 가능. 상태·reason 대응 없음 | 대응표 하나로 정리 / GPT / 문서 내 코드가 모두 표에 존재 |
| m3 | §0, §3.1, §5 그림 | MVP 과다. Kernel projection은 원천에 있으나 view model 필드가 없음 | 1차는 목록, 설치/활성/공개, 최신 실행·영수증, 근거로 제한. 의존·인계·Kernel 연결은 후속 / GPT / 추적표에 고아 원천 0 |
| m4 | §9, §12 L183·L231 | G0~G2 미완 상태의 G3 리뷰라는 조건부 범위가 불명확. G2는 "0~10절"만 지칭. REVISE/HOLD 처리 경로 없음 | 이번 리뷰는 논리 계약 검토로 한정, G0로 A→B/A3 변경 시 사용자 결정, REVISE 처리 명시 / GPT / 문서 확인 |
| m5 | L83 | `code-analyzer`에 `v0.15.7`을 묶은 예시. 같은 대상인지 패키지로 확인 불가 | 합성 식별자·버전으로 교체 / GPT / 예시에 실명·실버전 결합 없음 |

---

## REQUEST 질문 요약 답변

1. **v0.5.8 충돌:** 실제 router/adapter 코드가 없어 충돌 여부는 `UNKNOWN`입니다. 설계는 route와 API 이름을 확정하지 않은 점이 적절합니다. 위험한 암묵 가정은 서버 측 ACL의 존재(B1), active v0.5.8 기준선(M5), 부작용 없는 조회 수단(M4)입니다.
2. **책임 침범:** §2 표에서 직접적인 침범은 없습니다. Viewer가 실행 성공을 자체 판정하는 방향만 제한하면 됩니다(M1). 새 Collector·DB는 불필요하며 A3 보류가 맞습니다.
3. **혼동 반례:** B3, M1, M2.
4. **ACL·XSS·유출:** B1, B2, M3.
5. **G0 가정:** B1, M5, M7. L29·L182의 `CONDITIONAL` 원칙은 유지하되 항목별 실패 시 동작을 붙여야 합니다.
6. **시험:** M6.

## A안 대 B안

| 항목 | A: UI + 기존 read adapter | B: 입증된 결손만 read projection 확장 |
|---|---|---|
| 상대 비용 | 낮음 | 중간(backend 변경, 권한·회귀 시험) |
| 복잡도 | 낮음. 단 원천이 많으면 합성 로직이 브라우저로 몰릴 위험 | 합성·필터를 서버 한 곳에 둘 수 있음 |
| 안전 | 기존 제공자가 서버 측 scope와 정제를 **이미** 할 때만 안전 | 집행점이 명확해지나 새 노출면과 롤백 대상이 생김 |
| 결손 처리 | 없는 필드는 `UNKNOWN` | 필요한 필드만 allowlist 추가 |

**권장: 조건부 A.** 서버 측 집행이 증명되면 A로 시작하고, 없는 필드는 `UNKNOWN`으로 둡니다. B는 핵심 필드의 결손이 입증되고 별도 설계·승인이 있을 때만 갑니다. 집행점 자체가 없으면 A도 B도 실데이터를 연결하지 않습니다(**실데이터 부분 HOLD**). 비용 평가는 상대 비교이며 실측치가 아닙니다.

## 선결 G0 한 행동

**실제 Linux에서 읽기 전용으로 "브라우저에 운영 데이터를 주는 현행 경로 1개"를 추적합니다.** 산출물은 한 세트입니다.
- active Viewer build hash
- 제공 컴포넌트와 read method 시그니처
- 사용자·host scope를 집행하는 지점
- 비식별 처리한 응답 예시 1건(허용·거절 각각)

이 결과가 A/B/HOLD와 기준 버전을 결정합니다. 자료는 제한된 업무 영역에만 보관하고 공개 저장소에 올리지 않습니다. 집행 지점을 확인하지 못하면 fail-closed(실데이터 미연결)입니다.

---

## 실제로 읽은 지식 파일
- 고정(pinned) 지식: **없음**(REQUEST에 미지정)
- 읽은 파일: `__SKILL_COLLAB_CONTEXT__/FILE_INDEX.txt`, `INDEPENDENT_REVIEW_GUIDE_r0001.md`, 설계서 전문

## 판단 기준 consumer profiles
`l1-workspace-viewer`, `skill-updater`, `job-list`, `work-ledger-kernel`. 프로필 원문이나 해당 스킬 코드는 패키지에 없어, 설계서 §2의 책임 서술을 기준으로 판단했습니다. REQUEST의 `skill_id`인 `l1-knowledge-updater`에 관한 코드나 계약도 패키지에 없어 평가하지 않았습니다.

## 미검증 사항
- Viewer v0.5.8 ZIP의 router·adapter·CSP·권한 코드, 기존 시험 목록
- Linux 설치본, active loader, 사용자 ACL, Job-list/Updater/Kernel/Runner의 실제 필드와 부작용, MCP action 목록
- §1에 링크된 인계·카탈로그·HTML 원문(열지 않았고 패키지에 없음)
- 패키지 및 설계서 SHA-256(직접 계산하지 않음)
- SM-01~20은 모두 `NOT_RUN`입니다. 인계의 PASS 주장은 제가 실행한 PASS가 아닙니다.
- Windows 정적 읽기는 Linux, 사내 LLM, MCP 동작을 검증하지 않습니다.

## 공통 지식 수정 제안 (적용 여부는 GPT 결정)
1. 읽기 전용 운영 화면 공통 규칙: "ACL·필드 allowlist·오류 정제는 서버 측에서 집행하고, 증명되지 않으면 실데이터를 연결하지 않는다."
2. "권한 거절·주체 전환 시 캐시 파기, 일시 장애만 stale 유지"를 구분해 명문화합니다.
3. 상태 표시 규칙: "최신 시도를 먼저 선택하고 과거 성공으로 대체하지 않는다. 소비 화면은 판정을 낮출 수만 있다."
4. 상태 값에는 원천 시각과 조회 시각, host identity, revision/digest를 함께 두고, 미조회와 없음을 구분합니다.
5. 리뷰 패키지 규칙: "유효 입력"으로 선언한 근거는 ZIP에 포함하거나, 미포함임을 명시하고 commit·digest로 pin합니다.
