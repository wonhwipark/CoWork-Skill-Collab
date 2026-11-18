# 팀 위키형 UI v0.1.0 PRIVATE 게시·원격 검증 영수증

- 작성: 2026-11-19 KST
- 저장소/브랜치: wonhwipark/CoWork-Skill-Collab / main
- CONTENT_COMMIT: `17ac2b39ad01dc3e01df467ada698fbac8b5c399`
- UI_SOURCE_TREE: `6282918d60fed523dba2ec0868866eb502ef08b5`
- CONTENT: 소스/설계/연동/시험/화면 23파일, 구현 결과 MD, 개발 후보 ZIP
- VERIFY: **REMOTE_SOURCE_TREE_BLOB_AND_SIZE=PASS 23/23 / REMOTE_ZIP_EXACT_BYTES=PASS / REMOTE_ZIP_SHA256=PASS / REMOTE_ZIP_CRC=PASS / INTEGRATION_BODY=PASS**

| 대상 | 원격 위치 | bytes | SHA-256 |
|---|---|---:|---|
| ZIP | collab/packages/l1-workspace-wiki-ui_v0_1_0_1119.zip | 267140 | `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9` |
| 단일 HTML | collab/projects/L1-WORKSPACE-RAG-20261111-001/ui/viewer-wiki-ui_v0_1_0/L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html | 65344 | `119be5e0104fbcc22d0daa89b42c418eefd8f00cdb94534a6f3518c79de4ed9d` |
| INTEGRATION.md | collab/projects/L1-WORKSPACE-RAG-20261111-001/ui/viewer-wiki-ui_v0_1_0/INTEGRATION.md | 7899 | `a2e2c4ecd4a8bf954a3f04238d13952141495d12794e891ef5b962d3ec48dfa3` |

고정 content commit에서 원격 ZIP을 base64로 실제 읽어 로컬 완성본과 전체 bytes 동일 확인. CRC 재검사 PASS. 원격 UI subtree의 23개 blob SHA/크기를 로컬 파일과 전부 비교. ZIP 내부 파일별 SHA-256 manifest 22항목(자기 자신 제외)도 PASS. INTEGRATION 원문 전체 동일. 검증용 로컬 mirror 저장 과정이 추가한 끝 newline 1개는 전송 아티팩트로 분리했으며 원격 원문을 변경·정규화해 비교한 것이 아님.

최종 브라우저 자체시험 PASS 56/56, 정적 검사 PASS 19/19. 개발 후보 `development_not_for_deployment`. 실제 Linux 통합·API/인증/권한·doc-converter B형 원본·동료 공유·B1/B2/B3는 미검증/미실행. 신규 독립 코드 리뷰·REQUEST/서명/READY·유료 호출·PUBLIC 전송·호스트 설치 0. 기존 리뷰/영수증·Work/Evidence·그룹 Knowledge·서비스/운영 설정 불변.

후속 CURRENT/TRACKER/이 영수증의 metadata commit은 게시 후 별도 readback으로 확인하며 자기 commit을 미리 기록하지 않음. 다음 한 행동은 업무 GPT의 INTEGRATION.md 기반 기존 Linux Viewer G0 및 최소 읽기 연결.
