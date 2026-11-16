# 정적 소스 근거 — 비민감 관리 스킬
아래 bytes/hash는 실제 읽은 ZIP 기준. 발췌는 source snapshot의 행 번호이며 실행·설치·호스트 E3 확인이 아님.

| 입력 | bytes | SHA-256 | Git blob |
|---|---:|---|---|
| Workflow 1.6.70 candidate | 758117 | a3070d3cfd64d78da7a684f8d81fc35ea323c3667d539a61d16bf5ac6fe40878 | eff2956b70a99d3fb343bd86da470aa416753b9d |
| Kernel 0.7.43 candidate | 319793 | 0e178e651c2a53175a5ddce2dae68e07f11141b4a92a6b94be6126114c5ab95c | 970724a048e7b2823eddc0d9f50e1d4124e0b7ca |
| Converter 0.2.26 public | 169204 | b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c | dcdb89205ec16ab07f04866bfc514954a02f8bc4 |
| Code Analyzer 0.15.2 public | 513811 | 9786bb0deb86fe5faed69f7e0c5a343e661af195d745a63e759b577c8b39a669 | 6017f81f51e9747286825648599fc13770cb8903 |
| Issue Analyzer 0.11.50 public | 440609 | 76f5a233f050674132a5ed095fabbbe8265d64cab7f74d8149a413119de6ef03 | f830b6bb561c0c3c1ac11ffd63625ccbf2fdfc13 |

## E01. Workflow가 Kernel 문서 export를 호출
후보 l1-fix-workflow/l1_fix_workflow/github_docs.py:
```python
148: def docs_sync(kernel, *, repo_root: Optional[str], work_id: Optional[str], host_id: Optional[str], sync_trigger: str="explicit") -> dict[str,Any]:
203:     out=kernel.work_docs_export(resolved["repo_root"],work_id)
```

## E02. Workflow MSC handoff의 제공자·계획 경계
후보 l1_fix_workflow/scenario_msc.py, build_msc_handoff:
```python
50:         'view_kind':view, 'code_fact_authority':'code-analyzer',
58:             'analyze_when_required':{'provider':'code-analyzer','action':'behavior-doc','reuse_unverified_facts_as_confirmed':False},
62:             'convert':{'provider':'doc-converter','action':'msc-scenario-adapt',
63:                        'package_action':'msc-package','one_shot_action':'msc-scenario-build','style':'L1_USER_SCENARIO_V1',
64:                        'profile':'L1_USER_SCENARIO','allow_unrendered':True,
67:             'record':{'owner':'work-ledger-kernel','kind':'asis_msc',
73:         'actual_execution':'NOT_STARTED',
```
이 파일에서 PROCEDURE_FEATURE/--view-mode 전달은 없음. 모든 외부 caller까지 감사한 결과는 아니며, 계획을 실제 호출 성공으로 해석하지 않음.

## E03. Kernel의 게시명 매핑·복사·Work MSC 안내
후보 work_ledger_kernel/work_ux.py:
```python
721:                 copy_if_changed(src, dst)
886:                         published = name_for(category, src.name.split("__",1)[-1], eid)
889:                     dst = out_dir / "artifacts" / category / published
900:                     copy_if_changed(src, dst)
901:                     artifact_entries[eid]={"evidence_id":eid,"published_path":artifact_rel,"sha256":digest}
903:                     if src.suffix.lower() == '.md' and 'MSC_VIEW' in src.stem.upper():
904:                         msc_artifacts.append(artifact_rel)
1069:             if msc_artifacts:
1073:                 msc_lines += ["- [변경 전후 MSC와 설명 보기]("+quote(path,safe='/')+")" for path in sorted(set(msc_artifacts))]
1075:                 write_communication(out_dir, 'MSC_VIEW.md', "\n".join(msc_lines))
1077:                     readme += ["", "## MSC 흐름", "", "- [변경 전후 그림 및 설명](MSC_VIEW.md)", ""]
```
원본 bytes와 게시명 매핑이 분리돼 있으므로 MD 상대 링크가 재배치 후 자동 유효하다고 추정 금지.
Kernel 0.7.43은 knowledge를 exporter 출력으로 만들지 않고 실제 knowledge/README가 있을 때 루트 탐색 링크만 추가.

## E04. Converter의 목적 mode·조건부 HTML·상세 MD
공개 doc-converter/scripts/msc_tool.py:
```python
293:     procedure_mode = str(payload.get("view_mode") or "ISSUE").upper() == "PROCEDURE_FEATURE"
318:         if row.get("html"):
319:             lines += ["[MSC 확대 보기 (로컬 HTML)](" + quote(row["name"] + ".html") + ")", ""]
861:     view_mode = str(getattr(ns, "view_mode", None) or payload.get("view_mode") or "ISSUE").upper()
922:         if render["ok"] and view_mode == "PROCEDURE_FEATURE":
928:                 _atomic_text(html, build_html(svg, str(spec.get("title") or name), phases, context=spec), overwrite=True)
976:     delta_md = outdir / "MSC_DELTA.md"
1053:     _atomic_text(outdir / "MSC_VIEW.md", msc_view_text(payload, diagram_results, specs_by_name), overwrite=True)
```
msc_view_text는 ISSUE에서 문제/핵심 변경/영향 설명을, PROCEDURE_FEATURE에서 목적 중심 설명을 선택. AS-IS/TO-BE 각 spec의 입력 설명·SVG/존재하는 HTML 링크와 비교 문서를 표시. 원인·승인·현재 코드 사실을 생성 표현물로 추론하지 않음.

## E05. 분석의 의미·승인 owner
Code Analyzer SKILL: call/IPC/state/compile condition/source line은 소스 근거로 확인. fix discussion에서는 requested facts만 제공하고 수정 방향 인터뷰/TO-BE 승인은 issue-analyzer가 담당.
Issue Analyzer SKILL: AS-IS/PROBLEM 설명·수정 후보·사용자 질의/결정·TO-BE 확정은 기존 fix-discuss-context 계약, 결정형 PUML/SVG 변환은 Converter action.
완료 Plus 보고서가 유효하면 Workflow가 전체 분석을 반복하지 않는 기존 정책 유지.

## E06. 미확인
Updater/group writer 설치 원문·실제 폴더/ID·Work 없는 출처 저장 형식·공유 Git actor/credential/lock/CAS·업무 HTML URL/E3는 미확인.
설치된 writer/helper의 링크 재매핑 지원도 G0 확인 대상이며 '기능 없음'으로 단정하지 않음. 업무 L1 코드/실제 MSC/로그는 입력하지 않았음.
