# CoWork Actions 선택 자동화 중지 · 상태변경 시 직접 게시 r0001
- 2026-11-20 KST / 사용자 최신 승인: “위세가지 모두필요없어. 상태변경은 실제로 업로드하면됨”
- PRIMARY Work: `COWORK-GITHUB-DASHBOARD-20261111-001`; 관련 Work: `COWORK-SKILL-DISCOVERY-20261112-001`
- STATUS: **사용자 지시로 3개 불필요한 GitHub Actions 실행 경로 중지.** 대상: `.github/workflows/cowork-dashboard.yml`, `cowork-public-status-sync.yml`, `cowork-skill-release-quality.yml`.
- 실행 이력·원본 YAML: Git commit history에 보존. 삭제된 workflow 파일 자체는 이후 자동/수동 실행 트리거로 사용할 수 없음. 이 조치는 기존 Windows Claude Code Watcher, GitHub reviews/requests/receipts 보호 검증, `joblist-*`, 일회성 PEC·ACE staging, CoWork public preview 별도 workflow, L1Work Pages 정적 게시에는 영향을 주지 않음.

## 앞으로의 기본 처리
1. **PRIVATE 상태 변경**은 Work의 `CURRENT.md` 최신 요약·근거·다음 행동만 직접 GitHub PRIVATE `main` 게시하고 원격 본문 및 Git blob 검증. 기존 결과·영수증 및 TRACKER와 필요한 필드만 동기화. 단순 문서 게시·GPT 투두 갱신은 Actions를 호출하지 않음.
2. **PUBLIC 상태 변경이 실제 필요한 경우에만**, PRIVATE의 승인된 사실을 직접 확인한 뒤 기존 `public_sync.py` 승인된 공개 범주·고정 레이블·단계 검증 계약을 재사용해 **직접** `L1Work/main/docs/cowork-dashboard/status.json`을 게시. 반드시 허용목록·출처·현재 시점·데이터 범위 검증과 변경 전후 SHA/readback 실시. PUBLIC이 허용하지 않은 상세 WORK/receipt/민감 데이터·업무 회사 자료는 계속 차단. 인계/ZIP은 승인된 별도 경로만.
3. **스킬 코드를 변경해도 Actions 자동 시험 금지**. 개발자/GPT가 접근 가능한 환경의 자체시험, 승인된 업무 호스트 시험과 독립 리뷰는 원래 계약대로 각각 분리. 실제 시험을 수행하지 않았다면 NOT_RUN. 유료 리뷰·운영 설치·PUBLIC 배포는 별도 승인 경계 유지.
4. **업데이트가 없으면 아무 작업도 하지 않음**: 예약·주기 갱신·상태 timestamp만 올리는 별도 자동화/일괄 동기화 신설 금지. 실제 상태 변경 시 한 번 게시.
5. Windows Watcher LIVE/보호 자동승인과 호스트 운영, GPT의 새 창 맥락 조회, 로컬 PRIVATE 조회 스크립트 `context_query.py`는 계속 유지. 그러나 이 로컬 스크립트는 자동 실행 보장이나 실호스트 상태 확인이 아님.

## 주의 및 후속
- 현재 L1Work PUBLIC `status.json`은 과거 GitHub 상태(2026-11-20 09:23:06Z). 자동 동기화가 더 이상 없으므로, 새 호스트 근거와 공개 레이블을 정합하게 **수동 게시한 뒤**만 LIVE로 표시 가능. 코드의 오래된 JSON 지연 경고는 수동 이벤트 중심 운영과 별개로 현재에는 보수적으로 동작하며, 변경 없는 기간이 30분을 넘으면 계속 표시될 수 있음.
- 다음 한 동작: 실제 상태 변경(예: v0.2.29 GitHub LIVE 호스트 보고)을 PUBLIC 허용목록으로 수동 반영할 때 검증된 공개본을 만든 뒤 정확한 파일만 직접 업로드. 또한 30분 주기 지연 경고는 이벤트 기반 운용에 맞춰 차기 PUBLIC UI 변경 때 수정.
- 해당 3개 workflow 제거/중지는 비용 승인·계정 Billing 변경이 아니다. 예전 실패/정산과 무료 사용량 정보는 그대로 보존. 추가 GitHub Actions 실행을 유도하지 않음.
