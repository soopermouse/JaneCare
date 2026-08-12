from fastapi import APIRouter, Depends, HTTPException
from ..auth import Principal, require_roles
from ..store import CASES, REFERRALS

router=APIRouter(prefix='/api/client',tags=['client-portal'])

@router.get('/dashboard')
def dashboard(p:Principal=Depends(require_roles('client'))):
    case=next((c for c in CASES if c['id']==p.client_case_id),None)
    if not case: raise HTTPException(404,'Case not found')
    referrals=[{'id':r['id'],'service':r['service'],'status':r['status'],'due':r['due']} for r in REFERRALS if r['case_id']==case['id']]
    safe_case={k:case[k] for k in ('id','need','priority','status','next_action')}
    return {'case':safe_case,'services':referrals,'message':'JaneCare shows only information authorized for this client account.'}
