# 업무 GPT → 기존 Linux Viewer 현장 연동 인계

2026-11-19 KST · UI v0.1.0 · development_not_for_deployment

## 1. 목표와 입력

새 UI를 다시 설계하지 말고, 이 패키지의 팀 위키 화면과 탐색 동작을 기존 Linux **별도 Viewer 서비스**에 최소 변경으로 연결해 주세요. 기존 서비스의 로그인·renderer·읽기 API를 먼저 재사용해요.

- 입력 ZIP: `l1-workspace-wiki-ui_v0_1_0_1119.zip`
- 압축 해제 후 기준: `viewer-wiki-ui/INTEGRATION.md`, `DESIGN.md`, `TEST_REPORT.md`, `manifest.sha256`
- 대상 구현 저장소·브랜치·서비스·원본 revision: **NOT_VERIFIED**. G0에서 실제 값을 확인해 현장 Work에 기록. 이름·API·포트·절대 경로를 추정하지 않아요.
- 이 패키지에 협업 서비스 접속·인증 의존성은 없어요. 수신한 로컬 파일만으로 UI 검토 가능해요.
- UI 데이터·인물·Work ID·revision·MSC는 전부 합성. 실제 자료와 혼합하지 않아요.

## 2. 한 번의 현장 읽기 조사 G0

기존 업무 Work와 유효한 호스트 권한 범위에서 다음을 한 번에 확인해 주세요. 이미 유효하게 확인된 근거는 재사용해요.

| 실제 확인 대상 | 기록할 결과 | 이번 패키지가 가정하지 않는 것 |
|---|---|---|
| 서비스 소스/프레임워크 | 저장소·브랜치·commit·실제 UI 진입 경로 | 새 웹 서비스 설치 |
| 인증/권한 | 현재 계정·service identity·읽기 권한 | 로그인 방식·동료 공유 가능성 |
| 전체 파일 탐색 | root·children 조회·ID·pagination·파일 형식·오류 | 임의 filesystem API |
| 문서 렌더 | 기존 Markdown·HTML/SVG·JSON·이미지·PDF handler | 새 sanitizer·converter 필수 개발 |
| Work·Knowledge | 실제 Module/Feature/Scenario·Procedure·Work/Evidence 관계 | fixture DTO를 영구 스키마로 채택 |
| 상태/메타 | 원천값·revision·검증·게시 근거·미확인 처리 | UNKNOWN을 PUBLISHED/PASS로 추정 |
| 검색 | 허용된 대상·최신화·캐시·제한 정보 검사 | 전체 본문 검색 지원 |
| MSC | 기존 B형 원본·별도 origin·sandbox·CSP·asset 정책 | 같은 origin HTML 직접 실행 |
| 보안/복구 | 아래 B1~B3·원본 SHA·백업/rollback·유효 승인 | UI 시험을 공유 승인으로 사용 |

## 3. adapter 매핑표

아래 함수는 **프런트엔드 예시 계약**이에요. 실 API URL·HTTP method·응답 필드의 정본이 아니에요. 기존 API를 읽기 범위에서 연결하거나 기존 서비스 컴포넌트로 이식해요.

| UI 메서드 | 필요 의미 | 현장 매핑·검증 |
|---|---|---|
| `listRoots(view)` | work/knowledge/files 진입 노드 | 실제 root·권한·조회 범위·pagination 확인 |
| `listChildren(nodeId)` | 하위 노드와 문서 ID | opaque ID 사용, 서버 root containment·크기/재귀 제한 |
| `getDocument(docId)` | 제목·종류·본문/원문·관련 문서 ID | 기존 safe renderer 우선, payload limit·MIME 검증 |
| `getDocumentMeta(docId)` | Work·경로·revision·검증·게시 표시값 | Updater/Kernel 원천을 읽기 매핑; 모르는 값은 null |
| `getMscTarget(docId)` | 기존 B형 MSC 연결 정보 | B3 검증 전 비활성; 임의 URL·srcdoc 삽입 금지 |
| `getSummary(docId)` | 관련 문서 카드의 제목/종류 | 동일 문서 접근권한 유지 |
| `search(query)` | 지원하는 범위의 검색 결과 | scope 표시를 실 지원 범위로 변경; 권한·최신화 확인 |

상태 어댑터는 실제 원천의 의미를 명시적으로 매핑해요. PUBLISHED는 검증된 게시 근거와 고정 revision이 있을 때만 표시해요. 현재의 `PUBLISHED · 예시`, `fixture-r1`, `합성 데모`, 검색 범위 표기는 실제 연동·시험 완료 후에만 현장 값으로 변경해요. 지원이 없는 기능은 버튼과 안내를 해당 상태로 표시해요.

개인 Knowledge 메타정보·그룹 선별 변환/승인 게시·readback/고정 revision 역링크는 Knowledge Updater 책임. Viewer 적용을 이유로 Workflow/Kernel/Updater/doc-converter·원본 Work/Evidence·그룹 정본을 수정하지 않아요.

## 4. 좁은 구현 순서

1. 실제 소스 revision·대상 저장소·브랜치·변경 파일과 기존 유효 승인을 기록하고 현 UI/asset·원본 SHA·권한을 보존해요.
2. 프레임워크 없는 기존 서비스면 HTML/CSS/JS를 정적 asset으로 이식. 기존 프레임워크면 레이아웃·디자인 토큰·읽기 동작만 컴포넌트에 이식해요.
3. adapter 한 곳에 실제 읽기 API를 연결. cookie/token을 JS/URL/파일에 새로 저장하지 않아요. 현재 CSP `connect-src 'none'`은 데모 전용이므로, 기존 승인된 인증·origin 계약에 맞는 최소 서버 헤더 정책으로 조정하고 시험해요. 임의 `*` 허용 금지.
4. 기존 Markdown renderer·문서 링크 mapper·형식별 handler를 연결. 원본 링크나 문서를 일괄 변경하지 않아요. 데모의 `doc:` 링크는 실제 설치 포맷이 아니므로 기존 링크 resolver로 교체해요.
5. 실제 B형 MSC는 원문·참가자·phase 의미를 보존하는 기존 핸들러에 연결. 프런트엔드 합성 SVG를 실제 renderer로 배포하지 않아요.
6. `fixtures/`, `tests/`, 합성 데이터와 standalone 데모를 업무 서비스 제공 경로에서 제외. 실제 접근권한과 동일한 검색·관련 문서·raw/download 권한을 적용해요.
7. 승인 범위 내 격리 시험 후에만 실제 UI 전환. 범위 밖 서비스 재시작·설치·공유는 개별 BLOCKED로 두고 가능한 개발·시험을 완료해요.

## 5. 실제 호스트 필수 게이트

| Gate | 부정 시험·수락 근거 | 현재 |
|---|---|---|
| B1 | canonical root 내부 여부, `../`·encoded/absolute·symlink/hardlink·NFC/case·TOCTOU·숨김/비밀 경로 fail-closed | NOT_VERIFIED / BLOCKING |
| B2 | 파일내용 embedded secret·제한자료, raw·검색·캐시·download까지 같은 차단 | NOT_VERIFIED / BLOCKING |
| B3 | MSC HTML 별도 origin, 인증 쿠키/토큰 접근 불가, 제한 sandbox/CSP·asset·외부요청 정책 | NOT_VERIFIED / BLOCKING |
| E3 | 기존 Linux localhost·권한·문서/원문·MSC·원본 SHA 불변·rollback | NOT_RUN |
| E4 | 유효한 공유 승인, 동료 2계정의 읽기만·동일한 허용 범위, 검색·deep link·원본 보호 | NOT_RUN |
| U01/U02 | 실제 담당자의 5초 진입 인지·이슈→MSC 3회 이내 주요 조작 | NOT_RUN |
| U03/U08 | 1440/390/320·긴 표/코드·200%·키보드·실기기, 접근성 확인 | 합성 일부 PASS; 현장 NOT_RUN |
| U05 | 실제 doc-converter B형 6/12 participant·긴 phase·확대·접기·복귀, 원문 불변 | 합성 placeholder만 PASS; 실제 NOT_RUN |

이 게이트 충족 전 동료 공유·운영 배포를 PASS로 표시하지 않아요. 신규 유료 독립 리뷰·PUBLIC 전송은 별도 유효 승인에 따라 판정해요.

## 6. 현장 결과와 rollback

허용된 업무 Work에 원본 revision·변경 파일·매핑표·시험·한계·rollback 위치를 기록해 주세요. 기존 writer와 데이터는 유지하며, UI asset/entry와 adapter만 보존본으로 복원할 수 있어야 해요. source/Evidence/Knowledge SHA가 바뀌었다면 원인을 확인하기 전 전환을 중단해요.

회신은 허용된 비민감 요약만 사용해요:

`G0=PASS/FAIL | API=REUSE/CONNECT/GAP/UNKNOWN | B1/B2/B3=PASS/FAIL/NOT_RUN | E3/E4=PASS/FAIL/NOT_RUN | UI=PASS/FAIL | 원본변경=0/확인필요 | 다음=연동/시험/승인대기`

민감 코드·로그·실제 MSC·호스트 절대 경로·토큰은 전달하지 않아요. 실제 저장소/브랜치/인계 파일 경로는 현장 실행 지시에 반드시 확정해서 넣고, 미확인이면 추측하지 않고 해당 단계만 차단해요.
