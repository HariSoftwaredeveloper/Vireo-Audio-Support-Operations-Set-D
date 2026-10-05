# 3-Minute Screen Recording & Walkthrough Script
**Project**: Vireo Pulse — Support Operations & SLA Root-Cause Workbench  
**Format**: Under 3 minutes, screen recording / direct dashboard demonstration (No slides)

---

## Part 1: The Prompts Used & Analytical Journey (0:00 – 1:00)

### What We Asked the Data:
1. **Prompt 1: "Reconcile Helpdesk Export vs Policy Truths"**
   - *Query*: "Identify why raw ticket count (11,816) exceeds expected volume, convert UTC helpdesk timestamps to Indian Standard Time (IST +5:30), and classify tickets into Support Policy Section 7 shift windows (Morning 06:00–14:00, Day 14:00–22:00, Night 22:00–06:00)."
   - *Result*: Found 616 duplicate tickets from Freshdesk re-import. Established 11,200 unique tickets.
2. **Prompt 2: "Deconstruct the Post-June 2025 SLA Spike"**
   - *Query*: "Calculate first-response SLA breach rates month by month across all 4 channels (Chat 15m, Voice 120m, Social 240m, Email 480m) and correlate with agent roster assignment dates."
   - *Result*: Uncovered that all 5 Indore night shift agents exited or moved to day shift on June 29–30, 2025. Night shift became completely unstaffed, yet Chat remained active 24x7.
3. **Prompt 3: "Audit Resolving Agent Attribution vs Ticket Creation Queue"**
   - *Query*: "Compare the shift where breached tickets were resolved against the shift where tickets were originally created."
   - *Result*: The breakthrough finding: **88.4% of Morning shift breaches (1,579 / 1,786) were tickets generated during the unstaffed night shift**.

---

## Part 2: What We Changed Between Versions (1:00 – 2:00)

### Evolution from Version 1 to Final:
- **Version 1 (Naive Breach Table)**:
  - Initially built what Neha requested: a simple agent-by-shift breach table. 
  - *The Problem*: It showed Morning agents with massive red breach counts (e.g. Rahul Sen at 179 breaches). It looked like the Morning shift was failing.
- **Version 2 (The True Origin Attribution Pivot)**:
  - Realized that attributing breaches to the *resolving agent* is an artifact of the helpdesk software, not operational reality.
  - Re-architected the analytics engine to separate **Ticket Creation Shift** from **Resolving Shift**.
  - Normalized agent scorecards to evaluate performance exclusively on tickets created during their active shift hours. Morning shift's true breach rate dropped to **8.2%** (matching Day shift's 8.1%).
- **Version 3 (The Comprehensive Executive Workbench)**:
  - Added the **Zero-Headcount ROI Simulator** with live sliders to give Neha and Arjun an actionable path forward.
  - Integrated the **Policy Leakage Audits** (§5 double recovery detection and §4 transfer re-handling churn).
  - Built the **AI Operations Copilot** with dual-mode intelligence (Gemini LLM + deterministic offline expert engine).

---

## Part 3: What We Threw Away (2:00 – 3:00)

1. **Threw Away: The Standard Helpdesk Breach Report**:
   - We threw away the exact deliverable Neha asked for (a report blaming the Morning shift) because presenting it without the night-shift context would have triggered unfair disciplinary actions and deepened team demoralization.
2. **Threw Away: Heavy Client-Side Frameworks (React / Next.js)**:
   - Started with a standard React scaffold, but threw it out in favor of a clean, high-performance FastAPI + Vanilla JS/CSS architecture. This ensures the application runs with zero configuration on any clean machine directly from `python run_tool.py`.
3. **Threw Away: Speculative Lifetime Value (LTV) Churn Modeling**:
   - Initially explored training regression models on customer lifetime churn based on CSAT drop.
   - Threw it away because speculative LTV assumptions distract financial stakeholders like Arjun Mehta. Grounding the business case in **realized cash leakages** (Rs 350 per breach credit, Rs 305 per transfer, Rs 4.37 Lakhs in double-recovery goods) delivered an indisputable **Rs 2,32,000 / quarter** savings goal.

---

## Video Walkthrough Script (Presenter Verbal Flow)

> *"Hi Neha and Vireo leadership. When you asked for a weekly report of which agents and shifts are breaching first-response SLAs, our initial data pull showed exactly what you suspected: the Morning shift is resolving 1,786 breaches, appearing to be the primary offender.*
>
> *[Show Tab 1: Executive Trends]*  
> *Here in the quarterly trajectory, you can see breach rates jumped from 9.3% in early 2025 to 25.0% in Q3 2025, and SLA penalty store credits tripled from Rs 37,000 to over Rs 2 Lakhs per quarter. This directly answers Arjun Mehta's P&L question.*
>
> *[Show Tab 2: Shift Diagnostic]*  
> *Now look at this side-by-side diagnostic. On June 30, 2025, Vireo dissolved the Indore night shift. Zero agents were staffed between 22:00 and 06:00 IST. Yet 24x7 Chat with a 15-minute SLA stayed live. As a result, 100% of overnight chats breached before 06:00 AM.*
>
> *When your Morning team arrives at 06:00 AM, they open the day to a wall of red. Because your helpdesk attributes breaches to whoever closes the ticket, 88.4% of breaches blamed on the Morning team were tickets created hours before they clocked in! On tickets actually submitted during morning hours, their breach rate is an excellent 8.2%—matching the Day shift.*
>
> *[Show Tab 3: Fair Scorecard & Tab 4: Leakage]*  
> *Our Fair Scorecard restores morale by showing the true in-shift numbers for agents like Rahul Sen. In our policy audit, we also discovered 95 orders that received both a refund and a replacement unit—leaking Rs 4.37 Lakhs.*
>
> *[Show Tab 5: Simulator]*  
> *Finally, our business goal: by configuring your overnight chat widget to route to an 8-hour email queue or deflection bot, and optimizing intake routing, you can cut breach rates from 24.9% to 8.5%, saving Rs 2,32,000 per quarter with zero new hires.*
>
> *The entire workbench and executive memo are live and ready for your team. Thank you."*
