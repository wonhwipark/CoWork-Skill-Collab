import copy
import hashlib
import unittest
from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import local_only_contract_r0002 as c

NOW = datetime(2026, 11, 14, 12, 0, tzinfo=timezone.utc)
ZIP_BYTES = b"pretend this is the confidential source archive"
ZIP_SHA = hashlib.sha256(ZIP_BYTES).hexdigest()


def keypair():
    key = Ed25519PrivateKey.generate()
    private = key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())
    public = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return private, public


class Setup(unittest.TestCase):
    def setUp(self):
        self.approver_priv, approver_pub = keypair()
        self.reviewer_priv, reviewer_pub = keypair()
        self.signer_keys = {"approver-1": approver_pub}
        self.reviewer_keys = {"reviewer-1": reviewer_pub}
        self.salt = c.new_salt()
        self.commitment = c.artifact_commitment(ZIP_SHA, self.salt)
        self.seen = set()
        self.request = self.make()

    def make(self, **override):
        args = dict(request_id="REQ-1", opaque_artifact_id=c.new_opaque_id(), commitment=self.commitment, policy_revision=1,
                    cost_cap_usd="0.00", nonce="nonce-0123456789", issued_at=(NOW - timedelta(minutes=1)).isoformat(),
                    expires_at=(NOW + timedelta(hours=12)).isoformat(), repo_id="repo-1", signer_key_id="approver-1",
                    signer_private=self.approver_priv)
        args.update(override)
        return c.make_request(**args)

    def receipt(self, request_doc, **override):
        args = dict(request_doc=request_doc, verdict="PASS", reviewer_id="local-reviewer", reviewer_locality="ON_PREM",
                    review_text=b"the local review text stays local", finding_counts={"blocking": 0, "suggestion": 2},
                    issued_at=NOW.isoformat(), reviewer_key_id="reviewer-1", reviewer_private=self.reviewer_priv,
                    runtime_attestation_sha256="ab" * 32)
        args.update(override)
        return c.make_receipt(**args)


class Commitment(Setup):
    def test_the_commitment_is_not_the_artifact_digest_and_hides_it(self):
        self.assertNotEqual(self.commitment, ZIP_SHA)
        self.assertNotEqual(self.commitment, c.artifact_commitment(ZIP_SHA, c.new_salt()))

    def test_the_holder_of_the_artifact_and_salt_can_bind_and_others_cannot(self):
        doc = c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=self.seen)
        c.bind_to_local_artifact(doc, ZIP_SHA, self.salt)
        with self.assertRaisesRegex(c.ContractError, "DOES_NOT_MATCH"):
            c.bind_to_local_artifact(doc, hashlib.sha256(b"another archive").hexdigest(), self.salt)
        with self.assertRaisesRegex(c.ContractError, "DOES_NOT_MATCH"):
            c.bind_to_local_artifact(doc, ZIP_SHA, c.new_salt())

    def test_guessing_the_digest_without_the_salt_does_not_confirm_it(self):
        guessed = c.artifact_commitment(ZIP_SHA, "00" * 32)
        self.assertNotEqual(guessed, self.commitment)

    def test_bad_digest_or_salt_is_refused(self):
        for digest, salt in (("zz", self.salt), (ZIP_SHA, "short")):
            with self.assertRaises(c.ContractError):
                c.artifact_commitment(digest, salt)


class Publishable(Setup):
    def test_the_published_record_contains_no_digest_size_name_or_path(self):
        c.assert_publishable(self.request, [ZIP_SHA, self.salt, str(len(ZIP_BYTES)), "source.zip", "C:\\Users"])

    def test_the_leak_check_catches_a_digest_or_a_path(self):
        leaky = copy.deepcopy(self.request)
        leaky["document"]["note"] = ZIP_SHA
        with self.assertRaisesRegex(c.ContractError, "FORBIDDEN"):
            c.assert_publishable(leaky, [ZIP_SHA])
        leaky["document"]["note"] = r"D:\secret\source.zip"
        with self.assertRaisesRegex(c.ContractError, "FORBIDDEN"):
            c.assert_publishable(leaky, ["source.zip"])

    def test_an_extra_field_is_refused_so_nothing_new_can_ride_along(self):
        env = copy.deepcopy(self.request)
        env["document"]["package_sha256"] = ZIP_SHA
        # re-sign with the approver key so only the field set, not the signature, is under test
        env = c._sign(env["document"], self.approver_priv)
        with self.assertRaisesRegex(c.ContractError, "UNEXPECTED_FIELDS"):
            c.check_request(env, self.signer_keys, now=NOW, seen_nonces=set())


class Request(Setup):
    def test_a_valid_request_passes_once(self):
        c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=self.seen)

    def test_any_changed_field_breaks_the_signature(self):
        for field, value in (("cost_cap_usd", "1.00"), ("artifact_commitment", "0" * 64), ("expires_at", "2099-01-01T00:00:00+00:00")):
            env = copy.deepcopy(self.request)
            env["document"][field] = value
            with self.assertRaisesRegex(c.ContractError, "BAD_SIGNATURE"):
                c.check_request(env, self.signer_keys, now=NOW, seen_nonces=set())

    def test_a_key_that_is_not_trusted_is_refused(self):
        other_priv, _ = keypair()
        env = self.make(signer_private=other_priv)
        with self.assertRaisesRegex(c.ContractError, "BAD_SIGNATURE"):
            c.check_request(env, self.signer_keys, now=NOW, seen_nonces=set())
        with self.assertRaisesRegex(c.ContractError, "UNKNOWN_KEY"):
            c.check_request(self.make(signer_key_id="nobody"), self.signer_keys, now=NOW, seen_nonces=set())

    def test_expired_and_not_yet_valid_requests_are_refused(self):
        late = NOW + timedelta(hours=13)
        with self.assertRaisesRegex(c.ContractError, "VALIDITY"):
            c.check_request(self.request, self.signer_keys, now=late, seen_nonces=set())
        with self.assertRaisesRegex(c.ContractError, "VALIDITY"):
            c.check_request(self.request, self.signer_keys, now=NOW - timedelta(hours=1), seen_nonces=set())

    def test_the_same_nonce_cannot_be_used_twice(self):
        c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=self.seen)
        with self.assertRaisesRegex(c.ContractError, "NONCE_REPLAY"):
            c.check_request(self.make(request_id="REQ-2"), self.signer_keys, now=NOW, seen_nonces=self.seen)


class Receipt(Setup):
    def setUp(self):
        super().setUp()
        self.doc = c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=self.seen)
        self.ledger = c.ReceiptLedger()

    def test_a_local_reviewer_receipt_is_accepted_and_carries_only_a_digest_of_the_text(self):
        env = self.receipt(self.doc)
        got = self.ledger.accept(env, self.reviewer_keys, self.doc)
        self.assertEqual(got["result_sha256"], hashlib.sha256(b"the local review text stays local").hexdigest())
        c.assert_publishable(env, ["the local review text stays local", ZIP_SHA])

    def test_a_second_receipt_for_the_same_request_is_refused_even_if_valid(self):
        self.ledger.accept(self.receipt(self.doc), self.reviewer_keys, self.doc)
        with self.assertRaisesRegex(c.ContractError, "DUPLICATE_RECEIPT"):
            self.ledger.accept(self.receipt(self.doc, verdict="FAIL"), self.reviewer_keys, self.doc)

    def test_a_receipt_claiming_an_external_api_reviewer_is_refused(self):
        with self.assertRaisesRegex(c.ContractError, "LOCALITY_NOT_ALLOWED"):
            self.ledger.accept(self.receipt(self.doc, reviewer_locality="EXTERNAL_API"), self.reviewer_keys, self.doc)

    def test_a_receipt_for_another_artifact_or_request_is_refused(self):
        other = c.check_request(self.make(request_id="REQ-9", nonce="nonce-other-000001",
                                          commitment=c.artifact_commitment(hashlib.sha256(b"x").hexdigest(), self.salt)),
                                self.signer_keys, now=NOW, seen_nonces=self.seen)
        with self.assertRaisesRegex(c.ContractError, "NOT_FOR_THIS_REQUEST"):
            self.ledger.accept(self.receipt(other), self.reviewer_keys, self.doc)

    def test_the_approver_cannot_review_its_own_request(self):
        self.reviewer_keys["approver-1"] = self.signer_keys["approver-1"]
        env = self.receipt(self.doc, reviewer_key_id="approver-1", reviewer_private=self.approver_priv)
        with self.assertRaisesRegex(c.ContractError, "REVIEWER_IS_THE_APPROVER"):
            self.ledger.accept(env, self.reviewer_keys, self.doc)

    def test_a_forged_receipt_is_refused(self):
        env = self.receipt(self.doc)
        env["document"]["verdict"] = "FAIL"
        with self.assertRaisesRegex(c.ContractError, "BAD_SIGNATURE"):
            self.ledger.accept(env, self.reviewer_keys, self.doc)

    def test_an_unknown_verdict_is_refused(self):
        with self.assertRaisesRegex(c.ContractError, "BAD_VERDICT"):
            self.ledger.accept(self.receipt(self.doc, verdict="MAYBE"), self.reviewer_keys, self.doc)


class Hardening(Setup):
    """Added for the threat model: persistence across restarts, zero cost, attestation, receipt window."""

    def test_a_local_only_request_with_a_nonzero_cost_cap_is_refused_even_when_properly_signed(self):
        for cap in ("1.00", "0.01", "0", "free"):
            with self.assertRaisesRegex(c.ContractError, "COST_NOT_ZERO"):
                c.check_request(self.make(cost_cap_usd=cap), self.signer_keys, now=NOW, seen_nonces=set())

    def test_a_receipt_without_a_runtime_attestation_digest_is_refused(self):
        doc = c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=set())
        for bad in ("", "not-hex", "ab" * 31):
            with self.assertRaisesRegex(c.ContractError, "RUNTIME_ATTESTATION"):
                c.ReceiptLedger().accept(self.receipt(doc, runtime_attestation_sha256=bad), self.reviewer_keys, doc)

    def test_a_receipt_issued_outside_the_request_window_is_refused(self):
        doc = c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=set())
        for when in (NOW - timedelta(days=1), NOW + timedelta(days=2)):
            with self.assertRaisesRegex(c.ContractError, "OUTSIDE_REQUEST_WINDOW"):
                c.ReceiptLedger().accept(self.receipt(doc, issued_at=when.isoformat()), self.reviewer_keys, doc)

    def test_replay_protection_survives_a_restart(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "state.json")
            first = c.State(path)
            doc = c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=set(), state=first)
            c.ReceiptLedger(first).accept(self.receipt(doc), self.reviewer_keys, doc)
            restarted = c.State(path)          # a new process reads the file
            with self.assertRaisesRegex(c.ContractError, "NONCE_REPLAY"):
                c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=set(), state=restarted)
            with self.assertRaisesRegex(c.ContractError, "DUPLICATE_RECEIPT"):
                c.ReceiptLedger(restarted).accept(self.receipt(doc), self.reviewer_keys, doc)

    def test_a_damaged_state_file_fails_closed_instead_of_starting_empty(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "state.json")
            open(path, "w").write("{ this is not json")
            with self.assertRaisesRegex(c.ContractError, "FAIL_CLOSED"):
                c.State(path)

    def test_the_state_file_holds_no_artifact_digest_commitment_or_review_text(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "state.json")
            st = c.State(path)
            doc = c.check_request(self.request, self.signer_keys, now=NOW, seen_nonces=set(), state=st)
            c.ReceiptLedger(st).accept(self.receipt(doc), self.reviewer_keys, doc)
            text = open(path).read()
            for secret in (ZIP_SHA, self.salt, self.commitment, "the local review text stays local"):
                self.assertNotIn(secret, text)


class SizeLeakCheck(Setup):
    def test_a_size_is_only_a_hit_when_it_is_a_whole_field_value_not_a_substring_of_hex(self):
        for _ in range(200):                 # random hex often contains any two-digit number
            c.assert_publishable(self.make(), [str(len(ZIP_BYTES))])
        leaky = self.make()
        leaky["document"]["size"] = str(len(ZIP_BYTES))
        with self.assertRaisesRegex(c.ContractError, "FORBIDDEN"):
            c.assert_publishable(leaky, [str(len(ZIP_BYTES))])


if __name__ == "__main__":
    unittest.main()
