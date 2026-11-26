# L1 Source Map LLM-first 통합 상세 설계 r0002
2026-11-27 KST / 기존 Work L1-WORKSPACE-RAG-20261111-001
R1 판정 10건 반영. 사용자 최신 결정: 이후 독립 리뷰 생략, GPT 자체 검토/회귀시험으로 진행. R2 생성 금지. 실제 업무 계약/품질 미검증; 운영/그룹 게시 승인 아님.

## 1. 목표 및 경계
Source Map은 C++ 코드 탐색용 지속적 공통 참조 기반. Module/Feature/Procedure/Scenario Knowledge는 동작 원리·조건·시나리오·MSC의 정본이며 Map과 중복 작성하지 않음. 개인 업무 l1-workspace/source-map/을 works/, knowledge/, recovery/와 동등한 독립 영역으로 제안(실제 writer ACL/export 계약 확인 후 확정). Viewer 독립 메뉴. 그룹 l1sw-dev-knowledge에 승인된 Source Map 영역 연계. 공개 L1Work에는 비민감 설계/승인된 패키지만 전달, 실제 지도/코드/경로/로그 반출 금지.
Claude Code JIT/hybrid context와 Aider 제한 Repo Map 개념 참고. exact lookup + bounded expansion 우선. 전체 prompt 주입·전역 재탐색·새 DB/파서/인덱스 엔진 기본 도입 금지. 기존 Discovery 7개 결과 재사용 우선(내용·승인·coverage 미확인). Source Map 없거나 stale이어도 기존 코드 분석 가능.
참조: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ; https://aider.chat/docs/repomap.html ; https://clang.llvm.org/docs/LibTooling.html . 개념 참조이며 실제 설치/비공개 구현 동일성 주장 아님.

## 2. 역할 및 변경 대상
| 소유 | 구성 | 요구 |
|---|---|---|
| 설계 GPT | 공통 계약 | 데이터/조회 규격, 합성 fixture, 자체시험 |
| 설계 GPT | Viewer | 독립 메뉴, 검색/상세/근거/버전/gaps, 기존 UI·Write 보호 유지 |
| 설계 GPT | code-analyzer | 제한 코드 사실 제공 + 선택적 Map 참조. 기존 입력으로 연결 가능하면 NO_CHANGE; 재현 결손만 수정 |
| 설계 GPT | work-ledger-kernel / l1-fix-workflow | 기존 Work/Evidence/공통 export 유지; source-map 보존·참조 전달 미지원 입증 시만 수정 |
| 설계 GPT | doc-converter | 기존 MSC/문서 변환 유지; Map 전용 renderer 기본 개발 금지 |
| 업무 GPT | l1-knowledge-updater | Discovery·검증·생성·갱신·개인 저장 요청·그룹 비교/Preview/게시·readback 전담 |
| 업무 GPT | Personal Store Writer | 승인된 actor/path·CAS·readback·충돌/경합 보호. Updater만 Map write 요청 |
| 업무 GPT | l1-channel-recovery | V1~V2 정상 Procedure/코드 사실, V3 후보 확장; 읽기 전용, 신뢰도 전파 |
| 업무 GPT | MCP/Viewer adapter/조회 | 실제 지원 action과 권한 확인 및 최소 연결 |
Job-list는 기존 실행 계약 유지. 신규 스킬/엔진 도입 금지. 설계 GPT는 업무 전용 Updater·Recovery 구현을 추정하지 않고 인계; 업무 GPT는 실제 설치 계약을 대조.

## 3. 데이터 계약 후보(기존 형식 매핑 우선)
정본은 하나의 검증된 snapshot. JSON/JSONL은 논리적 권장 표현이며 새 필수 API/schema는 G0 확인 전 확정하지 않음. 물리 형식은 기존 기능 재사용.
- manifest: map_id, snapshot_id, source_identity, source_revision, build/variant, scope/exclusion, producer/version, extraction method, coverage/gaps, record/hash 목록, 생성 시점, predecessor.
- entity: entity_id, kind(module/file/function/class/struct/enum/message/state), canonical/qualified name, signature/qualifiers, module/RAT, source-relative anchor, variant, provenance, extraction_status, validation_status.
- relation: relation_id, source/target entity IDs, kind(contains/declares/defines/calls/registers/dispatches/sends/receives/payload/read/write/callback/include/knowledge_ref), applicable build/guard, provenance, extraction_status, validation_status, evidence_refs. REQ/CNF/IND 대응은 근거 있는 경우만 기록. 등록·정적 도달·실행 관찰은 다른 관계.
- evidence: source revision/build, anchor(파일·심볼·범위), excerpt/hash 또는 기존 Evidence 참조, 검증 주체/방법/결과. 원문은 업무 환경에만 보존.
- gaps: 조사 범위/제외/잘림/unknown 및 재조회 힌트. absence of map entry != absence of code.
- identity: qualified name + signature/qualifiers + linkage/TU(필요시) + definition anchor + build variant. 동명/오버로드/템플릿/매크로/조건부 빌드/간접 호출 해소 불가면 별개 후보 UNKNOWN. revision 간 안정 alias는 실제 확인 시만 연결.
- provenance(parser/tool/LLM/manual/unknown)과 extraction_status(EXTRACTED/INFERRED/UNKNOWN), validation_status(VERIFIED/UNVERIFIED/CONFLICT) 분리. EXTRACTED도 자동 VERIFIED 아님. LLM 추론을 근거 없이 추출/검증으로 승격 금지. 새 실제 증거가 있으면 별도 검증 기록·revision을 남겨 변경. freshness는 소비 시 현재 source pin/build 비교로 별도 판단.
- 실제 Analyzer가 어떤 방식으로 추출하는지 현재 미확인. AST 기반임을 전제하지 않음. 업무 G0에서 action별 파서/문자열/LLM 혼용 및 정확도 확인. 이 조건이 해소되기 전 실제 데이터 정확성 인증/확대 금지.

## 4. 조회 계약과 Workflow
논리적 조회 단위: 현재 프로젝트/revision/build + query(모듈/심볼/message ID/구조체/state) + relation types/direction + scope + budget. 기존 action으로 표현 가능하면 그대로 사용.
반환: snapshot/revision/build, freshness, 매칭 entity/relations, 근거 refs, provenance/validation, coverage/truncated/next candidate, unknown/conflict. 결과 정렬: exact qualified ID > exact symbol/message > 관련 모듈 > 제한 1-hop; 더 깊은 확장은 목적과 예산 확인 후. 별도 랭킹은 실제 실패 사례/효과/비용/소유권/승인 평가 후만.
1. 요청 대상/실제 source pin/build 확정. 기존 지도·Knowledge 확인.
2. 관련 소규모 Map bundle 선택. 일치하지 않으면 STALE/UNKNOWN 힌트로만 소비; 실제 코드 확인.
3. Code Analyzer로 현재 원본 bounded probe, relation/guard/상태/메시지 검증. Map 밖 탐색 가능; 맵에 없다는 이유로 후보 제외/종결 금지.
4. Updater는 누락/충돌 변경 후보를 같은 Work에 보존. 소비자 직접 Map write 금지.
5. Updater가 권한 내 기존 산출물과 대조, 필요 부분만 Discovery/정규화, 검증, 승인된 writer 저장/readback. G6의 정확한 승인 범위는 G0; 자동 우회 금지.
6. 동일 활성 snapshot을 Viewer/스킬/MCP에서 조회. 그룹 반영은 별도 Preview/승인/CAS/readback, 개인 분석 보존.
Recovery: V1→V2에는 관련 정상 Procedure Knowledge와 실제 source facts를 조합; V3에는 map seed와 map 외 탐색 병행. 모든 후보에 원래 신뢰도/source pin/근거 유지. V4~V6 최초 위반·반대 근거·복구 책임·MSC 의미 검증. CNF timeout 제외 정책 유지.

## 5. 저장/갱신/충돌
후보 논리 트리: source-map/README.md, manifest.json, nr/, lte/, common/, interfaces/, index/, history/, gaps.md. 구조화 정본과 MD/기존 HTML 표시는 동일 snapshot에서 파생. snapshot 변경 시 파생물 재생성 및 ID/hash 일치 확인. 기존 atomic/CAS 계약으로 staging 검증 후 활성 참조 전환; 미지원이면 HOLD, 혼합 revision 노출 금지. 경로/활성 참조의 구체 방식은 기존 writer/ACL 확인 후 결정. Kernel exporter는 source-map 영역을 보존하며 write 소유권 침범 금지.
기존 7개 산출물/manifest/revision/coverage/hash 대조. 중복은 동일 ID/동일 근거일 때 병합, 충돌은 원문 확인 전 HOLD; 오래된 원본·이력 보존. 한 프로젝트/build 선택 범위에서 승인된 활성 snapshot 하나. 그룹 Base/Ours/Theirs 비교, 충돌·stale Preview·권한 없음 차단. 그룹 게시 성공 후 정산 실패는 정산만 재개, 재게시 금지. 게시/승인 불확실 자동 retry 금지.

## 6. LLM 예산 및 평가
업무 모델 Qwen3.6-27B 표기는 사용자 제공 식별자이며 실제 모델 ID/context/output/tool 상한 G0 확인. 초기 pilot 제안(기존 낮은 상한 우선): Map bundle <=4096 tokenizer tokens, <=50 records, 1-hop 기본; actual source distinct files <=20/step, 총 <=60/task, 최대 4단계의 추가 probe, 총 입력+출력 토큰 <=32768/task 및 시간 <=20분/task. 실제 모델/런너 한도 확인 후 pilot 전에 합의·고정. 토큰 계측 불가 시 NOT_VERIFIED 및 확대 보류. 한도 도달 partial/unknown/next action, 조용한 잘림 금지.
동일 source/build/model/config/허용 tools/총 예산·질의·정답 기준으로 독립 맥락 D0 현행, D1 map-only, D2 procedure-only, D3 both. D1/D3 지도 번들 포함 비용 계측, 사전 Discovery 구축 비용과 갱신 비용 별도. 실제 실패 Seed 1건과 독립 평가 사례(정답 입력 노출 금지). 담당자 검증 골드 관계 >=30, 음성/반례 >=10(오버로드/variant/없는 등록/간접 호출/동명 포함). 분모 사전 고정, unknown은 recall 누락에 포함, precision은 검증된 예측만이 아니라 전체 확정 예측으로 계산. 파일 수·토큰·시간·오탐·누락·unknown 기록. pilot 수락 목표 recall >=90%(30개면 >=27), 근거 없는 CONFIRMED 0, stale/variant 불일치 검출 100%, 범위 밖 읽기 0. 음성 오탐 별도 측정. 근거 없는 CONFIRMED 1건이면 해당 결과 게시/확대 즉시 HOLD, 수정 및 회귀. D1/D3 개선이 재현되지 않으면 Map 활용 확대 보류; 결과 차이는 원인 단서이지 단일 시험 인과 확정 아님. Recovery V2 규칙 정확도/V3 후보 recall·precision/V4 잘못된 종결 별도. 성능 수치는 목표이며 실측 아님.

## 7. Viewer UI 최소 범위
기존 Wiki UI 유지. top-level Source Map 메뉴(Work/Knowledge/Recovery 동일 레벨). 왼쪽 RAT/module·종류 탐색, 중앙 검색 결과 표(name/type/owner/revision/status), 상세 entity/relations·근거·관련 Knowledge/Work 링크, 상단 revision/build/coverage, 우측 기존 목차/도우미 유지. 필터: module, symbol, message/handler, struct/state, verified/inferred/unknown, stale. 큰 전체 그래프는 후순위. 사용자 열람은 MD/기존 렌더 우선; 링크 허용 경로·접근 권한 확인, 내부 원문 외부 URL 생성 금지. Map 미등록/충돌/미검증/읽기 실패는 각각 구분. Viewer는 생성/갱신 엔진이 아님.

## 8. 단계별 실행 게이트와 자체 시험
G0 업무 GPT: 활성 Updater/Analyzer/Writer/Kernel/MCP/adapter/Recovery version/action/권한, 7개 산출물의 manifest/hash/필드/coverage/추출 근거, G6 개인 vs 그룹 승인 범위, source-map path/export/search/readback, 모델/예산 확인. 원문 반출 요구 없음. 읽기 전용. 현장 응답 없으면 BLOCKED_HOST_CONTRACT.
G1 설계 GPT: G0에 근거하여 공통 계약 확정, 합성 fixture 및 UI 목업, 기존 관리 스킬 원본의 실제 gap 확인. 독립 리뷰 생략, 자체 검토·시험 필수.
G2 업무 GPT: 대표 모듈 한 개 기존 map 재사용/후보 생성, 동일 예산 D0~D3 실제 검증; 권한 없으면 해당 write NOT_RUN.
G3 설계 GPT: 필요한 관리 스킬만 변경/전체 회귀/패키지 해시·기존 기능 보존; 업무 GPT 인계/현장 adapter·Updater·Recovery 연동과 E2E. 설치/운영 전환은 별도 승인.
G4: pilot 수락 후 RAT 단위 점진 확대, 그룹 게시 별도 승인. 전체 Discovery/Job 재실행 기본 금지.
자체시험 T01 오버로드·variant·동명 분리; T02 LLM inferred 격상 방지; T03 등록 vs 실행 구별; T04 stale/unknown 및 map 외 탐색; T05 budget/partial/actual reads; T06 기존 산출물 중복/충돌; T07 CAS/ACL/혼합 snapshot 차단 및 readback; T08 MD/JSON 동일 snapshot; T09 Viewer 검색·링크·원문 및 기존 기능 회귀; T10 Recovery 신뢰도 전파·종결 보호; T11 D0~D3 고정 분모·비용 측정; T12 그룹 승인·정산 실패 재게시 방지.
R1 추적: B1 §3/8; M1 §6; M2 §4; M3/m1 §6; M4 §4; M5 §5; M6 §8; m2 §5; m3 §8.
현재 설계 보완만 완료. 호스트 G0/코드 수정/실제 테스트/설치/그룹 게시 NOT_RUN. 독립 리뷰 R2 SKIP_USER_DIRECTIVE.
