# CoWork 협업 대시보드

> **PRIVATE · GitHub에서 바로 보기 · MIGRATION_NOT_CUTOVER**
>
> 활성 리뷰 제공자 기록 미확인. 이 화면은 GitHub 기록을 읽기 전용으로 표시합니다.

## 리뷰 처리 흐름

**REQUEST → READY → REVIEW → RECEIPT → GPT 판정**

## 협업 흐름과 상태 · 역할 기준

**협업 관리 환경** — GPT · GitHub / **업무 실행 환경** — Windows 감시기 · Claude Code

```mermaid
flowchart TB
  subgraph LIVE["현재 리뷰 제공자 기록 미확인"]
    L1["최신 CURRENT.md 확인"] --> L2["운영 근거 검증 필요"]
  end
  subgraph NEXT["GitHub 목표 경로 · 개별 리뷰 검증 별도"]
    A["GPT 요구·범위 확정"] --> B["GitHub PRIVATE / REQUEST·READY"]
    B --> C["Windows watcher / 승인·신뢰 검증"]
    C --> D["Claude Code / 독립 리뷰"]
    D --> E["GitHub PRIVATE / 리뷰·영수증"]
    E --> F["GPT / 판정·피드백"]
    F --> G["GitHub Actions / 대시보드"]
  end
  %% 독립 리뷰 운송은 별도 유효 요청과 LIVE 승인 이후에만 실행
```

> 화살표는 설계된 경로입니다. Windows 실행·서명 검증·독립 리뷰의 PASS를 뜻하지 않습니다.

### 운영·검증 상태

| 구분 | 현재 상태 | 근거 범위 |
|---|---|---|
| 현재 운영 경로 | **활성 리뷰 제공자 기록 미확인** | 최신 이관 CURRENT 기록 · 실제 호스트는 별도 검증 |
| GitHub 전환 | **기록 미관측** | 호스트 보고·GPT 판정과 신규 요청 실전 검증은 별개 |
| Windows 실행·SHADOW | **기록 미관측** | 실제 호스트 실행 증거 필요 |
| Claude Code 독립 리뷰 | **기록 미관측** | 자체 시험과 구분 |
| GitHub 요청·결과·영수증 | **요청 17 · 결과 12 · 영수증 12** | PRIVATE 파일 관측 수일 뿐 완료 건수가 아님 |
| 공개 Work 대시보드 | **기록 미관측** | L1Work에 승인된 비식별 상태만 자동 요약 · PRIVATE 원문은 비공개 |

[전환·Windows 원문](../projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) · [대시보드 원문](../projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md)


## 한눈에 보기

| 현재 프로젝트 | GitHub REQUEST | GitHub REVIEW | GitHub RECEIPT |
|:---:|:---:|:---:|:---:|
| **10** | **17** | **12** | **12** |

**파일 수 = 검증 완료 건수 아님.** 아직 GitHub로 이관되지 않은 자료는 미확인입니다.

**[원본 HTML 파일](index.html)** · **[자동 갱신 Actions](../../.github/workflows/cowork-dashboard.yml)** · **[설명](README.md)**

HTML은 GitHub에서 소스로 표시되므로 다운로드 후 브라우저로 열 수 있습니다. 이 페이지는 GitHub에서 바로 렌더링됩니다.

---
## 상세 현황

> **MIGRATION_NOT_CUTOVER** — 활성 리뷰 제공자 기록 미확인. GitHub 기록과 리뷰 실행은 별개입니다.

이 문서는 GitHub Actions가 생성하는 안내 화면이며 리뷰·설치·배포 승인이나 자동 실행 결과가 아닙니다.

- 문서가 있는 프로젝트: **10개**
- GitHub REQUEST 파일 관측: **17개** (검증 안 됨)
- GitHub REVIEW 파일 관측: **12개** (검증 안 됨)
- GitHub RECEIPT 파일 관측: **12개** (검증 안 됨)



## 작업별 진행 현황 · 독립 Work Tracker

각 Work는 고유 ID로 구분. 단계/시험/리뷰 표시는 문서 신고값이며 실제 완료 검증이 아닙니다.

| Work ID | 스킬 | 진행 단계(신고) | 담당 | 시험(신고) | 독립 리뷰(신고) | 다음 조치 |
|---|---|---|---|---|---|---|
| [COWORK-AUTO-APPROVAL-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md) | 미지정 | 단계 미확인 | 미등록 | NOT_VERIFIED | NOT_VERIFIED | CURRENT.md 최신 상태 및 다음 담당 확인 |
| [COWORK-DROPBOX-TO-GITHUB-MIGRATION](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) | cowork-review-watcher | 완료 신고 (검증 필요) | GPT / Claude Code | PASS | PASS | 2026-11-18: GPT CRLF 독립 게이트 fixture 최소 수정·원격 readback PASS (commit 9b9141b, sha256 409c956d…). 운영 GitHub LIVE/v0.2.25는 기존 호스트 보고 유지. Windows pending/Guard 원샷 실행 결과 미 |
| [COWORK-GITHUB-DASHBOARD-20261111-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md) | cowork-dashboard | 완료 신고 (검증 필요) | GPT | PASS | NOT_RUN | P1 4카드·P2 관계/변경분 B안 Pages 게시, 합성 UI·Pages 배포 PASS, 독립 리뷰 사용자 생략. 다음: PC/모바일 실제 보기 |
| [COWORK-SKILL-DISCOVERY-20261112-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md) | skill-discovery | 완료 신고 (검증 필요) | GPT | PASS | NOT_RUN | P1/P2 질문별 조회·근거 관계·변경분 PRIVATE 구현/CI PASS, 사용자 독립 리뷰 생략. 공개 B안 배송 완료. 다음: PC/모바일 시인성 확인 |
| [ISSUE-ANALYZER-20261114-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/ISSUE-ANALYZER-20261114-001/CURRENT.md) | issue-analyzer | 차단·보류 | GPT | NOT_VERIFIED | NOT_RUN | 전체 회귀·독립 리뷰 후 L1Work PUBLIC 루트에 ZIP 게시 및 SHA 원격 재검증 |
| [JOBLIST-NRTX-20261112-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md) | job-list | 개발·시험 | GPT | PASS | NOT_RUN | Windows Claude Code에서 handoff 리뷰 r0002 원샷의 실설정 사전검증/정식 요청 가능성 판정 후 허용된 리뷰 1회 |
| [JOBLIST-SMOKE-20261114-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-SMOKE-20261114-001/CURRENT.md) | 미지정 | 단계 미확인 | 미등록 | NOT_VERIFIED | NOT_VERIFIED | CURRENT.md 최신 상태 및 다음 담당 확인 |
| [L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001/CURRENT.md) | l1-knowledge-updater | 독립 리뷰 | GPT | PASS | NOT_RUN | v0.9 215행 담당자 검토; 실제 ID·산출물 검증은 첫 승인된 분석 후속 |
| [L1-WORKSPACE-RAG-20261111-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) | 미지정 | 단계 미확인 | 미등록 | NOT_VERIFIED | NOT_VERIFIED | CURRENT.md 최신 상태 및 다음 담당 확인 |
| [NR-L1TX-CODE-ANALYSIS-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md) | 미지정 | 단계 미확인 | 미등록 | NOT_VERIFIED | NOT_VERIFIED | CURRENT.md 최신 상태 및 다음 담당 확인 |

스킬별 병렬 작업은 각 프로젝트의 TRACKER.json으로 등록합니다. 등록 전에는 확인되지 않은 실제 진행률을 추정하지 않습니다.


### 프로젝트별 상태 원문

| 프로젝트 | 문서상 상태 | 근거 |
|---|---|---|
| COWORK-AUTO-APPROVAL-20261115-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md) |
| COWORK-DROPBOX-TO-GITHUB-MIGRATION | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) |
| COWORK-GITHUB-DASHBOARD-20261111-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md) |
| COWORK-SKILL-DISCOVERY-20261112-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md) |
| ISSUE-ANALYZER-20261114-001 | 상태 확인 필요 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/ISSUE-ANALYZER-20261114-001/CURRENT.md) |
| JOBLIST-NRTX-20261112-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md) |
| JOBLIST-SMOKE-20261114-001 | 상태 확인 필요 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-SMOKE-20261114-001/CURRENT.md) |
| L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001 | 상태 확인 필요 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001/CURRENT.md) |
| L1-WORKSPACE-RAG-20261111-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) |
| NR-L1TX-CODE-ANALYSIS-20261115-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md) |

미이관 파일이나 승인·서명 검증 결과가 없어도, 이 화면은 이를 임의로 성공/0건 완료 처리하지 않습니다.

## GitHub 리뷰·GPT 판정 연결

문서 연결은 승인 서명·운영 실행 검증이 아닙니다.

| 요청 | Work | 단계 | GPT 판정 |
|---|---|---|---|
| [REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-ACE-PEC-HOP-ACON-DESIGN-R1-20261118/REQUEST.md) | COWORK-SKILL-DISCOVERY-20261112-001 | GPT_RECORDED_UNAUTHENTICATED | ACCEPT_WITH_CHANGE |
| ↳ N1 | reuse ordered Work decisions and explicit authorization; conflicts HOLD; ACE-02 counterexample | ACCEPT_WITH_CHANGE | - |
| ↳ N2 | compare source pinned bytes/offset SHA-256 against quoted ranges; PEC-01/03 corruption tests | ACCEPT_WITH_CHANGE | - |
| ↳ N4 | ACE role names are existing manual workflow stages; no new subagents or paid calls | ACCEPT | - |
| [REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-AUTO-APPROVAL-V023-R2-20261115/REQUEST.md) | COWORK-AUTO-APPROVAL-20261115-001 | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-BUDGET-V025-DESIGN-R1-20261117/REQUEST.md) | COWORK-AUTO-APPROVAL-20261115-001 | READY_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-BUDGET-V025-LARGE-R2-20261117](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-BUDGET-V025-LARGE-R2-20261117/REQUEST.md) | COWORK-AUTO-APPROVAL-20261115-001 | GPT_RECORDED_UNAUTHENTICATED | ACCEPT_WITH_CHANGE |
| [REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001/REQUEST.md) | COWORK-GITHUB-DASHBOARD-20261111-001 | READY_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-V0214-R1-20261114](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0214-R1-20261114/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-V0217-R2-20261114](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0217-R2-20261114/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| ↳ N1 | — Approval nonce has no replay store (relevant to Q7)** | NOT_ADJUDICATED | - |
| ↳ N2 | — `repo_id` is a config-supplied label, not a GitHub-verified identity (Q7, confirms known gap)** | NOT_ADJUDICATED | - |
| ↳ N3 | — `read_github_token`'s repo-match check is advisory, not authorization (Q7, cli.py:33-55)** | NOT_ADJUDICATED | - |
| [REQ-COWORK-V0219-R2-20261114](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0219-R2-20261114/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| ↳ Q1 | — Atomicity of the reservation | NOT_ADJUDICATED | - |
| ↳ Q2 | — Duplicate keys / binding | NOT_ADJUDICATED | - |
| ↳ Q3 | — Classification / double start / permanent refusal | NOT_ADJUDICATED | - |
| ↳ Q4 | — Crash / restore | NOT_ADJUDICATED | - |
| ↳ Q5 | — Remote errors / fail-closed | NOT_ADJUDICATED | - |
| ↳ Q6 | — N2 repository-id binding — **BLOCKING finding** | NOT_ADJUDICATED | - |
| ↳ Q7 | — Cost/gates, reservation vs. ceilings, SHADOW | NOT_ADJUDICATED | - |
| ↳ Q8 | — Interaction with v0.2.18, locking, seal_interrupted, publish-only retry | NOT_ADJUDICATED | - |
| [REQ-COWORK-V0220-R1-20261115](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0220-R1-20261115/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-V028-AUTO-REVIEW-R1-20261120](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V028-AUTO-REVIEW-R1-20261120/REQUEST.md) | COWORK-AUTO-APPROVAL-20261115-001 | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-MSC-DUAL-ENTRY-DESIGN-R1-20261117/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | GPT_NOT_OBSERVED | NOT_VERIFIED |
| ↳ Q9 | (과잉 설계 여부)**: 섹션 2, 5, 7에서 신규 엔진/Kernel 상태기계/Evidence enum/Work profile 확장을 명시적으로 기본안에서 제외했습니다. 재사용  | NOT_ADJUDICATED | - |
| [REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | READY_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | READY_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-WORK-KNOWLEDGE-FIXED-R1-20261116/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | GPT_RECORDED_UNAUTHENTICATED | ACCEPT_WITH_CHANGE |
| ↳ B-1 | Work 역링크 계약 모순 수용; 개인 Knowledge origin 우선 | ACCEPT | - |
| ↳ M-1 | Workflow 쓰기 방지는 검증된 실제 경계 필요 | ACCEPT | - |
| ↳ M-2 | 공통 Git writer 경합 직렬화 및 CAS | ACCEPT | - |
| ↳ M-3 | 그룹 구조 변경은 충돌·보류 후 재승인 | ACCEPT | - |
| ↳ M-4 | Exporter 보존 회귀 T01/T02 필수 | ACCEPT | - |
| ↳ m-1 | 전체 commit SHA와 파일별 revision 단위 명시 | ACCEPT | - |
| ↳ m-2 | 개인 복구 최대 3회, 그룹 재게시 0 | ACCEPT | - |
| [REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-WORK-KNOWLEDGE-GUARD-CODE-R1-20261117/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | READY_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | GPT_NOT_OBSERVED | NOT_VERIFIED |
| ↳ B1 | Path containment 알고리즘이 구체화되지 않음 (R10, T09/T10/T16/T31 관련) | NOT_ADJUDICATED | - |
| ↳ B2 | 전체 기본공개 전환에 따른 콘텐츠 내부 비밀 탐지가 한 줄 서술로만 존재 (R24) | NOT_ADJUDICATED | - |
| ↳ B3 | MSC HTML sandbox의 "별도 origin"이 구현 수준에서 정의되지 않음 (R08/R09, T29) | NOT_ADJUDICATED | - |
| ↳ T31 | /R10 수용 기준에 구체적 path-canonicalization 알고리즘(realpath + commonpath + TOCTOU 대응) 명문화. | NOT_ADJUDICATED | - |
| ↳ T12 | /R24 수용 기준에 비밀 스캔 실패 시 fail-closed 원칙과 룰셋 소유자를 명시. | NOT_ADJUDICATED | - |
| ↳ T29 | /R08 수용 기준에 origin 분리의 구현 방식(서브도메인 vs 쿠키 scope)을 양자택일로 확정하도록 명시. | NOT_ADJUDICATED | - |
| [REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-WORKSPACE-WIKI-UI-UX-R1-20261119/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | GPT_NOT_OBSERVED | NOT_VERIFIED |

비차단 지적도 GPT 판정 기록 전에는 해결 처리하지 않습니다.
