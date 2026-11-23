"""Offline regression tests for the repository metadata and contents URLs."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gpt_disposition_actions as actions


class RepositoryURLTests(unittest.TestCase):
    def check_url(self, path, expected):
        with patch.object(actions.urllib.request, 'urlopen') as open_url:
            response = open_url.return_value.__enter__.return_value
            response.status = 200
            response.read.return_value = b'{"private": false}'
            result = actions.github_json('GET', 'example/project', path, 'fixture')
        self.assertEqual(result, (200, {'private': False}))
        self.assertEqual(open_url.call_args.args[0].full_url, expected)

    def test_repository_metadata(self):
        self.check_url('', 'https://api.github.com/repos/example/project')

    def test_contents_path(self):
        self.check_url('contents/a%20b?ref=main',
                       'https://api.github.com/repos/example/project/contents/a%20b?ref=main')
