import copy
import json
import unittest
from pathlib import Path
from engine import simulate

DATA = json.loads(Path(__file__).with_name('examples.json').read_text())

class WorkflowTests(unittest.TestCase):
    def test_bad_fixture_flags_three_classes(self):
        report = simulate(DATA['rules'], DATA['record'])
        self.assertEqual({'missing_owner','duplicate_followup','cycle_detected'}, {f['code'] for f in report['findings']})
        self.assertEqual(0, report['external_actions'])

    def test_clean_rule_advances_and_assigns(self):
        rules = [
          {'id':'owner','event':'deal_created','action':'assign_owner','value':'fictional-team'},
          {'id':'stage','event':'deal_created','action':'set_stage','value':'qualified'},
          {'id':'follow','event':'stage_changed','action':'queue_followup','value':'day-2'},
        ]
        input_record = {'id':'x','stage':'new'}
        report = simulate(rules, input_record)
        self.assertEqual([], report['findings'])
        self.assertEqual('qualified', report['state']['stage'])
        self.assertEqual('fictional-team', report['state']['owner'])
        self.assertEqual('new', input_record['stage'])

    def test_duplicate_rule_id_fails(self):
        with self.assertRaises(ValueError):
            simulate([DATA['rules'][0], DATA['rules'][0]], DATA['record'])

    def test_unrecognized_action_fails(self):
        rule = dict(DATA['rules'][0], action='send_email')
        with self.assertRaises(ValueError):
            simulate([rule], DATA['record'])

    def test_step_limit(self):
        result = simulate(DATA['rules'], DATA['record'], max_steps=2)
        self.assertIn('step_limit', [f['code'] for f in result['findings']])

    def test_determinism(self):
        self.assertEqual(simulate(DATA['rules'], DATA['record']), simulate(copy.deepcopy(DATA['rules']), copy.deepcopy(DATA['record'])))

if __name__ == '__main__':
    unittest.main()
