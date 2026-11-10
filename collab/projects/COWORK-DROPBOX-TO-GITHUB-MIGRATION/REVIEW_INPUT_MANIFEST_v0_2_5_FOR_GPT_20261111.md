# 독립 리뷰 입력 자료 — skill-collab-watcher v0.2.5 (무인 리뷰 실행 안전장치 포함) (REVIEW_INPUT, 실행 요청 아님)

2026-11-10 KST | 작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION | 증거 수준: SELF_TEST_REPORTED
이 문서는 REQUEST도 READY도 아니며 어떤 리뷰 실행도 유발하지 않는다. `collab/requests/`에 두지 않는다.
정식 독립 리뷰는 사용자 명시 승인, 유효한 서명된 REQUEST/READY, 비용 단계 지정, 영수증 확인 이후에만 시작한다.

## 1. 리뷰 대상 식별
- 후보: skill-collab-watcher_v0_2_5_1110.zip
- 크기: 155,288 bytes
- SHA-256: 40a1a944ec55d7414051374a67e264fd4fe03dadfcdead449ff37bac86dd93e6
- 기준선: 운영 중인 v0.1.5 (읽기 전용 대조). 이전 후보 v0.2.0 / v0.2.1 / v0.2.2 / v0.2.3 / v0.2.4는 불변 보존.
- 위치: Windows 로컬 전용. GitHub에 게시하지 않았다 (아래 5절 참조). 분류: development_not_for_deployment.
- 개발자 자체 시험: 448 PASS / 0 FAIL / 12 SKIP (GUI 옵트인 8, 프로젝트 .venv 조건 4). 압축을 푼 사본에서도 동일.

## 2. 우선 검토 요청 영역 (보안·무손실 핵심)
| 영역 | 파일 | 확인해 달라는 질문 |
|---|---|---|
| 승인 검증 순서와 fail-closed | skill_collab_watcher/approval.py | 서명 검증 전에 신뢰하는 입력이 있는가. 모든 거부 경로가 모델 호출 0인가. 키 상태·유효 기간·수명 상한·동결·nonce 검사 누락은 없는가 |
| 승인 게이트 호출부 | skill_collab_watcher/orchestrator.py (_check_approval, 읽기 후 검증, 재게시 경로) | 승인 없이 디스패치에 도달하는 경로가 있는가. 결과 재검증이 다른 작업의 영수증을 걸러내는가 |
| 상태 저장소 | skill_collab_watcher/state_store.py | 제공자별 대기 범위 분리, 단일 LIVE lease, 전환 거부 조건, 중단 작업 봉인(잠금 보유 + 소유자 구분), 신뢰 루트 버전 래칫, 읽기 전용 모드 |
| GitHub 전송 | skill_collab_watcher/github_transport.py | 고정 커밋 읽기, blob SHA와 크기 검증, add-only 게시와 충돌 처리, 토큰 비노출, 속도 제한 처리 |
| 패키지 안전 | skill_collab_watcher/zip_safety.py | 자격증명 형태 검사가 호출 전에 동작하는가. 누락되는 형태가 있는가 |
| 알림 | skill_collab_watcher/notify_events.py | 워터마크 초기화 없이 발송되지 않는가. 크래시 후 중복·누락 |
| 실행 구성 | skill_collab_watcher/cli.py | 신뢰 루트 고정·ACL·롤백 거부, SHADOW의 읽기 전용 열기와 작업 폴더 분리, recover --requeue 차단 |
| 무인 실행 사전 점검 | skill_collab_watcher/review_runner.py (preflight), orchestrator.py (claim 직전 호출) | 로그인 만료·CLI 오류가 요청을 소모하지 않고 대기로 남는가. 사전 점검이 계정 정보를 남기지 않는가 |
| 일일 상한·원격 정지 | orchestrator.py (_check_ceilings, PAUSE_REVIEWS), state_store.py (spend_since, dispatches_since) | 비용 미기록 호출을 상한으로 집계하는 것이 올바른가. 정지 표지를 쓸 수 있는 누구나 시작 방향으로는 영향을 줄 수 없는가 |
| 정지 감지 알림 | skill_collab_watcher/notify_events.py (check_stalled) | 중복·누락 없이 장애당 1회, 복구 1회인가 |
| 신뢰 루트 도구 | tools/trust_root_tool.py | 공개키만 다루는가. 기존 파일을 덮어쓰지 않는가 |
| 정적 경계 시험 | tests/test_model_call_boundary.py | 프로세스 시작은 review_runner.py 한 곳뿐이라는 보장이 유지되는가 (ACL 점검을 Windows API로 구현해 이 시험을 약화하지 않았음) |

## 3. 알려진 한계 (리뷰어가 사실로 받아들일 것)
1. 실제 운영 신뢰 루트와 서명 키는 없다. Ed25519 시험은 시험마다 메모리에서 만든 시험 키로만 수행.
2. 호스트 SHADOW, 실제 GitHub REQUEST/READY, 실제 Telegram 발송, 운영 DB의 실제 이행은 수행하지 않았다.
3. lease 만료 자동 탈취는 없다. 비정상 종료 후에는 사람이 확인한다.
4. 변이 시험과 커버리지 측정은 하지 않았다.
5. 표본 63쌍에는 BOM과 CRLF가 없어서 그 경로는 합성 시험으로만 확인했다.
6. Windows 외 환경(Linux, 사내 LLM)은 검증하지 않았다.
6a. 무인 실행: 구독 사용량 한도에 걸렸을 때 CLI가 내는 오류 형식은 관찰하지 못했다 (실제 호출이 필요해 미실행). 현재는 일반 실패로 처리되어 요청이 종료 상태가 된다.
6b. 예약 작업은 사용자 로그온이 필요한 Interactive 방식이다. 재부팅 후 로그온 없이는 시작되지 않는다.
6c. 운영 중인 Telegram notifier 스크립트는 변경하지 않았으므로 새 알림(정지 감지 등)은 아직 연결되지 않았다.
7. 이 검토 입력은 개발 세션이 작성했으므로 편향 가능성이 있다. 독립 검토자는 이 문서의 결론이 아니라 소스와 시험을 직접 보아야 한다.

## 4. 재현 방법
1. ZIP의 SHA-256이 위 값과 같은지 확인한다.
2. 압축을 풀고 격리 가상환경에서 `python -m pytest tests -q`를 실행한다 (실서명 시험은 `requirements-crypto-test.lock`의 해시 고정 설치가 필요하며, 없으면 해당 모듈은 건너뛴다).
3. 아래 6절 표의 파일별 SHA-256과 비교한다.
4. 운영 소스와의 차이는 "vs v0.1.5" 열과 `docs/CUTOVER_RUNBOOK.md`를 따른다.

## 5. 소스 전달 조건
- ZIP에는 자격증명 형태 문자열이 없다 (빌드 비밀 검사 65파일 0건, 로컬 자격 값 대조 포함). 시험 입력은 합성 데이터이고 운영 요청·로그·DB는 포함하지 않는다.
- 그래도 소스 ZIP의 PRIVATE 게시는 파일별 반출 분류가 확정되고 사용자가 승인한 뒤에만 한다. 현재 NOT_APPROVED.
- 승인 시 게시 위치 제안: `collab/packages/` 아래 새 파일명 (덮어쓰기 금지). 게시 후 원격 바이트 SHA-256 재검증.

## 6. 정식 리뷰 시작 전 체크리스트
- [ ] 사용자 명시 승인 (리뷰 실행, 비용 단계: STATIC $1 / LARGE $3 / XLARGE $6 상한)
- [ ] 운영 신뢰 루트 부트스트랩과 승인 키 (docs/CUTOVER_RUNBOOK.md 2절)
- [ ] 소스 전달 승인과 반출 분류 (위 5절)
- [ ] REQUEST: 후보 ZIP, 지식 참조(이 문서, 설계 r0002, 시험 매트릭스, 결과 문서)를 SHA-256으로 고정
- [ ] READY와 승인 서명은 마지막에 한 번 게시 (커밋 A, 커밋 B)
- [ ] 결과와 영수증 원격 재조회 일치

## 7. 파일별 식별 (ZIP 항목 65개)

| file | bytes | sha256 | vs v0.1.5 | +lines | -lines |
|---|---|---|---|---|---|
| config/reviewer.config.example.json | 826 | 0ce0e3b034b431a98ec2e38a05791a177a1f99ac8b91c0a6102ff5af081575a8 | UNCHANGED | 0 | 0 |
| docs/CUTOVER_RUNBOOK.md | 10594 | 4e4a1b199787ff6edf951fec125831a7c8dd2f7761b8ccaa2f1c17608de58b96 | NEW | 133 | 0 |
| prompts/review_instructions.md | 3551 | f69c60e44a5999fcc37f9ffb4cc65528c210acf37f5ee9aade80d2c9022aa0aa | UNCHANGED | 0 | 0 |
| requirements-crypto-test.lock | 1998 | 1df4e4a0a83ca21dabf3f1116a797a3e9f74af78a99fb252623fb59dab35922a | NEW | 21 | 0 |
| requirements.txt | 47 | 5c9380b4c3837cd8da9060a398de7250c129386f8a84f145b0a25ceeefa4b73e | UNCHANGED | 0 | 0 |
| skill_collab_watcher/__init__.py | 22 | 5ec6b76b238c5648545a6e2dd3a61ec871346a98e965e7f12c7e32969d020ed5 | CHANGED | 1 | 1 |
| skill_collab_watcher/approval.py | 15340 | 536fec9e3363e5930ede397ef337de610b9ffc5aa74c11f3e3d1de582ec2b959 | NEW | 357 | 0 |
| skill_collab_watcher/auth_flow.py | 4420 | e1c23bb2e5f5ae45388b25539b485e112b9c13f5a0a770f25cf2652f92dfcc2e | UNCHANGED | 0 | 0 |
| skill_collab_watcher/cli.py | 27132 | 561c5a682f5d2045826476322117c7f778050347a9a5a04088603f47f6e200e0 | CHANGED | 97 | 19 |
| skill_collab_watcher/config.py | 11023 | 047c0ef677844b09b3d015afd9e84135f6997a1e9383972ce7f9d2349a99f398 | CHANGED | 35 | 0 |
| skill_collab_watcher/dropbox_transport.py | 13159 | 2913eca341aea1be17dcc63fcaf88d8dac1c269a7429c82cf8168b018b66ef77 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/fake_runner.py | 1335 | 18c5ba10bf9e9cdd52aea56f544f87fa6c4071d633df81ff7467db74f4026100 | CHANGED | 6 | 0 |
| skill_collab_watcher/github_transport.py | 12554 | fa60ba4fa2f190ad4f8e20b6cf69974f52feba80ae4dd6d153f46f86b72ef5d6 | NEW | 296 | 0 |
| skill_collab_watcher/lock.py | 1746 | 1d4969b54de04faa9b4acb5cc8f2d8bfd87f70703f640fa1668f51ff1bc5f929 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/mock_transport.py | 6687 | c3247dab9d3d2efffc28c398074abada0bdbd1176231bf91a017ccd2976fcfa3 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/models.py | 1597 | b964f0cff2f15352e7b92a20e003f268359846f61e72d3a65c8119ad7f51d4dd | UNCHANGED | 0 | 0 |
| skill_collab_watcher/notify_events.py | 8724 | a6f16aae28262fed6a5e2cdac86d7211b0e800892393023e4710d0a0f3059503 | NEW | 179 | 0 |
| skill_collab_watcher/orchestrator.py | 41743 | c237636616cf7e8af5b19eac6a78cb7cb90fa4243a726d312378e575e6b853e5 | CHANGED | 255 | 29 |
| skill_collab_watcher/review_runner.py | 10862 | 58140f181f381a492ff5a04cbf1b6bb47ef6647155471b0a3245ae52633e9928 | CHANGED | 25 | 0 |
| skill_collab_watcher/secret_prompt.py | 3466 | 61e5df6d9d229a325554ab4550c842e14fd04a1d46e2e9e69d983831b395e442 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/secrets_store.py | 2257 | 0adc31ec37864dcaddae7ca5a1adaca0f5c539da412aeb8442481500b0b0a868 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/signature_backend.py | 1228 | 262c1db7e805d3623e9875a023582410d05c4e7ffb1dedde0c04b1e1389d1684 | NEW | 36 | 0 |
| skill_collab_watcher/state_store.py | 22404 | 3d7d64e549b2495830a8a70e024ceaaf29e86a1d02336126caf74d0ae0310248 | CHANGED | 308 | 13 |
| skill_collab_watcher/transport_base.py | 3430 | 189fbbf79811056bb51fe7b34dbfda2e18315177abab05abb59023ee87801b28 | CHANGED | 33 | 0 |
| skill_collab_watcher/validator.py | 9715 | 9d3cf7b28e07d27a58d6175c92fbafff0655862ab30101078c38a6db5eed45d7 | CHANGED | 14 | 2 |
| skill_collab_watcher/watch_loop.py | 4671 | fb994ca39d79c6d7c62e20c237454c489629f1139fbe6a1ae0ac26fb89373911 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/zip_safety.py | 2779 | d1c16a836dabe72c9944f230768b8ada0ae6f7da57e7591d586bb5b62ad34d94 | CHANGED | 29 | 0 |
| tests/bundle.py | 4939 | 7eda487a9309b1d8c1d161ffe0fbbbf569a8b17003a5c12c045daeb5cde4975b | NEW | 106 | 0 |
| tests/conftest.py | 3916 | 7153d77d044a4d5e39d410274e1d5d0ac761cd44a6e369abbe0cf3fa8d72b56e | CHANGED | 13 | 0 |
| tests/fake_github.py | 6032 | 04dddaa90d865e377779564d7d003efd519bf0770dd1c79e0c2944e6e942ded7 | NEW | 152 | 0 |
| tests/test_auth_flow.py | 13994 | 940a9cec9a11239f7ca3bfc96062c469afe20663fbaef9469247e302bf8c7b12 | UNCHANGED | 0 | 0 |
| tests/test_config.py | 4921 | 54c345b26b5254fd0e1058b79a92ade08b45317dde6a21d5c021b8f3bba7aafc | UNCHANGED | 0 | 0 |
| tests/test_cursor_and_pending.py | 9838 | 9dc3becc99dfa83e35a5edcca4aba6182e94550655e0d46ce3bb04b9ae2cbbfa | UNCHANGED | 0 | 0 |
| tests/test_dropbox_transport_errors.py | 14188 | 4cb11bc34f589b16382634c40523f5eb34420fd697487c66662122b515ec3c18 | UNCHANGED | 0 | 0 |
| tests/test_model_call_boundary.py | 1930 | c593a22d0668ea3deb578ba9a44eae2fc6db7cf578e157657374116c358b31ab | UNCHANGED | 0 | 0 |
| tests/test_no_model_calls.py | 11582 | 0b02170669d468fab1f08a00b8ac42a6e64eba8644232d43375a7e7746d4c8e3 | UNCHANGED | 0 | 0 |
| tests/test_phase1_approval.py | 7318 | 8b133a31c968c0a384aa1c36092c6cfe7e4abf5119011e54b79fcc1616d14a26 | NEW | 177 | 0 |
| tests/test_phase1_blocking_fixes.py | 12951 | 0e52433861d5d4eae41fe0aa05b8f7870d9a409e0b3ab582a25dce8aec75d393 | NEW | 292 | 0 |
| tests/test_phase1_github.py | 11002 | 0780d0145de83b7746a54f9b54cda7e229177b413876635f7dd72837fca3b26a | NEW | 247 | 0 |
| tests/test_phase2_acceptance.py | 9649 | 9dd1dcc1a2c3f2d67397a51abcb98ab585d148398e962fc4cf6900175e9eb2a5 | NEW | 209 | 0 |
| tests/test_phase2_cutover.py | 6315 | e00fca22d97dd86d9caf03262558ad90fee9c5bf46b19b5d47099638b4783507 | NEW | 143 | 0 |
| tests/test_phase2_ed25519.py | 11964 | d035526d5f4c2c6366220ffc00c02e1a4fd1ccb6af9c686bae63b3ea400a9323 | NEW | 246 | 0 |
| tests/test_phase2_notify.py | 8537 | 5aedc458b32b6805074203d5f0d9e8287150a35429fb0fb96b00dd2b09942483 | NEW | 207 | 0 |
| tests/test_phase3_gates.py | 17040 | 67c3ab15fabfd06d90f22333615625c127d143788a7e7839315d692c11b6bd7e | NEW | 395 | 0 |
| tests/test_phase3_trust_tool.py | 3186 | 272bd69b19c24a33a2d431af714d07b389fd2fe7fb3badf90781005e00044465 | NEW | 80 | 0 |
| tests/test_phase4_unattended.py | 17028 | 52eb5f34b5e66fa704410cd8d0ad762f36f7418817aacd3eaa1eb0efdc818e2c | NEW | 363 | 0 |
| tests/test_release_packaging.py | 4651 | cac4a78eccc20984b960e777b91fbfe33d9eb800205a430078896f5c3fccba7f | UNCHANGED | 0 | 0 |
| tests/test_review_runner_argv.py | 1241 | 2e83952712aca9e5f39a9b5f17ea3b0c6434fa04cce0e09fe6e9dcb560e39fec | UNCHANGED | 0 | 0 |
| tests/test_secret_prompt.py | 8153 | 72dc87aec138979ad1a2f90140d3b89f6ea0cf53ebfae5520eeaf501f537551e | UNCHANGED | 0 | 0 |
| tests/test_state_store.py | 1806 | 3aff3fbdae0846f1ecca4231803aeac84f9206fe6a4a525b0633b2b9c3efe9e2 | UNCHANGED | 0 | 0 |
| tests/test_v013_hardening.py | 11163 | 548360cac092e039f0527e79ecf33830167fdb53b9a2538723a2f50dbc0f8237 | UNCHANGED | 0 | 0 |
| tests/test_v014_budget_tiers.py | 8220 | 91918a33c69bcd688252dbac8cc58f742ebda4b7f19c7ae5944097ea8d66bc8c | UNCHANGED | 0 | 0 |
| tests/test_v015_token_savings.py | 13422 | 51a55699d5731049c9d0213ef8bdb15b2cb02c3480eaab16653580a0be1c6d8a | UNCHANGED | 0 | 0 |
| tests/test_validator.py | 2084 | 3970de86b0bb1b5bc411e9f49837f5f167d5deeac35f4757991990ecd9d728e7 | UNCHANGED | 0 | 0 |
| tests/test_watch_loop.py | 4955 | d1df51ef8ab3df9d0d676cf12c118dbcea04a2f8bad7b2d48d98bc5ec4900747 | UNCHANGED | 0 | 0 |
| tests/test_windows_scripts.py | 1469 | 239a15cb4381bff8c4fce7642a8226bf5a17028d014f53c2843603022ff13a97 | UNCHANGED | 0 | 0 |
| tests/test_zip_safety.py | 887 | 534e11f038301bbf62c114eb3d751f98b049c1bc3e6731f261ed72669a88602b | UNCHANGED | 0 | 0 |
| tools/__init__.py | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | UNCHANGED | 0 | 0 |
| tools/build_release.py | 7411 | 8d5d2a70c1e5377df33da5427beaaf4bbf6c7383c2d33195d790caa7b1f14282 | CHANGED | 2 | 2 |
| tools/trust_root_tool.py | 4197 | 2090579ed5450243a5642ab5bb6ba43cf58334a594f139c93dce2bfd31ce5697 | NEW | 101 | 0 |
| windows/auth_init.cmd | 211 | 12c93ad4c5f6fdc902aea8808d6d941c3193c80bae0b3df2fcc67ba557683102 | UNCHANGED | 0 | 0 |
| windows/recover.cmd | 209 | 2b07c8e8a171138a729649b1fcc277abc283f4017430206628c6ca13a4f0d881 | UNCHANGED | 0 | 0 |
| windows/run_scan.cmd | 206 | acaccf6a288766b73cdc0348473e1c3ea9456e6a8c1d5abb4a0f3868da3d7701 | UNCHANGED | 0 | 0 |
| windows/run_watch.cmd | 386 | a674441e82200c78a5065bbfb190a7b9906798c8c6949f4f4469914fa5b9a123 | UNCHANGED | 0 | 0 |
| windows/status.cmd | 205 | eca8223b56c18b5b183e96fb202ceb6e3b9347434b97ab4bc922c1dcaac10904 | UNCHANGED | 0 | 0 |

끝.
