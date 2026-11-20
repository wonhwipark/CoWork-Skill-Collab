# CLAUDE v0.2.25 LIVE 백업 번들 생성 결과 (GPT·사용자 확인용)

- 작성: Windows Claude Code, 2026-11-20 KST(호스트 20:07). 근거: `LIVE_ENABLE_EXECUTION_REQUEST_V029_20261120_KST.md` §3-3, §5, 그리고 이번 실행 범위에 대한 사용자의 선택: **"백업 번들만", 위치 "skill-collab-watcher-dist 아래".**
- **결론:** 백업 번들 1개를 만들고 검증했다. **LIVE는 한 군데도 바꾸지 않았다.** watcher는 정지하지 않았고(계속 Running), v0.2.29 설치·설정·위임·`enabled_at`·가격 변경·재가동은 하지 않았다. `LIVE_EXECUTION=NOT_RUN`, `LIVE_ENABLE=NOT_RUN`. 신규 리뷰·REQUEST/READY·서명·모델 호출 0.

## 상태

```
BACKUP_BUNDLE=CREATED_AND_VERIFIED
LOCATION=D:\User\whpark\skill-collab-watcher-dist\backup_v0_2_25_install_20261120_200712 (Dropbox 표식 없음, D: 여유 810GB, 기존 backup_v0_1_4_src_20261104와 같은 관례)
FILES=117 (설치 트리 108 + 보호 파일 사본 3 + DB 스냅샷 1 + 작업 XML 2 + 매니페스트·정보·복원 안내 3)
MANIFEST_SHA256=d23b52068733ec7dcce95024f6f919a0e30147e00b502b3bd449d29406256d92 (모든 파일 재읽기 검증 통과)
INSTALL_TREE_SHA256=f691bcf808cbf81e9c2c2a9be65335e527c2df99ea4d54a427665e4c90045c9f == 운영 트리 (v0.2.25, 108개 파일)
DB_SNAPSHOT=온라인 백업 API로 일관 스냅샷, integrity_check=ok, jobs 9 / auto_claims 3 / auto_seen 11 / pending_requests 9 (운영 DB와 행 수 일치), SHA 111c85ab30de926759d1caebec78b65a228dd4ab7bfa126c3587ce13dd465fa5
PROTECTED_COPIES=위임(SHA ddead4e4…), 신뢰 루트 2개. 개인키·암호문(approver.key.enc, approver.pass.dpapi) 복사 0
CONFIG_SHA=fbce30a97c06f8d04e2e0029c731c41d2ccd87963196afe80279f10cf7509c27 (설치 트리 안의 reviewer.config.json)
TASK_XML=GitHub watcher·Notifier 내보내기 rc=0
LIVE_BEFORE_AFTER=설치 트리·설정·위임 SHA 동일, 작업 상태 동일(GitHub watcher·Notifier Running, Dropbox 시대 3개 Disabled), job 9 COMPLETED
```

## 요청서 §5 체크리스트에 미치는 영향

- **백업 저장 위치 지정 + 번들 매니페스트 검증:** 충족(위 위치, 매니페스트 검증 통과). 컷오버 직전에 설치 트리 SHA가 여전히 `f691bcf8…`인지 다시 확인하고, 다르면 번들을 새로 만든다.
- **롤백 책임자 확인:** 이 세션에서 확인하지 않았다(사용자 몫).
- **LIVE 운영 변경 승인, 보호 파일 수정 승인, 라벨 해제 기록:** 컷오버 단계 승인 때 확인한다. 이번에는 해당 없음.
- 번들은 **DB가 컷오버 후 변경되기 전의 스냅샷**이다. 컷오버 후 유료 job이 처리됐다면 DB는 되돌리지 않는다는 요청서 §4 규칙은 그대로이다.

## 알아둘 점

- 번들 폴더에는 `Authenticated Users:(M)`가 상속된다(설치 폴더와 같은 정도). 변조는 매니페스트 SHA로 감지할 수 있다. 권한을 더 좁히는 것은 선택 사항이며 이번에 바꾸지 않았다.
- 번들은 watcher가 실행 중인 상태에서 만들었다. DB는 온라인 백업 API로 일관성을 보장했고, 설치 트리와 설정은 SHA로 동일함을 확인했다.
- 복원 규칙과 옛 `skill-collab-watcher\.venv` 이동·삭제 금지는 번들 안 `README_RESTORE.txt`에 적어 두었다.
- 번들 자체(DB·위임 사본 포함)는 PRIVATE 저장소에 올리지 않았다. 이 문서와 스크립트만 게시했다.

## 다음 한 동작 (사용자)

전체 컷오버(정지 → 설치 → 등록 3.0 + 위임 3.0 + 신규 `enabled_at` → 검증 → 재가동)는 별도로 승인하실 때 진행한다. 그때 요청서 §5를 다시 확인한다. 지금은 아무 것도 보류 상태로 남아 있지 않다(watcher는 정상 가동 중).
