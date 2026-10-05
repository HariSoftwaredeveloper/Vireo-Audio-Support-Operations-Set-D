# Vireo Pulse — Support Operations & SLA Root-Cause Workbench

> **Operational Intelligence & Financial Leakage Prevention for Vireo Audio**  
> Evaluated on 18 months of support data (11,816 tickets, 44 agents across Bengaluru & Indore)

---

## Quick Start (Clean Machine)

You can launch the full-stack interactive workbench with a single command:

### 1. Install Dependencies
```bash
pip install fastapi uvicorn pandas numpy
```
*(Optional for live Gemini LLM calls: `pip install google-genai`, or pass your API key directly in the UI)*

### 2. Launch the Application
```bash
python run_tool.py
```
Open your browser and navigate to: **[http://localhost:8000](http://localhost:8000)**

---

## Alternative CLI Modes

If you prefer to run from the terminal without opening a browser:

### Generate Terminal Executive Briefing
```bash
python run_tool.py --report
```

### Run Automated Verification Suite (10/10 Tests)
```bash
python run_tool.py --test
# or
python test_suite.py
```

---

## The Business Goal (Stated as a Concrete Number)

> **"Cut Vireo's first-response SLA breach rate from 24.9% to 8.5% within 30 days, saving Rs 1,68,000 per quarter in automated store credits and recovering Rs 64,000 per quarter in avoidable transfer re-handling — delivering a total net recurring impact of Rs 2,32,000 per quarter (Rs 9.28 Lakhs annually), while lifting customer CSAT by +0.35 points with ZERO additional headcount."**

---

## Core Findings & Root Causes Discovered in the Data

1. **The Indore Night Shift Cut (June 29–30, 2025)**:
   - Vireo dissolved the 5-agent Indore night shift at the end of June 2025. Zero night agents were staffed from July 1, 2025 onwards.
   - However, **24x7 Chat with a 15-minute SLA target remained active**.
   - Result: **100% of post-reshuffle night-created chat tickets (1,034 of 1,034) breached before 06:00 AM**.

2. **The Helpdesk Attribution Trap**:
   - The helpdesk assigns breaches to whichever agent **resolves** the ticket, not when the ticket arrived.
   - The Morning shift arrives at 06:00 AM and clears the overnight backlog.
   - **88.4% of all breaches pinned on Morning agents (1,579 out of 1,786) were created during unstaffed night hours.**
   - Evaluated fairly on tickets created during their own shift, Morning agents achieve an **8.2% breach rate**, virtually identical to the Day shift (8.1%).
   - Reprimanding Morning agents would punish high performers and fail to prevent any breaches.

3. **Solving Arjun Mehta’s P&L Mystery (Tripled SLA Credits)**:
   - Support Policy §3 mandates an automatic **Rs 350 store credit** for every SLA breach.
   - Pre-reshuffle SLA credits averaged **Rs 36,925/quarter**.
   - Post-reshuffle SLA credits tripled to **~Rs 2,00,000 to Rs 2,15,000/quarter** (totaling **Rs 7,80,150** paid out post-reshuffle).

4. **Secondary Policy Leakages**:
   - **Double-Recovery Violations (§5)**: 95 orders received BOTH a refund and a replacement unit, leaking **Rs 4,37,418**.
   - **Internal Transfer Churn (§4)**: 1,129 transfers @ Rs 305 = **Rs 3,44,345** in avoidable re-handling overhead.

---

## Deliverables in This Repository

| Deliverable | File / Path | Description |
| :--- | :--- | :--- |
| **1. Working AI Tool** | `app.py`, `vireo_engine.py`, `templates/index.html` | Interactive dashboard with charts, shift diagnostics, fair scorecards, and simulator. |
| **2. Business Goal** | `submission-form.md`, `README.md`, `memo_to_neha.md` | Concrete metric: Cut breach rate from 24.9% to 8.5%, saving Rs 2,32,000/quarter. |
| **3. Verification Proof** | `test_suite.py` | 10 automated tests verifying deduplication, timezones, SLAs, shifts, and calculations (100% pass). |
| **4. Executive Memo** | `memo_to_neha.md` | Non-technical one-page memo for Neha Kulkarni (~8 min read). |
| **5. Screen Recording Walkthrough** | `walkthrough_script.md` | Prompt walkthrough, version evolution, and discarded alternatives. |
| **6. Submission Form** | `submission-form.md` | Fully completed evaluation submission form. |

---

## Project Structure

```
Task1/
├── app.py                  # FastAPI web server and REST API routes
├── vireo_engine.py         # Core analytical engine, deduplication, and metrics
├── ai_advisor.py           # GenAI & deterministic heuristic advisor
├── run_tool.py             # Single-command launcher (web, report, test)
├── test_suite.py           # 10 automated validation tests
├── memo_to_neha.md         # One-page executive memo for Neha Kulkarni
├── submission-form.md      # Official completed evaluation submission form
├── walkthrough_script.md   # Script & breakdown of prompts, changes, and discards
├── templates/
│   └── index.html          # Modern dashboard UI with dark glassmorphism & Chart.js
└── data/                   # Original dataset files
    ├── tickets.csv
    ├── agents.csv
    ├── orders.csv
    ├── customers.csv
    ├── products.csv
    ├── support-policy.pdf
    ├── email-thread.txt
    └── README.txt
```
