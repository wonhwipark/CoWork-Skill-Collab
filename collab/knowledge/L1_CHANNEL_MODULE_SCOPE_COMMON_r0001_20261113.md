# L1_CHANNEL 공통 사전지식 — 담당 모듈 범위와 Knowledge 분석 분류

- Revision: **r0001 / 2026-11-13 KST**
- Repository: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/knowledge/`
- Status: **USER_CONFIRMED_SCOPE + OWNER_REVIEW_CANDIDATE** — 실제 코드 사실·모든 3GPP 적합성·전체 항목 확정 아님
- Purpose: 새로운 지식 업데이트, 모듈 간 이슈 조사, 분석 범위 설정, 담당자 회의 및 사내 GPT 검토 전에 참고할 **공통 사전 맥락**
- Full review table: [L1 NR/LTE 담당자 검토용 v0.7 (A 97행, B 84행)](references/L1_NR_LTE_OWNER_REVIEW_CLASSIFICATION_v0_7_20261113.md)
- Provenance: 사용자가 정의·정정한 모듈 책임 및 대화에서 작성한 v0.6/v0.7 분류 초안. **v0.7 ↔ v0.6 완전 1:1 대조 미실시**; 실제 코드 증거와 담당자 검토 전까지 가설/후보로 처리

## 1. 사용자 확인 담당 분야 — 향후 작업의 기본 조사 범위

| 담당 분야 | 역할에 관한 사용자 확인 사항 | 분석 경계 |
|---|---|---|
| **NR BCH Controller (`BCH_CTRLR`)** | 이름과 달리 PBCH 전용이 아닌 **NR L1 Channel Controller**. DL/UL SCell Configuration/Activation/Deactivation/Release의 **L1 Channel Procedure 주관** | Cell Search/Measurement는 Measure Controller 소유; DRX 상태머신은 DRX Controller 소유. 관련 인터페이스만 필요 범위에서 확인 |
| **LTE ChCfg** | NR BCH에 대응하는 **LTE L1 Channel Configuration Controller** 역할 | LTE Channel/SCell 절차 중심으로 검토, NR 전용 BWP 기능을 자동 전용하지 않음. 구체적 구현/호출 경계는 코드 검증 필요 |
| **NR L1 Tx** | NR UL 송신 설정·Tx resource·switching 담당 영역. NR SCell L1 절차에 **UL Tx 하위 구간으로 참여** | SCell 전체 주관으로 취급하지 않음. 참여 조건과 하위 호출을 코드로 확인 |
| **LTE L1 Tx** | LTE UL Tx·Tx path/resource·LTE SCell UL Tx 참여 영역. NR Tx와 **공통 분석 분류 모델** 사용 | LTE 실제 지원 기능을 NR에서 그대로 복제하지 않음. Tx Antenna Switching 등은 코드 확인 항목 |

- 이 목록은 **분석할 선호/담당 범위의 사용자 정의**다. 사내 조직의 공식 소유자 표나 클래스/코드 소유권을 검증한 문서는 아니다.
- 개인의 유일 담당 범위를 넘는 이슈는 관련 Interface 범위까지 조사할 수 있으나, 타 모듈 전체를 사용자 담당이라고 확대 해석하지 않는다.

## 2. 재사용 분류 원칙

1. **A. Procedure / Scenario**: 3GPP 통신 절차/네트워크 상태 변화를 상위 기준으로 설정하고, 각 L1 모듈 관점에서 발생하는 대표 흐름·변형·AS-IS MSC 후보를 열거. 카테고리명 중 사내 편의상 집계한 이름도 있으므로 모든 명칭이 3GPP의 독립 표준 절차라는 주장은 금지.
2. **B. Technical Knowledge**: Physical Channel/Reference Signal, BWP·CC·SCell, Tx Resource, Switching, Configuration, Interface, State/Recovery 등의 공통 재사용 기술을 별도 축으로 분리.
3. **A↔B는 링크**: 동일 기능의 개별 Procedure 흐름과 공통 기술 설명을 연결하고 내용을 무조건 중복 작성하지 않는다.
4. **코드 분석 전에 항목 확정하지 않음**: 표의 `미검토`는 적절성·지원여부·완전성 확정이 아니라 담당자 검토 대기 상태.
5. **우선순위**: 담당자/회의에서 누락·분류 확인 → 사내 GPT 종합 점검 → 선정된 항목만 `l1-knowledge-updater`(+ 적합한 기존 `code-analyzer`, `doc-converter`) 분석 후보.

| 모듈 | A 검토 세부 행 수 | B 검토 세부 행 수 | 구분 |
|---|---:|---:|---|
| NR BCH (L1 Channel) | 9개 | 7개 | NR L1 Channel |
| NR L1 Tx | 10개 | 7개 | NR UL Tx |
| LTE ChCfg (L1 Channel) | 8개 | 7개 | LTE L1 Channel |
| LTE L1 Tx | 8개 | 7개 | LTE UL Tx |
| **계** | **97** | **84** | **총 181개 검토 후보** |

### 1. NR BCH (L1 Channel)

**A. Procedure / Scenario**: Initial Access / Attach · System Information Acquisition · RRC Reconfiguration · Mobility / Handover · Cell Change / Recovery · Release / Suspend / Resume · Exception / Recovery · BWP Switching · SCell Config / Activation / Deactivation / Release

**B. Technical Knowledge**: L1 Channel Configuration · PBCH / MIB / System Information · BWP / CC / SCell Resource · Interface · State Management · Timing / Scheduling · Recovery / Diagnostics

### 2. NR L1 Tx

**A. Procedure / Scenario**: Initial Access / UL Transmission · RRC Reconfiguration · UL CA / SCell 참여 · EN-DC · Mobility / Handover · Connected Mode UL Tx · CDRX 연동 · Exception / Recovery · NRDC · Dual SIM

**B. Technical Knowledge**: UL Physical Channel · Reference Signal / SRS · Tx Resource · Tx Switching · Tx Configuration · Interface · State / Recovery

### 3. LTE ChCfg (L1 Channel)

**A. Procedure / Scenario**: Initial Access / Attach · System Information Acquisition · RRC Reconfiguration · SCell Config / Activation / Deactivation / Release · Mobility / Handover · PCell / CC Reconfiguration · EN-DC LTE Anchor 연동 · Release / Exception / Recovery

**B. Technical Knowledge**: LTE Channel Configuration · MIB / SIB / System Information · PCell / SCell / CC Resource · Interface · State Management · Timing / Scheduling · Recovery / Diagnostics

### 4. LTE L1 Tx

**A. Procedure / Scenario**: Initial Access / UL Transmission · UL Tx Configuration · UL CA / SCell 참여 · UL Tx Resource · Tx Antenna / Path Switching · EN-DC · Dual SIM · Exception / Recovery

**B. Technical Knowledge**: UL Physical Channel · Reference Signal / SRS · Tx Resource · Tx Switching · Tx Configuration · Interface · State / Recovery

## 3. 핵심 시나리오 경계/조건

| 분석 주제 | Procedure / Scenario(A)에서 관리 | Technical Knowledge(B)에서 관리 | 판정 주의 |
|---|---|---|---|
| NR/LTE SCell Config/Act/Deact/Release | 해당 RAT의 **Channel Controller** L1 Procedure, L1 Tx는 UL Tx 관련 하위 처리 | Channel config/resource/state, Tx config/resource/interface | DL/UL 영향 구간을 구별하지만 DL·UL Activation이 항상 별도 네트워크 이벤트라는 의미는 아님 |
| NR BWP Switching | NR BCH의 BWP 관련 L1 설정·전환 시나리오 | BWP/CC/SCell Resource, State/Timing | RRC/DCI/Timer 각 트리거의 실제 수행 모듈 확인. LTE에 자동 복제 금지 |
| NR Tx UL Tx Switching / SRS Carrier Switching | UL CA/SCell, Connected, 기타 실제 연계 Procedure의 조건부 Tx subflow | Tx Switching, Reference Signal/SRS, Tx Resource | 모든 SCell 이벤트에 필수 실행된다고 간주하지 않음 |
| NRDC | NR L1 Tx: **BB TX Reconfig, F1 Rank Change** | Tx Configuration / Interface / State | **EN-DC와 별도 분류**. `F1` 의미·조건은 사내 코드/정의 확인 필요 |
| UL CA | NR L1 Tx: SCell의 UL 참여 및 **SLO, RF Tx Configuration** 관련 흐름 | Tx Configuration / Resource / Switching | `SLO` 사내 의미 및 실제 조건 확인 필요 |
| Dual SIM | NR/LTE L1 Tx: **Tx Sharing, BB Tx Change** 후보 | Tx Resource / Switching / Configuration | 실제 RAT별 지원, 우선순위 및 BB 변경 범위는 코드 확인 |
| DRX/Search/Measure | **TX는 CDRX 연동만**, Channel Controller는 인터페이스까지만 | State / Interface 연동 | Measure의 Search/Measurement, DRX Controller의 Idle DRX/CDRX 본체는 대상 아님. **Paging 독립 시나리오 제외** |

## 4. 새 이슈·분석 요청 시 사전 확인 절차

- 본 공통 문서를 먼저 보고 관련 RAT/모듈과 A Procedure, B Technical 후보를 선택. 모듈 이름만으로 분석 범위를 확장하지 않음.
- 실제 소스의 branch/commit, 구현 메시지·핸들러/상태, 결과물/영수증을 확인하고 `IN_SCOPE_CANDIDATE / INTERFACE_ONLY / OUT_OF_SCOPE / NEEDS_OWNER_CONFIRMATION` 중 하나로 범위를 판정.
- 예: NR SCell Activation에서 Tx Path 변화가 핵심이면 **NR BCH의 SCell Procedure(A)** + **NR L1 Tx 참여(A)** + **Tx Switching(B)** 를 연동. 자동 실행 또는 지식 정본 갱신 요청으로 간주하지 않음.
- 대표 시나리오 선정 후의 산출물 후보: Overview, 코드 근거(Code Facts), 검증된 AS-IS MSC, 조건·예외·상태, 기존 그룹 지식 `l1sw-dev-knowledge` 변경 후보. 그룹 정본 변경/배포는 별도 승인.
- 이번 단계에서 코드 검토, LLM 분석, Job-list 실행, Skill-Updater 배포, 그룹 지식 수정, 독립 리뷰는 **모두 NOT_RUN**.

## 5. 담당자 검토/변경 관리

- Confluence용 원표는 **모듈 / 대분류 / 세부 시나리오·기술 / 담당자 검토** 4열로 유지하며 `적절 / 누락 / 변경 / 제외`로 피드백.
- v0.7 표의 181행은 분류 후보일 뿐, 누락 없음이나 기능 구현을 보증하지 않는다. 필요하면 신규 개정판으로 델타만 반영하고 이전본 보존.
- 기존 v0.6 설계 초안과의 1:1 대조 및 담당자/사내 GPT 검토가 남아 있다. 이 공통 문서의 변경이 사내 환경, 코드, 스킬, 운영 watcher, 자동 리뷰 또는 PUBLIC ZIP의 실행 신호가 되지 않음.
