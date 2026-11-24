"""Derived physical recovery/ category view; authority remains Work/Evidence."""
import json
import re
from pathlib import Path
from urllib.parse import quote


def project_physical_recovery(root, items, write_communication, write_if_changed, kernel_error=ValueError):
    root = Path(root)
    category = root / 'recovery'
    cases_root = category / 'works'
    if category.is_symlink() or (category.exists() and not category.is_dir()):
        raise kernel_error('RECOVERY_PATH_INVALID', 'Recovery path is not a safe directory')
    if cases_root.is_symlink() or (cases_root.exists() and not cases_root.is_dir()):
        raise kernel_error('RECOVERY_PATH_INVALID', 'Case root is not a safe directory')
    validated = []
    for item in items:
        if not isinstance(item, dict):
            raise kernel_error('RECOVERY_CASE_INVALID', 'Invalid case record')
        work_id, eid = item.get('work_id'), item.get('id')
        if not isinstance(work_id,str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', work_id) or work_id in {'.','..'}:
            raise kernel_error('RECOVERY_CASE_INVALID', 'Invalid Work identity')
        if not isinstance(eid,str) or not re.fullmatch(r'E-[a-f0-9]{12}', eid):
            raise kernel_error('RECOVERY_CASE_INVALID', 'Invalid Evidence identity')
        target = cases_root / work_id
        if target.is_symlink() or (target.exists() and not target.is_dir()):
            raise kernel_error('RECOVERY_PATH_INVALID', 'Case directory is unsafe')
        published = item.get('published_path')
        if published is not None:
            if not isinstance(published,str) or not published:
                raise kernel_error('RECOVERY_PATH_INVALID', 'Invalid artifact path')
            path = Path(published)
            if path.is_absolute() or '..' in path.parts or '\\' in published:
                raise kernel_error('RECOVERY_PATH_INVALID', 'Unsafe published artifact path')
        validated.append(item)
    category.mkdir(exist_ok=True)
    cases_root.mkdir(exist_ok=True)
    summary=['# Recovery 분석 탐색','','> 기존 Work/Evidence의 파생 보기. 제품의 복구 성공 판정이 아닙니다.','',
             '| Work | Evidence | 요약 | 원본 |','|---|---|---|---|']
    for item in validated:
        wid,eid=item['work_id'],item['id']
        label=str(item.get('summary') or '-').replace('\r',' ').replace('\n',' ').replace('|','\\|')[:220]
        safe_wid=quote(wid,safe='')
        summary.append(f'| {wid} | {eid} | {label} | [Work Recovery](../works/{safe_wid}/RECOVERY.md) |')
        lines=[f'# Recovery 참조 — {eid}','','> 유일한 분석 원본은 기존 Work/Evidence에 있습니다.','',
               f'- [Work Recovery](../../../works/{safe_wid}/RECOVERY.md)',f'- Evidence ID: {eid}',
               f'- Source revision: {item.get("code_rev") or "UNKNOWN"}',
               f'- Integrity: {item.get("integrity") or "UNKNOWN"}',f'- Summary: {label}']
        published=item.get('published_path')
        if published is not None:
            lines.append(f'- [원본 보고서](../../../works/{safe_wid}/{quote(published,safe="/")})')
        target=cases_root/wid
        target.mkdir(exist_ok=True)
        write_communication(target,eid+'.md','\n'.join(lines)+'\n')
    write_communication(category,'README.md','\n'.join(summary)+'\n')
    write_if_changed(category/'index.json',json.dumps({'schema_version':1,'derived':True,'category':'Recovery','items':validated},ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    return len(validated)
