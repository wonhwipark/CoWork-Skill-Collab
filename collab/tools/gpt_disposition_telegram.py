#!/usr/bin/env python3
"""One-shot Telegram notification AFTER a verified GPT disposition was published.

No model, signer, watcher, or review calls. No automated retry after a claimed send.
The two Telegram credentials are loaded only from GitHub Actions secrets.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

REPO = 'wonhwipark/CoWork-Skill-Collab'
REPO_ID = '1451933830'
RID = re.compile(r'REQ-[A-Z0-9][A-Z0-9-]{3,120}\Z')
WORK = re.compile(r'[A-Z][A-Z0-9_-]{2,100}\Z')
VERDICTS = {'ACCEPT', 'ACCEPT_WITH_CHANGE', 'REJECT', 'DEFER', 'NEED_INFO'}
BOT_TOKEN = re.compile(r'[0-9]{5,15}:[A-Za-z0-9_-]{25,100}\Z')
CHAT_ID = re.compile(r'-?[0-9]{1,22}\Z')


class Blocked(Exception):
    pass


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise Blocked(reason)


def github(method: str, relative: str, token: str, content: dict | None = None) -> tuple[int, dict]:
    url = f'https://api.github.com/repos/{REPO}/' + relative
    data = json.dumps(content, ensure_ascii=False).encode() if content is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/json',
        'User-Agent': 'cowork-gpt-telegram-v1',
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status, json.loads(response.read(150_000).decode())
    except urllib.error.HTTPError as e:
        if e.code in (404, 409, 422):
            return e.code, {}
        raise Blocked('GITHUB_HTTP_FAILURE') from None
    except (OSError, ValueError):
        raise Blocked('GITHUB_UNCERTAIN') from None


def get_json(relative: str, token: str) -> tuple[dict, bytes]:
    status, record = github('GET', 'contents/' + relative, token)
    require(status == 200 and record.get('encoding') == 'base64', 'REQUIRED_RECORD_NOT_VERIFIED')
    try:
        raw = base64.b64decode(record['content'], validate=False)
        require(0 < len(raw) <= 90000, 'RECORD_SIZE_INVALID')
        data = json.loads(raw)
    except (ValueError, KeyError, TypeError):
        raise Blocked('INVALID_RECORD_JSON') from None
    require(isinstance(data, dict), 'RECORD_NOT_OBJECT')
    return data, raw


def claim_only(path: str, token: str, content: dict) -> None:
    status, _ = github('GET', 'contents/' + path, token)
    require(status == 404, 'NOTIFICATION_ALREADY_CLAIMED_OR_UNVERIFIED')
    data = (json.dumps(content, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    status, _ = github('PUT', 'contents/' + path, token, {
        'message': 'notify: reserve one Telegram delivery [skip ci]',
        'branch': 'main', 'content': base64.b64encode(data).decode(),
    })
    require(status in (200, 201), 'NOTIFICATION_CLAIM_UNCERTAIN')
    _, raw = get_json(path, token)
    require(raw == data, 'NOTIFICATION_CLAIM_READBACK_FAILED')


def checked_disposition(rid: str, token: str, run_id: str) -> tuple[dict, bytes]:
    rel = f'collab/reviews/{rid}/GPT_DISPOSITION.json'
    disposition, raw = get_json(rel, token)
    work_id = disposition.get('work_id')
    require(disposition.get('schema') == 'COWORK_GPT_DISPOSITION_V1' and
            disposition.get('request_id') == rid and
            isinstance(work_id, str) and WORK.fullmatch(work_id) is not None and
            disposition.get('verdict') in VERDICTS and
            disposition.get('trust') == 'APPROVAL_SIGNATURE_VERIFIED_AND_DOCUMENT_FIELDS_MATCHED',
            'INVALID_DISPOSITION_FIELDS')
    claim_path = f'collab/reviews/{rid}/GPT_API_EXECUTION_CLAIM.json'
    work_claim_path = f'collab/projects/{work_id}/ONE_CYCLE_CLAIM.json'
    require(disposition.get('claim_path') == claim_path and
            disposition.get('work_claim_path') == work_claim_path,
            'DISPOSITION_CLAIM_PATH_MISMATCH')
    claim, _ = get_json(claim_path, token)
    work_claim, _ = get_json(work_claim_path, token)
    require(claim.get('schema') == 'COWORK_GPT_API_CLAIM_V1' and
            str(claim.get('github_run_id')) == run_id and
            claim.get('request_id') == rid and claim.get('work_id') == work_id and
            work_claim.get('schema') == 'COWORK_ONE_CYCLE_CLAIM_V1' and
            work_claim.get('request_id') == rid and work_claim.get('work_id') == work_id,
            'DISPOSITION_NOT_FROM_THIS_RUN')
    for key in ('package_sha256', 'processing_key', 'request_revision'):
        require(str(disposition.get(key)) == str(claim.get(key)) == str(work_claim.get(key)),
                'DISPOSITION_CHAIN_MISMATCH')
    require(isinstance(disposition.get('response_id'), str) and len(disposition['response_id']) > 4,
            'MODEL_RECEIPT_MISSING')
    return disposition, raw


def telegram_send(bot_token: str, chat_id: str, text: str) -> int:
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
    payload = json.dumps({'chat_id': chat_id, 'text': text,
                          'disable_web_page_preview': True}, ensure_ascii=False).encode()
    request = urllib.request.Request(url, data=payload, method='POST',
                                     headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            require(response.status == 200, 'TELEGRAM_SEND_NOT_CONFIRMED')
            reply = json.loads(response.read(65536))
    except (urllib.error.HTTPError, OSError, ValueError):
        # Never print exception/URL: Telegram token is embedded in the URL.
        raise Blocked('TELEGRAM_SEND_UNCERTAIN_NO_AUTO_RETRY') from None
    require(reply.get('ok') is True and isinstance(reply.get('result'), dict) and
            type(reply['result'].get('message_id')) is int, 'TELEGRAM_RESPONSE_UNVERIFIED')
    return reply['result']['message_id']


def run(rid: str, env: dict[str, str]) -> str:
    if env.get('COWORK_GPT_TELEGRAM_NOTIFY_ENABLED') != 'true':
        return 'SKIP: Telegram notifier OFF; no send, no writes'
    require(RID.fullmatch(rid) is not None, 'INVALID_REQUEST_ID')
    require(env.get('GITHUB_REPOSITORY') == REPO and
            env.get('GITHUB_REPOSITORY_ID') == REPO_ID and
            env.get('GITHUB_REF') == 'refs/heads/main', 'REPOSITORY_CONTEXT_MISMATCH')
    token = env.get('GITHUB_TOKEN', '')
    bot = env.get('COWORK_TELEGRAM_BOT_TOKEN', '')
    chat = env.get('COWORK_TELEGRAM_CHAT_ID', '')
    run_id = env.get('GITHUB_RUN_ID', '')
    require(bool(token) and bool(re.fullmatch(r'[0-9]{1,22}', run_id)), 'RUN_CONTEXT_MISSING')
    require(BOT_TOKEN.fullmatch(bot) is not None and CHAT_ID.fullmatch(chat) is not None,
            'TELEGRAM_SECRETS_MISSING_OR_INVALID')
    disp, raw = checked_disposition(rid, token, run_id)
    rel = f'collab/reviews/{rid}/GPT_TELEGRAM_NOTIFICATION_CLAIM.json'
    receipt_rel = f'collab/reviews/{rid}/GPT_TELEGRAM_NOTIFICATION_RECEIPT.json'
    code, _ = github('GET', 'contents/' + receipt_rel, token)
    require(code == 404, 'ALREADY_SENT_OR_RECEIPT_UNVERIFIED')
    claim_only(rel, token, {
        'schema': 'COWORK_GPT_TELEGRAM_CLAIM_V1', 'request_id': rid,
        'disposition_sha256': hashlib.sha256(raw).hexdigest(),
        'github_run_id': run_id,
        'state': 'SEND_ATTEMPT_RESERVED_DO_NOT_AUTO_RETRY',
        'created_at': datetime.now(timezone.utc).isoformat(),
    })
    link = f'https://github.com/{REPO}/blob/main/collab/reviews/{rid}/GPT_DISPOSITION.json'
    # No model-generated summary, customer data, bot token or chat ID in the message.
    label = {'ACCEPT': '수용', 'ACCEPT_WITH_CHANGE': '수정 수용',
             'REJECT': '거절', 'DEFER': '보류', 'NEED_INFO': '추가 확인 필요'}[disp['verdict']]
    msg = f'🟢 [GPT 최종 판정 완료]\nWork: {disp["work_id"]}\nRequest: {rid}\n판정: {label}\n결과: {link}\n\n모바일 ChatGPT 어느 창에서든 “CoWork 최신 판정 확인해줘”라고 질문하세요.'
    message_id = telegram_send(bot, chat, msg)
    claim_only(receipt_rel, token, {
        'schema': 'COWORK_GPT_TELEGRAM_RECEIPT_V1', 'request_id': rid,
        'github_run_id': run_id,
        'disposition_sha256': hashlib.sha256(raw).hexdigest(),
        'telegram_message_id': message_id,
        'state': 'TELEGRAM_SEND_ACKNOWLEDGED',
        'created_at': datetime.now(timezone.utc).isoformat(),
    })
    return 'SENT: Telegram acknowledgement and GitHub receipt verified (' + rid + ')'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--request-id', required=True)
    args = parser.parse_args()
    try:
        print(run(args.request_id, os.environ))
        return 0
    except Blocked as e:
        print('BLOCKED: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
