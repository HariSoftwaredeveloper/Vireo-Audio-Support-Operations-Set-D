"""
Vireo AI Advisor Module
Provides generative AI diagnostics, executive briefing generation, and ticket root cause insights.
Integrates with Google Gemini API when GEMINI_API_KEY is available, with an expert
deterministic decision-intelligence fallback when running offline or without credentials.
"""

import os
import json
from typing import Dict, Any, List, Optional
from vireo_engine import data_store

class VireoAIAdvisor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.gemini_client = None
        self._init_gemini()

    def _init_gemini(self):
        if self.api_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[AI Advisor] Gemini init warning: {e}. Falling back to rule engine.")
                self.gemini_client = None

    def ask(self, query: str, context_filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Answer executive queries using Gemini or heuristic expert engine."""
        kpis = data_store.get_summary_kpis()
        root_cause = data_store.get_shift_root_cause_analysis()
        sim = data_store.simulate_solution_impact()

        prompt_context = f"""
You are the Lead Support Operations AI Advisor for Vireo Audio.
Key Operational Telemetry (Jan 2025 - Jun 2026):
- Total Tickets: {kpis['total_tickets']:,}
- Pre-Reshuffle Breach Rate (before July 1, 2025): {kpis['pre_reshuffle_rate']}% (Quarterly credits: ~Rs 37,000)
- Post-Reshuffle Breach Rate (after June 30, 2025 Indore night cut): {kpis['post_reshuffle_rate']}% (Quarterly credits: ~Rs 195,000 - Rs 215,000)
- Total SLA penalty store credits paid since reshuffle: Rs {kpis['post_reshuffle_credits_inr']:,.2f}
- Core Root Cause: Indore night shift was dissolved on June 29, 2025. Zero night shift agents exist since July 1, 2025.
- Chat is active 24x7 with a 15-minute SLA. Result: 100% of night-created chat tickets (1,034 of 1,034) breach before 06:00 AM.
- Helpdesk Reporting Attribution Flaw: The helpdesk attributes breaches to the resolving agent.
- 88.4% of breaches resolved by Morning shift agents were tickets created at night while the desk was closed.
- Morning shift in-shift breach rate is actually ~8.8% (normal and matches Day shift at ~8.0%).
- Double-Recovery Leakage: 95 orders received BOTH refund and replacement, leaking Rs {kpis['double_recovery_leakage_inr']:,.2f}.
- Headcount Status: Frozen until Q4 (no hiring allowed).
- Proposed Fix: Bot triage / SLA pause overnight + shift rebalancing + fix attribution metric.
- Financial Goal: Cut breach rate from 24.9% to 8.5%, saving Rs 168,000/qtr in SLA credits + Rs 64,000/qtr in transfers = Rs 232,000/quarter.

User Question: "{query}"
Provide a clear, decisive, operational response directly tailored to Vireo Audio's executive leadership.
"""
        if self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_context,
                )
                return {
                    'source': 'gemini-2.5-flash',
                    'answer': response.text,
                    'timestamp': str(data_store.tickets['created_at_ist'].max())
                }
            except Exception as e:
                # Fall back to heuristic engine
                pass

        # Expert Deterministic Heuristic Engine
        q_lower = query.lower()
        if any(w in q_lower for w in ['morning', 'blame', 'agent', 'who is breaching', 'roster', 'people']):
            answer = (
                "**Executive Finding: The Morning Shift is NOT at Fault.**\n\n"
                "Although standard helpdesk reports attribute **1,786 breaches** to Morning shift agents since July 2025, "
                "our forensic audit reveals that **88.4% (1,579 tickets)** were created during the unstaffed Night shift (22:00–06:00 IST).\n\n"
                "- When evaluated strictly on tickets created during Morning hours, their in-shift breach rate is **8.8%**, "
                "completely in line with Day shift (8.1%).\n"
                "- Pushing Neha's intended disciplinary conversation onto Rahul Sen, Krishna Kaur, or Farah Sheikh would penalize "
                "the very agents who clear the overnight backlog every morning and worsen the morale crisis Priya Raman flagged.\n"
                "- **Action**: Re-attribute breach metrics to creation-shift queue origin rather than resolving agent."
            )
        elif any(w in q_lower for w in ['finance', 'credit', 'p&l', 'arjun', 'cost', 'tripled', 'money']):
            answer = (
                "**Financial Explanation for Arjun Mehta (Controller):**\n\n"
                "The SLA store credit line roughly tripled from ~Rs 37,000/quarter (Q1–Q2 2025) to over **Rs 200,000/quarter** (Q3 2025–Q2 2026), "
                "totaling **Rs 7,80,150** paid out post-reshuffle.\n\n"
                "- **Root Driver**: The June 2025 Indore reshuffle cut 5 night agents. But Chat remained advertised as 24x7 with a 15-minute SLA. "
                "Without overnight agents, 100% of night chats breached automatically, issuing Rs 350 to each customer upon resolution.\n"
                "- **Leakage Bonus**: We also discovered **Rs 4.37 Lakhs in double-recovery leakage** (95 orders received both refund and replacement) "
                "and **Rs 3.44 Lakhs in internal transfer churn** (1,129 transfers @ Rs 305).\n"
                "- **Total Potential Savings**: **Rs 2.32 Lakhs per quarter** without increasing headcount."
            )
        elif any(w in q_lower for w in ['goal', 'target', 'business goal', 'number', 'solution', 'recommend']):
            answer = (
                "**Vireo Support Optimization Business Goal:**\n\n"
                "> *'Cut first-response SLA breach rate from 24.9% to 8.5% within 30 days, saving Rs 1,68,000 per quarter in automated store credits, "
                "and recover Rs 64,000 per quarter in avoidable transfer re-handling — delivering a total net recurring impact of Rs 2,32,000 per quarter "
                "(Rs 9.28 Lakhs annually), while lifting customer CSAT by +0.35 points and restoring Morning shift retention without hiring additional headcount.'*\n\n"
                "**Implementation Pillars**:\n"
                "1. **Night Bot Deflection / Queue Pause**: Switch overnight chat to off-hours triage bot or pause the 15m timer until 06:00 IST.\n"
                "2. **Zero-Headcount Roster Tuning**: Stagger 2 Day shift chat agents into evening/night rotation.\n"
                "3. **Double-Recovery Blocker**: Implement an automated ERP validation gate preventing refund approval if a replacement RMA exists.\n"
                "4. **Metric Realignment**: Benchmark agents by handled in-shift response time rather than legacy resolving-agent attribution."
            )
        else:
            answer = (
                f"**Vireo Support Diagnostic Overview**:\n\n"
                f"- **Dataset Size**: {kpis['total_tickets']:,} deduplicated tickets (Jan 2025 – Jun 2026).\n"
                f"- **Current SLA Breach Rate**: {kpis['post_reshuffle_rate']}% (vs 9.3% historical baseline).\n"
                f"- **Financial Impact**: Rs {kpis['post_reshuffle_credits_inr']:,.2f} in SLA store credits paid out since July 2025.\n"
                f"- **Root Cause**: Unstaffed night queue (1,034 night chats @ 100% breach rate) mapped to morning agents due to helpdesk attribution flaw.\n"
                f"- **Headcount Constraint**: Zero hiring required; cost-neutral operational and workflow configuration recovers Rs 2.32 Lakhs/quarter."
            )

        return {
            'source': 'vireo-expert-rules-engine',
            'answer': answer,
            'timestamp': str(data_store.tickets['created_at_ist'].max())
        }

    def generate_executive_memo(self) -> str:
        """Return the pre-compiled one-page executive memo for Neha Kulkarni."""
        memo_path = os.path.join(os.path.dirname(__file__), 'memo_to_neha.md')
        if os.path.exists(memo_path):
            with open(memo_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "Executive memo file pending generation."

# Singleton instance
ai_advisor = VireoAIAdvisor()
