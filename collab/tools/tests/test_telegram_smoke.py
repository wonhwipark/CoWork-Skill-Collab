"""Network-free tests for the manually gated Telegram smoke path."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import telegram_smoke as smoke
import gpt_disposition_telegram as bot

ENV={
    "COWORK_TELEGRAM_SMOKE_ENABLED":"true",
    "GITHUB_REPOSITORY":bot.REPO,
    "GITHUB_REPOSITORY_ID":bot.REPO_ID,
    "GITHUB_REF":"refs/heads/main",
    "GITHUB_EVENT_NAME":"workflow_dispatch",
    "GITHUB_ACTOR":"wonhwipark",
    "GITHUB_RUN_ATTEMPT":"1",
    "GITHUB_RUN_ID":"123456",
    "GITHUB_TOKEN":"mock-token",
    "COWORK_TELEGRAM_BOT_TOKEN":"123456789:"+("A"*35),
    "COWORK_TELEGRAM_CHAT_ID":"-1001234567890",
}

class TestSmoke(unittest.TestCase):
    def test_off_has_no_calls(self):
        with patch.object(bot,"github") as gh,patch.object(bot,"telegram_send") as send:
            self.assertTrue(smoke.run({}).startswith("SKIP"))
            gh.assert_not_called();send.assert_not_called()

    def test_actor_is_restricted(self):
        with patch.object(bot,"github") as gh:
            with self.assertRaisesRegex(bot.Blocked,"SMOKE_CONTEXT_NOT_ALLOWED"):
                smoke.run({**ENV,"GITHUB_ACTOR":"someoneelse"})
            gh.assert_not_called()

    def test_no_rerun(self):
        with patch.object(bot,"github") as gh:
            with self.assertRaisesRegex(bot.Blocked,"SMOKE_RERUN_FORBIDDEN"):
                smoke.run({**ENV,"GITHUB_RUN_ATTEMPT":"2"})
            gh.assert_not_called()

    def test_missing_secrets(self):
        with patch.object(bot,"github") as gh:
            with self.assertRaisesRegex(bot.Blocked,"TELEGRAM_SMOKE_SECRETS_MISSING"):
                smoke.run({**ENV,"COWORK_TELEGRAM_BOT_TOKEN":""})
            gh.assert_not_called()

    def test_success_claim_before_send_and_receipt(self):
        events=[]
        def claim(path,token,body):events.append(("claim",path))
        def send(token,chat,text):
            events.append(("send",text))
            self.assertIn("유료 모델 호출: 0회",text)
            self.assertTrue(text.startswith("🔔 [CoWork 연결 시험]\n"))
            self.assertIn("https://github.com/"+bot.REPO+"/actions/runs/"+ENV["GITHUB_RUN_ID"],text)
            self.assertNotIn("[리뷰",text)
            self.assertNotIn("[GPT",text)
            self.assertNotIn(token,text)
            return 42
        with patch.object(bot,"github",return_value=(404,{})),\
             patch.object(bot,"claim_only",side_effect=claim),\
             patch.object(bot,"telegram_send",side_effect=send):
            self.assertTrue(smoke.run(ENV).startswith("PASS"))
        self.assertEqual([x[0] for x in events],["claim","send","claim"])
        self.assertIn("CLAIM",events[0][1]);self.assertIn("RECEIPT",events[2][1])

    def test_claim_failure_sends_zero(self):
        with patch.object(bot,"github",return_value=(404,{})),\
             patch.object(bot,"claim_only",side_effect=bot.Blocked("CLAIM_FAIL")),\
             patch.object(bot,"telegram_send") as send:
            with self.assertRaises(bot.Blocked): smoke.run(ENV)
            send.assert_not_called()

    def test_existing_receipt_sends_zero(self):
        with patch.object(bot,"github",return_value=(200,{})),\
             patch.object(bot,"claim_only") as claim,\
             patch.object(bot,"telegram_send") as send:
            with self.assertRaises(bot.Blocked): smoke.run(ENV)
            claim.assert_not_called();send.assert_not_called()

if __name__=="__main__":
    unittest.main()
