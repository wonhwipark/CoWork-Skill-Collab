# CoWork PUBLIC Pages 자동 상태 갱신 — 연결·권한·검증 인계

기준: 2026-11-12 KST / PRIVATE `wonhwipark/CoWork-Skill-Collab` / PUBLIC `wonhwipark/L1Work`

## 목표 · 기본 경로

**기본 HTML 주소:** https://wonhwipark.github.io/L1Work/cowork-dashboard/

```text
[CoWork PRIVATE]
CURRENT.md / TRACKER.json
        │
        ▼
CoWork PRIVATE dashboard Actions (시험·상태 JSON 갱신)
        │  성공한 실행에 한해서만
        ▼
PUBLIC status exporter (재생성·증거 정합성 검사)
        │  고정 허용목록: 비식별 상위 5개 범주 + 이미 공개된 스킬명 2개
        ▼
[승인된 PUBLIC 쓰기 토큰 유무?]
        ├── 없음 → BLOCKED_MISSING_SECRET / PUBLIC 쓰기 0
        └── 있음 → L1Work/main/docs/cowork-dashboard/status.json 단일 파일 PUT
                       │
                       ▼
                   GitHub API 원격 readback / payload 일치 확인
                       │
                       ▼
                   GitHub Pages 자동 배포
                       │
                       ▼
                   Executive index.html + same-origin status.js
                   (PUBLIC status.json 로드, 카드·지표 동적 갱신)
```

## 설치 전 필수 1회 사용자 작업

1. GitHub 계정 **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**. *Resource owner*: `wonhwipark`. *Repository access*: **Only select repositories** → **`L1Work` 한 개만 선택**. *Repository permissions*: **Contents = Read and write**, 그 밖의 권한은 가능한 모두 No access (Metadata Read는 GitHub 기본). 만료 기간은 조직 정책에 맞춰 설정·주기적으로 갱신.
2. 토큰을 **절대로 대화창이나 GitHub 파일·로그에 입력하지 말고**, PRIVATE 저장소의 [Actions Secrets 설정](https://github.com/wonhwipark/CoWork-Skill-Collab/settings/secrets/actions)에서 **New repository secret**으로 등록. 이름 **`COWORK_PUBLIC_DASHBOARD_WRITE_TOKEN`**. Secret 값에 새 토큰을 입력.
3. 등록 직후 PRIVATE 저장소 [Actions](https://github.com/wonhwipark/CoWork-Skill-Collab/actions)에서 **`CoWork PUBLIC Pages status sync (allowlist only)` → Run workflow (main)** 실행. 또는 다음 `CURRENT.md`/`TRACKER.json` 갱신 시 자동 실행 대기. 첫 게시 전 `prepare`의 정책·시험이 PASS여야 함.
4. Actions의 `PUBLIC_SYNC=POSTED_READBACK_PASS` 또는 `PUBLIC_SYNC=UNCHANGED`를 확인한 뒤 PUBLIC `L1Work`의 Pages 배포가 SUCCESS인지 확인하고 위 HTML 링크 클릭. TOKEN이 없으면 `BLOCKED_MISSING_SECRET`이고, 공개 파일은 기존 스냅샷 상태 그대로 유지.

**주의:** Fine-grained token은 GitHub 정책상 저장소 **전체 Contents 쓰기 권한**을 갖습니다. 특정 `status.json` 한 파일만으로 권한 자체를 한정할 수 없습니다. 구현 코드·출력 경로를 단일 파일로 고정했고 PRIVATE repo secrets에만 저장하지만 이 계정 권한 위험은 남습니다. 더 강한 분리가 필요하면 별도 PUBLIC 대시보드 전용 저장소를 사용하는 방안을 승인 후 설계해야 합니다.

## 구현 및 계약

- PRIVATE exporter: `collab/dashboard/public_sync.py`.
- PRIVATE 자동 Action: `.github/workflows/cowork-public-status-sync.yml` (기존 대시보드 Action SUCCESS의 `workflow_run`, 같은 저장소 `main`; 수동 `workflow_dispatch` 지원).
- PRIVATE 회귀시험: `collab/dashboard/tests/test_public_sync.py` (합성·무네트워크).
- PUBLIC page: `wonhwipark/L1Work` `docs/cowork-dashboard/index.html`, `status.js`, `status.json`. 공개 Pages는 JSON 갱신 시 자동 재배포, 브라우저는 same-origin JSON만 로드. PRIVATE API를 브라우저에서 직접 호출하지 않음.
- **PUBLIC 내용 허용:** 일반 업무 범주명·고정 담당 역할·미검증 구분이 붙은 phase/status·합계 개수·기준일. `l1-fix-workflow`, `l1-github`는 기존 공개 예시로 이미 명시된 스킬명으로서, 실제 PRIVATE Work가 등록된 경우에만 공개 카드로 표시.
- **PUBLIC 차단:** PRIVATE 원문, Work ID, 고객/개인정보, ZIP·SHA, 검토 결과 본문, 비용/키, 로그/로컬 절대경로, 내부 next_action/free-text/사용자·파트원 이름. 새로운 스킬명은 허용목록 갱신과 별도 공개 범위 승인이 없으면 PUBLIC에 나오지 않음.
- **상태 주의:** `TRACKER.json` 자체시험 `PASS` 또는 독립 리뷰 `PASS`는 검증된 운영 완료로 승격되지 않음. 공개 화면은 `자체시험 기록·별도 검증` / `독립 리뷰 증거 미검증` 등으로만 표시.
- **Fail-closed:** `state.json`이 실제 CURRENT/TRACKER를 재생성한 값과 일치하지 않거나 스키마·전환상태·개수 이상·출력 경로 불일치 시 공개 발행 중단. 토큰 없음/HTTP 오류는 추가 모델 호출이나 무제한 재시도 없이 그 실행만 차단.
- 기존 `MIGRATION_NOT_CUTOVER` 상태, Dropbox LIVE, Windows watcher, 운영 DB/예약 작업, 모델 리뷰 실행과 **무관한 공개 화면 갱신 자동화**만 다룹니다.
- Token rotation: 토큰 만료 전에 새로운 토큰 발급→동일 Secret 값을 갱신→동일 Action 수동 재실행→상태 확인. 사고 시 토큰 폐기/Secret 비활성화 후 PUBLIC 이력 검토.

## 배포 상태 판정

- `SOURCE_GENERATOR`, `PUBLIC_CLIENT`, `PUBLIC_STATUS_BOOTSTRAP`, `WORKFLOW_POLICY`, `SECRET_CONFIGURED`, `AUTO_PUBLISH_E2E`, `PAGES_DEPLOY`, `PUBLIC_HTTP`는 **독립적으로 기록**.
- README/운영 문서 게시 또는 Actions 워크플로 파일 생성 자체가 Secret 설치·자동 게시 성공을 뜻하지 않습니다.
- `AUTO_PUBLISH_E2E=PASS`는 인증 후 실제 `PUBLIC_SYNC=POSTED_READBACK_PASS`와 Pages 배포 SUCCESS를 확인한 경우에만 부여합니다.
