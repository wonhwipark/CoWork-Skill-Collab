import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gpt_disposition_telegram as mod

RID = 'REQ-ACTION-NOTIFY-R1-20261121'
ENV = {
    'COWORK_GPT_TELEGRAM_NOTIFY_ENABLED':'true',
    'GITHUB_REPOSITORY':mod.REPO,'GITHUB_REPOSITORY_ID':mod.REPO_ID,
    'GITHUB_REF':'refs/heads/main','GITHUB_TOKEN':'not-a-real-token',
    'COWORK_TELEGRAM_BOT_TOKEN':'123456789:'+'A'*35,
    'COWORK_TELEGRAM_CHAT_ID':'-1001234567890','GITHUB_RUN_ID':'123456789',
}
DISPOSITION={'verdict':'ACCEPT_WITH_CHANGE','work_id':'COWORK-TEST','request_id':RID}

class TestTelegram(unittest.TestCase):
    def test_default_off_has_no_effects(self):
        with patch.object(mod,'github') as api, patch.object(mod,'telegram_send') as bot:
            self.assertTrue(mod.run(RID,{}).startswith('SKIP'))
            api.assert_not_called();bot.assert_not_called()

    def test_missing_credentials_fail_before_access(self):
        with patch.object(mod,'github') as api:
            with self.assertRaises(mod.Blocked):mod.run(RID,{**ENV,'COWORK_TELEGRAM_BOT_TOKEN':''})
            api.assert_not_called()

    def test_invalid_request_fail_closed(self):
        with patch.object(mod,'github') as api:
            with self.assertRaises(mod.Blocked):mod.run('WRONG', ENV)
            api.assert_not_called()

    def test_sender_invoked_once_after_reservation(self):
        events=[]
        def fake_gh(method,path,token,*args):
            if 'RECEIPT.json' in path:return 404, {}
            return 404, {}
        def fake_claim(rel,token,content): events.append('claim:'+rel)
        def fake_send(bot,chat,msg):
            events.append('send')
            self.assertIn('수정 수용',msg)
            self.assertTrue(msg.startswith('🟢 [GPT 최종 판정 완료]\n'))
            self.assertNotIn('[Claude',msg)
            self.assertNotIn(bot,msg)
            self.assertNotIn(chat,msg)
            return 123
        with patch.object(mod,'checked_disposition',return_value=(DISPOSITION,b'{}')),\
             patch.object(mod,'github',side_effect=fake_gh),\
             patch.object(mod,'claim_only',side_effect=fake_claim),\
             patch.object(mod,'telegram_send',side_effect=fake_send):
            self.assertTrue(mod.run(RID,ENV).startswith('SENT'))
        self.assertEqual(len(events),3)
        self.assertIn('CLAIM',events[0]);self.assertEqual(events[1],'send');self.assertIn('RECEIPT',events[2])

    def test_claim_failure_prevents_send(self):
        with patch.object(mod,'checked_disposition',return_value=(DISPOSITION,b'{}')),\
             patch.object(mod,'github',return_value=(404,{})),\
             patch.object(mod,'claim_only',side_effect=mod.Blocked('CLAIM_FAILED')),\
             patch.object(mod,'telegram_send') as bot:
            with self.assertRaises(mod.Blocked):mod.run(RID,ENV)
            bot.assert_not_called()

    def test_duplicate_receipt_prevents_send(self):
        with patch.object(mod,'checked_disposition',return_value=(DISPOSITION,b'{}')),\
             patch.object(mod,'github',return_value=(200,{})),\
             patch.object(mod,'claim_only') as claim, patch.object(mod,'telegram_send') as bot:
            with self.assertRaises(mod.Blocked):mod.run(RID,ENV)
            claim.assert_not_called();bot.assert_not_called()

    def test_run_id_mismatch_prevents_send(self):
        with patch.object(mod,'get_json',side_effect=[(
                {'schema':'COWORK_GPT_DISPOSITION_V1',
                 'request_id':RID,'work_id':'COWORK-TEST','verdict':'ACCEPT',
                 'trust':'APPROVAL_SIGNATURE_VERIFIED_AND_DOCUMENT_FIELDS_MATCHED',
                 'claim_path':f'collab/reviews/{RID}/GPT_API_EXECUTION_CLAIM.json',
                 'work_claim_path':'collab/projects/COWORK-TEST/ONE_CYCLE_CLAIM.json',
                 'response_id':'resp-123'},b'{}'),
                 ({'schema':'COWORK_GPT_API_CLAIM_V1','github_run_id':'other'},b'{}'),
                 ({'schema':'COWORK_ONE_CYCLE_CLAIM_V1'},b'{}')]):
            with self.assertRaisesRegex(mod.Blocked,'DISPOSITION_NOT_FROM_THIS_RUN'):
                mod.checked_disposition(RID,'token','123456789')

if __name__=='__main__':unittest.main()
