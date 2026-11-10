# CLAUDE CUTOVER READINESS 보충: C-4 Dropbox 실샘플 B-6 대조 결과 2026-11-10

- 대상: CLAUDE_CUTOVER_READINESS_RESULT_FOR_GPT_20261110.md (커밋 0b95968a)의 C-4 항목. 이 문서가 해당 항목을 대체하며 기존 문서는 수정하지 않음.
- 증거 수준: SELF_TEST_REPORTED. 정식 독립 리뷰가 아님. INDEPENDENT_REVIEW=NOT_RUN.
- 수행 방식: 운영 감시기(v0.1.5)의 전송 계층 코드로 Dropbox를 읽기 전용 접근. 호출은 목록 조회와 다운로드뿐이며 업로드·삭제·이동 없음. 자격 증명은 전송 계층 내부에서만 사용되고 출력되지 않음. 출력은 개수와 참/거짓뿐이며 요청 ID, 파일명, 내용은 출력·게시하지 않음.
- 모델 호출 0회. 운영 변경 없음.

## 결과 (C-4: PASS(REAL, 읽기 전용))
| 항목 | 값 |
|---|---|
| 목록에서 확인한 요청 폴더 | 65 |
| REQUEST·READY가 각각 정확히 1개인 쌍 (대조 대상) | 63 |
| 쌍이 아닌 폴더 | 2 (REQUEST 또는 READY가 없거나 중복) |
| 원본 바이트 SHA-256 = 재인코딩 SHA-256 | 63 / 63 |
| READY가 선언한 request_sha256 = 원본 바이트 SHA-256 | 63 / 63 |
| READY가 선언한 request_sha256 = 재인코딩 SHA-256 | 63 / 63 |
| 어느 쪽과도 불일치 | 0 |
| REQUEST에 BOM | 0 |
| READY에 BOM | 0 |
| REQUEST에 CRLF | 0 |
| UTF-8이 아닌 REQUEST | 0 |
| REQUEST/READY와 비슷한 이름의 사이드카가 있는 폴더 | 0 |

## 판정에 미치는 영향
1. B-6: 실제 기존 Dropbox 요청 63쌍에서 원본 바이트 해시와 v0.1.5 방식(엄격 UTF-8 decode 후 encode) 해시가 모두 같고 READY 선언값과도 일치. 원본 바이트 기준 검증으로 바꿔도 기존 Dropbox 요청이 거부되지 않음. 이 표본에는 BOM과 CRLF가 없어 해당 경로는 실표본으로 검증되지 않았고, 합성 속성 시험(무작위 2,000건)으로만 근거를 가짐.
2. B-2: 정확한 basename 분류와 사이드카 차단이 영향을 주는 기존 폴더는 0개. 과거 요청이 새로 활성화되거나 재검출될 위험은 이 표본에서 관찰되지 않음.
3. 쌍이 아닌 폴더 2개의 내용·원인은 확인하지 않음. 이 중 하나가 운영 DB의 정산되지 않은 대기 요청 1건과 관련될 수 있으나 연결 여부는 미확인. 전환 전 reconcile 명령으로 대기 ID를 정산해야 한다는 기존 요건은 그대로 유효함.
4. 표본은 요청 폴더 전체 65개 중 63쌍이며, 상한(80쌍) 안에서 모두 조회함. 이후 신규 요청에는 적용되지 않음.

## 차단 요건 갱신
- C-4: 해소 (위 결과).
- 여전히 열린 요건: 운영 신뢰 루트 수명주기(B-7), 정산되지 않은 Dropbox 대기 요청 1건 처리, 호스트 SHADOW, 독립 리뷰와 영수증, 운영 DB의 실제 이행(백업·정지 시점·정산 선행), 사용자 명시 승인.

C4_STATUS: PASS_REAL_READONLY ; pairs_compared: 63 ; hash_mismatch: 0 ; legacy_sidecar_folders: 0 ; model_review_calls: 0 ; production_changed: false ; independent_review: NOT_RUN
