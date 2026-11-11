# CoWork 공개용 HTML 후보 — PRIVATE 검토 전용

**판정:** `DEVELOPMENT_CANDIDATE` / `DATA=SYNTHETIC_ONLY` / `PUBLICATION=NOT_APPROVED`

- 별도의 공개용 대시보드 화면을 구현했지만 **실제로 웹에 공개하지 않았습니다**.
- `build.py`는 정해진 샘플 문구만 사용합니다. `CURRENT.md`, REQUEST/READY, 리뷰, 영수증, GPT 판정, 파일 경로, 해시, 내부 통계 등 PRIVATE 운영 자료를 읽지 않습니다.
- `index.html`은 PRIVATE 저장소 안의 시험 후보이며 3개의 샘플 단계 카드만 보여줍니다. **실제 업무 진행 현황이 아닙니다.**
- `tests/test_public_preview.py`는 유출 방지, 결정성, 외부 요청/스크립트 차단 등을 시험합니다.
- `.github/workflows/cowork-dashboard.yml`의 PRIVATE Actions에서만 생성·검증·후보 커밋을 수행하도록 구성합니다. PUBLIC L1Work, GitHub Pages, CDN 및 외부 게시 경로는 사용하지 않습니다.
- 모바일·데스크톱 화면 시각 시험은 별도 로컬 Chromium에서 진행합니다.

## 실제 공개 전 별도 승인 게이트
1. 후보 **실제 HTML 전체 바이트와 SHA-256**, 포함 필드·민감정보 반출 적합성 확인.
2. 공개 URL/호스팅 방식·접근 권한·유효기간·운영 책임 및 롤백 계획 확인.
3. 사용자 명시적 **공개 콘텐츠 승인과 배포 승인**을 별도 수령.
4. 승인된 정확한 바이트만 PUBLIC 경로로 전달. 미래의 생성물과 내부 데이터 자동 공개는 허용하지 않습니다.
5. 실제 데이터 공개가 필요해지면 새 허용 목록 기반 스키마와 별도 보안 검토를 설계합니다.

**금지:** PRIVATE `collab/dashboard/index.html` 또는 `state.json`을 그대로 PUBLIC에 복제하거나 GitHub Pages를 활성화하는 행위.
