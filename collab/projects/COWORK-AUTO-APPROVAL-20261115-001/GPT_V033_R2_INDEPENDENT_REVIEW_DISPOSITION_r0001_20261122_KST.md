# v0.2.33 r2 독립 리뷰 결과·GPT 실물 보완 판정
기준: 2026-11-22 KST / wonhwipark/CoWork-Skill-Collab / main
Work: COWORK-AUTO-APPROVAL-20261115-001

**INDEPENDENT_REVIEW=COMPLETED, BLOCKING=0. GPT_DISPOSITION=HOLD_FOR_CORRECTIONS, LIVE_READY=NO.**
독립 리뷰는 도착했고 정상 완료됐다. 이후 GPT가 공개된 동일 ZIP을 직접 검사해 발견한 아래 보완 사항은 독립 리뷰어의 지적과 구별한다. 동결 r2·기존 승인·READY·결과·영수증은 수정하거나 재실행하지 않는다.

## 1. 고정 입력·디스패치 확인

- 요청: `REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122` rev1, cowork-review-watcher, STATIC_ONLY, POLICY-STATIC-V1.
- Commit A(REQUEST+ZIP): `dbcfccac2d8552e9aa536a8ffd61671b6488ff40`.
- SOURCE_PIN Commit B: `9e8175a3c6f135be778eaffe065ae2d3027959be`, repo_id는 문자열 `"1451933830"`, A를 가리킴.
- APPROVAL `3036e4a8dec422d32ce60cccf4d1def0d40cff43` → READY `4539852c7ea0c0992eef434a95364b70b3904972`.
- 승인 메타데이터: cowork-approver-1, issued 2026-11-22T13:55:45.216228+00:00, expires 15:55:45.216228+00:00. GPT가 원격 요청·ZIP·PIN·READY 바인딩과 순서를 대조함. 호스트 보호 신뢰 루트로 직접 암호서명 재검증은 NOT_RUN; 사용자 확인 및 실제 운영 처리와 구별.
- [DISPATCH_1.md](../../dispatch/REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122/DISPATCH_1.md): 2026-11-22 **22:57:05 KST**, 설치 watcher v0.2.29. 처리 키는 RID|1|정확 ZIP SHA|1.
- [REVIEW_RESULT_1.md](../../reviews/REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122/REVIEW_RESULT_1.md): COMPLETED, 9,479 B, SHA-256 `bf6f299dc5d192d04a0f0c19e73775e03040748c5f9a342b70672c5684c3ffe6`.
- [RECEIPT_1.md](../../receipts/REQ-COWORK-V033-R2-WATCHER-REVIEW-20261122/RECEIPT_1.md): ok=true, RID/revision/SHA/처리 키 일치. SHA-256 `52cfd63bd71fe90ebd431316233dc09520e7411762a1f748576960a6662ca163`.
- 비용·호출 수: Windows 결과 §11.4가 감사 DB 기준 **USD 1.057171, 디스패치 1회, 중복 0**을 보고. GPT가 운영 DB를 직접 읽은 값은 아니며 원격 영수증에는 비용 필드가 없음. 내부 턴 36을 36회 디스패치로 해석하지 않음. 이번 GPT 작업에서 새 리뷰·모델 실행 요청 0.

## 2. 독립 리뷰 판정

정적 코드 리뷰의 BLOCKING 0과 완료 증거는 수용. 5개 비차단 관찰은 nonce 검증 순서, 크기 표현, 비용 경로, 전송 원자성의 확인 한계, 중단 봉인/잠금 연결에 관한 내용으로 모두 결함 5건이라는 뜻은 아님. 리뷰어는 시험을 실행하지 않았고 GitHub/Dropbox 전송 구현 본문을 읽지 않았다고 명시했음.

비용 설명은 수정 수용: 후보 auto_policy.assess는 비용·일/월 사용량을 승인 게이트로 쓰지 않으며 관련 loader도 값을 0으로 정규화한다. 리뷰의 “집계 signer 게이트 유지” 설명만으로 후보의 금액 상한을 보장할 수 없음. 이번 설치본 v0.2.29 리뷰의 실제 비용 보고와 후보의 미래 LIVE 비용 정책을 혼동하지 않음.

## 3. GPT 추가 직접 검증

ZIP: `collab/packages/v0_2_33_r2_intent_wired_candidate.zip`
SHA-256: `23579a5c8c6690b5831116410fc623e3a8bbc5c659cb6fdea8628e765fa7c206`
301,136 B / 111항목. A 고정 raw bytes를 내려받아 직접 일치 확인. CRC, 중복 이름, 절대경로/경로탈출, 심볼릭 링크 검사 PASS. Windows tree SHA `e4ecdc4c9d141ec76be922410dcd0ea1eb8e3598c6df01a80908ccfadf4cd0e0`는 기존 호스트 보고를 유지하며 이번 GPT가 같은 알고리즘으로 재계산한 값으로 표시하지 않음.

| 항목 | 결과 | 근거·한계 |
|---|---|---|
| 고정 ZIP bytes·안전 경로 | PASS | 위 SHA/크기/CRC/111항목 직접 확인 |
| 소비 후 REVIEW_INTENT 만료 재검증 | **FAIL(함수 단위 합성 재현)** | F1. 실제 _revalidate와 pure gate, 합성 store/trust/transport. 전체 서명 경로 실행은 아님 |
| 패키지 RELEASE_MANIFEST 일치 | **FAIL** | F2. 버전 0.2.26, 크기 또는 SHA 불일치 21건, 없는 파일 참조 13건 |
| Git Commit A의 의도 발행 가능성 | **소스 충돌 확인 / 실제 Git 시험 NOT_RUN** | F3. A 안에서 A를 바인딩한 서명 파일을 요구 |
| GitHub add-only 전송 | PASS(소스 확인) / 실제 경합 NOT_RUN | contents PUT에 기존 sha 없음, 409/422는 UploadConflict. 운영 경쟁 쓰기 미실행 |
| 기존 전체 회귀 | PASS(Windows 보고) | 1014 PASS/0 FAIL/12 SKIP 재사용. GPT 환경에 pytest 없어 전체 재실행 NOT_RUN |
| 설치/Task SHADOW·운영 DB 이행·LIVE | NOT_RUN | 이번 원격 결과 확인 범위에서 실행하지 않음 |

### F1. 의도 만료 시점이 소비 후 사라짐 — 수정 필요
`skill_collab_watcher/auto_approval.py:375`의 _intent_scope는 원본 의도의 서명·시각·바인딩을 처음 검증하지만, :600 후보 기록에는 intent_nonce와 intent_key_id만 남긴다. :636–678 _revalidate는 nonce owner와 현재 키 ACTIVE/purpose, 현행 위임만 확인한 뒤 스킬을 확장한다. 원본 의도 expires_at/서명된 바인딩을 다시 읽거나 검증하지 않는다.

실제 함수 AST를 그대로 추출하고 후보의 실제 auto_policy.assess를 사용한 합성 재현:
`intent_expiry=1999999999, now=2000000000, delegation_expiry=2000086400 → (True, "ok")`.
원래 의도가 만료된 뒤의 재검증을 거부해야 하는 요구와 불일치. 초기 검증·실제 Ed25519 서명·모델은 이 시험에서 실행하지 않았음. **이번 완료 리뷰의 2시간짜리 APPROVAL이 무효라는 의미가 아니며**, 신규 REVIEW_INTENT 경로의 결함임.

수정 수용 범위: 소비된 의도의 서명 원문/고정 해시와 정확 바인딩·발급/만료를 보존하고, 서명·READY 직전 현재 시간/현재 trust로 다시 검증. 재검증은 nonce를 새로 소비하지 않고 기존 소유권·요청 revision/입력을 확인. 만료·키 해지·입력 변경은 서명/READY/모델 0. 기존 운영 nonce 이력 삭제 금지.

### F2. 0.2.26 매니페스트가 r2 실물과 불일치 — 수정 필요
`docs/RELEASE_MANIFEST.json`의 version=0.2.26/baseline=0.2.25. listed files를 직접 대조하면 21개 크기/해시 불일치와 13개 부재 참조가 있다. 신규 review_intent 파일도 이 구 목록에 반영되지 않음. 독립 리뷰 범위에서 확인된 항목이 아니며 외부 ZIP SHA가 일치한다는 사실만으로 내부 매니페스트를 PASS로 볼 수 없음.
다음 후보에서 실제 포함 파일/버전 기준으로 재생성하고 자기 파일 해시 제외 규칙을 명시한다. 구 ZIP은 변경하지 않는다.

### F3. Commit A 자기 참조 — 발행 흐름 수정·시험 필요
_intent_scope는 `download_at_commit(.../REVIEW_INTENT.json, A)`를 호출하면서 서명된 source_commit도 A여야 한다. 일반 Git 발행에서 A를 만든 뒤 A를 바인딩해 서명한 의도를 추가하면 새 커밋이 생기므로 A에는 그 파일이 없다. 기존 `tests/test_v033_intent_wiring.py:55–64`는 commit과 무관하게 의도 bytes를 반환하는 monkeypatch를 써서 이 발행 가능성을 입증하지 못함. 보안 우회가 실증됐다는 뜻이 아니라 새 SCOPE 기능의 실제 발행이 성립하지 않는 소스 설계 충돌임.

최소 보완 방향: REQUEST/ZIP을 A에 고정한 채 **A 이후의 별도 고정 snapshot**에 서명된 의도를 두고 A·요청/revision/원본 bytes에 바인딩. 기존 전송/서명 계약 재사용. 후속 snapshot을 최초 검증 때 고정·보존하여 최신 파일 교체로 권한이 바뀌지 않도록 한다. 로컬 실제 Git A→의도 snapshot 생성 시험 및 정확 revision/재시작/만료/경합 시험을 한 묶음으로 보완. 보호 키·운영 DB·위임 변경으로 우회하지 않는다.

재현 자료: [함수 단위 검사](evidence/v033_r2_gpt_supplementary_check.py), [관측값·불일치 목록](evidence/v033_r2_gpt_supplementary_evidence.json). 검사 스크립트의 root는 안전하게 풀어 둔 후보 루트로 지정. signer/network/운영 DB를 사용하지 않음.

## 4. 보존·다음 한 동작
다음 동작은 **동결 r2의 F1/F2/F3를 한 번에 고친 별도 개발 후보 + 관련 시험 + 회귀 + 패키징**. 새 SHA를 r2 리뷰 완료로 승격하지 않는다. 새 후보 PUBLIC 게시 허용/추가 독립 리뷰는 이번 정확 r2 공개 허용·단 1회 실행으로 자동 확대하지 않으며, 기존 리뷰를 재큐잉하지 않는다. 본 문서·지시서 게시 자체가 Windows 실행 트리거는 아님.

현재 LIVE v0.2.29에 대해 이번 GPT는 설치·기동/정지·Task·Notifier·설정·키·trust root·위임·운영 DB를 변경하지 않았다. 이전 호스트 “설치 트리 불변”은 호스트 보고이며 GPT의 현재 직접 점검이 아님. LIVE_AUDIT_DELTA_CAUSE=UNVERIFIED 유지. rollback은 현재 DB/nonce/완료 이력 보존, 과거 DB 교체·nonce 테이블 DROP 금지.

운영 DB 이행, 필요한 설치 기반 SHADOW, 비용 무상한 위험 수용과 10단계 LIVE 최종 승인은 보완 후보의 유효 증거·GPT 판정 및 사용자 별도 확인 후 처리. **LIVE_READY=NO.** 독립 리뷰 대기·승인 파일 재발급이 현재 다음 동작은 아님.
