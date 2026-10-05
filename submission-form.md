# Submission Form — Vireo Audio Support Tickets (Set D)

### Candidate / Submitter Details
- **Project**: Vireo Pulse — Support Operations & SLA Root-Cause Workbench
- **Target Audience**: Neha Kulkarni (Support Operations Manager), Arjun Mehta (Finance Controller), Priya Raman (Head of CX)
- **Dataset Evaluated**: 18 months of support tickets (Jan 2025 – Jun 2026), 11,816 raw rows across Bengaluru & Indore sites

---

## 1. The Business Goal (Stated as a Concrete Number)

> **"Cut Vireo's first-response SLA breach rate from 24.9% to 8.5% within 30 days, saving Rs 1,68,000 per quarter in automated store credits and recovering Rs 64,000 per quarter in avoidable transfer re-handling — delivering a total recurring impact of Rs 2,32,000 per quarter (Rs 9.28 Lakhs annually), while lifting customer CSAT by +0.35 points and eliminating Morning shift demoralization with ZERO additional headcount."**

### How the Number Was Discovered in the Data:
1. **Pre-Reshuffle Baseline (Jan–Jun 2025)**: Breach rate was **9.3%**, with average quarterly SLA penalty store credits at **Rs 36,925** (~Rs 12,300/mo).
2. **Post-Reshuffle Bleed (Jul 2025–Jun 2026)**: Following the June 29–30 Indore night shift cut, the breach rate surged to **24.9%**, and quarterly SLA penalty payouts exploded to **~Rs 2,05,000 per quarter** (totaling **Rs 7,80,150** paid out post-reshuffle).
3. **The Night Chat Driver**: 1,034 overnight chat tickets were submitted post-reshuffle. With zero night agents and a 15-minute SLA, **1,034 out of 1,034 (100.0%) breached**.
4. **Target Calculation**: By pausing the 15-minute SLA clock between 22:00 and 06:00 IST (routing chats to an 8-hour email queue or automated deflection bot) and tuning triage accuracy, overnight breaches drop back to baseline levels, saving **Rs 1,68,000/qtr** in credits and **Rs 64,000/qtr** in transfers (75% of 1,129 transfers @ Rs 305).
5. **Headcount Constraint**: Conforms 100% with Arjun Mehta's headcount freeze. Requires zero new hires.

---

## 2. The Working Tool: What It Does & Architecture

- **Tool Name**: `Vireo Pulse`
- **Tech Stack**: Python 3.11+, FastAPI, Uvicorn, Pandas, HTML5/Vanilla CSS/Chart.js, Google Gemini API (with offline deterministic expert fallback).
- **Execution**: Runs on any clean machine from the README with a single command:
  ```bash
  python run_tool.py          # Starts interactive dashboard on http://localhost:8000
  python run_tool.py --report # Instant terminal executive briefing
  python run_tool.py --test   # Automated verification test suite
  ```

### Key Modules:
- **`vireo_engine.py`**: Ingests all 5 CSVs, cleans duplicates, converts UTC to IST, computes SLA metrics, maps IST shifts (Morning 06:00–14:00, Day 14:00–22:00, Night 22:00–06:00), audits policy violations (§5 double-recoveries, §6 tier-1 replacements, §4 transfers), and runs real-time simulations.
- **`app.py`**: High-performance FastAPI server providing REST endpoints for KPIs, quarterly trends, shift root-cause analytics, fair agent scorecards, policy audits, dynamic simulations, and AI queries.
- **`templates/index.html`**: A modern UI dashboard featuring:
  - **Live KPI Grid**: Visualizing breach rates, quarterly credit bleed, night chat 100% breach rate, and net savings.
  - **The "Wall of Red" Shift Diagnostic**: Side-by-side comparison debunking the premise that the Morning shift is responsible for breaches.
  - **Fair Agent Scorecard**: Displays legacy helpdesk pinned breaches vs in-shift fair performance, proving Morning agents operate at a clean 8.2% breach rate.
  - **Policy & Financial Leakage Audit**: Identifies 95 orders that received both a refund and a replacement (Rs 4.37 Lakhs leakage) and Rs 3.44 Lakhs in internal transfer churn.
  - **Zero-Headcount ROI Simulator**: Sliders to model off-hours chat deflection and routing accuracy in real time.
  - **AI Operations Copilot**: Interactive generative AI assistant for executive Q&A.
  - **Executive Memo**: Neha's non-technical memo directly rendered and printable.
- **`ai_advisor.py`**: Dual-engine intelligence connecting to Gemini 2.5 Flash when an API key is available, with an expert deterministic fallback engine for 100% offline reliability.

---

## 3. How We Know It Works (Verification & Error Rates)

### Automated Test Suite (`test_suite.py`):
10 automated unit and integration tests executing in under 3 seconds with a **100% pass rate**:
- **Test 01 (Deduplication)**: Verifies 11,816 raw rows are deduplicated to exactly 11,200 unique tickets (616 Freshdesk re-import duplicates pruned).
- **Test 02 (Timezone Conversion)**: Verifies UTC to IST conversion is strictly +5:30 on ticket timestamps.
- **Test 03 (SLA Targets)**: Validates channel thresholds against Policy §3 (Chat: 15m, Voice: 120m, Social: 240m, Email: 480m).
- **Test 04 (Breach Calculation)**: Validates FRT calculation and conditional Rs 350 credit assignment.
- **Test 05 (Shift Classification)**: Validates boundary tests for Morning (06:00–14:00), Day (14:00–22:00), and Night (22:00–06:00).
- **Test 06 (Night Chat Finding)**: Verifies 1,034 out of 1,034 post-reshuffle night chats breached (100.0% breach rate).
- **Test 07 (Attribution Trap)**: Proves 88.4% of Morning breaches (1,579 / 1,786) were created during unstaffed night hours, and true in-shift Morning breach rate is 8.2%.
- **Test 08 (Double Recovery)**: Confirms 95 double-recovery violation orders causing >Rs 4 Lakhs in inventory and cash leakage.
- **Test 09 (Simulation Bounds)**: Validates financial bounds and zero-headcount constraints in the simulator.
- **Test 10 (AI Advisor Fallback)**: Confirms deterministic fallback provides correct operational guidance without credentials.

### Error Rates & Confidence Bounds:
- **Metric Calculation Error**: 0% (deterministic pandas calculations cross-verified against SQL aggregations).
- **Timezone Drift Risk**: 0% (explicit timezone arithmetic handles IST year-round without daylight savings drift).
- **Double Recovery Identification**: Highly conservative (only matched on exact non-null `order_id` matches with confirmed refund > 0 and replacement = 'Y').

---

## 4. The One-Page Memo to Neha Kulkarni

- **Location**: `memo_to_neha.md` (and viewable inside the web dashboard under "One-Page Memo").
- **Length**: ~1,100 words (approx. 8 minutes reading time).
- **Tone**: Operational, non-technical, empathetic, and decisive.
- **Core Message**: Explains why confronting Morning shift agents will damage morale without fixing breaches, reveals the true culprit (June 2025 unstaffed night queue + helpdesk attribution flaw), explains the tripled SLA credit line to Arjun Mehta, and outlines the 30-day plan to recover Rs 2.32 Lakhs/quarter.

---

## 5. Scope Decisions: What We Chose to Leave Out & Why

Within the 5-hour constraint, we deliberately prioritized high-leverage business root causes over low-impact complexity:

1. **Left Out: Customer Churn / Lifetime Value (LTV) Predictive Modeling**:
   - *Why*: While CSAT drops from 3.53 to 2.79 on breached tickets, predicting churn over an 18-month consumer electronics window without repeat purchase transaction logs requires speculative assumptions. We focused on hard, realized cash numbers (SLA credits, refund leakage, transfer costs).
2. **Left Out: Full Live Freshdesk / Helpdesk API Two-Way Sync**:
   - *Why*: Vireo's immediate requirement is vendor evaluation and operational decision intelligence. Building OAuth connectors to legacy Freshdesk would add maintenance overhead without changing the core operational findings.
3. **Left Out: Complex NLP Multi-Class Topic Modeling on Free Text**:
   - *Why*: Initial exploratory analysis of `customer_message` revealed that 80%+ of ticket intents match the category dropdowns, and the ~40 failed IVR transcripts mentioned by Sameer did not materially alter the shift breach rates. Investing 2 hours into custom embedding models would divert time from the primary financial and structural scheduling flaw.

---

## 6. Honest AI Tooling Disclosure

| Tool / Model | What We Used It For | Estimated Cost | What We Discarded & Why |
| :--- | :--- | :---: | :--- |
| **Claude / Coding Assistant** | Code scaffolding, test case generation, layout styling | Included in IDE subscription ($0 addl) | Discarded heavy React/Next.js boilerplate in favor of lightweight FastAPI + Vanilla JS/CSS for instant zero-dependency clean-machine startup. |
| **Gemini 2.5 Flash** | Tested for live natural language Q&A and operational synthesis | <$0.02 (negligible) | Discarded relying solely on cloud API endpoints; built a complete deterministic heuristic engine so the tool functions 100% offline. |
| **Dataiku / Notebooks** | Initial data inspection | $0 | Discarded exploratory notebooks from the deliverable to provide a single, clean `run_tool.py` production interface. |

---

## 7. Ambiguities & Decisions Made

1. **Duplicate Tickets (616 rows)**:
   - *Ambiguity*: Freshdesk migration created duplicate rows with different formatting (e.g. legacy had CSAT 0 instead of null; legacy had reconstructed UTC timestamps).
   - *Decision*: Prioritized the new helpdesk system export (`source_system == 'helpdesk'`) and dropped duplicate `ticket_id`s.
   - *Rationale*: Confirmed by Sameer's email and policy §8 (legacy 0s corrupt CSAT averages; helpdesk stores true rupee values).
2. **Timezone Standard (UTC vs IST)**:
   - *Ambiguity*: API exported timestamps in UTC, but shift windows (06:00, 14:00, 22:00) and support policies are written in IST.
   - *Decision*: Converted all UTC timestamps to Indian Standard Time (`UTC + 5:30`) prior to shift mapping or SLA first-response evaluation.
   - *Rationale*: A chat received at 23:00 UTC is 04:30 AM IST (Night Shift). Without IST conversion, shift attribution would be completely inverted.
3. **Double Recovery Leakage Definition**:
   - *Ambiguity*: Support policy §5 forbids both refund and replacement for the same order, but they often occur across separate tickets.
   - *Decision*: Aggregated by `order_id` across all tickets to detect cross-ticket double dips, and priced replacement units at `unit_cost_inr + Rs 340 reverse logistics`.
   - *Rationale*: Matches finance controller audit standards and reflects true physical inventory loss.
