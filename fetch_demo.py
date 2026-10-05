import urllib.request
import json

base_url = 'http://127.0.0.1:8000'

def fetch(path):
    req = urllib.request.urlopen(base_url + path)
    return json.loads(req.read().decode('utf-8'))

print("=" * 70)
print("1. /api/kpis — Operational Overview")
print("=" * 70)
print(json.dumps(fetch('/api/kpis'), indent=2))

print("\n" + "=" * 70)
print("2. /api/shift-root-cause — The 'Wall of Red' Forensic Audit")
print("=" * 70)
root = fetch('/api/shift-root-cause')
print("Morning Shift Audit:")
print(json.dumps(root['morning_shift_audit'], indent=2))
print("\nChat Overnight Audit:")
print(json.dumps(root['chat_overnight_audit'], indent=2))

print("\n" + "=" * 70)
print("3. /api/agent-scorecard — Fair Attribution vs Helpdesk Blame (Top 5)")
print("=" * 70)
scorecard = fetch('/api/agent-scorecard')
for a in scorecard[:5]:
    print(f"Agent: {a['name']} ({a['agent_id']}) | Shift: {a['shift']} | Team: {a['team']}")
    print(f"  • Helpdesk Pinned Breaches : {a['pinned_breaches']} ({a['pinned_breach_rate']}% breach rate)")
    print(f"  • Inherited Night Breaches : {a['inherited_night_breaches']}")
    print(f"  • True In-Shift Breaches   : {a['in_shift_breaches']} ({a['fair_in_shift_rate']}% fair rate)")
    print(f"  • Attribution Distortion   : -{a['distortion_gap_pct']}% unfair inflation\n")
