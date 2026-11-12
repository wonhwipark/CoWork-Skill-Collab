# CoWork Work Tracker V1 — 병렬 스킬별 진행 상태 계약

기준: 2026-11-12 KST · PRIVATE main · Pages 기본 디자인: Executive

## 목적과 사용 예시

- 서로 다른 스킬을 병렬 개발/검토하더라도 **각각 고유한 Work ID**로 진행 단계·담당·개발자 자체시험·독립 리뷰·다음 행동을 추적.
- 예시: `l1-fix-workflow` 및 `l1-github`가 동시에 진행한다면, 각각 **서로 다른 `work_id`**와 최신 `CURRENT.md` 근거를 사용. 실제로 등록된 증거가 없으므로 현재 두 스킬을 진행 중이라고 보고하지 않는다.
- 한 작업에 여러 스킬이 포함되면 1개 프로젝트 폴더에 복수 `works`를 등록 가능. 서로 독립 업무면 `collab/projects/<WORK_ID>/` 각각 개별 폴더.
- GPT가 작업을 생성/수정할 때 등록 파일을 함께 게시하는 것이 기본. **사용자에게 매번 수작업을 요구하지 않는다.**

## 저장소·정확한 경로

- PRIVATE: `wonhwipark/CoWork-Skill-Collab` / `main`
- 근거: `collab/projects/<WORK_ID>/CURRENT.md` (운영 실행 근거, 변경·미완료 이력)
- 추적 메타데이터: `collab/projects/<WORK_ID>/TRACKER.json`
- 엔진: `collab/dashboard/work_tracker.py`, `generate.py`
- 자동 생성: `collab/dashboard/state.json` / `index.html` / `VIEW.md` / `SUMMARY.md`
- GitHub Action: `.github/workflows/cowork-dashboard.yml` (CURRENT.md 및 TRACKER.json 변경 자동 갱신, PRIVATE 쓰기만)
- 공개 기본 화면: `https://wonhwipark.github.io/L1Work/cowork-dashboard/` (허용 범위만 포함한 별도 수동 검증 스냅샷)

## TRACKER.json 형식 (개념 예시, 실제 작업 등록 아님)

```json
{
  "schema": "COWORK_WORK_TRACKER_V1",
  "works": [
    {
      "work_id": "EXAMPLE-FIX-001",
      "skill": "l1-fix-workflow",
      "title": "Workflow 기능 보완",
      "phase": "DEVELOPMENT",
      "owner": "GPT",
      "self_test": "NOT_RUN",
      "independent_review": "NOT_RUN",
      "next_action": "코드 변경·회귀시험 근거 확인"
    },
    {
      "work_id": "EXAMPLE-GITHUB-002",
      "skill": "l1-github",
      "title": "Repository 작업 개선",
      "phase": "REVIEW",
      "owner": "Claude Code",
      "self_test": "PASS",
      "independent_review": "PENDING",
      "next_action": "서명된 리뷰 결과·영수증 확인"
    }
  ]
}
```

**위 값은 테스트 시나리오이며 실제 작업 상태가 아닙니다.** 특히 `self_test=PASS`는 개발자 자기 신고값이며, 독립 리뷰 PASS나 배포 승인이 아님.

## 상태 스키마와 검증

| 필드 | 허용 값 | 주의 |
|---|---|---|
| `work_id` | 영문·숫자·`_`·`-` 고유값 | 전체 프로젝트에 걸쳐 중복 거부 |
| `skill` | 소문자/숫자/하이픈/언더바 | 기술명 표시, 사용자 데이터 기재 금지 |
| `phase` | `REQUIREMENT / DEVELOPMENT / REVIEW / DISPOSITION / COMPLETE / BLOCKED / UNKNOWN` | **문서 신고 위치**이지 검증된 완료율이 아님 |
| `owner` | 담당 주체 또는 역할 | 개인 정보·로그/경로 기재 금지 |
| `self_test` | `PASS / FAIL / SKIP / NOT_RUN / NOT_VERIFIED` | 개발자 자체 시험과 독립 리뷰 분리 |
| `independent_review` | `PASS / FAIL / PENDING / NOT_RUN / NOT_VERIFIED` | 독립 리뷰 영수증/정합성 검증이 없으면 PASS로 판정 금지 |
| `next_action` | 간략한 다음 조치 | 우회·운영 승인 지시 작성 금지 |

- `TRACKER.json`이 없으면 각 `CURRENT.md`당 1개 Work 카드를 자동 생성하되 **담당 미등록·단계 UNKNOWN**으로 보수적으로 표시.
- 잘못된 JSON/ID/중복/상태는 해당 등록을 **무시하고 CURRENT만 표시**하거나 중복 충돌에서는 fail-closed; 다른 Work의 상태를 혼합하지 않는다.
- 단계별 진행 막대는 위치만 표시하며 증빙 없이 중간 단계를 PASS로 승격하지 않는다.
- GitHub PRIVATE 본문에서는 출처 `CURRENT.md` 링크를 확인. PRIVATE Action은 모델 리뷰를 호출하거나 Windows watcher를 변경하지 않는다.
- `CUTOVER=MIGRATION_NOT_CUTOVER`; LIVE 전환은 별도 승인 전 불변.

## PUBLIC Pages 표시 게이트

- PUBLIC은 Work ID, 정확한 내부 경로, 상세 승인 정책, 리뷰 원문 및 내부 피드백을 복제하지 않는다. 공개 허용된 **일반 작업 범주·상위 상태·다음 조치 요약**만 수동 검증 후 갱신.
- PUBLIC 프로젝트 작업 숫자/상태는 마지막 게시 시점의 스냅샷. PRIVATE 변경이 PUBLIC에 자동 동기화되는 것은 아니다.
- 공개 상태 자동 반영 시스템 구축은 보안·권한·비용·실행 승인 범위를 별도로 정의하고 사용자 명시 승인을 받아야 한다.

## 실제 시험 결과

- GitHub Actions [#43235494674](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/43235494674): PRIVATE Python 회귀 35 PASS, 공개 후보 보안 8 PASS.
- 서로 다른 스킬(`l1-fix-workflow`, `l1-github`)의 별도 Work ID·단계·시험·담당·다음 조치 분리와 중복 ID/불명 상태 거부, HTML 이스케이프, 반복 출력 결정성을 합성시험.
- 실제 Windows 호스트/Claude Code 독립 리뷰/운영 DB/LIVE 전환은 이 작업에서 시험·변경하지 않음.
