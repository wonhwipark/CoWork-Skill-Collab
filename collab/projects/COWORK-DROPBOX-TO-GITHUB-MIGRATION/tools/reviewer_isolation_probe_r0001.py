#!/usr/bin/env python3
"""Egress probe for a candidate LOCAL reviewer environment (prototype r0001, stdlib only).

Question it answers: from THIS machine and account, can a process reach well-known external model or
code-hosting endpoints? A local reviewer is only acceptable under LOCAL_ONLY if it cannot.

What it does: DNS resolution and a bare TCP connect (no bytes are sent, no TLS, no API call) to each target, a
loopback positive control that must register as CONNECTED, a loopback negative control that must NOT, and a
look at proxy and model-endpoint environment variable NAMES (values are never read or printed).

What it cannot do: prove the absence of every other path (other ports, DNS tunnelling, a host-level proxy the
probe does not see). A passing result is NECESSARY, NOT SUFFICIENT; the organisation must still verify the
runtime's network policy. The evidence digest covers results only (no host name, user or path) and is meant to
be carried in the receipt as `runtime_attestation_sha256`.

Usage: python reviewer_isolation_probe_r0001.py [--target host:port ...]
Exit: 0 ISOLATED_BY_PROBE, 1 NOT_ISOLATED, 2 NOT_PROVEN.
"""
import argparse
import hashlib
import json
import os
import socket
import sys

DEFAULT_TARGETS = ["api.anthropic.com:443", "api.openai.com:443", "generativelanguage.googleapis.com:443",
                   "github.com:443", "example.com:443"]
PROXY_VARS = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")
ENDPOINT_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "OPENAI_API_KEY", "OPENAI_BASE_URL", "GOOGLE_API_KEY",
                 "OLLAMA_HOST")


def tcp_connect(host, port, timeout=3.0, resolve=socket.getaddrinfo, connect=socket.create_connection):
    """DNS_FAIL | CONNECTED | REFUSED_OR_UNREACHABLE | TIMEOUT. Nothing is ever sent."""
    try:
        resolve(host, port, type=socket.SOCK_STREAM)
    except OSError:
        return "DNS_FAIL"
    try:
        sock = connect((host, port), timeout=timeout)
    except socket.timeout:
        return "TIMEOUT"
    except OSError:
        return "REFUSED_OR_UNREACHABLE"
    sock.close()
    return "CONNECTED"


def loopback_controls(connect=tcp_connect):
    """A listening local port must register CONNECTED; a freshly closed one must not."""
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    open_port = listener.getsockname()[1]
    try:
        positive = connect("127.0.0.1", open_port)
    finally:
        listener.close()
    negative = connect("127.0.0.1", open_port)   # same port, now closed
    return positive == "CONNECTED" and negative != "CONNECTED"


def environment_names(environ=None):
    environ = os.environ if environ is None else environ
    return {"proxy_variables_set": sorted(n for n in PROXY_VARS if environ.get(n) and n != "NO_PROXY"),
            "model_endpoint_variables_present": sorted(n for n in ENDPOINT_VARS if environ.get(n))}


def run(targets, connect=tcp_connect, controls=loopback_controls, environ=None):
    results = {}
    for target in targets:
        host, _, port = target.rpartition(":")
        results[target] = connect(host, int(port))
    env = environment_names(environ)
    control_ok = controls()
    reachable = sorted(t for t, r in results.items() if r == "CONNECTED")
    if not control_ok:
        verdict = "NOT_PROVEN"
        reason = "the loopback positive/negative control failed, so the probe itself is not trusted"
    elif reachable:
        verdict, reason = "NOT_ISOLATED", "external endpoints are reachable"
    elif env["proxy_variables_set"]:
        verdict, reason = "NOT_ISOLATED", "a proxy is configured, so direct failures do not show the real egress"
    else:
        verdict, reason = "ISOLATED_BY_PROBE", "no listed endpoint was reachable (necessary, not sufficient)"
    body = {"schema": "REVIEWER_ISOLATION_PROBE_V1", "verdict": verdict, "control_ok": control_ok,
            "results": results, "reachable_count": len(reachable), "environment_names": env}
    evidence = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {**body, "reason": reason, "evidence_digest": evidence}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--target", action="append", help="host:port (repeatable); default is a built-in list")
    args = parser.parse_args(argv)
    report = run(args.target or DEFAULT_TARGETS)
    print(json.dumps(report, indent=2, sort_keys=True))
    return {"ISOLATED_BY_PROBE": 0, "NOT_ISOLATED": 1}.get(report["verdict"], 2)


if __name__ == "__main__":
    sys.exit(main())
