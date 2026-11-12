# CoWork GitHub SHADOW 대시보드

> **MIGRATION_NOT_CUTOVER** — 운영은 Dropbox LIVE 유지. GitHub 데이터만 표시합니다.

이 문서는 GitHub Actions가 생성하는 안내 화면이며 리뷰·설치·배포 승인이나 자동 실행 결과가 아닙니다.

- 문서가 있는 프로젝트: **4개**
- GitHub REQUEST 파일 관측: **0개** (검증 안 됨)
- GitHub REVIEW 파일 관측: **0개** (검증 안 됨)
- GitHub RECEIPT 파일 관측: **0개** (검증 안 됨)

## 협업 흐름과 상태 · 역할 기준

**협업 관리 환경** — GPT · GitHub / **업무 실행 환경** — Windows 감시기 · Claude Code

```mermaid
flowchart TB
  subgraph LIVE["현재 운영 경로 · 변경 없음"]
    L1["GPT 요구·판정"] --> L2["기존 LIVE 운송"]
    L2 --> L3["Windows 감시기 / Claude Code"]
    L3 --> L4["결과·영수증 / GPT"]
  end
  subgraph NEXT["GitHub 목표 경로 · 정식 전환 전"]
    A["GPT 요구·범위 확정"] --> B["GitHub PRIVATE / REQUEST·READY"]
    B --> C["Windows watcher / 승인·신뢰 검증"]
    C --> D["Claude Code / 독립 리뷰"]
    D --> E["GitHub PRIVATE / 리뷰·영수증"]
    E --> F["GPT / 판정·피드백"]
    F --> G["GitHub Actions / 대시보드"]
  end
  L4 -. "필수 게이트 및 별도 LIVE 승인 이후" .-> A
```

> 화살표는 설계된 경로입니다. Windows 실행·서명 검증·독립 리뷰의 PASS를 뜻하지 않습니다.

### 운영·검증 상태

| 구분 | 현재 상태 | 근거 범위 |
|---|---|---|
| 현재 운영 경로 | **기존 LIVE 유지 (문서 기준)** | GitHub 정식 전환과 별개 |
| GitHub 전환 | **정식 전환 전** | 별도 명시적 승인 전 전환 금지 |
| Windows 실행·SHADOW | **기록 미관측** | 실제 호스트 실행 증거 필요 |
| Claude Code 독립 리뷰 | **미실행** | 자체 시험과 구분 |
| GitHub 요청·결과·영수증 | **요청 0 · 결과 0 · 영수증 0** | PRIVATE 파일 관측 수일 뿐 완료 건수가 아님 |
| 공개 샘플 웹페이지 | **기록 미관측** | L1Work의 샘플만 PUBLIC, 실제 협업 현황 비공개 |

[전환·Windows 원문](../projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) · [대시보드 원문](../projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md)


### 프로젝트별 상태 원문

| 프로젝트 | 문서상 상태 | 근거 |
|---|---|---|
| COWORK-DROPBOX-TO-GITHUB-MIGRATION | 전환 전 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/CURRENT.md) |
| COWORK-GITHUB-DASHBOARD-20261111-001 | 전환 전 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/COWORK-GITHUB-DASHBOARD-20261111-001/CURRENT.md) |
| JOBLIST-NRTX-20261112-001 | 상태 확인 필요 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md) |
| L1-WORKSPACE-RAG-20261111-001 | 문서상 진행 | [CURRENT.md](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md) |

미이관 파일이나 승인·서명 검증 결과가 없어도, 이 화면은 이를 임의로 성공/0건 완료 처리하지 않습니다.

## GitHub 리뷰·GPT 판정 연결

문서 연결은 승인 서명·운영 실행 검증이 아닙니다.

| 요청 | Work | 단계 | GPT 판정 |
|---|---|---|---|
| 미이관 | - | 미확인 | - |

비차단 지적도 GPT 판정 기록 전에는 해결 처리하지 않습니다.
