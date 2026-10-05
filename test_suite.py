"""
Vireo Pulse - Comprehensive Verification and Test Suite
Validates:
1. Data ingestion, deduplication, and schema integrity
2. Timezone conversion accuracy (UTC to IST)
3. Channel SLA target calculation and boundary tests
4. Shift assignment logic (Morning, Day, Night)
5. True root-cause attribution metrics (Night generation vs Morning handling)
6. Financial calculations (SLA credits, transfers, double recovery)
7. Simulation model correctness and bounds
8. AI Advisor fallback and live reasoning
"""

import unittest
import pandas as pd
import numpy as np
from vireo_engine import data_store, get_shift_ist, SLA_TARGETS_MIN, SLA_CREDIT_PER_BREACH_INR
from ai_advisor import ai_advisor

class TestVireoPulse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.store = data_store
        cls.tickets = data_store.tickets

    def test_01_deduplication_integrity(self):
        """Verify that Freshdesk re-import duplicates were properly identified and pruned."""
        raw_count = len(pd.read_csv('data/tickets.csv'))
        clean_count = len(self.tickets)
        self.assertEqual(raw_count, 11816, "Raw dataset should have 11,816 rows.")
        self.assertEqual(clean_count, 11200, "Clean deduplicated dataset must have exactly 11,200 unique tickets.")
        self.assertEqual(self.tickets['ticket_id'].nunique(), 11200, "All ticket IDs must be unique.")

    def test_02_timezone_conversion(self):
        """Verify UTC to IST (+5:30) conversion on sample ticket."""
        sample = self.tickets[self.tickets['ticket_id'] == 'TK-240001'].iloc[0]
        # created_at: 2025-01-01T06:12:00Z -> IST: 2025-01-01 11:42:00+05:30
        delta = sample['created_at_ist'] - sample['created_at_utc']
        self.assertEqual(delta.total_seconds(), 5.5 * 3600, "Timestamp shift must be exactly +5 hours and 30 minutes.")

    def test_03_sla_channel_targets(self):
        """Verify SLA targets against Support Policy Section 3:
        Chat: 15 min, Voice: 120 min, Social: 240 min, Email: 480 min.
        """
        for channel, target in SLA_TARGETS_MIN.items():
            channel_tickets = self.tickets[self.tickets['channel'] == channel]
            self.assertTrue((channel_tickets['sla_target_min'] == target).all(), f"Target mismatch for channel: {channel}")

    def test_04_sla_breach_calculation(self):
        """Verify SLA breach classification boolean logic and credit assignment."""
        breached = self.tickets[self.tickets['is_breached']]
        unbreached = self.tickets[~self.tickets['is_breached']]

        self.assertTrue((breached['frt_minutes'] > breached['sla_target_min']).all())
        self.assertTrue((unbreached['frt_minutes'] <= unbreached['sla_target_min']).all())
        self.assertTrue((breached['sla_credit_inr'] == 350.0).all())
        self.assertTrue((unbreached['sla_credit_inr'] == 0.0).all())

    def test_05_shift_classification(self):
        """Verify IST shift definitions:
        Morning: 06:00-14:00, Day: 14:00-22:00, Night: 22:00-06:00.
        """
        self.assertEqual(get_shift_ist(pd.Timestamp('2025-05-01 06:00:00')), 'Morning')
        self.assertEqual(get_shift_ist(pd.Timestamp('2025-05-01 13:59:59')), 'Morning')
        self.assertEqual(get_shift_ist(pd.Timestamp('2025-05-01 14:00:00')), 'Day')
        self.assertEqual(get_shift_ist(pd.Timestamp('2025-05-01 21:59:59')), 'Day')
        self.assertEqual(get_shift_ist(pd.Timestamp('2025-05-01 22:00:00')), 'Night')
        self.assertEqual(get_shift_ist(pd.Timestamp('2025-05-01 05:59:59')), 'Night')

    def test_06_night_chat_100_percent_breach(self):
        """Verify the core finding: 100% of night-created chats post-reshuffle breached."""
        post = self.tickets[self.tickets['is_post_reshuffle']]
        night_chats = post[(post['channel'] == 'chat') & (post['creation_shift'] == 'Night')]
        self.assertEqual(len(night_chats), 1034, "Post-reshuffle night chats must count 1,034.")
        self.assertEqual(night_chats['is_breached'].sum(), 1034, "All 1,034 post-reshuffle night chats must be breached.")
        self.assertEqual(night_chats['is_breached'].mean(), 1.0, "Night chat breach rate post-reshuffle must be 100%.")

    def test_07_morning_attribution_trap(self):
        """Verify that 88.4% of breaches resolved by Morning shift were created at Night."""
        analysis = self.store.get_shift_root_cause_analysis()
        m_audit = analysis['morning_shift_audit']
        self.assertEqual(m_audit['total_breaches_pinned_on_morning'], 1786)
        self.assertEqual(m_audit['breaches_inherited_from_night'], 1579)
        self.assertAlmostEqual(m_audit['percentage_inherited_from_night'], 88.4, delta=0.2)
        # Verify in-shift rate is ~8.2%
        self.assertAlmostEqual(m_audit['true_in_shift_breach_rate'], 8.2, delta=0.2)

    def test_08_double_recovery_audit(self):
        """Verify policy §5 violation: 95 orders with both refund and replacement."""
        leakage = self.store.get_double_recovery_audit()
        self.assertEqual(leakage['double_recovery_orders_count'], 95)
        self.assertGreater(leakage['total_leakage_inr'], 400000.0, "Total double recovery leakage should exceed 4 Lakhs.")

    def test_09_simulation_bounds(self):
        """Verify simulation returns valid non-negative business metrics."""
        sim = self.store.simulate_solution_impact(night_chat_policy='deflect_or_pause', intake_routing_accuracy_pct=80.0)
        self.assertLess(sim['projected_breach_rate_pct'], sim['baseline_breach_rate_pct'])
        self.assertGreater(sim['total_quarterly_savings_inr'], 100000.0)
        self.assertEqual(sim['headcount_change'], 0)

    def test_10_ai_advisor_fallback(self):
        """Verify AI advisor responds safely and accurately even without API key."""
        res = ai_advisor.ask("Why is the morning shift breaching so much?")
        self.assertIn("Morning Shift is NOT at Fault", res['answer'])
        self.assertIn("88.4%", res['answer'])

if __name__ == '__main__':
    print("=" * 70)
    print("RUNNING VIREO PULSE AUTOMATED VERIFICATION SUITE")
    print("=" * 70)
    unittest.main(verbosity=2)
