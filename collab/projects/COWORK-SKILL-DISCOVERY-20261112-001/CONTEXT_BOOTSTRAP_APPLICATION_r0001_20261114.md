# 새 창 통합 브리프 문서 적용 결과 — r0001

- 기준일: 2026-11-14 KST
- 사용자 승인: 기존 개선 검토안의 통합 브리프·고정 진입 문서 적용을 요청.
- 적용: collab/CONTEXT_BRIEF.md + README/AGENTS/START_HERE/baseline/카탈로그/기존 발견 절차의 같은 진입 연결. L1·Job CURRENT의 현재 요약 및 과거 후보/리뷰 상태 구분.
- 정본: 기존 계약·스킬 원문·프로젝트 CURRENT 유지. 브리프는 source blob을 가진 읽기용 파생 요약.
- 유지보수: 원문 변경 작업에서 관련 요약·출처·확인일을 함께 갱신하거나 확인 필요로 표시. 별도 DB·자동 생성기·모델 호출 없음.
- 문서/서식/신규 상대 링크 검증: PASS.
- 브리프 UTF-8 크기: 11290 bytes (목표 상한 12,288 이내) — PASS.
- source blob: 10개 비교 PASS. 같은 게시에서 바꾼 4개는 최종 문서 bytes로 계산.
- 카탈로그 18+별도1, 총 19개 스킬이 브리프 기능 묶음에 모두 포함 — PASS.
- 요청별 8개 경로의 존재/연결 정적 확인 — PASS. 실제 새 대화의 동작/정확도 시험이 아님.
- CURRENT 첫 요약 3개·기존 TRACKER schema/상태 보존 — PASS.
- 신규 표기·과거 원문/이력 보존 확인 — PASS.
- INDEPENDENT_REVIEW / REAL_NEW_CHAT_E2E / HOST_API_TEST: NOT_RUN.
- 프로젝트 설정·백그라운드 로더·운영/Job/스킬 코드·PUBLIC 신규 자료·LIVE 변경 없음.
- 아래 해시는 게시 전 문서 bytes의 SHA-256. 실제 commit·원격 전체 readback은 게시 후 별도 확인하며 이 결과를 설치/API PASS로 올리지 않음. 이 결과 파일 자신의 hash/commit은 자기 참조로 선기록하지 않음.

| 문서 | bytes | SHA-256 |
|---|---:|---|
| `AGENTS.md` | 2336 | `be9183ac3361abb5adcb8026805595ef89e6489fefb9384d0caa3af04757c1ab` |
| `README.md` | 4746 | `e2a664e1afe2e6b2cf38560237c51bc5c7f796cd64455a29474c579eb1a936c0` |
| `collab/START_HERE.md` | 15582 | `45af4b6825142329b8056ee62cbfc48ebf44e32dc2c56e9178c81344885ce273` |
| `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md` | 6316 | `41c541af8e7ccf35ff2ece551140579e81a60a4813e494ccfcd68370373857bc` |
| `collab/knowledge/OPERATING_BASELINE.md` | 4689 | `026ea0ee1eeb0dec01e30947a54e0b19eff4949a2de461de4324a939bb421ef2` |
| `collab/knowledge/SKILL_CAPABILITY_CATALOG.md` | 7765 | `659566bf640c0bf44408e35396da2481ec60ed245730aadec61e0de362933cd0` |
| `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` | 50722 | `a3a5a0011b2a67090a0ff909985cf715881a153a0c6238100b6ca940329295b2` |
| `collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md` | 31006 | `5a35b6aae9067ee699935ffc6f4c200d608afe189ea34731a4a4b50431a5f895` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md` | 9556 | `20bd13d115df0baf768829ae6633dcfce1a38796e57fde89fbb6679f0a1f2661` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/TRACKER.json` | 464 | `29c36c821cb74147e79ec2156816f9a9aeb6da7bef9f1178f78fe3b41bc10d5c` |
| `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/NEW_CHAT_CONTEXT_BOOTSTRAP_REVIEW_r0001_20261114.md` | 13001 | `5649c890610f73538319f99b1e8e77d254d4ed6e8d13bf76ccf65fdc98e4d8e5` |
| `collab/CONTEXT_BRIEF.md` | 11290 | `364cb519a33a02504c48c69fb63754066bac7c3e55f269075d44d387bca75f6d` |

다음 한 동작: 실제 새 창에서 PRIVATE wonhwipark/CoWork-Skill-Collab main의 collab/CONTEXT_BRIEF.md부터 읽도록 요청하고 관련 CURRENT로 이어간다. 이후 원문 변경 시 관련 요약만 유지보수한다.
