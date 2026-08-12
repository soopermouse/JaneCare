from fastapi import APIRouter, HTTPException, Depends
from ..auth import Principal, require_roles
from ..store import REFERRALS, event
from ..schemas import ProviderAction

router=APIRouter(prefix='/api/providers', tags=['provider-network'])

def visible(p):
    if p.role in ('admin','professional'): return REFERRALS
    return [r for r in REFERRALS if r['provider']==p.provider_org]

@router.get('/dashboard')
def dashboard(p:Principal=Depends(require_roles('provider','professional','admin'))):
    refs=visible(p)
    return {'counts':{'new':sum(r['status']=='new' for r in refs),'active':sum(r['status']=='active' for r in refs),
      'information_requested':sum(r['status']=='awaiting_information' for r in refs),'overdue':0},'referrals':refs}

def change(referral_id,status,note,p):
    r=next((x for x in visible(p) if x['id']==referral_id),None)
    if not r: raise HTTPException(404,'Referral not found or not assigned to this provider')
    r['status']=status
    event('provider_update',f'{referral_id} changed to {status}',{'note':note,'principal_id':p.id,'provider':p.provider_org})
    return r

@router.post('/referrals/{referral_id}/accept')
def accept(referral_id:str, body:ProviderAction,p:Principal=Depends(require_roles('provider','professional','admin'))): return change(referral_id,'active',body.note,p)
@router.post('/referrals/{referral_id}/request-information')
def request_info(referral_id:str, body:ProviderAction,p:Principal=Depends(require_roles('provider','professional','admin'))): return change(referral_id,'awaiting_information',body.note,p)
@router.post('/referrals/{referral_id}/complete')
def complete(referral_id:str, body:ProviderAction,p:Principal=Depends(require_roles('provider','professional','admin'))): return change(referral_id,'completed',body.note,p)
