import socket
import unittest

import reviewer_isolation_probe_r0001 as p

TARGETS = ["a.example:443", "b.example:443"]


def fake(outcome):
    return lambda host, port, *a, **k: outcome if isinstance(outcome, str) else outcome[host]


class Verdicts(unittest.TestCase):
    def run_probe(self, outcome, controls=True, environ=None):
        return p.run(TARGETS, connect=fake(outcome), controls=lambda: controls, environ=environ or {})

    def test_every_failure_kind_without_a_connection_is_isolated_by_probe(self):
        for kind in ("DNS_FAIL", "REFUSED_OR_UNREACHABLE", "TIMEOUT"):
            self.assertEqual(self.run_probe(kind)["verdict"], "ISOLATED_BY_PROBE")

    def test_one_reachable_endpoint_is_not_isolated(self):
        r = self.run_probe({"a.example": "DNS_FAIL", "b.example": "CONNECTED"})
        self.assertEqual((r["verdict"], r["reachable_count"]), ("NOT_ISOLATED", 1))

    def test_a_configured_proxy_is_not_isolated_even_if_direct_connects_fail(self):
        r = self.run_probe("DNS_FAIL", environ={"HTTPS_PROXY": "http://proxy.internal:3128"})
        self.assertEqual(r["verdict"], "NOT_ISOLATED")

    def test_an_empty_no_proxy_alone_is_not_a_proxy(self):
        self.assertEqual(self.run_probe("DNS_FAIL", environ={"NO_PROXY": "localhost"})["verdict"], "ISOLATED_BY_PROBE")

    def test_a_failed_control_makes_every_result_untrusted(self):
        self.assertEqual(self.run_probe("DNS_FAIL", controls=False)["verdict"], "NOT_PROVEN")

    def test_the_failed_control_wins_over_a_reachable_endpoint_verdict_ordering(self):
        self.assertEqual(self.run_probe("CONNECTED", controls=False)["verdict"], "NOT_PROVEN")

    def test_endpoint_variable_names_are_listed_but_never_their_values(self):
        secret = "sk-this-must-never-appear"
        r = self.run_probe("DNS_FAIL", environ={"ANTHROPIC_API_KEY": secret})
        self.assertEqual(r["environment_names"]["model_endpoint_variables_present"], ["ANTHROPIC_API_KEY"])
        self.assertNotIn(secret, str(r))

    def test_the_evidence_digest_is_stable_and_changes_with_the_result(self):
        a, b = self.run_probe("DNS_FAIL"), self.run_probe("DNS_FAIL")
        c = self.run_probe("TIMEOUT")
        self.assertEqual(a["evidence_digest"], b["evidence_digest"])
        self.assertNotEqual(a["evidence_digest"], c["evidence_digest"])

    def test_the_report_contains_no_host_identity(self):
        text = str(self.run_probe("DNS_FAIL")).lower()
        self.assertNotIn(socket.gethostname().lower(), text)


class Classification(unittest.TestCase):
    def test_dns_failure_timeout_refusal_and_success_are_distinguished(self):
        def boom(*a, **k):
            raise socket.gaierror("no dns")

        self.assertEqual(p.tcp_connect("x", 1, resolve=boom), "DNS_FAIL")

        def timeout(*a, **k):
            raise socket.timeout()

        self.assertEqual(p.tcp_connect("x", 1, resolve=lambda *a, **k: [], connect=timeout), "TIMEOUT")

        def refused(*a, **k):
            raise ConnectionRefusedError()

        self.assertEqual(p.tcp_connect("x", 1, resolve=lambda *a, **k: [], connect=refused), "REFUSED_OR_UNREACHABLE")

        class Sock:
            closed = False

            def close(self):
                Sock.closed = True

        self.assertEqual(p.tcp_connect("x", 1, resolve=lambda *a, **k: [], connect=lambda *a, **k: Sock()), "CONNECTED")
        self.assertTrue(Sock.closed)


class RealLoopback(unittest.TestCase):
    def test_the_real_loopback_controls_work_on_this_machine(self):
        self.assertTrue(p.loopback_controls())

    def test_a_real_listener_is_detected_as_connected_and_a_closed_port_is_not(self):
        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        self.assertEqual(p.tcp_connect("127.0.0.1", port), "CONNECTED")
        listener.close()
        self.assertNotEqual(p.tcp_connect("127.0.0.1", port), "CONNECTED")


if __name__ == "__main__":
    unittest.main()
