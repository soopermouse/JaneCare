from ..store import CASES, REFERRALS, EVENTS, event

MANIFEST={
 "id":"janecare","name":"JaneCare","version":"0.1.0",
 "managed_by":"JaneOS",
 "capabilities":["cases.read","cases.coordinate","tasks.manage","referrals.manage","providers.coordinate","reports.prepare","reports.validate","alerts.emit","metrics.read","lifecycle.inspect"]
}

SAFE_COMMANDS={"follow_up_provider","prioritize_case","refresh_state","summarize_queue"}

class JaneCareAdapter:
    def manifest(self): return MANIFEST
    def health(self): return {"status":"healthy","components":{"api":"healthy","provider_network":"healthy","government_gateway":"healthy"}}
    def state(self): return {"cases":len(CASES),"waiting":sum(c['status'].startswith('waiting') for c in CASES),"provider_referrals":len(REFERRALS),"recent_events":EVENTS[:10]}
    def metrics(self): return {"case_count":len(CASES),"high_priority":sum(c['priority']=='high' for c in CASES),"waiting_provider":sum(c['status']=='waiting_provider' for c in CASES)}
    def command(self, command,args):
        if command not in SAFE_COMMANDS:
            return {"ok":False,"status":"blocked","reason":"Command is not in JaneCare permitted-management command set"}
        if command=='prioritize_case':
            cid=args.get('case_id'); c=next((x for x in CASES if x['id']==cid),None)
            if not c: return {"ok":False,"status":"not_found"}
            c['priority']=args.get('priority','high'); event('jane_command',f"Jane prioritized {cid}",args)
        elif command=='follow_up_provider':
            event('jane_command','Jane initiated provider follow-up',args)
        elif command=='summarize_queue':
            return {"ok":True,"summary":self.state()}
        return {"ok":True,"status":"accepted","command":command}
