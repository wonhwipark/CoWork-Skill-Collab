# L1 Channel Recovery — Viewer/Kernel 개발용 ZIP 공개 전달 결과 r0001

- 2026-11-24 KST / 기존 Work L1-WORKSPACE-RAG-20261111-001
- 저장소: GitHub PUBLIC wonhwipark/L1Work / branch main
- PUBLIC commit: 9eeda1cc674b4453f6637da2a60bb12a61f8c445
- 공개 범위: 비민감 스킬 코드·합성 Fixture/테스트·설계/인계. 업무 코드·로그·상세 MSC 없음.

## 1. 공개 게시 및 원격 확인

| 산출물 | 경로 | bytes | SHA-256 / Git blob | 판정 |
|---|---|---:|---|---|
| Viewer v0.5.3 전체 ZIP | l1-workspace-viewer-wiki-integrated_v0_5_3_1124.zip | 399,993 | SHA-256 9fe5d6cce9ac7064152099e183cdeee21421a0cefe9044ce48d39db686b67411; Git d71ba9d53f4040d0d90a980750365c9503671a3c | POSTED/READBACK_PASS |
| Kernel v0.7.47 전체 ZIP | work-ledger-kernel_v0_7_47_1124.zip | 406,507 | SHA-256 5c1f73a09b2cd8c4ec93134f387ed7f80cec799b534f2d044978b66e6c38b20c; Git ea7158d581955ec9f54f35e7d1490d2ae92f1bf7 | POSTED/READBACK_PASS |
| 업무 GPT 단일 인계 | handoffs/L1_CHANNEL_RECOVERY_VIEWER_KERNEL_CONVERTER_COMPLETE_HANDOFF_r0001_20261124_KST.md | UTF-8 MD | Git 0e59d629ef4e12bebd8080f3d2975ef104536e0c | POSTED/READBACK_PASS |
| handoffs 인덱스 | handoffs/README.md | UTF-8 MD | Git a37a429f7b92aeb2f93477790bb8997e271c302b | POSTED/READBACK_PASS |

출처 원본 SHA 고정: Viewer v0.5.2 15e83f136fa10ef680619602b55d74c4cd4c0c86a6cc470c1bec9cac250239ba, Kernel Recovery v0.7.46 dabd412847354c77ca105da3ed686924f676f5f3c67428a2b984e68f2998076e, Viewer Write guard v0.7.43 9866ff7164884b0fb346bd31d37dbdf2013b5e5910e5857f8e35075624cf92f1.

## 2. 변경 내용

- Viewer: v0.5.2 기존 UI/Write/도우미 기능과 3개 Write 파일 SHA 보존, #/recovery 목록·상세·Work/MSC 열람 callback. HTML/SVG는 호스트 허용된 OpenArtifact/권한으로만 열고 임의 HTML/URL 삽입 없음. Edge 미확정 표시. standalone-preview와 CSP SHA 재생성.
- Kernel: Recovery v0.7.46 원본 SHA/Evidence/recovery_analysis 지원·기존 index/recovery.json을 보존하고 v0.7.43 viewer_write_guard/시험/문서 병합. 추가된 recovery_physical 모듈은 물리적 recovery/README.md, recovery/index.json, recovery/works/<work-id>/<Evidence ID>.md 파생 연결을 생성; 원본 분석은 Work/Evidence.
- Workflow: 동일 v1.6.75의 11/20 Recovery 후보와 11/21 Viewer Write 후보는 소스 충돌 위험. 이번에 수정하지 않음. 업무 G0에서 실제 활성본과 연결 gap 확인 후 별도 새 고유 버전 판단.
- l1-channel-recovery, doc-converter, 제품 코드, 실제 업무 설치본, 그룹 Knowledge는 수정하지 않음. 업무 GPT 책임인 Seed 전후/AS-IS·TO-BE MSC 생성 및 Edge 정의 요구는 HO에 명시.
- 개발 소스 및 합성시험: 같은 Work의 dev/recovery-v20261124/ 경로. 별도 Work 생성 없음.

## 3. 실제 시험과 증거

| 항목 | 결과 |
|---|---|
| 원본 ZIP 3종 실제 GitHub 바이트 SHA-256 비교 | PASS |
| Viewer v0.5.3 GitHub main 원격 SHA-256/바이트, ZIP 40/40 CRC, manifest 39/39 | PASS |
| Kernel v0.7.47 GitHub main 원격 SHA-256/바이트, ZIP 172/172 CRC, manifest 171/171 | PASS |
| Viewer 추가 JS 구문/Recovery 식별·형식/변조를 거부하는 격리 단위 | PASS |
| Kernel 물리적 Recovery 모듈 격리 실행(파생 보기/멱등·경로 거부) | PASS (격리 원형, 패키지 전체 Python suite 아님) |
| 기존 Viewer 최신 Node 전체 regression/assistant-client/readability, 신규 recovery.cjs Node 전체 실행, Kernel 전체 Python unittest | NOT_RUN |
| 실제 Linux Viewer read adapter·writer·doc-converter HTML/SVG/PUML·Browser/권한·CSP E2E | NOT_RUN |
| Windows Claude Code 독립 코드 리뷰·업무 호스트 설치·운영 Write ON·제품 Recovery 효과 | NOT_RUN |

판정: **PUBLIC_DEVELOPMENT_PACKAGE_DELIVERY=PASS**, **HOST_DEPLOY=NOT_RUN**, **INDEPENDENT_REVIEW=NOT_RUN**, 개발 패키지는 development_not_for_deployment. 문서/ZIP 게시를 기술 분석 완료나 런타임 Recovery 성공으로 보고하지 않음.

## 4. 확인된 제약·다음 행동

- 원본 Seed CL/PR·실제 제품 code revision·Edge 의미/판정·doc-converter 실제 호출 출력·업무 Viewer host callback/ACL은 업무 GPT G0에서만 확인 가능.
- 기존 Workflow v1.6.75 source 충돌 해결은 자동 덮어쓰기 금지; 조회 후 입증된 gap만 조정.
- 사용자는 Viewer v0.5.3 + Kernel v0.7.47 두 ZIP을 업무 GPT에 전달하도록 요청했으며, 완결 HO r0001에 이전 Viewer v0.5.2 인계 전체를 부록으로 보존.
- **NEXT_ONE_ACTION:** 업무 GPT가 실제 업무 Work 하나에서 기존 완료 결과를 재사용하고 Seed 전후/후보 AS-IS/TO-BE MSC의 doc-converter 출력·Evidence readback→recovery/index.json→Viewer 그림 링크까지 순차 검증하고 비민감 상태만 회신.
