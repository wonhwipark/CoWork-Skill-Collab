"""Derived physical recovery/ category view; source is existing Work/Evidence."""
import json
import re
from pathlib import Path
from urllib.parse import quote


def project_physical_recovery(root, items, write_communication, write_if_changed, kernel_error=ValueError):
    directory = Path(root) / 'recovery'
    if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
        raise kernel_error('RECOVERY_PATH_INVALID', 'Recovery output path is not a safe directory')
    directory.mkdir(exist_ok=True)
    rows = []
    lines = ['# Recovery 분석 탐색', '', '> 기존 Work/Evidence에서 파생된 읽기 전용 목록. 제품 Recovery 성공 판정이 아닙니다.', '',
             '| Work | Evidence | 요약 | 원본 |', '|---|---|---|---|']
    for item in items:
        work_id = item['work_id']
        evidence_id = item['id']
        if not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', work_id) or work_id in {'.', '..'} or not re.fullmatch(r'E-[a-f0-9]{12}', evidence_id):
            raise kernel_error('RECOVERY_CASE_INVALID', 'Invalid Work or Evidence reference')
        encoded_work = quote(work_id, safe='')
        display = str(item.get('summary') or '-').replace('\r', ' ').replace('\n', ' ').replace('|', '\\|')[:220]
        lines.append(f'| {work_id} | {evidence_id} | {display} | [Work Recovery](../works/{encoded_work}/RECOVERY.md) |')
        case_dir = directory / 'works' / work_id
        if case_dir.is_symlink() or (case_dir.exists() and not case_dir.is_dir()):
            raise kernel_error('RECOVERY_PATH_INVALID', 'Case directory is not safe')
        case_dir.mkdir(parents=True, exist_ok=True)
        detail = [f'# Recovery 참조 — {evidence_id}', '', '> 파생 요약. 원본 Evidence가 유일한 분석 원본입니다.', '',
                  f'- Work: [{work_id}](../../../works/{encoded_work}/RECOVERY.md)',
                  f'- Evidence: {evidence_id}', f'- Source revision: {item.get("code_rev") or "UNKNOWN"}',
                  f'- Integrity: {item.get("integrity") or "UNKNOWN"}', f'- Summary: {display}']
        if item.get('published_path'):
            published = Path(item['published_path'])
            if published.is_absolute() or '..' in published.parts:
                raise kernel_error('RECOVERY_PATH_INVALID', 'Published path is unsafe')
            detail.append(f'- [원본 보고서](../../../works/{encoded_work}/{quote(published.as_posix(), safe="/")})')
        write_communication(case_dir, evidence_id + '.md', '\n'.join(detail) + '\n')
        rows.append(dict(item))
    write_communication(directory, 'README.md', '\n'.join(lines) + '\n')
    write_if_changed(directory / 'index.json', json.dumps({'schema_version': 1, 'derived': True, 'category': 'Recovery', 'items': rows}, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
    return len(rows)
