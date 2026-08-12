from fastapi import APIRouter, HTTPException, Depends
from ..auth import Principal, require_roles
from ..store import CASES, EVENTS, event
from ..schemas import JaneRecommendationDecision

router=APIRouter(prefix='/api', tags=['professional-dashboard'])

def visible_cases(p):
    if p.role=='admin': return CASES
    allowed=set(p.case_ids or [])
    return [c for c in CASES if c['id'] in allowed or c.get('owner')==p.name]

@router.get('/dashboard/summary')
def summary(p:Principal=Depends(require_roles('professional','admin'))):
    items=visible_cases(p)
    urgent=sum(1 for c in items if c['priority']=='high')
    waiting=sum(1 for c in items if c['status'].startswith('waiting'))
    review=sum(1 for c in items if c['human_review_required'])
    return {'cases':len(items),'urgent':urgent,'needs_review':review,'waiting':waiting,'resolved':0,
        'attention':[{'severity':'high','text':f'{review} case(s) require accountable human review'},
                     {'severity':'medium','text':f'{waiting} case(s) are waiting on providers'},
                     {'severity':'normal','text':'Routine follow-ups can be coordinated by Jane'}],
        'activity':EVENTS[:8]}

@router.get('/cases')
def cases(p:Principal=Depends(require_roles('professional','admin'))): return visible_cases(p)

@router.get('/cases/{case_id}')
def case(case_id:str,p:Principal=Depends(require_roles('professional','admin'))):
    c=next((x for x in visible_cases(p) if x['id']==case_id),None)
    if c: return c
    raise HTTPException(404,'Case not found or not assigned to this account')

@router.post('/cases/{case_id}/recommendation')
def decide(case_id:str, body:JaneRecommendationDecision,p:Principal=Depends(require_roles('professional','admin'))):
    c=next((x for x in visible_cases(p) if x['id']==case_id),None)
    if not c: raise HTTPException(404,'Case not found or not assigned to this account')
    event('human_decision',f'Recommendation {body.decision} for {case_id}',{'case_id':case_id,'note':body.note,'principal_id':p.id})
    if body.decision=='approve': c['human_review_required']=False
    return {'ok':True,'case':c}
