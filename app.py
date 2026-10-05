"""
Vireo Pulse - Web Application Backend (FastAPI)
Serves REST API endpoints for KPI analytics, shift diagnostics, fair agent scorecards,
policy audits, scenario simulations, and AI advisor intelligence.
"""

import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from vireo_engine import data_store
from ai_advisor import ai_advisor

app = FastAPI(
    title="Vireo Pulse - Support Operations Intelligence Workbench",
    description="Operational diagnostics, fair SLA attribution, and financial leakage prevention for Vireo Audio",
    version="1.0.0"
)

# Request Models
class AskAIRequest(BaseModel):
    query: str
    api_key: Optional[str] = None

class SimulationRequest(BaseModel):
    night_chat_policy: str = 'deflect_or_pause'
    intake_routing_accuracy_pct: float = 80.0

@app.get("/api/kpis")
def get_kpis():
    """Retrieve high-level operational KPIs."""
    return data_store.get_summary_kpis()

@app.get("/api/quarterly-trend")
def get_quarterly_trend():
    """Retrieve quarterly trend data for charts."""
    return data_store.get_quarterly_trend()

@app.get("/api/shift-root-cause")
def get_shift_root_cause():
    """Retrieve the comparative breakdown of creation shift vs resolving shift."""
    return data_store.get_shift_root_cause_analysis()

@app.get("/api/agent-scorecard")
def get_agent_scorecard():
    """Retrieve the fair agent scorecard comparing helpdesk pinned vs in-shift metrics."""
    return data_store.get_agent_scorecard()

@app.get("/api/policy-audit")
def get_policy_audit():
    """Retrieve policy violations: double recoveries, tier-1 replacements, transfer costs."""
    double_recovery = data_store.get_double_recovery_audit()
    transfers_total = int(data_store.tickets['transfers'].sum()) if 'transfers' in data_store.tickets else 1129
    transfer_cost = transfers_total * 305.0

    # Tier 1 replacements
    repl_tickets = data_store.tickets[data_store.tickets['replacement_issued'] == 'Y']
    tier1_replacements = int((repl_tickets['tier'] == 1).sum())
    tier2_replacements = int((repl_tickets['tier'] == 2).sum())

    return {
        'double_recovery': double_recovery,
        'transfers': {
            'total_transfers': transfers_total,
            'cost_inr': transfer_cost,
            'cost_per_transfer_inr': 305.0
        },
        'replacements_audit': {
            'total_replacements': len(repl_tickets),
            'tier1_approved_count': tier1_replacements,
            'tier2_approved_count': tier2_replacements,
            'tier1_violation_rate_pct': round((tier1_replacements / len(repl_tickets)) * 100, 1) if len(repl_tickets) > 0 else 0
        }
    }

@app.post("/api/simulate")
def simulate(req: SimulationRequest):
    """Run interactive simulation modeling SLA breach and financial recovery."""
    impact = data_store.simulate_solution_impact(
        night_chat_policy=req.night_chat_policy,
        intake_routing_accuracy_pct=req.intake_routing_accuracy_pct
    )
    # Ensure all float values are standard Python floats for JSON response
    return {k: (float(v) if hasattr(v, '__float__') and not isinstance(v, (int, bool)) else v) for k, v in impact.items()}

@app.post("/api/ai/query")
def ai_query(req: AskAIRequest):
    """Query the AI Operations Advisor."""
    if req.api_key:
        ai_advisor.api_key = req.api_key
        ai_advisor._init_gemini()
    response = ai_advisor.ask(req.query)
    return response

@app.get("/api/memo")
def get_memo():
    """Return the raw markdown of the executive memo to Neha Kulkarni."""
    memo_path = os.path.join(os.path.dirname(__file__), 'memo_to_neha.md')
    if os.path.exists(memo_path):
        with open(memo_path, 'r', encoding='utf-8') as f:
            return {"memo": f.read()}
    return {"memo": "Memo file not found."}

@app.get("/api/tickets/sample")
def get_sample_tickets(
    shift: Optional[str] = None,
    channel: Optional[str] = None,
    breached: Optional[bool] = None,
    limit: int = 15
):
    """Inspect underlying ticket records with customer messages and agent notes."""
    df = data_store.tickets
    if shift:
        df = df[df['creation_shift'] == shift]
    if channel:
        df = df[df['channel'] == channel]
    if breached is not None:
        df = df[df['is_breached'] == breached]

    cols = [
        'ticket_id', 'created_at_ist', 'channel', 'category', 'creation_shift',
        'response_shift', 'frt_minutes', 'sla_target_min', 'is_breached',
        'name', 'customer_message', 'agent_notes', 'refund_amount_inr', 'replacement_issued'
    ]
    sample = df[cols].head(limit).copy()
    sample['created_at_ist'] = sample['created_at_ist'].astype(str)
    return sample.to_dict(orient='records')

# Serve Single Page Dashboard UI
@app.get("/", response_class=HTMLResponse)
def index_page():
    index_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Vireo Pulse Workbench - Templates loading...</h1>"

if __name__ == "__main__":
    import uvicorn
    print("Launching Vireo Pulse Workbench on http://localhost:8000 ...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
