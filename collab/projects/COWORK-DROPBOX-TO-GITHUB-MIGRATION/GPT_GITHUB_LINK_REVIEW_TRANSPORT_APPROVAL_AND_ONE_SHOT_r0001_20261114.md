# CoWork / L1Work — GitHub 링크 기반 독립 리뷰 전달 승인 및 원샷 실행 계약
작성: 2026-11-14 KST | r0001
Repo: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab` | Branch: `main`
Exact path: `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/GPT_GITHUB_LINK_REVIEW_TRANSPORT_APPROVAL_AND_ONE_SHOT_r0001_20261114.md`
Status: **USER_AUTHORIZED_REVIEW_MATERIAL_TRANSFER / REVIEW_NOT_INVOKED / LIVE_NOT_APPROVED**

## 1. 사용자 명시 승인 — 이전 D2와 충돌 해소
2026-11-14 사용자가 **CoWork 감시기 자체 소스와 ZIP을 기존 Claude 독립 리뷰에 전달하는 것을 허용**하고, **L1Work의 스킬 및 Handoff MD 리뷰**도 허용. 전달 방식은 **GitHub에 리뷰 자료를 올린 뒤 정확한 파일 링크(저장소/branch/commit/path)를 Claude에게 제공**하는 것으로 결정.
- `CoWork watcher`에 대한 과거 `D=2 LOCAL_ONLY` 기본 제한은 **사용자가 지정한 CoWork 자체 작업물에 한해 리뷰 전송 허용으로 대체**. `COMPANY_L1_SOURCE`, 회사 업무용 제한 코드·로그·고객자료·인증 정보, 조직 정책상 제한된 파생자료에는 이 예외가 적용되지 않음.
- Windows Claude Code·Watcher PC는 회사 L1 업무 소스에 접속 불가(사용자 확인). 따라서 외부 Claude 독립 리뷰어를 자동으로 거부하기 위한 **온프레미스 로컬 LLM 확보·추가 서명자 PC 의무화는 이 일반 1인 협업의 필수 게이트가 아님**.
- **이번 승인에 포함된 것**: 검토 목적의 CoWork 자체 코드·시험·패키지 PRIVATE GitHub 게시 및 기존 Claude 독립 리뷰어에게 그 링크 공유, 기게시 L1Work PUBLIC 스킬/Handoff 내용에 대한 리뷰 요청 설계 및 링크 사용, 코드/문서의 범위/기밀 검증을 포함한 격리 준비.
- **이번 승인에 포함되지 않은 것**: 새 유료 Claude 리뷰 호출/추가 비용, signed REQUEST/READY 실제 게시, 미승인 후보의 L1Work PUBLIC 배포, LIVE watcher/Task/DB/Notifier/Token 설치·변경, 사내 호스트 실행·Skill-Updater 설치, 다른 사용자·조직 전체 자료 공개.

## 2. 경로별 역할 / GitHub 링크 선택
| 대상 | 리뷰 자료 경로 | 검증 및 배포 |
|---|---|---|
| **CoWork 감시기 자체 소스·후보 ZIP** | `wonhwipark/CoWork-Skill-Collab` **PRIVATE** `main`의 별도 `collab/projects/COWORK-DROPBOX-TO-GITHUB-MIGRATION/review-inputs/<review_id>/` 등으로 원본/검토 묶음 게시 | 실제 검토자에게 **PRIVATE repo 접근권**이 필요. 업로드 전에 스캔·바이트 SHA-256/크기·ZIP 경로/CRC 검증, GitHub 원격 재다운로드 원본 바이트·SHA 대조. 공개 저장소로 자동 복제 금지 |
| **L1Work 기존 승인된 PUBLIC ZIP** | `wonhwipark/L1Work` **PUBLIC** `main` 루트의 정확한 ZIP 파일 | 해당 **이미 공개된 버전**의 immutable commit pin URL 제공. 기존 ZIP 바이트/해시 검토 |
| **L1Work 공개 Handoff MD** | `wonhwipark/L1Work` **PUBLIC** `main/handoffs/`의 정확한 MD | 신규/갱신 공개 허용 문구 스캔 후 게시, commit pin 링크를 리뷰어에 제공. 게시가 실행·배포 승인 아님 |
| **미승인 스킬 후보 / 아직 공개되지 않은 Handoff** | PUBLIC 게시 금지. 검토용 비민감·게시 허용 후보만 `CoWork-Skill-Collab` **PRIVATE**에서 리뷰 | 리뷰 PASS·GPT 판정·실제 공개 승인 이후 최종 ZIP만 `L1Work/main` 루트로, Handoff MD는 `L1Work/main/handoffs/`로 각각 게시 |
| **회사 L1 코드·고객자료·토큰** | **업로드 금지**(PRIVATE/PUBLIC 모두) | 작업 PC 내부의 별도 도구/승인 절차를 따름 |

**링크 원칙**: `https://github.com/<owner>/<repo>/blob/<commit>/<path>` 고정 commit 파일 링크, 바이너리 ZIP에는 해당 원본을 내려받을 수 있는 GitHub 링크를 명시(정확 URL은 실제 원격 게시 후 조회해서 확보); reviewer에게 branch 이름·commit·상대 경로·SHA-256 및 크기 제공. 이전 리뷰 ZIP과 최신 ZIP 혼동 금지. 링크/파일 존재와 실제 리뷰 실행을 구별.

## 3. 기본 독립 리뷰 워크플로 — 사용자 1인, 반복 최소화
1. GPT: 요구·대상 ZIP/MD·변경파일·diff·기존 리뷰 지적·완료 기준을 한 번에 명시. `CURRENT.md`, `START_HERE.md` 최신 기준으로 old signer PC/온프레미스 reviewer 블로커 재도입 금지.
2. Windows Claude Code: **허용된 CoWork 소스만** 격리 후보 개발·자체 시험, 새 버전 ZIP 보존. 이미 검증한 500+ 전체 시험·로컬-only r0003/v2/ETW를 근거 없이 재실행하지 않음.
3. Windows Claude Code: 리뷰용 후보 ZIP·필요 소스·diff(회사 원본/토큰 없음)를 GitHub PRIVATE 리뷰 전용 경로에 게시. **실제 업로드 가능한 bytes**를 로컬 검사한 다음, GitHub에서 내려받은 원본 bytes SHA/크기/commit을 검증. 올릴 수 없는 자료는 `BLOCKED_NOT_POSTED`로 구분하고 게시했다고 주장 금지.
4. `REVIEW_MANIFEST.md`: reviewer에게 대상과 한도·고정 링크·SHA·선행 결과, 소스/패키지 범위·이전 지적·변경 diff, `DEVELOPMENT=SELF_TEST_REPORTED`, 독립 리뷰 요청 계획을 짧게 제공. **정책상 허용된 CoWork 자료이므로 review-inputs PRIVATE에 CoWork ZIP SHA/크기 기재 가능**, 회사 제한 코드는 금지.
5. 실제 **별도 Claude 독립 리뷰**는 개발 세션 자체 검토와 분리된 명시 리뷰 요청·입력·실행·결과·영수증으로 확인. 기존 Dropbox/GitHub watcher 정식 REQUEST/READY 계약 및 비용 상한을 **임의 우회하지 말 것**. 비용 있는 모델 호출은 승인한 모드/상한/요청에만 실행. 사용자가 링크를 허용한 것과 자동 유료 실행 승인 구분.
6. 리뷰 결과는 GitHub PRIVATE `reviews/<id>` 또는 기존 `collab/projects/.../` 계약에 따라 게시·readback, GPT가 `수용/수정 수용/거절/보류` 통합 판정. 재리뷰는 수정량과 별도 명시 요청이 있을 때만.
7. **배포**: 별도 승인·정식 게이트 통과 후에만 `wonhwipark/L1Work/main` **루트에 최종 스킬 ZIP**, `main/handoffs/`에 업무용 GPT/Agent 인계 MD를 게시하고 각각 별도 원격 바이트/commit 재조회. PRIVATE 검토 후보 게시는 업무 PC로 배송한 것이 아니며 PUBLIC 게시는 호스트 설치·Job 실행이 아님.

## 4. GitHub LINK 리뷰 시 손쉬운 메시지 형식
```text
[Claude 독립 리뷰 요청 — <WORK_ID>/<REVIEW_ID>]
대상 저장소: <PRIVATE CoWork-Skill-Collab 또는 PUBLIC L1Work>
고정 커밋: <exact SHA>
검토 파일: <repo-relative path와 확인된 GitHub URL>
ZIP 해시/크기: <실제 원격 검증값; 회사 제한 자료 제외>
참조: <CURRENT.md / REVIEW_MANIFEST.md>
검토 범위: <결함·호환성·회귀·보안·설계>
개발 세션 자체 시험: SELF_TEST_REPORTED
리뷰 실행 모드/비용 승인: <실제 승인된 값 또는 NOT_APPROVED>
요청: 별도 독립 리뷰로 수행하고 결과·영수증을 PRIVATE에 게시, 원격 readback.
```
URL이 실제로 생성되지 않았으면 추정/가상 URL을 쓰지 않는다. GitHub 링크는 **리뷰 자료 전달 경로**이고, 자체로 모델 호출/자동 리뷰 시작 신호는 아니다.

## 5. 다음 Windows Claude Code 한 번의 작업 (준비 범위, 운영 변경 금지)
- 최신 v0.2.13 로컬 후보와 과거 자체시험 결과를 확인하고 **CoWork 검토 자료 범위·민감정보/회사 코드 미포함 정적 검증**부터 실시.
- review-inputs 새 리뷰 ID 하나를 잡아 필요 소스·ZIP·짧은 manifest를 GitHub PRIVATE `main`에 **이미 허용된 자료에 한하여** 게시하고 실제 원본 원격 SHA·commit readback. 제품 전체를 무조건 PUBLIC에 올리지 말 것.
- ZIP 업로드에 연결된 도구/권한/환경이 막히면 **해당 부분만** `BLOCKED_UPLOAD`, 나머지 manifest/설계/최소 delta 리뷰 입력 준비. 전송 실패 때문에 모델 호출을 해선 안 됨.
- 기존 Claude 독립 리뷰 실행 인터페이스(비용/서명/요청 승인)를 1회 확인해, 사용자에게 다음에 승인할 **리뷰 실행·비용 한도만** 명확하게 제시. 이 단계에서 유료 리뷰/READY/운영 watcher 시작은 하지 않음.
- CoWork 코드에 대한 허용된 리뷰 전송과 L1Work PUBLIC handoff 리뷰는 서로 다른 work/review ID로 관리. 기존 공개 스킬은 실제 L1Work 소스 commit 링크만 사용.
- 한 번의 통합 결과 `CLAUDE_GITHUB_LINK_REVIEW_INPUT_READY_FOR_GPT_20261114.md`를 PRIVATE main에 게시하고 해당 작업 `CURRENT.md`/`TRACKER.json`에 반영, 모두 원격 재조회.
- 다음 단계로부터 LIVE를 목표로 할 때는 **독립 리뷰 실제 PASS/필요 delta 수정·시험, 중복방지·비용 통제 및 단일 LIVE/기존 요청 보존·롤백**을 검증한 후 최종 명시 승인. 기존 서명/정식 transport 계약을 새 문서만으로 자동 변경하지 않음.

## 6. 상태 및 판정
`USER_APPROVAL=REVIEW_MATERIAL_TRANSFER_AUTHORIZED`
`COWORK_SOURCE_ZIP_GITHUB_PRIVATE_UPLOAD=AUTHORIZED_SUBJECT_TO_CONTENT_CHECK`
`L1WORK_PUBLIC_APPROVED_SKILL_AND_HANDOFF_REVIEW=AUTHORIZED`
`ONPREM_REVIEWER_MANDATORY=NO_FOR_APPROVED_COWORK_CODE`
`NEW_PAID_REVIEW=NOT_AUTHORIZED`
`REVIEW_INPUT_UPLOAD=NOT_RUN`
`INDEPENDENT_REVIEW=NOT_RUN`
`ACTIVE_PROVIDER=NONE`
`MIGRATION_NOT_CUTOVER`
