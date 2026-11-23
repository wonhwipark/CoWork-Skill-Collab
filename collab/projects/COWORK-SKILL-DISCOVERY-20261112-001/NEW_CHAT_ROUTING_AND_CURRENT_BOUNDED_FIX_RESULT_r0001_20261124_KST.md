# CoWork 새 대화 Work 라우팅·CURRENT 읽기 보완 결과 r0001

- 작성: 2026-11-24 KST
- 작업 Work: `COWORK-SKILL-DISCOVERY-20261112-001` (기존 Work 재사용)
- 입력 평가: 사용자 제공 `COWORK_MULTI_AGENT_NEW_CHAT_ASSESSMENT_r0001_20261123_2358_KST.md` (평가 기준 `6b9f3faa405fff859e5ea6e6c287e5fdbe84f68a`)
- 실제 변경 전 HEAD: `6fb0472bc926135a06bb53b33c95fe5acf755972` (평가 뒤 2개 커밋은 다른 Work의 CURRENT)
- 저장소: `wonhwipark/CoWork-Skill-Collab`, `main`, 실제 `visibility=PUBLIC` 확인

## 1. 피드백 판정·수정

| 평가 제안 | 판정 | 조치 |
|---|---|---|
| PRIVATE/PUBLIC·상대 링크 불일치 | 수용 | 최신 PUBLIC 운영 사실을 브리프와 시작 계약에 정합화; `collab/collab/...` 오경로 복원; PUBLIC이라고 해서 제한자료·인증정보 허용하지 않음 |
| 312,413B CURRENT에서 요약 실패 | 수정 수용 | 오로지 CURRENT만 1MiB 상한(기존 요청/증거 256KB 유지), bounded 48 H2 질문별 선별·3600자 반환·신뢰 경고·원격 원문 링크 제공 |
| 6종 키워드로 Viewer/NR Job/Smoke 오분류 | 수용 | 기존 10개 Work에 대해 11개 topic(Viewer는 Knowledge와 동일 Work) 지원, 강한 구별 규칙 우선, 다중 후보/폴백 경고 유지 |
| 전용 스킬·새 원장 추가 | 거절 | 기존 `collab/dashboard/context_query.py` 최소 보완 및 같은 Work에 결과 보존 |
| ChatGPT 프로젝트 설정 자동 변경 | 추가 확인 | GitHub 파일 수정과 별개. 프로젝트 지침 r0002의 PRIVATE 표현은 사용자 설정에서 직접 변경해야 실제 반영 |

## 2. 소스·문서·정확한 원격 위치

| 파일 | Git blob SHA-1 | SHA-256 (원격 전체 본문 계산) |
|---|---|---|
| [조회기](../../dashboard/context_query.py) | `0182e8a75879e0f154a008cd6fdb3e85a9f36a1a` | `23fc2e7064a575a5d97557467a04ed9f511310e397929137fd5cf1ab8f203263` |
| [39개 시험 원본](../../dashboard/tests/test_context_query.py) | `9b00129000c5a793682e758b3156cf1410e3871f` | `ea15b38ec837ff848c660a62caf041fba8d7244779a7b16c97a1d3ded2b89b9a` |
| [공통 맥락 브리프](../../CONTEXT_BRIEF.md) | `6644fef032e3bd26e336e5eac2feed1fb7d944c1` | `042b90db4b7a844d517a3d91f854fade0bdaf30279a7c7163022da132daa2f50` |
| [스킬 발견 시작 계약](../../ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md) | `19b304e2c072da7b9efd92baad48a64d8b62afe1` | `b3ea399d7fd252dc9e8ff2148f52e30880b27a9248be6316a1b785db49da3e72` |

게시 커밋: 소스 변경 `740bf7e540ca883544ca4c922773eba5edc1ca99`, 소스 설명 `8b0c1b0b41f8f75d756ba1980fe4224ef32915e6`, 시험 `ddb6b12933b64a70b3f03d2bbd15e6889e7b415f`, 브리프 `878144496d6bf1555d7c982f02164b13c528e7dd`, 시작 계약 `b6b3bc6ef7a99f09ab52b92acf10dc546e383fc1`. GitHub readback 전체 본문과 blob 확인.

## 3. 실제 시험 구분

| 시험·확인 | 결과 | 상세 |
|---|---|---|
| 수정된 라우팅 핵심 코드의 독립 격리 Python 재현 | PASS | 11/11 사례, 문서 구간 선택 합성 2/2; Python 3.13.5 해당 추출 코드 `py_compile` PASS |
| 원격 실제 L1 Workspace CURRENT로 선택 함수 재현 | PASS (동일 알고리즘 재현) | Git blob `dbdb5364410757580d5620c44d977194d7161a06`, 312,413 bytes. Viewer 질문은 H2 index=1, Updater 야간 질문은 H2 index=2를 선택 |
| 원격 변경 코드·시험·브리프·계약 readback | PASS | Git blob 및 전체 본문 SHA-256 대조 |
| 게시본 전체 Python `py_compile`, 39건 unittest | **NOT_RUN** | GitHub 연결을 통해 파일 쓰기·읽기는 가능했으나 이번 샌드박스에서 전체 원격 파일을 Python 실행 컨테이너로 가져오는 경로가 차단됨 |
| 실제 312,413B CURRENT를 사용하는 게시본 `snapshot()` | **NOT_RUN** | 동등한 선택 로직·실제 원문 대조는 PASS, Python 종단 직접 호출은 미검증 |
| Windows Claude 새 세션 import / 독립 리뷰 / 업무 Linux·RAG·LIVE E2E | **NOT_RUN** | 문서·보조 조회기 변경으로 설치/실행 완료 주장 금지 |

## 4. 적용 경계·ChatGPT 프로젝트 설정 수정 권고

- **CoWork `PUBLIC` 유지.** 사용자 2026-11-23 지시를 실제 저장소 공개 속성으로 확인. 공개 범위 내 비민감 협업 조회기/문서/시험만 변경. 금지 대상: 키/토큰/회사 제한 C++ 원문/상세 MSC/로그/고객자료.
- **프로젝트 설정 수동 정합화 필요:** 현재 대화에 주입된 프로젝트 운영 지침 r0002의 `정본 저장소: GitHub PRIVATE`를 `정본 저장소: GitHub PUBLIC wonhwipark/CoWork-Skill-Collab, main; 공개 범위는 허용된 비민감 협업 자료만`로 교체. 본문의 `CoWork PRIVATE 게시`는 `CoWork PUBLIC main에 승인된 비민감 자료만 게시`로 교체. 신규 공개 자료·민감정보·LIVE·유료 호출의 별도 승인 경계는 그대로. 오래된 PRIVATE 기록은 당시 이력으로 보존. GitHub 게시만으로 ChatGPT 프로젝트 설정 변경을 **완료했다고 보고하지 않음**.
- REQUEST/APPROVAL/READY·영수증·가격 정책·watcher/DB/Telegram·운영 Windows/Linux·스킬 ZIP·L1Work 공개 배포는 모두 **미변경**.

## 5. 다음 한 행동

**Windows Claude Code 또는 원격 파일을 실행 환경으로 가져올 수 있는 허용된 호스트에서** `wonhwipark/CoWork-Skill-Collab/main` 최신 정본의 `collab/dashboard/context_query.py`와 `collab/dashboard/tests/test_context_query.py`를 읽어 `python -m py_compile` 및 `python -m unittest discover -s collab/dashboard/tests -p test_context_query.py -v`를 실행하고, 실제 312,413B `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`를 대상으로 Viewer·Updater `snapshot()` 두 사례를 확인. 실패가 있으면 같은 Work에서 최소 수정 후 재시험. 기존 완료된 P1/P2 R1 독립 리뷰는 재실행하지 않음.
