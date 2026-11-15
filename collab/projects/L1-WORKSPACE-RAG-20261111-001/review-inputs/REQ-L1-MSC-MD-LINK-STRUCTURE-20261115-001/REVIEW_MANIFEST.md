# MSC·MD 링크 독립 구조 리뷰 — 고정 입력 manifest

- Request: `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001`, revision 1 / Work `L1-WORKSPACE-RAG-20261111-001`
- 입력 문서 원문 기준: PRIVATE commit `b3f207728867ad9fad5d06d0ad8d3ff244106b06`.
- 공개 코드 발췌 기준: PUBLIC L1Work commit `41d151e54651cc030e6ef66c94a7d62f654aec2b`; 원본 ZIP 및 개별 파일 SHA는 ZIP의 `06_BASELINE_PROVENANCE.json`에 고정했어요.
- 입력 ZIP: `collab/packages/msc-md-link-structure_r0001_1115_REVIEW_INPUT.zip` / **38132 B**
- SHA-256: `90bb61a0e7c3b429942c620480ad9a079980d2a3432b72cea8ba80a4b915907d`
- Git blob: `34744b9fe1b2fe7bfe3b49961b807fec4ab62a9c`
- 압축 전: 89240 B / 텍스트 8개. 설치/배포 패키지가 아니에요.
- 검사: 원문 Git blob/바이트 동일성, ZIP CRC·경로·일반파일 PASS; 토큰/개인키 패턴 발견 0. 공개 도구 코드 발췌·일반 설계·합성 샘플 범위만 포함해요.
- `HOST_VALIDATOR=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, 실제 모델 호출 0. GPT 패키징 검사를 호스트 validator나 독립 리뷰로 취급하지 않아요.

| 파일 | bytes | SHA-256 |
|---|---:|---|
| 00_README.md | 3378 | `256820525b791d96ed79e780edc5ba3ae6ad9da873d9594c53966e76b28334f1` |
| 01_REVIEW_QUESTIONS.md | 3618 | `8c1848d57b1218797bd8c509a90459b57aa68c7b148c72a55c5cf823b4243790` |
| 02_PROPOSAL.md | 18401 | `b4f64584c0edf48921f77c0930b520e438b14d6299dd8aa49da5f9ef86ee290a` |
| 03_SOURCE_EVIDENCE.md | 33648 | `281dc8562f4ddb06906d724c035dad1b0dd809f9e473990560b9a3ce537e3cc0` |
| 04_ACCEPTED_TWO_ENTRY_FLOW.md | 9372 | `2e4f186ae4868a63132fb337027341fd7b30a32474ead6f4bfa0e63934fac43f` |
| 05_SAMPLE_VERIFICATION_RESULT.md | 7720 | `ebcd009811a6ff7cae3c0d3c0417005802d737b50bbb5bc71ec2192b5ff5ee73` |
| 06_BASELINE_PROVENANCE.json | 6512 | `27d33e5e0673c10cdb09720dd5a34d74338861f7d9c700a791f4e9d7925e431d` |
| 07_WORKSPACE_VIEW_STRUCTURE.md | 6591 | `47efe75530ff172697cc3d35457b9f0f18a234c5bfe9168131f6084dc1e7bfc7` |

REQUEST·ZIP을 Commit A에 게시·원격 검증한 뒤 Commit B의 SOURCE_PIN으로 고정해요. 승인·READY·호스트 실행 상태는 실제 산출물로만 확인해요. 이전 동결 Work→Knowledge 요청을 대체하거나 그 승인/영수증을 재사용하지 않아요.
