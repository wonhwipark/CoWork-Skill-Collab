"""The GitHub token file may be one plain line or the JSON form already on this PC. Synthetic values only."""
import json

import pytest

from skill_collab_watcher.cli import read_github_token
from skill_collab_watcher.transport_base import AuthRequired

SECRET = "synthetic-token-not-real-0123456789"


def write(tmp_path, text, name="t.txt"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_a_plain_one_line_file_still_works(tmp_path):
    assert read_github_token(write(tmp_path, SECRET + "\r\n"), "o/r") == SECRET


def test_a_bom_and_whitespace_are_ignored(tmp_path):
    p = tmp_path / "t.txt"
    p.write_bytes(b"\xef\xbb\xbf  " + SECRET.encode() + b"  \n")
    assert read_github_token(str(p), "o/r") == SECRET


def test_the_existing_json_form_is_read_without_a_copy(tmp_path):
    doc = {"token": SECRET, "repo": "Owner/Repo", "scope": "contents:write", "expires": "none"}
    assert read_github_token(write(tmp_path, json.dumps(doc)), "owner/repo") == SECRET   # repo compared case-insensitively


def test_json_without_a_repo_key_is_accepted(tmp_path):
    assert read_github_token(write(tmp_path, json.dumps({"token": SECRET})), "o/r") == SECRET


@pytest.mark.parametrize("text", ['{"token": ""}', '{"token": 5}', '{"other": "x"}', '{"token": "x"', '{ not json'])
def test_unusable_json_is_refused_and_the_message_never_shows_the_content(tmp_path, text):
    with pytest.raises(AuthRequired) as err:
        read_github_token(write(tmp_path, text), "o/r")
    assert "token\": " not in str(err.value) and SECRET not in str(err.value)


def test_a_token_file_for_another_repository_is_refused(tmp_path):
    with pytest.raises(AuthRequired, match="different repository") as err:
        read_github_token(write(tmp_path, json.dumps({"token": SECRET, "repo": "other/repo"})), "o/r")
    assert SECRET not in str(err.value)


def test_missing_or_unset_file_is_auth_required(tmp_path):
    with pytest.raises(AuthRequired):
        read_github_token(str(tmp_path / "nope.txt"), "o/r")
    with pytest.raises(AuthRequired):
        read_github_token(None, "o/r")
