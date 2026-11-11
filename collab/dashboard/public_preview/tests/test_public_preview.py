"""Offline fail-closed tests: public preview must never leak PRIVATE data."""
import hashlib
import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "build.py"
spec = importlib.util.spec_from_file_location("cowork_public_preview_builder", MODULE)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PublicPreviewTests(unittest.TestCase):
    def test_explicit_synthetic_and_unapproved_marker(self):
        text = builder.render()
        self.assertIn('data-classification="SYNTHETIC_ONLY"', text)
        self.assertIn('data-release="NOT_APPROVED"', text)
        self.assertIn('실제 업무 현황', text)
        self.assertIn('배포 승인 전', text)

    def test_no_private_source_links_network_or_scripts(self):
        text = builder.render()
        for pattern in (r'https?://', r'<script\b', r'<iframe\b', r'<img\b',
                        r'<form\b', r'fetch\(', r'XMLHttpRequest',
                        r'github\.com', r'/SKILL-COLLAB', r'collab/projects/',
                        r'collab/requests/', r'collab/reviews/', r'collab/receipts/'):
            self.assertIsNone(re.search(pattern, text, flags=re.I), pattern)

    def test_offline_csp(self):
        text = builder.render()
        self.assertIn("default-src 'none'", text)
        self.assertIn("script-src 'none'", text)
        self.assertIn("connect-src 'none'", text)

    def test_no_dynamic_private_identifiers_or_fake_live_metrics(self):
        text = builder.render()
        for phrase in ("MIGRATION_NOT_CUTOVER", "HOST_APPLIED", "RECEIPT_1.md",
                       "REQUEST.md", "SHA-256", "winhwipark", "wonhwipark",
                       "DASHBOARD-AUTO", "L1-WORKSPACE", "GPT_DISPOSITION"):
            self.assertNotIn(phrase, text)
        self.assertNotRegex(text, r'\b(?:\d+\s*(?:건|개)\s*(?:완료|요청|리뷰))\b')

    def test_repeat_byte_identical_and_no_clock_dependent_content(self):
        a = builder.render().encode('utf-8')
        b = builder.render().encode('utf-8')
        self.assertEqual(hashlib.sha256(a).digest(), hashlib.sha256(b).digest())

    def test_synthetic_private_directory_does_not_enter_output(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            private = root / 'collab' / 'projects' / 'INTERNAL-SECRET'
            private.mkdir(parents=True)
            sentinel = 'CONFIDENTIAL_PROJECT_0123456789'
            (private / 'CURRENT.md').write_text(sentinel, encoding='utf-8')
            (root / 'README.md').write_text('token_very_secret_123', encoding='utf-8')
            out = root / 'staging' / 'index.html'
            count = builder.write(out)
            payload = out.read_bytes()
            self.assertEqual(count, len(payload))
            self.assertNotIn(sentinel.encode(), payload)
            self.assertNotIn(b'token_very_secret_123', payload)
            self.assertEqual(payload, builder.render().encode('utf-8'))

    def test_responsive_and_accessible_semantics(self):
        text = builder.render()
        for phrase in ('<html lang="ko">', '<main ', '<header>', '<section',
                       'aria-label=', '@media(max-width:760px)',
                       '<meta name="viewport"'):
            self.assertIn(phrase, text)

    def test_no_filename_or_env_input_to_renderer(self):
        self.assertEqual(builder.render.__code__.co_argcount, 0)
        self.assertEqual(builder.DATA_CLASSIFICATION, 'SYNTHETIC_ONLY')
        self.assertEqual(builder.RELEASE_GATE, 'NOT_APPROVED')


if __name__ == '__main__':
    unittest.main()
