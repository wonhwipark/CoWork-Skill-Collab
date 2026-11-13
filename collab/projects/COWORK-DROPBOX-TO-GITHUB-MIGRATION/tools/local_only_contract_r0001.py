#!/usr/bin/env python3
"""LOCAL_ONLY review contract, prototype r0001 (design evidence, not a deployed protocol).

Under D2 the artifact (source ZIP) never leaves the organisation, so GitHub cannot carry it and cannot be used to
re-derive its SHA-256. GitHub carries only a control-plane record: an opaque id, a SALTED COMMITMENT to the
artifact digest, scope, policy, cost cap, nonce and expiry, signed by the approver. The salt travels with the
artifact over a local channel, so only a party that holds the artifact can prove it matches. The reviewer returns
a signed receipt that carries a digest of the (local) review text, never the text.

What this proves: field minimisation, binding between approval, artifact and receipt, expiry, replay and
duplicate-receipt rejection. What it cannot prove: that the reviewer really ran on-premises. `reviewer_locality`
is a signed CLAIM (ATTESTED_NOT_VERIFIED); the organisation must verify the runtime out of band.
Requires the `cryptography` package for Ed25519.
"""
from __future__ import annotations

import hashlib
import json
import re
import secrets
from datetime import datetime, timezone

REQUEST_SCHEMA = "LOCAL_ONLY_REVIEW_REQUEST_V1"
RECEIPT_SCHEMA = "LOCAL_ONLY_REVIEW_RECEIPT_V1"
COMMITMENT_DOMAIN = b"COWORK-LOCAL-ARTIFACT-V1\x00"
ALLOWED_LOCALITY = ("ON_PREM", "HUMAN")            # EXTERNAL_API is refused under LOCAL_ONLY
REQUEST_FIELDS = {"schema", "request_id", "opaque_artifact_id", "artifact_commitment", "review_scope", "policy_revision",
                  "cost_cap_usd", "nonce", "issued_at", "expires_at", "repo_id", "signer_key_id"}
RECEIPT_FIELDS = {"schema", "request_id", "artifact_commitment", "verdict", "reviewer_id", "reviewer_locality",
                  "result_sha256", "finding_counts", "issued_at", "reviewer_key_id"}
VERDICTS = ("PASS", "FAIL", "UNCERTAIN")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class ContractError(ValueError):
    """Any violation; the message is a stable code, never a path or a digest of the artifact."""


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def new_salt() -> str:
    return secrets.token_hex(32)


def new_opaque_id() -> str:
    return "art-" + secrets.token_hex(8)


def artifact_commitment(artifact_sha256: str, salt_hex: str) -> str:
    if not HEX64.fullmatch(artifact_sha256.lower()) or not re.fullmatch(r"[0-9a-f]{64}", salt_hex):
        raise ContractError("BAD_DIGEST_OR_SALT")
    return hashlib.sha256(COMMITMENT_DOMAIN + bytes.fromhex(salt_hex) + bytes.fromhex(artifact_sha256.lower())).hexdigest()


def _utc(text: str) -> datetime:
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ContractError("TIMEZONE_REQUIRED")
    return value.astimezone(timezone.utc)


def _keys(private_bytes=None, public_bytes=None):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    return Ed25519PrivateKey, Ed25519PublicKey


def _sign(document: dict, private_bytes: bytes) -> dict:
    Private, _ = _keys()
    signature = Private.from_private_bytes(private_bytes).sign(canonical(document))
    return {"document": document, "signature": signature.hex()}


def _verify(envelope: dict, public_keys: dict, key_field: str) -> dict:
    from cryptography.exceptions import InvalidSignature
    _, Public = _keys()
    document, signature = envelope.get("document"), envelope.get("signature")
    if not isinstance(document, dict) or not isinstance(signature, str):
        raise ContractError("MALFORMED_ENVELOPE")
    public = public_keys.get(document.get(key_field))
    if public is None:
        raise ContractError("UNKNOWN_KEY")
    try:
        Public.from_public_bytes(public).verify(bytes.fromhex(signature), canonical(document))
    except (InvalidSignature, ValueError):
        raise ContractError("BAD_SIGNATURE") from None
    return document


def make_request(*, request_id, opaque_artifact_id, commitment, policy_revision, cost_cap_usd, nonce, issued_at, expires_at,
                 repo_id, signer_key_id, signer_private: bytes) -> dict:
    doc = {"schema": REQUEST_SCHEMA, "request_id": request_id, "opaque_artifact_id": opaque_artifact_id,
           "artifact_commitment": commitment, "review_scope": "LOCAL_ONLY", "policy_revision": str(policy_revision),
           "cost_cap_usd": str(cost_cap_usd), "nonce": nonce, "issued_at": issued_at, "expires_at": expires_at,
           "repo_id": repo_id, "signer_key_id": signer_key_id}
    return _sign(doc, signer_private)


def check_request(envelope: dict, signer_keys: dict, *, now: datetime, seen_nonces: set) -> dict:
    doc = _verify(envelope, signer_keys, "signer_key_id")
    if set(doc) != REQUEST_FIELDS or doc["schema"] != REQUEST_SCHEMA or doc["review_scope"] != "LOCAL_ONLY":
        raise ContractError("UNEXPECTED_FIELDS_OR_SCOPE")
    if not _utc(doc["issued_at"]) <= now < _utc(doc["expires_at"]):
        raise ContractError("NOT_IN_VALIDITY_WINDOW")
    if doc["nonce"] in seen_nonces:
        raise ContractError("NONCE_REPLAY")
    seen_nonces.add(doc["nonce"])
    return doc


def bind_to_local_artifact(request_doc: dict, artifact_sha256: str, salt_hex: str) -> None:
    """Run where the artifact is: proves THIS file is the one the approver committed to."""
    if artifact_commitment(artifact_sha256, salt_hex) != request_doc["artifact_commitment"]:
        raise ContractError("ARTIFACT_DOES_NOT_MATCH_COMMITMENT")


def assert_publishable(envelope: dict, forbidden: list[str]) -> None:
    """Refuse to publish anything that mentions an artifact digest, size, name or local path."""
    text = canonical(envelope).decode("ascii").lower()
    for item in forbidden:
        if item and str(item).lower() in text:
            raise ContractError("FORBIDDEN_VALUE_PRESENT")


def make_receipt(*, request_doc, verdict, reviewer_id, reviewer_locality, review_text: bytes, finding_counts: dict,
                 issued_at, reviewer_key_id, reviewer_private: bytes) -> dict:
    doc = {"schema": RECEIPT_SCHEMA, "request_id": request_doc["request_id"],
           "artifact_commitment": request_doc["artifact_commitment"], "verdict": verdict, "reviewer_id": reviewer_id,
           "reviewer_locality": reviewer_locality, "result_sha256": hashlib.sha256(review_text).hexdigest(),
           "finding_counts": finding_counts, "issued_at": issued_at, "reviewer_key_id": reviewer_key_id}
    return _sign(doc, reviewer_private)


class ReceiptLedger:
    """One accepted receipt per request; a second one, even a valid one, is refused."""

    def __init__(self):
        self.accepted: set[str] = set()

    def accept(self, envelope: dict, reviewer_keys: dict, request_doc: dict, *, signer_key_id_of_reviewer_must_differ=True) -> dict:
        doc = _verify(envelope, reviewer_keys, "reviewer_key_id")
        if set(doc) != RECEIPT_FIELDS or doc["schema"] != RECEIPT_SCHEMA:
            raise ContractError("UNEXPECTED_FIELDS")
        if doc["request_id"] != request_doc["request_id"] or doc["artifact_commitment"] != request_doc["artifact_commitment"]:
            raise ContractError("RECEIPT_NOT_FOR_THIS_REQUEST")
        if doc["reviewer_locality"] not in ALLOWED_LOCALITY:
            raise ContractError("LOCALITY_NOT_ALLOWED_UNDER_LOCAL_ONLY")
        if doc["verdict"] not in VERDICTS or not HEX64.fullmatch(str(doc["result_sha256"])):
            raise ContractError("BAD_VERDICT_OR_RESULT_DIGEST")
        if signer_key_id_of_reviewer_must_differ and doc["reviewer_key_id"] == request_doc["signer_key_id"]:
            raise ContractError("REVIEWER_IS_THE_APPROVER")
        if doc["request_id"] in self.accepted:
            raise ContractError("DUPLICATE_RECEIPT")
        self.accepted.add(doc["request_id"])
        return doc
