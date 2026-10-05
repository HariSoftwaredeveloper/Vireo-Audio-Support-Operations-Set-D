"""
Vireo Pulse - Single-Command Launcher
Usage:
    python run_tool.py           # Starts interactive web workbench on http://localhost:8000
    python run_tool.py --report  # Generates terminal executive briefing
    python run_tool.py --test    # Runs automated verification suite
"""

import sys
import os
import argparse
import uvicorn
from vireo_engine import data_store

def print_terminal_report():
    kpis = data_store.get_summary_kpis()
    root = data_store.get_shift_root_cause_analysis()
    sim = data_store.simulate_solution_impact()

    print("\n" + "=" * 78)
    print("  VIREO PULSE - SUPPORT OPERATIONS & SLA ROOT-CAUSE EXECUTIVE BRIEFING")
    print("=" * 78)
    print(f"Total Unique Tickets Analyzed : {kpis['total_tickets']:,} (11,816 raw minus 616 duplicates)")
    print(f"Pre-Reshuffle SLA Breach Rate : {kpis['pre_reshuffle_rate']}% (Jan 2025 - Jun 2025)")
    print(f"Post-Reshuffle SLA Breach Rate: {kpis['post_reshuffle_rate']}% (Jul 2025 - Jun 2026)")
    print(f"Total Post-Reshuffle Credits  : Rs {kpis['post_reshuffle_credits_inr']:,.2f} (Tripled in P&L)")
    print("-" * 78)
    print("CORE OPERATIONAL ROOT CAUSE (THE 'WALL OF RED'):")
    print("1. Indore night shift was dissolved on June 29, 2025 (zero night agents scheduled).")
    print("2. 24x7 Chat with 15-min SLA remained active. 100% of night chats (1,034/1,034) breached.")
    print("3. Helpdesk attributes breaches to resolving agents instead of creation shift.")
    print(f"4. 88.4% of Morning shift breaches (1,579 / 1,786) were created during unstaffed night hours.")
    print("5. Morning agents' true in-shift breach rate is 8.2%, completely matching Day shift (8.1%).")
    print("-" * 78)
    print("POLICY & FINANCIAL LEAKAGE AUDIT:")
    print(f"• Double-Recovery Orders (§5) : 95 orders received BOTH refund and replacement")
    print(f"• Double-Recovery Cash Leakage: Rs {kpis['double_recovery_leakage_inr']:,.2f}")
    print(f"• Internal Transfer Churn (§4): {kpis['total_transfers']:,} transfers @ Rs 305 = Rs {kpis['transfer_cost_inr']:,.2f}")
    print("-" * 78)
    print("BUSINESS GOAL & SAVINGS (ZERO HEADCOUNT CHANGE):")
    print(f"• Target Breach Rate          : Cut from {sim['baseline_breach_rate_pct']}% to {sim['projected_breach_rate_pct']}%")
    print(f"• SLA Credit Cash Savings/Qtr : Rs {sim['quarterly_sla_credit_savings_inr']:,.2f}")
    print(f"• Avoided Transfer Savings/Qtr: Rs {sim['quarterly_transfer_savings_inr']:,.2f}")
    print(f"• Total Net Savings / Quarter : Rs {sim['total_quarterly_savings_inr']:,.2f} (~Rs 9.28 Lakhs / year)")
    print(f"• Projected CSAT Recovery     : +0.35 points (from 2.79 to 3.50+ on overnight volume)")
    print("=" * 78 + "\n")

def run_tests():
    import unittest
    import test_suite
    suite = unittest.TestLoader().loadTestsFromModule(test_suite)
    unittest.TextTestRunner(verbosity=2).run(suite)

def start_server():
    print("\nStarting Vireo Pulse Workbench on http://localhost:8000 ...")
    print("Open your browser and navigate to http://localhost:8000\n")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vireo Pulse CLI & Workbench Runner")
    parser.add_argument("--report", action="store_true", help="Print executive terminal report")
    parser.add_argument("--test", action="store_true", help="Run automated test suite")
    parser.add_argument("--port", type=int, default=8000, help="Port to run server on")
    args = parser.parse_args()

    if args.report:
        print_terminal_report()
    elif args.test:
        run_tests()
    else:
        start_server()
