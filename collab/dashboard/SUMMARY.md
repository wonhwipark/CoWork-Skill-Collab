# CoWork GitHub SHADOW 대시보드

> **MIGRATION_NOT_CUTOVER** — GitHub 리뷰 제공자 (문서 기록). GitHub 기록과 리뷰 실행은 별개입니다.

이 문서는 GitHub Actions가 생성하는 안내 화면이며 리뷰·설치·배포 승인이나 자동 실행 결과가 아닙니다.

- 문서가 있는 프로젝트: **10개**
- GitHub REQUEST 파일 관측: **6개** (검증 안 됨)
- GitHub REVIEW 파일 관측: **4개** (검증 안 됨)
- GitHub RECEIPT 파일 관측: **4개** (검증 안 됨)

## 협업 흐름과 상태 · 역할 기준

**협업 관리 환경** — GPT · GitHub / **업무 실행 환경** — Windows 감시기 · Claude Code

```mermaid
flowchart TB
  subgraph LIVE["현재 리뷰 제공자 기록 미확인"]
    L1["최신 CURRENT.md 확인"] --> L2["운영 근거 검증 필요"]
  end
  subgraph NEXT["GitHub 목표 경로 · 정식 전환 전"]
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
| 현재 운영 경로 | **GitHub 리뷰 제공자 (문서 기록)** | 최신 이관 CURRENT 기록 · 실제 호스트는 별도 검증 |
| GitHub 전환 | **원문 확인 필요** | 별도 명시적 승인 전 전환 금지 |
| Windows 실행·SHADOW | **기록 미관측** | 실제 호스트 실행 증거 필요 |
| Claude Code 독립 리뷰 | **기록 미관측** | 자체 시험과 구분 |
| GitHub 요청·결과·영수증 | **요청 6 · 결과 4 · 영수증 4** | PRIVATE 파일 관측 수일 뿐 완료 건수가 아님 |
| 공개 Work 대시보드 | **기록 미관측** | L1Work에 승인된 비식별 상태만 자동 요약 · PRIVATE 원문은 비공개 |

[전환·Windows 원문](../projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) · [대시보드 원문](../projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md)


## 작업별 진행 현황 · 독립 Work Tracker

각 Work는 고유 ID로 구분. 단계/시험/리뷰 표시는 문서 신고값이며 실제 완료 검증이 아닙니다.

| Work ID | 스킬 | 진행 단계(신고) | 담당 | 시험(신고) | 독립 리뷰(신고) | 다음 조치 |
|---|---|---|---|---|---|---|
| [COWORK-AUTO-APPROVAL-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md) | cowork-review-watcher | 차단·보류 | GPT / Windows Claude Code | PASS | NOT_RUN | 2026-11-15 GPT DIRECT STATIC: v0.2.21 candidate actual ZIP 272839B SHA256 16921bf4021714345cabc78de5e2e8a6882891615f90b5747622570ca4465d8b verified; Windows SELF_TES |
| [COWORK-DROPBOX-TO-GITHUB-MIGRATION](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) | cowork-review-watcher | 완료 신고 (검증 필요) | GPT / Claude Code | PASS | PASS | 2026-11-15 GPT 최종 판정 ACCEPT_GITHUB_LIVE_CUTOVER_HOST_REPORTED_AND_REVIEW_VERIFIED. Windows 결과 v0.2.20 R1 독립 리뷰 BLOCKING 0, 모델 1회 $0.3769412(한도 $1), B1 cryptography,  |
| [COWORK-GITHUB-DASHBOARD-20261111-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md) | cowork-dashboard | 독립 리뷰 | GPT | PASS | PENDING | 발표용 개선 설계 독립 리뷰 요청 등록; Windows 호스트가 이번 요청 비용 권한·서명 확인 후 READY 게시. 실제 모델 리뷰 미실행. |
| [COWORK-SKILL-DISCOVERY-20261112-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md) | skill-discovery | GPT 판정 | GPT | PASS | NOT_RUN | 통합 설계 TODO D01~D08 변경안·영향 파일과 D09 검증 계획을 묶어서 검토; D10 실제 분석 검증은 후속 |
| [ISSUE-ANALYZER-20261114-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/ISSUE-ANALYZER-20261114-001/CURRENT.md) | issue-analyzer | 차단·보류 | GPT | NOT_VERIFIED | NOT_RUN | 전체 회귀·독립 리뷰 후 L1Work PUBLIC 루트에 ZIP 게시 및 SHA 원격 재검증 |
| [JOBLIST-NRTX-20261112-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md) | job-list | 개발·시험 | GPT | PASS | NOT_RUN | 호스트 G0 확인 전 후보 패키지 검증 범위 유지 |
| [JOBLIST-SMOKE-20261114-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-SMOKE-20261114-001/CURRENT.md) | 미지정 | 단계 미확인 | 미등록 | NOT_VERIFIED | NOT_VERIFIED | CURRENT.md 최신 상태 및 다음 담당 확인 |
| [L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001/CURRENT.md) | l1-knowledge-updater | 독립 리뷰 | GPT | PASS | NOT_RUN | v0.9 215행 담당자 검토; 실제 ID·산출물 검증은 첫 승인된 분석 후속 |
| [L1-WORKSPACE-RAG-20261111-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) | 미지정 | 단계 미확인 | 미등록 | NOT_VERIFIED | NOT_VERIFIED | CURRENT.md 최신 상태 및 다음 담당 확인 |
| [NR-L1TX-CODE-ANALYSIS-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md) | 미지정 | 단계 미확인 | 미등록 | NOT_VERIFIED | NOT_VERIFIED | CURRENT.md 최신 상태 및 다음 담당 확인 |

스킬별 병렬 작업은 각 프로젝트의 TRACKER.json으로 등록합니다. 등록 전에는 확인되지 않은 실제 진행률을 추정하지 않습니다.


### 프로젝트별 상태 원문

| 프로젝트 | 문서상 상태 | 근거 |
|---|---|---|
| COWORK-AUTO-APPROVAL-20261115-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-AUTO-APPROVAL-20261115-001/CURRENT.md) |
| COWORK-DROPBOX-TO-GITHUB-MIGRATION | 문서상 진행 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) |
| COWORK-GITHUB-DASHBOARD-20261111-001 | 전환 전 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md) |
| COWORK-SKILL-DISCOVERY-20261112-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md) |
| ISSUE-ANALYZER-20261114-001 | 상태 확인 필요 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/ISSUE-ANALYZER-20261114-001/CURRENT.md) |
| JOBLIST-NRTX-20261112-001 | 문서상 진행 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md) |
| JOBLIST-SMOKE-20261114-001 | 상태 확인 필요 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-SMOKE-20261114-001/CURRENT.md) |
| L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001 | 상태 확인 필요 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-CHANNEL-KNOWLEDGE-SCOPE-20261113-001/CURRENT.md) |
| L1-WORKSPACE-RAG-20261111-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) |
| NR-L1TX-CODE-ANALYSIS-20261115-001 | 검증 진행 중 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md) |

미이관 파일이나 승인·서명 검증 결과가 없어도, 이 화면은 이를 임의로 성공/0건 완료 처리하지 않습니다.

## GitHub 리뷰·GPT 판정 연결

문서 연결은 승인 서명·운영 실행 검증이 아닙니다.

| 요청 | Work | 단계 | GPT 판정 |
|---|---|---|---|
| [REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-DASHBOARD-PRESENTATION-20261115-001/REQUEST.md) | COWORK-GITHUB-DASHBOARD-20261111-001 | READY_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-V0214-R1-20261114](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0214-R1-20261114/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-V0217-R2-20261114](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0217-R2-20261114/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-V0219-R2-20261114](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0219-R2-20261114/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-COWORK-V0220-R1-20261115](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-COWORK-V0220-R1-20261115/REQUEST.md) | COWORK-DROPBOX-TO-GITHUB-MIGRATION | GPT_NOT_OBSERVED | NOT_VERIFIED |
| [REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-WORK-KNOWLEDGE-DESIGN-20261115-001/REQUEST.md) | L1-WORKSPACE-RAG-20261111-001 | READY_NOT_OBSERVED | NOT_VERIFIED |

비차단 지적도 GPT 판정 기록 전에는 해결 처리하지 않습니다.
