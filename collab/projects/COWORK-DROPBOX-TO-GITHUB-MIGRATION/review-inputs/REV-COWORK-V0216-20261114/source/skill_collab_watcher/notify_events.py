"""Decide which audit events deserve a message, once each, and word them per provider.

The sender is injected. Nothing here talks to Telegram; tests pass a fake sender.

Delivery position is a watermark per "<provider>:<epoch>". A watermark must be
initialised explicitly (bootstrap) before anything is sent, so a fresh state can
never replay the whole audit history (C-2).
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

NOTIFY_EVENTS = (
    "COMPLETED", "FAILED", "REVIEW_UNCERTAIN", "UPLOAD_FAILED", "CONFLICT",
    "AUTH_REQUIRED", "REJECTED", "LEGACY_SIDECAR_BLOCKED", "PENDING_HELD",
    "CLAUDE_AUTH_REQUIRED", "USAGE_LIMIT_DEFERRED", "DAILY_BUDGET_BLOCKED", "DAILY_LIMIT_BLOCKED",
)


class NotifyNotInitialized(RuntimeError):
    """run_once was called for a provider/epoch that was never bootstrapped."""


def scope_key(provider: str, epoch: int) -> str:
    return f"{provider}:{epoch}"


@dataclass
class NotifyState:
    watermarks: dict[str, int] = field(default_factory=dict)
    delivered: set[str] = field(default_factory=set)

    @classmethod
    def load(cls, path: Path) -> "NotifyState":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(watermarks={k: int(v) for k, v in (data.get("watermarks") or {}).items()},
                   delivered=set(data.get("delivered", [])))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps({"watermarks": self.watermarks, "delivered": sorted(self.delivered)}),
                       encoding="utf-8")
        tmp.replace(path)

    def bootstrap(self, conn: sqlite3.Connection, provider: str, epoch: int, *,
                  legacy_last_id: int | None = None) -> bool:
        """Set the starting position once. Returns True when it was newly set.

        legacy_last_id is the position the running notifier has already reached
        (it only advances after Telegram accepted the message), so events up to
        it are never re-sent while later unsent events still are. Without it the
        position is the newest audit row: history is not replayed."""
        key = scope_key(provider, epoch)
        if key in self.watermarks:
            return False
        newest = conn.execute("SELECT COALESCE(MAX(id), 0) FROM audit_log").fetchone()[0]
        start = newest if legacy_last_id is None else min(int(legacy_last_id), newest)
        self.watermarks[key] = start
        return True


def read_legacy_last_id(path: Path) -> int | None:
    """last_id from the notifier that is already running, or None."""
    try:
        return int(json.loads(path.read_text(encoding="utf-8"))["last_id"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _split_key(key: str | None) -> tuple[str, str]:
    parts = (key or "").split("|")
    return (parts[0] or "?", parts[1] if len(parts) > 1 else "?")


def _location(provider: str, repo: str | None, request_id: str, revision: str) -> str:
    if provider == "github":
        if not repo:
            raise ValueError("a GitHub provider needs the repository name")
        path = f"collab/reviews/{request_id}/REVIEW_RESULT_{revision}.md"
        return f"GitHub {repo} {path}\nhttps://github.com/{repo}/blob/main/{path}"
    return f"Dropbox reviews/{request_id}/REVIEW_RESULT_{revision}.md"


def build_message(event: str, key: str | None, detail: str | None, provider: str, repo: str | None = None) -> str:
    if event == "REJECTED":
        return f"[요청 거부] {detail or ''}"
    if event == "PENDING_HELD":
        return f"[전환 보류 요청] {detail or ''}. 자동으로 처리하지 않고 보존했습니다."
    if event == "CLAUDE_AUTH_REQUIRED":
        return ("[Claude 로그인 필요] 리뷰 대기열을 멈췄습니다. 요청은 소모하지 않았고 모델도 호출하지 않았습니다. "
                f"PC에서 Claude Code에 다시 로그인하면 자동으로 재개됩니다. ({detail or ''})")
    if event == "USAGE_LIMIT_DEFERRED":
        return ("[사용량 한도] Claude 사용량 한도에 걸려 리뷰를 시작하지 못했습니다. 모델 작업은 하지 않았고 요청은 대기합니다. "
                f"한도가 풀리면 자동으로 이어서 실행합니다. ({detail or ''})")
    if event == "DAILY_BUDGET_BLOCKED":
        return "[일일 비용 상한] 오늘 한도에 도달해 새 리뷰를 시작하지 않습니다. 요청은 대기 상태로 보존됩니다."
    if event == "DAILY_LIMIT_BLOCKED":
        return "[일일 리뷰 횟수 상한] 오늘 한도에 도달해 새 리뷰를 시작하지 않습니다. 요청은 대기 상태로 보존됩니다."
    request_id, revision = _split_key(key)
    where = _location(provider, repo, request_id, revision)
    if event == "COMPLETED":
        return f"[리뷰 완료] {request_id} r{revision}\n위치: {where}\n결과와 영수증을 확인하고 GPT에 판정을 요청하세요."
    if event == "REVIEW_UNCERTAIN":
        return (f"[불확실] {request_id} r{revision}: 모델 호출 중 감시기가 끊겼습니다. "
                "자동 재실행하지 않았습니다. 새 revision을 발행해야 다시 리뷰됩니다.")
    if event == "FAILED":
        return f"[실패] {request_id} r{revision}: {detail or ''}"
    if event == "CONFLICT":
        return f"[충돌] {request_id} r{revision}: {detail or ''}. 기존 결과는 보존했습니다."
    if event == "UPLOAD_FAILED":
        return f"[게시 재시도 대기] {request_id} r{revision}: 모델은 다시 호출하지 않고 게시만 재시도합니다."
    if event == "LEGACY_SIDECAR_BLOCKED":
        return f"[자동 처리 차단] {request_id}: {detail or ''}"
    if event == "AUTH_REQUIRED":
        return f"[인증 필요] {provider} 인증을 PC에서 확인하세요."
    return f"[{event}] {request_id} r{revision}"


def check_stalled(conn: sqlite3.Connection, state: NotifyState, *, now: datetime, send,
                  max_age: timedelta = timedelta(minutes=15), persist=None) -> str | None:
    """Dead-man alert for unattended use: the watcher writes SCAN_START every cycle,
    so a stale newest SCAN_START means it stopped (crash, logoff, sleep). One alert
    per outage, and one message when it comes back. Returns "STALLED", "RECOVERED"
    or None. A database with no scan yet is not an outage."""
    row = conn.execute("SELECT MAX(ts) FROM audit_log WHERE event='SCAN_START'").fetchone()
    if not row or not row[0]:
        return None
    last = datetime.fromisoformat(row[0])
    stalls = sorted(m.split("|", 1)[1] for m in state.delivered if m.startswith("STALL|"))
    recovered = {m.split("|", 1)[1] for m in state.delivered if m.startswith("RECOVER|")}
    if now - last > max_age:
        if row[0] not in stalls:
            minutes = int((now - last).total_seconds() // 60)
            send(f"[감시기 정지] {minutes}분 동안 스캔 기록이 없습니다. PC가 꺼졌거나 감시기가 멈췄을 수 있습니다. "
                 "대기 중인 요청은 보존되며 재개되면 이어서 처리됩니다.")
            state.delivered.add(f"STALL|{row[0]}")
            if persist is not None:
                persist()
            return "STALLED"
        return None
    unrecovered = [s for s in stalls if s not in recovered and s != row[0]]
    if unrecovered:
        send("[감시기 재개] 스캔 기록이 다시 확인됩니다.")
        for s in unrecovered:
            state.delivered.add(f"RECOVER|{s}")
        if persist is not None:
            persist()
        return "RECOVERED"
    return None


def run_once(conn: sqlite3.Connection, state: NotifyState, *, provider: str, repo: str | None,
             send, epoch: int = 1, persist=None) -> int:
    """Send each new notifiable audit row once. The watermark moves only after a
    successful send, so a failed send is retried on the next run. persist (if
    given) is called after every send so a crash cannot repeat a delivered row."""
    key = scope_key(provider, epoch)
    if key not in state.watermarks:
        raise NotifyNotInitialized(f"{key} was never bootstrapped; refusing to replay history")
    rows = conn.execute(
        "SELECT id, event, processing_key, detail FROM audit_log WHERE id > ? ORDER BY id",
        (state.watermarks[key],),
    ).fetchall()
    sent = 0
    for row_id, event, pkey, detail in rows:
        if event in NOTIFY_EVENTS:
            marker = f"{key}|{event}|{pkey or detail or ''}"
            if marker not in state.delivered:
                send(build_message(event, pkey, detail, provider, repo))
                state.delivered.add(marker)
                sent += 1
        state.watermarks[key] = row_id
        if persist is not None:
            persist()
    return sent
