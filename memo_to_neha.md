# Executive Briefing & Operational Audit

**TO:** Neha Kulkarni, Support Operations Manager, Vireo Audio  
**FROM:** Vendor Evaluation & Support Operations Analytics Team  
**DATE:** September 2026  
**SUBJECT:** SLA Breach Diagnosis, True Root-Cause Analysis, and Action Plan  
**READING TIME:** ~8 minutes (Non-Technical Executive Memo)

---

### Executive Summary: Why Having "That Conversation" Will Harm Your Best Team

Neha, you asked for a weekly report identifying which agents and shifts are breaching first-response SLAs most frequently, so you could "have the conversation with the right people." 

We built that reporting tool for you, but before you hold those conversations, there is a critical operational discovery you must see:

**The Morning shift is not failing your SLA targets. The Morning shift is inheriting a queue of tickets that are already breached before they even clock in.**

If you confront agents like Rahul Sen, Krishna Kaur, or Farah Sheikh about their breach numbers, you will be reprimanding the very team members who rescue your queue every morning. More importantly, it will not prevent a single SLA breach tomorrow.

Here is what is actually happening, the financial bleed it is causing across Vireo's P&L, and the exact zero-headcount roadmap to recover **Rs 2,32,000 every quarter**.

---

### 1. The Anatomy of the "Wall of Red"

When Priya Raman noted that the morning team "opens the day to a wall of red," she identified the symptom of a structural breakdown that began on **June 30, 2025**.

#### A. The Night Shift Was Dissolved, But 24x7 Chat Stayed On
Prior to July 2025, Vireo maintained a dedicated night shift in Indore (5 agents across Chat and Email). On June 29–30, 2025, that shift was reallocated to day hours or exited. Since July 1, 2025, **zero agents have staffed the 22:00 to 06:00 IST night window**.

However, Vireo's website and app continued to offer **24x7 live chat** with a strict **15-minute first-response SLA**. 

#### B. 100% of Overnight Chats Automatically Breach
Customers naturally continued messaging throughout the night. Between 22:00 and 06:00 IST, every single chat ticket sits completely untouched for hours. 
- In the 12 months since the reshuffle, **1,034 overnight chat tickets** were created.
- **1,034 of them breached their 15-minute SLA (a 100.0% breach rate).**
- Overnight email and social media tickets experienced similar severe delays.

#### C. The Helpdesk Attribution Trap
Vireo’s helpdesk reporting does not track which shift *caused* a breach; it assigns the breach to whichever agent **resolves** the ticket. 

When your Morning agents clock in at 06:00 AM, they immediately begin answering the accumulated overnight backlog. Because they are the ones who reply and close the ticket, the helpdesk tags them with the breach.
- **88.4% of all breaches pinned on the Morning shift (1,579 out of 1,786 tickets) were created at night while the desk was closed.**
- On tickets actually submitted during Morning hours (06:00–14:00 IST), your Morning agents achieve an **8.8% breach rate**—virtually identical to the Day shift's **8.1%**.

Your Morning team is performing with discipline. They are simply taking the blame for an empty night queue.

---

### 2. The Financial Connection: Solving Arjun Mehta’s P&L Mystery

Arjun Mehta flagged that Vireo’s SLA credit line in the P&L has roughly tripled since last summer. He suspected a connection to the June reshuffle, even though it was considered payroll-neutral. He was right.

Under Vireo Support Policy §3, every ticket that breaches its first-response SLA automatically deposits a **Rs 350 store credit** into the customer's account.

| Time Period | Overall Breach Rate | Average Quarterly SLA Credits | Annualized Bleed |
| :--- | :---: | :---: | :---: |
| **Pre-Reshuffle (Jan – Jun 2025)** | **9.3%** | **Rs 36,925** | ~Rs 1.48 Lakhs |
| **Post-Reshuffle (Jul 2025 – Jun 2026)** | **24.9%** | **Rs 1,95,000 – Rs 2,14,900** | **~Rs 8.00 Lakhs** |
| **Net Operational Bleed** | **+15.6% jump** | **+Rs 1,68,000 / quarter** | **+Rs 6.52 Lakhs wasted** |

The June reshuffle looked cost-neutral on staffing spreadsheets, but it silently triggered **over Rs 6.5 Lakhs in unbudgeted cash credits** by allowing overnight tickets to breach unchecked.

#### Two Additional Leakages Uncovered in the Audit:
1. **Double-Recovery Violations (§5)**: We discovered **95 customer orders** that received **both a full refund and a replacement unit**, totaling **Rs 4,37,418 in duplicate inventory and cash loss**. In several cases, customers lodged an email and a chat for the same order, and separate frontline agents approved both without cross-referencing.
2. **Transfer Churn (§4)**: Inaccurate initial intake routing triggered **1,129 internal transfers**, costing **Rs 305 per re-handling**—burning an additional **Rs 3,44,345** in administrative overhead.

---

### 3. The Business Goal & 30-Day Zero-Headcount Action Plan

Arjun has made it clear that headcount is frozen until Q4. **You do not need to hire to fix this.** 

Here is our commitment, stated as a concrete business outcome:

> **"Cut Vireo's first-response SLA breach rate from 24.9% to 8.5% within 30 days, saving Rs 1,68,000 per quarter in automated store credits, and recover Rs 64,000 per quarter in avoidable transfer re-handling — delivering a total net recurring impact of Rs 2,32,000 per quarter (Rs 9.28 Lakhs annually), while lifting customer CSAT from 2.79 to 3.50+ on overnight tickets, with zero additional headcount."**

#### Immediate Action Steps (Next 14 Days):

1. **Fix the Overnight Chat SLA Trigger (Immediate — IT / Sameer Qureshi)**:
   - Between 22:00 and 06:00 IST, configure the web and app widget to state: *"Our live agents are offline until 06:00 AM IST. Leave a message, and we'll reply by email within 8 hours."*
   - Route overnight chat submissions into the Email queue (8-hour SLA) or pause the SLA clock until 06:00 AM. 
   - **Result**: Instantly eliminates 1,034 automated breaches per year and saves ~Rs 90,000 per quarter overnight.

2. **Rebalance Shifts Without New Hires (Operations / Neha Kulkarni)**:
   - Shift 2 of the 13 Chat agents currently scheduled on the Day shift to a staggered evening/night intake coverage (or a 04:00–12:00 early triage slot). 
   - This ensures overnight emails and high-priority voice callback requests are triaged before 06:00 AM, allowing the Morning shift to arrive to a clean queue.

3. **Switch Neha's Weekly Scorecard to "In-Shift Fair Metrics"**:
   - Change your helpdesk reporting logic from *Resolving Agent* to *Queue In-Shift Performance*.
   - Benchmark agents only on tickets that arrived during their active shift hours.
   - Share this data openly with the Morning team. Showing them that management recognizes their true performance will instantly stop team demoralization and turnover.

4. **Plug the Double-Recovery Drain (Finance & Tech / Arjun Mehta)**:
   - Implement an automated safeguard in the helpdesk: when an agent clicks "Issue Refund" or "Issue Replacement," the system must check whether the order already has an active return, refund, or replacement flag.
   - Enforce Team Lead approval for any second claim on the same order_id. This recovers over Rs 1.0 Lakh per quarter in duplicate leakages.

---

### Conclusion

Neha, the data proves your Morning shift is doing heroic work under unfair metrics. By fixing the overnight chat queue configuration, aligning your scorecard to true origin shifts, and locking down duplicate refund claims, you can walk into your next leadership meeting with Arjun and Priya not with bad news about agent performance, but with a **Rs 2.32 Lakh quarterly savings plan** that solves the SLA crisis permanently.

Our interactive workbench is ready for you to explore these numbers, simulate shift configurations, and track weekly progress. Let's review it together.
