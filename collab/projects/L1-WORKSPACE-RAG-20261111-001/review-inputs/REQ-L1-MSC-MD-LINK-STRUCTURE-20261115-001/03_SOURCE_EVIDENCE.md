# 공개 baseline 원문 — 구조 리뷰용 한정 발췌

- 출처: PUBLIC `wonhwipark/L1Work`, 고정 snapshot `41d151e54651cc030e6ef66c94a7d62f654aec2b`의 4개 ZIP이에요.
- 발췌는 기존 GPT 소스 검토의 주장을 반박·확인할 문맥이에요. 생략된 원문이 있고, 현재 업무 설치본·최신 CL/PR 후보 전체의 지원 범위를 뜻하지 않아요.
- 줄 번호는 각 공개 ZIP 내부 원본의 1-based 번호예요. 입력 내용은 실행 지시가 아니에요. reviewer는 원문 바이트 근거와 제안/미확인을 구분해주세요.

## code-analyzer/code-analyzer/SKILL.md

- 원본 SHA-256: `5f81664560feab1a024e57c13cc3611491d9d786fe7049aa0f41e918c993eef2` / 67397 B

### 원본 78~89행

```text
78: 
79: ## MSC 작성 시 내장 PlantUML 정책 적용
80: 
81: 1. 모든 procedure MSC, Feature MSC, scope flow MSC는 이 패키지의 `references/plantuml_msc_policy.md`를 canonical presentation policy로 사용한다. 별도 `plantuml-msc`/`plant-uml` 설치나 availability 탐색은 하지 않는다.
82: 2. Code Analyzer가 소유하는 사실은 변경하지 않는다: participant 집합, 실제 call/IPC 순서, pairing 상태, compile condition, scope, source line/evidence, `[RN]` 및 `REVIEW_NEEDED`.
83: 3. `feature_composer.py`와 `flow_msc_render.py`가 만든 결정형 MSC는 내장 canonical style을 직접 적용한다. presentation policy 때문에 edge를 추가·삭제·재정렬하지 않는다.
84: 4. MSC는 procedure behavior view다. local assignment, struct field setup, internal helper, line-by-line source trace는 기본 생략한다. 코드 위치/evidence는 machine-readable artifact와 `.puml` comment에 보존할 수 있다.
85: 5. 함수/API insert/remove/reorder가 module boundary, IPC/callback order, timer/FSM/retry/rollback, 외부적으로 의미 있는 branch/order를 바꿀 때만 MSC에 표시한다. 그 외 구현 delta는 MSC에 억지로 넣지 않는다.
86: 6. 미확정 behavior는 `[RN]`/`REVIEW_NEEDED`로 유지하고 confirmed message처럼 그리지 않는다.
87: 7. Fix discussion targeted 요청에서 Code Analyzer는 requested facts만 제공한다. 수정 방향 인터뷰/TO-BE 승인 owner는 `issue-analyzer`다.
88: 
89: 상세 계약: `references/plantuml_msc_integration.md`, `references/plantuml_msc_policy.md`, `references/code_analyzer_msc_contract.md`
```

## code-analyzer/code-analyzer/references/code_analyzer_msc_contract.md

- 원본 SHA-256: `5a0910245bd8c82ed32f729e8caed093e687b45719d67903abe552541eeb8935` / 1596 B

### 원본 1~44행

```text
1: # Code Analyzer MSC Contract
2: 
3: ## Ownership
4: 
5: Code-analyzer owns **code-confirmed procedure facts** and code-centric sequence visualization. It does not own the final fix-direction interview or approval gate.
6: 
7: ## Default outputs
8: 
9: When MSC materially improves understanding, emit semantic/code evidence that can produce:
10: - `AS_IS` — current code-confirmed procedure
11: - `FOCUSED` — trigger-to-fault or API-order detail when needed
12: - `CHANGE_IMPACT` — only when comparing a concrete proposed/actual code change
13: 
14: Do not create `TO_BE_USER_APPROVED`; that state belongs to issue-analyzer.
15: 
16: ## Evidence rules
17: 
18: Each visible step should map to code evidence where possible:
19: - file
20: - symbol/function
21: - line/range or stable anchor
22: - call/API/message
23: - evidence state (`CODE_CONFIRMED`, `RN`, etc.)
24: 
25: A report or prior analysis statement is not automatically `CODE_CONFIRMED`.
26: 
27: ## API change visibility
28: 
29: Show API insert/remove/reorder in MSC when it changes one or more of:
30: - module boundary interaction
31: - external ordering
32: - IPC REQ/CNF/callback ordering
33: - timer/FSM/retry/rollback behavior
34: - externally meaningful branch behavior
35: 
36: Otherwise omit it from MSC and record implementation detail separately.
37: 
38: ## Low-spec model rule
39: 
40: Prefer structured semantic MSC data and deterministic rendering. Do not ask the model to hand-write large PlantUML diagrams. Apply the embedded policy in `plantuml_msc_policy.md`.
41: 
42: ## Handoff to issue-analyzer
43: 
44: When invoked for a fix-discussion fact gap, return only the requested targeted facts plus evidence anchors. Do not independently select or approve a fix direction.
```

## doc-converter/doc-converter/scripts/msc_tool.py

- 원본 SHA-256: `b55b022db60220fa3ce6ae65dc36b63ed557f09b293509b89b69c88ecaa6cd44` / 61105 B

### 원본 287~332행

```python
287: def msc_view_text(payload: dict, results: list[dict], specs: dict[str,dict]) -> str:
288:     """Standalone human explanation without inventing findings or browser verification."""
289:     def safe(x: Any) -> str:
290:         from html import escape
291:         return escape(_clean_label(x),quote=False).replace("[", "\\[").replace("]", "\\]")
292:     lines = ["# MSC 동작 흐름 — " + safe(payload.get("issue_id") or "Work"), "",
293:              "> **그림 상태:** 로컬 canonical MSC 산출물 기준. 원격 파일 확인·브라우저 SVG 표시·시험 통과는 별도 검증이 필요합니다.", "",
294:              "## 이 그림에서 확인할 내용", "",
295:              "- **문제:** 현재 Work 근거 요약을 참조하세요. 이 패키지는 원인 확인 근거를 독립적으로 생성하지 않습니다.",
296:              "- **핵심 변경:** 아래 AS-IS/TO-BE 그림과 변경 표식을 비교하세요.",
297:              "- **기대 효과·영향:** 효과 미검증 · 영향 범위 확인 필요",
298:              "- **확인 수준:** canonical MSC package 생성 결과. 실제 코드·시험 확인 아님",
299:              "- **요청 사항:** 변경 순서와 누락된 예외 흐름을 검토하세요.", ""]
300:     for row in results:
301:         sp = specs.get(row["name"], {})
302:         kind = str(sp.get("kind", "OVERVIEW")).upper()
303:         label = "변경 전" if kind == "AS_IS" else "변경 후" if kind == "TO_BE" else "예외·집중 흐름" if kind == "FOCUSED" else "흐름"
304:         title = safe(sp.get("title") or row["name"])
305:         heading = title if title.startswith(label + " — ") else label + " — " + title
306:         if is_user_scenario(sp):
307:             phases = [str(x.get("label")) for x in sp.get("steps",[]) if isinstance(x,dict) and x.get("type")=="divider"]
308:             lines += ["**시나리오:** " + title, "**Phase:** " + (" → ".join(safe(x) for x in phases) or "시나리오 구간 미지정"),
309:                       "**근거 유형:** " + safe(sp.get("design_status") or "검증 상태 별도 확인 필요"),
310:                       "**소스 revision:** " + safe((sp.get("source_provenance") or {}).get("revision") or "미확인"), ""]
311:         lines += ["## " + heading, "",
312:                   "**시작 조건·범위:** " + safe(sp.get("start_condition") or "시작 조건 근거 미작성") + " · " + safe(sp.get("scope") or kind), ""]
313:         if row.get("svg"):
314:             lines += ["![" + title + " — " + label + " 순서도](" + quote(row["name"] + ".svg") + ")", ""]
315:         elif row.get("puml"):
316:             lines += ["> **그림 생성 미완료:** SVG가 확인되지 않았습니다. [canonical PUML](" + quote(row["name"] + ".puml") + ")", ""]
317:         else:
318:             lines += ["> **그림 생성 미완료:** 검증·렌더 결과를 확인하세요.", ""]
319:         explanation = sp.get("explanation") or sp.get("caption")
320:         lines += ["**흐름 설명:** " + (safe(explanation) if isinstance(explanation,str) and explanation.strip() else
321:                                        "호출 순서와 변경 이유에 대한 설명 근거 미작성. 아래 원본 step을 검토해야 합니다."), ""]
322:         marks = [(str(x.get("display_change")),str(x.get("chg_id") or x.get("change_ref")))
323:                  for x in sp.get("steps",[]) if isinstance(x,dict) and x.get("display_change")]
324:         if marks:
325:             lines += ["**변경 위치:** " + ", ".join(dict.fromkeys(a + " ("+b+")" for a,b in marks)), ""]
326:     lines += ["## 원본·추적 기준", "", "- [변경 전후 비교](MSC_DELTA.md)",
327:               "- [canonical 상세 추적](MSC_TRACEABILITY.json)",
328:               "- [게시용 manifest](MSC_PUBLIC_MANIFEST.json)",
329:               "- 실제 설계 확정·source_write 승인·동작 검증은 Work Ledger의 별도 기록이 기준입니다.", ""]
330:     return "\n".join(lines)
331: 
332: 
```

### 원본 829~903행

```python
829: def cmd_package(ns: argparse.Namespace) -> int:
830:     src = Path(ns.input).expanduser()
831:     try:
832:         payload = getattr(ns, "_payload", None)
833:         if payload is None:
834:             payload = _json_load(src)
835:     except ValueError as exc:
836:         print(json.dumps({"status":"failed","reason_code":"INPUT_INVALID","error":str(exc)},ensure_ascii=False)); return EXIT_INPUT
837:     if not isinstance(payload, dict) or payload.get("schema") != PACKAGE_SCHEMA:
838:         print(json.dumps({"status":"failed","reason_code":"PACKAGE_SCHEMA_INVALID","error":f"expected schema {PACKAGE_SCHEMA}"},ensure_ascii=False)); return EXIT_VALIDATION
839:     diagrams = payload.get("diagrams")
840:     if not isinstance(diagrams, list) or not diagrams:
841:         print(json.dumps({"status":"failed","reason_code":"DIAGRAMS_REQUIRED","error":"diagrams must be non-empty list"},ensure_ascii=False)); return EXIT_VALIDATION
842:     outdir = Path(ns.output_dir).expanduser().resolve()
843:     if outdir.exists() and any(outdir.iterdir()) and not ns.overwrite:
844:         print(json.dumps({"status":"failed","reason_code":"OUTPUT_DIR_NOT_EMPTY","error":str(outdir)},ensure_ascii=False)); return EXIT_CONFLICT
845:     outdir.mkdir(parents=True, exist_ok=True)
846:     if getattr(ns, "_payload", None) is not None:
847:         src = outdir / "MSC_CANONICAL_PACKAGE.json"
848:         _atomic_json(src, payload, overwrite=True)
849: 
850:     renderer = _find_renderer()
851:     diagram_results: list[dict[str, Any]] = []
852:     specs_by_name: dict[str, dict[str, Any]] = {}
853:     hard_fail = False
854:     render_skipped = False
855:     package_errors: list[dict[str, Any]] = []
856:     package_warnings: list[dict[str, Any]] = []
857:     package_change_marks = change_marks({str(i):r.get("spec") for i,r in enumerate(diagrams)
858:                                          if isinstance(r,dict) and isinstance(r.get("spec"),dict)})
859:     for index, row in enumerate(diagrams, 1):
860:         if not isinstance(row, dict):
861:             diagram_results.append({"name": f"diagram_{index}", "status":"INVALID", "errors":[{"code":"DIAGRAM_NOT_OBJECT","message":"diagram item must be object"}]}); hard_fail=True; continue
862:         name = re.sub(r"[^A-Za-z0-9_.-]+", "_", _clean_label(row.get("name") or f"diagram_{index}"))
863:         spec = row.get("spec")
864:         if not isinstance(spec, dict):
865:             diagram_results.append({"name": name, "status":"INVALID", "errors":[{"code":"SPEC_REQUIRED","message":"diagram.spec must be object"}]}); hard_fail=True; continue
866:         if profile_of(spec) in {"SIMPLE", "FOCUSED"} and (row.get("auto_simplify") or spec.get("auto_simplify")):
867:             spec, trace = simplify_spec(spec)
868:             # The input package remains canonical; this is the deterministic View.
869:             row["_communication_trace"] = trace
870:         for step in spec.get("steps", []):
871:             if isinstance(step,dict):
872:                 cid = str(step.get("chg_id") or step.get("change_ref") or "")
873:                 if cid in package_change_marks and str(step.get("change", "UNCHANGED")).upper() != "UNCHANGED":
874:                     step["display_change"] = package_change_marks[cid]
875:         specs_by_name[name] = spec
876:         validation = validate_spec(spec)
877:         vr = outdir / f"{name}.validation.json"
878:         _atomic_json(vr, validation, overwrite=True)
879:         result: dict[str, Any] = {"name": name, "kind": str(spec.get("kind","OVERVIEW")).upper(), "validation": str(vr), "valid": validation["valid"]}
880:         if not validation["valid"]:
881:             result["status"] = "INVALID"; result["errors"] = validation["errors"]; hard_fail=True; diagram_results.append(result); continue
882:         puml = outdir / f"{name}.puml"
883:         _atomic_text(puml, render_spec_to_puml(spec), overwrite=True)
884:         result["puml"] = str(puml); result["puml_sha256"] = _sha256(puml)
885:         svg = outdir / f"{name}.svg"
886:         render = _render_puml(puml, svg, timeout=ns.timeout)
887:         result["render"] = render
888:         if render["ok"]:
889:             result["svg"] = str(svg); result["status"] = "READY"
890:         elif ns.allow_unrendered:
891:             result["status"] = "PUML_READY_RENDER_SKIPPED"
892:             render_skipped = True
893:         else:
894:             result["status"] = render["status"]; hard_fail=True
895:         diagram_results.append(result)
896: 
897:     # Package-level readability: keep the relative order of shared participants
898:     # stable across AS-IS / PROBLEM / TO-BE diagrams. New participants may be
899:     # inserted, but existing participants must not swap positions.
900:     if specs_by_name:
901:         baseline_name = next((n for n,sp in specs_by_name.items() if str(sp.get("kind", "")).upper() == "AS_IS"), next(iter(specs_by_name)))
902:         baseline = [_clean_label(x.get("id")) for x in specs_by_name[baseline_name].get("participants", []) if isinstance(x, dict)]
903:         base_labels = {_clean_label(x.get("id")): _clean_label(x.get("label") or x.get("id")) for x in specs_by_name[baseline_name].get("participants", []) if isinstance(x, dict)}
```

### 원본 995~1032행

```python
995:     trace_rows = [{"diagram": row.get("name"), **trace} for row in diagrams if isinstance(row,dict)
996:                   for trace in (row.get("_communication_trace") or [])]
997:     _atomic_json(outdir / "MSC_TRACEABILITY.json", {"schema": "doc-converter/msc-traceability/v1",
998:         "source": "input canonical package", "abstract_mappings": trace_rows,
999:         "scenario_trace": payload.get("scenario_trace"),
1000:         "visible_step_sources": [{"diagram": name, "id": step.get("id"),
1001:                                   "source_refs": step.get("source_refs", []),
1002:                                   "source_step_ids": step.get("source_step_ids", []),
1003:                                   "evidence_status": step.get("evidence_status")}
1004:             for name, spec in specs_by_name.items() for step in spec.get("steps", [])
1005:             if isinstance(step,dict) and step.get("type", "message") in {"message","note"} and step.get("visible",True)]}, overwrite=True)
1006:     style_results = {name:style_validation(spec) for name,spec in specs_by_name.items()}
1007:     _atomic_json(outdir / "MSC_STYLE_VALIDATION.json", {"schema":"doc-converter/msc-package-style-validation/v1",
1008:         "diagrams":style_results, "valid":all(x["valid"] for x in style_results.values())},overwrite=True)
1009:     manifest["style_validation"] = str(outdir/"MSC_STYLE_VALIDATION.json")
1010:     _atomic_text(outdir / "MSC_VIEW.md", msc_view_text(payload, diagram_results, specs_by_name), overwrite=True)
1011:     if hard_fail:
1012:         manifest["status"] = "BLOCKED"; manifest["msc_ready"] = False; manifest["render_ready"] = False
1013:     manifest["msc_view"] = str(outdir / "MSC_VIEW.md")
1014:     manifest["traceability"] = str(outdir / "MSC_TRACEABILITY.json")
1015:     # Publication projection has no source path, local renderer command, diagnostics
1016:     # containing arbitrary bytes or private file/function references. The internal
1017:     # MSC_MANIFEST remains unchanged for local handoff/debug.
1018:     public_manifest = {
1019:         "schema": "doc-converter/msc-public-manifest/v1",
1020:         "status": manifest["status"],
1021:         "diagrams": [{"name":r["name"], "kind":r.get("kind"), "status":r.get("status"),
1022:                       "validation":r["name"]+".validation.json",
1023:                       "puml":r["name"]+".puml" if r.get("puml") else None,
1024:                       "svg":r["name"]+".svg" if r.get("svg") else None} for r in diagram_results],
1025:         "msc_view":"MSC_VIEW.md", "traceability":"MSC_TRACEABILITY.json",
1026:         "style_validation":"MSC_STYLE_VALIDATION.json",
1027:         "remote_verified":False, "browser_svg_verified":False,
1028:     }
1029:     _atomic_json(outdir/"MSC_PUBLIC_MANIFEST.json",public_manifest,overwrite=True)
1030:     if isinstance(change_map,list):
1031:         public_changes = [{"chg_id":x.get("chg_id") or x.get("change_ref"),
1032:                            "msc_step":x.get("msc_step"),
```

## doc-converter/doc-converter/scripts/doc_converter.py

- 원본 SHA-256: `51fab4de2ff6d785e39d416da716a70605f85f85b47fc2607c2f34c2f441edc9` / 65026 B

### 원본 476~496행

```python
476: def markdown_to_html(text: str, standalone: bool = True, title: str | None = None) -> tuple[str, list[str], list[str], dict[str, int]]:
477:     lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
478:     out: list[str] = []
479:     warnings: list[str] = []
480:     loss: list[str] = []
481:     counts = {"headings": 0, "tables": 0, "images": len(re.findall(r"!\[[^\]]*\]\([^)]+\)", text)), "links": len(re.findall(r"(?<!!)\[[^\]]+\]\([^)]+\)", text))}
482:     i = 0
483:     while i < len(lines):
484:         line = lines[i]
485:         if not line.strip():
486:             i += 1; continue
487:         fm = MD_FENCE.match(line)
488:         if fm:
489:             lang = fm.group(1).strip()
490:             body: list[str] = []; i += 1
491:             while i < len(lines) and not MD_FENCE.match(lines[i]):
492:                 body.append(lines[i]); i += 1
493:             if i >= len(lines):
494:                 warnings.append("unclosed fenced code block")
495:                 loss.append("unclosed_code_fence")
496:             else:
```

### 원본 978~1003행

```python
978: def cmd_msc_export(args: argparse.Namespace) -> int:
979:     adapter = load_storage_adapter()
980:     paths = [Path(x).expanduser().resolve() for x in args.puml]
981:     try:
982:         sources, warnings = adapter.explicit_puml_sources(paths, strict_puml=args.strict)
983:         payload = adapter.export_msc_markdown(
984:             sources, args.output_dir, index_path=args.index,
985:             manifest_path=args.manifest, warnings=warnings,
986:         )
987:     except Exception as exc:
988:         raise DocConverterError("MSC export failed: %s" % exc, EXIT_CONVERSION, "MSC_EXPORT_FAILED")
989:     payload.update({"tool":TOOL, "tool_version":VERSION, "status":"done"})
990:     print(json.dumps(payload, ensure_ascii=False) if args.json else "msc index: %s" % payload.get("index_markdown"))
991:     return EXIT_OK
992: 
993: # ---------------- publish ----------------
994: 
995: def auth_header() -> dict[str, str]:
996:     pat = os.environ.get("CONFLUENCE_PAT")
997:     if pat: return {"Authorization":"Bearer "+pat}
998:     user = os.environ.get("CONFLUENCE_USER"); pw = os.environ.get("CONFLUENCE_PASSWORD")
999:     if user and pw:
1000:         token = base64.b64encode((user+":"+pw).encode("utf-8")).decode("ascii")
1001:         return {"Authorization":"Basic "+token}
1002:     raise DocConverterError("Confluence credentials are not configured", EXIT_PUBLISH, "CONFLUENCE_AUTH_MISSING")
1003: 
```

## l1-fix-workflow/l1-fix-workflow/l1_fix_workflow/scenario_msc.py

- 원본 SHA-256: `cd669af77700c37acbf115a9cb4a906c13329d2f3e4b4ba830d9ca183eca92ff` / 4941 B

### 원본 40~74행

```python
40: def build_msc_handoff(mode: str, question: str, work_id: str, record: dict[str,Any],
41:                       *, focus: list[str]|None=None) -> dict[str,Any]:
42:     if mode not in MODES: raise ValueError('unsupported MSC mode')
43:     if not work_id: raise ValueError('work ID required')
44:     evidence=candidate_evidence(record)
45:     need_analysis=mode=='ANALYZE_AND_CREATE'
46:     view=('COMPARE' if mode=='COMPARE' else 'TO_BE' if mode=='CREATE_TO_BE' else 'AS_IS_OR_TO_BE_CONTEXT')
47:     return {
48:         'schema':'l1-workflow/msc-handoff/v1', 'work_id':work_id,
49:         'mode':mode, 'question':question, 'scenario_focus':focus or [],
50:         'view_kind':view, 'code_fact_authority':'code-analyzer',
51:         'code_analysis_required':need_analysis, 'reuse_existing_code_facts_first':not need_analysis,
52:         'evidence_candidates':evidence,'evidence_freshness':'UNVERIFIED',
53:         'source_scope_policy':'APPROVED_CODE_ROOT_BOUNDED_READONLY',
54:         'source_revision_digest_required':True, 'dirty_state_must_match':True,
55:         'context_scope':'CURRENT_VERIFIED_WORK_ONLY',
56:         'design_approval_from_work_only':True,
57:         'artifact_pipeline':{
58:             'analyze_when_required':{'provider':'code-analyzer','action':'behavior-doc','reuse_unverified_facts_as_confirmed':False},
59:             'facts_format':'behavior_facts.json and source anchors',
60:             'projection_policy':'ONLY_VERIFIED_IR; no raw .puml, no code facts auto-inference; trace internal steps',
61:             'ir_schema':'l1-scenario-ir/v1',
62:             'convert':{'provider':'doc-converter','action':'msc-scenario-adapt',
63:                        'package_action':'msc-package','one_shot_action':'msc-scenario-build','style':'L1_USER_SCENARIO_V1',
64:                        'profile':'L1_USER_SCENARIO','allow_unrendered':True,
65:                        'require_verified_scenario_ir':True, 'require_style_validation':True,
66:                        'require_traceability':True},
67:             'record':{'owner':'work-ledger-kernel','kind':'asis_msc',
68:                       'no_lifecycle_advance':True,'require_verified_manifest':True},
69:         },
70:         'publication':{'github_push':False,'approval_required':True},
71:         'blocked_on':['UNVERIFIED_WORK','UNREGISTERED_ROOT','PROVIDER_UNAVAILABLE','CODE_SCOPE_REQUIRED',
72:                       'STALE_SOURCE','MSC_SYNTAX_INVALID','MSC_STYLE_INVALID','SCENARIO_IR_REQUIRED'],
73:         'actual_execution':'NOT_STARTED',
74:     }
```

## l1-fix-workflow/l1-fix-workflow/l1_fix_workflow/msc_view.py

- 원본 SHA-256: `df5c9bc3d4c1c804dabfdfe2554995487f1374e4181d7b30ba6fabd976015006` / 19150 B

### 원본 298~324행

```python
298: def view_work_msc(kernel: Any, work_id: str, *, detail: bool=False, page: int=1) -> dict[str,Any]:
299:     """Read a single exact Work's latest byte-verified MSC evidence (never write)."""
300:     base={'read_only':True,'saved':False,'provider_executed':False,'code_analysis_executed':False,
301:           'converter_executed':False,'git_push':False,'jira_write':False,'work_state_changed':False,
302:           'action':'MSC_VIEW_READ_ONLY','view':'msc','effective_view':'msc','work_id':work_id}
303:     if not work_id:
304:         return {**base,'ok':False,'action':'MSC_WORK_ID_REQUIRED','user_summary':'MSC 조회에는 정확한 Work ID가 필요합니다.'}
305:     if not isinstance(work_id,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}',work_id) or '..' in work_id:
306:         return {**base,'ok':False,'action':'MSC_WORK_ID_INVALID','user_summary':'Work ID 형식이 안전하지 않습니다.'}
307:     try:
308:         record=kernel.load_record(work_id)
309:     except Exception:
310:         return {**base,'ok':False,'action':'MSC_WORK_NOT_FOUND','user_summary':'해당 Work를 찾지 못했습니다. 정확한 Work ID를 확인해 주세요.'}
311:     matches=[e for e in reversed(record.get('evidence_index') or [])
312:              if str(e.get('kind') or '').lower() in EVIDENCE_KINDS]
313:     if not matches:
314:         return {**base,'ok':False,'action':'MSC_SOURCE_REQUIRED',
315:                 'user_summary':f'[{work_id}] 등록된 MSC Evidence가 없습니다. 기존 .puml 또는 원본 MSC를 Work에 연결해야 조회할 수 있습니다.'}
316:     attempted=[]
317:     for e in matches:
318:         evidence_id=str(e.get('evidence_id') or e.get('id') or '')
319:         source=Path(str(e.get('path') or ''))
320:         if source.suffix.lower() not in {'.puml','.md','.txt','.json'}:
321:             attempted.append({'evidence_id':evidence_id,'blocker':'MSC_CANONICAL_PUML_REQUIRED'})
322:             continue
323:         raw,state=_safe_file(kernel,work_id,e)
324:         if state!='OK':
```

## l1-fix-workflow/l1-fix-workflow/SKILL.md

- 원본 SHA-256: `9b13fa463ac0e69e1faf936afde24b0c78ca43ad23f869d54f5407f33cc58faf` / 37460 B

### 원본 14~24행

```text
14: ## v1.6.66 — 기존 l1-github를 이용한 그룹 개발지식 조회 (개발 후보)
15: 
16: - `l1-fix-workflow group-knowledge status|lookup|read-body`를 추가한다. 사내 그룹 스킬 파일 없이 **기존 `l1-github repo-config`의 `knowledge` 역할**에서 `l1sw-dev-knowledge`의 호스트 checkout을 확인한 후, 검증된 로컬 Git HEAD의 Markdown을 읽기 전용으로 조회한다.
17: - 지식 본문은 `lookup` 반환 경로·SHA-256·커밋을 모두 고정해 명시 요청할 때만 읽는다. 역할/원격/브랜치 불일치, 경로 탈출, symlink Blob, 스냅샷 변경은 차단한다. 자동 fetch·pull·Git Push·권한 승격 없음.
18: - **그룹 스킬 자체의 지식 조회 API 연계 또는 Code Analyzer 자동 입력 주입을 완료했다고 주장하지 않는다.** 기존 개인 `module-library`/Code Analyzer/Work/Git 게시 방식은 보존한다. 그룹 지식은 참고 맥락으로만 사용한다.
19: - 운영 계정/내부 URL·원문은 사외로 반출하지 않는다. 상세 명령·미검증 조건: `docs/GROUP_KNOWLEDGE_L1_GITHUB_BRIDGE_v1666.md`.
20: 
21: ## v1.6.65 — 플랫폼 보호 범위·원문 보관 문서 보완
22: 
23: - v1.6.64 실행 로직을 유지한다. Windows O_NOFOLLOW 부재와 전용 ACL 설정/검사 미구현, 실제 DACL/상속 확인 조건, 원문 Run 보관/정리 기준을 명시했다. 자동 ACL 차단·원문 삭제 기능은 추가하지 않았다.
24: - `docs/KNOWLEDGE_BODY_INPUT_v1664.md`의 v1.6.65 보충과 `RELEASE_NOTES_v1_6_65.md`를 따른다. 독립 리뷰 007은 이전 코드 후보에 대한 정적 검토이며 새 버전의 사내 설치/정식 배포 승인이 아니다.
```

## work-ledger-kernel/work_ledger_kernel/work_ux.py

- 원본 SHA-256: `61f597a11bc797972a434bc684d814774797a333b2fcc4abb69198c46611f747` / 82800 B

### 원본 815~868행

```python
815:                 raise KernelError("WORK_DOCS_UNSAFE_PATH", "Work state directory is not safe")
816:             brief = self.brief_resume(wid)
817:             decisions = brief.get("decisions") or []
818:             docs: list[str] = []
819:             msc_artifacts: list[str] = []
820:             artifact_entries: dict[str,dict] = {}
821:             mapping_file = out_dir / MAP_PATH
822:             if mapping_file.is_symlink():
823:                 raise KernelError("ARTIFACT_MAP_INVALID", "Published artifact map is a symlink")
824:             if mapping_file.is_file():
825:                 try:
826:                     existing_map=json.loads(mapping_file.read_text(encoding="utf-8"))
827:                     if existing_map.get("schema_version") != 1 or existing_map.get("work_id") != wid:
828:                         raise ValueError('wrong map identity')
829:                     artifact_entries={e["evidence_id"]:e for e in existing_map.get("entries",[])}
830:                 except (ValueError,TypeError,KeyError,OSError):
831:                     raise KernelError("ARTIFACT_MAP_INVALID", "Published artifact map is invalid")
832: 
833:             for e in rec.get("evidence_index") or []:
834:                 source_rel = e.get("path")
835:                 if not source_rel:
836:                     continue
837:                 src = self.storage.work_dir(wid) / source_rel
838:                 # Never follow an Evidence path out of this Work (or a symlink).
839:                 safe_source = (isinstance(source_rel, str) and not Path(source_rel).is_absolute()
840:                                and '..' not in Path(source_rel).parts and not src.is_symlink()
841:                                and src.resolve().is_relative_to(self.storage.work_dir(wid).resolve()))
842:                 if safe_source and e.get("kind") != "change_provenance" and copy_small_evidence and src.is_file() and src.suffix.lower() in {".md", ".html", ".json", ".txt"} and src.stat().st_size <= max_copy_bytes:
843:                     category = evidence_category(e)
844:                     eid = str(e.get("id") or "")
845:                     try:
846:                         published = name_for(category, src.name.split("__",1)[-1], eid)
847:                     except ValueError as exc:
848:                         raise KernelError("ARTIFACT_NAME_INVALID", str(exc)) from exc
849:                     dst = out_dir / "artifacts" / category / published
850:                     artifact_rel = dst.relative_to(out_dir).as_posix()
851:                     digest=artifact_sha(src)
852:                     if e.get('sha256') and str(e['sha256']).lower() != digest:
853:                         raise KernelError('ARTIFACT_SOURCE_HASH_MISMATCH', 'Evidence bytes changed after Ledger registration')
854:                     old_mapping=artifact_entries.get(eid)
855:                     if old_mapping is not None and (old_mapping.get("published_path") != artifact_rel or
856:                                                    old_mapping.get("sha256") != digest):
857:                         raise KernelError("ARTIFACT_MAP_CONFLICT", "Existing published mapping differs; manual reconciliation required")
858:                     if dst.is_symlink() or (dst.exists() and artifact_sha(dst) != digest):
859:                         raise KernelError("ARTIFACT_DESTINATION_CONFLICT", "Published artifact already exists with different content")
860:                     copy_if_changed(src, dst)
861:                     artifact_entries[eid]={"evidence_id":eid,"published_path":artifact_rel,"sha256":digest}
862:                     docs.append(artifact_rel)
863:                     if src.suffix.lower() == '.md' and 'MSC_VIEW' in src.stem.upper():
864:                         msc_artifacts.append(artifact_rel)
865: 
866:             if artifact_entries:
867:                 write_if_changed(mapping_file, json.dumps({"schema_version":1,"work_id":wid,
868:                     "entries":sorted(artifact_entries.values(),key=lambda x:x['evidence_id'])},
```

### 원본 1021~1038행

```python
1021:                 if len(history)==2:history.append('- 변경 이력 없음')
1022:                 write_if_changed(out_dir/'CHANGE_HISTORY.md','\n'.join(history)+'\n')
1023:                 readme += ['','## Feature 요구사항/설계','',
1024:                            '- [요구사항](REQUIREMENTS.md)','- [코드 사실](CODE_FACTS.md)',
1025:                            '- [현재 설계](DESIGN_CURRENT.md)','- [변경 이력](CHANGE_HISTORY.md)',
1026:                            '- [결정 기록](decisions.md)','']
1027:             # Optional source-grounded design View. Missing CHG metadata is not invented.
1028:             if msc_artifacts:
1029:                 msc_lines = ["# MSC 흐름 안내 — " + _md(work_title, 150), ""] + summary_lines(shared)
1030:                 msc_lines += ["## 실제 생성된 canonical MSC", "",
1031:                               "> 이 문서는 실제 Evidence에서 복사한 MSC 설명을 연결합니다. 원격 게시·브라우저 렌더 검증을 의미하지 않습니다.", ""]
1032:                 msc_lines += ["- [변경 전후 MSC와 설명 보기]("+quote(path,safe='/')+")" for path in sorted(set(msc_artifacts))]
1033:                 msc_lines += ["", "## 확인할 내용", "", "- 시작 조건, 주요 변경 순서, 분리된 예외 흐름과 검증 근거를 확인하세요.", ""]
1034:                 write_communication(out_dir, 'MSC_VIEW.md', "\n".join(msc_lines))
1035:                 if (out_dir / 'MSC_VIEW.md').is_file():
1036:                     readme += ["", "## MSC 흐름", "", "- [변경 전후 그림 및 설명](MSC_VIEW.md)", ""]
1037:             impl_text = implementation_view(rec, shared)
1038:             if impl_text is not None:
```

## work-ledger-kernel/contracts/registry_v1.json

- 원본 SHA-256: `246b25f888c202ec2825e223236d2f3f766379985800aae355862ee12fc586ea` / 5690 B

### 원본 45~76행

```json
45:         "BUG",
46:         "BUG-NR",
47:         "FEATURE",
48:         "REFACTOR",
49:         "PERF",
50:         "MAINT",
51:         "TOOLING"
52:       ],
53:       "providers": [
54:         "code-analyzer"
55:       ],
56:       "evidence_kinds": [
57:         "asis_callflow",
58:         "asis_msc",
59:         "impact",
60:         "structure_metric",
61:         "behavior_delta_set"
62:       ]
63:     },
64:     {
65:       "stage": "specify",
66:       "capability": "specify",
67:       "profiles": [
68:         "BUG",
69:         "BUG-NR"
70:       ],
71:       "providers": [
72:         "issue-analyzer",
73:         "user"
74:       ],
75:       "evidence_kinds": [
76:         "spec_input"
```

