#!/usr/bin/env python3
"""Manually-triggered, model-free one-shot Telegram connectivity smoke test.

This is NOT a review, READY, GPT disposition, or automatic notifier.
No retries. A per-GitHub-run CREATE_ONLY claim is written before sending.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone

import gpt_disposition_telegram as bot

WORK = "COWORK-DROPBOX-TO-GITHUB-MIGRATION"
EXPECTED_ACTOR = "wonhwipark"


def run(env: dict[str, str]) -> str:
    if env.get("COWORK_TELEGRAM_SMOKE_ENABLED") != "true":
        return "SKIP: Telegram smoke disabled; zero sends and zero writes"

    bot.require(env.get("GITHUB_REPOSITORY") == bot.REPO
                and env.get("GITHUB_REPOSITORY_ID") == bot.REPO_ID
                and env.get("GITHUB_REF") == "refs/heads/main"
                and env.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
                and env.get("GITHUB_ACTOR") == EXPECTED_ACTOR, "SMOKE_CONTEXT_NOT_ALLOWED")
    bot.require(env.get("GITHUB_RUN_ATTEMPT") == "1", "SMOKE_RERUN_FORBIDDEN")
    run_id = env.get("GITHUB_RUN_ID", "")
    token = env.get("GITHUB_TOKEN", "")
    secret = env.get("COWORK_TELEGRAM_BOT_TOKEN", "")
    chat = env.get("COWORK_TELEGRAM_CHAT_ID", "")
    bot.require(re.fullmatch(r"[0-9]{1,22}", run_id) is not None and bool(token), "RUN_TOKEN_MISSING")
    bot.require(bot.BOT_TOKEN.fullmatch(secret) is not None
                and bot.CHAT_ID.fullmatch(chat) is not None, "TELEGRAM_SMOKE_SECRETS_MISSING")

    base = f"collab/projects/{WORK}/telegram-smoke"
    claim = f"{base}/RUN-{run_id}-CLAIM.json"
    receipt = f"{base}/RUN-{run_id}-RECEIPT.json"
    status, _ = bot.github("GET", "contents/" + receipt, token)
    bot.require(status == 404, "SMOKE_ALREADY_DELIVERED_OR_UNVERIFIED")

    bot.claim_only(claim, token, {
        "schema": "COWORK_TELEGRAM_SMOKE_CLAIM_V1",
        "github_run_id": run_id,
        "state": "ONE_SEND_RESERVED_NO_AUTO_RETRY",
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    # Fixed, non-review text: never leak secrets, source, customer data or review content.
    run_url = f"https://github.com/{bot.REPO}/actions/runs/{run_id}"
    message = ("🔔 [CoWork 연결 시험]\n"
               f"GitHub Actions Run: {run_id}\n"
               f"결과 링크: {run_url}\n"
               "유료 모델 호출: 0회\n"
               "리뷰/판정 실행: 없음\n"
               "수동 연결 시험 메시지입니다.")
    msg_id = bot.telegram_send(secret, chat, message)
    bot.claim_only(receipt, token, {
        "schema": "COWORK_TELEGRAM_SMOKE_RECEIPT_V1",
        "github_run_id": run_id,
        "telegram_message_id": msg_id,
        "state": "SEND_ACKNOWLEDGED",
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return "PASS: isolated model-free Telegram smoke acknowledged, run=" + run_id


def main() -> int:
    try:
        print(run(os.environ))
        return 0
    except bot.Blocked as e:
        print("BLOCKED: " + str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
