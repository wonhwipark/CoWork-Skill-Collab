# 독립 리뷰 입력 자료 — skill-collab-watcher v0.2.8 (REVIEW_PREP, 실행 요청 아님)

2026-11-11 KST | 작업 ID: COWORK-DROPBOX-TO-GITHUB-MIGRATION | 증거 수준: SELF_TEST_REPORTED
이 문서는 REQUEST도 READY도 아니며 어떤 리뷰 실행도 유발하지 않는다. `collab/requests/`에 두지 않는다.
정식 독립 리뷰는 사용자 명시 승인, 승인자의 유효한 서명, 고정 커밋, 비용 단계 지정, 영수증 확인 이후에만 시작한다.
`INDEPENDENT_REVIEW=NOT_RUN`. 개발 세션의 자체 시험은 독립 리뷰가 아니다.

## 1. 리뷰 대상 식별
- 후보: skill-collab-watcher_v0_2_8_1111.zip
- 크기: 173,615 bytes
- SHA-256: c6231cc329faff26c6e04a0ca454dec0d62a5eaaa0eb08edf9b6a57280f78daa
- 항목 70개, CRC 통과, 경로 이탈·심볼릭 링크·중첩 압축·비밀·반출 금지 파일 0, 개인 식별자 0.
- 기준선: 운영 중인 Dropbox 감시기 v0.1.5 (읽기 전용 대조, 불변). 변경 12개 / 신규 24개 / 동일 34개, 소스(패키지+도구) 추가 2,221줄 / 삭제 68줄.
- 이전 후보 v0.2.0~v0.2.5(전부)와 중간본 v0.2.6, v0.2.7은 불변 보존. v0.2.6은 시험 헬퍼의 간헐 실패(2초 경계) 수정 전, v0.2.7은 런북이 낡은 SHADOW 설계를 설명하던 상태라 폐기(superseded)했다.
- 위치: Windows 로컬 전용. GitHub에 게시하지 않았다 (5절). 분류: development_not_for_deployment.
- 개발자 자체 시험: 522 PASS / 0 FAIL / 12 SKIP (시험용 가상환경, 암호 라이브러리 포함). 운영 인터프리터(암호 라이브러리 없음)에서는 487 PASS / 0 FAIL / 14 SKIP (실서명 두 모듈 35건이 건너뜀). 압축을 푼 사본에서 각각 재현.
- SKIP 12건 = GUI 실창 8건(옵트인) + 프로젝트 .venv 조건 4건. 원인 불명 SKIP 없음.

## 2. 우선 검토 요청 영역과 질문 (이번 변경분 중심)
| 영역 | 파일 | 확인해 달라는 질문 |
|---|---|---|
| S-1 SHADOW가 운영 DB를 열지 않음 | skill_collab_watcher/shadow_guard.py, cli.py (_work_dir, _db_path, _open_runtime), config.py (shadow.state_dir) | 경로 가드에 우회가 있는가 (junction, 8.3 이름, 대소문자, 확인 후 생성 사이의 틈, UNC, 파일 정체성). SHADOW 코드 경로 중 live `state_dir`을 읽거나 만드는 곳이 남았는가 |
| SHADOW 방어층 | github_transport.py (read_only), shadow_guard.py (ShadowRunner) | 쓰기 호출이나 리뷰 시작이 객체 수준에서 불가능한가 |
| S-2 감시기 계정의 신뢰 루트 수정 가능성 | approval.py (_effective_mask, watcher_write_findings), cli.py (_load_trust) | 유효 권한 계산이 상승 토큰·그룹 차이에서 과소 판정하지 않는가. 검사 대상(루트, 폴더, 핀을 담은 설정, 그 폴더)이 충분한가 |
| 시계 단조 증가 | state_store.py (check_time_ratchet), orchestrator.py (_check_approval) | 제공자 시계 역행과 로컬 시계 되돌림을 모두 막는가. 읽기 전용 저장소는 기록하지 않는가 |
| 승인자 서명 도구 | tools/approval_signer.py | 서명 대상 필드가 감시기의 검증 필드와 정확히 같은가. 개인키가 출력·파일·로그로 새지 않는가. 덮어쓰기 거부 |
| 이전 변경분(재확인 대상) | approval.py, orchestrator.py, state_store.py, github_transport.py, zip_safety.py, notify_events.py, review_runner.py | 승인 검증 순서와 fail-closed, 처리키 멱등성, 대기 요청의 제공자별 분리, 봉인, 읽기 후 검증, 로그인 사전 점검, 일일 상한 |
| 모델 호출 경계 | tests/test_model_call_boundary.py | 프로세스 생성이 review_runner.py 한 곳뿐이라는 정적 보장이 유지되는가 (ACL 점검은 Windows API 호출로 구현해 이 시험을 약화하지 않았다) |
| 운영자 도구 | tools/trust_root_tool.py | 공개키만 다루는가. 기존 파일을 덮어쓰지 않는가 |

## 3. 알려진 결함과 한계 (리뷰어가 사실로 받아들일 것)
1. 호스트 SHADOW는 설치·가동하지 않았다. 운영 DB를 열지 않는다는 증명은 격리 환경의 파일 핸들 수준이며, 실제 호스트 프로세스의 파일 I/O 추적은 NOT_RUN이다.
2. 이 호스트에서는 감시기가 대화형 관리자 계정으로 돌고 그 계정 프로필에 모든 파일이 있어서, S-2 독립성 검사는 LIVE에서 **거부**한다 (실제 Windows API 시험으로 확인). 통과하려면 비관리자 실행 계정과 관리자 전용 신뢰 폴더가 필요하며 아직 구성하지 않았다.
3. 운영 신뢰 루트와 승인자 개인키는 없다. 실서명 시험은 시험마다 만든 임시 키로만 수행했다.
4. 유효 권한 점검은 사용자와 그 그룹 기준의 계산이며, 상승되지 않은 관리자 토큰을 과대 판정한다(보수적, 거부 쪽 오류).
5. 정식 독립 리뷰, 실제 GitHub REQUEST/READY, 실제 Telegram, 운영 DB의 실제 이행은 수행하지 않았다.
6. lease 만료 자동 탈취는 없다. 구독 사용량 한도 시 CLI 오류 형식은 미관찰이다.
7. 변이 시험과 커버리지는 측정하지 않았다. 표본 63쌍에는 BOM·CRLF가 없다.
8. 이 문서는 개발 세션이 작성했으므로 편향 가능성이 있다. 독립 검토자는 이 문서의 결론이 아니라 소스와 시험을 직접 보아야 한다.

## 4. 재현 방법 (모델 호출 0)
1. ZIP의 SHA-256이 위 값과 같은지 확인한다.
2. 압축을 풀고 격리 가상환경에서 `python -m pytest tests -q`를 실행한다. 실서명 시험은 `requirements-crypto-test.lock`의 해시 고정 설치가 필요하며 없으면 두 모듈이 건너뛴다.
3. SHADOW 도구 잠금 시험만: `python -m pytest tests/test_phase5_shadow.py -q` (Windows 필요).
4. S-2 독립성: `python -m pytest tests/test_phase5_independence.py -q`.
5. 서명 도구 왕복: `python -m pytest tests/test_phase5_signer.py -q` (암호 라이브러리 필요).
6. 아래 7절 표의 파일별 SHA-256과 비교한다. 운영 소스와의 차이는 "vs v0.1.5" 열을 따른다.
7. 모델 호출이 없음을 확인하는 방법: 시험은 가짜 러너만 쓰고, 프로세스 생성 정적 시험이 통과한다.

## 5. 소스 전달 조건과 반출 분류
- 분류(파일 70개): 패키지 소스 23, 운영자 도구 4, 시험 33 (합성 데이터만), 문서 1, Windows 런처 5, 리뷰 프롬프트 1, 설정 예시 1, 의존성·README 2.
- 검사: 자격증명 형태 문자열 0, 소유자 핸들·절대 사용자 경로·계정명·장치명·이메일 0, 운영 요청·로그·DB 0, 실행 가능한 REQUEST/READY 0.
- 의존성: `requirements-crypto-test.lock` 19개 패키지, 모두 정확한 버전과 SHA-256 고정.
- 그래도 소스 ZIP의 PRIVATE 게시는 사용자가 반출 분류를 승인한 뒤에만 한다. 현재 NOT_APPROVED. 승인 시 `collab/packages/`에 새 파일명으로 추가하고 원격 바이트 SHA-256을 재검증한다. 덮어쓰기 금지.

## 6. 정식 리뷰 시작 전 체크리스트 (모두 미충족)
- [ ] 사용자 명시 승인 (리뷰 실행, 비용 단계 STATIC $1 / LARGE $3 / XLARGE $6 상한, 자동 증액 금지, 같은 리뷰 재호출 금지)
- [ ] 승인자 기기에서 키 생성, 신뢰 루트를 감시기 계정이 쓸 수 없는 폴더에 설치하고 핀 설정 (S-2)
- [ ] 소스 전달 승인과 반출 분류 (5절)
- [ ] REQUEST 작성: 후보 ZIP과 지식 참조(이 문서, 설계 r0002, 시험 매트릭스, 결과 문서)를 SHA-256으로 고정
- [ ] 커밋 A: REQUEST와 패키지. 승인자 기기에서 `approval_signer sign`으로 커밋 A에 묶어 서명. 커밋 B: READY, APPROVAL_SIG.json, SOURCE_PIN.json을 마지막에 한 번에 게시
- [ ] 게시 전 `approval_signer check`로 감시기의 검증을 오프라인으로 먼저 통과
- [ ] 결과와 영수증 원격 재조회 일치

## 7. 파일별 식별 (ZIP 항목 70개)

| file | bytes | sha256 | vs v0.1.5 | +lines | -lines |
|---|---|---|---|---|---|
| config/reviewer.config.example.json | 826 | 0ce0e3b034b431a98ec2e38a05791a177a1f99ac8b91c0a6102ff5af081575a8 | UNCHANGED | 0 | 0 |
| docs/CUTOVER_RUNBOOK.md | 13764 | 52f6cb537478578994840e849117bcbcc36398de4624e36eef13c4e5c131578c | NEW | 168 | 0 |
| prompts/review_instructions.md | 3551 | f69c60e44a5999fcc37f9ffb4cc65528c210acf37f5ee9aade80d2c9022aa0aa | UNCHANGED | 0 | 0 |
| requirements-crypto-test.lock | 1998 | 1df4e4a0a83ca21dabf3f1116a797a3e9f74af78a99fb252623fb59dab35922a | NEW | 21 | 0 |
| requirements.txt | 47 | 5c9380b4c3837cd8da9060a398de7250c129386f8a84f145b0a25ceeefa4b73e | UNCHANGED | 0 | 0 |
| skill_collab_watcher/__init__.py | 22 | 1ba0dbc6adb0b3ed59017c030fcab4296b9e62db28fd8e94cafb63f2c456b0f2 | CHANGED | 1 | 1 |
| skill_collab_watcher/approval.py | 19441 | 2d29562a22238036decd6ad8e7c953791691942e347266c2ef1e396303aa866c | NEW | 434 | 0 |
| skill_collab_watcher/auth_flow.py | 4420 | e1c23bb2e5f5ae45388b25539b485e112b9c13f5a0a770f25cf2652f92dfcc2e | UNCHANGED | 0 | 0 |
| skill_collab_watcher/cli.py | 28305 | 27a14d4973d7413e48f62cf3a4150f32d0e309a6ff3b68288ddbe6051c4fb39c | CHANGED | 118 | 21 |
| skill_collab_watcher/config.py | 12383 | 3e3864c0ad6602c6f5c0a0b6beecf8b4331f5530e5f2c1f3d18cc901f3c2f400 | CHANGED | 53 | 0 |
| skill_collab_watcher/dropbox_transport.py | 13159 | 2913eca341aea1be17dcc63fcaf88d8dac1c269a7429c82cf8168b018b66ef77 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/fake_runner.py | 1335 | 18c5ba10bf9e9cdd52aea56f544f87fa6c4071d633df81ff7467db74f4026100 | CHANGED | 6 | 0 |
| skill_collab_watcher/github_transport.py | 12828 | 0020c802b0391e188206168f126a3eca02a6f3c84dafc5ffada990ccff02ee14 | NEW | 300 | 0 |
| skill_collab_watcher/lock.py | 1746 | 1d4969b54de04faa9b4acb5cc8f2d8bfd87f70703f640fa1668f51ff1bc5f929 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/mock_transport.py | 6687 | c3247dab9d3d2efffc28c398074abada0bdbd1176231bf91a017ccd2976fcfa3 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/models.py | 1597 | b964f0cff2f15352e7b92a20e003f268359846f61e72d3a65c8119ad7f51d4dd | UNCHANGED | 0 | 0 |
| skill_collab_watcher/notify_events.py | 8724 | a6f16aae28262fed6a5e2cdac86d7211b0e800892393023e4710d0a0f3059503 | NEW | 179 | 0 |
| skill_collab_watcher/orchestrator.py | 41846 | ed635df3c836bcd930a5845de7407e9384b22ada2a78a7da2dd8051a7a64dd23 | CHANGED | 257 | 29 |
| skill_collab_watcher/review_runner.py | 10862 | 58140f181f381a492ff5a04cbf1b6bb47ef6647155471b0a3245ae52633e9928 | CHANGED | 25 | 0 |
| skill_collab_watcher/secret_prompt.py | 3466 | 61e5df6d9d229a325554ab4550c842e14fd04a1d46e2e9e69d983831b395e442 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/secrets_store.py | 2257 | 0adc31ec37864dcaddae7ca5a1adaca0f5c539da412aeb8442481500b0b0a868 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/shadow_guard.py | 5152 | 5e70ae35e432f1eeed2eef69d8d1848506c644a9db07c482f39892d23c4e5102 | NEW | 129 | 0 |
| skill_collab_watcher/signature_backend.py | 1228 | 262c1db7e805d3623e9875a023582410d05c4e7ffb1dedde0c04b1e1389d1684 | NEW | 36 | 0 |
| skill_collab_watcher/state_store.py | 23161 | ac01bce2d52a164248810701cae656fb1d70292f122ff81e62b3719ee9ff6997 | CHANGED | 320 | 13 |
| skill_collab_watcher/transport_base.py | 3430 | 189fbbf79811056bb51fe7b34dbfda2e18315177abab05abb59023ee87801b28 | CHANGED | 33 | 0 |
| skill_collab_watcher/validator.py | 9715 | 9d3cf7b28e07d27a58d6175c92fbafff0655862ab30101078c38a6db5eed45d7 | CHANGED | 14 | 2 |
| skill_collab_watcher/watch_loop.py | 4671 | fb994ca39d79c6d7c62e20c237454c489629f1139fbe6a1ae0ac26fb89373911 | UNCHANGED | 0 | 0 |
| skill_collab_watcher/zip_safety.py | 2779 | d1c16a836dabe72c9944f230768b8ada0ae6f7da57e7591d586bb5b62ad34d94 | CHANGED | 29 | 0 |
| tests/bundle.py | 4939 | 7eda487a9309b1d8c1d161ffe0fbbbf569a8b17003a5c12c045daeb5cde4975b | NEW | 106 | 0 |
| tests/conftest.py | 4195 | 11d401fa53566c494f7144b9c942d3bded2b3c44f74b46607b604f4b87cdd34a | CHANGED | 17 | 1 |
| tests/fake_github.py | 6028 | c677ecb87e3b48f338ae4793a927a6d8d337ed4387bdc6ff95dd0be1cef14498 | NEW | 152 | 0 |
| tests/test_auth_flow.py | 13994 | 940a9cec9a11239f7ca3bfc96062c469afe20663fbaef9469247e302bf8c7b12 | UNCHANGED | 0 | 0 |
| tests/test_config.py | 4921 | 54c345b26b5254fd0e1058b79a92ade08b45317dde6a21d5c021b8f3bba7aafc | UNCHANGED | 0 | 0 |
| tests/test_cursor_and_pending.py | 9838 | 9dc3becc99dfa83e35a5edcca4aba6182e94550655e0d46ce3bb04b9ae2cbbfa | UNCHANGED | 0 | 0 |
| tests/test_dropbox_transport_errors.py | 14188 | 4cb11bc34f589b16382634c40523f5eb34420fd697487c66662122b515ec3c18 | UNCHANGED | 0 | 0 |
| tests/test_model_call_boundary.py | 1930 | c593a22d0668ea3deb578ba9a44eae2fc6db7cf578e157657374116c358b31ab | UNCHANGED | 0 | 0 |
| tests/test_no_model_calls.py | 11582 | 0b02170669d468fab1f08a00b8ac42a6e64eba8644232d43375a7e7746d4c8e3 | UNCHANGED | 0 | 0 |
| tests/test_phase1_approval.py | 7318 | 8b133a31c968c0a384aa1c36092c6cfe7e4abf5119011e54b79fcc1616d14a26 | NEW | 177 | 0 |
| tests/test_phase1_blocking_fixes.py | 12982 | 95870ecf060bc80373b289a2360826cadc8c8b7c511bf5505b80dd860027d189 | NEW | 293 | 0 |
| tests/test_phase1_github.py | 11002 | 0780d0145de83b7746a54f9b54cda7e229177b413876635f7dd72837fca3b26a | NEW | 247 | 0 |
| tests/test_phase2_acceptance.py | 9649 | 9dd1dcc1a2c3f2d67397a51abcb98ab585d148398e962fc4cf6900175e9eb2a5 | NEW | 209 | 0 |
| tests/test_phase2_cutover.py | 6315 | e00fca22d97dd86d9caf03262558ad90fee9c5bf46b19b5d47099638b4783507 | NEW | 143 | 0 |
| tests/test_phase2_ed25519.py | 11964 | d035526d5f4c2c6366220ffc00c02e1a4fd1ccb6af9c686bae63b3ea400a9323 | NEW | 246 | 0 |
| tests/test_phase2_notify.py | 8537 | 5aedc458b32b6805074203d5f0d9e8287150a35429fb0fb96b00dd2b09942483 | NEW | 207 | 0 |
| tests/test_phase3_gates.py | 14402 | 45a2b47b75dff2589761ec5edc3382186ee6cfa458ee83b4aee95b4ea0a0f640 | NEW | 336 | 0 |
| tests/test_phase3_trust_tool.py | 3186 | 272bd69b19c24a33a2d431af714d07b389fd2fe7fb3badf90781005e00044465 | NEW | 80 | 0 |
| tests/test_phase4_unattended.py | 16665 | a0ad6d11f5dd5031486e1c2bbe8fd7838379c6ffb2feacd2e6f226e473928d3b | NEW | 363 | 0 |
| tests/test_phase5_independence.py | 8803 | 25b3439b38c3ed1c47ae27a04d7fe76c0bd87d248be6ba8857bf5a74222385df | NEW | 194 | 0 |
| tests/test_phase5_shadow.py | 15562 | a8d87c01f2594ecd55d95c713541b99b117e7ee48fa7408bdb5fa7a013590002 | NEW | 387 | 0 |
| tests/test_phase5_signer.py | 9290 | 49fa97c677c8dfb243ef09552a673df1fc97061e3e4955ffed06c99ed6e177e6 | NEW | 189 | 0 |
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
| tools/approval_signer.py | 9277 | c4bb3ea6adaaaed3b274305b1b1e5d4d2ed42e885039fd1078237a50bb7d3f9d | NEW | 184 | 0 |
| tools/build_release.py | 7411 | 8d5d2a70c1e5377df33da5427beaaf4bbf6c7383c2d33195d790caa7b1f14282 | CHANGED | 2 | 2 |
| tools/trust_root_tool.py | 4197 | 2090579ed5450243a5642ab5bb6ba43cf58334a594f139c93dce2bfd31ce5697 | NEW | 101 | 0 |
| windows/auth_init.cmd | 211 | 12c93ad4c5f6fdc902aea8808d6d941c3193c80bae0b3df2fcc67ba557683102 | UNCHANGED | 0 | 0 |
| windows/recover.cmd | 209 | 2b07c8e8a171138a729649b1fcc277abc283f4017430206628c6ca13a4f0d881 | UNCHANGED | 0 | 0 |
| windows/run_scan.cmd | 206 | acaccf6a288766b73cdc0348473e1c3ea9456e6a8c1d5abb4a0f3868da3d7701 | UNCHANGED | 0 | 0 |
| windows/run_watch.cmd | 386 | a674441e82200c78a5065bbfb190a7b9906798c8c6949f4f4469914fa5b9a123 | UNCHANGED | 0 | 0 |
| windows/status.cmd | 205 | eca8223b56c18b5b183e96fb202ceb6e3b9347434b97ab4bc922c1dcaac10904 | UNCHANGED | 0 | 0 |

끝.
