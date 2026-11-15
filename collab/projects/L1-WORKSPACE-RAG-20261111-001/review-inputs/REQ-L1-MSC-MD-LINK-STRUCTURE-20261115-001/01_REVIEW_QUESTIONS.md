# 독립 구조 리뷰 질문 — R01~R10

| ID | 판단할 관계와 반례 |
|---|---|
| R01 | Workflow와 Updater 둘 다 같은 Work에 저장/갱신할 수 있나요? Updater가 저장할 때 전체 Workflow를 다시 실행하게 만들거나, converter가 별도 writer/원장을 갖게 하는 모순이 있나요? |
| R02 | code-analyzer의 사실·source revision·AS-IS/TO-BE·msc_ref/원본과 converter의 표현 책임이 분명한가요? 변경 없는 분석을 재실행하거나 추정 흐름을 코드 사실로 승격하는 경로가 있나요? |
| R03 | 기존 msc-package/일반 HTML 변환/msc-export를 재사용하는 B 뷰어 보완이 최소 범위인가요? 실제 SVG viewBox·단계 근거 없는 입력, 여러 MSC, 렌더러 없음에서 가상 Phase나 잘못된 완료 링크가 생길 수 있나요? |
| R04 | F2의 Kernel 복사 확장자·Evidence 이름 변경 해석이 정확한가요? 기존 bundle/export/writer 재사용으로 해결되는 부분과 실제로 필요한 최소 확장이 분리됐나요? 상대 경로 변경·등록·원본 해시를 함께 보존할 수 있나요? |
| R05 | Workspace 원본 보존과 그룹 지식의 검증·Preview·유효 승인·게시 revision·독자 접근을 구분했나요? 읽기 전용 group-knowledge를 writer로 오인하거나, 개인 URL만 그룹 본문에 복사하는 경로가 남았나요? |
| R06 | 실제 Procedure/Feature·Scenario와 기존 본문 마커를 선택해 MSC 절만 갱신할 수 있나요? 수동 문서, 여러 MSC, 같은 입력 재게시, 잘못된 대상 선택에서 중복·덮어쓰기·섞인 revision을 막을 책임이 명확한가요? |
| R07 | 원본 생성·렌더·게시·브라우저 표시·Work 역링크의 각 실패를 구분하나요? 일부 자산만 게시, MD 게시 실패, 그룹 게시 성공 후 Work 연결 실패, 불확실 실행에서 전체 재분석·중복 게시 없이 복구할 수 있나요? |
| R08 | F1~F5 중 코드 발췌로 입증된 사실과 G1 제안·미확인 업무 설치 기능이 정확히 나뉘나요? 공개 baseline을 최신 설치/개발 후보로 오인하거나 UI 샘플 PASS를 자동 변환·업무 E2E PASS로 승격한 부분이 있나요? |
| R09 | 대상 독자의 실제 HTML 열람 주소·호스트 SVG/스크립트 허용 정책·접근권한을 기존 기능으로 확인할 수 있나요? HTML 파일 화면/raw 링크를 뷰어로 착각하거나, 호스트가 HTML을 못 보여줄 때 무의미한 링크만 남기는 부분이 있나요? 새 호스팅은 기본 해법으로 요구하지 마세요. |
| R10 | 설치 I/O 좁은 확인 → converter 보완 → 기존 writer/본문 경로 연결 → 두 진입 → 한 실제 사례 순서가 타당한가요? 두 진입 × 두 목적지의 완료 기준과 실패 기준이 충분한가요? 더 적은 변경으로 사용자 경험을 만족하는 대안이 있으면 근거와 함께 제안해주세요. |

각 행은 `수용 / 수정 수용 / 거절 / 보류 / 추가 확인`과 짧은 근거로 판정해주세요. 핵심 지적은 BLOCKING/MAJOR/MINOR 최대 6개로 묶고, “미접근”만을 결함으로 분류하지 마세요. 요청한 구조 리뷰 안에서 가정을 반박하거나 더 단순한 구조를 제안해도 돼요.

실행·산출물 확인 수준: `INDEPENDENT_REVIEW`는 실제 결과/receipt 이후 판정하고, `HOST_VALIDATOR`, `AUTO_GENERATED_VIEWER_E2E`, `BUSINESS_WORKSPACE_GROUP_PUBLISH_E2E`는 실행 근거 없으면 `NOT_RUN/NOT_VERIFIED`로 유지해요. GPT의 사전 정적 검토와 이번 독립 리뷰를 구분해주세요.
