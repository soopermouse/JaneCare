from uuid import uuid4
from fastapi import APIRouter, HTTPException, Depends
from ..auth import Principal, require_roles
from ..schemas import ReportRequest, SubmissionRequest
from ..store import CASES, REPORTS, event, now_iso
from ..government import get_adapter

router=APIRouter(prefix='/api/government',tags=['government-gateway'])

def check_jurisdiction(p,j):
    if p.role=='government' and j not in (p.jurisdictions or []): raise HTTPException(403,'Jurisdiction is outside this government account scope')

@router.post('/reports/prepare')
def prepare(body:ReportRequest,p:Principal=Depends(require_roles('government','professional','admin'))):
    check_jurisdiction(p,body.jurisdiction)
    report_id='GR-'+uuid4().hex[:8].upper()
    canonical={'report_id':report_id,'period':body.period,'case_count':len(CASES),'prepared_at':now_iso(),'standard':body.standard}
    adapter=get_adapter(body.jurisdiction,body.standard); payload=adapter.transform(canonical)
    REPORTS[report_id]={'id':report_id,'jurisdiction':body.jurisdiction,'standard':body.standard,'status':'prepared','payload':payload,'errors':[],'created_by':p.id}
    event('government_report',f'Prepared report {report_id}',{'jurisdiction':body.jurisdiction,'standard':body.standard,'principal_id':p.id})
    return REPORTS[report_id]

@router.post('/reports/{report_id}/validate')
def validate(report_id:str,p:Principal=Depends(require_roles('government','professional','admin'))):
    report=REPORTS.get(report_id)
    if not report: raise HTTPException(404,'Report not found')
    check_jurisdiction(p,report['jurisdiction'])
    adapter=get_adapter(report['jurisdiction'],report['standard']); errors=adapter.validate(report['payload'])
    report['errors']=errors; report['status']='invalid' if errors else 'validated'; return report

@router.post('/reports/{report_id}/submit')
def submit(report_id:str, body:SubmissionRequest,p:Principal=Depends(require_roles('government','admin'))):
    report=REPORTS.get(report_id)
    if not report: raise HTTPException(404,'Report not found')
    check_jurisdiction(p,report['jurisdiction'])
    if report['status']!='validated': raise HTTPException(409,'Report must be validated first')
    if not body.human_authorized: raise HTTPException(403,'Accountable human authorization is required')
    adapter=get_adapter(report['jurisdiction'],report['standard']); result=adapter.submit(report['payload'])
    report['status']='authorized_for_transport'; report['authorized_by']=p.id
    event('government_submission_authorized',f'Report {report_id} authorized',{'principal_id':p.id})
    return {'report':report,'transport':result}
