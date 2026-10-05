import pandas as pd
import numpy as np

# Load datasets
raw_tickets = pd.read_csv('data/tickets.csv')
agents = pd.read_csv('data/agents.csv')
orders = pd.read_csv('data/orders.csv')
customers = pd.read_csv('data/customers.csv')
products = pd.read_csv('data/products.csv')

# Deduplicate tickets (helpdesk preferred)
tickets = raw_tickets.sort_values(by=['ticket_id', 'source_system'], ascending=[True, True]).drop_duplicates(subset='ticket_id', keep='first').copy()

# Date handling
tickets['created_at_utc'] = pd.to_datetime(tickets['created_at'])
tickets['first_response_at_utc'] = pd.to_datetime(tickets['first_response_at'])
tickets['resolved_at_utc'] = pd.to_datetime(tickets['resolved_at'])

tickets['created_at_ist'] = tickets['created_at_utc'] + pd.Timedelta(hours=5, minutes=30)
tickets['first_response_at_ist'] = tickets['first_response_at_utc'] + pd.Timedelta(hours=5, minutes=30)
tickets['resolved_at_ist'] = tickets['resolved_at_utc'] + pd.Timedelta(hours=5, minutes=30)

tickets['response_time_min'] = (tickets['first_response_at_utc'] - tickets['created_at_utc']).dt.total_seconds() / 60.0
targets = {'chat': 15, 'voice': 120, 'social': 240, 'email': 480}
tickets['target_min'] = tickets['channel'].map(targets)
tickets['is_breached'] = tickets['response_time_min'] > tickets['target_min']

def get_shift(dt):
    if pd.isna(dt): return 'Unknown'
    h = dt.hour
    if 6 <= h < 14: return 'Morning'
    elif 14 <= h < 22: return 'Day'
    else: return 'Night'

tickets['created_shift'] = tickets['created_at_ist'].apply(get_shift)
tickets['response_shift'] = tickets['first_response_at_ist'].apply(get_shift)
tickets['created_month'] = tickets['created_at_ist'].dt.to_period('M')

print("=== 1. DOUBLE RECOVERY ANOMALY ===")
# Policy 5: "In no case is a customer to receive both a refund and a replacement for the same order"
both = tickets[(tickets['refund_amount_inr'] > 0) & (tickets['replacement_issued'] == 'Y')]
print(f"Tickets with BOTH refund and replacement: {len(both)}")
if len(both) > 0:
    print(f"Total refund amount on double recovery: Rs {both['refund_amount_inr'].sum():,.2f}")
    # Merge with products to calculate replacement cost
    both_prod = both.merge(products, left_on='product_sku', right_on='sku', how='left')
    # Policy 5: "Replacement cost for planning: unit cost + Rs 340"
    repl_cost = both_prod['unit_cost_inr'].sum() + len(both) * 340
    print(f"Estimated replacement cost of double recovery: Rs {repl_cost:,.2f}")
    print(f"Total leakage from double recovery: Rs {both['refund_amount_inr'].sum() + repl_cost:,.2f}")

print("\n=== 2. CSAT SCORE TRENDS ===")
# Exclude 0 and null
valid_csat = tickets[tickets['csat_score'].isin([1, 2, 3, 4, 5])]
print("CSAT by month:")
print(valid_csat.groupby('created_month')['csat_score'].agg(['count', 'mean']).to_string())

print("\nCSAT by Breach Status:")
print(valid_csat.groupby('is_breached')['csat_score'].agg(['count', 'mean']).to_string())

print("\nCSAT by Created Shift:")
print(valid_csat.groupby('created_shift')['csat_score'].agg(['count', 'mean']).to_string())

print("\n=== 3. IVR FAILED TRANSCRIPTS ===")
failed_ivr = tickets[tickets['customer_message'].str.contains('failed|transcript|unintelligible|error|inaudible|disconnect', case=False, na=False)]
print(f"Messages with failed/error keywords: {len(failed_ivr)}")
print("Sample messages:")
for msg in failed_ivr['customer_message'].head(5):
    print(f" - {msg[:100]}")

print("\n=== 4. TRANSFERS AND RE-ROUTING ===")
# Policy 4: "Internal transfer between teams: Rs 305 per transfer"
if 'transfers' in tickets.columns:
    print(f"Total transfers in helpdesk: {tickets['transfers'].sum()}")
    print(f"Transfer cost: Rs {tickets['transfers'].sum() * 305:,.2f}")
    print("Transfers distribution:")
    print(tickets['transfers'].value_counts(dropna=False))

print("\n=== 5. WHO BREACHES? RESOLVING AGENT VS ACTUAL ROOT CAUSE ===")
# Helpdesk assigns breaches to resolving agent
morning_agents = tickets[tickets['response_shift'] == 'Morning']
agent_breaches = tickets.groupby('agent_id').agg(
    total_handled=('ticket_id', 'count'),
    breaches_pinned=('is_breached', 'sum'),
    breach_rate=('is_breached', 'mean'),
    night_created_handled=('created_shift', lambda s: (s=='Night').sum())
).reset_index()
agent_breaches = agent_breaches.merge(agents[['agent_id', 'name', 'team', 'shift', 'site']].drop_duplicates('agent_id'), on='agent_id', how='left')
print(agent_breaches.sort_values(by='breaches_pinned', ascending=False).head(10).to_string())
