# MSC·MD 링크 구조 리뷰 — Commit A 게시 검증 영수증

- Request: `REQ-L1-MSC-MD-LINK-STRUCTURE-20261115-001`, revision 1 / 같은 Work `L1-WORKSPACE-RAG-20261111-001`.
- PRIVATE `wonhwipark/CoWork-Skill-Collab/main`, Commit A `013b9f26fde91c3bcc87374952f64a61111c5a69`.
- GPT 직접 확인: 요청·접수 원샷·상태·manifest·고정 입력 문서 8개, 합계 텍스트 **12개**, 원격 내용과 실제 Git blob SHA-1 재계산 일치.
- ZIP: `collab/packages/msc-md-link-structure_r0001_1115_REVIEW_INPUT.zip`, **38132 B**, SHA-256 `90bb61a0e7c3b429942c620480ad9a079980d2a3432b72cea8ba80a4b915907d`, Git blob `34744b9fe1b2fe7bfe3b49961b807fec4ab62a9c`.
- 원격 `fetch_file(encoding=base64)`에서 받아 실제 bytes를 다시 디코딩한 SHA-256/크기/Git blob·ZIP CRC·8개 멤버 SHA/크기 **PASS**. 로컬만 해시한 결과가 아니에요.
- 입력 원문 4개는 PRIVATE `b3f207728867ad9fad5d06d0ad8d3ff244106b06`의 Git blob과 바이트 일치. 발췌 9개 소스 파일은 PUBLIC snapshot의 4개 ZIP 출처/파일 SHA와 범위를 입력에 기록했어요.
- 비민감 일반 제안·공개 도구 코드·합성 샘플만 포함. 토큰/개인키 패턴 발견 0. ZIP 경로 이탈/일반파일 검사는 PASS.
- SOURCE_PIN은 후속 Commit B에서 이 Commit A와 repo ID `1451933830`를 고정해요. REQUEST/ZIP은 다시 쓰지 않아요. READY/승인 서명은 게시하지 않았어요.
- `HOST_VALIDATOR=NOT_RUN`, `INDEPENDENT_REVIEW=NOT_RUN`, `MODEL_CALLS=0`. 게시 검증은 실제 Windows 접수/Claude 실행/영수증/업무 저장·그룹 게시 검증이 아니에요.
- 이전 동결 Work→Knowledge 요청과 기존 승인·후보·결과 이력은 보존했어요. 이번 요청의 독립 리뷰 결과는 별도 result/receipt에서 확인해요.

| 파일 | bytes | 원격 실제 내용 SHA-256 |
|---|---:|---|
| REQUEST.md | 5747 | `850f7ec185acfeea51356b0f60b0f49cb1564b8a98756c93c5ba5c7b2b3c5693` |
| HOST_SUBMIT_ONESHOT.md | 3690 | `2eecb9ac9acbeaff68cb7a39c6776607bd046985a409cc1f83ab6206f7e3f459` |
| SUBMISSION_STATUS.json | 2029 | `8316f41a9a83cbdb6a1dbb1ad76ec393f952bde64dcd28d16b960d68ae165b45` |
| REVIEW_MANIFEST.md | 2300 | `ee9e547188be973c3ec99676bcc3301e809644f38ac6a1a0835180dd47550698` |
| 00_README.md | 3378 | `256820525b791d96ed79e780edc5ba3ae6ad9da873d9594c53966e76b28334f1` |
| 01_REVIEW_QUESTIONS.md | 3618 | `8c1848d57b1218797bd8c509a90459b57aa68c7b148c72a55c5cf823b4243790` |
| 02_PROPOSAL.md | 18401 | `b4f64584c0edf48921f77c0930b520e438b14d6299dd8aa49da5f9ef86ee290a` |
| 03_SOURCE_EVIDENCE.md | 33648 | `281dc8562f4ddb06906d724c035dad1b0dd809f9e473990560b9a3ce537e3cc0` |
| 04_ACCEPTED_TWO_ENTRY_FLOW.md | 9372 | `2e4f186ae4868a63132fb337027341fd7b30a32474ead6f4bfa0e63934fac43f` |
| 05_SAMPLE_VERIFICATION_RESULT.md | 7720 | `ebcd009811a6ff7cae3c0d3c0417005802d737b50bbb5bc71ec2192b5ff5ee73` |
| 06_BASELINE_PROVENANCE.json | 6512 | `27d33e5e0673c10cdb09720dd5a34d74338861f7d9c700a791f4e9d7925e431d` |
| 07_WORKSPACE_VIEW_STRUCTURE.md | 6591 | `47efe75530ff172697cc3d35457b9f0f18a234c5bfe9168131f6084dc1e7bfc7` |

다음 한 행동: [HOST_SUBMIT_ONESHOT.md](HOST_SUBMIT_ONESHOT.md)의 정확한 PRIVATE/main/요청 경로로 호스트가 현재 권한·중복·validator를 확인하고 허용된 리뷰 1회 또는 차단 이유를 게시해요.
