from datetime import datetime, timezone
from typing import Any

CASES = [
    {"id":"JC-1024","client":"Sarah M.","need":"Housing","priority":"high","status":"human_review","waiting_days":4,"owner":"M. de Vries","next_action":"Review housing escalation","human_review_required":True},
    {"id":"JC-1017","client":"David K.","need":"Benefits","priority":"medium","status":"waiting_provider","waiting_days":9,"owner":"A. Jansen","next_action":"Follow up with benefits adviser","human_review_required":False},
    {"id":"JC-1098","client":"Lina P.","need":"Support","priority":"normal","status":"active","waiting_days":1,"owner":"R. Smit","next_action":"Monitor scheduled appointment","human_review_required":False},
    {"id":"JC-1103","client":"Eva T.","need":"Transport","priority":"medium","status":"waiting_provider","waiting_days":5,"owner":"A. Jansen","next_action":"Confirm mobility transport referral","human_review_required":False},
]

REFERRALS = [
    {"id":"RF-3001","case_id":"JC-1017","provider":"Benefits Advice Tilburg","service":"Benefits assessment","status":"new","due":"2026-08-15"},
    {"id":"RF-3002","case_id":"JC-1103","provider":"Mobility Service","service":"Accessible transport","status":"new","due":"2026-08-16"},
    {"id":"RF-2994","case_id":"JC-1024","provider":"Housing Support","service":"Emergency housing review","status":"awaiting_information","due":"2026-08-13"},
]

EVENTS = []
REPORTS: dict[str, dict[str, Any]] = {}

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def event(kind: str, message: str, payload: dict | None = None):
    item={"time":now_iso(),"type":kind,"message":message,"payload":payload or {}}
    EVENTS.insert(0,item)
    del EVENTS[100:]
    return item
