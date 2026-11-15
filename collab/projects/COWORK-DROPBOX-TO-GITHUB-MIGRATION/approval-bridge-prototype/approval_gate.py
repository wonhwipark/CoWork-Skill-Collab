"""CoWork Approval Bridge isolated, side-effect-free policy prototype (v0.1).

NO GitHub/Telegram/Windows I/O, NO signer invocation, NO READY generation.
This is NOT an operating service. The host integration must durably reserve the
approval exactly once before calling its existing signer and must reconcile
remote publish results without calling a paid model.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
from typing import Literal


@dataclass(frozen=True)
class PinnedRequest:
    request_id: str
    revision: int
    request_sha256: str
    zip_sha256: str
    commit_a: str
    repo_id: str
    policy: str
    max_cost_cents: int
    max_calls: int


@dataclass(frozen=True)
class ApprovalOffer:
    pinned: PinnedRequest
    owner_user_id: int
    owner_chat_id: int
    sent_message_id: int
    challenge_sha256: str
    issued_at: int
    expires_at: int
    state: Literal["OFFERED", "CLAIMED", "CONSUMED", "CANCELLED"]


@dataclass(frozen=True)
class TelegramCallback:
    user_id: int
    chat_id: int
    message_id: int
    callback_data: str
    update_id: int


def offer_digest(challenge: str) -> str:
    """Hash only an unpredictable host-generated challenge, never a user name."""
    return sha256(challenge.encode("utf-8")).hexdigest()


def eligible(
    offer: ApprovalOffer,
    callback: TelegramCallback,
    current_request: PinnedRequest,
    now_epoch: int,
    consumed_update_ids: frozenset[int],
) -> tuple[bool, str]:
    """Validate a callback. Does not sign, write, or mark the callback consumed.

    The host MUST atomically reserve (request_id, revision, zip_sha256,
    approval_attempt) in a durable local store before any signature is made.
    A previously consumed Telegram update or approval reservation fails closed.
    """
    if offer.state != "OFFERED":
        return False, "ALREADY_USED_OR_CANCELLED"
    if not (offer.issued_at <= now_epoch < offer.expires_at):
        return False, "EXPIRED_OR_BAD_CLOCK"
    if not (0 < offer.expires_at - offer.issued_at <= 900):
        return False, "INVALID_TTL"
    if type(callback.user_id) is not int or type(callback.chat_id) is not int or type(callback.message_id) is not int:
        return False, "INVALID_TELEGRAM_IDS"
    if (callback.user_id, callback.chat_id, callback.message_id) != (
        offer.owner_user_id, offer.owner_chat_id, offer.sent_message_id
    ):
        return False, "WRONG_SENDER_OR_MESSAGE"
    if callback.update_id in consumed_update_ids:
        return False, "REPLAYED_UPDATE"
    if offer.pinned != current_request:
        return False, "REQUEST_CHANGED"
    if (offer.pinned.policy != "POLICY-STATIC-V1"
            or offer.pinned.max_cost_cents > 100
            or offer.pinned.max_cost_cents < 1
            or offer.pinned.max_calls != 1):
        return False, "UNAPPROVED_POLICY_OR_COST"
    if not (offer.pinned.request_id and offer.pinned.revision >= 1
            and offer.pinned.repo_id and offer.pinned.commit_a):
        return False, "INVALID_BINDING"
    if any(len(s) != 64 or any(c not in "0123456789abcdef" for c in s)
           for s in (offer.pinned.request_sha256, offer.pinned.zip_sha256)):
        return False, "BAD_HASH"
    if (not isinstance(callback.callback_data, str)
            or len(callback.callback_data.encode("utf-8")) > 64
            or not callback.callback_data.startswith("approve:")):
        return False, "BAD_CALLBACK"
    challenge = callback.callback_data[len("approve:"):]
    if not challenge or not compare_digest(offer.challenge_sha256, offer_digest(challenge)):
        return False, "BAD_CHALLENGE"
    return True, "LOCAL_ATOMIC_RESERVATION_REQUIRED"
